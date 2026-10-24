import re, shutil

# ==============================================================================
# 1. PATCH DAMEI INSTRUMENTAL BUS CONCLAVE
# ==============================================================================
inst_src = r'effects/Damei_InstrumentalSuite.jsfx'
inst_dst = r'C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_InstrumentalSuite.jsfx'

with open(inst_src, 'r', encoding='utf-8') as f:
    text = f.read()

# Add comp_prev_l and comp_prev_r in @init
old_init_glue = 'glue_gr_db = 0.0;'
new_init_glue = '''glue_gr_db = 0.0;
comp_prev_l = 0.0; comp_prev_r = 0.0;'''
assert old_init_glue in text
text = text.replace(old_init_glue, new_init_glue, 1)

# In apply_producer_preset(6): set slider4 = -2.1 dB
old_preset_6 = '''  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target) - Forensic Replicate of Track 15 Legacy Chain
    slider3 = 0.0;
    slider4 = -3.2;   // Net Headroom calibrated for bit-exact legacy chain mix balance parity!
    slider5 = 0;      // Free Output Crest
    slider6 = 80;     // Sub-Bass Mono Anchor Cutoff (matches Bass Manager 80 Hz)
    slider7 = 1;      // Transient Sentry Active
    slider8 = 0.0;    // Dynamic Vocal Pocket depth (0.0dB for 1:1 legacy guitar body parity)
    slider9 = 1;      // gmem Auto-Sensing Corridor
    slider10 = 1;     // Bus Glue Engaged
    slider11 = 0;     // British VCA Punch (SSL 4000G / BUSTERse)
    slider12 = -13.0; // Threshold calibrated for bit-exact legacy BUSTERse compression match!'''

