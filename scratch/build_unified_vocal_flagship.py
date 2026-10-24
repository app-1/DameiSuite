# build_unified_vocal_flagship.py
import os, sys

target_path = r"c:\Dev\DameiSuite\effects\Damei_VocalBus.jsfx"
reaper_path = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_VocalBus.jsfx"

# Read gen_vocal_flagship_v5.py
with open(r"c:\Dev\DameiSuite\scratch\gen_vocal_flagship_v5.py", "r", encoding="utf-8") as f:
    text = f.read()

# We need to extract the JSFX code string inside f.write(r"""...""")
start_marker = 'f.write(r"""'
end_marker = '""")'

start_pos = text.find(start_marker) + len(start_marker)
end_pos = text.rfind(end_marker)
jsfx_content = text[start_pos:end_pos]

# Let's verify content length
print(f"Extracted JSFX content: {len(jsfx_content)} bytes")

# 1. Update sliders
old_sliders = """slider14:0<0,1,1{Fairchild 670 Smooth Tube, Vintage Opto Leveler}>-Glue Topology
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
slider27:1<0,1,1{Standby, Active Autonomous Carve Request}>-Dynamic Corridor Pocket Request"""

new_sliders = """slider14:1<0,2,1{Fairchild 670 Tube, 1176 FET + LA-2A Serial Opto, Smooth Opto Leveler}>-Glue Dynamics Topology
slider15:-8.0<-36.0,0.0,0.5>-Vocal Glue Threshold (dB)
slider16:1<0,3,1{1.5:1 Smooth Vocal, 2:1 Master Sum, 3:1 Cohesion, 4:1 Radio Glue}>-Vocal Glue Ratio
slider17:8.0<0.2,50.0,0.5>-Vocal Glue Attack (ms)
slider18:1<0,4,1{100ms Fast, 300ms Vocal Natural, 600ms Silk Opto, 1200ms Lush, Auto Ballistics}>-Vocal Glue Release
slider19:100<0,100,1>-Vocal Glue Dry/Wet Mix (%)
slider20:2.0<0.0,10.0,0.1>-Vocal Tube Warmth Saturation (dB)
slider21:1.15<0.80,1.40,0.01>-Vocal Spatial Width (Lead Center Lock)
slider22:0<0,2,1{Manual Standby, Local Ollama / HF Audit, Safe Auto-Calibrate (±0.5dB Max)}>-AI Vocal Assistant Engine
slider23:0<0,1,1{Normal Audio, Delta Solo Audition}>-Delta Solo Audition
slider24:0<0,1,1{Snapshot A, Snapshot B}>-A/B Comparison Snapshot
slider25:0<0,1,1{Master Vocal Sum, Stem Vocal Sum}>-Vocal Summing Architecture Mode
slider26:1.5<0.0,3.0,0.1>-Presence Sentry Sensitivity (dB)
slider27:1<0,1,1{Standby, Active Autonomous Carve Request}>-Dynamic Corridor Pocket Request
slider28:2.0<0.0,6.0,0.1>-Maag 16kHz Air Band Sheen (dB)
slider29:-2.5<-6.0,0.0,0.1>-ReEQ 380Hz Chest Mud Scoop (dB)
slider30:-2.2<-6.0,0.0,0.1>-ReEQ 5.2kHz De-Harsh Notch (dB)
slider31:1<0,1,1{Off, Auto Pre-Drop Throw (Final Bar into Chorus)}> -Pre-Chorus Throw Delay
slider32:1<0,1,1{Off, Active Reverse Vocal Swell into Chorus}>-Reverse Swell Generator
slider33:0<0,2,1{Clean Lead, Auto Pre-Drop Choke, Megaphone / Lo-Fi Drop}>-Drop Filter Mode
slider34:15<0,100,1>-Producer Ear-Candy Intensity (%)"""

assert old_sliders in jsfx_content, "old_sliders not found"
jsfx_content = jsfx_content.replace(old_sliders, new_sliders)
print("Updated sliders with Maag Air, ReEQ notches, and Ear-Candy automators.")

# 2. Add filter coefficients to update_vocal_filters
old_filter_code = """  // 4. De-Esser Detector Bandpass Filter (slider7)
  de_f0 = clamp(slider7, 4000.0, 10000.0);
  w0 = 2.0 * M_PI * de_f0 / srate;
  alpha = sin(w0) / (2.0 * 2.2);
  de_b0 = alpha;
  de_b1 = 0.0;
  de_b2 = -alpha;
  de_a0 = 1.0 + alpha;
  de_a1 = -2.0 * cos(w0);
  de_a2 = 1.0 - alpha;
);"""

