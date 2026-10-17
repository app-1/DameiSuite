"""
Patcher for Damei_VocalSuite.jsfx:
Adds AnalogObsession FETISH (FET), LALA (LA-2A), LOADES (De-Esser), and ReEQ studio rack.
"""
import sys, re

P = r'C:\Dev\DameiAPI\reaper_scripts\Damei_VocalSuite.jsfx'
raw = open(P, 'rb').read().decode('utf-8')
crlf = '\r\n' in raw
t = raw.replace('\r\n', '\n')

# 1. Update Tab 2 label in slider1
old_s1 = 'slider1:0<0,5,1{Vocal Aura & Stem Commander,Producer Ear-Candy & Drops,Dual-Stage Dynamics (FET+Opto),Mid/Side & Pocket Handshake,Analog Desk & Air Sheen,Producer Vocal Matrix}>-Active Module'
new_s1 = 'slider1:0<0,5,1{Vocal Aura & Stem Commander,Producer Ear-Candy & Drops,AnalogObsession Dual-Comp & De-Esser,Mid/Side & Pocket Handshake,Analog Desk & Air Sheen,Producer Vocal Matrix}>-Active Module'
assert old_s1 in t, "slider1 not found"
t = t.replace(old_s1, new_s1, 1)

# 2. Add new sliders for FETISH, LALA, LOADES, and ReEQ
old_s42 = 'slider42:1<0,1,1{Manual Palette,Follow Producer Preset}>-Ear-Candy Palette Follows Producer\n'
new_vocal_sliders = (
    '// AnalogObsession Modeled Dynamics (FETISH, LALA, LOADES) & ReEQ\n'
    'slider43:0<0,4,1{4:1 Ratio,8:1 Ratio,12:1 Ratio,20:1 Ratio,ALL-BUTTONS (SLAM)}>-FET Comp Ratio (AnalogObsession FETISH)\n'
    'slider44:0<0,1,1{Compress (Smooth 3:1),Limit (Hard Opto Knee)}>-LA-2A Mode (AnalogObsession LALA)\n'
    'slider45:1<0,1,1{Off,Sidechain Highpass Emphasis (Protect Chest Warmth)}>-LA-2A Sidechain Emphasis\n'
    'slider46:1<0,1,1{Wideband,Split-Band (Sibilance Isolation)}>-LOADES De-Esser Mode (AnalogObsession LOADES)\n'
    'slider47:85<60,160,5>-ReEQ Highpass Cutoff (Hz)\n'
    'slider48:-2.0<-8.0,2.0,0.5>-ReEQ 380Hz Chest Mud Scoop (dB)\n'
    'slider49:-2.5<-8.0,2.0,0.5>-ReEQ 5.2kHz Harshness Notch (dB)\n'
)
assert old_s42 in t, "slider42 not found"
t = t.replace(old_s42, old_s42 + new_vocal_sliders, 1)

# 3. Add serialization
old_ser = 'file_var(0, slider34);'
new_ser = (
    'file_var(0, slider34);\n'
    'file_var(0, slider39); file_var(0, slider40); file_var(0, slider41); file_var(0, slider42);\n'
    'file_var(0, slider43); file_var(0, slider44); file_var(0, slider45); file_var(0, slider46);\n'
    'file_var(0, slider47); file_var(0, slider48); file_var(0, slider49);'
)
assert old_ser in t, "serialize not found"
t = t.replace(old_ser, new_ser, 1)

