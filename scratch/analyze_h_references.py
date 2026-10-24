import os
import soundfile as sf
import numpy as np

ref_dir = r"H:\REFERENCES"

tracks = [
    ("Kel Pinchin (Split Chain)", "Split Chain - motionblur - 03 I'm Not Dying To Be Here.wav"),
    ("Adam Nolly Getgood (Bleed)", "01 The End of All We Know.flac"),
    ("Buster Odeholm (thrown)", "thrown - on the verge.wav"),
    ("Sam Guaiana (Mirrorcell)", "Mirrorcell - U(phoria).wav"),
    ("Zakk Cervini (Bad Omens)", "Bad Omens - THE DEATH OF PEACE OF MIND.wav"),
    ("Will Putney (Fit For An Autopsy)", "Fit For An Autopsy - Walk With Me In Hell.wav"),
    ("Lance Prenc (Alpha Wolf)", "Alpha Wolf, Holding Absence - Alpha Wolf - 60cm Of Steel (feat. Holding Absence).wav"),
    ("George Lever (Loathe)", "Loathe - Agressive Evolution.wav"),
    ("Acle Kahney (TesseracT)", "TesseracT - King.wav"),
    ("Henrik Udd (Architects)", "8. Gravity.flac"),
]

def analyze_track(name, filename):
    path = os.path.join(ref_dir, filename)
    if not os.path.exists(path):
        return f"{name:32s} | NOT FOUND: {filename}"
    
    # Read middle 30 seconds (typically chorus)
    info = sf.info(path)
    sr = info.samplerate
    start_sec = max(30, int(info.duration * 0.4))
    num_frames = int(sr * 25.0)
    
    data, _ = sf.read(path, start=int(start_sec * sr), frames=num_frames, dtype='float32')
    if data.ndim == 1:
        data = np.column_stack([data, data])
    
    left = data[:, 0]
    right = data[:, 1]
    mid = 0.5 * (left + right)
    side = 0.5 * (left - right)
    
    # True Peak / RMS
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
    rms_l = np.sqrt(np.mean(left**2))
    rms_r = np.sqrt(np.mean(right**2))
    rms = 0.5 * (rms_l + rms_r)
    
    crest_db = 20 * np.log10(max(peak, 1e-5) / max(rms, 1e-5))
    peak_db = 20 * np.log10(max(peak, 1e-5))
    rms_db = 20 * np.log10(max(rms, 1e-5))
    
    # M/S ratio
    rms_mid = np.sqrt(np.mean(mid**2))
    rms_side = np.sqrt(np.mean(side**2))
    side_to_mid_db = 20 * np.log10(max(rms_side, 1e-5) / max(rms_mid, 1e-5))
    
    # FFT Spectral energy bands
    fft_l = np.abs(np.fft.rfft(left))
    freqs = np.fft.rfftfreq(len(left), 1.0 / sr)
    
    def band_energy(f_low, f_high):
        idx = (freqs >= f_low) & (freqs < f_high)
        if not np.any(idx): return 1e-5
        return np.sqrt(np.mean(fft_l[idx]**2))
    
    sub = band_energy(20, 80)
    low_punch = band_energy(80, 200)
    mud = band_energy(200, 500)
    mid_body = band_energy(500, 2000)
    pick_bite = band_energy(2000, 5000)
    air = band_energy(8000, 20000)
    
    # Relative ratios (dB relative to mid_body)
    sub_rel = 20 * np.log10(sub / mid_body)
    punch_rel = 20 * np.log10(low_punch / mid_body)
    mud_rel = 20 * np.log10(mud / mid_body)
    bite_rel = 20 * np.log10(pick_bite / mid_body)
    air_rel = 20 * np.log10(air / mid_body)
    
    return {
        "name": name,
        "peak_db": round(peak_db, 2),
        "rms_db": round(rms_db, 2),
        "crest_db": round(crest_db, 2),
        "side_to_mid_db": round(side_to_mid_db, 2),
        "sub_rel": round(sub_rel, 2),
        "punch_rel": round(punch_rel, 2),
        "mud_rel": round(mud_rel, 2),
        "bite_rel": round(bite_rel, 2),
        "air_rel": round(air_rel, 2),
    }

results = []
print(f"{'PRODUCER / REFERENCE':32s} | RMS (dB) | Crest | S/M Width | 80Hz Punch | 200Hz Mud | 3kHz Bite | 8kHz Air")
print("-" * 105)
for name, f in tracks:
    res = analyze_track(name, f)
    if isinstance(res, dict):
        results.append(res)
        print(f"{res['name']:32s} | {res['rms_db']:7.1f} | {res['crest_db']:5.1f} | {res['side_to_mid_db']:8.1f}dB | {res['punch_rel']:9.1f}dB | {res['mud_rel']:8.1f}dB | {res['bite_rel']:8.1f}dB | {res['air_rel']:7.1f}dB")
    else:
        print(res)
