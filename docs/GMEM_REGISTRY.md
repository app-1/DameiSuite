# Damei `gmem:DameiMixMetering` Address Registry

Single source of truth. **Before using any address, check this file and the output of `scratch/scan_gmem2.py`.**
Generated from a scan of `DameiSuite`, `DameiAPI` and the installed REAPER Effects/Scripts (Phase 0).

## Occupied ranges (do not reuse)

| Range | Owner / purpose |
| :--- | :--- |
| 100–105 | Song structure / region bridge (`damei_song_structure_bridge.lua`) |
| 800–815 | Mixing/Ozone/Devastator bus telemetry |
| 820–827 | Drum suite telemetry (also read by Bass/Guitar/Synth/Assessment) |
| 840–848, 855 | Guitar suite (also Bass/Assessment/Devastator/Mixing reads) |
| 860–869 | Bass suite |
| 880–895 | Vocal suite (+ `damei_mir_bridge.lua` 891–895) |
| 1000–1039 | Mixing Suite published state |
| 1059–1060 | TonalBalance / TBC view |
| 1090–1166 | Assessment Matrix, MIR bridge, A/B gainmatch, calibration locks (1158/1159) |
| 1198–1200 | SpectrumProbe / TBC view / other |
| 1300 | In use (verify owner before touching) |
| 4410–4418, 4450–4457, 4500, 4600 | Other tools (DameiAPI) |
| 8999, 9000, 99999 | Sentinels / misc |

## Reserved for new bus suites

| Range | Owner |
| :--- | :--- |
| **1400–1449** | `Damei_InstrumentalSuite.jsfx` (publishes) |
| **1450–1499** | `Damei_VocalBus.jsfx` (publishes) |

### Layout (offsets from the owner's base)

| Offset | Field | Notes |
| :-: | :--- | :--- |
| +0 | heartbeat timestamp (`time_precise()`) | Readers treat > 1.5 s old as **dead** and fade to neutral over 30 ms |
| +1 | alive flag (1/0) | |
| +2 | RMS dBFS | |
| +3 | peak dBFS | |
| +4 | crest dB | |
| +5 | stereo width | |
| +6 | sub-band (<90 Hz) correlation | |
| +7 | active canonical producer id | index into `tools/preset_map.json` `canon_order` |
| +8 | operating tier (0 stereo, 1 ecosystem, 2 8-ch) | |
| +10 | requested pocket depth dB (Vocal -> Instrumental) | clamp ±3.0 at the reader |
| +11 | sentry trigger (kick/bass) | |
| +12..+19 | reserved | |

## Rules
1. Writers publish **only** inside their own range.
2. Every reader checks the heartbeat before using a value.
3. Readers apply bounded, slewed offsets internally. They never write user sliders.
4. Add new allocations here in the same commit that introduces them.