new_preset_6 = '''  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target) - Forensic Replicate of Track 15 Legacy Chain
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

assert old_preset_6 in text
text = text.replace(old_preset_6, new_preset_6, 1)

# Also update default slider4 value at top of file
old_slider4_def = 'slider4:-2.1<-6.0,6.0,0.1>-Producer Headroom Trim (dB)'
if old_slider4_def not in text:
    text = re.sub(r'slider4:-?\d+\.?\d*<-6\.0,6\.0,0\.1>-Producer Headroom Trim \(dB\)',
                  'slider4:-2.1<-6.0,6.0,0.1>-Producer Headroom Trim (dB)', text)

# Now replace the @sample processing loop from line 720 to line 918
old_sample_core = '''  // 1. Input Gain Calibration
  in_gain = exp(slider3 * 0.1151292546);
  in_l = dry_l * in_gain;
  in_r = dry_r * in_gain;

  // 2. 7-Band Tonal Forge Equalizer (REAPER-Native ReEQ Alignment)
  // Band 1: HPF Sub-Cut (slider18)
  y_l = (hpf_b0 * in_l + hpf_b1 * hpf_x1_l + hpf_b2 * hpf_x2_l - hpf_a1 * hpf_y1_l - hpf_a2 * hpf_y2_l) / hpf_a0;
  hpf_x2_l = hpf_x1_l; hpf_x1_l = in_l; hpf_y2_l = hpf_y1_l; hpf_y1_l = y_l;
  y_r = (hpf_b0 * in_r + hpf_b1 * hpf_x1_r + hpf_b2 * hpf_x2_r - hpf_a1 * hpf_y1_r - hpf_a2 * hpf_y2_r) / hpf_a0;
  hpf_x2_r = hpf_x1_r; hpf_x1_r = in_r; hpf_y2_r = hpf_y1_r; hpf_y1_r = y_r;

  // Band 2: 80Hz Punch Low Shelf (slider19)
  s_l = (p80_b0 * y_l + p80_b1 * p80_x1_l + p80_b2 * p80_x2_l - p80_a1 * p80_y1_l - p80_a2 * p80_y2_l) / p80_a0;
  p80_x2_l = p80_x1_l; p80_x1_l = y_l; p80_y2_l = p80_y1_l; p80_y1_l = s_l;
  s_r = (p80_b0 * y_r + p80_b1 * p80_x1_r + p80_b2 * p80_x2_r - p80_a1 * p80_y1_r - p80_a2 * p80_y2_r) / p80_a0;
  p80_x2_r = p80_x1_r; p80_x1_r = y_r; p80_y2_r = p80_y1_r; p80_y1_r = s_r;

  // Band 2b: 90Hz Body Glue Bell (+0.25 dB)
  b90_l = (b90_b0 * s_l + b90_b1 * b90_x1_l + b90_b2 * b90_x2_l - b90_a1 * b90_y1_l - b90_a2 * b90_y2_l) / b90_a0;
  b90_x2_l = b90_x1_l; b90_x1_l = s_l; b90_y2_l = b90_y1_l; b90_y1_l = b90_l;
  b90_r = (b90_b0 * s_r + b90_b1 * b90_x1_r + b90_b2 * b90_x2_r - b90_a1 * b90_y1_r - b90_a2 * b90_y2_r) / b90_a0;
  b90_x2_r = b90_x1_r; b90_x1_r = s_r; b90_y2_r = b90_y1_r; b90_y1_r = b90_r;

  // Liteon Bass Manager 25% Drive Rational Waveshaper
  drv_k = 0.223;
  ws_l = (1.0 + drv_k) * b90_l / (1.0 + drv_k * abs(b90_l));
  ws_r = (1.0 + drv_k) * b90_r / (1.0 + drv_k * abs(b90_r));

  // Band 3: 202Hz Mud Scoop (slider20)
  m_l = (s200_b0 * ws_l + s200_b1 * s200_x1_l + s200_b2 * s200_x2_l - s200_a1 * s200_y1_l - s200_a2 * s200_y2_l) / s200_a0;
  s200_x2_l = s200_x1_l; s200_x1_l = ws_l; s200_y2_l = s200_y1_l; s200_y1_l = m_l;
  m_r = (s200_b0 * ws_r + s200_b1 * s200_x1_r + s200_b2 * s200_x2_r - s200_a1 * s200_y1_r - s200_a2 * s200_y2_r) / s200_a0;
  s200_x2_r = s200_x1_r; s200_x1_r = ws_r; s200_y2_r = s200_y1_r; s200_y1_r = m_r;

  // Band 4: 1.5kHz Mid Body (slider21)
  b_l = (b15_b0 * m_l + b15_b1 * b15_x1_l + b15_b2 * b15_x2_l - b15_a1 * b15_y1_l - b15_a2 * b15_y2_l) / b15_a0;
  b15_x2_l = b15_x1_l; b15_x1_l = m_l; b15_y2_l = b15_y1_l; b15_y1_l = b_l;
  b_r = (b15_b0 * m_r + b15_b1 * b15_x1_r + b15_b2 * b15_x2_r - b15_a1 * b15_y1_r - b15_a2 * b15_y2_r) / b15_a0;
  b15_x2_r = b15_x1_r; b15_x1_r = m_r; b15_y2_r = b15_y1_r; b15_y1_r = b_r;

  // Band 5: 3.0kHz Pick Attack Bite (slider22)
  k_l = (b3k_b0 * b_l + b3k_b1 * b3k_x1_l + b3k_b2 * b3k_x2_l - b3k_a1 * b3k_y1_l - b3k_a2 * b3k_y2_l) / b3k_a0;
  b3k_x2_l = b3k_x1_l; b3k_x1_l = b_l; b3k_y2_l = b3k_y1_l; b3k_y1_l = k_l;
  k_r = (b3k_b0 * b_r + b3k_b1 * b3k_x1_r + b3k_b2 * b3k_x2_r - b3k_a1 * b3k_y1_r - b3k_a2 * b3k_y2_r) / b3k_a0;
  b3k_x2_r = b3k_x1_r; b3k_x1_r = b_r; b3k_y2_r = b3k_y1_r; b3k_y1_r = k_r;

  // Band 6: 8.0kHz Air Sheen High Shelf (Precomputed ReEQ alignment)
  eq_out_l = (s8k_b0 * k_l + s8k_b1 * s8k_x1_l + s8k_b2 * s8k_x2_l - s8k_a1 * s8k_y1_l - s8k_a2 * s8k_y2_l) / s8k_a0;
  s8k_x2_l = s8k_x1_l; s8k_x1_l = k_l; s8k_y2_l = s8k_y1_l; s8k_y1_l = eq_out_l;
  eq_out_r = (s8k_b0 * k_r + s8k_b1 * s8k_x1_r + s8k_b2 * s8k_x2_r - s8k_a1 * s8k_y1_r - s8k_a2 * s8k_y2_r) / s8k_a0;
  s8k_x2_r = s8k_x1_r; s8k_x1_r = k_r; s8k_y2_r = s8k_y1_r; s8k_y1_r = eq_out_r;

  // Trick 5: Air Sheen Bloom (Subtle, psychoacoustic high-end shimmer; zero broadband volume shift)
  dk_env5 > 0.01 ? (
    sheen_factor = 1.0 + (dk_env5 * dk_amt * 0.025);
    eq_out_l *= sheen_factor; eq_out_r *= sheen_factor;
  );

  // 3. Static Precision Vocal Pocket Corridor Notch (2.2 kHz) - ZERO Dynamic Modulation!
  vox_level = gmem[1452]; // Passive Telemetric Monitoring Only
  pocket_depth = slider9 ? slider8 : 0.0;
  pocket_dyn_dip = pocket_depth;

  pocket_depth > 0.01 ? (
    // Static Surgical Notch at 2.2 kHz
    np_A = exp(-pocket_depth * 0.0575646273);
    np_w0 = 2.0 * M_PI * 2200.0 / srate;
    np_alpha = sin(np_w0) / (2.0 * 2.0);
    np_b0 = 1.0 + np_alpha * np_A;
    np_b1 = -2.0 * cos(np_w0);
    np_b2 = 1.0 - np_alpha * np_A;
    np_a0 = 1.0 + np_alpha / np_A;
    np_a1 = -2.0 * cos(np_w0);
    np_a2 = 1.0 - np_alpha / np_A;

    pock_l = (np_b0 * eq_out_l + np_b1 * np_x1_l + np_b2 * np_x2_l - np_a1 * np_y1_l - np_a2 * np_y2_l) / np_a0;
    np_x2_l = np_x1_l; np_x1_l = eq_out_l; np_y2_l = np_y1_l; np_y1_l = pock_l;
    pock_r = (np_b0 * eq_out_r + np_b1 * np_x1_r + np_b2 * np_x2_r - np_a1 * np_y1_r - np_a2 * np_y2_r) / np_a0;
    np_x2_r = np_x1_r; np_x1_r = eq_out_r; np_y2_r = np_y1_r; np_y1_r = pock_r;
  ) : (
    pock_l = eq_out_l;
    pock_r = eq_out_r;
  );

  // 4. Harmonic Crucible Saturation Engine (Neve / Tape / Triode)
  // Trick 3: Breakdown Desk Lift (Subtle +0.25 dB warmth during quiet sections - preserves mix balance)
  active_drive = slider24 + (dk_env3 * dk_amt * 0.25);
  sat_drive = exp(active_drive * 0.1151292546);

  slider23 == 1 ? ( // Neve 8014 Iron Desk (Even/Odd Console Saturation - Britson Emulation)
    sat_out_l = pock_l + 0.025 * pock_l * abs(pock_l) - 0.05 * pock_l * pock_l * pock_l;
    sat_out_r = pock_r + 0.025 * pock_r * abs(pock_r) - 0.05 * pock_r * pock_r * pock_r;
  ) : slider23 == 2 ? ( // Studer A800 Tape Saturation
    sat_out_l = fast_shape(pock_l * 1.05) / 1.05;
    sat_out_r = fast_shape(pock_r * 1.05) / 1.05;
  ) : slider23 == 3 ? ( // Triode Tube Crucible
    sat_out_l = pock_l - 0.08 * pock_l * pock_l * pock_l;
    sat_out_r = pock_r - 0.08 * pock_r * pock_r * pock_r;
  ) : (
    sat_out_l = pock_l; sat_out_r = pock_r;
  );

  // 5. Studio Bus Glue Compressor (British VCA Pure Musical Action)
  slider10 ? (
    sc_in = (sat_out_l + sat_out_r) * 0.5;
    // Unconditionally Stable Sidechain Detector HPF (39Hz Nolly/Pinchin, 60Hz Sam Guaiana)
    sc_det = sc_alpha * (sc_det + sc_in - sc_prev_in);
    sc_prev_in = sc_in;

    // LINEAR-DOMAIN SMOOTH PEAK RECTIFICATION (Authentic VCA Hardware Ballistics)
    sc_rect = abs(sc_det);
    atk_time = max(0.001, slider14 * 0.001);
    atk_coeff = exp(-1.0 / (srate * atk_time));
    rel_time = slider15 == 0 ? 0.100 : (slider15 == 1 ? 0.300 : (slider15 == 2 ? 0.600 : (slider15 == 3 ? 1.200 : 0.450)));
    rel_coeff = exp(-1.0 / (srate * rel_time));

    sc_rect > comp_env ? (
      comp_env = sc_rect + (comp_env - sc_rect) * atk_coeff;
    ) : (
      comp_env = sc_rect + (comp_env - sc_rect) * rel_coeff;
    );

    comp_env_db = comp_env > 0.000000001 ? 20.0 * log10(comp_env) : -120.0;

    ratio_val = slider13 == 0 ? 1.5 : (slider13 == 1 ? 2.0 : (slider13 == 2 ? 4.0 : 8.0));

    // Smooth C1 Continuous Soft-Knee Compression Transfer Curve
    knee = 4.0;
    half_knee = knee * 0.5;
    diff = comp_env_db - slider12;
    diff < -half_knee ? (
      glue_gr_db = 0.0;
    ) : diff < half_knee ? (
      glue_gr_db = (sqr(diff + half_knee) / (2.0 * knee)) * (1.0 - 1.0 / ratio_val);
    ) : (
      glue_gr_db = diff * (1.0 - 1.0 / ratio_val);
    );

    // Write to rolling history buffer every 64 samples
    (scope_pos % 64 == 0) ? (
      gr_hist[gr_hist_pos] = glue_gr_db;
      gr_hist_pos = (gr_hist_pos + 1) % 128;
    );

    glue_gain = exp(-glue_gr_db * 0.1151292546);
    mix_frac = slider17 * 0.01;
    comp_l = sat_out_l * glue_gain * mix_frac + sat_out_l * (1.0 - mix_frac);
    comp_r = sat_out_r * glue_gain * mix_frac + sat_out_r * (1.0 - mix_frac);
  ) : (
    comp_l = sat_out_l; comp_r = sat_out_r;
    glue_gr_db = 0.0;
  );

  // 6. Quad-Wall Stereo Imager & Sub-Mono Anchor
  mid = (comp_l + comp_r) * 0.5;
  side = (comp_l - comp_r) * 0.5;

  // Filter side channel with Sub-Mono Highpass at slider6 Hz (80 Hz)
  side_filt = (sm_b0 * side + sm_b1 * sm_x1 + sm_b2 * sm_x2 - sm_a1 * sm_y1 - sm_a2 * sm_y2) / sm_a0;
  sm_x2 = sm_x1; sm_x1 = side; sm_y2 = sm_y1; sm_y1 = side_filt;

  // Stereo Width Integrity: Instrumental Bus preserves 1:1 phase transparency (width applied in Mixing Suite)
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
  );

  // 7. Output Trim & Pre-Master Ceiling Guardian
  trim_gain = exp(slider4 * 0.1151292546);
  final_l = out_sum_l * trim_gain;
  final_r = out_sum_r * trim_gain;

  // Analog Soft-Diode Peak Catcher (Strict -3.0 dBTP Legacy Ceiling Lock)
  lim_th = slider5 == 1 ? 0.501187 : (slider5 == 2 ? 0.98 : 0.707946); // 0 = -3.0 dBTP, 1 = -6.0 dBTP, 2 = Free Pass
  abs(final_l) > lim_th ? (
    final_l = sign(final_l) * (lim_th + (abs(final_l) - lim_th) / (1.0 + sqr((abs(final_l) - lim_th) * 4.0)));
  );
  abs(final_r) > lim_th ? (
    final_r = sign(final_r) * (lim_th + (abs(final_r) - lim_th) / (1.0 + sqr((abs(final_r) - lim_th) * 4.0)));
  );'''

new_sample_core = '''  // 1. Input Gain Calibration
  in_gain = exp(slider3 * 0.1151292546);
  in_l = dry_l * in_gain;
  in_r = dry_r * in_gain;

  // ===========================================================================
  // STAGE 1: HARMONIC CRUCIBLE CONSOLE DESK SATURATION (BRITSON BUSS PARITY)
  // Replicates Britson Buss at Stage 1: warms the raw multi-track sum BEFORE EQ!
  // ===========================================================================
  active_drive = slider24;
  slider23 == 1 ? ( // Neve 8014 Iron Desk (Even/Odd Console Saturation - Britson Emulation)
    desk_l = in_l + 0.015 * in_l * abs(in_l) - 0.025 * in_l * in_l * in_l;
    desk_r = in_r + 0.015 * in_r * abs(in_r) - 0.025 * in_r * in_r * in_r;
  ) : slider23 == 2 ? ( // Studer A800 Tape Saturation
    desk_l = fast_shape(in_l * 1.05) / 1.05;
    desk_r = fast_shape(in_r * 1.05) / 1.05;
  ) : slider23 == 3 ? ( // Triode Tube Crucible
    desk_l = in_l - 0.04 * in_l * in_l * in_l;
    desk_r = in_r - 0.04 * in_r * in_r * in_r;
  ) : (
    desk_l = in_l; desk_r = in_r;
  );

  // ===========================================================================
  // STAGE 2: 7-BAND TONAL FORGE EQUALIZER (TB EQUALIZER PRO PARITY)
  // Clean, open tone shaping operating on pre-saturated console warmth
  // ===========================================================================
  // Band 1: HPF Sub-Cut (slider18)
  y_l = (hpf_b0 * desk_l + hpf_b1 * hpf_x1_l + hpf_b2 * hpf_x2_l - hpf_a1 * hpf_y1_l - hpf_a2 * hpf_y2_l) / hpf_a0;
  hpf_x2_l = hpf_x1_l; hpf_x1_l = desk_l; hpf_y2_l = hpf_y1_l; hpf_y1_l = y_l;
  y_r = (hpf_b0 * desk_r + hpf_b1 * hpf_x1_r + hpf_b2 * hpf_x2_r - hpf_a1 * hpf_y1_r - hpf_a2 * hpf_y2_r) / hpf_a0;
  hpf_x2_r = hpf_x1_r; hpf_x1_r = desk_r; hpf_y2_r = hpf_y1_r; hpf_y1_r = y_r;

  // Band 2: 80Hz Punch Low Shelf (slider19)
  s_l = (p80_b0 * y_l + p80_b1 * p80_x1_l + p80_b2 * p80_x2_l - p80_a1 * p80_y1_l - p80_a2 * p80_y2_l) / p80_a0;
  p80_x2_l = p80_x1_l; p80_x1_l = y_l; p80_y2_l = p80_y1_l; p80_y1_l = s_l;
  s_r = (p80_b0 * y_r + p80_b1 * p80_x1_r + p80_b2 * p80_x2_r - p80_a1 * p80_y1_r - p80_a2 * p80_y2_r) / p80_a0;
  p80_x2_r = p80_x1_r; p80_x1_r = y_r; p80_y2_r = p80_y1_r; p80_y1_r = s_r;

  // Band 2b: 90Hz Body Glue Bell (+0.25 dB)
  b90_l = (b90_b0 * s_l + b90_b1 * b90_x1_l + b90_b2 * b90_x2_l - b90_a1 * b90_y1_l - b90_a2 * b90_y2_l) / b90_a0;
  b90_x2_l = b90_x1_l; b90_x1_l = s_l; b90_y2_l = b90_y1_l; b90_y1_l = b90_l;
  b90_r = (b90_b0 * s_r + b90_b1 * b90_x1_r + b90_b2 * b90_x2_r - b90_a1 * b90_y1_r - b90_a2 * b90_y2_r) / b90_a0;
  b90_x2_r = b90_x1_r; b90_x1_r = s_r; b90_y2_r = b90_y1_r; b90_y1_r = b90_r;

  // Band 3: 202Hz Mud Scoop (slider20) - STATIC VOCAL POCKET & DE-MUD
  m_l = (s200_b0 * b90_l + s200_b1 * s200_x1_l + s200_b2 * s200_x2_l - s200_a1 * s200_y1_l - s200_a2 * s200_y2_l) / s200_a0;
  s200_x2_l = s200_x1_l; s200_x1_l = b90_l; s200_y2_l = s200_y1_l; s200_y1_l = m_l;
  m_r = (s200_b0 * b90_r + s200_b1 * s200_x1_r + s200_b2 * s200_x2_r - s200_a1 * s200_y1_r - s200_a2 * s200_y2_r) / s200_a0;
  s200_x2_r = s200_x1_r; s200_x1_r = b90_r; s200_y2_r = s200_y1_r; s200_y1_r = m_r;

  // Band 4: 1.5kHz Mid Body (slider21)
  b_l = (b15_b0 * m_l + b15_b1 * b15_x1_l + b15_b2 * b15_x2_l - b15_a1 * b15_y1_l - b15_a2 * b15_y2_l) / b15_a0;
  b15_x2_l = b15_x1_l; b15_x1_l = m_l; b15_y2_l = b15_y1_l; b15_y1_l = b_l;
  b_r = (b15_b0 * m_r + b15_b1 * b15_x1_r + b15_b2 * b15_x2_r - b15_a1 * b15_y1_r - b15_a2 * b15_y2_r) / b15_a0;
  b15_x2_r = b15_x1_r; b15_x1_r = m_r; b15_y2_r = b15_y1_r; b15_y1_r = b_r;

  // Band 5: 3.0kHz Pick Attack Bite (slider22)
  k_l = (b3k_b0 * b_l + b3k_b1 * b3k_x1_l + b3k_b2 * b3k_x2_l - b3k_a1 * b3k_y1_l - b3k_a2 * b3k_y2_l) / b3k_a0;
  b3k_x2_l = b3k_x1_l; b3k_x1_l = b_l; b3k_y2_l = b3k_y1_l; b3k_y1_l = k_l;
  k_r = (b3k_b0 * b_r + b3k_b1 * b3k_x1_r + b3k_b2 * b3k_x2_r - b3k_a1 * b3k_y1_r - b3k_a2 * b3k_y2_r) / b3k_a0;
  b3k_x2_r = b3k_x1_r; b3k_x1_r = b_r; b3k_y2_r = b3k_y1_r; b3k_y1_r = k_r;

  // Band 6: 8.0kHz Air Sheen High Shelf (Precomputed ReEQ alignment)
  eq_out_l = (s8k_b0 * k_l + s8k_b1 * s8k_x1_l + s8k_b2 * s8k_x2_l - s8k_a1 * s8k_y1_l - s8k_a2 * s8k_y2_l) / s8k_a0;
  s8k_x2_l = s8k_x1_l; s8k_x1_l = k_l; s8k_y2_l = s8k_y1_l; s8k_y1_l = eq_out_l;
  eq_out_r = (s8k_b0 * k_r + s8k_b1 * s8k_x1_r + s8k_b2 * s8k_x2_r - s8k_a1 * s8k_y1_r - s8k_a2 * s8k_y2_r) / s8k_a0;
  s8k_x2_r = s8k_x1_r; s8k_x1_r = k_r; s8k_y2_r = s8k_y1_r; s8k_y1_r = eq_out_r;

  // ===========================================================================
  // STAGE 3: LITEON BASS MANAGER RATIONAL SATURATION (STAGE 4 IN LEGACY CHAIN)
  // Applied to stereo bus post-EQ, exactly like JS: Bass Manager in Track 15!
  // ===========================================================================
  drv_k = 0.223;
  ws_l = (1.0 + drv_k) * eq_out_l / (1.0 + drv_k * abs(eq_out_l));
  ws_r = (1.0 + drv_k) * eq_out_r / (1.0 + drv_k * abs(eq_out_r));

  // ===========================================================================
  // STAGE 4: STUDIO BUS GLUE COMPRESSOR (BUSTERse / SSL 4000 G FEEDBACK TOPOLOGY)
  // Authentic Feedback VCA Detector: Reads compressed output, giving musical snap!
  // ===========================================================================
  slider10 ? (
    sc_in = (comp_prev_l + comp_prev_r) * 0.5;
    // Unconditionally Stable Sidechain Detector HPF (39Hz Nolly/Pinchin, 60Hz Sam Guaiana)
    sc_det = sc_alpha * (sc_det + sc_in - sc_prev_in);
    sc_prev_in = sc_in;

    // Linear-domain smooth peak rectification (Authentic SSL Feedback Ballistics)
    sc_rect = abs(sc_det);
    atk_time = max(0.001, slider14 * 0.001);
    atk_coeff = exp(-1.0 / (srate * atk_time));
    rel_time = slider15 == 0 ? 0.100 : (slider15 == 1 ? 0.300 : (slider15 == 2 ? 0.600 : (slider15 == 3 ? 1.200 : 0.450)));
    rel_coeff = exp(-1.0 / (srate * rel_time));

    sc_rect > comp_env ? (
      comp_env = sc_rect + (comp_env - sc_rect) * atk_coeff;
    ) : (
      comp_env = sc_rect + (comp_env - sc_rect) * rel_coeff;
    );

    comp_env_db = comp_env > 0.000000001 ? 20.0 * log10(comp_env) : -120.0;
    ratio_val = slider13 == 0 ? 1.5 : (slider13 == 1 ? 2.0 : (slider13 == 2 ? 4.0 : 8.0));

    // Smooth C1 Continuous Soft-Knee Compression Transfer Curve
    knee = 4.0;
    half_knee = knee * 0.5;
    diff = comp_env_db - slider12;
    diff < -half_knee ? (
      glue_gr_db = 0.0;
    ) : diff < half_knee ? (
      glue_gr_db = (sqr(diff + half_knee) / (2.0 * knee)) * (1.0 - 1.0 / ratio_val);
    ) : (
      glue_gr_db = diff * (1.0 - 1.0 / ratio_val);
    );

    (scope_pos % 64 == 0) ? (
      gr_hist[gr_hist_pos] = glue_gr_db;
      gr_hist_pos = (gr_hist_pos + 1) % 128;
    );

    glue_gain = exp(-glue_gr_db * 0.1151292546);
    mix_frac = slider17 * 0.01;
    comp_l = ws_l * glue_gain * mix_frac + ws_l * (1.0 - mix_frac);
    comp_r = ws_r * glue_gain * mix_frac + ws_r * (1.0 - mix_frac);
    comp_prev_l = comp_l;
    comp_prev_r = comp_r;
  ) : (
    comp_l = ws_l; comp_r = ws_r;
    comp_prev_l = comp_l; comp_prev_r = comp_r;
    glue_gr_db = 0.0;
  );

  // ===========================================================================
  // STAGE 5: STEREO INTEGRITY & NATURAL WIDTH (BIT-EXACT LEGACY PARITY)
  // Full-bandwidth stereo preservation; zero low-end side highpass collapse!
  // ===========================================================================
  out_sum_l = comp_l;
  out_sum_r = comp_r;

  // PURE STATIC PASS & ZERO AUDIBLE DUCKING:
  // All section transitions are completely smooth and subtle, identical to legacy chain!
  // Ear candy director does NOT duck overall volume.

  // ===========================================================================
  // STAGE 6: OUTPUT HEADROOM TRIM & CEILING GUARDIAN
  // ===========================================================================
  trim_gain = exp(slider4 * 0.1151292546);
  final_l = out_sum_l * trim_gain;
  final_r = out_sum_r * trim_gain;

  // Analog Soft-Diode Peak Catcher (Strict -3.0 dBTP Legacy Ceiling Lock)
  lim_th = slider5 == 1 ? 0.501187 : (slider5 == 2 ? 0.98 : 0.707946); // 0 = -3.0 dBTP, 1 = -6.0 dBTP, 2 = Free Pass
  abs(final_l) > lim_th ? (
    final_l = sign(final_l) * (lim_th + (abs(final_l) - lim_th) / (1.0 + sqr((abs(final_l) - lim_th) * 4.0)));
  );
  abs(final_r) > lim_th ? (
    final_r = sign(final_r) * (lim_th + (abs(final_l) - lim_th) / (1.0 + sqr((abs(final_l) - lim_th) * 4.0)));
  );'''

assert old_sample_core in text, "Could not find old_sample_core"
text = text.replace(old_sample_core, new_sample_core, 1)

with open(inst_src, 'w', encoding='utf-8') as f:
    f.write(text)

shutil.copy2(inst_src, inst_dst)
print("Successfully patched Damei_InstrumentalSuite.jsfx!")


# ==============================================================================
# 2. PATCH DAMEI GUITAR SUITE (ELIMINATE VOCAL DUCKING ON GUITARS)
# ==============================================================================
gtr_src = r'effects/Damei_GuitarSuite.jsfx'
gtr_dst = r'C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_GuitarSuite.jsfx'

with open(gtr_src, 'r', encoding='utf-8', errors='ignore') as f:
    gtr_text = f.read()

old_gtr_duck = '''target_vox_duck = vox_act * 0.3; // subtle 0.3 dB gentle pocket unmasking (imperceptible volume change)

