"""
Patcher for Damei_DrumSuite.jsfx:
Adds BSA Drum Bus (Black Salt Audio) hardware rack, controls, DSP, and producer calibrations.
"""
import sys, re

P = r'C:\Dev\DameiAPI\reaper_scripts\Damei_DrumSuite.jsfx'
raw = open(P, 'rb').read().decode('utf-8')
crlf = '\r\n' in raw
t = raw.replace('\r\n', '\n')

# 1. Update slider1 to add "BSA Drum Bus (Black Salt Audio)" tab (7 tabs total)
old_s1 = 'slider1:0<0,5,1{Drum Overview,Beat Leveler (Sound Radix),Cymbal Silk & De-Trash,Shell Weight & Bleed Tamer,Transient Snap & Analog Chain,Producer Matrix & GGD Mode}>-Active Module'
new_s1 = 'slider1:0<0,6,1{Drum Overview,Beat Leveler (Sound Radix),Cymbal Silk & De-Trash,Shell Weight & Bleed Tamer,BSA Drum Bus (Black Salt Audio),Transient Snap & Analog Chain,Producer Matrix & GGD Mode}>-Active Module'
assert old_s1 in t, "slider1 not found"
t = t.replace(old_s1, new_s1, 1)

# 2. Add BSA sliders right after slider42 (hidden Matrix Trim)
old_s42 = 'slider42:1<0,1,1{Off,On}>-Matrix Trim (applies Assessment Matrix auto-correct lane)\n'
if old_s42 not in t:
    # check if leading dash is there
    m = re.search(r'slider42:[^\n]+\n', t)
    assert m, "slider42 not found"
    old_s42 = m.group(0)

bsa_sliders = (
    '// BSA Drum Bus (Black Salt Audio Modeled Rack)\n'
    'slider43:0<0,1,1{Standard (Musical 4:1 Glue),Slammed (Aggressive 20:1 Crush)}>-BSA Mode\n'
    'slider44:38<0,100,1>-BSA Comp Drive (%)\n'
    'slider45:26<0,100,1>-BSA Heat Saturation (%)\n'
    'slider46:60<0,100,1>-BSA Attack Punch (%)\n'
    'slider47:50<0,100,1>-BSA Tone Tilt (%)\n'
    'slider48:35<0,100,1>-BSA Salt Sheen Exciter (%)\n'
    'slider49:80<20,300,5>-BSA Sidechain HPF (Hz)\n'
    'slider50:85<0,100,1>-BSA Parallel Mix (%)\n'
    'slider51:0.0<-12.0,12.0,0.5>-BSA Output Trim (dB)\n'
)
t = t.replace(old_s42, old_s42 + bsa_sliders, 1)

# 3. Add serialization for new sliders
old_ser = 'file_var(0, slider41);\nfile_var(0, is_user_customized);'
new_ser = (
    'file_var(0, slider41);\n'
    'file_var(0, slider43); file_var(0, slider44); file_var(0, slider45);\n'
    'file_var(0, slider46); file_var(0, slider47); file_var(0, slider48);\n'
    'file_var(0, slider49); file_var(0, slider50); file_var(0, slider51);\n'
    'file_var(0, is_user_customized);'
)
assert old_ser in t, "serialize not found"
t = t.replace(old_ser, new_ser, 1)

# 4. In @init, initialize BSA variables and filters
bsa_init = r'''
// BSA Drum Bus State & Ballistics
bsa_gr_db = 0.0;
bsa_gr_meter = 0.0;
bsa_env = 0.0;
bsa_sc_x1 = 0; bsa_sc_x2 = 0; bsa_sc_y1 = 0; bsa_sc_y2 = 0;
bsa_tilt_lx1 = 0; bsa_tilt_lx2 = 0; bsa_tilt_ly1 = 0; bsa_tilt_ly2 = 0;
bsa_tilt_rx1 = 0; bsa_tilt_rx2 = 0; bsa_tilt_ry1 = 0; bsa_tilt_ry2 = 0;
bsa_salt_lx1 = 0; bsa_salt_lx2 = 0; bsa_salt_ly1 = 0; bsa_salt_ly2 = 0;
bsa_salt_rx1 = 0; bsa_salt_rx2 = 0; bsa_salt_ry1 = 0; bsa_salt_ry2 = 0;
'''
t = t.replace('ext_noinit = 1.0;', 'ext_noinit = 1.0;\n' + bsa_init, 1)

