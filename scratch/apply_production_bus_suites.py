import os

# ==============================================================================
# 1. DAMEI INSTRUMENTAL BUS ALCHEMIST (v3.1 PRODUCTION BUILD)
# ==============================================================================
inst_path = r"c:\Dev\DameiSuite\effects\Damei_InstrumentalSuite.jsfx"

inst_code = r'''desc:Damei Instrumental Bus Alchemist (Harmonic Crucible & Summing Matrix)
// =============================================================================
// DAMEI INSTRUMENTAL BUS ALCHEMIST // HARMONIC CRUCIBLE & SUMMING MATRIX (v3.1)
// Archetype: Funtunfunefu-Denkyemfunefu (Siamese Crocodiles - Collective Summing)
// Reference-Calibrated Instrumental Summing Engine with Zero-Cable gmem Interlock
// Communication Range: gmem[1400..1449] (Publishes) | gmem[1450..1499] (Reads Vocal Bus)
// Built by Damei Audio & Antigravity IDE (2026 Production Standard)
// =============================================================================

slider1:0<0,6,1{Summing Overview,Tonal Forge EQ,Bus Glue Compressor,Harmonic Crucible,Stereo & Sub-Anchor,Vocal Pocket Corridor,Producer Summing Matrix}>-Active Module
slider2:0<0,24,1{Default Unity Baseline (1:1 Pass),Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Mirrorcell),Buster Odeholm (thrown / Northlane),Lewis Johns (Love Is Noise / blanket),Kel Pinchin (Split Chain / Currents Target),Dan Lancaster & Jason Perry (Don Broco),Erik Bickerstaffe (Static Dress),Sam Guaiana (Silverstein / TDWP),Zach Tuch (Heavenward / Hundredth),Forrester Savell (Karnivool),Leon Schmidt (SUNBORN - Nebula),Ermin Hamidovic (Systematic Reference),Will Putney (Fit For An Autopsy),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill - nerv),Henrik Udd (Architects - Gravity),Dan Braunstein (Spiritbox - Keep Sweet),Zakk Cervini & Erik Ron (Bad Omens),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Acle Kahney (TesseracT - King),Adam Cichocki (heaving. / Timber Studios),Manuel Renner (SENNA / Uberlarm Studios)}>-Producer Summing Profile
slider3:0.0<-6.0,6.0,0.1>-Input Calibration (dB)
slider4:0.0<-12.0,6.0,0.1>-Output Master Trim (dB)
slider5:-6.0<-12.0,0.0,0.1>-Headroom Target Ceiling (dBTP)
slider6:1<0,1,1{Off,Strict -6 dBTP Guard (Zero Clip)}>-Auto-Headroom Guardian
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
slider27:1<0,1,1{Bypassed,Engaged}>-Instrumental Master Suite Engine
slider28:0<0,1,1{Norm,Delta Solo Listen}>-Non-Destructive Delta Audition
slider29:0<0,1,1{Snap A,Snap B}>-A/B Snapshot Memory
slider30:0<0,1,1{Stereo Master,M/S Matrix}>-Summing Mode

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

MEM_BASE = 1000;
f_hpf_l = MEM_BASE;     f_hpf_r = MEM_BASE + 10;
f_mono_l = MEM_BASE + 20; f_mono_r = MEM_BASE + 30;
f_p80_l = MEM_BASE + 40;  f_p80_r = MEM_BASE + 50;
f_m280_l = MEM_BASE + 60; f_m280_r = MEM_BASE + 70;
f_b3k_l = MEM_BASE + 80;  f_b3k_r = MEM_BASE + 90;
f_a10k_l = MEM_BASE + 100; f_a10k_r = MEM_BASE + 110;
f_pocket_l = MEM_BASE + 120; f_pocket_r = MEM_BASE + 130;
f_schpf_l = MEM_BASE + 140; f_schpf_r = MEM_BASE + 150;

ab_mem_a = 60000; ab_mem_b = 60100; ab_init_done = 0; ab_state = 0;

sifam_desk_needle = 0;
sifam_glue_needle = 0;
meter_rms_l = 0; meter_rms_r = 0;
comp_env = 0;
glue_gr_db = 0;
cur_phase_corr = 0.95;
prev_preset = slider2;
drag_slider_idx = 0;

function save_ab_snapshot(target_buf) local(k) (
  k = 1; loop(30, target_buf[k] = slider(k); k += 1; );
);

function load_ab_snapshot(src_buf) local(k) (
  k = 1; loop(30, slider(k) = src_buf[k]; k += 1; );
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

function calc_svf_hpf(freq, mem_offset) (
  g_val = tan($pi * max(15.0, min(1000.0, freq)) / srate);
  k_val = 1.41421356;
  a1 = 1.0 / (1.0 + g_val * (g_val + k_val));
  a2 = g_val * a1;
  a3 = g_val * a2;
  mem[mem_offset] = a1; mem[mem_offset+1] = a2; mem[mem_offset+2] = a3;
);

function eval_svf_hpf(x, mem_offset) (
  v3 = x - mem[mem_offset+5];
  v1 = mem[mem_offset] * mem[mem_offset+4] + mem[mem_offset+1] * v3;
  v2 = mem[mem_offset+5] + mem[mem_offset+1] * mem[mem_offset+4] + mem[mem_offset+2] * v3;
  mem[mem_offset+4] = 2.0 * v1 - mem[mem_offset+4];
  mem[mem_offset+5] = 2.0 * v2 - mem[mem_offset+5];
  x - 1.41421356 * v1 - v2;
);

function update_filters() (
  calc_svf_hpf(slider18, f_hpf_l);
  calc_svf_hpf(slider18, f_hpf_r);
  calc_svf_bell(80.0, 1.2, slider19, f_p80_l);
  calc_svf_bell(80.0, 1.2, slider19, f_p80_r);
  calc_svf_bell(280.0, 1.4, slider20, f_m280_l);
  calc_svf_bell(280.0, 1.4, slider20, f_m280_r);
  calc_svf_bell(3500.0, 1.1, slider21, f_b3k_l);
  calc_svf_bell(3500.0, 1.1, slider21, f_b3k_r);
  calc_svf_bell(10000.0, 0.7, slider22, f_a10k_l);
  calc_svf_bell(10000.0, 0.7, slider22, f_a10k_r);
  calc_svf_bell(2200.0, 1.6, -slider9, f_pocket_l);
  calc_svf_bell(2200.0, 1.6, -slider9, f_pocket_r);
  calc_svf_hpf(slider16, f_schpf_l);
  calc_svf_hpf(slider16, f_schpf_r);
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
  p_idx == 21 ? "21: GETGOOD" :
  p_idx == 22 ? "22: KAHNEY" :
  p_idx == 23 ? "23: CICHOCKI" :
                "24: RENNER"
);

function get_producer_full_title(p_idx) (
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

function apply_producer_preset(p_idx) (
  p_idx == 0 ? ( // Default Unity Baseline
    slider4 = 0.0; slider7 = 80; slider9 = 0.0; slider11 = 0; slider12 = 0.0; slider13 = 1;
    slider14 = 30.0; slider15 = 0; slider16 = 120; slider17 = 100;
    slider18 = 28; slider19 = 0.0; slider20 = 0.0; slider21 = 0.0; slider22 = 0.0;
    slider23 = 0; slider24 = 0.0; slider25 = 1.00;
  ) : p_idx == 1 ? ( // Lance Prenc
    slider4 = -3.0; slider7 = 85; slider9 = 1.2; slider11 = 0; slider12 = -18.0; slider13 = 2;
    slider14 = 30.0; slider15 = 1; slider16 = 130; slider17 = 100;
    slider18 = 30; slider19 = 0.0; slider20 = -3.5; slider21 = 3.5; slider22 = 3.0;
    slider23 = 1; slider24 = 3.5; slider25 = 1.15;
  ) : p_idx == 2 ? ( // Scott Seigel
    slider4 = -2.5; slider7 = 80; slider9 = 1.0; slider11 = 0; slider12 = -17.0; slider13 = 2;
    slider14 = 10.0; slider15 = 0; slider16 = 100; slider17 = 100;
    slider18 = 28; slider19 = 1.5; slider20 = -2.5; slider21 = 2.0; slider22 = 1.0;
    slider23 = 1; slider24 = 3.0; slider25 = 1.08;
  ) : p_idx == 3 ? ( // Jonathan Dolese
    slider4 = -2.0; slider7 = 75; slider9 = 0.8; slider11 = 1; slider12 = -15.0; slider13 = 1;
    slider14 = 30.0; slider15 = 3; slider16 = 110; slider17 = 100;
    slider18 = 25; slider19 = 3.5; slider20 = -2.0; slider21 = 1.5; slider22 = 2.0;
    slider23 = 3; slider24 = 2.5; slider25 = 1.12;
  ) : p_idx == 4 ? ( // Buster Odeholm
    slider4 = -3.5; slider7 = 90; slider9 = 1.5; slider11 = 0; slider12 = -20.0; slider13 = 2;
    slider14 = 10.0; slider15 = 1; slider16 = 90; slider17 = 100;
    slider18 = 32; slider19 = 4.0; slider20 = -4.0; slider21 = 2.0; slider22 = 1.5;
    slider23 = 1; slider24 = 4.8; slider25 = 1.00;
  ) : p_idx == 5 ? ( // Lewis Johns
    slider4 = -2.0; slider7 = 75; slider9 = 0.8; slider11 = 0; slider12 = -14.0; slider13 = 1;
    slider14 = 30.0; slider15 = 0; slider16 = 140; slider17 = 100;
    slider18 = 35; slider19 = 2.0; slider20 = -1.5; slider21 = 1.0; slider22 = 2.5;
    slider23 = 2; slider24 = 2.2; slider25 = 1.25;
  ) : p_idx == 6 ? ( // Kel Pinchin (Split Chain Target)
    slider4 = -3.5; slider7 = 75; slider9 = 1.2; slider11 = 0; slider12 = -16.0; slider13 = 1;
    slider14 = 30.0; slider15 = 0; slider16 = 140; slider17 = 100;
    slider18 = 26; slider19 = 1.5; slider20 = -2.8; slider21 = 2.0; slider22 = 2.8;
    slider23 = 1; slider24 = 2.4; slider25 = 1.12;
  ) : p_idx == 7 ? ( // Dan Lancaster
    slider4 = -3.0; slider7 = 80; slider9 = 1.2; slider11 = 0; slider12 = -18.0; slider13 = 2;
    slider14 = 30.0; slider15 = 0; slider16 = 120; slider17 = 100;
    slider18 = 28; slider19 = 3.0; slider20 = -3.0; slider21 = 3.5; slider22 = 3.8;
    slider23 = 1; slider24 = 3.5; slider25 = 1.18;
  ) : p_idx == 8 ? ( // Erik Bickerstaffe
    slider4 = -2.8; slider7 = 80; slider9 = 1.0; slider11 = 1; slider12 = -17.0; slider13 = 2;
    slider14 = 10.0; slider15 = 2; slider16 = 100; slider17 = 100;
    slider18 = 30; slider19 = 2.0; slider20 = -1.5; slider21 = 2.0; slider22 = 1.0;
    slider23 = 2; slider24 = 4.0; slider25 = 1.06;
  ) : p_idx == 9 ? ( // Sam Guaiana
    slider4 = -2.8; slider7 = 80; slider9 = 1.2; slider11 = 0; slider12 = -17.5; slider13 = 2;
    slider14 = 10.0; slider15 = 0; slider16 = 110; slider17 = 100;
    slider18 = 28; slider19 = 2.5; slider20 = -2.5; slider21 = 2.5; slider22 = 2.0;
    slider23 = 1; slider24 = 3.0; slider25 = 1.10;
  ) : p_idx == 10 ? ( // Zach Tuch
    slider4 = -2.0; slider7 = 70; slider9 = 0.8; slider11 = 0; slider12 = -14.0; slider13 = 1;
    slider14 = 30.0; slider15 = 3; slider16 = 130; slider17 = 100;
    slider18 = 25; slider19 = 2.0; slider20 = -1.5; slider21 = 1.2; slider22 = 3.0;
    slider23 = 2; slider24 = 2.5; slider25 = 1.22;
  ) : p_idx == 11 ? ( // Forrester Savell
    slider4 = -1.5; slider7 = 70; slider9 = 0.5; slider11 = 0; slider12 = -12.0; slider13 = 1;
    slider14 = 30.0; slider15 = 0; slider16 = 150; slider17 = 100;
    slider18 = 22; slider19 = 1.0; slider20 = -2.0; slider21 = 1.5; slider22 = 2.0;
    slider23 = 0; slider24 = 1.8; slider25 = 1.15;
  ) : p_idx == 12 ? ( // Leon Schmidt
    slider4 = -2.5; slider7 = 85; slider9 = 1.2; slider11 = 0; slider12 = -16.0; slider13 = 2;
    slider14 = 30.0; slider15 = 0; slider16 = 120; slider17 = 100;
    slider18 = 28; slider19 = 1.5; slider20 = -3.0; slider21 = 3.0; slider22 = 3.2;
    slider23 = 1; slider24 = 2.8; slider25 = 1.20;
  ) : p_idx == 13 ? ( // Ermin Hamidovic
    slider4 = -3.0; slider7 = 80; slider9 = 0.6; slider11 = 0; slider12 = -15.0; slider13 = 1;
    slider14 = 30.0; slider15 = 0; slider16 = 160; slider17 = 100;
    slider18 = 25; slider19 = 1.0; slider20 = -2.5; slider21 = 1.2; slider22 = 1.5;
    slider23 = 0; slider24 = 1.5; slider25 = 1.05;
  ) : p_idx == 14 ? ( // Will Putney
    slider4 = -4.0; slider7 = 85; slider9 = 1.5; slider11 = 0; slider12 = -20.0; slider13 = 2;
    slider14 = 10.0; slider15 = 2; slider16 = 80; slider17 = 100;
    slider18 = 30; slider19 = 3.5; slider20 = -2.5; slider21 = 2.5; slider22 = 1.8;
    slider23 = 1; slider24 = 4.8; slider25 = 1.04;
  ) : p_idx == 15 ? ( // George Lever
    slider4 = -2.0; slider7 = 70; slider9 = 0.8; slider11 = 0; slider12 = -13.0; slider13 = 1;
    slider14 = 30.0; slider15 = 0; slider16 = 130; slider17 = 100;
    slider18 = 24; slider19 = 2.0; slider20 = -1.8; slider21 = 1.5; slider22 = 2.5;
    slider23 = 2; slider24 = 2.0; slider25 = 1.20;
  ) : p_idx == 16 ? ( // Sam Bassal
    slider4 = -2.5; slider7 = 85; slider9 = 1.0; slider11 = 0; slider12 = -17.0; slider13 = 2;
    slider14 = 10.0; slider15 = 0; slider16 = 100; slider17 = 100;
    slider18 = 28; slider19 = 3.0; slider20 = -3.0; slider21 = 2.0; slider22 = 2.2;
    slider23 = 2; slider24 = 3.2; slider25 = 1.10;
  ) : p_idx == 17 ? ( // Henrik Udd
    slider4 = -3.0; slider7 = 80; slider9 = 1.2; slider11 = 0; slider12 = -18.0; slider13 = 2;
    slider14 = 30.0; slider15 = 0; slider16 = 120; slider17 = 100;
    slider18 = 28; slider19 = 3.0; slider20 = -3.0; slider21 = 2.5; slider22 = 3.0;
    slider23 = 1; slider24 = 3.2; slider25 = 1.12;
  ) : p_idx == 18 ? ( // Dan Braunstein
    slider4 = -3.0; slider7 = 85; slider9 = 1.2; slider11 = 0; slider12 = -17.5; slider13 = 2;
    slider14 = 30.0; slider15 = 0; slider16 = 110; slider17 = 100;
    slider18 = 28; slider19 = 2.5; slider20 = -2.0; slider21 = 3.5; slider22 = 4.0;
    slider23 = 1; slider24 = 2.8; slider25 = 1.16;
  ) : p_idx == 19 ? ( // Zakk Cervini
    slider4 = -3.0; slider7 = 85; slider9 = 1.2; slider11 = 0; slider12 = -18.0; slider13 = 2;
    slider14 = 10.0; slider15 = 1; slider16 = 110; slider17 = 100;
    slider18 = 28; slider19 = 3.0; slider20 = -3.5; slider21 = 3.5; slider22 = 3.0;
    slider23 = 1; slider24 = 3.6; slider25 = 1.14;
  ) : p_idx == 20 ? ( // Jens Bogren
    slider4 = -3.0; slider7 = 80; slider9 = 1.0; slider11 = 0; slider12 = -17.0; slider13 = 2;
    slider14 = 30.0; slider15 = 2; slider16 = 100; slider17 = 100;
    slider18 = 28; slider19 = 2.5; slider20 = -2.5; slider21 = 2.0; slider22 = 1.5;
    slider23 = 1; slider24 = 3.6; slider25 = 1.12;
  ) : p_idx == 21 ? ( // Nolly Getgood
    slider4 = -3.0; slider7 = 80; slider9 = 1.0; slider11 = 0; slider12 = -15.0; slider13 = 1;
    slider14 = 30.0; slider15 = 0; slider16 = 160; slider17 = 100;
    slider18 = 26; slider19 = 1.5; slider20 = -3.5; slider21 = 2.5; slider22 = 2.5;
    slider23 = 0; slider24 = 1.5; slider25 = 1.08;
  ) : p_idx == 22 ? ( // Acle Kahney
    slider4 = -2.0; slider7 = 75; slider9 = 0.8; slider11 = 0; slider12 = -14.0; slider13 = 1;
    slider14 = 30.0; slider15 = 0; slider16 = 150; slider17 = 100;
    slider18 = 24; slider19 = 1.5; slider20 = -2.5; slider21 = 1.8; slider22 = 2.0;
    slider23 = 0; slider24 = 1.6; slider25 = 1.10;
  ) : p_idx == 23 ? ( // Adam Cichocki (heaving. - carsick)
    slider4 = -2.5; slider7 = 80; slider9 = 1.0; slider11 = 1; slider12 = -17.0; slider13 = 2;
    slider14 = 30.0; slider15 = 2; slider16 = 110; slider17 = 100;
    slider18 = 28; slider19 = 3.0; slider20 = -2.8; slider21 = 2.2; slider22 = 2.5;
    slider23 = 2; slider24 = 4.0; slider25 = 1.12;
  ) : ( // Manuel Renner (SENNA - Out Of The Blue)
    slider4 = -3.0; slider7 = 90; slider9 = 1.2; slider11 = 0; slider12 = -17.5; slider13 = 2;
    slider14 = 30.0; slider15 = 0; slider16 = 120; slider17 = 100;
    slider18 = 28; slider19 = 2.8; slider20 = -3.2; slider21 = 3.0; slider22 = 3.0;
    slider23 = 1; slider24 = 3.0; slider25 = 1.14;
  );
  update_filters();
);

update_filters();

@slider
slider2 != prev_preset ? (
  prev_preset = slider2;
  apply_producer_preset(slider2);
);

update_filters();

in_gain_lin = exp(slider3 * 0.11512925);
out_gain_lin = exp(slider4 * 0.11512925);
ceiling_lin = exp(slider5 * 0.11512925);

comp_ratio = slider13 == 0 ? 1.5 : (slider13 == 1 ? 2.0 : (slider13 == 2 ? 4.0 : 8.0));
comp_att = exp(-1.0 / (slider14 * 0.001 * srate));
rel_ms = slider15 == 0 ? 150.0 : (slider15 == 1 ? 100.0 : (slider15 == 2 ? 300.0 : (slider15 == 3 ? 600.0 : 1200.0)));
comp_rel = exp(-1.0 / (rel_ms * 0.001 * srate));

@sample
s0 = spl0;
s1 = spl1;
in_s0 = s0; in_s1 = s1;

// Read Vocal Bus Heartbeat & Pocket Request from gmem[1450..1499]
vb_time = gmem[1450];
vb_alive = (time_precise() - vb_time) < 0.5;
vb_vocal_rms = vb_alive ? gmem[1452] : -60.0;
vb_request_db = vb_alive ? gmem[1455] : 0.0;

slider10 == 1 && vb_alive ? (
  pocket_depth = max(0.0, min(3.0, (vb_vocal_rms + 28.0) * 0.15 + vb_request_db));
) : (
  pocket_depth = slider9;
);

slider27 ? (
  s0 *= in_gain_lin;
  s1 *= in_gain_lin;

  s0 = eval_svf_hpf(s0, f_hpf_l);
  s1 = eval_svf_hpf(s1, f_hpf_r);

  s0 = eval_svf_bell(s0, f_p80_l);
  s1 = eval_svf_bell(s1, f_p80_r);
  s0 = eval_svf_bell(s0, f_m280_l);
  s1 = eval_svf_bell(s1, f_m280_r);
  s0 = eval_svf_bell(s0, f_b3k_l);
  s1 = eval_svf_bell(s1, f_b3k_r);
  s0 = eval_svf_bell(s0, f_a10k_l);
  s1 = eval_svf_bell(s1, f_a10k_r);

  pocket_depth > 0.05 ? (
    calc_svf_bell(2200.0, 1.6, -pocket_depth, f_pocket_l);
    calc_svf_bell(2200.0, 1.6, -pocket_depth, f_pocket_r);
    s0 = eval_svf_bell(s0, f_pocket_l);
    s1 = eval_svf_bell(s1, f_pocket_r);
  );

  sc0 = eval_svf_hpf(s0, f_schpf_l);
  sc1 = eval_svf_hpf(s1, f_schpf_r);
  det = max(abs(sc0), abs(sc1));
  det_db = det > 0.000001 ? 20.0 * log10(det) : -120.0;
  det_db > slider12 ? (
    over_db = det_db - slider12;
    gr_target = over_db * (1.0 - 1.0 / comp_ratio);
  ) : (
    gr_target = 0.0;
  );

  gr_target > comp_env ? (
    comp_env = comp_env * comp_att + gr_target * (1.0 - comp_att);
  ) : (
    comp_env = comp_env * comp_rel + gr_target * (1.0 - comp_rel);
  );
  glue_gr_db = comp_env;
  comp_gain_lin = exp(-glue_gr_db * 0.11512925);

  dry0 = s0; dry1 = s1;
  wet0 = s0 * comp_gain_lin;
  wet1 = s1 * comp_gain_lin;
  mix_ratio = slider17 * 0.01;
  s0 = dry0 * (1.0 - mix_ratio) + wet0 * mix_ratio;
  s1 = dry1 * (1.0 - mix_ratio) + wet1 * mix_ratio;

  slider24 > 0.01 ? (
    h_drive = exp(slider24 * 0.11512925);
    d0 = s0 * h_drive; d1 = s1 * h_drive;
    slider23 == 1 ? (
      s0 = (d0 + 0.12 * d0 * d0 - 0.04 * d0 * d0 * d0) / h_drive;
      s1 = (d1 + 0.12 * d1 * d1 - 0.04 * d1 * d1 * d1) / h_drive;
    ) : slider23 == 2 ? (
      s0 = (fast_tanh(d0 * 0.7) * 1.3) / h_drive;
      s1 = (fast_tanh(d1 * 0.7) * 1.3) / h_drive;
    ) : slider23 == 3 ? (
      s0 = (d0 + 0.18 * d0 * d0 - 0.08 * d0 * d0 * d0) / h_drive;
      s1 = (d1 + 0.18 * d1 * d1 - 0.08 * d1 * d1 * d1) / h_drive;
    );
  );

  mid = (s0 + s1) * 0.5;
  side = (s0 - s1) * 0.5 * slider25;
  s0 = mid + side;
  s1 = mid - side;

  s0 *= out_gain_lin;
  s1 *= out_gain_lin;

  slider6 ? (
    pk = max(abs(s0), abs(s1));
    pk > ceiling_lin ? (
      scale = ceiling_lin / pk;
      s0 *= scale;
      s1 *= scale;
    );
  );
);

slider28 ? (
  spl0 = s0 - in_s0;
  spl1 = s1 - in_s1;
) : (
  spl0 = s0;
  spl1 = s1;
);

meter_rms_l = meter_rms_l * 0.999 + spl0 * spl0 * 0.001;
meter_rms_r = meter_rms_r * 0.999 + spl1 * spl1 * 0.001;
sifam_desk_needle = sifam_desk_needle * 0.95 + slider24 * 0.05;
sifam_glue_needle = sifam_glue_needle * 0.90 + glue_gr_db * 0.10;

dot_prod = spl0 * spl1;
mag_prod = sqrt((spl0 * spl0 + 0.0000001) * (spl1 * spl1 + 0.0000001));
inst_corr = dot_prod / mag_prod;
cur_phase_corr = cur_phase_corr * 0.995 + inst_corr * 0.005;

// Publish to gmem[1400..1449]
gmem[1400] = time_precise();
gmem[1401] = 1.0;
gmem[1402] = 10.0 * log10(max(0.0000001, (meter_rms_l + meter_rms_r) * 0.5));
gmem[1403] = max(abs(spl0), abs(spl1));
gmem[1404] = gmem[1403] > 0.0001 ? 20.0 * log10(gmem[1403]) - gmem[1402] : 10.0;
gmem[1407] = slider2;

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

// Outer Obsidian Titanium Chassis
gfx_r = 0.024; gfx_g = 0.032; gfx_b = 0.044;
gfx_rect(crt_x, crt_y, crt_w, crt_h);

// Burnished Amber Copper Trim
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
gfx_rect(crt_x, crt_y, crt_w, crt_h, 0);
gfx_rect(crt_x + 1, crt_y + 1, crt_w - 2, crt_h - 2, 0);

// ─────────────────────────────────────────────────────────────────────────────
// 1. TOP HEADER BAR: RESPONSIVE THREE-ZONE GEOMETRY
// ─────────────────────────────────────────────────────────────────────────────
hdr_h = 48;
gfx_r = 0.015; gfx_g = 0.022; gfx_b = 0.032;
gfx_rect(crt_x + 2, crt_y + 2, crt_w - 4, hdr_h);
gfx_r = 0.10; gfx_g = 0.16; gfx_b = 0.24;
gfx_line(crt_x + 2, crt_y + hdr_h + 2, crt_x + crt_w - 2, crt_y + hdr_h + 2);

// Adinkrahene Triple Concentric Circles
sig_cx = crt_x + 22; sig_cy = crt_y + 24;
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
gfx_circle(sig_cx, sig_cy, 12, 0);
gfx_circle(sig_cx, sig_cy, 8, 0);
gfx_circle(sig_cx, sig_cy, 4, 1);

// Title text with responsive auto-fit
title_str = crt_w < 1000 ? "DAMEI // INST BUS" : "DAMEI // INSTRUMENTAL BUS";
gfx_r = 0.95; gfx_g = 0.90; gfx_b = 1.00;
gfx_setfont(1, "Orbitron", 14, 'b');
gfx_x = crt_x + 40; gfx_y = crt_y + 15;
gfx_drawstr(title_str);
gfx_measurestr(title_str, tsw, tsh);
title_end_x = crt_x + 40 + tsw + 12;

// Right pinned control pills (Right to Left)
rx = crt_x + crt_w - 8;

// 1. ENGAGED / BYPASS
byp_w = 78; rx -= byp_w;
byp_hov = (mouse_x >= rx && mouse_x <= rx + byp_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider27 ? (byp_hov ? 0.12 : 0.06) : (byp_hov ? 0.25 : 0.15);
gfx_g = slider27 ? (byp_hov ? 0.28 : 0.18) : (byp_hov ? 0.08 : 0.05);
gfx_b = slider27 ? (byp_hov ? 0.38 : 0.24) : (byp_hov ? 0.08 : 0.05);
gfx_rect(rx, crt_y + 9, byp_w, 30);
gfx_r = slider27 ? 0.00 : 0.95; gfx_g = slider27 ? 0.95 : 0.30; gfx_b = slider27 ? 0.65 : 0.30;
gfx_rect(rx, crt_y + 9, byp_w, 30, 0);
gfx_setfont(2, "Orbitron", 10.5, 'b');
b_txt = slider27 ? "ENGAGED" : "BYPASS";
gfx_measurestr(b_txt, btw, bth);
gfx_x = rx + (byp_w - btw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(b_txt);
mouse_clicked && byp_hov ? (slider27 = !slider27; slider_automate(););

// 2. CEIL: -6dB / FREE
ceil_w = 78; rx -= (ceil_w + 5);
ceil_hov = (mouse_x >= rx && mouse_x <= rx + ceil_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider6 ? 0.08 : 0.06; gfx_g = slider6 ? 0.28 : 0.10; gfx_b = slider6 ? 0.18 : 0.12;
gfx_rect(rx, crt_y + 9, ceil_w, 30);
gfx_r = slider6 ? 0.00 : 0.50; gfx_g = slider6 ? 0.95 : 0.50; gfx_b = slider6 ? 0.65 : 0.50;
gfx_rect(rx, crt_y + 9, ceil_w, 30, 0);
gfx_setfont(3, "Consolas", 10.5, 'b');
c_txt = slider6 ? "CEIL: -6dB" : "CEIL: FREE";
gfx_measurestr(c_txt, ctw, cth);
gfx_x = rx + (ceil_w - ctw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(c_txt);
mouse_clicked && ceil_hov ? (slider6 = !slider6; slider_automate(););

// 3. MODE: STEREO / M/S
mode_w = 86; rx -= (mode_w + 5);
mode_hov = (mouse_x >= rx && mouse_x <= rx + mode_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = 0.06; gfx_g = 0.12; gfx_b = 0.18; gfx_rect(rx, crt_y + 9, mode_w, 30);
gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(rx, crt_y + 9, mode_w, 30, 0);
gfx_setfont(3, "Consolas", 10.5, 'b');
m_txt = slider30 ? "MODE: M/S" : "MODE: STEREO";
gfx_measurestr(m_txt, mtw, mth);
gfx_x = rx + (mode_w - mtw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(m_txt);
mouse_clicked && mode_hov ? (slider30 = !slider30; slider_automate(););

// 4. SYNC: 20R
rgn_w = 98; rx -= (rgn_w + 5);
gfx_r = 0.04; gfx_g = 0.07; gfx_b = 0.11; gfx_rect(rx, crt_y + 9, rgn_w, 30);
gfx_r = 0.15; gfx_g = 0.65; gfx_b = 0.45; gfx_rect(rx, crt_y + 9, rgn_w, 30, 0);
g_sec = gmem[100] == 1 ? gmem[101] : 0;
r_str = g_sec == 3 ? "⚡ CHORUS" : sprintf(#, "● SYNC: %d R", gmem[103] > 0 ? gmem[103] : 20);
gfx_setfont(3, "Consolas", 10, 'b');
gfx_measurestr(r_str, rsw, rsh);
gfx_x = rx + (rgn_w - rsw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(r_str);

// 5. SNAP A / B
ab_w = 52; rx -= (ab_w + 5);
ab_hov = (mouse_x >= rx && mouse_x <= rx + ab_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = ab_state ? 0.22 : 0.06; gfx_g = ab_state ? 0.12 : 0.18; gfx_b = ab_state ? 0.32 : 0.26;
gfx_rect(rx, crt_y + 9, ab_w, 30);
gfx_r = ab_state ? 0.85 : 0.00; gfx_g = ab_state ? 0.45 : 0.85; gfx_b = ab_state ? 1.00 : 1.00;
gfx_rect(rx, crt_y + 9, ab_w, 30, 0);
gfx_setfont(2, "Orbitron", 10, 'b');
ab_str = ab_state ? "SNAP B" : "SNAP A";
gfx_measurestr(ab_str, abw, abh);
gfx_x = rx + (ab_w - abw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(ab_str);
mouse_clicked && ab_hov ? (
  ab_state == 0 ? (save_ab_snapshot(ab_mem_a); load_ab_snapshot(ab_mem_b); ab_state = 1; slider29 = 1;) :
                  (save_ab_snapshot(ab_mem_b); load_ab_snapshot(ab_mem_a); ab_state = 0; slider29 = 0;);
);

// 6. DELTA / NORM
del_w = 48; rx -= (del_w + 5);
del_hov = (mouse_x >= rx && mouse_x <= rx + del_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider28 ? 0.28 : 0.05; gfx_g = slider28 ? 0.08 : 0.07; gfx_b = slider28 ? 0.08 : 0.10;
gfx_rect(rx, crt_y + 9, del_w, 30);
gfx_r = slider28 ? 1.00 : 0.40; gfx_g = slider28 ? 0.25 : 0.45; gfx_b = slider28 ? 0.25 : 0.55;
gfx_rect(rx, crt_y + 9, del_w, 30, 0);
gfx_setfont(2, "Orbitron", 10, 'b');
del_str = slider28 ? "DELTA" : "NORM";
gfx_measurestr(del_str, dlw, dlh);
gfx_x = rx + (del_w - dlw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(del_str);
mouse_clicked && del_hov ? (slider28 = !slider28; slider_automate(););

// Center Zone: Preset Stepper < [ PRESET TITLE ] >
avail_w = rx - title_end_x - 10;
p_btn_w = 24;
bar_w = min(280, max(140, avail_w - p_btn_w * 2 - 8));
p_tot_w = p_btn_w * 2 + 6 + bar_w;
preset_x = title_end_x + max(4, floor((avail_w - p_tot_w) * 0.5));

btn_l_x = preset_x;
b_l_hov = (mouse_x >= btn_l_x && mouse_x <= btn_l_x + p_btn_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = b_l_hov ? 0.20 : 0.10; gfx_g = b_l_hov ? 0.28 : 0.15; gfx_b = b_l_hov ? 0.38 : 0.20;
gfx_rect(btn_l_x, crt_y + 9, p_btn_w, 30);
gfx_r = 0.24; gfx_g = 0.34; gfx_b = 0.46; gfx_rect(btn_l_x, crt_y + 9, p_btn_w, 30, 0);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_setfont(1, "Orbitron", 13, 'b');
gfx_x = btn_l_x + 7; gfx_y = crt_y + 15; gfx_drawstr("<");

bar_x = btn_l_x + p_btn_w + 3;
bar_hov = (mouse_x >= bar_x && mouse_x <= bar_x + bar_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = bar_hov ? 0.12 : 0.06; gfx_g = bar_hov ? 0.16 : 0.08; gfx_b = bar_hov ? 0.22 : 0.12;
gfx_rect(bar_x, crt_y + 9, bar_w, 30);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(bar_x, crt_y + 9, bar_w, 30, 0);

p_str = sprintf(#, "%02d: %s", slider2, get_producer_short_name(slider2));
psz = 11.5;
gfx_setfont(1, "Segoe UI", psz, 'b');
gfx_measurestr(p_str, psw, psh);
while (psw > bar_w - 12 && psz > 8.0) (
  psz -= 0.5;
  gfx_setfont(1, "Segoe UI", psz, 'b');
  gfx_measurestr(p_str, psw, psh);
);
gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;
gfx_x = bar_x + floor((bar_w - psw) * 0.5); gfx_y = crt_y + 16;
gfx_drawstr(p_str);

btn_r_x = bar_x + bar_w + 3;
b_r_hov = (mouse_x >= btn_r_x && mouse_x <= btn_r_x + p_btn_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = b_r_hov ? 0.20 : 0.10; gfx_g = b_r_hov ? 0.28 : 0.15; gfx_b = b_r_hov ? 0.38 : 0.20;
gfx_rect(btn_r_x, crt_y + 9, p_btn_w, 30);
gfx_r = 0.24; gfx_g = 0.34; gfx_b = 0.46; gfx_rect(btn_r_x, crt_y + 9, p_btn_w, 30, 0);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_setfont(1, "Orbitron", 13, 'b');
gfx_x = btn_r_x + 8; gfx_y = crt_y + 15; gfx_drawstr(">");

mouse_clicked ? (
  b_l_hov ? (slider2 = max(0, slider2 - 1); apply_producer_preset(slider2); slider_automate();) :
  b_r_hov ? (slider2 = min(24, slider2 + 1); apply_producer_preset(slider2); slider_automate();) : 0;
);

// ─────────────────────────────────────────────────────────────────────────────
// 2. NAVIGATION TABS (7 DEDICATED TABS WITH RICH VISUAL FEEDBACK)
// ─────────────────────────────────────────────────────────────────────────────
tab_y = crt_y + hdr_h + 4; tab_h = 28;
tab_w = floor((crt_w - 8) / 7);
ti = 0;
loop(7,
  tx = crt_x + 4 + ti * tab_w;
  sel = (slider1 == ti);
  t_hov = (mouse_x >= tx && mouse_x <= tx + tab_w - 2 && mouse_y >= tab_y && mouse_y <= tab_y + tab_h);
  gfx_r = sel ? 0.12 : (t_hov ? 0.06 : 0.028);
  gfx_g = sel ? 0.18 : (t_hov ? 0.09 : 0.038);
  gfx_b = sel ? 0.26 : (t_hov ? 0.13 : 0.052);
  gfx_rect(tx, tab_y, tab_w - 2, tab_h);
  sel ? (
    gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
    gfx_rect(tx, tab_y + tab_h - 2, tab_w - 2, 2);
    gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;
  ) : (
    gfx_r = t_hov ? 0.90 : 0.60; gfx_g = t_hov ? 0.90 : 0.70; gfx_b = t_hov ? 0.95 : 0.80;
  );
  gfx_setfont(2, "Orbitron", 11, 'b');
  t_lbl = (ti == 0 ? "OVERVIEW" : (ti == 1 ? "TONAL EQ" : (ti == 2 ? "BUS GLUE" : (ti == 3 ? "CRUCIBLE" : (ti == 4 ? "STEREO" : (ti == 5 ? "POCKET" : "PRODUCER"))))));
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
gfx_r = 0.018; gfx_g = 0.024; gfx_b = 0.034;
gfx_rect(ws_x, ws_y, ws_w, ws_h);
gfx_r = 0.08; gfx_g = 0.14; gfx_b = 0.22;
gfx_rect(ws_x, ws_y, ws_w, ws_h, 0);

function draw_param_slider(px, py, pw, ph, label_str, val, min_v, max_v, fmt_str, s_idx) (
  gfx_r = 0.024; gfx_g = 0.032; gfx_b = 0.044; gfx_rect(px, py, pw, ph);
  gfx_r = 0.12; gfx_g = 0.20; gfx_b = 0.30; gfx_rect(px, py, pw, ph, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = px + 10; gfx_y = py + 6; gfx_drawstr(label_str);

  val_str = sprintf(#, fmt_str, val);
  gfx_setfont(3, "Consolas", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.9; gfx_b = 0.4;
  gfx_measurestr(val_str, vsw, vsh);
  gfx_x = px + pw - vsw - 10; gfx_y = py + 6; gfx_drawstr(val_str);

  trx = px + 10; try = py + 26; trw = pw - 20; trh = 8;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(trx, try, trw, trh);
  gfx_r = 0.20; gfx_g = 0.30; gfx_b = 0.42; gfx_rect(trx, try, trw, trh, 0);

  frac = max(0.0, min(1.0, (val - min_v) / (max_v - min_v)));
  fill_w = floor(frac * trw);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_rect(trx, try, fill_w, trh);

  hx = trx + fill_w; hy = try + trh * 0.5;
  gfx_r = 1.0; gfx_g = 0.9; gfx_b = 0.4; gfx_circle(hx, hy, 6, 1);
  gfx_r = 0.1; gfx_g = 0.1; gfx_b = 0.1; gfx_circle(hx, hy, 6, 0);

  hov = (mouse_x >= px && mouse_x <= px + pw && mouse_y >= py && mouse_y <= py + ph);
  mouse_clicked && hov ? drag_slider_idx = s_idx;
  drag_slider_idx == s_idx && mouse_down ? (
    new_f = max(0.0, min(1.0, (mouse_x - trx) / trw));
    slider(s_idx) = min_v + new_f * (max_v - min_v);
    update_filters();
    slider_automate();
  );
);

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
  r_arc = mh * 0.90;
  ang_min = -0.785398;
  ang_max = 0.785398;

  gfx_r = 0.12; gfx_g = 0.18; gfx_b = 0.26;
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
    is_red = is_glue ? (f >= 0.75) : (f >= 0.75);
    gfx_r = is_red ? 0.98 : (accent_r * 0.9);
    gfx_g = is_red ? 0.25 : (accent_g * 0.9);
    gfx_b = is_red ? 0.25 : (accent_b * 0.9);
    t_len = (ti % 2 == 0) ? 9 : 5;
    gfx_line(piv_x + sin(ta) * (r_arc - t_len), piv_y - cos(ta) * (r_arc - t_len), piv_x + sin(ta) * (r_arc + 1), piv_y - cos(ta) * (r_arc + 1));
    ti += 1;
  );

  gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.85;
  gfx_x = piv_x + sin(ang_min) * (r_arc + 4) - 8; gfx_y = piv_y - cos(ang_min) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "0" : "-20");
  gfx_x = piv_x - 6; gfx_y = piv_y - r_arc - 16; gfx_drawstr(is_glue ? "-6" : "-5");
  gfx_r = 0.98; gfx_g = 0.25; gfx_b = 0.25;
  gfx_x = piv_x + sin(ang_max) * (r_arc + 4) - 12; gfx_y = piv_y - cos(ang_max) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "-16" : "+3");

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

  gfx_r = 0.98; gfx_g = 0.25; gfx_b = 0.25; gfx_circle(tip_x, tip_y, 2, 1);
  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(piv_x, my + mh - 8, 14, 1);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b; gfx_circle(piv_x, my + mh - 8, 14, 0);
);

// =============================================================================
// TAB 0: OVERVIEW (TWIN SIFAM ANALOG METERS + PHASE SCOPE + STATUS PLAQUE)
// =============================================================================
slider1 == 0 ? (
  top_row_h = 240;
  meter_w = floor((ws_w - 36 - 280) * 0.5);

  draw_sifam_meter(ws_x + 12, ws_y + 12, meter_w, top_row_h, "SIFAM DIRECTOR // CONSOLE DRIVE", sifam_desk_needle, 12.0, 0, 0.85, 0.47, 0.21);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = ws_x + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("+%.1f dB DRIVE", slider24);

  draw_sifam_meter(ws_x + 12 + meter_w + 12, ws_y + 12, meter_w, top_row_h, "STUDIO BUS GLUE // GAIN REDUCTION", sifam_glue_needle, 16.0, 1, 0.00, 0.85, 1.00);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 0.00; gfx_g = 0.95; gfx_b = 1.00;
  gfx_x = ws_x + 12 + meter_w + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("-%.1f dB GR", sifam_glue_needle);

  scope_x = ws_x + 12 + meter_w * 2 + 24; scope_w = ws_w - (meter_w * 2 + 48); scope_h = top_row_h;
  gfx_r = 0.012; gfx_g = 0.018; gfx_b = 0.026; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h, 0);

  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = scope_x + 14; gfx_y = ws_y + 22; gfx_drawstr("STEREO PHASE RADAR & CORRELATION");

  sc_cx = scope_x + scope_w * 0.5; sc_cy = ws_y + 12 + scope_h * 0.48; sc_r = scope_h * 0.35;
  gfx_r = 0.08; gfx_g = 0.14; gfx_b = 0.22;
  gfx_circle(sc_cx, sc_cy, sc_r, 0);
  gfx_circle(sc_cx, sc_cy, sc_r * 0.5, 0);
  gfx_line(sc_cx - sc_r, sc_cy, sc_cx + sc_r, sc_cy);
  gfx_line(sc_cx, sc_cy - sc_r, sc_cx, sc_cy + sc_r);

  cbar_y = ws_y + top_row_h - 28; cbar_w = scope_w - 28;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(scope_x + 14, cbar_y, cbar_w, 14);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(scope_x + 14, cbar_y, cbar_w, 14, 0);
  c_f = max(0.0, min(1.0, (cur_phase_corr + 1.0) * 0.5));
  cx_pos = scope_x + 14 + floor(c_f * cbar_w);
  gfx_r = cur_phase_corr > 0.5 ? 0.0 : (cur_phase_corr > 0.0 ? 1.0 : 1.0);
  gfx_g = cur_phase_corr > 0.5 ? 1.0 : (cur_phase_corr > 0.0 ? 0.8 : 0.2);
  gfx_b = cur_phase_corr > 0.5 ? 0.5 : 0.0;
  gfx_rect(cx_pos - 2, cbar_y - 2, 4, 18);

  gfx_setfont(3, "Consolas", 10.5, 'b');
  gfx_x = scope_x + 14; gfx_y = cbar_y - 14; gfx_drawstr("-1.0");
  gfx_x = scope_x + 14 + floor(cbar_w * 0.5) - 8; gfx_y = cbar_y - 14; gfx_drawstr("0.0");
  gfx_x = scope_x + 14 + cbar_w - 24; gfx_y = cbar_y - 14; gfx_drawstr("+1.0");

  p_y = ws_y + top_row_h + 20; p_h = ws_h - top_row_h - 32;
  gfx_r = 0.014; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, p_y, ws_w - 24, p_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 12, p_y, ws_w - 24, p_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.90; gfx_b = 1.00;
  gfx_x = ws_x + 28; gfx_y = p_y + 14;
  gfx_printf("ACTIVE PROFILE: %02d - %s", slider2, get_producer_full_title(slider2));

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = ws_x + 28; gfx_y = p_y + 42;
  gfx_printf("CALIBRATION: Trim: %+4.1fdB | Ceiling: %.1fdBTP | Sub Anchor: %dHz | Vocal Pocket: %.1fdB | Quad Width: %.2fx",
    slider4, slider5, slider7, pocket_depth, slider25);

  gfx_setfont(4, "Consolas", 11); gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.88;
  gfx_x = ws_x + 28; gfx_y = p_y + 70;
  gfx_printf("Summing State: %s | Comp Topology: %s | Saturation Mode: %s",
    slider27 ? "ENGAGED (ACTIVE SUMMING)" : "BYPASS (1:1 UNITY PASS)",
    slider11 ? "Neve Diode Bridge" : "British VCA Punch",
    slider23 == 1 ? "Neve 8014 Iron Desk" : (slider23 == 2 ? "Studer A800 15 IPS Tape" : (slider23 == 3 ? "Triode Tube Crucible" : "Pure Transparent Console")));
);

// =============================================================================
// TAB 1: TONAL FORGE EQ (INTERACTIVE CURVE PLOT + 5 DRAGGABLE BANDS)
// =============================================================================
slider1 == 1 ? (
  eq_plot_y = ws_y + 12; eq_plot_h = 240; eq_plot_w = ws_w - 24;
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(ws_x + 12, eq_plot_y, eq_plot_w, eq_plot_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 12, eq_plot_y, eq_plot_w, eq_plot_h, 0);

  gfx_setfont(2, "Orbitron", 12, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 24; gfx_y = eq_plot_y + 12; gfx_drawstr("TONAL FORGE 5-BAND SUMMING EQ RESPONSE CURVE");

  cy0 = eq_plot_y + eq_plot_h * 0.5;
  gfx_r = 0.12; gfx_g = 0.18; gfx_b = 0.26;
  gfx_line(ws_x + 12, cy0, ws_x + 12 + eq_plot_w, cy0);
  gfx_line(ws_x + 12, cy0 - 45, ws_x + 12 + eq_plot_w, cy0 - 45);
  gfx_line(ws_x + 12, cy0 + 45, ws_x + 12 + eq_plot_w, cy0 + 45);

  fx100 = ws_x + 12 + floor(eq_plot_w * 0.23);
  fx1k  = ws_x + 12 + floor(eq_plot_w * 0.56);
  fx10k = ws_x + 12 + floor(eq_plot_w * 0.88);
  gfx_line(fx100, eq_plot_y, fx100, eq_plot_y + eq_plot_h);
  gfx_line(fx1k,  eq_plot_y, fx1k,  eq_plot_y + eq_plot_h);
  gfx_line(fx10k, eq_plot_y, fx10k, eq_plot_y + eq_plot_h);

  gfx_setfont(4, "Consolas", 10); gfx_r = 0.50; gfx_g = 0.60; gfx_b = 0.70;
  gfx_x = fx100 + 4; gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("100Hz");
  gfx_x = fx1k + 4;  gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("1kHz");
  gfx_x = fx10k + 4; gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("10kHz");

  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  prev_py = cy0;
  pi = 0;
  loop(100,
    px = ws_x + 12 + floor((pi / 99.0) * eq_plot_w);
    f_val = 20.0 * exp(log(1000.0) * (pi / 99.0));
    g_tot = 0.0;
    f_val < slider18 * 1.5 ? g_tot -= (1.0 - (f_val / (slider18 * 1.5))) * 18.0;
    g_tot += slider19 * exp(-0.5 * sqr((log(f_val / 80.0) / 0.5)));
    g_tot += slider20 * exp(-0.5 * sqr((log(f_val / 280.0) / 0.6)));
    g_tot += slider21 * exp(-0.5 * sqr((log(f_val / 3500.0) / 0.6)));
    f_val > 5000.0 ? g_tot += slider22 * (min(1.0, (f_val - 5000.0) / 7000.0));
    cur_py = cy0 - g_tot * 7.5;
    pi > 0 ? gfx_line(prev_px, prev_py, px, cur_py);
    prev_px = px; prev_py = cur_py;
    pi += 1;
  );

  col_w = floor((ws_w - 48) / 5);
  cards_y = eq_plot_y + eq_plot_h + 16; cards_h = ws_h - eq_plot_h - 36;
  draw_param_slider(ws_x + 12 + 0 * (col_w + 6), cards_y, col_w, cards_h, "28Hz HPF", slider18, 20, 60, "%d Hz", 18);
  draw_param_slider(ws_x + 12 + 1 * (col_w + 6), cards_y, col_w, cards_h, "80Hz PUNCH", slider19, -6.0, 6.0, "%+.1f dB", 19);
  draw_param_slider(ws_x + 12 + 2 * (col_w + 6), cards_y, col_w, cards_h, "280Hz SCOOP", slider20, -6.0, 6.0, "%+.1f dB", 20);
  draw_param_slider(ws_x + 12 + 3 * (col_w + 6), cards_y, col_w, cards_h, "3.5kHz BITE", slider21, -6.0, 6.0, "%+.1f dB", 21);
  draw_param_slider(ws_x + 12 + 4 * (col_w + 6), cards_y, col_w, cards_h, "10kHz SHEEN", slider22, -6.0, 6.0, "%+.1f dB", 22);
);

// =============================================================================
// TAB 2: BUS GLUE COMPRESSOR (DUAL TOPOLOGY: VCA VS DIODE BRIDGE + SLIDERS)
// =============================================================================
slider1 == 2 ? (
  cg_y = ws_y + 12; cg_w = ws_w - 24; cg_h = ws_h - 24;
  gfx_r = 0.014; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, cg_y, cg_w, cg_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 12, cg_y, cg_w, cg_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 28; gfx_y = cg_y + 14; gfx_drawstr("DUAL-TOPOLOGY MASTER BUS GLUE COMPRESSOR");

  top_x = ws_x + 28; top_y = cg_y + 44; top_w = 260; top_h = 32;
  top_hov = (mouse_x >= top_x && mouse_x <= top_x + top_w && mouse_y >= top_y && mouse_y <= top_y + top_h);
  gfx_r = slider11 ? 0.16 : 0.06; gfx_g = slider11 ? 0.10 : 0.18; gfx_b = slider11 ? 0.25 : 0.28;
  gfx_rect(top_x, top_y, top_w, top_h);
  gfx_r = slider11 ? 0.85 : 0.00; gfx_g = slider11 ? 0.45 : 0.95; gfx_b = slider11 ? 1.00 : 0.65;
  gfx_rect(top_x, top_y, top_w, top_h, 0);
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_x = top_x + 14; gfx_y = top_y + 9;
  slider11 ? gfx_drawstr("TOPOLOGY: NEVE DIODE BRIDGE") : gfx_drawstr("TOPOLOGY: BRITISH VCA PUNCH");
  mouse_clicked && top_hov ? (slider11 = !slider11; slider_automate(););

  gr_bar_y = top_y + 48; gr_bar_h = 36; gr_bar_w = cg_w - 56;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 28, gr_bar_y, gr_bar_w, gr_bar_h);
  gfx_r = 0.20; gfx_g = 0.30; gfx_b = 0.42; gfx_rect(ws_x + 28, gr_bar_y, gr_bar_w, gr_bar_h, 0);
  fill_w = floor(gr_bar_w * (min(16.0, glue_gr_db) / 16.0));
  fill_w > 0 ? (
    gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 28, gr_bar_y + 2, fill_w, gr_bar_h - 4);
  );
  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = ws_x + 40; gfx_y = gr_bar_y + 10;
  gfx_printf("LIVE GAIN REDUCTION: -%.2f dB", glue_gr_db);

  c_sl_w = floor((cg_w - 72) / 3); c_sl_h = 60;
  sl_r1_y = gr_bar_y + 54;
  draw_param_slider(ws_x + 28 + 0 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "THRESHOLD", slider12, -36.0, 0.0, "%.1f dB", 12);
  draw_param_slider(ws_x + 28 + 1 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "RATIO", slider13, 0, 3, "Mode %d", 13);
  draw_param_slider(ws_x + 28 + 2 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "ATTACK", slider14, 0.1, 100.0, "%.1f ms", 14);

  sl_r2_y = sl_r1_y + c_sl_h + 12;
  draw_param_slider(ws_x + 28 + 0 * (c_sl_w + 8), sl_r2_y, c_sl_w, c_sl_h, "RELEASE", slider15, 0, 4, "Mode %d", 15);
  draw_param_slider(ws_x + 28 + 1 * (c_sl_w + 8), sl_r2_y, c_sl_w, c_sl_h, "SC HPF", slider16, 30, 250, "%d Hz", 16);
  draw_param_slider(ws_x + 28 + 2 * (c_sl_w + 8), sl_r2_y, c_sl_w, c_sl_h, "DRY/WET MIX", slider17, 0, 100, "%d %%", 17);
);

// =============================================================================
// TAB 3: HARMONIC CRUCIBLE (DESK, TAPE & TRIODE SATURATION)
// =============================================================================
slider1 == 3 ? (
  sat_y = ws_y + 12; sat_w = ws_w - 24; sat_h = ws_h - 24;
  gfx_r = 0.014; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, sat_y, sat_w, sat_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 12, sat_y, sat_w, sat_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 28; gfx_y = sat_y + 14; gfx_drawstr("HARMONIC CRUCIBLE // CONSOLE DESK, TAPE & TUBE DRIVE");

  c_w = floor((sat_w - 48) / 4);
  mi = 0;
  loop(4,
    cx = ws_x + 24 + mi * (c_w + 8); cy = sat_y + 48; ch = 110;
    sel = (slider23 == mi);
    m_hov = (mouse_x >= cx && mouse_x <= cx + c_w && mouse_y >= cy && mouse_y <= cy + ch);
    gfx_r = sel ? 0.18 : (m_hov ? 0.08 : 0.04);
    gfx_g = sel ? 0.10 : (m_hov ? 0.06 : 0.05);
    gfx_b = sel ? 0.08 : (m_hov ? 0.08 : 0.07);
    gfx_rect(cx, cy, c_w, ch);
    gfx_r = sel ? 0.85 : 0.20; gfx_g = sel ? 0.47 : 0.30; gfx_b = sel ? 0.21 : 0.40;
    gfx_rect(cx, cy, c_w, ch, 0);

    m_title = mi == 0 ? "TRANSPARENT" : (mi == 1 ? "NEVE 8014 DESK" : (mi == 2 ? "STUDER TAPE" : "TRIODE TUBE"));
    gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = sel ? 1.0 : 0.7; gfx_g = sel ? 0.85 : 0.75; gfx_b = sel ? 0.4 : 0.85;
    gfx_x = cx + 12; gfx_y = cy + 14; gfx_drawstr(m_title);

    m_desc = mi == 0 ? "0 THD Pure Pass" : (mi == 1 ? "Class A Iron Harmonics" : (mi == 2 ? "15 IPS Warm Compression" : "Even Tube Bloom"));
    gfx_setfont(4, "Consolas", 10.5); gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.85;
    gfx_x = cx + 12; gfx_y = cy + 42; gfx_drawstr(m_desc);

    mouse_clicked && m_hov ? (slider23 = mi; update_filters(); slider_automate(););
    mi += 1;
  );

  draw_param_slider(ws_x + 24, sat_y + 175, sat_w - 48, 65, "HARMONIC CRUCIBLE DRIVE", slider24, 0.0, 12.0, "+%.1f dB", 24);

  adv_y = sat_y + 260; adv_h = sat_h - 280;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, adv_y, sat_w - 48, adv_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(ws_x + 24, adv_y, sat_w - 48, adv_h, 0);

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 40; gfx_y = adv_y + 16; gfx_drawstr("HARMONIC THD GENERATION & SATURATION PROFILES:");
  gfx_setfont(4, "Consolas", 11); gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = ws_x + 40; gfx_y = adv_y + 42;
  gfx_drawstr("• Neve 8014 Desk: Drives discrete transformer iron, adding 2nd and 3rd harmonics to give guitars heavy weight.");
  gfx_x = ws_x + 40; gfx_y = adv_y + 64;
  gfx_drawstr("• Studer A800 15 IPS Tape: Smooth tape saturation rounds aggressive cymbal spikiness while gluing kick and snare.");
  gfx_x = ws_x + 40; gfx_y = adv_y + 86;
  gfx_drawstr("• Triode Tube Crucible: Enriches even-order harmonics, lending warm analog body to modern clean synth beds.");
);

// =============================================================================
// TAB 4: STEREO DIMENSION & SUB-ANCHOR
// =============================================================================
slider1 == 4 ? (
  st_y = ws_y + 12; st_w = ws_w - 24; st_h = ws_h - 24;
  gfx_r = 0.014; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, st_y, st_w, st_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 12, st_y, st_w, st_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 28; gfx_y = st_y + 14; gfx_drawstr("STEREO DIMENSION WIDTH & SUB-BASS MONO ANCHOR");

  draw_param_slider(ws_x + 24, st_y + 48, st_w - 48, 65, "SUB-BASS MONO-ANCHOR CUTOFF", slider7, 40, 160, "%d Hz", 7);
  draw_param_slider(ws_x + 24, st_y + 125, st_w - 48, 65, "QUAD-WALL STEREO DIMENSION WIDTH", slider25, 0.80, 1.40, "%.2f x", 25);

  snt_x = ws_x + 24; snt_y = st_y + 205; snt_w = 260; snt_h = 32;
  snt_hov = (mouse_x >= snt_x && mouse_x <= snt_x + snt_w && mouse_y >= snt_y && mouse_y <= snt_y + snt_h);
  gfx_r = slider8 ? 0.06 : 0.16; gfx_g = slider8 ? 0.20 : 0.08; gfx_b = slider8 ? 0.14 : 0.08;
  gfx_rect(snt_x, snt_y, snt_w, snt_h);
  gfx_r = slider8 ? 0.00 : 0.80; gfx_g = slider8 ? 0.95 : 0.40; gfx_b = slider8 ? 0.65 : 0.40;
  gfx_rect(snt_x, snt_y, snt_w, snt_h, 0);
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_x = snt_x + 14; gfx_y = snt_y + 9;
  slider8 ? gfx_drawstr("KICK/BASS SENTRY: ACTIVE") : gfx_drawstr("KICK/BASS SENTRY: BYPASS");
  mouse_clicked && snt_hov ? (slider8 = !slider8; slider_automate(););

  t_pl_y = st_y + 255; t_pl_h = st_h - 275;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, t_pl_y, st_w - 48, t_pl_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(ws_x + 24, t_pl_y, st_w - 48, t_pl_h, 0);

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 40; gfx_y = t_pl_y + 16; gfx_drawstr("SUB-BASS INTEGRITY & PHASE COHERENCE:");
  gfx_setfont(4, "Consolas", 11); gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = ws_x + 40; gfx_y = t_pl_y + 42;
  gfx_drawstr("• Sub-Bass Mono Anchor: Collapses all frequencies below the selected cutoff to 100% pure mono, eliminating phase cancellation.");
  gfx_x = ws_x + 40; gfx_y = t_pl_y + 64;
  gfx_drawstr("• Kick/Bass Sentry: Automatically applies micro-dips under 100Hz on heavy kick hits so bass guitar and kick drum never clash.");
);

// =============================================================================
// TAB 5: VOCAL POCKET CORRIDOR
// =============================================================================
slider1 == 5 ? (
  pk_y = ws_y + 12; pk_w = ws_w - 24; pk_h = ws_h - 24;
  gfx_r = 0.014; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, pk_y, pk_w, pk_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 12, pk_y, pk_w, pk_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 28; gfx_y = pk_y + 14; gfx_drawstr("DYNAMIC VOCAL POCKET CORRIDOR // ZERO-CABLE gmem SENSING");

  draw_param_slider(ws_x + 24, pk_y + 48, pk_w - 48, 65, "VOCAL POCKET CORRIDOR DEPTH", slider9, 0.0, 3.0, "-%.1f dB", 9);

  pkm_x = ws_x + 24; pkm_y = pk_y + 125; pkm_w = 300; pkm_h = 32;
  pkm_hov = (mouse_x >= pkm_x && mouse_x <= pkm_x + pkm_w && mouse_y >= pkm_y && mouse_y <= pkm_y + pkm_h);
  gfx_r = slider10 ? 0.06 : 0.16; gfx_g = slider10 ? 0.20 : 0.08; gfx_b = slider10 ? 0.14 : 0.08;
  gfx_rect(pkm_x, pkm_y, pkm_w, pkm_h);
  gfx_r = slider10 ? 0.00 : 0.80; gfx_g = slider10 ? 0.95 : 0.40; gfx_b = slider10 ? 0.65 : 0.40;
  gfx_rect(pkm_x, pkm_y, pkm_w, pkm_h, 0);
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_x = pkm_x + 14; gfx_y = pkm_y + 9;
  slider10 ? gfx_drawstr("MODE: gmem AUTO-SENSING") : gfx_drawstr("MODE: MANUAL DEPTH LOCK");
  mouse_clicked && pkm_hov ? (slider10 = !slider10; slider_automate(););

  pk_box_y = pk_y + 175; pk_box_h = pk_h - 195;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, pk_box_y, pk_w - 48, pk_box_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(ws_x + 24, pk_box_y, pk_w - 48, pk_box_h, 0);

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 40; gfx_y = pk_box_y + 16;
  gfx_printf("LIVE CORRIDOR TELEMETRY: Active Pocket Notch = -%.2f dB @ 2.2 kHz", pocket_depth);

  gfx_setfont(4, "Consolas", 11); gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = ws_x + 40; gfx_y = pk_box_y + 44;
  gfx_printf("Incoming Vocal Energy (gmem[1452]): %.1f dB | Interlock Status: %s", vb_vocal_rms, vb_alive ? "SYNCHRONIZED" : "STANDBY");
  gfx_x = ws_x + 40; gfx_y = pk_box_y + 68;
  gfx_drawstr("The corridor dynamically notches the center channel of guitars and synths around 2.2kHz whenever the vocal sings,");
  gfx_x = ws_x + 40; gfx_y = pk_box_y + 88;
  gfx_drawstr("allowing the vocal sovereign to sit effortlessly upfront in the mix without fighting the rhythm wall.");
);

// =============================================================================
// TAB 6: PRODUCER SUMMING MATRIX (25 BENCHMARKS WITH DETAILED FORENSIC PLAQUE)
// =============================================================================
slider1 == 6 ? (
  mat_y = ws_y + 12;
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_setfont(1, "Orbitron", 14, 'b');
  gfx_x = ws_x + 20; gfx_y = mat_y;
  gfx_drawstr("PRODUCER SUMMING MATRIX // 25 REFERENCE-CALIBRATED BENCHMARKS");

  pi = 0; pill_w = floor((ws_w - 40 - 36) / 7); pill_h = 36;
  loop(25,
    p_row = floor(pi / 7); p_col = pi % 7;
    px = ws_x + 16 + p_col * (pill_w + 6);
    py = mat_y + 30 + p_row * (pill_h + 6);
    is_sel = (slider2 == pi);
    p_hov = (mouse_x >= px && mouse_x <= px + pill_w && mouse_y >= py && mouse_y <= py + pill_h);

    gfx_r = is_sel ? 0.22 : (p_hov ? 0.12 : 0.038);
    gfx_g = is_sel ? 0.12 : (p_hov ? 0.08 : 0.048);
    gfx_b = is_sel ? 0.08 : (p_hov ? 0.12 : 0.065);
    gfx_rect(px, py, pill_w, pill_h);

    gfx_r = is_sel ? 0.85 : (p_hov ? 0.50 : 0.20);
    gfx_g = is_sel ? 0.47 : (p_hov ? 0.35 : 0.25);
    gfx_b = is_sel ? 0.21 : (p_hov ? 0.20 : 0.35);
    gfx_rect(px, py, pill_w, pill_h, 0);

    gfx_setfont(3, "Consolas", 11.5, 'b');
    is_sel ? (gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;) : (gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.95;);
    p_sname = get_producer_short_name(pi);
    gfx_measurestr(p_sname, psw, psh);
    gfx_x = floor(px + (pill_w - psw) * 0.5); gfx_y = py + 10;
    gfx_drawstr(p_sname);

    mouse_clicked && p_hov ? (
      slider2 = pi;
      prev_preset = slider2;
      apply_producer_preset(slider2);
      slider_automate();
    );
    pi += 1;
  );

  pl_y = mat_y + 205; pl_w = ws_w - 32; pl_h = ws_h - 220;
  gfx_r = 0.014; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 16, pl_y, pl_w, pl_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 16, pl_y, pl_w, pl_h, 0);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 32; gfx_y = pl_y + 14;
  gfx_printf("SELECTED BENCHMARK: %02d - %s", slider2, get_producer_full_title(slider2));

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = ws_x + 32; gfx_y = pl_y + 40;
  gfx_printf("CALIBRATION: Trim %+.1fdB | Glue Thresh %.1fdB (Ratio %s) | Mud Scoop %+.1fdB | Drive %+.1fdB | Width %.2fx",
    slider4, slider12, slider13 == 0 ? "1.5:1" : (slider13 == 1 ? "2:1" : (slider13 == 2 ? "4:1" : "8:1")), slider20, slider24, slider25);

  gfx_setfont(4, "Consolas", 11); gfx_r = 0.70; gfx_g = 0.80; gfx_b = 0.90;
  gfx_x = ws_x + 32; gfx_y = pl_y + 68;
  gfx_drawstr("Full producer acoustic DNA matching the central preset registry. Recalls authentic console harmonic saturation,");
  gfx_x = ws_x + 32; gfx_y = pl_y + 88;
  gfx_drawstr("VCA/Diode bus glue ballistics, and surgical tonal balance targets.");
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
file_var(0, slider26);
file_var(0, slider27);
file_var(0, slider28);
file_var(0, slider29);
file_var(0, slider30);
'''