# 4. In @init, initialize ReEQ filters
req_init = r'''
// ReEQ Vocal Biquad Filters (HPF, 380Hz Mud Scoop, 5.2kHz De-Harsh)
req_hp_x1_l = 0; req_hp_x2_l = 0; req_hp_y1_l = 0; req_hp_y2_l = 0;
req_hp_x1_r = 0; req_hp_x2_r = 0; req_hp_y1_r = 0; req_hp_y2_r = 0;
req_mud_x1_l = 0; req_mud_x2_l = 0; req_mud_y1_l = 0; req_mud_y2_l = 0;
req_mud_x1_r = 0; req_mud_x2_r = 0; req_mud_y1_r = 0; req_mud_y2_r = 0;
req_hrsh_x1_l = 0; req_hrsh_x2_l = 0; req_hrsh_y1_l = 0; req_hrsh_y2_l = 0;
req_hrsh_x1_r = 0; req_hrsh_x2_r = 0; req_hrsh_y1_r = 0; req_hrsh_y2_r = 0;
'''
t = t.replace('ext_noinit = 1.0;', 'ext_noinit = 1.0;\n' + req_init, 1)

# 5. In update_vocal_filters, calculate ReEQ biquads
req_filter_calc = r'''
  // ReEQ HPF (slider47: 60-160Hz Butterworth)
  req_hp_w0 = 2.0 * $pi * max(50.0, min(200.0, slider47)) / srate;
  req_hp_al = sin(req_hp_w0) * 0.7071;
  req_hp_a0 = 1.0 + req_hp_al;
  req_hp_b0 = ((1.0 + cos(req_hp_w0)) * 0.5) / req_hp_a0;
  req_hp_b1 = (-(1.0 + cos(req_hp_w0))) / req_hp_a0;
  req_hp_b2 = ((1.0 + cos(req_hp_w0)) * 0.5) / req_hp_a0;
  req_hp_a1 = (-2.0 * cos(req_hp_w0)) / req_hp_a0;
  req_hp_a2 = (1.0 - req_hp_al) / req_hp_a0;

  // ReEQ 380Hz Mud Scoop (slider48: -8 to +2 dB)
  req_mud_w0 = 2.0 * $pi * 380.0 / srate;
  req_mud_a = exp(slider48 * 0.05756462); // 10^(dB/40)
  req_mud_al = sin(req_mud_w0) * 0.5 * (1.0 / 1.2);
  req_mud_a0 = 1.0 + req_mud_al / req_mud_a;
  req_mud_b0 = (1.0 + req_mud_al * req_mud_a) / req_mud_a0;
  req_mud_b1 = (-2.0 * cos(req_mud_w0)) / req_mud_a0;
  req_mud_b2 = (1.0 - req_mud_al * req_mud_a) / req_mud_a0;
  req_mud_a1 = (-2.0 * cos(req_mud_w0)) / req_mud_a0;
  req_mud_a2 = (1.0 - req_mud_al / req_mud_a) / req_mud_a0;

  // ReEQ 5.2kHz Harshness Notch (slider49: -8 to +2 dB)
  req_hrsh_w0 = 2.0 * $pi * 5200.0 / srate;
  req_hrsh_a = exp(slider49 * 0.05756462);
  req_hrsh_al = sin(req_hrsh_w0) * 0.5 * (1.0 / 1.8);
  req_hrsh_a0 = 1.0 + req_hrsh_al / req_hrsh_a;
  req_hrsh_b0 = (1.0 + req_hrsh_al * req_hrsh_a) / req_hrsh_a0;
  req_hrsh_b1 = (-2.0 * cos(req_hrsh_w0)) / req_hrsh_a0;
  req_hrsh_b2 = (1.0 - req_hrsh_al * req_hrsh_a) / req_hrsh_a0;
  req_hrsh_a1 = (-2.0 * cos(req_hrsh_w0)) / req_hrsh_a0;
  req_hrsh_a2 = (1.0 - req_hrsh_al / req_hrsh_a) / req_hrsh_a0;
'''
assert 'function update_vocal_filters()' in t
t = t.replace('function update_vocal_filters() (', 'function update_vocal_filters() (\n' + req_filter_calc, 1)

