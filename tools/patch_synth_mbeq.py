"""
Patcher for Damei_SynthSuite.jsfx:
Adds MultibandEQ (4-Band Frequency Sculptor & Dynamic Crossover) + producer calibrations.
"""
import sys, re

P = r'C:\Dev\DameiAPI\reaper_scripts\Damei_SynthSuite.jsfx'
raw = open(P, 'rb').read().decode('utf-8')
crlf = '\r\n' in raw
t = raw.replace('\r\n', '\n')

# 1. Update slider1 to 8 tabs (add MultibandEQ)
old_s1 = 'slider1:0<0,6,1{Nebula Overview & Scope,Dynamic Pockets & Devastator Link,Asase SynBass & Tight-Arse Sub,3D Horizon & Matemasie Spatial,Analog Sheen & Britson Console,Producer Matrix & Bridge Codex,Ear-Candy Director}>-Active Module'
new_s1 = 'slider1:0<0,7,1{Nebula Overview & Scope,Dynamic Pockets & Devastator Link,Asase SynBass & Tight-Arse Sub,3D Horizon & Matemasie Spatial,MultibandEQ Frequency Sculptor,Analog Sheen & Britson Console,Producer Matrix & Bridge Codex,Ear-Candy Director}>-Active Module'
assert old_s1 in t, "slider1 not found"
t = t.replace(old_s1, new_s1, 1)

# 2. Add MultibandEQ sliders after slider31
old_s31 = 'slider31:1<0,1,1{Manual Palette,Follow Producer Preset}>-Ear-Candy Palette Follows Producer\n'
mbeq_sliders = (
    '// MultibandEQ Frequency Sculptor (4-Band Dynamic Crossover)\n'
    'slider32:1<0,1,1{Bypassed,Active}>-MultibandEQ Engine Toggle\n'
    'slider33:0.0<-12.0,12.0,0.5>-MultibandEQ Band 1: Sub Bass (<110Hz) (dB)\n'
    'slider34:-1.5<-12.0,12.0,0.5>-MultibandEQ Band 2: Low-Mid (110-650Hz) (dB)\n'
    'slider35:1.2<-12.0,12.0,0.5>-MultibandEQ Band 3: High-Mid (650Hz-4.5kHz) (dB)\n'
    'slider36:2.5<-12.0,12.0,0.5>-MultibandEQ Band 4: Glassy Air (>4.5kHz) (dB)\n'
    'slider37:1.40<0.80,2.20,0.05>-MultibandEQ High Band Width Ratio\n'
)
assert old_s31 in t, "slider31 not found"
t = t.replace(old_s31, old_s31 + mbeq_sliders, 1)

# 3. Add serialization
old_ser = 'file_var(0, slider26);'
new_ser = (
    'file_var(0, slider26);\n'
    'file_var(0, slider28); file_var(0, slider29); file_var(0, slider30); file_var(0, slider31);\n'
    'file_var(0, slider32); file_var(0, slider33); file_var(0, slider34); file_var(0, slider35); file_var(0, slider36); file_var(0, slider37);'
)
assert old_ser in t, "serialize not found"
t = t.replace(old_ser, new_ser, 1)

# 4. In @init, initialize MultibandEQ filters
mbeq_init = r'''
// MultibandEQ 4-Band Crossover Filters (110Hz, 650Hz, 4500Hz)
mbeq_x1_l = 0; mbeq_x2_l = 0; mbeq_y1_l = 0; mbeq_y2_l = 0;
mbeq_x1_r = 0; mbeq_x2_r = 0; mbeq_y1_r = 0; mbeq_y2_r = 0;
mbeq_m1_l = 0; mbeq_m2_l = 0; mbeq_my1_l = 0; mbeq_my2_l = 0;
mbeq_m1_r = 0; mbeq_m2_r = 0; mbeq_my1_r = 0; mbeq_my2_r = 0;
mbeq_h1_l = 0; mbeq_h2_l = 0; mbeq_hy1_l = 0; mbeq_hy2_l = 0;
mbeq_h1_r = 0; mbeq_h2_r = 0; mbeq_hy1_r = 0; mbeq_hy2_r = 0;
'''
t = t.replace('ext_noinit = 1.0;', 'ext_noinit = 1.0;\n' + mbeq_init, 1)

