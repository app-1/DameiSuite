"""
Master generator for Damei Vocal Empress (Master Vocal Sum Suite).
Implements complete Luxury Console Surface Architecture (@gfx 1080 700),
all 7 tabs with zero empty gaps, responsive 3-zone header bar with center preset stepper,
and full 25-producer benchmark matrix.
"""

import os

VOCAL_BUS_CODE = r'''desc:Damei Vocal Empress (Imperial Sceptre & Master Vocal Sum)
// =============================================================================
// DAMEI SUITE // 2026 REAPER MASTER SUMMING INFRASTRUCTURE
// ARCHETYPE: DUAFE (The Wooden Comb - Pristine Grooming, Refinement & Royalty)
// LUXURY CONSOLE SURFACE ARCHITECTURE (@gfx 1080 700)
// =============================================================================

slider1:0<0,6,1{0: OVERVIEW, 1: BAXANDALL, 2: VOCAL GLUE, 3: DE-ESSER, 4: SPATIAL, 5: PRESENCE, 6: PRODUCER}>-Active Navigation Tab
slider2:0<0,24,1{00: Default Unity Baseline (1:1 Pass), 01: Lance Prenc (Alpha Wolf / Polaris), 02: Scott Seigel (DIESECT), 03: Jonathan Dolese (Mirrorcell), 04: Buster Odeholm (thrown / Northlane), 05: Lewis Johns (Love Is Noise / blanket), 06: Kel Pinchin (Split Chain Target), 07: Dan Lancaster & Jason Perry (Don Broco), 08: Erik Bickerstaffe (Static Dress), 09: Sam Guaiana (Silverstein / TDWP), 10: Zach Tuch (Heavenward / Hundredth), 11: Forrester Savell (Karnivool), 12: Leon Schmidt (SUNBORN - Nebula), 13: Ermin Hamidovic (Systematic Reference), 14: Will Putney (Fit For An Autopsy), 15: George Lever (Sleep Token / Loathe), 16: Sam Bassal (Thornhill - nerv), 17: Henrik Udd (Architects - Gravity), 18: Dan Braunstein (Spiritbox), 19: Zakk Cervini & Erik Ron (Bad Omens), 20: Jens Bogren (Fascination Street), 21: Adam Nolly Getgood (Periphery / GGD), 22: Acle Kahney (TesseracT - King), 23: Adam Cichocki (heaving. / Timber), 24: Manuel Renner (SENNA / Uberlarm)}>-Producer Benchmark Matrix
slider3:0<-6.0,6.0,0.1>-Input Calibration Gain (dB)
slider4:0<-6.0,6.0,0.1>-Producer Headroom Trim (dB)
slider5:1<0,1,1{Free Output, -6.0 dBTP Strict Pre-Master Lock}>-Headroom Guardian Mode
slider6:-18.0<-36.0,0.0,0.5>-Master De-Esser Threshold (dB)
slider7:6800<4000,10000,50>-Master De-Esser Frequency (Hz)
slider8:-6.0<-12.0,0.0,0.5>-Master De-Esser Max Range (dB)
slider9:0<0,1,1{Normal Audio, Audition Clamped Sibilance}>-De-Esser Delta Audition
slider10:0.0<-6.0,6.0,0.1>-Baxandall 100Hz Warmth (dB)
slider11:0.0<-6.0,6.0,0.1>-Baxandall 3.5kHz Presence (dB)
slider12:0.0<-6.0,6.0,0.1>-Baxandall 12kHz Silk Air (dB)
slider13:1<0,1,1{Bypass, Engaged}>-Master Vocal Bus Glue Compressor
slider14:0<0,1,1{Fairchild 670 Smooth Tube, Vintage Opto Leveler}>-Glue Topology
slider15:0.0<-36.0,0.0,0.5>-Vocal Glue Threshold (dB)
slider16:1<0,3,1{1.5:1 Smooth Vocal, 2:1 Master Sum, 3:1 Cohesion, 4:1 Radio Glue}>-Vocal Glue Ratio
slider17:15.0<0.2,50.0,0.5>-Vocal Glue Attack (ms)
slider18:2<0,4,1{100ms Fast, 300ms Vocal Natural, 600ms Silk Opto, 1200ms Lush, Auto Ballistics}>-Vocal Glue Release
slider19:100<0,100,1>-Vocal Glue Dry/Wet Mix (%)
slider20:0.0<0.0,10.0,0.1>-Vocal Tube Warmth Saturation (dB)
slider21:1.00<0.80,1.40,0.01>-Vocal Spatial Width (Lead Center Lock)
slider22:1<0,1,1{Bypass 1:1 Unity, Engaged Active Processing}>-Master Suite Processing State
slider23:0<0,1,1{Normal Audio, Delta Solo Audition}>-Delta Solo Audition
slider24:0<0,1,1{Snapshot A, Snapshot B}>-A/B Comparison Snapshot
slider25:0<0,1,1{Master Vocal Sum, Stem Vocal Sum}>-Vocal Summing Architecture Mode
slider26:1.5<0.0,3.0,0.1>-Presence Sentry Sensitivity (dB)
slider27:1<0,1,1{Standby, Active Autonomous Carve Request}>-Dynamic Corridor Pocket Request

in_pin:Vocal Sum In L
in_pin:Vocal Sum In R
out_pin:Master Vocal Sum L
out_pin:Master Vocal Sum R

options:gmem=DameiMixMetering
options:maxmem=65536

@init
ext_noinit = 1.0;
M_PI = 3.14159265358979323846;

// Memory partitioning
ab_mem_a = 2000;
ab_mem_b = 2050;

// Filter state memories
bax_w_x1 = 0; bax_w_x2 = 0; bax_w_y1 = 0; bax_w_y2 = 0;
bax_p_x1 = 0; bax_p_x2 = 0; bax_p_y1 = 0; bax_p_y2 = 0;
bax_a_x1 = 0; bax_a_x2 = 0; bax_a_y1 = 0; bax_a_y2 = 0;

// De-Esser biquad state
ds_hp_x1 = 0; ds_hp_x2 = 0; ds_hp_y1 = 0; ds_hp_y2 = 0;
ds_env = 0.0;
ds_reduction_db = 0.0;

// Glue compressor state
vocal_comp_env = 0.0;
vocal_glue_gr_db = 0.0;
sifam_tube_needle = 0.0;
sifam_vocal_glue_needle = 0.0;

// Live metering
vocal_peak = 0.0;
vocal_rms = 0.0;
vocal_phase_corr = 1.0;
v_acc_l = 0.0; v_acc_r = 0.0; v_cnt = 0;

// Shared memory telemetry registration (Vocal: 1450..1499)
gmem[1450] = 1; // Handshake heartbeat

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
  idx == 1  ? "Lance Prenc (Hyper-Upfront Aggressive Bite)" :
  idx == 2  ? "Scott Seigel (Saturated Tube Mid Presence)" :
  idx == 3  ? "Jonathan Dolese (Glossy Modern Pop-Metal Sheen)" :
  idx == 4  ? "Buster Odeholm (Crushed Industrial Vocal Clamp)" :
  idx == 5  ? "Lewis Johns (Ethereal Ambient Bloom & Silk Glue)" :
  idx == 6  ? "Kel Pinchin (Split Chain Target - Dynamic Vocal Lift)" :
  idx == 7  ? "Dan Lancaster & Jason Perry (Radio Rock High Gloss)" :
  idx == 8  ? "Erik Bickerstaffe (Saturated Analog Mic Drive)" :
  idx == 9  ? "Sam Guaiana (Upfront Post-Hardcore Urgency)" :
  idx == 10 ? "Zach Tuch (Lush Reverb Space & Warm Opto Leveler)" :
  idx == 11 ? "Forrester Savell (Organic Dynamic Transparency)" :
  idx == 12 ? "Leon Schmidt (Cyber Sheen & Crystalline Top-End)" :
  idx == 13 ? "Ermin Hamidovic (Flat Phase-Coherent Vocal Master)" :
  idx == 14 ? "Will Putney (Aggressive Screaming Vocal Control)" :
  idx == 15 ? "George Lever (Silky Dark Top-End & Deep Chest Warmth)" :
  idx == 16 ? "Sam Bassal (Modern Alternative Grungegaze Sheen)" :
  idx == 17 ? "Henrik Udd (Arena Wall Vocal Sheen & Pristine De-Ess)" :
  idx == 18 ? "Dan Braunstein (Spiritbox - Silky Modern Presence)" :
  idx == 19 ? "Zakk Cervini & Erik Ron (Radio Vocal Sheen & Focus)" :
  idx == 20 ? "Jens Bogren (Dense European Metal Vocal Glue)" :
  idx == 21 ? "Adam Nolly Getgood (Pristine Center Focus & Mud Cut)" :
  idx == 22 ? "Acle Kahney (TesseracT - King Dynamic Clarity)" :
  idx == 23 ? "Adam Cichocki (Saturated Wall-Of-Sound Vocal Halo)" :
              "Manuel Renner (SENNA - Out Of The Blue Laser Focus)";
);

function apply_producer_preset(idx) (
  idx == 0 ? ( // Unity Baseline (1:1 Transparent Pass)
    slider3 = 0.0; slider4 = 0.0; slider5 = 1; slider6 = -18.0; slider7 = 6800; slider8 = 0.0;
    slider10 = 0.0; slider11 = 0.0; slider12 = 0.0;
    slider13 = 1; slider14 = 0; slider15 = 0.0; slider16 = 1; slider17 = 15.0; slider18 = 2; slider19 = 100;
    slider20 = 0.0; slider21 = 1.00;
  ) : idx == 1 ? ( // Lance Prenc
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = -20.0; slider7 = 6500; slider8 = -6.5;
    slider10 = -1.0; slider11 = 2.5; slider12 = 3.2;
    slider13 = 1; slider14 = 0; slider15 = -8.0; slider16 = 2; slider17 = 10.0; slider18 = 1; slider19 = 100;
    slider20 = 3.5; slider21 = 1.05;
  ) : idx == 2 ? ( // Scott Seigel
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = -18.0; slider7 = 6800; slider8 = -5.0;
    slider10 = 1.5; slider11 = 2.0; slider12 = 1.5;
    slider13 = 1; slider14 = 0; slider15 = -6.5; slider16 = 2; slider17 = 15.0; slider18 = 4; slider19 = 100;
    slider20 = 3.0; slider21 = 1.00;
  ) : idx == 3 ? ( // Jonathan Dolese
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = -19.0; slider7 = 7200; slider8 = -6.0;
    slider10 = 1.0; slider11 = 1.8; slider12 = 3.5;
    slider13 = 1; slider14 = 1; slider15 = -6.0; slider16 = 1; slider17 = 20.0; slider18 = 2; slider19 = 100;
    slider20 = 2.5; slider21 = 1.10;
  ) : idx == 4 ? ( // Buster Odeholm
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = -22.0; slider7 = 6400; slider8 = -8.0;
    slider10 = -1.5; slider11 = 2.8; slider12 = 1.0;
    slider13 = 1; slider14 = 0; slider15 = -12.0; slider16 = 3; slider17 = 5.0; slider18 = 0; slider19 = 100;
    slider20 = 5.0; slider21 = 1.00;
  ) : idx == 5 ? ( // Lewis Johns
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = -16.0; slider7 = 7000; slider8 = -4.0;
    slider10 = 1.2; slider11 = 0.8; slider12 = 3.0;
    slider13 = 1; slider14 = 1; slider15 = -5.0; slider16 = 1; slider17 = 25.0; slider18 = 4; slider19 = 100;
    slider20 = 2.0; slider21 = 1.20;
  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target)
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = -19.0; slider7 = 6800; slider8 = -6.0;
    slider10 = 0.5; slider11 = 2.2; slider12 = 2.8;
    slider13 = 1; slider14 = 0; slider15 = -6.0; slider16 = 1; slider17 = 15.0; slider18 = 4; slider19 = 100;
    slider20 = 2.5; slider21 = 1.08;
  ) : idx == 7 ? ( // Dan Lancaster & Jason Perry
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = -20.0; slider7 = 6800; slider8 = -7.0;
    slider10 = 0.8; slider11 = 3.0; slider12 = 3.8;
    slider13 = 1; slider14 = 0; slider15 = -8.0; slider16 = 2; slider17 = 12.0; slider18 = 4; slider19 = 100;
    slider20 = 3.5; slider21 = 1.12;
  ) : idx == 8 ? ( // Erik Bickerstaffe
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = -17.0; slider7 = 6200; slider8 = -5.5;
    slider10 = 2.0; slider11 = 2.5; slider12 = 1.2;
    slider13 = 1; slider14 = 1; slider15 = -7.0; slider16 = 2; slider17 = 15.0; slider18 = 1; slider19 = 100;
    slider20 = 4.2; slider21 = 1.02;
  ) : idx == 9 ? ( // Sam Guaiana
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = -19.0; slider7 = 6600; slider8 = -6.0;
    slider10 = 0.5; slider11 = 2.6; slider12 = 2.5;
    slider13 = 1; slider14 = 0; slider15 = -7.5; slider16 = 2; slider17 = 10.0; slider18 = 4; slider19 = 100;
    slider20 = 3.0; slider21 = 1.05;
  ) : idx == 10 ? ( // Zach Tuch
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = -16.0; slider7 = 7000; slider8 = -4.5;
    slider10 = 1.5; slider11 = 1.2; slider12 = 2.8;
    slider13 = 1; slider14 = 1; slider15 = -5.0; slider16 = 1; slider17 = 20.0; slider18 = 2; slider19 = 100;
    slider20 = 2.4; slider21 = 1.18;
  ) : idx == 11 ? ( // Forrester Savell
    slider3 = 0.0; slider4 = -1.5; slider5 = 1; slider6 = -16.0; slider7 = 6800; slider8 = -4.0;
    slider10 = 0.8; slider11 = 1.2; slider12 = 2.2;
    slider13 = 1; slider14 = 1; slider15 = -4.5; slider16 = 1; slider17 = 25.0; slider18 = 4; slider19 = 100;
    slider20 = 1.8; slider21 = 1.14;
  ) : idx == 12 ? ( // Leon Schmidt
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = -20.0; slider7 = 7200; slider8 = -6.5;
    slider10 = -0.5; slider11 = 2.2; slider12 = 3.5;
    slider13 = 1; slider14 = 0; slider15 = -6.5; slider16 = 2; slider17 = 15.0; slider18 = 4; slider19 = 100;
    slider20 = 2.8; slider21 = 1.16;
  ) : idx == 13 ? ( // Ermin Hamidovic
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = -18.0; slider7 = 6800; slider8 = -5.0;
    slider10 = 0.0; slider11 = 1.0; slider12 = 1.5;
    slider13 = 1; slider14 = 0; slider15 = -4.5; slider16 = 1; slider17 = 20.0; slider18 = 4; slider19 = 100;
    slider20 = 1.2; slider21 = 1.00;
  ) : idx == 14 ? ( // Will Putney
    slider3 = 0.0; slider4 = -4.0; slider5 = 1; slider6 = -22.0; slider7 = 6400; slider8 = -8.0;
    slider10 = 1.8; slider11 = 3.2; slider12 = 1.8;
    slider13 = 1; slider14 = 0; slider15 = -10.0; slider16 = 3; slider17 = 8.0; slider18 = 1; slider19 = 100;
    slider20 = 4.8; slider21 = 1.02;
  ) : idx == 15 ? ( // George Lever
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = -17.0; slider7 = 6800; slider8 = -4.5;
    slider10 = 2.0; slider11 = 1.0; slider12 = 2.2;
    slider13 = 1; slider14 = 1; slider15 = -5.0; slider16 = 1; slider17 = 25.0; slider18 = 4; slider19 = 100;
    slider20 = 2.4; slider21 = 1.15;
  ) : idx == 16 ? ( // Sam Bassal
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = -18.0; slider7 = 6500; slider8 = -5.5;
    slider10 = 1.2; slider11 = 2.2; slider12 = 2.0;
    slider13 = 1; slider14 = 0; slider15 = -7.0; slider16 = 2; slider17 = 12.0; slider18 = 4; slider19 = 100;
    slider20 = 3.2; slider21 = 1.08;
  ) : idx == 17 ? ( // Henrik Udd
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = -20.0; slider7 = 6800; slider8 = -7.0;
    slider10 = 0.8; slider11 = 2.8; slider12 = 3.2;
    slider13 = 1; slider14 = 0; slider15 = -7.5; slider16 = 2; slider17 = 15.0; slider18 = 4; slider19 = 100;
    slider20 = 3.2; slider21 = 1.10;
  ) : idx == 18 ? ( // Dan Braunstein
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = -20.0; slider7 = 6900; slider8 = -6.5;
    slider10 = 0.6; slider11 = 2.8; slider12 = 3.8;
    slider13 = 1; slider14 = 0; slider15 = -7.0; slider16 = 2; slider17 = 15.0; slider18 = 4; slider19 = 100;
    slider20 = 3.0; slider21 = 1.12;
  ) : idx == 19 ? ( // Zakk Cervini & Erik Ron
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = -21.0; slider7 = 6800; slider8 = -7.5;
    slider10 = 0.5; slider11 = 3.2; slider12 = 3.5;
    slider13 = 1; slider14 = 0; slider15 = -8.5; slider16 = 3; slider17 = 10.0; slider18 = 0; slider19 = 100;
    slider20 = 3.6; slider21 = 1.08;
  ) : idx == 20 ? ( // Jens Bogren
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = -19.0; slider7 = 6600; slider8 = -6.0;
    slider10 = 1.5; slider11 = 2.0; slider12 = 1.8;
    slider13 = 1; slider14 = 0; slider15 = -7.0; slider16 = 2; slider17 = 18.0; slider18 = 1; slider19 = 100;
    slider20 = 3.8; slider21 = 1.05;
  ) : idx == 21 ? ( // Adam Nolly Getgood
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = -18.0; slider7 = 6800; slider8 = -5.0;
    slider10 = 0.0; slider11 = 2.0; slider12 = 2.4;
    slider13 = 1; slider14 = 0; slider15 = -5.5; slider16 = 1; slider17 = 20.0; slider18 = 4; slider19 = 100;
    slider20 = 1.8; slider21 = 1.00;
  ) : idx == 22 ? ( // Acle Kahney
    slider3 = 0.0; slider4 = -2.0; slider5 = 1; slider6 = -17.0; slider7 = 6800; slider8 = -4.5;
    slider10 = 0.5; slider11 = 1.6; slider12 = 2.2;
    slider13 = 1; slider14 = 0; slider15 = -5.0; slider16 = 1; slider17 = 22.0; slider18 = 4; slider19 = 100;
    slider20 = 1.5; slider21 = 1.06;
  ) : idx == 23 ? ( // Adam Cichocki
    slider3 = 0.0; slider4 = -2.5; slider5 = 1; slider6 = -18.0; slider7 = 6400; slider8 = -5.5;
    slider10 = 1.8; slider11 = 2.0; slider12 = 2.0;
    slider13 = 1; slider14 = 1; slider15 = -6.5; slider16 = 2; slider17 = 18.0; slider18 = 1; slider19 = 100;
    slider20 = 4.0; slider21 = 1.10;
  ) : ( // Manuel Renner (SENNA - Out Of The Blue)
    slider3 = 0.0; slider4 = -3.0; slider5 = 1; slider6 = -20.0; slider7 = 6800; slider8 = -6.5;
    slider10 = 0.8; slider11 = 2.6; slider12 = 3.4;
    slider13 = 1; slider14 = 0; slider15 = -7.5; slider16 = 2; slider17 = 15.0; slider18 = 4; slider19 = 100;
    slider20 = 3.2; slider21 = 1.05;
  );
);

function update_filters() local(w0, alpha, A, beta) (
  // Baxandall 100Hz Warmth Shelf (slider10)
  A = exp(slider10 * 0.0575646273);
  w0 = 2.0 * M_PI * 100.0 / srate;
  alpha = sin(w0) / (2.0 * 0.7071);
  beta = 2.0 * sqrt(A) * alpha;
  bw_b0 = A * ((A + 1.0) - (A - 1.0) * cos(w0) + beta);
  bw_b1 = 2.0 * A * ((A - 1.0) - (A + 1.0) * cos(w0));
  bw_b2 = A * ((A + 1.0) - (A - 1.0) * cos(w0) - beta);
  bw_a0 = (A + 1.0) + (A - 1.0) * cos(w0) + beta;
  bw_a1 = -2.0 * ((A - 1.0) + (A + 1.0) * cos(w0));
  bw_a2 = (A + 1.0) + (A - 1.0) * cos(w0) - beta;

  // Baxandall 3.5kHz Presence Bell (slider11)
  A = exp(slider11 * 0.0575646273);
  w0 = 2.0 * M_PI * 3500.0 / srate;
  alpha = sin(w0) / (2.0 * 0.7);
  bp_b0 = 1.0 + alpha * A;
  bp_b1 = -2.0 * cos(w0);
  bp_b2 = 1.0 - alpha * A;
  bp_a0 = 1.0 + alpha / A;
  bp_a1 = -2.0 * cos(w0);
  bp_a2 = 1.0 - alpha / A;

  // Baxandall 12kHz Silk Air Shelf (slider12)
  A = exp(slider12 * 0.0575646273);
  w0 = 2.0 * M_PI * 12000.0 / srate;
  alpha = sin(w0) / (2.0 * 0.7071);
  beta = 2.0 * sqrt(A) * alpha;
  ba_b0 = A * ((A + 1.0) + (A - 1.0) * cos(w0) + beta);
  ba_b1 = -2.0 * A * ((A - 1.0) + (A + 1.0) * cos(w0));
  ba_b2 = A * ((A + 1.0) + (A - 1.0) * cos(w0) - beta);
  ba_a0 = (A + 1.0) - (A - 1.0) * cos(w0) + beta;
  ba_a1 = 2.0 * ((A - 1.0) - (A + 1.0) * cos(w0));
  ba_a2 = (A + 1.0) - (A - 1.0) * cos(w0) - beta;

  // De-Esser Detector High-Pass Filter (slider7)
  w0 = 2.0 * M_PI * clamp(slider7, 4000.0, 10000.0) / srate;
  alpha = sin(w0) / (2.0 * 0.7071);
  ds_b0 = (1.0 + cos(w0)) * 0.5;
  ds_b1 = -(1.0 + cos(w0));
  ds_b2 = (1.0 + cos(w0)) * 0.5;
  ds_a0 = 1.0 + alpha;
  ds_a1 = -2.0 * cos(w0);
  ds_a2 = 1.0 - alpha;
);

update_filters();

@slider
prev_preset != slider2 ? (
  apply_producer_preset(slider2);
  prev_preset = slider2;
);
update_filters();

@sample
dry_l = spl0; dry_r = spl1;

!slider22 ? (
  vocal_peak = max(abs(spl0), abs(spl1));
) : (
  in_trim = exp(slider3 * 0.1151292546497);
  s0 = spl0 * in_trim;
  s1 = spl1 * in_trim;

  // 1. High-Frequency Limiter & Master De-Esser
  ds_in = (s0 + s1) * 0.5;
  ds_hp = (ds_b0 * ds_in + ds_b1 * ds_hp_x1 + ds_b2 * ds_hp_x2 - ds_a1 * ds_hp_y1 - ds_a2 * ds_hp_y2) / ds_a0;
  ds_hp_x2 = ds_hp_x1; ds_hp_x1 = ds_in; ds_hp_y2 = ds_hp_y1; ds_hp_y1 = ds_hp;

  ds_level = abs(ds_hp);
  ds_db = ds_level > 0.000001 ? 20.0 * log10(ds_level) : -120.0;
  ds_gr_target = 0.0;
  ds_db > slider6 ? (
    ds_gr_target = min(abs(slider8), (ds_db - slider6) * 0.85);
  );
  ds_reduction_db = ds_reduction_db * 0.85 + ds_gr_target * 0.15;
  ds_gain = exp(-ds_reduction_db * 0.1151292546497);

  // Apply de-esser clamping to high band
  s0 = (s0 - ds_hp) + ds_hp * ds_gain;
  s1 = (s1 - ds_hp) + ds_hp * ds_gain;

  // 2. Master Vocal Baxandall EQ
  // 100Hz Warmth
  ty0 = (bw_b0 * s0 + bw_b1 * bax_w_x1 + bw_b2 * bax_w_x2 - bw_a1 * bax_w_y1 - bw_a2 * bax_w_y2) / bw_a0;
  bax_w_x2 = bax_w_x1; bax_w_x1 = s0; bax_w_y2 = bax_w_y1; bax_w_y1 = ty0; s0 = ty0;
  ty1 = (bw_b0 * s1 + bw_b1 * bax_w_x1 + bw_b2 * bax_w_x2 - bw_a1 * bax_w_y1 - bw_a2 * bax_w_y2) / bw_a0;
  s1 = ty1;

  // 3.5kHz Presence
  ty0 = (bp_b0 * s0 + bp_b1 * bax_p_x1 + bp_b2 * bax_p_x2 - bp_a1 * bax_p_y1 - bp_a2 * bax_p_y2) / bp_a0;
  bax_p_x2 = bax_p_x1; bax_p_x1 = s0; bax_p_y2 = bax_p_y1; bax_p_y1 = ty0; s0 = ty0;
  ty1 = (bp_b0 * s1 + bp_b1 * bax_p_x1 + bp_b2 * bax_p_x2 - bp_a1 * bax_p_y1 - bp_a2 * bax_p_y2) / bp_a0;
  s1 = ty1;

  // 12kHz Silk Air
  ty0 = (ba_b0 * s0 + ba_b1 * bax_a_x1 + ba_b2 * bax_a_x2 - ba_a1 * bax_a_y1 - ba_a2 * bax_a_y2) / ba_a0;
  bax_a_x2 = bax_a_x1; bax_a_x1 = s0; bax_a_y2 = bax_a_y1; bax_a_y1 = ty0; s0 = ty0;
  ty1 = (ba_b0 * s1 + ba_b1 * bax_a_x1 + ba_b2 * bax_a_x2 - ba_a1 * bax_a_y1 - ba_a2 * bax_a_y2) / ba_a0;
  s1 = ty1;

  // 3. Master Vocal Bus Glue Compressor
  slider13 ? (
    sc_sig = max(abs(s0), abs(s1));
    sc_db = sc_sig > 0.000001 ? 20.0 * log10(sc_sig) : -120.0;
    r_val = slider16 == 0 ? 1.5 : (slider16 == 1 ? 2.0 : (slider16 == 2 ? 3.0 : 4.0));
    gr_target = 0.0;
    sc_db > slider15 ? (
      over_db = sc_db - slider15;
      slider14 == 1 ? (
        // Opto Leveler two-stage release ballistics
        gr_target = over_db * (1.0 - 1.0 / r_val) * 1.1;
      ) : (
        // Fairchild 670 progressive smooth tube curve
        gr_target = over_db * (1.0 - 1.0 / r_val);
      );
    );
    att_coeff = exp(-1.0 / (clamp(slider17, 0.2, 50.0) * 0.001 * srate));
    rel_ms = slider18 == 0 ? 100.0 : (slider18 == 1 ? 300.0 : (slider18 == 2 ? 600.0 : (slider18 == 3 ? 1200.0 : 350.0)));
    rel_coeff = exp(-1.0 / (rel_ms * 0.001 * srate));

    gr_target > vocal_glue_gr_db ? (
      vocal_glue_gr_db = vocal_glue_gr_db * att_coeff + gr_target * (1.0 - att_coeff);
    ) : (
      vocal_glue_gr_db = vocal_glue_gr_db * rel_coeff + gr_target * (1.0 - rel_coeff);
    );

    comp_gain = exp(-vocal_glue_gr_db * 0.1151292546497);
    wet_f = slider19 * 0.01;
    s0 = s0 * (1.0 - wet_f + comp_gain * wet_f);
    s1 = s1 * (1.0 - wet_f + comp_gain * wet_f);
  );

  // 4. Vocal Tube Warmth Saturation
  slider20 > 0.0 ? (
    t_drive = exp(slider20 * 0.1151292546497);
    td0 = s0 * t_drive; td1 = s1 * t_drive;
    // Even-harmonic tube bloom
    s0 = (td0 + 0.18 * td0 * td0) / (1.0 + abs(td0 + 0.18 * td0 * td0) * 0.35);
    s1 = (td1 + 0.18 * td1 * td1) / (1.0 + abs(td1 + 0.18 * td1 * td1) * 0.35);
    s0 = s0 / sqrt(t_drive);
    s1 = s1 / sqrt(t_drive);
  );

  // 5. Master Vocal Spatializer (Lead Mono Center Lock + Stereo Reverb Spread)
  mid_sig = (s0 + s1) * 0.5;
  side_sig = (s0 - s1) * 0.5 * slider21;
  s0 = mid_sig + side_sig;
  s1 = mid_sig - side_sig;

  // 6. Producer Headroom Trim & Pre-Master Ceiling Guard
  out_trim = exp(slider4 * 0.1151292546497);
  s0 *= out_trim;
  s1 *= out_trim;

  slider5 == 1 ? (
    s0 = clamp(s0, -0.501187, 0.501187);
    s1 = clamp(s1, -0.501187, 0.501187);
  );

  // 7. Delta Audition Mode
  slider23 ? (
    spl0 = s0 - dry_l;
    spl1 = s1 - dry_r;
  ) : (
    spl0 = s0;
    spl1 = s1;
  );

  vocal_peak = max(abs(spl0), abs(spl1));
);

// Ballistics & Shared Memory Telemetry
sifam_tube_needle = sifam_tube_needle * 0.92 + (slider20) * 0.08;
sifam_vocal_glue_needle = sifam_vocal_glue_needle * 0.90 + (vocal_glue_gr_db) * 0.10;

v_acc_l += spl0 * spl0;
v_acc_r += spl1 * spl1;
v_cnt += 1;
v_cnt >= 1024 ? (
  vocal_rms = 10.0 * log10(max(0.000000001, (v_acc_l + v_acc_r) / (v_cnt * 2.0)));
  v_acc_l = 0.0; v_acc_r = 0.0; v_cnt = 0;
  // Publish live telemetry (1450..1499)
  gmem[1451] = 20.0 * log10(max(0.000001, vocal_peak));
  gmem[1452] = vocal_rms;
  gmem[1454] = ds_reduction_db;
  gmem[1455] = vocal_glue_gr_db;
  gmem[1456] = slider27 ? min(3.0, max(0.0, (vocal_rms + 35.0) * 0.15)) : 0.0;
  gmem[1457] = slider2;
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

// Outer Deep Royal Empress Plum Chassis
gfx_r = 0.038; gfx_g = 0.016; gfx_b = 0.048;
gfx_rect(crt_x, crt_y, crt_w, crt_h);

// Cyber Rose Quartz Border Trim
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
gfx_rect(crt_x, crt_y, crt_w, crt_h, 0);
gfx_rect(crt_x + 1, crt_y + 1, crt_w - 2, crt_h - 2, 0);

// Corner Machine Screws (Rose Gold)
function draw_vocal_screw(sx, sy) (
  gfx_r = 0.22; gfx_g = 0.10; gfx_b = 0.28; gfx_circle(sx, sy, 5, 1);
  gfx_r = 1.00; gfx_g = 0.50; gfx_b = 0.75; gfx_circle(sx, sy, 5, 0);
  gfx_line(sx - 3, sy, sx + 3, sy);
);
draw_vocal_screw(crt_x + 8, crt_y + 8);
draw_vocal_screw(crt_x + crt_w - 8, crt_y + 8);
draw_vocal_screw(crt_x + 8, crt_y + crt_h - 8);
draw_vocal_screw(crt_x + crt_w - 8, crt_y + crt_h - 8);

// ─────────────────────────────────────────────────────────────────────────────
// 1. TOP HEADER BAR: DUAFE CREST, PRESET STEPPER & SYSTEM STATUS PILLS
// ─────────────────────────────────────────────────────────────────────────────
hdr_h = 48;
gfx_r = 0.024; gfx_g = 0.010; gfx_b = 0.032;
gfx_rect(crt_x + 2, crt_y + 2, crt_w - 4, hdr_h);
gfx_r = 0.20; gfx_g = 0.10; gfx_b = 0.26;
gfx_line(crt_x + 2, crt_y + hdr_h + 2, crt_x + crt_w - 2, crt_y + hdr_h + 2);

// Duafe Wooden Comb Emblem (Symbol of Beauty, Refinement & Royalty)
sig_cx = crt_x + 24; sig_cy = crt_y + 24;
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
gfx_circle(sig_cx, sig_cy, 12, 0);
gfx_circle(sig_cx, sig_cy, 8, 0);
gfx_circle(sig_cx, sig_cy, 4, 1);

gfx_r = 1.00; gfx_g = 0.90; gfx_b = 1.00;
gfx_setfont(1, "Orbitron", 13.0, 'b');
gfx_x = crt_x + 44; gfx_y = crt_y + 16;
t_str = "DAMEI // VOCAL EMPRESS";
gfx_drawstr(t_str);
gfx_measurestr(t_str, tsw, tsh);
title_end_x = crt_x + 44 + tsw + 12;
right_edge_x = crt_x + crt_w - 12;

// Right Header Zone: Pinned Control Pills (Right to Left)
// Pill 1: ENGAGED / BYPASS
byp_w = 78; byp_x = right_edge_x - byp_w;
byp_hov = (mouse_x >= byp_x && mouse_x <= byp_x + byp_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider22 ? (byp_hov ? 0.18 : 0.09) : (byp_hov ? 0.28 : 0.16);
gfx_g = slider22 ? (byp_hov ? 0.08 : 0.04) : (byp_hov ? 0.08 : 0.04);
gfx_b = slider22 ? (byp_hov ? 0.24 : 0.13) : (byp_hov ? 0.10 : 0.05);
gfx_rect(byp_x, crt_y + 9, byp_w, 30);
gfx_r = slider22 ? 1.00 : 0.95; gfx_g = slider22 ? 0.41 : 0.30; gfx_b = slider22 ? 0.70 : 0.30;
gfx_rect(byp_x, crt_y + 9, byp_w, 30, 0);
gfx_setfont(2, "Orbitron", 10.5, 'b');
b_txt = slider22 ? "ENGAGED" : "BYPASS";
gfx_measurestr(b_txt, btw, bth);
gfx_x = byp_x + (byp_w - btw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(b_txt);
mouse_clicked && byp_hov ? (slider22 = !slider22; slider_automate(););

// Pill 2: Headroom Ceiling (-6dB Lock vs Free)
ceil_w = 84; ceil_x = byp_x - ceil_w - 6;
ceil_hov = (mouse_x >= ceil_x && mouse_x <= ceil_x + ceil_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider5 ? 0.12 : 0.06; gfx_g = slider5 ? 0.06 : 0.04; gfx_b = slider5 ? 0.18 : 0.08;
gfx_rect(ceil_x, crt_y + 9, ceil_w, 30);
gfx_r = slider5 ? 1.00 : 0.50; gfx_g = slider5 ? 0.41 : 0.50; gfx_b = slider5 ? 0.70 : 0.50;
gfx_rect(ceil_x, crt_y + 9, ceil_w, 30, 0);
gfx_setfont(3, "Consolas", 10.5, 'b');
c_txt = slider5 ? "CEIL: -6dB" : "CEIL: FREE";
gfx_measurestr(c_txt, ctw, cth);
gfx_x = ceil_x + (ceil_w - ctw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(c_txt);
mouse_clicked && ceil_hov ? (slider5 = !slider5; slider_automate(););

// Pill 3: Mode (Master Sum vs Stem Sum)
mode_w = 88; mode_x = ceil_x - mode_w - 6;
mode_hov = (mouse_x >= mode_x && mouse_x <= mode_x + mode_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = 0.12; gfx_g = 0.06; gfx_b = 0.18; gfx_rect(mode_x, crt_y + 9, mode_w, 30);
gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(mode_x, crt_y + 9, mode_w, 30, 0);
gfx_setfont(3, "Consolas", 10.0, 'b');
m_txt = slider25 ? "MODE: STEM" : "MODE: MASTER";
gfx_measurestr(m_txt, mtw, mth);
gfx_x = mode_x + (mode_w - mtw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(m_txt);
mouse_clicked && mode_hov ? (slider25 = !slider25; slider_automate(););

// Pill 4: Music Bus Telemetry Link
ib_inst_rms = gmem[1402];
ib_alive = (gmem[1400] == 1);
mlink_w = 98; mlink_x = mode_x - mlink_w - 6;
gfx_r = ib_alive ? 0.06 : 0.08; gfx_g = ib_alive ? 0.12 : 0.06; gfx_b = ib_alive ? 0.16 : 0.08;
gfx_rect(mlink_x, crt_y + 9, mlink_w, 30);
gfx_r = ib_alive ? 0.00 : 0.50; gfx_g = ib_alive ? 0.85 : 0.50; gfx_b = ib_alive ? 1.00 : 0.50;
gfx_rect(mlink_x, crt_y + 9, mlink_w, 30, 0);
gfx_setfont(3, "Consolas", 10.0, 'b');
ib_str = ib_alive ? sprintf(#, "MUS: %.1fdB", ib_inst_rms) : "MUS: STBY";
gfx_measurestr(ib_str, ibw, ibh);
gfx_x = mlink_x + (mlink_w - ibw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(ib_str);

// Pill 5: Song Structure Sync
rgn_w = 92; rgn_x = mlink_x - rgn_w - 6;
gfx_r = 0.08; gfx_g = 0.04; gfx_b = 0.11; gfx_rect(rgn_x, crt_y + 9, rgn_w, 30);
gfx_r = 0.85; gfx_g = 0.45; gfx_b = 1.00; gfx_rect(rgn_x, crt_y + 9, rgn_w, 30, 0);
g_sec = gmem[100] == 1 ? gmem[101] : 0;
r_str = g_sec == 3 ? "⚡ CHORUS" : sprintf(#, "● SYNC: %dR", gmem[103] > 0 ? gmem[103] : 20);
gfx_setfont(3, "Consolas", 10.0, 'b');
gfx_measurestr(r_str, rsw, rsh);
gfx_x = rgn_x + (rgn_w - rsw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(r_str);

// Pill 6: Non-Destructive A/B Snapshot
ab_w = 50; ab_x = rgn_x - ab_w - 6;
ab_hov = (mouse_x >= ab_x && mouse_x <= ab_x + ab_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider24 ? 0.25 : 0.08; gfx_g = slider24 ? 0.10 : 0.04; gfx_b = slider24 ? 0.32 : 0.16;
gfx_rect(ab_x, crt_y + 9, ab_w, 30);
gfx_r = slider24 ? 1.00 : 0.70; gfx_g = slider24 ? 0.45 : 0.40; gfx_b = slider24 ? 0.85 : 0.90;
gfx_rect(ab_x, crt_y + 9, ab_w, 30, 0);
gfx_setfont(2, "Orbitron", 10.0, 'b');
ab_str = slider24 ? "SNAP B" : "SNAP A";
gfx_measurestr(ab_str, abw, abh);
gfx_x = ab_x + (ab_w - abw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(ab_str);
mouse_clicked && ab_hov ? (slider24 = !slider24; slider_automate(););

// Pill 7: Delta Solo Listen
del_w = 46; del_x = ab_x - del_w - 6;
del_hov = (mouse_x >= del_x && mouse_x <= del_x + del_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = slider23 ? 0.32 : 0.08; gfx_g = slider23 ? 0.08 : 0.04; gfx_b = slider23 ? 0.10 : 0.08;
gfx_rect(del_x, crt_y + 9, del_w, 30);
gfx_r = slider23 ? 1.00 : 0.50; gfx_g = slider23 ? 0.25 : 0.35; gfx_b = slider23 ? 0.35 : 0.45;
gfx_rect(del_x, crt_y + 9, del_w, 30, 0);
gfx_setfont(2, "Orbitron", 10.0, 'b');
del_str = slider23 ? "DELTA" : "NORM";
gfx_measurestr(del_str, dlw, dlh);
gfx_x = del_x + (del_w - dlw) * 0.5; gfx_y = crt_y + 16;
gfx_drawstr(del_str);
mouse_clicked && del_hov ? (slider23 = !slider23; slider_automate(););

// Center Preset Stepper Zone
avail_mid = max(80, del_x - title_end_x - 10);
btn_step_w = 22;
bar_w = max(70, avail_mid - btn_step_w * 2 - 8);
btn_l_x = title_end_x + 5;
bar_x = btn_l_x + btn_step_w + 4;
btn_r_x = bar_x + bar_w + 4;

// Left Step Button '<'
btn_l_hov = (mouse_x >= btn_l_x && mouse_x <= btn_l_x + btn_step_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = btn_l_hov ? 0.25 : 0.09; gfx_g = btn_l_hov ? 0.10 : 0.04; gfx_b = btn_l_hov ? 0.20 : 0.12;
gfx_rect(btn_l_x, crt_y + 9, btn_step_w, 30);
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(btn_l_x, crt_y + 9, btn_step_w, 30, 0);
gfx_setfont(1, "Orbitron", 12, 'b'); gfx_x = btn_l_x + 6; gfx_y = crt_y + 15; gfx_drawstr("<");
mouse_clicked && btn_l_hov ? (
  slider2 = (slider2 - 1 + 25) % 25;
  apply_producer_preset(slider2);
  slider_automate();
);

// Center Preset Bar
bar_hov = (mouse_x >= bar_x && mouse_x <= bar_x + bar_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = bar_hov ? 0.18 : 0.08; gfx_g = bar_hov ? 0.08 : 0.04; gfx_b = bar_hov ? 0.16 : 0.09;
gfx_rect(bar_x, crt_y + 9, bar_w, 30);
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(bar_x, crt_y + 9, bar_w, 30, 0);

p_str = get_producer_short_name(slider2);
p_sz = 11.0;
gfx_setfont(4, "Segoe UI", p_sz, 'b');
gfx_measurestr(p_str, psw, psh);
while (psw > bar_w - 12 && p_sz > 8.0) (
  p_sz -= 0.5;
  gfx_setfont(4, "Segoe UI", p_sz, 'b');
  gfx_measurestr(p_str, psw, psh);
);
gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;
gfx_x = bar_x + floor((bar_w - psw) * 0.5); gfx_y = crt_y + 16;
gfx_drawstr(p_str);
mouse_clicked && bar_hov ? (
  slider2 = (slider2 + 1) % 25;
  apply_producer_preset(slider2);
  slider_automate();
);

// Right Step Button '>'
btn_r_hov = (mouse_x >= btn_r_x && mouse_x <= btn_r_x + btn_step_w && mouse_y >= crt_y + 9 && mouse_y <= crt_y + 39);
gfx_r = btn_r_hov ? 0.25 : 0.09; gfx_g = btn_r_hov ? 0.10 : 0.04; gfx_b = btn_r_hov ? 0.20 : 0.12;
gfx_rect(btn_r_x, crt_y + 9, btn_step_w, 30);
gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(btn_r_x, crt_y + 9, btn_step_w, 30, 0);
gfx_setfont(1, "Orbitron", 12, 'b'); gfx_x = btn_r_x + 7; gfx_y = crt_y + 15; gfx_drawstr(">");
mouse_clicked && btn_r_hov ? (
  slider2 = (slider2 + 1) % 25;
  apply_producer_preset(slider2);
  slider_automate();
);

// ─────────────────────────────────────────────────────────────────────────────
// 2. NAVIGATION TABS (7 DEDICATED TABS)
// ─────────────────────────────────────────────────────────────────────────────
tab_y = crt_y + hdr_h + 4; tab_h = 28;
tab_w = floor((crt_w - 8) / 7);
ti = 0;
loop(7,
  tx = crt_x + 4 + ti * tab_w;
  sel = (slider1 == ti);
  t_hov = (mouse_x >= tx && mouse_x <= tx + tab_w - 2 && mouse_y >= tab_y && mouse_y <= tab_y + tab_h);
  gfx_r = sel ? 0.18 : (t_hov ? 0.09 : 0.04);
  gfx_g = sel ? 0.08 : (t_hov ? 0.04 : 0.02);
  gfx_b = sel ? 0.26 : (t_hov ? 0.13 : 0.06);
  gfx_rect(tx, tab_y, tab_w - 2, tab_h);
  sel ? (
    gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
    gfx_rect(tx, tab_y + tab_h - 2, tab_w - 2, 2);
    gfx_r = 1.00; gfx_g = 0.90; gfx_b = 1.00;
  ) : (
    gfx_r = t_hov ? 0.95 : 0.70; gfx_g = t_hov ? 0.85 : 0.60; gfx_b = t_hov ? 0.95 : 0.75;
  );
  gfx_setfont(2, "Orbitron", 10.5, 'b');
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
gfx_r = 0.025; gfx_g = 0.012; gfx_b = 0.035;
gfx_rect(ws_x, ws_y, ws_w, ws_h);
gfx_r = 0.22; gfx_g = 0.10; gfx_b = 0.28;
gfx_rect(ws_x, ws_y, ws_w, ws_h, 0);

// Helper function for full-height interactive channel strip slider
function draw_vocal_channel_strip(px, py, pw, ph, label_str, badge_str, val, min_v, max_v, fmt_str, s_idx, accent_r, accent_g, accent_b) (
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(px, py, pw, ph);
  gfx_r = accent_r * 0.7; gfx_g = accent_g * 0.7; gfx_b = accent_b * 0.7; gfx_rect(px, py, pw, ph, 0);

  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_measurestr(label_str, lsw, lsh);
  gfx_x = px + floor((pw - lsw) * 0.5); gfx_y = py + 12; gfx_drawstr(label_str);

  gfx_setfont(3, "Consolas", 10.0, 'b'); gfx_r = 0.70; gfx_g = 0.60; gfx_b = 0.85;
  gfx_measurestr(badge_str, bsw, bsh);
  gfx_x = px + floor((pw - bsw) * 0.5); gfx_y = py + 30; gfx_drawstr(badge_str);

  v_box_y = py + 52; v_box_h = 28; v_box_w = pw - 20;
  gfx_r = 0.028; gfx_g = 0.014; gfx_b = 0.038; gfx_rect(px + 10, v_box_y, v_box_w, v_box_h);
  gfx_r = accent_r * 0.8; gfx_g = accent_g * 0.8; gfx_b = accent_b * 0.8; gfx_rect(px + 10, v_box_y, v_box_w, v_box_h, 0);
  val_str = sprintf(#, fmt_str, val);
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.95;
  gfx_measurestr(val_str, vsw, vsh);
  gfx_x = px + floor((pw - vsw) * 0.5); gfx_y = v_box_y + 7; gfx_drawstr(val_str);

  trk_x = px + floor(pw * 0.5) - 4; trk_y = py + 95; trk_h = ph - 140; trk_w = 8;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(trk_x, trk_y, trk_w, trk_h);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(trk_x, trk_y, trk_w, trk_h, 0);

  gfx_setfont(3, "Consolas", 9.5); gfx_r = 0.60; gfx_g = 0.50; gfx_b = 0.75;
  gfx_line(trk_x - 14, trk_y, trk_x - 4, trk_y); gfx_x = trk_x - 36; gfx_y = trk_y - 5; gfx_drawstr("+6");
  gfx_line(trk_x - 14, trk_y + trk_h * 0.5, trk_x - 4, trk_y + trk_h * 0.5); gfx_x = trk_x - 30; gfx_y = trk_y + trk_h * 0.5 - 5; gfx_drawstr("0");
  gfx_line(trk_x - 14, trk_y + trk_h, trk_x - 4, trk_y + trk_h); gfx_x = trk_x - 36; gfx_y = trk_y + trk_h - 5; gfx_drawstr("-6");

  frac = max(0.0, min(1.0, (val - min_v) / (max_v - min_v)));
  h_cy = trk_y + trk_h - floor(frac * trk_h);

  mid_y = trk_y + trk_h * 0.5;
  h_cy < mid_y ? (
    gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
    gfx_rect(trk_x + 1, h_cy, trk_w - 2, mid_y - h_cy);
  ) : (
    gfx_r = accent_r * 0.6; gfx_g = accent_g * 0.6; gfx_b = accent_b * 0.6;
    gfx_rect(trk_x + 1, mid_y, trk_w - 2, h_cy - mid_y);
  );

  cap_w = pw - 34; cap_h = 16; cap_x = px + 17; cap_y = h_cy - 8;
  gfx_r = 0.24; gfx_g = 0.14; gfx_b = 0.32; gfx_rect(cap_x, cap_y, cap_w, cap_h);
  gfx_r = 0.95; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(cap_x, cap_y, cap_w, cap_h, 0);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b; gfx_line(cap_x + 6, cap_y + 8, cap_x + cap_w - 6, cap_y + 8);

  b_lbl_y = py + ph - 28;
  gfx_setfont(3, "Consolas", 10.0, 'b'); gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  bot_str = "DRAG / WHEEL";
  gfx_measurestr(bot_str, bbw, bbh);
  gfx_x = px + floor((pw - bbw) * 0.5); gfx_y = b_lbl_y; gfx_drawstr(bot_str);

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
  gfx_r = 0.028; gfx_g = 0.014; gfx_b = 0.038; gfx_rect(px, py, pw, ph);
  gfx_r = 0.28; gfx_g = 0.14; gfx_b = 0.36; gfx_rect(px, py, pw, ph, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_x = px + 10; gfx_y = py + 6; gfx_drawstr(label_str);

  val_str = sprintf(#, fmt_str, val);
  gfx_setfont(3, "Consolas", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.95;
  gfx_measurestr(val_str, vsw, vsh);
  gfx_x = px + pw - vsw - 10; gfx_y = py + 6; gfx_drawstr(val_str);

  trx = px + 10; try = py + 26; trw = pw - 20; trh = 8;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(trx, try, trw, trh);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(trx, try, trw, trh, 0);

  frac = max(0.0, min(1.0, (val - min_v) / (max_v - min_v)));
  fill_w = floor(frac * trw);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_rect(trx, try, fill_w, trh);

  hx = trx + fill_w; hy = try + trh * 0.5;
  gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.95; gfx_circle(hx, hy, 6, 1);
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

// Helper for SIFAM Analogue VU Meter with backlit rose/violet scale arc
function draw_vocal_sifam(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) (
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026;
  gfx_rect(mx, my, mw, mh);
  gfx_r = accent_r * 0.7; gfx_g = accent_g * 0.7; gfx_b = accent_b * 0.7;
  gfx_rect(mx, my, mw, mh, 0);

  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_x = mx + 14; gfx_y = my + 10; gfx_drawstr(title_str);

  gfx_setfont(3, "Consolas", 10.5, 'b'); gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  gfx_x = mx + mw - 75; gfx_y = my + 10;
  gfx_drawstr(is_glue ? "GR GAIN" : "TUBE VU");

  piv_x = mx + mw * 0.5;
  piv_y = my + mh + 28;
  r_arc = mh * 0.88;
  ang_min = -0.785398;
  ang_max = 0.785398;

  gfx_r = 0.22; gfx_g = 0.12; gfx_b = 0.30;
  step_a = (ang_max - ang_min) / 40.0;
  ai = 0;
  loop(40,
    a1 = ang_min + ai * step_a; a2 = a1 + step_a;
    gfx_line(piv_x + sin(a1) * r_arc, piv_y - cos(a1) * r_arc, piv_x + sin(a2) * r_arc, piv_y - cos(a2) * r_arc);
    ai += 1;
  );

  gfx_setfont(3, "Consolas", 9.5);
  ti = 0;
  loop(9,
    f = ti / 8.0;
    ta = ang_min + f * (ang_max - ang_min);
    is_red = (f >= 0.75);
    gfx_r = is_red ? 1.00 : (accent_r * 0.9);
    gfx_g = is_red ? 0.30 : (accent_g * 0.9);
    gfx_b = is_red ? 0.40 : (accent_b * 0.9);
    t_len = (ti % 2 == 0) ? 9 : 5;
    gfx_line(piv_x + sin(ta) * (r_arc - t_len), piv_y - cos(ta) * (r_arc - t_len), piv_x + sin(ta) * (r_arc + 1), piv_y - cos(ta) * (r_arc + 1));
    ti += 1;
  );

  gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  gfx_x = piv_x + sin(ang_min) * (r_arc + 4) - 8; gfx_y = piv_y - cos(ang_min) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "0" : "-20");
  gfx_x = piv_x - 6; gfx_y = piv_y - r_arc - 16; gfx_drawstr(is_glue ? "-6" : "-5");
  gfx_r = 1.00; gfx_g = 0.30; gfx_b = 0.40;
  gfx_x = piv_x + sin(ang_max) * (r_arc + 4) - 12; gfx_y = piv_y - cos(ang_max) * (r_arc + 4) - 6; gfx_drawstr(is_glue ? "-16" : "+3");

  n_frac = max(0.0, min(1.0, needle_val / max_val));
  n_ang = ang_min + n_frac * (ang_max - ang_min);
  tip_x = piv_x + sin(n_ang) * (r_arc + 2);
  tip_y = piv_y - cos(n_ang) * (r_arc + 2);
  base_x = piv_x + sin(n_ang) * 14;
  base_y = piv_y - cos(n_ang) * 14;

  gfx_r = 0.05; gfx_g = 0.02; gfx_b = 0.08;
  gfx_line(base_x + 2, base_y + 2, tip_x + 2, tip_y + 2);

  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;
  gfx_line(base_x - 0.5, base_y, tip_x - 0.5, tip_y);
  gfx_line(base_x + 0.5, base_y, tip_x + 0.5, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  gfx_r = 1.00; gfx_g = 0.30; gfx_b = 0.40; gfx_circle(tip_x, tip_y, 2, 1);
  gfx_r = 0.16; gfx_g = 0.08; gfx_b = 0.22; gfx_circle(piv_x, my + mh - 8, 14, 1);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b; gfx_circle(piv_x, my + mh - 8, 14, 0);
);

// =============================================================================
// TAB 0: OVERVIEW (TWIN SIFAM ANALOG METERS + SPATIAL SCOPE + 3-COLUMN DASHBOARD)
// =============================================================================
slider1 == 0 ? (
  top_row_h = 240;
  meter_w = floor((ws_w - 36 - 280) * 0.5);

  // Left Meter: SIFAM Vocal Tube Warmth VU
  draw_vocal_sifam(ws_x + 12, ws_y + 12, meter_w, top_row_h, "VOCAL TUBE WARMTH // SATURATION", sifam_tube_needle, 10.0, 0, 1.00, 0.41, 0.70);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = ws_x + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("+%.1f dB TUBE", slider20);

  // Middle Meter: SIFAM Master Vocal Bus Glue GR
  draw_vocal_sifam(ws_x + 12 + meter_w + 12, ws_y + 12, meter_w, top_row_h, "MASTER VOCAL GLUE // GAIN REDUCTION", sifam_vocal_glue_needle, 16.0, 1, 0.70, 0.53, 1.00);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = ws_x + 12 + meter_w + 26; gfx_y = ws_y + top_row_h - 22;
  gfx_printf("-%.1f dB GR", sifam_vocal_glue_needle);

  // Right Box: Master Vocal Spatial Radar & Phase Correlation
  scope_x = ws_x + 12 + meter_w * 2 + 24; scope_w = ws_w - (meter_w * 2 + 48); scope_h = top_row_h;
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(scope_x, ws_y + 12, scope_w, scope_h, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = scope_x + 14; gfx_y = ws_y + 22; gfx_drawstr("VOCAL SPATIAL RADAR");

  sc_cx = scope_x + scope_w * 0.5; sc_cy = ws_y + 12 + scope_h * 0.48; sc_r = scope_h * 0.35;
  gfx_r = 0.22; gfx_g = 0.12; gfx_b = 0.30;
  gfx_circle(sc_cx, sc_cy, sc_r, 0);
  gfx_circle(sc_cx, sc_cy, sc_r * 0.5, 0);
  gfx_line(sc_cx - sc_r, sc_cy, sc_cx + sc_r, sc_cy);
  gfx_line(sc_cx, sc_cy - sc_r, sc_cx, sc_cy + sc_r);

  // Phase Correlation Bar
  cbar_y = ws_y + top_row_h - 28; cbar_w = scope_w - 28;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(scope_x + 14, cbar_y, cbar_w, 14);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(scope_x + 14, cbar_y, cbar_w, 14, 0);
  c_f = max(0.0, min(1.0, (vocal_phase_corr + 1.0) * 0.5));
  cx_pos = scope_x + 14 + floor(c_f * cbar_w);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_rect(cx_pos - 2, cbar_y - 2, 4, 18);

  gfx_setfont(3, "Consolas", 9.5, 'b'); gfx_r = 0.75; gfx_g = 0.65; gfx_b = 0.85;
  gfx_x = scope_x + 14; gfx_y = cbar_y - 14; gfx_drawstr("-1.0");
  gfx_x = scope_x + 14 + floor(cbar_w * 0.5) - 8; gfx_y = cbar_y - 14; gfx_drawstr("0.0");
  gfx_x = scope_x + 14 + cbar_w - 24; gfx_y = cbar_y - 14; gfx_drawstr("+1.0");

  // Bottom Status & Forensic 3-Column Dashboard
  p_y = ws_y + top_row_h + 16; p_h = ws_h - top_row_h - 26;
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 12, p_y, ws_w - 24, p_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 12, p_y, ws_w - 24, p_h, 0);

  // Plaque Title Bar
  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = ws_x + 28; gfx_y = p_y + 12;
  gfx_printf("ACTIVE PROFILE: %02d - %s", slider2, get_producer_full_title(slider2));

  // 3 Forensic Columns
  col_w = floor((ws_w - 24 - 40) / 3);
  cy_start = p_y + 40;

  // Column 1: Gain Staging & Empress Calibration
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 28; gfx_y = cy_start; gfx_drawstr("1. VOCAL GAIN & SUMMING");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.85; gfx_g = 0.80; gfx_b = 0.95;
  gfx_x = ws_x + 28; gfx_y = cy_start + 22; gfx_printf("Input Calibration : %+4.1f dB", slider3);
  gfx_x = ws_x + 28; gfx_y = cy_start + 40; gfx_printf("Producer Output   : %+4.1f dB Trim", slider4);
  gfx_x = ws_x + 28; gfx_y = cy_start + 58; gfx_printf("Pre-Master Ceiling: %s", slider5 ? "-6.0 dBTP Strict Lock" : "Free Range");
  gfx_x = ws_x + 28; gfx_y = cy_start + 76; gfx_printf("Summing State     : %s", slider22 ? "ACTIVE VOCAL SUM" : "1:1 PASS");
  gfx_x = ws_x + 28; gfx_y = cy_start + 94; gfx_printf("Delta Solo State  : %s", slider23 ? "ACTIVE SOLO" : "NORMAL SUM");

  // Column 2: Master Vocal Glue & De-Esser
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start; gfx_drawstr("2. GLUE & SIBILANCE SENTRY");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.85; gfx_g = 0.80; gfx_b = 0.95;
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start + 22; gfx_printf("Glue Topology     : %s", slider14 ? "Vintage Opto Leveler" : "Fairchild 670 Tube");
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start + 40; gfx_printf("Threshold / Ratio : %.1f dB | %s", slider15, slider16 == 0 ? "1.5:1" : (slider16 == 1 ? "2:1" : (slider16 == 2 ? "3:1" : "4:1")));
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start + 58; gfx_printf("Attack / Release  : %.1fms | %s", slider17, slider18 == 0 ? "100ms" : (slider18 == 1 ? "300ms" : (slider18 == 2 ? "600ms" : "Auto")));
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start + 76; gfx_printf("De-Esser Clamp    : %.1fdB @ %d Hz", ds_reduction_db, slider7);
  gfx_x = ws_x + 28 + col_w + 12; gfx_y = cy_start + 94; gfx_printf("Live Vocal Glue GR: -%.2f dB Peak Hold", vocal_glue_gr_db);

  // Column 3: Baxandall & Music Corridor Handshake
  gfx_setfont(2, "Orbitron", 11, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.40;
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start; gfx_drawstr("3. BAXANDALL & CORRIDOR");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.85; gfx_g = 0.80; gfx_b = 0.95;
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start + 22; gfx_printf("100Hz Warmth Shelf: %+.1f dB", slider10);
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start + 40; gfx_printf("3.5kHz Presence   : %+.1f dB", slider11);
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start + 58; gfx_printf("12kHz Silk Air    : %+.1f dB Shelf", slider12);
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start + 76; gfx_printf("Spatial Width     : %.2f x (Lead Lock)", slider21);
  gfx_x = ws_x + 28 + (col_w + 12) * 2; gfx_y = cy_start + 94; gfx_printf("Pocket Carve Sent : -%.1f dB Request", slider27 ? (vocal_rms > -40.0 ? 1.5 : 0.0) : 0.0);
);

// =============================================================================
// TAB 1: BAXANDALL EQ (CURVE PLOT + 4 FULL-HEIGHT CHANNEL STRIPS)
// =============================================================================
slider1 == 1 ? (
  eq_plot_y = ws_y + 12; eq_plot_h = 230; eq_plot_w = ws_w - 24;
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 12, eq_plot_y, eq_plot_w, eq_plot_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 12, eq_plot_y, eq_plot_w, eq_plot_h, 0);

  gfx_setfont(2, "Orbitron", 11.5, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 24; gfx_y = eq_plot_y + 10; gfx_drawstr("MASTER VOCAL BAXANDALL EQ RESPONSE CURVE");

  cy0 = eq_plot_y + eq_plot_h * 0.5;
  gfx_r = 0.15; gfx_g = 0.08; gfx_b = 0.22;
  gfx_line(ws_x + 12, cy0, ws_x + 12 + eq_plot_w, cy0);
  gfx_line(ws_x + 12, cy0 - 45, ws_x + 12 + eq_plot_w, cy0 - 45);
  gfx_line(ws_x + 12, cy0 + 45, ws_x + 12 + eq_plot_w, cy0 + 45);

  fx100 = ws_x + 12 + floor(eq_plot_w * 0.23);
  fx1k  = ws_x + 12 + floor(eq_plot_w * 0.56);
  fx10k = ws_x + 12 + floor(eq_plot_w * 0.88);
  gfx_line(fx100, eq_plot_y, fx100, eq_plot_y + eq_plot_h);
  gfx_line(fx1k,  eq_plot_y, fx1k,  eq_plot_y + eq_plot_h);
  gfx_line(fx10k, eq_plot_y, fx10k, eq_plot_y + eq_plot_h);

  gfx_setfont(3, "Consolas", 9.5); gfx_r = 0.70; gfx_g = 0.60; gfx_b = 0.85;
  gfx_x = fx100 + 4; gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("100Hz");
  gfx_x = fx1k + 4;  gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("1kHz");
  gfx_x = fx10k + 4; gfx_y = eq_plot_y + eq_plot_h - 18; gfx_drawstr("10kHz");

  // Draw Baxandall Response Curve
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  prev_py = cy0;
  pi = 0;
  loop(120,
    px = ws_x + 12 + floor((pi / 119.0) * eq_plot_w);
    f_val = 20.0 * exp(log(1000.0) * (pi / 119.0));
    g_tot = 0.0;
    // 100Hz warmth shelf
    f_val < 300.0 ? g_tot += slider10 * (1.0 - min(1.0, f_val / 300.0));
    // 3.5kHz broad presence bell
    g_tot += slider11 * exp(-0.5 * sqr((log(f_val / 3500.0) / 0.65)));
    // 12kHz silk air shelf
    f_val > 5000.0 ? g_tot += slider12 * (min(1.0, (f_val - 5000.0) / 7000.0));
    cur_py = cy0 - g_tot * 7.5;
    pi > 0 ? gfx_line(prev_px, prev_py, px, cur_py);
    prev_px = px; prev_py = cur_py;
    pi += 1;
  );

  // 4 Full-Height Channel Strips with zero empty gaps!
  col_w = floor((ws_w - 24 - 24) / 4);
  cards_y = eq_plot_y + eq_plot_h + 12; cards_h = ws_h - eq_plot_h - 28;
  draw_vocal_channel_strip(ws_x + 12 + 0 * (col_w + 8), cards_y, col_w, cards_h, "100Hz WARMTH", "CHEST RESONANCE", slider10, -6.0, 6.0, "%+.1f dB", 10, 1.00, 0.41, 0.70);
  draw_vocal_channel_strip(ws_x + 12 + 1 * (col_w + 8), cards_y, col_w, cards_h, "3.5kHz PRESENCE", "INTELLIGIBILITY", slider11, -6.0, 6.0, "%+.1f dB", 11, 0.70, 0.53, 1.00);
  draw_vocal_channel_strip(ws_x + 12 + 2 * (col_w + 8), cards_y, col_w, cards_h, "12kHz SILK AIR", "CONDENSER SHEEN", slider12, -6.0, 6.0, "%+.1f dB", 12, 1.00, 0.85, 0.40);
  draw_vocal_channel_strip(ws_x + 12 + 3 * (col_w + 8), cards_y, col_w, cards_h, "MASTER TRIM", "OUTPUT STAGING", slider4, -6.0, 6.0, "%+.1f dB", 4, 1.00, 0.41, 0.70);
);

// =============================================================================
// TAB 2: VOCAL GLUE COMPRESSOR (TRANSFER PLOT + DUAL TOPOLOGY + DENSE CONTROLS)
// =============================================================================
slider1 == 2 ? (
  cg_y = ws_y + 12; cg_w = ws_w - 24; cg_h = ws_h - 24;
  left_w = floor((cg_w - 24) * 0.45);
  right_w = cg_w - left_w - 16;

  // Left Box: Dynamic Compression Transfer Function Plot
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 12, cg_y, left_w, cg_h);
  gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(ws_x + 12, cg_y, left_w, cg_h, 0);

  gfx_setfont(2, "Orbitron", 11.5, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = ws_x + 24; gfx_y = cg_y + 12; gfx_drawstr("VOCAL GLUE TRANSFER FUNCTION");

  p_x0 = ws_x + 40; p_y0 = cg_y + 45; p_size = min(left_w - 60, cg_h - 180);
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(p_x0, p_y0, p_size, p_size);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(p_x0, p_y0, p_size, p_size, 0);

  // 1:1 Unity Line
  gfx_r = 0.40; gfx_g = 0.30; gfx_b = 0.50;
  gfx_line(p_x0, p_y0 + p_size, p_x0 + p_size, p_y0);

  // Compression Slope Curve
  r_val = slider16 == 0 ? 1.5 : (slider16 == 1 ? 2.0 : (slider16 == 2 ? 3.0 : 4.0));
  th_frac = (slider15 + 40.0) / 40.0;
  th_px = p_x0 + floor(th_frac * p_size);
  th_py = p_y0 + p_size - floor(th_frac * p_size);

  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_line(p_x0, p_y0 + p_size, th_px, th_py);
  end_py = th_py - floor(((p_size - (th_px - p_x0)) / r_val));
  gfx_line(th_px, th_py, p_x0 + p_size, end_py);

  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.40;
  gfx_circle(th_px, th_py, 4, 1);

  // Live Operating Point
  live_in_db = max(-40.0, min(0.0, vocal_rms));
  live_frac = (live_in_db + 40.0) / 40.0;
  live_x = p_x0 + floor(live_frac * p_size);
  live_y = live_in_db < slider15 ? (p_y0 + p_size - floor(live_frac * p_size)) : (th_py - floor(((live_x - th_px) / r_val)));
  gfx_r = 1.00; gfx_g = 0.30; gfx_b = 0.40;
  gfx_circle(live_x, live_y, 6, 1);
  gfx_r = 1.00; gfx_g = 1.00; gfx_b = 1.00;
  gfx_circle(live_x, live_y, 2, 1);

  // Ballistics Readout Bar
  sc_box_y = p_y0 + p_size + 20;
  gfx_setfont(3, "Consolas", 10.5, 'b'); gfx_r = 0.85; gfx_g = 0.75; gfx_b = 0.95;
  gfx_x = p_x0; gfx_y = sc_box_y;
  gfx_printf("Topology: %s", slider14 ? "Vintage Opto Leveler" : "Fairchild 670 Smooth Tube");
  gfx_x = p_x0; gfx_y = sc_box_y + 20;
  gfx_printf("Summed Vocal Peak: %.1f dB | Live GR: -%.2f dB", vocal_peak > 0 ? 20.0*log10(vocal_peak) : -120.0, vocal_glue_gr_db);

  // Right Box: Dual Topology & Parameter Controls
  rx = ws_x + 12 + left_w + 16;
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(rx, cg_y, right_w, cg_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(rx, cg_y, right_w, cg_h, 0);

  // Dual-Topology Selector Buttons (Fairchild vs Opto)
  btn_top_w = floor((right_w - 40) * 0.5);
  t1_x = rx + 16; t1_y = cg_y + 16;
  t1_hov = (mouse_x >= t1_x && mouse_x <= t1_x + btn_top_w && mouse_y >= t1_y && mouse_y <= t1_y + 36);
  gfx_r = (slider14 == 0) ? 0.20 : 0.06; gfx_g = (slider14 == 0) ? 0.08 : 0.03; gfx_b = (slider14 == 0) ? 0.28 : 0.09;
  gfx_rect(t1_x, t1_y, btn_top_w, 36);
  gfx_r = (slider14 == 0) ? 1.00 : 0.40; gfx_g = (slider14 == 0) ? 0.41 : 0.25; gfx_b = (slider14 == 0) ? 0.70 : 0.45;
  gfx_rect(t1_x, t1_y, btn_top_w, 36, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_x = t1_x + 14; gfx_y = t1_y + 10; gfx_drawstr("FAIRCHILD 670 TUBE");
  mouse_clicked && t1_hov ? (slider14 = 0; slider_automate(););

  t2_x = t1_x + btn_top_w + 8; t2_y = cg_y + 16;
  t2_hov = (mouse_x >= t2_x && mouse_x <= t2_x + btn_top_w && mouse_y >= t2_y && mouse_y <= t2_y + 36);
  gfx_r = (slider14 == 1) ? 0.20 : 0.06; gfx_g = (slider14 == 1) ? 0.08 : 0.03; gfx_b = (slider14 == 1) ? 0.28 : 0.09;
  gfx_rect(t2_x, t2_y, btn_top_w, 36);
  gfx_r = (slider14 == 1) ? 0.70 : 0.40; gfx_g = (slider14 == 1) ? 0.53 : 0.25; gfx_b = (slider14 == 1) ? 1.00 : 0.45;
  gfx_rect(t2_x, t2_y, btn_top_w, 36, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_x = t2_x + 14; gfx_y = t2_y + 10; gfx_drawstr("VINTAGE OPTO LEVELER");
  mouse_clicked && t2_hov ? (slider14 = 1; slider_automate(););

  // Big Gain Reduction Meter Bar
  gr_bar_y = t1_y + 48; gr_bar_h = 32; gr_bar_w = right_w - 32;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(rx + 16, gr_bar_y, gr_bar_w, gr_bar_h);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(rx + 16, gr_bar_y, gr_bar_w, gr_bar_h, 0);
  fill_w = floor(gr_bar_w * (min(16.0, vocal_glue_gr_db) / 16.0));
  fill_w > 0 ? (
    gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(rx + 16, gr_bar_y + 2, fill_w, gr_bar_h - 4);
  );
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = rx + 28; gfx_y = gr_bar_y + 8;
  gfx_printf("LIVE VOCAL GAIN REDUCTION: -%.2f dB", vocal_glue_gr_db);

  // 5 Sliders arranged ergonomically
  c_sl_w = floor((right_w - 48) / 3); c_sl_h = 65;
  sl_r1_y = gr_bar_y + 48;
  draw_param_slider(rx + 16 + 0 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "THRESHOLD", slider15, -36.0, 0.0, "%.1f dB", 15, 1.00, 0.41, 0.70);
  draw_param_slider(rx + 16 + 1 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "RATIO", slider16, 0, 3, "Mode %d", 16, 0.70, 0.53, 1.00);
  draw_param_slider(rx + 16 + 2 * (c_sl_w + 8), sl_r1_y, c_sl_w, c_sl_h, "ATTACK", slider17, 0.2, 50.0, "%.1f ms", 17, 1.00, 0.41, 0.70);

  sl_r2_y = sl_r1_y + c_sl_h + 12;
  draw_param_slider(rx + 16 + 0 * (c_sl_w + 8), sl_r2_y, c_sl_w, c_sl_h, "RELEASE", slider18, 0, 4, "Mode %d", 18, 0.70, 0.53, 1.00);
  draw_param_slider(rx + 16 + 1 * (c_sl_w + 8), sl_r2_y, c_sl_w, c_sl_h, "DRY/WET MIX", slider19, 0, 100, "%d %%", 19, 1.00, 0.85, 0.40);
  draw_param_slider(rx + 16 + 2 * (c_sl_w + 8), sl_r2_y, c_sl_w, c_sl_h, "TUBE WARMTH", slider20, 0.0, 10.0, "+%.1f dB", 20, 1.00, 0.41, 0.70);

  // Bottom Ballistics Forensic Notes Box
  fn_y = sl_r2_y + c_sl_h + 16; fn_h = cg_h - (fn_y - cg_y) - 16;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(rx + 16, fn_y, right_w - 32, fn_h);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(rx + 16, fn_y, right_w - 32, fn_h, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = rx + 28; gfx_y = fn_y + 12; gfx_drawstr("MASTER VOCAL GLUE SPECIFICATION:");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.85; gfx_g = 0.80; gfx_b = 0.95;
  gfx_x = rx + 28; gfx_y = fn_y + 34;
  gfx_drawstr("• Fairchild 670 Smooth Tube: Variable-mu valve compression that wraps lead vocals and background stacks into a unified wall.");
  gfx_x = rx + 28; gfx_y = fn_y + 54;
  gfx_drawstr("• Vintage Opto Leveler: Two-stage optical release cell offering fast initial recovery followed by a slow, transparent decay tail.");
  gfx_x = rx + 28; gfx_y = fn_y + 74;
  gfx_drawstr("• Tube Warmth Stage: Injects pure even-order tube harmonics, fattening thin consonants and anchoring aggressive metalcore screams.");
);

// =============================================================================
// TAB 3: DE-ESSER & TUBE WARMTH (SPECTRAL SPLIT + CLAMP SENTRY + TUBE DRIVE)
// =============================================================================
slider1 == 3 ? (
  ds_y = ws_y + 12; ds_w = ws_w - 24; ds_h = ws_h - 24;
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 12, ds_y, ds_w, ds_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 12, ds_y, ds_w, ds_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 28; gfx_y = ds_y + 14; gfx_drawstr("MASTER VOCAL SIBILANCE CLAMP & TUBE SATURATION ENGINE");

  // Top Section: Spectral Sibilance Split Plot
  top_h = 220;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(ws_x + 24, ds_y + 44, ds_w - 48, top_h);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(ws_x + 24, ds_y + 44, ds_w - 48, top_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 36; gfx_y = ds_y + 54; gfx_drawstr("HIGH-FREQUENCY SIBILANCE DETECTION & CLAMPING SPECTRUM");

  p_cx0 = ws_x + 36; p_cy0 = ds_y + 85; p_cw = ds_w - 72; p_ch = top_h - 55;
  gfx_r = 0.15; gfx_g = 0.08; gfx_b = 0.22;
  gfx_line(p_cx0, p_cy0 + p_ch * 0.5, p_cx0 + p_cw, p_cy0 + p_ch * 0.5);

  // Sibilance frequency split point
  split_f = (slider7 - 4000.0) / 6000.0;
  split_x = p_cx0 + floor(0.70 * p_cw + split_f * 0.20 * p_cw);
  // Shaded Clamp Zone
  gfx_r = 0.22; gfx_g = 0.08; gfx_b = 0.16;
  gfx_rect(split_x, p_cy0, (p_cx0 + p_cw) - split_x, p_ch);
  gfx_r = 1.00; gfx_g = 0.30; gfx_b = 0.40;
  gfx_line(split_x, p_cy0, split_x, p_cy0 + p_ch);

  gfx_setfont(3, "Consolas", 10.5, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = split_x + 10; gfx_y = p_cy0 + 20; gfx_printf("SIBILANCE CLAMP BAND: > %d Hz", slider7);
  gfx_x = split_x + 10; gfx_y = p_cy0 + 40; gfx_printf("ACTIVE REDUCTION: -%.2f dB", ds_reduction_db);

  // Middle Section: 4 De-Esser Sliders
  c_sl_w = floor((ds_w - 48 - 24) / 4); c_sl_h = 65;
  sl_y = ds_y + 276;
  draw_param_slider(ws_x + 24 + 0 * (c_sl_w + 8), sl_y, c_sl_w, c_sl_h, "CLAMP THRESH", slider6, -36.0, 0.0, "%.1f dB", 6, 1.00, 0.41, 0.70);
  draw_param_slider(ws_x + 24 + 1 * (c_sl_w + 8), sl_y, c_sl_w, c_sl_h, "FREQ SWEEP", slider7, 4000, 10000, "%d Hz", 7, 0.70, 0.53, 1.00);
  draw_param_slider(ws_x + 24 + 2 * (c_sl_w + 8), sl_y, c_sl_w, c_sl_h, "MAX RANGE", slider8, -12.0, 0.0, "%.1f dB", 8, 1.00, 0.41, 0.70);
  draw_param_slider(ws_x + 24 + 3 * (c_sl_w + 8), sl_y, c_sl_w, c_sl_h, "TUBE DRIVE", slider20, 0.0, 10.0, "+%.1f dB", 20, 1.00, 0.85, 0.40);

  // De-Esser Delta Solo Button
  ds_btn_x = ws_x + 24; ds_btn_y = sl_y + 76; ds_btn_w = 260; ds_btn_h = 32;
  ds_btn_hov = (mouse_x >= ds_btn_x && mouse_x <= ds_btn_x + ds_btn_w && mouse_y >= ds_btn_y && mouse_y <= ds_btn_y + ds_btn_h);
  gfx_r = slider9 ? 0.28 : 0.08; gfx_g = slider9 ? 0.08 : 0.04; gfx_b = slider9 ? 0.12 : 0.14;
  gfx_rect(ds_btn_x, ds_btn_y, ds_btn_w, ds_btn_h);
  gfx_r = slider9 ? 1.00 : 0.50; gfx_g = slider9 ? 0.30 : 0.35; gfx_b = slider9 ? 0.40 : 0.60;
  gfx_rect(ds_btn_x, ds_btn_y, ds_btn_w, ds_btn_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_x = ds_btn_x + 14; gfx_y = ds_btn_y + 9;
  slider9 ? gfx_drawstr("DELTA: AUDITION SIBILANCE") : gfx_drawstr("NORMAL: DE-ESSER ACTIVE");
  mouse_clicked && ds_btn_hov ? (slider9 = !slider9; slider_automate(););

  // Bottom Technical Plaque
  t_pl_y = ds_btn_y + 42; t_pl_h = ds_h - (t_pl_y - ds_y) - 16;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(ws_x + 24, t_pl_y, ds_w - 48, t_pl_h);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(ws_x + 24, t_pl_y, ds_w - 48, t_pl_h, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 36; gfx_y = t_pl_y + 12; gfx_drawstr("SIBILANCE SUPPRESSION & TUBE HARMONIC ARCHITECTURE:");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.85; gfx_g = 0.80; gfx_b = 0.95;
  gfx_x = ws_x + 36; gfx_y = t_pl_y + 32;
  gfx_drawstr("• Summed High-Frequency Limiter: Clamps harsh vocal sibilants ('s', 't', 'sh') across the entire master vocal group in one transparent pass.");
  gfx_x = ws_x + 36; gfx_y = t_pl_y + 50;
  gfx_drawstr("• Drum Cymbal Bleed Shield: Suppresses spiky overhead cymbal spill picked up by aggressive lead vocal microphones.");
  gfx_x = ws_x + 36; gfx_y = t_pl_y + 68;
  gfx_drawstr("• Tube Saturation Stage: Reconstructs lost high-frequency acoustic body with musical 2nd order harmonics without adding brittle glare.");
);

// =============================================================================
// TAB 4: SPATIAL (LEAD CENTER LOCK + STEREO REVERB SPREAD)
// =============================================================================
slider1 == 4 ? (
  sp_y = ws_y + 12; sp_w = ws_w - 24; sp_h = ws_h - 24;
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 12, sp_y, sp_w, sp_h);
  gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00; gfx_rect(ws_x + 12, sp_y, sp_w, sp_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = ws_x + 28; gfx_y = sp_y + 14; gfx_drawstr("MASTER VOCAL SPATIALIZER // LEAD MONO LOCK & STEREO REVERB HALO");

  top_h = 240;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(ws_x + 24, sp_y + 44, sp_w - 48, top_h);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(ws_x + 24, sp_y + 44, sp_w - 48, top_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 36; gfx_y = sp_y + 54; gfx_drawstr("POLAR VOCAL SPREAD RADAR & LEAD MONO ANCHOR");

  r_cx = ws_x + floor(sp_w * 0.5); r_cy = sp_y + 44 + floor(top_h * 0.55);
  gfx_r = 0.22; gfx_g = 0.12; gfx_b = 0.30;
  gfx_circle(r_cx, r_cy, 65, 0);
  gfx_circle(r_cx, r_cy, 35, 0);
  gfx_line(r_cx - 65, r_cy, r_cx + 65, r_cy);
  gfx_line(r_cx, r_cy - 65, r_cx, r_cy + 65);

  // Center mono anchor icon
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_circle(r_cx, r_cy, 8, 1);
  gfx_setfont(3, "Consolas", 10.0, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;
  gfx_x = r_cx - 30; gfx_y = r_cy + 15; gfx_drawstr("LEAD MONO CORE");

  // Bottom Section: Sliders
  draw_param_slider(ws_x + 24, sp_y + 296, sp_w - 48, 65, "VOCAL SPATIAL STEREO WIDTH", slider21, 0.80, 1.40, "%.2f x", 21, 0.70, 0.53, 1.00);

  // Technical explanation plaque
  t_pl_y = sp_y + 372; t_pl_h = sp_h - 386;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(ws_x + 24, t_pl_y, sp_w - 48, t_pl_h);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(ws_x + 24, t_pl_y, sp_w - 48, t_pl_h, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 0.70; gfx_g = 0.53; gfx_b = 1.00;
  gfx_x = ws_x + 36; gfx_y = t_pl_y + 12; gfx_drawstr("VOCAL SPATIAL COHESION PRINCIPLES:");
  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.85; gfx_g = 0.80; gfx_b = 0.95;
  gfx_x = ws_x + 36; gfx_y = t_pl_y + 34;
  gfx_drawstr("• Lead Vocal Mono Lock: Ensures the primary lead vocal remains 100% focused dead-center, maximizing intelligibility on phone speakers.");
  gfx_x = ws_x + 36; gfx_y = t_pl_y + 54;
  gfx_drawstr("• Stereo Reverb / Doubles Halo: Widens backing vocal stacks, octave doubles, and stereo reverb returns out to the sides without washing out the lead.");
);

// =============================================================================
// TAB 5: PRESENCE (DYNAMIC PRESENCE SENTRY & CORRIDOR REQUEST)
// =============================================================================
slider1 == 5 ? (
  pr_y = ws_y + 12; pr_w = ws_w - 24; pr_h = ws_h - 24;
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 12, pr_y, pr_w, pr_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 12, pr_y, pr_w, pr_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 28; gfx_y = pr_y + 14; gfx_drawstr("DYNAMIC PRESENCE SENTRY // ZERO-CABLE MUSIC CORRIDOR REQUEST");

  // Top Section: Live Vocal vs Music Balance Radar
  top_h = 220;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(ws_x + 24, pr_y + 44, pr_w - 48, top_h);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(ws_x + 24, pr_y + 44, pr_w - 48, top_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 36; gfx_y = pr_y + 54; gfx_drawstr("LIVE VOCAL-TO-MUSIC DYNAMIC BALANCE COMPARISON");

  // Dual Energy Meter Bars (Music vs Vocal)
  bar_y0 = pr_y + 90; bar_h0 = 28; bar_w0 = pr_w - 96;
  // Music RMS Bar
  gfx_r = 0.018; gfx_g = 0.024; gfx_b = 0.034; gfx_rect(ws_x + 48, bar_y0, bar_w0, bar_h0);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 48, bar_y0, bar_w0, bar_h0, 0);
  m_frac = max(0.0, min(1.0, (ib_inst_rms + 60.0) / 60.0));
  gfx_rect(ws_x + 48, bar_y0 + 2, floor(m_frac * bar_w0), bar_h0 - 4);
  gfx_setfont(3, "Consolas", 10.5, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = ws_x + 58; gfx_y = bar_y0 + 7; gfx_printf("INSTRUMENTAL MUSIC RMS (gmem[1402]): %.1f dB", ib_inst_rms);

  // Vocal RMS Bar
  bar_y1 = bar_y0 + 38;
  gfx_r = 0.024; gfx_g = 0.010; gfx_b = 0.032; gfx_rect(ws_x + 48, bar_y1, bar_w0, bar_h0);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 48, bar_y1, bar_w0, bar_h0, 0);
  v_frac = max(0.0, min(1.0, (vocal_rms + 60.0) / 60.0));
  gfx_rect(ws_x + 48, bar_y1 + 2, floor(v_frac * bar_w0), bar_h0 - 4);
  gfx_setfont(3, "Consolas", 10.5, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = ws_x + 58; gfx_y = bar_y1 + 7; gfx_printf("SUMMED VOCAL RMS (LOCAL): %.1f dB", vocal_rms);

  // Middle Section: Sensitivity Slider & Corridor Request Toggle
  draw_param_slider(ws_x + 24, pr_y + 276, pr_w - 48, 65, "PRESENCE SENTRY SENSITIVITY", slider26, 0.0, 3.0, "%.1f dB", 26, 1.00, 0.41, 0.70);

  crm_x = ws_x + 24; crm_y = pr_y + 350; crm_w = 340; crm_h = 32;
  crm_hov = (mouse_x >= crm_x && mouse_x <= crm_x + crm_w && mouse_y >= crm_y && mouse_y <= crm_y + crm_h);
  gfx_r = slider27 ? 0.20 : 0.08; gfx_g = slider27 ? 0.08 : 0.04; gfx_b = slider27 ? 0.28 : 0.12;
  gfx_rect(crm_x, crm_y, crm_w, crm_h);
  gfx_r = slider27 ? 1.00 : 0.40; gfx_g = slider27 ? 0.41 : 0.25; gfx_b = slider27 ? 0.70 : 0.45;
  gfx_rect(crm_x, crm_y, crm_w, crm_h, 0);
  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_x = crm_x + 14; gfx_y = crm_y + 9;
  slider27 ? gfx_drawstr("AUTONOMOUS CORRIDOR REQUEST: ACTIVE") : gfx_drawstr("CORRIDOR REQUEST: STANDBY");
  mouse_clicked && crm_hov ? (slider27 = !slider27; slider_automate(););

  // Bottom Telemetry Log Box
  pr_box_y = pr_y + 392; pr_box_h = pr_h - 406;
  gfx_r = 0.012; gfx_g = 0.006; gfx_b = 0.018; gfx_rect(ws_x + 24, pr_box_y, pr_w - 48, pr_box_h);
  gfx_r = 0.35; gfx_g = 0.20; gfx_b = 0.45; gfx_rect(ws_x + 24, pr_box_y, pr_w - 48, pr_box_h, 0);

  gfx_setfont(2, "Orbitron", 10.5, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 36; gfx_y = pr_box_y + 12;
  gfx_printf("PRESENCE SENTRY TELEMETRY: Corridor Request Sent = -%.2f dB to gmem[1456]", gmem[1456]);

  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.85; gfx_g = 0.80; gfx_b = 0.95;
  gfx_x = ws_x + 36; gfx_y = pr_box_y + 34;
  gfx_printf("Interlock Connection: %s | Music RMS = %.1f dB | Vocal RMS = %.1f dB", ib_alive ? "SYNCHRONIZED (ONLINE)" : "STANDBY (OFFLINE)", ib_inst_rms, vocal_rms);
  gfx_x = ws_x + 36; gfx_y = pr_box_y + 54;
  gfx_drawstr("The sentry compares live Vocal RMS against Instrumental Bus RMS in real time. If the vocal level is in danger of being masked,");
  gfx_x = ws_x + 36; gfx_y = pr_box_y + 72;
  gfx_drawstr("it signals the Instrumental Bus Alchemist to dynamically carve a 2.2kHz center pocket, maintaining pristine vocal clarity.");
);

// =============================================================================
// TAB 6: PRODUCER SUMMING MATRIX (25 CLICKABLE TILES + FORENSIC PLAQUE)
// =============================================================================
slider1 == 6 ? (
  mat_y = ws_y + 12;
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_setfont(1, "Orbitron", 13.5, 'b');
  gfx_x = ws_x + 20; gfx_y = mat_y;
  gfx_drawstr("MASTER VOCAL PRODUCER MATRIX // 25 REFERENCE-CALIBRATED BENCHMARKS");

  pi = 0; pill_w = floor((ws_w - 40 - 36) / 7); pill_h = 36;
  loop(25,
    p_row = floor(pi / 7); p_col = pi % 7;
    px = ws_x + 16 + p_col * (pill_w + 6);
    py = mat_y + 30 + p_row * (pill_h + 6);
    is_sel = (slider2 == pi);
    p_hov = (mouse_x >= px && mouse_x <= px + pill_w && mouse_y >= py && mouse_y <= py + pill_h);

    gfx_r = is_sel ? 0.28 : (p_hov ? 0.14 : 0.04);
    gfx_g = is_sel ? 0.10 : (p_hov ? 0.06 : 0.02);
    gfx_b = is_sel ? 0.22 : (p_hov ? 0.14 : 0.05);
    gfx_rect(px, py, pill_w, pill_h);

    gfx_r = is_sel ? 1.00 : (p_hov ? 0.60 : 0.30);
    gfx_g = is_sel ? 0.41 : (p_hov ? 0.30 : 0.15);
    gfx_b = is_sel ? 0.70 : (p_hov ? 0.50 : 0.35);
    gfx_rect(px, py, pill_w, pill_h, 0);

    gfx_setfont(3, "Consolas", 10.5, 'b');
    is_sel ? (gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;) : (gfx_r = 0.85; gfx_g = 0.80; gfx_b = 0.95;);
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
  gfx_r = 0.018; gfx_g = 0.010; gfx_b = 0.026; gfx_rect(ws_x + 16, pl_y, pl_w, pl_h);
  gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70; gfx_rect(ws_x + 16, pl_y, pl_w, pl_h, 0);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.00; gfx_g = 0.41; gfx_b = 0.70;
  gfx_x = ws_x + 32; gfx_y = pl_y + 14;
  gfx_printf("SELECTED BENCHMARK: %02d - %s", slider2, get_producer_full_title(slider2));

  gfx_setfont(3, "Consolas", 11.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = ws_x + 32; gfx_y = pl_y + 40;
  gfx_printf("CALIBRATION: Trim %+.1fdB | De-Esser %.1fdB @ %dHz | Bax Air %+.1fdB | Tube Drive %+.1fdB | Width %.2fx",
    slider4, slider6, slider7, slider12, slider20, slider21);

  gfx_setfont(3, "Consolas", 11.0); gfx_r = 0.80; gfx_g = 0.75; gfx_b = 0.90;
  gfx_x = ws_x + 32; gfx_y = pl_y + 68;
  gfx_drawstr("Full master vocal forensic acoustic profile matching reference benchmarks. Recalls authentic Fairchild variable-mu glue,");
  gfx_x = ws_x + 32; gfx_y = pl_y + 88;
  gfx_drawstr("tube saturation warmth, precision Baxandall tone curves, and high-frequency sibilance suppression.");
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
'''

print(f"Generated Vocal Bus Code: {len(VOCAL_BUS_CODE)} bytes")

vocal_target = r"c:\Dev\DameiSuite\effects\Damei_VocalBus.jsfx"
with open(vocal_target, "w", encoding="utf-8") as f:
    f.write(VOCAL_BUS_CODE)
print(f"Successfully wrote {vocal_target}")