# 6. In @sample, add the ReEQ processing and upgrade FET/Opto with ratio and mode switches
req_dsp = r'''
// ---- ReEQ Surgical Vocal Curve (HPF, 380Hz Mud Scoop, 5.2kHz De-Harsh) ----
s_l = req_hp_b0 * s_l + req_hp_b1 * req_hp_x1_l + req_hp_b2 * req_hp_x2_l - req_hp_a1 * req_hp_y1_l - req_hp_a2 * req_hp_y2_l;
req_hp_x2_l = req_hp_x1_l; req_hp_x1_l = s_l; req_hp_y2_l = req_hp_y1_l; req_hp_y1_l = s_l;

s_r = req_hp_b0 * s_r + req_hp_b1 * req_hp_x1_r + req_hp_b2 * req_hp_x2_r - req_hp_a1 * req_hp_y1_r - req_hp_a2 * req_hp_y2_r;
req_hp_x2_r = req_hp_x1_r; req_hp_x1_r = s_r; req_hp_y2_r = req_hp_y1_r; req_hp_y1_r = s_r;

slider48 != 0.0 ? (
  f_mud_l = req_mud_b0 * s_l + req_mud_b1 * req_mud_x1_l + req_mud_b2 * req_mud_x2_l - req_mud_a1 * req_mud_y1_l - req_mud_a2 * req_mud_y2_l;
  req_mud_x2_l = req_mud_x1_l; req_mud_x1_l = s_l; req_mud_y2_l = req_mud_y1_l; req_mud_y1_l = f_mud_l;
  s_l = f_mud_l;

  f_mud_r = req_mud_b0 * s_r + req_mud_b1 * req_mud_x1_r + req_mud_b2 * req_mud_x2_r - req_mud_a1 * req_mud_y1_r - req_mud_a2 * req_mud_y2_r;
  req_mud_x2_r = req_mud_x1_r; req_mud_x1_r = s_r; req_mud_y2_r = req_mud_y1_r; req_mud_y1_r = f_mud_r;
  s_r = f_mud_r;
);

slider49 != 0.0 ? (
  f_hrsh_l = req_hrsh_b0 * s_l + req_hrsh_b1 * req_hrsh_x1_l + req_hrsh_b2 * req_hrsh_x2_l - req_hrsh_a1 * req_hrsh_y1_l - req_hrsh_a2 * req_hrsh_y2_l;
  req_hrsh_x2_l = req_hrsh_x1_l; req_hrsh_x1_l = s_l; req_hrsh_y2_l = req_hrsh_y1_l; req_hrsh_y1_l = f_hrsh_l;
  s_l = f_hrsh_l;

  f_hrsh_r = req_hrsh_b0 * s_r + req_hrsh_b1 * req_hrsh_x1_r + req_hrsh_b2 * req_hrsh_x2_r - req_hrsh_a1 * req_hrsh_y1_r - req_hrsh_a2 * req_hrsh_y2_r;
  req_hrsh_x2_r = req_hrsh_x1_r; req_hrsh_x1_r = s_r; req_hrsh_y2_r = req_hrsh_y1_r; req_hrsh_y1_r = f_hrsh_r;
  s_r = f_hrsh_r;
);
'''
old_deess_comment = '// 1. Sibilance Bandpass Detection'
assert old_deess_comment in t, "de-ess comment not found"
t = t.replace(old_deess_comment, req_dsp + '\n' + old_deess_comment, 1)

# Upgrade FET ratio in @sample:
old_fet_ratio = 'fet_gr_db = -min(4.0, fet_over * (slider6 * 0.05));'
new_fet_ratio = r'''fet_rat = slider43 == 0 ? 4.0 : (slider43 == 1 ? 8.0 : (slider43 == 2 ? 12.0 : (slider43 == 3 ? 20.0 : 40.0)));
fet_gr_db = -min(slider43 == 4 ? 16.0 : 8.0, fet_over * (1.0 - 1.0/fet_rat) * (slider6 * 0.04));
slider43 == 4 ? fet_gr_db *= 1.35; // All-Buttons slam boost'''
assert old_fet_ratio in t, "fet ratio not found"
t = t.replace(old_fet_ratio, new_fet_ratio, 1)

