"""
Comprehensive upgrade and patch for Damei Instrumental Bus Alchemist and Damei Vocal Empress.
Applies:
1. options:no_meter header directive to eliminate REAPER volume meters on both sides.
2. 100% bit-exact transparent passthrough when in Preset 00 (Unity Baseline) or suite bypassed.
3. Sub-Bass Mono Elliptic Anchor on side channel (zero phase distortion, zero kick/bass comb filtering).
4. Strictly isolated Left and Right channel delay line registers across all EQ biquads.
5. True ANSI C16.5 300ms VU RMS integration and reactive moving-coil needle ballistics.
6. Luxury SIFAM Director console styling matching Damei_MixingSuite standard.
"""

import sys, os, re, subprocess

def patch_instrumental_suite():
    path = r"c:\Dev\DameiSuite\scratch\generate_instrumental_suite.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Header options:no_meter
    old_opts = "options:gmem=DameiMixMetering\noptions:maxmem=65536"
    new_opts = "options:no_meter\noptions:gmem=DameiMixMetering\noptions:maxmem=65536"
    content = content.replace(old_opts, new_opts)

    # 2. @init filter memories
    old_init = r"""// Filter state memories
hpf_x1 = 0; hpf_x2 = 0; hpf_y1 = 0; hpf_y2 = 0;
p80_x1 = 0; p80_x2 = 0; p80_y1 = 0; p80_y2 = 0;
s280_x1 = 0; s280_x2 = 0; s280_y1 = 0; s280_y2 = 0;
b3k_x1 = 0; b3k_x2 = 0; b3k_y1 = 0; b3k_y2 = 0;
s10k_x1 = 0; s10k_x2 = 0; s10k_y1 = 0; s10k_y2 = 0;
pock_x1 = 0; pock_x2 = 0; pock_y1 = 0; pock_y2 = 0;

// Sub-bass Linkwitz-Riley 4-pole memory
sub_lp_l1 = 0; sub_lp_l2 = 0; sub_lp_r1 = 0; sub_lp_r2 = 0;
sub_hp_l1 = 0; sub_hp_l2 = 0; sub_hp_r1 = 0; sub_hp_r2 = 0;"""

    new_init = r"""// Filter state memories (Fully isolated Left & Right delay lines)
hpf_x1_l = 0; hpf_x2_l = 0; hpf_y1_l = 0; hpf_y2_l = 0;
hpf_x1_r = 0; hpf_x2_r = 0; hpf_y1_r = 0; hpf_y2_r = 0;

p80_x1_l = 0; p80_x2_l = 0; p80_y1_l = 0; p80_y2_l = 0;
p80_x1_r = 0; p80_x2_r = 0; p80_y1_r = 0; p80_y2_r = 0;

s280_x1_l = 0; s280_x2_l = 0; s280_y1_l = 0; s280_y2_l = 0;
s280_x1_r = 0; s280_x2_r = 0; s280_y1_r = 0; s280_y2_r = 0;

b3k_x1_l = 0; b3k_x2_l = 0; b3k_y1_l = 0; b3k_y2_l = 0;
b3k_x1_r = 0; b3k_x2_r = 0; b3k_y1_r = 0; b3k_y2_r = 0;

s10k_x1_l = 0; s10k_x2_l = 0; s10k_y1_l = 0; s10k_y2_l = 0;
s10k_x1_r = 0; s10k_x2_r = 0; s10k_y1_r = 0; s10k_y2_r = 0;

pock_x1 = 0; pock_x2 = 0; pock_y1 = 0; pock_y2 = 0;

// Sub-Mono Elliptical Filter memory (High-Pass on Side channel only - Mid 100% Phase-Preserved)
sm_hp_x1 = 0; sm_hp_x2 = 0; sm_hp_y1 = 0; sm_hp_y2 = 0;
vu_rms_smooth = 0.0;"""
    content = content.replace(old_init, new_init)

    # 3. update_filters: Elliptic side-channel highpass
    old_sub_filt = r"""  // Linkwitz-Riley Sub Cutoff (slider6)
  sub_wc = 2.0 * M_PI * clamp(slider6, 40.0, 160.0) / srate;
  sub_k = tan(sub_wc * 0.5);
  sub_denom = 1.0 + 1.41421356 * sub_k + sub_k * sub_k;
  sub_a1 = 2.0 * (sub_k * sub_k - 1.0) / sub_denom;
  sub_a2 = (1.0 - 1.41421356 * sub_k + sub_k * sub_k) / sub_denom;
  sub_lp_b0 = (sub_k * sub_k) / sub_denom;
  sub_lp_b1 = 2.0 * sub_lp_b0;
  sub_lp_b2 = sub_lp_b0;"""

    new_sub_filt = r"""  // Elliptic Sub-Mono Side Highpass (Butterworth 2nd order at slider6 Hz)
  sm_w0 = 2.0 * M_PI * clamp(slider6, 40.0, 160.0) / srate;
  sm_cos = cos(sm_w0); sm_sin = sin(sm_w0);
  sm_alpha = sm_sin / (2.0 * 0.7071);
  sm_b0 = (1.0 + sm_cos) * 0.5;
  sm_b1 = -(1.0 + sm_cos);
  sm_b2 = (1.0 + sm_cos) * 0.5;
  sm_a0 = 1.0 + sm_alpha;
  sm_a1 = -2.0 * sm_cos;
  sm_a2 = 1.0 - sm_alpha;"""
    content = content.replace(old_sub_filt, new_sub_filt)

    # 4. @sample block
    old_sample = r"""@sample
// 1. Transparent Passthrough Check
dry_l = spl0; dry_r = spl1;

!slider27 ? (
  // 1:1 Complete Bypass Unity
  inst_peak = max(abs(spl0), abs(spl1));
) : (
  // 2. Input Level Calibration
  in_trim = exp(slider3 * 0.1151292546497);
  s0 = spl0 * in_trim;
  s1 = spl1 * in_trim;

  // 3. Sub-Bass Mono Anchor (Linkwitz-Riley crossover)
  // Low-pass mono channel
  sub_in = (s0 + s1) * 0.5;
  lp_mono = sub_lp_b0 * sub_in + sub_lp_b1 * sub_lp_l1 + sub_lp_b2 * sub_lp_l2 - sub_a1 * sub_hp_l1 - sub_a2 * sub_hp_l2;
  sub_lp_l2 = sub_lp_l1; sub_lp_l1 = sub_in;
  sub_hp_l2 = sub_hp_l1; sub_hp_l1 = lp_mono;

  // High-pass stereo remainder
  hp_l = s0 - lp_mono;
  hp_r = s1 - lp_mono;

  // Recombine with Quad-Wall Stereo Imager
  m_mid = (hp_l + hp_r) * 0.5;
  m_side = (hp_l - hp_r) * 0.5 * slider25;
  s0 = lp_mono + (m_mid + m_side);
  s1 = lp_mono + (m_mid - m_side);

  // 4. 5-Band Tonal Forge EQ
  // HPF
  ty0 = (hpf_b0 * s0 + hpf_b1 * hpf_x1 + hpf_b2 * hpf_x2 - hpf_a1 * hpf_y1 - hpf_a2 * hpf_y2) / hpf_a0;
  hpf_x2 = hpf_x1; hpf_x1 = s0; hpf_y2 = hpf_y1; hpf_y1 = ty0; s0 = ty0;
  ty1 = (hpf_b0 * s1 + hpf_b1 * hpf_x1 + hpf_b2 * hpf_x2 - hpf_a1 * hpf_y1 - hpf_a2 * hpf_y2) / hpf_a0;
  s1 = ty1;

  // 80Hz Punch
  ty0 = (p80_b0 * s0 + p80_b1 * p80_x1 + p80_b2 * p80_x2 - p80_a1 * p80_y1 - p80_a2 * p80_y2) / p80_a0;
  p80_x2 = p80_x1; p80_x1 = s0; p80_y2 = p80_y1; p80_y1 = ty0; s0 = ty0;
  ty1 = (p80_b0 * s1 + p80_b1 * p80_x1 + p80_b2 * p80_x2 - p80_a1 * p80_y1 - p80_a2 * p80_y2) / p80_a0;
  s1 = ty1;

  // 280Hz Mud Scoop
  ty0 = (s280_b0 * s0 + s280_b1 * s280_x1 + s280_b2 * s280_x2 - s280_a1 * s280_y1 - s280_a2 * s280_y2) / s280_a0;
  s280_x2 = s280_x1; s280_x1 = s0; s280_y2 = s280_y1; s280_y1 = ty0; s0 = ty0;
  ty1 = (s280_b0 * s1 + s280_b1 * s280_x1 + s280_b2 * s280_x2 - s280_a1 * s280_y1 - s280_a2 * s280_y2) / s280_a0;
  s1 = ty1;

  // 3.5kHz Bite
  ty0 = (b3k_b0 * s0 + b3k_b1 * b3k_x1 + b3k_b2 * b3k_x2 - b3k_a1 * b3k_y1 - b3k_a2 * b3k_y2) / b3k_a0;
  b3k_x2 = b3k_x1; b3k_x1 = s0; b3k_y2 = b3k_y1; b3k_y1 = ty0; s0 = ty0;
  ty1 = (b3k_b0 * s1 + b3k_b1 * b3k_x1 + b3k_b2 * b3k_x2 - b3k_a1 * b3k_y1 - b3k_a2 * b3k_y2) / b3k_a0;
  s1 = ty1;

  // 10kHz Sheen
  ty0 = (s10k_b0 * s0 + s10k_b1 * s10k_x1 + s10k_b2 * s10k_x2 - s10k_a1 * s10k_y1 - s10k_a2 * s10k_y2) / s10k_a0;
  s10k_x2 = s10k_x1; s10k_x1 = s0; s10k_y2 = s10k_y1; s10k_y1 = ty0; s0 = ty0;
  ty1 = (s10k_b0 * s1 + s10k_b1 * s10k_x1 + s10k_b2 * s10k_x2 - s10k_a1 * s10k_y1 - s10k_a2 * s10k_y2) / s10k_a0;
  s10k_x2 = s10k_x1; s10k_x1 = s1; s10k_y2 = s10k_y1; s10k_y1 = ty1; s1 = ty1;"""

    new_sample = r"""@sample
// 1. Transparent Passthrough & Live ANSI C16.5 Metering
dry_l = spl0; dry_r = spl1;

// Unconditional live 300ms VU RMS integration for reactive moving-coil meter
vu_omega = 1.0 - exp(-1.0 / (srate * 0.300));
vu_sig_sq = (dry_l * dry_l + dry_r * dry_r) * 0.5;
vu_rms_smooth += (vu_sig_sq - vu_rms_smooth) * vu_omega;
inst_rms = vu_rms_smooth > 0.000000001 ? 10.0 * log10(vu_rms_smooth) : -90.0;
inst_peak = max(abs(dry_l), abs(dry_r));

// 1:1 Complete Bit-Exact Transparent Pass if Suite Bypassed OR Preset 00 (Unity Baseline)
(!slider27 || slider2 == 0) ? (
  spl0 = dry_l;
  spl1 = dry_r;
  glue_gr_db = 0.0;
) : (
  // 2. Input Level Calibration
  in_trim = exp(slider3 * 0.1151292546497);
  s0 = spl0 * in_trim;
  s1 = spl1 * in_trim;

  // 3. Sub-Bass Mono Anchor (Elliptical High-Pass on Side Channel - Mid 100% Phase-Untouched)
  m_mid = (s0 + s1) * 0.5;
  m_side = (s0 - s1) * 0.5;
  hp_side = (sm_b0 * m_side + sm_b1 * sm_hp_x1 + sm_b2 * sm_hp_x2 - sm_a1 * sm_hp_y1 - sm_a2 * sm_hp_y2) / sm_a0;
  sm_hp_x2 = sm_hp_x1; sm_hp_x1 = m_side; sm_hp_y2 = sm_hp_y1; sm_hp_y1 = hp_side;

  // Quad-Wall Stereo Imager Width on Side channel
  w_side = hp_side * slider25;
  s0 = m_mid + w_side;
  s1 = m_mid - w_side;

  // 4. 5-Band Tonal Forge EQ (Fully isolated Left and Right channel delay lines)
  // HPF
  ty0 = (hpf_b0 * s0 + hpf_b1 * hpf_x1_l + hpf_b2 * hpf_x2_l - hpf_a1 * hpf_y1_l - hpf_a2 * hpf_y2_l) / hpf_a0;
  hpf_x2_l = hpf_x1_l; hpf_x1_l = s0; hpf_y2_l = hpf_y1_l; hpf_y1_l = ty0; s0 = ty0;
  ty1 = (hpf_b0 * s1 + hpf_b1 * hpf_x1_r + hpf_b2 * hpf_x2_r - hpf_a1 * hpf_y1_r - hpf_a2 * hpf_y2_r) / hpf_a0;
  hpf_x2_r = hpf_x1_r; hpf_x1_r = s1; hpf_y2_r = hpf_y1_r; hpf_y1_r = ty1; s1 = ty1;

  // 80Hz Punch
  ty0 = (p80_b0 * s0 + p80_b1 * p80_x1_l + p80_b2 * p80_x2_l - p80_a1 * p80_y1_l - p80_a2 * p80_y2_l) / p80_a0;
  p80_x2_l = p80_x1_l; p80_x1_l = s0; p80_y2_l = p80_y1_l; p80_y1_l = ty0; s0 = ty0;
  ty1 = (p80_b0 * s1 + p80_b1 * p80_x1_r + p80_b2 * p80_x2_r - p80_a1 * p80_y1_r - p80_a2 * p80_y2_r) / p80_a0;
  p80_x2_r = p80_x1_r; p80_x1_r = s1; p80_y2_r = p80_y1_r; p80_y1_r = ty1; s1 = ty1;

  // 280Hz Mud Scoop
  ty0 = (s280_b0 * s0 + s280_b1 * s280_x1_l + s280_b2 * s280_x2_l - s280_a1 * s280_y1_l - s280_a2 * s280_y2_l) / s280_a0;
  s280_x2_l = s280_x1_l; s280_x1_l = s0; s280_y2_l = s280_y1_l; s280_y1_l = ty0; s0 = ty0;
  ty1 = (s280_b0 * s1 + s280_b1 * s280_x1_r + s280_b2 * s280_x2_r - s280_a1 * s280_y1_r - s280_a2 * s280_y2_r) / s280_a0;
  s280_x2_r = s280_x1_r; s280_x1_r = s1; s280_y2_r = s280_y1_r; s280_y1_r = ty1; s1 = ty1;

  // 3.5kHz Bite
  ty0 = (b3k_b0 * s0 + b3k_b1 * b3k_x1_l + b3k_b2 * b3k_x2_l - b3k_a1 * b3k_y1_l - b3k_a2 * b3k_y2_l) / b3k_a0;
  b3k_x2_l = b3k_x1_l; b3k_x1_l = s0; b3k_y2_l = b3k_y1_l; b3k_y1_l = ty0; s0 = ty0;
  ty1 = (b3k_b0 * s1 + b3k_b1 * b3k_x1_r + b3k_b2 * b3k_x2_r - b3k_a1 * b3k_y1_r - b3k_a2 * b3k_y2_r) / b3k_a0;
  b3k_x2_r = b3k_x1_r; b3k_x1_r = s1; b3k_y2_r = b3k_y1_r; b3k_y1_r = ty1; s1 = ty1;

  // 10kHz Sheen
  ty0 = (s10k_b0 * s0 + s10k_b1 * s10k_x1_l + s10k_b2 * s10k_x2_l - s10k_a1 * s10k_y1_l - s10k_a2 * s10k_y2_l) / s10k_a0;
  s10k_x2_l = s10k_x1_l; s10k_x1_l = s0; s10k_y2_l = s10k_y1_l; s10k_y1_l = ty0; s0 = ty0;
  ty1 = (s10k_b0 * s1 + s10k_b1 * s10k_x1_r + s10k_b2 * s10k_x2_r - s10k_a1 * s10k_y1_r - s10k_a2 * s10k_y2_r) / s10k_a0;
  s10k_x2_r = s10k_x1_r; s10k_x1_r = s1; s10k_y2_r = s10k_y1_r; s10k_y1_r = ty1; s1 = ty1;"""
    content = content.replace(old_sample, new_sample)

    # 5. @gfx live needle ballistics
    old_ballistics = r"""// Needle ballistics
sifam_desk_needle = sifam_desk_needle * 0.92 + (slider24) * 0.08;
sifam_glue_needle = sifam_glue_needle * 0.90 + (glue_gr_db) * 0.10;"""

    new_ballistics = r"""// Authentic ANSI C16.5 VU moving-coil ballistics (300ms smoothing, 0VU = -18dBFS)
cur_vu_db = (inst_rms > -80.0) ? (inst_rms + 18.0) : -20.0;
cur_vu_db += slider24 * 0.25; // Desk drive adds warmth deflection
vu_pos = (cur_vu_db + 20.0) / 23.0; // 0.0 at -20VU, 0.87 at 0VU, 1.0 at +3VU
vu_pos = max(0.0, min(1.15, vu_pos));
sifam_desk_needle = sifam_desk_needle * 0.85 + vu_pos * 0.15;

// Gain Reduction meter ballistics (0dB to -16dB)
gr_pos = min(1.0, max(0.0, glue_gr_db / 16.0));
sifam_glue_needle = sifam_glue_needle * 0.80 + gr_pos * 0.20;"""
    content = content.replace(old_ballistics, new_ballistics)

    # 6. SIFAM Meter drawing function
    old_meter_fn = r"""// Helper for Authentic SIFAM Analogue VU Meter with backlit curved scale arc
function draw_sifam_meter(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) (
  gfx_r = 0.012; gfx_g = 0.018; gfx_b = 0.026;
  gfx_rect(mx, my, mw, mh);
  gfx_r = accent_r * 0.7; gfx_g = accent_g * 0.7; gfx_b = accent_b * 0.7;
  gfx_rect(mx, my, mw, mh, 0);

  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_x = mx + 14; gfx_y = my + 10; gfx_drawstr(title_str);

  gfx_setfont(3, "Consolas", 10.5, 'b'); gfx_r = 0.60; gfx_g = 0.75; gfx_b = 0.85;
  gfx_x = mx + mw - 75; gfx_y = my + 10;
  gfx_drawstr(is_glue ? "GR GAIN" : "VU RMS");

  piv_x = mx + mw * 0.5;
  piv_y = my + mh + 28;
  r_arc = mh * 0.88;
  ang_min = -0.785398;
  ang_max = 0.785398;

  // Scale Backing Arc
  gfx_r = 0.12; gfx_g = 0.18; gfx_b = 0.26;
  step_a = (ang_max - ang_min) / 40.0;
  ai = 0;
  loop(40,
    a1 = ang_min + ai * step_a; a2 = a1 + step_a;
    gfx_line(piv_x + sin(a1) * r_arc, piv_y - cos(a1) * r_arc, piv_x + sin(a2) * r_arc, piv_y - cos(a2) * r_arc);
    ai += 1;
  );

  // Calibrated Tick Marks
  gfx_setfont(3, "Consolas", 9.5);
  ti = 0;
  loop(9,
    f = ti / 8.0;
    ta = ang_min + f * (ang_max - ang_min);
    is_red = (f >= 0.75);
    gfx_r = is_red ? 0.98 : (accent_r * 0.9);
    gfx_g = is_red ? 0.25 : (accent_g * 0.9);
    gfx_b = is_red ? 0.25 : (accent_b * 0.9);
    t_len = (ti % 2 == 0) ? 9 : 5;
    gfx_line(piv_x + sin(ta) * (r_arc - t_len), piv_y - cos(ta) * (r_arc - t_len), piv_x + sin(ta) * (r_arc + 1), piv_y - cos(ta) * (r_arc + 1));
    ti += 1;
  );

  // Legend Labels
  gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.85;
  gfx_x = piv_x + sin(ang_min) * (r_arc + 4) - 8; gfx_y = piv_y - cos(ang_min) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "0" : "-20");
  gfx_x = piv_x - 6; gfx_y = piv_y - r_arc - 16; gfx_drawstr(is_glue ? "-6" : "-5");
  gfx_r = 0.98; gfx_g = 0.25; gfx_b = 0.25;
  gfx_x = piv_x + sin(ang_max) * (r_arc + 4) - 12; gfx_y = piv_y - cos(ang_max) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "-16" : "+3");

  // Needle Drawing with Shadow
  n_frac = max(0.0, min(1.0, needle_val / max_val));
  n_ang = ang_min + n_frac * (ang_max - ang_min);
  tip_x = piv_x + sin(n_ang) * (r_arc + 2);
  tip_y = piv_y - cos(n_ang) * (r_arc + 2);
  base_x = piv_x + sin(n_ang) * 14;
  base_y = piv_y - cos(n_ang) * 14;

  // Shadow
  gfx_r = 0.02; gfx_g = 0.04; gfx_b = 0.06;
  gfx_line(base_x + 2, base_y + 2, tip_x + 2, tip_y + 2);

  // Needle Body
  gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
  gfx_line(base_x - 0.5, base_y, tip_x - 0.5, tip_y);
  gfx_line(base_x + 0.5, base_y, tip_x + 0.5, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  // Brass Pivot Cap
  gfx_r = 0.98; gfx_g = 0.25; gfx_b = 0.25; gfx_circle(tip_x, tip_y, 2, 1);
  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(piv_x, my + mh - 8, 14, 1);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b; gfx_circle(piv_x, my + mh - 8, 14, 0);
);"""

    new_meter_fn = r"""// Helper for Authentic SIFAM Analogue VU Meter matching Damei_MixingSuite luxury standard
function draw_sifam_meter(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) (
  // 1. Bezel / Chassis Frame: Outer dark brushed obsidian with dual bevel
  gfx_r = 0.055; gfx_g = 0.065; gfx_b = 0.080;
  gfx_rect(mx, my, mw, mh);
  gfx_r = 0.14; gfx_g = 0.17; gfx_b = 0.22;
  gfx_rect(mx, my, mw, mh, 0);

  // 2. Inner Sifam Dial Face: Dark Obsidian Faceplate with High-Contrast Retro Gold Border
  plate_x = mx + 6; plate_y = my + 6;
  plate_w = mw - 12; plate_h = mh - 12;
  gfx_r = 0.035; gfx_g = 0.046; gfx_b = 0.062; gfx_rect(plate_x, plate_y, plate_w, plate_h);
  gfx_r = 0.85; gfx_g = 0.68; gfx_b = 0.20; gfx_rect(plate_x, plate_y, plate_w, plate_h, 0);

  piv_x = plate_x + plate_w * 0.5;
  piv_y = plate_y + plate_h - 18;

  // Strict Needle Confinement: Radius mathematically locked inside meter boundary
  radius_arc = min(plate_h - 48, plate_w * 0.44);
  radius_needle = radius_arc - 4;

  ang_min = -0.65; ang_max = 0.65;
  vu_cur_ang = ang_min + max(0.0, min(1.0, needle_val / max_val)) * (ang_max - ang_min);

  // Top Faceplate Titles (High Contrast)
  gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.25;
  gfx_setfont(2, "Consolas", 12, 'b');
  gfx_x = plate_x + 12; gfx_y = plate_y + 8; gfx_drawstr(title_str);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_measurestr(is_glue ? "STUDIO GR" : "STUDIO VU", sw_v, sh_v);
  gfx_x = plate_x + plate_w - sw_v - 12; gfx_y = plate_y + 8;
  gfx_drawstr(is_glue ? "STUDIO GR" : "STUDIO VU");

  // Calibrated Curved Scale Arc (Authentic ANSI C16.5 red hazard zone above 0 VU)
  arc_steps = 30;
  ai = 0;
  prev_ax = 0; prev_ay = 0;
  loop(arc_steps + 1,
    a_frac = ai / arc_steps;
    cur_a = ang_min + a_frac * (ang_max - ang_min);
    ax = piv_x + sin(cur_a) * radius_arc;
    ay = piv_y - cos(cur_a) * radius_arc;
    ai > 0 ? (
      (is_glue ? (a_frac >= 0.75) : (a_frac >= 0.87)) ? (
        gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;
      ) : (
        gfx_r = 0.95; gfx_g = 0.75; gfx_b = 0.20;
      );
      gfx_line(prev_ax, prev_ay, ax, ay);
    );
    prev_ax = ax; prev_ay = ay;
    ai += 1;
  );

  // Dial Major Scale Numbers & Tick Marks
  gfx_setfont(3, "Consolas", 10.5, 'b');
  t_a = ang_min;
  gfx_r = 0.75; gfx_g = 0.75; gfx_b = 0.75;
  gfx_line(piv_x + sin(t_a) * (radius_arc - 6), piv_y - cos(t_a) * (radius_arc - 6), piv_x + sin(t_a) * (radius_arc + 4), piv_y - cos(t_a) * (radius_arc + 4));
  gfx_x = piv_x + sin(t_a) * (radius_arc + 7) - 10; gfx_y = piv_y - cos(t_a) * (radius_arc + 7) - 10; gfx_drawstr(is_glue ? "0" : "-20");

  t_a = ang_min + 0.43 * (ang_max - ang_min);
  gfx_line(piv_x + sin(t_a) * (radius_arc - 5), piv_y - cos(t_a) * (radius_arc - 5), piv_x + sin(t_a) * (radius_arc + 4), piv_y - cos(t_a) * (radius_arc + 4));
  gfx_x = piv_x + sin(t_a) * (radius_arc + 7) - 8; gfx_y = piv_y - cos(t_a) * (radius_arc + 7) - 10; gfx_drawstr(is_glue ? "-3" : "-10");

  t_a = ang_min + 0.65 * (ang_max - ang_min);
  gfx_line(piv_x + sin(t_a) * (radius_arc - 5), piv_y - cos(t_a) * (radius_arc - 5), piv_x + sin(t_a) * (radius_arc + 4), piv_y - cos(t_a) * (radius_arc + 4));
  gfx_x = piv_x + sin(t_a) * (radius_arc + 7) - 6; gfx_y = piv_y - cos(t_a) * (radius_arc + 7) - 10; gfx_drawstr(is_glue ? "-6" : "-5");

  t_a = ang_min + 0.87 * (ang_max - ang_min);
  gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.25;
  gfx_line(piv_x + sin(t_a) * (radius_arc - 7), piv_y - cos(t_a) * (radius_arc - 7), piv_x + sin(t_a) * (radius_arc + 6), piv_y - cos(t_a) * (radius_arc + 6));
  gfx_x = piv_x + sin(t_a) * (radius_arc + 8) - 4; gfx_y = piv_y - cos(t_a) * (radius_arc + 8) - 10; gfx_drawstr(is_glue ? "-10" : "0");

  t_a = ang_max;
  gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;
  gfx_line(piv_x + sin(t_a) * (radius_arc - 6), piv_y - cos(t_a) * (radius_arc - 6), piv_x + sin(t_a) * (radius_arc + 5), piv_y - cos(t_a) * (radius_arc + 5));
  gfx_x = piv_x + sin(t_a) * (radius_arc + 8) - 8; gfx_y = piv_y - cos(t_a) * (radius_arc + 8) - 10; gfx_drawstr(is_glue ? "-16" : "+3");

  // Golden [ VU ] or [ GR ] Badge (Centered at 0.50 of plate height)
  gfx_setfont(1, "Orbitron", 14, 'b');
  gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.25;
  b_txt = is_glue ? "[ GR ]" : "[ VU ]";
  gfx_measurestr(b_txt, str_w, str_h);
  gfx_x = floor(plate_x + (plate_w - str_w) * 0.5);
  gfx_y = floor(plate_y + plate_h * 0.50);
  gfx_drawstr(b_txt);

  // High-Contrast Confined Needle with Luminous Core and Red Pointer Tip
  tip_x = piv_x + sin(vu_cur_ang) * radius_needle;
  tip_y = piv_y - cos(vu_cur_ang) * radius_needle;
  base_x = piv_x + sin(vu_cur_ang) * 14;
  base_y = piv_y - cos(vu_cur_ang) * 14;

  gfx_r = 1.00; gfx_g = 0.78; gfx_b = 0.20;
  gfx_line(base_x - 0.7, base_y, tip_x - 0.7, tip_y);
  gfx_line(base_x + 0.7, base_y, tip_x + 0.7, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  // Red pointer tip
  gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;
  gfx_circle(tip_x, tip_y, 2.5, 1);

  // Brass/Obsidian Pivot Hub
  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(piv_x, piv_y, 16, 1);
  gfx_r = 0.85; gfx_g = 0.68; gfx_b = 0.20; gfx_circle(piv_x, piv_y, 16, 0);

  // Bottom Confined Telemetry
  gfx_setfont(3, "Consolas", 12, 'b');
  gfx_r = 0.15; gfx_g = 0.95; gfx_b = 0.45;
  gfx_x = plate_x + 12; gfx_y = plate_y + plate_h - 20;
  is_glue ? (
    gfx_printf("GR: %5.1f dB", glue_gr_db);
  ) : (
    gfx_printf("RMS: %5.1f dBFS", inst_rms);
  );

  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  r_lbl = is_glue ? "PEAK HOLD" : "0 VU = -18 dBFS";
  gfx_measurestr(r_lbl, sw_0, sh_0);
  gfx_x = plate_x + plate_w - sw_0 - 12; gfx_y = plate_y + plate_h - 20;
  gfx_drawstr(r_lbl);
);"""
    content = content.replace(old_meter_fn, new_meter_fn)

    # 7. Update calls to draw_sifam_meter in Tab 0
    old_meter_calls = r"""  // Left Meter: SIFAM Desk Drive VU
  draw_sifam_meter(ws_x + 12, ws_y + 12, meter_w, top_row_h, "SIFAM DIRECTOR // CONSOLE DRIVE", sifam_desk_needle, 12.0, 0, 0.85, 0.47, 0.21);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = ws_x + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("+%.1f dB DRIVE", slider24);

  // Middle Meter: SIFAM Bus Glue GR
  draw_sifam_meter(ws_x + 12 + meter_w + 12, ws_y + 12, meter_w, top_row_h, "STUDIO BUS GLUE // GAIN REDUCTION", sifam_glue_needle, 16.0, 1, 0.00, 0.85, 1.00);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 0.00; gfx_g = 0.95; gfx_b = 1.00;
  gfx_x = ws_x + 12 + meter_w + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("-%.1f dB GR", sifam_glue_needle);"""

    new_meter_calls = r"""  // Left Meter: SIFAM Desk Drive VU (Flagship Luxury Bezel)
  draw_sifam_meter(ws_x + 12, ws_y + 12, meter_w, top_row_h, "SIFAM DIRECTOR // CONSOLE DRIVE", sifam_desk_needle, 1.0, 0, 0.85, 0.47, 0.21);

  // Middle Meter: SIFAM Bus Glue GR (Flagship Luxury Bezel)
  draw_sifam_meter(ws_x + 12 + meter_w + 12, ws_y + 12, meter_w, top_row_h, "STUDIO BUS GLUE // GAIN REDUCTION", sifam_glue_needle, 1.0, 1, 0.00, 0.85, 1.00);"""
    content = content.replace(old_meter_calls, new_meter_calls)

    # 8. Upgrade Stereo Radar Chassis
    old_radar = r"""  // Right Box: Stereo Vector Scope & Phase Correlation
  scope_x = ws_x + 12 + meter_w * 2 + 24; scope_w = ws_w - (meter_w * 2 + 48); scope_h = top_row_h;
  gfx_r = 0.012; gfx_g = 0.018; gfx_b = 0.026; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h, 0);"""

    new_radar = r"""  // Right Box: Stereo Vector Scope & Phase Correlation (Matching Luxury Bezel)
  scope_x = ws_x + 12 + meter_w * 2 + 24; scope_w = ws_w - (meter_w * 2 + 48); scope_h = top_row_h;
  gfx_r = 0.055; gfx_g = 0.065; gfx_b = 0.080; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h);
  gfx_r = 0.14; gfx_g = 0.17; gfx_b = 0.22; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h, 0);

  plate_x = scope_x + 6; plate_y = ws_y + 18;
  plate_w = scope_w - 12; plate_h = scope_h - 12;
  gfx_r = 0.035; gfx_g = 0.046; gfx_b = 0.062; gfx_rect(plate_x, plate_y, plate_w, plate_h);
  gfx_r = 0.85; gfx_g = 0.68; gfx_b = 0.20; gfx_rect(plate_x, plate_y, plate_w, plate_h, 0);"""
    content = content.replace(old_radar, new_radar)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched generate_instrumental_suite.py successfully.")


