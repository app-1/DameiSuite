# Damei Sankofa Oracle (`Damei_AssessmentMatrix.jsfx`)

## Overview
The **Damei Sankofa Oracle** is an intelligent reference match analyzer, closed-loop auto-correction brain, and full-scale **Mastering Console** for Cockos REAPER. Inserted on the mix/master channel, audio passes through 100% untouched while the engine performs continuous real-time analysis against commercial reference targets.

---

## 🎛️ Navigation Views
The plugin UI features three dedicated views accessible via the top-right header:
1. **`MATRIX VIEW`**: 7-band spectral divergence bars, stereo width deviation, dynamics, and heuristic critic recommendations.
2. **`MASTERING CONSOLE`**: Dedicated full-screen commercial mastering dashboard with high-resolution meters, True Peak ISP, EBU R128 loudness, streaming platform penalties, and mono translation racks.
3. **`REF LIBRARY`**: Interactive browser of 22 commercial reference tracks with live percentage match indicators.

---

## 📊 Comprehensive Mastering Metrics Suite

### 1. EBU R128 & ITU-R BS.1770-4 Loudness Engine
* **`LUFS-I` (Integrated Loudness)**: Gated commercial loudness (-70 LUFS absolute, -10 LU relative).
* **`LUFS-S` (Short-Term Loudness)**: 3-second sliding window with continuous peak hold (`LUFS-S Max`).
* **`LUFS-M` (Momentary Loudness)**: 400 ms sliding window with continuous peak hold (`LUFS-M Max`).
* **`LRA` (Loudness Range)**: EBU R128 statistical distribution (p95 - p10 in LU).

### 2. Intersample True Peak & Headroom Engine
* **4x Polyphase True Peak (dBTP)**: Zero-latency Hermite interpolator detecting inter-sample overs before lossy encoding (MP3, AAC).
* **True Peak Max L & R**: Independent channel monitoring.
* **ISP Overs Counter**: Real-time counter of inter-sample clipping events (`>= 0.0 dBTP`).
* **Dynamic Spread (PLR)**: Peak-to-Loudness Ratio in dB.
* **Crest Factor**: Peak-to-RMS ratio in dB.
* **DC Offset**: Direct current asymmetry detection (dBFS).

### 3. Streaming Platform Distribution & Penalty Matrix
Calculates real-time normalization penalties (how many dB the streaming service's normalizer will turn down the track) and compliance status:
* **Spotify**: Target -14.0 LUFS, -1.0 dBTP ceiling
* **Apple Music**: Target -16.0 LUFS, -1.0 dBTP (Sound Check)
* **YouTube Music**: Target -14.0 LUFS, -1.0 dBTP
* **Tidal / Amazon Music**: Target -14.0 LUFS, -1.0 dBTP
* **Commercial CD / Club**: Target -8.5 LUFS to -6.5 LUFS, -0.3 dBTP

### 4. Translation & Mono Compatibility Rack
* **Stereo Phase Correlation**: Continuous -1.0 to +1.0 meter with phase cancellation warning threshold.
* **Mono Summing Cancellation Loss (dB)**: Measures how much energy is lost when the stereo mix is collapsed to mono (critical for mobile phones and mono club PAs).
* **Sub-Bass (<100 Hz) Mono Percentage**: Assesses whether low-end energy is centered (>95% for vinyl cutting and club subwoofers).

---

## 🌐 Telemetry Bus Mapping (`gmem:DameiMixMetering`)
All mastering metrics are published to shared memory at audio rate for external script and bridge access:

| Address | Parameter | Description |
|---|---|---|
| `1130` | `True_Peak_L` | True Peak Left channel (dBTP) |
| `1131` | `True_Peak_R` | True Peak Right channel (dBTP) |
| `1132` | `True_Peak_Max` | True Peak Global Max (dBTP) |
| `1133` | `LUFS_M` | Momentary Loudness (LUFS) |
| `1134` | `LUFS_M_Max` | Momentary Loudness Max (LUFS) |
| `1135` | `LUFS_S` | Short-Term Loudness (LUFS) |
| `1136` | `LUFS_S_Max` | Short-Term Loudness Max (LUFS) |
| `1137` | `LRA` | Loudness Range (LU) |
| `1138` | `Spotify_Penalty` | Spotify volume reduction (dB) |
| `1139` | `Apple_Penalty` | Apple Sound Check reduction (dB) |
| `1140` | `YouTube_Penalty` | YouTube volume reduction (dB) |
| `1141` | `CD_Delta` | Difference from -8.5 LUFS CD target (dB) |
| `1142` | `Mono_Loss_dB` | Mono collapse cancellation loss (dB) |
| `1143` | `Sub_Mono_Pct` | Sub-bass mono percentage (%) |
| `1144` | `DC_Offset_dB` | DC offset level (dBFS) |
| `1145` | `ISP_Overs_Count` | Number of inter-sample overs detected |
