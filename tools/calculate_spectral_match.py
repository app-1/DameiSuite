import os, sys, math, json
import numpy as np
import soundfile as sf

REF_PATH = r"H:\REFERENCES\Split Chain - motionblur - 03 I'm Not Dying To Be Here.wav"
MIX_PATH = r"H:\HexGirls2\HexGyal\DemoMix\HexGyal.wav"
REF_STEMS_DIR = r"H:\STEMS FOLDER\SplitChain\I'm Not Dying To Be Here"

ref, sr = sf.read(REF_PATH, dtype='float32')
mix, _ = sf.read(MIX_PATH, dtype='float32')

if ref.ndim == 2:
    ref_m = np.mean(ref, axis=1)
else:
    ref_m = ref

if mix.ndim == 2:
    mix_m = np.mean(mix, axis=1)
else:
    mix_m = mix

fft_sz = 32768
hann = np.hanning(fft_sz)
freqs = np.fft.rfftfreq(fft_sz, 1.0 / sr)

def get_mean_spec(audio):
    n_chunks = len(audio) // fft_sz
    spec_acc = np.zeros(fft_sz // 2 + 1, dtype=np.float64)
    chunks_used = min(300, n_chunks)
    for c in range(chunks_used):
        chunk = audio[c * fft_sz : (c + 1) * fft_sz] * hann
        spec_acc += np.abs(np.fft.rfft(chunk))**2
    return spec_acc / max(1, chunks_used)

ref_spec = get_mean_spec(ref_m)
mix_spec = get_mean_spec(mix_m)

# Band definitions:
# Sub: 20-60 Hz
mask_sub = (freqs >= 20) & (freqs < 60)
# Boom / Mud: 80-200 Hz
mask_boom = (freqs >= 80) & (freqs < 200)
# Low-Mid Body: 250-800 Hz
mask_lomid = (freqs >= 250) & (freqs < 800)
# Presence: 2.5k-5k Hz
mask_pres = (freqs >= 2500) & (freqs < 5000)
# Brightness: 5k-16k Hz
mask_bright = (freqs >= 5000) & (freqs < 16000)

ref_tot = np.sum(ref_spec)
mix_tot = np.sum(mix_spec)

ref_sub_pct = np.sum(ref_spec[mask_sub]) / ref_tot * 100.0
ref_boom_pct = np.sum(ref_spec[mask_boom]) / ref_tot * 100.0
ref_bright_pct = np.sum(ref_spec[mask_bright]) / ref_tot * 100.0
ref_ratio = ref_boom_pct / max(1e-6, ref_sub_pct)

mix_sub_pct = np.sum(mix_spec[mask_sub]) / mix_tot * 100.0
mix_boom_pct = np.sum(mix_spec[mask_boom]) / mix_tot * 100.0
mix_bright_pct = np.sum(mix_spec[mask_bright]) / mix_tot * 100.0
mix_ratio = mix_boom_pct / max(1e-6, mix_sub_pct)

print("=== BOOMINESS & BRIGHTNESS ANALYSIS ===")
print(f"Reference Track (Split Chain):")
print(f"  Sub (20-60 Hz) Energy:        {ref_sub_pct:.2f}%")
print(f"  Boominess (80-200 Hz) Energy: {ref_boom_pct:.2f}%")
print(f"  Brightness (5-16 kHz) Energy: {ref_bright_pct:.2f}%")
print(f"  Boom-to-Sub Ratio:            {ref_ratio:.2f}x (Controlled low-end punch)")

print(f"\nHexGyal Mix:")
print(f"  Sub (20-60 Hz) Energy:        {mix_sub_pct:.2f}% (Deficit: {mix_sub_pct - ref_sub_pct:+.2f}%)")
print(f"  Boominess (80-200 Hz) Energy: {mix_boom_pct:.2f}% (Excess Mud: {mix_boom_pct - ref_boom_pct:+.2f}%)")
print(f"  Brightness (5-16 kHz) Energy: {mix_bright_pct:.2f}% (Deficit: {mix_bright_pct - ref_bright_pct:+.2f}%)")
print(f"  Boom-to-Sub Ratio:            {mix_ratio:.2f}x (Excess boominess masking mix!)")

# Frequencies of interest:
key_freqs = [25, 35, 50, 80, 100, 130, 160, 200, 250, 380, 800, 1500, 2500, 3800, 5000, 7500, 10000, 12500, 16000]
eq_targets = {}
print("\n=== EQ TARGET CURVE (Ref vs Mix) ===")
for kf in key_freqs:
    idx = np.argmin(np.abs(freqs - kf))
    w = max(1, int(idx * 0.08))
    r_val = np.mean(ref_spec[max(0, idx-w) : min(len(freqs), idx+w+1)]) / ref_tot
    m_val = np.mean(mix_spec[max(0, idx-w) : min(len(freqs), idx+w+1)]) / mix_tot
    diff_db = round(float(10 * np.log10(r_val / (m_val + 1e-12))), 2)
    eq_targets[kf] = diff_db
    print(f"  {kf:5d} Hz: {diff_db:+.2f} dB")

# Also analyze the reference stems levels:
stems_analysis = {}
if os.path.exists(REF_STEMS_DIR):
    for f in os.listdir(REF_STEMS_DIR):
        if f.endswith('.wav'):
            s_name = f.split('_(')[-1].replace(').wav', '') if '_(' in f else f
            s_data, _ = sf.read(os.path.join(REF_STEMS_DIR, f), dtype='float32')
            if s_data.ndim == 2:
                s_rms = np.sqrt(0.5 * (np.mean(s_data[:, 0]**2) + np.mean(s_data[:, 1]**2)))
                s_peak = max(np.max(np.abs(s_data[:, 0])), np.max(np.abs(s_data[:, 1])))
            else:
                s_rms = np.sqrt(np.mean(s_data**2))
                s_peak = np.max(np.abs(s_data))
            
            s_rms_db = 20 * math.log10(s_rms + 1e-9)
            s_peak_db = 20 * math.log10(s_peak + 1e-9)
            s_lufs = s_rms_db - 0.69
            stems_analysis[s_name] = {
                'lufs': round(s_lufs, 2),
                'peak_db': round(s_peak_db, 2),
                'rms_db': round(s_rms_db, 2)
            }

print("\n=== REFERENCE STEM LEVEL BALANCE ===")
for s_name, s_met in sorted(stems_analysis.items()):
    print(f"  {s_name:10s} -> LUFS: {s_met['lufs']:6.2f} dB | Peak: {s_met['peak_db']:6.2f} dB")

result = {
    'boom_sub_analysis': {
        'ref_sub_pct': round(ref_sub_pct, 2),
        'ref_boom_pct': round(ref_boom_pct, 2),
        'ref_ratio': round(ref_ratio, 2),
        'mix_sub_pct': round(mix_sub_pct, 2),
        'mix_boom_pct': round(mix_boom_pct, 2),
        'mix_ratio': round(mix_ratio, 2),
        'boom_delta_pct': round(mix_boom_pct - ref_boom_pct, 2),
        'brightness_delta_pct': round(mix_bright_pct - ref_bright_pct, 2)
    },
    'eq_target_curve': eq_targets,
    'reference_stems_balance': stems_analysis
}

with open(r"C:\Dev\DameiSuite\tools\spectral_match_data.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print("\nSaved spectral match data to C:\\Dev\\DameiSuite\\tools\\spectral_match_data.json")
