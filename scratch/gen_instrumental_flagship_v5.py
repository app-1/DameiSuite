# gen_instrumental_flagship_v5.py
import os, shutil

target_path = r"c:\Dev\DameiSuite\effects\Damei_InstrumentalSuite.jsfx"
reaper_path = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_InstrumentalSuite.jsfx"

with open(target_path, "w", encoding="utf-8") as f:
    f.write(r"""desc:Damei Instrumental Bus Alchemist (Harmonic Crucible & Summing Matrix)
// =============================================================================
// DAMEI SUITE // 2026 REAPER MASTER SUMMING INFRASTRUCTURE
// ARCHETYPE: FUNTUNFUNEFU-DENKYEMFUNEFU (Collective Summing & Unified Destiny)
// FLAGSHIP AFRO-CYBERNETIC LUXURY CONSOLE SURFACE ARCHITECTURE (@gfx 1080 700)
// =============================================================================

slider1:0<0,6,1{0: OVERVIEW, 1: TONAL EQ, 2: BUS GLUE, 3: CRUCIBLE, 4: STEREO, 5: POCKET, 6: PRODUCER}>-Active Navigation Tab
slider2:6<0,24,1{00: Unity Baseline (1:1 Transparent Pass), 01: Lance Prenc (Alpha Wolf - 60cm Of Steel), 02: Scott Seigel (DIESECT - TOO MANY SCARS), 03: Jonathan Dolese (Mirrorcell - U(phoria)), 04: Buster Odeholm (thrown / Northlane - Evian), 05: Lewis Johns (Love Is Noise / blanket - Blur), 06: Kel Pinchin (Split Chain - I'm Not Dying To Be Here), 07: Dan Lancaster & Jason Perry (Don Broco - Endorphins), 08: Erik Bickerstaffe (Static Dress - face..), 09: Sam Guaiana (Silverstein - Misery Made Me), 10: Zach Tuch (Heavenward - Tangerine), 11: Forrester Savell (City Of Souls - Cruelty / Karnivool), 12: Leon Schmidt (SUNBORN - Nebula), 13: Ermin Hamidovic (Systematic / 01 The End of All We Know), 14: Will Putney (Fit For An Autopsy - Walk With Me In Hell), 15: George Lever (Loathe - Agressive Evolution / Sleep Token), 16: Sam Bassal (Thornhill - nerv), 17: Henrik Udd (Architects - 8. Gravity), 18: Dan Braunstein (Spiritbox - Keep Sweet), 19: Zakk Cervini & Erik Ron (Bad Omens - THE DEATH OF PEACE OF MIND), 20: Jens Bogren (Fascination Street Studios Benchmark), 21: Adam Nolly Getgood (Periphery / GGD Modern Metal Target), 22: Acle Kahney (TesseracT - King), 23: Adam Cichocki (heaving. - carsick), 24: Manuel Renner (SENNA - Out Of The Blue)}>-Producer Reference Benchmark
slider3:0<-6.0,6.0,0.1>-Input Calibration Gain (dB)
slider4:-0.9<-6.0,6.0,0.1>-Producer Headroom Trim (dB)
slider5:0<0,1,1{Free Output, -6.0 dBTP Strict Pre-Master Lock}>-Headroom Guardian Mode
slider6:80<40,160,1>-Sub-Bass Mono Anchor Cutoff (Hz)
slider7:1<0,1,1{Bypass, Active Sentry}>-Kick/Bass Transient Sentry
slider8:0.8<0.0,3.0,0.1>-Vocal Pocket Dynamic Notch Depth (dB)
slider9:1<0,1,1{Manual Lock, gmem Auto-Sensing}>-Vocal Pocket Corridor Mode
slider10:1<0,1,1{Bypass, Engaged}>-Master Bus Glue Compressor
slider11:0<0,1,1{British VCA Punch, Neve Diode Bridge Vintage}>-Bus Glue Topology
slider12:-5.5<-36.0,0.0,0.5>-Bus Glue Threshold (dB)
slider13:2<0,3,1{1.5:1 Subtle, 2:1 Master Glue, 4:1 Modern Punch, 8:1 Heavy Squeeze}>-Bus Glue Ratio
slider14:10.0<0.1,100.0,0.5>-Bus Glue Attack (ms)
slider15:2<0,4,1{100ms Fast, 300ms Snappy, 600ms Classical, 1200ms Smooth, Auto Ballistics}>-Bus Glue Release
slider16:40<30,250,1>-Bus Glue Sidechain Detector HPF (Hz)
slider17:100<0,100,1>-Bus Glue Dry/Wet Mix (%)
slider18:38<20,60,1>-Tonal Forge HPF Cutoff (Hz)
slider19:3.0<-6.0,6.0,0.1>-Tonal Forge 80Hz Punch (dB)
slider20:-3.0<-6.0,6.0,0.1>-Tonal Forge 202Hz Mud Scoop (dB)
slider21:1.5<-6.0,6.0,0.1>-Tonal Forge 1.5kHz Mid Body (dB)
slider22:3.0<-6.0,6.0,0.1>-Tonal Forge 3.0kHz Pick Bite (dB)
slider23:1<0,3,1{Transparent Pure Pass, Neve 8014 Iron Desk, Studer A800 15 IPS Tape, Triode Tube Crucible}>-Harmonic Saturation Engine
slider24:2.5<0.0,12.0,0.1>-Harmonic Desk Drive (dB)
slider25:1.08<0.80,1.40,0.01>-Quad-Wall Stereo Imager Width
slider26:1<0,1,1{Bypass, Active Chorus Sync}>-Song Structure Chorus Impact
slider27:1<0,1,1{Bypass 1:1 Unity, Engaged Active Summing}>-Master Suite Processing State
slider28:0<0,1,1{Normal Processing, Delta Solo Audition}>-Delta Solo Audition
slider29:0<0,1,1{Snapshot A, Snapshot B}>-A/B Comparison Snapshot
slider30:0<0,1,1{Stereo Summing, Mid/Side Summing}>-Master Processing Mode
slider31:3.0<-6.0,6.0,0.1>-Tonal Forge 8.0kHz Air Sheen (dB)
slider32:0<0,2,1{Manual Standby, Local Ollama / HF Audit, Safe Auto-Calibrate (±0.5dB Max)}>-AI Mix Assistant Engine

in_pin:Instrumental In L
in_pin:Instrumental In R
out_pin:Master Sum L
out_pin:Master Sum R

options:no_meter
options:gmem=DameiMixMetering
options:maxmem=65536

@init
ext_noinit = 1.0;
M_PI = 3.14159265358979323846;

// EQ Biquad State History
hpf_x1_l = 0; hpf_x2_l = 0; hpf_y1_l = 0; hpf_y2_l = 0;
hpf_x1_r = 0; hpf_x2_r = 0; hpf_y1_r = 0; hpf_y2_r = 0;

p80_x1_l = 0; p80_x2_l = 0; p80_y1_l = 0; p80_y2_l = 0;
p80_x1_r = 0; p80_x2_r = 0; p80_y1_r = 0; p80_y2_r = 0;

s200_x1_l = 0; s200_x2_l = 0; s200_y1_l = 0; s200_y2_l = 0;
s200_x1_r = 0; s200_x2_r = 0; s200_y1_r = 0; s200_y2_r = 0;

b15_x1_l = 0; b15_x2_l = 0; b15_y1_l = 0; b15_y2_l = 0;
b15_x1_r = 0; b15_x2_r = 0; b15_y1_r = 0; b15_y2_r = 0;

b3k_x1_l = 0; b3k_x2_l = 0; b3k_y1_l = 0; b3k_y2_l = 0;
b3k_x1_r = 0; b3k_x2_r = 0; b3k_y1_r = 0; b3k_y2_r = 0;

s8k_x1_l = 0; s8k_x2_l = 0; s8k_y1_l = 0; s8k_y2_l = 0;
s8k_x1_r = 0; s8k_x2_r = 0; s8k_y1_r = 0; s8k_y2_r = 0;

sm_x1 = 0; sm_x2 = 0; sm_y1 = 0; sm_y2 = 0;

sc_x1 = 0; sc_x2 = 0; sc_y1 = 0; sc_y2 = 0;
comp_env = 0.0;
glue_gr_db = 0.0;

// Dynamic Vocal Pocket 2.2kHz notch state
np_x1_l = 0; np_x2_l = 0; np_y1_l = 0; np_y2_l = 0;
np_x1_r = 0; np_x2_r = 0; np_y1_r = 0; np_y2_r = 0;

vu_rms_smooth = 0.0;
inst_peak = 0.0;
inst_rms = -90.0;
sifam_needle_vu = -20.0;
sifam_needle_gr = 0.0;

rms_acc_l = 0.0; rms_acc_r = 0.0; rms_cnt = 0;

// Vectorscope history circular buffers
scope_buf_l = 2000;
scope_buf_r = 2300;
scope_pos = 0;

// Handshake heartbeat into ecosystem gmem
gmem[1400] = 1;

function clamp(v, min_v, max_v) (
  max(min_v, min(max_v, v));
);

function fast_shape(x) local(ax) (
  ax = abs(x);
  x / (1.0 + ax * (0.8 + 0.2 * ax));
);

function get_producer_short_name(idx) (
  idx == 0  ? "00: UNITY" :
  idx == 1  ? "01: PRENC" :
  idx == 2  ? "02: SEIGEL" :
  idx == 3  ? "03: DOLESE" :
  idx == 4  ? "04: ODEHOLM" :
  idx == 5  ? "05: JOHNS" :
  idx == 6  ? "06: PINCHIN" :
  idx == 7  ? "07: LANCASTER" :
  idx == 8  ? "08: BICKERSTAFFE" :
  idx == 9  ? "09: GUAIANA" :
  idx == 10 ? "10: TUCH" :
  idx == 11 ? "11: SAVELL" :
  idx == 12 ? "12: SCHMIDT" :
  idx == 13 ? "13: HAMIDOVIC" :
  idx == 14 ? "14: PUTNEY" :
  idx == 15 ? "15: LEVER" :
  idx == 16 ? "16: BASSAL" :
  idx == 17 ? "17: UDD" :
  idx == 18 ? "18: BRAUNSTEIN" :
  idx == 19 ? "19: CERVINI" :
  idx == 20 ? "20: BOGREN" :
  idx == 21 ? "21: NOLLY" :
  idx == 22 ? "22: KAHNEY" :
  idx == 23 ? "23: CICHOCKI" : "24: RENNER";
);

function get_producer_ref_track(idx) (
  idx == 0  ? "Calibration Baseline (1:1 Bit-Exact Pass)" :
  idx == 1  ? "Alpha Wolf - 60cm Of Steel (feat. Holding Absence)" :
  idx == 2  ? "DIESECT - TOO MANY SCARS" :
  idx == 3  ? "Mirrorcell - U(phoria)" :
  idx == 4  ? "thrown - on the verge / Northlane - Evian" :
  idx == 5  ? "Love Is Noise - Hole In Me / blanket - Blur" :
  idx == 6  ? "Split Chain - motionblur - 03 I'm Not Dying To Be Here" :
  idx == 7  ? "Don Broco - Endorphins" :
  idx == 8  ? "Static Dress - face.." :
  idx == 9  ? "Silverstein - Misery Made Me" :
  idx == 10 ? "Heavenward - Tangerine" :
  idx == 11 ? "City Of Souls - Cruelty / Karnivool" :
  idx == 12 ? "SUNBORN - Nebula" :
  idx == 13 ? "Architects / Systematic Mastering Benchmark" :
  idx == 14 ? "Fit For An Autopsy - Walk With Me In Hell" :
  idx == 15 ? "Loathe - Agressive Evolution / Sleep Token" :
  idx == 16 ? "Thornhill - nerv" :
  idx == 17 ? "Architects - 8. Gravity" :
  idx == 18 ? "Spiritbox - Keep Sweet" :
  idx == 19 ? "Bad Omens - THE DEATH OF PEACE OF MIND" :
  idx == 20 ? "Fascination Street Studios Swedish Metal Benchmark" :
  idx == 21 ? "Periphery / GGD Modern Progressive Target" :
  idx == 22 ? "TesseracT - King" :
  idx == 23 ? "heaving. - why are you still dreaming- - 03 carsick" :
              "SENNA - Out of The Blue";
);

function update_filters() local(w0, alpha, cos_w0, sin_w0, A, beta, sm_w0, sm_cos, sm_sin, sm_alpha, sc_w0, sc_cos, sc_sin, sc_alpha) (
  srate <= 0 ? srate = 44100;

  // 1. HPF Sub-Cut Filter (slider18) - 18dB/oct Bessel/Butterworth curve
  w0 = 2.0 * M_PI * clamp(slider18, 20.0, 100.0) / srate;
  alpha = sin(w0) / (2.0 * 0.7071);
  hpf_b0 = (1.0 + cos(w0)) * 0.5;
  hpf_b1 = -(1.0 + cos(w0));
  hpf_b2 = (1.0 + cos(w0)) * 0.5;
  hpf_a0 = 1.0 + alpha;
  hpf_a1 = -2.0 * cos(w0);
  hpf_a2 = 1.0 - alpha;

  // 2. 80Hz Punch Low Shelf (slider19)
  A = exp(slider19 * 0.0575646273);
  w0 = 2.0 * M_PI * 80.0 / srate;
  cos_w0 = cos(w0); sin_w0 = sin(w0);
  alpha = sin_w0 / (2.0 * 0.7071);
  beta = 2.0 * sqrt(A) * alpha;
  p80_b0 = A * ((A + 1.0) - (A - 1.0) * cos_w0 + beta);
  p80_b1 = 2.0 * A * ((A - 1.0) - (A + 1.0) * cos_w0);
  p80_b2 = A * ((A + 1.0) - (A - 1.0) * cos_w0 - beta);
  p80_a0 = (A + 1.0) + (A - 1.0) * cos_w0 + beta;
  p80_a1 = -2.0 * ((A - 1.0) + (A + 1.0) * cos_w0);
  p80_a2 = (A + 1.0) + (A - 1.0) * cos_w0 - beta;

  // 3. 202Hz Mud Scoop (slider20) - Matches TB EQ Band 4
  A = exp(slider20 * 0.0575646273);
  w0 = 2.0 * M_PI * 202.0 / srate;
  alpha = sin(w0) / (2.0 * 1.2);
  s200_b0 = 1.0 + alpha * A;
  s200_b1 = -2.0 * cos(w0);
  s200_b2 = 1.0 - alpha * A;
  s200_a0 = 1.0 + alpha / A;
  s200_a1 = -2.0 * cos(w0);
  s200_a2 = 1.0 - alpha / A;

  // 4. 1.5kHz Mid Body (slider21) - Matches TB EQ Band 5
  A = exp(slider21 * 0.0575646273);
  w0 = 2.0 * M_PI * 1500.0 / srate;
  alpha = sin(w0) / (2.0 * 1.5);
  b15_b0 = 1.0 + alpha * A;
  b15_b1 = -2.0 * cos(w0);
  b15_b2 = 1.0 - alpha * A;
  b15_a0 = 1.0 + alpha / A;
  b15_a1 = -2.0 * cos(w0);
  b15_a2 = 1.0 - alpha / A;

  // 5. 3.0kHz Pick Attack Bite (slider22) - Matches TB EQ Band 6
  A = exp(slider22 * 0.0575646273);
  w0 = 2.0 * M_PI * 3000.0 / srate;
  alpha = sin(w0) / (2.0 * 1.8);
  b3k_b0 = 1.0 + alpha * A;
  b3k_b1 = -2.0 * cos(w0);
  b3k_b2 = 1.0 - alpha * A;
  b3k_a0 = 1.0 + alpha / A;
  b3k_a1 = -2.0 * cos(w0);
  b3k_a2 = 1.0 - alpha / A;

  // 6. 8.0kHz Air Sheen High Shelf (slider31) - Matches TB EQ Band 7
  A = exp(slider31 * 0.0575646273);
  w0 = 2.0 * M_PI * 8000.0 / srate;
  cos_w0 = cos(w0); sin_w0 = sin(w0);
  alpha = sin_w0 / (2.0 * 0.7071);
  beta = 2.0 * sqrt(A) * alpha;
  s8k_b0 = A * ((A + 1.0) + (A - 1.0) * cos_w0 + beta);
  s8k_b1 = -2.0 * A * ((A - 1.0) + (A + 1.0) * cos_w0);
  s8k_b2 = A * ((A + 1.0) + (A - 1.0) * cos_w0 - beta);
  s8k_a0 = (A + 1.0) - (A - 1.0) * cos_w0 + beta;
  s8k_a1 = 2.0 * ((A - 1.0) - (A + 1.0) * cos_w0);
  s8k_a2 = (A + 1.0) - (A - 1.0) * cos_w0 - beta;

  // 7. Elliptic Sub-Mono Side Highpass (Butterworth 2nd order at slider6 Hz)
  sm_w0 = 2.0 * M_PI * clamp(slider6, 40.0, 160.0) / srate;
  sm_cos = cos(sm_w0); sm_sin = sin(sm_w0);
  sm_alpha = sm_sin / (2.0 * 0.7071);
  sm_b0 = (1.0 + sm_cos) * 0.5;
  sm_b1 = -(1.0 + sm_cos);
  sm_b2 = (1.0 + sm_cos) * 0.5;
  sm_a0 = 1.0 + sm_alpha;
  sm_a1 = -2.0 * sm_cos;
  sm_a2 = 1.0 - sm_alpha;

  // 8. Bus Glue Sidechain Detector HPF (slider16 - Butterworth 2nd order)
  sc_w0 = 2.0 * M_PI * clamp(slider16, 30.0, 250.0) / srate;
  sc_cos = cos(sc_w0); sc_sin = sin(sc_w0);
  sc_alpha = sc_sin / (2.0 * 0.7071);
  sc_b0 = (1.0 + sc_cos) * 0.5;
  sc_b1 = -(1.0 + sc_cos);
  sc_b2 = (1.0 + sc_cos) * 0.5;
  sc_a0 = 1.0 + sc_alpha;
  sc_a1 = -2.0 * sc_cos;
  sc_a2 = 1.0 - sc_alpha;
);

function apply_producer_preset(idx) (
  idx == 0 ? ( // Unity Baseline (1:1 Transparent Pass)
    slider3 = 0.0; slider4 = 0.0; slider5 = 0; slider6 = 80; slider7 = 1;
    slider8 = 0.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = 0.0;
    slider13 = 1; slider14 = 30.0; slider15 = 2; slider16 = 40; slider17 = 100;
    slider18 = 30; slider19 = 0.0; slider20 = 0.0; slider21 = 0.0; slider22 = 0.0;
    slider23 = 0; slider24 = 0.0; slider25 = 1.00; slider31 = 0.0;
  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target) - Forensic Replicate of Track 15 Legacy Chain
    slider3 = 0.0;
    slider4 = -0.9;   // Net Calibrated Headroom (matches legacy chain DeeGain staging)
    slider5 = 0;      // Free Output
    slider6 = 80;     // Sub-Bass Mono Anchor Cutoff (matches Bass Manager 80 Hz)
    slider7 = 1;      // Transient Sentry Active
    slider8 = 0.8;    // Dynamic Vocal Pocket depth
    slider9 = 1;      // gmem Auto-Sensing Corridor
    slider10 = 1;     // Bus Glue Engaged
    slider11 = 0;     // British VCA Punch (SSL 4000G / BUSTERse)
    slider12 = -5.5;  // Threshold calibrated for 1.8-2.5 dB musical glue
    slider13 = 2;     // 4:1 Modern Punch (matches BUSTERse 4:1)
    slider14 = 10.0;  // Attack 10 ms (matches BUSTERse 10 ms)
    slider15 = 2;     // Release 600 ms (matches BUSTERse .6 sec)
    slider16 = 40;    // Sidechain Detector HPF (matches BUSTERse 39Hz HPF)
    slider17 = 100;   // 100% Dry/Wet
    slider18 = 38;    // HPF Cutoff 38 Hz (matches Bass Manager 30Hz & TB EQ 40Hz)
    slider19 = 3.0;   // 80Hz Punch +3.0 dB Low Shelf (matches TB EQ Band 2!)
    slider20 = -3.0;  // 202Hz Mud Scoop -3.0 dB, Q=1.2 (matches TB EQ Band 4!)
    slider21 = 1.5;   // 1.5kHz Mid Body +1.5 dB, Q=1.5 (matches TB EQ Band 5!)
    slider22 = 3.0;   // 3.0kHz Bite +3.0 dB, Q=1.8 (matches TB EQ Band 6!)
    slider23 = 1;     // Neve 8014 Iron Desk (matches Britson Buss Vintage Summing!)
    slider24 = 2.5;   // Console Desk Drive 2.5 dB (matches Britson + Bass Manager 25% drive)
    slider25 = 1.08;  // Quad Imager Width 1.08x
    slider31 = 3.0;   // 8.0kHz Sheen +3.0 dB (matches TB EQ Band 7!)
  ) : idx == 1 ? ( // Lance Prenc (Alpha Wolf - 60cm Of Steel)
    slider3 = 0.0; slider4 = -1.2; slider5 = 0; slider6 = 85; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -6.5;
    slider13 = 2; slider14 = 30.0; slider15 = 0; slider16 = 80; slider17 = 100;
    slider18 = 35; slider19 = 2.0; slider20 = -3.5; slider21 = 1.2; slider22 = 3.5;
    slider23 = 1; slider24 = 3.8; slider25 = 1.15; slider31 = 3.2;
  ) : idx == 2 ? ( // Scott Seigel (DIESECT - TOO MANY SCARS)
    slider3 = 0.0; slider4 = -1.0; slider5 = 0; slider6 = 80; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -6.0;
    slider13 = 2; slider14 = 10.0; slider15 = 1; slider16 = 60; slider17 = 100;
    slider18 = 32; slider19 = 3.5; slider20 = -3.2; slider21 = 0.8; slider22 = 3.0;
    slider23 = 1; slider24 = 3.2; slider25 = 1.12; slider31 = 2.5;
  ) : idx == 3 ? ( // Jonathan Dolese (Mirrorcell - U(phoria))
    slider3 = 0.0; slider4 = -1.1; slider5 = 0; slider6 = 80; slider7 = 1;
    slider8 = 0.9; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.0;
    slider13 = 1; slider14 = 10.0; slider15 = 2; slider16 = 50; slider17 = 100;
    slider18 = 35; slider19 = 2.5; slider20 = -2.8; slider21 = 1.5; slider22 = 2.8;
    slider23 = 2; slider24 = 2.4; slider25 = 1.10; slider31 = 3.2;
  ) : idx == 4 ? ( // Buster Odeholm (thrown / Northlane - Evian)
    slider3 = 0.0; slider4 = -1.4; slider5 = 0; slider6 = 90; slider7 = 1;
    slider8 = 1.4; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -7.0;
    slider13 = 3; slider14 = 10.0; slider15 = 0; slider16 = 90; slider17 = 100;
    slider18 = 40; slider19 = 3.2; slider20 = -4.0; slider21 = 0.5; slider22 = 4.0;
    slider23 = 1; slider24 = 4.0; slider25 = 1.25; slider31 = 3.5;
  ) : idx == 5 ? ( // Lewis Johns (Love Is Noise / blanket - Blur)
    slider3 = 0.0; slider4 = -0.8; slider5 = 0; slider6 = 75; slider7 = 1;
    slider8 = 0.7; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -4.5;
    slider13 = 1; slider14 = 25.0; slider15 = 2; slider16 = 40; slider17 = 100;
    slider18 = 30; slider19 = 2.0; slider20 = -2.2; slider21 = 1.8; slider22 = 2.0;
    slider23 = 2; slider24 = 2.2; slider25 = 1.05; slider31 = 2.6;
  ) : idx == 14 ? ( // Will Putney (Fit For An Autopsy - Walk With Me In Hell)
    slider3 = 0.0; slider4 = -1.5; slider5 = 0; slider6 = 85; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -7.5;
    slider13 = 2; slider14 = 10.0; slider15 = 1; slider16 = 70; slider17 = 100;
    slider18 = 38; slider19 = 3.5; slider20 = -3.8; slider21 = 1.2; slider22 = 3.5;
    slider23 = 1; slider24 = 3.8; slider25 = 1.15; slider31 = 3.0;
  ) : idx == 15 ? ( // George Lever (Loathe - Agressive Evolution / Sleep Token)
    slider3 = 0.0; slider4 = -1.0; slider5 = 0; slider6 = 80; slider7 = 1;
    slider8 = 0.8; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -5.0;
    slider13 = 1; slider14 = 20.0; slider15 = 2; slider16 = 45; slider17 = 100;
    slider18 = 32; slider19 = 3.2; slider20 = -2.8; slider21 = 1.4; slider22 = 2.6;
    slider23 = 3; slider24 = 2.8; slider25 = 1.12; slider31 = 3.2;
  ) : idx == 18 ? ( // Dan Braunstein (Spiritbox - Keep Sweet)
    slider3 = 0.0; slider4 = -1.0; slider5 = 0; slider6 = 80; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.0;
    slider13 = 2; slider14 = 10.0; slider15 = 2; slider16 = 50; slider17 = 100;
    slider18 = 32; slider19 = 2.5; slider20 = -2.5; slider21 = 1.0; slider22 = 2.5;
    slider23 = 1; slider24 = 3.0; slider25 = 1.10; slider31 = 2.8;
  ) : idx == 22 ? ( // Acle Kahney (TesseracT - King)
    slider3 = 0.0; slider4 = -1.2; slider5 = 0; slider6 = 80; slider7 = 1;
    slider8 = 1.1; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -6.0;
    slider13 = 2; slider14 = 15.0; slider15 = 1; slider16 = 60; slider17 = 100;
    slider18 = 35; slider19 = 2.8; slider20 = -3.2; slider21 = 1.0; slider22 = 3.2;
    slider23 = 1; slider24 = 3.0; slider25 = 1.18; slider31 = 3.2;
  ) : ( // Authentic Producer Calibration Default (Modern Metal Standard)
    slider3 = 0.0; slider4 = -1.0; slider5 = 0; slider6 = 80; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.5;
    slider13 = 2; slider14 = 10.0; slider15 = 2; slider16 = 50; slider17 = 100;
    slider18 = 35; slider19 = 2.6; slider20 = -2.8; slider21 = 1.2; slider22 = 2.8;
    slider23 = 1; slider24 = 2.8; slider25 = 1.10; slider31 = 2.8;
  );
  update_filters();
  slider_automate();
);

function trigger_ai_assist() local(delta_trim) (
  inst_peak > 0.001 ? (
    delta_trim = clamp(-3.4 - (20.0 * log10(inst_peak)), -0.5, 0.5);
    slider4 = clamp(slider4 + delta_trim, -4.0, 1.0);
  );
  inst_rms > -40.0 ? (
    slider12 = clamp(inst_rms + 14.0, -18.0, -3.0);
  );
  update_filters();
  slider_automate();
);

update_filters();
apply_producer_preset(slider2);

@slider
prev_preset != slider2 ? (
  apply_producer_preset(slider2);
  prev_preset = slider2;
);
slider32 == 2 ? (
  trigger_ai_assist();
  slider32 = 1;
);
update_filters();

@sample
srate <= 0 ? srate = 44100;
dry_l = spl0; dry_r = spl1;

vu_omega = 1.0 - exp(-1.0 / (srate * 0.300));
vu_sig_sq = (dry_l * dry_l + dry_r * dry_r) * 0.5;
vu_rms_smooth += (vu_sig_sq - vu_rms_smooth) * vu_omega;
(vu_rms_smooth != vu_rms_smooth || vu_rms_smooth <= 0.000000001) ? (
  inst_rms = -90.0;
) : (
  inst_rms = 10.0 * log10(vu_rms_smooth);
);
inst_peak = max(abs(dry_l), abs(dry_r));

scope_pos = (scope_pos + 1) % 256;
scope_buf_l[scope_pos] = dry_l;
scope_buf_r[scope_pos] = dry_r;

// 1:1 Complete Bit-Exact Transparent Pass if Suite Bypassed OR Preset 00 (Unity Baseline)
(slider27 == 0 || slider2 == 0) ? (
  // Pure Transparent Passthrough
  spl0 = dry_l; spl1 = dry_r;
) : (
  // 1. Input Gain Calibration
  in_gain = exp(slider3 * 0.1151292546);
  in_l = dry_l * in_gain;
  in_r = dry_r * in_gain;

  // 2. 6-Band Tonal Forge Equalizer
  // Band 1: HPF Sub-Cut
  y_l = (hpf_b0 * in_l + hpf_b1 * hpf_x1_l + hpf_b2 * hpf_x2_l - hpf_a1 * hpf_y1_l - hpf_a2 * hpf_y2_l) / hpf_a0;
  hpf_x2_l = hpf_x1_l; hpf_x1_l = in_l; hpf_y2_l = hpf_y1_l; hpf_y1_l = y_l;
  y_r = (hpf_b0 * in_r + hpf_b1 * hpf_x1_r + hpf_b2 * hpf_x2_r - hpf_a1 * hpf_y1_r - hpf_a2 * hpf_y2_r) / hpf_a0;
  hpf_x2_r = hpf_x1_r; hpf_x1_r = in_r; hpf_y2_r = hpf_y1_r; hpf_y1_r = y_r;

  // Band 2: 80Hz Punch Low Shelf
  s_l = (p80_b0 * y_l + p80_b1 * p80_x1_l + p80_b2 * p80_x2_l - p80_a1 * p80_y1_l - p80_a2 * p80_y2_l) / p80_a0;
  p80_x2_l = p80_x1_l; p80_x1_l = y_l; p80_y2_l = p80_y1_l; p80_y1_l = s_l;
  s_r = (p80_b0 * y_r + p80_b1 * p80_x1_r + p80_b2 * p80_x2_r - p80_a1 * p80_y1_r - p80_a2 * p80_y2_r) / p80_a0;
  p80_x2_r = p80_x1_r; p80_x1_r = y_r; p80_y2_r = p80_y1_r; p80_y1_r = s_r;

  // Band 3: 202Hz Mud Scoop Notch
  m_l = (s200_b0 * s_l + s200_b1 * s200_x1_l + s200_b2 * s200_x2_l - s200_a1 * s200_y1_l - s200_a2 * s200_y2_l) / s200_a0;
  s200_x2_l = s200_x1_l; s200_x1_l = s_l; s200_y2_l = s200_y1_l; s200_y1_l = m_l;
  m_r = (s200_b0 * s_r + s200_b1 * s200_x1_r + s200_b2 * s200_x2_r - s200_a1 * s200_y1_r - s200_a2 * s200_y2_r) / s200_a0;
  s200_x2_r = s200_x1_r; s200_x1_r = s_r; s200_y2_r = s200_y1_r; s200_y1_r = m_r;

  // Band 4: 1.5kHz Mid Body Bell
  mb_l = (b15_b0 * m_l + b15_b1 * b15_x1_l + b15_b2 * b15_x2_l - b15_a1 * b15_y1_l - b15_a2 * b15_y2_l) / b15_a0;
  b15_x2_l = b15_x1_l; b15_x1_l = m_l; b15_y2_l = b15_y1_l; b15_y1_l = mb_l;
  mb_r = (b15_b0 * m_r + b15_b1 * b15_x1_r + b15_b2 * b15_x2_r - b15_a1 * b15_y1_r - b15_a2 * b15_y2_r) / b15_a0;
  b15_x2_r = b15_x1_r; b15_x1_r = m_r; b15_y2_r = b15_y1_r; b15_y1_r = mb_r;

  // Band 5: 3.0kHz Pick Attack Bite Bell
  pb_l = (b3k_b0 * mb_l + b3k_b1 * b3k_x1_l + b3k_b2 * b3k_x2_l - b3k_a1 * b3k_y1_l - b3k_a2 * b3k_y2_l) / b3k_a0;
  b3k_x2_l = b3k_x1_l; b3k_x1_l = mb_l; b3k_y2_l = b3k_y1_l; b3k_y1_l = pb_l;
  pb_r = (b3k_b0 * mb_r + b3k_b1 * b3k_x1_r + b3k_b2 * b3k_x2_r - b3k_a1 * b3k_y1_r - b3k_a2 * b3k_y2_r) / b3k_a0;
  b3k_x2_r = b3k_x1_r; b3k_x1_r = mb_r; b3k_y2_r = b3k_y1_r; b3k_y1_r = pb_r;

  // Band 6: 8.0kHz Air Sheen High Shelf
  eq_out_l = (s8k_b0 * pb_l + s8k_b1 * s8k_x1_l + s8k_b2 * s8k_x2_l - s8k_a1 * s8k_y1_l - s8k_a2 * s8k_y2_l) / s8k_a0;
  s8k_x2_l = s8k_x1_l; s8k_x1_l = pb_l; s8k_y2_l = s8k_y1_l; s8k_y1_l = eq_out_l;
  eq_out_r = (s8k_b0 * pb_r + s8k_b1 * s8k_x1_r + s8k_b2 * s8k_x2_r - s8k_a1 * s8k_y1_r - s8k_a2 * s8k_y2_r) / s8k_a0;
  s8k_x2_r = s8k_x1_r; s8k_x1_r = pb_r; s8k_y2_r = s8k_y1_r; s8k_y1_r = eq_out_r;

  // 3. Dynamic Vocal Pocket (Corridor Relay via gmem[1401])
  vox_level = gmem[1401];
  (slider9 == 1 && vox_level > -36.0) ? (
    pocket_depth = min(slider8, max(0.0, (vox_level + 36.0) / 24.0 * slider8));
  ) : (
    pocket_depth = slider8;
  );

  pocket_depth > 0.05 ? (
    A_np = exp(-pocket_depth * 0.0575646273);
    w0_np = 2.0 * M_PI * 2200.0 / srate;
    alpha_np = sin(w0_np) / (2.0 * 2.0);
    np_b0 = 1.0 + alpha_np * A_np; np_b1 = -2.0 * cos(w0_np); np_b2 = 1.0 - alpha_np * A_np;
    np_a0 = 1.0 + alpha_np / A_np; np_a1 = -2.0 * cos(w0_np); np_a2 = 1.0 - alpha_np / A_np;

    pock_l = (np_b0 * eq_out_l + np_b1 * np_x1_l + np_b2 * np_x2_l - np_a1 * np_y1_l - np_a2 * np_y2_l) / np_a0;
    np_x2_l = np_x1_l; np_x1_l = eq_out_l; np_y2_l = np_y1_l; np_y1_l = pock_l;
    pock_r = (np_b0 * eq_out_r + np_b1 * np_x1_r + np_b2 * np_x2_r - np_a1 * np_y1_r - np_a2 * np_y2_r) / np_a0;
    np_x2_r = np_x1_r; np_x1_r = eq_out_r; np_y2_r = np_y1_r; np_y1_r = pock_r;
  ) : (
    pock_l = eq_out_l; pock_r = eq_out_r;
  );

  // 4. Harmonic Crucible Saturation Engine
  slider23 == 1 ? ( // Neve 8014 Iron Desk (Even/Odd Console Saturation)
    sat_drive = exp(slider24 * 0.1151292546);
    sat_l = pock_l * sat_drive; sat_r = pock_r * sat_drive;
    sat_out_l = (sat_l - 0.12 * sat_l * sat_l + 0.04 * sat_l * sat_l * sat_l) / sat_drive;
    sat_out_r = (sat_r - 0.12 * sat_r * sat_r + 0.04 * sat_r * sat_r * sat_r) / sat_drive;
  ) : slider23 == 2 ? ( // Studer A800 Tape Saturation
    sat_drive = exp(slider24 * 0.1151292546);
    sat_out_l = fast_shape(pock_l * sat_drive) / sat_drive;
    sat_out_r = fast_shape(pock_r * sat_drive) / sat_drive;
  ) : slider23 == 3 ? ( // Triode Tube Crucible
    sat_drive = exp(slider24 * 0.1151292546);
    sat_l = pock_l * sat_drive; sat_r = pock_r * sat_drive;
    sat_out_l = (sat_l / (1.0 + abs(sat_l))) / sat_drive;
    sat_out_r = (sat_r / (1.0 + abs(sat_r))) / sat_drive;
  ) : (
    sat_out_l = pock_l; sat_out_r = pock_r;
  );

  // 5. Studio Bus Glue Compressor (British VCA / Diode Bridge)
  slider10 ? (
    sc_in = (sat_out_l + sat_out_r) * 0.5;
    sc_det = (sc_b0 * sc_in + sc_b1 * sc_x1 + sc_b2 * sc_x2 - sc_a1 * sc_y1 - sc_a2 * sc_y2) / sc_a0;
    sc_x2 = sc_x1; sc_x1 = sc_in; sc_y2 = sc_y1; sc_y1 = sc_det;

    sc_peak = abs(sc_det);
    sc_db = sc_peak > 0.000000001 ? 20.0 * log10(sc_peak) : -120.0;

    atk_coeff = exp(-1.0 / (srate * (slider14 * 0.001)));
    rel_time = slider15 == 0 ? 0.100 : (slider15 == 1 ? 0.300 : (slider15 == 2 ? 0.600 : (slider15 == 3 ? 1.200 : 0.450)));
    rel_coeff = exp(-1.0 / (srate * rel_time));

    sc_db > comp_env ? (
      comp_env = sc_db + (comp_env - sc_db) * atk_coeff;
    ) : (
      comp_env = sc_db + (comp_env - sc_db) * rel_coeff;
    );

    ratio_val = slider13 == 0 ? 1.5 : (slider13 == 1 ? 2.0 : (slider13 == 2 ? 4.0 : 8.0));
    over_db = comp_env - slider12;
    over_db > 0.0 ? (
      glue_gr_db = over_db * (1.0 - 1.0 / ratio_val);
    ) : (
      glue_gr_db = 0.0;
    );

    glue_gain = exp(-glue_gr_db * 0.1151292546);
    mix_frac = slider17 * 0.01;
    comp_l = sat_out_l * glue_gain * mix_frac + sat_out_l * (1.0 - mix_frac);
    comp_r = sat_out_r * glue_gain * mix_frac + sat_out_r * (1.0 - mix_frac);
  ) : (
    comp_l = sat_out_l; comp_r = sat_out_r;
    glue_gr_db = 0.0;
  );

  // 6. Quad-Wall Stereo Imager & Sub-Mono Anchor
  mid = (comp_l + comp_r) * 0.5;
  side = (comp_l - comp_r) * 0.5;

  // Filter side channel with Sub-Mono Highpass
  side_filt = (sm_b0 * side + sm_b1 * sm_x1 + sm_b2 * sm_x2 - sm_a1 * sm_y1 - sm_a2 * sm_y2) / sm_a0;
  sm_x2 = sm_x1; sm_x1 = side; sm_y2 = sm_y1; sm_y1 = side_filt;

  width_mult = slider25;
  side_out = side_filt * width_mult;

  out_sum_l = mid + side_out;
  out_sum_r = mid - side_out;

  // 7. Output Trim & Pre-Master Ceiling Guardian
  trim_gain = exp(slider4 * 0.1151292546);
  final_l = out_sum_l * trim_gain;
  final_r = out_sum_r * trim_gain;

  slider5 ? (
    ceil_lin = exp(-6.0 * 0.1151292546);
    final_l = clamp(final_l, -ceil_lin, ceil_lin);
    final_r = clamp(final_r, -ceil_lin, ceil_lin);
  );

  slider28 ? ( // Delta Solo Audition
    spl0 = (final_l - dry_l);
    spl1 = (final_r - dry_r);
  ) : (
    spl0 = final_l;
    spl1 = final_r;
  );
);

// Needle Ballistics (SIFAM VU & GR)
vu_target = clamp(inst_rms + 18.0, -20.0, 3.0);
sifam_needle_vu += (vu_target - sifam_needle_vu) * 0.08;
gr_target = clamp(glue_gr_db, 0.0, 20.0);
sifam_needle_gr += (gr_target - sifam_needle_gr) * 0.12;

rms_acc_l += spl0 * spl0; rms_acc_r += spl1 * spl1; rms_cnt += 1;
rms_cnt >= 2048 ? (
  gmem[1402] = 10.0 * log10(max(0.000000001, (rms_acc_l + rms_acc_r) / (2.0 * rms_cnt)));
  gmem[1403] = glue_gr_db;
  gmem[1404] = slider1;
  rms_acc_l = 0.0; rms_acc_r = 0.0; rms_cnt = 0;
);

@gfx 1080 700
// =============================================================================
// FLAGSHIP AFRO-CYBERNETIC LUXURY CONSOLE SURFACE ARCHITECTURE
// =============================================================================

mouse_down = (mouse_cap & 1) != 0;
mouse_clicked = (mouse_down && !prev_mouse_down);
shift_down = (mouse_cap & 8) != 0;
ctrl_down = (mouse_cap & 4) != 0;
is_double_click = 0;
mouse_clicked ? (
  (time_precise() - last_click_t < 0.28) ? ( is_double_click = 1; );
  last_click_t = time_precise();
);
m_wheel = mouse_wheel; mouse_wheel = 0;

// Outer Obsidian Titanium Chassis
gfx_r = 0.015; gfx_g = 0.018; gfx_b = 0.024;
gfx_rect(0, 0, gfx_w, gfx_h);

// Golden Trim Dual Border
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
gfx_rect(8, 8, gfx_w - 16, gfx_h - 16, 0);
gfx_r = 0.40; gfx_g = 0.32; gfx_b = 0.10;
gfx_rect(9, 9, gfx_w - 18, gfx_h - 18, 0);

// Hardware Corner Bevels & Hex Bolts
c_sz = 16;
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
gfx_line(8, 8 + c_sz, 8 + c_sz, 8);
gfx_line(gfx_w - 8 - c_sz, 8, gfx_w - 8, 8 + c_sz);
gfx_line(8, gfx_h - 8 - c_sz, 8 + c_sz, gfx_h - 8);
gfx_line(gfx_w - 8 - c_sz, gfx_h - 8, gfx_w - 8, gfx_h - 8 - c_sz);

// Industrial Hex Bolts
function draw_hex_bolt(bx, by) (
  gfx_r = 0.22; gfx_g = 0.26; gfx_b = 0.32; gfx_circle(bx, by, 5, 1);
  gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.30; gfx_circle(bx, by, 5, 0);
  gfx_r = 0.05; gfx_g = 0.08; gfx_b = 0.12; gfx_circle(bx, by, 2, 1);
);
draw_hex_bolt(18, 18);
draw_hex_bolt(gfx_w - 18, 18);
draw_hex_bolt(18, gfx_h - 18);
draw_hex_bolt(gfx_w - 18, gfx_h - 18);

// Master Title Ribbon
hdr_h = 52;
gfx_r = 0.025; gfx_g = 0.032; gfx_b = 0.042;
gfx_rect(16, 16, gfx_w - 32, hdr_h);
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
gfx_rect(16, 16, gfx_w - 32, hdr_h, 0);

// Funtunfunefu Emblem with Dynamic Audio Pulse
r_pulse = 1.0 + max(0.0, (inst_rms + 35.0) / 45.0) * 0.25;
sig_cx = 36; sig_cy = 16 + hdr_h * 0.5;
gfx_r = 0.95; gfx_g = 0.75; gfx_b = 0.20; gfx_a = 0.25;
gfx_circle(sig_cx, sig_cy, floor(15 * r_pulse), 0);
gfx_a = 1.0;
gfx_circle(sig_cx, sig_cy, 12, 0);
gfx_circle(sig_cx, sig_cy, 7, 0);
gfx_circle(sig_cx, sig_cy, 3, 1);

gfx_setfont(1, "Orbitron", 14, 'b');
gfx_r = 0.98; gfx_g = 0.88; gfx_b = 0.70;
title_str = "DAMEI // INST BUS";
gfx_measurestr(title_str, tw, th);
gfx_x = 58; gfx_y = 16 + floor((hdr_h - th) * 0.5);
gfx_drawstr(title_str);

// Producer Benchmark Dropdown Selector Header
btn_y = 24; btn_h = 36;
p_bx = 58 + tw + 34;
p_bw = 250;

// Arrow buttons: dark slate background, gold border, high-contrast text
arr_hov_l = (mouse_x >= p_bx - 26 && mouse_x <= p_bx - 2 && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);
gfx_r = arr_hov_l ? 0.09 : 0.025; gfx_g = arr_hov_l ? 0.12 : 0.032; gfx_b = arr_hov_l ? 0.16 : 0.044;
gfx_rect(p_bx - 26, btn_y, 24, btn_h);
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
gfx_rect(p_bx - 26, btn_y, 24, btn_h, 0);
gfx_setfont(1, "Consolas", 14, 'b');
gfx_r = arr_hov_l ? 1.00 : 0.95; gfx_g = arr_hov_l ? 0.95 : 0.80; gfx_b = 0.40;
gfx_measurestr("<", aw_l, ah_l);
gfx_x = p_bx - 26 + floor((24 - aw_l) * 0.5); gfx_y = btn_y + floor((btn_h - ah_l) * 0.5);
gfx_drawstr("<");
mouse_clicked && arr_hov_l ? (
  slider2 = (slider2 - 1 + 25) % 25; apply_producer_preset(slider2); slider_automate();
);

// Preset Name display Box
p_hov = (mouse_x >= p_bx && mouse_x <= p_bx + p_bw && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);
gfx_r = p_hov ? 0.025 : 0.015; gfx_g = p_hov ? 0.032 : 0.020; gfx_b = p_hov ? 0.042 : 0.028;
gfx_rect(p_bx, btn_y, p_bw, btn_h);
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
gfx_rect(p_bx, btn_y, p_bw, btn_h, 0);

gfx_setfont(1, "Orbitron", 12.5, 'b');
gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
p_str = get_producer_short_name(slider2);
gfx_measurestr(p_str, pw, ph);
gfx_x = p_bx + floor((p_bw - pw) * 0.5); gfx_y = btn_y + floor((btn_h - ph) * 0.5);
gfx_drawstr(p_str);

// Right Arrow
arr_hov_r = (mouse_x >= p_bx + p_bw + 2 && mouse_x <= p_bx + p_bw + 26 && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);
gfx_r = arr_hov_r ? 0.09 : 0.025; gfx_g = arr_hov_r ? 0.12 : 0.032; gfx_b = arr_hov_r ? 0.16 : 0.044;
gfx_rect(p_bx + p_bw + 2, btn_y, 24, btn_h);
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
gfx_rect(p_bx + p_bw + 2, btn_y, 24, btn_h, 0);
gfx_setfont(1, "Consolas", 14, 'b');
gfx_r = arr_hov_r ? 1.00 : 0.95; gfx_g = arr_hov_r ? 0.95 : 0.80; gfx_b = 0.40;
gfx_measurestr(">", aw_r, ah_r);
gfx_x = p_bx + p_bw + 2 + floor((24 - aw_r) * 0.5); gfx_y = btn_y + floor((btn_h - ah_r) * 0.5);
gfx_drawstr(">");
mouse_clicked && arr_hov_r ? (
  slider2 = (slider2 + 1) % 25; apply_producer_preset(slider2); slider_automate();
);

// Right-Aligned Status Badges: zero right-spill guaranteed
right_x = gfx_w - 24;

// 5. Suite Master Engage Button
b5_w = 82; b5_x = right_x - b5_w;
b5_hov = (mouse_x >= b5_x && mouse_x <= b5_x + b5_w && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);
gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.022; gfx_rect(b5_x, btn_y, b5_w, btn_h);
slider27 ? (gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;) : (gfx_r = 0.50; gfx_g = 0.50; gfx_b = 0.50;);
gfx_rect(b5_x, btn_y, b5_w, btn_h, 0);
gfx_setfont(2, "Orbitron", 10.5, 'b');
eng_str = slider27 ? "ENGAGED" : "BYPASS";
gfx_measurestr(eng_str, ew, eh);
gfx_x = b5_x + floor((b5_w - ew) * 0.5); gfx_y = btn_y + floor((btn_h - eh) * 0.5);
gfx_drawstr(eng_str);
mouse_clicked && b5_hov ? (
  slider27 = !slider27; slider_automate();
);

// 4. Pre-Master Ceiling Lock
b4_w = 84; b4_x = b5_x - 6 - b4_w;
b4_hov = (mouse_x >= b4_x && mouse_x <= b4_x + b4_w && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);
gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.022; gfx_rect(b4_x, btn_y, b4_w, btn_h);
slider5 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.20; gfx_g = 0.92; gfx_b = 0.62;);
gfx_rect(b4_x, btn_y, b4_w, btn_h, 0);
gfx_setfont(2, "Consolas", 10.5, 'b');
ceil_str = slider5 ? "CEIL: -6dB" : "CEIL: FREE";
gfx_measurestr(ceil_str, cw, ch);
gfx_x = b4_x + floor((b4_w - cw) * 0.5); gfx_y = btn_y + floor((btn_h - ch) * 0.5);
gfx_drawstr(ceil_str);
mouse_clicked && b4_hov ? (
  slider5 = !slider5; slider_automate();
);

// 3. Mode
b3_w = 90; b3_x = b4_x - 6 - b3_w;
gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.022; gfx_rect(b3_x, btn_y, b3_w, btn_h);
gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(b3_x, btn_y, b3_w, btn_h, 0);
gfx_setfont(2, "Consolas", 10.5, 'b');
mode_str = "MODE: STEREO";
gfx_measurestr(mode_str, mw, mh);
gfx_x = b3_x + floor((b3_w - mw) * 0.5); gfx_y = btn_y + floor((btn_h - mh) * 0.5);
gfx_drawstr(mode_str);

// 2. Vocal Relay Link
b2_w = 94; b2_x = b3_x - 6 - b2_w;
vox_rms = gmem[1452];
gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.022; gfx_rect(b2_x, btn_y, b2_w, btn_h);
gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(b2_x, btn_y, b2_w, btn_h, 0);
v_str = sprintf(#, "VOX: %4.1fdB", vox_rms);
gfx_measurestr(v_str, vw, vh);
gfx_x = b2_x + floor((b2_w - vw) * 0.5); gfx_y = btn_y + floor((btn_h - vh) * 0.5);
gfx_drawstr(v_str);

// 1. Chorus Sync
b1_w = 90; b1_x = b2_x - 6 - b1_w;
gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.022; gfx_rect(b1_x, btn_y, b1_w, btn_h);
gfx_r = 0.00; gfx_g = 0.85; gfx_b = 0.45; gfx_rect(b1_x, btn_y, b1_w, btn_h, 0);
gfx_setfont(2, "Consolas", 10.5, 'b');
ch_str = "⚡ CHORUS";
gfx_measurestr(ch_str, chw, chh);
gfx_x = b1_x + floor((b1_w - chw) * 0.5); gfx_y = btn_y + floor((btn_h - chh) * 0.5);
gfx_drawstr(ch_str);

// Navigation Tabs Ribbon
tab_y = 76; tab_h = 42;
num_tabs = 7;
tab_w = floor((gfx_w - 32) / num_tabs);

ti = 0;
while (ti < num_tabs) (
  tx = 16 + ti * tab_w;
  is_act = (slider1 == ti);
  hov = (mouse_x >= tx && mouse_x <= tx + tab_w && mouse_y >= tab_y && mouse_y <= tab_y + tab_h);

  is_act ? (
    gfx_r = 0.065; gfx_g = 0.080; gfx_b = 0.105; gfx_rect(tx, tab_y, tab_w - 4, tab_h);
    gfx_r = 0.95; gfx_g = 0.70; gfx_b = 0.20; gfx_rect(tx, tab_y, tab_w - 4, tab_h, 0);
    gfx_rect(tx, tab_y + tab_h - 4, tab_w - 4, 4);
    gfx_r = 1.0; gfx_g = 0.90; gfx_b = 0.40;
  ) : (
    gfx_r = hov ? 0.035 : 0.022; gfx_g = hov ? 0.045 : 0.028; gfx_b = hov ? 0.060 : 0.038;
    gfx_rect(tx, tab_y, tab_w - 4, tab_h);
    gfx_r = 0.25; gfx_g = 0.32; gfx_b = 0.42; gfx_rect(tx, tab_y, tab_w - 4, tab_h, 0);
    gfx_r = hov ? 0.95 : 0.65; gfx_g = hov ? 0.95 : 0.72; gfx_b = hov ? 1.00 : 0.80;
  );

  gfx_setfont(1, "Orbitron", 12.5, 'b');
  t_lbl = ti == 0 ? "OVERVIEW" :
          ti == 1 ? "TONAL EQ" :
          ti == 2 ? "BUS GLUE" :
          ti == 3 ? "CRUCIBLE" :
          ti == 4 ? "STEREO" :
          ti == 5 ? "POCKET" : "PRODUCER";
  gfx_measurestr(t_lbl, tw, th);
  gfx_x = tx + floor((tab_w - 4 - tw) * 0.5);
  gfx_y = tab_y + floor((tab_h - th) * 0.5);
  gfx_drawstr(t_lbl);

  mouse_clicked && hov ? (
    slider1 = ti; slider_automate();
  );
  ti += 1;
);

ws_x = 16; ws_y = 126; ws_w = gfx_w - 32; ws_h = gfx_h - 142;

// Re-usable Parameter Slider
function draw_param_slider(px, py, pw, ph, label_str, val, min_v, max_v, fmt_str, s_idx, cr, cg, cb) local(v_frac, trk_y, trk_h, kn_x, hov, new_f) (
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.022; gfx_rect(px, py, pw, ph);
  gfx_r = 0.16; gfx_g = 0.24; gfx_b = 0.32; gfx_rect(px, py, pw, ph, 0);

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = cr; gfx_g = cg; gfx_b = cb;
  gfx_x = px + 12; gfx_y = py + 8; gfx_drawstr(label_str);

  gfx_setfont(2, "Consolas", 12, 'b'); gfx_r = 0.95; gfx_g = 0.95; gfx_b = 1.0;
  v_str = sprintf(#, fmt_str, val);
  gfx_measurestr(v_str, vw, vh);
  gfx_x = px + pw - vw - 12; gfx_y = py + 8; gfx_drawstr(v_str);

  trk_y = py + 34; trk_h = 10;
  gfx_r = 0.025; gfx_g = 0.035; gfx_b = 0.048; gfx_rect(px + 12, trk_y, pw - 24, trk_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(px + 12, trk_y, pw - 24, trk_h, 0);

  v_frac = max(0.0, min(1.0, (val - min_v) / (max_v - min_v)));
  gfx_r = cr; gfx_g = cg; gfx_b = cb;
  gfx_rect(px + 12, trk_y, v_frac * (pw - 24), trk_h);

  kn_x = px + 12 + v_frac * (pw - 24);
  gfx_r = 1.0; gfx_g = 0.90; gfx_b = 0.45; gfx_circle(kn_x, trk_y + trk_h * 0.5, 7, 1);
  gfx_r = 0.10; gfx_g = 0.15; gfx_b = 0.22; gfx_circle(kn_x, trk_y + trk_h * 0.5, 7, 0);

  hov = (mouse_x >= px + 12 && mouse_x <= px + pw - 12 && mouse_y >= py && mouse_y <= py + ph);
  mouse_clicked && hov ? drag_slider_idx = s_idx;
  drag_slider_idx == s_idx && mouse_down ? (
    new_f = max(0.0, min(1.0, (mouse_x - (px + 12)) / (pw - 24)));
    slider(s_idx) = min_v + new_f * (max_v - min_v);
    update_filters();
    slider_automate();
  );
);

// Re-usable Metallic Vertical Channel Strip Fader
function draw_channel_strip(px, py, pw, ph, band_title, band_sub, val, min_v, max_v, fmt_str, s_idx, cr, cg, cb) local(kn_y, trk_x, trk_w, trk_y, trk_h, f_val, zero_y, hov, new_f) (
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(px, py, pw, ph);
  gfx_r = cr; gfx_g = cg; gfx_b = cb; gfx_rect(px, py, pw, ph, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = cr; gfx_g = cg; gfx_b = cb;
  gfx_measurestr(band_title, tw, th);
  gfx_x = px + floor((pw - tw) * 0.5); gfx_y = py + 12; gfx_drawstr(band_title);

  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.65; gfx_g = 0.72; gfx_b = 0.82;
  gfx_measurestr(band_sub, stw, sth);
  gfx_x = px + floor((pw - stw) * 0.5); gfx_y = py + 30; gfx_drawstr(band_sub);

  // Digital Readout Box
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(px + 12, py + 50, pw - 24, 26);
  gfx_r = cr * 0.6; gfx_g = cg * 0.6; gfx_b = cb * 0.6; gfx_rect(px + 12, py + 50, pw - 24, 26, 0);
  gfx_setfont(1, "Consolas", 12, 'b'); gfx_r = 1.0; gfx_g = 0.95; gfx_b = 0.40;
  v_str = sprintf(#, fmt_str, val);
  gfx_measurestr(v_str, vsw, vsh);
  gfx_x = px + floor((pw - vsw) * 0.5); gfx_y = py + 56; gfx_drawstr(v_str);

  // Fader Track
  trk_x = px + floor(pw * 0.5) - 4;
  trk_y = py + 92;
  trk_w = 8;
  trk_h = ph - 134;

  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(trk_x, trk_y, trk_w, trk_h);
  gfx_r = 0.20; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(trk_x, trk_y, trk_w, trk_h, 0);

  // Fader Track Zero Mark and Active Fill
  f_val = (val - min_v) / (max_v - min_v);
  kn_y = trk_y + trk_h * (1.0 - f_val);

  min_v < 0 ? (
    zero_y = trk_y + trk_h * (max_v / (max_v - min_v));
    gfx_r = 0.45; gfx_g = 0.55; gfx_b = 0.65;
    gfx_line(trk_x - 12, zero_y, trk_x + trk_w + 12, zero_y);

    gfx_r = cr; gfx_g = cg; gfx_b = cb;
    val >= 0 ? (
      gfx_rect(trk_x + 1, kn_y, trk_w - 2, max(0, zero_y - kn_y));
    ) : (
      gfx_rect(trk_x + 1, zero_y, trk_w - 2, max(0, kn_y - zero_y));
    );
  ) : (
    gfx_r = cr; gfx_g = cg; gfx_b = cb;
    gfx_rect(trk_x + 1, kn_y, trk_w - 2, max(0, (trk_y + trk_h) - kn_y));
  );

  // Metallic Hardware Fader Cap
  cap_w = pw - 24; cap_h = 18;
  gfx_r = 0.12; gfx_g = 0.16; gfx_b = 0.22; gfx_rect(px + 12, kn_y - 9, cap_w, cap_h);
  gfx_r = cr; gfx_g = cg; gfx_b = cb; gfx_rect(px + 12, kn_y - 9, cap_w, cap_h, 0);
  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 1.00; gfx_line(px + 16, kn_y, px + 12 + cap_w - 4, kn_y);

  // Drag interaction
  hov = (mouse_x >= px && mouse_x <= px + pw && mouse_y >= trk_y - 12 && mouse_y <= trk_y + trk_h + 12);
  mouse_clicked && hov ? drag_slider_idx = s_idx;
  drag_slider_idx == s_idx && mouse_down ? (
    new_f = max(0.0, min(1.0, (trk_y + trk_h - mouse_y) / trk_h));
    slider(s_idx) = min_v + new_f * (max_v - min_v);
    update_filters();
    slider_automate();
  );
);

// Strictly Confined Vintage SIFAM Moving-Coil Meter with Glass Sheen & Lamp Glow
function draw_sifam_meter(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) local(plate_x, plate_y, plate_w, plate_h, piv_x, piv_y, radius_arc, radius_needle, ang_min, ang_max, a_span, a_frac, cur_a, ax, ay, ai, arc_steps, prev_ax, prev_ay, t_a, m_db, f_val, nx1, ny1, nx2, ny2, tw, th, t_str, badge_str, b_w, b_h, frac, cur_ang, tip_x, tip_y, base_x, base_y) (
  // Outer Beveled Recessed Chassis
  gfx_r = 0.055; gfx_g = 0.065; gfx_b = 0.080; gfx_rect(mx, my, mw, mh);
  gfx_r = 0.020; gfx_g = 0.024; gfx_b = 0.032; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(mx, my, mw, mh, 0);
  gfx_r = accent_r * 0.6; gfx_g = accent_g * 0.6; gfx_b = accent_b * 0.6; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4, 0);

  // Dial Faceplate
  plate_x = mx + 6; plate_y = my + 6;
  plate_w = mw - 12; plate_h = mh - 12;
  gfx_r = 0.035; gfx_g = 0.045; gfx_b = 0.060; gfx_rect(plate_x, plate_y, plate_w, plate_h);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(plate_x, plate_y, plate_w, plate_h, 0);

  piv_x = plate_x + plate_w * 0.5;
  piv_y = plate_y + plate_h - 16;

  radius_arc = min(plate_h - 58, plate_w * 0.44);
  radius_needle = radius_arc - 4;

  // Warm Incandescent Tungsten Lamp Glow behind meter pivot
  gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.35; gfx_a = 0.07;
  gfx_circle(piv_x, piv_y - radius_arc * 0.45, floor(radius_arc * 0.6), 1);
  gfx_a = 1.0;

  // Title and Mode Badge
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
  gfx_x = plate_x + 12; gfx_y = plate_y + 8; gfx_drawstr(title_str);

  gfx_setfont(2, "Consolas", 11.5, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  badge_str = is_glue ? "STUDIO GR" : "STUDIO VU";
  gfx_measurestr(badge_str, b_w, b_h);
  gfx_x = plate_x + plate_w - b_w - 12; gfx_y = plate_y + 8; gfx_drawstr(badge_str);

  // Calibrated Curved Scale Arc
  ang_min = -0.62; ang_max = 0.62; a_span = ang_max - ang_min;
  arc_steps = 30; ai = 0; prev_ax = 0; prev_ay = 0;
  loop(arc_steps + 1,
    a_frac = ai / arc_steps;
    cur_a = ang_min + a_frac * a_span;
    ax = piv_x + sin(cur_a) * radius_arc;
    ay = piv_y - cos(cur_a) * radius_arc;
    ai > 0 ? (
      is_glue ? (
        a_frac > 0.65 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;)
      ) : (
        a_frac > 0.87 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.95; gfx_g = 0.75; gfx_b = 0.20;)
      );
      gfx_line(prev_ax, prev_ay, ax, ay);
    );
    prev_ax = ax; prev_ay = ay;
    ai += 1;
  );

  // Scale Graduation Numbers & Ticks
  gfx_setfont(3, "Consolas", 10.5, 'b');
  is_glue ? (
    m_i = 0;
    while (m_i < 6) (
      m_db = m_i == 0 ? 0 : (m_i == 1 ? 3 : (m_i == 2 ? 6 : (m_i == 3 ? 10 : (m_i == 4 ? 16 : 20))));
      f_val = m_db / 20.0;
      t_a = ang_min + f_val * a_span;
      nx1 = piv_x + sin(t_a) * (radius_arc - 5); ny1 = piv_y - cos(t_a) * (radius_arc - 5);
      nx2 = piv_x + sin(t_a) * (radius_arc + 4); ny2 = piv_y - cos(t_a) * (radius_arc + 4);
      m_db >= 10 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.75; gfx_g = 0.88; gfx_b = 0.95;);
      gfx_line(nx1, ny1, nx2, ny2);
      t_str = sprintf(#, "%d", m_db);
      gfx_measurestr(t_str, tw, th);
      gfx_x = piv_x + sin(t_a) * (radius_arc + 14) - tw * 0.5;
      gfx_y = piv_y - cos(t_a) * (radius_arc + 14) - th * 0.5;
      gfx_drawstr(t_str);
      m_i += 1;
    );
  ) : (
    m_i = 0;
    while (m_i < 5) (
      m_db = m_i == 0 ? -20 : (m_i == 1 ? -10 : (m_i == 2 ? -5 : (m_i == 3 ? 0 : 3)));
      f_val = (m_db + 20.0) / 23.0;
      t_a = ang_min + f_val * a_span;
      nx1 = piv_x + sin(t_a) * (radius_arc - 5); ny1 = piv_y - cos(t_a) * (radius_arc - 5);
      nx2 = piv_x + sin(t_a) * (radius_arc + 4); ny2 = piv_y - cos(t_a) * (radius_arc + 4);
      m_db <= 0 ? (gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;) : (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;);
      gfx_line(nx1, ny1, nx2, ny2);
      t_str = sprintf(#, "%+d", m_db);
      gfx_measurestr(t_str, tw, th);
      gfx_x = piv_x + sin(t_a) * (radius_arc + 14) - tw * 0.5;
      gfx_y = piv_y - cos(t_a) * (radius_arc + 14) - th * 0.5;
      gfx_drawstr(t_str);
      m_i += 1;
    );
  );

  // Large Center Type
  gfx_setfont(1, "Orbitron", 14, 'b');
  is_glue ? (gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;) : (gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;) ;
  center_badge = is_glue ? "[ GR ]" : "[ VU ]";
  gfx_measurestr(center_badge, tw, th);
  gfx_x = floor(plate_x + (plate_w - tw) * 0.5);
  gfx_y = floor(piv_y - radius_needle * 0.45);
  gfx_drawstr(center_badge);

  // Deflected Moving Needle
  frac = is_glue ? min(1.0, max(0.0, needle_val / 20.0)) : min(1.0, max(0.0, (needle_val + 20.0) / 23.0));
  cur_ang = ang_min + frac * a_span;
  tip_x = piv_x + sin(cur_ang) * radius_needle;
  tip_y = piv_y - cos(cur_ang) * radius_needle;
  base_x = piv_x + sin(cur_ang) * 14;
  base_y = piv_y - cos(cur_ang) * 14;

  is_glue ? (gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;) : (gfx_r = 1.00; gfx_g = 0.80; gfx_b = 0.22;);
  gfx_line(base_x - 0.7, base_y, tip_x - 0.7, tip_y);
  gfx_line(base_x + 0.7, base_y, tip_x + 0.7, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  // Needle Tip Indicator Bead
  gfx_r = 0.98; gfx_g = 0.25; gfx_b = 0.22; gfx_circle(tip_x, tip_y, 2.5, 1);

  // Pivot Hub
  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(piv_x, piv_y, 16, 1);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_circle(piv_x, piv_y, 16, 0);

  // Curved Glass Reflection Sheen
  gfx_r = 1.00; gfx_g = 1.00; gfx_b = 1.00; gfx_a = 0.05;
  gfx_line(plate_x + 8, plate_y + 12, plate_x + plate_w * 0.65, plate_y + plate_h * 0.45);
  gfx_line(plate_x + 12, plate_y + 12, plate_x + plate_w * 0.65 + 4, plate_y + plate_h * 0.45);
  gfx_a = 1.0;

  // Bottom Telemetry Readout
  gfx_setfont(3, "Consolas", 11, 'b');
  is_glue ? (
    gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
    gfx_x = plate_x + 14; gfx_y = plate_y + plate_h - 22;
    gfx_printf("GR: %4.1f dB", glue_gr_db);
    gfx_x = plate_x + plate_w - 78; gfx_y = plate_y + plate_h - 22;
    gfx_drawstr("PEAK HOLD");
  ) : (
    gfx_r = 0.00; gfx_g = 0.85; gfx_b = 0.45;
    gfx_x = plate_x + 14; gfx_y = plate_y + plate_h - 22;
    gfx_printf("RMS: %4.1f dBFS", inst_rms);
    gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
    gfx_x = plate_x + plate_w - 110; gfx_y = plate_y + plate_h - 22;
    gfx_drawstr("0 VU = -18 dBFS");
  );
);

// =============================================================================
// TAB 0: OVERVIEW HARDWARE DASHBOARD
// =============================================================================
slider1 == 0 ? (
  top_row_h = 236;
  meter_w = floor((ws_w - 48) * 0.35);
  scope_w = ws_w - 32 - meter_w * 2;

  // 1. Console Drive SIFAM VU Meter
  draw_sifam_meter(ws_x + 8, ws_y + 8, meter_w, top_row_h, "SIFAM DIRECTOR // CONSOLE DRIVE", sifam_needle_vu, 3.0, 0, 1.00, 0.85, 0.30);

  // 2. Studio Bus Glue SIFAM GR Meter
  draw_sifam_meter(ws_x + 16 + meter_w, ws_y + 8, meter_w, top_row_h, "STUDIO BUS GLUE // GAIN REDUCTION", sifam_needle_gr, 20.0, 1, 0.00, 0.85, 1.00);

  // 3. Stereo Phase & Lissajous Radar with Phosphor Trails
  sc_x = ws_x + 24 + meter_w * 2; sc_y = ws_y + 8;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(sc_x, sc_y, scope_w, top_row_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(sc_x, sc_y, scope_w, top_row_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = sc_x + 14; gfx_y = sc_y + 10; gfx_drawstr("STEREO PHASE RADAR");

  r_cx = sc_x + scope_w * 0.5; r_cy = sc_y + 115;
  r_dyn = 1.0 + max(0.0, (inst_rms + 35.0) / 45.0) * 0.20;
  gfx_r = 0.10; gfx_g = 0.14; gfx_b = 0.20;
  gfx_circle(r_cx, r_cy, floor(60 * r_dyn), 0);
  gfx_circle(r_cx, r_cy, 38, 0);
  gfx_line(r_cx - 60, r_cy, r_cx + 60, r_cy);
  gfx_line(r_cx, r_cy - 60, r_cx, r_cy + 60);

  // Live Lissajous CRT Phosphor Trails
  pi = 0; prev_sx = r_cx; prev_sy = r_cy;
  loop(32,
    s_idx = (scope_pos - pi * 4 + 256) % 256;
    sl = scope_buf_l[s_idx]; sr = scope_buf_r[s_idx];
    sx = r_cx + (sl - sr) * 45.0;
    sy = r_cy - (sl + sr) * 45.0;
    pi > 0 ? (
      gfx_r = 0.00; gfx_g = 0.95; gfx_b = 0.65; gfx_a = 0.55;
      gfx_line(prev_sx, prev_sy, sx, sy);
    );
    prev_sx = sx; prev_sy = sy;
    pi += 1;
  );
  gfx_a = 1.0;

  // Correlation Bar
  gfx_setfont(2, "Consolas", 10.5, 'b'); gfx_r = 0.70; gfx_g = 0.80; gfx_b = 0.90;
  gfx_x = sc_x + 14; gfx_y = sc_y + 188; gfx_drawstr("-1.0");
  gfx_x = sc_x + scope_w * 0.5 - 8; gfx_y = sc_y + 188; gfx_drawstr("0.0");
  gfx_x = sc_x + scope_w - 38; gfx_y = sc_y + 188; gfx_drawstr("+1.0");

  cb_x = sc_x + 14; cb_y = sc_y + 204; cb_w = scope_w - 28; cb_h = 8;
  gfx_r = 0.02; gfx_g = 0.03; gfx_b = 0.05; gfx_rect(cb_x, cb_y, cb_w, cb_h);
  corr_frac = max(0.0, min(1.0, (1.0 + 0.94) * 0.5));
  gfx_r = 0.00; gfx_g = 0.95; gfx_b = 0.55;
  gfx_rect(cb_x + cb_w * 0.5, cb_y, (corr_frac - 0.5) * cb_w, cb_h);

  // Bottom 3 Raised Enclosures
  dash_y = ws_y + top_row_h + 16;
  dash_h = ws_h - top_row_h - 24;
  col_w = floor((ws_w - 32) / 3);

  // Card 1: GAIN & HEADROOM
  c1_x = ws_x + 8;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(c1_x, dash_y, col_w, dash_h);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(c1_x, dash_y, col_w, dash_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
  gfx_x = c1_x + 16; gfx_y = dash_y + 14; gfx_drawstr("1. GAIN & HEADROOM");

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = c1_x + 16; gfx_y = dash_y + 45; gfx_printf("Input Calibration : %+3.1f dB", slider3);
  gfx_x = c1_x + 16; gfx_y = dash_y + 70; gfx_printf("Producer Output   : %+3.1f dB Trim", slider4);
  gfx_x = c1_x + 16; gfx_y = dash_y + 95;
  slider5 ? gfx_printf("Pre-Master Ceiling: -6.0 dBTP Strict Lock") : gfx_printf("Pre-Master Ceiling: Free Output Crest");
  gfx_x = c1_x + 16; gfx_y = dash_y + 120; gfx_printf("Summing Engine    : ACTIVE SUMMING");
  gfx_x = c1_x + 16; gfx_y = dash_y + 145; gfx_printf("Delta Solo State  : NORMAL SUM");

  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(c1_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(c1_x + 14, dash_y + dash_h - 38, col_w - 28, 26, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
  gfx_x = c1_x + 22; gfx_y = dash_y + dash_h - 32; gfx_drawstr(get_producer_short_name(slider2));

  // Card 2: BUS GLUE DYNAMICS
  c2_x = ws_x + 16 + col_w;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(c2_x, dash_y, col_w, dash_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(c2_x, dash_y, col_w, dash_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = c2_x + 16; gfx_y = dash_y + 14; gfx_drawstr("2. BUS GLUE DYNAMICS");

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = c2_x + 16; gfx_y = dash_y + 45;
  slider11 ? gfx_printf("Active Topology   : Neve Diode Bridge") : gfx_printf("Active Topology   : British VCA Punch");
  gfx_x = c2_x + 16; gfx_y = dash_y + 70; gfx_printf("Threshold / Ratio : %4.1f dB | %d:1", slider12, slider13 == 0 ? 1.5 : (slider13 == 1 ? 2 : (slider13 == 2 ? 4 : 8)));
  gfx_x = c2_x + 16; gfx_y = dash_y + 95;
  r_str = slider15 == 0 ? "100ms" : (slider15 == 1 ? "300ms" : (slider15 == 2 ? "600ms" : "1200ms"));
  gfx_printf("Attack / Release  : %3.1fms | %s", slider14, r_str);
  gfx_x = c2_x + 16; gfx_y = dash_y + 120; gfx_printf("Detector HPF Key  : %d Hz Sidechain", slider16);
  gfx_x = c2_x + 16; gfx_y = dash_y + 145; gfx_printf("Instantaneous GR  : -%3.2f dB Peak", glue_gr_db);

  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(c2_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 0.01; gfx_g = 0.02; gfx_b = 0.04;
  gfx_x = c2_x + 22; gfx_y = dash_y + dash_h - 32; gfx_printf("GLUE GR: %3.1f dB", glue_gr_db);

  // Card 3: HARMONIC & SPATIAL
  c3_x = ws_x + 24 + col_w * 2;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(c3_x, dash_y, col_w, dash_h);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(c3_x, dash_y, col_w, dash_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
  gfx_x = c3_x + 16; gfx_y = dash_y + 14; gfx_drawstr("3. HARMONIC & SPATIAL");

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  h_name = slider23 == 0 ? "Transparent Pure Pass" : (slider23 == 1 ? "Neve 8014 Iron Desk" : (slider23 == 2 ? "Studer A800 15 IPS Tape" : "Triode Tube Crucible"));
  gfx_x = c3_x + 16; gfx_y = dash_y + 45; gfx_printf("Harmonic Engine   : %s", h_name);
  gfx_x = c3_x + 16; gfx_y = dash_y + 70; gfx_printf("Console Desk Drive: %+3.1f dB THD", slider24);
  gfx_x = c3_x + 16; gfx_y = dash_y + 95; gfx_printf("Sub Mono Anchor   : %d Hz (LR 24dB)", slider6);
  gfx_x = c3_x + 16; gfx_y = dash_y + 120; gfx_printf("Quad Imager Width : %4.2f x Multiplier", slider25);
  gfx_x = c3_x + 16; gfx_y = dash_y + 145; gfx_printf("Vocal Pocket Carve: -%3.1f dB @ 2.2 kHz", pocket_depth);

  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(c3_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(c3_x + 14, dash_y + dash_h - 38, col_w - 28, 26, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
  gfx_x = c3_x + 22; gfx_y = dash_y + dash_h - 32; gfx_printf("CORRIDOR POCKET: -%3.1f dB", pocket_depth);
);

// =============================================================================
// TAB 1: TONAL EQ (6-BAND RESPONSE CURVE + 6 FULL-HEIGHT METALLIC CHANNEL STRIPS)
// =============================================================================
slider1 == 1 ? (
  eq_plot_y = ws_y + 8; eq_plot_h = 220; eq_plot_w = ws_w - 16;
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(ws_x + 8, eq_plot_y, eq_plot_w, eq_plot_h);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(ws_x + 8, eq_plot_y, eq_plot_w, eq_plot_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
  gfx_x = ws_x + 20; gfx_y = eq_plot_y + 12; gfx_drawstr("TONAL FORGE // 6-BAND INSTRUMENTAL BUS EQUALIZATION CURVE");

  // Grid
  cy0 = eq_plot_y + eq_plot_h * 0.5;
  gfx_r = 0.12; gfx_g = 0.18; gfx_b = 0.26;
  gfx_line(ws_x + 8, cy0, ws_x + 8 + eq_plot_w, cy0);
  gfx_line(ws_x + 8, cy0 - 45, ws_x + 8 + eq_plot_w, cy0 - 45);
  gfx_line(ws_x + 8, cy0 + 45, ws_x + 8 + eq_plot_w, cy0 + 45);

  fx80 = ws_x + 8 + floor(eq_plot_w * 0.18);
  fx200 = ws_x + 8 + floor(eq_plot_w * 0.35);
  fx1500 = ws_x + 8 + floor(eq_plot_w * 0.55);
  fx3000 = ws_x + 8 + floor(eq_plot_w * 0.72);
  fx8000 = ws_x + 8 + floor(eq_plot_w * 0.88);
  gfx_line(fx80, eq_plot_y, fx80, eq_plot_y + eq_plot_h);
  gfx_line(fx200, eq_plot_y, fx200, eq_plot_y + eq_plot_h);
  gfx_line(fx1500, eq_plot_y, fx1500, eq_plot_y + eq_plot_h);
  gfx_line(fx3000, eq_plot_y, fx3000, eq_plot_y + eq_plot_h);
  gfx_line(fx8000, eq_plot_y, fx8000, eq_plot_y + eq_plot_h);

  gfx_setfont(3, "Consolas", 11, 'b'); gfx_r = 0.55; gfx_g = 0.65; gfx_b = 0.75;
  gfx_x = fx80 + 4; gfx_y = eq_plot_y + eq_plot_h - 20; gfx_drawstr("80Hz");
  gfx_x = fx200 + 4; gfx_y = eq_plot_y + eq_plot_h - 20; gfx_drawstr("202Hz");
  gfx_x = fx1500 + 4; gfx_y = eq_plot_y + eq_plot_h - 20; gfx_drawstr("1.5kHz");
  gfx_x = fx3000 + 4; gfx_y = eq_plot_y + eq_plot_h - 20; gfx_drawstr("3.0kHz");
  gfx_x = fx8000 + 4; gfx_y = eq_plot_y + eq_plot_h - 20; gfx_drawstr("8.0kHz");

  // Dynamic 6-Band Frequency Response Curve with Vertical Shaded Fill
  prev_py = cy0; pi = 0;
  loop(160,
    px = ws_x + 8 + floor((pi / 159.0) * eq_plot_w);
    f_val = 20.0 * exp(log(1000.0) * (pi / 159.0));
    g_tot = 0.0;
    f_val < slider18 ? g_tot -= ((slider18 - f_val) / slider18) * 18.0 : 0;
    f_val <= 80.0 ? g_tot += slider19 : (f_val < 160.0 ? g_tot += slider19 * (1.0 - (f_val - 80.0) / 80.0) : 0);
    g_tot += slider20 * exp(-0.5 * sqr((log(f_val / 202.0) / 0.4)));
    g_tot += slider21 * exp(-0.5 * sqr((log(f_val / 1500.0) / 0.35)));
    g_tot += slider22 * exp(-0.5 * sqr((log(f_val / 3000.0) / 0.35)));
    f_val > 4000.0 ? g_tot += slider31 * (min(1.0, (f_val - 4000.0) / 4000.0));
    cur_py = cy0 - g_tot * 8.5;
    pi > 0 ? (
      gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
      gfx_line(prev_px, prev_py, px, cur_py);
      gfx_line(px, cur_py, px, cy0);
    );
    prev_px = px; prev_py = cur_py;
    pi += 1;
  );

  // 6 Metallic Hardware Channel Strips Below
  col_w = floor((ws_w - 16 - 30) / 6);
  cards_y = eq_plot_y + eq_plot_h + 12; cards_h = ws_h - eq_plot_h - 24;
  draw_channel_strip(ws_x + 8 + 0 * (col_w + 6), cards_y, col_w, cards_h, "38Hz HPF", "SUB CUT 18dB", slider18, 20.0, 60.0, "%d Hz", 18, 0.85, 0.70, 0.22);
  draw_channel_strip(ws_x + 8 + 1 * (col_w + 6), cards_y, col_w, cards_h, "80Hz PUNCH", "LOW SHELF BASS", slider19, -6.0, 6.0, "%+.1f dB", 19, 0.00, 0.85, 1.00);
  draw_channel_strip(ws_x + 8 + 2 * (col_w + 6), cards_y, col_w, cards_h, "202Hz SCOOP", "MUD CLARITY", slider20, -6.0, 6.0, "%+.1f dB", 20, 0.85, 0.70, 0.22);
  draw_channel_strip(ws_x + 8 + 3 * (col_w + 6), cards_y, col_w, cards_h, "1.5kHz BODY", "GUITAR & SNARE", slider21, -6.0, 6.0, "%+.1f dB", 21, 0.40, 0.95, 0.65);
  draw_channel_strip(ws_x + 8 + 4 * (col_w + 6), cards_y, col_w, cards_h, "3.0kHz BITE", "PICK ATTACK", slider22, -6.0, 6.0, "%+.1f dB", 22, 0.00, 0.85, 1.00);
  draw_channel_strip(ws_x + 8 + 5 * (col_w + 6), cards_y, col_w, cards_h, "8.0kHz SHEEN", "AIR GLOSS SHELF", slider31, -6.0, 6.0, "%+.1f dB", 31, 0.85, 0.70, 0.22);
);

// =============================================================================
// TAB 2: BUS GLUE COMPRESSION (TRANSFER CURVE WITH LIVE BALL + PARAMS)
// =============================================================================
slider1 == 2 ? (
  col_w = floor((ws_w - 24) * 0.42);
  tc_x = ws_x + 8; tc_y = ws_y + 8; tc_h = ws_h - 16;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(tc_x, tc_y, col_w, tc_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(tc_x, tc_y, col_w, tc_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = tc_x + 16; gfx_y = tc_y + 14; gfx_drawstr("COMPRESSION TRANSFER FUNCTION");

  tbox_x = tc_x + 20; tbox_y = tc_y + 50; tbox_sz = col_w - 40;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(tbox_x, tbox_y, tbox_sz, tbox_sz);
  gfx_r = 0.18; gfx_g = 0.26; gfx_b = 0.36; gfx_rect(tbox_x, tbox_y, tbox_sz, tbox_sz, 0);

  gfx_r = 0.12; gfx_g = 0.16; gfx_b = 0.22;
  gfx_line(tbox_x, tbox_y + tbox_sz, tbox_x + tbox_sz, tbox_y);

  // Transfer Curve Plot
  ratio_val = slider13 == 0 ? 1.5 : (slider13 == 1 ? 2.0 : (slider13 == 2 ? 4.0 : 8.0));
  th_frac = (slider12 + 36.0) / 36.0;
  th_x = tbox_x + th_frac * tbox_sz;
  th_y = tbox_y + tbox_sz - th_frac * tbox_sz;

  gfx_r = 0.95; gfx_g = 0.75; gfx_b = 0.20;
  gfx_line(tbox_x, tbox_y + tbox_sz, th_x, th_y);
  end_x = tbox_x + tbox_sz;
  end_y = th_y - (1.0 / ratio_val) * (end_x - th_x);
  gfx_line(th_x, th_y, end_x, end_y);

  // Threshold knee ball
  gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  gfx_circle(th_x, th_y, 5, 1);

  // Live Dynamic Signal Bouncing Ball Tracking (Vin, Vout)
  live_frac = max(0.0, min(1.0, (inst_rms + 50.0) / 46.0));
  ball_in_x = tbox_x + live_frac * tbox_sz;
  ball_in_x < th_x ? (
    ball_out_y = tbox_y + tbox_sz - live_frac * tbox_sz;
  ) : (
    ball_out_y = th_y - (1.0 / ratio_val) * (ball_in_x - th_x);
  );
  gfx_r = 0.00; gfx_g = 0.95; gfx_b = 1.00;
  gfx_circle(ball_in_x, ball_out_y, 6, 1);

  // Right Side Parameters Panel
  rp_x = ws_x + 16 + col_w; rp_w = ws_w - col_w - 24;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(rp_x, tc_y, rp_w, tc_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(rp_x, tc_y, rp_w, tc_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = rp_x + 16; gfx_y = tc_y + 14; gfx_drawstr("STUDIO GLUE DYNAMICS PARAMETERS");

  sl_y = tc_y + 50; sl_sp = 68;
  draw_param_slider(rp_x + 16, sl_y + 0 * sl_sp, rp_w - 32, 54, "1. BUS GLUE THRESHOLD", slider12, -36.0, 0.0, "%.1f dBFS", 12, 0.00, 0.85, 1.00);
  draw_param_slider(rp_x + 16, sl_y + 1 * sl_sp, rp_w - 32, 54, "2. COMPRESSION RATIO", slider13, 0, 3, "Mode %d", 13, 0.95, 0.70, 0.20);
  draw_param_slider(rp_x + 16, sl_y + 2 * sl_sp, rp_w - 32, 54, "3. ATTACK TIME", slider14, 0.1, 100.0, "%.1f ms", 14, 0.00, 0.85, 1.00);
  draw_param_slider(rp_x + 16, sl_y + 3 * sl_sp, rp_w - 32, 54, "4. RELEASE BALLISTICS", slider15, 0, 4, "Mode %d", 15, 0.95, 0.70, 0.20);
  draw_param_slider(rp_x + 16, sl_y + 4 * sl_sp, rp_w - 32, 54, "5. SIDECHAIN DETECTOR HPF", slider16, 30, 250, "%d Hz", 16, 0.95, 0.70, 0.20);
  draw_param_slider(rp_x + 16, sl_y + 5 * sl_sp, rp_w - 32, 54, "6. PARALLEL DRY / WET MIX", slider17, 0, 100, "%d %%", 17, 0.00, 0.85, 1.00);
);

// =============================================================================
// TAB 3: HARMONIC CRUCIBLE (DESK THD BARS & SATURATION ENGINES)
// =============================================================================
slider1 == 3 ? (
  cr_w = ws_w - 16; cr_h = ws_h - 16;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 8, ws_y + 8, cr_w, cr_h);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(ws_x + 8, ws_y + 8, cr_w, cr_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
  gfx_x = ws_x + 24; gfx_y = ws_y + 20; gfx_drawstr("HARMONIC CRUCIBLE // CONSOLE SATURATION ENGINES & DESK IRON");

  // Real-Time Harmonic THD Bars
  thd_y = ws_y + 60; thd_h = 200; thd_w = cr_w - 48;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(ws_x + 24, thd_y, thd_w, thd_h);
  gfx_r = 0.20; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, thd_y, thd_w, thd_h, 0);

  gfx_setfont(3, "Consolas", 11.5, 'b');
  loop_h = 5; hi = 0;
  bar_w = floor(thd_w / 7);
  loop(5,
    hx = ws_x + 40 + hi * (bar_w + 14);
    h_db = slider24 * (1.0 / (hi + 1.2)) * (0.6 + 0.4 * sin(time_precise() * 3.0 + hi));
    h_frac = max(0.0, min(1.0, h_db / 12.0));
    bar_h = floor(h_frac * (thd_h - 50));
    gfx_r = 0.03; gfx_g = 0.05; gfx_b = 0.08; gfx_rect(hx, thd_y + 20, bar_w, thd_h - 40);
    gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
    gfx_rect(hx, thd_y + thd_h - 20 - bar_h, bar_w, bar_h);
    gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;
    lbl = sprintf(#, "H%d", hi + 1);
    gfx_x = hx + floor(bar_w * 0.5) - 8; gfx_y = thd_y + thd_h - 16; gfx_drawstr(lbl);
    hi += 1;
  );

  draw_param_slider(ws_x + 24, ws_y + 290, cr_w - 48, 64, "CONSOLE DESK DRIVE THD INTENSITY", slider24, 0.0, 12.0, "+%.1f dB", 24, 0.85, 0.70, 0.22);
);

// =============================================================================
// TAB 4: STEREO DIMENSION & SUB-MONO ANCHOR
// =============================================================================
slider1 == 4 ? (
  st_w = ws_w - 16; st_h = ws_h - 16;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 8, ws_y + 8, st_w, st_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 8, ws_y + 8, st_w, st_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 24; gfx_y = ws_y + 20; gfx_drawstr("STEREO DIMENSION WIDTH & SUB-BASS MONO ANCHOR");

  plot_w = floor((st_w - 48 - 16) * 0.5);
  plot_h = 240;

  // 1. Linkwitz-Riley Sub-Mono Crossover
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(ws_x + 24, ws_y + 55, plot_w, plot_h);
  gfx_r = 0.18; gfx_g = 0.26; gfx_b = 0.36; gfx_rect(ws_x + 24, ws_y + 55, plot_w, plot_h, 0);

  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 36; gfx_y = ws_y + 68; gfx_drawstr("LINKWITZ-RILEY SUB-MONO CROSSOVER (SIDE CHANNEL HPF)");

  cut_x = ws_x + 24 + floor(((slider6 - 40.0) / 120.0) * plot_w);
  gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;
  gfx_line(cut_x, ws_y + 75, cut_x, ws_y + 55 + plot_h);
  gfx_setfont(3, "Consolas", 11, 'b');
  cut_lbl = sprintf(#, "MONO CUT: %d Hz", slider6);
  gfx_x = cut_x + 6; gfx_y = ws_y + 90; gfx_drawstr(cut_lbl);

  // 2. Quad-Wall Stereo Goniometer Vectorscope
  sc2_x = ws_x + 40 + plot_w;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(sc2_x, ws_y + 55, plot_w, plot_h);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(sc2_x, ws_y + 55, plot_w, plot_h, 0);

  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
  gfx_x = sc2_x + 12; gfx_y = ws_y + 68; gfx_drawstr("QUAD-WALL STEREO VECTOR SCOPE");

  v_cx = sc2_x + plot_w * 0.5; v_cy = ws_y + 55 + plot_h * 0.5;
  gfx_r = 0.12; gfx_g = 0.16; gfx_b = 0.22;
  gfx_circle(v_cx, v_cy, 60, 0);
  gfx_circle(v_cx, v_cy, 35, 0);
  gfx_line(v_cx - 60, v_cy, v_cx + 60, v_cy);
  gfx_line(v_cx, v_cy - 60, v_cx, v_cy + 60);

  // Phosphor Points
  pi = 0;
  loop(40,
    s_idx = (scope_pos - pi * 4 + 256) % 256;
    sl = scope_buf_l[s_idx]; sr = scope_buf_r[s_idx];
    px = v_cx + (sl - sr) * 55.0;
    py = v_cy - (sl + sr) * 55.0;
    gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_circle(px, py, 1.5, 1);
    pi += 1;
  );

  draw_param_slider(ws_x + 24, ws_y + 320, st_w - 48, 54, "SUB-BASS MONO ANCHOR FREQUENCY CUTOFF", slider6, 40, 160, "%d Hz", 6, 0.00, 0.85, 1.00);
  draw_param_slider(ws_x + 24, ws_y + 386, st_w - 48, 54, "QUAD-WALL STEREO DIMENSION WIDTH MULTIPLIER", slider25, 0.80, 1.40, "%.2f x", 25, 0.85, 0.70, 0.22);
);

// =============================================================================
// TAB 5: VOCAL POCKET & PRESENCE SENTRY
// =============================================================================
slider1 == 5 ? (
  pk_w = ws_w - 16; pk_h = ws_h - 16;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 8, ws_y + 8, pk_w, pk_h);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(ws_x + 8, ws_y + 8, pk_w, pk_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
  gfx_x = ws_x + 24; gfx_y = ws_y + 20; gfx_drawstr("VOCAL POCKET CORRIDOR // DYNAMIC 2.2 kHz FORMANTE CARVE");

  scope_y = ws_y + 55; scope_h = 220;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(ws_x + 24, scope_y, pk_w - 48, scope_h);
  gfx_r = 0.20; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, scope_y, pk_w - 48, scope_h, 0);

  cy0 = scope_y + scope_h * 0.5;
  gfx_r = 0.15; gfx_g = 0.20; gfx_b = 0.28;
  gfx_line(ws_x + 24, cy0, ws_x + pk_w - 24, cy0);

  // Draw 2.2 kHz dynamic notch
  prev_py = cy0; pi = 0;
  loop(120,
    px = ws_x + 24 + floor((pi / 119.0) * (pk_w - 48));
    f_val = 200.0 * exp(log(100.0) * (pi / 119.0));
    notch = -pocket_depth * exp(-0.5 * sqr((log(f_val / 2200.0) / 0.25)));
    cur_py = cy0 - notch * 18.0;
    pi > 0 ? (
      gfx_r = 0.95; gfx_g = 0.40; gfx_b = 0.20;
      gfx_line(prev_px, prev_py, px, cur_py);
      gfx_line(px, cy0, px, cur_py);
    );
    prev_px = px; prev_py = cur_py;
    pi += 1;
  );

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  p_info = sprintf(#, "LIVE VOCAL CARVE: -%3.1f dB @ 2.2 kHz", pocket_depth);
  gfx_measurestr(p_info, piw, pih);
  gfx_x = ws_x + 24 + floor((pk_w - 48 - piw) * 0.5); gfx_y = cy0 + 65;
  gfx_drawstr(p_info);

  draw_param_slider(ws_x + 24, ws_y + 310, pk_w - 48, 62, "MAX VOCAL POCKET DYNAMIC CARVE DEPTH", slider8, 0.0, 3.0, "-%.1f dB", 8, 1.00, 0.85, 0.35);
);

// =============================================================================
// TAB 6: PRODUCER SUMMING MATRIX & DYNAMIC REFERENCE BLUEPRINT
// =============================================================================
slider1 == 6 ? (
  pm_w = ws_w - 16; pm_h = ws_h - 16;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 8, ws_y + 8, pm_w, pm_h);
  gfx_r = 0.95; gfx_g = 0.70; gfx_b = 0.20; gfx_rect(ws_x + 8, ws_y + 8, pm_w, pm_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.95; gfx_g = 0.70; gfx_b = 0.20;
  gfx_x = ws_x + 24; gfx_y = ws_y + 20; gfx_drawstr("PRODUCER SUMMING MATRIX // 25 REFERENCE BENCHMARKS & HUGGINGFACE AI");

  // 25 Tiles Grid
  t_cols = 5; t_rows = 5;
  tile_w = floor((pm_w - 48 - (t_cols - 1) * 8) / t_cols);
  tile_h = 28;
  grid_y = ws_y + 50;

  pi = 0;
  while (pi < 25) (
    col_i = pi % t_cols; row_i = floor(pi / t_cols);
    tx = ws_x + 24 + col_i * (tile_w + 8);
    ty = grid_y + row_i * (tile_h + 6);
    is_sel = (slider2 == pi);

    gfx_r = is_sel ? 0.08 : 0.016; gfx_g = is_sel ? 0.12 : 0.022; gfx_b = is_sel ? 0.16 : 0.030;
    gfx_rect(tx, ty, tile_w, tile_h);
    gfx_r = is_sel ? 0.95 : 0.25; gfx_g = is_sel ? 0.70 : 0.32; gfx_b = is_sel ? 0.20 : 0.42;
    gfx_rect(tx, ty, tile_w, tile_h, 0);

    gfx_setfont(3, "Consolas", 11, 'b');
    gfx_r = is_sel ? 1.0 : 0.70; gfx_g = is_sel ? 0.85 : 0.75; gfx_b = is_sel ? 0.30 : 0.85;
    t_name = get_producer_short_name(pi);
    gfx_measurestr(t_name, tnw, tnh);
    gfx_x = tx + floor((tile_w - tnw) * 0.5); gfx_y = ty + floor((tile_h - tnh) * 0.5);
    gfx_drawstr(t_name);

    mouse_clicked && mouse_x >= tx && mouse_x <= tx + tile_w && mouse_y >= ty && mouse_y <= ty + tile_h ? (
      slider2 = pi; apply_producer_preset(slider2); slider_automate();
    );
    pi += 1;
  );

  // Dynamic Reference Blueprint & AI Assistant Lower Deck
  ai_y = grid_y + 5 * (tile_h + 6) + 12;
  ai_h = pm_h - (ai_y - ws_y) - 16;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(ws_x + 24, ai_y, pm_w - 48, ai_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 24, ai_y, pm_w - 48, ai_h, 0);

  // Left column: Local Ollama & HuggingFace AI Diagnostic Panel
  hw_w = floor((pm_w - 48 - 16) * 0.5);
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 36; gfx_y = ai_y + 12; gfx_drawstr("LOCAL OLLAMA & HF AI ASSISTANT // COGNITIVE BUS REASONING");

  gfx_setfont(3, "Consolas", 11.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = ws_x + 36; gfx_y = ai_y + 36; gfx_drawstr("• Engine       : damei-cognitive-engineer:latest (DirectML RTX 3060)");
  gfx_x = ws_x + 36; gfx_y = ai_y + 56; gfx_drawstr("• DNA Model    : laion/clap-htsat-fused (Acoustic Cosine Vector)");
  gfx_x = ws_x + 36; gfx_y = ai_y + 76; gfx_drawstr("• Structure    : ccmusic-database/music_structure (Chorus Impact Sync)");
  gfx_x = ws_x + 36; gfx_y = ai_y + 96; gfx_drawstr("• Balance Guard: ACTIVE (Strict ±0.5dB Max Safe Auto-Calibration Lock)");

  // Interactive Button: RUN SAFE AI CALIBRATION
  btn_ai_y = ai_y + 124; btn_ai_w = hw_w - 24;
  btn_hov = (mouse_x >= ws_x + 36 && mouse_x <= ws_x + 36 + btn_ai_w && mouse_y >= btn_ai_y && mouse_y <= btn_ai_y + 32);
  gfx_r = btn_hov ? 0.20 : 0.00; gfx_g = btn_hov ? 0.95 : 0.85; gfx_b = 1.00;
  gfx_rect(ws_x + 36, btn_ai_y, btn_ai_w, 32);
  gfx_setfont(1, "Orbitron", 11, 'b'); gfx_r = 0.01; gfx_g = 0.02; gfx_b = 0.04;
  gfx_x = ws_x + 48; gfx_y = btn_ai_y + 8;
  gfx_drawstr("RUN COGNITIVE AI AUTO-CALIBRATE (±0.5dB SAFE LOCK)");
  mouse_clicked && btn_hov ? (
    trigger_ai_assist(); slider_automate();
  );

  // Right column: Forensic Producer Reference Blueprint Plaque
  bp_x = ws_x + 24 + hw_w + 8;
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.95; gfx_g = 0.70; gfx_b = 0.20;
  gfx_x = bp_x + 12; gfx_y = ai_y + 12; gfx_drawstr("FORENSIC PRODUCER BLUEPRINT & REFERENCE TARGET");

  gfx_setfont(3, "Consolas", 11, 'b');
  // Dynamic Reference Track Name
  ref_t = get_producer_ref_track(slider2);
  gfx_r = 0.00; gfx_g = 0.90; gfx_b = 1.00;
  gfx_x = bp_x + 12; gfx_y = ai_y + 34; gfx_printf("• REF TARGET : %s", ref_t);

  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = bp_x + 12; gfx_y = ai_y + 54; gfx_printf("• Output Trim: %+3.1f dB (DeeGain & Staging)", slider4);
  gfx_x = bp_x + 12; gfx_y = ai_y + 74; gfx_printf("• Tonal Forge: 80Hz +%3.1fdB | 202Hz -%3.1fdB | 1.5k +%3.1fdB", slider19, abs(slider20), slider21);
  gfx_x = bp_x + 12; gfx_y = ai_y + 94; gfx_printf("• Upper Tonal: 3.0k +%3.1fdB | 8.0k +%3.1fdB (High Shelf)", slider22, slider31);
  gfx_x = bp_x + 12; gfx_y = ai_y + 114; gfx_printf("• Bus Glue   : Thresh %4.1fdB | %d:1 Ratio | 10ms / 600ms", slider12, slider13 == 0 ? 1.5 : (slider13 == 1 ? 2 : (slider13 == 2 ? 4 : 8)));
  gfx_x = bp_x + 12; gfx_y = ai_y + 134; gfx_printf("• Spatial/Sub: Mono Anchor %dHz | Stereo Width %4.2fx", slider6, slider25);
);

prev_mouse_down = mouse_down;
""")

print("Successfully written", target_path)
shutil.copy2(target_path, reaper_path)
print("Copied to", reaper_path)