new_filter_code = """  // 4. De-Esser Detector Bandpass Filter (slider7)
  de_f0 = clamp(slider7, 4000.0, 10000.0);
  w0 = 2.0 * M_PI * de_f0 / srate;
  alpha = sin(w0) / (2.0 * 2.2);
  de_b0 = alpha;
  de_b1 = 0.0;
  de_b2 = -alpha;
  de_a0 = 1.0 + alpha;
  de_a1 = -2.0 * cos(w0);
  de_a2 = 1.0 - alpha;

  // 5. Maag 16kHz Air Band Sheen (slider28, Q=0.50 broad air shelf)
  A_air = exp(slider28 * 0.0575646273);
  w0_air = 2.0 * M_PI * 16000.0 / srate;
  cos_air = cos(w0_air); sin_air = sin(w0_air);
  alpha_air = sin_air / (2.0 * 0.50);
  beta_air = 2.0 * sqrt(A_air) * alpha_air;
  air_b0 = A_air * ((A_air + 1.0) + (A_air - 1.0) * cos_air + beta_air);
  air_b1 = -2.0 * A_air * ((A_air - 1.0) + (A_air + 1.0) * cos_air);
  air_b2 = A_air * ((A_air + 1.0) - (A_air - 1.0) * cos_air - beta_air);
  air_a0 = (A_air + 1.0) - (A_air - 1.0) * cos_air + beta_air;
  air_a1 = 2.0 * ((A_air - 1.0) - (A_air + 1.0) * cos_air);
  air_a2 = (A_air + 1.0) - (A_air - 1.0) * cos_air - beta_air;

  // 6. ReEQ 380Hz Chest Mud Scoop (slider29, Q=1.2)
  A_380 = exp(slider29 * 0.0575646273);
  w0_380 = 2.0 * M_PI * 380.0 / srate;
  alpha_380 = sin(w0_380) / (2.0 * 1.2);
  s380_b0 = 1.0 + alpha_380 * A_380;
  s380_b1 = -2.0 * cos(w0_380);
  s380_b2 = 1.0 - alpha_380 * A_380;
  s380_a0 = 1.0 + alpha_380 / A_380;
  s380_a1 = -2.0 * cos(w0_380);
  s380_a2 = 1.0 - alpha_380 / A_380;

  // 7. ReEQ 5.2kHz De-Harsh Notch (slider30, Q=2.0)
  A_5k = exp(slider30 * 0.0575646273);
  w0_5k = 2.0 * M_PI * 5200.0 / srate;
  alpha_5k = sin(w0_5k) / (2.0 * 2.0);
  s5k_b0 = 1.0 + alpha_5k * A_5k;
  s5k_b1 = -2.0 * cos(w0_5k);
  s5k_b2 = 1.0 - alpha_5k * A_5k;
  s5k_a0 = 1.0 + alpha_5k / A_5k;
  s5k_a1 = -2.0 * cos(w0_5k);
  s5k_a2 = 1.0 - alpha_5k / A_5k;
);"""

assert old_filter_code in jsfx_content, "old_filter_code not found"
jsfx_content = jsfx_content.replace(old_filter_code, new_filter_code)
print("Updated filter calculations.")

# 3. Update Preset 06 to Kel Pinchin Sovereign levels (Trim +1.8dB, 1176+LA2A, Maag Air 2.0dB)
old_p6 = """  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target) - Calibrated for Vocal Lead Sum
    slider3 = 0.0; slider4 = -2.5; slider5 = 0;
    slider6 = -19.0; slider7 = 6800; slider8 = -7.0; slider9 = 0;
    slider10 = 1.2; slider11 = 2.8; slider12 = 3.8;
    slider13 = 1; slider14 = 0; slider15 = -5.5; slider16 = 1; slider17 = 12.0;
    slider18 = 1; slider19 = 100; slider20 = 3.2; slider21 = 1.08;"""

new_p6 = """  ) : idx == 6 ? ( // Kel Pinchin (Split Chain Target - Unified Flagship Calibration)
    slider3 = 0.0; slider4 = 1.8; slider5 = 0;
    slider6 = -32.0; slider7 = 6600; slider8 = -3.5; slider9 = 0; // Gentle de-esser (preserves articulation!)
    slider10 = 1.2; slider11 = 1.4; slider12 = 3.2;
    slider13 = 1; slider14 = 1; // 1176 FET + LA-2A Serial Opto
    slider15 = -8.0; slider16 = 1;
    slider17 = 8.0; slider18 = 1; slider19 = 100;
    slider20 = 2.0; slider21 = 1.15; // Lead Center Lock + 1.15 Backing Width
    slider28 = 2.0; // Maag 16kHz Air Band +2.0 dB Sheen!
    slider29 = -2.5; // ReEQ 380Hz Chest Mud Scoop
    slider30 = -2.2; // ReEQ 5.2kHz De-Harsh Notch
    slider31 = 1; slider32 = 1; slider33 = 0; slider34 = 15; // Ear-candy throw & reverse swell active"""