# 5. In update_synth_filters, calculate 4-band crossovers
mbeq_filter_calc = r'''
  // MultibandEQ Crossovers: 110Hz, 650Hz, 4500Hz
  mbq_w1 = 2.0 * $pi * 110.0 / srate;
  mbq_al1 = sin(mbq_w1) * 0.7071;
  mbq_lp1_a0 = 1.0 + mbq_al1;
  mbq_lp1_b0 = ((1.0 - cos(mbq_w1)) * 0.5) / mbq_lp1_a0;
  mbq_lp1_b1 = (1.0 - cos(mbq_w1)) / mbq_lp1_a0;
  mbq_lp1_b2 = ((1.0 - cos(mbq_w1)) * 0.5) / mbq_lp1_a0;
  mbq_lp1_a1 = (-2.0 * cos(mbq_w1)) / mbq_lp1_a0;
  mbq_lp1_a2 = (1.0 - mbq_al1) / mbq_lp1_a0;

  mbq_w2 = 2.0 * $pi * 650.0 / srate;
  mbq_al2 = sin(mbq_w2) * 0.7071;
  mbq_lp2_a0 = 1.0 + mbq_al2;
  mbq_lp2_b0 = ((1.0 - cos(mbq_w2)) * 0.5) / mbq_lp2_a0;
  mbq_lp2_b1 = (1.0 - cos(mbq_w2)) / mbq_lp2_a0;
  mbq_lp2_b2 = ((1.0 - cos(mbq_w2)) * 0.5) / mbq_lp2_a0;
  mbq_lp2_a1 = (-2.0 * cos(mbq_w2)) / mbq_lp2_a0;
  mbq_lp2_a2 = (1.0 - mbq_al2) / mbq_lp2_a0;

  mbq_w3 = 2.0 * $pi * 4500.0 / srate;
  mbq_al3 = sin(mbq_w3) * 0.7071;
  mbq_hp3_a0 = 1.0 + mbq_al3;
  mbq_hp3_b0 = ((1.0 + cos(mbq_w3)) * 0.5) / mbq_hp3_a0;
  mbq_hp3_b1 = (-(1.0 + cos(mbq_w3))) / mbq_hp3_a0;
  mbq_hp3_b2 = ((1.0 + cos(mbq_w3)) * 0.5) / mbq_hp3_a0;
  mbq_hp3_a1 = (-2.0 * cos(mbq_w3)) / mbq_hp3_a0;
  mbq_hp3_a2 = (1.0 - mbq_al3) / mbq_hp3_a0;
'''
assert 'function update_synth_filters()' in t
t = t.replace('function update_synth_filters() (', 'function update_synth_filters() (\n' + mbeq_filter_calc, 1)