# 5. In update_drum_filters, calculate BSA filters (sidechain HPF, tilt low/high shelf, salt exciter)
bsa_filters_calc = r'''
  // BSA Sidechain HPF (slider49: 20-300Hz 2nd order Butterworth)
  bsa_hp_w0 = 2.0 * $pi * max(20.0, min(300.0, slider49)) / srate;
  bsa_hp_alpha = sin(bsa_hp_w0) * 0.7071;
  bsa_hp_b0 = (1.0 + cos(bsa_hp_w0)) * 0.5;
  bsa_hp_b1 = -(1.0 + cos(bsa_hp_w0));
  bsa_hp_b2 = (1.0 + cos(bsa_hp_w0)) * 0.5;
  bsa_hp_a0 = 1.0 + bsa_hp_alpha;
  bsa_hp_a1 = -2.0 * cos(bsa_hp_w0);
  bsa_hp_a2 = 1.0 - bsa_hp_alpha;
  bsa_hp_b0 /= bsa_hp_a0; bsa_hp_b1 /= bsa_hp_a0; bsa_hp_b2 /= bsa_hp_a0;
  bsa_hp_a1 /= bsa_hp_a0; bsa_hp_a2 /= bsa_hp_a0;

  // BSA Tone Tilt (slider47: 0-100%, 50% = flat; tilt low shelf @ 130Hz, high shelf @ 3.8kHz)
  bsa_tilt_db = (slider47 - 50.0) * 0.12; // -6dB to +6dB tilt
  bsa_t_a = exp(bsa_tilt_db * 0.11512925); // 10^(db/20)
  bsa_tl_w0 = 2.0 * $pi * 130.0 / srate;
  bsa_tl_cs = cos(bsa_tl_w0); bsa_tl_sn = sin(bsa_tl_w0);
  bsa_tl_al = bsa_tl_sn * 0.5 * sqrt((bsa_t_a + 1.0/bsa_t_a)*(1.0/0.7071 - 1.0) + 2.0);
  bsa_tl_a0 = (bsa_t_a + 1.0) + (bsa_t_a - 1.0)*bsa_tl_cs + 2.0*sqrt(bsa_t_a)*bsa_tl_al;
  bsa_tl_b0 = (bsa_t_a * ((bsa_t_a + 1.0) - (bsa_t_a - 1.0)*bsa_tl_cs + 2.0*sqrt(bsa_t_a)*bsa_tl_al)) / bsa_tl_a0;
  bsa_tl_b1 = (2.0 * bsa_t_a * ((bsa_t_a - 1.0) - (bsa_t_a + 1.0)*bsa_tl_cs)) / bsa_tl_a0;
  bsa_tl_b2 = (bsa_t_a * ((bsa_t_a + 1.0) - (bsa_t_a - 1.0)*bsa_tl_cs - 2.0*sqrt(bsa_t_a)*bsa_tl_al)) / bsa_tl_a0;
  bsa_tl_a1 = (-2.0 * ((bsa_t_a - 1.0) + (bsa_t_a + 1.0)*bsa_tl_cs)) / bsa_tl_a0;
  bsa_tl_a2 = ((bsa_t_a + 1.0) + (bsa_t_a - 1.0)*bsa_tl_cs - 2.0*sqrt(bsa_t_a)*bsa_tl_al) / bsa_tl_a0;

  // BSA Salt Sheen Exciter (slider48: highpass @ 7.8kHz)
  bsa_st_w0 = 2.0 * $pi * 7800.0 / srate;
  bsa_st_al = sin(bsa_st_w0) * 0.7071;
  bsa_st_a0 = 1.0 + bsa_st_al;
  bsa_st_b0 = ((1.0 + cos(bsa_st_w0)) * 0.5) / bsa_st_a0;
  bsa_st_b1 = (-(1.0 + cos(bsa_st_w0))) / bsa_st_a0;
  bsa_st_b2 = ((1.0 + cos(bsa_st_w0)) * 0.5) / bsa_st_a0;
  bsa_st_a1 = (-2.0 * cos(bsa_st_w0)) / bsa_st_a0;
  bsa_st_a2 = (1.0 - bsa_st_al) / bsa_st_a0;
'''
assert 'function update_drum_filters()' in t
t = t.replace('function update_drum_filters() (', 'function update_drum_filters() (\n' + bsa_filters_calc, 1)

# 6. In @sample, replace the legacy bsa block with the full BSA Drum Bus DSP engine
old_bsa_dsp = r'''// 7. BSA Drum Bus Glue & Heat (Only active if Standalone Mode is engaged)
(slider37 == 1 && slider35 > 0) ? (
  bsa_amt = slider35 / 100.0;
  bsa_drive = 1.0 + bsa_amt * 1.15;
  bsa_l = sin(max(-1.5707, min(1.5707, proc_l * bsa_drive * 0.65))) * 1.48;
  proc_l = proc_l * (1.0 - bsa_amt * 0.35) + bsa_l * (bsa_amt * 0.35);

  bsa_r = sin(max(-1.5707, min(1.5707, proc_r * bsa_drive * 0.65))) * 1.48;
  proc_r = proc_r * (1.0 - bsa_amt * 0.35) + bsa_r * (bsa_amt * 0.35);
  // Modeled BSA Drum Bus Output Makeup Gain (+3.91 dB = 1.568x factor)
  proc_l *= (1.0 + 0.568 * bsa_amt);
  proc_r *= (1.0 + 0.568 * bsa_amt);
);'''

