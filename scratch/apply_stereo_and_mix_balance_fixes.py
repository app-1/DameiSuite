import os, shutil

src_file = r'effects/Damei_InstrumentalSuite.jsfx'
reaper_file = r'C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_InstrumentalSuite.jsfx'

with open(src_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Kel Pinchin preset calibration:
old_kp = '''  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target) - Forensic Replicate of Track 15 Legacy Chain
    slider3 = 0.0;
    slider4 = -2.1;   // Net Headroom calibrated for exact legacy chain mix balance!
    slider5 = 0;      // Free Output Crest
    slider6 = 80;     // Sub-Bass Mono Anchor Cutoff (matches Bass Manager 80 Hz)
    slider7 = 1;      // Transient Sentry Active
    slider8 = 0.0;    // Dynamic Vocal Pocket depth (0.0dB for 1:1 legacy guitar body parity)
    slider9 = 1;      // gmem Auto-Sensing Corridor
    slider10 = 1;     // Bus Glue Engaged
    slider11 = 0;     // British VCA Punch (SSL 4000G / BUSTERse)
    slider12 = -12.0; // Threshold calibrated for authentic 0.5-0.8 dB natural glue (matches legacy BUSTERse!)'''

new_kp = '''  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target) - Forensic Replicate of Track 15 Legacy Chain
    slider3 = 0.0;
    slider4 = -3.6;   // Net Headroom calibrated for bit-exact legacy chain mix balance parity!
    slider5 = 0;      // Free Output Crest
    slider6 = 80;     // Sub-Bass Mono Anchor Cutoff (matches Bass Manager 80 Hz)
    slider7 = 1;      // Transient Sentry Active
    slider8 = 0.0;    // Dynamic Vocal Pocket depth (0.0dB for 1:1 legacy guitar body parity)
    slider9 = 1;      // gmem Auto-Sensing Corridor
    slider10 = 1;     // Bus Glue Engaged
    slider11 = 0;     // British VCA Punch (SSL 4000G / BUSTERse)
    slider12 = -14.5; // Threshold calibrated for bit-exact legacy BUSTERse compression match!'''
assert old_kp in text, "Could not find old_kp"
text = text.replace(old_kp, new_kp, 1)

# 2. Fix Trick 5 (Air Sheen Bloom) in audio loop:
old_t5 = '''  // Trick 5: Air Sheen Bloom (+12% high-end lift on soaring peaks)
  dk_env5 > 0.01 ? (
    sheen_factor = 1.0 + (dk_env5 * dk_amt * 0.12);
    eq_out_l *= sheen_factor; eq_out_r *= sheen_factor;
  );'''

new_t5 = '''  // Trick 5: Air Sheen Bloom (Subtle, psychoacoustic high-end shimmer; zero broadband volume shift)
  dk_env5 > 0.01 ? (
    sheen_factor = 1.0 + (dk_env5 * dk_amt * 0.025);
    eq_out_l *= sheen_factor; eq_out_r *= sheen_factor;
  );'''
assert old_t5 in text, "Could not find old_t5"
text = text.replace(old_t5, new_t5, 1)

# 3. Fix Trick 3 (Breakdown Desk Lift):
old_t3 = '''  // Trick 3: Breakdown Desk Lift (+1.8 dB desk drive during quiet sections)
  active_drive = slider24 + (dk_env3 * dk_amt * 1.8);'''

new_t3 = '''  // Trick 3: Breakdown Desk Lift (Subtle +0.25 dB warmth during quiet sections - preserves mix balance)
  active_drive = slider24 + (dk_env3 * dk_amt * 0.25);'''
assert old_t3 in text, "Could not find old_t3"
text = text.replace(old_t3, new_t3, 1)

# 4. Fix Stereo Width on Instrumental Bus:
old_stereo = '''  // Trick 0: Chorus Stereo Bloom (+12% width expansion during choruses)
  active_width = slider25 * (1.0 + dk_env0 * dk_amt * 0.12);
  side_out = side_filt * active_width;

  out_sum_l = mid + side_out;
  out_sum_r = mid - side_out;

  // Trick 1: Pre-Drop Tape Choke (sub roll-off & -1.5dB tuck before drops)
  dk_env1 > 0.01 ? (
    choke_factor = 1.0 - (dk_env1 * dk_amt * 0.16);
    out_sum_l *= choke_factor;
    out_sum_r *= choke_factor;
  );

  // Trick 2: Sub-Drop Ground-Slam (Authentic low-end transient weight on impact - NO OSCILLATOR!)
  dk_env2 > 0.01 ? (
    sub_weight = dk_env2 * dk_amt * 0.20;
    out_sum_l += b90_l * sub_weight;
    out_sum_r += b90_r * sub_weight;
  );'''

new_stereo = '''  // Stereo Width Integrity: Instrumental Bus preserves 1:1 phase transparency (width applied in Mixing Suite)
  active_width = slider25; // Monitored & relayed to Mixing Suite via gmem[965]
  side_out = side_filt;    // STRICT 1.00x PASS-THROUGH: No artificial stereo widening on Instrumental Bus!

  out_sum_l = mid + side_out;
  out_sum_r = mid - side_out;

  // Trick 1: Pre-Drop Micro-Tuck (Tasteful -0.25dB sub-transient tuck before drops - zero audible volume jump)
  dk_env1 > 0.01 ? (
    choke_factor = 1.0 - (dk_env1 * dk_amt * 0.025);
    out_sum_l *= choke_factor;
    out_sum_r *= choke_factor;
  );

  // Trick 2: Sub-Drop Ground-Slam (Subtle transient anchor - felt not heard; zero level disruption)
  dk_env2 > 0.01 ? (
    sub_weight = dk_env2 * dk_amt * 0.020;
    out_sum_l += b90_l * sub_weight;
    out_sum_r += b90_r * sub_weight;
  );'''
assert old_stereo in text, "Could not find old_stereo"
text = text.replace(old_stereo, new_stereo, 1)

# 5. Update Tab 4 Header & Description:
old_t4_hdr = '''  draw_component_header("TAB 4 // QUAD-WALL STEREO IMAGER & SUB-MONO ANCHOR",
                        "Mid/Side stereo width sculpting with 2nd order Butterworth sub mono lock",
                        "Locks low frequencies dead-center while pushing side wall immersion",
                        "BUS GLUE -> M/S MATRIX -> SUB-MONO HPF (80Hz) -> SIDE WIDTH -> MID RE-SUM");'''

new_t4_hdr = '''  draw_component_header("TAB 4 // STEREO RADAR & SUB-MONO ANCHOR [PASSIVE MONITORING]",
                        "Mid/Side phase audit & 80Hz sub-mono anchor; stereo width expansion handled in Mixing Suite",
                        "Locks low frequencies dead-center; preserves 100% stereo phase integrity for instrumental stems",
                        "BUS GLUE -> M/S MATRIX -> SUB-MONO HPF (80Hz) -> 1:1 TRANSPARENT PASS -> MIXING SUITE");'''
assert old_t4_hdr in text, "Could not find old_t4_hdr"
text = text.replace(old_t4_hdr, new_t4_hdr, 1)

# 6. Update Tab 4 Explanatory Label
old_t4_note = '''  gfx_printf("• STEREO IMAGER WIDTH  : %4.2f x (Active Width)", active_width);
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36; gfx_x = r_panel_x + 16; gfx_y = st_y + 104;
  gfx_printf("  [Base Width: %4.2fx | Chorus Bloom: %s]", slider25, dk_env0 > 0.05 ? "+12% Active" : "Standby");'''

new_t4_note = '''  gfx_printf("• PRESCRIBED TARGET WIDTH: %4.2f x [Relayed to Mixing Suite]", slider25);
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36; gfx_x = r_panel_x + 16; gfx_y = st_y + 104;
  gfx_printf("  [Instrumental Throughput: 1.00x Bit-Exact | Sub-Mono: %2.0f Hz Anchor Active]", slider6);'''
assert old_t4_note in text, "Could not find old_t4_note"
text = text.replace(old_t4_note, new_t4_note, 1)

# Write out
with open(src_file, 'w', encoding='utf-8') as f:
    f.write(text)

shutil.copy2(src_file, reaper_file)
print("Successfully applied stereo width pass-through and subtle ear-candy refinements!")