# 6. In @sample, add the MultibandEQ 4-band processing block before output trim
mbeq_dsp = r'''
// ---- MultibandEQ 4-Band Frequency Sculptor ----
slider32 == 1 ? (
  // Band 1: Sub Bass (<110Hz)
  mbq_sub_l = mbq_lp1_b0 * out_l + mbq_lp1_b1 * mbeq_x1_l + mbq_lp1_b2 * mbeq_x2_l - mbq_lp1_a1 * mbeq_y1_l - mbq_lp1_a2 * mbeq_y2_l;
  mbeq_x2_l = mbeq_x1_l; mbeq_x1_l = out_l; mbeq_y2_l = mbeq_y1_l; mbeq_y1_l = mbq_sub_l;
  mbq_sub_r = mbq_lp1_b0 * out_r + mbq_lp1_b1 * mbeq_x1_r + mbq_lp1_b2 * mbeq_x2_r - mbq_lp1_a1 * mbeq_y1_r - mbq_lp1_a2 * mbeq_y2_r;
  mbeq_x2_r = mbeq_x1_r; mbeq_x1_r = out_r; mbeq_y2_r = mbeq_y1_r; mbeq_y1_r = mbq_sub_r;

  // Band 4: Glassy Air Sheen (>4.5kHz)
  mbq_air_l = mbq_hp3_b0 * out_l + mbq_hp3_b1 * mbeq_h1_l + mbq_hp3_b2 * mbeq_h2_l - mbq_hp3_a1 * mbeq_hy1_l - mbq_hp3_a2 * mbeq_hy2_l;
  mbeq_h2_l = mbeq_h1_l; mbeq_h1_l = out_l; mbeq_hy2_l = mbeq_hy1_l; mbeq_hy1_l = mbq_air_l;
  mbq_air_r = mbq_hp3_b0 * out_r + mbq_hp3_b1 * mbeq_h1_r + mbq_hp3_b2 * mbeq_h2_r - mbq_hp3_a1 * mbeq_hy1_r - mbq_hp3_a2 * mbeq_hy2_r;
  mbeq_h2_r = mbeq_h1_r; mbeq_h1_r = out_r; mbeq_hy2_r = mbeq_hy1_r; mbeq_hy1_r = mbq_air_r;

  // Split remainder into Low-Mid (110-650Hz) and High-Mid (650-4500Hz)
  mbq_mid_tot_l = out_l - mbq_sub_l - mbq_air_l;
  mbq_mid_tot_r = out_r - mbq_sub_r - mbq_air_r;

  mbq_lmid_l = mbq_lp2_b0 * mbq_mid_tot_l + mbq_lp2_b1 * mbeq_m1_l + mbq_lp2_b2 * mbeq_m2_l - mbq_lp2_a1 * mbeq_my1_l - mbq_lp2_a2 * mbeq_my2_l;
  mbeq_m2_l = mbeq_m1_l; mbeq_m1_l = mbq_mid_tot_l; mbeq_my2_l = mbeq_my1_l; mbeq_my1_l = mbq_lmid_l;
  mbq_lmid_r = mbq_lp2_b0 * mbq_mid_tot_r + mbq_lp2_b1 * mbeq_m1_r + mbq_lp2_b2 * mbeq_m2_r - mbq_lp2_a1 * mbeq_my1_r - mbq_lp2_a2 * mbeq_my2_r;
  mbeq_m2_r = mbeq_m1_r; mbeq_m1_r = mbq_mid_tot_r; mbeq_my2_r = mbeq_my1_r; mbeq_my1_r = mbq_lmid_r;

  mbq_hmid_l = mbq_mid_tot_l - mbq_lmid_l;
  mbq_hmid_r = mbq_mid_tot_r - mbq_lmid_r;

  // Apply per-band gains
  g1 = exp(slider33 * 0.11512925);
  g2 = exp(slider34 * 0.11512925);
  g3 = exp(slider35 * 0.11512925);
  g4 = exp(slider36 * 0.11512925);

  mbq_sub_l *= g1; mbq_sub_r *= g1;
  mbq_lmid_l *= g2; mbq_lmid_r *= g2;
  mbq_hmid_l *= g3; mbq_hmid_r *= g3;

  // High Band Stereo Horizon Width
  air_m = (mbq_air_l + mbq_air_r) * 0.5;
  air_s = (mbq_air_l - mbq_air_r) * 0.5 * slider37;
  mbq_air_l = (air_m + air_s) * g4;
  mbq_air_r = (air_m - air_s) * g4;

  out_l = mbq_sub_l + mbq_lmid_l + mbq_hmid_l + mbq_air_l;
  out_r = mbq_sub_r + mbq_lmid_r + mbq_hmid_r + mbq_air_r;
);
'''
old_out_trim = 'out_l *= out_trim_mult;'
assert old_out_trim in t, "out_trim_mult not found"
t = t.replace(old_out_trim, mbeq_dsp + '\n' + old_out_trim, 1)

