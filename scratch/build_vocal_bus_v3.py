import os

target_path = r"c:\Dev\DameiSuite\effects\Damei_VocalBus.jsfx"

code = r'''desc:Damei Vocal Empress (Imperial Sceptre & Master Vocal Sum)
// =============================================================================
// DAMEI VOCAL EMPRESS // IMPERIAL SCEPTRE & MASTER VOCAL SUM (v3.0)
// Archetype: Duafe (The Wooden Comb - Pristine Grooming & Imperial Refinement)
// Summed Master Vocal Processing Engine with Dynamic Music Corridor Interlock
// Communication Range: gmem[1450..1499] (Publishes) | gmem[1400..1449] (Reads Instrumental Bus)
// Built by Damei Audio & Antigravity IDE (2026 Production Standard)
// =============================================================================

slider1:0<0,6,1{Empress Overview,Baxandall Master EQ,Vocal Bus Glue,De-Esser & Bleed Sentry,Spatial Immersion,Dynamic Presence Sentry,Producer Vocal Matrix}>-Active Module
slider2:0<0,24,1{Default Unity Baseline (1:1 Pass),Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Mirrorcell),Buster Odeholm (thrown / Northlane),Lewis Johns (Love Is Noise / blanket),Kel Pinchin (Split Chain / Currents Target),Dan Lancaster & Jason Perry (Don Broco),Erik Bickerstaffe (Static Dress),Sam Guaiana (Silverstein / TDWP),Zach Tuch (Heavenward / Hundredth),Forrester Savell (Karnivool),Leon Schmidt (SUNBORN - Nebula),Ermin Hamidovic (Systematic Reference),Will Putney (Fit For An Autopsy),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill - nerv),Henrik Udd (Architects - Gravity),Dan Braunstein (Spiritbox - Keep Sweet),Zakk Cervini & Erik Ron (Bad Omens),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Acle Kahney (TesseracT - King),Adam Cichocki (heaving. / Timber Studios),Manuel Renner (SENNA / Uberlarm Studios)}>-Producer Vocal Profile
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
slider22:1<0,1,1{Bypassed,Engaged}>-Vocal Master Suite Engine
slider23:0<0,1,1{Norm,Delta Solo Listen}>-Non-Destructive Delta Audition
slider24:0<0,1,1{Snap A,Snap B}>-A/B Snapshot Memory
slider25:0<0,1,1{Master Sum,Stem Sum}>-Summing Mode

options:gmem=DameiMixMetering
options:maxmem=65536
in_pin:left input
in_pin:right input
out_pin:left output
out_pin:right output

@init
ext_noinit = 1;
srate <= 0 ? srate = 48000;

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

ab_mem_a = 61000; ab_mem_b = 61100; ab_init_done = 0; ab_state = 0;

sifam_tube_needle = 0;
sifam_vglue_needle = 0;
v_meter_rms_l = 0; v_meter_rms_r = 0;
v_meter_peak_l = 0; v_meter_peak_r = 0;
v_comp_env = 0;
vglue_gr_db = 0;
cur_phase_corr = 0.98;
prev_vpreset = slider2;
drag_slider_idx = 0;

function save_ab_snapshot(target_buf) local(k) (
  k = 1; loop(25, target_buf[k] = slider(k); k += 1; );
);

function load_ab_snapshot(src_buf) local(k) (
  k = 1; loop(25, slider(k) = src_buf[k]; k += 1; );
  slider_automate();
);

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
  p_idx == 0  ? "Default Unity Baseline (1:1 Transparent Pass)" :
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
  p_idx == 13 ? "Ermin Hamidovic (Systematic Reference)" :
  p_idx == 14 ? "Will Putney (Fit For An Autopsy / Knocked Loose)" :
  p_idx == 15 ? "George Lever (Sleep Token / Loathe)" :
  p_idx == 16 ? "Sam Bassal (Thornhill - Heroine)" :
  p_idx == 17 ? "Henrik Udd (Architects - Holy Hell)" :
  p_idx == 18 ? "Dan Braunstein (Spiritbox - Keep Sweet)" :
  p_idx == 19 ? "Zakk Cervini & Erik Ron (Bad Omens - TDOPOM)" :
  p_idx == 20 ? "Jens Bogren (Fascination Street Studios)" :
  p_idx == 21 ? "Adam Nolly Getgood (Periphery / GGD)" :
  p_idx == 22 ? "Acle Kahney (TesseracT - King)" :
  p_idx == 23 ? "Adam Cichocki (heaving. - carsick / Timber Studios)" :
                "Manuel Renner (SENNA - Out Of The Blue / Uberlarm Studios)"
);

function apply_vocal_preset(p_idx) (
  p_idx == 0 ? ( // Default Unity Baseline (1:1 Transparent Pass)
    slider4 = 0.0; slider7 = 0.0; slider9 = 0.0; slider10 = 0.0; slider11 = 0.0;
    slider12 = 0; slider13 = 0.0; slider14 = 0; slider15 = 25.0; slider16 = 150.0;
    slider18 = 1.00; slider20 = 1.2; slider21 = 0.0;
  ) : p_idx == 1 ? ( // Lance Prenc
    slider4 = -3.0; slider7 = -2.8; slider9 = -1.2; slider10 = 2.4; slider11 = 2.6;
    slider12 = 0; slider13 = -18.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.05; slider20 = 1.8; slider21 = 2.5;
  ) : p_idx == 2 ? ( // Scott Seigel
    slider4 = -2.5; slider7 = -3.0; slider9 = -0.8; slider10 = 2.6; slider11 = 2.0;
    slider12 = 0; slider13 = -19.0; slider14 = 2; slider15 = 15.0; slider16 = 100.0;
    slider18 = 1.02; slider20 = 2.0; slider21 = 3.5;
  ) : p_idx == 3 ? ( // Jonathan Dolese
    slider4 = -2.5; slider7 = -2.2; slider9 = -0.5; slider10 = 2.0; slider11 = 2.8;
    slider12 = 1; slider13 = -16.0; slider14 = 1; slider15 = 25.0; slider16 = 140.0;
    slider18 = 1.08; slider20 = 1.5; slider21 = 2.0;
  ) : p_idx == 4 ? ( // Buster Odeholm
    slider4 = -3.5; slider7 = -3.5; slider9 = -1.5; slider10 = 3.0; slider11 = 1.5;
    slider12 = 0; slider13 = -20.0; slider14 = 2; slider15 = 12.0; slider16 = 90.0;
    slider18 = 1.00; slider20 = 2.2; slider21 = 4.2;
  ) : p_idx == 5 ? ( // Lewis Johns
    slider4 = -2.0; slider7 = -1.5; slider9 = 1.0; slider10 = 1.2; slider11 = 2.0;
    slider12 = 1; slider13 = -14.0; slider14 = 0; slider15 = 35.0; slider16 = 200.0;
    slider18 = 1.15; slider20 = 1.0; slider21 = 2.8;
  ) : p_idx == 6 ? ( // Kel Pinchin (Split Chain Target)
    slider4 = -2.5; slider7 = -2.4; slider9 = -0.8; slider10 = 2.2; slider11 = 2.4;
    slider12 = 0; slider13 = -16.5; slider14 = 1; slider15 = 20.0; slider16 = 130.0;
    slider18 = 1.06; slider20 = 1.6; slider21 = 2.0;
  ) : p_idx == 7 ? ( // Dan Lancaster
    slider4 = -3.0; slider7 = -2.5; slider9 = -1.0; slider10 = 2.8; slider11 = 3.0;
    slider12 = 0; slider13 = -18.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.10; slider20 = 1.8; slider21 = 2.2;
  ) : p_idx == 8 ? ( // Erik Bickerstaffe
    slider4 = -2.5; slider7 = -1.8; slider9 = 0.8; slider10 = 2.0; slider11 = 1.4;
    slider12 = 1; slider13 = -17.0; slider14 = 1; slider15 = 20.0; slider16 = 100.0;
    slider18 = 1.02; slider20 = 1.4; slider21 = 3.4;
  ) : p_idx == 9 ? ( // Sam Guaiana
    slider4 = -2.5; slider7 = -2.2; slider9 = -0.6; slider10 = 2.4; slider11 = 2.2;
    slider12 = 0; slider13 = -16.0; slider14 = 1; slider15 = 25.0; slider16 = 130.0;
    slider18 = 1.05; slider20 = 1.5; slider21 = 2.2;
  ) : p_idx == 10 ? ( // Zach Tuch
    slider4 = -2.0; slider7 = -1.5; slider9 = 1.2; slider10 = 1.4; slider11 = 2.2;
    slider12 = 1; slider13 = -14.0; slider14 = 0; slider15 = 30.0; slider16 = 180.0;
    slider18 = 1.12; slider20 = 1.0; slider21 = 2.0;
  ) : p_idx == 11 ? ( // Forrester Savell
    slider4 = -1.5; slider7 = -1.2; slider9 = 0.2; slider10 = 1.5; slider11 = 1.8;
    slider12 = 0; slider13 = -13.0; slider14 = 0; slider15 = 35.0; slider16 = 160.0;
    slider18 = 1.08; slider20 = 1.2; slider21 = 1.2;
  ) : p_idx == 12 ? ( // Leon Schmidt
    slider4 = -2.5; slider7 = -2.6; slider9 = -1.0; slider10 = 2.6; slider11 = 2.8;
    slider12 = 0; slider13 = -17.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.10; slider20 = 1.6; slider21 = 2.4;
  ) : p_idx == 13 ? ( // Ermin Hamidovic
    slider4 = -3.0; slider7 = -1.5; slider9 = 0.0; slider10 = 1.0; slider11 = 1.2;
    slider12 = 0; slider13 = -15.0; slider14 = 0; slider15 = 30.0; slider16 = 140.0;
    slider18 = 1.02; slider20 = 1.0; slider21 = 0.8;
  ) : p_idx == 14 ? ( // Will Putney
    slider4 = -3.5; slider7 = -3.2; slider9 = -1.2; slider10 = 2.6; slider11 = 1.8;
    slider12 = 0; slider13 = -19.0; slider14 = 2; slider15 = 15.0; slider16 = 100.0;
    slider18 = 1.02; slider20 = 1.8; slider21 = 3.6;
  ) : p_idx == 15 ? ( // George Lever
    slider4 = -2.0; slider7 = -1.8; slider9 = 1.2; slider10 = 1.6; slider11 = 2.2;
    slider12 = 1; slider13 = -15.0; slider14 = 0; slider15 = 30.0; slider16 = 180.0;
    slider18 = 1.12; slider20 = 1.2; slider21 = 2.6;
  ) : p_idx == 16 ? ( // Sam Bassal
    slider4 = -2.5; slider7 = -2.2; slider9 = -0.5; slider10 = 2.2; slider11 = 2.2;
    slider12 = 0; slider13 = -16.5; slider14 = 1; slider15 = 25.0; slider16 = 130.0;
    slider18 = 1.06; slider20 = 1.4; slider21 = 2.4;
  ) : p_idx == 17 ? ( // Henrik Udd
    slider4 = -3.0; slider7 = -2.8; slider9 = -0.8; slider10 = 2.6; slider11 = 2.8;
    slider12 = 0; slider13 = -18.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.08; slider20 = 1.8; slider21 = 2.5;
  ) : p_idx == 18 ? ( // Dan Braunstein
    slider4 = -3.0; slider7 = -2.5; slider9 = -0.8; slider10 = 2.5; slider11 = 3.2;
    slider12 = 0; slider13 = -17.5; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.10; slider20 = 1.8; slider21 = 2.2;
  ) : p_idx == 19 ? ( // Zakk Cervini
    slider4 = -3.0; slider7 = -2.8; slider9 = -1.0; slider10 = 2.8; slider11 = 3.0;
    slider12 = 0; slider13 = -18.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.08; slider20 = 1.8; slider21 = 2.6;
  ) : p_idx == 20 ? ( // Jens Bogren
    slider4 = -3.0; slider7 = -2.2; slider9 = 0.2; slider10 = 2.0; slider11 = 1.8;
    slider12 = 0; slider13 = -17.0; slider14 = 1; slider15 = 25.0; slider16 = 130.0;
    slider18 = 1.04; slider20 = 1.5; slider21 = 2.5;
  ) : p_idx == 21 ? ( // Nolly Getgood
    slider4 = -2.5; slider7 = -2.4; slider9 = -1.0; slider10 = 2.4; slider11 = 2.6;
    slider12 = 0; slider13 = -16.0; slider14 = 1; slider15 = 25.0; slider16 = 130.0;
    slider18 = 1.04; slider20 = 1.6; slider21 = 1.8;
  ) : p_idx == 22 ? ( // Acle Kahney
    slider4 = -2.0; slider7 = -1.8; slider9 = 0.0; slider10 = 1.8; slider11 = 2.0;
    slider12 = 0; slider13 = -14.0; slider14 = 0; slider15 = 30.0; slider16 = 150.0;
    slider18 = 1.06; slider20 = 1.2; slider21 = 1.0;
  ) : p_idx == 23 ? ( // Adam Cichocki (heaving.)
    slider4 = -2.5; slider7 = -2.0; slider9 = 0.8; slider10 = 1.8; slider11 = 2.8;
    slider12 = 1; slider13 = -16.0; slider14 = 1; slider15 = 25.0; slider16 = 140.0;
    slider18 = 1.12; slider20 = 1.4; slider21 = 3.2;
  ) : ( // Manuel Renner (SENNA)
    slider4 = -3.0; slider7 = -2.6; slider9 = -0.8; slider10 = 2.6; slider11 = 3.0;
    slider12 = 0; slider13 = -18.0; slider14 = 1; slider15 = 20.0; slider16 = 120.0;
    slider18 = 1.06; slider20 = 1.8; slider21 = 2.4;
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
in_s0 = s0; in_s1 = s1;

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

// Non-destructive Delta Solo Listen
slider23 ? (
  spl0 = s0 - in_s0;
  spl1 = s1 - in_s1;
) : (
  spl0 = s0;
  spl1 = s1;
);

// Ballistics & Telemetry
v_meter_rms_l = v_meter_rms_l * 0.999 + spl0 * spl0 * 0.001;
v_meter_rms_r = v_meter_rms_r * 0.999 + spl1 * spl1 * 0.001;
sifam_tube_needle = sifam_tube_needle * 0.95 + slider21 * 0.05;
sifam_vglue_needle = sifam_vglue_needle * 0.90 + vglue_gr_db * 0.10;

dot_prod_v = spl0 * spl1;
mag_prod_v = sqrt((spl0 * spl0 + 0.0000001) * (spl1 * spl1 + 0.0000001));
inst_corr_v = dot_prod_v / mag_prod_v;
cur_phase_corr = cur_phase_corr * 0.995 + inst_corr_v * 0.005;

// Publish to gmem[1450..1499]
gmem[1450] = time_precise();
gmem[1451] = 1.0;
gmem[1452] = 10.0 * log10(max(0.0000001, (v_meter_rms_l + v_meter_rms_r) * 0.5));
gmem[1453] = max(abs(spl0), abs(spl1));
gmem[1454] = gmem[1453] > 0.0001 ? 20.0 * log10(gmem[1453]) - gmem[1452] : 12.0;
gmem[1455] = slider20; // Corridor Request (dB)
gmem[1457] = slider2;

// =============================================================================
// @GFX 1080 700: LUXURY MASTER VOCAL CONSOLE SURFACE (DUAFE ADINKRA THEME)
// =============================================================================
@gfx 1080 700
w = gfx_w; h = gfx_h;
crt_x = 8; crt_y = 8;
crt_w = w - 16; crt_h = h - 16;

mouse_down = (mouse_cap & 1);
mouse_clicked = (mouse_down && !prev_mouse_down);
shift_down = (mouse_cap & 8);
ctrl_down = (mouse_cap & 4);

!mouse_down ? drag_slider_idx = 0;

!ab_init_done ? (
  save_ab_snapshot(ab_mem_a);
  save_ab_snapshot(ab_mem_b);
  ab_init_done = 1;
);

!fonts_initialized ? (
  gfx_setfont(1, "Orbitron", 14, 'b');
  gfx_setfont(2, "Orbitron", 11, 'b');
  gfx_setfont(3, "Consolas", 12, 'b');
  gfx_setfont(4, "Consolas", 10.5);
  fonts_initialized = 1;
);

// Outer Deep Royal Empress Plum Chassis
gfx_r = 0.038; gfx_g = 0.016; gfx_b = 0.048;
gfx_rect(crt_x, crt_y, crt_w, crt_h);

// Cyber Rose Quartz Border Trim
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
gfx_rect(crt_x, crt_y, crt_w, crt_h, 0);
gfx_rect(crt_x + 1, crt_y + 1, crt_w - 2, crt_h - 2, 0);

// ─────────────────────────────────────────────────────────────────────────────
// 1. TOP HEADER BAR: DUAFE CREST, PRESET STEPPER & SYSTEM STATUS PILLS
// ─────────────────────────────────────────────────────────────────────────────
hdr_h = 48;
gfx_r = 0.024; gfx_g = 0.010; gfx_b = 0.032;
gfx_rect(crt_x + 2, crt_y + 2, crt_w - 4, hdr_h);
gfx_r = 0.18; gfx_g = 0.08; gfx_b = 0.22;
gfx_line(crt_x + 2, crt_y + hdr_h + 2, crt_x + crt_w - 2, crt_y + hdr_h + 2);

// Duafe Wooden Comb Emblem
sig_cx = crt_x + 24; sig_cy = crt_y + 24;
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
gfx_circle(sig_cx, sig_cy, 12, 0);
gfx_circle(sig_cx, sig_cy, 8, 0);
gfx_circle(sig_cx, sig_cy, 4, 1);

gfx_r = 1.00; gfx_g = 0.90; gfx_b = 1.00;
gfx_setfont(1, "Orbitron", 15, 'b');
gfx_x = crt_x + 44; gfx_y = crt_y + 15;
gfx_drawstr("DAMEI // VOCAL EMPRESS (MASTER VOCAL SUM)");

title_end_x = crt_x + 440;
right_edge_x = crt_x + crt_w - 12;

// Right Header Zone: Pinned Control Pills
// Pill 1: ENGAGED / BYPASS
byp_w = 88; byp_x = right_edge_x - byp_w;
byp_hov = (mouse_x >= byp_x && mouse_x <= byp_x + byp_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider22 ? (byp_hov ? 0.18 : 0.09) : (byp_hov ? 0.28 : 0.16);
gfx_g = slider22 ? (byp_hov ? 0.08 : 0.04) : (byp_hov ? 0.08 : 0.04);
gfx_b = slider22 ? (byp_hov ? 0.24 : 0.13) : (byp_hov ? 0.10 : 0.05);
gfx_rect(byp_x, crt_y + 9, byp_w, 30);
gfx_r = slider22 ? 1.00 : 0.95; gfx_g = slider22 ? 0.41 : 0.30; gfx_b = slider22 ? 0.70 : 0.30;
gfx_rect(byp_x, crt_y + 9, byp_w, 30, 0);
gfx_setfont(2, "Orbitron", 11, 'b');
b_txt = slider22 ? "ENGAGED" : "BYPASS";
gfx_measurestr(b_txt, btw, bth);
gfx_x = byp_x + (byp_w - btw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(b_txt);
mouse_clicked && byp_hov ? (slider22 = !slider22; slider_automate(););

// Pill 2: Headroom Ceiling (-6dB Lock vs Free)
ceil_w = 90; ceil_x = byp_x - ceil_w - 6;
ceil_hov = (mouse_x >= ceil_x && mouse_x <= ceil_x + ceil_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider6 ? 0.12 : 0.06; gfx_g = slider6 ? 0.06 : 0.04; gfx_b = slider6 ? 0.18 : 0.08;
gfx_rect(ceil_x, crt_y + 9, ceil_w, 30);
gfx_r = slider6 ? 1.00 : 0.50; gfx_g = slider6 ? 0.41 : 0.50; gfx_b = slider6 ? 0.70 : 0.50;
gfx_rect(ceil_x, crt_y + 9, ceil_w, 30, 0);
gfx_setfont(3, "Consolas", 11, 'b');
c_txt = slider6 ? "CEIL: -6dB" : "CEIL: FREE";
gfx_measurestr(c_txt, ctw, cth);
gfx_x = ceil_x + (ceil_w - ctw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(c_txt);
mouse_clicked && ceil_hov ? (slider6 = !slider6; slider_automate(););

// Pill 3: Summing Mode (Master Sum vs Stem Sum)
mode_w = 110; mode_x = ceil_x - mode_w - 6;
mode_hov = (mouse_x >= mode_x && mouse_x <= mode_x + mode_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = 0.12; gfx_g = 0.06; gfx_b = 0.18; gfx_rect(mode_x, crt_y + 9, mode_w, 30);
gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(mode_x, crt_y + 9, mode_w, 30, 0);
gfx_setfont(3, "Consolas", 11, 'b');
m_txt = slider25 ? "MODE: STEM SUM" : "MODE: MASTER SUM";
gfx_measurestr(m_txt, mtw, mth);
gfx_x = mode_x + (mode_w - mtw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(m_txt);
mouse_clicked && mode_hov ? (slider25 = !slider25; slider_automate(););

// Pill 4: Music Bus Telemetry Link
mlink_w = 135; mlink_x = mode_x - mlink_w - 6;
gfx_r = ib_alive ? 0.06 : 0.08; gfx_g = ib_alive ? 0.12 : 0.06; gfx_b = ib_alive ? 0.16 : 0.08;
gfx_rect(mlink_x, crt_y + 9, mlink_w, 30);
gfx_r = ib_alive ? 0.00 : 0.50; gfx_g = ib_alive ? 0.85 : 0.50; gfx_b = ib_alive ? 1.00 : 0.50;
gfx_rect(mlink_x, crt_y + 9, mlink_w, 30, 0);
gfx_setfont(3, "Consolas", 10.5, 'b');
ib_str = ib_alive ? sprintf(#, "MUSIC: %.1fdB", ib_inst_rms) : "MUSIC: STANDBY";
gfx_measurestr(ib_str, ibw, ibh);
gfx_x = mlink_x + (mlink_w - ibw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(ib_str);

// Pill 5: Song Structure Sync (Reads gmem[100..105])
rgn_w = 120; rgn_x = mlink_x - rgn_w - 6;
gfx_r = 0.08; gfx_g = 0.04; gfx_b = 0.12; gfx_rect(rgn_x, crt_y + 9, rgn_w, 30);
gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(rgn_x, crt_y + 9, rgn_w, 30, 0);
g_sec = gmem[100] == 1 ? gmem[101] : 0;
r_str = g_sec == 3 ? "⚡ CHORUS SYNC" : sprintf(#, "● SYNC: %d RGNS", gmem[103] > 0 ? gmem[103] : 20);
gfx_setfont(3, "Consolas", 10.5, 'b');
gfx_measurestr(r_str, rsw, rsh);
gfx_x = rgn_x + (rgn_w - rsw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(r_str);

// Pill 6: Non-Destructive A/B Snapshot
ab_w = 54; ab_x = rgn_x - ab_w - 6;
ab_hov = (mouse_x >= ab_x && mouse_x <= ab_x + ab_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = ab_state ? 0.24 : 0.10; gfx_g = ab_state ? 0.08 : 0.04; gfx_b = ab_state ? 0.28 : 0.14;
gfx_rect(ab_x, crt_y + 9, ab_w, 30);
gfx_r = ab_state ? 1.00 : 0.70; gfx_g = ab_state ? 0.41 : 0.53; gfx_b = ab_state ? 0.70 : 1.00;
gfx_rect(ab_x, crt_y + 9, ab_w, 30, 0);
gfx_setfont(2, "Orbitron", 10.5, 'b');
ab_str = ab_state ? "SNAP B" : "SNAP A";
gfx_measurestr(ab_str, abw, abh);
gfx_x = ab_x + (ab_w - abw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(ab_str);
mouse_clicked && ab_hov ? (
  ab_state == 0 ? (
    save_ab_snapshot(ab_mem_a);
    load_ab_snapshot(ab_mem_b);
    ab_state = 1; slider24 = 1;
  ) : (
    save_ab_snapshot(ab_mem_b);
    load_ab_snapshot(ab_mem_a);
    ab_state = 0; slider24 = 0;
  );
);

// Pill 7: Delta Solo Listen
del_w = 50; del_x = ab_x - del_w - 6;
del_hov = (mouse_x >= del_x && mouse_x <= del_x + del_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider23 ? 0.28 : 0.08; gfx_g = slider23 ? 0.08 : 0.04; gfx_b = slider23 ? 0.20 : 0.10;
gfx_rect(del_x, crt_y + 9, del_w, 30);
gfx_r = slider23 ? 1.00 : 0.50; gfx_g = slider23 ? 0.41 : 0.40; gfx_b = slider23 ? 0.70 : 0.60;
gfx_rect(del_x, crt_y + 9, del_w, 30, 0);
gfx_setfont(2, "Orbitron", 10.5, 'b');
del_str = slider23 ? "DELTA" : "NORM";
gfx_measurestr(del_str, dlw, dlh);
gfx_x = del_x + (del_w - dlw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(del_str);
mouse_clicked && del_hov ? (slider23 = !slider23; slider_automate(););

// ─────────────────────────────────────────────────────────────────────────────
// 2. NAVIGATION TABS (7 DEDICATED VOCAL EMPRESS TABS)
// ─────────────────────────────────────────────────────────────────────────────
tab_y = crt_y + hdr_h + 4; tab_h = 28;
tab_w = floor((crt_w - 8) / 7);
ti = 0;
loop(7,
  tx = crt_x + 4 + ti * tab_w;
  sel = (slider1 == ti);
  t_hov = (mouse_x >= tx && mouse_x <= tx + tab_w - 2 && mouse_y >= tab_y && mouse_y <= tab_y + tab_h);
  gfx_r = sel ? 0.16 : (t_hov ? 0.08 : 0.035);
  gfx_g = sel ? 0.06 : (t_hov ? 0.04 : 0.020);
  gfx_b = sel ? 0.20 : (t_hov ? 0.10 : 0.045);
  gfx_rect(tx, tab_y, tab_w - 2, tab_h);
  sel ? (
    gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
    gfx_rect(tx, tab_y + tab_h - 2, tab_w - 2, 2);
    gfx_r = 1.00; gfx_g = 0.90; gfx_b = 1.00;
  ) : (
    gfx_r = t_hov ? 0.95 : 0.70; gfx_g = t_hov ? 0.85 : 0.60; gfx_b = t_hov ? 0.95 : 0.75;
  );
  gfx_setfont(2, "Orbitron", 11, 'b');
  t_lbl = (ti == 0 ? "OVERVIEW" : (ti == 1 ? "BAXANDALL" : (ti == 2 ? "VOCAL GLUE" : (ti == 3 ? "DE-ESSER" : (ti == 4 ? "SPATIAL" : (ti == 5 ? "PRESENCE" : "PRODUCER"))))));
  gfx_measurestr(t_lbl, tlw, tlh);
  gfx_x = floor(tx + (tab_w - 2 - tlw) * 0.5); gfx_y = tab_y + 8;
  gfx_drawstr(t_lbl);
  mouse_clicked && t_hov ? (
    slider1 = ti;
    slider_automate();
  );
  ti += 1;
);

// ─────────────────────────────────────────────────────────────────────────────
// 3. CENTRAL WORKSPACE CHASSIS
// ─────────────────────────────────────────────────────────────────────────────
ws_x = crt_x + 4; ws_y = tab_y + tab_h + 4;
ws_w = crt_w - 8; ws_h = crt_h - (ws_y - crt_y) - 6;
gfx_r = 0.024; gfx_g = 0.010; gfx_b = 0.032;
gfx_rect(ws_x, ws_y, ws_w, ws_h);
gfx_r = 0.18; gfx_g = 0.08; gfx_b = 0.22;
gfx_rect(ws_x, ws_y, ws_w, ws_h, 0);

function draw_param_slider(px, py, pw, ph, label_str, val, min_v, max_v, fmt_str, s_idx) (
  gfx_r = 0.032; gfx_g = 0.014; gfx_b = 0.042; gfx_rect(px, py, pw, ph);
  gfx_r = 0.22; gfx_g = 0.10; gfx_b = 0.28; gfx_rect(px, py, pw, ph, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = px + 10; gfx_y = py + 6; gfx_drawstr(label_str);

  val_str = sprintf(#, fmt_str, val);
  gfx_setfont(3, "Consolas", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.95;
  gfx_measurestr(val_str, vsw, vsh);
  gfx_x = px + pw - vsw - 10; gfx_y = py + 6; gfx_drawstr(val_str);

  trx = px + 10; try = py + 26; trw = pw - 20; trh = 8;
  gfx_r = 0.014; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(trx, try, trw, trh);
  gfx_r = 0.30; gfx_g = 0.15; gfx_b = 0.38; gfx_rect(trx, try, trw, trh, 0);

  frac = max(0.0, min(1.0, (val - min_v) / (max_v - min_v)));
  fill_w = floor(frac * trw);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_rect(trx, try, fill_w, trh);

  hx = trx + fill_w; hy = try + trh * 0.5;
  gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.95; gfx_circle(hx, hy, 6, 1);
  gfx_r = 0.2; gfx_g = 0.1; gfx_b = 0.2; gfx_circle(hx, hy, 6, 0);

  hov = (mouse_x >= px && mouse_x <= px + pw && mouse_y >= py && mouse_y <= py + ph);
  mouse_clicked && hov ? drag_slider_idx = s_idx;
  drag_slider_idx == s_idx && mouse_down ? (
    new_f = max(0.0, min(1.0, (mouse_x - trx) / trw));
    slider(s_idx) = min_v + new_f * (max_v - min_v);
    update_vocal_filters();
    slider_automate();
  );
);

function draw_sifam_vocal_meter(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) (
  gfx_r = 0.016; gfx_g = 0.007; gfx_b = 0.022;
  gfx_rect(mx, my, mw, mh);
  gfx_r = accent_r * 0.7; gfx_g = accent_g * 0.7; gfx_b = accent_b * 0.7;
  gfx_rect(mx, my, mw, mh, 0);

  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_x = mx + 14; gfx_y = my + 10; gfx_drawstr(title_str);

  gfx_setfont(3, "Consolas", 10.5, 'b'); gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  gfx_x = mx + mw - 75; gfx_y = my + 10;
  gfx_drawstr(is_glue ? "GR GAIN" : "TUBE RMS");

  piv_x = mx + mw * 0.5;
  piv_y = my + mh + 28;
  r_arc = mh * 0.90;
  ang_min = -0.785398;
  ang_max = 0.785398;

  gfx_r = 0.18; gfx_g = 0.08; gfx_b = 0.22;
  step_a = (ang_max - ang_min) / 40.0;
  ai = 0;
  loop(40,
    a1 = ang_min + ai * step_a; a2 = a1 + step_a;
    gfx_line(piv_x + sin(a1) * r_arc, piv_y - cos(a1) * r_arc, piv_x + sin(a2) * r_arc, piv_y - cos(a2) * r_arc);
    ai += 1;
  );

  gfx_setfont(4, "Consolas", 10);
  ti = 0;
  loop(9,
    f = ti / 8.0;
    ta = ang_min + f * (ang_max - ang_min);
    is_red = (f >= 0.75);
    gfx_r = is_red ? 0.98 : (accent_r * 0.9);
    gfx_g = is_red ? 0.25 : (accent_g * 0.9);
    gfx_b = is_red ? 0.30 : (accent_b * 0.9);
    t_len = (ti % 2 == 0) ? 9 : 5;
    gfx_line(piv_x + sin(ta) * (r_arc - t_len), piv_y - cos(ta) * (r_arc - t_len), piv_x + sin(ta) * (r_arc + 1), piv_y - cos(ta) * (r_arc + 1));
    ti += 1;
  );

  gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  gfx_x = piv_x + sin(ang_min) * (r_arc + 4) - 8; gfx_y = piv_y - cos(ang_min) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "0" : "0");
  gfx_x = piv_x - 6; gfx_y = piv_y - r_arc - 16; gfx_drawstr(is_glue ? "-6" : "+5");
  gfx_r = 0.98; gfx_g = 0.30; gfx_b = 0.40;
  gfx_x = piv_x + sin(ang_max) * (r_arc + 4) - 12; gfx_y = piv_y - cos(ang_max) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "-16" : "+10");

  n_frac = max(0.0, min(1.0, needle_val / max_val));
  n_ang = ang_min + n_frac * (ang_max - ang_min);
  tip_x = piv_x + sin(n_ang) * (r_arc + 2);
  tip_y = piv_y - cos(n_ang) * (r_arc + 2);
  base_x = piv_x + sin(n_ang) * 14;
  base_y = piv_y - cos(n_ang) * 14;

  gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
  gfx_line(base_x - 0.5, base_y, tip_x - 0.5, tip_y);
  gfx_line(base_x + 0.5, base_y, tip_x + 0.5, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_circle(tip_x, tip_y, 2, 1);
  gfx_r = 0.08; gfx_g = 0.04; gfx_b = 0.10; gfx_circle(piv_x, my + mh - 8, 14, 1);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b; gfx_circle(piv_x, my + mh - 8, 14, 0);
);

// =============================================================================
// TAB 0: OVERVIEW (SIFAM METERS + CORRELATION RADAR + PLAQUE)
// =============================================================================
slider1 == 0 ? (
  top_row_h = 240;
  meter_w = floor((ws_w - 36 - 280) * 0.5);

  draw_sifam_vocal_meter(ws_x + 12, ws_y + 12, meter_w, top_row_h, "SIFAM VOCAL EMPRESS // TUBE WARMTH", sifam_tube_needle, 10.0, 0, 1.00, 0.41, 0.70);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 1.00; gfx_g = 0.75; gfx_b = 0.90;
  gfx_x = ws_x + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("+%.1f dB TUBE", slider21);

  draw_sifam_vocal_meter(ws_x + 12 + meter_w + 12, ws_y + 12, meter_w, top_row_h, "MASTER VOCAL GLUE // GAIN REDUCTION", sifam_vglue_needle, 16.0, 1, 0.70, 0.53, 1.00);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 0.75; gfx_g = 0.60; gfx_b = 1.00;
  gfx_x = ws_x + 12 + meter_w + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("-%.1f dB GR", sifam_vglue_needle);

  scope_x = ws_x + 12 + meter_w * 2 + 24; scope_w = ws_w - (meter_w * 2 + 48); scope_h = top_row_h;
  gfx_r = 0.016; gfx_g = 0.007; gfx_b = 0.022; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h);
  gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h, 0);

  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = scope_x + 14; gfx_y = ws_y + 22; gfx_drawstr("VOCAL PHASE & STEREO SPREAD");

  sc_cx = scope_x + scope_w * 0.5; sc_cy = ws_y + 12 + scope_h * 0.48; sc_r = scope_h * 0.35;
  gfx_r = 0.18; gfx_g = 0.08; gfx_b = 0.22;
  gfx_circle(sc_cx, sc_cy, sc_r, 0);
  gfx_circle(sc_cx, sc_cy, sc_r * 0.5, 0);
  gfx_line(sc_cx - sc_r, sc_cy, sc_cx + sc_r, sc_cy);
  gfx_line(sc_cx, sc_cy - sc_r, sc_cx, sc_cy + sc_r);

  cbar_y = ws_y + top_row_h - 28; cbar_w = scope_w - 28;
  gfx_r = 0.012; gfx_g = 0.005; gfx_b = 0.016; gfx_rect(scope_x + 14, cbar_y, cbar_w, 14);
  gfx_r = 0.30; gfx_g = 0.15; gfx_b = 0.38; gfx_rect(scope_x + 14, cbar_y, cbar_w, 14, 0);
  c_f = max(0.0, min(1.0, (cur_phase_corr + 1.0) * 0.5));
  cx_pos = scope_x + 14 + floor(c_f * cbar_w);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_rect(cx_pos - 2, cbar_y - 2, 4, 18);

  gfx_setfont(3, "Consolas", 10.5, 'b');
  gfx_x = scope_x + 14; gfx_y = cbar_y - 14; gfx_drawstr("-1.0");
  gfx_x = scope_x + 14 + floor(cbar_w * 0.5) - 8; gfx_y = cbar_y - 14; gfx_drawstr("0.0");
  gfx_x = scope_x + 14 + cbar_w - 24; gfx_y = cbar_y - 14; gfx_drawstr("+1.0");

  p_y = ws_y + top_row_h + 20; p_h = ws_h - top_row_h - 32;
  gfx_r = 0.018; gfx_g = 0.008; gfx_b = 0.024; gfx_rect(ws_x + 12, p_y, ws_w - 24, p_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 12, p_y, ws_w - 24, p_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.90; gfx_b = 1.00;
  gfx_x = ws_x + 28; gfx_y = p_y + 14;
  gfx_printf("ACTIVE PROFILE: %02d - %s", slider2, get_vocal_full_title(slider2));

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.90; gfx_g = 0.82; gfx_b = 0.98;
  gfx_x = ws_x + 28; gfx_y = p_y + 42;
  gfx_printf("CALIBRATION: Trim: %+4.1fdB | Ceiling: %.1fdBTP | De-Ess: %.1fdB @ %dHz | Bax Air: %+.1fdB | Width: %.2fx",
    slider4, slider5, slider7, slider8, slider11, slider18);

  gfx_setfont(4, "Consolas", 11); gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  gfx_x = ws_x + 28; gfx_y = p_y + 70;
  gfx_printf("Summing State: %s | Glue Topology: %s | Music Corridor Request: %.1fdB",
    slider22 ? "ENGAGED (ACTIVE VOCAL SUM)" : "BYPASS (1:1 UNITY PASS)",
    slider12 ? "Opto 2A Vocal Leveler" : "Fairchild 670 Smooth Tube", slider20);
);

// =============================================================================
// TAB 1: BAXANDALL MASTER EQ (CURVE PLOT + 3 INTERACTIVE BANDS)
// =============================================================================
slider1 == 1 ? (
  eq_plot_y = ws_y + 12; eq_plot_h = 240; eq_plot_w = ws_w - 24;
  gfx_r = 0.016; gfx_g = 0.007; gfx_b = 0.022; gfx_rect(ws_x + 12, eq_plot_y, eq_plot_w, eq_plot_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 12, eq_plot_y, eq_plot_w, eq_plot_h, 0);

  gfx_setfont(2, "Orbitron", 12, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 24; gfx_y = eq_plot_y + 12; gfx_drawstr("BAXANDALL IMPERIAL MASTER VOCAL EQUALIZER RESPONSE CURVE");

  cy0 = eq_plot_y + eq_plot_h * 0.5;
  gfx_r = 0.18; gfx_g = 0.08; gfx_b = 0.22;
  gfx_line(ws_x + 12, cy0, ws_x + 12 + eq_plot_w, cy0);
  gfx_line(ws_x + 12, cy0 - 45, ws_x + 12 + eq_plot_w, cy0 - 45);
  gfx_line(ws_x + 12, cy0 + 45, ws_x + 12 + eq_plot_w, cy0 + 45);

  fx100 = ws_x + 12 + floor(eq_plot_w * 0.23);
  fx1k  = ws_x + 12 + floor(eq_plot_w * 0.56);
  fx10k = ws_x + 12 + floor(eq_plot_w * 0.88);
  gfx_line(fx100, eq_plot_y, fx100, eq_plot_y + eq_plot_h);
  gfx_line(fx1k,  eq_plot_y, fx1k,  eq_plot_y + eq_plot_h);
  gfx_line(fx10k, eq_plot_y, fx10k, eq_plot_y + eq_plot_h);

  gfx_setfont(4, "Consolas", 10); gfx_r = 0.60; gfx_g = 0.50; gfx_b = 0.70;
  gfx_x = fx100 + 4; gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("100Hz");
  gfx_x = fx1k + 4;  gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("1kHz");
  gfx_x = fx10k + 4; gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("10kHz");

  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  prev_py = cy0;
  pi = 0;
  loop(100,
    px = ws_x + 12 + floor((pi / 99.0) * eq_plot_w);
    f_val = 20.0 * exp(log(1000.0) * (pi / 99.0));
    g_tot = 0.0;
    f_val < 300.0 ? g_tot += slider9 * (max(0.0, 1.0 - (f_val / 300.0)));
    g_tot += slider10 * exp(-0.5 * sqr((log(f_val / 3500.0) / 0.5)));
    f_val > 5000.0 ? g_tot += slider11 * (min(1.0, (f_val - 5000.0) / 7000.0));
    cur_py = cy0 - g_tot * 7.5;
    pi > 0 ? gfx_line(prev_px, prev_py, px, cur_py);
    prev_px = px; prev_py = cur_py;
    pi += 1;
  );

  col_w = floor((ws_w - 36) / 3);
  cards_y = eq_plot_y + eq_plot_h + 16; cards_h = ws_h - eq_plot_h - 36;
  draw_param_slider(ws_x + 12 + 0 * (col_w + 6), cards_y, col_w, cards_h, "100Hz WARMTH SHELF", slider9, -6.0, 6.0, "%+.1f dB", 9);
  draw_param_slider(ws_x + 12 + 1 * (col_w + 6), cards_y, col_w, cards_h, "3.5kHz CLARITY BELL", slider10, -6.0, 6.0, "%+.1f dB", 10);
  draw_param_slider(ws_x + 12 + 2 * (col_w + 6), cards_y, col_w, cards_h, "12kHz AIR SHEEN SHELF", slider11, -6.0, 6.0, "%+.1f dB", 11);
);

// =============================================================================
// TAB 2: MASTER VOCAL BUS GLUE COMPRESSOR
// =============================================================================
slider1 == 2 ? (
  cg_y = ws_y + 12; cg_w = ws_w - 24; cg_h = ws_h - 24;
  gfx_r = 0.018; gfx_g = 0.008; gfx_b = 0.024; gfx_rect(ws_x + 12, cg_y, cg_w, cg_h);
  gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(ws_x + 12, cg_y, cg_w, cg_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = ws_x + 28; gfx_y = cg_y + 14; gfx_drawstr("MASTER VOCAL GLUE COMPRESSOR (FAIRCHILD 670 / OPTO 2A)");

  top_x = ws_x + 28; top_y = cg_y + 44; top_w = 280; top_h = 32;
  top_hov = (mouse_x >= top_x && mouse_x <= top_x + top_w && mouse_y >= top_y && mouse_y <= top_y + top_h);
  gfx_r = slider12 ? 0.18 : 0.08; gfx_g = slider12 ? 0.08 : 0.14; gfx_b = slider12 ? 0.24 : 0.20;
  gfx_rect(top_x, top_y, top_w, top_h);
  gfx_r = slider12 ? 0.70 : 1.00; gfx_g = slider12 ? 0.53 : 0.41; gfx_b = slider12 ? 1.00 : 0.70;
  gfx_rect(top_x, top_y, top_w, top_h, 0);
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_x = top_x + 14; gfx_y = top_y + 9;
  slider12 ? gfx_drawstr("TOPOLOGY: OPTO 2A VOCAL LEVELER") : gfx_drawstr("TOPOLOGY: FAIRCHILD 670 SMOOTH TUBE");
  mouse_clicked && top_hov ? (slider12 = !slider12; slider_automate(););

  gr_bar_y = top_y + 48; gr_bar_h = 36; gr_bar_w = cg_w - 56;
  gfx_r = 0.012; gfx_g = 0.005; gfx_b = 0.016; gfx_rect(ws_x + 28, gr_bar_y, gr_bar_w, gr_bar_h);
  gfx_r = 0.30; gfx_g = 0.15; gfx_b = 0.38; gfx_rect(ws_x + 28, gr_bar_y, gr_bar_w, gr_bar_h, 0);
  fill_w = floor(gr_bar_w * (min(16.0, vglue_gr_db) / 16.0));
  fill_w > 0 ? (
    gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(ws_x + 28, gr_bar_y + 2, fill_w, gr_bar_h - 4);
  );
  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = ws_x + 40; gfx_y = gr_bar_y + 10;
  gfx_printf("LIVE VOCAL GLUE REDUCTION: -%.2f dB", vglue_gr_db);

  c_sl_w = floor((cg_w - 72) / 3); c_sl_h = 60;
  sl_r1_y = gr_bar_y + 54;
  draw_param_slider(ws_x + 28 + 0 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "THRESHOLD", slider13, -36.0, 0.0, "%.1f dB", 13);
  draw_param_slider(ws_x + 28 + 1 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "RATIO", slider14, 0, 2, "Mode %d", 14);
  draw_param_slider(ws_x + 28 + 2 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "ATTACK", slider15, 1.0, 80.0, "%.1f ms", 15);

  sl_r2_y = sl_r1_y + c_sl_h + 12;
  draw_param_slider(ws_x + 28 + 0 * (c_sl_w + 8), sl_r2_y, c_sl_w, c_sl_h, "RELEASE", slider16, 20.0, 500.0, "%.1f ms", 16);
  draw_param_slider(ws_x + 28 + 1 * (c_sl_w + 8), sl_r2_y, c_sl_w, c_sl_h, "DRY/WET MIX", slider17, 0, 100, "%d %%", 17);
);

// =============================================================================
// TAB 3: DE-ESSER & BLEED SENTRY
// =============================================================================
slider1 == 3 ? (
  de_y = ws_y + 12; de_w = ws_w - 24; de_h = ws_h - 24;
  gfx_r = 0.018; gfx_g = 0.008; gfx_b = 0.024; gfx_rect(ws_x + 12, de_y, de_w, de_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 12, de_y, de_w, de_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 28; gfx_y = de_y + 14; gfx_drawstr("DE-ESSER & HIGH-FREQUENCY BLEED SENTRY");

  draw_param_slider(ws_x + 24, de_y + 48, de_w - 48, 65, "SIBILANCE CLAMP DEPTH", slider7, -12.0, 0.0, "%.1f dB", 7);
  draw_param_slider(ws_x + 24, de_y + 125, de_w - 48, 65, "DE-ESSER CENTER FREQUENCY", slider8, 4500, 9500, "%d Hz", 8);

  adv_y = de_y + 205; adv_h = de_h - 225;
  gfx_r = 0.012; gfx_g = 0.005; gfx_b = 0.016; gfx_rect(ws_x + 24, adv_y, de_w - 48, adv_h);
  gfx_r = 0.30; gfx_g = 0.15; gfx_b = 0.38; gfx_rect(ws_x + 24, adv_y, de_w - 48, adv_h, 0);

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 40; gfx_y = adv_y + 16; gfx_drawstr("MASTER STACK SIBILANCE SUPPRESSION:");
  gfx_setfont(4, "Consolas", 11); gfx_r = 0.85; gfx_g = 0.75; gfx_b = 0.95;
  gfx_x = ws_x + 40; gfx_y = adv_y + 42;
  gfx_drawstr("• Targets cumulative harshness and cymbal bleed across the entire vocal stack (Lead + Doubles + Harmonies).");
  gfx_x = ws_x + 40; gfx_y = adv_y + 64;
  gfx_drawstr("• Dynamic clamp acts only when high-frequency energy spikes above threshold, preserving open air sheen.");
);

// =============================================================================
// TAB 4: SPATIAL IMMERSION & STEREO CORRIDOR
// =============================================================================
slider1 == 4 ? (
  sp_y = ws_y + 12; sp_w = ws_w - 24; sp_h = ws_h - 24;
  gfx_r = 0.018; gfx_g = 0.008; gfx_b = 0.024; gfx_rect(ws_x + 12, sp_y, sp_w, sp_h);
  gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(ws_x + 12, sp_y, sp_w, sp_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = ws_x + 28; gfx_y = sp_y + 14; gfx_drawstr("VOCAL SPATIAL IMMERSION & DYNAMIC MUSIC CORRIDOR");

  draw_param_slider(ws_x + 24, sp_y + 48, sp_w - 48, 65, "VOCAL MID/SIDE WIDTH MULTIPLIER", slider18, 0.80, 1.30, "%.2f x", 18);
  draw_param_slider(ws_x + 24, sp_y + 125, sp_w - 48, 65, "DYNAMIC MUSIC CORRIDOR REQUEST (TO INST BUS)", slider20, 0.0, 3.0, "+%.1f dB", 20);

  ml_x = ws_x + 24; ml_y = sp_y + 205; ml_w = 280; ml_h = 32;
  ml_hov = (mouse_x >= ml_x && mouse_x <= ml_x + ml_w && mouse_y >= ml_y && mouse_y <= ml_y + ml_h);
  gfx_r = slider19 ? 0.18 : 0.08; gfx_g = slider19 ? 0.08 : 0.14; gfx_b = slider19 ? 0.24 : 0.20;
  gfx_rect(ml_x, ml_y, ml_w, ml_h);
  gfx_r = slider19 ? 1.00 : 0.60; gfx_g = slider19 ? 0.41 : 0.40; gfx_b = slider19 ? 0.70 : 0.70;
  gfx_rect(ml_x, ml_y, ml_w, ml_h, 0);
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_x = ml_x + 14; gfx_y = ml_y + 9;
  slider19 ? gfx_drawstr("MONO LOCK: STRICT CENTER ANCHOR") : gfx_drawstr("MONO LOCK: STEREO WIDE PASS");
  mouse_clicked && ml_hov ? (slider19 = !slider19; slider_automate(););

  t_pl_y = sp_y + 255; t_pl_h = sp_h - 275;
  gfx_r = 0.012; gfx_g = 0.005; gfx_b = 0.016; gfx_rect(ws_x + 24, t_pl_y, sp_w - 48, t_pl_h);
  gfx_r = 0.30; gfx_g = 0.15; gfx_b = 0.38; gfx_rect(ws_x + 24, t_pl_y, sp_w - 48, t_pl_h, 0);

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = ws_x + 40; gfx_y = t_pl_y + 16; gfx_drawstr("DYNAMIC MUSIC CORRIDOR PROTOCOL:");
  gfx_setfont(4, "Consolas", 11); gfx_r = 0.85; gfx_g = 0.75; gfx_b = 0.95;
  gfx_x = ws_x + 40; gfx_y = t_pl_y + 42;
  gfx_drawstr("• Publishes request to gmem[1455] for Instrumental Bus Alchemist to carve out conflicting mid-range energy.");
  gfx_x = ws_x + 40; gfx_y = t_pl_y + 64;
  gfx_drawstr("• Mono Center Lock ensures lead vocal stays focused dead-center while wide reverbs and double-tracks bloom wide.");
);

// =============================================================================
// TAB 5: DYNAMIC PRESENCE SENTRY
// =============================================================================
slider1 == 5 ? (
  pr_y = ws_y + 12; pr_w = ws_w - 24; pr_h = ws_h - 24;
  gfx_r = 0.018; gfx_g = 0.008; gfx_b = 0.024; gfx_rect(ws_x + 12, pr_y, pr_w, pr_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 12, pr_y, pr_w, pr_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 28; gfx_y = pr_y + 14; gfx_drawstr("DYNAMIC PRESENCE SENTRY & SPECTRAL HARMONICS");

  draw_param_slider(ws_x + 24, pr_y + 48, pr_w - 48, 65, "VOCAL TUBE WARMTH SATURATION", slider21, 0.0, 10.0, "+%.1f dB", 21);

  box_y = pr_y + 130; box_h = pr_h - 150;
  gfx_r = 0.012; gfx_g = 0.005; gfx_b = 0.016; gfx_rect(ws_x + 24, box_y, pr_w - 48, box_h);
  gfx_r = 0.30; gfx_g = 0.15; gfx_b = 0.38; gfx_rect(ws_x + 24, box_y, pr_w - 48, box_h, 0);

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 40; gfx_y = box_y + 16;
  gfx_printf("VOCAL ENTHALPY: Tube Drive = +%.1f dB | Instrumental Energy (gmem[1402]): %.1f dB", slider21, ib_inst_rms);

  gfx_setfont(4, "Consolas", 11); gfx_r = 0.85; gfx_g = 0.75; gfx_b = 0.95;
  gfx_x = ws_x + 40; gfx_y = box_y + 44;
  gfx_drawstr("• Adds asymmetrical 2nd and 3rd harmonic saturation, giving voices authoritative cut and radio intimacy.");
  gfx_x = ws_x + 40; gfx_y = box_y + 66;
  gfx_drawstr("• Interlocks with Instrumental Bus Alchemist to guarantee clear vocal translation across dense wall-of-sound guitar mixes.");
);

// =============================================================================
// TAB 6: PRODUCER VOCAL MATRIX (25 BENCHMARKS WITH DETAILED FORENSIC PLAQUE)
// =============================================================================
slider1 == 6 ? (
  mat_y = ws_y + 12;
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_setfont(1, "Orbitron", 14, 'b');
  gfx_x = ws_x + 20; gfx_y = mat_y;
  gfx_drawstr("PRODUCER VOCAL MATRIX // 25 REFERENCE-CALIBRATED BENCHMARKS");

  pi = 0; pill_w = floor((ws_w - 40 - 36) / 7); pill_h = 36;
  loop(25,
    p_row = floor(pi / 7); p_col = pi % 7;
    px = ws_x + 16 + p_col * (pill_w + 6);
    py = mat_y + 30 + p_row * (pill_h + 6);
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

    gfx_setfont(3, "Consolas", 11.5, 'b');
    is_sel ? (gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;) : (gfx_r = 0.90; gfx_g = 0.85; gfx_b = 0.98;);
    p_sname = get_vocal_short_name(pi);
    gfx_measurestr(p_sname, psw, psh);
    gfx_x = floor(px + (pill_w - psw) * 0.5); gfx_y = py + 10;
    gfx_drawstr(p_sname);

    mouse_clicked && p_hov ? (
      slider2 = pi;
      prev_vpreset = slider2;
      apply_vocal_preset(slider2);
      slider_automate();
    );
    pi += 1;
  );

  pl_y = mat_y + 205; pl_w = ws_w - 32; pl_h = ws_h - 220;
  gfx_r = 0.018; gfx_g = 0.008; gfx_b = 0.024; gfx_rect(ws_x + 16, pl_y, pl_w, pl_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 16, pl_y, pl_w, pl_h, 0);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 32; gfx_y = pl_y + 14;
  gfx_printf("SELECTED BENCHMARK: %02d - %s", slider2, get_vocal_full_title(slider2));

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.90; gfx_g = 0.82; gfx_b = 0.98;
  gfx_x = ws_x + 32; gfx_y = pl_y + 40;
  gfx_printf("CALIBRATION: Trim %+.1fdB | De-Ess %.1fdB @ %dHz | Bax Mid %+.1fdB | Bax Air %+.1fdB | Tube %+.1fdB | Corridor %.1fdB",
    slider4, slider7, slider8, slider10, slider11, slider21, slider20);

  gfx_setfont(4, "Consolas", 11); gfx_r = 0.80; gfx_g = 0.70; gfx_b = 0.90;
  gfx_x = ws_x + 32; gfx_y = pl_y + 68;
  gfx_drawstr("Full master vocal profile matching the central preset registry. Recalls authentic Baxandall air curves,");
  gfx_x = ws_x + 32; gfx_y = pl_y + 88;
  gfx_drawstr("tube opto/Fairchild vocal glue ballistics, and dynamic unmasking corridor requests.");
);

prev_mouse_down = mouse_down;

@serialize
file_var(0, slider1);
file_var(0, slider2);
file_var(0, slider3);
file_var(0, slider4);
file_var(0, slider5);
file_var(0, slider6);
file_var(0, slider7);
file_var(0, slider8);
file_var(0, slider9);
file_var(0, slider10);
file_var(0, slider11);
file_var(0, slider12);
file_var(0, slider13);
file_var(0, slider14);
file_var(0, slider15);
file_var(0, slider16);
file_var(0, slider17);
file_var(0, slider18);
file_var(0, slider19);
file_var(0, slider20);
file_var(0, slider21);
file_var(0, slider22);
file_var(0, slider23);
file_var(0, slider24);
file_var(0, slider25);
'''

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Damei_VocalBus.jsfx v3.0 written successfully.")
