# scratch/analyze_kel_pinchin_bass.py
import soundfile as sf
import numpy as np

ref_path = r"H:\REFERENCES\Split Chain - motionblur - 03 I'm Not Dying To Be Here.wav"
info = sf.info(ref_path)
print(f"Split Chain Reference: Duration={info.duration:.1f}s, SR={info.samplerate}, Channels={info.channels}")

# Read chorus section (around 45s to 70s)
start_frame = int(info.samplerate * 45.0)
frames = int(info.samplerate * 25.0)
data, sr = sf.read(ref_path, start=start_frame, frames=frames, dtype='float32')

left = data[:, 0]
right = data[:, 1]
mid = 0.5 * (left + right)
side = 0.5 * (left - right)

# Frequency analysis
fft_mid = np.abs(np.fft.rfft(mid))
fft_side = np.abs(np.fft.rfft(side))
freqs = np.fft.rfftfreq(len(mid), 1.0 / sr)

def band_rms(fft_data, f_low, f_high):
    idx = (freqs >= f_low) & (freqs < f_high)
    if not np.any(idx): return -120.0
    return 20.0 * np.log10(np.sqrt(np.mean(fft_data[idx]**2)) + 1e-12)

print("=== Split Chain (Kel Pinchin) Acoustic Profile ===")
print(f"  Total RMS           : {20 * np.log10(np.sqrt(np.mean(data**2))):.2f} dBFS")
print(f"  True Peak           : {20 * np.log10(np.max(np.abs(data))):.2f} dBFS")
print(f"  Crest Factor        : {20 * np.log10(np.max(np.abs(data)) / np.sqrt(np.mean(data**2))):.2f} dB")
print(f"  Sub-Rumble (20-40Hz): Mid = {band_rms(fft_mid, 20, 40):.2f} dB | Side = {band_rms(fft_side, 20, 40):.2f} dB (Side/Mid: {band_rms(fft_side, 20, 40) - band_rms(fft_mid, 20, 40):.2f} dB)")
print(f"  Sub-Bass (40-80Hz)  : Mid = {band_rms(fft_mid, 40, 80):.2f} dB | Side = {band_rms(fft_side, 40, 80):.2f} dB (Side/Mid: {band_rms(fft_side, 40, 80) - band_rms(fft_mid, 40, 80):.2f} dB)")
print(f"  Bass Punch (80-160) : Mid = {band_rms(fft_mid, 80, 160):.2f} dB | Side = {band_rms(fft_side, 80, 160):.2f} dB (Side/Mid: {band_rms(fft_side, 80, 160) - band_rms(fft_mid, 80, 160):.2f} dB)")
print(f"  Low Mid (160-350Hz) : Mid = {band_rms(fft_mid, 160, 350):.2f} dB | Side = {band_rms(fft_side, 160, 350):.2f} dB")
print(f"  Mid Body (500-2kHz) : Mid = {band_rms(fft_mid, 500, 2000):.2f} dB | Side = {band_rms(fft_side, 500, 2000):.2f} dB")
print(f"  Air Sheen (8k-20kHz): Mid = {band_rms(fft_mid, 8000, 20000):.2f} dB | Side = {band_rms(fft_side, 8000, 20000):.2f} dB")