new_bsa_dsp = r'''// 7. BSA DRUM BUS HARDWARE CONSOLE (VCA Comp + Heat + Attack + Tone + Salt Sheen)
// Active whenever Standalone Mode is engaged OR BSA tab is active OR slider44 > 0
(slider37 == 1 || slider44 > 0 || slider45 > 0) ? (
  bsa_dry_l = proc_l; bsa_dry_r = proc_r;

  // A. Sidechain HPF detection
  bsa_sc_mono = (proc_l + proc_r) * 0.5;
  bsa_sc_f = bsa_hp_b0 * bsa_sc_mono + bsa_hp_b1 * bsa_sc_x1 + bsa_hp_b2 * bsa_sc_x2 - bsa_hp_a1 * bsa_sc_y1 - bsa_hp_a2 * bsa_sc_y2;
  bsa_sc_x2 = bsa_sc_x1; bsa_sc_x1 = bsa_sc_mono; bsa_sc_y2 = bsa_sc_y1; bsa_sc_y1 = bsa_sc_f;

  // B. VCA Compressor (Standard 4:1 vs Slammed 20:1)
  bsa_sc_pk = abs(bsa_sc_f);
  bsa_is_slammed = (slider43 == 1);
  bsa_ratio = bsa_is_slammed ? 20.0 : 4.0;
  bsa_thr = -8.0 - (slider44 * 0.28); // Threshold driven by Comp knob
  bsa_att_ms = bsa_is_slammed ? (1.5 + (1.0 - slider46*0.01) * 8.0) : (8.0 + (1.0 - slider46*0.01) * 35.0);
  bsa_rel_ms = bsa_is_slammed ? 55.0 : 130.0;
  bsa_att_c = exp(-1.0 / (srate * bsa_att_ms * 0.001));
  bsa_rel_c = exp(-1.0 / (srate * bsa_rel_ms * 0.001));

  bsa_sc_db = bsa_sc_pk > 0.000001 ? 20.0 * log10(bsa_sc_pk) : -120.0;
  bsa_over = bsa_sc_db - bsa_thr;
  bsa_target_gr = bsa_over > 0.0 ? bsa_over * (1.0 - 1.0 / bsa_ratio) : 0.0;
  bsa_target_gr = max(0.0, min(24.0, bsa_target_gr * (slider44 * 0.01)));

  bsa_gr_db = bsa_target_gr > bsa_gr_db ? (bsa_target_gr + (bsa_gr_db - bsa_target_gr) * bsa_att_c) : (bsa_target_gr + (bsa_gr_db - bsa_target_gr) * bsa_rel_c);
  bsa_gr_meter = bsa_gr_meter * 0.92 + bsa_gr_db * 0.08; // smooth needle ballistics

  bsa_comp_gain = exp(-bsa_gr_db * 0.11512925);
  proc_l *= bsa_comp_gain; proc_r *= bsa_comp_gain;

  // C. HEAT Saturation (tube / transformer asymmetrical overdrive)
  slider45 > 0 ? (
    bsa_h_drv = 1.0 + (slider45 * 0.01) * 2.2;
    bsa_h_l = proc_l * bsa_h_drv;
    bsa_h_r = proc_r * bsa_h_drv;
    bsa_h_l = (bsa_h_l - 0.15 * bsa_h_l * bsa_h_l) / (1.0 + abs(bsa_h_l) * 0.45);
    bsa_h_r = (bsa_h_r - 0.15 * bsa_h_r * bsa_h_r) / (1.0 + abs(bsa_h_r) * 0.45);
    bsa_h_mix = (slider45 * 0.01) * 0.65;
    proc_l = proc_l * (1.0 - bsa_h_mix) + bsa_h_l * bsa_h_mix;
    proc_r = proc_r * (1.0 - bsa_h_mix) + bsa_h_r * bsa_h_mix;
  );

  // D. TONE Tilt EQ
  slider47 != 50 ? (
    bsa_tl_out_l = bsa_tl_b0 * proc_l + bsa_tl_b1 * bsa_tilt_lx1 + bsa_tl_b2 * bsa_tilt_lx2 - bsa_tl_a1 * bsa_tilt_ly1 - bsa_tl_a2 * bsa_tilt_ly2;
    bsa_tilt_lx2 = bsa_tilt_lx1; bsa_tilt_lx1 = proc_l; bsa_tilt_ly2 = bsa_tilt_ly1; bsa_tilt_ly1 = bsa_tl_out_l;
    proc_l = bsa_tl_out_l;

    bsa_tl_out_r = bsa_tl_b0 * proc_r + bsa_tl_b1 * bsa_tilt_rx1 + bsa_tl_b2 * bsa_tilt_rx2 - bsa_tl_a1 * bsa_tilt_ry1 - bsa_tl_a2 * bsa_tilt_ry2;
    bsa_tilt_rx2 = bsa_tilt_rx1; bsa_tilt_rx1 = proc_r; bsa_tilt_ry2 = bsa_tilt_ry1; bsa_tilt_ry1 = bsa_tl_out_r;
    proc_r = bsa_tl_out_r;
  );

  // E. SALT Sheen Exciter (>7.8kHz high harmonic sparkle)
  slider48 > 0 ? (
    bsa_st_l = bsa_st_b0 * proc_l + bsa_st_b1 * bsa_salt_lx1 + bsa_st_b2 * bsa_salt_lx2 - bsa_st_a1 * bsa_salt_ly1 - bsa_st_a2 * bsa_salt_ly2;
    bsa_salt_lx2 = bsa_salt_lx1; bsa_salt_lx1 = proc_l; bsa_salt_ly2 = bsa_salt_ly1; bsa_salt_ly1 = bsa_st_l;

    bsa_st_r = bsa_st_b0 * proc_r + bsa_st_b1 * bsa_salt_rx1 + bsa_st_b2 * bsa_salt_rx2 - bsa_st_a1 * bsa_salt_ry1 - bsa_st_a2 * bsa_salt_ry2;
    bsa_salt_rx2 = bsa_salt_rx1; bsa_salt_rx1 = proc_r; bsa_salt_ry2 = bsa_salt_ry1; bsa_salt_ry1 = bsa_st_r;

    // Harmonic exciter generator
    bsa_exc_l = max(-0.8, min(0.8, bsa_st_l * 2.5));
    bsa_exc_l = (bsa_exc_l - 0.333 * bsa_exc_l * bsa_exc_l * bsa_exc_l);
    bsa_exc_r = max(-0.8, min(0.8, bsa_st_r * 2.5));
    bsa_exc_r = (bsa_exc_r - 0.333 * bsa_exc_r * bsa_exc_r * bsa_exc_r);

    bsa_salt_gain = (slider48 * 0.01) * 0.45;
    proc_l += bsa_exc_l * bsa_salt_gain;
    proc_r += bsa_exc_r * bsa_salt_gain;
  );

  // F. Parallel MIX & Output Trim
  bsa_mix = slider50 * 0.01;
  bsa_out_gain = exp(slider51 * 0.11512925);
  proc_l = (bsa_dry_l * (1.0 - bsa_mix) + proc_l * bsa_mix) * bsa_out_gain;
  proc_r = (bsa_dry_r * (1.0 - bsa_mix) + proc_r * bsa_mix) * bsa_out_gain;
);'''

