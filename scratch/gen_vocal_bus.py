import os

target_path = r"c:\Dev\DameiSuite\effects\Damei_VocalBus.jsfx"

code = r'''desc:Damei Vocal Empress (Imperial Sceptre & Master Vocal Sum)
// =============================================================================
// DAMEI VOCAL EMPRESS // IMPERIAL SCEPTRE & MASTER VOCAL SUM (v1.0)
// Archetype: Duafe (The Wooden Comb - Pristine Grooming & Imperial Refinement)
// Summed Master Vocal Processing Engine with Dynamic Music Corridor Interlock
// Communication Range: gmem[1450..1499] (Publishes) | gmem[1400..1449] (Reads Instrumental Bus)
// Built by Damei Audio & Antigravity IDE
// =============================================================================

slider1:0<0,6,1{Empress Overview,Baxandall Master EQ,Vocal Bus Glue,De-Esser & Bleed Sentry,Spatial Immersion,Dynamic Presence Sentry,Producer Vocal Matrix}>-Active Module
slider2:0<0,24,1{Default Unity Baseline (1:1 Transparent Pass),Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Mirrorcell),Buster Odeholm (thrown / Northlane),Lewis Johns (Love Is Noise / blanket),Kel Pinchin (Split Chain / Currents Target),Dan Lancaster & Jason Perry (Don Broco),Erik Bickerstaffe (Static Dress),Sam Guaiana (Silverstein / TDWP),Zach Tuch (Heavenward / Hundredth),Forrester Savell (Karnivool),Leon Schmidt (SUNBORN - Nebula),Ermin Hamidovic (Systematic Benchmark),Will Putney (Fit For An Autopsy),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill - nerv),Henrik Udd (Architects - Gravity),Dan Braunstein (Spiritbox - Keep Sweet),Zakk Cervini & Erik Ron (Bad Omens),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Acle Kahney (TesseracT - King),Adam Cichocki (heaving. / Timber Studios),Manuel Renner (SENNA / Uberlarm Studios)}>-Producer Vocal Profile
slider3:0.0<-6.0,6.0,0.1>-Input Calibration (dB)
slider4:0.0<-12.0,6.0,0.1>-Master Vocal Trim (dB)
slider5:-6.0<-12.0,0.0,0.1>-Headroom Target Ceiling (dBTP)
slider6:1<0,1,1{Off,Strict -6 dBTP Guard (Zero Clip)}>-Auto-Headroom Guardian
slider7:0.0<-12.0,0.0,0.2>-Master De-Esser Sibilance Clamp (dB)
slider8:6800<4500,9500,50>-De-Esser Center Frequency (Hz)
slider9:0.0<-6.0,6.0,0.1>-Baxandall 100Hz Warmth Shelf (dB)
slider10:0.0<-6.0,6.0,0.1>-Baxandall 3.5kHz Clarity Bell (dB)
slider11:0.0<-6.0,6.0,0.1>-Baxandall 12kHz Air Sheen Shelf (dB)
slider12:0<0,1,1{Fairchild 670 (Smooth Tube),Opto 2A (Vocal Leveler)}>-Vocal Bus Glue Topology
slider13:0.0<-36.0,0.0,0.5>-Vocal Bus Glue Threshold (dB)
slider14:1<0,2,1{1.5:1 (Transparent Open),2:1 (Modern Pop-Metal),3:1 (Heavy Lock)}>-Vocal Bus Glue Ratio
slider15:25.0<1.0,80.0,1.0>-Vocal Bus Glue Attack (ms)
slider16:150.0<20.0,500.0,5.0>-Vocal Bus Glue Release (ms)
slider17:100<0,100,1>-Vocal Bus Glue Dry/Wet Mix (%)
slider18:1.00<0.80,1.30,0.01>-Vocal Spatial Width (Mid/Side)
slider19:1<0,1,1{Stereo Wide,Strict Mono Center Anchor}>-Lead Vocal Mono Lock
slider20:1.2<0.0,3.0,0.1>-Dynamic Music Corridor Request (dB)
slider21:0.0<0.0,10.0,0.1>-Vocal Tube Warmth Saturation (dB)
slider22:0<0,1,1{Bypassed,Engaged}>-Vocal Master Suite Engine

options:gmem=DameiMixMetering
options:maxmem=65536
in_pin:left input
in_pin:right input
out_pin:left output
out_pin:right output

@init
ext_noinit = 1;
srate <= 0 ? srate = 48000;

MEM_BASE = 2000;
f_deess_l = MEM_BASE;     f_deess_r = MEM_BASE + 10;
f_bax_low_l = MEM_BASE + 20; f_bax_low_r = MEM_BASE + 30;
f_bax_mid_l = MEM_BASE + 40; f_bax_mid_r = MEM_BASE + 50;
f_bax_air_l = MEM_BASE + 60; f_bax_air_r = MEM_BASE + 70;

sifam_tube_needle = 0;
sifam_vglue_needle = 0;
v_meter_rms_l = 0; v_meter_rms_r = 0;
v_comp_env = 0;
prev_vpreset = slider2;

function calc_svf_bell(freq, q_val, gain_db, mem_offset) (
  A_val = exp(gain_db * 0.11512925);
  g_val = tan($pi * max(20.0, min(22000.0, freq)) / srate);
  g_val <= 0.0 ? g_val = 0.05;
  k_val = 1.0 / max(0.2, q_val);
  a1 = 1.0 / (1.0 + g_val * (g_val + k_val));
  a2 = g_val * a1;
  a3 = g_val * a2;
  mem[mem_offset] = A_val; mem[mem_offset+1] = a1; mem[mem_offset+2] = a2; mem[mem_offset+3] = a3;
  mem[mem_offset+4] = k_val;
);

function eval_svf_bell(x, mem_offset) (
  v3 = x - mem[mem_offset+6];
  v1 = mem[mem_offset+1] * mem[mem_offset+5] + mem[mem_offset+2] * v3;
  v2 = mem[mem_offset+6] + mem[mem_offset+2] * mem[mem_offset+5] + mem[mem_offset+3] * v3;
  mem[mem_offset+5] = 2.0 * v1 - mem[mem_offset+5];
  mem[mem_offset+6] = 2.0 * v2 - mem[mem_offset+6];
  x + mem[mem_offset+4] * (mem[mem_offset] - 1.0) * v1;
);

function update_vocal_filters() (
  calc_svf_bell(slider8, 2.5, slider7, f_deess_l);
  calc_svf_bell(slider8, 2.5, slider7, f_deess_r);
  calc_svf_bell(100.0, 0.7, slider9, f_bax_low_l);
  calc_svf_bell(100.0, 0.7, slider9, f_bax_low_r);
  calc_svf_bell(3500.0, 1.2, slider10, f_bax_mid_l);
  calc_svf_bell(3500.0, 1.2, slider10, f_bax_mid_r);
  calc_svf_bell(12000.0, 0.7, slider11, f_bax_air_l);
  calc_svf_bell(12000.0, 0.7, slider11, f_bax_air_r);
);

function get_vocal_short_name(p_idx) (
  p_idx == 0  ? "0: UNITY" :
  p_idx == 1  ? "1: PRENC" :
  p_idx == 2  ? "2: SEIGEL" :
  p_idx == 3  ? "3: DOLESE" :
  p_idx == 4  ? "4: ODEHOLM" :
  p_idx == 5  ? "5: JOHNS" :
  p_idx == 6  ? "6: PINCHIN" :
  p_idx == 7  ? "7: LANCASTER" :
  p_idx == 8  ? "8: BICKERSTAFFE" :
  p_idx == 9  ? "9: GUAIANA" :
  p_idx == 10 ? "10: TUCH" :
  p_idx == 11 ? "11: SAVELL" :
  p_idx == 12 ? "12: SCHMIDT" :
  p_idx == 13 ? "13: HAMIDOVIC" :
  p_idx == 14 ? "14: PUTNEY" :
  p_idx == 15 ? "15: LEVER" :
  p_idx == 16 ? "16: BASSAL" :
  p_idx == 17 ? "17: UDD" :
  p_idx == 18 ? "18: BRAUNSTEIN" :
  p_idx == 19 ? "19: CERVINI" :
  p_idx == 20 ? "20: BOGREN" :
  p_idx == 21 ? "21: NOLLY" :
  p_idx == 22 ? "22: ACLE" :
  p_idx == 23 ? "23: CICHOCKI" :
  "24: RENNER";
);

function get_vocal_full_title(p_idx) (
  p_idx == 0  ? "Default Unity Baseline (1:1 Transparent Pass)" :
  p_idx == 1  ? "Lance Prenc (Alpha Wolf / Polaris)" :
  p_idx == 2  ? "Scott Seigel (DIESECT)" :
  p_idx == 3  ? "Jonathan Dolese (Mirrorcell)" :
  p_idx == 4  ? "Buster Odeholm (thrown / Northlane)" :
  p_idx == 5  ? "Lewis Johns (Love Is Noise / blanket)" :
  p_idx == 6  ? "Kel Pinchin (Split Chain / Currents Target)" :
  p_idx == 7  ? "Dan Lancaster & Jason Perry (Don Broco)" :
  p_idx == 8  ? "Erik Bickerstaffe (Static Dress)" :
  p_idx == 9  ? "Sam Guaiana (Silverstein / TDWP)" :
  p_idx == 10 ? "Zach Tuch (Heavenward / Hundredth)" :
  p_idx == 11 ? "Forrester Savell (Karnivool)" :
  p_idx == 12 ? "Leon Schmidt (SUNBORN - Nebula)" :
  p_idx == 13 ? "Ermin Hamidovic (Systematic Benchmark)" :
  p_idx == 14 ? "Will Putney (Fit For An Autopsy)" :
  p_idx == 15 ? "George Lever (Sleep Token / Loathe)" :
  p_idx == 16 ? "Sam Bassal (Thornhill - nerv)" :
  p_idx == 17 ? "Henrik Udd (Architects - Gravity)" :
  p_idx == 18 ? "Dan Braunstein (Spiritbox - Keep Sweet)" :
  p_idx == 19 ? "Zakk Cervini & Erik Ron (Bad Omens)" :
  p_idx == 20 ? "Jens Bogren (Fascination Street)" :
  p_idx == 21 ? "Adam Nolly Getgood (Periphery / GGD)" :
  p_idx == 22 ? "Acle Kahney (TesseracT - King)" :
  p_idx == 23 ? "Adam Cichocki (heaving. / Timber Studios)" :
  "Manuel Renner (SENNA / Uberlarm Studios)";
);

function apply_vocal_preset(p_idx) (
  p_idx == 0 ? ( // Default Unity Baseline
    slider3 = 0.0; slider4 = 0.0; slider5 = -6.0; slider6 = 1;
    slider7 = 0.0; slider8 = 6800; slider9 = 0.0; slider10 = 0.0; slider11 = 0.0;
    slider12 = 0; slider13 = 0.0; slider14 = 0; slider15 = 25.0; slider16 = 150.0;
    slider17 = 100; slider18 = 1.00; slider19 = 1; slider20 = 0.0; slider21 = 0.0; slider22 = 1;
  ) : p_idx == 1 ? ( // Lance Prenc
    slider4 = -2.5; slider7 = -2.8; slider9 = -1.2; slider10 = 2.5; slider11 = 2.5;
    slider12 = 0; slider13 = -18.0; slider14 = 1; slider15 = 15.0; slider16 = 100.0;
    slider18 = 1.05; slider20 = 1.8; slider21 = 2.2; slider22 = 1;
  ) : p_idx == 2 ? ( // Scott Seigel
    slider4 = -2.0; slider7 = -2.0; slider9 = 0.5; slider10 = 2.0; slider11 = 1.8;
    slider12 = 1; slider13 = -16.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.02; slider20 = 1.5; slider21 = 3.0; slider22 = 1;
  ) : p_idx == 3 ? ( // Jonathan Dolese
    slider4 = -2.0; slider7 = -2.2; slider9 = -0.5; slider10 = 2.2; slider11 = 2.8;
    slider12 = 0; slider13 = -15.0; slider14 = 0; slider15 = 25.0; slider16 = 140.0;
    slider18 = 1.08; slider20 = 1.4; slider21 = 1.5; slider22 = 1;
  ) : p_idx == 4 ? ( // Buster Odeholm
    slider4 = -3.0; slider7 = -3.5; slider9 = -1.5; slider10 = 1.8; slider11 = 1.2;
    slider12 = 0; slider13 = -20.0; slider14 = 2; slider15 = 10.0; slider16 = 80.0;
    slider18 = 1.00; slider20 = 2.0; slider21 = 3.5; slider22 = 1;
  ) : p_idx == 5 ? ( // Lewis Johns
    slider4 = -2.0; slider7 = -1.5; slider9 = 1.0; slider10 = 1.2; slider11 = 2.6;
    slider12 = 1; slider13 = -14.0; slider14 = 0; slider15 = 35.0; slider16 = 200.0;
    slider18 = 1.15; slider20 = 1.0; slider21 = 1.8; slider22 = 1;
  ) : p_idx == 6 ? ( // Kel Pinchin (Split Chain Target)
    slider4 = -2.5; slider7 = -2.4; slider9 = -0.8; slider10 = 2.2; slider11 = 2.4;
    slider12 = 0; slider13 = -16.5; slider14 = 1; slider15 = 20.0; slider16 = 130.0;
    slider18 = 1.06; slider20 = 1.6; slider21 = 2.0; slider22 = 1;
  ) : p_idx == 7 ? ( // Dan Lancaster
    slider4 = -3.0; slider7 = -2.5; slider9 = -1.0; slider10 = 2.8; slider11 = 3.0;
    slider12 = 0; slider13 = -18.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.10; slider20 = 1.8; slider21 = 2.2; slider22 = 1;
  ) : p_idx == 8 ? ( // Erik Bickerstaffe
    slider4 = -2.5; slider7 = -1.8; slider9 = 0.8; slider10 = 2.0; slider11 = 1.4;
    slider12 = 1; slider13 = -17.0; slider14 = 1; slider15 = 20.0; slider16 = 100.0;
    slider18 = 1.02; slider20 = 1.4; slider21 = 3.4; slider22 = 1;
  ) : p_idx == 9 ? ( // Sam Guaiana
    slider4 = -2.5; slider7 = -2.2; slider9 = -0.6; slider10 = 2.4; slider11 = 2.2;
    slider12 = 0; slider13 = -16.0; slider14 = 1; slider15 = 25.0; slider16 = 130.0;
    slider18 = 1.05; slider20 = 1.5; slider21 = 2.2; slider22 = 1;
  ) : p_idx == 10 ? ( // Zach Tuch
    slider4 = -2.0; slider7 = -1.5; slider9 = 1.2; slider10 = 1.4; slider11 = 2.2;
    slider12 = 1; slider13 = -14.0; slider14 = 0; slider15 = 30.0; slider16 = 180.0;
    slider18 = 1.12; slider20 = 1.0; slider21 = 2.0; slider22 = 1;
  ) : p_idx == 11 ? ( // Forrester Savell
    slider4 = -1.5; slider7 = -1.2; slider9 = 0.2; slider10 = 1.5; slider11 = 1.8;
    slider12 = 0; slider13 = -13.0; slider14 = 0; slider15 = 35.0; slider16 = 160.0;
    slider18 = 1.08; slider20 = 1.2; slider21 = 1.2; slider22 = 1;
  ) : p_idx == 12 ? ( // Leon Schmidt
    slider4 = -2.5; slider7 = -2.6; slider9 = -1.0; slider10 = 2.6; slider11 = 2.8;
    slider12 = 0; slider13 = -17.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.10; slider20 = 1.6; slider21 = 2.4; slider22 = 1;
  ) : p_idx == 13 ? ( // Ermin Hamidovic
    slider4 = -3.0; slider7 = -1.5; slider9 = 0.0; slider10 = 1.0; slider11 = 1.2;
    slider12 = 0; slider13 = -15.0; slider14 = 0; slider15 = 30.0; slider16 = 140.0;
    slider18 = 1.02; slider20 = 1.0; slider21 = 0.8; slider22 = 1;
  ) : p_idx == 14 ? ( // Will Putney
    slider4 = -3.5; slider7 = -3.2; slider9 = -1.2; slider10 = 2.6; slider11 = 1.8;
    slider12 = 0; slider13 = -19.0; slider14 = 2; slider15 = 15.0; slider16 = 100.0;
    slider18 = 1.02; slider20 = 1.8; slider21 = 3.6; slider22 = 1;
  ) : p_idx == 15 ? ( // George Lever
    slider4 = -2.0; slider7 = -1.8; slider9 = 1.2; slider10 = 1.6; slider11 = 2.2;
    slider12 = 1; slider13 = -15.0; slider14 = 0; slider15 = 30.0; slider16 = 180.0;
    slider18 = 1.12; slider20 = 1.2; slider21 = 2.6; slider22 = 1;
  ) : p_idx == 16 ? ( // Sam Bassal
    slider4 = -2.5; slider7 = -2.2; slider9 = -0.5; slider10 = 2.2; slider11 = 2.2;
    slider12 = 0; slider13 = -16.5; slider14 = 1; slider15 = 25.0; slider16 = 130.0;
    slider18 = 1.06; slider20 = 1.4; slider21 = 2.4; slider22 = 1;
  ) : p_idx == 17 ? ( // Henrik Udd
    slider4 = -3.0; slider7 = -2.8; slider9 = -0.8; slider10 = 2.6; slider11 = 2.8;
    slider12 = 0; slider13 = -18.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.08; slider20 = 1.8; slider21 = 2.5; slider22 = 1;
  ) : p_idx == 18 ? ( // Dan Braunstein
    slider4 = -3.0; slider7 = -2.5; slider9 = -0.8; slider10 = 2.5; slider11 = 3.2;
    slider12 = 0; slider13 = -17.5; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.10; slider20 = 1.8; slider21 = 2.2; slider22 = 1;
  ) : p_idx == 19 ? ( // Zakk Cervini
    slider4 = -3.0; slider7 = -2.8; slider9 = -1.0; slider10 = 2.8; slider11 = 3.0;
    slider12 = 0; slider13 = -18.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.08; slider20 = 1.8; slider21 = 2.6; slider22 = 1;
  ) : p_idx == 20 ? ( // Jens Bogren
    slider4 = -3.0; slider7 = -2.2; slider9 = 0.2; slider10 = 2.0; slider11 = 1.8;
    slider12 = 0; slider13 = -17.0; slider14 = 1; slider15 = 25.0; slider16 = 130.0;
    slider18 = 1.04; slider20 = 1.5; slider21 = 2.5; slider22 = 1;
  ) : p_idx == 21 ? ( // Nolly Getgood
    slider4 = -2.5; slider7 = -2.4; slider9 = -1.0; slider10 = 2.4; slider11 = 2.6;
    slider12 = 0; slider13 = -16.0; slider14 = 1; slider15 = 25.0; slider16 = 130.0;
    slider18 = 1.04; slider20 = 1.6; slider21 = 1.8; slider22 = 1;
  ) : p_idx == 22 ? ( // Acle Kahney
    slider4 = -2.0; slider7 = -1.8; slider9 = 0.0; slider10 = 1.8; slider11 = 2.0;
    slider12 = 0; slider13 = -14.0; slider14 = 0; slider15 = 30.0; slider16 = 150.0;
    slider18 = 1.06; slider20 = 1.2; slider21 = 1.0; slider22 = 1;
  ) : p_idx == 23 ? ( // Adam Cichocki (heaving.)
    slider4 = -2.5; slider7 = -2.0; slider9 = 0.8; slider10 = 1.8; slider11 = 2.8;
    slider12 = 1; slider13 = -16.0; slider14 = 1; slider15 = 25.0; slider16 = 140.0;
    slider18 = 1.12; slider20 = 1.4; slider21 = 3.2; slider22 = 1;
  ) : ( // Manuel Renner (SENNA)
    slider4 = -3.0; slider7 = -2.6; slider9 = -0.8; slider10 = 2.6; slider11 = 3.0;
    slider12 = 0; slider13 = -18.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.06; slider20 = 1.8; slider21 = 2.4; slider22 = 1;
  );
  update_vocal_filters();
);

update_vocal_filters();
apply_vocal_preset(slider2);

@slider
slider2 != prev_vpreset ? (
  prev_vpreset = slider2;
  apply_vocal_preset(slider2);
);
update_vocal_filters();

@block
// Read Instrumental Bus Telemetry (gmem[1400..1449])
ib_alive = (time_precise() - gmem[1400] < 1.5) && gmem[1401];
ib_inst_rms = ib_alive ? gmem[1402] : -90.0;

// Dynamic Corridor Request (Published to gmem[1460] for Instrumental Bus)
gmem[1460] = slider20;

// Compressor time constants
vcomp_att = exp(-1.0 / (max(0.1, slider15) * 0.001 * srate));
vcomp_rel = exp(-1.0 / (max(10.0, slider16) * 0.001 * srate));
vcomp_ratio = slider14 == 0 ? 1.5 : (slider14 == 1 ? 2.0 : 3.0);
vcomp_thresh = slider13;

in_gain_lin  = exp(slider3 * 0.11512925);
out_gain_lin = exp(slider4 * 0.11512925);
ceiling_lin  = exp(slider5 * 0.11512925);

@sample
s0 = spl0 * in_gain_lin;
s1 = spl1 * in_gain_lin;

slider22 ? (
  // 1. Master De-Esser Sibilance & Bleed Clamp
  slider7 < -0.01 ? (
    s0 = eval_svf_bell(s0, f_deess_l);
    s1 = eval_svf_bell(s1, f_deess_r);
  );

  // 2. Baxandall Master Vocal EQ
  s0 = eval_svf_bell(s0, f_bax_low_l); s1 = eval_svf_bell(s1, f_bax_low_r);
  s0 = eval_svf_bell(s0, f_bax_mid_l); s1 = eval_svf_bell(s1, f_bax_mid_r);
  s0 = eval_svf_bell(s0, f_bax_air_l); s1 = eval_svf_bell(s1, f_bax_air_r);

  // 3. Master Vocal Bus Glue Compressor
  v_max = max(abs(s0), abs(s1));
  v_db = v_max > 0.000001 ? 20.0 * log10(v_max) : -120.0;
  v_over = v_db - vcomp_thresh;
  v_over > 0.0 ? (
    vgr_target = v_over * (1.0 - 1.0 / vcomp_ratio);
  ) : (
    vgr_target = 0.0;
  );

  vgr_target > v_comp_env ? (
    v_comp_env = v_comp_env * vcomp_att + vgr_target * (1.0 - vcomp_att);
  ) : (
    v_comp_env = v_comp_env * vcomp_rel + vgr_target * (1.0 - vcomp_rel);
  );
  vglue_gr_db = v_comp_env;
  vglue_gain_lin = exp(-vglue_gr_db * 0.11512925);

  dry0 = s0; dry1 = s1;
  wet0 = s0 * vglue_gain_lin;
  wet1 = s1 * vglue_gain_lin;
  mix_ratio = slider17 * 0.01;
  s0 = dry0 * (1.0 - mix_ratio) + wet0 * mix_ratio;
  s1 = dry1 * (1.0 - mix_ratio) + wet1 * mix_ratio;

  // 4. Vocal Tube Warmth Saturation
  slider21 > 0.01 ? (
    t_drive = exp(slider21 * 0.11512925);
    d0 = s0 * t_drive; d1 = s1 * t_drive;
    s0 = (d0 + 0.15 * d0 * d0 - 0.05 * d0 * d0 * d0) / t_drive;
    s1 = (d1 + 0.15 * d1 * d1 - 0.05 * d1 * d1 * d1) / t_drive;
  );

  // 5. Spatial Immersion & Mono Lock
  mid = (s0 + s1) * 0.5;
  side = (s0 - s1) * 0.5 * slider18;
  slider19 ? ( // Strict Mono Center Lock
    s0 = mid + side * 0.85;
    s1 = mid - side * 0.85;
  ) : (
    s0 = mid + side;
    s1 = mid - side;
  );

  // 6. Output Master Trim
  s0 *= out_gain_lin;
  s1 *= out_gain_lin;

  // 7. Strict -6 dBTP Headroom Guardian
  slider6 ? (
    pk = max(abs(s0), abs(s1));
    pk > ceiling_lin ? (
      scale = ceiling_lin / pk;
      s0 *= scale;
      s1 *= scale;
    );
  );
);

spl0 = s0;
spl1 = s1;

// Ballistics & Telemetry
v_meter_rms_l = v_meter_rms_l * 0.999 + spl0 * spl0 * 0.001;
v_meter_rms_r = v_meter_rms_r * 0.999 + spl1 * spl1 * 0.001;
sifam_tube_needle = sifam_tube_needle * 0.95 + slider21 * 0.05;
sifam_vglue_needle = sifam_vglue_needle * 0.90 + vglue_gr_db * 0.10;

// Publish to gmem[1450..1499]
gmem[1450] = time_precise();
gmem[1451] = 1.0;
gmem[1452] = 10.0 * log10(max(0.0000001, (v_meter_rms_l + v_meter_rms_r) * 0.5));
gmem[1453] = max(abs(spl0), abs(spl1));
gmem[1454] = gmem[1453] > 0.0001 ? 20.0 * log10(gmem[1453]) - gmem[1452] : 12.0;
gmem[1455] = slider18;
gmem[1457] = slider2;

@gfx 840 480
disp_w = gfx_w; disp_h = gfx_h;

!fonts_initialized ? (
  gfx_setfont(1, "Orbitron", 13, 'b');
  gfx_setfont(2, "Orbitron", 10, 'b');
  gfx_setfont(3, "Consolas", 11, 'b');
  gfx_setfont(4, "Consolas", 10);
  fonts_initialized = 1;
);

// 1. Chassis Background (Deep Royal Plum)
gfx_r = 0.045; gfx_g = 0.020; gfx_b = 0.055;
gfx_rect(0, 0, disp_w, disp_h);

// 2. Top Header Bar
hdr_y = 6; hdr_h = 42;
gfx_r = 0.065; gfx_g = 0.030; gfx_b = 0.080;
gfx_rect(8, hdr_y, disp_w - 16, hdr_h);
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
gfx_rect(8, hdr_y, disp_w - 16, hdr_h, 0);

// Title & Adinkra Archetype
gfx_setfont(1, "Orbitron", 13, 'b');
gfx_r = 1.00; gfx_g = 0.92; gfx_b = 1.00;
gfx_x = 20; gfx_y = hdr_y + 6;
gfx_drawstr("V O C A L   E M P R E S S   //   M A S T E R   V O C A L   S U M");

gfx_setfont(4);
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
gfx_x = 20; gfx_y = hdr_y + 24;
gfx_drawstr("IMPERIAL SCEPTRE & VOCAL COHESION ENGINE // DUAFE MATRIX");

// Bypass Button
byp_w = 85; byp_h = 24; byp_x = disp_w - byp_w - 16; byp_y = hdr_y + 9;
byp_hov = (mouse_x >= byp_x && mouse_x <= byp_x + byp_w && mouse_y >= byp_y && mouse_y <= byp_y + byp_h);
gfx_r = slider22 ? (byp_hov ? 0.16 : 0.08) : (byp_hov ? 0.28 : 0.16);
gfx_g = slider22 ? (byp_hov ? 0.10 : 0.04) : (byp_hov ? 0.08 : 0.04);
gfx_b = slider22 ? (byp_hov ? 0.22 : 0.12) : (byp_hov ? 0.10 : 0.05);
gfx_rect(byp_x, byp_y, byp_w, byp_h);
gfx_r = slider22 ? 1.00 : 0.95; gfx_g = slider22 ? 0.41 : 0.30; gfx_b = slider22 ? 0.70 : 0.30;
gfx_rect(byp_x, byp_y, byp_w, byp_h, 0);
gfx_setfont(2); gfx_x = byp_x + (slider22 ? 12 : 10); gfx_y = byp_y + 5;
slider22 ? gfx_drawstr("ENGAGED") : gfx_drawstr("BYPASS");
(mouse_cap & 1) && !prev_mouse_cap && byp_hov ? (
  slider22 = !slider22;
  slider_automate(2097152);
);

// Music Bus Telemetry Link Indicator
link_w = 145; link_h = 24; link_x = byp_x - link_w - 10; link_y = hdr_y + 9;
gfx_r = ib_alive ? 0.06 : 0.08; gfx_g = ib_alive ? 0.12 : 0.06; gfx_b = ib_alive ? 0.16 : 0.08;
gfx_rect(link_x, link_y, link_w, link_h);
gfx_r = ib_alive ? 0.00 : 0.50; gfx_g = ib_alive ? 0.85 : 0.50; gfx_b = ib_alive ? 1.00 : 0.50;
gfx_rect(link_x, link_y, link_w, link_h, 0);
gfx_setfont(4); gfx_x = link_x + 8; gfx_y = link_y + 5;
ib_alive ? (
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_printf("MUSIC LINK: %.1fdB", ib_inst_rms);
) : (
  gfx_r = 0.60; gfx_g = 0.70; gfx_b = 0.80;
  gfx_drawstr("MUSIC LINK: STANDBY");
);

// 3. Navigation Tabs
tab_y = hdr_y + hdr_h + 6; tab_h = 24;
tab_w = floor((disp_w - 24) / 7);
ti = 0;
loop(7,
  tx = 12 + ti * tab_w;
  sel = (slider1 == ti);
  gfx_r = sel ? 0.14 : 0.045; gfx_g = sel ? 0.06 : 0.025; gfx_b = sel ? 0.18 : 0.060;
  gfx_rect(tx, tab_y, tab_w - 3, tab_h);
  sel ? (
    gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
    gfx_rect(tx, tab_y + tab_h - 2, tab_w - 3, 2);
    gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  ) : (
    gfx_r = 0.65; gfx_g = 0.60; gfx_b = 0.75;
  );
  gfx_setfont(4);
  t_lbl = (ti == 0 ? "OVERVIEW" : (ti == 1 ? "BAXANDALL" : (ti == 2 ? "VOCAL GLUE" : (ti == 3 ? "DE-ESSER" : (ti == 4 ? "SPATIAL" : (ti == 5 ? "PRESENCE" : "PRODUCER"))))));
  gfx_measurestr(t_lbl, tlw, tlh);
  gfx_x = floor(tx + (tab_w - 3 - tlw) * 0.5); gfx_y = tab_y + 6;
  gfx_drawstr(t_lbl);
  (mouse_cap & 1) && !prev_mouse_cap && (mouse_x >= tx && mouse_x <= tx + tab_w - 3 && mouse_y >= tab_y && mouse_y <= tab_y + tab_h) ? (
    slider1 = ti;
    slider_automate(1);
  );
  ti += 1;
);

// Central Workspace
ws_x = 10; ws_y = tab_y + tab_h + 6;
ws_w = disp_w - 20; ws_h = disp_h - ws_y - 10;
gfx_r = 0.030; gfx_g = 0.015; gfx_b = 0.038;
gfx_rect(ws_x, ws_y, ws_w, ws_h);
gfx_r = 0.18; gfx_g = 0.10; gfx_b = 0.22;
gfx_rect(ws_x, ws_y, ws_w, ws_h, 0);

// =============================================================================
// TAB 0: EMPRESS OVERVIEW (TWIN SIFAM ANALOG METERS & VOCAL COHESION CALIBRATION)
// =============================================================================
slider1 == 0 ? (
  sm_y = ws_y + 12; sm_h = 175;
  sm_w = floor((ws_w - 30) / 2);

  // Meter 1: Vocal Tube Warmth
  m1_x = ws_x + 10;
  gfx_r = 0.020; gfx_g = 0.012; gfx_b = 0.028; gfx_rect(m1_x, sm_y, sm_w, sm_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(m1_x, sm_y, sm_w, sm_h, 0);
  gfx_setfont(2); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = m1_x + 12; gfx_y = sm_y + 10; gfx_drawstr("VOCAL TUBE WARMTH / SATURATION %");
  n1_cx = m1_x + sm_w * 0.5; n1_cy = sm_y + sm_h - 15;
  n1_ang = -0.7 + (min(10.0, sifam_tube_needle) / 10.0) * 1.4;
  n1_len = sm_h * 0.65;
  gfx_line(n1_cx, n1_cy, n1_cx + sin(n1_ang) * n1_len, n1_cy - cos(n1_ang) * n1_len);
  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.70; gfx_b = 0.88;
  gfx_x = m1_x + 12; gfx_y = sm_y + sm_h - 30;
  gfx_printf("+%.1f dB TUBE", slider21);

  // Meter 2: Master Vocal Bus Glue GR
  m2_x = m1_x + sm_w + 10;
  gfx_r = 0.020; gfx_g = 0.012; gfx_b = 0.028; gfx_rect(m2_x, sm_y, sm_w, sm_h);
  gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(m2_x, sm_y, sm_w, sm_h, 0);
  gfx_setfont(2); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = m2_x + 12; gfx_y = sm_y + 10; gfx_drawstr("MASTER VOCAL BUS GLUE GR (dB)");
  n2_cx = m2_x + sm_w * 0.5; n2_cy = sm_y + sm_h - 15;
  n2_ang = -0.7 + (min(10.0, sifam_vglue_needle) / 10.0) * 1.4;
  gfx_line(n2_cx, n2_cy, n2_cx + sin(n2_ang) * n1_len, n2_cy - cos(n2_ang) * n1_len);
  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = m2_x + 12; gfx_y = sm_y + sm_h - 30;
  gfx_printf("-%.1f dB GR", sifam_vglue_needle);

  // Bottom Status & Controls Plaque
  p_y = sm_y + sm_h + 12; p_h = ws_h - sm_h - 30;
  gfx_r = 0.040; gfx_g = 0.022; gfx_b = 0.050; gfx_rect(ws_x + 10, p_y, ws_w - 20, p_h);
  gfx_r = 0.22; gfx_g = 0.12; gfx_b = 0.28; gfx_rect(ws_x + 10, p_y, ws_w - 20, p_h, 0);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.00; gfx_g = 0.90; gfx_b = 1.00;
  gfx_x = ws_x + 24; gfx_y = p_y + 12;
  gfx_printf("ACTIVE PROFILE: %02d - %s", slider2, get_vocal_full_title(slider2));

  gfx_setfont(3); gfx_r = 0.90; gfx_g = 0.80; gfx_b = 0.98;
  gfx_x = ws_x + 24; gfx_y = p_y + 36;
  gfx_printf("CALIBRATION: Trim: %+4.1fdB | Ceiling: %.1fdBTP | De-Ess: %.1fdB @ %dHz | Bax Air: %+.1fdB | Width: %.2fx",
    slider4, slider5, slider7, slider8, slider11, slider18);

  gfx_setfont(4); gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  gfx_x = ws_x + 24; gfx_y = p_y + 60;
  gfx_printf("Summing State: %s | Glue Topology: %s | Music Corridor Request: %.1fdB",
    slider22 ? "ENGAGED (ACTIVE VOCAL SUM)" : "BYPASS (1:1 UNITY PASS)",
    slider12 ? "Opto 2A Vocal Leveler" : "Fairchild 670 Smooth Tube", slider20);
);

// =============================================================================
// TAB 6: PRODUCER VOCAL MATRIX (25 MIXING BENCHMARKS)
// =============================================================================
slider1 == 6 ? (
  mat_y = ws_y + 10;
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_setfont(1, "Orbitron", 14, 'b');
  gfx_x = ws_x + 14; gfx_y = mat_y;
  gfx_drawstr("PRODUCER VOCAL MATRIX // 25 REFERENCE-CALIBRATED BENCHMARKS");

  pi = 0; pill_w = floor((ws_w - 32 - 36) / 7); pill_h = 32;
  loop(25,
    p_row = floor(pi / 7); p_col = pi % 7;
    px = ws_x + 12 + p_col * (pill_w + 6);
    py = mat_y + 26 + p_row * (pill_h + 6);
    is_sel = (slider2 == pi);
    p_hov = (mouse_x >= px && mouse_x <= px + pill_w && mouse_y >= py && mouse_y <= py + pill_h);

    gfx_r = is_sel ? 0.22 : (p_hov ? 0.12 : 0.045);
    gfx_g = is_sel ? 0.08 : (p_hov ? 0.05 : 0.025);
    gfx_b = is_sel ? 0.24 : (p_hov ? 0.14 : 0.060);
    gfx_rect(px, py, pill_w, pill_h);

    gfx_r = is_sel ? 1.00 : (p_hov ? 0.60 : 0.30);
    gfx_g = is_sel ? 0.41 : (p_hov ? 0.25 : 0.15);
    gfx_b = is_sel ? 0.70 : (p_hov ? 0.45 : 0.20);
    gfx_rect(px, py, pill_w, pill_h, 0);

    gfx_setfont(3);
    is_sel ? (gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;) : (gfx_r = 0.90; gfx_g = 0.85; gfx_b = 0.98;);
    p_sname = get_vocal_short_name(pi);
    gfx_measurestr(p_sname, psw, psh);
    gfx_x = floor(px + (pill_w - psw) * 0.5); gfx_y = py + 8;
    gfx_drawstr(p_sname);

    (mouse_cap & 1) && !prev_mouse_cap && p_hov ? (
      slider2 = pi;
      prev_vpreset = slider2;
      apply_vocal_preset(slider2);
      slider_automate(2);
    );
    pi += 1;
  );

  pl_y = mat_y + 185; pl_w = ws_w - 24; pl_h = ws_h - 195;
  gfx_r = 0.040; gfx_g = 0.022; gfx_b = 0.050; gfx_rect(ws_x + 12, pl_y, pl_w, pl_h);
  gfx_r = 0.22; gfx_g = 0.12; gfx_b = 0.28; gfx_rect(ws_x + 12, pl_y, pl_w, pl_h, 0);

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 24; gfx_y = pl_y + 12;
  gfx_printf("SELECTED BENCHMARK: %02d - %s", slider2, get_vocal_full_title(slider2));

  gfx_setfont(3); gfx_r = 0.90; gfx_g = 0.80; gfx_b = 0.98;
  gfx_x = ws_x + 24; gfx_y = pl_y + 36;
  gfx_printf("SETTINGS: Trim %+.1fdB | De-Ess %+.1fdB | Bax Mid %+.1fdB | Bax Air %+.1fdB | Tube %+.1fdB | Music Corridor: %.1fdB",
    slider4, slider7, slider10, slider11, slider21, slider20);
);

prev_mouse_cap = mouse_cap;
'''

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Damei_VocalBus.jsfx generated successfully.")
