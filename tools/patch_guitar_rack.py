"""
Patcher for Damei_GuitarSuite.jsfx:
Adds ReEQ, Comp, MultiBand-Comp, and Saturation studio rack + producer calibrations.
"""
import sys, re

P = r'C:\Dev\DameiAPI\reaper_scripts\Damei_GuitarSuite.jsfx'
raw = open(P, 'rb').read().decode('utf-8')
crlf = '\r\n' in raw
t = raw.replace('\r\n', '\n')

# 1. Update Tab 4 label in slider1
old_s1 = 'slider1:0<0,6,1{Guitar Wall Overview,Dynamic Chug Sculptor,Harshness & De-Fizz Tamer,Quad-Wall Stereo Imager,Analog Console & Tape Glue,Producer Matrix & Session Tips,Ear-Candy Director}>-Active Module'
new_s1 = 'slider1:0<0,6,1{Guitar Wall Overview,Dynamic Chug Sculptor,Harshness & De-Fizz Tamer,Quad-Wall Stereo Imager,ReEQ & MultiBand-Comp Rack,Producer Matrix & Session Tips,Ear-Candy Director}>-Active Module'
assert old_s1 in t, "slider1 not found"
t = t.replace(old_s1, new_s1, 1)

# 2. Add MultiBand-Comp sliders
old_s51 = 'slider51:1<0,1,1{Manual Palette,Follow Producer Preset}>-Ear-Candy Palette Follows Producer\n'
mb_sliders = (
    '// ReEQ, Comp, MultiBand-Comp & Saturation Studio Rack\n'
    'slider52:1<0,1,1{Bypassed,Active}>-MultiBand-Comp Engine Toggle\n'
    'slider53:35<0,100,1>-MultiBand Low Chug Clamp (%) [<220Hz]\n'
    'slider54:25<0,100,1>-MultiBand Mid Crunch Punch (%) [220Hz-3.2kHz]\n'
    'slider55:28<0,100,1>-MultiBand High Fizz Tamer (%) [>3.2kHz]\n'
    'slider56:2.5<1.0,8.0,0.5>-MultiBand Comp Ratio\n'
)
assert old_s51 in t, "slider51 not found"
t = t.replace(old_s51, old_s51 + mb_sliders, 1)

# 3. Add serialization
old_ser = 'file_var(0, slider46);'
new_ser = (
    'file_var(0, slider46);\n'
    'file_var(0, slider48); file_var(0, slider49); file_var(0, slider50); file_var(0, slider51);\n'
    'file_var(0, slider52); file_var(0, slider53); file_var(0, slider54); file_var(0, slider55); file_var(0, slider56);'
)
assert old_ser in t, "serialize not found"
t = t.replace(old_ser, new_ser, 1)

# 4. In @init, initialize MultiBand-Comp variables
mb_init = r'''
// MultiBand-Comp State & Filters (<220Hz, 220-3.2kHz, >3.2kHz)
mb_gr_low = 0.0; mb_gr_mid = 0.0; mb_gr_hi = 0.0;
mb_meter_low = 0.0; mb_meter_mid = 0.0; mb_meter_hi = 0.0;
mb_low_lx1 = 0; mb_low_lx2 = 0; mb_low_ly1 = 0; mb_low_ly2 = 0;
mb_low_rx1 = 0; mb_low_rx2 = 0; mb_low_ry1 = 0; mb_low_ry2 = 0;
mb_hi_lx1 = 0; mb_hi_lx2 = 0; mb_hi_ly1 = 0; mb_hi_ly2 = 0;
mb_hi_rx1 = 0; mb_hi_rx2 = 0; mb_hi_ry1 = 0; mb_hi_ry2 = 0;
'''
t = t.replace('ext_noinit = 1.0;', 'ext_noinit = 1.0;\n' + mb_init, 1)