assert old_bsa_dsp in t, "old_bsa_dsp not found in sample"
t = t.replace(old_bsa_dsp, new_bsa_dsp, 1)

# 7. Update tab loop in @gfx to 7 tabs:
old_tab_loop = r'''tab_y = card_y + card_h + 8;
tab_h = 40;
tab_w = floor((crt_w - 24) / 6);
ti = 0;
loop(6,
  tx = crt_x + 8 + ti * tab_w;
  sel = (slider1 == ti);
  gfx_r = sel ? 0.09 : 0.04; gfx_g = sel ? 0.14 : 0.05; gfx_b = sel ? 0.20 : 0.07;
  gfx_rect(tx, tab_y, tab_w - 4, tab_h);
  sel ? (
    gfx_r = 0.85; gfx_g = 0.68; gfx_b = 0.20;
    gfx_rect(tx, tab_y + tab_h - 3, tab_w - 4, 3);
    gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  ) : (
    gfx_r = 0.55; gfx_g = 0.65; gfx_b = 0.75;
  );
  gfx_setfont(1, "Orbitron", 13, 'b');
  t_lbl = (ti==0 ? "Drum Overview" : (ti==1 ? "Beat Leveler" : (ti==2 ? "Cymbal Silk" : (ti==3 ? "Shell Weight" : (ti==4 ? "Transient Snap" : "Producer Matrix")))));'''

new_tab_loop = r'''tab_y = card_y + card_h + 8;
tab_h = 40;
tab_w = floor((crt_w - 24) / 7);
ti = 0;
loop(7,
  tx = crt_x + 8 + ti * tab_w;
  sel = (slider1 == ti);
  gfx_r = sel ? 0.09 : 0.04; gfx_g = sel ? 0.14 : 0.05; gfx_b = sel ? 0.20 : 0.07;
  gfx_rect(tx, tab_y, tab_w - 4, tab_h);
  sel ? (
    gfx_r = 0.85; gfx_g = 0.68; gfx_b = 0.20;
    gfx_rect(tx, tab_y + tab_h - 3, tab_w - 4, 3);
    gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  ) : (
    gfx_r = 0.55; gfx_g = 0.65; gfx_b = 0.75;
  );
  gfx_setfont(1, "Orbitron", 12, 'b');
  t_lbl = (ti==0 ? "Overview" : (ti==1 ? "Beat Leveler" : (ti==2 ? "Cymbal Silk" : (ti==3 ? "Shell Weight" : (ti==4 ? "BSA Drum Bus" : (ti==5 ? "Transient Snap" : "Producer Matrix"))))));'''

assert old_tab_loop in t, "tab loop not found"
t = t.replace(old_tab_loop, new_tab_loop, 1)

# Shift existing Tab 4 & Tab 5 to Tab 5 & Tab 6:
# Replace `slider1 == 5 ? (` with `slider1 == 6 ? (`
# And replace `slider1 == 4 ? (` with `slider1 == 5 ? (`
# And insert `slider1 == 4 ? (` for BSA Drum Bus!
t = t.replace('slider1 == 5 ? (', 'slider1 == 6 ? (', 1)
t = t.replace('slider1 == 4 ? (', 'slider1 == 5 ? (', 1)