assert old_p6 in jsfx_content, "old_p6 not found"
jsfx_content = jsfx_content.replace(old_p6, new_p6)
print("Updated Preset 06 to Kel Pinchin Unified Flagship calibration.")

# 4. Update @sample loop with Maag Air, ReEQ notches, 1176+LA2A dynamics, and delay throw
old_sample_bax = """  // 3. Baxandall Smooth Vocal Equalizer
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
  bax_a_x2_r = bax_a_x1_r; bax_a_x1_r = p_r; bax_a_y2_r = bax_a_y1_r; bax_a_y1_r = bax_out_r;"""

new_sample_bax = """  // 2b. ReEQ 380Hz Chest Mud Scoop & 5.2kHz De-Harsh Notch
  m380_l = (s380_b0 * de_out_l + s380_b1 * s380_x1_l + s380_b2 * s380_x2_l - s380_a1 * s380_y1_l - s380_a2 * s380_y2_l) / s380_a0;
  s380_x2_l = s380_x1_l; s380_x1_l = de_out_l; s380_y2_l = s380_y1_l; s380_y1_l = m380_l;
  m380_r = (s380_b0 * de_out_r + s380_b1 * s380_x1_r + s380_b2 * s380_x2_r - s380_a1 * s380_y1_r - s380_a2 * s380_y2_r) / s380_a0;
  s380_x2_r = s380_x1_r; s380_x1_r = de_out_r; s380_y2_r = s380_y1_r; s380_y1_r = m380_r;

  n5k_l = (s5k_b0 * m380_l + s5k_b1 * s5k_x1_l + s5k_b2 * s5k_x2_l - s5k_a1 * s5k_y1_l - s5k_a2 * s5k_y2_l) / s5k_a0;
  s5k_x2_l = s5k_x1_l; s5k_x1_l = m380_l; s5k_y2_l = s5k_y1_l; s5k_y1_l = n5k_l;
  n5k_r = (s5k_b0 * m380_r + s5k_b1 * s5k_x1_r + s5k_b2 * s5k_x2_r - s5k_a1 * s5k_y1_r - s5k_a2 * s5k_y2_r) / s5k_a0;
  s5k_x2_r = s5k_x1_r; s5k_x1_r = m380_r; s5k_y2_r = s5k_y1_r; s5k_y1_r = n5k_r;

  // 3. Baxandall Smooth Vocal Equalizer
  // Band 1: 100Hz Warmth Shelf
  w_l = (bw_b0 * n5k_l + bw_b1 * bax_w_x1_l + bw_b2 * bax_w_x2_l - bw_a1 * bax_w_y1_l - bw_a2 * bax_w_y2_l) / bw_a0;
  bax_w_x2_l = bax_w_x1_l; bax_w_x1_l = n5k_l; bax_w_y2_l = bax_w_y1_l; bax_w_y1_l = w_l;
  w_r = (bw_b0 * n5k_r + bw_b1 * bax_w_x1_r + bw_b2 * bax_w_x2_r - bw_a1 * bax_w_y1_r - bw_a2 * bax_w_y2_r) / bw_a0;
  bax_w_x2_r = bax_w_x1_r; bax_w_x1_r = n5k_r; bax_w_y2_r = bax_w_y1_r; bax_w_y1_r = w_r;

  // Band 2: 3.5kHz Presence Bell
  p_l = (bp_b0 * w_l + bp_b1 * bax_p_x1_l + bp_b2 * bax_p_x2_l - bp_a1 * bax_p_y1_l - bp_a2 * bax_p_y2_l) / bp_a0;
  bax_p_x2_l = bax_p_x1_l; bax_p_x1_l = w_l; bax_p_y2_l = bax_p_y1_l; bax_p_y1_l = p_l;
  p_r = (bp_b0 * w_r + bp_b1 * bax_p_x1_r + bp_b2 * bax_p_x2_r - bp_a1 * bax_p_y1_r - bp_a2 * bax_p_y2_r) / bp_a0;
  bax_p_x2_r = bax_p_x1_r; bax_p_x1_r = w_r; bax_p_y2_r = bax_p_y1_r; bax_p_y1_r = p_r;

  // Band 3: 12kHz Silk Air Shelf
  bax_a_l = (ba_b0 * p_l + ba_b1 * bax_a_x1_l + ba_b2 * bax_a_x2_l - ba_a1 * bax_a_y1_l - ba_a2 * bax_a_y2_l) / ba_a0;
  bax_a_x2_l = bax_a_x1_l; bax_a_x1_l = p_l; bax_a_y2_l = bax_a_y1_l; bax_a_y1_l = bax_a_l;
  bax_a_r = (ba_b0 * p_r + ba_b1 * bax_a_x1_r + ba_b2 * bax_a_x2_r - ba_a1 * bax_a_y1_r - ba_a2 * bax_a_y2_r) / ba_a0;
  bax_a_x2_r = bax_a_x1_r; bax_a_x1_r = p_r; bax_a_y2_r = bax_a_y1_r; bax_a_y1_r = bax_a_r;

  // Band 4: Maag 16kHz Air Band Sheen (+2.0 dB broad shimmer)
  bax_out_l = (air_b0 * bax_a_l + air_b1 * air_x1_l + air_b2 * air_x2_l - air_a1 * air_y1_l - air_a2 * air_y2_l) / air_a0;
  air_x2_l = air_x1_l; air_x1_l = bax_a_l; air_y2_l = air_y1_l; air_y1_l = bax_out_l;
  bax_out_r = (air_b0 * bax_a_r + air_b1 * air_x1_r + air_b2 * air_x2_r - air_a1 * air_y1_r - air_a2 * air_y2_r) / air_a0;
  air_x2_r = air_x1_r; air_x1_r = bax_a_r; air_y2_r = air_y1_r; air_y1_r = bax_out_r;"""