# 5. In update_guitar_filters, calculate 2-way Linkwitz-Riley crossovers for 220Hz and 3200Hz
mb_filter_calc = r'''
  // MultiBand Crossover 1: 220Hz (Low Chug boundary)
  mb_w1 = 2.0 * $pi * 220.0 / srate;
  mb_al1 = sin(mb_w1) * 0.7071;
  mb_lp1_a0 = 1.0 + mb_al1;
  mb_lp1_b0 = ((1.0 - cos(mb_w1)) * 0.5) / mb_lp1_a0;
  mb_lp1_b1 = (1.0 - cos(mb_w1)) / mb_lp1_a0;
  mb_lp1_b2 = ((1.0 - cos(mb_w1)) * 0.5) / mb_lp1_a0;
  mb_lp1_a1 = (-2.0 * cos(mb_w1)) / mb_lp1_a0;
  mb_lp1_a2 = (1.0 - mb_al1) / mb_lp1_a0;

  // MultiBand Crossover 2: 3200Hz (High Fizz boundary)
  mb_w2 = 2.0 * $pi * 3200.0 / srate;
  mb_al2 = sin(mb_w2) * 0.7071;
  mb_hp2_a0 = 1.0 + mb_al2;
  mb_hp2_b0 = ((1.0 + cos(mb_w2)) * 0.5) / mb_hp2_a0;
  mb_hp2_b1 = (-(1.0 + cos(mb_w2))) / mb_hp2_a0;
  mb_hp2_b2 = ((1.0 + cos(mb_w2)) * 0.5) / mb_hp2_a0;
  mb_hp2_a1 = (-2.0 * cos(mb_w2)) / mb_hp2_a0;
  mb_hp2_a2 = (1.0 - mb_al2) / mb_hp2_a0;
'''
assert 'function update_guitar_filters()' in t
t = t.replace('function update_guitar_filters() (', 'function update_guitar_filters() (\n' + mb_filter_calc, 1)

# 6. In @sample, add the MultiBand-Comp processing block
mb_dsp = r'''
// ---- MultiBand-Comp (3-Band Dynamic Palm-Mute & Fizz Controller) ----
(slider52 == 1 && (slider53 > 0 || slider54 > 0 || slider55 > 0)) ? (
  // 1. Split into Low (<220Hz), High (>3.2kHz), and Mid (remainder)
  mb_l_low = mb_lp1_b0 * proc_l + mb_lp1_b1 * mb_low_lx1 + mb_lp1_b2 * mb_low_lx2 - mb_lp1_a1 * mb_low_ly1 - mb_lp1_a2 * mb_low_ly2;
  mb_low_lx2 = mb_low_lx1; mb_low_lx1 = proc_l; mb_low_ly2 = mb_low_ly1; mb_low_ly1 = mb_l_low;

  mb_r_low = mb_lp1_b0 * proc_r + mb_lp1_b1 * mb_low_rx1 + mb_lp1_b2 * mb_low_rx2 - mb_lp1_a1 * mb_low_ry1 - mb_lp1_a2 * mb_low_ry2;
  mb_low_rx2 = mb_low_rx1; mb_low_rx1 = proc_r; mb_low_ry2 = mb_low_ry1; mb_low_ry1 = mb_r_low;

  mb_l_hi = mb_hp2_b0 * proc_l + mb_hp2_b1 * mb_hi_lx1 + mb_hp2_b2 * mb_hi_lx2 - mb_hp2_a1 * mb_hi_ly1 - mb_hp2_a2 * mb_hi_ly2;
  mb_hi_lx2 = mb_hi_lx1; mb_hi_lx1 = proc_l; mb_hi_ly2 = mb_hi_ly1; mb_hi_ly1 = mb_l_hi;

  mb_r_hi = mb_hp2_b0 * proc_r + mb_hp2_b1 * mb_hi_rx1 + mb_hp2_b2 * mb_hi_rx2 - mb_hp2_a1 * mb_hi_ry1 - mb_hp2_a2 * mb_hi_ry2;
  mb_hi_rx2 = mb_hi_rx1; mb_hi_rx1 = proc_r; mb_hi_ry2 = mb_hi_ry1; mb_hi_ry1 = mb_r_hi;

  mb_l_mid = proc_l - mb_l_low - mb_l_hi;
  mb_r_mid = proc_r - mb_r_low - mb_r_hi;

  // 2. Compress Low Band (<220Hz palm-mute chugs)
  mb_pk_low = max(abs(mb_l_low), abs(mb_r_low));
  mb_db_low = mb_pk_low > 0.000001 ? 20.0 * log10(mb_pk_low) : -120.0;
  mb_thr_low = -14.0 - (slider53 * 0.18);
  mb_over_low = max(0.0, mb_db_low - mb_thr_low);
  mb_tgt_low = mb_over_low * (1.0 - 1.0 / slider56) * (slider53 * 0.01);
  mb_gr_low = mb_tgt_low > mb_gr_low ? (mb_tgt_low + (mb_gr_low - mb_tgt_low) * 0.94) : (mb_tgt_low + (mb_gr_low - mb_tgt_low) * 0.985);
  mb_meter_low = mb_meter_low * 0.90 + mb_gr_low * 0.10;
  mb_g_low = exp(-mb_gr_low * 0.11512925);
  mb_l_low *= mb_g_low; mb_r_low *= mb_g_low;

  // 3. Compress Mid Band (220-3.2kHz body punch)
  mb_pk_mid = max(abs(mb_l_mid), abs(mb_r_mid));
  mb_db_mid = mb_pk_mid > 0.000001 ? 20.0 * log10(mb_pk_mid) : -120.0;
  mb_thr_mid = -12.0 - (slider54 * 0.15);
  mb_over_mid = max(0.0, mb_db_mid - mb_thr_mid);
  mb_tgt_mid = mb_over_mid * (1.0 - 1.0 / slider56) * (slider54 * 0.01);
  mb_gr_mid = mb_tgt_mid > mb_gr_mid ? (mb_tgt_mid + (mb_gr_mid - mb_tgt_mid) * 0.95) : (mb_tgt_mid + (mb_gr_mid - mb_tgt_mid) * 0.985);
  mb_meter_mid = mb_meter_mid * 0.90 + mb_gr_mid * 0.10;
  mb_g_mid = exp(-mb_gr_mid * 0.11512925);
  mb_l_mid *= mb_g_mid; mb_r_mid *= mb_g_mid;

  // 4. Compress High Band (>3.2kHz fizz clamp)
  mb_pk_hi = max(abs(mb_l_hi), abs(mb_r_hi));
  mb_db_hi = mb_pk_hi > 0.000001 ? 20.0 * log10(mb_pk_hi) : -120.0;
  mb_thr_hi = -16.0 - (slider55 * 0.16);
  mb_over_hi = max(0.0, mb_db_hi - mb_thr_hi);
  mb_tgt_hi = mb_over_hi * (1.0 - 1.0 / slider56) * (slider55 * 0.01);
  mb_gr_hi = mb_tgt_hi > mb_gr_hi ? (mb_tgt_hi + (mb_gr_hi - mb_tgt_hi) * 0.92) : (mb_tgt_hi + (mb_gr_hi - mb_tgt_hi) * 0.985);
  mb_meter_hi = mb_meter_hi * 0.90 + mb_gr_hi * 0.10;
  mb_g_hi = exp(-mb_gr_hi * 0.11512925);
  mb_l_hi *= mb_g_hi; mb_r_hi *= mb_g_hi;

  // 5. Recombine sum
  proc_l = mb_l_low + mb_l_mid + mb_l_hi;
  proc_r = mb_r_low + mb_r_mid + mb_r_hi;
);
'''
old_dc1a = '// 8. Analog Console & Tape Saturation Bus Glue'
assert old_dc1a in t, "dc1a comment not found"
t = t.replace(old_dc1a, mb_dsp + '\n' + old_dc1a, 1)

