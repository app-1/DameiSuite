# gen_vocal_flagship_v5.py
import os, shutil

target_path = r"c:\Dev\DameiSuite\effects\Damei_VocalBus.jsfx"
reaper_path = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_VocalBus.jsfx"

with open(target_path, "w", encoding="utf-8") as f:
    f.write(r"""desc:Damei Vocal Empress (Imperial Sceptre & Master Vocal Sum)
// =============================================================================
// DAMEI SUITE // 2026 REAPER MASTER SUMMING INFRASTRUCTURE
// ARCHETYPE: DUAFE (The Wooden Comb - Pristine Grooming, Refinement & Royalty)
// FLAGSHIP AFRO-CYBERNETIC LUXURY CONSOLE SURFACE ARCHITECTURE (@gfx 1080 700)
// =============================================================================

slider1:0<0,6,1{0: OVERVIEW, 1: BAXANDALL, 2: VOCAL GLUE, 3: DE-ESSER, 4: SPATIAL, 5: PRESENCE, 6: PRODUCER}>-Active Navigation Tab
slider2:6<0,24,1{00: Unity Baseline (1:1 Transparent Pass), 01: Lance Prenc (Alpha Wolf - 60cm Of Steel), 02: Scott Seigel (DIESECT - TOO MANY SCARS), 03: Jonathan Dolese (Mirrorcell - U(phoria)), 04: Buster Odeholm (thrown / Northlane - Evian), 05: Lewis Johns (Love Is Noise / blanket - Blur), 06: Kel Pinchin (Split Chain - I'm Not Dying To Be Here), 07: Dan Lancaster & Jason Perry (Don Broco - Endorphins), 08: Erik Bickerstaffe (Static Dress - face..), 09: Sam Guaiana (Silverstein - Misery Made Me), 10: Zach Tuch (Heavenward - Tangerine), 11: Forrester Savell (City Of Souls - Cruelty / Karnivool), 12: Leon Schmidt (SUNBORN - Nebula), 13: Ermin Hamidovic (Systematic / 01 The End of All We Know), 14: Will Putney (Fit For An Autopsy - Walk With Me In Hell), 15: George Lever (Loathe - Agressive Evolution / Sleep Token), 16: Sam Bassal (Thornhill - nerv), 17: Henrik Udd (Architects - 8. Gravity), 18: Dan Braunstein (Spiritbox - Keep Sweet), 19: Zakk Cervini & Erik Ron (Bad Omens - THE DEATH OF PEACE OF MIND), 20: Jens Bogren (Fascination Street Studios Benchmark), 21: Adam Nolly Getgood (Periphery / GGD Modern Metal Target), 22: Acle Kahney (TesseracT - King), 23: Adam Cichocki (heaving. - carsick), 24: Manuel Renner (SENNA - Out Of The Blue)}>-Producer Reference Benchmark
slider3:0<-6.0,6.0,0.1>-Input Calibration Gain (dB)
slider4:-2.5<-6.0,6.0,0.1>-Producer Headroom Trim (dB)
slider5:0<0,1,1{Free Output, -6.0 dBTP Strict Pre-Master Lock}>-Headroom Guardian Mode
slider6:-19.0<-36.0,0.0,0.5>-Master De-Esser Threshold (dB)
slider7:6800<4000,10000,50>-Master De-Esser Frequency (Hz)
slider8:-7.0<-12.0,0.0,0.5>-Master De-Esser Max Range (dB)
slider9:0<0,1,1{Normal Audio, Audition Clamped Sibilance}>-De-Esser Delta Audition
slider10:1.2<-6.0,6.0,0.1>-Baxandall 100Hz Warmth (dB)
slider11:2.8<-6.0,6.0,0.1>-Baxandall 3.5kHz Presence (dB)
slider12:3.8<-6.0,6.0,0.1>-Baxandall 12kHz Silk Air (dB)
slider13:1<0,1,1{Bypass, Engaged}>-Master Vocal Bus Glue Compressor
slider14:0<0,1,1{Fairchild 670 Smooth Tube, Vintage Opto Leveler}>-Glue Topology
slider15:-5.5<-36.0,0.0,0.5>-Vocal Glue Threshold (dB)
slider16:1<0,3,1{1.5:1 Smooth Vocal, 2:1 Master Sum, 3:1 Cohesion, 4:1 Radio Glue}>-Vocal Glue Ratio
slider17:12.0<0.2,50.0,0.5>-Vocal Glue Attack (ms)
slider18:1<0,4,1{100ms Fast, 300ms Vocal Natural, 600ms Silk Opto, 1200ms Lush, Auto Ballistics}>-Vocal Glue Release
slider19:100<0,100,1>-Vocal Glue Dry/Wet Mix (%)
slider20:3.2<0.0,10.0,0.1>-Vocal Tube Warmth Saturation (dB)
slider21:1.08<0.80,1.40,0.01>-Vocal Spatial Width (Lead Center Lock)
slider22:0<0,2,1{Manual Standby, Local Ollama / HF Audit, Safe Auto-Calibrate (±0.5dB Max)}>-AI Vocal Assistant Engine
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

bax_w_x1_l = 0; bax_w_x2_l = 0; bax_w_y1_l = 0; bax_w_y2_l = 0;
bax_w_x1_r = 0; bax_w_x2_r = 0; bax_w_y1_r = 0; bax_w_y2_r = 0;

bax_p_x1_l = 0; bax_p_x2_l = 0; bax_p_y1_l = 0; bax_p_y2_l = 0;
bax_p_x1_r = 0; bax_p_x2_r = 0; bax_p_y1_r = 0; bax_p_y2_r = 0;

bax_a_x1_l = 0; bax_a_x2_l = 0; bax_a_y1_l = 0; bax_a_y2_l = 0;
bax_a_x1_r = 0; bax_a_x2_r = 0; bax_a_y1_r = 0; bax_a_y2_r = 0;

de_bp_x1_l = 0; de_bp_x2_l = 0; de_bp_y1_l = 0; de_bp_y2_l = 0;
de_bp_x1_r = 0; de_bp_x2_r = 0; de_bp_y1_r = 0; de_bp_y2_r = 0;
de_env_smooth = 0.0;
de_gr_db = 0.0;

vu_rms_smooth = 0.0;
vocal_peak = 0.0;
vocal_rms = -90.0;
vocal_gr_db = 0.0;
sifam_vocal_vu = -20.0;
sifam_vocal_gr = 0.0;

rms_acc_l = 0.0; rms_acc_r = 0.0; rms_cnt = 0;

scope_buf_l = 4000;
scope_buf_r = 4300;
scope_pos = 0;

gmem[1450] = 1;

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

function update_vocal_filters() local(w0, cos_w0, sin_w0, alpha, A, beta) (
  srate <= 0 ? srate = 44100;

  // 1. Baxandall 100Hz Warmth Shelf (slider10)
  A = exp(slider10 * 0.0575646273);
  w0 = 2.0 * M_PI * 100.0 / srate;
  cos_w0 = cos(w0); sin_w0 = sin(w0);
  alpha = sin_w0 / (2.0 * 0.7071);
  beta = 2.0 * sqrt(A) * alpha;
  bw_b0 = A * ((A + 1.0) - (A - 1.0) * cos_w0 + beta);
  bw_b1 = 2.0 * A * ((A - 1.0) - (A + 1.0) * cos_w0);
  bw_b2 = A * ((A + 1.0) - (A - 1.0) * cos_w0 - beta);
  bw_a0 = (A + 1.0) + (A - 1.0) * cos_w0 + beta;
  bw_a1 = -2.0 * ((A - 1.0) + (A + 1.0) * cos_w0);
  bw_a2 = (A + 1.0) + (A - 1.0) * cos_w0 - beta;

  // 2. Baxandall 3.5kHz Presence Bell (slider11)
  A = exp(slider11 * 0.0575646273);
  w0 = 2.0 * M_PI * 3500.0 / srate;
  alpha = sin(w0) / (2.0 * 0.85);
  bp_b0 = 1.0 + alpha * A;
  bp_b1 = -2.0 * cos(w0);
  bp_b2 = 1.0 - alpha * A;
  bp_a0 = 1.0 + alpha / A;
  bp_a1 = -2.0 * cos(w0);
  bp_a2 = 1.0 - alpha / A;

  // 3. Baxandall 12kHz Silk Air Shelf (slider12)
  A = exp(slider12 * 0.0575646273);
  w0 = 2.0 * M_PI * 12000.0 / srate;
  cos_w0 = cos(w0); sin_w0 = sin(w0);
  alpha = sin_w0 / (2.0 * 0.7071);
  beta = 2.0 * sqrt(A) * alpha;
  ba_b0 = A * ((A + 1.0) + (A - 1.0) * cos_w0 + beta);
  ba_b1 = -2.0 * A * ((A - 1.0) + (A + 1.0) * cos_w0);
  ba_b2 = A * ((A + 1.0) + (A - 1.0) * cos_w0 - beta);
  ba_a0 = (A + 1.0) - (A - 1.0) * cos_w0 + beta;
  ba_a1 = 2.0 * ((A - 1.0) - (A + 1.0) * cos_w0);
  ba_a2 = (A + 1.0) - (A - 1.0) * cos_w0 - beta;

  // 4. De-Esser Detector Bandpass Filter (slider7)
  de_f0 = clamp(slider7, 4000.0, 10000.0);
  w0 = 2.0 * M_PI * de_f0 / srate;
  alpha = sin(w0) / (2.0 * 2.2);
  de_b0 = alpha;
  de_b1 = 0.0;
  de_b2 = -alpha;
  de_a0 = 1.0 + alpha;
  de_a1 = -2.0 * cos(w0);
  de_a2 = 1.0 - alpha;
);

function apply_producer_preset(idx) (
  idx == 0 ? ( // Unity Baseline (1:1 Transparent Pass)
    slider3 = 0.0; slider4 = 0.0; slider5 = 0; slider6 = -18.0; slider7 = 6800;
    slider8 = 0.0; slider9 = 0; slider10 = 0.0; slider11 = 0.0; slider12 = 0.0;
    slider13 = 1; slider14 = 0; slider15 = 0.0; slider16 = 1; slider17 = 15.0;
    slider18 = 2; slider19 = 100; slider20 = 0.0; slider21 = 1.00;
  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target) - Calibrated for Vocal Lead Sum
    slider3 = 0.0; slider4 = -2.5; slider5 = 0;
    slider6 = -19.0; slider7 = 6800; slider8 = -7.0; slider9 = 0;
    slider10 = 1.2; slider11 = 2.8; slider12 = 3.8;
    slider13 = 1; slider14 = 0; slider15 = -5.5; slider16 = 1; slider17 = 12.0;
    slider18 = 1; slider19 = 100; slider20 = 3.2; slider21 = 1.08;
  ) : idx == 1 ? ( // Lance Prenc (Alpha Wolf - 60cm Of Steel)
    slider3 = 0.0; slider4 = -2.0; slider5 = 0;
    slider6 = -20.0; slider7 = 6500; slider8 = -8.0; slider9 = 0;
    slider10 = 1.0; slider11 = 3.5; slider12 = 3.0;
    slider13 = 1; slider14 = 0; slider15 = -6.5; slider16 = 2; slider17 = 8.0;
    slider18 = 0; slider19 = 100; slider20 = 3.8; slider21 = 1.05;
  ) : idx == 4 ? ( // Buster Odeholm (thrown / Northlane - Evian)
    slider3 = 0.0; slider4 = -2.8; slider5 = 0;
    slider6 = -22.0; slider7 = 6200; slider8 = -9.0; slider9 = 0;
    slider10 = 0.5; slider11 = 4.0; slider12 = 3.5;
    slider13 = 1; slider14 = 0; slider15 = -7.5; slider16 = 3; slider17 = 5.0;
    slider18 = 0; slider19 = 100; slider20 = 4.5; slider21 = 1.00;
  ) : idx == 18 ? ( // Dan Braunstein (Spiritbox - Keep Sweet)
    slider3 = 0.0; slider4 = -2.2; slider5 = 0;
    slider6 = -18.0; slider7 = 7000; slider8 = -6.5; slider9 = 0;
    slider10 = 1.0; slider11 = 2.5; slider12 = 4.0;
    slider13 = 1; slider14 = 0; slider15 = -5.0; slider16 = 1; slider17 = 15.0;
    slider18 = 1; slider19 = 100; slider20 = 2.8; slider21 = 1.10;
  ) : ( // Modern Metal Vocal Standard Fallback
    slider3 = 0.0; slider4 = -2.0; slider5 = 0;
    slider6 = -18.0; slider7 = 6800; slider8 = -6.0; slider9 = 0;
    slider10 = 1.0; slider11 = 2.5; slider12 = 3.0;
    slider13 = 1; slider14 = 0; slider15 = -5.0; slider16 = 1; slider17 = 12.0;
    slider18 = 1; slider19 = 100; slider20 = 2.5; slider21 = 1.05;
  );
  update_vocal_filters();
  slider_automate();
);

function trigger_vocal_ai_assist() local(delta_trim) (
  vocal_peak > 0.001 ? (
    delta_trim = clamp(-6.0 - (20.0 * log10(vocal_peak)), -0.5, 0.5);
    slider4 = clamp(slider4 + delta_trim, -6.0, 1.0);
  );
  update_vocal_filters();
  slider_automate();
);

update_vocal_filters();
apply_producer_preset(slider2);

@slider
prev_preset != slider2 ? (
  apply_producer_preset(slider2);
  prev_preset = slider2;
);
slider22 == 2 ? (
  trigger_vocal_ai_assist();
  slider22 = 1;
);
update_vocal_filters();

@sample
srate <= 0 ? srate = 44100;
dry_l = spl0; dry_r = spl1;

vu_omega = 1.0 - exp(-1.0 / (srate * 0.300));
vu_sig_sq = (dry_l * dry_l + dry_r * dry_r) * 0.5;
vu_rms_smooth += (vu_sig_sq - vu_rms_smooth) * vu_omega;
(vu_rms_smooth != vu_rms_smooth || vu_rms_smooth <= 0.000000001) ? (
  vocal_rms = -90.0;
) : (
  vocal_rms = 10.0 * log10(vu_rms_smooth);
);
vocal_peak = max(abs(dry_l), abs(dry_r));

scope_pos = (scope_pos + 1) % 256;
scope_buf_l[scope_pos] = dry_l;
scope_buf_r[scope_pos] = dry_r;

// 1:1 Complete Bit-Exact Passthrough if Preset 00 (Unity Baseline)
slider2 == 0 ? (
  spl0 = dry_l; spl1 = dry_r;
) : (
  // 1. Input Gain Calibration
  in_gain = exp(slider3 * 0.1151292546);
  in_l = dry_l * in_gain;
  in_r = dry_r * in_gain;

  // 2. Master Vocal De-Esser (Sibilance Sentry)
  de_det_l = (de_b0 * in_l + de_b1 * de_bp_x1_l + de_b2 * de_bp_x2_l - de_a1 * de_bp_y1_l - de_a2 * de_bp_y2_l) / de_a0;
  de_bp_x2_l = de_bp_x1_l; de_bp_x1_l = in_l; de_bp_y2_l = de_bp_y1_l; de_bp_y1_l = de_det_l;
  de_det_r = (de_b0 * in_r + de_b1 * de_bp_x1_r + de_b2 * de_bp_x2_r - de_a1 * de_bp_y1_r - de_a2 * de_bp_y2_r) / de_a0;
  de_bp_x2_r = de_bp_x1_r; de_bp_x1_r = in_r; de_bp_y2_r = de_bp_y1_r; de_bp_y1_r = de_det_r;

  de_pk = max(abs(de_det_l), abs(de_det_r));
  de_db = de_pk > 0.000000001 ? 20.0 * log10(de_pk) : -120.0;

  de_atk = exp(-1.0 / (srate * 0.001));
  de_rel = exp(-1.0 / (srate * 0.040));
  de_db > de_env_smooth ? (
    de_env_smooth = de_db + (de_env_smooth - de_db) * de_atk;
  ) : (
    de_env_smooth = de_db + (de_env_smooth - de_db) * de_rel;
  );

  de_over = de_env_smooth - slider6;
  de_over > 0.0 ? (
    de_gr_db = min(abs(slider8), de_over * 0.75);
  ) : (
    de_gr_db = 0.0;
  );

  de_gain = exp(-de_gr_db * 0.1151292546);
  slider9 ? ( // Sibilance delta audition
    de_out_l = (in_l - in_l * de_gain);
    de_out_r = (in_r - in_r * de_gain);
  ) : (
    de_out_l = in_l * de_gain;
    de_out_r = in_r * de_gain;
  );

  // 3. Baxandall Smooth Vocal Equalizer
  // Band 1: 100Hz Warmth Shelf
  w_l = (bw_b0 * de_out_l + bw_b1 * bax_w_x1_l + bw_b2 * bax_w_x2_l - bw_a1 * bax_w_y1_l - bw_a2 * bax_w_y2_l) / bw_a0;
  bax_w_x2_l = bax_w_x1_l; bax_w_x1_l = de_out_l; bax_w_y2_l = bax_w_y1_l; bax_w_y1_l = w_l;
  w_r = (bw_b0 * de_out_r + bw_b1 * bax_w_x1_r + bw_b2 * bax_w_x2_r - bw_a1 * bax_w_y1_r - bw_a2 * bax_w_y2_r) / bw_a0;
  bax_w_x2_r = bax_w_x1_r; bax_w_x1_r = de_out_r; bax_w_y2_r = bax_w_y1_r; bax_w_y1_r = w_r;

  // Band 2: 3.5kHz Presence Bell
  p_l = (bp_b0 * w_l + bp_b1 * bax_p_x1_l + bp_b2 * bax_p_x2_l - bp_a1 * bax_p_y1_l - bp_a2 * bax_p_y2_l) / bp_a0;
  bax_p_x2_l = bax_p_x1_l; bax_p_x1_l = w_l; bax_p_y2_l = bax_p_y1_l; bax_p_y1_l = p_l;
  p_r = (bp_b0 * w_r + bp_b1 * bax_p_x1_r + bp_b2 * bax_p_x2_r - bp_a1 * bax_p_y1_r - bp_a2 * bax_p_y2_r) / bp_a0;
  bax_p_x2_r = bax_p_x1_r; bax_p_x1_r = w_r; bax_p_y2_r = bax_p_y1_r; bax_p_y1_r = p_r;

  // Band 3: 12kHz Silk Air Shelf
  bax_out_l = (ba_b0 * p_l + ba_b1 * bax_a_x1_l + ba_b2 * bax_a_x2_l - ba_a1 * bax_a_y1_l - ba_a2 * bax_a_y2_l) / ba_a0;
  bax_a_x2_l = bax_a_x1_l; bax_a_x1_l = p_l; bax_a_y2_l = bax_a_y1_l; bax_a_y1_l = bax_out_l;
  bax_out_r = (ba_b0 * p_r + ba_b1 * bax_a_x1_r + ba_b2 * bax_a_x2_r - ba_a1 * bax_a_y1_r - ba_a2 * bax_a_y2_r) / ba_a0;
  bax_a_x2_r = bax_a_x1_r; bax_a_x1_r = p_r; bax_a_y2_r = bax_a_y1_r; bax_a_y1_r = bax_out_r;

  // 4. Vocal Tube Warmth Saturation
  slider20 > 0.05 ? (
    tube_drive = exp(slider20 * 0.1151292546);
    sat_l = bax_out_l * tube_drive; sat_r = bax_out_r * tube_drive;
    tube_out_l = (sat_l - 0.10 * sat_l * sat_l + 0.03 * sat_l * sat_l * sat_l) / tube_drive;
    tube_out_r = (sat_r - 0.10 * sat_r * sat_r + 0.03 * sat_r * sat_r * sat_r) / tube_drive;
  ) : (
    tube_out_l = bax_out_l; tube_out_r = bax_out_r;
  );

  // 5. Master Vocal Glue Compressor (Fairchild 670 / Vintage Opto)
  slider13 ? (
    det_sig = (tube_out_l + tube_out_r) * 0.5;
    det_pk = abs(det_sig);
    det_db = det_pk > 0.000000001 ? 20.0 * log10(det_pk) : -120.0;

    v_atk_coeff = exp(-1.0 / (srate * (slider17 * 0.001)));
    v_rel_time = slider18 == 0 ? 0.100 : (slider18 == 1 ? 0.300 : (slider18 == 2 ? 0.600 : (slider18 == 3 ? 1.200 : 0.400)));
    v_rel_coeff = exp(-1.0 / (srate * v_rel_time));

    det_db > vocal_env ? (
      vocal_env = det_db + (vocal_env - det_db) * v_atk_coeff;
    ) : (
      vocal_env = det_db + (vocal_env - det_db) * v_rel_coeff;
    );

    v_ratio = slider16 == 0 ? 1.5 : (slider16 == 1 ? 2.0 : (slider16 == 2 ? 3.0 : 4.0));
    v_over = vocal_env - slider15;
    v_over > 0.0 ? (
      vocal_gr_db = v_over * (1.0 - 1.0 / v_ratio);
    ) : (
      vocal_gr_db = 0.0;
    );

    v_glue_gain = exp(-vocal_gr_db * 0.1151292546);
    v_mix_frac = slider19 * 0.01;
    comp_l = tube_out_l * v_glue_gain * v_mix_frac + tube_out_l * (1.0 - v_mix_frac);
    comp_r = tube_out_r * v_glue_gain * v_mix_frac + tube_out_r * (1.0 - v_mix_frac);
  ) : (
    comp_l = tube_out_l; comp_r = tube_out_r;
    vocal_gr_db = 0.0;
  );

  // 6. Lead Center-Lock Spatial Width Multiplier
  mid_vox = (comp_l + comp_r) * 0.5;
  side_vox = (comp_l - comp_r) * 0.5;
  side_vox_out = side_vox * slider21;
  vox_sum_l = mid_vox + side_vox_out;
  vox_sum_r = mid_vox - side_vox_out;

  // 7. Output Trim & Pre-Master Ceiling Guardian
  trim_gain = exp(slider4 * 0.1151292546);
  final_l = vox_sum_l * trim_gain;
  final_r = vox_sum_r * trim_gain;

  slider5 ? (
    ceil_lin = exp(-6.0 * 0.1151292546);
    final_l = clamp(final_l, -ceil_lin, ceil_lin);
    final_r = clamp(final_r, -ceil_lin, ceil_lin);
  );

  slider23 ? ( // Delta Solo Audition
    spl0 = final_l - dry_l;
    spl1 = final_r - dry_r;
  ) : (
    spl0 = final_l;
    spl1 = final_r;
  );
);

// Needle Ballistics (SIFAM VU & GR)
vu_target = clamp(vocal_rms + 18.0, -20.0, 3.0);
sifam_vocal_vu += (vu_target - sifam_vocal_vu) * 0.08;
gr_target = clamp(vocal_gr_db, 0.0, 20.0);
sifam_vocal_gr += (gr_target - sifam_vocal_gr) * 0.12;

rms_acc_l += spl0 * spl0; rms_acc_r += spl1 * spl1; rms_cnt += 1;
rms_cnt >= 2048 ? (
  gmem[1401] = 10.0 * log10(max(0.000000001, (rms_acc_l + rms_acc_r) / (2.0 * rms_cnt)));
  gmem[1451] = vocal_gr_db;
  gmem[1452] = vocal_rms;
  rms_acc_l = 0.0; rms_acc_r = 0.0; rms_cnt = 0;
);

@gfx 1080 700
// =============================================================================
// FLAGSHIP AFRO-CYBERNETIC LUXURY VOCAL EMPRESS SURFACE ARCHITECTURE
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

// Outer Obsidian Titanium Enclosure
gfx_r = 0.015; gfx_g = 0.016; gfx_b = 0.022;
gfx_rect(0, 0, gfx_w, gfx_h);

// Royal Magenta Dual Border
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
gfx_rect(8, 8, gfx_w - 16, gfx_h - 16, 0);
gfx_r = 0.44; gfx_g = 0.12; gfx_b = 0.32;
gfx_rect(9, 9, gfx_w - 18, gfx_h - 18, 0);

// Hardware Corner Bevels & Hex Bolts
c_sz = 16;
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
gfx_line(8, 8 + c_sz, 8 + c_sz, 8);
gfx_line(gfx_w - 8 - c_sz, 8, gfx_w - 8, 8 + c_sz);
gfx_line(8, gfx_h - 8 - c_sz, 8 + c_sz, gfx_h - 8);
gfx_line(gfx_w - 8 - c_sz, gfx_h - 8, gfx_w - 8, gfx_h - 8 - c_sz);

function draw_hex_bolt(bx, by) (
  gfx_r = 0.22; gfx_g = 0.26; gfx_b = 0.32; gfx_circle(bx, by, 5, 1);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_circle(bx, by, 5, 0);
  gfx_r = 0.05; gfx_g = 0.08; gfx_b = 0.12; gfx_circle(bx, by, 2, 1);
);
draw_hex_bolt(18, 18);
draw_hex_bolt(gfx_w - 18, 18);
draw_hex_bolt(18, gfx_h - 18);
draw_hex_bolt(gfx_w - 18, gfx_h - 18);

// Master Title Ribbon
hdr_h = 52;
gfx_r = 0.024; gfx_g = 0.026; gfx_b = 0.038;
gfx_rect(16, 16, gfx_w - 32, hdr_h);
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
gfx_rect(16, 16, gfx_w - 32, hdr_h, 0);

// Duafe Comb Royal Emblem with Dynamic Vocal Pulse
r_pulse = 1.0 + max(0.0, (vocal_rms + 35.0) / 45.0) * 0.25;
sig_cx = 36; sig_cy = 16 + hdr_h * 0.5;
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_a = 0.25;
gfx_circle(sig_cx, sig_cy, floor(15 * r_pulse), 0);
gfx_a = 1.0;
gfx_circle(sig_cx, sig_cy, 12, 0);
gfx_circle(sig_cx, sig_cy, 7, 0);
gfx_circle(sig_cx, sig_cy, 3, 1);

gfx_setfont(1, "Orbitron", 14, 'b');
gfx_r = 0.98; gfx_g = 0.88; gfx_b = 0.95;
title_str = "DAMEI // VOCAL BUS";
gfx_measurestr(title_str, tw, th);
gfx_x = 58; gfx_y = 16 + floor((hdr_h - th) * 0.5);
gfx_drawstr(title_str);

// Producer Benchmark Dropdown Selector Header
btn_y = 24; btn_h = 36;
p_bx = 58 + tw + 34;
p_bw = 250;

// Arrow buttons: dark slate background, magenta border, high-contrast text
arr_hov_l = (mouse_x >= p_bx - 26 && mouse_x <= p_bx - 2 && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);
gfx_r = arr_hov_l ? 0.12 : 0.025; gfx_g = arr_hov_l ? 0.06 : 0.032; gfx_b = arr_hov_l ? 0.18 : 0.044;
gfx_rect(p_bx - 26, btn_y, 24, btn_h);
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
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
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
gfx_rect(p_bx, btn_y, p_bw, btn_h, 0);

gfx_setfont(1, "Orbitron", 12.5, 'b');
gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
p_str = get_producer_short_name(slider2);
gfx_measurestr(p_str, pw, ph);
gfx_x = p_bx + floor((p_bw - pw) * 0.5); gfx_y = btn_y + floor((btn_h - ph) * 0.5);
gfx_drawstr(p_str);

// Right Arrow
arr_hov_r = (mouse_x >= p_bx + p_bw + 2 && mouse_x <= p_bx + p_bw + 26 && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);
gfx_r = arr_hov_r ? 0.12 : 0.025; gfx_g = arr_hov_r ? 0.06 : 0.032; gfx_b = arr_hov_r ? 0.18 : 0.044;
gfx_rect(p_bx + p_bw + 2, btn_y, 24, btn_h);
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
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
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
gfx_rect(b5_x, btn_y, b5_w, btn_h, 0);
gfx_setfont(2, "Orbitron", 10.5, 'b');
gfx_measurestr("ENGAGED", ew, eh);
gfx_x = b5_x + floor((b5_w - ew) * 0.5); gfx_y = btn_y + floor((btn_h - eh) * 0.5);
gfx_drawstr("ENGAGED");

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
mode_str = "MODE: MASTER";
gfx_measurestr(mode_str, mw, mh);
gfx_x = b3_x + floor((b3_w - mw) * 0.5); gfx_y = btn_y + floor((btn_h - mh) * 0.5);
gfx_drawstr(mode_str);

// 2. Music Bus Energy Relay
b2_w = 94; b2_x = b3_x - 6 - b2_w;
mus_rms = gmem[1402];
gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.022; gfx_rect(b2_x, btn_y, b2_w, btn_h);
gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(b2_x, btn_y, b2_w, btn_h, 0);
v_str = sprintf(#, "MUS: %4.1fdB", mus_rms);
gfx_measurestr(v_str, vw, vh);
gfx_x = b2_x + floor((b2_w - vw) * 0.5); gfx_y = btn_y + floor((btn_h - vh) * 0.5);
gfx_drawstr(v_str);

// 1. Chorus Sync
b1_w = 90; b1_x = b2_x - 6 - b1_w;
gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.022; gfx_rect(b1_x, btn_y, b1_w, btn_h);
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(b1_x, btn_y, b1_w, btn_h, 0);
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
    gfx_r = 0.065; gfx_g = 0.075; gfx_b = 0.100; gfx_rect(tx, tab_y, tab_w - 4, tab_h);
    gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(tx, tab_y, tab_w - 4, tab_h, 0);
    gfx_rect(tx, tab_y + tab_h - 4, tab_w - 4, 4);
    gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.95;
  ) : (
    gfx_r = hov ? 0.035 : 0.022; gfx_g = hov ? 0.045 : 0.028; gfx_b = hov ? 0.060 : 0.038;
    gfx_rect(tx, tab_y, tab_w - 4, tab_h);
    gfx_r = 0.25; gfx_g = 0.32; gfx_b = 0.42; gfx_rect(tx, tab_y, tab_w - 4, tab_h, 0);
    gfx_r = hov ? 0.95 : 0.65; gfx_g = hov ? 0.95 : 0.72; gfx_b = hov ? 1.00 : 0.80;
  );

  gfx_setfont(1, "Orbitron", 12.5, 'b');
  t_lbl = ti == 0 ? "OVERVIEW" :
          ti == 1 ? "BAXANDALL" :
          ti == 2 ? "VOCAL GLUE" :
          ti == 3 ? "DE-ESSER" :
          ti == 4 ? "SPATIAL" :
          ti == 5 ? "PRESENCE" : "PRODUCER";
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
    update_vocal_filters();
    slider_automate();
  );
);

// Vocal Channel Strip Fader
function draw_vocal_channel_strip(px, py, pw, ph, band_title, band_sub, val, min_v, max_v, fmt_str, s_idx, cr, cg, cb) local(kn_y, trk_x, trk_w, trk_y, trk_h, f_val, zero_y, hov, new_f) (
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(px, py, pw, ph);
  gfx_r = cr; gfx_g = cg; gfx_b = cb; gfx_rect(px, py, pw, ph, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = cr; gfx_g = cg; gfx_b = cb;
  gfx_measurestr(band_title, tw, th);
  gfx_x = px + floor((pw - tw) * 0.5); gfx_y = py + 12; gfx_drawstr(band_title);

  gfx_setfont(3, "Consolas", 10.5); gfx_r = 0.65; gfx_g = 0.72; gfx_b = 0.82;
  gfx_measurestr(band_sub, stw, sth);
  gfx_x = px + floor((pw - stw) * 0.5); gfx_y = py + 30; gfx_drawstr(band_sub);

  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(px + 12, py + 50, pw - 24, 26);
  gfx_r = cr * 0.6; gfx_g = cg * 0.6; gfx_b = cb * 0.6; gfx_rect(px + 12, py + 50, pw - 24, 26, 0);
  gfx_setfont(1, "Consolas", 12, 'b'); gfx_r = 1.0; gfx_g = 0.95; gfx_b = 0.40;
  v_str = sprintf(#, fmt_str, val);
  gfx_measurestr(v_str, vsw, vsh);
  gfx_x = px + floor((pw - vsw) * 0.5); gfx_y = py + 56; gfx_drawstr(v_str);

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

  cap_w = pw - 24; cap_h = 18;
  gfx_r = 0.12; gfx_g = 0.16; gfx_b = 0.22; gfx_rect(px + 12, kn_y - 9, cap_w, cap_h);
  gfx_r = cr; gfx_g = cg; gfx_b = cb; gfx_rect(px + 12, kn_y - 9, cap_w, cap_h, 0);
  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 1.00; gfx_line(px + 16, kn_y, px + 12 + cap_w - 4, kn_y);

  hov = (mouse_x >= px && mouse_x <= px + pw && mouse_y >= trk_y - 12 && mouse_y <= trk_y + trk_h + 12);
  mouse_clicked && hov ? drag_slider_idx = s_idx;
  drag_slider_idx == s_idx && mouse_down ? (
    new_f = max(0.0, min(1.0, (trk_y + trk_h - mouse_y) / trk_h));
    slider(s_idx) = min_v + new_f * (max_v - min_v);
    update_vocal_filters();
    slider_automate();
  );
);

// Strictly Confined SIFAM Analogue Moving-Coil Meter for Vocals with Glass Sheen & Lamp Glow
function draw_sifam_vocal_meter(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) local(plate_x, plate_y, plate_w, plate_h, piv_x, piv_y, radius_arc, radius_needle, ang_min, ang_max, a_span, a_frac, cur_a, ax, ay, ai, arc_steps, prev_ax, prev_ay, t_a, m_db, f_val, nx1, ny1, nx2, ny2, tw, th, t_str, badge_str, b_w, b_h, frac, cur_ang, tip_x, tip_y, base_x, base_y) (
  gfx_r = 0.055; gfx_g = 0.065; gfx_b = 0.080; gfx_rect(mx, my, mw, mh);
  gfx_r = 0.020; gfx_g = 0.024; gfx_b = 0.032; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(mx, my, mw, mh, 0);
  gfx_r = accent_r * 0.6; gfx_g = accent_g * 0.6; gfx_b = accent_b * 0.6; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4, 0);

  plate_x = mx + 6; plate_y = my + 6;
  plate_w = mw - 12; plate_h = mh - 12;
  gfx_r = 0.035; gfx_g = 0.045; gfx_b = 0.060; gfx_rect(plate_x, plate_y, plate_w, plate_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(plate_x, plate_y, plate_w, plate_h, 0);

  piv_x = plate_x + plate_w * 0.5;
  piv_y = plate_y + plate_h - 16;

  radius_arc = min(plate_h - 58, plate_w * 0.44);
  radius_needle = radius_arc - 4;

  // Warm Incandescent Tungsten Lamp Glow behind meter pivot
  gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.35; gfx_a = 0.07;
  gfx_circle(piv_x, piv_y - radius_arc * 0.45, floor(radius_arc * 0.6), 1);
  gfx_a = 1.0;

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = plate_x + 12; gfx_y = plate_y + 8; gfx_drawstr(title_str);

  gfx_setfont(2, "Consolas", 11.5, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  badge_str = is_glue ? "IMPERIAL GR" : "TUBE VU";
  gfx_measurestr(badge_str, b_w, b_h);
  gfx_x = plate_x + plate_w - b_w - 12; gfx_y = plate_y + 8; gfx_drawstr(badge_str);

  ang_min = -0.62; ang_max = 0.62; a_span = ang_max - ang_min;
  arc_steps = 30; ai = 0; prev_ax = 0; prev_ay = 0;
  loop(arc_steps + 1,
    a_frac = ai / arc_steps;
    cur_a = ang_min + a_frac * a_span;
    ax = piv_x + sin(cur_a) * radius_arc;
    ay = piv_y - cos(cur_a) * radius_arc;
    ai > 0 ? (
      is_glue ? (
        a_frac > 0.65 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;)
      ) : (
        a_frac > 0.87 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.95; gfx_g = 0.75; gfx_b = 0.20;)
      );
      gfx_line(prev_ax, prev_ay, ax, ay);
    );
    prev_ax = ax; prev_ay = ay;
    ai += 1;
  );

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

  gfx_setfont(1, "Orbitron", 14, 'b');
  is_glue ? (gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;) : (gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;) ;
  center_badge = is_glue ? "[ GR ]" : "[ VU ]";
  gfx_measurestr(center_badge, tw, th);
  gfx_x = floor(plate_x + (plate_w - tw) * 0.5);
  gfx_y = floor(piv_y - radius_needle * 0.45);
  gfx_drawstr(center_badge);

  frac = is_glue ? min(1.0, max(0.0, needle_val / 20.0)) : min(1.0, max(0.0, (needle_val + 20.0) / 23.0));
  cur_ang = ang_min + frac * a_span;
  tip_x = piv_x + sin(cur_ang) * radius_needle;
  tip_y = piv_y - cos(cur_ang) * radius_needle;
  base_x = piv_x + sin(cur_ang) * 14;
  base_y = piv_y - cos(cur_ang) * 14;

  is_glue ? (gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;) : (gfx_r = 1.00; gfx_g = 0.80; gfx_b = 0.22;);
  gfx_line(base_x - 0.7, base_y, tip_x - 0.7, tip_y);
  gfx_line(base_x + 0.7, base_y, tip_x + 0.7, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  gfx_r = 0.98; gfx_g = 0.25; gfx_b = 0.22; gfx_circle(tip_x, tip_y, 2.5, 1);

  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(piv_x, piv_y, 16, 1);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_circle(piv_x, piv_y, 16, 0);

  // Curved Glass Reflection Sheen
  gfx_r = 1.00; gfx_g = 1.00; gfx_b = 1.00; gfx_a = 0.05;
  gfx_line(plate_x + 8, plate_y + 12, plate_x + plate_w * 0.65, plate_y + plate_h * 0.45);
  gfx_line(plate_x + 12, plate_y + 12, plate_x + plate_w * 0.65 + 4, plate_y + plate_h * 0.45);
  gfx_a = 1.0;

  gfx_setfont(3, "Consolas", 11, 'b');
  is_glue ? (
    gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
    gfx_x = plate_x + 14; gfx_y = plate_y + plate_h - 22;
    gfx_printf("GR: %4.1f dB", vocal_gr_db);
    gfx_x = plate_x + plate_w - 78; gfx_y = plate_y + plate_h - 22;
    gfx_drawstr("PEAK HOLD");
  ) : (
    gfx_r = 0.00; gfx_g = 0.85; gfx_b = 0.45;
    gfx_x = plate_x + 14; gfx_y = plate_y + plate_h - 22;
    gfx_printf("RMS: %4.1f dBFS", vocal_rms);
    gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
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

  // 1. Vocal Tube Warmth SIFAM Meter
  draw_sifam_vocal_meter(ws_x + 8, ws_y + 8, meter_w, top_row_h, "VOCAL TUBE WARMTH // SATURATION", sifam_vocal_vu, 3.0, 0, 1.00, 0.85, 0.35);

  // 2. Master Vocal Glue SIFAM Meter
  draw_sifam_vocal_meter(ws_x + 16 + meter_w, ws_y + 8, meter_w, top_row_h, "MASTER VOCAL GLUE // GAIN REDUCTION", sifam_vocal_gr, 20.0, 1, 0.88, 0.25, 0.65);

  // 3. Vocal Spatial Radar
  sc_x = ws_x + 24 + meter_w * 2; sc_y = ws_y + 8;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(sc_x, sc_y, scope_w, top_row_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(sc_x, sc_y, scope_w, top_row_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = sc_x + 14; gfx_y = sc_y + 10; gfx_drawstr("VOCAL SPATIAL RADAR");

  r_cx = sc_x + scope_w * 0.5; r_cy = sc_y + 115;
  r_dyn = 1.0 + max(0.0, (vocal_rms + 35.0) / 45.0) * 0.20;
  gfx_r = 0.10; gfx_g = 0.14; gfx_b = 0.20;
  gfx_circle(r_cx, r_cy, floor(60 * r_dyn), 0);
  gfx_circle(r_cx, r_cy, 38, 0);
  gfx_line(r_cx - 60, r_cy, r_cx + 60, r_cy);
  gfx_line(r_cx, r_cy - 60, r_cx, r_cy + 60);

  // Live Lissajous Phosphor Trails
  pi = 0; prev_sx = r_cx; prev_sy = r_cy;
  loop(32,
    s_idx = (scope_pos - pi * 4 + 256) % 256;
    sl = scope_buf_l[s_idx]; sr = scope_buf_r[s_idx];
    sx = r_cx + (sl - sr) * 45.0;
    sy = r_cy - (sl + sr) * 45.0;
    pi > 0 ? (
      gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_a = 0.55;
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
  corr_frac = max(0.0, min(1.0, (1.0 + 1.0) * 0.5));
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_rect(cb_x + cb_w * 0.5, cb_y, (corr_frac - 0.5) * cb_w, cb_h);

  // Bottom 3 Raised Enclosures
  dash_y = ws_y + top_row_h + 16;
  dash_h = ws_h - top_row_h - 24;
  col_w = floor((ws_w - 32) / 3);

  // Card 1: VOCAL GAIN & SUMMING
  c1_x = ws_x + 8;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(c1_x, dash_y, col_w, dash_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(c1_x, dash_y, col_w, dash_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = c1_x + 16; gfx_y = dash_y + 14; gfx_drawstr("1. VOCAL GAIN & SUMMING");

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = c1_x + 16; gfx_y = dash_y + 45; gfx_printf("Input Calibration : %+3.1f dB", slider3);
  gfx_x = c1_x + 16; gfx_y = dash_y + 70; gfx_printf("Producer Output   : %+3.1f dB Trim", slider4);
  gfx_x = c1_x + 16; gfx_y = dash_y + 95;
  slider5 ? gfx_printf("Pre-Master Ceiling: -6.0 dBTP Strict Lock") : gfx_printf("Pre-Master Ceiling: Free Output Crest");
  gfx_x = c1_x + 16; gfx_y = dash_y + 120; gfx_printf("Summing State     : ACTIVE VOCAL SUM");
  gfx_x = c1_x + 16; gfx_y = dash_y + 145; gfx_printf("Delta Solo State  : NORMAL SUM");

  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(c1_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(c1_x + 14, dash_y + dash_h - 38, col_w - 28, 26, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = c1_x + 22; gfx_y = dash_y + dash_h - 32; gfx_drawstr(get_producer_short_name(slider2));

  // Card 2: GLUE & SIBILANCE SENTRY
  c2_x = ws_x + 16 + col_w;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(c2_x, dash_y, col_w, dash_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(c2_x, dash_y, col_w, dash_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = c2_x + 16; gfx_y = dash_y + 14; gfx_drawstr("2. GLUE & SIBILANCE SENTRY");

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = c2_x + 16; gfx_y = dash_y + 45;
  slider14 ? gfx_printf("Glue Topology     : Vintage Opto Leveler") : gfx_printf("Glue Topology     : Fairchild 670 Tube");
  gfx_x = c2_x + 16; gfx_y = dash_y + 70; gfx_printf("Threshold / Ratio : %4.1f dB | %d:1", slider15, slider16 == 0 ? 1.5 : (slider16 == 1 ? 2 : (slider16 == 2 ? 3 : 4)));
  gfx_x = c2_x + 16; gfx_y = dash_y + 95;
  r_str = slider18 == 0 ? "100ms" : (slider18 == 1 ? "300ms" : (slider18 == 2 ? "600ms" : "1200ms"));
  gfx_printf("Attack / Release  : %3.1fms | %s", slider17, r_str);
  gfx_x = c2_x + 16; gfx_y = dash_y + 120; gfx_printf("De-Esser Clamp    : -%3.1f dB @ %d Hz", de_gr_db, slider7);
  gfx_x = c2_x + 16; gfx_y = dash_y + 145; gfx_printf("Live Vocal Glue GR: -%3.2f dB Peak Hold", vocal_gr_db);

  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(c2_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 0.01; gfx_g = 0.02; gfx_b = 0.04;
  gfx_x = c2_x + 22; gfx_y = dash_y + dash_h - 32; gfx_printf("VOCAL GLUE: %3.1f dB", vocal_gr_db);

  // Card 3: BAXANDALL & CORRIDOR
  c3_x = ws_x + 24 + col_w * 2;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(c3_x, dash_y, col_w, dash_h);
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35; gfx_rect(c3_x, dash_y, col_w, dash_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = c3_x + 16; gfx_y = dash_y + 14; gfx_drawstr("3. BAXANDALL & CORRIDOR");

  gfx_setfont(3, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = c3_x + 16; gfx_y = dash_y + 45; gfx_printf("100Hz Warmth Shelf: %+3.1f dB", slider10);
  gfx_x = c3_x + 16; gfx_y = dash_y + 70; gfx_printf("3.5kHz Presence   : %+3.1f dB", slider11);
  gfx_x = c3_x + 16; gfx_y = dash_y + 95; gfx_printf("12kHz Silk Air    : %+3.1f dB Shelf", slider12);
  gfx_x = c3_x + 16; gfx_y = dash_y + 120; gfx_printf("Spatial Width     : %4.2f x (Lead Lock)", slider21);
  gfx_x = c3_x + 16; gfx_y = dash_y + 145; gfx_printf("Tube Saturation   : %+3.1f dB Warmth", slider20);

  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(c3_x + 14, dash_y + dash_h - 38, col_w - 28, 26);
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35; gfx_rect(c3_x + 14, dash_y + dash_h - 38, col_w - 28, 26, 0);
  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 1.0; gfx_g = 0.90; gfx_b = 0.40;
  gfx_x = c3_x + 22; gfx_y = dash_y + dash_h - 32; gfx_drawstr("CORRIDOR RELAY: ACTIVE LINK");
);

// =============================================================================
// TAB 1: BAXANDALL EQ (RESPONSE CURVE + 3 FULL-HEIGHT CHANNEL STRIPS)
// =============================================================================
slider1 == 1 ? (
  bax_plot_y = ws_y + 8; bax_plot_h = 220; bax_plot_w = ws_w - 16;
  gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.024; gfx_rect(ws_x + 8, bax_plot_y, bax_plot_w, bax_plot_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(ws_x + 8, bax_plot_y, bax_plot_w, bax_plot_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 20; gfx_y = bax_plot_y + 12; gfx_drawstr("BAXANDALL TONE // SMOOTH BROAD-CURVATURE VOCAL EQUALIZATION");

  cy0 = bax_plot_y + bax_plot_h * 0.5;
  gfx_r = 0.12; gfx_g = 0.18; gfx_b = 0.26;
  gfx_line(ws_x + 8, cy0, ws_x + 8 + bax_plot_w, cy0);
  gfx_line(ws_x + 8, cy0 - 45, ws_x + 8 + bax_plot_w, cy0 - 45);
  gfx_line(ws_x + 8, cy0 + 45, ws_x + 8 + bax_plot_w, cy0 + 45);

  fx100 = ws_x + 8 + floor(bax_plot_w * 0.22);
  fx1k  = ws_x + 8 + floor(bax_plot_w * 0.55);
  fx10k = ws_x + 8 + floor(bax_plot_w * 0.85);
  gfx_line(fx100, bax_plot_y, fx100, bax_plot_y + bax_plot_h);
  gfx_line(fx1k,  bax_plot_y, fx1k,  bax_plot_y + bax_plot_h);
  gfx_line(fx10k, bax_plot_y, fx10k, bax_plot_y + bax_plot_h);

  gfx_setfont(3, "Consolas", 11.5, 'b'); gfx_r = 0.55; gfx_g = 0.65; gfx_b = 0.75;
  gfx_x = fx100 + 4; gfx_y = bax_plot_y + bax_plot_h - 20; gfx_drawstr("100Hz");
  gfx_x = fx1k + 4;  gfx_y = bax_plot_y + bax_plot_h - 20; gfx_drawstr("1kHz");
  gfx_x = fx10k + 4; gfx_y = bax_plot_y + bax_plot_h - 20; gfx_drawstr("10kHz");

  // Dynamic Baxandall curve with vertical shaded fill
  prev_py = cy0; pi = 0;
  loop(160,
    px = ws_x + 8 + floor((pi / 159.0) * bax_plot_w);
    f_val = 20.0 * exp(log(1000.0) * (pi / 159.0));
    g_tot = 0.0;
    f_val <= 100.0 ? g_tot += slider10 : (f_val < 400.0 ? g_tot += slider10 * (1.0 - (f_val - 100.0) / 300.0) : 0);
    g_tot += slider11 * exp(-0.5 * sqr((log(f_val / 3500.0) / 0.5)));
    f_val > 6000.0 ? g_tot += slider12 * (min(1.0, (f_val - 6000.0) / 6000.0));
    cur_py = cy0 - g_tot * 8.5;
    pi > 0 ? (
      gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
      gfx_line(prev_px, prev_py, px, cur_py);
      gfx_line(px, cur_py, px, cy0);
    );
    prev_px = px; prev_py = cur_py;
    pi += 1;
  );

  col_w = floor((ws_w - 16 - 16) / 3);
  cards_y = bax_plot_y + bax_plot_h + 12; cards_h = ws_h - bax_plot_h - 24;
  draw_vocal_channel_strip(ws_x + 8 + 0 * (col_w + 8), cards_y, col_w, cards_h, "100Hz WARMTH", "CHEST RESONANCE SHELF", slider10, -6.0, 6.0, "%+.1f dB", 10, 0.88, 0.25, 0.65);
  draw_vocal_channel_strip(ws_x + 8 + 1 * (col_w + 8), cards_y, col_w, cards_h, "3.5kHz PRESENCE", "VOCAL CUT & BITE", slider11, -6.0, 6.0, "%+.1f dB", 11, 0.00, 0.85, 1.00);
  draw_vocal_channel_strip(ws_x + 8 + 2 * (col_w + 8), cards_y, col_w, cards_h, "12kHz SILK AIR", "IMPERIAL SHEEN SHELF", slider12, -6.0, 6.0, "%+.1f dB", 12, 1.00, 0.85, 0.35);
);

// =============================================================================
// TAB 2: MASTER VOCAL GLUE COMPRESSION (TRANSFER CURVE WITH LIVE BALL + PARAMS)
// =============================================================================
slider1 == 2 ? (
  col_w = floor((ws_w - 24) * 0.42);
  tc_x = ws_x + 8; tc_y = ws_y + 8; tc_h = ws_h - 16;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(tc_x, tc_y, col_w, tc_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(tc_x, tc_y, col_w, tc_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = tc_x + 16; gfx_y = tc_y + 14; gfx_drawstr("VOCAL GLUE TRANSFER FUNCTION");

  tbox_x = tc_x + 20; tbox_y = tc_y + 50; tbox_sz = col_w - 40;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(tbox_x, tbox_y, tbox_sz, tbox_sz);
  gfx_r = 0.28; gfx_g = 0.18; gfx_b = 0.26; gfx_rect(tbox_x, tbox_y, tbox_sz, tbox_sz, 0);

  gfx_r = 0.18; gfx_g = 0.12; gfx_b = 0.20;
  gfx_line(tbox_x, tbox_y + tbox_sz, tbox_x + tbox_sz, tbox_y);

  v_ratio = slider16 == 0 ? 1.5 : (slider16 == 1 ? 2.0 : (slider16 == 2 ? 3.0 : 4.0));
  th_frac = (slider15 + 36.0) / 36.0;
  th_x = tbox_x + th_frac * tbox_sz;
  th_y = tbox_y + tbox_sz - th_frac * tbox_sz;

  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_line(tbox_x, tbox_y + tbox_sz, th_x, th_y);
  end_x = tbox_x + tbox_sz;
  end_y = th_y - (1.0 / v_ratio) * (end_x - th_x);
  gfx_line(th_x, th_y, end_x, end_y);

  gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.35;
  gfx_circle(th_x, th_y, 5, 1);

  // Live Bouncing Ball tracking (Vin, Vout)
  live_frac = max(0.0, min(1.0, (vocal_rms + 50.0) / 46.0));
  ball_in_x = tbox_x + live_frac * tbox_sz;
  ball_in_x < th_x ? (
    ball_out_y = tbox_y + tbox_sz - live_frac * tbox_sz;
  ) : (
    ball_out_y = th_y - (1.0 / v_ratio) * (ball_in_x - th_x);
  );
  gfx_r = 0.00; gfx_g = 0.95; gfx_b = 1.00;
  gfx_circle(ball_in_x, ball_out_y, 6, 1);

  // Right Side Parameters Panel
  rp_x = ws_x + 16 + col_w; rp_w = ws_w - col_w - 24;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(rp_x, tc_y, rp_w, tc_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(rp_x, tc_y, rp_w, tc_h, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = rp_x + 16; gfx_y = tc_y + 14; gfx_drawstr("MASTER VOCAL GLUE PARAMETERS");

  sl_y = tc_y + 50; sl_sp = 68;
  draw_param_slider(rp_x + 16, sl_y + 0 * sl_sp, rp_w - 32, 54, "1. VOCAL GLUE THRESHOLD", slider15, -36.0, 0.0, "%.1f dBFS", 15, 0.88, 0.25, 0.65);
  draw_param_slider(rp_x + 16, sl_y + 1 * sl_sp, rp_w - 32, 54, "2. COMPRESSION RATIO", slider16, 0, 3, "Mode %d", 16, 0.95, 0.70, 0.20);
  draw_param_slider(rp_x + 16, sl_y + 2 * sl_sp, rp_w - 32, 54, "3. ATTACK TIME", slider17, 0.2, 50.0, "%.1f ms", 17, 0.88, 0.25, 0.65);
  draw_param_slider(rp_x + 16, sl_y + 3 * sl_sp, rp_w - 32, 54, "4. RELEASE BALLISTICS", slider18, 0, 4, "Mode %d", 18, 0.95, 0.70, 0.20);
  draw_param_slider(rp_x + 16, sl_y + 4 * sl_sp, rp_w - 32, 54, "5. TUBE WARMTH SATURATION", slider20, 0.0, 10.0, "+%.1f dB", 20, 1.00, 0.85, 0.35);
  draw_param_slider(rp_x + 16, sl_y + 5 * sl_sp, rp_w - 32, 54, "6. PARALLEL DRY / WET MIX", slider19, 0, 100, "%d %%", 19, 0.00, 0.85, 1.00);
);

// =============================================================================
// TAB 3: SIBILANCE SENTRY (MASTER DE-ESSER & CLAMP SCOPE)
// =============================================================================
slider1 == 3 ? (
  de_w = ws_w - 16; de_h = ws_h - 16;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 8, ws_y + 8, de_w, de_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 8, ws_y + 8, de_w, de_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 24; gfx_y = ws_y + 20; gfx_drawstr("SIBILANCE SENTRY // DYNAMIC HARSHNESS CLAMP SCOPE");

  d_sc_y = ws_y + 55; d_sc_h = 220;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(ws_x + 24, d_sc_y, de_w - 48, d_sc_h);
  gfx_r = 0.20; gfx_g = 0.28; gfx_b = 0.38; gfx_rect(ws_x + 24, d_sc_y, de_w - 48, d_sc_h, 0);

  cy0 = d_sc_y + d_sc_h * 0.5;
  gfx_r = 0.15; gfx_g = 0.20; gfx_b = 0.28;
  gfx_line(ws_x + 24, cy0, ws_x + de_w - 24, cy0);

  // Draw Sibilance Clamp Bandpass Envelope
  band_x = ws_x + 24 + floor(((slider7 - 4000.0) / 6000.0) * (de_w - 48));
  gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;
  gfx_line(band_x, d_sc_y, band_x, d_sc_y + d_sc_h);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  c_info = sprintf(#, "LIVE SIBILANCE CLAMP: -%3.1f dB @ %d Hz", de_gr_db, slider7);
  gfx_measurestr(c_info, ciw, cih);
  gfx_x = ws_x + 24 + floor((de_w - 48 - ciw) * 0.5); gfx_y = cy0 + 65;
  gfx_drawstr(c_info);

  draw_param_slider(ws_x + 24, ws_y + 295, de_w - 48, 54, "1. MASTER DE-ESSER THRESHOLD", slider6, -36.0, 0.0, "%.1f dBFS", 6, 0.00, 0.85, 1.00);
  draw_param_slider(ws_x + 24, ws_y + 355, de_w - 48, 54, "2. SIBILANCE DETECTION FREQUENCY", slider7, 4000, 10000, "%d Hz", 7, 0.88, 0.25, 0.65);
  draw_param_slider(ws_x + 24, ws_y + 415, de_w - 48, 54, "3. MAXIMUM SIBILANCE REDUCTION RANGE", slider8, -12.0, 0.0, "%.1f dB", 8, 1.00, 0.85, 0.35);
);

// =============================================================================
// TAB 4: VOCAL SPATIAL DIMENSION (LEAD CENTER-LOCK & VECTORSCOPE)
// =============================================================================
slider1 == 4 ? (
  sp_w = ws_w - 16; sp_h = ws_h - 16;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 8, ws_y + 8, sp_w, sp_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(ws_x + 8, ws_y + 8, sp_w, sp_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 24; gfx_y = ws_y + 20; gfx_drawstr("VOCAL SPATIAL DIMENSION // LEAD CENTER-LOCK & LIVE VECTORSCOPE");

  v_box_w = sp_w - 48; v_box_h = 240;
  gfx_r = 0.010; gfx_g = 0.014; gfx_b = 0.020; gfx_rect(ws_x + 24, ws_y + 55, v_box_w, v_box_h);
  gfx_r = 0.24; gfx_g = 0.18; gfx_b = 0.28; gfx_rect(ws_x + 24, ws_y + 55, v_box_w, v_box_h, 0);

  vc_x = ws_x + 24 + v_box_w * 0.5; vc_y = ws_y + 55 + v_box_h * 0.5;
  gfx_r = 0.14; gfx_g = 0.10; gfx_b = 0.18;
  gfx_circle(vc_x, vc_y, 70, 0);
  gfx_circle(vc_x, vc_y, 40, 0);
  gfx_line(vc_x - 70, vc_y, vc_x + 70, vc_y);
  gfx_line(vc_x, vc_y - 70, vc_x, vc_y + 70);

  pi = 0;
  loop(40,
    s_idx = (scope_pos - pi * 4 + 256) % 256;
    sl = scope_buf_l[s_idx]; sr = scope_buf_r[s_idx];
    px = vc_x + (sl - sr) * 55.0;
    py = vc_y - (sl + sr) * 55.0;
    gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_circle(px, py, 1.5, 1);
    pi += 1;
  );

  draw_param_slider(ws_x + 24, ws_y + 320, sp_w - 48, 56, "VOCAL SPATIAL WIDTH MULTIPLIER (LEAD CENTER LOCK)", slider21, 0.80, 1.40, "%.2f x", 21, 0.88, 0.25, 0.65);
);

// =============================================================================
// TAB 5: VOCAL PRESENCE SENTRY
// =============================================================================
slider1 == 5 ? (
  pr_w = ws_w - 16; pr_h = ws_h - 16;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 8, ws_y + 8, pr_w, pr_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ws_x + 8, ws_y + 8, pr_w, pr_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ws_x + 24; gfx_y = ws_y + 20; gfx_drawstr("VOCAL PRESENCE SENTRY // LEAD INTIMACY & FORMANTE CORRIDOR");

  draw_param_slider(ws_x + 24, ws_y + 70, pr_w - 48, 64, "PRESENCE SENTRY SENSITIVITY", slider26, 0.0, 3.0, "%.1f dB", 26, 0.00, 0.85, 1.00);
);

// =============================================================================
// TAB 6: VOCAL PRODUCER MATRIX & DYNAMIC REFERENCE BLUEPRINT
// =============================================================================
slider1 == 6 ? (
  pm_w = ws_w - 16; pm_h = ws_h - 16;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ws_x + 8, ws_y + 8, pm_w, pm_h);
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(ws_x + 8, ws_y + 8, pm_w, pm_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 24; gfx_y = ws_y + 20; gfx_drawstr("MASTER VOCAL PRODUCER MATRIX // 25 REFERENCE BENCHMARKS & HUGGINGFACE AI");

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

    gfx_r = is_sel ? 0.12 : 0.016; gfx_g = is_sel ? 0.06 : 0.022; gfx_b = is_sel ? 0.18 : 0.030;
    gfx_rect(tx, ty, tile_w, tile_h);
    gfx_r = is_sel ? 0.88 : 0.25; gfx_g = is_sel ? 0.25 : 0.32; gfx_b = is_sel ? 0.65 : 0.42;
    gfx_rect(tx, ty, tile_w, tile_h, 0);

    gfx_setfont(3, "Consolas", 11, 'b');
    gfx_r = is_sel ? 1.0 : 0.70; gfx_g = is_sel ? 0.85 : 0.75; gfx_b = is_sel ? 0.95 : 0.85;
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
  gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(ws_x + 24, ai_y, pm_w - 48, ai_h, 0);

  // Left column: Local Ollama & HuggingFace AI Diagnostic Panel
  hw_w = floor((pm_w - 48 - 16) * 0.5);
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
  gfx_x = ws_x + 36; gfx_y = ai_y + 12; gfx_drawstr("LOCAL OLLAMA & HF VOCAL AI // MULTIMODAL REASONING");

  gfx_setfont(3, "Consolas", 11.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = ws_x + 36; gfx_y = ai_y + 36; gfx_drawstr("• Engine       : damei-audio-critic & cognitive-engineer (:11434)");
  gfx_x = ws_x + 36; gfx_y = ai_y + 56; gfx_drawstr("• Sibilance    : Dynamic Bandpass Clamp @ 6.8 kHz");
  gfx_x = ws_x + 36; gfx_y = ai_y + 76; gfx_drawstr("• Corridor Sync: gmem[1401] Active Lead Vocal RMS Relay");
  gfx_x = ws_x + 36; gfx_y = ai_y + 96; gfx_drawstr("• Balance Guard: ACTIVE (Strict ±0.5dB Max Safe Auto-Calibration Lock)");

  // Interactive Button: RUN SAFE AI VOCAL CALIBRATION
  btn_ai_y = ai_y + 124; btn_ai_w = hw_w - 24;
  btn_hov = (mouse_x >= ws_x + 36 && mouse_x <= ws_x + 36 + btn_ai_w && mouse_y >= btn_ai_y && mouse_y <= btn_ai_y + 32);
  gfx_r = btn_hov ? 0.98 : 0.88; gfx_g = btn_hov ? 0.35 : 0.25; gfx_b = btn_hov ? 0.75 : 0.65;
  gfx_rect(ws_x + 36, btn_ai_y, btn_ai_w, 32);
  gfx_setfont(1, "Orbitron", 11, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = ws_x + 48; gfx_y = btn_ai_y + 8;
  gfx_drawstr("RUN COGNITIVE AI VOCAL CALIBRATE (±0.5dB LOCK)");
  mouse_clicked && btn_hov ? (
    trigger_vocal_ai_assist(); slider_automate();
  );

  // Right column: Forensic Producer Reference Blueprint Plaque
  bp_x = ws_x + 24 + hw_w + 8;
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.35;
  gfx_x = bp_x + 12; gfx_y = ai_y + 12; gfx_drawstr("SELECTED VOCAL PRODUCER BLUEPRINT & REFERENCE");

  gfx_setfont(3, "Consolas", 11, 'b');
  ref_t = get_producer_ref_track(slider2);
  gfx_r = 0.00; gfx_g = 0.90; gfx_b = 1.00;
  gfx_x = bp_x + 12; gfx_y = ai_y + 34; gfx_printf("• REF TARGET : %s", ref_t);

  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = bp_x + 12; gfx_y = ai_y + 54; gfx_printf("• Output Trim: %+3.1f dB (Staging)", slider4);
  gfx_x = bp_x + 12; gfx_y = ai_y + 74; gfx_printf("• Baxandall  : 100Hz %+3.1fdB | 3.5k %+3.1fdB | 12k %+3.1fdB", slider10, slider11, slider12);
  gfx_x = bp_x + 12; gfx_y = ai_y + 94; gfx_printf("• Vocal Glue : Thresh %4.1fdB | Fairchild Variable-Mu", slider15);
  gfx_x = bp_x + 12; gfx_y = ai_y + 114; gfx_printf("• De-Esser   : Thresh %4.1fdB | Range %4.1fdB @ %dHz", slider6, slider8, slider7);
  gfx_x = bp_x + 12; gfx_y = ai_y + 134; gfx_printf("• Sat/Width  : Tube Sat +%3.1fdB | Spatial Width %4.2fx", slider20, slider21);
);

prev_mouse_down = mouse_down;
""")

print("Successfully written", target_path)
shutil.copy2(target_path, reaper_path)
print("Copied to", reaper_path)
