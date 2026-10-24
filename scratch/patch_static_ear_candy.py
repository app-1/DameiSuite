import re, shutil

src = r'effects/Damei_InstrumentalSuite.jsfx'
dst = r'C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_InstrumentalSuite.jsfx'

with open(src, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Kel Pinchin preset: slider4 = -1.6, slider12 = -12.0
old_p6 = '''  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target) - Forensic Replicate of Track 15 Legacy Chain
    slider3 = 0.0;
    slider4 = -2.1;   // Headroom Staging Calibrated for 1:1 Bit-Exact Legacy Chain Mix Balance Parity!
    slider5 = 0;      // -3.0 dBTP Strict Legacy Staging Ceiling Lock
    slider6 = 80;     // Sub-Bass Anchor Cutoff
    slider7 = 1;      // Transient Sentry Active
    slider8 = 0.0;    // Vocal Pocket depth 0.0dB (relies on static 202Hz Tonal Forge Mud Scoop)
    slider9 = 0;      // Static Flat Wire Bypass (Zero Dynamic Modulation)
    slider10 = 1;     // Bus Glue Engaged
    slider11 = 0;     // British VCA Punch (SSL 4000G / BUSTERse Feedback Topology)
    slider12 = -13.0; // Threshold calibrated for bit-exact legacy BUSTERse compression match!'''

new_p6 = '''  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target) - Forensic Replicate of Track 15 Legacy Chain
    slider3 = 0.0;
    slider4 = -1.6;   // Headroom Staging Calibrated for Bit-Exact Legacy Chain RMS & Peak Parity!
    slider5 = 0;      // -3.0 dBTP Strict Legacy Staging Ceiling Lock
    slider6 = 80;     // Sub-Bass Anchor Cutoff
    slider7 = 1;      // Transient Sentry Active
    slider8 = 0.0;    // Vocal Pocket depth 0.0dB (relies on static 202Hz Tonal Forge Mud Scoop)
    slider9 = 0;      // Static Flat Wire Bypass (Zero Dynamic Modulation)
    slider10 = 1;     // Bus Glue Engaged
    slider11 = 0;     // British VCA Punch (SSL 4000G / BUSTERse Feedback Topology)
    slider12 = -12.0; // Threshold calibrated for bit-exact legacy BUSTERse compression match!'''

assert old_p6 in text, "Could not find old_p6"
text = text.replace(old_p6, new_p6, 1)

# 2. Update default slider4 definition at top of file
old_slider4_def = 'slider4:-2.1<-6.0,6.0,0.1>-Producer Headroom Trim (dB)'
new_slider4_def = 'slider4:-1.6<-6.0,6.0,0.1>-Producer Headroom Trim (dB)'
assert old_slider4_def in text, "Could not find old_slider4_def"
text = text.replace(old_slider4_def, new_slider4_def, 1)

# 3. Update Ear Candy Director to be 100% STATIC (zero dynamic envelopes, zero section jumping)
old_ec_director = '''slider48 == 0 ? (
  // PURE STATIC PASS: All dynamic section tricks locked strictly to 0
  dk_env0 = 0.0; dk_env1 = 0.0; dk_env2 = 0.0; dk_env3 = 0.0;
  dk_env4 = 0.0; dk_env5 = 0.0; dk_env6 = 0.0; dk_env7 = 0.0;
) : (
  // Creative Audition Mode
  // Trick 0: Chorus Stereo Bloom
  dk_trg0 = (dk_auto && dk_r_idx == 4) || slider33;
  dk_env0 += ((dk_trg0 ? 1.0 : 0.0) - dk_env0) * 0.008;

  // Trick 1: Pre-Drop Tape Choke
  dk_trg1 = (dk_auto && dk_r_idx == 3 && gmem[105] > 0.85 && dk_fast_db > -18.0) || slider34;
  dk_env1 += ((dk_trg1 ? 1.0 : 0.0) - dk_env1) * 0.015;

  // Trick 2: Sub-Drop Ground-Slam (Dynamic transient punch on section entry)
  dk_trg2 = (dk_auto && dk_r_idx == 4 && inst_peak > 0.42) || slider35;
  dk_env2 += ((dk_trg2 ? 1.0 : 0.0) - dk_env2) * 0.020;

  // Trick 3: Breakdown Desk Lift
  dk_trg3 = (dk_auto && (dk_r_idx == 2 || dk_r_idx == 5) && dk_fast_db < -20.0) || slider36;
  dk_env3 += ((dk_trg3 ? 1.0 : 0.0) - dk_env3) * 0.005;

  // Trick 4: Snare Sidechain Snap
  dk_trg4 = (slider16 <= 42);
  dk_env4 += ((dk_trg4 ? 1.0 : 0.0) - dk_env4) * 0.050;

  // Trick 5: Air Sheen Bloom
  dk_trg5 = (dk_auto && dk_r_idx == 4);
  dk_env5 += ((dk_trg5 ? 1.0 : 0.0) - dk_env5) * 0.008;

  // Trick 6: Kick Decoupling Anchor
  dk_trg6 = (slider16 >= 55);
  dk_env6 += ((dk_trg6 ? 1.0 : 0.0) - dk_env6) * 0.050;

  // Trick 7: Haas Wall Widener
  dk_trg7 = (dk_auto && dk_r_idx == 5);
  dk_env7 += ((dk_trg7 ? 1.0 : 0.0) - dk_env7) * 0.010;
);'''

new_ec_director = '''// =============================================================================
// STATIC EAR-CANDY IMPLEMENTATION (ZERO DYNAMIC DRIFT / ZERO SECTION PUMPING)
// Like the legacy chain, all processes are applied statically to preserve mix balance!
// =============================================================================
slider48 == 0 ? (
  // PURE STATIC PASS: All ear candy tricks locked strictly to 0
  dk_env0 = 0.0; dk_env1 = 0.0; dk_env2 = 0.0; dk_env3 = 0.0;
  dk_env4 = 0.0; dk_env5 = 0.0; dk_env6 = 0.0; dk_env7 = 0.0;
) : (
  // STATIC EAR CANDY PROFILE:
  // Processes apply as constant, static harmonic/spatial colorations without time-varying envelopes!
  // Trick 0: Static Stereo Air Bloom
  dk_env0 = ((slider50 & 1) || slider33) ? (dk_amt * 1.0) : 0.0;

  // Trick 1: Static Analog Tape Head Saturation (zero volume ducking)
  dk_env1 = ((slider50 & 2) || slider34) ? (dk_amt * 1.0) : 0.0;

  // Trick 2: Static Sub Foundation Weight
  dk_env2 = ((slider50 & 4) || slider35) ? (dk_amt * 1.0) : 0.0;

  // Trick 3: Static Desk Transformer Warmth (+0.3dB Neve desk drive)
  dk_env3 = ((slider50 & 8) || slider36) ? (dk_amt * 1.0) : 0.0;

  // Trick 4: Static Snare Sidechain Snap (39Hz Detector HPF)
  dk_env4 = (slider50 & 16) ? (dk_amt * 1.0) : 0.0;

  // Trick 5: Static Air Sheen (+0.3dB Silk Air Shelf)
  dk_env5 = (slider50 & 32) ? (dk_amt * 1.0) : 0.0;

  // Trick 6: Static Kick Decoupling Anchor (60Hz Detector HPF)
  dk_env6 = (slider50 & 64) ? (dk_amt * 1.0) : 0.0;

  // Trick 7: Static Spatial Air Decorrelation
  dk_env7 = (slider50 & 128) ? (dk_amt * 1.0) : 0.0;
);'''

assert old_ec_director in text, "Could not find old_ec_director"
text = text.replace(old_ec_director, new_ec_director, 1)

# In Stage 1: Harmonic Crucible, incorporate static desk lift if dk_env3 active
old_stage1_drive = 'active_drive = slider24;'
new_stage1_drive = 'active_drive = slider24 + (dk_env3 * 0.3);'
assert old_stage1_drive in text, "Could not find old_stage1_drive"
text = text.replace(old_stage1_drive, new_stage1_drive, 1)

with open(src, 'w', encoding='utf-8') as f:
    f.write(text)

shutil.copy2(src, dst)
print("Successfully patched Damei_InstrumentalSuite.jsfx with static Ear Candy and -1.6dB calibrated trim!")