# Now define `draw_bsa_tab` and `slider1 == 4 ? (`
bsa_tab_ui = r'''
// =============================================================================
// TAB 4: BSA DRUM BUS (BLACK SALT AUDIO HARDWARE CONSOLE)
// =============================================================================
function draw_bsa_rotary(kx, ky, rad, val, vmin, vmax, vstep, lbl, unit, is_lg, p_id) local(ang, nx, ny, t_ang, i, dx, dy, tw, th, s_val, hov, nval) (
  hov = (mouse_x >= kx - rad - 12 && mouse_x <= kx + rad + 12 && mouse_y >= ky - rad - 8 && mouse_y <= ky + rad + 24);

  // Outer bezel
  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(kx, ky, rad + 4, 1);
  gfx_r = 0.18; gfx_g = 0.22; gfx_b = 0.28; gfx_circle(kx, ky, rad + 4, 0);

  // Knob Body
  gfx_r = 0.12; gfx_g = 0.14; gfx_b = 0.18; gfx_circle(kx, ky, rad, 1);
  gfx_r = hov ? 0.95 : 0.45; gfx_g = hov ? 0.55 : 0.35; gfx_b = hov ? 0.35 : 0.28;
  gfx_circle(kx, ky, rad, 0);

  // Perimeter ticks
  i = 0;
  loop(11,
    t_ang = -2.356 + i * 0.4712;
    dx = kx + sin(t_ang) * (rad + 8); dy = ky - cos(t_ang) * (rad + 8);
    gfx_r = 0.35; gfx_g = 0.40; gfx_b = 0.48; gfx_circle(dx, dy, 1.2, 1);
    i += 1;
  );

  // Pointer needle
  ang = -2.356 + ((val - vmin) / (vmax - vmin)) * 4.712;
  nx = kx + sin(ang) * (rad - 3);
  ny = ky - cos(ang) * (rad - 3);
  gfx_r = 0.95; gfx_g = 0.90; gfx_b = 0.85;
  gfx_line(kx, ky, nx, ny);
  gfx_line(kx - 1, ky, nx - 1, ny);
  gfx_line(kx + 1, ky, nx + 1, ny);

  // Center cap
  gfx_r = 0.06; gfx_g = 0.08; gfx_b = 0.10; gfx_circle(kx, ky, max(4, floor(rad * 0.35)), 1);

  // Label
  gfx_setfont(1, "Orbitron", is_lg ? 13.5 : 11.5, 'b');
  gfx_r = 0.92; gfx_g = 0.48; gfx_b = 0.36; // Warm copper/orange BSA theme
  gfx_measurestr(lbl, tw, th);
  gfx_x = kx - tw * 0.5; gfx_y = ky + rad + 6; gfx_drawstr(lbl);

  // Value text
  gfx_setfont(1, "Consolas", 12, 'b');
  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.95;
  sprintf(#s_val, "%d %s", floor(val + 0.5), unit);
  gfx_measurestr(#s_val, tw, th);
  gfx_x = kx - tw * 0.5; gfx_y = ky + rad + 21; gfx_drawstr(#s_val);

  // Drag interaction
  mouse_down && hov ? (
    nval = val - (mouse_y - prev_mouse_y_bsa) * ((vmax - vmin) * 0.007);
    nval = max(vmin, min(vmax, floor(nval / vstep + 0.5) * vstep));
    val = nval;
    update_drum_filters();
    slider_automate();
  );
  val;
);

slider1 == 4 ? (
  bsa_x = disp_x + 10; bsa_y = disp_y + 8;
  bsa_w = disp_w - 20; bsa_h = disp_h - 16;

  // Dark Brushed Metal Background
  gfx_r = 0.024; gfx_g = 0.028; gfx_b = 0.036; gfx_rect(bsa_x, bsa_y, bsa_w, bsa_h);
  gfx_r = 0.85; gfx_g = 0.45; gfx_b = 0.30; gfx_rect(bsa_x, bsa_y, bsa_w, bsa_h, 0);

  // Top Title & Brand Logo
  gfx_setfont(1, "Orbitron", 17, 'b'); gfx_r = 0.95; gfx_g = 0.50; gfx_b = 0.35;
  gfx_x = bsa_x + 20; gfx_y = bsa_y + 12;
  gfx_drawstr("BSA // DRUM BUS");
  gfx_setfont(1, "Consolas", 12, 'b'); gfx_r = 0.65; gfx_g = 0.72; gfx_b = 0.82;
  gfx_x = bsa_x + 20; gfx_y = bsa_y + 34;
  gfx_drawstr("BLACK SALT AUDIO VCA GLUE, HEAT & SALT EXCITER // CALIBRATED TO GGD MODERN & MASSIVE");

  // GGD Preset Badge
  ggd_badge = sprintf(#, "PRESET: %s (GGD CALIBRATED)", slider25==15 ? "Dan Braunstein" : (slider25==4 ? "Buster Odeholm" : (slider25==9 ? "Nolly Getgood" : "Modern Metal")));
  gfx_measurestr(ggd_badge, gbw, gbh);
  gfx_r = 0.15; gfx_g = 0.08; gfx_b = 0.06; gfx_rect(bsa_x + bsa_w - gbw - 30, bsa_y + 14, gbw + 16, 26);
  gfx_r = 0.85; gfx_g = 0.45; gfx_b = 0.30; gfx_rect(bsa_x + bsa_w - gbw - 30, bsa_y + 14, gbw + 16, 26, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.40;
  gfx_x = bsa_x + bsa_w - gbw - 22; gfx_y = bsa_y + 20; gfx_drawstr(ggd_badge);

  // ─────────────────────────────────────────────────────────────────────────
  // 1. VINTAGE NEEDLE GAIN REDUCTION METER WITH CRACKED GLASS
  // ─────────────────────────────────────────────────────────────────────────
  meter_w = min(460, floor(bsa_w * 0.55));
  meter_h = 135;
  meter_x = bsa_x + floor((bsa_w - meter_w) * 0.5);
  meter_y = bsa_y + 54;

  // Meter Housing
  gfx_r = 0.015; gfx_g = 0.018; gfx_b = 0.024; gfx_rect(meter_x, meter_y, meter_w, meter_h);
  gfx_r = 0.18; gfx_g = 0.12; gfx_b = 0.10; gfx_rect(meter_x, meter_y, meter_w, meter_h, 0);

  // Warm Amber Dial Glow
  gfx_r = 0.12; gfx_g = 0.07; gfx_b = 0.05; gfx_rect(meter_x + 2, meter_y + 2, meter_w - 4, meter_h - 4);

  // Meter Arc Scale (0, 4, 8, 12, 16, 20 dB)
  arc_cx = meter_x + meter_w * 0.5;
  arc_cy = meter_y + meter_h + 35;
  arc_r = 130;

  mi = 0;
  loop(6,
    m_val = mi * 4;
    m_ang = -0.75 + (mi / 5.0) * 1.5; // -43 deg to +43 deg
    ax1 = arc_cx + sin(m_ang) * (arc_r - 6); ay1 = arc_cy - cos(m_ang) * (arc_r - 6);
    ax2 = arc_cx + sin(m_ang) * (arc_r + 2); ay2 = arc_cy - cos(m_ang) * (arc_r + 2);
    gfx_r = 0.85; gfx_g = 0.80; gfx_b = 0.75;
    gfx_line(ax1, ay1, ax2, ay2);

    sprintf(#m_txt, "%d", m_val);
    gfx_setfont(1, "Consolas", 12, 'b');
    gfx_measurestr(#m_txt, mtw, mth);
    gfx_x = arc_cx + sin(m_ang) * (arc_r - 18) - mtw * 0.5;
    gfx_y = arc_cy - cos(m_ang) * (arc_r - 18) - mth * 0.5;
    gfx_drawstr(#m_txt);
    mi += 1;
  );

  // Subtitle in meter: "dB Gain Reduction"
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.95; gfx_g = 0.85; gfx_b = 0.75;
  gfx_measurestr("dB", dtw, dth); gfx_x = arc_cx - dtw * 0.5; gfx_y = meter_y + 70; gfx_drawstr("dB");
  gfx_measurestr("Gain Reduction", gtw, gth); gfx_x = arc_cx - gtw * 0.5; gfx_y = meter_y + 86; gfx_drawstr("Gain Reduction");

  // Needle Line
  needle_db = min(20.0, max(0.0, bsa_gr_meter));
  needle_ang = -0.75 + (needle_db / 20.0) * 1.5;
  nd_x = arc_cx + sin(needle_ang) * (arc_r + 6);
  nd_y = arc_cy - cos(needle_ang) * (arc_r + 6);
  gfx_r = 0.98; gfx_g = 0.25; gfx_b = 0.20; // Red needle
  gfx_line(arc_cx, arc_cy, nd_x, nd_y);
  gfx_line(arc_cx - 1, arc_cy, nd_x - 1, nd_y);
  gfx_line(arc_cx + 1, arc_cy, nd_x + 1, nd_y);

  // Cracked Glass Aesthetic Lines across meter face
  gfx_r = 0.45; gfx_g = 0.48; gfx_b = 0.55; gfx_a = 0.45;
  gfx_line(meter_x + 40, meter_y + 25, meter_x + 140, meter_y + 55);
  gfx_line(meter_x + 140, meter_y + 55, meter_x + 280, meter_y + 35);
  gfx_line(meter_x + 280, meter_y + 35, meter_x + 360, meter_y + 70);
  gfx_line(meter_x + 140, meter_y + 55, meter_x + 180, meter_y + 95);
  gfx_a = 1.0;

  // ─────────────────────────────────────────────────────────────────────────
  // 2. STANDARD / SLAMMED SLIDING TOGGLE SWITCH
  // ─────────────────────────────────────────────────────────────────────────
  sw_y = meter_y + meter_h + 16;
  sw_w = 120; sw_h = 28;
  sw_x = bsa_x + floor((bsa_w - sw_w) * 0.5);
  sw_hov = (mouse_x >= sw_x - 90 && mouse_x <= sw_x + sw_w + 90 && mouse_y >= sw_y && mouse_y <= sw_y + sw_h);

  // Standard text on left
  gfx_setfont(1, "Orbitron", 13, 'b');
  slider43 == 0 ? (gfx_r = 0.95; gfx_g = 0.90; gfx_b = 0.85;) : (gfx_r = 0.45; gfx_g = 0.48; gfx_b = 0.55;);
  gfx_measurestr("STANDARD", stw, sth);
  gfx_x = sw_x - stw - 18; gfx_y = sw_y + 6; gfx_drawstr("STANDARD");

  // Switch Track
  gfx_r = 0.04; gfx_g = 0.05; gfx_b = 0.07; gfx_rect(sw_x, sw_y, sw_w, sw_h);
  gfx_r = 0.35; gfx_g = 0.25; gfx_b = 0.22; gfx_rect(sw_x, sw_y, sw_w, sw_h, 0);

  // Switch Thumb
  th_w = floor(sw_w * 0.5) - 4;
  th_x = slider43 == 0 ? (sw_x + 2) : (sw_x + sw_w - th_w - 2);
  gfx_r = 0.85; gfx_g = 0.45; gfx_b = 0.30; gfx_rect(th_x, sw_y + 2, th_w, sw_h - 4);
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.75; gfx_rect(th_x, sw_y + 2, th_w, sw_h - 4, 0);

  // Slammed text on right
  slider43 == 1 ? (gfx_r = 0.98; gfx_g = 0.35; gfx_b = 0.25;) : (gfx_r = 0.45; gfx_g = 0.48; gfx_b = 0.55;);
  gfx_x = sw_x + sw_w + 18; gfx_y = sw_y + 6; gfx_drawstr("SLAMMED");

  mouse_clicked && sw_hov ? (
    slider43 = !slider43;
    slider_automate();
  );

  // ─────────────────────────────────────────────────────────────────────────
  // 3. MAIN BSA KNOBS: TOP ROW (COMP & HEAT - LARGE)
  // ─────────────────────────────────────────────────────────────────────────
  k_top_y = sw_y + sw_h + 46;
  k_spacing_top = floor(bsa_w * 0.22);
  k_cx = bsa_x + floor(bsa_w * 0.5);

  slider44 = draw_bsa_rotary(k_cx - k_spacing_top, k_top_y, 44, slider44, 0, 100, 1, "COMP", "%", 1, 44);
  slider45 = draw_bsa_rotary(k_cx + k_spacing_top, k_top_y, 44, slider45, 0, 100, 1, "HEAT", "%", 1, 45);

  // ─────────────────────────────────────────────────────────────────────────
  // 4. SECOND ROW: ATTACK, TONE, SALT (MEDIUM KNOBS)
  // ─────────────────────────────────────────────────────────────────────────
  k_mid_y = k_top_y + 115;
  k_spacing_mid = floor(bsa_w * 0.24);

  slider46 = draw_bsa_rotary(k_cx - k_spacing_mid, k_mid_y, 35, slider46, 0, 100, 1, "ATTACK", "%", 0, 46);
  slider47 = draw_bsa_rotary(k_cx, k_mid_y, 35, slider47, 0, 100, 1, "TONE", "%", 0, 47);
  slider48 = draw_bsa_rotary(k_cx + k_spacing_mid, k_mid_y, 35, slider48, 0, 100, 1, "SALT", "%", 0, 48);

  // ─────────────────────────────────────────────────────────────────────────
  // 5. BOTTOM ROW: HPF, OUTPUT SLIDER + METER, MIX
  // ─────────────────────────────────────────────────────────────────────────
  k_bot_y = k_mid_y + 98;

  // HPF Rotary on bottom-left
  slider49 = draw_bsa_rotary(bsa_x + 90, k_bot_y, 28, slider49, 20, 300, 5, "HPF", "Hz", 0, 49);

  // OUTPUT Slider with meter in center
  out_sx = bsa_x + 170;
  out_sw = bsa_w - 340;
  out_sy = k_bot_y - 14;
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.92; gfx_g = 0.48; gfx_b = 0.36;
  gfx_measurestr("OUTPUT", otw, oth); gfx_x = out_sx + (out_sw - otw) * 0.5; gfx_y = out_sy - 16; gfx_drawstr("OUTPUT");

  // Output frame
  gfx_r = 0.04; gfx_g = 0.05; gfx_b = 0.07; gfx_rect(out_sx, out_sy, out_sw, 18);
  gfx_r = 0.28; gfx_g = 0.32; gfx_b = 0.40; gfx_rect(out_sx, out_sy, out_sw, 18, 0);

  // Output slider fader thumb
  out_norm = (slider51 - (-12.0)) / 24.0;
  f_x = out_sx + floor(out_norm * (out_sw - 20));
  gfx_r = 0.85; gfx_g = 0.88; gfx_b = 0.95; gfx_rect(f_x, out_sy - 2, 20, 22);
  gfx_r = 0.85; gfx_g = 0.45; gfx_b = 0.30; gfx_rect(f_x + 9, out_sy, 2, 18);

  out_hov = (mouse_x >= out_sx && mouse_x <= out_sx + out_sw && mouse_y >= out_sy - 8 && mouse_y <= out_sy + 26);
  mouse_down && out_hov ? (
    slider51 = -12.0 + ((mouse_x - out_sx) / out_sw) * 24.0;
    slider51 = max(-12.0, min(12.0, floor(slider51 * 2.0) * 0.5));
    slider_automate();
  );

  // Output meter readout
  gfx_setfont(1, "Consolas", 11, 'b'); gfx_r = 0.65; gfx_g = 0.70; gfx_b = 0.80;
  gfx_x = out_sx + 4; gfx_y = out_sy + 22; gfx_drawstr("-60");
  gfx_x = out_sx + floor(out_sw * 0.3); gfx_drawstr("-24");
  gfx_x = out_sx + floor(out_sw * 0.6); gfx_drawstr("-12");
  gfx_x = out_sx + floor(out_sw * 0.82); gfx_drawstr("0");
  gfx_x = out_sx + out_sw - 20; gfx_drawstr("+6");

  // MIX Rotary on bottom-right
  slider50 = draw_bsa_rotary(bsa_x + bsa_w - 90, k_bot_y, 28, slider50, 0, 100, 1, "MIX", "%", 0, 50);

  prev_mouse_y_bsa = mouse_y;
);
'''