# Upgrade LA-2A mode in @sample:
old_opto_ratio = 'opto_gr_db = -min(3.5, opto_over * (slider7 * 0.04));'
new_opto_ratio = r'''opto_rat = slider44 == 0 ? 3.5 : 15.0; // Compress vs Limit
opto_gr_db = -min(slider44 == 1 ? 12.0 : 6.0, opto_over * (1.0 - 1.0/opto_rat) * (slider7 * 0.035));'''
assert old_opto_ratio in t, "opto ratio not found"
t = t.replace(old_opto_ratio, new_opto_ratio, 1)

# 7. Update Tab 2 GUI title and labels:
t = t.replace('"Dual-Stage Dynamics (FET+Opto)"', '"AnalogObsession Rack"')
t = t.replace('gfx_drawstr("DUAL-STAGE DYNAMICS ENGINE (STAGE 1: 1176 FET // STAGE 2: LA-2A OPTO)");',
              'gfx_drawstr("ANALOGOBSESSION DUAL-COMP RACK (FETISH 1176 + LALA LA-2A + LOADES DE-ESSER)");')

# 8. Calibrate all 17 producer presets in apply_vocal_preset
# Dan Braunstein (p_idx == 15): Spiritbox / Dayseeker calibrated for pristine modern vocal
p_calibs_voc = {
    0: (0, 0, 1, 1, 85, -2.0, -2.5),  # Default
    1: (4, 1, 1, 1, 95, -3.0, -3.5),  # Lance Prenc (slam all-buttons)
    2: (4, 1, 1, 1, 90, -3.5, -4.0),  # Scott Seigel
    3: (1, 0, 1, 1, 85, -2.0, -2.5),  # Jonathan Dolese
    4: (4, 1, 1, 1, 100, -4.0, -4.0), # Buster Odeholm (aggressive djent clamp)
    5: (0, 0, 1, 1, 85, -2.0, -2.0),  # Kel Pinchin
    6: (1, 0, 1, 1, 80, -2.5, -2.5),  # Sam Guaiana
    7: (0, 0, 1, 1, 75, -1.5, -1.5),  # Forrester Savell
    8: (1, 1, 1, 1, 85, -2.5, -3.0),  # Jens Bogren
    9: (0, 0, 1, 1, 85, -2.0, -2.0),  # Nolly Getgood (Periphery clarity)
    10: (3, 1, 1, 1, 95, -3.0, -3.5), # Will Putney
    11: (0, 0, 1, 1, 80, -1.8, -2.0), # George Lever
    12: (1, 0, 1, 1, 85, -2.0, -2.2), # Sam Bassal
    13: (2, 0, 1, 1, 85, -2.5, -2.8), # Henrik Udd
    14: (4, 1, 1, 1, 95, -3.5, -3.5), # Joey Sturgis (heavy 1176 metalcore slam)
    15: (0, 0, 1, 1, 90, -2.5, -2.5), # Dan Braunstein (Spiritbox clean upfront vocal)
    16: (4, 1, 1, 1, 85, -2.0, -2.0), # Zakk Cervini (All-Buttons radio punch)
}

for p_idx, (fet_r, la_m, la_hp, l_sp, hpf, mud, hrsh) in p_calibs_voc.items():
    pattern = rf'(p_idx == {p_idx} \? \([^\n]*\n)'
    calib_str = (
        f'    // AnalogObsession & ReEQ Producer Calibrations\n'
        f'    slider43 = {fet_r}; slider44 = {la_m}; slider45 = {la_hp}; slider46 = {l_sp};\n'
        f'    slider47 = {hpf}; slider48 = {mud}; slider49 = {hrsh};\n'
    )
    t = re.sub(pattern, rf'\1{calib_str}', t, count=1)

open(P, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
print('VocalSuite AnalogObsession patch complete.')