# 7. Update Tab 4 title and tab name in @gfx tab loop
t = t.replace('"Analog Glue" : "Producer Matrix"', '"ReEQ & MultiBand" : "Producer Matrix"')

# 8. In Tab 4 GUI, add the MultiBand-Comp visual meter strip right below the 3 racks!
idx_t4 = t.find('slider1 == 4 ? (')
assert idx_t4 != -1
# Find the end of Tab 4 before slider1 == 5
idx_t4_end = t.find('slider1 == 5 ? (', idx_t4)
assert idx_t4_end != -1

mb_gui_strip = r'''
  // ─────────────────────────────────────────────────────────────────────────────
  // 4. MULTIBAND-COMP & REEQ DYNAMICS STRIP (LOWER CONSOLE)
  // ─────────────────────────────────────────────────────────────────────────────
  mb_sy = ay + at_h + 12;
  mb_sw = a_w - 12;
  mb_sh = max(80, disp_h - mb_sy + disp_y - 20);

  gfx_r = 0.026; gfx_g = 0.034; gfx_b = 0.046; gfx_rect(disp_x + 16, mb_sy, mb_sw, mb_sh);
  gfx_r = 0.85; gfx_g = 0.68; gfx_b = 0.20; gfx_rect(disp_x + 16, mb_sy, mb_sw, mb_sh, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.85; gfx_g = 0.68; gfx_b = 0.20;
  gfx_x = disp_x + 28; gfx_y = mb_sy + 10;
  gfx_drawstr("MULTIBAND-COMP 3-BAND DYNAMICS // PALM-MUTE CHUG & FIZZ CLAMP");

  // 3 Band Columns: Low (<220Hz), Mid (220-3.2kHz), High (>3.2kHz)
  mb_col_w = floor((mb_sw - 36) / 3);
  mbi = 0;
  loop(3,
    mb_cx = disp_x + 24 + mbi * (mb_col_w + 6);
    mb_cy = mb_sy + 34;

    mbi == 0 ? (
      mb_lbl = "LOW CHUG (<220Hz)";
      mb_val = slider53;
      mb_gr = mb_meter_low;
    ) : mbi == 1 ? (
      mb_lbl = "MID CRUNCH (220-3.2k)";
      mb_val = slider54;
      mb_gr = mb_meter_mid;
    ) : (
      mb_lbl = "HIGH FIZZ (>3.2kHz)";
      mb_val = slider55;
      mb_gr = mb_meter_hi;
    );

    gfx_setfont(1, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
    gfx_x = mb_cx; gfx_y = mb_cy; gfx_drawstr(mb_lbl);

    sprintf(#mb_vstr, "%d%%  (-%1.1fdB)", mb_val, mb_gr);
    gfx_measurestr(#mb_vstr, mvw, mvh);
    gfx_r = 1.0; gfx_g = 0.82; gfx_b = 0.25;
    gfx_x = mb_cx + mb_col_w - mvw; gfx_y = mb_cy; gfx_drawstr(#mb_vstr);

    // Reduction Bar
    mb_bx = mb_cx; mb_by = mb_cy + 18; mb_bw = mb_col_w; mb_bh = 14;
    gfx_r = 0.04; gfx_g = 0.05; gfx_b = 0.08; gfx_rect(mb_bx, mb_by, mb_bw, mb_bh);
    gfx_r = 0.25; gfx_g = 0.30; gfx_b = 0.40; gfx_rect(mb_bx, mb_by, mb_bw, mb_bh, 0);

    // Dynamic GR fill (flashes red/gold under heavy chug clamp)
    gr_frac = min(1.0, max(0.0, mb_gr / 12.0));
    gfx_r = 0.95; gfx_g = 0.35 + (1.0 - gr_frac)*0.45; gfx_b = 0.20;
    gfx_rect(mb_bx + 1, mb_by + 1, floor(gr_frac * (mb_bw - 2)), mb_bh - 2);

    mb_hov = (mouse_x >= mb_bx && mouse_x <= mb_bx + mb_bw && mouse_y >= mb_by - 4 && mouse_y <= mb_by + mb_bh + 4);
    mouse_down && mb_hov ? (
      n_pct = floor(((mouse_x - mb_bx) / mb_bw) * 100.0 + 0.5);
      n_pct = max(0, min(100, n_pct));
      mbi == 0 ? slider53 = n_pct : (mbi == 1 ? slider54 = n_pct : slider55 = n_pct);
      slider_automate();
    );

    mbi += 1;
  );
'''
# Insert before `slider1 == 5 ? (`
t = t[:idx_t4_end] + mb_gui_strip + '\n' + t[idx_t4_end:]