assert old_sample_bax in jsfx_content, "old_sample_bax not found"
jsfx_content = jsfx_content.replace(old_sample_bax, new_sample_bax)
print("Updated @sample with ReEQ and Maag Air filters.")

# 5. Update Dynamics to support 1176 FET + LA-2A Serial Opto
old_comp = """  // 5. Master Vocal Glue Compressor (Fairchild 670 / Vintage Opto)
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
  );"""

new_comp = """  // 5. Master Vocal Dynamics Engine (Fairchild 670 vs 1176 FET + LA-2A Serial Opto)
  slider13 ? (
    slider14 == 1 ? (
      // Topology 1: 1176 Fast FET Peak Shaver into LA-2A Optical Leveler
      det_sig = (tube_out_l + tube_out_r) * 0.5;
      det_pk = abs(det_sig);
      det_db = det_pk > 0.000000001 ? 20.0 * log10(det_pk) : -120.0;

      // Stage 1: 1176 FET (fast peak shaver: 0.3ms attack, 80ms release, 8:1 ratio)
      fet_atk = exp(-1.0 / (srate * 0.0003));
      fet_rel = exp(-1.0 / (srate * 0.080));
      det_db > fet_env ? ( fet_env = det_db + (fet_env - det_db) * fet_atk; ) : ( fet_env = det_db + (fet_env - det_db) * fet_rel; );
      fet_over = fet_env - (slider15 + 2.0);
      fet_gr = fet_over > 0.0 ? fet_over * 0.875 : 0.0;

      // Stage 2: LA-2A Opto Body Leveler (10ms attack, 300ms natural dual-stage release)
      opto_atk = exp(-1.0 / (srate * 0.010));
      opto_rel = exp(-1.0 / (srate * 0.300));
      (det_db - fet_gr) > opto_env ? ( opto_env = (det_db - fet_gr) + (opto_env - (det_db - fet_gr)) * opto_atk; ) : ( opto_env = (det_db - fet_gr) + (opto_env - (det_db - fet_gr)) * opto_rel; );
      opto_over = opto_env - slider15;
      opto_gr = opto_over > 0.0 ? opto_over * 0.50 : 0.0;

      vocal_gr_db = min(16.0, fet_gr + opto_gr);
      v_glue_gain = exp(-vocal_gr_db * 0.1151292546);
      v_mix_frac = slider19 * 0.01;
      comp_l = tube_out_l * v_glue_gain * v_mix_frac + tube_out_l * (1.0 - v_mix_frac);
      comp_r = tube_out_r * v_glue_gain * v_mix_frac + tube_out_r * (1.0 - v_mix_frac);
    ) : (
      // Topology 0 / 2: Fairchild 670 Tube / Vintage Opto
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
    );
  ) : (
    comp_l = tube_out_l; comp_r = tube_out_r;
    vocal_gr_db = 0.0;
  );"""

assert old_comp in jsfx_content, "old_comp not found"
jsfx_content = jsfx_content.replace(old_comp, new_comp)
print("Updated Dynamics with 1176 FET + LA-2A Serial Opto engine.")

# Write updated file
with open(target_path, "w", encoding="utf-8") as f:
    f.write(jsfx_content)
with open(reaper_path, "w", encoding="utf-8") as f:
    f.write(jsfx_content)

print(f"Unified Flagship Vocal Empress successfully written to {target_path} and deployed to REAPER!")
