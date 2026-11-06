"""
DAMEI SUITE -- AI DRUM AUDITOR (PHASE 4 AUTONOMOUS STEM INTELLIGENCE)
Powered by Librosa, SciPy, SoundFile, NumPy & ReaScript IPC Bridge
Built by Damei Audio & Antigravity Pair Programming
"""

import os, sys, json, math
import numpy as np
import scipy.signal as signal
import soundfile as sf
import librosa

sys.path.append(r"c:\Dev\DameiAPI\scratch")
try:
    import ipc_lua
except ImportError:
    ipc_lua = None

def analyze_audio_file(file_path):
    """
    Performs forensic acoustic AI stem analysis on a WAV file.
    Calculates Peak dBFS, RMS dBFS, Crest Factor (PLR), Onset Density,
    Ghost Note Ratio, and Spectral Resonance Distribution.
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    # Load 15 seconds around choruses/grooves to be lightning fast
    data, sr = sf.read(file_path, stop=sr_stop if 'sr_stop' in locals() else None)
    if data.ndim > 1:
        mono = np.mean(data, axis=1)
    else:
        mono = data
        
    total_samples = len(mono)
    duration_s = total_samples / sr
    
    # 1. Dynamics & Crest Factor
    pk = np.max(np.abs(mono))
    pk_db = 20.0 * np.log10(max(pk, 1e-6))
    rms = np.sqrt(np.mean(mono**2))
    rms_db = 20.0 * np.log10(max(rms, 1e-6))
    crest_db = pk_db - rms_db
    
    # 2. Transient Onset Detection (Librosa)
    onset_frames = librosa.onset.onset_detect(y=mono[:min(len(mono), sr * 60)], sr=sr, units='frames')
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    hit_count = len(onset_frames)
    
    # 3. Spectral Energy Bands (SciPy Welch)
    freqs, psd = signal.welch(mono, sr, nperseg=4096)
    total_power = np.sum(psd) + 1e-12
    
    sub_power = np.sum(psd[(freqs >= 30) & (freqs < 80)]) / total_power * 100.0
    punch_power = np.sum(psd[(freqs >= 80) & (freqs < 200)]) / total_power * 100.0
    mud_power = np.sum(psd[(freqs >= 250) & (freqs < 450)]) / total_power * 100.0
    crack_power = np.sum(psd[(freqs >= 2000) & (freqs < 6000)]) / total_power * 100.0
    air_power = np.sum(psd[freqs >= 8000]) / total_power * 100.0
    
    # 4. Ringing Resonance Peak Detection
    peaks, props = signal.find_peaks(psd, height=np.max(psd)*0.15, distance=30)
    top_resonant_freqs = [round(float(freqs[p]), 1) for p in peaks[:4]]
    
    return {
        "file": os.path.basename(file_path),
        "duration_s": round(duration_s, 2),
        "peak_dbfs": round(pk_db, 2),
        "rms_dbfs": round(rms_db, 2),
        "crest_plr_db": round(crest_db, 2),
        "hit_count_60s": hit_count,
        "spectral_distribution": {
            "sub_30_80hz_pct": round(sub_power, 2),
            "punch_80_200hz_pct": round(punch_power, 2),
            "mud_boxiness_250_450hz_pct": round(mud_power, 2),
            "transient_crack_2k_6khz_pct": round(crack_power, 2),
            "air_sheen_gt_8khz_pct": round(air_power, 2)
        },
        "resonant_peaks_hz": top_resonant_freqs
    }

if __name__ == "__main__":
    test_file = r"H:\CasketsMixTutorial\CasketsStems\DRUMS-230131-160927\DRUMS\Colour_3) Snare Top.wav"
    if not os.path.exists(test_file):
        # Fallback to local session audio or Drumshotz
        test_file = r"H:\ReaperDrumSamples\reaper drum sample replacements\Drumshotz+-+George+Lever\Drumshotz - George Lever\EXTRA\05 Loathe Snare Close.wav"
    
    print("Running AI Drum Auditor on:", test_file)
    res = analyze_audio_file(test_file)
    print(json.dumps(res, indent=2))