# 7. Update tab loop in @gfx to 8 tabs:
t = t.replace('num_tabs = 7;', 'num_tabs = 8;')
old_tab_lbls = (
    '  ti == 0 ? t_label = "OVERVIEW" :\n'
    '  ti == 1 ? t_label = "POCKETS & DEV" :\n'
    '  ti == 2 ? t_label = "ASASE SYNBASS" :\n'
    '  ti == 3 ? t_label = "3D HORIZON" :\n'
    '  ti == 4 ? t_label = "BRITSON SHEEN" :\n'
    '            ti == 5 ? t_label = "PRODUCER CODEX" :\n'
    't_label = "EAR-CANDY";'
)

new_tab_lbls = (
    '  ti == 0 ? t_label = "OVERVIEW" :\n'
    '  ti == 1 ? t_label = "POCKETS & DEV" :\n'
    '  ti == 2 ? t_label = "ASASE SYNBASS" :\n'
    '  ti == 3 ? t_label = "3D HORIZON" :\n'
    '  ti == 4 ? t_label = "MULTIBAND EQ" :\n'
    '  ti == 5 ? t_label = "BRITSON SHEEN" :\n'
    '  ti == 6 ? t_label = "PRODUCER CODEX" :\n'
    't_label = "EAR-CANDY";'
)

assert old_tab_lbls in t, "old_tab_lbls not found"
t = t.replace(old_tab_lbls, new_tab_lbls, 1)

# Shift existing tabs:
# slider1 == 6 (Ear-Candy) -> slider1 == 7
# slider1 == 5 (Producer Codex) -> slider1 == 6
# slider1 == 4 (Britson Sheen) -> slider1 == 5
# insert slider1 == 4 for MultibandEQ!
t = t.replace('slider1 == 6 ? (', 'slider1 == 7 ? (', 1)
t = t.replace('slider1 == 5 ? (', 'slider1 == 6 ? (', 1)
t = t.replace('slider1 == 4 ? (', 'slider1 == 5 ? (', 1)