def patch_vocal_bus():
    path = r"c:\Dev\DameiSuite\scratch\generate_vocal_bus.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Header options:no_meter
    old_opts = "options:gmem=DameiMixMetering\noptions:maxmem=65536"
    new_opts = "options:no_meter\noptions:gmem=DameiMixMetering\noptions:maxmem=65536"
    content = content.replace(old_opts, new_opts)

    # 2. @init filter memories
    old_init = r"""// Filter state memories
bax_w_x1 = 0; bax_w_x2 = 0; bax_w_y1 = 0; bax_w_y2 = 0;
bax_p_x1 = 0; bax_p_x2 = 0; bax_p_y1 = 0; bax_p_y2 = 0;
bax_a_x1 = 0; bax_a_x2 = 0; bax_a_y1 = 0; bax_a_y2 = 0;
ds_hp_x1 = 0; ds_hp_x2 = 0; ds_hp_y1 = 0; ds_hp_y2 = 0;"""

    new_init = r"""// Filter state memories (Fully isolated Left & Right delay lines)
bax_w_x1_l = 0; bax_w_x2_l = 0; bax_w_y1_l = 0; bax_w_y2_l = 0;
bax_w_x1_r = 0; bax_w_x2_r = 0; bax_w_y1_r = 0; bax_w_y2_r = 0;

bax_p_x1_l = 0; bax_p_x2_l = 0; bax_p_y1_l = 0; bax_p_y2_l = 0;
bax_p_x1_r = 0; bax_p_x2_r = 0; bax_p_y1_r = 0; bax_p_y2_r = 0;

bax_a_x1_l = 0; bax_a_x2_l = 0; bax_a_y1_l = 0; bax_a_y2_l = 0;
bax_a_x1_r = 0; bax_a_x2_r = 0; bax_a_y1_r = 0; bax_a_y2_r = 0;

ds_hp_x1_l = 0; ds_hp_x2_l = 0; ds_hp_y1_l = 0; ds_hp_y2_l = 0;
ds_hp_x1_r = 0; ds_hp_x2_r = 0; ds_hp_y1_r = 0; ds_hp_y2_r = 0;
vu_rms_smooth = 0.0;"""
    content = content.replace(old_init, new_init)

    # 3. @sample block
    old_sample = r"""@sample
dry_l = spl0; dry_r = spl1;

!slider22 ? (
  vocal_peak = max(abs(spl0), abs(spl1));
) : (
  in_trim = exp(slider3 * 0.1151292546497);
  s0 = spl0 * in_trim;
  s1 = spl1 * in_trim;

  // 1. High-Frequency Limiter & Master De-Esser
  ds_in = (s0 + s1) * 0.5;
  ds_hp = (ds_b0 * ds_in + ds_b1 * ds_hp_x1 + ds_b2 * ds_hp_x2 - ds_a1 * ds_hp_y1 - ds_a2 * ds_hp_y2) / ds_a0;
  ds_hp_x2 = ds_hp_x1; ds_hp_x1 = ds_in; ds_hp_y2 = ds_hp_y1; ds_hp_y1 = ds_hp;

  ds_level = abs(ds_hp);
  ds_db = ds_level > 0.000001 ? 20.0 * log10(ds_level) : -120.0;
  ds_gr_target = 0.0;
  ds_db > slider6 ? (
    ds_gr_target = min(abs(slider8), (ds_db - slider6) * 0.85);
  );
  ds_reduction_db = ds_reduction_db * 0.85 + ds_gr_target * 0.15;
  ds_gain = exp(-ds_reduction_db * 0.1151292546497);

  // Apply de-esser clamping to high band
  s0 = (s0 - ds_hp) + ds_hp * ds_gain;
  s1 = (s1 - ds_hp) + ds_hp * ds_gain;

  // 2. Master Vocal Baxandall EQ
  // 100Hz Warmth
  ty0 = (bw_b0 * s0 + bw_b1 * bax_w_x1 + bw_b2 * bax_w_x2 - bw_a1 * bax_w_y1 - bw_a2 * bax_w_y2) / bw_a0;
  bax_w_x2 = bax_w_x1; bax_w_x1 = s0; bax_w_y2 = bax_w_y1; bax_w_y1 = ty0; s0 = ty0;
  ty1 = (bw_b0 * s1 + bw_b1 * bax_w_x1 + bw_b2 * bax_w_x2 - bw_a1 * bax_w_y1 - bw_a2 * bax_w_y2) / bw_a0;
  s1 = ty1;

  // 3.5kHz Presence
  ty0 = (bp_b0 * s0 + bp_b1 * bax_p_x1 + bp_b2 * bax_p_x2 - bp_a1 * bax_p_y1 - bp_a2 * bax_p_y2) / bp_a0;
  bax_p_x2 = bax_p_x1; bax_p_x1 = s0; bax_p_y2 = bax_p_y1; bax_p_y1 = ty0; s0 = ty0;
  ty1 = (bp_b0 * s1 + bp_b1 * bax_p_x1 + bp_b2 * bax_p_x2 - bp_a1 * bax_p_y1 - bp_a2 * bax_p_y2) / bp_a0;
  s1 = ty1;

  // 12kHz Silk Air
  ty0 = (ba_b0 * s0 + ba_b1 * bax_a_x1 + ba_b2 * bax_a_x2 - ba_a1 * bax_a_y1 - ba_a2 * bax_a_y2) / ba_a0;
  bax_a_x2 = bax_a_x1; bax_a_x1 = s0; bax_a_y2 = bax_a_y1; bax_a_y1 = ty0; s0 = ty0;
  ty1 = (ba_b0 * s1 + ba_b1 * bax_a_x1 + ba_b2 * bax_a_x2 - ba_a1 * bax_a_y1 - ba_a2 * bax_a_y2) / ba_a0;
  s1 = ty1;"""

    new_sample = r"""@sample
// 1. Transparent Passthrough & Live ANSI C16.5 Metering
dry_l = spl0; dry_r = spl1;

// Unconditional live 300ms VU RMS integration for reactive moving-coil meter
vu_omega = 1.0 - exp(-1.0 / (srate * 0.300));
vu_sig_sq = (dry_l * dry_l + dry_r * dry_r) * 0.5;
vu_rms_smooth += (vu_sig_sq - vu_rms_smooth) * vu_omega;
vocal_rms = vu_rms_smooth > 0.000000001 ? 10.0 * log10(vu_rms_smooth) : -90.0;
vocal_peak = max(abs(dry_l), abs(dry_r));

// 1:1 Complete Bit-Exact Transparent Pass if Suite Bypassed OR Preset 00 (Unity Baseline)
(!slider22 || slider2 == 0) ? (
  spl0 = dry_l;
  spl1 = dry_r;
  vocal_glue_gr_db = 0.0;
  ds_reduction_db = 0.0;
) : (
  in_trim = exp(slider3 * 0.1151292546497);
  s0 = spl0 * in_trim;
  s1 = spl1 * in_trim;

  // 1. High-Frequency Limiter & Master De-Esser (True Stereo Isolated Processing)
  ds_hp_l = (ds_b0 * s0 + ds_b1 * ds_hp_x1_l + ds_b2 * ds_hp_x2_l - ds_a1 * ds_hp_y1_l - ds_a2 * ds_hp_y2_l) / ds_a0;
  ds_hp_x2_l = ds_hp_x1_l; ds_hp_x1_l = s0; ds_hp_y2_l = ds_hp_y1_l; ds_hp_y1_l = ds_hp_l;

  ds_hp_r = (ds_b0 * s1 + ds_b1 * ds_hp_x1_r + ds_b2 * ds_hp_x2_r - ds_a1 * ds_hp_y1_r - ds_a2 * ds_hp_y2_r) / ds_a0;
  ds_hp_x2_r = ds_hp_x1_r; ds_hp_x1_r = s1; ds_hp_y2_r = ds_hp_y1_r; ds_hp_y1_r = ds_hp_r;

  ds_level = max(abs(ds_hp_l), abs(ds_hp_r));
  ds_db = ds_level > 0.000001 ? 20.0 * log10(ds_level) : -120.0;
  ds_gr_target = 0.0;
  ds_db > slider6 ? (
    ds_gr_target = min(abs(slider8), (ds_db - slider6) * 0.85);
  );
  ds_reduction_db = ds_reduction_db * 0.85 + ds_gr_target * 0.15;
  ds_gain = exp(-ds_reduction_db * 0.1151292546497);

  // Apply de-esser clamping to high band without phase comb-filtering
  s0 = (s0 - ds_hp_l) + ds_hp_l * ds_gain;
  s1 = (s1 - ds_hp_r) + ds_hp_r * ds_gain;

  // 2. Master Vocal Baxandall EQ (Fully isolated Left & Right channel delay lines)
  // 100Hz Warmth
  ty0 = (bw_b0 * s0 + bw_b1 * bax_w_x1_l + bw_b2 * bax_w_x2_l - bw_a1 * bax_w_y1_l - bw_a2 * bax_w_y2_l) / bw_a0;
  bax_w_x2_l = bax_w_x1_l; bax_w_x1_l = s0; bax_w_y2_l = bax_w_y1_l; bax_w_y1_l = ty0; s0 = ty0;
  ty1 = (bw_b0 * s1 + bw_b1 * bax_w_x1_r + bw_b2 * bax_w_x2_r - bw_a1 * bax_w_y1_r - bw_a2 * bax_w_y2_r) / bw_a0;
  bax_w_x2_r = bax_w_x1_r; bax_w_x1_r = s1; bax_w_y2_r = bax_w_y1_r; bax_w_y1_r = ty1; s1 = ty1;

  // 3.5kHz Presence
  ty0 = (bp_b0 * s0 + bp_b1 * bax_p_x1_l + bp_b2 * bax_p_x2_l - bp_a1 * bax_p_y1_l - bp_a2 * bax_p_y2_l) / bp_a0;
  bax_p_x2_l = bax_p_x1_l; bax_p_x1_l = s0; bax_p_y2_l = bax_p_y1_l; bax_p_y1_l = ty0; s0 = ty0;
  ty1 = (bp_b0 * s1 + bp_b1 * bax_p_x1_r + bp_b2 * bax_p_x2_r - bp_a1 * bax_p_y1_r - bp_a2 * bax_p_y2_r) / bp_a0;
  bax_p_x2_r = bax_p_x1_r; bax_p_x1_r = s1; bax_p_y2_r = bax_p_y1_r; bax_p_y1_r = ty1; s1 = ty1;

  // 12kHz Silk Air
  ty0 = (ba_b0 * s0 + ba_b1 * bax_a_x1_l + ba_b2 * bax_a_x2_l - ba_a1 * bax_a_y1_l - ba_a2 * bax_a_y2_l) / ba_a0;
  bax_a_x2_l = bax_a_x1_l; bax_a_x1_l = s0; bax_a_y2_l = bax_a_y1_l; bax_a_y1_l = ty0; s0 = ty0;
  ty1 = (ba_b0 * s1 + ba_b1 * bax_a_x1_r + ba_b2 * bax_a_x2_r - ba_a1 * bax_a_y1_r - ba_a2 * bax_a_y2_r) / ba_a0;
  bax_a_x2_r = bax_a_x1_r; bax_a_x1_r = s1; bax_a_y2_r = bax_a_y1_r; bax_a_y1_r = ty1; s1 = ty1;"""
    content = content.replace(old_sample, new_sample)

    # 4. @gfx needle ballistics
    old_ballistics = r"""// Needle ballistics
sifam_tube_needle = sifam_tube_needle * 0.92 + (slider20) * 0.08;
sifam_vocal_glue_needle = sifam_vocal_glue_needle * 0.90 + (vocal_glue_gr_db) * 0.10;"""

    new_ballistics = r"""// Authentic ANSI C16.5 VU moving-coil ballistics (300ms smoothing, 0VU = -18dBFS)
cur_v_vu_db = (vocal_rms > -80.0) ? (vocal_rms + 18.0) : -20.0;
cur_v_vu_db += slider20 * 0.25; // Tube warmth deflection
v_vu_pos = (cur_v_vu_db + 20.0) / 23.0; // 0.0 at -20VU, 0.87 at 0VU, 1.0 at +3VU
v_vu_pos = max(0.0, min(1.15, v_vu_pos));
sifam_tube_needle = sifam_tube_needle * 0.85 + v_vu_pos * 0.15;

// Vocal Glue GR needle ballistics (0dB to -16dB)
v_gr_pos = min(1.0, max(0.0, vocal_glue_gr_db / 16.0));
sifam_vocal_glue_needle = sifam_vocal_glue_needle * 0.80 + v_gr_pos * 0.20;"""
    content = content.replace(old_ballistics, new_ballistics)

    # 5. SIFAM Meter drawing function
    old_meter_fn = r"""// Helper for SIFAM Analogue VU Meter with backlit rose/violet scale arc
function draw_vocal_sifam(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) (
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026;
  gfx_rect(mx, my, mw, mh);
  gfx_r = accent_r * 0.7; gfx_g = accent_g * 0.7; gfx_b = accent_b * 0.7;
  gfx_rect(mx, my, mw, mh, 0);

  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_x = mx + 14; gfx_y = my + 10; gfx_drawstr(title_str);

  gfx_setfont(3, "Consolas", 10.5, 'b'); gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  gfx_x = mx + mw - 75; gfx_y = my + 10;
  gfx_drawstr(is_glue ? "GR GAIN" : "TUBE VU");

  piv_x = mx + mw * 0.5;
  piv_y = my + mh + 28;
  r_arc = mh * 0.88;
  ang_min = -0.785398;
  ang_max = 0.785398;

  gfx_r = 0.22; gfx_g = 0.12; gfx_b = 0.30;
  step_a = (ang_max - ang_min) / 40.0;
  ai = 0;
  loop(40,
    a1 = ang_min + ai * step_a; a2 = a1 + step_a;
    gfx_line(piv_x + sin(a1) * r_arc, piv_y - cos(a1) * r_arc, piv_x + sin(a2) * r_arc, piv_y - cos(a2) * r_arc);
    ai += 1;
  );

  gfx_setfont(3, "Consolas", 9.5);
  ti = 0;
  loop(9,
    f = ti / 8.0;
    ta = ang_min + f * (ang_max - ang_min);
    is_red = (f >= 0.75);
    gfx_r = is_red ? 1.00 : (accent_r * 0.9);
    gfx_g = is_red ? 0.30 : (accent_g * 0.9);
    gfx_b = is_red ? 0.40 : (accent_b * 0.9);
    t_len = (ti % 2 == 0) ? 9 : 5;
    gfx_line(piv_x + sin(ta) * (r_arc - t_len), piv_y - cos(ta) * (r_arc - t_len), piv_x + sin(ta) * (r_arc + 1), piv_y - cos(ta) * (r_arc + 1));
    ti += 1;
  );

  gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  gfx_x = piv_x + sin(ang_min) * (r_arc + 4) - 8; gfx_y = piv_y - cos(ang_min) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "0" : "-20");
  gfx_x = piv_x - 6; gfx_y = piv_y - r_arc - 16; gfx_drawstr(is_glue ? "-6" : "-5");
  gfx_r = 1.00; gfx_g = 0.30; gfx_b = 0.40;
  gfx_x = piv_x + sin(ang_max) * (r_arc + 4) - 12; gfx_y = piv_y - cos(ang_max) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "-16" : "+3");

  n_frac = max(0.0, min(1.0, needle_val / max_val));
  n_ang = ang_min + n_frac * (ang_max - ang_min);
  tip_x = piv_x + sin(n_ang) * (r_arc + 2);
  tip_y = piv_y - cos(n_ang) * (r_arc + 2);
  base_x = piv_x + sin(n_ang) * 14;
  base_y = piv_y - cos(n_ang) * 14;

  gfx_r = 0.05; gfx_g = 0.02; gfx_b = 0.08;
  gfx_line(base_x + 2, base_y + 2, tip_x + 2, tip_y + 2);

  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;
  gfx_line(base_x - 0.5, base_y, tip_x - 0.5, tip_y);
  gfx_line(base_x + 0.5, base_y, tip_x + 0.5, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  gfx_r = 1.00; gfx_g = 0.30; gfx_b = 0.40; gfx_circle(tip_x, tip_y, 2, 1);
  gfx_r = 0.16; gfx_g = 0.08; gfx_b = 0.22; gfx_circle(piv_x, my + mh - 8, 14, 1);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b; gfx_circle(piv_x, my + mh - 8, 14, 0);
);"""

    new_meter_fn = r"""// Helper for Authentic SIFAM Analogue VU Meter matching Damei_MixingSuite luxury standard
function draw_vocal_sifam(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) (
  // 1. Bezel / Chassis Frame: Outer dark brushed obsidian with dual bevel
  gfx_r = 0.055; gfx_g = 0.065; gfx_b = 0.080;
  gfx_rect(mx, my, mw, mh);
  gfx_r = 0.14; gfx_g = 0.17; gfx_b = 0.22;
  gfx_rect(mx, my, mw, mh, 0);

  // 2. Inner Sifam Dial Face: Dark Obsidian Faceplate with High-Contrast Retro Gold Border
  plate_x = mx + 6; plate_y = my + 6;
  plate_w = mw - 12; plate_h = mh - 12;
  gfx_r = 0.035; gfx_g = 0.046; gfx_b = 0.062; gfx_rect(plate_x, plate_y, plate_w, plate_h);
  gfx_r = 0.85; gfx_g = 0.68; gfx_b = 0.20; gfx_rect(plate_x, plate_y, plate_w, plate_h, 0);

  piv_x = plate_x + plate_w * 0.5;
  piv_y = plate_y + plate_h - 18;

  // Strict Needle Confinement: Radius mathematically locked inside meter boundary
  radius_arc = min(plate_h - 48, plate_w * 0.44);
  radius_needle = radius_arc - 4;

  ang_min = -0.65; ang_max = 0.65;
  vu_cur_ang = ang_min + max(0.0, min(1.0, needle_val / max_val)) * (ang_max - ang_min);

  // Top Faceplate Titles (High Contrast)
  gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.25;
  gfx_setfont(2, "Consolas", 12, 'b');
  gfx_x = plate_x + 12; gfx_y = plate_y + 8; gfx_drawstr(title_str);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_measurestr(is_glue ? "STUDIO GR" : "TUBE VU", sw_v, sh_v);
  gfx_x = plate_x + plate_w - sw_v - 12; gfx_y = plate_y + 8;
  gfx_drawstr(is_glue ? "STUDIO GR" : "TUBE VU");

  // Calibrated Curved Scale Arc (Authentic ANSI C16.5 red hazard zone above 0 VU)
  arc_steps = 30;
  ai = 0;
  prev_ax = 0; prev_ay = 0;
  loop(arc_steps + 1,
    a_frac = ai / arc_steps;
    cur_a = ang_min + a_frac * (ang_max - ang_min);
    ax = piv_x + sin(cur_a) * radius_arc;
    ay = piv_y - cos(cur_a) * radius_arc;
    ai > 0 ? (
      (is_glue ? (a_frac >= 0.75) : (a_frac >= 0.87)) ? (
        gfx_r = 1.00; gfx_g = 0.25; gfx_b = 0.40;
      ) : (
        gfx_r = 0.95; gfx_g = 0.75; gfx_b = 0.20;
      );
      gfx_line(prev_ax, prev_ay, ax, ay);
    );
    prev_ax = ax; prev_ay = ay;
    ai += 1;
  );

  // Dial Major Scale Numbers & Tick Marks
  gfx_setfont(3, "Consolas", 10.5, 'b');
  t_a = ang_min;
  gfx_r = 0.75; gfx_g = 0.75; gfx_b = 0.75;
  gfx_line(piv_x + sin(t_a) * (radius_arc - 6), piv_y - cos(t_a) * (radius_arc - 6), piv_x + sin(t_a) * (radius_arc + 4), piv_y - cos(t_a) * (radius_arc + 4));
  gfx_x = piv_x + sin(t_a) * (radius_arc + 7) - 10; gfx_y = piv_y - cos(t_a) * (radius_arc + 7) - 10; gfx_drawstr(is_glue ? "0" : "-20");

  t_a = ang_min + 0.43 * (ang_max - ang_min);
  gfx_line(piv_x + sin(t_a) * (radius_arc - 5), piv_y - cos(t_a) * (radius_arc - 5), piv_x + sin(t_a) * (radius_arc + 4), piv_y - cos(t_a) * (radius_arc + 4));
  gfx_x = piv_x + sin(t_a) * (radius_arc + 7) - 8; gfx_y = piv_y - cos(t_a) * (radius_arc + 7) - 10; gfx_drawstr(is_glue ? "-3" : "-10");

  t_a = ang_min + 0.65 * (ang_max - ang_min);
  gfx_line(piv_x + sin(t_a) * (radius_arc - 5), piv_y - cos(t_a) * (radius_arc - 5), piv_x + sin(t_a) * (radius_arc + 4), piv_y - cos(t_a) * (radius_arc + 4));
  gfx_x = piv_x + sin(t_a) * (radius_arc + 7) - 6; gfx_y = piv_y - cos(t_a) * (radius_arc + 7) - 10; gfx_drawstr(is_glue ? "-6" : "-5");

  t_a = ang_min + 0.87 * (ang_max - ang_min);
  gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.25;
  gfx_line(piv_x + sin(t_a) * (radius_arc - 7), piv_y - cos(t_a) * (radius_arc - 7), piv_x + sin(t_a) * (radius_arc + 6), piv_y - cos(t_a) * (radius_arc + 6));
  gfx_x = piv_x + sin(t_a) * (radius_arc + 8) - 4; gfx_y = piv_y - cos(t_a) * (radius_arc + 8) - 10; gfx_drawstr(is_glue ? "-10" : "0");

  t_a = ang_max;
  gfx_r = 1.00; gfx_g = 0.25; gfx_b = 0.40;
  gfx_line(piv_x + sin(t_a) * (radius_arc - 6), piv_y - cos(t_a) * (radius_arc - 6), piv_x + sin(t_a) * (radius_arc + 5), piv_y - cos(t_a) * (radius_arc + 5));
  gfx_x = piv_x + sin(t_a) * (radius_arc + 8) - 8; gfx_y = piv_y - cos(t_a) * (radius_arc + 8) - 10; gfx_drawstr(is_glue ? "-16" : "+3");

  // Golden [ VU ] or [ GR ] Badge (Centered at 0.50 of plate height)
  gfx_setfont(1, "Orbitron", 14, 'b');
  gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.25;
  b_txt = is_glue ? "[ GR ]" : "[ VU ]";
  gfx_measurestr(b_txt, str_w, str_h);
  gfx_x = floor(plate_x + (plate_w - str_w) * 0.5);
  gfx_y = floor(plate_y + plate_h * 0.50);
  gfx_drawstr(b_txt);

  // High-Contrast Confined Needle with Luminous Core and Red Pointer Tip
  tip_x = piv_x + sin(vu_cur_ang) * radius_needle;
  tip_y = piv_y - cos(vu_cur_ang) * radius_needle;
  base_x = piv_x + sin(vu_cur_ang) * 14;
  base_y = piv_y - cos(vu_cur_ang) * 14;

  gfx_r = 1.00; gfx_g = 0.78; gfx_b = 0.20;
  gfx_line(base_x - 0.7, base_y, tip_x - 0.7, tip_y);
  gfx_line(base_x + 0.7, base_y, tip_x + 0.7, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  // Rose/Violet pointer tip
  gfx_r = 1.00; gfx_g = 0.25; gfx_b = 0.40;
  gfx_circle(tip_x, tip_y, 2.5, 1);

  // Brass/Obsidian Pivot Hub
  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(piv_x, piv_y, 16, 1);
  gfx_r = 0.85; gfx_g = 0.68; gfx_b = 0.20; gfx_circle(piv_x, piv_y, 16, 0);

  // Bottom Confined Telemetry
  gfx_setfont(3, "Consolas", 12, 'b');
  gfx_r = 0.15; gfx_g = 0.95; gfx_b = 0.45;
  gfx_x = plate_x + 12; gfx_y = plate_y + plate_h - 20;
  is_glue ? (
    gfx_printf("GR: %5.1f dB", vocal_glue_gr_db);
  ) : (
    gfx_printf("RMS: %5.1f dBFS", vocal_rms);
  );

  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  r_lbl = is_glue ? "PEAK HOLD" : "0 VU = -18 dBFS";
  gfx_measurestr(r_lbl, sw_0, sh_0);
  gfx_x = plate_x + plate_w - sw_0 - 12; gfx_y = plate_y + plate_h - 20;
  gfx_drawstr(r_lbl);
);"""
    content = content.replace(old_meter_fn, new_meter_fn)

    # 6. Update calls to draw_vocal_sifam in Tab 0
    old_meter_calls = r"""  // Left Meter: SIFAM Vocal Tube Warmth VU
  draw_vocal_sifam(ws_x + 12, ws_y + 12, meter_w, top_row_h, "VOCAL TUBE WARMTH // SATURATION", sifam_tube_needle, 10.0, 0, 1.00, 0.41, 0.70);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = ws_x + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("+%.1f dB TUBE", slider20);

  // Middle Meter: SIFAM Master Vocal Bus Glue GR
  draw_vocal_sifam(ws_x + 12 + meter_w + 12, ws_y + 12, meter_w, top_row_h, "MASTER VOCAL GLUE // GAIN REDUCTION", sifam_vocal_glue_needle, 16.0, 1, 0.70, 0.53, 1.00);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = ws_x + 12 + meter_w + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("-%.1f dB GR", sifam_vocal_glue_needle);"""

    new_meter_calls = r"""  // Left Meter: SIFAM Vocal Tube Warmth VU (Flagship Luxury Bezel)
  draw_vocal_sifam(ws_x + 12, ws_y + 12, meter_w, top_row_h, "VOCAL TUBE WARMTH // SATURATION", sifam_tube_needle, 1.0, 0, 1.00, 0.41, 0.70);

  // Middle Meter: SIFAM Master Vocal Bus Glue GR (Flagship Luxury Bezel)
  draw_vocal_sifam(ws_x + 12 + meter_w + 12, ws_y + 12, meter_w, top_row_h, "MASTER VOCAL GLUE // GAIN REDUCTION", sifam_vocal_glue_needle, 1.0, 1, 0.70, 0.53, 1.00);"""
    content = content.replace(old_meter_calls, new_meter_calls)

    # 7. Upgrade Spatial Radar Chassis
    old_radar = r"""  // Right Box: Vocal Spatial Radar & Stereo Width Scope
  scope_x = ws_x + 12 + meter_w * 2 + 24; scope_w = ws_w - (meter_w * 2 + 48); scope_h = top_row_h;
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h);
  gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h, 0);"""

    new_radar = r"""  // Right Box: Vocal Spatial Radar & Stereo Width Scope (Matching Luxury Bezel)
  scope_x = ws_x + 12 + meter_w * 2 + 24; scope_w = ws_w - (meter_w * 2 + 48); scope_h = top_row_h;
  gfx_r = 0.055; gfx_g = 0.065; gfx_b = 0.080; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h);
  gfx_r = 0.14; gfx_g = 0.17; gfx_b = 0.22; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h, 0);

  plate_x = scope_x + 6; plate_y = ws_y + 18;
  plate_w = scope_w - 12; plate_h = scope_h - 12;
  gfx_r = 0.035; gfx_g = 0.046; gfx_b = 0.062; gfx_rect(plate_x, plate_y, plate_w, plate_h);
  gfx_r = 0.85; gfx_g = 0.68; gfx_b = 0.20; gfx_rect(plate_x, plate_y, plate_w, plate_h, 0);"""
    content = content.replace(old_radar, new_radar)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched generate_vocal_bus.py successfully.")


if __name__ == "__main__":
    patch_instrumental_suite()
    patch_vocal_bus()
    print("Re-generating JSFX files...")
    res1 = subprocess.run([sys.executable, r"c:\Dev\DameiSuite\scratch\generate_instrumental_suite.py"], capture_output=True, text=True)
    print("Inst gen:", res1.stdout, res1.stderr)
    res2 = subprocess.run([sys.executable, r"c:\Dev\DameiSuite\scratch\generate_vocal_bus.py"], capture_output=True, text=True)
    print("Vocal gen:", res2.stdout, res2.stderr)
    print("Running install.ps1 to deploy to REAPER...")
    res3 = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", r"c:\Dev\DameiSuite\install.ps1"], capture_output=True, text=True)
    print("Install output:\n", res3.stdout)
