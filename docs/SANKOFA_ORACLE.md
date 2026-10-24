# Damei Sankofa Oracle (`Damei_AssessmentMatrix.jsfx`)

## Overview
The **Damei Sankofa Oracle** is an intelligent reference match analyzer, closed-loop auto-correction brain, and full-scale **Mastering Console** for Cockos REAPER. Inserted on the mix/master channel, audio passes through 100% untouched while the engine performs continuous real-time analysis against commercial reference targets.

---

8: ## 🎛️ Navigation Views
9: The plugin UI features dedicated views accessible via the top-right header:
10: 1. **`MATRIX VIEW`**: 7-band spectral divergence bars, stereo width deviation, dynamics, and heuristic critic recommendations.
11: 2. **`STEM A/B`**: Side-by-side stem shootout console with 4-channel sidechain input (Pins 3/4), loudness-matched A/B auditioning, auditory null diff, 7-band live spectral delta bars, low-end punch index, and inter-track phase coherence.
12: 3. **`MASTERING CONSOLE`**: Dedicated full-screen commercial mastering dashboard with high-resolution meters, True Peak ISP, EBU R128 loudness, streaming platform penalties, and mono translation racks.
13: 4. **`REF LIBRARY`**: Interactive browser of 22 commercial reference tracks with live percentage match indicators.
14: 5. **`OLLAMA AI`**: Direct local neural MIR bridge (Qwen2.5-Coder, BS-RoFormer, CLAP).
15: 
16: ---
17: 
18: ## 📊 Comprehensive Mastering & Comparative Stem Metrics Suite
19: 
20: ### 1. 4-Channel Live Sidechain & Auditory Null Controller
21: * **Pins 1/2**: Your Mix / Stem.
22: * **Pins 3/4**: Reference Master / Stem (External sidechain).
23: * **Audition Modes**: Mix (Pass-through), Reference (Auto LUFS-Matched), Reference (Raw), and Auditory Null Diff ($Mix - Ref$).
24: * **Stem Profile Targets**: Calibrated scoring profiles for `Master`, `Drums`, `Bass`, `Vocals`, and `Other/Synth`.
25: 
26: ### 2. Low-End Punch Index & Spectral Tilt
27: * **Low Punch Index (dB)**: Dedicated Crest Factor of the 20–250 Hz band on Mix vs Reference (revealing whether kick/bass transients are over-limited or choked).
28: * **Continuous Spectral Tilt (dB/oct)**: Linear regression slope of the 7-band spectrum showing overall macro brightness/darkness relative to commercial target curves.
29: * **Inter-Track Phase Coherence ($r_{xy}(f)$)**: Measures phase alignment per band between your stem and the reference stem.
30: 
31: ### 3. EBU R128 & ITU-R BS.1770-4 Loudness Engine
32: * **`LUFS-I` (Integrated Loudness)**: Gated commercial loudness (-70 LUFS absolute, -10 LU relative).
33: * **`LUFS-S` (Short-Term Loudness)**: 3-second sliding window with continuous peak hold (`LUFS-S Max`).
34: * **`LUFS-M` (Momentary Loudness)**: 400 ms sliding window with continuous peak hold (`LUFS-M Max`).
35: * **`LRA` (Loudness Range)**: EBU R128 statistical distribution (p95 - p10 in LU).
36: 
37: ### 4. Intersample True Peak & Headroom Engine
38: * **4x Polyphase True Peak (dBTP)**: Zero-latency Hermite interpolator detecting inter-sample overs before lossy encoding (MP3, AAC).
39: * **True Peak Max L & R**: Independent channel monitoring.
40: * **ISP Overs Counter**: Real-time counter of inter-sample clipping events (`>= 0.0 dBTP`).
41: * **Dynamic Spread (PLR)**: Peak-to-Loudness Ratio in dB.
42: * **Crest Factor**: Peak-to-RMS ratio in dB.
43: * **DC Offset**: Direct current asymmetry detection (dBFS).
44: 
45: ### 5. Streaming Platform Distribution & Penalty Matrix
46: Calculates real-time normalization penalties (how many dB the streaming service's normalizer will turn down the track) and compliance status:
47: * **Spotify**: Target -14.0 LUFS, -1.0 dBTP ceiling
48: * **Apple Music**: Target -16.0 LUFS, -1.0 dBTP (Sound Check)
49: * **YouTube Music**: Target -14.0 LUFS, -1.0 dBTP
50: * **Tidal / Amazon Music**: Target -14.0 LUFS, -1.0 dBTP
51: * **Commercial CD / Club**: Target -8.5 LUFS to -6.5 LUFS, -0.3 dBTP
52: 
53: ### 6. Translation & Mono Compatibility Rack
54: * **Stereo Phase Correlation**: Continuous -1.0 to +1.0 meter with phase cancellation warning threshold.
55: * **Mono Summing Cancellation Loss (dB)**: Measures how much energy is lost when the stereo mix is collapsed to mono (critical for mobile phones and mono club PAs).
56: * **Sub-Bass (<100 Hz) Mono Percentage**: Assesses whether low-end energy is centered (>95% for vinyl cutting and club subwoofers).
57: 
58: ---
59: 
60: ## 🌐 Telemetry Bus Mapping (`gmem:DameiMixMetering`)
61: All mastering & comparative stem metrics are published to shared memory at audio rate for external script and bridge access:
62: 
63: | Address | Parameter | Description |
64: |---|---|---|
65: | `1130` | `True_Peak_L` | True Peak Left channel (dBTP) |
66: | `1131` | `True_Peak_R` | True Peak Right channel (dBTP) |
67: | `1132` | `True_Peak_Max` | True Peak Global Max (dBTP) |
68: | `1133` | `LUFS_M` | Momentary Loudness (LUFS) |
69: | `1134` | `LUFS_M_Max` | Momentary Loudness Max (LUFS) |
70: | `1135` | `LUFS_S` | Short-Term Loudness (LUFS) |
71: | `1136` | `LUFS_S_Max` | Short-Term Loudness Max (LUFS) |
72: | `1137` | `LRA` | Loudness Range (LU) |
73: | `1138` | `Spotify_Penalty` | Spotify volume reduction (dB) |
74: | `1139` | `Apple_Penalty` | Apple Sound Check reduction (dB) |
75: | `1140` | `YouTube_Penalty` | YouTube volume reduction (dB) |
76: | `1141` | `CD_Delta` | Difference from -8.5 LUFS CD target (dB) |
77: | `1142` | `Mono_Loss_dB` | Mono collapse cancellation loss (dB) |
78: | `1143` | `Sub_Mono_Pct` | Sub-bass mono percentage (%) |
79: | `1144` | `DC_Offset_dB` | DC offset level (dBFS) |
80: | `1145` | `ISP_Overs_Count` | Number of inter-sample overs detected |
81: | `1146` | `Ref_LUFS_Delta` | Real-time gain offset needed to loudness-match Ref to Mix |
82: | `1147` | `Low_Punch_Mix` | Crest factor of 20–250 Hz band on Mix (dB) |
83: | `1148` | `Low_Punch_Ref` | Crest factor of 20–250 Hz band on Reference (dB) |
84: | `1149` | `Spectral_Tilt_Delta`| Slope deviation from reference curve ($\Delta \text{dB/oct}$) |
85: | `1150..1156` | `Live_Band_Diff_dB`| Direct live differential per band (Bands 1–7) |
86: | `1157` | `Stem_Profile_Mode` | Active stem profile (0=Master, 1=Drums, 2=Bass, 3=Vocals, 4=Other) |
87: | `1158` | `Monitor_Mode` | Audition Monitor (0=Mix, 1=Ref Matched, 2=Ref Raw, 3=Null Diff) |
88: | `1159` | `Ref_LUFS_I` | Integrated loudness of Reference sidechain |
89: | `1160` | `Have_Sidechain` | 1 if signal present on Pins 3/4, 0 otherwise |