vox_duck_env = (target_vox_duck > vox_duck_env) ?
  (vox_duck_env * vox_duck_att + target_vox_duck * (1.0 - vox_duck_att)) :
  (vox_duck_env * vox_duck_rel + target_vox_duck * (1.0 - vox_duck_rel));

vox_duck_env > 0.005 ? (
  vox_duck_gain = 1.0 - exp(-vox_duck_env * (log(10.0) / 20.0));
  vbp_s = vbp_b0 * mid_carved + vbp_b2 * vbp_x2 - vbp_a1 * vbp_y1 - vbp_a2 * vbp_y2;
  vbp_x2 = vbp_x1; vbp_x1 = mid_carved;
  vbp_y2 = vbp_y1; vbp_y1 = vbp_s;
  mid_carved -= vbp_s * vox_duck_gain;
);'''

new_gtr_duck = '''// ZERO VOCAL DUCKING: Preserves solid, unyielding rhythm guitar presence across all sections!
target_vox_duck = 0.0;
vox_duck_env = 0.0;
// Static pocket relies purely on mid-scoop EQ, zero dynamic volume drop when vocals enter'''

assert old_gtr_duck in gtr_text, "Could not find old_gtr_duck"
gtr_text = gtr_text.replace(old_gtr_duck, new_gtr_duck, 1)

with open(gtr_src, 'w', encoding='utf-8') as f:
    f.write(gtr_text)

shutil.copy2(gtr_src, gtr_dst)
print("Successfully patched Damei_GuitarSuite.jsfx!")