# Insert the bsa_tab_ui right before `slider1 == 5 ? (` (which was original slider1 == 4)
idx = t.find('slider1 == 5 ? (')
assert idx != -1, "slider1 == 5 ? ( not found"
t = t[:idx] + bsa_tab_ui + '\n\n' + t[idx:]

# 8. Producer calibrations for BSA in apply_drum_preset:
# Calibrate all 17 presets with realistic BSA Drum Bus parameters
# Dan Braunstein (p_idx == 15): Spiritbox / Dayseeker calibrated specifically for GGD Modern & Massive!
p_calibs = {
    0: (0, 35, 20, 60, 50, 30, 80, 80, 0.0), # Default GGD
    1: (1, 55, 38, 75, 48, 45, 90, 85, 0.5), # Lance Prenc (slam heavy punch)
    2: (1, 60, 42, 70, 46, 50, 95, 80, 0.5), # Scott Seigel
    3: (0, 48, 30, 65, 52, 38, 85, 85, 0.0), # Jonathan Dolese
    4: (1, 68, 50, 80, 44, 55, 100, 75, 1.0), # Buster Odeholm (ultra slammed)
    5: (0, 42, 24, 62, 53, 40, 80, 85, 0.0), # Kel Pinchin
    6: (0, 40, 25, 58, 50, 35, 75, 90, 0.0), # Sam Guaiana
    7: (0, 32, 18, 55, 54, 30, 70, 95, -0.5), # Forrester Savell
    8: (0, 45, 28, 60, 50, 38, 80, 85, 0.0), # Jens Bogren
    9: (0, 40, 22, 65, 52, 42, 85, 90, 0.0), # Nolly Getgood (GGD Modern & Massive punch)
    10: (1, 58, 40, 70, 48, 44, 90, 80, 0.5), # Will Putney
    11: (0, 38, 26, 52, 54, 36, 75, 85, 0.0), # George Lever
    12: (0, 44, 28, 62, 51, 40, 80, 85, 0.0), # Sam Bassal
    13: (0, 48, 32, 66, 50, 42, 85, 85, 0.5), # Henrik Udd
    14: (1, 62, 45, 75, 46, 48, 90, 80, 1.0), # Joey Sturgis
    15: (0, 42, 26, 68, 52, 42, 85, 85, 0.5), # Dan Braunstein (Spiritbox GGD Modern & Massive)
    16: (0, 46, 30, 65, 49, 45, 80, 90, 0.5), # Zakk Cervini
}

# Update apply_drum_preset:
# For each p_idx, inject the BSA settings: slider43..51
for p_idx, (m, c, h, a, tn, s, hp, mx, ot) in p_calibs.items():
    pattern = rf'(p_idx == {p_idx} \? \([^\n]*\n)'
    calib_str = (
        f'    // BSA Drum Bus Settings (Producer Signature Calibration)\n'
        f'    slider43 = {m}; slider44 = {c}; slider45 = {h}; slider46 = {a};\n'
        f'    slider47 = {tn}; slider48 = {s}; slider49 = {hp}; slider50 = {mx}; slider51 = {ot};\n'
    )
    t = re.sub(pattern, rf'\1{calib_str}', t, count=1)

# Ensure Standalone Mode default is engaged in presets
t = t.replace('slider37 = 0; // IN-CHAIN FINISHER MODE: Complements external DeeGain/Britson/BSA/Devil-Loc',
              'slider37 = 1; // STANDALONE ALL-IN-ONE MODE: Full native hardware emulation')

open(P, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
print('DrumSuite BSA patch complete.')
