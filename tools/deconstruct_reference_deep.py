import os, sys, math, json
import numpy as np
import soundfile as sf

REF_PATH = r"H:\REFERENCES\Split Chain - motionblur - 03 I'm Not Dying To Be Here.wav"
MIX_PATH = r"H:\HexGirls2\HexGyal\DemoMix\HexGyal.wav"
REF_STEMS_DIR = r"H:\STEMS FOLDER\SplitChain\I'm Not Dying To Be Here"

def load_wav(path):
    data, sr = sf.read(path, dtype='float32')
    if data.ndim == 2:
        left = data[:, 0]
        right = data[:, 1]
    else:
        left = data
        right = data
    return left, right, sr

def band_energies(left, right, sr):
    mid = 0.5 * (left + right)
    side = 0.5 * (left - right)
    
    # 7-band FFT filter simulation
    # Sub: 20-60, Low: 60-250, Low-Mid: 250-800, Mid: 800-2.5k, High-Mid: 2.5k-6k, High: 6k-10k, Air: 10k-20k
    n = len(mid)
    # Use 32768 FFT chunking for speed and precision
    chunk = 32768
    num_chunks = min(300, n // chunk)
    
    bands = [
        (20, 60),
        (60, 250),
        (250, 800),
        (800, 2500),
        (2500, 6000),
        (6000, 10000),
        (10000, 20000)
    ]
    
    band_m_energy = np.zeros(7)
    band_s_energy = np.zeros(7)
    
    freqs = np.fft.rfftfreq(chunk, 1.0 / sr)
    hann = np.hanning(chunk)
    
    for c in range(num_chunks):
        idx = c * chunk
        m_c = mid[idx : idx + chunk] * hann
        s_c = side[idx : idx + chunk] * hann
        
        m_fft = np.abs(np.fft.rfft(m_c))**2
        s_fft = np.abs(np.fft.rfft(s_c))**2
        
        for bi, (f_lo, f_hi) in enumerate(bands):
            mask = (freqs >= f_lo) & (freqs < f_hi)
            band_m_energy[bi] += np.sum(m_fft[mask])
            band_s_energy[bi] += np.sum(s_fft[mask])
    
    total_energy = np.sum(band_m_energy) + 1e-12
    band_pct = (band_m_energy / total_energy) * 100.0
    band_widths = np.sqrt(band_s_energy / (band_m_energy + 1e-12))
    
    return band_pct.tolist(), band_widths.tolist()

def analyze_track_full(path):
    left, right, sr = load_wav(path)
    dur = len(left) / sr
    
    peak_l = np.max(np.abs(left))
    peak_r = np.max(np.abs(right))
    peak = max(peak_l, peak_r)
    
    rms_l = np.sqrt(np.mean(left**2))
    rms_r = np.sqrt(np.mean(right**2))
    rms = np.sqrt(0.5 * (rms_l**2 + rms_r**2))
    
    mid = 0.5 * (left + right)
    side = 0.5 * (left - right)
    m_rms = np.sqrt(np.mean(mid**2))
    s_rms = np.sqrt(np.mean(side**2))
    width = s_rms / (m_rms + 1e-9)
    corr = np.corrcoef(left, right)[0, 1]
    
    peak_db = 20 * math.log10(peak + 1e-9)
    rms_db = 20 * math.log10(rms + 1e-9)
    crest = peak_db - rms_db
    # Approximated LUFS-I
    lufs = rms_db - 0.69
    plr = peak_db - lufs
    
    pcts, widths = band_energies(left, right, sr)
    
    # Analyze sections: segment into 4-bar chunks (assume ~150-160 bpm)
    # Find high-energy chorus vs low-energy verse
    sec_len = int(sr * 4.0) # 4-second blocks
    num_secs = len(left) // sec_len
    sec_rms = []
    sec_widths = []
    for s in range(num_secs):
        idx = s * sec_len
        l_s = left[idx : idx + sec_len]
        r_s = right[idx : idx + sec_len]
        r_val = np.sqrt(0.5 * (np.mean(l_s**2) + np.mean(r_s**2)))
        m_s = 0.5 * (l_s + r_s)
        s_s = 0.5 * (l_s - r_s)
        w_val = np.sqrt(np.mean(s_s**2)) / (np.sqrt(np.mean(m_s**2)) + 1e-9)
        sec_rms.append(20 * math.log10(r_val + 1e-9))
        sec_widths.append(w_val)
    
    max_sec_rms = max(sec_rms) if sec_rms else rms_db
    min_sec_rms = min([x for x in sec_rms if x > -50] or [rms_db])
    dynamic_spread = max_sec_rms - min_sec_rms
    chorus_width = np.mean([w for i, w in enumerate(sec_widths) if sec_rms[i] > max_sec_rms - 3.0]) if sec_rms else width
    verse_width = np.mean([w for i, w in enumerate(sec_widths) if sec_rms[i] < max_sec_rms - 6.0 and sec_rms[i] > -50]) if sec_rms else width
    
    return {
        'path': path,
        'duration_sec': round(dur, 2),
        'lufs_integrated': round(lufs, 2),
        'peak_dbfs': round(peak_db, 2),
        'plr': round(plr, 2),
        'crest_db': round(crest, 2),
        'overall_width': round(width, 3),
        'inter_channel_corr': round(corr, 3),
        'band_pct_energy': [round(x, 2) for x in pcts],
        'band_widths': [round(x, 3) for x in widths],
        'chorus_rms_db': round(max_sec_rms, 2),
        'verse_rms_db': round(min_sec_rms, 2),
        'macro_dynamic_spread_db': round(dynamic_spread, 2),
        'chorus_width': round(chorus_width, 3),
        'verse_width': round(verse_width, 3),
        'width_expansion_chorus_pct': round((chorus_width / (verse_width + 1e-9) - 1.0) * 100, 1)
    }

print("Running deep deconstruction on Split Chain Reference...")
ref_analysis = analyze_track_full(REF_PATH)
print("Running deep deconstruction on HexGyal Mix...")
mix_analysis = analyze_track_full(MIX_PATH)

# Check stems in Split Chain folder
stem_data = {}
if os.path.exists(REF_STEMS_DIR):
    for f in os.listdir(REF_STEMS_DIR):
        if f.endswith('.wav'):
            stem_name = f.split('_(')[-1].replace(').wav', '') if '_(' in f else f
            stem_path = os.path.join(REF_STEMS_DIR, f)
            print(f"Analyzing reference stem: {stem_name}...")
            stem_data[stem_name] = analyze_track_full(stem_path)

output = {
    'reference': ref_analysis,
    'mix': mix_analysis,
    'reference_stems': stem_data,
    'comparison': {
        'lufs_delta': round(mix_analysis['lufs_integrated'] - ref_analysis['lufs_integrated'], 2),
        'plr_delta': round(mix_analysis['plr'] - ref_analysis['plr'], 2),
        'crest_delta': round(mix_analysis['crest_db'] - ref_analysis['crest_db'], 2),
        'width_delta': round(mix_analysis['overall_width'] - ref_analysis['overall_width'], 3),
        'corr_delta': round(mix_analysis['inter_channel_corr'] - ref_analysis['inter_channel_corr'], 3),
        'band_energy_delta': [round(m - r, 2) for m, r in zip(mix_analysis['band_pct_energy'], ref_analysis['band_pct_energy'])],
        'band_width_delta': [round(m - r, 3) for m, r in zip(mix_analysis['band_widths'], ref_analysis['band_widths'])],
        'macro_spread_delta': round(mix_analysis['macro_dynamic_spread_db'] - ref_analysis['macro_dynamic_spread_db'], 2),
        'chorus_expansion_delta': round(mix_analysis['width_expansion_chorus_pct'] - ref_analysis['width_expansion_chorus_pct'], 1)
    }
}

out_file = r"C:\Dev\DameiSuite\tools\deep_deconstruction_report.json"
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, default=float)

print("\nDeep Deconstruction Complete! Saved to:", out_file)
print(json.dumps(output['comparison'], indent=2, default=float))
