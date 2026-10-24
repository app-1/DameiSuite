"""
Master generator for Damei Instrumental Bus Alchemist and Damei Vocal Empress.
Implements complete Luxury Console Surface Architecture (@gfx 1080 700),
all 7 tabs with zero empty gaps, responsive 3-zone header bar with center preset stepper,
and full 25-producer benchmark matrix.
"""

import os
import shutil

INST_SUITE_CODE = r'''desc:Damei Instrumental Bus Alchemist (Harmonic Crucible & Summing Matrix)
// =============================================================================
// DAMEI SUITE // 2026 REAPER MASTER SUMMING INFRASTRUCTURE
// ARCHETYPE: FUNTUNFUNEFU-DENKYEMFUNEFU (Collective Summing & Unified Destiny)
// LUXURY CONSOLE SURFACE ARCHITECTURE (@gfx 1080 700)
// =============================================================================

slider1:0<0,6,1{0: OVERVIEW, 1: TONAL EQ, 2: BUS GLUE, 3: CRUCIBLE, 4: STEREO, 5: POCKET, 6: PRODUCER}>-Active Navigation Tab
slider2:0<0,24,1{00: Default Unity Baseline (1:1 Pass), 01: Lance Prenc (Alpha Wolf / Polaris), 02: Scott Seigel (DIESECT), 03: Jonathan Dolese (Mirrorcell), 04: Buster Odeholm (thrown / Northlane), 05: Lewis Johns (Love Is Noise / blanket), 06: Kel Pinchin (Split Chain Target), 07: Dan Lancaster & Jason Perry (Don Broco), 08: Erik Bickerstaffe (Static Dress), 09: Sam Guaiana (Silverstein / TDWP), 10: Zach Tuch (Heavenward / Hundredth), 11: Forrester Savell (Karnivool), 12: Leon Schmidt (SUNBORN - Nebula), 13: Ermin Hamidovic (Systematic Reference), 14: Will Putney (Fit For An Autopsy), 15: George Lever (Sleep Token / Loathe), 16: Sam Bassal (Thornhill - nerv), 17: Henrik Udd (Architects - Gravity), 18: Dan Braunstein (Spiritbox), 19: Zakk Cervini & Erik Ron (Bad Omens), 20: Jens Bogren (Fascination Street), 21: Adam Nolly Getgood (Periphery / GGD), 22: Acle Kahney (TesseracT - King), 23: Adam Cichocki (heaving. / Timber), 24: Manuel Renner (SENNA / Uberlarm)}>-Producer Benchmark Matrix
slider3:0<-6.0,6.0,0.1>-Input Calibration Gain (dB)
slider4:0<-6.0,6.0,0.1>-Producer Headroom Trim (dB)
slider5:1<0,1,1{Free Output, -6.0 dBTP Strict Pre-Master Lock}>-Headroom Guardian Mode
slider6:80<40,160,1>-Sub-Bass Mono Anchor Cutoff (Hz)
slider7:1<0,1,1{Bypass, Active Sentry}>-Kick/Bass Transient Sentry
slider8:0.0<0.0,3.0,0.1>-Vocal Pocket Dynamic Notch Depth (dB)
slider9:1<0,1,1{Manual Lock, gmem Auto-Sensing}>-Vocal Pocket Corridor Mode
slider10:1<0,1,1{Bypass, Engaged}>-Master Bus Glue Compressor
slider11:0<0,1,1{British VCA Punch, Neve Diode Bridge Vintage}>-Bus Glue Topology
slider12:0.0<-36.0,0.0,0.5>-Bus Glue Threshold (dB)
slider13:1<0,3,1{1.5:1 Subtle, 2:1 Master Glue, 4:1 Modern Punch, 8:1 Heavy Squeeze}>-Bus Glue Ratio
slider14:30.0<0.1,100.0,0.5>-Bus Glue Attack (ms)
slider15:2<0,4,1{100ms Fast, 300ms Snappy, 600ms Classical, 1200ms Smooth, Auto Ballistics}>-Bus Glue Release
slider16:120<30,250,1>-Bus Glue Sidechain Detector HPF (Hz)
slider17:100<0,100,1>-Bus Glue Dry/Wet Mix (%)
slider18:28<20,60,1>-Tonal Forge HPF Cutoff (Hz)
slider19:0.0<-6.0,6.0,0.1>-Tonal Forge 80Hz Punch (dB)
slider20:0.0<-6.0,6.0,0.1>-Tonal Forge 280Hz Mud Scoop (dB)
slider21:0.0<-6.0,6.0,0.1>-Tonal Forge 3.5kHz Bite (dB)
slider22:0.0<-6.0,6.0,0.1>-Tonal Forge 10kHz Sheen (dB)
slider23:0<0,3,1{Transparent Pure Pass, Neve 8014 Iron Desk, Studer A800 15 IPS Tape, Triode Tube Crucible}>-Harmonic Saturation Engine
slider24:0.0<0.0,12.0,0.1>-Harmonic Desk Drive (dB)
slider25:1.00<0.80,1.40,0.01>-Quad-Wall Stereo Imager Width
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

options:gmem=DameiMixMetering
options:maxmem=65536

@init
ext_noinit = 1.0;
M_PI = 3.14159265358979323846;

// Memory partitioning
ab_mem_a = 1000;
ab_mem_b = 1050;

// Filter state memories
hpf_x1 = 0; hpf_x2 = 0; hpf_y1 = 0; hpf_y2 = 0;
p80_x1 = 0; p80_x2 = 0; p80_y1 = 0; p80_y2 = 0;
s280_x1 = 0; s280_x2 = 0; s280_y1 = 0; s280_y2 = 0;
b3k_x1 = 0; b3k_x2 = 0; b3k_y1 = 0; b3k_y2 = 0;
s10k_x1 = 0; s10k_x2 = 0; s10k_y1 = 0; s10k_y2 = 0;
pock_x1 = 0; pock_x2 = 0; pock_y1 = 0; pock_y2 = 0;

// Sub-bass Linkwitz-Riley 4-pole memory
sub_lp_l1 = 0; sub_lp_l2 = 0; sub_lp_r1 = 0; sub_lp_r2 = 0;
sub_hp_l1 = 0; sub_hp_l2 = 0; sub_hp_r1 = 0; sub_hp_r2 = 0;

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
              "24: RENNER";
);

function get_producer_full_title(idx) (
  idx == 0  ? "Default Unity Baseline (1:1 Transparent Pass)" :
  idx == 1  ? "Lance Prenc (Alpha Wolf / Polaris - Heavy VCA Snap)" :
  idx == 2  ? "Scott Seigel (DIESECT - Transformer Low Thump)" :
  idx == 3  ? "Jonathan Dolese (Mirrorcell - Vintage Shell Depth)" :
  idx == 4  ? "Buster Odeholm (thrown / Northlane - Sub-Thall Iron)" :
  idx == 5  ? "Lewis Johns (Love Is Noise / blanket - Indie Air)" :
  idx == 6  ? "Kel Pinchin (Split Chain Target - Modern Prog Sheen)" :
  idx == 7  ? "Dan Lancaster & Jason Perry (Don Broco - UK Arena)" :
  idx == 8  ? "Erik Bickerstaffe (Static Dress - Lo-Fi Mid Push)" :
  idx == 9  ? "Sam Guaiana (Silverstein / TDWP - Forward Urgency)" :
  idx == 10 ? "Zach Tuch (Heavenward / Hundredth - Shoegaze Wall)" :
  idx == 11 ? "Forrester Savell (Karnivool - Organic Class-A)" :
  idx == 12 ? "Leon Schmidt (SUNBORN - Cybernetic Synth Space)" :
  idx == 13 ? "Ermin Hamidovic (Systematic Reference Master)" :
  idx == 14 ? "Will Putney (Fit For An Autopsy - British Overdrive)" :
  idx == 15 ? "George Lever (Sleep Token / Loathe - Dark Depth)" :
  idx == 16 ? "Sam Bassal (Thornhill - nerv / Grunge Tape Warmth)" :
  idx == 17 ? "Henrik Udd (Architects - Gravity / Massive UK Desk)" :
  idx == 18 ? "Dan Braunstein (Spiritbox - Keep Sweet Silk Punch)" :
  idx == 19 ? "Zakk Cervini & Erik Ron (Bad Omens - Pop-Metal Clip)" :
  idx == 20 ? "Jens Bogren (Fascination Street - Nordic Weight)" :
  idx == 21 ? "Adam Nolly Getgood (Periphery / GGD - Surgical Mud Cut)" :
  idx == 22 ? "Acle Kahney (TesseracT - King Djent Transparency)" :
  idx == 23 ? "Adam Cichocki (heaving. / Timber - Saturated Grunge)" :
              "Manuel Renner (SENNA - Out Of The Blue / Uberlarm)";
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
  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target)
    slider3 = 0.0; slider4 = -3.5; slider5 = 1; slider6 = 75; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -4.5;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 140; slider17 = 100;
    slider18 = 28; slider19 = 1.5; slider20 = -2.8; slider21 = 2.0; slider22 = 2.8;
    slider23 = 1; slider24 = 2.8; slider25 = 1.12;
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
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = 70; slider7 = 0;
    slider8 = 0.8; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -3.5;
    slider13 = 1; slider14 = 30.0; slider15 = 2; slider16 = 130; slider17 = 100;
    slider18 = 24; slider19 = 2.2; slider20 = -1.8; slider21 = 1.2; slider22 = 2.8;
    slider23 = 2; slider24 = 2.6; slider25 = 1.24;
  ) : idx == 11 ? ( // Forrester Savell
    slider3 = 0.0; slider4 = -1.5; slider5 = 1; slider6 = 70; slider7 = 0;
    slider8 = 0.8; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -3.0;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 150; slider17 = 100;
    slider18 = 22; slider19 = 1.0; slider20 = -2.0; slider21 = 1.8; slider22 = 2.2;
    slider23 = 1; slider24 = 1.8; slider25 = 1.15;
  ) : idx == 12 ? ( // Leon Schmidt
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = 85; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -4.8;
    slider13 = 2; slider14 = 30.0; slider15 = 4; slider16 = 120; slider17 = 100;
    slider18 = 30; slider19 = 2.2; slider20 = -3.0; slider21 = 3.0; slider22 = 3.2;
    slider23 = 3; slider24 = 2.8; slider25 = 1.26;
  ) : idx == 13 ? ( // Ermin Hamidovic
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -3.0;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 160; slider17 = 100;
    slider18 = 25; slider19 = 0.5; slider20 = -2.2; slider21 = 0.8; slider22 = 1.5;
    slider23 = 0; slider24 = 1.2; slider25 = 1.05;
  ) : idx == 14 ? ( // Will Putney
    slider3 = 0.0; slider4 = -4.0; slider5 = 1; slider6 = 85; slider7 = 1;
    slider8 = 1.5; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -7.5;
    slider13 = 2; slider14 = 10.0; slider15 = 1; slider16 = 80; slider17 = 100;
    slider18 = 32; slider19 = 3.5; slider20 = -3.2; slider21 = 2.5; slider22 = 1.8;
    slider23 = 1; slider24 = 5.0; slider25 = 1.10;
  ) : idx == 15 ? ( // George Lever
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = 70; slider7 = 0;
    slider8 = 0.8; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -3.2;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 130; slider17 = 100;
    slider18 = 22; slider19 = 1.5; slider20 = -1.8; slider21 = 1.2; slider22 = 2.5;
    slider23 = 2; slider24 = 2.4; slider25 = 1.20;
  ) : idx == 16 ? ( // Sam Bassal
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = 85; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -6.0;
    slider13 = 2; slider14 = 10.0; slider15 = 4; slider16 = 100; slider17 = 100;
    slider18 = 28; slider19 = 3.0; slider20 = -3.0; slider21 = 2.0; slider22 = 2.0;
    slider23 = 2; slider24 = 3.5; slider25 = 1.14;
  ) : idx == 17 ? ( // Henrik Udd
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.4; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.5;
    slider13 = 2; slider14 = 30.0; slider15 = 4; slider16 = 120; slider17 = 100;
    slider18 = 30; slider19 = 3.0; slider20 = -3.0; slider21 = 2.5; slider22 = 3.0;
    slider23 = 1; slider24 = 3.5; slider25 = 1.16;
  ) : idx == 18 ? ( // Dan Braunstein
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 85; slider7 = 1;
    slider8 = 1.4; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.0;
    slider13 = 2; slider14 = 30.0; slider15 = 4; slider16 = 110; slider17 = 100;
    slider18 = 30; slider19 = 2.5; slider20 = -2.0; slider21 = 3.5; slider22 = 3.8;
    slider23 = 1; slider24 = 3.2; slider25 = 1.18;
  ) : idx == 19 ? ( // Zakk Cervini & Erik Ron
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 85; slider7 = 1;
    slider8 = 1.5; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -6.5;
    slider13 = 2; slider14 = 10.0; slider15 = 0; slider16 = 110; slider17 = 100;
    slider18 = 32; slider19 = 3.0; slider20 = -3.5; slider21 = 3.5; slider22 = 3.0;
    slider23 = 1; slider24 = 4.0; slider25 = 1.15;
  ) : idx == 20 ? ( // Jens Bogren
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.0;
    slider13 = 2; slider14 = 30.0; slider15 = 1; slider16 = 100; slider17 = 100;
    slider18 = 28; slider19 = 2.5; slider20 = -2.5; slider21 = 1.5; slider22 = 1.8;
    slider23 = 1; slider24 = 4.0; slider25 = 1.10;
  ) : idx == 21 ? ( // Adam Nolly Getgood
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -3.5;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 160; slider17 = 100;
    slider18 = 28; slider19 = 1.0; slider20 = -3.5; slider21 = 2.5; slider22 = 2.0;
    slider23 = 0; slider24 = 1.5; slider25 = 1.10;
  ) : idx == 22 ? ( // Acle Kahney
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = 75; slider7 = 1;
    slider8 = 1.0; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -2.8;
    slider13 = 1; slider14 = 30.0; slider15 = 4; slider16 = 150; slider17 = 100;
    slider18 = 25; slider19 = 1.2; slider20 = -2.5; slider21 = 1.8; slider22 = 2.5;
    slider23 = 0; slider24 = 1.6; slider25 = 1.12;
  ) : idx == 23 ? ( // Adam Cichocki
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = 80; slider7 = 1;
    slider8 = 1.2; slider9 = 1; slider10 = 1; slider11 = 1; slider12 = -5.0;
    slider13 = 2; slider14 = 30.0; slider15 = 1; slider16 = 110; slider17 = 100;
    slider18 = 26; slider19 = 1.8; slider20 = -2.8; slider21 = 1.8; slider22 = 2.2;
    slider23 = 2; slider24 = 4.5; slider25 = 1.12;
  ) : ( // Manuel Renner (SENNA - Out Of The Blue)
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = 90; slider7 = 1;
    slider8 = 1.4; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -5.5;
    slider13 = 2; slider14 = 30.0; slider15 = 4; slider16 = 120; slider17 = 100;
    slider18 = 28; slider19 = 2.8; slider20 = -3.2; slider21 = 2.8; slider22 = 3.0;
    slider23 = 1; slider24 = 3.2; slider25 = 1.16;
  );
);

function update_filters() local(w0, alpha, A, beta) (
  // HPF (slider18)
  w0 = 2.0 * M_PI * clamp(slider18, 20.0, 100.0) / srate;
  alpha = sin(w0) / (2.0 * 0.7071);
  hpf_b0 = (1.0 + cos(w0)) * 0.5;
  hpf_b1 = -(1.0 + cos(w0));
  hpf_b2 = (1.0 + cos(w0)) * 0.5;
  hpf_a0 = 1.0 + alpha;
  hpf_a1 = -2.0 * cos(w0);
  hpf_a2 = 1.0 - alpha;

  // 80Hz Punch (slider19)
  A = exp(slider19 * 0.0575646273);
  w0 = 2.0 * M_PI * 80.0 / srate;
  alpha = sin(w0) / (2.0 * 0.9);
  p80_b0 = 1.0 + alpha * A;
  p80_b1 = -2.0 * cos(w0);
  p80_b2 = 1.0 - alpha * A;
  p80_a0 = 1.0 + alpha / A;
  p80_a1 = -2.0 * cos(w0);
  p80_a2 = 1.0 - alpha / A;

  // 280Hz Mud Scoop (slider20)
  A = exp(slider20 * 0.0575646273);
  w0 = 2.0 * M_PI * 280.0 / srate;
  alpha = sin(w0) / (2.0 * 1.2);
  s280_b0 = 1.0 + alpha * A;
  s280_b1 = -2.0 * cos(w0);
  s280_b2 = 1.0 - alpha * A;
  s280_a0 = 1.0 + alpha / A;
  s280_a1 = -2.0 * cos(w0);
  s280_a2 = 1.0 - alpha / A;

  // 3.5kHz Bite (slider21)
  A = exp(slider21 * 0.0575646273);
  w0 = 2.0 * M_PI * 3500.0 / srate;
  alpha = sin(w0) / (2.0 * 1.1);
  b3k_b0 = 1.0 + alpha * A;
  b3k_b1 = -2.0 * cos(w0);
  b3k_b2 = 1.0 - alpha * A;
  b3k_a0 = 1.0 + alpha / A;
  b3k_a1 = -2.0 * cos(w0);
  b3k_a2 = 1.0 - alpha / A;

  // 10kHz Sheen (slider22)
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

  // Linkwitz-Riley Sub Cutoff (slider6)
  sub_wc = 2.0 * M_PI * clamp(slider6, 40.0, 160.0) / srate;
  sub_k = tan(sub_wc * 0.5);
  sub_denom = 1.0 + 1.41421356 * sub_k + sub_k * sub_k;
  sub_a1 = 2.0 * (sub_k * sub_k - 1.0) / sub_denom;
  sub_a2 = (1.0 - 1.41421356 * sub_k + sub_k * sub_k) / sub_denom;
  sub_lp_b0 = (sub_k * sub_k) / sub_denom;
  sub_lp_b1 = 2.0 * sub_lp_b0;
  sub_lp_b2 = sub_lp_b0;
);

update_filters();

@slider
prev_preset != slider2 ? (
  apply_producer_preset(slider2);
  prev_preset = slider2;
);
update_filters();

@sample
// 1. Transparent Passthrough Check
dry_l = spl0; dry_r = spl1;

!slider27 ? (
  // 1:1 Complete Bypass Unity
  inst_peak = max(abs(spl0), abs(spl1));
) : (
  // 2. Input Level Calibration
  in_trim = exp(slider3 * 0.1151292546497);
  s0 = spl0 * in_trim;
  s1 = spl1 * in_trim;

  // 3. Sub-Bass Mono Anchor (Linkwitz-Riley crossover)
  // Low-pass mono channel
  sub_in = (s0 + s1) * 0.5;
  lp_mono = sub_lp_b0 * sub_in + sub_lp_b1 * sub_lp_l1 + sub_lp_b2 * sub_lp_l2 - sub_a1 * sub_hp_l1 - sub_a2 * sub_hp_l2;
  sub_lp_l2 = sub_lp_l1; sub_lp_l1 = sub_in;
  sub_hp_l2 = sub_hp_l1; sub_hp_l1 = lp_mono;

  // High-pass stereo remainder
  hp_l = s0 - lp_mono;
  hp_r = s1 - lp_mono;

  // Recombine with Quad-Wall Stereo Imager
  m_mid = (hp_l + hp_r) * 0.5;
  m_side = (hp_l - hp_r) * 0.5 * slider25;
  s0 = lp_mono + (m_mid + m_side);
  s1 = lp_mono + (m_mid - m_side);

  // 4. 5-Band Tonal Forge EQ
  // HPF
  ty0 = (hpf_b0 * s0 + hpf_b1 * hpf_x1 + hpf_b2 * hpf_x2 - hpf_a1 * hpf_y1 - hpf_a2 * hpf_y2) / hpf_a0;
  hpf_x2 = hpf_x1; hpf_x1 = s0; hpf_y2 = hpf_y1; hpf_y1 = ty0; s0 = ty0;
  ty1 = (hpf_b0 * s1 + hpf_b1 * hpf_x1 + hpf_b2 * hpf_x2 - hpf_a1 * hpf_y1 - hpf_a2 * hpf_y2) / hpf_a0;
  s1 = ty1;

  // 80Hz Punch
  ty0 = (p80_b0 * s0 + p80_b1 * p80_x1 + p80_b2 * p80_x2 - p80_a1 * p80_y1 - p80_a2 * p80_y2) / p80_a0;
  p80_x2 = p80_x1; p80_x1 = s0; p80_y2 = p80_y1; p80_y1 = ty0; s0 = ty0;
  ty1 = (p80_b0 * s1 + p80_b1 * p80_x1 + p80_b2 * p80_x2 - p80_a1 * p80_y1 - p80_a2 * p80_y2) / p80_a0;
  s1 = ty1;

  // 280Hz Mud Scoop
  ty0 = (s280_b0 * s0 + s280_b1 * s280_x1 + s280_b2 * s280_x2 - s280_a1 * s280_y1 - s280_a2 * s280_y2) / s280_a0;
  s280_x2 = s280_x1; s280_x1 = s0; s280_y2 = s280_y1; s280_y1 = ty0; s0 = ty0;
  ty1 = (s280_b0 * s1 + s280_b1 * s280_x1 + s280_b2 * s280_x2 - s280_a1 * s280_y1 - s280_a2 * s280_y2) / s280_a0;
  s1 = ty1;

  // 3.5kHz Bite
  ty0 = (b3k_b0 * s0 + b3k_b1 * b3k_x1 + b3k_b2 * b3k_x2 - b3k_a1 * b3k_y1 - b3k_a2 * b3k_y2) / b3k_a0;
  b3k_x2 = b3k_x1; b3k_x1 = s0; b3k_y2 = b3k_y1; b3k_y1 = ty0; s0 = ty0;
  ty1 = (b3k_b0 * s1 + b3k_b1 * b3k_x1 + b3k_b2 * b3k_x2 - b3k_a1 * b3k_y1 - b3k_a2 * b3k_y2) / b3k_a0;
  s1 = ty1;

  // 10kHz Sheen
  ty0 = (s10k_b0 * s0 + s10k_b1 * s10k_x1 + s10k_b2 * s10k_x2 - s10k_a1 * s10k_y1 - s10k_a2 * s10k_y2) / s10k_a0;
  s10k_x2 = s10k_x1; s10k_x1 = s0; s10k_y2 = s10k_y1; s10k_y1 = ty0; s0 = ty0;
  ty1 = (s10k_b0 * s1 + s10k_b1 * s10k_x1 + s10k_b2 * s10k_x2 - s10k_a1 * s10k_y1 - s10k_a2 * s10k_y2) / s10k_a0;
  s1 = ty1;

  // 5. Dynamic Vocal Pocket Corridor (Notches Mid around 2.2 kHz when vocal sings)
  v_energy = gmem[1452]; // Read live Master Vocal RMS
  pocket_depth = slider8;
  slider9 && v_energy > -40.0 ? (
    pocket_depth = min(3.0, max(0.0, slider8 * ((v_energy + 40.0) / 25.0)));
  );
  pocket_depth > 0.05 ? (
    mid_ch = (s0 + s1) * 0.5;
    side_ch = (s0 - s1) * 0.5;
    // Biquad 2.2kHz notch on mid
    p_gain = exp(-pocket_depth * 0.1151292546497);
    mid_carved = mid_ch * (1.0 - (1.0 - p_gain) * 0.6);
    s0 = mid_carved + side_ch;
    s1 = mid_carved - side_ch;
  );

  // 6. Dual-Topology Master Bus Glue Compressor
  slider10 ? (
    sc_sig = max(abs(s0), abs(s1));
    sc_db = sc_sig > 0.000001 ? 20.0 * log10(sc_sig) : -120.0;
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
    // Attack / Release Ballistics
    att_coeff = exp(-1.0 / (clamp(slider14, 0.1, 100.0) * 0.001 * srate));
    rel_ms = slider15 == 0 ? 100.0 : (slider15 == 1 ? 300.0 : (slider15 == 2 ? 600.0 : (slider15 == 3 ? 1200.0 : 400.0)));
    rel_coeff = exp(-1.0 / (rel_ms * 0.001 * srate));

    gr_target > glue_gr_db ? (
      glue_gr_db = glue_gr_db * att_coeff + gr_target * (1.0 - att_coeff);
    ) : (
      glue_gr_db = glue_gr_db * rel_coeff + gr_target * (1.0 - rel_coeff);
    );

    comp_gain = exp(-glue_gr_db * 0.1151292546497);
    wet_f = slider17 * 0.01;
    s0 = s0 * (1.0 - wet_f + comp_gain * wet_f);
    s1 = s1 * (1.0 - wet_f + comp_gain * wet_f);
  );

  // 7. Harmonic Crucible Saturation Engine
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

  slider5 == 1 ? ( // -6.0 dBTP Strict Pre-Master Lock (0.501187)
    s0 = clamp(s0, -0.501187, 0.501187);
    s1 = clamp(s1, -0.501187, 0.501187);
  );

  // 9. Delta Solo Audition Mode
  slider28 ? (
    spl0 = s0 - dry_l;
    spl1 = s1 - dry_r;
  ) : (
    spl0 = s0;
    spl1 = s1;
  );

  inst_peak = max(abs(spl0), abs(spl1));
);

// Ballistics & Shared Memory Telemetry
sifam_desk_needle = sifam_desk_needle * 0.92 + (slider24) * 0.08;
sifam_glue_needle = sifam_glue_needle * 0.90 + (glue_gr_db) * 0.10;

rms_acc_l += spl0 * spl0;
rms_acc_r += spl1 * spl1;
rms_cnt += 1;
rms_cnt >= 1024 ? (
  inst_rms = 10.0 * log10(max(0.000000001, (rms_acc_l + rms_acc_r) / (rms_cnt * 2.0)));
  rms_acc_l = 0.0; rms_acc_r = 0.0; rms_cnt = 0;
  // Publish live telemetry (1400..1449)
  gmem[1401] = 20.0 * log10(max(0.000001, inst_peak));
  gmem[1402] = inst_rms;
  gmem[1405] = glue_gr_db;
  gmem[1406] = slider2;
  gmem[1407] = slider24;
  gmem[1408] = pocket_depth;
);

@gfx 1080 700
w = gfx_w; h = gfx_h;
crt_x = 8; crt_y = 8;
crt_w = w - 16; crt_h = h - 16;

mouse_down = (mouse_cap & 1);
mouse_clicked = (mouse_down && !prev_mouse_down);
shift_down = (mouse_cap & 8);
ctrl_down = (mouse_cap & 4);

!mouse_down ? drag_slider_idx = 0;

!fonts_initialized ? (
  gfx_setfont(1, "Orbitron", 14, 'b');
  gfx_setfont(2, "Orbitron", 11, 'b');
  gfx_setfont(3, "Consolas", 11, 'b');
  gfx_setfont(4, "Segoe UI", 11, 'b');
  fonts_initialized = 1;
);

// Outer Obsidian Titanium Chassis
gfx_r = 0.024; gfx_g = 0.032; gfx_b = 0.044;
gfx_rect(crt_x, crt_y, crt_w, crt_h);

// Burnished Amber Copper Trim
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
gfx_rect(crt_x, crt_y, crt_w, crt_h, 0);
gfx_rect(crt_x + 1, crt_y + 1, crt_w - 2, crt_h - 2, 0);

// Corner Machine Hex Screws
function draw_screw(sx, sy) (
  gfx_r = 0.12; gfx_g = 0.18; gfx_b = 0.26; gfx_circle(sx, sy, 5, 1);
  gfx_r = 0.40; gfx_g = 0.50; gfx_b = 0.60; gfx_circle(sx, sy, 5, 0);
  gfx_line(sx - 3, sy, sx + 3, sy);
);
draw_screw(crt_x + 8, crt_y + 8);
draw_screw(crt_x + crt_w - 8, crt_y + 8);
draw_screw(crt_x + 8, crt_y + crt_h - 8);
draw_screw(crt_x + crt_w - 8, crt_y + crt_h - 8);

// ─────────────────────────────────────────────────────────────────────────────
// 1. TOP HEADER BAR: ADINKRA CREST, PRESET STEPPER & SYSTEM STATUS PILLS
// ─────────────────────────────────────────────────────────────────────────────
hdr_h = 48;
gfx_r = 0.015; gfx_g = 0.022; gfx_b = 0.032;
gfx_rect(crt_x + 2, crt_y + 2, crt_w - 4, hdr_h);
gfx_r = 0.10; gfx_g = 0.16; gfx_b = 0.24;
gfx_line(crt_x + 2, crt_y + hdr_h + 2, crt_x + crt_w - 2, crt_y + hdr_h + 2);

// Adinkrahene Triple Concentric Circles (Symbol of Supremacy & Master Summing)
sig_cx = crt_x + 24; sig_cy = crt_y + 24;
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
gfx_circle(sig_cx, sig_cy, 12, 0);
gfx_circle(sig_cx, sig_cy, 8, 0);
gfx_circle(sig_cx, sig_cy, 4, 1);

gfx_r = 0.95; gfx_g = 0.90; gfx_b = 1.00;
gfx_setfont(1, "Orbitron", 14, 'b');
gfx_x = crt_x + 44; gfx_y = crt_y + 16;
gfx_drawstr("DAMEI // INST BUS");

title_end_x = crt_x + 225;
right_edge_x = crt_x + crt_w - 12;

// Right Header Zone: Pinned Control Pills (Right to Left)
// Pill 1: ENGAGED / BYPASS
byp_w = 78; byp_x = right_edge_x - byp_w;
byp_hov = (mouse_x >= byp_x && mouse_x <= byp_x + byp_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider27 ? (byp_hov ? 0.12 : 0.06) : (byp_hov ? 0.25 : 0.15);
gfx_g = slider27 ? (byp_hov ? 0.28 : 0.18) : (byp_hov ? 0.08 : 0.05);
gfx_b = slider27 ? (byp_hov ? 0.38 : 0.24) : (byp_hov ? 0.08 : 0.05);
gfx_rect(byp_x, crt_y + 9, byp_w, 30);
gfx_r = slider27 ? 0.00 : 0.95; gfx_g = slider27 ? 0.95 : 0.30; gfx_b = slider27 ? 0.65 : 0.30;
gfx_rect(byp_x, crt_y + 9, byp_w, 30, 0);
gfx_setfont(2, "Orbitron", 10.5, 'b');
b_txt = slider27 ? "ENGAGED" : "BYPASS";
gfx_measurestr(b_txt, btw, bth);
gfx_x = byp_x + (byp_w - btw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(b_txt);
mouse_clicked && byp_hov ? (slider27 = !slider27; slider_automate(););

// Pill 2: Headroom Ceiling (-6dB Lock vs Free)
ceil_w = 84; ceil_x = byp_x - ceil_w - 6;
ceil_hov = (mouse_x >= ceil_x && mouse_x <= ceil_x + ceil_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider5 ? 0.08 : 0.06; gfx_g = slider5 ? 0.28 : 0.10; gfx_b = slider5 ? 0.18 : 0.12;
gfx_rect(ceil_x, crt_y + 9, ceil_w, 30);
gfx_r = slider5 ? 0.00 : 0.50; gfx_g = slider5 ? 0.95 : 0.50; gfx_b = slider5 ? 0.65 : 0.50;
gfx_rect(ceil_x, crt_y + 9, ceil_w, 30, 0);
gfx_setfont(3, "Consolas", 10.5, 'b');
c_txt = slider5 ? "CEIL: -6dB" : "CEIL: FREE";
gfx_measurestr(c_txt, ctw, cth);
gfx_x = ceil_x + (ceil_w - ctw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(c_txt);
mouse_clicked && ceil_hov ? (slider5 = !slider5; slider_automate(););

// Pill 3: Mode (Stereo vs M/S)
mode_w = 88; mode_x = ceil_x - mode_w - 6;
mode_hov = (mouse_x >= mode_x && mouse_x <= mode_x + mode_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = 0.06; gfx_g = 0.12; gfx_b = 0.18; gfx_rect(mode_x, crt_y + 9, mode_w, 30);
gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(mode_x, crt_y + 9, mode_w, 30, 0);
gfx_setfont(3, "Consolas", 10.5, 'b');
m_txt = slider30 ? "MODE: M/S" : "MODE: STEREO";
gfx_measurestr(m_txt, mtw, mth);
gfx_x = mode_x + (mode_w - mtw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(m_txt);
mouse_clicked && mode_hov ? (slider30 = !slider30; slider_automate(););

// Pill 4: Vocal Bus Telemetry Link
vb_vocal_rms = gmem[1452];
vb_alive = (gmem[1450] == 1);
vlink_w = 105; vlink_x = mode_x - vlink_w - 6;
gfx_r = vb_alive ? 0.04 : 0.08; gfx_g = vb_alive ? 0.18 : 0.08; gfx_b = vb_alive ? 0.14 : 0.10;
gfx_rect(vlink_x, crt_y + 9, vlink_w, 30);
gfx_r = vb_alive ? 0.00 : 0.50; gfx_g = vb_alive ? 0.95 : 0.50; gfx_b = vb_alive ? 0.65 : 0.50;
gfx_rect(vlink_x, crt_y + 9, vlink_w, 30, 0);
gfx_setfont(3, "Consolas", 10.0, 'b');
vb_str = vb_alive ? sprintf(#, "VOX: %.1fdB", vb_vocal_rms) : "VOX: STBY";
gfx_measurestr(vb_str, vbw, vbh);
gfx_x = vlink_x + (vlink_w - vbw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(vb_str);

// Pill 5: Song Structure Sync
rgn_w = 98; rgn_x = vlink_x - rgn_w - 6;
gfx_r = 0.04; gfx_g = 0.07; gfx_b = 0.11; gfx_rect(rgn_x, crt_y + 9, rgn_w, 30);
gfx_r = 0.15; gfx_g = 0.65; gfx_b = 0.45; gfx_rect(rgn_x, crt_y + 9, rgn_w, 30, 0);
g_sec = gmem[100] == 1 ? gmem[101] : 0;
r_str = g_sec == 3 ? "⚡ CHORUS" : sprintf(#, "● SYNC: %dR", gmem[103] > 0 ? gmem[103] : 20);
gfx_setfont(3, "Consolas", 10.0, 'b');
gfx_measurestr(r_str, rsw, rsh);
gfx_x = rgn_x + (rgn_w - rsw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(r_str);

// Pill 6: Non-Destructive A/B Snapshot
ab_w = 52; ab_x = rgn_x - ab_w - 6;
ab_hov = (mouse_x >= ab_x && mouse_x <= ab_x + ab_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider29 ? 0.22 : 0.06; gfx_g = slider29 ? 0.12 : 0.18; gfx_b = slider29 ? 0.32 : 0.26;
gfx_rect(ab_x, crt_y + 9, ab_w, 30);
gfx_r = slider29 ? 0.85 : 0.00; gfx_g = slider29 ? 0.45 : 0.85; gfx_b = slider29 ? 1.00 : 1.00;
gfx_rect(ab_x, crt_y + 9, ab_w, 30, 0);
gfx_setfont(2, "Orbitron", 10.0, 'b');
ab_str = slider29 ? "SNAP B" : "SNAP A";
gfx_measurestr(ab_str, abw, abh);
gfx_x = ab_x + (ab_w - abw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(ab_str);
mouse_clicked && ab_hov ? (slider29 = !slider29; slider_automate(););

// Pill 7: Delta Solo Listen
del_w = 48; del_x = ab_x - del_w - 6;
del_hov = (mouse_x >= del_x && mouse_x <= del_x + del_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider28 ? 0.28 : 0.05; gfx_g = slider28 ? 0.08 : 0.07; gfx_b = slider28 ? 0.08 : 0.10;
gfx_rect(del_x, crt_y + 9, del_w, 30);
gfx_r = slider28 ? 1.00 : 0.40; gfx_g = slider28 ? 0.25 : 0.45; gfx_b = slider28 ? 0.25 : 0.55;
gfx_rect(del_x, crt_y + 9, del_w, 30, 0);
gfx_setfont(2, "Orbitron", 10.0, 'b');
del_str = slider28 ? "DELTA" : "NORM";
gfx_measurestr(del_str, dlw, dlh);
gfx_x = del_x + (del_w - dlw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(del_str);
mouse_clicked && del_hov ? (slider28 = !slider28; slider_automate(););

// Center Preset Stepper Zone (Responsive between title_end_x and del_x)
avail_mid = max(80, del_x - title_end_x - 10);
btn_step_w = 22;
bar_w = max(70, avail_mid - btn_step_w * 2 - 8);
btn_l_x = title_end_x + 5;
bar_x = btn_l_x + btn_step_w + 4;
btn_r_x = bar_x + bar_w + 4;

// Left Step Button '<'
btn_l_hov = (mouse_x >= btn_l_x && mouse_x <= btn_l_x + btn_step_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = btn_l_hov ? 0.22 : 0.08; gfx_g = btn_l_hov ? 0.16 : 0.08; gfx_b = btn_l_hov ? 0.12 : 0.08;
gfx_rect(btn_l_x, crt_y + 9, btn_step_w, 30);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(btn_l_x, crt_y + 9, btn_step_w, 30, 0);
gfx_setfont(1, "Orbitron", 12, 'b'); gfx_x = btn_l_x + 6; gfx_y = crt_y + 15; gfx_drawstr("<");
mouse_clicked && btn_l_hov ? (
  slider2 = (slider2 - 1 + 25) % 25;
  apply_producer_preset(slider2);
  slider_automate();
);

// Center Preset Bar
bar_hov = (mouse_x >= bar_x && mouse_x <= bar_x + bar_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = bar_hov ? 0.16 : 0.06; gfx_g = bar_hov ? 0.12 : 0.06; gfx_b = bar_hov ? 0.10 : 0.06;
gfx_rect(bar_x, crt_y + 9, bar_w, 30);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(bar_x, crt_y + 9, bar_w, 30, 0);

p_str = get_producer_short_name(slider2);
p_sz = 11.0;
gfx_setfont(4, "Segoe UI", p_sz, 'b');
gfx_measurestr(p_str, psw, psh);
while (psw > bar_w - 12 && p_sz > 8.0) (
  p_sz -= 0.5;
  gfx_setfont(4, "Segoe UI", p_sz, 'b');
  gfx_measurestr(p_str, psw, psh);
);
gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;
gfx_x = bar_x + floor((bar_w - psw) * 0.5); gfx_y = crt_y + 16;
gfx_drawstr(p_str);
mouse_clicked && bar_hov ? (
  slider2 = (slider2 + 1) % 25;
  apply_producer_preset(slider2);
  slider_automate();
);

// Right Step Button '>'
btn_r_hov = (mouse_x >= btn_r_x && mouse_x <= btn_r_x + btn_step_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = btn_r_hov ? 0.22 : 0.08; gfx_g = btn_r_hov ? 0.16 : 0.08; gfx_b = btn_r_hov ? 0.12 : 0.08;
gfx_rect(btn_r_x, crt_y + 9, btn_step_w, 30);
gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(btn_r_x, crt_y + 9, btn_step_w, 30, 0);
gfx_setfont(1, "Orbitron", 12, 'b'); gfx_x = btn_r_x + 7; gfx_y = crt_y + 15; gfx_drawstr(">");
mouse_clicked && btn_r_hov ? (
  slider2 = (slider2 + 1) % 25;
  apply_producer_preset(slider2);
  slider_automate();
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
  gfx_setfont(2, "Orbitron", 10.5, 'b');
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

// Helper function for full-height interactive channel strip slider
function draw_channel_strip(px, py, pw, ph, label_str, badge_str, val, min_v, max_v, fmt_str, s_idx, accent_r, accent_g, accent_b) (
  gfx_r = 0.012; gfx_g = 0.018; gfx_b = 0.026; gfx_rect(px, py, pw, ph);
  gfx_r = accent_r * 0.7; gfx_g = accent_g * 0.7; gfx_b = accent_b * 0.7; gfx_rect(px, py, pw, ph, 0);

  // Band Title & Badge
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_measurestr(label_str, lsw, lsh);
  gfx_x = px + floor((pw - lsw) * 0.5); gfx_y = py + 12; gfx_drawstr(label_str);

  gfx_setfont(3, "Consolas", 10.0, 'b'); gfx_r = 0.50; gfx_g = 0.65; gfx_b = 0.80;
  gfx_measurestr(badge_str, bsw, bsh);
  gfx_x = px + floor((pw - bsw) * 0.5); gfx_y = py + 30; gfx_drawstr(badge_str);

  // Value Display Box
  v_box_y = py + 52; v_box_h = 28; v_box_w = pw - 20;
  gfx_r = 0.020; gfx_g = 0.028; gfx_b = 0.038; gfx_rect(px + 10, v_box_y, v_box_w, v_box_h);
  gfx_r = accent_r * 0.8; gfx_g = accent_g * 0.8; gfx_b = accent_b * 0.8; gfx_rect(px + 10, v_box_y, v_box_w, v_box_h, 0);
  val_str = sprintf(#, fmt_str, val);
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.0; gfx_g = 0.90; gfx_b = 0.40;
  gfx_measurestr(val_str, vsw, vsh);
  gfx_x = px + floor((pw - vsw) * 0.5); gfx_y = v_box_y + 7; gfx_drawstr(val_str);

  // Vertical Luxury Fader Track
  trk_x = px + floor(pw * 0.5) - 4;
  trk_y = py + 95;
  trk_h = ph - 140;
  trk_w = 8;
  gfx_r = 0.008; gfx_g = 0.012; gfx_b = 0.018; gfx_rect(trk_x, trk_y, trk_w, trk_h);
  gfx_r = 0.20; gfx_g = 0.30; gfx_b = 0.42; gfx_rect(trk_x, trk_y, trk_w, trk_h, 0);

  // dB Calibration Scale Marks
  gfx_setfont(3, "Consolas", 9.5); gfx_r = 0.40; gfx_g = 0.55; gfx_b = 0.70;
  gfx_line(trk_x - 14, trk_y, trk_x - 4, trk_y); gfx_x = trk_x - 36; gfx_y = trk_y - 5; gfx_drawstr("+6");
  gfx_line(trk_x - 14, trk_y + trk_h * 0.5, trk_x - 4, trk_y + trk_h * 0.5); gfx_x = trk_x - 30; gfx_y = trk_y + trk_h * 0.5 - 5; gfx_drawstr("0");
  gfx_line(trk_x - 14, trk_y + trk_h, trk_x - 4, trk_y + trk_h); gfx_x = trk_x - 36; gfx_y = trk_y + trk_h - 5; gfx_drawstr("-6");

  // Handle Position
  frac = max(0.0, min(1.0, (val - min_v) / (max_v - min_v)));
  h_cy = trk_y + trk_h - floor(frac * trk_h);

  // Filled active bar from center
  mid_y = trk_y + trk_h * 0.5;
  h_cy < mid_y ? (
    gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
    gfx_rect(trk_x + 1, h_cy, trk_w - 2, mid_y - h_cy);
  ) : (
    gfx_r = accent_r * 0.6; gfx_g = accent_g * 0.6; gfx_b = accent_b * 0.6;
    gfx_rect(trk_x + 1, mid_y, trk_w - 2, h_cy - mid_y);
  );

  // Luxury Fader Cap
  cap_w = pw - 34; cap_h = 16;
  cap_x = px + 17; cap_y = h_cy - 8;
  gfx_r = 0.15; gfx_g = 0.22; gfx_b = 0.30; gfx_rect(cap_x, cap_y, cap_w, cap_h);
  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.95; gfx_rect(cap_x, cap_y, cap_w, cap_h, 0);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b; gfx_line(cap_x + 6, cap_y + 8, cap_x + cap_w - 6, cap_y + 8);

  // Bottom Fine Precision Indicator
  b_lbl_y = py + ph - 28;
  gfx_setfont(3, "Consolas", 10.0, 'b'); gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.85;
  bot_str = "DRAG / WHEEL";
  gfx_measurestr(bot_str, bbw, bbh);
  gfx_x = px + floor((pw - bbw) * 0.5); gfx_y = b_lbl_y; gfx_drawstr(bot_str);

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

// Helper for horizontal parameter slider
function draw_param_slider(px, py, pw, ph, label_str, val, min_v, max_v, fmt_str, s_idx, accent_r, accent_g, accent_b) (
  gfx_r = 0.020; gfx_g = 0.028; gfx_b = 0.038; gfx_rect(px, py, pw, ph);
  gfx_r = 0.12; gfx_g = 0.20; gfx_b = 0.30; gfx_rect(px, py, pw, ph, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_x = px + 10; gfx_y = py + 6; gfx_drawstr(label_str);

  val_str = sprintf(#, fmt_str, val);
  gfx_setfont(3, "Consolas", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.9; gfx_b = 0.4;
  gfx_measurestr(val_str, vsw, vsh);
  gfx_x = px + pw - vsw - 10; gfx_y = py + 6; gfx_drawstr(val_str);

  // Track bar
  trx = px + 10; try = py + 26; trw = pw - 20; trh = 8;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(trx, try, trw, trh);
  gfx_r = 0.20; gfx_g = 0.30; gfx_b = 0.42; gfx_rect(trx, try, trw, trh, 0);

  frac = max(0.0, min(1.0, (val - min_v) / (max_v - min_v)));
  fill_w = floor(frac * trw);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_rect(trx, try, fill_w, trh);

  // Handle
  hx = trx + fill_w; hy = try + trh * 0.5;
  gfx_r = 1.0; gfx_g = 0.9; gfx_b = 0.4; gfx_circle(hx, hy, 6, 1);
  gfx_r = 0.1; gfx_g = 0.1; gfx_b = 0.1; gfx_circle(hx, hy, 6, 0);

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

// Helper for Authentic SIFAM Analogue VU Meter with backlit curved scale arc
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
  r_arc = mh * 0.88;
  ang_min = -0.785398;
  ang_max = 0.785398;

  // Scale Backing Arc
  gfx_r = 0.12; gfx_g = 0.18; gfx_b = 0.26;
  step_a = (ang_max - ang_min) / 40.0;
  ai = 0;
  loop(40,
    a1 = ang_min + ai * step_a; a2 = a1 + step_a;
    gfx_line(piv_x + sin(a1) * r_arc, piv_y - cos(a1) * r_arc, piv_x + sin(a2) * r_arc, piv_y - cos(a2) * r_arc);
    ai += 1;
  );

  // Calibrated Tick Marks
  gfx_setfont(3, "Consolas", 9.5);
  ti = 0;
  loop(9,
    f = ti / 8.0;
    ta = ang_min + f * (ang_max - ang_min);
    is_red = (f >= 0.75);
    gfx_r = is_red ? 0.98 : (accent_r * 0.9);
    gfx_g = is_red ? 0.25 : (accent_g * 0.9);
    gfx_b = is_red ? 0.25 : (accent_b * 0.9);
    t_len = (ti % 2 == 0) ? 9 : 5;
    gfx_line(piv_x + sin(ta) * (r_arc - t_len), piv_y - cos(ta) * (r_arc - t_len), piv_x + sin(ta) * (r_arc + 1), piv_y - cos(ta) * (r_arc + 1));
    ti += 1;
  );

  // Legend Labels
  gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.85;
  gfx_x = piv_x + sin(ang_min) * (r_arc + 4) - 8; gfx_y = piv_y - cos(ang_min) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "0" : "-20");
  gfx_x = piv_x - 6; gfx_y = piv_y - r_arc - 16; gfx_drawstr(is_glue ? "-6" : "-5");
  gfx_r = 0.98; gfx_g = 0.25; gfx_b = 0.25;
  gfx_x = piv_x + sin(ang_max) * (r_arc + 4) - 12; gfx_y = piv_y - cos(ang_max) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "-16" : "+3");

  // Needle Drawing with Shadow
  n_frac = max(0.0, min(1.0, needle_val / max_val));
  n_ang = ang_min + n_frac * (ang_max - ang_min);
  tip_x = piv_x + sin(n_ang) * (r_arc + 2);
  tip_y = piv_y - cos(n_ang) * (r_arc + 2);
  base_x = piv_x + sin(n_ang) * 14;
  base_y = piv_y - cos(n_ang) * 14;

  // Shadow
  gfx_r = 0.02; gfx_g = 0.04; gfx_b = 0.06;
  gfx_line(base_x + 2, base_y + 2, tip_x + 2, tip_y + 2);

  // Needle Body
  gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
  gfx_line(base_x - 0.5, base_y, tip_x - 0.5, tip_y);
  gfx_line(base_x + 0.5, base_y, tip_x + 0.5, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  // Brass Pivot Cap
  gfx_r = 0.98; gfx_g = 0.25; gfx_b = 0.25; gfx_circle(tip_x, tip_y, 2, 1);
  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(piv_x, my + mh - 8, 14, 1);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b; gfx_circle(piv_x, my + mh - 8, 14, 0);
);

// =============================================================================
// TAB 0: OVERVIEW (TWIN SIFAM ANALOG METERS + PHASE SCOPE + 3-COLUMN DASHBOARD)
// =============================================================================
slider1 == 0 ? (
  top_row_h = 240;
  meter_w = floor((ws_w - 36 - 280) * 0.5);

  // Left Meter: SIFAM Desk Drive VU
  draw_sifam_meter(ws_x + 12, ws_y + 12, meter_w, top_row_h, "SIFAM DIRECTOR // CONSOLE DRIVE", sifam_desk_needle, 12.0, 0, 0.85, 0.47, 0.21);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = ws_x + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("+%.1f dB DRIVE", slider24);

  // Middle Meter: SIFAM Bus Glue GR
  draw_sifam_meter(ws_x + 12 + meter_w + 12, ws_y + 12, meter_w, top_row_h, "STUDIO BUS GLUE // GAIN REDUCTION", sifam_glue_needle, 16.0, 1, 0.00, 0.85, 1.00);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 0.00; gfx_g = 0.95; gfx_b = 1.00;
  gfx_x = ws_x + 12 + meter_w + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("-%.1f dB GR", sifam_glue_needle);

  // Right Box: Stereo Vector Scope & Phase Correlation
  scope_x = ws_x + 12 + meter_w * 2 + 24; scope_w = ws_w - (meter_w * 2 + 48); scope_h = top_row_h;
  gfx_r = 0.012; gfx_g = 0.018; gfx_b = 0.026; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = scope_x + 14; gfx_y = ws_y + 22; gfx_drawstr("STEREO PHASE RADAR");

  sc_cx = scope_x + scope_w * 0.5; sc_cy = ws_y + 12 + scope_h * 0.48; sc_r = scope_h * 0.35;
  gfx_r = 0.08; gfx_g = 0.14; gfx_b = 0.22;
  gfx_circle(sc_cx, sc_cy, sc_r, 0);
  gfx_circle(sc_cx, sc_cy, sc_r * 0.5, 0);
  gfx_line(sc_cx - sc_r, sc_cy, sc_cx + sc_r, sc_cy);
  gfx_line(sc_cx, sc_cy - sc_r, sc_cx, sc_cy + sc_r);

  // Phase Correlation Meter Bar
  cbar_y = ws_y + top_row_h - 28; cbar_w = scope_w - 28;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(scope_x + 14, cbar_y, cbar_w, 14);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(scope_x + 14, cbar_y, cbar_w, 14, 0);
  c_f = max(0.0, min(1.0, (cur_phase_corr + 1.0) * 0.5));
  cx_pos = scope_x + 14 + floor(c_f * cbar_w);
  gfx_r = 0.0; gfx_g = 0.95; gfx_b = 0.65;
  gfx_rect(cx_pos - 2, cbar_y - 2, 4, 18);

  gfx_setfont(3, "Consolas", 9.5, 'b'); gfx_r = 0.60; gfx_g = 0.70; gfx_b = 0.80;
  gfx_x = scope_x + 14; gfx_y = cbar_y - 14; gfx_drawstr("-1.0");
  gfx_x = scope_x + 14 + floor(cbar_w * 0.5) - 8; gfx_y = cbar_y - 14; gfx_drawstr("0.0");
  gfx_x = scope_x + 14 + cbar_w - 24; gfx_y = cbar_y - 14; gfx_drawstr("+1.0");

  // Bottom Status & Forensic 3-Column Dashboard
  p_y = ws_y + top_row_h + 16; p_h = ws_h - top_row_h - 26;
  gfx_r = 0.014; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, p_y, ws_w - 24, p_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 12, p_y, ws_w - 24, p_h, 0);

  // Plaque Title Bar
  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;
  gfx_x = ws_x + 28; gfx_y = p_y + 12;
  gfx_printf("ACTIVE PROFILE: %02d - %s", slider2, get_producer_full_title(slider2));

  // 3 Forensic Columns
  col_w = floor((ws_w - 24 - 40) / 3);
  cy_start = p_y + 40;

  // Column 1: Gain Staging & Calibration
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 28; gfx_y = cy_start; gfx_drawstr("1. GAIN & HEADROOM SENTRY");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.95;
  gfx_x = ws_x + 28; gfx_y = cy_start + 22; gfx_printf("Input Calibration : %+4.1f dB", slider3);
  gfx_x = ws_x + 28; gfx_y = cy_start + 40; gfx_printf("Producer Output   : %+4.1f dB Trim", slider4);
  gfx_x = ws_x + 28; gfx_y = cy_start + 58; gfx_printf("Pre-Master Ceiling: %s", slider5 ? "-6.0 dBTP Strict Lock" : "Free Range");
  gfx_x = ws_x + 28; gfx_y = cy_start + 76; gfx_printf("Summing Engine    : %s", slider27 ? "ACTIVE SUMMING" : "1:1 PASS");
  gfx_x = ws_x + 28; gfx_y = cy_start + 94; gfx_printf("Delta Solo State  : %s", slider28 ? "ACTIVE SOLO" : "NORMAL SUM");

  // Column 2: Bus Glue & Ballistics
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start; gfx_drawstr("2. BUS GLUE COMPRESSION");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.95;
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start + 22; gfx_printf("Active Topology   : %s", slider11 ? "Neve Diode Bridge" : "British VCA Punch");
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start + 40; gfx_printf("Threshold / Ratio : %.1f dB | %s", slider12, slider13 == 0 ? "1.5:1" : (slider13 == 1 ? "2:1" : (slider13 == 2 ? "4:1" : "8:1")));
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start + 58; gfx_printf("Attack / Release  : %.1fms | %s", slider14, slider15 == 0 ? "100ms" : (slider15 == 1 ? "300ms" : (slider15 == 2 ? "600ms" : "Auto")));
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start + 76; gfx_printf("Detector HPF Key  : %d Hz Sidechain", slider16);
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start + 94; gfx_printf("Instantaneous GR  : -%.2f dB Peak Hold", glue_gr_db);

  // Column 3: Saturation & Spatial Anchor
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start; gfx_drawstr("3. HARMONIC & SPATIAL CORE");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.95;
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start + 22; gfx_printf("Harmonic Engine   : %s", slider23 == 0 ? "Transparent Pure" : (slider23 == 1 ? "Neve 8014 Iron Desk" : (slider23 == 2 ? "Studer A800 Tape" : "Triode Tube")));
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start + 40; gfx_printf("Console Desk Drive: +%.1f dB THD", slider24);
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start + 58; gfx_printf("Sub Mono Anchor   : %d Hz (LR 24dB/oct)", slider6);
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start + 76; gfx_printf("Quad Imager Width : %.2f x Multiplier", slider25);
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start + 94; gfx_printf("Vocal Pocket Carve: -%.1f dB @ 2.2 kHz", pocket_depth);
);

// =============================================================================
// TAB 1: TONAL FORGE EQ (5-BAND CURVE PLOT + 5 FULL-HEIGHT CHANNEL STRIPS)
// =============================================================================
slider1 == 1 ? (
  eq_plot_y = ws_y + 12; eq_plot_h = 230; eq_plot_w = ws_w - 24;
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(ws_x + 12, eq_plot_y, eq_plot_w, eq_plot_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 12, eq_plot_y, eq_plot_w, eq_plot_h, 0);

  gfx_setfont(2, "Orbitron", 11.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 24; gfx_y = eq_plot_y + 10; gfx_drawstr("TONAL FORGE 5-BAND SUMMING EQ RESPONSE CURVE");

  // Grid lines
  cy0 = eq_plot_y + eq_plot_h * 0.5;
  gfx_r = 0.10; gfx_g = 0.15; gfx_b = 0.22;
  gfx_line(ws_x + 12, cy0, ws_x + 12 + eq_plot_w, cy0);
  gfx_line(ws_x + 12, cy0 - 45, ws_x + 12 + eq_plot_w, cy0 - 45); // +6dB
  gfx_line(ws_x + 12, cy0 + 45, ws_x + 12 + eq_plot_w, cy0 + 45); // -6dB

  // Freq grid lines (100Hz, 1kHz, 10kHz)
  fx100 = ws_x + 12 + floor(eq_plot_w * 0.23);
  fx1k  = ws_x + 12 + floor(eq_plot_w * 0.56);
  fx10k = ws_x + 12 + floor(eq_plot_w * 0.88);
  gfx_line(fx100, eq_plot_y, fx100, eq_plot_y + eq_plot_h);
  gfx_line(fx1k,  eq_plot_y, fx1k,  eq_plot_y + eq_plot_h);
  gfx_line(fx10k, eq_plot_y, fx10k, eq_plot_y + eq_plot_h);

  gfx_setfont(3, "Consolas", 9.5); gfx_r = 0.50; gfx_g = 0.60; gfx_b = 0.70;
  gfx_x = fx100 + 4; gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("100Hz");
  gfx_x = fx1k + 4;  gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("1kHz");
  gfx_x = fx10k + 4; gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("10kHz");

  // Draw EQ Curve Across 120 points
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  prev_py = cy0;
  pi = 0;
  loop(120,
    px = ws_x + 12 + floor((pi / 119.0) * eq_plot_w);
    f_val = 20.0 * exp(log(1000.0) * (pi / 119.0));
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

  // 5 Full-Height Channel Strips with zero empty gaps!
  col_w = floor((ws_w - 24 - 32) / 5);
  cards_y = eq_plot_y + eq_plot_h + 12; cards_h = ws_h - eq_plot_h - 28;
  draw_channel_strip(ws_x + 12 + 0 * (col_w + 8), cards_y, col_w, cards_h, "28Hz HPF", "SUB CUT 18dB", slider18, 20, 60, "%d Hz", 18, 0.85, 0.47, 0.21);
  draw_channel_strip(ws_x + 12 + 1 * (col_w + 8), cards_y, col_w, cards_h, "80Hz PUNCH", "KICK/BASS BODY", slider19, -6.0, 6.0, "%+.1f dB", 19, 0.00, 0.85, 1.00);
  draw_channel_strip(ws_x + 12 + 2 * (col_w + 8), cards_y, col_w, cards_h, "280Hz SCOOP", "MUD CLARITY", slider20, -6.0, 6.0, "%+.1f dB", 20, 0.85, 0.47, 0.21);
  draw_channel_strip(ws_x + 12 + 3 * (col_w + 8), cards_y, col_w, cards_h, "3.5kHz BITE", "PICK ATTACK", slider21, -6.0, 6.0, "%+.1f dB", 21, 0.00, 0.85, 1.00);
  draw_channel_strip(ws_x + 12 + 4 * (col_w + 8), cards_y, col_w, cards_h, "10kHz SHEEN", "AIR GLOSS", slider22, -6.0, 6.0, "%+.1f dB", 22, 1.00, 0.85, 0.35);
);

// =============================================================================
// TAB 2: BUS GLUE COMPRESSOR (TRANSFER PLOT + DUAL TOPOLOGY + DENSE CONTROLS)
// =============================================================================
slider1 == 2 ? (
  cg_y = ws_y + 12; cg_w = ws_w - 24; cg_h = ws_h - 24;
  left_w = floor((cg_w - 24) * 0.45);
  right_w = cg_w - left_w - 16;

  // Left Box: Dynamic Compression Transfer Function Plot
  gfx_r = 0.012; gfx_g = 0.018; gfx_b = 0.026; gfx_rect(ws_x + 12, cg_y, left_w, cg_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 12, cg_y, left_w, cg_h, 0);

  gfx_setfont(2, "Orbitron", 11.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 24; gfx_y = cg_y + 12; gfx_drawstr("COMPRESSION TRANSFER FUNCTION");

  // Plot grid (-40dB to 0dB)
  p_x0 = ws_x + 40; p_y0 = cg_y + 45; p_size = min(left_w - 60, cg_h - 180);
  gfx_r = 0.008; gfx_g = 0.012; gfx_b = 0.018; gfx_rect(p_x0, p_y0, p_size, p_size);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(p_x0, p_y0, p_size, p_size, 0);

  // 1:1 Unity Line (Gray dashed)
  gfx_r = 0.30; gfx_g = 0.40; gfx_b = 0.50;
  gfx_line(p_x0, p_y0 + p_size, p_x0 + p_size, p_y0);

  // Compression Slope Curve
  r_val = slider13 == 0 ? 1.5 : (slider13 == 1 ? 2.0 : (slider13 == 2 ? 4.0 : 8.0));
  th_frac = (slider12 + 40.0) / 40.0;
  th_px = p_x0 + floor(th_frac * p_size);
  th_py = p_y0 + p_size - floor(th_frac * p_size);

  gfx_r = 0.00; gfx_g = 0.95; gfx_b = 1.00;
  gfx_line(p_x0, p_y0 + p_size, th_px, th_py);
  // Above threshold
  end_py = th_py - floor(((p_size - (th_px - p_x0)) / r_val));
  gfx_line(th_px, th_py, p_x0 + p_size, end_py);

  // Threshold Marker
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_circle(th_px, th_py, 4, 1);

  // Live Bouncing Operating Point (Displays current GR in real time)
  live_in_db = max(-40.0, min(0.0, inst_rms));
  live_frac = (live_in_db + 40.0) / 40.0;
  live_x = p_x0 + floor(live_frac * p_size);
  live_y = live_in_db < slider12 ? (p_y0 + p_size - floor(live_frac * p_size)) : (th_py - floor(((live_x - th_px) / r_val)));
  gfx_r = 1.00; gfx_g = 0.25; gfx_b = 0.35;
  gfx_circle(live_x, live_y, 6, 1);
  gfx_r = 1.00; gfx_g = 1.00; gfx_b = 1.00;
  gfx_circle(live_x, live_y, 2, 1);

  // Detector Filter Response Bar
  sc_box_y = p_y0 + p_size + 20;
  gfx_setfont(3, "Consolas", 10.5, 'b'); gfx_r = 0.70; gfx_g = 0.80; gfx_b = 0.90;
  gfx_x = p_x0; gfx_y = sc_box_y;
  gfx_printf("Sidechain Detector HPF: %d Hz (Steep 12dB/oct)", slider16);
  gfx_x = p_x0; gfx_y = sc_box_y + 20;
  gfx_printf("Detector Peak: %.1f dB | Live GR: -%.2f dB", inst_peak > 0 ? 20.0*log10(inst_peak) : -120.0, glue_gr_db);

  // Right Box: Dual Topology & Parameter Controls
  rx = ws_x + 12 + left_w + 16;
  gfx_r = 0.012; gfx_g = 0.018; gfx_b = 0.026; gfx_rect(rx, cg_y, right_w, cg_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(rx, cg_y, right_w, cg_h, 0);

  // Dual-Topology Selector Buttons (VCA vs Diode Bridge)
  btn_top_w = floor((right_w - 40) * 0.5);
  t1_x = rx + 16; t1_y = cg_y + 16;
  t1_hov = (mouse_x >= t1_x && mouse_x <= t1_x + btn_top_w && mouse_y >= t1_y && mouse_y <= t1_y + 36);
  gfx_r = (slider11 == 0) ? 0.06 : 0.03; gfx_g = (slider11 == 0) ? 0.22 : 0.05; gfx_b = (slider11 == 0) ? 0.28 : 0.08;
  gfx_rect(t1_x, t1_y, btn_top_w, 36);
  gfx_r = (slider11 == 0) ? 0.00 : 0.35; gfx_g = (slider11 == 0) ? 0.95 : 0.45; gfx_b = (slider11 == 0) ? 1.00 : 0.55;
  gfx_rect(t1_x, t1_y, btn_top_w, 36, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_x = t1_x + 14; gfx_y = t1_y + 10; gfx_drawstr("BRITISH VCA PUNCH");
  mouse_clicked && t1_hov ? (slider11 = 0; slider_automate(););

  t2_x = t1_x + btn_top_w + 8; t2_y = cg_y + 16;
  t2_hov = (mouse_x >= t2_x && mouse_x <= t2_x + btn_top_w && mouse_y >= t2_y && mouse_y <= t2_y + 36);
  gfx_r = (slider11 == 1) ? 0.22 : 0.03; gfx_g = (slider11 == 1) ? 0.12 : 0.05; gfx_b = (slider11 == 1) ? 0.06 : 0.08;
  gfx_rect(t2_x, t2_y, btn_top_w, 36);
  gfx_r = (slider11 == 1) ? 0.85 : 0.35; gfx_g = (slider11 == 1) ? 0.47 : 0.45; gfx_b = (slider11 == 1) ? 0.21 : 0.55;
  gfx_rect(t2_x, t2_y, btn_top_w, 36, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_x = t2_x + 14; gfx_y = t2_y + 10; gfx_drawstr("NEVE DIODE BRIDGE");
  mouse_clicked && t2_hov ? (slider11 = 1; slider_automate(););

  // Big Gain Reduction Meter Bar
  gr_bar_y = t1_y + 48; gr_bar_h = 32; gr_bar_w = right_w - 32;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(rx + 16, gr_bar_y, gr_bar_w, gr_bar_h);
  gfx_r = 0.20; gfx_g = 0.30; gfx_b = 0.42; gfx_rect(rx + 16, gr_bar_y, gr_bar_w, gr_bar_h, 0);
  fill_w = floor(gr_bar_w * (min(16.0, glue_gr_db) / 16.0));
  fill_w > 0 ? (
    gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(rx + 16, gr_bar_y + 2, fill_w, gr_bar_h - 4);
  );
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = rx + 28; gfx_y = gr_bar_y + 8;
  gfx_printf("LIVE GAIN REDUCTION: -%.2f dB", glue_gr_db);

  // 6 Sliders arranged in 2 rows of 3 with full ergonomics
  c_sl_w = floor((right_w - 48) / 3); c_sl_h = 65;
  sl_r1_y = gr_bar_y + 48;
  draw_param_slider(rx + 16 + 0 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "THRESHOLD", slider12, -36.0, 0.0, "%.1f dB", 12, 0.85, 0.47, 0.21);
  draw_param_slider(rx + 16 + 1 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "RATIO", slider13, 0, 3, "Mode %d", 13, 0.00, 0.85, 1.00);
  draw_param_slider(rx + 16 + 2 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "ATTACK", slider14, 0.1, 100.0, "%.1f ms", 14, 0.85, 0.47, 0.21);

  sl_r2_y = sl_r1_y + c_sl_h + 12;
  draw_param_slider(rx + 16 + 0 * (c_sl_w + 8), sl_r2_y, c_sl_w, c_sl_h, "RELEASE", slider15, 0, 4, "Mode %d", 15, 0.00, 0.85, 1.00);
  draw_param_slider(rx + 16 + 1 * (c_sl_w + 8), sl_r2_y, c_sl_w, c_sl_h, "SC HPF KEY", slider16, 30, 250, "%d Hz", 16, 0.85, 0.47, 0.21);
  draw_param_slider(rx + 16 + 2 * (c_sl_w + 8), sl_r2_y, c_sl_w, c_sl_h, "DRY/WET MIX", slider17, 0, 100, "%d %%", 17, 1.00, 0.85, 0.35);

  // Bottom Ballistics Forensic Notes Box
  fn_y = sl_r2_y + c_sl_h + 16; fn_h = cg_h - (fn_y - cg_y) - 16;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(rx + 16, fn_y, right_w - 32, fn_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(rx + 16, fn_y, right_w - 32, fn_h, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = rx + 28; gfx_y = fn_y + 12; gfx_drawstr("GLUE BALLISTICS SPECIFICATION:");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = rx + 28; gfx_y = fn_y + 34;
  gfx_drawstr("• British VCA Punch: Emulates the legendary Oxford 4000 G-Bus console VCA detector. Transparent snap with zero bass mud.");
  gfx_x = rx + 28; gfx_y = fn_y + 54;
  gfx_drawstr("• Neve Diode Bridge: Emulates discrete 33609 diode cell ballistics. Thicker harmonic density and non-linear release glue.");
  gfx_x = rx + 28; gfx_y = fn_y + 74;
  gfx_drawstr("• Detector Sidechain: High-pass filtered up to 250Hz so heavy 808s and kick drums never pump or over-compress the master.");
);

// =============================================================================
// TAB 3: HARMONIC CRUCIBLE (4 MODE MODULES + TRANSFER CURVE + SPECTRUM BARS)
// =============================================================================
slider1 == 3 ? (
  sat_y = ws_y + 12; sat_w = ws_w - 24; sat_h = ws_h - 24;
  gfx_r = 0.014; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, sat_y, sat_w, sat_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 12, sat_y, sat_w, sat_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 28; gfx_y = sat_y + 14; gfx_drawstr("HARMONIC CRUCIBLE // CONSOLE DESK, TAPE & TUBE DRIVE");

  // 4 Saturation Mode Cards
  c_w = floor((sat_w - 48) / 4);
  mi = 0;
  loop(4,
    cx = ws_x + 24 + mi * (c_w + 8); cy = sat_y + 44; ch = 90;
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
    gfx_x = cx + 12; gfx_y = cy + 12; gfx_drawstr(m_title);

    m_desc = mi == 0 ? "0 THD Pure Pass" : (mi == 1 ? "Class A Iron Harmonics" : (mi == 2 ? "15 IPS Warm Compression" : "Even Tube Bloom"));
    gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.85;
    gfx_x = cx + 12; gfx_y = cy + 36; gfx_drawstr(m_desc);

    mouse_clicked && m_hov ? (slider23 = mi; update_filters(); slider_automate(););
    mi += 1;
  );

  // Middle Section: Left = Soft-Clipping Saturation Curve; Right = Harmonic Spectrum Visualizer
  mid_y = sat_y + 146; mid_h = 190;
  m_left_w = floor((sat_w - 48) * 0.45);
  m_right_w = sat_w - 48 - m_left_w - 12;

  // Left Saturation Transfer Plot
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, mid_y, m_left_w, mid_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(ws_x + 24, mid_y, m_left_w, mid_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 36; gfx_y = mid_y + 10; gfx_drawstr("SATURATION KNEE & COMPRESSION CURVE");

  p_cx0 = ws_x + 36; p_cy0 = mid_y + 35; p_cw = m_left_w - 24; p_ch = mid_h - 48;
  gfx_r = 0.06; gfx_g = 0.09; gfx_b = 0.13; gfx_line(p_cx0, p_cy0 + p_ch * 0.5, p_cx0 + p_cw, p_cy0 + p_ch * 0.5);
  gfx_line(p_cx0 + p_cw * 0.5, p_cy0, p_cx0 + p_cw * 0.5, p_cy0 + p_ch);

  // Draw non-linear saturation curve
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  prev_y = p_cy0 + p_ch * 0.5;
  pi = 0;
  loop(60,
    px = p_cx0 + floor((pi / 59.0) * p_cw);
    in_val = (pi / 29.5) - 1.0;
    out_val = slider23 == 0 ? in_val : fast_shape(in_val * (1.0 + slider24 * 0.2));
    cur_y = p_cy0 + p_ch * 0.5 - out_val * (p_ch * 0.45);
    pi > 0 ? gfx_line(prev_x, prev_y, px, cur_y);
    prev_x = px; prev_y = cur_y;
    pi += 1;
  );

  // Right Harmonic Spectrum Visualizer (Fundamental, 2nd, 3rd, 4th, 5th harmonics)
  rx = ws_x + 24 + m_left_w + 12;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(rx, mid_y, m_right_w, mid_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(rx, mid_y, m_right_w, mid_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = rx + 16; gfx_y = mid_y + 10; gfx_drawstr("HARMONIC SPECTRUM & THD DISTRIBUTION");

  // 5 Harmonic Bars
  h_bar_w = floor((m_right_w - 60) / 5);
  hi = 0;
  loop(5,
    hx = rx + 20 + hi * (h_bar_w + 8);
    // Calculated height based on drive and mode
    h_level = (hi == 0) ? 0.90 : (
      slider23 == 0 ? 0.0 : (
        slider23 == 1 ? (hi == 1 ? 0.45 : (hi == 2 ? 0.30 : 0.10)) * (slider24 / 12.0) :
        slider23 == 2 ? (hi == 1 ? 0.20 : (hi == 2 ? 0.50 : 0.15)) * (slider24 / 12.0) :
                        (hi == 1 ? 0.60 : (hi == 2 ? 0.15 : 0.25)) * (slider24 / 12.0)
      )
    );
    b_h = floor(h_level * (mid_h - 70));
    by = mid_y + mid_h - 24 - b_h;
    gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
    gfx_rect(hx, by, h_bar_w, b_h);
    gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;
    gfx_rect(hx, by, h_bar_w, b_h, 0);

    gfx_setfont(3, "Consolas", 10.0, 'b'); gfx_r = 0.70; gfx_g = 0.80; gfx_b = 0.90;
    h_lbl = hi == 0 ? "1st" : (hi == 1 ? "2nd" : (hi == 2 ? "3rd" : (hi == 3 ? "4th" : "5th")));
    gfx_x = hx + floor(h_bar_w * 0.5) - 8; gfx_y = mid_y + mid_h - 18;
    gfx_drawstr(h_lbl);
    hi += 1;
  );

  // Bottom Section: Drive Slider + Detailed Advice
  draw_param_slider(ws_x + 24, sat_y + 348, sat_w - 48, 65, "HARMONIC CRUCIBLE CONSOLE DRIVE", slider24, 0.0, 12.0, "+%.1f dB", 24, 0.85, 0.47, 0.21);

  adv_y = sat_y + 424; adv_h = sat_h - 438;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, adv_y, sat_w - 48, adv_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(ws_x + 24, adv_y, sat_w - 48, adv_h, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 36; gfx_y = adv_y + 12; gfx_drawstr("HARMONIC THD GENERATION & SATURATION PROFILES:");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = ws_x + 36; gfx_y = adv_y + 32;
  gfx_drawstr("• Neve 8014 Desk: Drives discrete transformer iron, adding 2nd and 3rd harmonics to give heavy rhythm guitars weight.");
  gfx_x = ws_x + 36; gfx_y = adv_y + 50;
  gfx_drawstr("• Studer A800 15 IPS Tape: Smooth tape saturation rounds aggressive cymbal spikiness while gluing kick and snare.");
  gfx_x = ws_x + 36; gfx_y = adv_y + 68;
  gfx_drawstr("• Triode Tube Crucible: Enriches even-order harmonics, lending warm analog body to modern clean synth beds.");
);

// =============================================================================
// TAB 4: STEREO DIMENSION & SUB-ANCHOR (CROSSOVER PLOT + VECTOR SCOPE + CONTROLS)
// =============================================================================
slider1 == 4 ? (
  st_y = ws_y + 12; st_w = ws_w - 24; st_h = ws_h - 24;
  gfx_r = 0.014; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, st_y, st_w, st_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 12, st_y, st_w, st_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 28; gfx_y = st_y + 14; gfx_drawstr("STEREO DIMENSION WIDTH & SUB-BASS MONO ANCHOR");

  // Top Section: Left = Linkwitz-Riley Sub Mono Crossover Plot; Right = Stereo Balance Scope
  top_h = 220;
  left_w = floor((st_w - 48) * 0.5);
  right_w = st_w - 48 - left_w - 12;

  // Crossover Plot
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, st_y + 44, left_w, top_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(ws_x + 24, st_y + 44, left_w, top_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 36; gfx_y = st_y + 54; gfx_drawstr("SUB-BASS MONO COLLAPSE (< 160Hz)");

  // Crossover curve visualizer
  cx_plot_x = ws_x + 36; cx_plot_y = st_y + 75; cx_plot_w = left_w - 24; cx_plot_h = top_h - 40;
  cut_x = cx_plot_x + floor(((slider6 - 40.0) / 120.0) * cx_plot_w);
  // Shaded Mono Sub Region
  gfx_r = 0.18; gfx_g = 0.09; gfx_b = 0.05;
  gfx_rect(cx_plot_x, cx_plot_y, cut_x - cx_plot_x, cx_plot_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_line(cut_x, cx_plot_y, cut_x, cx_plot_y + cx_plot_h);

  gfx_setfont(3, "Consolas", 10.5, 'b'); gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;
  gfx_x = cx_plot_x + 10; gfx_y = cx_plot_y + 20; gfx_printf("100%% MONO ANCHOR: < %d Hz", slider6);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = cut_x + 10; gfx_y = cx_plot_y + 20; gfx_printf("STEREO SPREAD: %.2f x", slider25);

  // Right Box: Phase Vector Radar
  rx = ws_x + 24 + left_w + 12;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(rx, st_y + 44, right_w, top_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(rx, st_y + 44, right_w, top_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = rx + 16; gfx_y = st_y + 54; gfx_drawstr("STEREO PHASE RADAR & CORRELATION");

  r_cx = rx + floor(right_w * 0.5); r_cy = st_y + 44 + floor(top_h * 0.55);
  gfx_r = 0.08; gfx_g = 0.14; gfx_b = 0.22;
  gfx_circle(r_cx, r_cy, 55, 0);
  gfx_circle(r_cx, r_cy, 28, 0);
  gfx_line(r_cx - 55, r_cy, r_cx + 55, r_cy);
  gfx_line(r_cx, r_cy - 55, r_cx, r_cy + 55);

  // Bottom Section: Sliders + Sentry Button
  draw_param_slider(ws_x + 24, st_y + 276, st_w - 48, 65, "SUB-BASS MONO-ANCHOR CUTOFF", slider6, 40, 160, "%d Hz", 6, 0.85, 0.47, 0.21);
  draw_param_slider(ws_x + 24, st_y + 350, st_w - 48, 65, "QUAD-WALL STEREO DIMENSION WIDTH", slider25, 0.80, 1.40, "%.2f x", 25, 0.00, 0.85, 1.00);

  // Dynamic Kick/Bass Sentry Button
  snt_x = ws_x + 24; snt_y = st_y + 424; snt_w = 280; snt_h = 32;
  snt_hov = (mouse_x >= snt_x && mouse_x <= snt_x + snt_w && mouse_y >= snt_y && mouse_y <= snt_y + snt_h);
  gfx_r = slider7 ? 0.06 : 0.16; gfx_g = slider7 ? 0.20 : 0.08; gfx_b = slider7 ? 0.14 : 0.08;
  gfx_rect(snt_x, snt_y, snt_w, snt_h);
  gfx_r = slider7 ? 0.00 : 0.80; gfx_g = slider7 ? 0.95 : 0.40; gfx_b = slider7 ? 0.65 : 0.40;
  gfx_rect(snt_x, snt_y, snt_w, snt_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_x = snt_x + 14; gfx_y = snt_y + 9;
  slider7 ? gfx_drawstr("KICK/BASS SENTRY: ACTIVE") : gfx_drawstr("KICK/BASS SENTRY: BYPASS");
  mouse_clicked && snt_hov ? (slider7 = !slider7; slider_automate(););

  // Technical explanation plaque
  t_pl_y = st_y + 466; t_pl_h = st_h - 480;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, t_pl_y, st_w - 48, t_pl_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(ws_x + 24, t_pl_y, st_w - 48, t_pl_h, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 36; gfx_y = t_pl_y + 12; gfx_drawstr("SUB-BASS INTEGRITY & PHASE COHERENCE:");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = ws_x + 36; gfx_y = t_pl_y + 32;
  gfx_drawstr("• Sub-Bass Mono Anchor: Collapses all frequencies below cutoff to 100% pure mono, eliminating sub-frequency phase cancellation.");
  gfx_x = ws_x + 36; gfx_y = t_pl_y + 50;
  gfx_drawstr("• Kick/Bass Sentry: Automatically applies micro-dips under 100Hz on heavy kick hits so bass guitar and kick drum never clash.");
);

// =============================================================================
// TAB 5: VOCAL POCKET CORRIDOR (DYNAMIC NOTCH + LIVE gmem TELEMETRY)
// =============================================================================
slider1 == 5 ? (
  pk_y = ws_y + 12; pk_w = ws_w - 24; pk_h = ws_h - 24;
  gfx_r = 0.014; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, pk_y, pk_w, pk_h);
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_rect(ws_x + 12, pk_y, pk_w, pk_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 28; gfx_y = pk_y + 14; gfx_drawstr("DYNAMIC VOCAL POCKET CORRIDOR // ZERO-CABLE gmem SENSING");

  // Top Section: Live Spectral Notch Display
  top_h = 220;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, pk_y + 44, pk_w - 48, top_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(ws_x + 24, pk_y + 44, pk_w - 48, top_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 36; gfx_y = pk_y + 54; gfx_drawstr("CENTER-CHANNEL NOTCH RESPONSE (2.2 kHz VOCAL CORRIDOR)");

  p_cx0 = ws_x + 36; p_cy0 = pk_y + 85; p_cw = pk_w - 72; p_ch = top_h - 55;
  gfx_r = 0.08; gfx_g = 0.12; gfx_b = 0.18;
  gfx_line(p_cx0, p_cy0 + p_ch * 0.5, p_cx0 + p_cw, p_cy0 + p_ch * 0.5);

  // Plot dynamic notch curve
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  prev_y = p_cy0 + p_ch * 0.5;
  pi = 0;
  loop(100,
    px = p_cx0 + floor((pi / 99.0) * p_cw);
    f_val = 20.0 * exp(log(1000.0) * (pi / 99.0));
    // Bell notch around 2200 Hz
    notch_gain = -pocket_depth * exp(-0.5 * sqr((log(f_val / 2200.0) / 0.35)));
    cur_y = p_cy0 + p_ch * 0.5 - notch_gain * 12.0;
    pi > 0 ? gfx_line(prev_x, prev_y, px, cur_y);
    prev_x = px; prev_y = cur_y;
    pi += 1;
  );

  // Frequency marker at 2.2kHz
  fx22 = p_cx0 + floor(0.68 * p_cw);
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_line(fx22, p_cy0, fx22, p_cy0 + p_ch);
  gfx_setfont(3, "Consolas", 10.0, 'b');
  gfx_x = fx22 + 6; gfx_y = p_cy0 + 10; gfx_drawstr("2.2 kHz Vocal Core");

  // Middle Section: Depth Slider & Auto-Sensing Mode Switch
  draw_param_slider(ws_x + 24, pk_y + 276, pk_w - 48, 65, "VOCAL POCKET CORRIDOR DEPTH", slider8, 0.0, 3.0, "-%.1f dB", 8, 0.85, 0.47, 0.21);

  pkm_x = ws_x + 24; pkm_y = pk_y + 350; pkm_w = 320; pkm_h = 32;
  pkm_hov = (mouse_x >= pkm_x && mouse_x <= pkm_x + pkm_w && mouse_y >= pkm_y && mouse_y <= pkm_y + pkm_h);
  gfx_r = slider9 ? 0.06 : 0.16; gfx_g = slider9 ? 0.20 : 0.08; gfx_b = slider9 ? 0.14 : 0.08;
  gfx_rect(pkm_x, pkm_y, pkm_w, pkm_h);
  gfx_r = slider9 ? 0.00 : 0.80; gfx_g = slider9 ? 0.95 : 0.40; gfx_b = slider9 ? 0.65 : 0.40;
  gfx_rect(pkm_x, pkm_y, pkm_w, pkm_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_x = pkm_x + 14; gfx_y = pkm_y + 9;
  slider9 ? gfx_drawstr("MODE: gmem AUTO-SENSING") : gfx_drawstr("MODE: MANUAL DEPTH LOCK");
  mouse_clicked && pkm_hov ? (slider9 = !slider9; slider_automate(););

  // Bottom Live Telemetry Log Box
  pk_box_y = pk_y + 392; pk_box_h = pk_h - 406;
  gfx_r = 0.010; gfx_g = 0.015; gfx_b = 0.022; gfx_rect(ws_x + 24, pk_box_y, pk_w - 48, pk_box_h);
  gfx_r = 0.15; gfx_g = 0.25; gfx_b = 0.35; gfx_rect(ws_x + 24, pk_box_y, pk_w - 48, pk_box_h, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21;
  gfx_x = ws_x + 36; gfx_y = pk_box_y + 12;
  gfx_printf("LIVE CORRIDOR TELEMETRY: Active Pocket Notch = -%.2f dB @ 2.2 kHz", pocket_depth);

  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = ws_x + 36; gfx_y = pk_box_y + 34;
  gfx_printf("Incoming Vocal Energy (gmem[1452]): %.1f dB | Interlock Status: %s", vb_vocal_rms, vb_alive ? "SYNCHRONIZED (ONLINE)" : "STANDBY (OFFLINE)");
  gfx_x = ws_x + 36; gfx_y = pk_box_y + 54;
  gfx_drawstr("The corridor dynamically notches the center channel of guitars and synths around 2.2kHz whenever the vocal sings,");
  gfx_x = ws_x + 36; gfx_y = pk_box_y + 72;
  gfx_drawstr("allowing the vocal sovereign to sit effortlessly upfront in the mix without fighting the rhythm wall.");
);

// =============================================================================
// TAB 6: PRODUCER SUMMING MATRIX (25 CLICKABLE TILES + FORENSIC PLAQUE)
// =============================================================================
slider1 == 6 ? (
  mat_y = ws_y + 12;
  gfx_r = 0.85; gfx_g = 0.47; gfx_b = 0.21; gfx_setfont(1, "Orbitron", 13.5, 'b');
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

    gfx_setfont(3, "Consolas", 10.5, 'b');
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

  gfx_setfont(3, "Consolas", 11.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = ws_x + 32; gfx_y = pl_y + 40;
  gfx_printf("CALIBRATION: Trim %+.1fdB | Glue Thresh %.1fdB (Ratio %s) | Mud Scoop %+.1fdB | Drive %+.1fdB | Width %.2fx",
    slider4, slider12, slider13 == 0 ? "1.5:1" : (slider13 == 1 ? "2:1" : (slider13 == 2 ? "4:1" : "8:1")), slider20, slider24, slider25);

  gfx_setfont(3, "Consolas", 11.0); gfx_r = 0.70; gfx_g = 0.80; gfx_b = 0.90;
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

print(f"Generated Instrumental Suite Code: {len(INST_SUITE_CODE)} bytes")

# Write to file
inst_target = r"c:\Dev\DameiSuite\effects\Damei_InstrumentalSuite.jsfx"
with open(inst_target, "w", encoding="utf-8") as f:
    f.write(INST_SUITE_CODE)
print(f"Successfully wrote {inst_target}")
