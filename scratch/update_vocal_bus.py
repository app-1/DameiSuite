import os

target_path = r"c:\Dev\DameiSuite\effects\Damei_VocalBus.jsfx"

code = r'''desc:Damei Vocal Empress (Imperial Sceptre & Master Vocal Sum)
// =============================================================================
// DAMEI VOCAL EMPRESS // IMPERIAL SCEPTRE & MASTER VOCAL SUM (v1.1)
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

// High-precision smooth polynomial Pade approximation of tanh(x)
function fast_tanh(x) (
  x <= -3.0 ? -1.0 :
  x >= 3.0  ?  1.0 :
  (x * (27.0 + x * x)) / (27.0 + 9.0 * x * x);
);

MEM_BASE = 2000;
f_deess_l = MEM_BASE;     f_deess_r = MEM_BASE + 10;
f_bax_low_l = MEM_BASE + 20; f_bax_low_r = MEM_BASE + 30;
f_bax_mid_l = MEM_BASE + 40; f_bax_mid_r = MEM_BASE + 50;
f_bax_air_l = MEM_BASE + 60; f_bax_air_r = MEM_BASE + 70;

sifam_tube_needle = 0;
sifam_vglue_needle = 0;
v_meter_rms_l = 0; v_meter_rms_r = 0;
v_meter_peak_l = 0; v_meter_peak_r = 0;
v_comp_env = 0;
prev_vpreset = slider2;

// SVF Filter implementation
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
  p_idx == 21 ? "21: GETGOOD" :
  p_idx == 22 ? "22: KAHNEY" :
  p_idx == 23 ? "23: CICHOCKI" :
                "24: RENNER"
);

function get_vocal_full_title(p_idx) (
  p_idx == 0  ? "Default Unity Baseline (1:1 Pass)" :
  p_idx == 1  ? "Lance Prenc (Alpha Wolf / Polaris)" :
  p_idx == 2  ? "Scott Seigel (DIESECT)" :
  p_idx == 3  ? "Jonathan Dolese (Mirrorcell)" :
  p_idx == 4  ? "Buster Odeholm (thrown / Humanity's Last Breath)" :
  p_idx == 5  ? "Lewis Johns (Love Is Noise / blanket)" :
  p_idx == 6  ? "Kel Pinchin (Split Chain / Currents Target)" :
  p_idx == 7  ? "Dan Lancaster & Jason Perry (Don Broco)" :
  p_idx == 8  ? "Erik Bickerstaffe (Static Dress)" :
  p_idx == 9  ? "Sam Guaiana (Silverstein / The Devil Wears Prada)" :
  p_idx == 10 ? "Zach Tuch (Heavenward / Hundredth)" :
  p_idx == 11 ? "Forrester Savell (Karnivool / Twelve Foot Ninja)" :
  p_idx == 12 ? "Leon Schmidt (SUNBORN - Nebula)" :
  p_idx == 13 ? "Ermin Hamidovic (Systematic Benchmark)" :
  p_idx == 14 ? "Will Putney (Fit For An Autopsy / Knocked Loose)" :
  p_idx == 15 ? "George Lever (Sleep Token / Loathe)" :
  p_idx == 16 ? "Sam Bassal (Thornhill - Heroine)" :
  p_idx == 17 ? "Henrik Udd (Architects - Holy Hell)" :
  p_idx == 18 ? "Dan Braunstein (Spiritbox - Keep Sweet)" :
  p_idx == 19 ? "Zakk Cervini & Erik Ron (Bad Omens - TDOPOM)" :
  p_idx == 20 ? "Jens Bogren (Fascination Street Studios)" :
  p_idx == 21 ? "Adam Nolly Getgood (Periphery / GGD)" :
  p_idx == 22 ? "Acle Kahney (TesseracT - King)" :
  p_idx == 23 ? "Adam Cichocki (heaving. / Timber Studios)" :
                "Manuel Renner (SENNA / Uberlarm Studios)"
);

function apply_vocal_preset(p_idx) (
  p_idx == 0 ? ( // Default Unity Baseline (1:1 Transparent Pass)
    slider4 = 0.0; slider7 = 0.0; slider9 = 0.0; slider10 = 0.0; slider11 = 0.0;
    slider12 = 0; slider13 = 0.0; slider14 = 0; slider15 = 25.0; slider16 = 150.0;
    slider18 = 1.00; slider20 = 1.2; slider21 = 0.0; slider22 = 0;
  ) : p_idx == 1 ? ( // Lance Prenc
    slider4 = -3.0; slider7 = -2.8; slider9 = -1.2; slider10 = 2.4; slider11 = 2.6;
    slider12 = 0; slider13 = -18.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.05; slider20 = 1.8; slider21 = 2.5; slider22 = 1;
  ) : p_idx == 2 ? ( // Scott Seigel
    slider4 = -2.5; slider7 = -3.0; slider9 = -0.8; slider10 = 2.6; slider11 = 2.0;
    slider12 = 0; slider13 = -19.0; slider14 = 2; slider15 = 15.0; slider16 = 100.0;
    slider18 = 1.02; slider20 = 2.0; slider21 = 3.5; slider22 = 1;
  ) : p_idx == 3 ? ( // Jonathan Dolese
    slider4 = -2.5; slider7 = -2.2; slider9 = -0.5; slider10 = 2.0; slider11 = 2.8;
    slider12 = 1; slider13 = -16.0; slider14 = 1; slider15 = 25.0; slider16 = 140.0;
    slider18 = 1.08; slider20 = 1.5; slider21 = 2.0; slider22 = 1;
  ) : p_idx == 4 ? ( // Buster Odeholm
    slider4 = -3.5; slider7 = -3.5; slider9 = -1.5; slider10 = 3.0; slider11 = 1.5;
    slider12 = 0; slider13 = -20.0; slider14 = 2; slider15 = 12.0; slider16 = 90.0;
    slider18 = 1.00; slider20 = 2.2; slider21 = 4.2; slider22 = 1;
  ) : p_idx == 5 ? ( // Lewis Johns
    slider4 = -2.0; slider7 = -1.5; slider9 = 1.0; slider10 = 1.2; slider11 = 2.0;
    slider12 = 1; slider13 = -14.0; slider14 = 0; slider15 = 35.0; slider16 = 200.0;
    slider18 = 1.15; slider20 = 1.0; slider21 = 2.8; slider22 = 1;
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

@slider
slider2 != prev_vpreset ? (
  prev_vpreset = slider2;
  apply_vocal_preset(slider2);
);

update_vocal_filters();

in_gain_lin = exp(slider3 * 0.11512925);
out_gain_lin = exp(slider4 * 0.11512925);
ceiling_lin = exp(slider5 * 0.11512925);

vcomp_ratio = slider14 == 0 ? 1.5 : (slider14 == 1 ? 2.0 : 3.0);
vcomp_att = exp(-1.0 / (slider15 * 0.001 * srate));
vcomp_rel = exp(-1.0 / (slider16 * 0.001 * srate));

@sample
s0 = spl0;
s1 = spl1;

// Read Instrumental Bus Heartbeat from gmem[1400..1449]
ib_time = gmem[1400];
ib_alive = (time_precise() - ib_time) < 0.5;
ib_inst_rms = ib_alive ? gmem[1402] : -60.0;

slider22 ? (
  // 1. Input Calibration
  s0 *= in_gain_lin;
  s1 *= in_gain_lin;

  // 2. Baxandall Master EQ
  s0 = eval_svf_bell(s0, f_bax_low_l);
  s1 = eval_svf_bell(s1, f_bax_low_r);
  s0 = eval_svf_bell(s0, f_bax_mid_l);
  s1 = eval_svf_bell(s1, f_bax_mid_r);
  s0 = eval_svf_bell(s0, f_bax_air_l);
  s1 = eval_svf_bell(s1, f_bax_air_r);

  // De-Esser clamp
  slider7 < -0.1 ? (
    s0 = eval_svf_bell(s0, f_deess_l);
    s1 = eval_svf_bell(s1, f_deess_r);
  );

  // 3. Master Vocal Bus Glue Compressor
  det = max(abs(s0), abs(s1));
  det_db = det > 0.000001 ? 20.0 * log10(det) : -120.0;
  det_db > slider13 ? (
    over_db = det_db - slider13;
    vgr_target = over_db * (1.0 - 1.0 / vcomp_ratio);
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

// 1. Chassis Background (Deep Royal Empress Violet/Plum)
gfx_r = 0.038; gfx_g = 0.016; gfx_b = 0.048;
gfx_rect(0, 0, disp_w, disp_h);

// 2. Top Header Bar
hdr_y = 6; hdr_h = 42;
gfx_r = 0.058; gfx_g = 0.024; gfx_b = 0.072;
gfx_rect(8, hdr_y, disp_w - 16, hdr_h);
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
gfx_rect(8, hdr_y, disp_w - 16, hdr_h, 0);

// Bypass Button
byp_w = 85; byp_h = 24; byp_x = disp_w - byp_w - 16; byp_y = hdr_y + 9;
byp_hov = (mouse_x >= byp_x && mouse_x <= byp_x + byp_w && mouse_y >= byp_y && mouse_y <= byp_y + byp_h);
gfx_r = slider22 ? (byp_hov ? 0.18 : 0.09) : (byp_hov ? 0.28 : 0.16);
gfx_g = slider22 ? (byp_hov ? 0.08 : 0.04) : (byp_hov ? 0.08 : 0.04);
gfx_b = slider22 ? (byp_hov ? 0.24 : 0.13) : (byp_hov ? 0.10 : 0.05);
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

// Title & Adinkra Archetype (Auto-Fit & Zero Spillage)
max_title_w = max(100, link_x - 30);
title_str = disp_w < 740 ? "VOCAL EMPRESS // MASTER VOCAL SUM" : "V O C A L   E M P R E S S   //   M A S T E R   V O C A L   S U M";
t_font_sz = 13.0;
gfx_setfont(1, "Orbitron", t_font_sz, 'b');
gfx_measurestr(title_str, tsw, tsh);
while (tsw > max_title_w && t_font_sz > 8.0) (
  t_font_sz -= 0.5;
  gfx_setfont(1, "Orbitron", t_font_sz, 'b');
  gfx_measurestr(title_str, tsw, tsh);
);
gfx_r = 1.00; gfx_g = 0.92; gfx_b = 1.00;
gfx_x = 20; gfx_y = hdr_y + 6;
gfx_drawstr(title_str);

sub_str = disp_w < 740 ? "IMPERIAL SCEPTRE & VOCAL COHESION" : "IMPERIAL SCEPTRE & VOCAL COHESION ENGINE // DUAFE MATRIX";
s_font_sz = 10.0;
gfx_setfont(4, "Consolas", s_font_sz);
gfx_measurestr(sub_str, ssw, ssh);
while (ssw > max_title_w && s_font_sz > 7.5) (
  s_font_sz -= 0.5;
  gfx_setfont(4, "Consolas", s_font_sz);
  gfx_measurestr(sub_str, ssw, ssh);
);
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
gfx_x = 20; gfx_y = hdr_y + 24;
gfx_drawstr(sub_str);

// 3. Navigation Tabs
tab_y = hdr_y + hdr_h + 6; tab_h = 24;
tab_w = floor((disp_w - 24) / 7);
ti = 0;
loop(7,
  tx = 12 + ti * tab_w;
  sel = (slider1 == ti);
  gfx_r = sel ? 0.16 : 0.045; gfx_g = sel ? 0.06 : 0.025; gfx_b = sel ? 0.20 : 0.060;
  gfx_rect(tx, tab_y, tab_w - 3, tab_h);
  sel ? (
    gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
    gfx_rect(tx, tab_y + tab_h - 2, tab_w - 3, 2);
    gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  ) : (
    gfx_r = 0.70; gfx_g = 0.60; gfx_b = 0.80;
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
gfx_r = 0.026; gfx_g = 0.012; gfx_b = 0.034;
gfx_rect(ws_x, ws_y, ws_w, ws_h);
gfx_r = 0.18; gfx_g = 0.10; gfx_b = 0.24;
gfx_rect(ws_x, ws_y, ws_w, ws_h, 0);

// Helper for drawing Authentic SIFAM Analogue VU Meter with curved scale arc
function draw_sifam_vocal_meter(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) (
  gfx_r = 0.018; gfx_g = 0.008; gfx_b = 0.024;
  gfx_rect(mx, my, mw, mh);
  gfx_r = accent_r * 0.7; gfx_g = accent_g * 0.7; gfx_b = accent_b * 0.7;
  gfx_rect(mx, my, mw, mh, 0);

  // Meter Title Header
  gfx_setfont(2); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_x = mx + 12; gfx_y = my + 8;
  gfx_drawstr(title_str);

  // Curved Scale Parameters
  piv_x = mx + mw * 0.5;
  piv_y = my + mh + 24;
  r_arc = mh * 0.88;
  ang_min = -0.785398;
  ang_max = 0.785398;

  // Scale Backing Arc
  gfx_r = 0.14; gfx_g = 0.08; gfx_b = 0.18;
  step_a = (ang_max - ang_min) / 40.0;
  ai = 0;
  loop(40,
    a1 = ang_min + ai * step_a; a2 = a1 + step_a;
    gfx_line(piv_x + sin(a1) * r_arc, piv_y - cos(a1) * r_arc, piv_x + sin(a2) * r_arc, piv_y - cos(a2) * r_arc);
    ai += 1;
  );

  // Calibrated Tick Marks
  gfx_setfont(4);
  ti = 0;
  loop(9,
    f = ti / 8.0;
    ta = ang_min + f * (ang_max - ang_min);
    is_red = is_glue ? (f >= 0.75) : (f >= 0.75);
    gfx_r = is_red ? 0.98 : (accent_r * 0.9);
    gfx_g = is_red ? 0.25 : (accent_g * 0.9);
    gfx_b = is_red ? 0.30 : (accent_b * 0.9);
    t_len = (ti % 2 == 0) ? 9 : 5;
    gfx_line(piv_x + sin(ta) * (r_arc - t_len), piv_y - cos(ta) * (r_arc - t_len), piv_x + sin(ta) * (r_arc + 1), piv_y - cos(ta) * (r_arc + 1));
    ti += 1;
  );

  // Legend Labels
  gfx_r = 0.60; gfx_g = 0.55; gfx_b = 0.70;
  gfx_x = piv_x + sin(ang_min) * (r_arc + 3) - 6; gfx_y = piv_y - cos(ang_min) * (r_arc + 3) - 6; gfx_drawstr(is_glue ? "0" : "0");
  gfx_x = piv_x - 4; gfx_y = piv_y - r_arc - 14; gfx_drawstr(is_glue ? "-6" : "+5");
  gfx_r = 0.98; gfx_g = 0.30; gfx_b = 0.40;
  gfx_x = piv_x + sin(ang_max) * (r_arc + 3) - 10; gfx_y = piv_y - cos(ang_max) * (r_arc + 3) - 6; gfx_drawstr(is_glue ? "-12" : "+10");

  // Needle Calculation
  n_frac = max(0.0, min(1.0, needle_val / max_val));
  n_ang = ang_min + n_frac * (ang_max - ang_min);
  tip_x = piv_x + sin(n_ang) * (r_arc + 2);
  tip_y = piv_y - cos(n_ang) * (r_arc + 2);
  base_x = piv_x + sin(n_ang) * 12;
  base_y = piv_y - cos(n_ang) * 12;

  gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
  gfx_line(base_x - 0.5, base_y, tip_x - 0.5, tip_y);
  gfx_line(base_x + 0.5, base_y, tip_x + 0.5, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  // Tip Marker & Brass Pivot Cap
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_circle(tip_x, tip_y, 2, 1);
  gfx_r = 0.08; gfx_g = 0.04; gfx_b = 0.10; gfx_circle(piv_x, my + mh - 8, 14, 1);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b; gfx_circle(piv_x, my + mh - 8, 14, 0);
);

// =============================================================================
// TAB 0: EMPRESS OVERVIEW (TWIN SIFAM ANALOG METERS & CALIBRATION)
// =============================================================================
slider1 == 0 ? (
  sm_y = ws_y + 12; sm_h = 175;
  sm_w = floor((ws_w - 30) / 2);

  // Meter 1: SIFAM Vocal Tube Warmth Saturation
  draw_sifam_vocal_meter(ws_x + 10, sm_y, sm_w, sm_h, "SIFAM VOCAL EMPRESS // TUBE WARMTH", sifam_tube_needle, 10.0, 0, 1.00, 0.41, 0.70);
  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.75; gfx_b = 0.90;
  gfx_x = ws_x + 24; gfx_y = sm_y + sm_h - 26;
  gfx_printf("+%.1f dB TUBE", slider21);

  // Meter 2: SIFAM Master Vocal Bus Glue GR
  draw_sifam_vocal_meter(ws_x + sm_w + 20, sm_y, sm_w, sm_h, "MASTER VOCAL GLUE // GAIN REDUCTION", sifam_vglue_needle, 12.0, 1, 0.70, 0.53, 1.00);
  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.75; gfx_g = 0.60; gfx_b = 1.00;
  gfx_x = ws_x + sm_w + 34; gfx_y = sm_y + sm_h - 26;
  gfx_printf("-%.1f dB GR", sifam_vglue_needle);

  // Status Plaque
  p_y = sm_y + sm_h + 12; p_h = ws_h - sm_h - 24;
  gfx_r = 0.038; gfx_g = 0.016; gfx_b = 0.048; gfx_rect(ws_x + 10, p_y, ws_w - 20, p_h);
  gfx_r = 0.22; gfx_g = 0.12; gfx_b = 0.28; gfx_rect(ws_x + 10, p_y, ws_w - 20, p_h, 0);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.00; gfx_g = 0.92; gfx_b = 1.00;
  gfx_x = ws_x + 24; gfx_y = p_y + 12;
  gfx_printf("ACTIVE PROFILE: %02d - %s", slider2, get_vocal_full_title(slider2));

  gfx_setfont(3); gfx_r = 0.90; gfx_g = 0.82; gfx_b = 0.98;
  gfx_x = ws_x + 24; gfx_y = p_y + 36;
  disp_w < 720 ? (
    gfx_printf("Trim: %+.1fdB | Ceil: %.1fdBTP | De-Ess: %.1fdB | Air: %+.1fdB | Width: %.2fx", slider4, slider5, slider7, slider11, slider18);
  ) : (
    gfx_printf("CALIBRATION: Trim: %+4.1fdB | Ceiling: %.1fdBTP | De-Ess: %.1fdB @ %dHz | Bax Air: %+.1fdB | Width: %.2fx", slider4, slider5, slider7, slider8, slider11, slider18);
  );

  gfx_setfont(4); gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  gfx_x = ws_x + 24; gfx_y = p_y + 60;
  gfx_printf("Summing State: %s | Glue Topology: %s | Music Corridor Request: %.1fdB",
    slider22 ? "ENGAGED (ACTIVE VOCAL SUM)" : "BYPASS (1:1 UNITY PASS)",
    slider12 ? "Opto 2A Vocal Leveler" : "Fairchild 670 Smooth Tube", slider20);
);

// =============================================================================
// TAB 1: BAXANDALL MASTER EQ (3-BAND INTERACTIVE SHELVING & CLARITY BELL)
// =============================================================================
slider1 == 1 ? (
  eq_y = ws_y + 12; eq_w = ws_w - 20; eq_h = 170;
  gfx_r = 0.020; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 10, eq_y, eq_w, eq_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 10, eq_y, eq_w, eq_h, 0);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 24; gfx_y = eq_y + 10; gfx_drawstr("BAXANDALL IMPERIAL MASTER VOCAL EQUALIZER");

  // Center 0 dB line
  cy = eq_y + eq_h * 0.52;
  gfx_r = 0.18; gfx_g = 0.10; gfx_b = 0.24; gfx_line(ws_x + 10, cy, ws_x + 10 + eq_w, cy);

  // Interactive 3 Band Cards
  c_w = floor((eq_w - 24) / 3);
  card_y = eq_y + eq_h + 10; card_h = ws_h - eq_h - 26;
  bi = 0;
  loop(3,
    bx = ws_x + 10 + bi * (c_w + 6);
    gfx_r = 0.038; gfx_g = 0.016; gfx_b = 0.048; gfx_rect(bx, card_y, c_w, card_h);
    gfx_r = 0.22; gfx_g = 0.12; gfx_b = 0.28; gfx_rect(bx, card_y, c_w, card_h, 0);

    b_name = bi == 0 ? "100Hz WARMTH SHELF" : (bi == 1 ? "3.5kHz CLARITY BELL" : "12kHz AIR SHEEN SHELF");
    b_val = bi == 0 ? slider9 : (bi == 1 ? slider10 : slider11);
    gfx_setfont(2); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
    gfx_x = bx + 8; gfx_y = card_y + 8; gfx_drawstr(b_name);

    gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;
    gfx_x = bx + 8; gfx_y = card_y + 28;
    gfx_printf("%+.1f dB", b_val);

    // +/- adjust buttons
    bm_x = bx + 10; bm_y = card_y + card_h - 26; bw = 24; bh = 18;
    bp_x = bx + c_w - 34; bp_y = bm_y;
    gfx_r = 0.14; gfx_g = 0.06; gfx_b = 0.18; gfx_rect(bm_x, bm_y, bw, bh); gfx_rect(bp_x, bp_y, bw, bh);
    gfx_r = 0.60; gfx_g = 0.30; gfx_b = 0.70; gfx_rect(bm_x, bm_y, bw, bh, 0); gfx_rect(bp_x, bp_y, bw, bh, 0);
    gfx_setfont(3); gfx_x = bm_x + 8; gfx_y = bm_y + 2; gfx_drawstr("-"); gfx_x = bp_x + 7; gfx_y = bp_y + 2; gfx_drawstr("+");

    (mouse_cap & 1) && !prev_mouse_cap && (mouse_x >= bm_x && mouse_x <= bm_x + bw && mouse_y >= bm_y && mouse_y <= bm_y + bh) ? (
      bi == 0 ? slider9 = max(-6.0, slider9 - 0.2) :
      bi == 1 ? slider10 = max(-6.0, slider10 - 0.2) :
                slider11 = max(-6.0, slider11 - 0.2);
      update_vocal_filters(); slider_automate();
    );
    (mouse_cap & 1) && !prev_mouse_cap && (mouse_x >= bp_x && mouse_x <= bp_x + bw && mouse_y >= bp_y && mouse_y <= bp_y + bh) ? (
      bi == 0 ? slider9 = min(6.0, slider9 + 0.2) :
      bi == 1 ? slider10 = min(6.0, slider10 + 0.2) :
                slider11 = min(6.0, slider11 + 0.2);
      update_vocal_filters(); slider_automate();
    );
    bi += 1;
  );
);

// =============================================================================
// TAB 2: VOCAL BUS GLUE (FAIRCHILD 670 TUBE VS OPTO 2A LEVELER)
// =============================================================================
slider1 == 2 ? (
  cg_y = ws_y + 12; cg_w = ws_w - 20; cg_h = ws_h - 24;
  gfx_r = 0.020; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 10, cg_y, cg_w, cg_h);
  gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(ws_x + 10, cg_y, cg_w, cg_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = ws_x + 24; gfx_y = cg_y + 12; gfx_drawstr("MASTER VOCAL GLUE COMPRESSOR (FAIRCHILD 670 / OPTO 2A)");

  // Topology Switch Button
  top_x = ws_x + 24; top_y = cg_y + 36; top_w = 260; top_h = 28;
  gfx_r = slider12 ? 0.18 : 0.08; gfx_g = slider12 ? 0.08 : 0.14; gfx_b = slider12 ? 0.24 : 0.20;
  gfx_rect(top_x, top_y, top_w, top_h);
  gfx_r = slider12 ? 0.70 : 1.00; gfx_g = slider12 ? 0.53 : 0.41; gfx_b = slider12 ? 1.00 : 0.70;
  gfx_rect(top_x, top_y, top_w, top_h, 0);
  gfx_setfont(2); gfx_x = top_x + 12; gfx_y = top_y + 7;
  slider12 ? gfx_drawstr("TOPOLOGY: OPTO 2A VOCAL LEVELER") : gfx_drawstr("TOPOLOGY: FAIRCHILD 670 SMOOTH TUBE");
  (mouse_cap & 1) && !prev_mouse_cap && (mouse_x >= top_x && mouse_x <= top_x + top_w && mouse_y >= top_y && mouse_y <= top_y + top_h) ? (
    slider12 = !slider12;
    slider_automate(2048);
  );

  // Parameters Readout & Controls
  gfx_setfont(3); gfx_r = 0.90; gfx_g = 0.85; gfx_b = 0.98;
  gfx_x = ws_x + 24; gfx_y = top_y + 44;
  gfx_printf("Threshold: %.1f dB | Ratio: %.1f:1 | Attack: %.1f ms | Release: %.1f ms | Mix: %d%%",
    slider13, vcomp_ratio, slider15, slider16, slider17);

  // Big Gain Reduction Meter Bar
  gr_bar_y = top_y + 80; gr_bar_h = 32; gr_bar_w = cg_w - 48;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.016; gfx_rect(ws_x + 24, gr_bar_y, gr_bar_w, gr_bar_h);
  gfx_r = 0.24; gfx_g = 0.14; gfx_b = 0.32; gfx_rect(ws_x + 24, gr_bar_y, gr_bar_w, gr_bar_h, 0);
  fill_w = floor(gr_bar_w * (min(16.0, vglue_gr_db) / 16.0));
  fill_w > 0 ? (
    gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(ws_x + 24, gr_bar_y + 2, fill_w, gr_bar_h - 4);
  );
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = ws_x + 36; gfx_y = gr_bar_y + 8;
  gfx_printf("LIVE VOCAL GLUE REDUCTION: -%.2f dB", vglue_gr_db);
);

// =============================================================================
// TAB 3: DE-ESSER & BLEED SENTRY (DYNAMIC SIBILANCE SUPPRESSOR)
// =============================================================================
slider1 == 3 ? (
  de_y = ws_y + 12; de_w = ws_w - 20; de_h = ws_h - 24;
  gfx_r = 0.020; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 10, de_y, de_w, de_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 10, de_y, de_w, de_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 24; gfx_y = de_y + 12; gfx_drawstr("DE-ESSER & HIGH-FREQUENCY BLEED SENTRY");

  // De-Esser Controls Card
  dc_x = ws_x + 24; dc_y = de_y + 40; dc_w = de_w - 48; dc_h = 100;
  gfx_r = 0.038; gfx_g = 0.016; gfx_b = 0.048; gfx_rect(dc_x, dc_y, dc_w, dc_h);
  gfx_r = 0.22; gfx_g = 0.12; gfx_b = 0.28; gfx_rect(dc_x, dc_y, dc_w, dc_h, 0);

  gfx_setfont(2); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = dc_x + 12; gfx_y = dc_y + 12; gfx_drawstr("SIBILANCE CLAMP DEPTH & FREQUENCY");

  gfx_setfont(1, "Orbitron", 16, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = dc_x + 12; gfx_y = dc_y + 36;
  gfx_printf("%.1f dB @ %d Hz", slider7, slider8);

  gfx_setfont(4); gfx_r = 0.70; gfx_g = 0.60; gfx_b = 0.80;
  gfx_x = dc_x + 12; gfx_y = dc_y + 68;
  gfx_drawstr("Targeted high-frequency sibilance suppression without dulling airy presence or vocal bite.");
);

// =============================================================================
// TAB 4: SPATIAL IMMERSION & STEREO CORRIDOR
// =============================================================================
slider1 == 4 ? (
  sp_y = ws_y + 12; sp_w = ws_w - 20; sp_h = ws_h - 24;
  gfx_r = 0.020; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 10, sp_y, sp_w, sp_h);
  gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(ws_x + 10, sp_y, sp_w, sp_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = ws_x + 24; gfx_y = sp_y + 12; gfx_drawstr("VOCAL SPATIAL IMMERSION & DYNAMIC MUSIC CORRIDOR");

  // Mono Center Lock Switch
  ml_x = ws_x + 24; ml_y = sp_y + 40; ml_w = 260; ml_h = 28;
  gfx_r = slider19 ? 0.18 : 0.08; gfx_g = slider19 ? 0.08 : 0.14; gfx_b = slider19 ? 0.24 : 0.20;
  gfx_rect(ml_x, ml_y, ml_w, ml_h);
  gfx_r = slider19 ? 1.00 : 0.60; gfx_g = slider19 ? 0.41 : 0.40; gfx_b = slider19 ? 0.70 : 0.70;
  gfx_rect(ml_x, ml_y, ml_w, ml_h, 0);
  gfx_setfont(2); gfx_x = ml_x + 12; gfx_y = ml_y + 7;
  slider19 ? gfx_drawstr("MONO LOCK: STRICT CENTER ANCHOR") : gfx_drawstr("MONO LOCK: STEREO WIDE PASS");
  (mouse_cap & 1) && !prev_mouse_cap && (mouse_x >= ml_x && mouse_x <= ml_x + ml_w && mouse_y >= ml_y && mouse_y <= ml_y + ml_h) ? (
    slider19 = !slider19;
    slider_automate(262144);
  );

  // Readout
  gfx_setfont(3); gfx_r = 0.90; gfx_g = 0.85; gfx_b = 0.98;
  gfx_x = ws_x + 24; gfx_y = ml_y + 44;
  gfx_printf("Mid/Side Width Multiplier: %.2fx | Music Corridor Request: %.1f dB", slider18, slider20);

  // Status Plaque
  gfx_setfont(4); gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  gfx_x = ws_x + 24; gfx_y = ml_y + 80;
  gfx_drawstr("The Dynamic Music Corridor requests real-time ducking of instrumental bus clutter via gmem interlock.");
);

// =============================================================================
// TAB 5: DYNAMIC PRESENCE SENTRY
// =============================================================================
slider1 == 5 ? (
  pr_y = ws_y + 12; pr_w = ws_w - 20; pr_h = ws_h - 24;
  gfx_r = 0.020; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 10, pr_y, pr_w, pr_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 10, pr_y, pr_w, pr_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 24; gfx_y = pr_y + 12; gfx_drawstr("DYNAMIC PRESENCE SENTRY & SPECTRAL HARMONICS");

  gfx_setfont(2); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = ws_x + 24; gfx_y = pr_y + 44;
  gfx_printf("Active Saturation: +%.1f dB Vocal Tube Bloom | Air Sheen Shelf: %+.1f dB", slider21, slider11);

  gfx_setfont(4); gfx_r = 0.70; gfx_g = 0.60; gfx_b = 0.80;
  gfx_x = ws_x + 24; gfx_y = pr_y + 76;
  gfx_drawstr("Even and odd harmonic excitation provides imperial intimacy and cut through dense wall-of-sound guitar mixes.");
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
  gfx_r = 0.038; gfx_g = 0.016; gfx_b = 0.048; gfx_rect(ws_x + 12, pl_y, pl_w, pl_h);
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

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Damei_VocalBus.jsfx v1.1 written successfully.")
