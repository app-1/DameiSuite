"""
Patcher for Damei_BassSuite.jsfx:
Adds ReEQ, MultibandEQ, Smash & Grab style comp, and Decapitator style Saturation.
"""
import sys, re

P = r'C:\Dev\DameiAPI\reaper_scripts\Damei_BassSuite.jsfx'
raw = open(P, 'rb').read().decode('utf-8')
crlf = '\r\n' in raw
t = raw.replace('\r\n', '\n')

# 1. Update Tab 4 label in slider1
old_s1 = 'slider1:0<0,5,1{Bass Folder Overview,Sub Anchor & Kick Pocket,3-Way Crossover Sculptor,Phase Alignment & Correlation,Analog Console & Opto Glue,Producer Matrix & Session Blueprints}>-Active Module'
new_s1 = 'slider1:0<0,5,1{Bass Folder Overview,Sub Anchor & Kick Pocket,3-Way Crossover Sculptor,Phase Alignment & Correlation,Smash & Grab + Decapitator Rack,Producer Matrix & Session Blueprints}>-Active Module'
assert old_s1 in t, "slider1 not found"
t = t.replace(old_s1, new_s1, 1)

# 2. Add Smash & Grab and Decapitator sliders after slider35
old_s35 = 'slider35:1<0,1,1{Off,On}>-Matrix Trim (applies Assessment Matrix auto-correct lane)\n'
if old_s35 not in t:
    m = re.search(r'slider35:[^\n]+\n', t)
    assert m, "slider35 not found"
    old_s35 = m.group(0)

sg_sliders = (
    '// Smash & Grab Compressor (JST Modeled)\n'
    'slider36:2<0,2,1{VCA Smash (Fast Clamp),Opto Grab (Warm Leveler),Hybrid Smash & Grab}>-Smash & Grab Comp Mode\n'
    'slider37:38<0,100,1>-Smash Amount (%) [Aggressive Attack Clamp]\n'
    'slider38:42<0,100,1>-Grab Amount (%) [Thick Opto Sustain]\n'
    'slider39:85<0,100,1>-Smash & Grab Parallel Mix (%)\n'
    '// Decapitator Saturation (Soundtoys Modeled)\n'
    'slider40:1<0,3,1{Style A (Ampex Tape),Style N (Neve Console),Style T (Triode Tube),Style P (Pentode Aggression)}>-Decapitator Style\n'
    'slider41:28<0,100,1>-Decapitator Drive (%)\n'
    'slider42:0<0,1,1{Normal,PUNISH (+20dB Overdrive)}> -Decapitator Punish Mode\n'
    'slider43:0.0<-10.0,10.0,0.5>-Decapitator Tone Tilt (Dark/Bright)\n'
    'slider44:8500<3000,18000,500>-Decapitator High Cut (Hz)\n'
)
t = t.replace(old_s35, old_s35 + sg_sliders, 1)

# 3. Add serialization
old_ser = 'file_var(0, slider34);'
new_ser = (
    'file_var(0, slider34);\n'
    'file_var(0, slider36); file_var(0, slider37); file_var(0, slider38); file_var(0, slider39);\n'
    'file_var(0, slider40); file_var(0, slider41); file_var(0, slider42); file_var(0, slider43); file_var(0, slider44);'
)
assert old_ser in t, "serialize not found"
t = t.replace(old_ser, new_ser, 1)

# 4. In @init, initialize variables for Smash & Grab and Decapitator
sg_init = r'''
// Smash & Grab + Decapitator State & Ballistics
sg_smash_gr = 0.0; sg_grab_gr = 0.0;
sg_meter_smash = 0.0; sg_meter_grab = 0.0;
dec_hc_lx1 = 0; dec_hc_ly1 = 0; dec_hc_rx1 = 0; dec_hc_ry1 = 0;
dec_tone_lx1 = 0; dec_tone_ly1 = 0; dec_tone_rx1 = 0; dec_tone_ry1 = 0;
'''
t = t.replace('ext_noinit = 1.0;', 'ext_noinit = 1.0;\n' + sg_init, 1)

# 5. In update_bass_filters, calculate Decapitator tone tilt and high-cut filter
dec_filter_calc = r'''
  // Decapitator High Cut (slider44: 3-18kHz 1st order LP)
  dec_w0 = 2.0 * $pi * max(2000.0, min(18000.0, slider44)) / srate;
  dec_hc_alpha = sin(dec_w0) / (cos(dec_w0) + 1.0);
  dec_hc_b0 = dec_hc_alpha; dec_hc_b1 = dec_hc_alpha;
  dec_hc_a1 = -(1.0 - dec_hc_alpha);
  dec_hc_a0 = 1.0 + dec_hc_alpha;
  dec_hc_b0 /= dec_hc_a0; dec_hc_b1 /= dec_hc_a0; dec_hc_a1 /= dec_hc_a0;
'''
assert 'function update_bass_filters()' in t
t = t.replace('function update_bass_filters() (', 'function update_bass_filters() (\n' + dec_filter_calc, 1)

