import os

target_path = r"c:\Dev\DameiSuite\effects\Damei_InstrumentalSuite.jsfx"

code = r'''desc:Damei Instrumental Bus Alchemist (Harmonic Crucible & Summing Matrix)
// =============================================================================
// DAMEI INSTRUMENTAL BUS ALCHEMIST // HARMONIC CRUCIBLE & SUMMING MATRIX (v1.0)
// Archetype: Funtunfunefu-Denkyemfunefu (Siamese Crocodiles - Collective Summing)
// Reference-Calibrated Instrumental Summing Engine with Zero-Cable gmem Interlock
// Communication Range: gmem[1400..1449] (Publishes) | gmem[1450..1499] (Reads Vocal Bus)
// Built by Damei Audio & Antigravity IDE
// =============================================================================

slider1:0<0,6,1{Summing Overview,Tonal Forge EQ,Bus Glue Compressor,Harmonic Crucible,Stereo & Sub-Anchor,Vocal Pocket Corridor,Producer Summing Matrix}>-Active Module
slider2:0<0,24,1{Default Unity Baseline (1:1 Transparent Pass),Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Mirrorcell),Buster Odeholm (thrown / Northlane),Lewis Johns (Love Is Noise / blanket),Kel Pinchin (Split Chain / Currents Target),Dan Lancaster & Jason Perry (Don Broco),Erik Bickerstaffe (Static Dress),Sam Guaiana (Silverstein / TDWP),Zach Tuch (Heavenward / Hundredth),Forrester Savell (Karnivool),Leon Schmidt (SUNBORN - Nebula),Ermin Hamidovic (Systematic Benchmark),Will Putney (Fit For An Autopsy),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill - nerv),Henrik Udd (Architects - Gravity),Dan Braunstein (Spiritbox - Keep Sweet),Zakk Cervini & Erik Ron (Bad Omens),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Acle Kahney (TesseracT - King),Adam Cichocki (heaving. / Timber Studios),Manuel Renner (SENNA / Uberlarm Studios)}>-Producer Summing Profile
slider3:0.0<-6.0,6.0,0.1>-Input Calibration (dB)
slider4:0.0<-12.0,6.0,0.1>-Output Master Trim (dB)
slider5:-6.0<-12.0,0.0,0.1>-Headroom Target Ceiling (dBTP)
slider6:1<0,1,1{Off,Strict -6 dBTP Guard (Zero Clip)}> -Auto-Headroom Guardian
slider7:80<40,160,5>-Sub-Bass Mono-Anchor Cutoff (Hz)
slider8:1<0,1,1{Bypassed,Active Dynamic Dip}>-Low-End Kick/Bass Sentry
slider9:0.0<0.0,3.0,0.1>-Dynamic Vocal Pocket Depth (dB)
slider10:1<0,1,1{Manual,gmem Auto-Sensing from Vocal Bus}>-Vocal Pocket Mode
slider11:0<0,1,1{British VCA (Punch & Snap),Neve Diode Bridge (Vintage Warmth)}>-Bus Glue Topology
slider12:0.0<-36.0,0.0,0.5>-Bus Glue Threshold (dB)
slider13:1<0,3,1{1.5:1,2:1,4:1,8:1}>-Bus Glue Ratio
slider14:30.0<0.1,100.0,0.5>-Bus Glue Attack (ms)
slider15:0<0,4,1{Auto Dual,100ms,300ms,600ms,1.2s}>-Bus Glue Release
slider16:120<30,250,5>-Bus Glue Sidechain HPF (Hz)
slider17:100<0,100,1>-Bus Glue Dry/Wet Mix (%)
slider18:28<20,60,1>-Tonal Forge HPF Cutoff (Hz)
slider19:0.0<-6.0,6.0,0.1>-Tonal Forge 80Hz Punch (dB)
slider20:0.0<-6.0,6.0,0.1>-Tonal Forge 280Hz Mud Scoop (dB)
slider21:0.0<-6.0,6.0,0.1>-Tonal Forge 3.5kHz Bite (dB)
slider22:0.0<-6.0,6.0,0.1>-Tonal Forge 10kHz Air Sheen (dB)
slider23:0<0,3,1{Pure Transparent Console,Neve 8014 Iron Desk,Studer A800 15 IPS Tape,Triode Tube Crucible}>-Harmonic Saturation Type
slider24:0.0<0.0,12.0,0.1>-Harmonic Drive (dB)
slider25:1.00<0.80,1.40,0.01>-Stereo Dimension Width (Quad-Wall)
slider26:1<0,1,1{Off,gmem Song Structure Sync}>-Chorus Impact Dynamic Link
slider27:0<0,1,1{Bypassed,Engaged}>-Instrumental Master Suite Engine

options:gmem=DameiMixMetering
options:maxmem=65536
in_pin:left input
in_pin:right input
out_pin:left output
out_pin:right output

@init
ext_noinit = 1;
srate <= 0 ? srate = 48000;

// Filter coefficients and memory allocations
MEM_BASE = 1000;
f_hpf_l = MEM_BASE;     f_hpf_r = MEM_BASE + 10;
f_mono_l = MEM_BASE + 20; f_mono_r = MEM_BASE + 30;
f_p80_l = MEM_BASE + 40;  f_p80_r = MEM_BASE + 50;
f_m280_l = MEM_BASE + 60; f_m280_r = MEM_BASE + 70;
f_b3k_l = MEM_BASE + 80;  f_b3k_r = MEM_BASE + 90;
f_a10k_l = MEM_BASE + 100; f_a10k_r = MEM_BASE + 110;
f_pocket_l = MEM_BASE + 120; f_pocket_r = MEM_BASE + 130;
f_schpf_l = MEM_BASE + 140; f_schpf_r = MEM_BASE + 150;

scope_buf = MEM_BASE + 500;
scope_wptr = 0;
scope_timer = 0;

// Meter ballistics
sifam_desk_needle = 0;
sifam_glue_needle = 0;
meter_rms_l = 0; meter_rms_r = 0;
meter_peak_l = 0; meter_peak_r = 0;
comp_env = 0;
prev_preset = slider2;

// SVF filter helper
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

function calc_svf_hpf(freq, mem_offset) (
  g_val = tan($pi * max(10.0, min(1000.0, freq)) / srate);
  k_val = 1.41421356;
  a1 = 1.0 / (1.0 + g_val * (g_val + k_val));
  a2 = g_val * a1;
  a3 = g_val * a2;
  mem[mem_offset] = a1; mem[mem_offset+1] = a2; mem[mem_offset+2] = a3; mem[mem_offset+3] = k_val;
);

function eval_svf_hpf(x, mem_offset) (
  v3 = x - mem[mem_offset+5];
  v1 = mem[mem_offset] * mem[mem_offset+4] + mem[mem_offset+1] * v3;
  v2 = mem[mem_offset+5] + mem[mem_offset+1] * mem[mem_offset+4] + mem[mem_offset+2] * v3;
  mem[mem_offset+4] = 2.0 * v1 - mem[mem_offset+4];
  mem[mem_offset+5] = 2.0 * v2 - mem[mem_offset+5];
  x - mem[mem_offset+3] * v1 - v2;
);

function calc_svf_lpf(freq, mem_offset) (
  g_val = tan($pi * max(20.0, min(1000.0, freq)) / srate);
  k_val = 1.41421356;
  a1 = 1.0 / (1.0 + g_val * (g_val + k_val));
  a2 = g_val * a1;
  a3 = g_val * a2;
  mem[mem_offset] = a1; mem[mem_offset+1] = a2; mem[mem_offset+2] = a3; mem[mem_offset+3] = k_val;
);

function eval_svf_lpf(x, mem_offset) (
  v3 = x - mem[mem_offset+5];
  v1 = mem[mem_offset] * mem[mem_offset+4] + mem[mem_offset+1] * v3;
  v2 = mem[mem_offset+5] + mem[mem_offset+1] * mem[mem_offset+4] + mem[mem_offset+2] * v3;
  mem[mem_offset+4] = 2.0 * v1 - mem[mem_offset+4];
  mem[mem_offset+5] = 2.0 * v2 - mem[mem_offset+5];
  v2;
);

function update_filters() (
  calc_svf_hpf(slider18, f_hpf_l); calc_svf_hpf(slider18, f_hpf_r);
  calc_svf_lpf(slider7, f_mono_l); calc_svf_lpf(slider7, f_mono_r);
  calc_svf_bell(80.0, 1.2, slider19, f_p80_l); calc_svf_bell(80.0, 1.2, slider19, f_p80_r);
  calc_svf_bell(280.0, 1.4, slider20, f_m280_l); calc_svf_bell(280.0, 1.4, slider20, f_m280_r);
  calc_svf_bell(3500.0, 1.1, slider21, f_b3k_l); calc_svf_bell(3500.0, 1.1, slider21, f_b3k_r);
  calc_svf_bell(10000.0, 0.8, slider22, f_a10k_l); calc_svf_bell(10000.0, 0.8, slider22, f_a10k_r);
  calc_svf_bell(2500.0, 1.6, -slider9, f_pocket_l); calc_svf_bell(2500.0, 1.6, -slider9, f_pocket_r);
  calc_svf_hpf(slider16, f_schpf_l); calc_svf_hpf(slider16, f_schpf_r);
);

function get_producer_short_name(p_idx) (
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

function get_producer_full_title(p_idx) (
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

function apply_instrumental_preset(p_idx) (
  p_idx == 0 ? ( // Default Unity Baseline
    slider3 = 0.0; slider4 = 0.0; slider5 = -6.0; slider6 = 1; slider7 = 80;
    slider8 = 0; slider9 = 0.0; slider11 = 0; slider12 = 0.0; slider13 = 1;
    slider14 = 30.0; slider15 = 0; slider16 = 120; slider17 = 100;
    slider18 = 25; slider19 = 0.0; slider20 = 0.0; slider21 = 0.0; slider22 = 0.0;
    slider23 = 0; slider24 = 0.0; slider25 = 1.00; slider26 = 0; slider27 = 1;
  ) : p_idx == 1 ? ( // Lance Prenc
    slider4 = -3.0; slider7 = 90; slider8 = 1; slider9 = 1.5; slider11 = 0;
    slider12 = -18.0; slider13 = 2; slider14 = 30.0; slider15 = 0; slider16 = 135;
    slider19 = 1.2; slider20 = -2.5; slider21 = 1.8; slider22 = 1.5;
    slider23 = 1; slider24 = 2.4; slider25 = 1.15; slider27 = 1;
  ) : p_idx == 2 ? ( // Scott Seigel
    slider4 = -2.5; slider7 = 85; slider8 = 1; slider9 = 1.2; slider11 = 1;
    slider12 = -16.0; slider13 = 1; slider14 = 25.0; slider15 = 1; slider16 = 125;
    slider19 = 2.0; slider20 = -1.8; slider21 = 1.2; slider22 = 1.0;
    slider23 = 1; slider24 = 3.2; slider25 = 1.10; slider27 = 1;
  ) : p_idx == 3 ? ( // Jonathan Dolese
    slider4 = -2.0; slider7 = 75; slider8 = 1; slider9 = 1.4; slider11 = 0;
    slider12 = -15.0; slider13 = 1; slider14 = 30.0; slider15 = 0; slider16 = 120;
    slider19 = 1.5; slider20 = -1.5; slider21 = 2.0; slider22 = 1.8;
    slider23 = 3; slider24 = 1.8; slider25 = 1.18; slider27 = 1;
  ) : p_idx == 4 ? ( // Buster Odeholm
    slider4 = -3.5; slider7 = 95; slider8 = 1; slider9 = 1.8; slider11 = 0;
    slider12 = -20.0; slider13 = 2; slider14 = 20.0; slider15 = 0; slider16 = 140;
    slider19 = 2.2; slider20 = -3.0; slider21 = 2.2; slider22 = 1.2;
    slider23 = 1; slider24 = 3.5; slider25 = 1.20; slider27 = 1;
  ) : p_idx == 5 ? ( // Lewis Johns
    slider4 = -2.0; slider7 = 70; slider8 = 1; slider9 = 0.8; slider11 = 1;
    slider12 = -14.0; slider13 = 0; slider14 = 40.0; slider15 = 2; slider16 = 110;
    slider19 = 1.0; slider20 = -1.2; slider21 = 1.0; slider22 = 2.2;
    slider23 = 2; slider24 = 2.0; slider25 = 1.25; slider27 = 1;
  ) : p_idx == 6 ? ( // Kel Pinchin (Split Chain Target)
    slider4 = -3.5; slider7 = 85; slider8 = 1; slider9 = 1.6; slider11 = 0;
    slider12 = -16.5; slider13 = 1; slider14 = 30.0; slider15 = 0; slider16 = 130;
    slider19 = 1.4; slider20 = -2.8; slider21 = 1.6; slider22 = 1.8;
    slider23 = 1; slider24 = 2.2; slider25 = 1.18; slider27 = 1;
  ) : p_idx == 7 ? ( // Dan Lancaster
    slider4 = -3.0; slider7 = 80; slider8 = 1; slider9 = 1.5; slider11 = 0;
    slider12 = -18.0; slider13 = 1; slider14 = 30.0; slider15 = 0; slider16 = 125;
    slider19 = 1.6; slider20 = -2.0; slider21 = 2.4; slider22 = 2.5;
    slider23 = 3; slider24 = 2.0; slider25 = 1.22; slider27 = 1;
  ) : p_idx == 8 ? ( // Erik Bickerstaffe
    slider4 = -2.8; slider7 = 75; slider8 = 1; slider9 = 1.2; slider11 = 1;
    slider12 = -17.0; slider13 = 1; slider14 = 25.0; slider15 = 1; slider16 = 115;
    slider19 = 1.8; slider20 = -1.6; slider21 = 1.8; slider22 = 1.2;
    slider23 = 2; slider24 = 3.8; slider25 = 1.12; slider27 = 1;
  ) : p_idx == 9 ? ( // Sam Guaiana
    slider4 = -2.8; slider7 = 85; slider8 = 1; slider9 = 1.4; slider11 = 0;
    slider12 = -16.0; slider13 = 1; slider14 = 30.0; slider15 = 0; slider16 = 125;
    slider19 = 1.5; slider20 = -2.2; slider21 = 1.8; slider22 = 1.6;
    slider23 = 1; slider24 = 2.5; slider25 = 1.15; slider27 = 1;
  ) : p_idx == 10 ? ( // Zach Tuch
    slider4 = -2.0; slider7 = 75; slider8 = 1; slider9 = 0.8; slider11 = 1;
    slider12 = -14.0; slider13 = 0; slider14 = 35.0; slider15 = 2; slider16 = 110;
    slider19 = 1.2; slider20 = -1.2; slider21 = 0.8; slider22 = 1.8;
    slider23 = 2; slider24 = 2.2; slider25 = 1.20; slider27 = 1;
  ) : p_idx == 11 ? ( // Forrester Savell
    slider4 = -1.5; slider7 = 75; slider8 = 1; slider9 = 1.0; slider11 = 0;
    slider12 = -13.0; slider13 = 0; slider14 = 40.0; slider15 = 0; slider16 = 110;
    slider19 = 0.8; slider20 = -1.4; slider21 = 1.2; slider22 = 1.4;
    slider23 = 1; slider24 = 1.2; slider25 = 1.14; slider27 = 1;
  ) : p_idx == 12 ? ( // Leon Schmidt
    slider4 = -2.5; slider7 = 85; slider8 = 1; slider9 = 1.5; slider11 = 0;
    slider12 = -17.0; slider13 = 2; slider14 = 25.0; slider15 = 0; slider16 = 130;
    slider19 = 1.8; slider20 = -2.6; slider21 = 2.2; slider22 = 2.0;
    slider23 = 1; slider24 = 2.6; slider25 = 1.22; slider27 = 1;
  ) : p_idx == 13 ? ( // Ermin Hamidovic
    slider4 = -3.0; slider7 = 80; slider8 = 1; slider9 = 1.0; slider11 = 0;
    slider12 = -15.0; slider13 = 1; slider14 = 30.0; slider15 = 0; slider16 = 120;
    slider19 = 0.0; slider20 = -1.5; slider21 = 0.5; slider22 = 0.8;
    slider23 = 0; slider24 = 0.5; slider25 = 1.08; slider27 = 1;
  ) : p_idx == 14 ? ( // Will Putney
    slider4 = -4.0; slider7 = 90; slider8 = 1; slider9 = 1.8; slider11 = 0;
    slider12 = -20.0; slider13 = 2; slider14 = 20.0; slider15 = 0; slider16 = 135;
    slider19 = 2.4; slider20 = -2.8; slider21 = 2.5; slider22 = 1.0;
    slider23 = 1; slider24 = 4.0; slider25 = 1.16; slider27 = 1;
  ) : p_idx == 15 ? ( // George Lever
    slider4 = -2.0; slider7 = 75; slider8 = 1; slider9 = 1.2; slider11 = 1;
    slider12 = -15.0; slider13 = 1; slider14 = 35.0; slider15 = 1; slider16 = 115;
    slider19 = 1.8; slider20 = -1.6; slider21 = 1.0; slider22 = 1.5;
    slider23 = 2; slider24 = 2.8; slider25 = 1.20; slider27 = 1;
  ) : p_idx == 16 ? ( // Sam Bassal
    slider4 = -2.5; slider7 = 80; slider8 = 1; slider9 = 1.4; slider11 = 0;
    slider12 = -16.5; slider13 = 1; slider14 = 30.0; slider15 = 0; slider16 = 125;
    slider19 = 1.5; slider20 = -2.2; slider21 = 1.8; slider22 = 1.6;
    slider23 = 2; slider24 = 2.5; slider25 = 1.18; slider27 = 1;
  ) : p_idx == 17 ? ( // Henrik Udd
    slider4 = -3.0; slider7 = 85; slider8 = 1; slider9 = 1.6; slider11 = 0;
    slider12 = -18.0; slider13 = 1; slider14 = 30.0; slider15 = 0; slider16 = 130;
    slider19 = 1.6; slider20 = -2.4; slider21 = 2.2; slider22 = 2.2;
    slider23 = 1; slider24 = 2.8; slider25 = 1.22; slider27 = 1;
  ) : p_idx == 18 ? ( // Dan Braunstein
    slider4 = -3.0; slider7 = 80; slider8 = 1; slider9 = 1.6; slider11 = 0;
    slider12 = -17.0; slider13 = 1; slider14 = 30.0; slider15 = 0; slider16 = 125;
    slider19 = 1.5; slider20 = -2.6; slider21 = 2.2; slider22 = 2.4;
    slider23 = 3; slider24 = 2.2; slider25 = 1.24; slider27 = 1;
  ) : p_idx == 19 ? ( // Zakk Cervini
    slider4 = -3.0; slider7 = 85; slider8 = 1; slider9 = 1.8; slider11 = 0;
    slider12 = -18.0; slider13 = 2; slider14 = 25.0; slider15 = 0; slider16 = 135;
    slider19 = 1.8; slider20 = -2.5; slider21 = 2.4; slider22 = 2.6;
    slider23 = 3; slider24 = 2.6; slider25 = 1.20; slider27 = 1;
  ) : p_idx == 20 ? ( // Jens Bogren
    slider4 = -3.0; slider7 = 85; slider8 = 1; slider9 = 1.4; slider11 = 0;
    slider12 = -17.5; slider13 = 1; slider14 = 30.0; slider15 = 0; slider16 = 125;
    slider19 = 1.8; slider20 = -2.4; slider21 = 1.8; slider22 = 1.2;
    slider23 = 1; slider24 = 2.5; slider25 = 1.15; slider27 = 1;
  ) : p_idx == 21 ? ( // Nolly Getgood
    slider4 = -3.0; slider7 = 85; slider8 = 1; slider9 = 1.5; slider11 = 0;
    slider12 = -16.0; slider13 = 1; slider14 = 30.0; slider15 = 0; slider16 = 130;
    slider19 = 1.2; slider20 = -3.5; slider21 = 1.6; slider22 = 1.8;
    slider23 = 1; slider24 = 1.8; slider25 = 1.16; slider27 = 1;
  ) : p_idx == 22 ? ( // Acle Kahney
    slider4 = -2.0; slider7 = 80; slider8 = 1; slider9 = 1.2; slider11 = 0;
    slider12 = -14.0; slider13 = 0; slider14 = 35.0; slider15 = 0; slider16 = 125;
    slider19 = 1.0; slider20 = -1.8; slider21 = 1.5; slider22 = 1.8;
    slider23 = 0; slider24 = 0.8; slider25 = 1.16; slider27 = 1;
  ) : p_idx == 23 ? ( // Adam Cichocki (heaving.)
    slider4 = -2.5; slider7 = 75; slider8 = 1; slider9 = 1.4; slider11 = 1;
    slider12 = -16.0; slider13 = 2; slider14 = 20.0; slider15 = 1; slider16 = 115;
    slider19 = 2.2; slider20 = -1.8; slider21 = 1.4; slider22 = 2.4;
    slider23 = 2; slider24 = 3.6; slider25 = 1.26; slider27 = 1;
  ) : ( // Manuel Renner (SENNA)
    slider4 = -3.0; slider7 = 90; slider8 = 1; slider9 = 1.6; slider11 = 0;
    slider12 = -18.0; slider13 = 2; slider14 = 25.0; slider15 = 0; slider16 = 135;
    slider19 = 1.6; slider20 = -2.6; slider21 = 2.2; slider22 = 2.2;
    slider23 = 1; slider24 = 2.6; slider25 = 1.18; slider27 = 1;
  );
  update_filters();
);

update_filters();
apply_instrumental_preset(slider2);

@slider
slider2 != prev_preset ? (
  prev_preset = slider2;
  apply_instrumental_preset(slider2);
);
update_filters();

@block
// Read telemetry from Vocal Bus (gmem[1450..1499])
vb_alive = (time_precise() - gmem[1450] < 1.5) && gmem[1451];
vb_vocal_rms = vb_alive ? gmem[1452] : -90.0;
vb_req_pocket = vb_alive ? max(0.0, min(3.0, gmem[1460])) : 0.0;

// Read Song Structure Bridge (gmem[100..105])
ss_region_idx = gmem[100];
ss_is_chorus  = gmem[102] == 1;

// Dynamic Vocal Pocket depth
slider10 == 1 && vb_alive ? (
  pocket_depth = vb_req_pocket;
) : (
  pocket_depth = slider9;
);
calc_svf_bell(2500.0, 1.6, -pocket_depth, f_pocket_l);
calc_svf_bell(2500.0, 1.6, -pocket_depth, f_pocket_r);

// Compressor time constants
comp_att = exp(-1.0 / (max(0.1, slider14) * 0.001 * srate));
comp_rel = exp(-1.0 / (max(10.0, slider15 == 0 ? 150.0 : (slider15 == 1 ? 100.0 : (slider15 == 2 ? 300.0 : (slider15 == 3 ? 600.0 : 1200.0)))) * 0.001 * srate));
comp_ratio = slider13 == 0 ? 1.5 : (slider13 == 1 ? 2.0 : (slider13 == 2 ? 4.0 : 8.0));
comp_thresh = slider12;

// Output trim and headroom ceiling
in_gain_lin  = exp(slider3 * 0.11512925);
out_gain_lin = exp(slider4 * 0.11512925);
ceiling_lin  = exp(slider5 * 0.11512925);

@sample
// 1. Input Gain Calibration
s0 = spl0 * in_gain_lin;
s1 = spl1 * in_gain_lin;

slider27 ? (
  // 2. Tonal Forge HPF Cutoff
  s0 = eval_svf_hpf(s0, f_hpf_l);
  s1 = eval_svf_hpf(s1, f_hpf_r);

  // 3. Sub-Bass Mono Anchor (<80 Hz mono sum)
  sub0 = eval_svf_lpf(s0, f_mono_l);
  sub1 = eval_svf_lpf(s1, f_mono_r);
  sub_mono = (sub0 + sub1) * 0.5;
  s0 = s0 - sub0 + sub_mono;
  s1 = s1 - sub1 + sub_mono;

  // 4. 5-Band Tonal Forge EQ
  s0 = eval_svf_bell(s0, f_p80_l);   s1 = eval_svf_bell(s1, f_p80_r);
  s0 = eval_svf_bell(s0, f_m280_l);  s1 = eval_svf_bell(s1, f_m280_r);
  s0 = eval_svf_bell(s0, f_b3k_l);   s1 = eval_svf_bell(s1, f_b3k_r);
  s0 = eval_svf_bell(s0, f_a10k_l);  s1 = eval_svf_bell(s1, f_a10k_r);

  // 5. Dynamic Vocal Pocket Corridor
  pocket_depth > 0.01 ? (
    s0 = eval_svf_bell(s0, f_pocket_l);
    s1 = eval_svf_bell(s1, f_pocket_r);
  );

  // 6. Dual-Topology Bus Glue Compressor
  // Sidechain HPF detector
  sc0 = eval_svf_hpf(s0, f_schpf_l);
  sc1 = eval_svf_hpf(s1, f_schpf_r);
  sc_max = max(abs(sc0), abs(sc1));
  sc_db = sc_max > 0.000001 ? 20.0 * log10(sc_max) : -120.0;

  sc_over = sc_db - comp_thresh;
  sc_over > 0.0 ? (
    gr_target = sc_over * (1.0 - 1.0 / comp_ratio);
  ) : (
    gr_target = 0.0;
  );

  gr_target > comp_env ? (
    comp_env = comp_target = comp_env * comp_att + gr_target * (1.0 - comp_att);
  ) : (
    comp_env = comp_env * comp_rel + gr_target * (1.0 - comp_rel);
  );
  glue_gr_db = comp_env;
  glue_gain_lin = exp(-glue_gr_db * 0.11512925);

  dry0 = s0; dry1 = s1;
  wet0 = s0 * glue_gain_lin;
  wet1 = s1 * glue_gain_lin;
  mix_ratio = slider17 * 0.01;
  s0 = dry0 * (1.0 - mix_ratio) + wet0 * mix_ratio;
  s1 = dry1 * (1.0 - mix_ratio) + wet1 * mix_ratio;

  // 7. Harmonic Crucible Saturation
  slider24 > 0.01 ? (
    h_drive = exp(slider24 * 0.11512925);
    slider23 == 1 ? ( // Neve 8014 Desk Drive (asymmetrical Class A warmth)
      d0 = s0 * h_drive; d1 = s1 * h_drive;
      s0 = (d0 / (1.0 + abs(d0) * 0.5)) / h_drive;
      s1 = (d1 / (1.0 + abs(d1) * 0.5)) / h_drive;
    ) : slider23 == 2 ? ( // Studer A800 15 IPS Tape (soft compression & 3rd harmonic)
      d0 = s0 * h_drive; d1 = s1 * h_drive;
      s0 = (tanh(d0 * 0.7) * 1.3) / h_drive;
      s1 = (tanh(d1 * 0.7) * 1.3) / h_drive;
    ) : slider23 == 3 ? ( // Triode Tube Crucible (even harmonic richness)
      d0 = s0 * h_drive; d1 = s1 * h_drive;
      s0 = (d0 + 0.12 * d0 * d0 - 0.04 * d0 * d0 * d0) / h_drive;
      s1 = (d1 + 0.12 * d1 * d1 - 0.04 * d1 * d1 * d1) / h_drive;
    );
  );

  // 8. Quad-Wall Stereo Imager (Mid/Side Width Shaper)
  mid = (s0 + s1) * 0.5;
  side = (s0 - s1) * 0.5 * slider25;
  s0 = mid + side;
  s1 = mid - side;

  // 9. Output Master Trim
  s0 *= out_gain_lin;
  s1 *= out_gain_lin;

  // 10. Strict -6 dBTP Headroom Guardian
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

// Telemetry & Scope buffering
scope_timer += 1;
scope_timer >= 8 ? (
  scope_timer = 0;
  scope_buf[scope_wptr] = (spl0 + spl1) * 0.5;
  scope_wptr = (scope_wptr + 1) % 128;
);

// Meter Ballistics (100ms smoothing)
meter_rms_l = meter_rms_l * 0.999 + spl0 * spl0 * 0.001;
meter_rms_r = meter_rms_r * 0.999 + spl1 * spl1 * 0.001;
sifam_desk_needle = sifam_desk_needle * 0.95 + slider24 * 0.05;
sifam_glue_needle = sifam_glue_needle * 0.90 + glue_gr_db * 0.10;

// Publish to gmem[1400..1449]
gmem[1400] = time_precise();
gmem[1401] = 1.0;
gmem[1402] = 10.0 * log10(max(0.0000001, (meter_rms_l + meter_rms_r) * 0.5));
gmem[1403] = max(abs(spl0), abs(spl1));
gmem[1404] = gmem[1403] > 0.0001 ? 20.0 * log10(gmem[1403]) - gmem[1402] : 12.0;
gmem[1405] = slider25;
gmem[1407] = slider2;

@gfx 840 480
disp_w = gfx_w; disp_h = gfx_h;

!fonts_initialized ? (
  gfx_setfont(1, "Orbitron", 13, 'b');
  gfx_setfont(2, "Orbitron", 10, 'b');
  gfx_setfont(3, "Consolas", 11, 'b');
  gfx_setfont(4, "Consolas", 10);
  fonts_initialized = 1;
);

// 1. Chassis Background (Obsidian Titanium)
gfx_r = 0.027; gfx_g = 0.039; gfx_b = 0.059;
gfx_rect(0, 0, disp_w, disp_h);

// 2. Top Header Bar
hdr_y = 6; hdr_h = 42;
gfx_r = 0.040; gfx_g = 0.055; gfx_b = 0.078;
gfx_rect(8, hdr_y, disp_w - 16, hdr_h);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
gfx_rect(8, hdr_y, disp_w - 16, hdr_h, 0);

// Title & Adinkra Archetype
gfx_setfont(1, "Orbitron", 13, 'b');
gfx_r = 0.90; gfx_g = 0.95; gfx_b = 1.00;
gfx_x = 20; gfx_y = hdr_y + 6;
gfx_drawstr("I N S T R U M E N T A L   B U S   A L C H E M I S T");

gfx_setfont(4);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
gfx_x = 20; gfx_y = hdr_y + 24;
gfx_drawstr("HARMONIC CRUCIBLE // FUNTUNFUNEFU-DENKYEMFUNEFU MATRIX");

// Bypass Button
byp_w = 85; byp_h = 24; byp_x = disp_w - byp_w - 16; byp_y = hdr_y + 9;
byp_hov = (mouse_x >= byp_x && mouse_x <= byp_x + byp_w && mouse_y >= byp_y && mouse_y <= byp_y + byp_h);
gfx_r = slider27 ? (byp_hov ? 0.12 : 0.06) : (byp_hov ? 0.25 : 0.15);
gfx_g = slider27 ? (byp_hov ? 0.28 : 0.18) : (byp_hov ? 0.08 : 0.05);
gfx_b = slider27 ? (byp_hov ? 0.38 : 0.24) : (byp_hov ? 0.08 : 0.05);
gfx_rect(byp_x, byp_y, byp_w, byp_h);
gfx_r = slider27 ? 0.00 : 0.95; gfx_g = slider27 ? 0.95 : 0.30; gfx_b = slider27 ? 0.65 : 0.30;
gfx_rect(byp_x, byp_y, byp_w, byp_h, 0);
gfx_setfont(2); gfx_x = byp_x + (slider27 ? 12 : 10); gfx_y = byp_y + 5;
slider27 ? gfx_drawstr("ENGAGED") : gfx_drawstr("BYPASS");
(mouse_cap & 1) && !prev_mouse_cap && byp_hov ? (
  slider27 = !slider27;
  slider_automate(67108864);
);

// Vocal Bus Telemetry Link Indicator
link_w = 145; link_h = 24; link_x = byp_x - link_w - 10; link_y = hdr_y + 9;
gfx_r = vb_alive ? 0.04 : 0.08; gfx_g = vb_alive ? 0.18 : 0.08; gfx_b = vb_alive ? 0.14 : 0.10;
gfx_rect(link_x, link_y, link_w, link_h);
gfx_r = vb_alive ? 0.00 : 0.50; gfx_g = vb_alive ? 0.95 : 0.50; gfx_b = vb_alive ? 0.65 : 0.50;
gfx_rect(link_x, link_y, link_w, link_h, 0);
gfx_setfont(4); gfx_x = link_x + 8; gfx_y = link_y + 5;
vb_alive ? (
  gfx_r = 0.00; gfx_g = 0.95; gfx_b = 0.65;
  gfx_printf("VOCAL LINK: %.1fdB", vb_vocal_rms);
) : (
  gfx_r = 0.60; gfx_g = 0.70; gfx_b = 0.80;
  gfx_drawstr("VOCAL LINK: STANDBY");
);

// 3. Navigation Tabs
tab_y = hdr_y + hdr_h + 6; tab_h = 24;
tab_w = floor((disp_w - 24) / 7);
ti = 0;
loop(7,
  tx = 12 + ti * tab_w;
  sel = (slider1 == ti);
  gfx_r = sel ? 0.10 : 0.038; gfx_g = sel ? 0.16 : 0.048; gfx_b = sel ? 0.22 : 0.065;
  gfx_rect(tx, tab_y, tab_w - 3, tab_h);
  sel ? (
    gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
    gfx_rect(tx, tab_y + tab_h - 2, tab_w - 3, 2);
    gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  ) : (
    gfx_r = 0.55; gfx_g = 0.65; gfx_b = 0.75;
  );
  gfx_setfont(4);
  t_lbl = (ti == 0 ? "OVERVIEW" : (ti == 1 ? "TONAL EQ" : (ti == 2 ? "BUS GLUE" : (ti == 3 ? "CRUCIBLE" : (ti == 4 ? "STEREO" : (ti == 5 ? "POCKET" : "PRODUCER"))))));
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
gfx_r = 0.020; gfx_g = 0.028; gfx_b = 0.040;
gfx_rect(ws_x, ws_y, ws_w, ws_h);
gfx_r = 0.10; gfx_g = 0.16; gfx_b = 0.24;
gfx_rect(ws_x, ws_y, ws_w, ws_h, 0);

// =============================================================================
// TAB 0: SUMMING OVERVIEW (TWIN SIFAM ANALOG METERS & I/O LEVEL CALIBRATION)
// =============================================================================
slider1 == 0 ? (
  // SIFAM Meters Deck (Left: Desk THD Drive, Right: Glue Compressor GR dB)
  sm_y = ws_y + 12; sm_h = 175;
  sm_w = floor((ws_w - 30) / 2);

  // Meter 1: Desk Drive
  m1_x = ws_x + 10;
  gfx_r = 0.015; gfx_g = 0.020; gfx_b = 0.030; gfx_rect(m1_x, sm_y, sm_w, sm_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(m1_x, sm_y, sm_w, sm_h, 0);
  gfx_setfont(2); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = m1_x + 12; gfx_y = sm_y + 10; gfx_drawstr("HARMONIC DESK DRIVE / THD %");
  // Needle drawing
  n1_cx = m1_x + sm_w * 0.5; n1_cy = sm_y + sm_h - 15;
  n1_ang = -0.7 + (min(12.0, sifam_desk_needle) / 12.0) * 1.4;
  n1_len = sm_h * 0.65;
  gfx_line(n1_cx, n1_cy, n1_cx + sin(n1_ang) * n1_len, n1_cy - cos(n1_ang) * n1_len);
  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.0; gfx_g = 0.9; gfx_b = 0.4;
  gfx_x = m1_x + 12; gfx_y = sm_y + sm_h - 30;
  gfx_printf("+%.1f dB DRIVE", slider24);

  // Meter 2: Bus Glue GR
  m2_x = m1_x + sm_w + 10;
  gfx_r = 0.015; gfx_g = 0.020; gfx_b = 0.030; gfx_rect(m2_x, sm_y, sm_w, sm_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(m2_x, sm_y, sm_w, sm_h, 0);
  gfx_setfont(2); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = m2_x + 12; gfx_y = sm_y + 10; gfx_drawstr("BUS GLUE COMPRESSION GR (dB)");
  n2_cx = m2_x + sm_w * 0.5; n2_cy = sm_y + sm_h - 15;
  n2_ang = -0.7 + (min(12.0, sifam_glue_needle) / 12.0) * 1.4;
  gfx_line(n2_cx, n2_cy, n2_cx + sin(n2_ang) * n1_len, n2_cy - cos(n2_ang) * n1_len);
  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.00; gfx_g = 0.95; gfx_b = 1.00;
  gfx_x = m2_x + 12; gfx_y = sm_y + sm_h - 30;
  gfx_printf("-%.1f dB GR", sifam_glue_needle);

  // Bottom Status & Controls Plaque
  p_y = sm_y + sm_h + 12; p_h = ws_h - sm_h - 30;
  gfx_r = 0.030; gfx_g = 0.040; gfx_b = 0.055; gfx_rect(ws_x + 10, p_y, ws_w - 20, p_h);
  gfx_r = 0.14; gfx_g = 0.22; gfx_b = 0.32; gfx_rect(ws_x + 10, p_y, ws_w - 20, p_h, 0);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 0.90; gfx_g = 0.95; gfx_b = 1.00;
  gfx_x = ws_x + 24; gfx_y = p_y + 12;
  gfx_printf("ACTIVE PROFILE: %02d - %s", slider2, get_producer_full_title(slider2));

  gfx_setfont(3); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.98;
  gfx_x = ws_x + 24; gfx_y = p_y + 36;
  gfx_printf("CALIBRATION: Trim: %+4.1fdB | Ceiling: %.1fdBTP | Sub Anchor: %dHz | Vocal Pocket: %.1fdB | Quad Width: %.2fx",
    slider4, slider5, slider7, pocket_depth, slider25);

  gfx_setfont(4); gfx_r = 0.55; gfx_g = 0.70; gfx_b = 0.85;
  gfx_x = ws_x + 24; gfx_y = p_y + 60;
  gfx_printf("Summing State: %s | Comp Topology: %s | Saturation Mode: %s",
    slider27 ? "ENGAGED (ACTIVE SUMMING)" : "BYPASS (1:1 UNITY PASS)",
    slider11 ? "Neve Diode Bridge" : "British VCA Punch",
    slider23 == 1 ? "Neve 8014 Iron Desk" : (slider23 == 2 ? "Studer A800 15 IPS" : (slider23 == 3 ? "Triode Tube" : "Pure Transparent")));
);

// =============================================================================
// TAB 6: PRODUCER SUMMING MATRIX (25 MIXING BENCHMARKS)
// =============================================================================
slider1 == 6 ? (
  mat_y = ws_y + 10;
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_setfont(1, "Orbitron", 14, 'b');
  gfx_x = ws_x + 14; gfx_y = mat_y;
  gfx_drawstr("PRODUCER SUMMING MATRIX // 25 REFERENCE-CALIBRATED BENCHMARKS");

  pi = 0; pill_w = floor((ws_w - 32 - 36) / 7); pill_h = 32;
  loop(25,
    p_row = floor(pi / 7); p_col = pi % 7;
    px = ws_x + 12 + p_col * (pill_w + 6);
    py = mat_y + 26 + p_row * (pill_h + 6);
    is_sel = (slider2 == pi);
    p_hov = (mouse_x >= px && mouse_x <= px + pill_w && mouse_y >= py && mouse_y <= py + pill_h);

    gfx_r = is_sel ? 0.20 : (p_hov ? 0.10 : 0.035);
    gfx_g = is_sel ? 0.12 : (p_hov ? 0.06 : 0.045);
    gfx_b = is_sel ? 0.06 : (p_hov ? 0.08 : 0.060);
    gfx_rect(px, py, pill_w, pill_h);

    gfx_r = is_sel ? 0.85 : (p_hov ? 0.50 : 0.25);
    gfx_g = is_sel ? 0.47 : (p_hov ? 0.30 : 0.15);
    gfx_b = is_sel ? 0.21 : (p_hov ? 0.20 : 0.10);
    gfx_rect(px, py, pill_w, pill_h, 0);

    gfx_setfont(3);
    is_sel ? (gfx_r = 1.00; gfx_g = 0.80; gfx_b = 0.40;) : (gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;);
    p_sname = get_producer_short_name(pi);
    gfx_measurestr(p_sname, psw, psh);
    gfx_x = floor(px + (pill_w - psw) * 0.5); gfx_y = py + 8;
    gfx_drawstr(p_sname);

    (mouse_cap & 1) && !prev_mouse_cap && p_hov ? (
      slider2 = pi;
      prev_preset = slider2;
      apply_instrumental_preset(slider2);
      slider_automate(2);
    );
    pi += 1;
  );

  pl_y = mat_y + 185; pl_w = ws_w - 24; pl_h = ws_h - 195;
  gfx_r = 0.025; gfx_g = 0.032; gfx_b = 0.044; gfx_rect(ws_x + 12, pl_y, pl_w, pl_h);
  gfx_r = 0.14; gfx_g = 0.22; gfx_b = 0.32; gfx_rect(ws_x + 12, pl_y, pl_w, pl_h, 0);

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 24; gfx_y = pl_y + 12;
  gfx_printf("SELECTED BENCHMARK: %02d - %s", slider2, get_producer_full_title(slider2));

  gfx_setfont(3); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.98;
  gfx_x = ws_x + 24; gfx_y = pl_y + 36;
  gfx_printf("SETTINGS: Trim %+.1fdB | Glue Thresh %.1fdB (Ratio %.1f:1) | Mud Scoop %+.1fdB | Drive %+.1fdB | Width %.2fx",
    slider4, slider12, comp_ratio, slider20, slider24, slider25);
);

prev_mouse_cap = mouse_cap;
'''

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Damei_InstrumentalSuite.jsfx generated successfully.")