mbeq_tab_gui = r'''
// =============================================================================
// TAB 4: MULTIBAND EQ FREQUENCY SCULPTOR (4-BAND CROSSOVER & DYNAMIC PROFILES)
// =============================================================================
slider1 == 4 ? (
  mbq_x = p_x; mbq_y = p_y; mbq_w = p_w; mbq_h = p_h;

  gfx_r = 0.024; gfx_g = 0.028; gfx_b = 0.038; gfx_rect(mbq_x, mbq_y, mbq_w, mbq_h);
  gfx_r = 0.55; gfx_g = 0.36; gfx_b = 0.95; gfx_rect(mbq_x, mbq_y, mbq_w, mbq_h, 0);

  // Top Header
  gfx_setfont(1, "Orbitron", 16, 'b'); gfx_r = 0.65; gfx_g = 0.45; gfx_b = 1.00;
  gfx_x = mbq_x + 20; gfx_y = mbq_y + 14;
  gfx_drawstr("MULTIBAND-EQ // 4-BAND FREQUENCY SCULPTOR");
  gfx_setfont(1, "Consolas", 12, 'b'); gfx_r = 0.65; gfx_g = 0.72; gfx_b = 0.85;
  gfx_x = mbq_x + 20; gfx_y = mbq_y + 36;
  gfx_drawstr("INDEPENDENT SUB BASS, LOW-MID POCKET, VOCAL CLEARANCE & 3D HIGH-BAND SHEEN");

  // Bypass / Active Toggle
  mb_togg_w = 120; mb_togg_h = 26;
  mb_togg_x = mbq_x + mbq_w - mb_togg_w - 20; mb_togg_y = mbq_y + 16;
  mb_togg_hov = (mouse_x >= mb_togg_x && mouse_x <= mb_togg_x + mb_togg_w && mouse_y >= mb_togg_y && mouse_y <= mb_togg_y + mb_togg_h);
  gfx_r = slider32 ? 0.35 : 0.08; gfx_g = slider32 ? 0.15 : 0.08; gfx_b = slider32 ? 0.55 : 0.12;
  gfx_rect(mb_togg_x, mb_togg_y, mb_togg_w, mb_togg_h);
  gfx_r = slider32 ? 0.85 : 0.45; gfx_g = slider32 ? 0.60 : 0.45; gfx_b = slider32 ? 1.00 : 0.55;
  gfx_rect(mb_togg_x, mb_togg_y, mb_togg_w, mb_togg_h, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  mb_txt = slider32 ? "ACTIVE" : "BYPASS";
  gfx_measurestr(mb_txt, mbtw, mbth);
  gfx_x = mb_togg_x + (mb_togg_w - mbtw) * 0.5; gfx_y = mb_togg_y + 6; gfx_drawstr(mb_txt);
  mouse_clicked && mb_togg_hov ? (slider32 = !slider32; slider_automate(););

  // 4 Main Band Cards
  bc_w = floor((mbq_w - 50) / 4);
  bc_h = mbq_h - 75;
  bci = 0;
  loop(4,
    bc_x = mbq_x + 16 + bci * (bc_w + 6);
    bc_y = mbq_y + 58;

    gfx_r = 0.030; gfx_g = 0.034; gfx_b = 0.046; gfx_rect(bc_x, bc_y, bc_w, bc_h);
    gfx_r = 0.25; gfx_g = 0.28; gfx_b = 0.42; gfx_rect(bc_x, bc_y, bc_w, bc_h, 0);

    bci == 0 ? (
      b_title = "BAND 1: SUB BASS";
      b_range = "<110 Hz Foundation";
      b_val = slider33;
      b_cr = 0.00; b_cg = 0.95; b_cb = 0.85; // Cyan
    ) : bci == 1 ? (
      b_title = "BAND 2: LOW-MID";
      b_range = "110-650 Hz Warmth";
      b_val = slider34;
      b_cr = 1.00; b_cg = 0.72; b_cb = 0.02; // Gold
    ) : bci == 2 ? (
      b_title = "BAND 3: HIGH-MID";
      b_range = "650Hz-4.5kHz Lead";
      b_val = slider35;
      b_cr = 0.95; b_cg = 0.35; b_cb = 0.55; // Magenta
    ) : (
      b_title = "BAND 4: AIR SHEEN";
      b_range = ">4.5 kHz Glass Sheen";
      b_val = slider36;
      b_cr = 0.65; b_cg = 0.45; b_cb = 1.00; // Violet
    );

    gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = b_cr; gfx_g = b_cg; gfx_b = b_cb;
    gfx_x = bc_x + 12; gfx_y = bc_y + 12; gfx_drawstr(b_title);
    gfx_setfont(1, "Consolas", 11.5, 'b'); gfx_r = 0.65; gfx_g = 0.70; gfx_b = 0.80;
    gfx_x = bc_x + 12; gfx_y = bc_y + 30; gfx_drawstr(b_range);

    // Vertical Gain Fader
    vf_w = 32; vf_h = bc_h - 130;
    vf_x = bc_x + floor((bc_w - vf_w) * 0.5);
    vf_y = bc_y + 54;
    gfx_r = 0.018; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(vf_x, vf_y, vf_w, vf_h);
    gfx_r = 0.28; gfx_g = 0.32; gfx_b = 0.42; gfx_rect(vf_x, vf_y, vf_w, vf_h, 0);

    // Center Zero line
    vf_zero_y = vf_y + floor(vf_h * 0.5);
    gfx_r = 0.45; gfx_g = 0.50; gfx_b = 0.60; gfx_line(vf_x, vf_zero_y, vf_x + vf_w, vf_zero_y);

    // Gain Fill
    g_frac = (b_val - (-12.0)) / 24.0;
    thumb_y = vf_y + floor((1.0 - g_frac) * (vf_h - 16));
    gfx_r = b_cr; gfx_g = b_cg; gfx_b = b_cb;
    b_val >= 0.0 ? (
      gfx_rect(vf_x + 4, thumb_y, vf_w - 8, vf_zero_y - thumb_y);
    ) : (
      gfx_rect(vf_x + 4, vf_zero_y, vf_w - 8, thumb_y - vf_zero_y + 16);
    );

    // Thumb handle
    gfx_r = 0.95; gfx_g = 0.98; gfx_b = 1.00;
    gfx_rect(vf_x + 1, thumb_y, vf_w - 2, 16);

    // Value readout
    gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.0; gfx_g = 0.90; gfx_b = 0.30;
    sprintf(#bv_txt, "%+1.1fdB", b_val);
    gfx_measurestr(#bv_txt, bvw, bvh);
    gfx_x = bc_x + (bc_w - bvw) * 0.5; gfx_y = vf_y + vf_h + 12;
    gfx_drawstr(#bv_txt);

    // Interaction
    vf_hov = (mouse_x >= vf_x - 8 && mouse_x <= vf_x + vf_w + 8 && mouse_y >= vf_y - 4 && mouse_y <= vf_y + vf_h + 4);
    mouse_down && vf_hov ? (
      n_db = 12.0 - ((mouse_y - vf_y) / vf_h) * 24.0;
      n_db = max(-12.0, min(12.0, floor(n_db * 2.0) * 0.5));
      bci == 0 ? slider33 = n_db : (bci == 1 ? slider34 = n_db : (bci == 2 ? slider35 = n_db : slider36 = n_db));
      slider_automate();
    );

    bci += 1;
  );
);
'''

