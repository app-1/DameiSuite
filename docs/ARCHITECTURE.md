# Damei Telemetry Architecture & Shared Memory Bus

## Overview
Unlike traditional standalone DAW plugins that operate in isolation, the **Damei Suite** uses REAPER's zero-latency inter-plugin shared memory architecture (`options:gmem=DameiMixMetering`). This allows every stem bus suite, the mixing suite, and the mastering chain to communicate bidirectionally at audio sample rate.

## Shared Memory Map (`gmem:DameiMixMetering`)

### 1. Global Master & Mixing Suite (1000 - 1099)
| Address | Parameter | Description |
|---|---|---|
| `1000` | `MixSuite_Active` | Heartbeat & active flag (1 = active) |
| `1001` | `Mix_Comp_GR` | Mix bus compressor gain reduction (dB) |
| `1002` | `Mix_Output_RMS` | Mix pre-master RMS level (dBFS) |
| `1003` | `Mix_Output_Peak` | Mix true peak level (dBTP) |
| `1004` | `Chorus_Impact_State` | Song structure state (0 = verse, 1 = pre, 2 = chorus, 3 = bridge) |
| `1008` | `Producer_Preset_Idx` | Active signature preset index (0 - 21) |
| `1098` | `Raw_Audit_Mode` | Raw mix audit bypass flag (1 = active) |
| `1099` | `Raw_Score_Overall` | Raw mix baseline match score (%) |

### 2. Sankofa Oracle Scoring & Deviations (1100 - 1199)
| Address | Parameter | Description |
|---|---|---|
| `1101` | `Overall_Match_Score` | Weighted match against reference fingerprint (0 - 100%) |
| `1102` | `Tonal_Score` | 7-band spectral balance score (0 - 100%) |
| `1103` | `Stereo_Score` | Per-band stereo width & correlation score (0 - 100%) |
| `1104` | `Dynamics_Score` | PLR, crest, and loudness match score (0 - 100%) |
| `1107 - 1113` | `Band_Deviations[0..6]` | Exact dB deviation from reference per band (Sub to Air) |
| `1114 - 1120` | `Stereo_Deviations[0..6]` | Exact stereo width deviation from reference per band |
| `1121` | `Integrated_LUFS` | ITU-R BS.1770 integrated loudness |
| `1122` | `PLR` | Peak-to-Loudness Ratio (dynamic punch) |
| `1123` | `Stereo_Correlation` | Master stereo correlation (-1.0 to +1.0) |
| `1127` | `Vocal_Anchor_Ratio` | Lead Vocal RMS relative to Master RMS (dB) |
| `1128` | `Kick_Sub_Correlation` | Phase correlation between Kick drum and Sub-bass |
| `1129` | `Drum_Punch_Crest` | Drum shell transient crest ratio (dB) |

### 3. Stem Bus Telemetry (800 - 899)
| Range | Suite | Primary Telemetry |
|---|---|---|
| `820 - 839` | Drum Bus Architect | Transient attack punch, kick-to-sub anchor, shell crest |
| `840 - 859` | Guitar Bus Alchemist | Wall width, 190Hz chug energy, mid carve |
| `860 - 879` | Bass Bus Engine | Sub energy, kick ducking GR, sub/kick correlation |
| `880 - 899` | Vocal Sovereign | Lead vocal RMS, sibilance energy, pocket depth |

### 4. Closed-Loop Auto-Correct Trim Distribution (1300 - 1399)
The Sankofa Oracle evaluates deviations against the reference target and calculates compensation trims for each of the 6 instrument suites:
* `1300 - 1315`: Drums trim block (+0 active, +1..+7 band trims, +8 side width, +9 density)
* `1316 - 1331`: Guitars trim block
* `1332 - 1347`: Bass trim block
* `1348 - 1363`: Vocals trim block
* `1364 - 1379`: Synths trim block
* `1380 - 1395`: Devastator / Cinematic FX trim block
