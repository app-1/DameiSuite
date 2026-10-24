# Python script to build the upgraded Damei_VocalBus.jsfx
import os, shutil

target_path = r"c:\Dev\DameiSuite\effects\Damei_VocalBus.jsfx"
reaper_path = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_VocalBus.jsfx"

code = r"""desc:Damei Vocal Empress (Imperial Sceptre & Master Vocal Sum)
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

options:no_meter
options:gmem=DameiMixMetering
options:maxmem=65536

@init
ext_noinit = 1.0;
M_PI = 3.14159265358979323846;

// Memory partitioning
ab_mem_a = 2000;
ab_mem_b = 2050;

// Filter state memories (Fully isolated Left & Right delay lines)
bax_w_x1_l = 0; bax_w_x2_l = 0; bax_w_y1_l = 0; bax_w_y2_l = 0;
bax_w_x1_r = 0; bax_w_x2_r = 0; bax_w_y1_r = 0; bax_w_y2_r = 0;

bax_p_x1_l = 0; bax_p_x2_l = 0; bax_p_y1_l = 0; bax_p_y2_l = 0;
bax_p_x1_r = 0; bax_p_x2_r = 0; bax_p_y1_r = 0; bax_p_y2_r = 0;

bax_a_x1_l = 0; bax_a_x2_l = 0; bax_a_y1_l = 0; bax_a_y2_l = 0;
bax_a_x1_r = 0; bax_a_x2_r = 0; bax_a_y1_r = 0; bax_a_y2_r = 0;

// De-Esser Bandpass Biquad Filter memories
de_bp_x1_l = 0; de_bp_x2_l = 0; de_bp_y1_l = 0; de_bp_y2_l = 0;
de_bp_x1_r = 0; de_bp_x2_r = 0; de_bp_y1_r = 0; de_bp_y2_r = 0;
de_env_smooth = 0.0;
de_gr_db = 0.0;

vu_rms_smooth = 0.0;
vocal_peak = 0.0;
vocal_rms = 0.0;
vocal_gr_db = 0.0;
sifam_vocal_vu = 0.0;
sifam_vocal_gr = 0.0;

rms_acc_l = 0.0;
rms_acc_r = 0.0;
rms_cnt = 0;

// Register Vocal Empress Telemetry (1450..1499)
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
  "24: RENNER"
);

function get_producer_full_title(idx) (
  idx == 0  ? "Default Unity Baseline (1:1 Transparent Pass)" :
  idx == 1  ? "Lance Prenc (Alpha Wolf / Polaris - Hyper-Intelligible Aggression)" :
  idx == 2  ? "Scott Seigel (DIESECT - Crushing Low-Mid Density)" :
  idx == 3  ? "Jonathan Dolese (Mirrorcell / Cane Hill - Thick Tube Warmth)" :
  idx == 4  ? "Buster Odeholm (thrown / Northlane - Industrial Clamp & Cut)" :
  idx == 5  ? "Lewis Johns (Love Is Noise / blanket - Ethereal Opto Space)" :
  idx == 6  ? "Kel Pinchin (Currents / Invent Animate - Pristine Modern Presence)" :
  idx == 7  ? "Dan Lancaster & Jason Perry (Don Broco - Stadium Vocal Energy)" :
  idx == 8  ? "Erik Bickerstaffe (Static Dress - Raw Analog Grit & Spit)" :
  idx == 9  ? "Sam Guaiana (Silverstein / TDWP - Radio Air & Punch)" :
  idx == 10 ? "Zach Tuch (Heavenward / Hundredth - Vintage Tube Bloom)" :
  idx == 11 ? "Forrester Savell (Karnivool / Twelve Foot Ninja - Hi-Fi Silk Air)" :
  idx == 12 ? "Leon Schmidt (SUNBORN - Nebula - Ambient Spatial Wash)" :
  idx == 13 ? "Ermin Hamidovic (Systematic Reference - Benchmark Precision)" :
  idx == 14 ? "Will Putney (Fit For An Autopsy / Knocked Loose - Forward Throat Bite)" :
  idx == 15 ? "George Lever (Sleep Token / Loathe - Dynamic Ethereal Depth)" :
  idx == 16 ? "Sam Bassal (Thornhill - nerv - Modern Electro-Metal Polish)" :
  idx == 17 ? "Henrik Udd (Architects / BMTH - Wall of Heavy Vocals)" :
  idx == 18 ? "Dan Braunstein (Spiritbox / Dayseeker - Hyper-Modern Air & Sheen)" :
  idx == 19 ? "Zakk Cervini & Erik Ron (Bad Omens - Commercial Radio Polish)" :
  idx == 20 ? "Jens Bogren (Fascination Street - European Grandeur & Depth)" :
  idx == 21 ? "Adam Nolly Getgood (Periphery / GGD - Surgical Air & Clarity)" :
  idx == 22 ? "Acle Kahney (TesseracT - King - Hi-Fi Pristine Space)" :
  idx == 23 ? "Adam Cichocki (heaving. / Timber - Raw Alt-Metal Crush)" :
  "Manuel Renner (SENNA / Uberlarm - Modern European Precision)"
);

function update_vocal_filters() local(w0, alpha, A, beta, cos_w0, sin_w0) (
  // 1. Baxandall 100Hz Warmth Low Shelf
  A = exp(slider10 * 0.0575646273);
  w0 = 2.0 * M_PI * 100.0 / srate;
  cos_w0 = cos(w0); sin_w0 = sin(w0);
  alpha = sin_w0 / (2.0 * 0.7071);
  beta = 2.0 * sqrt(A) * alpha;
  bax_w_b0 = A * ((A + 1.0) - (A - 1.0) * cos_w0 + beta);
  bax_w_b1 = 2.0 * A * ((A - 1.0) - (A + 1.0) * cos_w0);
  bax_w_b2 = A * ((A + 1.0) - (A - 1.0) * cos_w0 - beta);
  bax_w_a0 = (A + 1.0) + (A - 1.0) * cos_w0 + beta;
  bax_w_a1 = -2.0 * ((A - 1.0) + (A + 1.0) * cos_w0);
  bax_w_a2 = (A + 1.0) + (A - 1.0) * cos_w0 - beta;

  // 2. Baxandall 3.5kHz Presence Bell
  A = exp(slider11 * 0.0575646273);
  w0 = 2.0 * M_PI * 3500.0 / srate;
  alpha = sin(w0) / (2.0 * 1.1);
  bax_p_b0 = 1.0 + alpha * A;
  bax_p_b1 = -2.0 * cos(w0);
  bax_p_b2 = 1.0 - alpha * A;
  bax_p_a0 = 1.0 + alpha / A;
  bax_p_a1 = -2.0 * cos(w0);
  bax_p_a2 = 1.0 - alpha / A;

  // 3. Baxandall 12kHz Silk Air High Shelf
  A = exp(slider12 * 0.0575646273);
  w0 = 2.0 * M_PI * 12000.0 / srate;
  cos_w0 = cos(w0); sin_w0 = sin(w0);
  alpha = sin_w0 / (2.0 * 0.7071);
  beta = 2.0 * sqrt(A) * alpha;
  bax_a_b0 = A * ((A + 1.0) + (A - 1.0) * cos_w0 + beta);
  bax_a_b1 = -2.0 * A * ((A - 1.0) + (A + 1.0) * cos_w0);
  bax_a_b2 = A * ((A + 1.0) + (A - 1.0) * cos_w0 - beta);
  bax_a_a0 = (A + 1.0) - (A - 1.0) * cos_w0 + beta;
  bax_a_a1 = 2.0 * ((A - 1.0) - (A + 1.0) * cos_w0);
  bax_a_a2 = (A + 1.0) - (A - 1.0) * cos_w0 - beta;

  // 4. De-Esser Bandpass Biquad Detector
  de_fc = clamp(slider7, 4000.0, 10000.0);
  w0 = 2.0 * M_PI * de_fc / srate;
  alpha = sin(w0) / (2.0 * 1.8);
  de_b0 = alpha;
  de_b1 = 0.0;
  de_b2 = -alpha;
  de_a0 = 1.0 + alpha;
  de_a1 = -2.0 * cos(w0);
  de_a2 = 1.0 - alpha;
);



function apply_producer_preset(idx) (
  idx == 0 ? ( // Unity Baseline (1:1 Transparent Pass)
    slider3 = 0.0; slider4 = 0.0; slider5 = 1;
    slider6 = -18.0; slider7 = 6800; slider8 = -6.0; slider9 = 0;
    slider10 = 0.0; slider11 = 0.0; slider12 = 0.0;
    slider13 = 1; slider14 = 0; slider15 = 0.0; slider16 = 1;
    slider17 = 15.0; slider18 = 2; slider19 = 100;
    slider20 = 0.0; slider21 = 1.00;
  ) : idx == 1 ? ( // Lance Prenc
    slider3 = 0.0; slider4 = -2.5; slider5 = 1;
    slider6 = -20.0; slider7 = 6500; slider8 = -8.0; slider9 = 0;
    slider10 = 1.0; slider11 = 3.0; slider12 = 3.5;
    slider13 = 1; slider14 = 0; slider15 = -6.0; slider16 = 2;
    slider17 = 10.0; slider18 = 1; slider19 = 100;
    slider20 = 3.5; slider21 = 1.05;
  ) : idx == 2 ? ( // Scott Seigel
    slider3 = 0.0; slider4 = -2.0; slider5 = 1;
    slider6 = -18.0; slider7 = 6200; slider8 = -6.5; slider9 = 0;
    slider10 = 2.0; slider11 = 1.5; slider12 = 2.0;
    slider13 = 1; slider14 = 1; slider15 = -5.0; slider16 = 1;
    slider17 = 20.0; slider18 = 2; slider19 = 100;
    slider20 = 4.0; slider21 = 1.02;
  ) : idx == 3 ? ( // Jonathan Dolese
    slider3 = 0.0; slider4 = -1.8; slider5 = 1;
    slider6 = -17.0; slider7 = 7000; slider8 = -6.0; slider9 = 0;
    slider10 = 1.8; slider11 = 2.0; slider12 = 2.5;
    slider13 = 1; slider14 = 0; slider15 = -4.5; slider16 = 1;
    slider17 = 15.0; slider18 = 2; slider19 = 100;
    slider20 = 4.5; slider21 = 1.04;
  ) : idx == 4 ? ( // Buster Odeholm
    slider3 = 0.0; slider4 = -3.0; slider5 = 1;
    slider6 = -22.0; slider7 = 6000; slider8 = -9.0; slider9 = 0;
    slider10 = 0.5; slider11 = 3.5; slider12 = 4.0;
    slider13 = 1; slider14 = 0; slider15 = -8.0; slider16 = 3;
    slider17 = 5.0; slider18 = 0; slider19 = 100;
    slider20 = 5.0; slider21 = 1.06;
  ) : idx == 5 ? ( // Lewis Johns
    slider3 = 0.0; slider4 = -1.5; slider5 = 1;
    slider6 = -16.0; slider7 = 7200; slider8 = -5.0; slider9 = 0;
    slider10 = 1.5; slider11 = 1.2; slider12 = 3.0;
    slider13 = 1; slider14 = 1; slider15 = -3.5; slider16 = 0;
    slider17 = 25.0; slider18 = 3; slider19 = 100;
    slider20 = 2.0; slider21 = 1.12;
  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target) - Currents / Invent Animate
    slider3 = 0.0; slider4 = -2.5; slider5 = 1;
    slider6 = -19.0; slider7 = 6800; slider8 = -7.0; slider9 = 0;
    slider10 = 1.2; slider11 = 2.8; slider12 = 3.8;
    slider13 = 1; slider14 = 0; slider15 = -5.5; slider16 = 1;
    slider17 = 12.0; slider18 = 1; slider19 = 100;
    slider20 = 3.2; slider21 = 1.08;
  ) : idx == 7 ? ( // Dan Lancaster & Jason Perry
    slider3 = 0.0; slider4 = -2.8; slider5 = 1;
    slider6 = -18.0; slider7 = 6600; slider8 = -7.5; slider9 = 0;
    slider10 = 1.5; slider11 = 3.2; slider12 = 3.5;
    slider13 = 1; slider14 = 0; slider15 = -6.0; slider16 = 2;
    slider17 = 10.0; slider18 = 2; slider19 = 100;
    slider20 = 3.8; slider21 = 1.10;
  ) : idx == 8 ? ( // Erik Bickerstaffe
    slider3 = 0.0; slider4 = -2.2; slider5 = 1;
    slider6 = -17.0; slider7 = 6400; slider8 = -6.0; slider9 = 0;
    slider10 = 2.0; slider11 = 2.5; slider12 = 2.0;
    slider13 = 1; slider14 = 1; slider15 = -5.0; slider16 = 2;
    slider17 = 15.0; slider18 = 0; slider19 = 100;
    slider20 = 5.2; slider21 = 1.02;
  ) : idx == 9 ? ( // Sam Guaiana
    slider3 = 0.0; slider4 = -2.4; slider5 = 1;
    slider6 = -18.5; slider7 = 6700; slider8 = -7.0; slider9 = 0;
    slider10 = 1.0; slider11 = 2.6; slider12 = 3.2;
    slider13 = 1; slider14 = 0; slider15 = -5.0; slider16 = 1;
    slider17 = 12.0; slider18 = 2; slider19 = 100;
    slider20 = 3.0; slider21 = 1.06;
  ) : idx == 10 ? ( // Zach Tuch
    slider3 = 0.0; slider4 = -1.8; slider5 = 1;
    slider6 = -16.0; slider7 = 7000; slider8 = -5.5; slider9 = 0;
    slider10 = 1.8; slider11 = 1.5; slider12 = 2.5;
    slider13 = 1; slider14 = 1; slider15 = -4.0; slider16 = 1;
    slider17 = 20.0; slider18 = 3; slider19 = 100;
    slider20 = 3.8; slider21 = 1.08;
  ) : idx == 11 ? ( // Forrester Savell
    slider3 = 0.0; slider4 = -1.6; slider5 = 1;
    slider6 = -17.5; slider7 = 7200; slider8 = -6.0; slider9 = 0;
    slider10 = 0.8; slider11 = 2.0; slider12 = 3.5;
    slider13 = 1; slider14 = 0; slider15 = -4.0; slider16 = 1;
    slider17 = 20.0; slider18 = 2; slider19 = 100;
    slider20 = 2.2; slider21 = 1.10;
  ) : idx == 12 ? ( // Leon Schmidt
    slider3 = 0.0; slider4 = -2.0; slider5 = 1;
    slider6 = -16.5; slider7 = 6800; slider8 = -5.5; slider9 = 0;
    slider10 = 1.2; slider11 = 1.8; slider12 = 3.0;
    slider13 = 1; slider14 = 1; slider15 = -4.0; slider16 = 0;
    slider17 = 25.0; slider18 = 3; slider19 = 100;
    slider20 = 2.8; slider21 = 1.15;
  ) : idx == 13 ? ( // Ermin Hamidovic
    slider3 = 0.0; slider4 = -2.2; slider5 = 1;
    slider6 = -18.0; slider7 = 6800; slider8 = -6.0; slider9 = 0;
    slider10 = 0.5; slider11 = 1.5; slider12 = 2.2;
    slider13 = 1; slider14 = 0; slider15 = -4.5; slider16 = 1;
    slider17 = 15.0; slider18 = 2; slider19 = 100;
    slider20 = 1.5; slider21 = 1.04;
  ) : idx == 14 ? ( // Will Putney
    slider3 = 0.0; slider4 = -2.8; slider5 = 1;
    slider6 = -19.5; slider7 = 6400; slider8 = -8.0; slider9 = 0;
    slider10 = 2.2; slider11 = 3.0; slider12 = 2.0;
    slider13 = 1; slider14 = 0; slider15 = -7.0; slider16 = 2;
    slider17 = 8.0; slider18 = 1; slider19 = 100;
    slider20 = 4.8; slider21 = 1.04;
  ) : idx == 15 ? ( // George Lever
    slider3 = 0.0; slider4 = -1.8; slider5 = 1;
    slider6 = -16.0; slider7 = 7200; slider8 = -5.0; slider9 = 0;
    slider10 = 1.5; slider11 = 1.6; slider12 = 3.2;
    slider13 = 1; slider14 = 1; slider15 = -4.0; slider16 = 0;
    slider17 = 25.0; slider18 = 3; slider19 = 100;
    slider20 = 2.5; slider21 = 1.14;
  ) : idx == 16 ? ( // Sam Bassal
    slider3 = 0.0; slider4 = -2.5; slider5 = 1;
    slider6 = -19.0; slider7 = 6600; slider8 = -7.0; slider9 = 0;
    slider10 = 1.5; slider11 = 2.8; slider12 = 3.0;
    slider13 = 1; slider14 = 0; slider15 = -6.0; slider16 = 2;
    slider17 = 10.0; slider18 = 2; slider19 = 100;
    slider20 = 3.8; slider21 = 1.08;
  ) : idx == 17 ? ( // Henrik Udd
    slider3 = 0.0; slider4 = -2.6; slider5 = 1;
    slider6 = -18.5; slider7 = 6500; slider8 = -7.0; slider9 = 0;
    slider10 = 1.8; slider11 = 2.8; slider12 = 3.2;
    slider13 = 1; slider14 = 0; slider15 = -5.5; slider16 = 1;
    slider17 = 15.0; slider18 = 2; slider19 = 100;
    slider20 = 3.5; slider21 = 1.10;
  ) : idx == 18 ? ( // Dan Braunstein
    slider3 = 0.0; slider4 = -2.8; slider5 = 1;
    slider6 = -19.0; slider7 = 6800; slider8 = -7.5; slider9 = 0;
    slider10 = 1.0; slider11 = 3.0; slider12 = 4.0;
    slider13 = 1; slider14 = 0; slider15 = -5.5; slider16 = 1;
    slider17 = 12.0; slider18 = 2; slider19 = 100;
    slider20 = 3.0; slider21 = 1.12;
  ) : idx == 19 ? ( // Zakk Cervini & Erik Ron
    slider3 = 0.0; slider4 = -2.8; slider5 = 1;
    slider6 = -19.5; slider7 = 6600; slider8 = -8.0; slider9 = 0;
    slider10 = 1.2; slider11 = 3.2; slider12 = 3.5;
    slider13 = 1; slider14 = 0; slider15 = -6.5; slider16 = 2;
    slider17 = 10.0; slider18 = 1; slider19 = 100;
    slider20 = 4.0; slider21 = 1.08;
  ) : idx == 20 ? ( // Jens Bogren
    slider3 = 0.0; slider4 = -2.2; slider5 = 1;
    slider6 = -18.0; slider7 = 6600; slider8 = -6.5; slider9 = 0;
    slider10 = 1.8; slider11 = 2.2; slider12 = 2.5;
    slider13 = 1; slider14 = 0; slider15 = -5.0; slider16 = 1;
    slider17 = 15.0; slider18 = 2; slider19 = 100;
    slider20 = 3.5; slider21 = 1.06;
  ) : idx == 21 ? ( // Adam Nolly Getgood
    slider3 = 0.0; slider4 = -2.0; slider5 = 1;
    slider6 = -18.0; slider7 = 6800; slider8 = -6.5; slider9 = 0;
    slider10 = 0.8; slider11 = 2.2; slider12 = 3.2;
    slider13 = 1; slider14 = 0; slider15 = -4.5; slider16 = 1;
    slider17 = 15.0; slider18 = 2; slider19 = 100;
    slider20 = 2.0; slider21 = 1.06;
  ) : idx == 22 ? ( // Acle Kahney
    slider3 = 0.0; slider4 = -1.8; slider5 = 1;
    slider6 = -17.0; slider7 = 7200; slider8 = -5.5; slider9 = 0;
    slider10 = 1.0; slider11 = 1.8; slider12 = 3.5;
    slider13 = 1; slider14 = 0; slider15 = -4.0; slider16 = 1;
    slider17 = 20.0; slider18 = 3; slider19 = 100;
    slider20 = 2.2; slider21 = 1.12;
  ) : idx == 23 ? ( // Adam Cichocki
    slider3 = 0.0; slider4 = -2.6; slider5 = 1;
    slider6 = -18.5; slider7 = 6400; slider8 = -7.0; slider9 = 0;
    slider10 = 2.0; slider11 = 2.5; slider12 = 2.0;
    slider13 = 1; slider14 = 1; slider15 = -6.0; slider16 = 2;
    slider17 = 15.0; slider18 = 1; slider19 = 100;
    slider20 = 4.8; slider21 = 1.04;
  ) : ( // Manuel Renner
    slider3 = 0.0; slider4 = -2.4; slider5 = 1;
    slider6 = -18.0; slider7 = 6700; slider8 = -6.5; slider9 = 0;
    slider10 = 1.2; slider11 = 2.5; slider12 = 3.0;
    slider13 = 1; slider14 = 0; slider15 = -5.0; slider16 = 1;
    slider17 = 15.0; slider18 = 2; slider19 = 100;
    slider20 = 3.2; slider21 = 1.08;
  );
  update_vocal_filters();
  slider_automate();
);

update_vocal_filters();

@slider
prev_preset != slider2 ? (
  apply_producer_preset(slider2);
  prev_preset = slider2;
);
update_vocal_filters();

@sample
dry_l = spl0; dry_r = spl1;

// ANSI C16.5 300ms RMS integration for moving coil
vu_omega = 1.0 - exp(-1.0 / (srate * 0.300));
vu_sig_sq = (dry_l * dry_l + dry_r * dry_r) * 0.5;
vu_rms_smooth += (vu_sig_sq - vu_rms_smooth) * vu_omega;
vocal_rms = vu_rms_smooth > 0.000000001 ? 10.0 * log10(vu_rms_smooth) : -90.0;
vocal_peak = max(abs(dry_l), abs(dry_r));

// 1:1 Complete Bit-Exact Transparent Pass if Suite Bypassed OR Preset 00
(!slider22 || slider2 == 0) ? (
  spl0 = dry_l;
  spl1 = dry_r;
  vocal_gr_db = 0.0;
  de_gr_db = 0.0;
) : (
  // 1. Input Calibration
  in_trim = exp(slider3 * 0.1151292546497);
  s0 = spl0 * in_trim;
  s1 = spl1 * in_trim;

  // 2. Master Sibilance Sentry (Dynamic High-Frequency Clamping)
  de_l = (de_b0 * s0 + de_b1 * de_bp_x1_l + de_b2 * de_bp_x2_l - de_a1 * de_bp_y1_l - de_a2 * de_bp_y2_l) / de_a0;
  de_bp_x2_l = de_bp_x1_l; de_bp_x1_l = s0; de_bp_y2_l = de_bp_y1_l; de_bp_y1_l = de_l;

  de_r = (de_b0 * s1 + de_b1 * de_bp_x1_r + de_b2 * de_bp_x2_r - de_a1 * de_bp_y1_r - de_a2 * de_bp_y2_r) / de_a0;
  de_bp_x2_r = de_bp_x1_r; de_bp_x1_r = s1; de_bp_y2_r = de_bp_y1_r; de_bp_y1_r = de_r;

  de_sig = max(abs(de_l), abs(de_r));
  de_db = de_sig > 0.000001 ? 20.0 * log10(de_sig) : -120.0;
  de_target_gr = 0.0;
  de_db > slider6 ? (
    de_over = de_db - slider6;
    de_target_gr = min(abs(slider8), de_over * 0.75);
  );
  de_att = exp(-1.0 / (0.001 * srate));
  de_rel = exp(-1.0 / (0.050 * srate));
  de_target_gr > de_gr_db ? (
    de_gr_db = de_gr_db * de_att + de_target_gr * (1.0 - de_att);
  ) : (
    de_gr_db = de_gr_db * de_rel + de_target_gr * (1.0 - de_rel);
  );

  slider9 ? ( // Sibilance Delta Solo
    spl0 = de_l * (de_gr_db > 0.5 ? 2.0 : 0.0);
    spl1 = de_r * (de_gr_db > 0.5 ? 2.0 : 0.0);
  ) : (
    de_gain = exp(-de_gr_db * 0.1151292546497);
    s0 = s0 - de_l * (1.0 - de_gain);
    s1 = s1 - de_r * (1.0 - de_gain);

    // 3. Baxandall Dual Tone Shaping
    ty0 = (bax_w_b0 * s0 + bax_w_b1 * bax_w_x1_l + bax_w_b2 * bax_w_x2_l - bax_w_a1 * bax_w_y1_l - bax_w_a2 * bax_w_y2_l) / bax_w_a0;
    bax_w_x2_l = bax_w_x1_l; bax_w_x1_l = s0; bax_w_y2_l = bax_w_y1_l; bax_w_y1_l = ty0; s0 = ty0;
    ty1 = (bax_w_b0 * s1 + bax_w_b1 * bax_w_x1_r + bax_w_b2 * bax_w_x2_r - bax_w_a1 * bax_w_y1_r - bax_w_a2 * bax_w_y2_r) / bax_w_a0;
    bax_w_x2_r = bax_w_x1_r; bax_w_x1_r = s1; bax_w_y2_r = bax_w_y1_r; bax_w_y1_r = ty1; s1 = ty1;

    ty0 = (bax_p_b0 * s0 + bax_p_b1 * bax_p_x1_l + bax_p_b2 * bax_p_x2_l - bax_p_a1 * bax_p_y1_l - bax_p_a2 * bax_p_y2_l) / bax_p_a0;
    bax_p_x2_l = bax_p_x1_l; bax_p_x1_l = s0; bax_p_y2_l = bax_p_y1_l; bax_p_y1_l = ty0; s0 = ty0;
    ty1 = (bax_p_b0 * s1 + bax_p_b1 * bax_p_x1_r + bax_p_b2 * bax_p_x2_r - bax_p_a1 * bax_p_y1_r - bax_p_a2 * bax_p_y2_r) / bax_p_a0;
    bax_p_x2_r = bax_p_x1_r; bax_p_x1_r = s1; bax_p_y2_r = bax_p_y1_r; bax_p_y1_r = ty1; s1 = ty1;

    ty0 = (bax_a_b0 * s0 + bax_a_b1 * bax_a_x1_l + bax_a_b2 * bax_a_x2_l - bax_a_a1 * bax_a_y1_l - bax_a_a2 * bax_a_y2_l) / bax_a_a0;
    bax_a_x2_l = bax_a_x1_l; bax_a_x1_l = s0; bax_a_y2_l = bax_a_y1_l; bax_a_y1_l = ty0; s0 = ty0;
    ty1 = (bax_a_b0 * s1 + bax_a_b1 * bax_a_x1_r + bax_a_b2 * bax_a_x2_r - bax_a_a1 * bax_a_y1_r - bax_a_a2 * bax_a_y2_r) / bax_a_a0;
    bax_a_x2_r = bax_a_x1_r; bax_a_x1_r = s1; bax_a_y2_r = bax_a_y1_r; bax_a_y1_r = ty1; s1 = ty1;

    // 4. Fairchild 670 Variable-Mu Tube Compressor / Opto Leveler
    slider13 ? (
      v_sig = max(abs(s0), abs(s1));
      v_db = v_sig > 0.000001 ? 20.0 * log10(v_sig) : -120.0;
      r_val = slider16 == 0 ? 1.5 : (slider16 == 1 ? 2.0 : (slider16 == 2 ? 3.0 : 4.0));
      v_gr_target = 0.0;
      v_db > slider15 ? (
        v_over = v_db - slider15;
        slider14 == 1 ? (
          // Vintage Opto Smooth Knee
          v_gr_target = v_over * (1.0 - 1.0 / r_val) * 1.1;
        ) : (
          // Fairchild Variable-Mu Progressive Soft-Curvature
          v_gr_target = (v_over * (1.0 - 1.0 / r_val)) * 1.0;
        );
      );
      v_att = exp(-1.0 / (clamp(slider17, 0.2, 50.0) * 0.001 * srate));
      v_rel_ms = slider18 == 0 ? 100.0 : (slider18 == 1 ? 300.0 : (slider18 == 2 ? 600.0 : (slider18 == 3 ? 1200.0 : 350.0)));
      v_rel = exp(-1.0 / (v_rel_ms * 0.001 * srate));

      v_gr_target > vocal_gr_db ? (
        vocal_gr_db = vocal_gr_db * v_att + v_gr_target * (1.0 - v_att);
      ) : (
        vocal_gr_db = vocal_gr_db * v_rel + v_gr_target * (1.0 - v_rel);
      );

      vg_gain = exp(-vocal_gr_db * 0.1151292546497);
      wet_v = slider19 * 0.01;
      s0 = s0 * (1.0 - wet_v + vg_gain * wet_v);
      s1 = s1 * (1.0 - wet_v + vg_gain * wet_v);
    ) : (
      vocal_gr_db = 0.0;
    );

    // 5. Vocal Tube Warmth Saturation
    slider20 > 0.0 ? (
      t_drive = exp(slider20 * 0.1151292546497);
      d0 = s0 * t_drive; d1 = s1 * t_drive;
      s0 = (d0 + 0.18 * d0 * d0) / (1.0 + abs(d0 + 0.18 * d0 * d0) * 0.35);
      s1 = (d1 + 0.18 * d1 * d1) / (1.0 + abs(d1 + 0.18 * d1 * d1) * 0.35);
      s0 = s0 / sqrt(t_drive);
      s1 = s1 / sqrt(t_drive);
    );

    // 6. Lead Center-Lock & Stereo Spread
    m_mid = (s0 + s1) * 0.5;
    m_side = (s0 - s1) * 0.5;
    w_side = m_side * slider21;
    s0 = m_mid + w_side;
    s1 = m_mid - w_side;

    // 7. Headroom Trim & Pre-Master Soft Limiter
    out_trim = exp(slider4 * 0.1151292546497);
    s0 *= out_trim;
    s1 *= out_trim;

    slider5 == 1 ? ( // -6.0 dBTP Transparent Soft Analog Safety Limiter
      ceil_lvl = 0.501187; // -6.0 dBFS
      abs0 = abs(s0); abs1 = abs(s1);
      abs0 > ceil_lvl ? (
        over0 = abs0 - ceil_lvl;
        s0 = (s0 > 0 ? 1 : -1) * (ceil_lvl + fast_shape(over0 * 2.5) * 0.04);
      );
      abs1 > ceil_lvl ? (
        over1 = abs1 - ceil_lvl;
        s1 = (s1 > 0 ? 1 : -1) * (ceil_lvl + fast_shape(over1 * 2.5) * 0.04);
      );
    );

    // 8. Delta Solo Mode
    slider23 ? (
      spl0 = s0 - dry_l;
      spl1 = s1 - dry_r;
    ) : (
      spl0 = s0;
      spl1 = s1;
    );
  );
);

// Needle ballistics
needle_omega = 1.0 - exp(-1.0 / (srate * 0.050));
cur_vu_db = vocal_rms + 18.0 + slider20 * 0.25;
sifam_vocal_vu += (cur_vu_db - sifam_vocal_vu) * needle_omega;
vocal_gr_db = clamp(vocal_gr_db, 0.0, 24.0);
sifam_vocal_gr += (vocal_gr_db - sifam_vocal_gr) * needle_omega;
sifam_vocal_gr = clamp(sifam_vocal_gr, 0.0, 24.0);

// Shared memory telemetry broadcast (1450..1499)
rms_acc_l += spl0 * spl0;
rms_acc_r += spl1 * spl1;
rms_cnt += 1;
rms_cnt >= 1024 ? (
  gmem[1451] = max(abs(spl0), abs(spl1));
  gmem[1452] = 10.0 * log10(max(0.000000001, (rms_acc_l + rms_acc_r) * (0.5 / 1024)));
  gmem[1453] = vocal_gr_db;
  gmem[1454] = de_gr_db;
  gmem[1455] = slider1;
  gmem[1456] = slider22;
  gmem[1457] = slider2;
  gmem[1458] = slider20;
  gmem[1459] = slider27; // Corridor Carve Request Active
  rms_acc_l = 0.0; rms_acc_r = 0.0; rms_cnt = 0;
);

@gfx 1080 700
// =============================================================================
// GLOBAL HARDWARE CONSOLE GUI ENGINE // LUXURY VOCAL EMPRESS CHASSIS
// =============================================================================
crt_x = 8; crt_y = 8;
crt_w = gfx_w - 16; crt_h = gfx_h - 16;

mouse_down = (mouse_cap & 1);
mouse_clicked = mouse_down && !prev_mouse_down;
prev_mouse_down = mouse_down;

// Outer Obsidian Titanium Dual Bezel Frame (Empress Magenta & Electric Cyan)
gfx_r = 0.016; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(crt_x, crt_y, crt_w, crt_h);
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(crt_x, crt_y, crt_w, crt_h, 0);
gfx_r = 0.14; gfx_g = 0.18; gfx_b = 0.28; gfx_rect(crt_x + 1, crt_y + 1, crt_w - 2, crt_h - 2, 0);

// Corner Machine Hex Bolts
function draw_screw(sx, sy) (
  gfx_r = 0.14; gfx_g = 0.16; gfx_b = 0.24; gfx_circle(sx, sy, 5, 1);
  gfx_r = 0.50; gfx_g = 0.55; gfx_b = 0.68; gfx_circle(sx, sy, 5, 0);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_line(sx - 3, sy, sx + 3, sy);
);
draw_screw(crt_x + 8, crt_y + 8);
draw_screw(crt_x + crt_w - 8, crt_y + 8);
draw_screw(crt_x + 8, crt_y + crt_h - 8);
draw_screw(crt_x + crt_w - 8, crt_y + crt_h - 8);

// Safe fitted text
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
// 1. TOP HEADER BAR: DUAFE COMB CREST, PRESET NAVIGATOR & STATUS PILLS
// ─────────────────────────────────────────────────────────────────────────────
hdr_h = 46;
gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.022; gfx_rect(crt_x + 2, crt_y + 2, crt_w - 4, hdr_h);
gfx_r = 0.16; gfx_g = 0.22; gfx_b = 0.34; gfx_line(crt_x + 2, crt_y + hdr_h + 2, crt_x + crt_w - 2, crt_y + hdr_h + 2);

// Duafe Comb Sceptre Crest
sig_cx = crt_x + 24; sig_cy = crt_y + 23;
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
gfx_circle(sig_cx, sig_cy, 11, 0);
gfx_circle(sig_cx, sig_cy, 7, 0);
gfx_circle(sig_cx, sig_cy, 3, 1);

gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.98; gfx_g = 0.90; gfx_b = 1.00;
gfx_x = crt_x + 42; gfx_y = crt_y + 15;
gfx_drawstr("DAMEI // VOCAL EMPRESS");

right_edge_x = crt_x + crt_w - 12;

// Pill 1: ENGAGED / BYPASS
byp_w = 84; byp_x = right_edge_x - byp_w;
byp_hov = (mouse_x >= byp_x && mouse_x <= byp_x + byp_w && mouse_y >= crt_y + 8 && mouse_y <= crt_y + 38);
gfx_r = slider22 ? (byp_hov ? 0.20 : 0.10) : (byp_hov ? 0.28 : 0.16);
gfx_g = slider22 ? (byp_hov ? 0.12 : 0.06) : (byp_hov ? 0.08 : 0.05);
gfx_b = slider22 ? (byp_hov ? 0.32 : 0.18) : (byp_hov ? 0.08 : 0.05);
gfx_rect(byp_x, crt_y + 8, byp_w, 30);
gfx_r = slider22 ? 0.88 : 0.95; gfx_g = slider22 ? 0.25 : 0.30; gfx_b = slider22 ? 0.65 : 0.30;
gfx_rect(byp_x, crt_y + 8, byp_w, 30, 0);
gfx_setfont(2, "Orbitron", 11.5, 'b');
b_txt = slider22 ? "ENGAGED" : "BYPASS";
gfx_measurestr(b_txt, btw, bth);
gfx_x = byp_x + (byp_w - btw) * 0.5; gfx_y = crt_y + 15;
gfx_drawstr(b_txt);
mouse_clicked && byp_hov ? (slider22 = !slider22; slider_automate(););

// Pill 2: Headroom Ceiling (-6dB Lock vs Free)
ceil_w = 88; ceil_x = byp_x - ceil_w - 6;
ceil_hov = (mouse_x >= ceil_x && mouse_x <= ceil_x + ceil_w && mouse_y >= crt_y + 8 && mouse_y <= crt_y + 38);
gfx_r = slider5 ? 0.12 : 0.06; gfx_g = slider5 ? 0.08 : 0.10; gfx_b = slider5 ? 0.20 : 0.12;
gfx_rect(ceil_x, crt_y + 8, ceil_w, 30);
gfx_r = slider5 ? 0.88 : 0.50; gfx_g = slider5 ? 0.25 : 0.50; gfx_b = slider5 ? 0.65 : 0.50;
gfx_rect(ceil_x, crt_y + 8, ceil_w, 30, 0);
gfx_setfont(3, "Consolas", 12, 'b');
c_txt = slider5 ? "CEIL: -6dB" : "CEIL: FREE";
gfx_measurestr(c_txt, ctw, cth);
gfx_x = ceil_x + (ceil_w - ctw) * 0.5; gfx_y = crt_y + 15;
gfx_drawstr(c_txt);
mouse_clicked && ceil_hov ? (slider5 = !slider5; slider_automate(););

// Pill 3: Mode (Master vs Stem)
mode_w = 96; mode_x = ceil_x - mode_w - 6;
mode_hov = (mouse_x >= mode_x && mouse_x <= mode_x + mode_w && mouse_y >= crt_y + 8 && mouse_y <= crt_y + 38);
gfx_r = 0.08; gfx_g = 0.06; gfx_b = 0.16; gfx_rect(mode_x, crt_y + 8, mode_w, 30);
gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(mode_x, crt_y + 8, mode_w, 30, 0);
gfx_setfont(3, "Consolas", 12, 'b');
m_txt = slider25 ? "MODE: STEM" : "MODE: MASTER";
gfx_measurestr(m_txt, mtw, mth);
gfx_x = mode_x + (mode_w - mtw) * 0.5; gfx_y = crt_y + 15;
gfx_drawstr(m_txt);
mouse_clicked && mode_hov ? (slider25 = !slider25; slider_automate(););

// Pill 4: Instrumental Music Telemetry Link
ib_mus_rms = gmem[1402];
ib_alive = (gmem[1400] == 1);
mlink_w = 110; mlink_x = mode_x - mlink_w - 6;
gfx_r = ib_alive ? 0.04 : 0.08; gfx_g = ib_alive ? 0.18 : 0.08; gfx_b = ib_alive ? 0.22 : 0.10;
gfx_rect(mlink_x, crt_y + 8, mlink_w, 30);
gfx_r = ib_alive ? 0.00 : 0.50; gfx_g = ib_alive ? 0.85 : 0.50; gfx_b = ib_alive ? 1.00 : 0.50;
gfx_rect(mlink_x, crt_y + 8, mlink_w, 30, 0);
gfx_setfont(3, "Consolas", 11.5, 'b');
ib_str = ib_alive ? sprintf(#, "MUS: %.1fdB", ib_mus_rms) : "MUS: STBY";
gfx_measurestr(ib_str, ibw, ibh);
gfx_x = mlink_x + (mlink_w - ibw) * 0.5; gfx_y = crt_y + 15;
gfx_drawstr(ib_str);

// Pill 5: Song Structure Sync
rgn_w = 105; rgn_x = mlink_x - rgn_w - 6;
gfx_r = 0.04; gfx_g = 0.08; gfx_b = 0.12; gfx_rect(rgn_x, crt_y + 8, rgn_w, 30);
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(rgn_x, crt_y + 8, rgn_w, 30, 0);
g_sec = gmem[100] == 1 ? gmem[101] : 0;
r_str = g_sec == 3 ? "⚡ CHORUS" : sprintf(#, "● SYNC: %dR", gmem[103] > 0 ? gmem[103] : 20);
gfx_setfont(3, "Consolas", 11.5, 'b');
gfx_measurestr(r_str, rsw, rsh);
gfx_x = rgn_x + (rgn_w - rsw) * 0.5; gfx_y = crt_y + 15;
gfx_drawstr(r_str);

// Center Stepper: Producer Benchmark Quick Navigator
mid_w = rgn_x - (crt_x + 235) - 12;
mid_x = crt_x + 235;
btn_sz = 26;
prv_x = mid_x; prv_y = crt_y + 10;
prv_hov = (mouse_x >= prv_x && mouse_x <= prv_x + btn_sz && mouse_y >= prv_y && mouse_y <= prv_y + btn_sz);
gfx_r = prv_hov ? 0.20 : 0.06; gfx_g = prv_hov ? 0.10 : 0.04; gfx_b = prv_hov ? 0.26 : 0.10;
gfx_rect(prv_x, prv_y, btn_sz, btn_sz);
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(prv_x, prv_y, btn_sz, btn_sz, 0);
gfx_setfont(1, "Orbitron", 12, 'b'); gfx_x = prv_x + 8; gfx_y = prv_y + 5; gfx_drawstr("<");
mouse_clicked && prv_hov ? (
  slider2 = (slider2 - 1 + 25) % 25;
  apply_producer_preset(slider2);
  prev_preset = slider2;
);

nxt_x = prv_x + mid_w - btn_sz; nxt_y = prv_y;
nxt_hov = (mouse_x >= nxt_x && mouse_x <= nxt_x + btn_sz && mouse_y >= nxt_y && mouse_y <= nxt_y + btn_sz);
gfx_r = nxt_hov ? 0.20 : 0.06; gfx_g = nxt_hov ? 0.10 : 0.04; gfx_b = nxt_hov ? 0.26 : 0.10;
gfx_rect(nxt_x, nxt_y, btn_sz, btn_sz);
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(nxt_x, nxt_y, btn_sz, btn_sz, 0);
gfx_setfont(1, "Orbitron", 12, 'b'); gfx_x = nxt_x + 8; gfx_y = nxt_y + 5; gfx_drawstr(">");
mouse_clicked && nxt_hov ? (
  slider2 = (slider2 + 1) % 25;
  apply_producer_preset(slider2);
  prev_preset = slider2;
);

lbl_x = prv_x + btn_sz + 4; lbl_w = mid_w - 2 * btn_sz - 8;
lbl_hov = (mouse_x >= lbl_x && mouse_x <= lbl_x + lbl_w && mouse_y >= prv_y && mouse_y <= prv_y + btn_sz);
gfx_r = lbl_hov ? 0.08 : 0.02; gfx_g = lbl_hov ? 0.04 : 0.02; gfx_b = lbl_hov ? 0.14 : 0.04;
gfx_rect(lbl_x, prv_y, lbl_w, btn_sz);
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(lbl_x, prv_y, lbl_w, btn_sz, 0);
p_str = get_producer_short_name(slider2);
gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
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
  gfx_r = sel ? 0.18 : (t_hov ? 0.10 : 0.035);
  gfx_g = sel ? 0.10 : (t_hov ? 0.06 : 0.030);
  gfx_b = sel ? 0.24 : (t_hov ? 0.14 : 0.055);
  gfx_rect(tx, tab_y, tab_w - 2, tab_h);
  sel ? (
    gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
    gfx_rect(tx, tab_y + tab_h - 3, tab_w - 2, 3);
    gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;
  ) : (
    gfx_r = t_hov ? 0.95 : 0.70; gfx_g = t_hov ? 0.95 : 0.75; gfx_b = t_hov ? 1.00 : 0.85;
  );
  gfx_setfont(2, "Orbitron", 12, 'b');
  t_lbl = (ti == 0 ? "OVERVIEW" : (ti == 1 ? "BAXANDALL" : (ti == 2 ? "VOCAL GLUE" : (ti == 3 ? "DE-ESSER" : (ti == 4 ? "SPATIAL" : (ti == 5 ? "PRESENCE" : "PRODUCER"))))));
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
gfx_r = 0.016; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x, ws_y, ws_w, ws_h);
gfx_r = 0.12; gfx_g = 0.16; gfx_b = 0.26; gfx_rect(ws_x, ws_y, ws_w, ws_h, 0);

// Helper for horizontal parameter slider
function draw_param_slider(px, py, pw, ph, label_str, val, min_v, max_v, fmt_str, s_idx, accent_r, accent_g, accent_b) local(val_str, vsw, vsh, trx, try, trw, trh, frac, fill_w, hx, hy, hov, new_f) (
  gfx_r = 0.022; gfx_g = 0.026; gfx_b = 0.038; gfx_rect(px, py, pw, ph);
  gfx_r = 0.16; gfx_g = 0.22; gfx_b = 0.34; gfx_rect(px, py, pw, ph, 0);

  gfx_setfont(2, "Orbitron", 11.5, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_x = px + 12; gfx_y = py + 7; gfx_drawstr(label_str);

  val_str = sprintf(#, fmt_str, val);
  gfx_setfont(3, "Consolas", 13, 'b'); gfx_r = 1.0; gfx_g = 0.9; gfx_b = 0.35;
  gfx_measurestr(val_str, vsw, vsh);
  gfx_x = px + pw - vsw - 12; gfx_y = py + 7; gfx_drawstr(val_str);

  trx = px + 12; try = py + 30; trw = pw - 24; trh = 9;
  gfx_r = 0.010; gfx_g = 0.012; gfx_b = 0.018; gfx_rect(trx, try, trw, trh);
  gfx_r = 0.24; gfx_g = 0.30; gfx_b = 0.44; gfx_rect(trx, try, trw, trh, 0);

  frac = max(0.0, min(1.0, (val - min_v) / (max_v - min_v)));
  fill_w = floor(frac * trw);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_rect(trx, try, fill_w, trh);

  hx = trx + fill_w; hy = try + trh * 0.5;
  gfx_r = 1.0; gfx_g = 0.90; gfx_b = 0.40; gfx_circle(hx, hy, 7, 1);
  gfx_r = 0.1; gfx_g = 0.12; gfx_b = 0.15; gfx_circle(hx, hy, 7, 0);

  hov = (mouse_x >= px && mouse_x <= px + pw && mouse_y >= py && mouse_y <= py + ph);
  mouse_clicked && hov ? drag_slider_idx = s_idx;
  drag_slider_idx == s_idx && mouse_down ? (
    new_f = max(0.0, min(1.0, (mouse_x - trx) / trw));
    slider(s_idx) = min_v + new_f * (max_v - min_v);
    update_vocal_filters();
    slider_automate();
  );
);

// Helper for Vertical Channel Strip
function draw_vocal_channel_strip(px, py, pw, ph, title_str, sub_str, val, min_v, max_v, fmt_str, s_idx, accent_r, accent_g, accent_b) local(val_str, vsw, vsh, trk_x, trk_y, trk_h, trk_w, frac, h_cy, mid_y, cap_w, cap_h, cap_x, cap_y, hov, new_f) (
  gfx_r = 0.020; gfx_g = 0.024; gfx_b = 0.034; gfx_rect(px, py, pw, ph);
  gfx_r = accent_r * 0.8; gfx_g = accent_g * 0.8; gfx_b = accent_b * 0.8; gfx_rect(px, py, pw, ph, 0);

  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(px + 1, py + 1, pw - 2, 48);
  gfx_r = 0.16; gfx_g = 0.22; gfx_b = 0.34; gfx_line(px + 1, py + 49, px + pw - 2, py + 49);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  gfx_measurestr(title_str, tsw, tsh);
  gfx_x = px + floor((pw - tsw) * 0.5); gfx_y = py + 9;
  gfx_drawstr(title_str);

  gfx_setfont(3, "Segoe UI", 12); gfx_r = 0.70; gfx_g = 0.78; gfx_b = 0.88;
  gfx_measurestr(sub_str, ssw, ssh);
  gfx_x = px + floor((pw - ssw) * 0.5); gfx_y = py + 28;
  gfx_drawstr(sub_str);

  v_box_y = py + 56; v_box_h = 30;
  gfx_r = 0.008; gfx_g = 0.012; gfx_b = 0.018; gfx_rect(px + 8, v_box_y, pw - 16, v_box_h);
  gfx_r = accent_r * 0.6; gfx_g = accent_g * 0.6; gfx_b = accent_b * 0.6; gfx_rect(px + 8, v_box_y, pw - 16, v_box_h, 0);

  val_str = sprintf(#, fmt_str, val);
  gfx_setfont(1, "Consolas", 13.5, 'b'); gfx_r = 1.0; gfx_g = 0.92; gfx_b = 0.40;
  gfx_measurestr(val_str, vsw, vsh);
  gfx_x = px + floor((pw - vsw) * 0.5); gfx_y = v_box_y + 7; gfx_drawstr(val_str);

  trk_x = px + floor(pw * 0.5) - 4;
  trk_y = py + 102;
  trk_h = ph - 150;
  trk_w = 8;
  gfx_r = 0.008; gfx_g = 0.012; gfx_b = 0.018; gfx_rect(trk_x, trk_y, trk_w, trk_h);
  gfx_r = 0.22; gfx_g = 0.32; gfx_b = 0.44; gfx_rect(trk_x, trk_y, trk_w, trk_h, 0);

  gfx_setfont(3, "Consolas", 11, 'b'); gfx_r = 0.50; gfx_g = 0.65; gfx_b = 0.80;
  gfx_line(trk_x - 12, trk_y, trk_x - 4, trk_y); gfx_x = trk_x - 36; gfx_y = trk_y - 6; gfx_drawstr("+6");
  gfx_line(trk_x - 12, trk_y + trk_h * 0.5, trk_x - 4, trk_y + trk_h * 0.5); gfx_x = trk_x - 30; gfx_y = trk_y + trk_h * 0.5 - 6; gfx_drawstr("0");
  gfx_line(trk_x - 12, trk_y + trk_h, trk_x - 4, trk_y + trk_h); gfx_x = trk_x - 36; gfx_y = trk_y + trk_h - 6; gfx_drawstr("-6");

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

  cap_w = pw - 32; cap_h = 18;
  cap_x = px + 16; cap_y = h_cy - 9;
  gfx_r = 0.16; gfx_g = 0.22; gfx_b = 0.32; gfx_rect(cap_x, cap_y, cap_w, cap_h);
  gfx_r = 0.88; gfx_g = 0.92; gfx_b = 0.98; gfx_rect(cap_x, cap_y, cap_w, cap_h, 0);
  gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b; gfx_line(cap_x + 8, cap_y + 9, cap_x + cap_w - 8, cap_y + 9);

  gfx_setfont(3, "Segoe UI", 12); gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.88;
  gfx_measurestr("DRAG FADER", bsw, bsh);
  gfx_x = px + floor((pw - bsw) * 0.5); gfx_y = py + ph - 26;
  gfx_drawstr("DRAG FADER");

  hov = (mouse_x >= px && mouse_x <= px + pw && mouse_y >= trk_y - 12 && mouse_y <= trk_y + trk_h + 12);
  mouse_clicked && hov ? drag_slider_idx = s_idx;
  drag_slider_idx == s_idx && mouse_down ? (
    new_f = max(0.0, min(1.0, (trk_y + trk_h - mouse_y) / trk_h));
    slider(s_idx) = min_v + new_f * (max_v - min_v);
    update_vocal_filters();
    slider_automate();
  );
);

// Authentic SIFAM Analogue Moving-Coil VU Meter for Vocals
function draw_sifam_vocal_meter(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) (
  gfx_r = 0.055; gfx_g = 0.065; gfx_b = 0.080; gfx_rect(mx, my, mw, mh);
  gfx_r = 0.020; gfx_g = 0.024; gfx_b = 0.032; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(mx, my, mw, mh, 0);
  gfx_r = 0.25; gfx_g = 0.32; gfx_b = 0.40; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4, 0);

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = mx + 14; gfx_y = my + 10; gfx_drawstr(title_str);

  gfx_setfont(2, "Orbitron", 11.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  badge_str = is_glue ? "IMPERIAL GR" : "TUBE VU";
  gfx_measurestr(badge_str, b_w, b_h);
  gfx_x = mx + mw - b_w - 14; gfx_y = my + 10; gfx_drawstr(badge_str);

  arc_cx = mx + mw * 0.5; arc_cy = my + mh + 20; arc_r = mh * 1.15;
  a_left = -0.58; a_right = 0.58; a_span = a_right - a_left;

  is_glue ? (
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

  frac = is_glue ? min(1.0, max(0.0, needle_val / 16.0)) : min(1.0, max(0.0, (needle_val + 20.0) / 23.0));
  cur_ang = a_left + frac * a_span;
  tip_x = arc_cx + sin(cur_ang) * arc_r; tip_y = arc_cy - cos(cur_ang) * arc_r;
  gfx_r = 1.0; gfx_g = 0.90; gfx_b = 0.45;
  gfx_line(arc_cx - 1, arc_cy, tip_x - 1, tip_y);
  gfx_line(arc_cx, arc_cy, tip_x, tip_y);
  gfx_line(arc_cx + 1, arc_cy, tip_x + 1, tip_y);
  gfx_r = 1.0; gfx_g = 0.30; gfx_b = 0.20; gfx_circle(tip_x, tip_y, 3, 1);

  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(arc_cx, arc_cy - 10, 16, 1);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_circle(arc_cx, arc_cy - 10, 16, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  center_badge = is_glue ? "[ GR ]" : "[ VU ]";
  gfx_measurestr(center_badge, cbw, cbh);
  gfx_x = arc_cx - cbw * 0.5; gfx_y = my + mh * 0.58; gfx_drawstr(center_badge);

  gfx_setfont(3, "Consolas", 12.5, 'b');
  is_glue ? (
    gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_x = mx + 16; gfx_y = my + mh - 24;
    gfx_printf("GR:  %4.1f dB", needle_val);
    gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.85; gfx_x = mx + mw - 110; gfx_y = my + mh - 24;
    gfx_drawstr("PEAK HOLD");
  ) : (
    gfx_r = 0.15; gfx_g = 0.95; gfx_b = 0.45; gfx_x = mx + 16; gfx_y = my + mh - 24;
    gfx_printf("RMS: %4.1f dBFS", vocal_rms);
    gfx_r = 0.85; gfx_g = 0.72; gfx_b = 0.28; gfx_x = mx + mw - 140; gfx_y = my + mh - 24;
    gfx_drawstr("0 VU = -18 dBFS");
  );
);

// =============================================================================
// TAB 0: OVERVIEW (TWIN SIFAM ANALOG METERS + SPATIAL RADAR + 3 HARDWARE CARDS)
// =============================================================================
slider1 == 0 ? (
  top_row_h = 240;
  meter_w = floor((ws_w - 40) * 0.36);
  scope_w = ws_w - 2 * meter_w - 32;

  draw_sifam_vocal_meter(ws_x + 12, ws_y + 12, meter_w, top_row_h, "VOCAL TUBE WARMTH // SATURATION", sifam_vocal_vu, 3.0, 0, 0.88, 0.25, 0.65);
  draw_sifam_vocal_meter(ws_x + 16 + meter_w, ws_y + 12, meter_w, top_row_h, "MASTER VOCAL GLUE // GAIN REDUCTION", sifam_vocal_gr, 16.0, 1, 0.00, 0.85, 1.00);

  // Vocal Spatial Radar
  scope_x = ws_x + 20 + 2 * meter_w;
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(scope_x, ws_y + 12, scope_w, top_row_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(scope_x, ws_y + 12, scope_w, top_row_h, 0);

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = scope_x + 14; gfx_y = ws_y + 22; gfx_drawstr("VOCAL SPATIAL RADAR");

  r_cx = scope_x + scope_w * 0.5; r_cy = ws_y + 12 + 105;
  gfx_r = 0.12; gfx_g = 0.16; gfx_b = 0.26;
  gfx_circle(r_cx, r_cy, 65, 0);
  gfx_circle(r_cx, r_cy, 40, 0);
  gfx_line(r_cx - 65, r_cy, r_cx + 65, r_cy);
  gfx_line(r_cx, r_cy - 65, r_cx, r_cy + 65);

  cbar_y = ws_y + top_row_h - 32; cbar_w = scope_w - 28;
  gfx_r = 0.06; gfx_g = 0.09; gfx_b = 0.14; gfx_rect(scope_x + 14, cbar_y, cbar_w, 8);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_rect(scope_x + 14 + floor(cbar_w * 0.5), cbar_y, floor((slider21 - 1.0) * (cbar_w * 0.5)), 8);

  gfx_setfont(3, "Consolas", 11, 'b'); gfx_r = 0.65; gfx_g = 0.75; gfx_b = 0.85;
  gfx_x = scope_x + 14; gfx_y = cbar_y - 16; gfx_drawstr("-1.0");
  gfx_x = scope_x + 14 + floor(cbar_w * 0.5) - 10; gfx_y = cbar_y - 16; gfx_drawstr("0.0");
  gfx_x = scope_x + 14 + cbar_w - 24; gfx_y = cbar_y - 16; gfx_drawstr("+1.0");

  // Bottom 3 Luxury Hardware Console Modules
  dash_y = ws_y + top_row_h + 16; dash_h = ws_h - top_row_h - 26;
  col_w = floor((ws_w - 32) / 3);

  // Card 1: VOCAL GAIN & HEADROOM
  c1_x = ws_x + 12;
  gfx_r = 0.020; gfx_g = 0.024; gfx_b = 0.034; gfx_rect(c1_x, dash_y, col_w, dash_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(c1_x, dash_y, col_w, dash_h, 0);
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(c1_x + 2, dash_y + 2, col_w - 4, 32);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = c1_x + 14; gfx_y = dash_y + 9; gfx_drawstr("1. VOCAL GAIN & SUMMING");

  gfx_setfont(3, "Consolas", 12.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.96;
  gfx_x = c1_x + 16; gfx_y = dash_y + 45; gfx_printf("Input Calibration : %+4.1f dB", slider3);
  gfx_x = c1_x + 16; gfx_y = dash_y + 70; gfx_printf("Producer Output   : %+4.1f dB Trim", slider4);
  gfx_x = c1_x + 16; gfx_y = dash_y + 95; gfx_printf("Pre-Master Ceiling: %s", slider5 ? "-6.0 dBTP Strict Lock" : "Free Range");
  gfx_x = c1_x + 16; gfx_y = dash_y + 120; gfx_printf("Summing State     : %s", slider22 ? "ACTIVE VOCAL SUM" : "1:1 PASS");
  gfx_x = c1_x + 16; gfx_y = dash_y + 145; gfx_printf("Delta Solo State  : %s", slider23 ? "ACTIVE SOLO" : "NORMAL SUM");

  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(c1_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(c1_x + 14, dash_y + dash_h - 38, col_w - 28, 26, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = c1_x + 22; gfx_y = dash_y + dash_h - 32;
  p_title = get_producer_short_name(slider2);
  gfx_drawstr(p_title);

  // Card 2: GLUE & SIBILANCE SENTRY
  c2_x = ws_x + 16 + col_w;
  gfx_r = 0.020; gfx_g = 0.024; gfx_b = 0.034; gfx_rect(c2_x, dash_y, col_w, dash_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(c2_x, dash_y, col_w, dash_h, 0);
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(c2_x + 2, dash_y + 2, col_w - 4, 32);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = c2_x + 14; gfx_y = dash_y + 9; gfx_drawstr("2. GLUE & SIBILANCE SENTRY");

  gfx_setfont(3, "Consolas", 12.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.96;
  gfx_x = c2_x + 16; gfx_y = dash_y + 45; gfx_printf("Glue Topology     : %s", slider14 ? "Vintage Opto Leveler" : "Fairchild 670 Tube");
  gfx_x = c2_x + 16; gfx_y = dash_y + 70; gfx_printf("Threshold / Ratio : %.1f dB | %s", slider15, slider16 == 0 ? "1.5:1" : (slider16 == 1 ? "2:1" : (slider16 == 2 ? "3:1" : "4:1")));
  gfx_x = c2_x + 16; gfx_y = dash_y + 95; gfx_printf("Attack / Release  : %.1fms | %s", slider17, slider18 == 0 ? "100ms" : (slider18 == 1 ? "300ms" : (slider18 == 2 ? "600ms" : "Auto")));
  gfx_x = c2_x + 16; gfx_y = dash_y + 120; gfx_printf("De-Esser Clamp    : -%.1f dB @ %d Hz", de_gr_db, slider7);
  gfx_x = c2_x + 16; gfx_y = dash_y + 145; gfx_printf("Live Vocal Glue GR: -%.2f dB Peak Hold", vocal_gr_db);

  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(c2_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(c2_x + 14, dash_y + dash_h - 38, col_w - 28, 26, 0);
  vgr_frac = min(1.0, max(0.0, vocal_gr_db / 12.0));
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_rect(c2_x + 15, dash_y + dash_h - 37, floor((col_w - 30) * vgr_frac), 24);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = c2_x + 22; gfx_y = dash_y + dash_h - 32; gfx_printf("VOCAL GLUE: %4.1f dB", vocal_gr_db);

  // Card 3: BAXANDALL & CORRIDOR
  c3_x = ws_x + 20 + 2 * col_w;
  gfx_r = 0.020; gfx_g = 0.024; gfx_b = 0.034; gfx_rect(c3_x, dash_y, col_w, dash_h);
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35; gfx_rect(c3_x, dash_y, col_w, dash_h, 0);
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(c3_x + 2, dash_y + 2, col_w - 4, 32);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = c3_x + 14; gfx_y = dash_y + 9; gfx_drawstr("3. BAXANDALL & CORRIDOR");

  gfx_setfont(3, "Consolas", 12.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.96;
  gfx_x = c3_x + 16; gfx_y = dash_y + 45; gfx_printf("100Hz Warmth Shelf: %+4.1f dB", slider10);
  gfx_x = c3_x + 16; gfx_y = dash_y + 70; gfx_printf("3.5kHz Presence   : %+4.1f dB", slider11);
  gfx_x = c3_x + 16; gfx_y = dash_y + 95; gfx_printf("12kHz Silk Air    : %+4.1f dB Shelf", slider12);
  gfx_x = c3_x + 16; gfx_y = dash_y + 120; gfx_printf("Spatial Width     : %.2f x (Lead Lock)", slider21);
  gfx_x = c3_x + 16; gfx_y = dash_y + 145; gfx_printf("Tube Saturation   : +%.1f dB Warmth", slider20);

  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(c3_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35; gfx_rect(c3_x + 14, dash_y + dash_h - 38, col_w - 28, 26, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.90; gfx_b = 0.40;
  gfx_x = c3_x + 22; gfx_y = dash_y + dash_h - 32;
  gfx_printf("CORRIDOR RELAY: ACTIVE LINK");
);

// =============================================================================
// TAB 1: BAXANDALL EQ (CURVE PLOT + 3 FULL-HEIGHT CHANNEL STRIPS)
// =============================================================================
slider1 == 1 ? (
  bax_plot_y = ws_y + 12; bax_plot_h = 220; bax_plot_w = ws_w - 24;
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(ws_x + 12, bax_plot_y, bax_plot_w, bax_plot_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(ws_x + 12, bax_plot_y, bax_plot_w, bax_plot_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 24; gfx_y = bax_plot_y + 12; gfx_drawstr("BAXANDALL TONE // SMOOTH BROAD-CURVATURE VOCAL EQUALIZATION");

  cy0 = bax_plot_y + bax_plot_h * 0.5;
  gfx_r = 0.12; gfx_g = 0.18; gfx_b = 0.26;
  gfx_line(ws_x + 12, cy0, ws_x + 12 + bax_plot_w, cy0);
  gfx_line(ws_x + 12, cy0 - 45, ws_x + 12 + bax_plot_w, cy0 - 45);
  gfx_line(ws_x + 12, cy0 + 45, ws_x + 12 + bax_plot_w, cy0 + 45);

  fx100 = ws_x + 12 + floor(bax_plot_w * 0.22);
  fx1k  = ws_x + 12 + floor(bax_plot_w * 0.55);
  fx10k = ws_x + 12 + floor(bax_plot_w * 0.85);
  gfx_line(fx100, bax_plot_y, fx100, bax_plot_y + bax_plot_h);
  gfx_line(fx1k,  bax_plot_y, fx1k,  bax_plot_y + bax_plot_h);
  gfx_line(fx10k, bax_plot_y, fx10k, bax_plot_y + bax_plot_h);

  gfx_setfont(3, "Consolas", 11.5, 'b'); gfx_r = 0.55; gfx_g = 0.65; gfx_b = 0.75;
  gfx_x = fx100 + 4; gfx_y = bax_plot_y + bax_plot_h - 20; gfx_drawstr("100Hz");
  gfx_x = fx1k + 4;  gfx_y = bax_plot_y + bax_plot_h - 20; gfx_drawstr("1kHz");
  gfx_x = fx10k + 4; gfx_y = bax_plot_y + bax_plot_h - 20; gfx_drawstr("10kHz");

  // Draw smooth Baxandall curve
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  prev_py = cy0;
  pi = 0;
  loop(140,
    px = ws_x + 12 + floor((pi / 139.0) * bax_plot_w);
    f_val = 20.0 * exp(log(1000.0) * (pi / 139.0));
    g_tot = 0.0;
    // Low Shelf 100Hz
    f_val <= 100.0 ? g_tot += slider10 : (f_val < 400.0 ? g_tot += slider10 * (1.0 - (f_val - 100.0) / 300.0) : 0);
    // Presence 3.5kHz
    g_tot += slider11 * exp(-0.5 * sqr((log(f_val / 3500.0) / 0.5)));
    // Silk Air 12kHz
    f_val > 6000.0 ? g_tot += slider12 * (min(1.0, (f_val - 6000.0) / 6000.0));
    cur_py = cy0 - g_tot * 7.5;
    pi > 0 ? (
      gfx_line(prev_px, prev_py, px, cur_py);
      gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
      gfx_line(px, cur_py, px, cy0);
    );
    prev_px = px; prev_py = cur_py;
    pi += 1;
  );

  // 3 Full-Height Channel Strips
  col_w = floor((ws_w - 24 - 16) / 3);
  cards_y = bax_plot_y + bax_plot_h + 12; cards_h = ws_h - bax_plot_h - 26;
  draw_vocal_channel_strip(ws_x + 12 + 0 * (col_w + 8), cards_y, col_w, cards_h, "100Hz WARMTH", "CHEST RESONANCE SHELF", slider10, -6.0, 6.0, "%+.1f dB", 10, 0.88, 0.25, 0.65);
  draw_vocal_channel_strip(ws_x + 12 + 1 * (col_w + 8), cards_y, col_w, cards_h, "3.5kHz PRESENCE", "VOCAL CUT & BITE", slider11, -6.0, 6.0, "%+.1f dB", 11, 0.00, 0.85, 1.00);
  draw_vocal_channel_strip(ws_x + 12 + 2 * (col_w + 8), cards_y, col_w, cards_h, "12kHz SILK AIR", "IMPERIAL SHEEN SHELF", slider12, -6.0, 6.0, "%+.1f dB", 12, 1.00, 0.85, 0.35);
);

// =============================================================================
// TAB 2: VOCAL GLUE COMPRESSOR (FAIRCHILD 670 VARIABLE-MU / OPTO PANEL)
// =============================================================================
slider1 == 2 ? (
  vg_y = ws_y + 12; vg_w = ws_w - 24; vg_h = ws_h - 24;
  left_w = floor((vg_w - 24) * 0.46);
  right_w = vg_w - left_w - 16;

  // Left Plot Box
  gfx_r = 0.016; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, vg_y, left_w, vg_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(ws_x + 12, vg_y, left_w, vg_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 24; gfx_y = vg_y + 14; gfx_drawstr("FAIRCHILD 670 VARIABLE-MU CURVE");

  p_x0 = ws_x + 36; p_y0 = vg_y + 50; p_size = min(left_w - 60, vg_h - 180);
  gfx_r = 0.008; gfx_g = 0.012; gfx_b = 0.018; gfx_rect(p_x0, p_y0, p_size, p_size);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.40; gfx_rect(p_x0, p_y0, p_size, p_size, 0);

  gfx_r = 0.35; gfx_g = 0.45; gfx_b = 0.55;
  gfx_line(p_x0, p_y0 + p_size, p_x0 + p_size, p_y0);

  r_val = slider16 == 0 ? 1.5 : (slider16 == 1 ? 2.0 : (slider16 == 2 ? 3.0 : 4.0));
  th_frac = (slider15 + 40.0) / 40.0;
  th_px = p_x0 + floor(th_frac * p_size);
  th_py = p_y0 + p_size - floor(th_frac * p_size);

  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.30;
  gfx_line(p_x0, p_y0 + p_size, th_px, th_py);
  end_py = th_py - floor(((p_size - (th_px - p_x0)) / r_val));
  gfx_line(th_px, th_py, p_x0 + p_size, end_py);
  gfx_circle(th_px, th_py, 5, 1);

  // Dynamic reduction meter
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_rect(p_x0 + p_size - 8, min(p_y0 + p_size, end_py), 8, floor(vocal_gr_db * 5.0));

  // Topology Pills
  t_pill_y = vg_y + vg_h - 90;
  tp_w = floor((left_w - 48) / 2);

  sel_fc = (slider14 == 0);
  hov_fc = (mouse_x >= ws_x + 24 && mouse_x <= ws_x + 24 + tp_w && mouse_y >= t_pill_y && mouse_y <= t_pill_y + 36);
  gfx_r = sel_fc ? 0.22 : 0.04; gfx_g = sel_fc ? 0.10 : 0.04; gfx_b = sel_fc ? 0.28 : 0.08;
  gfx_rect(ws_x + 24, t_pill_y, tp_w, 36);
  gfx_r = sel_fc ? 0.88 : 0.30; gfx_g = sel_fc ? 0.25 : 0.35; gfx_b = sel_fc ? 0.65 : 0.45;
  gfx_rect(ws_x + 24, t_pill_y, tp_w, 36, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = sel_fc ? 1.0 : 0.7; gfx_g = sel_fc ? 1.0 : 0.75; gfx_b = sel_fc ? 1.0 : 0.8;
  gfx_x = ws_x + 32; gfx_y = t_pill_y + 10; gfx_drawstr("FAIRCHILD 670 TUBE");
  mouse_clicked && hov_fc ? (slider14 = 0; slider_automate(););

  sel_op = (slider14 == 1);
  hov_op = (mouse_x >= ws_x + 24 + tp_w + 12 && mouse_x <= ws_x + 24 + 2 * tp_w + 12 && mouse_y >= t_pill_y && mouse_y <= t_pill_y + 36);
  gfx_r = sel_op ? 0.20 : 0.04; gfx_g = sel_op ? 0.24 : 0.04; gfx_b = sel_op ? 0.32 : 0.08;
  gfx_rect(ws_x + 24 + tp_w + 12, t_pill_y, tp_w, 36);
  gfx_r = sel_op ? 0.00 : 0.30; gfx_g = sel_op ? 0.85 : 0.35; gfx_b = sel_op ? 1.00 : 0.45;
  gfx_rect(ws_x + 24 + tp_w + 12, t_pill_y, tp_w, 36, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = sel_op ? 1.0 : 0.7; gfx_g = sel_op ? 1.0 : 0.75; gfx_b = sel_op ? 1.0 : 0.8;
  gfx_x = ws_x + 32 + tp_w + 12; gfx_y = t_pill_y + 10; gfx_drawstr("VINTAGE OPTO LA");
  mouse_clicked && hov_op ? (slider14 = 1; slider_automate(););

  // Quick Style Pills row
  sp_y = vg_y + vg_h - 44;
  sp_w = floor((left_w - 48 - 16) / 3);
  sp_i = 0;
  loop(3,
    sp_x = ws_x + 24 + sp_i * (sp_w + 8);
    sp_hov = (mouse_x >= sp_x && mouse_x <= sp_x + sp_w && mouse_y >= sp_y && mouse_y <= sp_y + 30);
    is_act = (sp_i == 0 ? (slider16 == 0 && slider17 == 20.0) : (sp_i == 1 ? (slider16 == 1 && slider17 == 12.0) : (slider16 == 3 && slider17 == 5.0)));
    gfx_r = is_act ? 0.20 : (sp_hov ? 0.10 : 0.04);
    gfx_g = is_act ? 0.12 : (sp_hov ? 0.08 : 0.05);
    gfx_b = is_act ? 0.26 : (sp_hov ? 0.14 : 0.07);
    gfx_rect(sp_x, sp_y, sp_w, 30);
    gfx_r = is_act ? 0.88 : 0.25; gfx_g = is_act ? 0.25 : 0.32; gfx_b = is_act ? 0.65 : 0.42;
    gfx_rect(sp_x, sp_y, sp_w, 30, 0);
    gfx_setfont(3, "Consolas", 11.5, 'b');
    gfx_r = is_act ? 1.0 : 0.75; gfx_g = is_act ? 1.0 : 0.80; gfx_b = is_act ? 1.0 : 0.88;
    sp_txt = (sp_i == 0 ? "SILK OPTO" : (sp_i == 1 ? "VOCAL GLUE" : "SQUEEZE 4:1"));
    gfx_measurestr(sp_txt, stw, sth);
    gfx_x = sp_x + (sp_w - stw) * 0.5; gfx_y = sp_y + 7;
    gfx_drawstr(sp_txt);
    mouse_clicked && sp_hov ? (
      sp_i == 0 ? (slider16 = 0; slider17 = 20.0; slider18 = 3; slider15 = -4.0;) :
      sp_i == 1 ? (slider16 = 1; slider17 = 12.0; slider18 = 2; slider15 = -5.5;) :
                  (slider16 = 3; slider17 = 5.0;  slider18 = 0; slider15 = -10.0;);
      update_vocal_filters();
      slider_automate();
    );
    sp_i += 1;
  );

  // Right Box: Tactile Sliders
  rx = ws_x + 12 + left_w + 16;
  gfx_r = 0.016; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(rx, vg_y, right_w, vg_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(rx, vg_y, right_w, vg_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = rx + 16; gfx_y = vg_y + 14; gfx_drawstr("MASTER VOCAL GLUE PARAMETERS");

  sl_w = right_w - 32;
  sl_h = 56;
  s_start_y = vg_y + 48;
  draw_param_slider(rx + 16, s_start_y + 0 * (sl_h + 10), sl_w, sl_h, "1. VOCAL GLUE THRESHOLD", slider15, -36.0, 0.0, "%.1f dBFS", 15, 0.88, 0.25, 0.65);
  draw_param_slider(rx + 16, s_start_y + 1 * (sl_h + 10), sl_w, sl_h, "2. COMPRESSION RATIO", slider16, 0, 3, "%d:1", 16, 0.00, 0.85, 1.00);
  draw_param_slider(rx + 16, s_start_y + 2 * (sl_h + 10), sl_w, sl_h, "3. ATTACK TIME", slider17, 0.2, 50.0, "%.1f ms", 17, 0.88, 0.25, 0.65);
  draw_param_slider(rx + 16, s_start_y + 3 * (sl_h + 10), sl_w, sl_h, "4. RELEASE BALLISTICS", slider18, 0, 4, "%d Mode", 18, 1.00, 0.85, 0.35);
  draw_param_slider(rx + 16, s_start_y + 4 * (sl_h + 10), sl_w, sl_h, "5. PARALLEL DRY / WET MIX", slider19, 0, 100, "%d %%", 19, 0.88, 0.25, 0.65);
  draw_param_slider(rx + 16, s_start_y + 5 * (sl_h + 10), sl_w, sl_h, "6. TUBE WARMTH SATURATION", slider20, 0.0, 10.0, "+%.1f dB", 20, 1.00, 0.85, 0.35);
);

// =============================================================================
// TAB 3: MASTER SIBILANCE SENTRY & TUBE WARMTH (DE-ESSER SCOPE + TUBE DRIVE)
// =============================================================================
slider1 == 3 ? (
  de_y = ws_y + 12; de_w = ws_w - 24; de_h = ws_h - 24;
  gfx_r = 0.016; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, de_y, de_w, de_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 12, de_y, de_w, de_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 28; gfx_y = de_y + 14; gfx_drawstr("MASTER SIBILANCE SENTRY // DYNAMIC SPECTRAL CLAMP & TUBE WARMTH");

  top_h = 180;
  // Sibilance Clamping Scope
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.022; gfx_rect(ws_x + 24, de_y + 44, de_w - 48, top_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, de_y + 44, de_w - 48, top_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 36; gfx_y = de_y + 56; gfx_drawstr("DYNAMIC HIGH-FREQUENCY SIBILANCE ATTENUATION SCOPE");

  d_cx0 = ws_x + 36; d_cy0 = de_y + 80; d_cw = de_w - 72; d_ch = top_h - 48;
  dy_mid = d_cy0 + d_ch * 0.3;
  gfx_r = 0.10; gfx_g = 0.16; gfx_b = 0.24;
  gfx_line(d_cx0, dy_mid, d_cx0 + d_cw, dy_mid);

  // Frequency Center Indicator
  f_pct = (slider7 - 4000.0) / 6000.0;
  fc_x = d_cx0 + floor(f_pct * d_cw);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_line(fc_x, d_cy0, fc_x, d_cy0 + d_ch);

  // Dynamic Clamping Curve
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  prev_y = dy_mid;
  pi = 0;
  loop(100,
    px = d_cx0 + floor((pi / 99.0) * d_cw);
    f_val = 3000.0 * exp(log(4.0) * (pi / 99.0));
    dip = de_gr_db * exp(-0.5 * sqr((log(f_val / slider7) / 0.25)));
    cur_y = dy_mid + dip * 15.0;
    pi > 0 ? (
      gfx_line(prev_px, prev_py, px, cur_y);
      gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
      gfx_line(px, dy_mid, px, cur_y);
    );
    prev_px = px; prev_py = cur_y;
    pi += 1;
  );

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  de_str = sprintf(#, "LIVE SIBILANCE CLAMP: -%.1f dB @ %d Hz", de_gr_db, slider7);
  gfx_measurestr(de_str, dsw, dsh);
  gfx_x = d_cx0 + floor((d_cw - dsw) * 0.5); gfx_y = dy_mid + 65;
  gfx_drawstr(de_str);

  // Controls
  draw_param_slider(ws_x + 24, de_y + 238, de_w - 48, 62, "SIBILANCE DETECTOR THRESHOLD", slider6, -36.0, 0.0, "%.1f dBFS", 6, 0.00, 0.85, 1.00);
  draw_param_slider(ws_x + 24, de_y + 308, de_w - 48, 62, "DETECTOR CENTER FREQUENCY", slider7, 4000, 10000, "%d Hz", 7, 0.88, 0.25, 0.65);
  draw_param_slider(ws_x + 24, de_y + 378, de_w - 48, 62, "MAX ATTENUATION CLAMP RANGE", slider8, -12.0, 0.0, "%.1f dB", 8, 1.00, 0.85, 0.35);

  // Delta Audition Button
  da_y = de_y + 448; da_w = de_w - 48;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.022; gfx_rect(ws_x + 24, da_y, da_w, 42);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, da_y, da_w, 42, 0);

  hov_da = (mouse_x >= ws_x + 24 && mouse_x <= ws_x + 24 + da_w && mouse_y >= da_y && mouse_y <= da_y + 42);
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 36; gfx_y = da_y + 12; gfx_drawstr("SIBILANCE DELTA AUDITION:");

  da_txt = slider9 ? "[ AUDITIONING REMOVED SIBILANCE ]" : "[ NORMAL AUDIO MONITOR ]";
  gfx_setfont(3, "Consolas", 13, 'b'); gfx_r = slider9 ? 1.00 : 0.65; gfx_g = slider9 ? 0.35 : 0.75; gfx_b = slider9 ? 0.35 : 0.85;
  gfx_measurestr(da_txt, datw, dath);
  gfx_x = ws_x + da_w - datw; gfx_y = da_y + 12; gfx_drawstr(da_txt);
  mouse_clicked && hov_da ? (slider9 = !slider9; slider_automate(););
);

// =============================================================================
// TAB 4: VOCAL SPATIAL DIMENSION (LEAD CENTER-LOCK & REVERB SPREAD)
// =============================================================================
slider1 == 4 ? (
  sp_y = ws_y + 12; sp_w = ws_w - 24; sp_h = ws_h - 24;
  gfx_r = 0.016; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, sp_y, sp_w, sp_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(ws_x + 12, sp_y, sp_w, sp_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 28; gfx_y = sp_y + 14; gfx_drawstr("VOCAL SPATIAL DIMENSION // LEAD CENTER-LOCK & REVERB SPREAD");

  top_h = 240;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.022; gfx_rect(ws_x + 24, sp_y + 44, sp_w - 48, top_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, sp_y + 44, sp_w - 48, top_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 36; gfx_y = sp_y + 56; gfx_drawstr("LEAD VOCAL CENTER ANCHOR & REVERB SIDE DEVIATION");

  r_cx = ws_x + 24 + (sp_w - 48) * 0.5; r_cy = sp_y + 44 + top_h * 0.5 + 8;
  gfx_r = 0.10; gfx_g = 0.16; gfx_b = 0.24;
  gfx_circle(r_cx, r_cy, 65, 0);
  gfx_circle(r_cx, r_cy, 40, 0);
  gfx_line(r_cx - 65, r_cy, r_cx + 65, r_cy);
  gfx_line(r_cx, r_cy - 65, r_cx, r_cy + 65);

  draw_param_slider(ws_x + 24, sp_y + 300, sp_w - 48, 62, "VOCAL SPATIAL WIDTH MULTIPLIER", slider21, 0.80, 1.40, "%.2f x", 21, 0.88, 0.25, 0.65);

  // Guidance Plaque
  adv_y = sp_y + 376; adv_h = sp_h - 390;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.022; gfx_rect(ws_x + 24, adv_y, sp_w - 48, adv_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, adv_y, sp_w - 48, adv_h, 0);
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 36; gfx_y = adv_y + 12; gfx_drawstr("SPATIAL ARCHITECTURE SPECIFICATIONS:");
  gfx_setfont(3, "Segoe UI", 13); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.96;
  gfx_x = ws_x + 36; gfx_y = adv_y + 36;
  gfx_drawstr("• Lead Center Lock: Guarantees dry lead vocal intimacy remains anchored dead-center in the mono summing corridor.");
  gfx_x = ws_x + 36; gfx_y = adv_y + 60;
  gfx_drawstr("• Reverb & Delay Spread: Width multiplier manipulates strictly stereo side ambiance without washing out dry vocal clarity.");
);

// =============================================================================
// TAB 5: DYNAMIC PRESENCE SENTRY & CORRIDOR RELAY TRANSMITTER
// =============================================================================
slider1 == 5 ? (
  pr_y = ws_y + 12; pr_w = ws_w - 24; pr_h = ws_h - 24;
  gfx_r = 0.016; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, pr_y, pr_w, pr_h);
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35; gfx_rect(ws_x + 12, pr_y, pr_w, pr_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = ws_x + 28; gfx_y = pr_y + 14; gfx_drawstr("DYNAMIC PRESENCE SENTRY // CORRIDOR CARVE TRANSMITTER");

  top_h = 240;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.022; gfx_rect(ws_x + 24, pr_y + 44, pr_w - 48, top_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, pr_y + 44, pr_w - 48, top_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = ws_x + 36; gfx_y = pr_y + 56; gfx_drawstr("CORRIDOR ENERGY MONITOR & INSTRUMENTAL NOTCH BROADCAST");

  // Telemetry Bar
  gfx_setfont(3, "Consolas", 13, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.96;
  gfx_x = ws_x + 36; gfx_y = pr_y + 90; gfx_printf("Live Vocal Master Energy (gmem[1452]): %4.1f dBFS", vocal_rms);
  gfx_x = ws_x + 36; gfx_y = pr_y + 120; gfx_printf("Presence Sensitivity Boost           : +%.1f dB", slider26);
  gfx_x = ws_x + 36; gfx_y = pr_y + 150; gfx_printf("Autonomous Corridor Request State    : %s", slider27 ? "ACTIVE BROADCASTING" : "STANDBY");

  draw_param_slider(ws_x + 24, pr_y + 300, pr_w - 48, 62, "PRESENCE SENTRY SENSITIVITY", slider26, 0.0, 3.0, "+%.1f dB", 26, 1.00, 0.85, 0.35);

  // Broadcast toggle
  br_y = pr_y + 372; br_w = pr_w - 48;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.022; gfx_rect(ws_x + 24, br_y, br_w, 42);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, br_y, br_w, 42, 0);

  hov_br = (mouse_x >= ws_x + 24 && mouse_x <= ws_x + 24 + br_w && mouse_y >= br_y && mouse_y <= br_y + 42);
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = ws_x + 36; gfx_y = br_y + 12; gfx_drawstr("DYNAMIC CORRIDOR REQUEST BROADCAST:");

  br_txt = slider27 ? "[ ACTIVE GMEM RELAY TRANSMITTING ]" : "[ TRANSMISSION STANDBY ]";
  gfx_setfont(3, "Consolas", 13, 'b'); gfx_r = slider27 ? 0.00 : 1.00; gfx_g = slider27 ? 0.95 : 0.85; gfx_b = slider27 ? 0.65 : 0.30;
  gfx_measurestr(br_txt, brtw, brth);
  gfx_x = ws_x + br_w - brtw; gfx_y = br_y + 12; gfx_drawstr(br_txt);
  mouse_clicked && hov_br ? (slider27 = !slider27; slider_automate(););

  // Advice
  adv_y = pr_y + 424; adv_h = pr_h - 438;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.022; gfx_rect(ws_x + 24, adv_y, pr_w - 48, adv_h);
  gfx_r = 0.18; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, adv_y, pr_w - 48, adv_h, 0);
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = ws_x + 36; gfx_y = adv_y + 12; gfx_drawstr("PRESENCE CORRIDOR RELAY ARCHITECTURE:");
  gfx_setfont(3, "Segoe UI", 13); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.96;
  gfx_x = ws_x + 36; gfx_y = adv_y + 36;
  gfx_drawstr("• Autonomous Relay: Transmits instant vocal energy telemetry to Damei Instrumental Bus Alchemist via gmem[1452].");
  gfx_x = ws_x + 36; gfx_y = adv_y + 60;
  gfx_drawstr("• Instrumental Mid Carve: Commands the instrumental bus to notch 2.2 kHz seamlessly without degrading guitar wall width.");
);

// =============================================================================
// TAB 6: PRODUCER SUMMING MATRIX (25 CLICKABLE TILES + VOCAL FORENSIC PLAQUE)
// =============================================================================
slider1 == 6 ? (
  pm_y = ws_y + 12; pm_w = ws_w - 24; pm_h = ws_h - 24;
  gfx_r = 0.016; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 12, pm_y, pm_w, pm_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(ws_x + 12, pm_y, pm_w, pm_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 28; gfx_y = pm_y + 14; gfx_drawstr("MASTER VOCAL PRODUCER MATRIX // 25 REFERENCE-CALIBRATED BENCHMARKS");

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

    gfx_r = is_sel ? 0.24 : (b_hov ? 0.12 : 0.035);
    gfx_g = is_sel ? 0.10 : (b_hov ? 0.06 : 0.030);
    gfx_b = is_sel ? 0.20 : (b_hov ? 0.10 : 0.055);
    gfx_rect(bx, by, btn_w, bh);

    gfx_r = is_sel ? 0.88 : (b_hov ? 0.50 : 0.20);
    gfx_g = is_sel ? 0.25 : (b_hov ? 0.25 : 0.28);
    gfx_b = is_sel ? 0.65 : (b_hov ? 0.40 : 0.38);
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

  plaque_y = pm_y + 44 + 4 * 40 + 8;
  plaque_h = pm_h - (plaque_y - pm_y) - 14;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.022; gfx_rect(ws_x + 24, plaque_y, pm_w - 48, plaque_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(ws_x + 24, plaque_y, pm_w - 48, plaque_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.40;
  gfx_x = ws_x + 38; gfx_y = plaque_y + 16;
  gfx_printf("SELECTED BENCHMARK: %02d - %s", slider2, get_producer_full_title(slider2));

  gfx_setfont(3, "Consolas", 13, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 38; gfx_y = plaque_y + 45;
  spec_str = sprintf(#, "CALIBRATION: Trim %+4.1fdB | De-Esser %.1fdB @ %dHz | Bax Air %+4.1fdB | Tube Drive +%.1fdB | Width %.2fx",
    slider4, slider6, slider7, slider12, slider20, slider21);
  gfx_drawstr(spec_str);

  gfx_setfont(3, "Segoe UI", 13.5); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = ws_x + 38; gfx_y = plaque_y + 75;
  gfx_drawstr("Full master vocal forensic acoustic profile matching reference benchmarks. Recalls authentic Fairchild variable-mu glue,");
  gfx_x = ws_x + 38; gfx_y = plaque_y + 98;
  gfx_drawstr("tube saturation warmth, precision Baxandall tone curves, and high-frequency sibilance suppression.");

  sub_w = floor((pm_w - 96) / 2); sub_y = plaque_y + 126; sub_h = plaque_h - 138;
  // Left: Tone & Sibilance Specs
  gfx_r = 0.016; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 38, sub_y, sub_w, sub_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(ws_x + 38, sub_y, sub_w, sub_h, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 48; gfx_y = sub_y + 8; gfx_drawstr("VOCAL TONE & DE-ESSER SENTRY");
  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.96;
  gfx_x = ws_x + 48; gfx_y = sub_y + 30; gfx_printf("De-Esser Threshold: %.1f dBFS", slider6);
  gfx_x = ws_x + 48; gfx_y = sub_y + 50; gfx_printf("De-Esser Frequency: %d Hz (Sharp)", slider7);
  gfx_x = ws_x + 48; gfx_y = sub_y + 70; gfx_printf("Baxandall 100Hz   : %+4.1f dB (Chest Shelf)", slider10);
  gfx_x = ws_x + 48; gfx_y = sub_y + 90; gfx_printf("Baxandall 3.5kHz  : %+4.1f dB (Presence)", slider11);
  gfx_x = ws_x + 48; gfx_y = sub_y + 110; gfx_printf("Baxandall 12kHz   : %+4.1f dB (Silk Air)", slider12);

  // Right: Dynamics & Corridor Specs
  gfx_r = 0.016; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(ws_x + 48 + sub_w, sub_y, sub_w, sub_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 48 + sub_w, sub_y, sub_w, sub_h, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 8; gfx_drawstr("FAIRCHILD GLUE & CORRIDOR RELAY");
  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.96;
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 30; gfx_printf("Glue Topology     : %s", slider14 ? "Vintage Opto LA" : "Fairchild 670 Tube");
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 50; gfx_printf("Glue Threshold    : %.1f dB | Ratio %s", slider15, slider16 == 0 ? "1.5:1" : (slider16 == 1 ? "2:1" : (slider16 == 2 ? "3:1" : "4:1")));
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 70; gfx_printf("Tube Saturation   : +%.1f dB Warmth THD", slider20);
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 90; gfx_printf("Spatial Lead Lock : %.2f x Multiplier", slider21);
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 110; gfx_printf("Corridor Broadcast: %s", slider27 ? "ACTIVE RELAY" : "STANDBY");
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
"""

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

shutil.copy2(target_path, reaper_path)
print("Successfully generated and deployed Damei_VocalBus.jsfx")