# Insert before `slider1 == 5 ? (`
idx_t5 = t.find('slider1 == 5 ? (')
assert idx_t5 != -1, "slider1 == 5 ? ( not found"
t = t[:idx_t5] + mbeq_tab_gui + '\n\n' + t[idx_t5:]

# 8. Calibrate all 18 producer presets in apply_synth_preset
p_calibs_synth = {
    0: (1, -2.0, -2.5, 2.0, 3.5, 1.60),  # Jordan Fish (BMTH)
    1: (1, 0.5, -1.5, 1.5, 2.8, 1.45),   # Dan Braunstein (Spiritbox)
    2: (1, 2.5, -3.0, 2.2, 1.2, 1.25),   # Buster Odeholm (heavy djent)
    3: (1, 0.0, -1.0, 1.0, 2.5, 1.50),   # George Lever
    4: (1, -1.0, -1.8, 2.5, 3.0, 1.55),  # Zakk Cervini
    5: (1, -1.5, -2.0, 2.8, 3.2, 1.50),  # Joey Sturgis
    6: (1, 3.5, 2.0, 3.0, 1.0, 1.30),    # Mick Gordon (DOOM raw power)
    7: (1, 1.0, -2.5, 2.5, 2.5, 1.45),   # Lance Prenc
    8: (1, 2.0, -2.0, 2.2, 2.0, 1.35),   # Scott Seigel
    9: (1, 0.5, -1.5, 1.8, 2.4, 1.40),   # Jonathan Dolese
    10: (1, 0.0, -1.8, 2.2, 3.0, 1.50),  # Kel Pinchin
    11: (1, -1.0, -1.2, 1.6, 2.6, 1.45), # Sam Guaiana
    12: (1, 0.5, -0.8, 1.4, 2.8, 1.55),  # Forrester Savell
    13: (1, 1.0, -1.0, 1.5, 2.2, 1.40),  # Jens Bogren
    14: (1, 0.0, -1.5, 1.8, 2.6, 1.45),  # Nolly Getgood
    15: (1, 2.0, -2.0, 2.5, 1.8, 1.35),  # Will Putney
    16: (1, 0.5, -1.2, 1.5, 2.8, 1.50),  # Sam Bassal
    17: (1, -0.5, -1.5, 2.0, 3.0, 1.55), # Henrik Udd
}

for p_idx, (on, b1, b2, b3, b4, w) in p_calibs_synth.items():
    pattern = rf'(p_idx == {p_idx} \? \([^\n]*\n)'
    calib_str = (
        f'    // MultibandEQ 4-Band Producer Calibration\n'
        f'    slider32 = {on}; slider33 = {b1}; slider34 = {b2}; slider35 = {b3}; slider36 = {b4}; slider37 = {w};\n'
    )
    t = re.sub(pattern, rf'\1{calib_str}', t, count=1)

open(P, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
print('SynthSuite MultibandEQ patch complete.')