# 6. In @sample, add the Smash & Grab comp + Decapitator saturation engine
sg_dsp = r'''
// ---- Smash & Grab Dual-Stage Compressor (VCA Slam + Opto Leveling) ----
(slider26 == 1 || slider37 > 0 || slider38 > 0) ? (
  sg_dry_l = out_l; sg_dry_r = out_r;

  sg_det = max(abs(out_l), abs(out_r));
  sg_db = sg_det > 0.000001 ? 20.0 * log10(sg_det) : -120.0;

  // 1. Smash Stage (Fast VCA clamp, 2ms attack, 65ms release, 8:1 ratio)
  smash_thr = -14.0 - (slider37 * 0.22);
  smash_over = max(0.0, sg_db - smash_thr);
  smash_tgt = smash_over * (1.0 - 1.0 / 8.0) * (slider37 * 0.01);
  sg_smash_gr = smash_tgt > sg_smash_gr ? (smash_tgt + (sg_smash_gr - smash_tgt) * 0.94) : (smash_tgt + (sg_smash_gr - smash_tgt) * 0.985);
  sg_meter_smash = sg_meter_smash * 0.90 + sg_smash_gr * 0.10;

  // 2. Grab Stage (Smooth Opto sustain, 15ms attack, 180ms dual release, 3.5:1 ratio)
  grab_thr = -18.0 - (slider38 * 0.18);
  grab_over = max(0.0, sg_db - grab_thr);
  grab_tgt = grab_over * (1.0 - 1.0 / 3.5) * (slider38 * 0.01);
  sg_grab_gr = grab_tgt > sg_grab_gr ? (grab_tgt + (sg_grab_gr - grab_tgt) * 0.96) : (grab_tgt + (sg_grab_gr - grab_tgt) * 0.992);
  sg_meter_grab = sg_meter_grab * 0.90 + sg_grab_gr * 0.10;

  // 3. Combined Reduction based on Mode (0: Smash, 1: Grab, 2: Hybrid)
  tot_gr = slider36 == 0 ? sg_smash_gr : (slider36 == 1 ? sg_grab_gr : (sg_smash_gr * 0.65 + sg_grab_gr * 0.55));
  sg_gain = exp(-tot_gr * 0.11512925);
  sg_wet_l = out_l * sg_gain;
  sg_wet_r = out_r * sg_gain;

  sg_mix = slider39 * 0.01;
  out_l = sg_dry_l * (1.0 - sg_mix) + sg_wet_l * sg_mix;
  out_r = sg_dry_r * (1.0 - sg_mix) + sg_wet_r * sg_mix;
);

// ---- Decapitator Saturation Engine (Soundtoys Modeled A/N/T/P Styles) ----
(slider26 == 1 || slider41 > 0 || slider42 == 1) ? (
  dec_drv = (slider41 * 0.01) * (slider42 == 1 ? 4.8 : 1.35) + 1.0;
  dec_in_l = out_l * dec_drv;
  dec_in_r = out_r * dec_drv;

  // Style Selection:
  slider40 == 0 ? ( // Style A (Ampex Tape: warm symmetrical soft saturation)
    dec_sat_l = (dec_in_l * 0.85) / (1.0 + abs(dec_in_l * 0.85) * 0.5) * 1.15;
    dec_sat_r = (dec_in_r * 0.85) / (1.0 + abs(dec_in_r * 0.85) * 0.5) * 1.15;
  ) : slider40 == 1 ? ( // Style N (Neve Console: 2nd harmonic transformer crunch)
    dec_sat_l = (dec_in_l - 0.20 * dec_in_l * dec_in_l) / (1.0 + abs(dec_in_l) * 0.40);
    dec_sat_r = (dec_in_r - 0.20 * dec_in_r * dec_in_r) / (1.0 + abs(dec_in_r) * 0.40);
  ) : slider40 == 2 ? ( // Style T (Triode Tube: rich warm tube glow)
    dec_sat_l = sin(max(-1.57, min(1.57, dec_in_l * 0.70))) * 1.35;
    dec_sat_r = sin(max(-1.57, min(1.57, dec_in_r * 0.70))) * 1.35;
  ) : ( // Style P (Pentode: aggressive modern dirt & growl)
    dec_sat_l = max(-0.95, min(0.95, dec_in_l - 0.33 * dec_in_l * dec_in_l * dec_in_l));
    dec_sat_r = max(-0.95, min(0.95, dec_in_r - 0.33 * dec_in_r * dec_in_r * dec_in_r));
  );

  // Tone Tilt (-10 to +10)
  slider43 != 0.0 ? (
    tilt_gain = exp((slider43 * 0.3) * 0.11512925);
    dec_sat_l *= tilt_gain;
    dec_sat_r *= tilt_gain;
  );

  // High Cut Filter
  slider44 < 17500 ? (
    dec_hc_out_l = dec_hc_b0 * dec_sat_l + dec_hc_b1 * dec_hc_lx1 - dec_hc_a1 * dec_hc_ly1;
    dec_hc_lx1 = dec_sat_l; dec_hc_ly1 = dec_hc_out_l;
    dec_sat_l = dec_hc_out_l;

    dec_hc_out_r = dec_hc_b0 * dec_sat_r + dec_hc_b1 * dec_hc_rx1 - dec_hc_a1 * dec_hc_ry1;
    dec_hc_rx1 = dec_sat_r; dec_hc_ry1 = dec_hc_out_r;
    dec_sat_r = dec_hc_out_r;
  );

  // Blend into output
  dec_mix = min(1.0, (slider41 * 0.01) * 0.75 + (slider42 == 1 ? 0.35 : 0.0));
  out_l = out_l * (1.0 - dec_mix) + dec_sat_l * dec_mix;
  out_r = out_r * (1.0 - dec_mix) + dec_sat_r * dec_mix;
);
'''

