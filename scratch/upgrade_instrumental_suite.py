# Python script to build the upgraded Damei_InstrumentalSuite.jsfx
import os, shutil

target_path = r"c:\Dev\DameiSuite\effects\Damei_InstrumentalSuite.jsfx"
reaper_path = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_InstrumentalSuite.jsfx"

# Build the complete JSFX source code for Instrumental Bus Suite
code = r"""desc:Damei Instrumental Bus Alchemist (Harmonic Crucible & Summing Matrix)
// =============================================================================
// DAMEI SUITE // 2026 REAPER MASTER SUMMING INFRASTRUCTURE
// ARCHETYPE: FUNTUNFUNEFU-DENKYEMFUNEFU (Collective Summing & Unified Destiny)
// LUXURY CONSOLE SURFACE ARCHITECTURE (@gfx 1080 700)
// =============================================================================

slider1:0<0,6,1{0: OVERVIEW, 1: TONAL EQ, 2: BUS GLUE, 3: CRUCIBLE, 4: STEREO, 5: POCKET, 6: PRODUCER}>-Active Navigation Tab
slider2:6<0,24,1{00: Default Unity Baseline (1:1 Pass), 01: Lance Prenc (Alpha Wolf / Polaris), 02: Scott Seigel (DIESECT), 03: Jonathan Dolese (Mirrorcell), 04: Buster Odeholm (thrown / Northlane), 05: Lewis Johns (Love Is Noise / blanket), 06: Kel Pinchin (Split Chain Target), 07: Dan Lancaster & Jason Perry (Don Broco), 08: Erik Bickerstaffe (Static Dress), 09: Sam Guaiana (Silverstein / TDWP), 10: Zach Tuch (Heavenward / Hundredth), 11: Forrester Savell (Karnivool), 12: Leon Schmidt (SUNBORN - Nebula), 13: Ermin Hamidovic (Systematic Reference), 14: Will Putney (Fit For An Autopsy), 15: George Lever (Sleep Token / Loathe), 16: Sam Bassal (Thornhill - nerv), 17: Henrik Udd (Architects - Gravity), 18: Dan Braunstein (Spiritbox), 19: Zakk Cervini & Erik Ron (Bad Omens), 20: Jens Bogren (Fascination Street), 21: Adam Nolly Getgood (Periphery / GGD), 22: Acle Kahney (TesseracT - King), 23: Adam Cichocki (heaving. / Timber), 24: Manuel Renner (SENNA / Uberlarm)}>-Producer Benchmark Matrix
slider3:0<-6.0,6.0,0.1>-Input Calibration Gain (dB)
slider4:-3.0<-6.0,6.0,0.1>-Producer Headroom Trim (dB)
slider5:1<0,1,1{Free Output, -6.0 dBTP Strict Pre-Master Lock}>-Headroom Guardian Mode
slider6:80<40,160,1>-Sub-Bass Mono Anchor Cutoff (Hz)
slider7:1<0,1,1{Bypass, Active Sentry}>-Kick/Bass Transient Sentry
slider8:0.8<0.0,3.0,0.1>-Vocal Pocket Dynamic Notch Depth (dB)
slider9:1<0,1,1{Manual Lock, gmem Auto-Sensing}>-Vocal Pocket Corridor Mode
slider10:1<0,1,1{Bypass, Engaged}>-Master Bus Glue Compressor
slider11:0<0,1,1{British VCA Punch, Neve Diode Bridge Vintage}>-Bus Glue Topology
slider12:-6.0<-36.0,0.0,0.5>-Bus Glue Threshold (dB)
slider13:2<0,3,1{1.5:1 Subtle, 2:1 Master Glue, 4:1 Modern Punch, 8:1 Heavy Squeeze}>-Bus Glue Ratio
slider14:10.0<0.1,100.0,0.5>-Bus Glue Attack (ms)
slider15:2<0,4,1{100ms Fast, 300ms Snappy, 600ms Classical, 1200ms Smooth, Auto Ballistics}>-Bus Glue Release
slider16:80<30,250,1>-Bus Glue Sidechain Detector HPF (Hz)
slider17:100<0,100,1>-Bus Glue Dry/Wet Mix (%)
slider18:32<20,60,1>-Tonal Forge HPF Cutoff (Hz)
slider19:3.0<-6.0,6.0,0.1>-Tonal Forge 80Hz Punch (dB)
slider20:-3.0<-6.0,6.0,0.1>-Tonal Forge 220Hz Mud Scoop (dB)
slider21:3.0<-6.0,6.0,0.1>-Tonal Forge 3.5kHz Bite (dB)
slider22:3.0<-6.0,6.0,0.1>-Tonal Forge 10kHz Sheen (dB)
slider23:1<0,3,1{Transparent Pure Pass, Neve 8014 Iron Desk, Studer A800 15 IPS Tape, Triode Tube Crucible}>-Harmonic Saturation Engine
slider24:2.5<0.0,12.0,0.1>-Harmonic Desk Drive (dB)
slider25:1.08<0.80,1.40,0.01>-Quad-Wall Stereo Imager Width
slider26:1<0,1,1{Bypass, Active Chorus Sync}>-Song Structure Chorus Impact
slider27:1<0,1,1{Bypass 1:1 Unity, Engaged Active Summing}>-Master Suite Processing State
slider28:0<0,1,1{Normal Processing, Delta Solo Audition}>-Delta Solo Audition
slider29:0<0,1,1{Snapshot A, Snapshot B}>-A/B Comparison Snapshot
slider30:0<0,1,1{Stereo Summing, Mid/Side Summing}>-Master Processing Mode

in_pin:Instrumental In L
in_pin:Instrumental In R
in_pin:Sidechain Vocal Key L
in_pin:Sidechain Vocal Key R
out_pin:Master Music Sum L
out_pin:Master Music Sum R

options:no_meter
options:gmem=DameiMixMetering
options:maxmem=65536

@init
ext_noinit = 1.0;
M_PI = 3.14159265358979323846;

// Memory partitioning
ab_mem_a = 1000;
ab_mem_b = 1050;

// Filter state memories (Fully isolated Left & Right delay lines)
hpf_x1_l = 0; hpf_x2_l = 0; hpf_y1_l = 0; hpf_y2_l = 0;
hpf_x1_r = 0; hpf_x2_r = 0; hpf_y1_r = 0; hpf_y2_r = 0;

p80_x1_l = 0; p80_x2_l = 0; p80_y1_l = 0; p80_y2_l = 0;
p80_x1_r = 0; p80_x2_r = 0; p80_y1_r = 0; p80_y2_r = 0;

s280_x1_l = 0; s280_x2_l = 0; s280_y1_l = 0; s280_y2_l = 0;
s280_x1_r = 0; s280_x2_r = 0; s280_y1_r = 0; s280_y2_r = 0;

b3k_x1_l = 0; b3k_x2_l = 0; b3k_y1_l = 0; b3k_y2_l = 0;
b3k_x1_r = 0; b3k_x2_r = 0; b3k_y1_r = 0; b3k_y2_r = 0;

s10k_x1_l = 0; s10k_x2_l = 0; s10k_y1_l = 0; s10k_y2_l = 0;
s10k_x1_r = 0; s10k_x2_r = 0; s10k_y1_r = 0; s10k_y2_r = 0;

pock_x1 = 0; pock_x2 = 0; pock_y1 = 0; pock_y2 = 0;

// Sub-Mono Elliptical Filter memory (High-Pass on Side channel only - Mid 100% Phase-Preserved)
sm_hp_x1 = 0; sm_hp_x2 = 0; sm_hp_y1 = 0; sm_hp_y2 = 0;

// Bus Glue Detector HPF state
sc_x1 = 0.0; sc_x2 = 0.0; sc_y1 = 0.0; sc_y2 = 0.0;

vu_rms_smooth = 0.0;

// Compressor ballistics state
comp_env = 0.0;
glue_gr_db = 0.0;
sifam_desk_needle = 0.0;
sifam_glue_needle = 0.0;

// Live metering
inst_peak = 0.0;
inst_rms = 0.0;
cur_phase_corr = 1.0;
rms_acc_l = 0.0;
rms_acc_r = 0.0;
rms_cnt = 0;

// Shared memory telemetry registration (Instrumental: 1400..1449)
gmem[1400] = 1; // Handshake heartbeat

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
  idx == 23 ? "23: CICHOCKI" :
  "24: RENNER"
);

function get_producer_full_title(idx) (
  idx == 0  ? "Default Unity Baseline (1:1 Transparent Pass)" :
  idx == 1  ? "Lance Prenc (Alpha Wolf / Polaris - Razor Punch)" :
  idx == 2  ? "Scott Seigel (DIESECT - Aggressive Low-End)" :
  idx == 3  ? "Jonathan Dolese (Mirrorcell / Cane Hill - Thick Tube Warmth)" :
  idx == 4  ? "Buster Odeholm (thrown / Northlane - Modern Thall Weight)" :
  idx == 5  ? "Lewis Johns (Love Is Noise / blanket - Atmospheric Tape Glue)" :
  idx == 6  ? "Kel Pinchin (Currents / Invent Animate - Modern Precision)" :
  idx == 7  ? "Dan Lancaster & Jason Perry (Don Broco - Stadium Energy)" :
  idx == 8  ? "Erik Bickerstaffe (Static Dress - Raw Analog Grit)" :
  idx == 9  ? "Sam Guaiana (Silverstein / TDWP - Polished Punch)" :
  idx == 10 ? "Zach Tuch (Heavenward / Hundredth - Vintage Bloom)" :
  idx == 11 ? "Forrester Savell (Karnivool / Twelve Foot Ninja - Prog Clarity)" :
  idx == 12 ? "Leon Schmidt (SUNBORN - Nebula - Ambient Tape Sheen)" :
  idx == 13 ? "Ermin Hamidovic (Systematic Reference - Benchmark Precision)" :
  idx == 14 ? "Will Putney (Fit For An Autopsy / Knocked Loose - Heavy Slap)" :
  idx == 15 ? "George Lever (Sleep Token / Loathe - Massive Dynamic Range)" :
  idx == 16 ? "Sam Bassal (Thornhill - nerv - Modern Electro-Metal Glue)" :
  idx == 17 ? "Henrik Udd (Architects / BMTH - Wall of Heavy Guitars)" :
  idx == 18 ? "Dan Braunstein (Spiritbox / Dayseeker - Hyper-Modern Air)" :
  idx == 19 ? "Zakk Cervini & Erik Ron (Bad Omens - Radio Polished Punch)" :
  idx == 20 ? "Jens Bogren (Fascination Street - European Grandeur)" :
  idx == 21 ? "Adam Nolly Getgood (Periphery / GGD - Surgical Punch)" :
  idx == 22 ? "Acle Kahney (TesseracT - King - Hi-Fi Pristine Space)" :
  idx == 23 ? "Adam Cichocki (heaving. / Timber - Raw Alt-Metal Crush)" :
  "Manuel Renner (SENNA / Uberlarm - Modern European Precision)"
);

function update_filters() local(w0, alpha, A, beta, cos_w0, sin_w0) (
  srate <= 0 ? srate = 44100;
  // 1. HPF Cutoff (slider18)
  w0 = 2.0 * M_PI * clamp(slider18, 20.0, 100.0) / srate;
  alpha = sin(w0) / (2.0 * 0.7071);
  hpf_b0 = (1.0 + cos(w0)) * 0.5;
  hpf_b1 = -(1.0 + cos(w0));
  hpf_b2 = (1.0 + cos(w0)) * 0.5;
  hpf_a0 = 1.0 + alpha;
  hpf_a1 = -2.0 * cos(w0);
  hpf_a2 = 1.0 - alpha;

  // 2. 80Hz Punch Low Shelf (slider19) - Authentic warm bottom foundation
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

  // 3. 220Hz Mud Scoop (slider20) - Precisely eliminates 200Hz boxiness
  A = exp(slider20 * 0.0575646273);
  w0 = 2.0 * M_PI * 220.0 / srate;
  alpha = sin(w0) / (2.0 * 1.1);
  s280_b0 = 1.0 + alpha * A;
  s280_b1 = -2.0 * cos(w0);
  s280_b2 = 1.0 - alpha * A;
  s280_a0 = 1.0 + alpha / A;
  s280_a1 = -2.0 * cos(w0);
  s280_a2 = 1.0 - alpha / A;

  // 4. 3.5kHz Bite (slider21) - Articulation & Pick Attack
  A = exp(slider21 * 0.0575646273);
  w0 = 2.0 * M_PI * 3500.0 / srate;
  alpha = sin(w0) / (2.0 * 1.1);
  b3k_b0 = 1.0 + alpha * A;
  b3k_b1 = -2.0 * cos(w0);
  b3k_b2 = 1.0 - alpha * A;
  b3k_a0 = 1.0 + alpha / A;
  b3k_a1 = -2.0 * cos(w0);
  b3k_a2 = 1.0 - alpha / A;

  // 5. 10kHz Sheen High Shelf (slider22) - Air sheen
  A = exp(slider22 * 0.0575646273);
  w0 = 2.0 * M_PI * 10000.0 / srate;
  alpha = sin(w0) / (2.0 * 0.7071);
  beta = 2.0 * sqrt(A) * alpha;
  s10k_b0 = A * ((A + 1.0) + (A - 1.0) * cos(w0) + beta);
  s10k_b1 = -2.0 * A * ((A - 1.0) + (A + 1.0) * cos(w0));
  s10k_b2 = A * ((A + 1.0) + (A - 1.0) * cos(w0) - beta);
  s10k_a0 = (A + 1.0) - (A - 1.0) * cos(w0) + beta;
  s10k_a1 = 2.0 * ((A - 1.0) - (A + 1.0) * cos(w0));
  s10k_a2 = (A + 1.0) - (A - 1.0) * cos(w0) - beta;

  // 6. Elliptic Sub-Mono Side Highpass (Butterworth 2nd order at slider6 Hz)
  sm_w0 = 2.0 * M_PI * clamp(slider6, 40.0, 160.0) / srate;
  sm_cos = cos(sm_w0); sm_sin = sin(sm_w0);
  sm_alpha = sm_sin / (2.0 * 0.7071);
  sm_b0 = (1.0 + sm_cos) * 0.5;
  sm_b1 = -(1.0 + sm_cos);
  sm_b2 = (1.0 + sm_cos) * 0.5;
  sm_a0 = 1.0 + sm_alpha;
  sm_a1 = -2.0 * sm_cos;
  sm_a2 = 1.0 - sm_alpha;

  // 7. Bus Glue Sidechain Detector HPF (slider16 - Butterworth 2nd order)
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
    slider3 = 0.0; slider4 = 0.0; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 0.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = 0.0;
    slider13 = 1; slider14 = 30.0; slider15 = 2; slider16 = 120; slider17 = 100;
    slider18 = 28; slider19 = 0.0; slider20 = 0.0; slider21 = 0.0; slider22 = 0.0;
    slider23 = 0; slider24 = 0.0; slider25 = 1.00;
  ) : idx == 1 ? ( // Lance Prenc
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 85; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -6.5;
    slider13 = 2; slider14 = 30.0; slider15 = 0; slider16 = 130; slider17 = 100;
    slider18 = 32; slider19 = 1.5; slider20 = -3.5; slider21 = 3.5; slider22 = 3.0;
    slider23 = 1; slider24 = 3.8; slider25 = 1.15;
  ) : idx == 2 ? ( // Scott Seigel
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.0;
    slider13 = 2; slider14 = 10.0; slider15 = 4; slider16 = 100; slider17 = 100;
    slider18 = 30; slider19 = 2.0; slider20 = -2.5; slider21 = 2.0; slider22 = 1.5;
    slider23 = 1; slider24 = 3.2; slider25 = 1.08;
  ) : idx == 3 ? ( // Jonathan Dolese
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = 75; slider7 = 1;
    slider8 = 0.8; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -4.0;
    slider13 = 1; slider14 = 30.0; slider15 = 2; slider16 = 110; slider17 = 100;
    slider18 = 25; slider19 = 3.0; slider20 = -2.0; slider21 = 1.2; slider22 = 2.0;
    slider23 = 3; slider24 = 2.8; slider25 = 1.10;
  ) : idx == 4 ? ( // Buster Odeholm
    slider3 = 0.0; slider4 = -3.5; slider5 = 1; slider6 = 90; slider7 = 1;
    slider8 = 1.8; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -9.0;
    slider13 = 2; slider14 = 10.0; slider15 = 0; slider16 = 90; slider17 = 100;
    slider18 = 35; slider19 = 4.0; slider20 = -4.0; slider21 = 1.5; slider22 = 0.5;
    slider23 = 1; slider24 = 5.2; slider25 = 1.20;
  ) : idx == 5 ? ( // Lewis Johns
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = 75; slider7 = 0;
    slider8 = 0.6; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -3.5;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 140; slider17 = 100;
    slider18 = 24; slider19 = 1.8; slider20 = -1.2; slider21 = 1.5; slider22 = 2.8;
    slider23 = 2; slider24 = 2.2; slider25 = 1.22;
  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target) - Forensic Replicate of Track 15 Legacy Chain
    slider3 = 0.0;
    slider4 = -0.9;   // Forensic Calibrated Headroom (matches legacy chain net output)
    slider5 = 0;      // Free Output (matches legacy chain dynamic crest factor)
    slider6 = 80;     // Sub-Bass Mono Anchor Cutoff (matches Bass Manager 80 Hz)
    slider7 = 1;      // Transient Sentry Active
    slider8 = 0.8;    // Dynamic Vocal Pocket depth
    slider9 = 1;      // gmem Auto-Sensing Corridor
    slider10 = 1;     // Bus Glue Engaged
    slider11 = 0;     // British VCA Punch (SSL 4000G / BUSTERse)
    slider12 = -6.0;  // Threshold calibrated for 2-3 dB musical glue
    slider13 = 2;     // 4:1 Modern Punch (matches BUSTERse 4:1)
    slider14 = 10.0;  // Attack 10 ms (matches BUSTERse 10 ms)
    slider15 = 2;     // Release 600 ms (matches BUSTERse .6 sec)
    slider16 = 80;    // Sidechain Detector HPF (clean 80Hz filter)
    slider17 = 100;   // 100% Dry/Wet
    slider18 = 32;    // HPF Cutoff 32 Hz (matches Bass Manager 30Hz & TB EQ 40Hz)
    slider19 = 3.0;   // 80Hz Punch +3.0 dB Low Shelf (matches TB EQ Band 2!)
    slider20 = -3.0;  // 220Hz Mud Scoop -3.0 dB (matches TB EQ Band 4 -3.0 dB!)
    slider21 = 3.0;   // 3.5kHz Bite +3.0 dB (matches TB EQ Band 6 +3.0 dB!)
    slider22 = 3.0;   // 10kHz Sheen +3.0 dB (matches TB EQ Band 7 +3.0 dB!)
    slider23 = 1;     // Neve 8014 Iron Desk (matches Britson Buss Vintage Summing!)
    slider24 = 2.5;   // Console Desk Drive 2.5 dB (matches Britson + Bass Manager 25% drive)
    slider25 = 1.08;  // Quad Imager Width 1.08x
  ) : idx == 7 ? ( // Dan Lancaster & Jason Perry
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.4; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -6.0;
    slider13 = 2; slider14 = 30.0; slider15 = 4; slider16 = 120; slider17 = 100;
    slider18 = 30; slider19 = 2.8; slider20 = -3.0; slider21 = 3.2; slider22 = 3.5;
    slider23 = 1; slider24 = 3.8; slider25 = 1.18;
  ) : idx == 8 ? ( // Erik Bickerstaffe
    slider3 = 0.0; slider4 = -2.8; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -5.5;
    slider13 = 2; slider14 = 10.0; slider15 = 1; slider16 = 100; slider17 = 100;
    slider18 = 28; slider19 = 2.0; slider20 = -1.5; slider21 = 2.5; slider22 = 1.0;
    slider23 = 2; slider24 = 4.2; slider25 = 1.06;
  ) : idx == 9 ? ( // Sam Guaiana
    slider3 = 0.0; slider4 = -2.8; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.5;
    slider13 = 2; slider14 = 10.0; slider15 = 4; slider16 = 110; slider17 = 100;
    slider18 = 30; slider19 = 2.5; slider20 = -2.5; slider21 = 2.5; slider22 = 2.2;
    slider23 = 1; slider24 = 3.2; slider25 = 1.12;
  ) : idx == 10 ? ( // Zach Tuch
    slider3 = 0.0; slider4 = -2.2; slider5 = 1; slider6 = 75; slider7 = 1;
    slider8 = 0.6; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -4.0;
    slider13 = 1; slider14 = 30.0; slider15 = 2; slider16 = 130; slider17 = 100;
    slider18 = 24; slider19 = 2.2; slider20 = -1.8; slider21 = 1.2; slider22 = 2.8;
    slider23 = 2; slider24 = 2.6; slider25 = 1.24;
  ) : idx == 11 ? ( // Forrester Savell
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -4.5;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 150; slider17 = 100;
    slider18 = 22; slider19 = 1.0; slider20 = -2.0; slider21 = 1.8; slider22 = 2.2;
    slider23 = 1; slider24 = 1.8; slider25 = 1.15;
  ) : idx == 12 ? ( // Leon Schmidt
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = 70; slider7 = 0;
    slider8 = 0.8; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -4.0;
    slider13 = 2; slider14 = 30.0; slider15 = 4; slider16 = 120; slider17 = 100;
    slider18 = 30; slider19 = 2.2; slider20 = -3.0; slider21 = 3.0; slider22 = 3.2;
    slider23 = 3; slider24 = 2.8; slider25 = 1.26;
  ) : idx == 13 ? ( // Ermin Hamidovic
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.0;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 160; slider17 = 100;
    slider18 = 25; slider19 = 0.5; slider20 = -2.2; slider21 = 0.8; slider22 = 1.5;
    slider23 = 0; slider24 = 1.2; slider25 = 1.05;
  ) : idx == 14 ? ( // Will Putney
    slider3 = 0.0; slider4 = -3.2; slider5 = 1; slider6 = 85; slider7 = 1;
    slider8 = 1.5; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -8.0;
    slider13 = 2; slider14 = 10.0; slider15 = 1; slider16 = 80; slider17 = 100;
    slider18 = 32; slider19 = 3.5; slider20 = -3.2; slider21 = 2.5; slider22 = 1.8;
    slider23 = 1; slider24 = 5.0; slider25 = 1.10;
  ) : idx == 15 ? ( // George Lever
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = 75; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -4.0;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 130; slider17 = 100;
    slider18 = 22; slider19 = 1.5; slider20 = -1.8; slider21 = 1.2; slider22 = 2.5;
    slider23 = 2; slider24 = 2.4; slider25 = 1.20;
  ) : idx == 16 ? ( // Sam Bassal
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 85; slider7 = 1;
    slider8 = 1.4; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -6.5;
    slider13 = 2; slider14 = 10.0; slider15 = 4; slider16 = 100; slider17 = 100;
    slider18 = 28; slider19 = 3.0; slider20 = -3.0; slider21 = 2.0; slider22 = 2.0;
    slider23 = 2; slider24 = 3.5; slider25 = 1.14;
  ) : idx == 17 ? ( // Henrik Udd
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -6.0;
    slider13 = 2; slider14 = 30.0; slider15 = 4; slider16 = 120; slider17 = 100;
    slider18 = 30; slider19 = 3.0; slider20 = -3.0; slider21 = 2.5; slider22 = 3.0;
    slider23 = 1; slider24 = 3.5; slider25 = 1.16;
  ) : idx == 18 ? ( // Dan Braunstein
    slider3 = 0.0; slider4 = -3.2; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -6.0;
    slider13 = 2; slider14 = 30.0; slider15 = 4; slider16 = 110; slider17 = 100;
    slider18 = 30; slider19 = 2.5; slider20 = -2.0; slider21 = 3.5; slider22 = 3.8;
    slider23 = 1; slider24 = 3.2; slider25 = 1.18;
  ) : idx == 19 ? ( // Zakk Cervini & Erik Ron
    slider3 = 0.0; slider4 = -3.2; slider5 = 1; slider6 = 85; slider7 = 1;
    slider8 = 1.5; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -7.0;
    slider13 = 2; slider14 = 10.0; slider15 = 0; slider16 = 110; slider17 = 100;
    slider18 = 32; slider19 = 3.0; slider20 = -3.5; slider21 = 3.5; slider22 = 3.0;
    slider23 = 1; slider24 = 4.0; slider25 = 1.15;
  ) : idx == 20 ? ( // Jens Bogren
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.0;
    slider13 = 2; slider14 = 30.0; slider15 = 1; slider16 = 100; slider17 = 100;
    slider18 = 28; slider19 = 2.5; slider20 = -2.5; slider21 = 1.5; slider22 = 1.8;
    slider23 = 1; slider24 = 4.0; slider25 = 1.10;
  ) : idx == 21 ? ( // Adam Nolly Getgood
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = 85; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -4.5;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 160; slider17 = 100;
    slider18 = 28; slider19 = 1.0; slider20 = -3.5; slider21 = 2.5; slider22 = 2.0;
    slider23 = 0; slider24 = 1.5; slider25 = 1.10;
  ) : idx == 22 ? ( // Acle Kahney
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = 75; slider7 = 1;
    slider8 = 0.8; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -4.0;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 150; slider17 = 100;
    slider18 = 25; slider19 = 1.2; slider20 = -2.5; slider21 = 1.8; slider22 = 2.5;
    slider23 = 0; slider24 = 1.6; slider25 = 1.12;
  ) : idx == 23 ? ( // Adam Cichocki
    slider3 = 0.0; slider4 = -3.2; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -6.5;
    slider13 = 2; slider14 = 30.0; slider15 = 1; slider16 = 110; slider17 = 100;
    slider18 = 26; slider19 = 1.8; slider20 = -2.8; slider21 = 1.8; slider22 = 2.2;
    slider23 = 2; slider24 = 4.5; slider25 = 1.12;
  ) : ( // Manuel Renner
    slider3 = 0.0; slider4 = -2.8; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.5;
    slider13 = 2; slider14 = 30.0; slider15 = 4; slider16 = 120; slider17 = 100;
    slider18 = 28; slider19 = 2.8; slider20 = -3.2; slider21 = 2.8; slider22 = 3.0;
    slider23 = 1; slider24 = 3.2; slider25 = 1.16;
  );
  update_filters();
  slider_automate();
);

update_filters();

@slider
prev_preset != slider2 ? (
  apply_producer_preset(slider2);
  prev_preset = slider2;
);
update_filters();

@sample
// 1. Transparent Passthrough & ANSI C16.5 Metering
dry_l = spl0; dry_r = spl1;

// Live 300ms VU RMS integration for reactive moving-coil meter
vu_omega = 1.0 - exp(-1.0 / (srate * 0.300));
vu_sig_sq = (dry_l * dry_l + dry_r * dry_r) * 0.5;
vu_rms_smooth += (vu_sig_sq - vu_rms_smooth) * vu_omega;
inst_rms = vu_rms_smooth > 0.000000001 ? 10.0 * log10(vu_rms_smooth) : -90.0;
inst_peak = max(abs(dry_l), abs(dry_r));

// 1:1 Complete Bit-Exact Transparent Pass if Suite Bypassed OR Preset 00 (Unity Baseline)
(!slider27 || slider2 == 0) ? (
  spl0 = dry_l;
  spl1 = dry_r;
  glue_gr_db = 0.0;
) : (
  // 2. Input Level Calibration
  in_trim = exp(slider3 * 0.1151292546497);
  s0 = spl0 * in_trim;
  s1 = spl1 * in_trim;

  // 3. Sub-Bass Mono Anchor (Elliptical High-Pass on Side Channel - Mid 100% Untouched)
  m_mid = (s0 + s1) * 0.5;
  m_side = (s0 - s1) * 0.5;
  hp_side = (sm_b0 * m_side + sm_b1 * sm_hp_x1 + sm_b2 * sm_hp_x2 - sm_a1 * sm_hp_y1 - sm_a2 * sm_hp_y2) / sm_a0;
  sm_hp_x2 = sm_hp_x1; sm_hp_x1 = m_side; sm_hp_y2 = sm_hp_y1; sm_hp_y1 = hp_side;

  // Quad-Wall Stereo Imager Width on Side channel
  w_side = hp_side * slider25;
  s0 = m_mid + w_side;
  s1 = m_mid - w_side;

  // 4. 5-Band Tonal Forge EQ (Fully isolated Left and Right delay lines)
  // HPF
  ty0 = (hpf_b0 * s0 + hpf_b1 * hpf_x1_l + hpf_b2 * hpf_x2_l - hpf_a1 * hpf_y1_l - hpf_a2 * hpf_y2_l) / hpf_a0;
  hpf_x2_l = hpf_x1_l; hpf_x1_l = s0; hpf_y2_l = hpf_y1_l; hpf_y1_l = ty0; s0 = ty0;
  ty1 = (hpf_b0 * s1 + hpf_b1 * hpf_x1_r + hpf_b2 * hpf_x2_r - hpf_a1 * hpf_y1_r - hpf_a2 * hpf_y2_r) / hpf_a0;
  hpf_x2_r = hpf_x1_r; hpf_x1_r = s1; hpf_y2_r = hpf_y1_r; hpf_y1_r = ty1; s1 = ty1;

  // 80Hz Punch Low Shelf
  ty0 = (p80_b0 * s0 + p80_b1 * p80_x1_l + p80_b2 * p80_x2_l - p80_a1 * p80_y1_l - p80_a2 * p80_y2_l) / p80_a0;
  p80_x2_l = p80_x1_l; p80_x1_l = s0; p80_y2_l = p80_y1_l; p80_y1_l = ty0; s0 = ty0;
  ty1 = (p80_b0 * s1 + p80_b1 * p80_x1_r + p80_b2 * p80_x2_r - p80_a1 * p80_y1_r - p80_a2 * p80_y2_r) / p80_a0;
  p80_x2_r = p80_x1_r; p80_x1_r = s1; p80_y2_r = p80_y1_r; p80_y1_r = ty1; s1 = ty1;

  // 220Hz Mud Scoop
  ty0 = (s280_b0 * s0 + s280_b1 * s280_x1_l + s280_b2 * s280_x2_l - s280_a1 * s280_y1_l - s280_a2 * s280_y2_l) / s280_a0;
  s280_x2_l = s280_x1_l; s280_x1_l = s0; s280_y2_l = s280_y1_l; s280_y1_l = ty0; s0 = ty0;
  ty1 = (s280_b0 * s1 + s280_b1 * s280_x1_r + s280_b2 * s280_x2_r - s280_a1 * s280_y1_r - s280_a2 * s280_y2_r) / s280_a0;
  s280_x2_r = s280_x1_r; s280_x1_r = s1; s280_y2_r = s280_y1_r; s280_y1_r = ty1; s1 = ty1;

  // 3.5kHz Bite
  ty0 = (b3k_b0 * s0 + b3k_b1 * b3k_x1_l + b3k_b2 * b3k_x2_l - b3k_a1 * b3k_y1_l - b3k_a2 * b3k_y2_l) / b3k_a0;
  b3k_x2_l = b3k_x1_l; b3k_x1_l = s0; b3k_y2_l = b3k_y1_l; b3k_y1_l = ty0; s0 = ty0;
  ty1 = (b3k_b0 * s1 + b3k_b1 * b3k_x1_r + b3k_b2 * b3k_x2_r - b3k_a1 * b3k_y1_r - b3k_a2 * b3k_y2_r) / b3k_a0;
  b3k_x2_r = b3k_x1_r; b3k_x1_r = s1; b3k_y2_r = b3k_y1_r; b3k_y1_r = ty1; s1 = ty1;

  // 10kHz Sheen High Shelf
  ty0 = (s10k_b0 * s0 + s10k_b1 * s10k_x1_l + s10k_b2 * s10k_x2_l - s10k_a1 * s10k_y1_l - s10k_a2 * s10k_y2_l) / s10k_a0;
  s10k_x2_l = s10k_x1_l; s10k_x1_l = s0; s10k_y2_l = s10k_y1_l; s10k_y1_l = ty0; s0 = ty0;
  ty1 = (s10k_b0 * s1 + s10k_b1 * s10k_x1_r + s10k_b2 * s10k_x2_r - s10k_a1 * s10k_y1_r - s10k_a2 * s10k_y2_r) / s10k_a0;
  s10k_x2_r = s10k_x1_r; s10k_x1_r = s1; s10k_y2_r = s10k_y1_r; s10k_y1_r = ty1; s1 = ty1;

  // 5. Dynamic Vocal Pocket Corridor (Mid 2.2 kHz dynamic dip when vocal is active)
  v_energy = gmem[1452];
  pocket_depth = slider8;
  slider9 && v_energy > -40.0 ? (
    pocket_depth = min(3.0, max(0.0, slider8 * ((v_energy + 40.0) / 25.0)));
  );
  pocket_depth > 0.05 ? (
    mid_ch = (s0 + s1) * 0.5;
    side_ch = (s0 - s1) * 0.5;
    p_gain = exp(-pocket_depth * 0.1151292546497);
    mid_carved = mid_ch * (1.0 - (1.0 - p_gain) * 0.6);
    s0 = mid_carved + side_ch;
    s1 = mid_carved - side_ch;
  );

  // 6. Dual-Topology Master Bus Glue Compressor with Sidechain Detector HPF
  slider10 ? (
    sc_in = (s0 + s1) * 0.5;
    sc_a0 <= 0.0001 ? sc_a0 = 1.0;
    sc_flt = (sc_b0 * sc_in + sc_b1 * sc_x1 + sc_b2 * sc_x2 - sc_a1 * sc_y1 - sc_a2 * sc_y2) / sc_a0;
    (sc_flt != sc_flt || abs(sc_flt) > 20.0) ? (
      sc_flt = sc_in; sc_x1 = 0.0; sc_x2 = 0.0; sc_y1 = 0.0; sc_y2 = 0.0;
    );
    sc_x2 = sc_x1; sc_x1 = sc_in; sc_y2 = sc_y1; sc_y1 = sc_flt;
    sc_sig = abs(sc_flt);
    (sc_sig != sc_sig || sc_sig <= 0.000001) ? (
      sc_db = -120.0;
    ) : (
      sc_db = 20.0 * log10(sc_sig);
    );

    r_val = slider13 == 0 ? 1.5 : (slider13 == 1 ? 2.0 : (slider13 == 2 ? 4.0 : 8.0));
    gr_target = 0.0;
    sc_db > slider12 ? (
      over_db = sc_db - slider12;
      slider11 == 1 ? (
        // Neve Diode Bridge smooth soft-knee
        gr_target = (over_db * (1.0 - 1.0 / r_val)) * 1.15;
      ) : (
        // British VCA progressive punch
        gr_target = over_db * (1.0 - 1.0 / r_val);
      );
    );
    srate <= 0 ? srate = 44100;
    att_coeff = exp(-1.0 / (clamp(slider14, 0.1, 100.0) * 0.001 * srate));
    rel_ms = slider15 == 0 ? 100.0 : (slider15 == 1 ? 300.0 : (slider15 == 2 ? 600.0 : (slider15 == 3 ? 1200.0 : 400.0)));
    rel_coeff = exp(-1.0 / (rel_ms * 0.001 * srate));

    (glue_gr_db != glue_gr_db) ? glue_gr_db = 0.0;
    (gr_target != gr_target) ? gr_target = 0.0;
    gr_target > glue_gr_db ? (
      glue_gr_db = glue_gr_db * att_coeff + gr_target * (1.0 - att_coeff);
    ) : (
      glue_gr_db = glue_gr_db * rel_coeff + gr_target * (1.0 - rel_coeff);
    );
    (glue_gr_db != glue_gr_db) ? glue_gr_db = 0.0;

    gmem[1410] = sc_in;
    gmem[1411] = sc_flt;
    gmem[1412] = sc_db;
    gmem[1413] = gr_target;
    gmem[1414] = glue_gr_db;

    comp_gain = exp(-glue_gr_db * 0.1151292546497);
    wet_f = slider17 * 0.01;
    s0 = s0 * (1.0 - wet_f + comp_gain * wet_f);
    s1 = s1 * (1.0 - wet_f + comp_gain * wet_f);
  ) : (
    glue_gr_db = 0.0;
  );

  // 7. Harmonic Crucible Saturation Engine (Neve 8014 Iron Desk, Studer A800, Tube)
  slider23 > 0 && slider24 > 0.0 ? (
    h_drive = exp(slider24 * 0.1151292546497);
    d0 = s0 * h_drive; d1 = s1 * h_drive;
    slider23 == 1 ? ( // Neve 8014 Desk Iron (2nd + 3rd harmonics)
      s0 = (d0 + 0.15 * d0 * abs(d0) - 0.06 * d0 * d0 * d0) / (1.0 + abs(d0) * 0.35);
      s1 = (d1 + 0.15 * d1 * abs(d1) - 0.06 * d1 * d1 * d1) / (1.0 + abs(d1) * 0.35);
    ) : slider23 == 2 ? ( // Studer A800 15 IPS Tape
      s0 = fast_shape(d0 * 0.85) * 1.15;
      s1 = fast_shape(d1 * 0.85) * 1.15;
    ) : ( // Triode Tube Crucible
      s0 = (d0 + 0.22 * d0 * d0) / (1.0 + abs(d0 + 0.22 * d0 * d0) * 0.4);
      s1 = (d1 + 0.22 * d1 * d1) / (1.0 + abs(d1 + 0.22 * d1 * d1) * 0.4);
    );
    s0 = s0 / sqrt(h_drive);
    s1 = s1 / sqrt(h_drive);
  );

  // 8. Producer Headroom Trim & Pre-Master Ceiling Guard
  out_trim = exp(slider4 * 0.1151292546497);
  s0 *= out_trim;
  s1 *= out_trim;

  slider5 == 1 ? ( // -6.0 dBTP Transparent Soft Analog Safety Limiter
    ceil_lvl = 0.501187; // -6.0 dBFS
    abs0 = abs(s0);
    abs1 = abs(s1);
    abs0 > ceil_lvl ? (
      over0 = abs0 - ceil_lvl;
      s0 = (s0 > 0 ? 1 : -1) * (ceil_lvl + fast_shape(over0 * 2.5) * 0.04);
    );
    abs1 > ceil_lvl ? (
      over1 = abs1 - ceil_lvl;
      s1 = (s1 > 0 ? 1 : -1) * (ceil_lvl + fast_shape(over1 * 2.5) * 0.04);
    );
  );

  // 9. Delta Solo Audition Mode
  slider28 ? (
    spl0 = s0 - dry_l;
    spl1 = s1 - dry_r;
  ) : (
    spl0 = s0;
    spl1 = s1;
  );
);

// Ballistics smooth needle updates
needle_omega = 1.0 - exp(-1.0 / (srate * 0.050));
cur_vu_db = inst_rms + 18.0;
cur_vu_db += slider24 * 0.25;
(cur_vu_db != cur_vu_db) ? cur_vu_db = -20.0;
sifam_desk_needle += (cur_vu_db - sifam_desk_needle) * needle_omega;
(sifam_desk_needle != sifam_desk_needle) ? sifam_desk_needle = -20.0;
(glue_gr_db != glue_gr_db) ? glue_gr_db = 0.0;
glue_gr_db = clamp(glue_gr_db, 0.0, 24.0);
sifam_glue_needle += (glue_gr_db - sifam_glue_needle) * needle_omega;
(sifam_glue_needle != sifam_glue_needle) ? sifam_glue_needle = 0.0;
sifam_glue_needle = clamp(sifam_glue_needle, 0.0, 24.0);

// Shared memory telemetry broadcast (1400..1449)
rms_acc_l += spl0 * spl0;
rms_acc_r += spl1 * spl1;
rms_cnt += 1;
rms_cnt >= 1024 ? (
  gmem[1401] = max(abs(spl0), abs(spl1));
  gmem[1402] = 10.0 * log10(max(0.000000001, (rms_acc_l + rms_acc_r) * (0.5 / 1024)));
  gmem[1403] = glue_gr_db;
  gmem[1404] = slider1;
  gmem[1405] = slider27;
  gmem[1406] = slider2;
  gmem[1407] = slider24;
  gmem[1408] = slider25;
  gmem[1409] = pocket_depth;
  rms_acc_l = 0.0; rms_acc_r = 0.0; rms_cnt = 0;
);

@gfx 1080 700
// =============================================================================
// GLOBAL HARDWARE CONSOLE GUI ENGINE // LUXURY FLAGGED CHASSIS
// =============================================================================
crt_x = 8; crt_y = 8;
crt_w = gfx_w - 16; crt_h = gfx_h - 16;

mouse_down = (mouse_cap & 1);
mouse_clicked = mouse_down && !prev_mouse_down;
prev_mouse_down = mouse_down;

// Outer Obsidian Titanium Dual Bezel Frame
gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(crt_x, crt_y, crt_w, crt_h);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(crt_x, crt_y, crt_w, crt_h, 0);
gfx_r = 0.12; gfx_g = 0.18; gfx_b = 0.26; gfx_rect(crt_x + 1, crt_y + 1, crt_w - 2, crt_h - 2, 0);

// Corner Machine Hex Bolts
function draw_screw(sx, sy) (
  gfx_r = 0.12; gfx_g = 0.16; gfx_b = 0.24; gfx_circle(sx, sy, 5, 1);
  gfx_r = 0.45; gfx_g = 0.55; gfx_b = 0.65; gfx_circle(sx, sy, 5, 0);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_line(sx - 3, sy, sx + 3, sy);
);
draw_screw(crt_x + 8, crt_y + 8);
draw_screw(crt_x + crt_w - 8, crt_y + 8);
draw_screw(crt_x + 8, crt_y + crt_h - 8);
draw_screw(crt_x + crt_w - 8, crt_y + crt_h - 8);

// Draw Text safely fitted within bounds
function draw_fit(str, face, sz, tx, ty, maxw) local(fit_s, fit_w, fit_h) (
  fit_s = sz;
  gfx_setfont(1, face, fit_s, 'b');
  gfx_measurestr(str, fit_w, fit_h);
  while (fit_w > maxw && fit_s > 8.5) (
    fit_s -= 0.5;
    gfx_setfont(1, face, fit_s, 'b');
    gfx_measurestr(str, fit_w, fit_h);
  );
  gfx_x = tx; gfx_y = ty;
  gfx_drawstr(str);
);

// ─────────────────────────────────────────────────────────────────────────────
// 1. TOP HEADER BAR: CREST, PRESET NAVIGATOR & STATUS PILLS
// ─────────────────────────────────────────────────────────────────────────────
hdr_h = 46;
gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(crt_x + 2, crt_y + 2, crt_w - 4, hdr_h);
gfx_r = 0.14; gfx_g = 0.22; gfx_b = 0.32; gfx_line(crt_x + 2, crt_y + hdr_h + 2, crt_x + crt_w - 2, crt_y + hdr_h + 2);

// Adinkra Triple Circle Crest
sig_cx = crt_x + 24; sig_cy = crt_y + 23;
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
gfx_circle(sig_cx, sig_cy, 11, 0);
gfx_circle(sig_cx, sig_cy, 7, 0);
gfx_circle(sig_cx, sig_cy, 3, 1);

gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.95; gfx_g = 0.92; gfx_b = 1.00;
gfx_x = crt_x + 42; gfx_y = crt_y + 15;
gfx_drawstr("DAMEI // INST BUS");

right_edge_x = crt_x + crt_w - 12;

// Pill 1: ENGAGED / BYPASS
byp_w = 84; byp_x = right_edge_x - byp_w;
byp_hov = (mouse_x >= byp_x && mouse_x <= byp_x + byp_w && mouse_y >= crt_y + 8 && mouse_y <= crt_y + 38);
gfx_r = slider27 ? (byp_hov ? 0.14 : 0.08) : (byp_hov ? 0.28 : 0.16);
gfx_g = slider27 ? (byp_hov ? 0.30 : 0.20) : (byp_hov ? 0.08 : 0.05);
gfx_b = slider27 ? (byp_hov ? 0.40 : 0.26) : (byp_hov ? 0.08 : 0.05);
gfx_rect(byp_x, crt_y + 8, byp_w, 30);
gfx_r = slider27 ? 0.00 : 0.95; gfx_g = slider27 ? 0.95 : 0.30; gfx_b = slider27 ? 0.65 : 0.30;
gfx_rect(byp_x, crt_y + 8, byp_w, 30, 0);
gfx_setfont(2, "Orbitron", 11.5, 'b');
b_txt = slider27 ? "ENGAGED" : "BYPASS";
gfx_measurestr(b_txt, btw, bth);
gfx_x = byp_x + (byp_w - btw) * 0.5; gfx_y = crt_y + 15;
gfx_drawstr(b_txt);
mouse_clicked && byp_hov ? (slider27 = !slider27; slider_automate(););

// Pill 2: Headroom Ceiling (-6dB Lock vs Free)
ceil_w = 88; ceil_x = byp_x - ceil_w - 6;
ceil_hov = (mouse_x >= ceil_x && mouse_x <= ceil_x + ceil_w && mouse_y >= crt_y + 8 && mouse_y <= crt_y + 38);
gfx_r = slider5 ? 0.08 : 0.06; gfx_g = slider5 ? 0.26 : 0.10; gfx_b = slider5 ? 0.18 : 0.12;
gfx_rect(ceil_x, crt_y + 8, ceil_w, 30);
gfx_r = slider5 ? 0.00 : 0.50; gfx_g = slider5 ? 0.95 : 0.50; gfx_b = slider5 ? 0.65 : 0.50;
gfx_rect(ceil_x, crt_y + 8, ceil_w, 30, 0);
gfx_setfont(3, "Consolas", 12, 'b');
c_txt = slider5 ? "CEIL: -6dB" : "CEIL: FREE";
gfx_measurestr(c_txt, ctw, cth);
gfx_x = ceil_x + (ceil_w - ctw) * 0.5; gfx_y = crt_y + 15;
gfx_drawstr(c_txt);
mouse_clicked && ceil_hov ? (slider5 = !slider5; slider_automate(););

// Pill 3: Mode (Stereo vs M/S)
mode_w = 96; mode_x = ceil_x - mode_w - 6;
mode_hov = (mouse_x >= mode_x && mouse_x <= mode_x + mode_w && mouse_y >= crt_y + 8 && mouse_y <= crt_y + 38);
gfx_r = 0.06; gfx_g = 0.12; gfx_b = 0.18; gfx_rect(mode_x, crt_y + 8, mode_w, 30);
gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(mode_x, crt_y + 8, mode_w, 30, 0);
gfx_setfont(3, "Consolas", 12, 'b');
m_txt = slider30 ? "MODE: M/S" : "MODE: STEREO";
gfx_measurestr(m_txt, mtw, mth);
gfx_x = mode_x + (mode_w - mtw) * 0.5; gfx_y = crt_y + 15;
gfx_drawstr(m_txt);
mouse_clicked && mode_hov ? (slider30 = !slider30; slider_automate(););

// Pill 4: Vocal Bus Telemetry Link
vb_vocal_rms = gmem[1452];
vb_alive = (gmem[1450] == 1);
vlink_w = 110; vlink_x = mode_x - vlink_w - 6;
gfx_r = vb_alive ? 0.04 : 0.08; gfx_g = vb_alive ? 0.20 : 0.08; gfx_b = vb_alive ? 0.15 : 0.10;
gfx_rect(vlink_x, crt_y + 8, vlink_w, 30);
gfx_r = vb_alive ? 0.00 : 0.50; gfx_g = vb_alive ? 0.95 : 0.50; gfx_b = vb_alive ? 0.65 : 0.50;
gfx_rect(vlink_x, crt_y + 8, vlink_w, 30, 0);
gfx_setfont(3, "Consolas", 11.5, 'b');
vb_str = vb_alive ? sprintf(#, "VOX: %.1fdB", vb_vocal_rms) : "VOX: STBY";
gfx_measurestr(vb_str, vbw, vbh);
gfx_x = vlink_x + (vlink_w - vbw) * 0.5; gfx_y = crt_y + 15;
gfx_drawstr(vb_str);

// Pill 5: Song Structure Sync
rgn_w = 105; rgn_x = vlink_x - rgn_w - 6;
gfx_r = 0.04; gfx_g = 0.08; gfx_b = 0.12; gfx_rect(rgn_x, crt_y + 8, rgn_w, 30);
gfx_r = 0.15; gfx_g = 0.75; gfx_b = 0.50; gfx_rect(rgn_x, crt_y + 8, rgn_w, 30, 0);
g_sec = gmem[100] == 1 ? gmem[101] : 0;
r_str = g_sec == 3 ? "⚡ CHORUS" : sprintf(#, "● SYNC: %dR", gmem[103] > 0 ? gmem[103] : 20);
gfx_setfont(3, "Consolas", 11.5, 'b');
gfx_measurestr(r_str, rsw, rsh);
gfx_x = rgn_x + (rgn_w - rsw) * 0.5; gfx_y = crt_y + 15;
gfx_drawstr(r_str);

// Center Stepper: Producer Benchmark Quick Navigator
mid_w = rgn_x - (crt_x + 215) - 12;
mid_x = crt_x + 215;
btn_sz = 26;
prv_x = mid_x; prv_y = crt_y + 10;
prv_hov = (mouse_x >= prv_x && mouse_x <= prv_x + btn_sz && mouse_y >= prv_y && mouse_y <= prv_y + btn_sz);
gfx_r = prv_hov ? 0.15 : 0.05; gfx_g = prv_hov ? 0.22 : 0.08; gfx_b = prv_hov ? 0.32 : 0.12;
gfx_rect(prv_x, prv_y, btn_sz, btn_sz);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(prv_x, prv_y, btn_sz, btn_sz, 0);
gfx_setfont(1, "Orbitron", 12, 'b'); gfx_x = prv_x + 8; gfx_y = prv_y + 5; gfx_drawstr("<");
mouse_clicked && prv_hov ? (
  slider2 = (slider2 - 1 + 25) % 25;
  apply_producer_preset(slider2);
  prev_preset = slider2;
);

nxt_x = prv_x + mid_w - btn_sz; nxt_y = prv_y;
nxt_hov = (mouse_x >= nxt_x && mouse_x <= nxt_x + btn_sz && mouse_y >= nxt_y && mouse_y <= nxt_y + btn_sz);
gfx_r = nxt_hov ? 0.15 : 0.05; gfx_g = nxt_hov ? 0.22 : 0.08; gfx_b = nxt_hov ? 0.32 : 0.12;
gfx_rect(nxt_x, nxt_y, btn_sz, btn_sz);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(nxt_x, nxt_y, btn_sz, btn_sz, 0);
gfx_setfont(1, "Orbitron", 12, 'b'); gfx_x = nxt_x + 8; gfx_y = nxt_y + 5; gfx_drawstr(">");
mouse_clicked && nxt_hov ? (
  slider2 = (slider2 + 1) % 25;
  apply_producer_preset(slider2);
  prev_preset = slider2;
);

lbl_x = prv_x + btn_sz + 4; lbl_w = mid_w - 2 * btn_sz - 8;
lbl_hov = (mouse_x >= lbl_x && mouse_x <= lbl_x + lbl_w && mouse_y >= prv_y && mouse_y <= prv_y + btn_sz);
gfx_r = lbl_hov ? 0.06 : 0.02; gfx_g = lbl_hov ? 0.09 : 0.03; gfx_b = lbl_hov ? 0.14 : 0.05;
gfx_rect(lbl_x, prv_y, lbl_w, btn_sz);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(lbl_x, prv_y, lbl_w, btn_sz, 0);
p_str = get_producer_short_name(slider2);
gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
gfx_measurestr(p_str, psw, psh);
gfx_x = lbl_x + (lbl_w - psw) * 0.5; gfx_y = prv_y + 5;
gfx_drawstr(p_str);
mouse_clicked && lbl_hov ? (
  slider2 = (slider2 + 1) % 25;
  apply_producer_preset(slider2);
  prev_preset = slider2;
);

// ─────────────────────────────────────────────────────────────────────────────
// 2. TAB NAVIGATION BAR (7 DENSE METALLIC TABS)
// ─────────────────────────────────────────────────────────────────────────────
tab_y = crt_y + hdr_h + 3; tab_h = 32;
tab_w = floor((crt_w - 8) / 7);
ti = 0;
loop(7,
  tx = crt_x + 4 + ti * tab_w;
  sel = (slider1 == ti);
  t_hov = (mouse_x >= tx && mouse_x <= tx + tab_w - 2 && mouse_y >= tab_y && mouse_y <= tab_y + tab_h);
  gfx_r = sel ? 0.14 : (t_hov ? 0.08 : 0.032);
  gfx_g = sel ? 0.20 : (t_hov ? 0.12 : 0.044);
  gfx_b = sel ? 0.30 : (t_hov ? 0.18 : 0.060);
  gfx_rect(tx, tab_y, tab_w - 2, tab_h);
  sel ? (
    gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
    gfx_rect(tx, tab_y + tab_h - 3, tab_w - 2, 3);
    gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;
  ) : (
    gfx_r = t_hov ? 0.95 : 0.70; gfx_g = t_hov ? 0.95 : 0.75; gfx_b = t_hov ? 1.00 : 0.85;
  );
  gfx_setfont(2, "Orbitron", 12, 'b');
  t_lbl = (ti == 0 ? "OVERVIEW" : (ti == 1 ? "TONAL EQ" : (ti == 2 ? "BUS GLUE" : (ti == 3 ? "CRUCIBLE" : (ti == 4 ? "STEREO" : (ti == 5 ? "POCKET" : "PRODUCER"))))));
  gfx_measurestr(t_lbl, tlw, tlh);
  gfx_x = floor(tx + (tab_w - 2 - tlw) * 0.5); gfx_y = tab_y + 9;
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
gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x, ws_y, ws_w, ws_h);
gfx_r = 0.10; gfx_g = 0.16; gfx_b = 0.24; gfx_rect(ws_x, ws_y, ws_w, ws_h, 0);

// Helper for horizontal parameter slider
function draw_param_slider(px, py, pw, ph, label_str, val, min_v, max_v, fmt_str, s_idx, accent_r, accent_g, accent_b) local(val_str, vsw, vsh, trx, try, trw, trh, frac, fill_w, hx, hy, hov, new_f) (
  gfx_r = 0.022; gfx_g = 0.030; gfx_b = 0.040; gfx_rect(px, py, pw, ph);
  gfx_r = 0.14; gfx_g = 0.22; gfx_b = 0.32; gfx_rect(px, py, pw, ph, 0);

  gfx_setfont(2, "Orbitron", 11.5, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_x = px + 12; gfx_y = py + 7; gfx_drawstr(label_str);

  val_str = sprintf(#, fmt_str, val);
  gfx_setfont(3, "Consolas", 13, 'b'); gfx_r = 1.0; gfx_g = 0.9; gfx_b = 0.35;
  gfx_measurestr(val_str, vsw, vsh);
  gfx_x = px + pw - vsw - 12; gfx_y = py + 7; gfx_drawstr(val_str);

  // Track bar
  trx = px + 12; try = py + 30; trw = pw - 24; trh = 9;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(trx, try, trw, trh);
  gfx_r = 0.22; gfx_g = 0.32; gfx_b = 0.44; gfx_rect(trx, try, trw, trh, 0);

  frac = max(0.0, min(1.0, (val - min_v) / (max_v - min_v)));
  fill_w = floor(frac * trw);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_rect(trx, try, fill_w, trh);

  // Handle
  hx = trx + fill_w; hy = try + trh * 0.5;
  gfx_r = 1.0; gfx_g = 0.90; gfx_b = 0.40; gfx_circle(hx, hy, 7, 1);
  gfx_r = 0.1; gfx_g = 0.12; gfx_b = 0.15; gfx_circle(hx, hy, 7, 0);

  // Drag interaction
  hov = (mouse_x >= px && mouse_x <= px + pw && mouse_y >= py && mouse_y <= py + ph);
  mouse_clicked && hov ? drag_slider_idx = s_idx;
  drag_slider_idx == s_idx && mouse_down ? (
    new_f = max(0.0, min(1.0, (mouse_x - trx) / trw));
    slider(s_idx) = min_v + new_f * (max_v - min_v);
    update_filters();
    slider_automate();
  );
);

// Helper for Vertical Luxury Channel Strip
function draw_channel_strip(px, py, pw, ph, title_str, sub_str, val, min_v, max_v, fmt_str, s_idx, accent_r, accent_g, accent_b) local(val_str, vsw, vsh, trk_x, trk_y, trk_h, trk_w, frac, h_cy, mid_y, cap_w, cap_h, cap_x, cap_y, hov, new_f) (
  // Raised hardware chassis
  gfx_r = 0.020; gfx_g = 0.026; gfx_b = 0.036; gfx_rect(px, py, pw, ph);
  gfx_r = accent_r * 0.8; gfx_g = accent_g * 0.8; gfx_b = accent_b * 0.8; gfx_rect(px, py, pw, ph, 0);

  // Header Box
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(px + 1, py + 1, pw - 2, 48);
  gfx_r = 0.15; gfx_g = 0.22; gfx_b = 0.32; gfx_line(px + 1, py + 49, px + pw - 2, py + 49);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_measurestr(title_str, tsw, tsh);
  gfx_x = px + floor((pw - tsw) * 0.5); gfx_y = py + 9;
  gfx_drawstr(title_str);

  gfx_setfont(3, "Segoe UI", 12); gfx_r = 0.70; gfx_g = 0.78; gfx_b = 0.88;
  gfx_measurestr(sub_str, ssw, ssh);
  gfx_x = px + floor((pw - ssw) * 0.5); gfx_y = py + 28;
  gfx_drawstr(sub_str);

  // Value Readout Plaque
  v_box_y = py + 56; v_box_h = 30;
  gfx_r = 0.008; gfx_g = 0.012; gfx_b = 0.018; gfx_rect(px + 8, v_box_y, pw - 16, v_box_h);
  gfx_r = accent_r * 0.6; gfx_g = accent_g * 0.6; gfx_b = accent_b * 0.6; gfx_rect(px + 8, v_box_y, pw - 16, v_box_h, 0);

  val_str = sprintf(#, fmt_str, val);
  gfx_setfont(1, "Consolas", 13.5, 'b'); gfx_r = 1.0; gfx_g = 0.92; gfx_b = 0.40;
  gfx_measurestr(val_str, vsw, vsh);
  gfx_x = px + floor((pw - vsw) * 0.5); gfx_y = v_box_y + 7; gfx_drawstr(val_str);

  // Vertical Luxury Fader Track
  trk_x = px + floor(pw * 0.5) - 4;
  trk_y = py + 102;
  trk_h = ph - 150;
  trk_w = 8;
  gfx_r = 0.008; gfx_g = 0.012; gfx_b = 0.018; gfx_rect(trk_x, trk_y, trk_w, trk_h);
  gfx_r = 0.22; gfx_g = 0.32; gfx_b = 0.44; gfx_rect(trk_x, trk_y, trk_w, trk_h, 0);

  // dB Scale Marks
  gfx_setfont(3, "Consolas", 11, 'b'); gfx_r = 0.50; gfx_g = 0.65; gfx_b = 0.80;
  gfx_line(trk_x - 12, trk_y, trk_x - 4, trk_y); gfx_x = trk_x - 36; gfx_y = trk_y - 6; gfx_drawstr("+6");
  gfx_line(trk_x - 12, trk_y + trk_h * 0.5, trk_x - 4, trk_y + trk_h * 0.5); gfx_x = trk_x - 30; gfx_y = trk_y + trk_h * 0.5 - 6; gfx_drawstr("0");
  gfx_line(trk_x - 12, trk_y + trk_h, trk_x - 4, trk_y + trk_h); gfx_x = trk_x - 36; gfx_y = trk_y + trk_h - 6; gfx_drawstr("-6");

  // Handle Position
  frac = max(0.0, min(1.0, (val - min_v) / (max_v - min_v)));
  h_cy = trk_y + trk_h - floor(frac * trk_h);

  // Active filled bar from center
  mid_y = trk_y + trk_h * 0.5;
  h_cy < mid_y ? (
    gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
    gfx_rect(trk_x + 1, h_cy, trk_w - 2, mid_y - h_cy);
  ) : (
    gfx_r = accent_r * 0.6; gfx_g = accent_g * 0.6; gfx_b = accent_b * 0.6;
    gfx_rect(trk_x + 1, mid_y, trk_w - 2, h_cy - mid_y);
  );

  // Luxury Metallic Fader Cap
  cap_w = pw - 32; cap_h = 18;
  cap_x = px + 16; cap_y = h_cy - 9;
  gfx_r = 0.16; gfx_g = 0.24; gfx_b = 0.34; gfx_rect(cap_x, cap_y, cap_w, cap_h);
  gfx_r = 0.88; gfx_g = 0.92; gfx_b = 0.98; gfx_rect(cap_x, cap_y, cap_w, cap_h, 0);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b; gfx_line(cap_x + 8, cap_y + 9, cap_x + cap_w - 8, cap_y + 9);

  // Bottom Interactive Indicator
  gfx_setfont(3, "Segoe UI", 12); gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.88;
  gfx_measurestr("DRAG FADER", bsw, bsh);
  gfx_x = px + floor((pw - bsw) * 0.5); gfx_y = py + ph - 26;
  gfx_drawstr("DRAG FADER");

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

// Authentic SIFAM Analogue Moving-Coil VU Meter
function draw_sifam_meter(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) (
  gfx_r = 0.055; gfx_g = 0.065; gfx_b = 0.080; gfx_rect(mx, my, mw, mh);
  gfx_r = 0.020; gfx_g = 0.025; gfx_b = 0.032; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4);
  gfx_r = 0.85; gfx_g = 0.72; gfx_b = 0.28; gfx_rect(mx, my, mw, mh, 0);
  gfx_r = 0.25; gfx_g = 0.32; gfx_b = 0.40; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4, 0);

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
  gfx_x = mx + 14; gfx_y = my + 10; gfx_drawstr(title_str);

  gfx_setfont(2, "Orbitron", 11.5, 'b'); gfx_r = 0.0; gfx_g = 0.85; gfx_b = 1.0;
  badge_str = is_glue ? "STUDIO GR" : "STUDIO VU";
  gfx_measurestr(badge_str, b_w, b_h);
  gfx_x = mx + mw - b_w - 14; gfx_y = my + 10; gfx_drawstr(badge_str);

  arc_cx = mx + mw * 0.5; arc_cy = my + mh + 20; arc_r = mh * 1.15;
  a_left = -0.58; a_right = 0.58; a_span = a_right - a_left;

  // Arc graduation marks
  is_glue ? (
    db_vals = 6;
    m_i = 0;
    while (m_i < 6) (
      m_db = m_i == 0 ? 0 : (m_i == 1 ? -3 : (m_i == 2 ? -6 : (m_i == 3 ? -10 : (m_i == 4 ? -16 : -20))));
      f_val = (m_db / -20.0);
      a_pos = a_left + f_val * a_span;
      nx1 = arc_cx + sin(a_pos) * (arc_r - 4); ny1 = arc_cy - cos(a_pos) * (arc_r - 4);
      nx2 = arc_cx + sin(a_pos) * (arc_r + 10); ny2 = arc_cy - cos(a_pos) * (arc_r + 10);
      m_db >= -6 ? (gfx_r = 0.95; gfx_g = 0.95; gfx_b = 1.0;) : (gfx_r = 1.0; gfx_g = 0.30; gfx_b = 0.20;);
      gfx_line(nx1, ny1, nx2, ny2);
      m_db != -20 ? (
        t_str = sprintf(#, "%d", m_db);
        gfx_setfont(3, "Consolas", 11, 'b');
        gfx_measurestr(t_str, tw, th);
        gfx_x = arc_cx + sin(a_pos) * (arc_r - 18) - tw * 0.5;
        gfx_y = arc_cy - cos(a_pos) * (arc_r - 18) - th * 0.5;
        gfx_drawstr(t_str);
      );
      m_i += 1;
    );
  ) : (
    m_i = 0;
    while (m_i < 5) (
      m_db = m_i == 0 ? -20 : (m_i == 1 ? -10 : (m_i == 2 ? -5 : (m_i == 3 ? 0 : 3)));
      f_val = (m_db + 20.0) / 23.0;
      a_pos = a_left + f_val * a_span;
      nx1 = arc_cx + sin(a_pos) * (arc_r - 4); ny1 = arc_cy - cos(a_pos) * (arc_r - 4);
      nx2 = arc_cx + sin(a_pos) * (arc_r + 10); ny2 = arc_cy - cos(a_pos) * (arc_r + 10);
      m_db <= 0 ? (gfx_r = 0.95; gfx_g = 0.95; gfx_b = 1.0;) : (gfx_r = 1.0; gfx_g = 0.30; gfx_b = 0.20;);
      gfx_line(nx1, ny1, nx2, ny2);
      t_str = sprintf(#, "%+d", m_db);
      gfx_setfont(3, "Consolas", 11, 'b');
      gfx_measurestr(t_str, tw, th);
      gfx_x = arc_cx + sin(a_pos) * (arc_r - 18) - tw * 0.5;
      gfx_y = arc_cy - cos(a_pos) * (arc_r - 18) - th * 0.5;
      gfx_drawstr(t_str);
      m_i += 1;
    );
  );

  // Moving coil needle
  frac = is_glue ? min(1.0, max(0.0, needle_val / 16.0)) : min(1.0, max(0.0, (needle_val + 20.0) / 23.0));
  cur_ang = a_left + frac * a_span;
  tip_x = arc_cx + sin(cur_ang) * arc_r; tip_y = arc_cy - cos(cur_ang) * arc_r;
  gfx_r = 1.0; gfx_g = 0.90; gfx_b = 0.45;
  gfx_line(arc_cx - 1, arc_cy, tip_x - 1, tip_y);
  gfx_line(arc_cx, arc_cy, tip_x, tip_y);
  gfx_line(arc_cx + 1, arc_cy, tip_x + 1, tip_y);
  gfx_r = 1.0; gfx_g = 0.40; gfx_b = 0.30; gfx_circle(tip_x, tip_y, 3, 1);

  // Pivot Hub
  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(arc_cx, arc_cy - 10, 16, 1);
  gfx_r = 0.85; gfx_g = 0.72; gfx_b = 0.28; gfx_circle(arc_cx, arc_cy - 10, 16, 0);

  // Centered Badge
  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
  center_badge = is_glue ? "[ GR ]" : "[ VU ]";
  gfx_measurestr(center_badge, cbw, cbh);
  gfx_x = arc_cx - cbw * 0.5; gfx_y = my + mh * 0.58; gfx_drawstr(center_badge);

  // Bottom Value Readouts
  gfx_setfont(3, "Consolas", 12.5, 'b');
  is_glue ? (
    gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_x = mx + 16; gfx_y = my + mh - 24;
    gfx_printf("GR:  %4.1f dB", needle_val);
    gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.85; gfx_x = mx + mw - 110; gfx_y = my + mh - 24;
    gfx_drawstr("PEAK HOLD");
  ) : (
    gfx_r = 0.15; gfx_g = 0.95; gfx_b = 0.45; gfx_x = mx + 16; gfx_y = my + mh - 24;
    gfx_printf("RMS: %4.1f dBFS", inst_rms);
    gfx_r = 0.85; gfx_g = 0.72; gfx_b = 0.28; gfx_x = mx + mw - 140; gfx_y = my + mh - 24;
    gfx_drawstr("0 VU = -18 dBFS");
  );
);

// =============================================================================
// TAB 0: OVERVIEW (TWIN SIFAM ANALOG METERS + PHASE SCOPE + 3 HARDWARE CARDS)
// =============================================================================
slider1 == 0 ? (
  top_row_h = 240;
  meter_w = floor((ws_w - 40) * 0.36);
  scope_w = ws_w - 2 * meter_w - 32;

  // SIFAM Meters
  draw_sifam_meter(ws_x + 12, ws_y + 12, meter_w, top_row_h, "SIFAM DIRECTOR // CONSOLE DRIVE", sifam_desk_needle, 3.0, 0, 0.85, 0.47, 0.21);
  draw_sifam_meter(ws_x + 16 + meter_w, ws_y + 12, meter_w, top_row_h, "STUDIO BUS GLUE // GAIN REDUCTION", sifam_glue_needle, 16.0, 1, 0.00, 0.85, 1.00);

  // Stereo Phase Radar
  scope_x = ws_x + 20 + 2 * meter_w;
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(scope_x, ws_y + 12, scope_w, top_row_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(scope_x, ws_y + 12, scope_w, top_row_h, 0);

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = scope_x + 14; gfx_y = ws_y + 22; gfx_drawstr("STEREO PHASE RADAR");

  r_cx = scope_x + scope_w * 0.5; r_cy = ws_y + 12 + 105;
  gfx_r = 0.10; gfx_g = 0.16; gfx_b = 0.24;
  gfx_circle(r_cx, r_cy, 65, 0);
  gfx_circle(r_cx, r_cy, 40, 0);
  gfx_line(r_cx - 65, r_cy, r_cx + 65, r_cy);
  gfx_line(r_cx, r_cy - 65, r_cx, r_cy + 65);

  // Phase Correlation Bar
  cbar_y = ws_y + top_row_h - 32; cbar_w = scope_w - 28;
  gfx_r = 0.06; gfx_g = 0.09; gfx_b = 0.14; gfx_rect(scope_x + 14, cbar_y, cbar_w, 8);
  corr_f = (cur_phase_corr + 1.0) * 0.5;
  gfx_r = cur_phase_corr > 0.4 ? 0.00 : (cur_phase_corr > 0.0 ? 1.00 : 1.00);
  gfx_g = cur_phase_corr > 0.4 ? 0.95 : (cur_phase_corr > 0.0 ? 0.85 : 0.20);
  gfx_b = cur_phase_corr > 0.4 ? 0.65 : (cur_phase_corr > 0.0 ? 0.20 : 0.20);
  gfx_rect(scope_x + 14 + floor(cbar_w * 0.5), cbar_y, floor((corr_f - 0.5) * cbar_w), 8);

  gfx_setfont(3, "Consolas", 11, 'b'); gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.85;
  gfx_x = scope_x + 14; gfx_y = cbar_y - 16; gfx_drawstr("-1.0");
  gfx_x = scope_x + 14 + floor(cbar_w * 0.5) - 10; gfx_y = cbar_y - 16; gfx_drawstr("0.0");
  gfx_x = scope_x + 14 + cbar_w - 24; gfx_y = cbar_y - 16; gfx_drawstr("+1.0");

  // Bottom 3 Luxury Hardware Console Modules (Zero Empty Void)
  dash_y = ws_y + top_row_h + 16; dash_h = ws_h - top_row_h - 26;
  col_w = floor((ws_w - 32) / 3);

  // Card 1: GAIN & HEADROOM SENTRY
  c1_x = ws_x + 12;
  gfx_r = 0.020; gfx_g = 0.026; gfx_b = 0.036; gfx_rect(c1_x, dash_y, col_w, dash_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(c1_x, dash_y, col_w, dash_h, 0);
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(c1_x + 2, dash_y + 2, col_w - 4, 32);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = c1_x + 14; gfx_y = dash_y + 9; gfx_drawstr("1. GAIN & HEADROOM");

  gfx_setfont(3, "Consolas", 12.5, 'b');
  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.96;
  gfx_x = c1_x + 16; gfx_y = dash_y + 45; gfx_printf("Input Calibration : %+4.1f dB", slider3);
  gfx_x = c1_x + 16; gfx_y = dash_y + 70; gfx_printf("Producer Output   : %+4.1f dB Trim", slider4);
  gfx_x = c1_x + 16; gfx_y = dash_y + 95; gfx_printf("Pre-Master Ceiling: %s", slider5 ? "-6.0 dBTP Strict Lock" : "Free Range");
  gfx_x = c1_x + 16; gfx_y = dash_y + 120; gfx_printf("Summing Engine    : %s", slider27 ? "ACTIVE SUMMING" : "1:1 PASS");
  gfx_x = c1_x + 16; gfx_y = dash_y + 145; gfx_printf("Delta Solo State  : %s", slider28 ? "ACTIVE SOLO" : "NORMAL SUM");

  // Sub-badge
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(c1_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(c1_x + 14, dash_y + dash_h - 38, col_w - 28, 26, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = c1_x + 22; gfx_y = dash_y + dash_h - 32;
  p_title = get_producer_short_name(slider2);
  gfx_drawstr(p_title);

  // Card 2: BUS GLUE COMPRESSION
  c2_x = ws_x + 16 + col_w;
  gfx_r = 0.020; gfx_g = 0.026; gfx_b = 0.036; gfx_rect(c2_x, dash_y, col_w, dash_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(c2_x, dash_y, col_w, dash_h, 0);
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(c2_x + 2, dash_y + 2, col_w - 4, 32);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = c2_x + 14; gfx_y = dash_y + 9; gfx_drawstr("2. BUS GLUE DYNAMICS");

  gfx_setfont(3, "Consolas", 12.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.96;
  gfx_x = c2_x + 16; gfx_y = dash_y + 45; gfx_printf("Active Topology   : %s", slider11 ? "Neve Diode Bridge" : "British VCA Punch");
  gfx_x = c2_x + 16; gfx_y = dash_y + 70; gfx_printf("Threshold / Ratio : %.1f dB | %s", slider12, slider13 == 0 ? "1.5:1" : (slider13 == 1 ? "2:1" : (slider13 == 2 ? "4:1" : "8:1")));
  gfx_x = c2_x + 16; gfx_y = dash_y + 95; gfx_printf("Attack / Release  : %.1fms | %s", slider14, slider15 == 0 ? "100ms" : (slider15 == 1 ? "300ms" : (slider15 == 2 ? "600ms" : "Auto")));
  gfx_x = c2_x + 16; gfx_y = dash_y + 120; gfx_printf("Detector HPF Key  : %d Hz Sidechain", slider16);
  gfx_x = c2_x + 16; gfx_y = dash_y + 145; gfx_printf("Instantaneous GR  : -%.2f dB Peak Hold", glue_gr_db);

  // Meter mini bar
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(c2_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(c2_x + 14, dash_y + dash_h - 38, col_w - 28, 26, 0);
  gr_frac = min(1.0, max(0.0, glue_gr_db / 12.0));
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_rect(c2_x + 15, dash_y + dash_h - 37, floor((col_w - 30) * gr_frac), 24);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = c2_x + 22; gfx_y = dash_y + dash_h - 32; gfx_printf("GLUE GR: %4.1f dB", glue_gr_db);

  // Card 3: HARMONIC & SPATIAL CORE
  c3_x = ws_x + 20 + 2 * col_w;
  gfx_r = 0.020; gfx_g = 0.026; gfx_b = 0.036; gfx_rect(c3_x, dash_y, col_w, dash_h);
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35; gfx_rect(c3_x, dash_y, col_w, dash_h, 0);
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(c3_x + 2, dash_y + 2, col_w - 4, 32);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = c3_x + 14; gfx_y = dash_y + 9; gfx_drawstr("3. HARMONIC & SPATIAL");

  gfx_setfont(3, "Consolas", 12.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.96;
  gfx_x = c3_x + 16; gfx_y = dash_y + 45; gfx_printf("Harmonic Engine   : %s", slider23 == 0 ? "Transparent Pure" : (slider23 == 1 ? "Neve 8014 Iron Desk" : (slider23 == 2 ? "Studer A800 Tape" : "Triode Tube")));
  gfx_x = c3_x + 16; gfx_y = dash_y + 70; gfx_printf("Console Desk Drive: +%.1f dB THD", slider24);
  gfx_x = c3_x + 16; gfx_y = dash_y + 95; gfx_printf("Sub Mono Anchor   : %d Hz (LR 24dB/oct)", slider6);
  gfx_x = c3_x + 16; gfx_y = dash_y + 120; gfx_printf("Quad Imager Width : %.2f x Multiplier", slider25);
  gfx_x = c3_x + 16; gfx_y = dash_y + 145; gfx_printf("Vocal Pocket Carve: -%.1f dB @ 2.2 kHz", pocket_depth);

  // Corridor status pill
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(c3_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35; gfx_rect(c3_x + 14, dash_y + dash_h - 38, col_w - 28, 26, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.90; gfx_b = 0.40;
  gfx_x = c3_x + 22; gfx_y = dash_y + dash_h - 32;
  gfx_printf("CORRIDOR POCKET: -%.1f dB", pocket_depth);
);

// =============================================================================
// TAB 1: TONAL FORGE EQ (5-BAND CURVE PLOT + 5 FULL-HEIGHT CHANNEL STRIPS)
// =============================================================================
slider1 == 1 ? (
  eq_plot_y = ws_y + 12; eq_plot_h = 220; eq_plot_w = ws_w - 24;
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(ws_x + 12, eq_plot_y, eq_plot_w, eq_plot_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 12, eq_plot_y, eq_plot_w, eq_plot_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 24; gfx_y = eq_plot_y + 12; gfx_drawstr("TONAL FORGE // 5-BAND BUS EQUALIZATION CURVE");

  // Grid lines
  cy0 = eq_plot_y + eq_plot_h * 0.5;
  gfx_r = 0.12; gfx_g = 0.18; gfx_b = 0.26;
  gfx_line(ws_x + 12, cy0, ws_x + 12 + eq_plot_w, cy0);
  gfx_line(ws_x + 12, cy0 - 45, ws_x + 12 + eq_plot_w, cy0 - 45); // +6dB
  gfx_line(ws_x + 12, cy0 + 45, ws_x + 12 + eq_plot_w, cy0 + 45); // -6dB

  // Freq grid lines (80Hz, 220Hz, 1kHz, 3.5kHz, 10kHz)
  fx80  = ws_x + 12 + floor(eq_plot_w * 0.18);
  fx220 = ws_x + 12 + floor(eq_plot_w * 0.35);
  fx1k  = ws_x + 12 + floor(eq_plot_w * 0.55);
  fx3k  = ws_x + 12 + floor(eq_plot_w * 0.72);
  fx10k = ws_x + 12 + floor(eq_plot_w * 0.88);
  gfx_line(fx80, eq_plot_y, fx80, eq_plot_y + eq_plot_h);
  gfx_line(fx220, eq_plot_y, fx220, eq_plot_y + eq_plot_h);
  gfx_line(fx1k,  eq_plot_y, fx1k,  eq_plot_y + eq_plot_h);
  gfx_line(fx3k,  eq_plot_y, fx3k,  eq_plot_y + eq_plot_h);
  gfx_line(fx10k, eq_plot_y, fx10k, eq_plot_y + eq_plot_h);

  gfx_setfont(3, "Consolas", 11.5, 'b'); gfx_r = 0.55; gfx_g = 0.65; gfx_b = 0.75;
  gfx_x = fx80 + 4;  gfx_y = eq_plot_y + eq_plot_h - 20; gfx_drawstr("80Hz");
  gfx_x = fx220 + 4; gfx_y = eq_plot_y + eq_plot_h - 20; gfx_drawstr("220Hz");
  gfx_x = fx1k + 4;  gfx_y = eq_plot_y + eq_plot_h - 20; gfx_drawstr("1kHz");
  gfx_x = fx3k + 4;  gfx_y = eq_plot_y + eq_plot_h - 20; gfx_drawstr("3.5kHz");
  gfx_x = fx10k + 4; gfx_y = eq_plot_y + eq_plot_h - 20; gfx_drawstr("10kHz");

  // Draw EQ Curve with live response
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  prev_py = cy0;
  pi = 0;
  loop(140,
    px = ws_x + 12 + floor((pi / 139.0) * eq_plot_w);
    f_val = 20.0 * exp(log(1000.0) * (pi / 139.0));
    g_tot = 0.0;
    f_val < slider18 * 1.5 ? g_tot -= (1.0 - (f_val / (slider18 * 1.5))) * 18.0;
    // Low shelf 80Hz
    f_val <= 80.0 ? g_tot += slider19 : (f_val < 300.0 ? g_tot += slider19 * (1.0 - (f_val - 80.0) / 220.0) : 0);
    // Mud scoop 220Hz
    g_tot += slider20 * exp(-0.5 * sqr((log(f_val / 220.0) / 0.5)));
    // Bite 3.5kHz
    g_tot += slider21 * exp(-0.5 * sqr((log(f_val / 3500.0) / 0.5)));
    // Sheen 10kHz
    f_val > 5000.0 ? g_tot += slider22 * (min(1.0, (f_val - 5000.0) / 5000.0));
    cur_py = cy0 - g_tot * 7.5;
    pi > 0 ? (
      gfx_line(prev_px, prev_py, px, cur_py);
      // Shaded fill to zero
      gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
      gfx_line(px, cur_py, px, cy0);
    );
    prev_px = px; prev_py = cur_py;
    pi += 1;
  );

  // 5 Full-Height Channel Strips (Zero empty space)
  col_w = floor((ws_w - 24 - 32) / 5);
  cards_y = eq_plot_y + eq_plot_h + 12; cards_h = ws_h - eq_plot_h - 26;
  draw_channel_strip(ws_x + 12 + 0 * (col_w + 8), cards_y, col_w, cards_h, "32Hz HPF", "SUB CUT 18dB", slider18, 20, 60, "%d Hz", 18, 0.85, 0.47, 0.21);
  draw_channel_strip(ws_x + 12 + 1 * (col_w + 8), cards_y, col_w, cards_h, "80Hz PUNCH", "KICK/BASS BODY", slider19, -6.0, 6.0, "%+.1f dB", 19, 0.00, 0.85, 1.00);
  draw_channel_strip(ws_x + 12 + 2 * (col_w + 8), cards_y, col_w, cards_h, "220Hz SCOOP", "MUD CLARITY", slider20, -6.0, 6.0, "%+.1f dB", 20, 0.85, 0.47, 0.21);
  draw_channel_strip(ws_x + 12 + 3 * (col_w + 8), cards_y, col_w, cards_h, "3.5kHz BITE", "PICK ATTACK", slider21, -6.0, 6.0, "%+.1f dB", 21, 0.00, 0.85, 1.00);
  draw_channel_strip(ws_x + 12 + 4 * (col_w + 8), cards_y, col_w, cards_h, "10kHz SHEEN", "AIR GLOSS", slider22, -6.0, 6.0, "%+.1f dB", 22, 1.00, 0.85, 0.35);
);

// =============================================================================
// TAB 2: BUS GLUE COMPRESSOR (VCA/DIODE FACEPLATE + COMPRESSION KNEE + CONTROLS)
// =============================================================================
slider1 == 2 ? (
  cg_y = ws_y + 12; cg_w = ws_w - 24; cg_h = ws_h - 24;
  left_w = floor((cg_w - 24) * 0.46);
  right_w = cg_w - left_w - 16;

  // Left Box: Compression Transfer Plot
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 12, cg_y, left_w, cg_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 12, cg_y, left_w, cg_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 24; gfx_y = cg_y + 14; gfx_drawstr("COMPRESSION TRANSFER FUNCTION");

  p_x0 = ws_x + 36; p_y0 = cg_y + 50; p_size = min(left_w - 60, cg_h - 180);
  gfx_r = 0.008; gfx_g = 0.012; gfx_b = 0.018; gfx_rect(p_x0, p_y0, p_size, p_size);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.40; gfx_rect(p_x0, p_y0, p_size, p_size, 0);

  // 1:1 Unity Line (Gray dashed)
  gfx_r = 0.35; gfx_g = 0.45; gfx_b = 0.55;
  gfx_line(p_x0, p_y0 + p_size, p_x0 + p_size, p_y0);

  // Compression Slope Curve
  r_val = slider13 == 0 ? 1.5 : (slider13 == 1 ? 2.0 : (slider13 == 2 ? 4.0 : 8.0));
  th_frac = (slider12 + 40.0) / 40.0;
  th_px = p_x0 + floor(th_frac * p_size);
  th_py = p_y0 + p_size - floor(th_frac * p_size);

  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.30;
  gfx_line(p_x0, p_y0 + p_size, th_px, th_py);
  end_py = th_py - floor(((p_size - (th_px - p_x0)) / r_val));
  gfx_line(th_px, th_py, p_x0 + p_size, end_py);
  gfx_circle(th_px, th_py, 5, 1);

  // Dynamic Reduction Indicator
  gr_mark_y = th_py + floor(glue_gr_db * 4.0);
  gfx_r = 1.0; gfx_g = 0.30; gfx_b = 0.20;
  gfx_rect(p_x0 + p_size - 8, min(p_y0 + p_size, end_py), 8, floor(glue_gr_db * 5.0));

  // Topology Pills below plot
  t_pill_y = cg_y + cg_h - 90;
  tp_w = floor((left_w - 48) / 2);
  // Button 1: BRITISH VCA PUNCH (SSL 4000G)
  sel_vca = (slider11 == 0);
  hov_vca = (mouse_x >= ws_x + 24 && mouse_x <= ws_x + 24 + tp_w && mouse_y >= t_pill_y && mouse_y <= t_pill_y + 36);
  gfx_r = sel_vca ? 0.18 : 0.04; gfx_g = sel_vca ? 0.28 : 0.06; gfx_b = sel_vca ? 0.38 : 0.08;
  gfx_rect(ws_x + 24, t_pill_y, tp_w, 36);
  gfx_r = sel_vca ? 0.00 : 0.30; gfx_g = sel_vca ? 0.85 : 0.35; gfx_b = sel_vca ? 1.00 : 0.45;
  gfx_rect(ws_x + 24, t_pill_y, tp_w, 36, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = sel_vca ? 1.0 : 0.7; gfx_g = sel_vca ? 1.0 : 0.75; gfx_b = sel_vca ? 1.0 : 0.8;
  gfx_x = ws_x + 32; gfx_y = t_pill_y + 10; gfx_drawstr("BRITISH VCA (SSL)");
  mouse_clicked && hov_vca ? (slider11 = 0; slider_automate(););

  // Button 2: NEVE DIODE BRIDGE (2254)
  sel_dio = (slider11 == 1);
  hov_dio = (mouse_x >= ws_x + 24 + tp_w + 12 && mouse_x <= ws_x + 24 + 2 * tp_w + 12 && mouse_y >= t_pill_y && mouse_y <= t_pill_y + 36);
  gfx_r = sel_dio ? 0.24 : 0.04; gfx_g = sel_dio ? 0.18 : 0.06; gfx_b = sel_dio ? 0.12 : 0.08;
  gfx_rect(ws_x + 24 + tp_w + 12, t_pill_y, tp_w, 36);
  gfx_r = sel_dio ? 0.85 : 0.30; gfx_g = sel_dio ? 0.47 : 0.35; gfx_b = sel_dio ? 0.21 : 0.45;
  gfx_rect(ws_x + 24 + tp_w + 12, t_pill_y, tp_w, 36, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = sel_dio ? 1.0 : 0.7; gfx_g = sel_dio ? 1.0 : 0.75; gfx_b = sel_dio ? 1.0 : 0.8;
  gfx_x = ws_x + 32 + tp_w + 12; gfx_y = t_pill_y + 10; gfx_drawstr("NEVE DIODE (2254)");
  mouse_clicked && hov_dio ? (slider11 = 1; slider_automate(););

  // Quick Style Pills row
  sp_y = cg_y + cg_h - 44;
  sp_w = floor((left_w - 48 - 16) / 3);
  sp_i = 0;
  loop(3,
    sp_x = ws_x + 24 + sp_i * (sp_w + 8);
    sp_hov = (mouse_x >= sp_x && mouse_x <= sp_x + sp_w && mouse_y >= sp_y && mouse_y <= sp_y + 30);
    is_act = (sp_i == 0 ? (slider13 == 1 && slider14 == 30.0) : (sp_i == 1 ? (slider13 == 2 && slider14 == 10.0 && slider15 == 2) : (slider13 == 3 && slider14 == 10.0)));
    gfx_r = is_act ? 0.18 : (sp_hov ? 0.10 : 0.04);
    gfx_g = is_act ? 0.24 : (sp_hov ? 0.14 : 0.05);
    gfx_b = is_act ? 0.34 : (sp_hov ? 0.20 : 0.07);
    gfx_rect(sp_x, sp_y, sp_w, 30);
    gfx_r = is_act ? 0.85 : 0.25; gfx_g = is_act ? 0.70 : 0.32; gfx_b = is_act ? 0.25 : 0.42;
    gfx_rect(sp_x, sp_y, sp_w, 30, 0);
    gfx_setfont(3, "Consolas", 11.5, 'b');
    gfx_r = is_act ? 1.0 : 0.75; gfx_g = is_act ? 1.0 : 0.80; gfx_b = is_act ? 1.0 : 0.88;
    sp_txt = (sp_i == 0 ? "SUBTLE GLUE" : (sp_i == 1 ? "PINCHIN 4:1" : "CRUSH 8:1"));
    gfx_measurestr(sp_txt, stw, sth);
    gfx_x = sp_x + (sp_w - stw) * 0.5; gfx_y = sp_y + 7;
    gfx_drawstr(sp_txt);
    mouse_clicked && sp_hov ? (
      sp_i == 0 ? (slider13 = 1; slider14 = 30.0; slider15 = 4; slider12 = -4.0;) :
      sp_i == 1 ? (slider13 = 2; slider14 = 10.0; slider15 = 2; slider12 = -6.0; slider16 = 80;) :
                  (slider13 = 3; slider14 = 10.0; slider15 = 0; slider12 = -12.0;);
      update_filters();
      slider_automate();
    );
    sp_i += 1;
  );

  // Right Box: Tactile Sliders Panel
  rx = ws_x + 12 + left_w + 16;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(rx, cg_y, right_w, cg_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(rx, cg_y, right_w, cg_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = rx + 16; gfx_y = cg_y + 14; gfx_drawstr("STUDIO GLUE DYNAMICS PARAMETERS");

  sl_w = right_w - 32;
  sl_h = 56;
  s_start_y = cg_y + 48;
  draw_param_slider(rx + 16, s_start_y + 0 * (sl_h + 10), sl_w, sl_h, "1. BUS GLUE THRESHOLD", slider12, -36.0, 0.0, "%.1f dBFS", 12, 0.00, 0.85, 1.00);
  draw_param_slider(rx + 16, s_start_y + 1 * (sl_h + 10), sl_w, sl_h, "2. COMPRESSION RATIO", slider13, 0, 3, "%d:1", 13, 0.85, 0.47, 0.21);
  draw_param_slider(rx + 16, s_start_y + 2 * (sl_h + 10), sl_w, sl_h, "3. ATTACK TIME", slider14, 0.1, 100.0, "%.1f ms", 14, 0.00, 0.85, 1.00);
  draw_param_slider(rx + 16, s_start_y + 3 * (sl_h + 10), sl_w, sl_h, "4. RELEASE BALLISTICS", slider15, 0, 4, "%d Mode", 15, 0.85, 0.47, 0.21);
  draw_param_slider(rx + 16, s_start_y + 4 * (sl_h + 10), sl_w, sl_h, "5. SIDECHAIN DETECTOR HPF", slider16, 30, 250, "%d Hz", 16, 1.00, 0.85, 0.35);
  draw_param_slider(rx + 16, s_start_y + 5 * (sl_h + 10), sl_w, sl_h, "6. PARALLEL DRY / WET MIX", slider17, 0, 100, "%d %%", 17, 0.00, 0.85, 1.00);
);

// =============================================================================
// TAB 3: HARMONIC CRUCIBLE (4 CONSOLE DESK MODES + TRANSFER + SPECTRUM BARS)
// =============================================================================
slider1 == 3 ? (
  sat_y = ws_y + 12; sat_w = ws_w - 24; sat_h = ws_h - 24;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 12, sat_y, sat_w, sat_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 12, sat_y, sat_w, sat_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 28; gfx_y = sat_y + 14; gfx_drawstr("HARMONIC CRUCIBLE // CONSOLE DESK, TAPE & TUBE HARMONICS");

  // 4 Raised Hardware Cards
  c_w = floor((sat_w - 48) / 4);
  mi = 0;
  loop(4,
    cx = ws_x + 24 + mi * (c_w + 8); cy = sat_y + 44; ch = 92;
    sel = (slider23 == mi);
    m_hov = (mouse_x >= cx && mouse_x <= cx + c_w && mouse_y >= cy && mouse_y <= cy + ch);
    gfx_r = sel ? 0.20 : (m_hov ? 0.10 : 0.04);
    gfx_g = sel ? 0.12 : (m_hov ? 0.08 : 0.05);
    gfx_b = sel ? 0.09 : (m_hov ? 0.10 : 0.07);
    gfx_rect(cx, cy, c_w, ch);
    gfx_r = sel ? 0.85 : 0.22; gfx_g = sel ? 0.47 : 0.32; gfx_b = sel ? 0.21 : 0.42;
    gfx_rect(cx, cy, c_w, ch, 0);

    m_title = mi == 0 ? "TRANSPARENT PASS" : (mi == 1 ? "NEVE 8014 DESK" : (mi == 2 ? "STUDER TAPE" : "TRIODE TUBE"));
    gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = sel ? 1.0 : 0.75; gfx_g = sel ? 0.90 : 0.80; gfx_b = sel ? 0.45 : 0.88;
    gfx_x = cx + 14; gfx_y = cy + 14; gfx_drawstr(m_title);

    m_desc = mi == 0 ? "0 THD Pure 1:1 Wire" : (mi == 1 ? "Transformer Iron Harmonics" : (mi == 2 ? "15 IPS Master Tape Compression" : "Warm Even-Order Tube Bloom"));
    gfx_setfont(3, "Segoe UI", 12.5); gfx_r = 0.70; gfx_g = 0.80; gfx_b = 0.90;
    gfx_x = cx + 14; gfx_y = cy + 40; gfx_drawstr(m_desc);

    mouse_clicked && m_hov ? (slider23 = mi; update_filters(); slider_automate(););
    mi += 1;
  );

  // Middle Section: Left = Transfer Curve; Right = Spectrum Analyzer
  mid_y = sat_y + 148; mid_h = 190;
  m_left_w = floor((sat_w - 48) * 0.46);
  m_right_w = sat_w - 48 - m_left_w - 12;

  // Left Transfer Plot
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, mid_y, m_left_w, mid_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, mid_y, m_left_w, mid_h, 0);
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 36; gfx_y = mid_y + 12; gfx_drawstr("SATURATION KNEE & COMPRESSION CURVE");

  p_cx0 = ws_x + 36; p_cy0 = mid_y + 36; p_cw = m_left_w - 24; p_ch = mid_h - 48;
  gfx_r = 0.08; gfx_g = 0.12; gfx_b = 0.18;
  gfx_line(p_cx0, p_cy0 + p_ch * 0.5, p_cx0 + p_cw, p_cy0 + p_ch * 0.5);
  gfx_line(p_cx0 + p_cw * 0.5, p_cy0, p_cx0 + p_cw * 0.5, p_cy0 + p_ch);

  // Draw saturation curve
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  prev_y = p_cy0 + p_ch * 0.5;
  pi = 0;
  loop(60,
    px = p_cx0 + floor((pi / 59.0) * p_cw);
    in_val = (pi / 29.5) - 1.0;
    out_val = slider23 == 0 ? in_val : fast_shape(in_val * (1.0 + slider24 * 0.25));
    cur_y = p_cy0 + p_ch * 0.5 - out_val * (p_ch * 0.45);
    pi > 0 ? gfx_line(prev_x, prev_y, px, cur_y);
    prev_x = px; prev_y = cur_y;
    pi += 1;
  );

  // Right Harmonic Spectrum Visualizer
  rx = ws_x + 24 + m_left_w + 12;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(rx, mid_y, m_right_w, mid_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(rx, mid_y, m_right_w, mid_h, 0);
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = rx + 16; gfx_y = mid_y + 12; gfx_drawstr("HARMONIC SPECTRUM & THD DISTRIBUTION");

  // 5 Harmonic Bars
  h_bar_w = floor((m_right_w - 60) / 5);
  hi = 0;
  loop(5,
    hx = rx + 20 + hi * (h_bar_w + 8);
    h_level = (hi == 0) ? 0.88 : (
      slider23 == 0 ? 0.0 : (
        slider23 == 1 ? (hi == 1 ? 0.45 : (hi == 2 ? 0.30 : 0.10)) * (slider24 / 12.0) :
        slider23 == 2 ? (hi == 1 ? 0.20 : (hi == 2 ? 0.50 : 0.15)) * (slider24 / 12.0) :
                        (hi == 1 ? 0.60 : (hi == 2 ? 0.15 : 0.25)) * (slider24 / 12.0)
      )
    );
    b_h = floor(h_level * (mid_h - 75));
    by = mid_y + mid_h - 26 - b_h;
    gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
    gfx_rect(hx, by, h_bar_w, b_h);
    gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;
    gfx_rect(hx, by, h_bar_w, b_h, 0);

    gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;
    h_lbl = hi == 0 ? "1st" : (hi == 1 ? "2nd" : (hi == 2 ? "3rd" : (hi == 3 ? "4th" : "5th")));
    gfx_x = hx + floor(h_bar_w * 0.5) - 10; gfx_y = mid_y + mid_h - 20;
    gfx_drawstr(h_lbl);
    hi += 1;
  );

  // Bottom Section: Drive Slider + Detailed Advice
  draw_param_slider(ws_x + 24, sat_y + 348, sat_w - 48, 65, "HARMONIC CRUCIBLE CONSOLE DRIVE", slider24, 0.0, 12.0, "+%.1f dB", 24, 0.85, 0.47, 0.21);

  adv_y = sat_y + 420; adv_h = sat_h - 430;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, adv_y, sat_w - 48, adv_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, adv_y, sat_w - 48, adv_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 36; gfx_y = adv_y + 12; gfx_drawstr("HARMONIC THD GENERATION & SATURATION PROFILES:");
  gfx_setfont(3, "Segoe UI", 13); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.96;
  gfx_x = ws_x + 36; gfx_y = adv_y + 36;
  gfx_drawstr("• Neve 8014 Desk: Drives transformer iron, adding 2nd and 3rd harmonics to give heavy rhythm guitars weight.");
  gfx_x = ws_x + 36; gfx_y = adv_y + 60;
  gfx_drawstr("• Studer A800 15 IPS Tape: Smooth tape saturation rounds cymbal spikiness while gluing kick and snare.");
  gfx_x = ws_x + 36; gfx_y = adv_y + 84;
  gfx_drawstr("• Triode Tube Crucible: Enriches even-order harmonics, lending warm analog body to clean synth beds.");
);

// =============================================================================
// TAB 4: STEREO DIMENSION & SUB-ANCHOR (CROSSOVER PLOT + VECTOR SCOPE + CONTROLS)
// =============================================================================
slider1 == 4 ? (
  st_y = ws_y + 12; st_w = ws_w - 24; st_h = ws_h - 24;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 12, st_y, st_w, st_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 12, st_y, st_w, st_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 28; gfx_y = st_y + 14; gfx_drawstr("STEREO DIMENSION WIDTH & SUB-BASS MONO ANCHOR");

  top_h = 230;
  left_w = floor((st_w - 48) * 0.5);
  right_w = st_w - 48 - left_w - 12;

  // Crossover Plot
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, st_y + 44, left_w, top_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, st_y + 44, left_w, top_h, 0);
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 36; gfx_y = st_y + 56; gfx_drawstr("LINKWITZ-RILEY SUB-MONO CROSSOVER (SIDE CHANNEL HPF)");

  cx_plot_x = ws_x + 36; cx_plot_y = st_y + 80; cx_plot_w = left_w - 24; cx_plot_h = top_h - 48;
  gfx_r = 0.08; gfx_g = 0.12; gfx_b = 0.18;
  gfx_line(cx_plot_x, cx_plot_y + cx_plot_h * 0.5, cx_plot_x + cx_plot_w, cx_plot_y + cx_plot_h * 0.5);

  cut_f = (log(slider6 / 20.0) / log(10.0));
  cut_x = cx_plot_x + floor(cut_f * (cx_plot_w * 0.5));
  gfx_r = 1.0; gfx_g = 0.30; gfx_b = 0.20;
  gfx_line(cut_x, cx_plot_y, cut_x, cx_plot_y + cx_plot_h);
  gfx_setfont(3, "Consolas", 12, 'b');
  gfx_x = cut_x + 8; gfx_y = cx_plot_y + 20; gfx_printf("MONO CUT: %d Hz", slider6);

  // Right Stereo Scope
  rx = ws_x + 24 + left_w + 12;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(rx, st_y + 44, right_w, top_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(rx, st_y + 44, right_w, top_h, 0);
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = rx + 16; gfx_y = st_y + 56; gfx_drawstr("QUAD-WALL STEREO VECTOR SCOPE");

  v_cx = rx + right_w * 0.5; v_cy = st_y + 44 + top_h * 0.5 + 8;
  gfx_r = 0.10; gfx_g = 0.16; gfx_b = 0.24;
  gfx_circle(v_cx, v_cy, 65, 0);
  gfx_circle(v_cx, v_cy, 40, 0);
  gfx_line(v_cx - 65, v_cy, v_cx + 65, v_cy);
  gfx_line(v_cx, v_cy - 65, v_cx, v_cy + 65);

  // Bottom Sliders
  draw_param_slider(ws_x + 24, st_y + 288, st_w - 48, 62, "SUB-BASS MONO ANCHOR FREQUENCY CUTOFF", slider6, 40, 160, "%d Hz", 6, 0.00, 0.85, 1.00);
  draw_param_slider(ws_x + 24, st_y + 360, st_w - 48, 62, "QUAD-WALL STEREO DIMENSION WIDTH MULTIPLIER", slider25, 0.80, 1.40, "%.2f x", 25, 1.00, 0.85, 0.35);

  // Guidance Plaque
  g_y = st_y + 434; g_h = st_h - 446;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, g_y, st_w - 48, g_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, g_y, st_w - 48, g_h, 0);
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 36; gfx_y = g_y + 12; gfx_drawstr("SUB-BASS MONO & STEREO CORRIDOR ARCHITECTURE:");
  gfx_setfont(3, "Segoe UI", 13); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.96;
  gfx_x = ws_x + 36; gfx_y = g_y + 36;
  gfx_drawstr("• Elliptic Mono Anchor: Sums sub frequencies strictly to mono via side-channel HPF, leaving mid punch 100% untouched.");
  gfx_x = ws_x + 36; gfx_y = g_y + 60;
  gfx_drawstr("• Quad-Wall Width: Expands rhythm guitar tracks outward while anchoring the snare, kick, and lead vocal directly dead-center.");
);

// =============================================================================
// TAB 5: VOCAL POCKET CORRIDOR (DYNAMIC MID NOTCH & GMEM AUTONOMOUS SENSING)
// =============================================================================
slider1 == 5 ? (
  pk_y = ws_y + 12; pk_w = ws_w - 24; pk_h = ws_h - 24;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 12, pk_y, pk_w, pk_h);
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35; gfx_rect(ws_x + 12, pk_y, pk_w, pk_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = ws_x + 28; gfx_y = pk_y + 14; gfx_drawstr("VOCAL POCKET CORRIDOR // DYNAMIC MIDNOTCH & GMEM SENSING");

  top_h = 240;
  // Curve Plot
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, pk_y + 44, pk_w - 48, top_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, pk_y + 44, pk_w - 48, top_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = ws_x + 36; gfx_y = pk_y + 56; gfx_drawstr("DYNAMIC 2.2 kHz MID CARVE ATTENUATION PLOT");

  c_cx0 = ws_x + 36; c_cy0 = pk_y + 80; c_cw = pk_w - 72; c_ch = top_h - 48;
  cy_mid = c_cy0 + c_ch * 0.3;
  gfx_r = 0.10; gfx_g = 0.16; gfx_b = 0.24;
  gfx_line(c_cx0, cy_mid, c_cx0 + c_cw, cy_mid);

  // Dynamic Carve Curve
  gfx_r = 1.00; gfx_g = 0.40; gfx_b = 0.20;
  prev_y = cy_mid;
  pi = 0;
  loop(100,
    px = c_cx0 + floor((pi / 99.0) * c_cw);
    f_val = 200.0 * exp(log(50.0) * (pi / 99.0));
    dip = pocket_depth * exp(-0.5 * sqr((log(f_val / 2200.0) / 0.35)));
    cur_y = cy_mid + dip * 20.0;
    pi > 0 ? (
      gfx_line(prev_px, prev_py, px, cur_y);
      gfx_r = 1.00; gfx_g = 0.40; gfx_b = 0.20;
      gfx_line(px, cy_mid, px, cur_y);
    );
    prev_px = px; prev_py = cur_y;
    pi += 1;
  );

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  notch_str = sprintf(#, "LIVE VOCAL CARVE: -%.1f dB @ 2.2 kHz", pocket_depth);
  gfx_measurestr(notch_str, nsw, nsh);
  gfx_x = c_cx0 + floor((c_cw - nsw) * 0.5); gfx_y = cy_mid + 65;
  gfx_drawstr(notch_str);

  // Sliders
  draw_param_slider(ws_x + 24, pk_y + 300, pk_w - 48, 62, "MAX VOCAL POCKET DYNAMIC CARVE DEPTH", slider8, 0.0, 3.0, "-%.1f dB", 8, 1.00, 0.85, 0.35);

  // Corridor Mode Pill
  cm_y = pk_y + 372; cm_w = pk_w - 48;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, cm_y, cm_w, 42);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, cm_y, cm_w, 42, 0);

  hov_cm = (mouse_x >= ws_x + 24 && mouse_x <= ws_x + 24 + cm_w && mouse_y >= cm_y && mouse_y <= cm_y + 42);
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 36; gfx_y = cm_y + 12; gfx_drawstr("CORRIDOR AUTO-SENSING MODE:");

  cm_txt = slider9 ? "[ ACTIVE GMEM AUTO-SENSING ]" : "[ MANUAL DEPTH LOCK ]";
  gfx_setfont(3, "Consolas", 13, 'b'); gfx_r = slider9 ? 0.00 : 1.00; gfx_g = slider9 ? 0.95 : 0.85; gfx_b = slider9 ? 0.65 : 0.30;
  gfx_measurestr(cm_txt, cmtw, cmth);
  gfx_x = ws_x + cm_w - cmtw; gfx_y = cm_y + 12; gfx_drawstr(cm_txt);
  mouse_clicked && hov_cm ? (slider9 = !slider9; slider_automate(););

  // Advice
  adv_y = pk_y + 424; adv_h = pk_h - 438;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, adv_y, pk_w - 48, adv_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, adv_y, pk_w - 48, adv_h, 0);
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = ws_x + 36; gfx_y = adv_y + 12; gfx_drawstr("AUTONOMOUS VOCAL CARVE SYSTEM:");
  gfx_setfont(3, "Segoe UI", 13); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.96;
  gfx_x = ws_x + 36; gfx_y = adv_y + 36;
  gfx_drawstr("• Real-Time gmem Link: Monitors live Vocal Empress energy via shared telemetry memory (gmem[1452]).");
  gfx_x = ws_x + 36; gfx_y = adv_y + 60;
  gfx_drawstr("• Dynamic Notch: When the lead vocal sings, a transparent 2.2 kHz notch carves room in the instrumental mid channel.");
  gfx_x = ws_x + 36; gfx_y = adv_y + 84;
  gfx_drawstr("• Side-Channel Preservation: Rhythm guitars stay wide and thick in the side channels without losing tone.");
);

// =============================================================================
// TAB 6: PRODUCER SUMMING MATRIX (25 CLICKABLE TILES + FORENSIC HARDWARE PLAQUE)
// =============================================================================
slider1 == 6 ? (
  pm_y = ws_y + 12; pm_w = ws_w - 24; pm_h = ws_h - 24;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 12, pm_y, pm_w, pm_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 12, pm_y, pm_w, pm_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 28; gfx_y = pm_y + 14; gfx_drawstr("PRODUCER SUMMING MATRIX // 25 REFERENCE-CALIBRATED BENCHMARKS");

  // 25 Tiles in 4 Rows (7, 7, 7, 4)
  t_rows = 4;
  pi = 0;
  loop(25,
    row_idx = (pi < 7 ? 0 : (pi < 14 ? 1 : (pi < 21 ? 2 : 3)));
    col_idx = (pi < 7 ? pi : (pi < 14 ? pi - 7 : (pi < 21 ? pi - 14 : pi - 21)));
    row_cols = (row_idx < 3 ? 7 : 4);
    btn_w = floor((pm_w - 48 - (row_cols - 1) * 8) / row_cols);
    bx = ws_x + 24 + col_idx * (btn_w + 8);
    by = pm_y + 44 + row_idx * 40;
    bh = 32;

    is_sel = (slider2 == pi);
    b_hov = (mouse_x >= bx && mouse_x <= bx + btn_w && mouse_y >= by && mouse_y <= by + bh);

    gfx_r = is_sel ? 0.22 : (b_hov ? 0.12 : 0.035);
    gfx_g = is_sel ? 0.14 : (b_hov ? 0.08 : 0.045);
    gfx_b = is_sel ? 0.09 : (b_hov ? 0.06 : 0.060);
    gfx_rect(bx, by, btn_w, bh);

    gfx_r = is_sel ? 0.85 : (b_hov ? 0.50 : 0.20);
    gfx_g = is_sel ? 0.47 : (b_hov ? 0.35 : 0.28);
    gfx_b = is_sel ? 0.21 : (b_hov ? 0.25 : 0.38);
    gfx_rect(bx, by, btn_w, bh, 0);

    gfx_setfont(2, "Orbitron", 11.5, 'b');
    gfx_r = is_sel ? 1.0 : (b_hov ? 0.95 : 0.70);
    gfx_g = is_sel ? 0.9 : (b_hov ? 0.90 : 0.75);
    gfx_b = is_sel ? 0.4 : (b_hov ? 0.80 : 0.80);

    t_name = get_producer_short_name(pi);
    gfx_measurestr(t_name, tnw, tnh);
    gfx_x = bx + floor((btn_w - tnw) * 0.5); gfx_y = by + 8;
    gfx_drawstr(t_name);

    mouse_clicked && b_hov ? (
      slider2 = pi;
      prev_preset = slider2;
      apply_producer_preset(slider2);
    );
    pi += 1;
  );

  // Forensic Plaque
  plaque_y = pm_y + 44 + 4 * 40 + 8;
  plaque_h = pm_h - (plaque_y - pm_y) - 14;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, plaque_y, pm_w - 48, plaque_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 24, plaque_y, pm_w - 48, plaque_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;
  gfx_x = ws_x + 38; gfx_y = plaque_y + 16;
  gfx_printf("SELECTED BENCHMARK: %02d - %s", slider2, get_producer_full_title(slider2));

  // Specifications
  gfx_setfont(3, "Consolas", 13, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 38; gfx_y = plaque_y + 45;
  spec_str = sprintf(#, "CALIBRATION: Trim %+4.1fdB | Glue Thresh %.1fdB (Ratio %s) | Mud Scoop %+4.1fdB | Desk Drive +%.1fdB | Width %.2fx",
    slider4, slider12, slider13 == 0 ? "1.5:1" : (slider13 == 1 ? "2:1" : (slider13 == 2 ? "4:1" : "8:1")), slider20, slider24, slider25);
  gfx_drawstr(spec_str);

  gfx_setfont(3, "Segoe UI", 13.5); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = ws_x + 38; gfx_y = plaque_y + 75;
  gfx_drawstr("Full producer acoustic DNA matching the central preset registry. Recalls authentic console harmonic saturation,");
  gfx_x = ws_x + 38; gfx_y = plaque_y + 98;
  gfx_drawstr("VCA/Diode bus glue ballistics, and surgical tonal balance targets tailored for high-energy modern metal and rock.");

  // Dual Hardware Specification Sub-Panels
  sub_w = floor((pm_w - 96) / 2); sub_y = plaque_y + 126; sub_h = plaque_h - 138;
  // Left: Tonal & Dynamic Specs
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 38, sub_y, sub_w, sub_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 38, sub_y, sub_w, sub_h, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 48; gfx_y = sub_y + 8; gfx_drawstr("TONAL BALANCE & COMPRESSION BLUEPRINT");
  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.96;
  gfx_x = ws_x + 48; gfx_y = sub_y + 30; gfx_printf("Sub HPF Cutoff   : %d Hz (18dB/oct)", slider18);
  gfx_x = ws_x + 48; gfx_y = sub_y + 50; gfx_printf("80Hz Foundation  : %+4.1f dB (Low Shelf)", slider19);
  gfx_x = ws_x + 48; gfx_y = sub_y + 70; gfx_printf("220Hz Mud Scoop  : %+4.1f dB (Q=1.1)", slider20);
  gfx_x = ws_x + 48; gfx_y = sub_y + 90; gfx_printf("3.5kHz Pick Bite : %+4.1f dB (Presence)", slider21);
  gfx_x = ws_x + 48; gfx_y = sub_y + 110; gfx_printf("10kHz Air Sheen  : %+4.1f dB (High Shelf)", slider22);

  // Right: Console Summing & Spatial Specs
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 48 + sub_w, sub_y, sub_w, sub_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 48 + sub_w, sub_y, sub_w, sub_h, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 8; gfx_drawstr("CONSOLE SUMMING & SPATIAL ENGINE");
  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.96;
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 30; gfx_printf("Console Engine   : %s", slider23 == 1 ? "Neve 8014 Iron Desk" : (slider23 == 2 ? "Studer A800 Tape" : "Transparent"));
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 50; gfx_printf("Console Drive    : +%.1f dB THD", slider24);
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 70; gfx_printf("Sub-Mono Anchor  : %d Hz Side-Channel HPF", slider6);
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 90; gfx_printf("Stereo Width     : %.2f x Multiplier", slider25);
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 110; gfx_printf("Vocal Pocket Carve: -%.1f dB @ 2.2 kHz", pocket_depth);
);

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
"""

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

shutil.copy2(target_path, reaper_path)
print("Successfully generated and deployed Damei_InstrumentalSuite.jsfx")