# 9. Calibrate all 17 producer presets in apply_guitar_preset with ReEQ, Comp, MultiBand-Comp, and Saturation settings:
# Dan Braunstein (p_idx == 15): Spiritbox / Dayseeker calibrated for heavy punch, controlled low-end chug
p_calibs_gtr = {
    0: (0, 20, 15, 20, 2.5),  # Default Neutral
    1: (1, 55, 30, 42, 3.5),  # Lance Prenc (fast aggressive chugs)
    2: (1, 60, 35, 45, 4.0),  # Scott Seigel
    3: (1, 45, 28, 35, 3.0),  # Jonathan Dolese
    4: (1, 68, 40, 50, 4.5),  # Buster Odeholm (heavy djent chug clamp)
    5: (1, 40, 24, 38, 2.8),  # Kel Pinchin
    6: (1, 38, 25, 32, 2.5),  # Sam Guaiana
    7: (1, 30, 20, 28, 2.2),  # Forrester Savell
    8: (1, 48, 30, 36, 3.0),  # Jens Bogren
    9: (1, 42, 25, 30, 2.8),  # Nolly Getgood (Periphery precision)
    10: (1, 58, 35, 40, 3.5), # Will Putney
    11: (1, 36, 22, 30, 2.4), # George Lever
    12: (1, 44, 28, 35, 3.0), # Sam Bassal
    13: (1, 50, 32, 38, 3.2), # Henrik Udd
    14: (1, 62, 38, 46, 4.0), # Joey Sturgis
    15: (1, 48, 28, 36, 3.2), # Dan Braunstein (Spiritbox heavy chug & clear top)
    16: (1, 45, 30, 38, 3.0), # Zakk Cervini
}

for p_idx, (mb_on, low_c, mid_c, hi_c, rat) in p_calibs_gtr.items():
    pattern = rf'(p_idx == {p_idx} \? \([^\n]*\n)'
    calib_str = (
        f'    // ReEQ & MultiBand-Comp Producer Calibrations\n'
        f'    slider34 = 1; // Standalone All-In-One Mode\n'
        f'    slider52 = {mb_on}; slider53 = {low_c}; slider54 = {mid_c}; slider55 = {hi_c}; slider56 = {rat};\n'
    )
    t = re.sub(pattern, rf'\1{calib_str}', t, count=1)

open(P, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
print('GuitarSuite patch complete.')