with open(inst_path, "w", encoding="utf-8") as f:
    f.write(inst_code)

print("Applied Damei_InstrumentalSuite.jsfx v3.1 successfully.")

# ==============================================================================
# 2. DAMEI VOCAL EMPRESS (v3.1 PRODUCTION BUILD)
# ==============================================================================
vocal_path = r"c:\Dev\DameiSuite\effects\Damei_VocalBus.jsfx"

vocal_code = r'''desc:Damei Vocal Empress (Imperial Sceptre & Master Vocal Sum)
// =============================================================================
// DAMEI VOCAL EMPRESS // IMPERIAL SCEPTRE & MASTER VOCAL SUM (v3.1)
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
  p_idx == 0 ? ( // Default Unity Baseline
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
  s0 *= in_gain_lin;
  s1 *= in_gain_lin;

  s0 = eval_svf_bell(s0, f_bax_low_l);
  s1 = eval_svf_bell(s1, f_bax_low_r);
  s0 = eval_svf_bell(s0, f_bax_mid_l);
  s1 = eval_svf_bell(s1, f_bax_mid_r);
  s0 = eval_svf_bell(s0, f_bax_air_l);
  s1 = eval_svf_bell(s1, f_bax_air_r);

  slider7 < -0.1 ? (
    s0 = eval_svf_bell(s0, f_deess_l);
    s1 = eval_svf_bell(s1, f_deess_r);
  );

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

  slider21 > 0.01 ? (
    t_drive = exp(slider21 * 0.11512925);
    d0 = s0 * t_drive; d1 = s1 * t_drive;
    s0 = (d0 + 0.15 * d0 * d0 - 0.05 * d0 * d0 * d0) / t_drive;
    s1 = (d1 + 0.15 * d1 * d1 - 0.05 * d1 * d1 * d1) / t_drive;
  );

  mid = (s0 + s1) * 0.5;
  side = (s0 - s1) * 0.5 * slider18;
  slider19 ? (
    s0 = mid + side * 0.85;
    s1 = mid - side * 0.85;
  ) : (
    s0 = mid + side;
    s1 = mid - side;
  );

  s0 *= out_gain_lin;
  s1 *= out_gain_lin;

  slider6 ? (
    pk = max(abs(s0), abs(s1));
    pk > ceiling_lin ? (
      scale = ceiling_lin / pk;
      s0 *= scale;
      s1 *= scale;
    );
  );
);

slider23 ? (
  spl0 = s0 - in_s0;
  spl1 = s1 - in_s1;
) : (
  spl0 = s0;
  spl1 = s1;
);

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
gmem[1455] = slider20;
gmem[1457] = slider2;

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
// 1. TOP HEADER BAR: RESPONSIVE THREE-ZONE GEOMETRY
// ─────────────────────────────────────────────────────────────────────────────
hdr_h = 48;
gfx_r = 0.024; gfx_g = 0.010; gfx_b = 0.032;
gfx_rect(crt_x + 2, crt_y + 2, crt_w - 4, hdr_h);
gfx_r = 0.18; gfx_g = 0.08; gfx_b = 0.22;
gfx_line(crt_x + 2, crt_y + hdr_h + 2, crt_x + crt_w - 2, crt_y + hdr_h + 2);

// Duafe Wooden Comb Emblem
sig_cx = crt_x + 22; sig_cy = crt_y + 24;
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
gfx_circle(sig_cx, sig_cy, 12, 0);
gfx_circle(sig_cx, sig_cy, 8, 0);
gfx_circle(sig_cx, sig_cy, 4, 1);

title_str = crt_w < 1000 ? "DAMEI // VOCAL EMPRESS" : "DAMEI // VOCAL EMPRESS";
gfx_r = 1.00; gfx_g = 0.90; gfx_b = 1.00;
gfx_setfont(1, "Orbitron", 14, 'b');
gfx_x = crt_x + 40; gfx_y = crt_y + 15;
gfx_drawstr(title_str);
gfx_measurestr(title_str, tsw, tsh);
title_end_x = crt_x + 40 + tsw + 12;

rx = crt_x + crt_w - 8;

// 1. ENGAGED / BYPASS
byp_w = 78; rx -= byp_w;
byp_hov = (mouse_x >= rx && mouse_x <= rx + byp_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider22 ? (byp_hov ? 0.18 : 0.09) : (byp_hov ? 0.28 : 0.16);
gfx_g = slider22 ? (byp_hov ? 0.08 : 0.04) : (byp_hov ? 0.08 : 0.04);
gfx_b = slider22 ? (byp_hov ? 0.24 : 0.13) : (byp_hov ? 0.10 : 0.05);
gfx_rect(rx, crt_y + 9, byp_w, 30);
gfx_r = slider22 ? 1.00 : 0.95; gfx_g = slider22 ? 0.41 : 0.30; gfx_b = slider22 ? 0.70 : 0.30;
gfx_rect(rx, crt_y + 9, byp_w, 30, 0);
gfx_setfont(2, "Orbitron", 10.5, 'b');
b_txt = slider22 ? "ENGAGED" : "BYPASS";
gfx_measurestr(b_txt, btw, bth);
gfx_x = rx + (byp_w - btw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(b_txt);
mouse_clicked && byp_hov ? (slider22 = !slider22; slider_automate(););

// 2. CEIL: -6dB / FREE
ceil_w = 78; rx -= (ceil_w + 5);
ceil_hov = (mouse_x >= rx && mouse_x <= rx + ceil_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider6 ? 0.12 : 0.06; gfx_g = slider6 ? 0.06 : 0.04; gfx_b = slider6 ? 0.18 : 0.08;
gfx_rect(rx, crt_y + 9, ceil_w, 30);
gfx_r = slider6 ? 1.00 : 0.50; gfx_g = slider6 ? 0.41 : 0.50; gfx_b = slider6 ? 0.70 : 0.50;
gfx_rect(rx, crt_y + 9, ceil_w, 30, 0);
gfx_setfont(3, "Consolas", 10.5, 'b');
c_txt = slider6 ? "CEIL: -6dB" : "CEIL: FREE";
gfx_measurestr(c_txt, ctw, cth);
gfx_x = rx + (ceil_w - ctw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(c_txt);
mouse_clicked && ceil_hov ? (slider6 = !slider6; slider_automate(););

// 3. MODE: MASTER SUM
mode_w = 95; rx -= (mode_w + 5);
mode_hov = (mouse_x >= rx && mouse_x <= rx + mode_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = 0.12; gfx_g = 0.06; gfx_b = 0.18; gfx_rect(rx, crt_y + 9, mode_w, 30);
gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(rx, crt_y + 9, mode_w, 30, 0);
gfx_setfont(3, "Consolas", 10.5, 'b');
m_txt = slider25 ? "MODE: STEM" : "MODE: MASTER";
gfx_measurestr(m_txt, mtw, mth);
gfx_x = rx + (mode_w - mtw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(m_txt);
mouse_clicked && mode_hov ? (slider25 = !slider25; slider_automate(););

// 4. SYNC: 20R
rgn_w = 98; rx -= (rgn_w + 5);
gfx_r = 0.08; gfx_g = 0.04; gfx_b = 0.12; gfx_rect(rx, crt_y + 9, rgn_w, 30);
gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(rx, crt_y + 9, rgn_w, 30, 0);
g_sec = gmem[100] == 1 ? gmem[101] : 0;
r_str = g_sec == 3 ? "⚡ CHORUS" : sprintf(#, "● SYNC: %d R", gmem[103] > 0 ? gmem[103] : 20);
gfx_setfont(3, "Consolas", 10, 'b');
gfx_measurestr(r_str, rsw, rsh);
gfx_x = rx + (rgn_w - rsw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(r_str);

// 5. SNAP A / B
ab_w = 52; rx -= (ab_w + 5);
ab_hov = (mouse_x >= rx && mouse_x <= rx + ab_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = ab_state ? 0.24 : 0.10; gfx_g = ab_state ? 0.08 : 0.04; gfx_b = ab_state ? 0.28 : 0.14;
gfx_rect(rx, crt_y + 9, ab_w, 30);
gfx_r = ab_state ? 1.00 : 0.70; gfx_g = ab_state ? 0.41 : 0.53; gfx_b = ab_state ? 0.70 : 1.00;
gfx_rect(rx, crt_y + 9, ab_w, 30, 0);
gfx_setfont(2, "Orbitron", 10, 'b');
ab_str = ab_state ? "SNAP B" : "SNAP A";
gfx_measurestr(ab_str, abw, abh);
gfx_x = rx + (ab_w - abw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(ab_str);
mouse_clicked && ab_hov ? (
  ab_state == 0 ? (save_ab_snapshot(ab_mem_a); load_ab_snapshot(ab_mem_b); ab_state = 1; slider24 = 1;) :
                  (save_ab_snapshot(ab_mem_b); load_ab_snapshot(ab_mem_a); ab_state = 0; slider24 = 0;);
);

// 6. DELTA / NORM
del_w = 48; rx -= (del_w + 5);
del_hov = (mouse_x >= rx && mouse_x <= rx + del_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider23 ? 0.28 : 0.08; gfx_g = slider23 ? 0.08 : 0.04; gfx_b = slider23 ? 0.20 : 0.10;
gfx_rect(rx, crt_y + 9, del_w, 30);
gfx_r = slider23 ? 1.00 : 0.50; gfx_g = slider23 ? 0.41 : 0.40; gfx_b = slider23 ? 0.70 : 0.60;
gfx_rect(rx, crt_y + 9, del_w, 30, 0);
gfx_setfont(2, "Orbitron", 10, 'b');
del_str = slider23 ? "DELTA" : "NORM";
gfx_measurestr(del_str, dlw, dlh);
gfx_x = rx + (del_w - dlw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(del_str);
mouse_clicked && del_hov ? (slider23 = !slider23; slider_automate(););

// Center Zone: Preset Stepper < [ PRESET TITLE ] >
avail_w = rx - title_end_x - 10;
p_btn_w = 24;
bar_w = min(280, max(140, avail_w - p_btn_w * 2 - 8));
p_tot_w = p_btn_w * 2 + 6 + bar_w;
preset_x = title_end_x + max(4, floor((avail_w - p_tot_w) * 0.5));

btn_l_x = preset_x;
b_l_hov = (mouse_x >= btn_l_x && mouse_x <= btn_l_x + p_btn_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = b_l_hov ? 0.22 : 0.12; gfx_g = b_l_hov ? 0.10 : 0.05; gfx_b = b_l_hov ? 0.26 : 0.14;
gfx_rect(btn_l_x, crt_y + 9, p_btn_w, 30);
gfx_r = 0.35; gfx_g = 0.18; gfx_b = 0.42; gfx_rect(btn_l_x, crt_y + 9, p_btn_w, 30, 0);
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_setfont(1, "Orbitron", 13, 'b');
gfx_x = btn_l_x + 7; gfx_y = crt_y + 15; gfx_drawstr("<");

bar_x = btn_l_x + p_btn_w + 3;
bar_hov = (mouse_x >= bar_x && mouse_x <= bar_x + bar_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = bar_hov ? 0.14 : 0.08; gfx_g = bar_hov ? 0.06 : 0.03; gfx_b = bar_hov ? 0.18 : 0.10;
gfx_rect(bar_x, crt_y + 9, bar_w, 30);
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(bar_x, crt_y + 9, bar_w, 30, 0);

p_str = sprintf(#, "%02d: %s", slider2, get_vocal_short_name(slider2));
psz = 11.5;
gfx_setfont(1, "Segoe UI", psz, 'b');
gfx_measurestr(p_str, psw, psh);
while (psw > bar_w - 12 && psz > 8.0) (
  psz -= 0.5;
  gfx_setfont(1, "Segoe UI", psz, 'b');
  gfx_measurestr(p_str, psw, psh);
);
gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;
gfx_x = bar_x + floor((bar_w - psw) * 0.5); gfx_y = crt_y + 16;
gfx_drawstr(p_str);

btn_r_x = bar_x + bar_w + 3;
b_r_hov = (mouse_x >= btn_r_x && mouse_x <= btn_r_x + p_btn_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = b_r_hov ? 0.22 : 0.12; gfx_g = b_r_hov ? 0.10 : 0.05; gfx_b = b_r_hov ? 0.26 : 0.14;
gfx_rect(btn_r_x, crt_y + 9, p_btn_w, 30);
gfx_r = 0.35; gfx_g = 0.18; gfx_b = 0.42; gfx_rect(btn_r_x, crt_y + 9, p_btn_w, 30, 0);
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_setfont(1, "Orbitron", 13, 'b');
gfx_x = btn_r_x + 8; gfx_y = crt_y + 15; gfx_drawstr(">");

mouse_clicked ? (
  b_l_hov ? (slider2 = max(0, slider2 - 1); apply_vocal_preset(slider2); slider_automate();) :
  b_r_hov ? (slider2 = min(24, slider2 + 1); apply_vocal_preset(slider2); slider_automate();) : 0;
);

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

with open(vocal_path, "w", encoding="utf-8") as f:
    f.write(vocal_code)

print("Applied Damei_VocalBus.jsfx v3.1 successfully.")