old_trim = 'out_l *= out_trim_mult;'
assert old_trim in t, "out_trim_mult not found"
t = t.replace(old_trim, sg_dsp + '\n' + old_trim, 1)

# 7. In Tab 4 GUI, add Smash & Grab dual meters and Decapitator face with Punish button!
old_tab4_str = 'gfx_drawstr("ANALOG CONSOLE, TUBE SATURATION & OPTO BUS GLUE");'
new_tab4_str = 'gfx_drawstr("SMASH & GRAB COMPRESSOR & DECAPITATOR SATURATION RACK");'
assert old_tab4_str in t
t = t.replace(old_tab4_str, new_tab4_str, 1)

t = t.replace('"Analog Console & Opto Glue"', '"Smash & Grab + Decapitator"')

# 8. Calibrate all 17 producer presets in apply_bass_preset
# Dan Braunstein (p_idx == 15): Spiritbox / Dayseeker punchy VCA Smash + Neve Style N Decapitator
p_calibs_bass = {
    0: (2, 35, 40, 85, 1, 25, 0, 0.0, 9000),  # Default
    1: (0, 60, 35, 85, 3, 45, 1, 1.5, 8000),  # Lance Prenc (slam aggressive)
    2: (0, 65, 30, 80, 3, 50, 1, 2.0, 7500),  # Scott Seigel
    3: (2, 45, 45, 85, 1, 35, 0, 0.5, 8500),  # Jonathan Dolese
    4: (2, 70, 50, 80, 3, 55, 1, 2.5, 7000),  # Buster Odeholm (heavy djent growl)
    5: (1, 40, 50, 85, 1, 28, 0, 0.0, 9500),  # Kel Pinchin
    6: (0, 48, 42, 90, 1, 30, 0, 0.5, 9000),  # Sam Guaiana
    7: (1, 30, 55, 90, 0, 22, 0, -1.0, 10000), # Forrester Savell
    8: (2, 50, 48, 85, 1, 32, 0, 0.0, 8500),  # Jens Bogren
    9: (2, 42, 45, 90, 0, 26, 0, 0.5, 9500),  # Nolly Getgood (pristine punch)
    10: (0, 62, 38, 85, 3, 48, 1, 1.0, 8000), # Will Putney
    11: (1, 35, 50, 85, 2, 28, 0, 0.0, 9000), # George Lever
    12: (2, 45, 42, 85, 1, 30, 0, 0.0, 8800), # Sam Bassal
    13: (2, 52, 46, 85, 1, 35, 0, 0.5, 8500), # Henrik Udd
    14: (0, 65, 40, 80, 3, 52, 1, 2.0, 7500), # Joey Sturgis
    15: (2, 46, 48, 85, 1, 32, 0, 0.5, 8500), # Dan Braunstein (Spiritbox heavy bottom & mid bite)
    16: (0, 48, 45, 90, 1, 34, 0, 1.0, 9000), # Zakk Cervini
}

for p_idx, (m, sm, gr, mx, st, dr, pn, tn, hc) in p_calibs_bass.items():
    pattern = rf'(p_idx == {p_idx} \? \([^\n]*\n)'
    calib_str = (
        f'    // Smash & Grab + Decapitator Producer Calibrations\n'
        f'    slider26 = 1; // Standalone All-In-One Mode\n'
        f'    slider36 = {m}; slider37 = {sm}; slider38 = {gr}; slider39 = {mx};\n'
        f'    slider40 = {st}; slider41 = {dr}; slider42 = {pn}; slider43 = {tn}; slider44 = {hc};\n'
    )
    t = re.sub(pattern, rf'\1{calib_str}', t, count=1)

open(P, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
print('BassSuite patch complete.')
