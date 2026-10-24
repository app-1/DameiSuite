# Update gen_instrumental_flagship_v8.py with bounded Neve saturation and stable s8k filter
with open(r'c:\Dev\DameiSuite\scratch\gen_instrumental_flagship_v8.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace Band 6 s8k in @sample
target_s8k = """  // Band 6: 8.0kHz Air Sheen High Shelf (slider31 + Trick 5 Air Sheen Bloom)
  sheen_boost = slider31 + (dk_env5 * dk_amt * 1.4);
  A_sheen = exp(sheen_boost * 0.0575646273);
  w0_s8k = 2.0 * M_PI * 8000.0 / srate;
  cos_s8k = cos(w0_s8k); sin_s8k = sin(w0_s8k);
  alpha_s8k = sin_s8k / (2.0 * 0.7071);
  beta_s8k = 2.0 * sqrt(A_sheen) * alpha_s8k;
  dyn_s8k_b0 = A_sheen * ((A_sheen + 1.0) + (A_sheen - 1.0) * cos_s8k + beta_s8k);
  dyn_s8k_b1 = -2.0 * A_sheen * ((A_sheen - 1.0) + (A_sheen + 1.0) * cos_s8k);
  dyn_s8k_b2 = A_sheen * ((A_sheen + 1.0) - (A_sheen - 1.0) * cos_s8k - beta_s8k);
  dyn_s8k_a0 = (A_sheen + 1.0) - (A_sheen - 1.0) * cos_s8k + beta_s8k;
  dyn_s8k_a1 = 2.0 * ((A_sheen - 1.0) - (A_sheen + 1.0) * cos_s8k);
  dyn_s8k_a2 = (A_sheen + 1.0) - (A_sheen - 1.0) * cos_s8k - beta_s8k;

  eq_out_l = (dyn_s8k_b0 * k_l + dyn_s8k_b1 * s8k_x1_l + dyn_s8k_b2 * s8k_x2_l - dyn_s8k_a1 * s8k_y1_l - dyn_s8k_a2 * s8k_y2_l) / dyn_s8k_a0;
  s8k_x2_l = s8k_x1_l; s8k_x1_l = k_l; s8k_y2_l = s8k_y1_l; s8k_y1_l = eq_out_l;
  eq_out_r = (dyn_s8k_b0 * k_r + dyn_s8k_b1 * s8k_x1_r + dyn_s8k_b2 * s8k_x2_r - dyn_s8k_a1 * s8k_y1_r - dyn_s8k_a2 * s8k_y2_r) / dyn_s8k_a0;
  s8k_x2_r = s8k_x1_r; s8k_x1_r = k_r; s8k_y2_r = s8k_y1_r; s8k_y1_r = eq_out_r;"""

repl_s8k = """  // Band 6: 8.0kHz Air Sheen High Shelf (Precomputed ReEQ alignment)
  eq_out_l = (s8k_b0 * k_l + s8k_b1 * s8k_x1_l + s8k_b2 * s8k_x2_l - s8k_a1 * s8k_y1_l - s8k_a2 * s8k_y2_l) / s8k_a0;
  s8k_x2_l = s8k_x1_l; s8k_x1_l = k_l; s8k_y2_l = s8k_y1_l; s8k_y1_l = eq_out_l;
  eq_out_r = (s8k_b0 * k_r + s8k_b1 * s8k_x1_r + s8k_b2 * s8k_x2_r - s8k_a1 * s8k_y1_r - s8k_a2 * s8k_y2_r) / s8k_a0;
  s8k_x2_r = s8k_x1_r; s8k_x1_r = k_r; s8k_y2_r = s8k_y1_r; s8k_y1_r = eq_out_r;

  // Trick 5: Air Sheen Bloom (+12% high-end lift on soaring peaks)
  dk_env5 > 0.01 ? (
    sheen_factor = 1.0 + (dk_env5 * dk_amt * 0.12);
    eq_out_l *= sheen_factor; eq_out_r *= sheen_factor;
  );"""

text = text.replace(target_s8k, repl_s8k)

# 2. Replace Crucible saturators with strictly bounded musical models
target_sat = """  slider23 == 1 ? ( // Neve 8014 Iron Desk (Even/Odd Console Saturation)
    sat_l = pock_l * sat_drive; sat_r = pock_r * sat_drive;
    sat_out_l = (sat_l - 0.14 * sat_l * sat_l + 0.05 * sat_l * sat_l * sat_l) / sat_drive;
    sat_out_r = (sat_r - 0.14 * sat_r * sat_r + 0.05 * sat_r * sat_r * sat_r) / sat_drive;
  ) : slider23 == 2 ? ( // Studer A800 Tape Saturation
    sat_out_l = fast_shape(pock_l * sat_drive) / sat_drive;
    sat_out_r = fast_shape(pock_r * sat_drive) / sat_drive;
  ) : slider23 == 3 ? ( // Triode Tube Crucible
    sat_l = pock_l * sat_drive; sat_r = pock_r * sat_drive;
    sat_out_l = (sat_l / (1.0 + abs(sat_l))) / sat_drive;
    sat_out_r = (sat_r / (1.0 + abs(sat_r))) / sat_drive;
  ) : (
    sat_out_l = pock_l; sat_out_r = pock_r;
  );"""

repl_sat = """  slider23 == 1 ? ( // Neve 8014 Iron Desk (Even/Odd Console Saturation - Bounded)
    sat_l = fast_shape(pock_l * sat_drive);
    sat_r = fast_shape(pock_r * sat_drive);
    sat_out_l = (sat_l - 0.08 * sat_l * abs(sat_l)) / sat_drive;
    sat_out_r = (sat_r - 0.08 * sat_r * abs(sat_r)) / sat_drive;
  ) : slider23 == 2 ? ( // Studer A800 Tape Saturation
    sat_out_l = fast_shape(pock_l * sat_drive) / sat_drive;
    sat_out_r = fast_shape(pock_r * sat_drive) / sat_drive;
  ) : slider23 == 3 ? ( // Triode Tube Crucible
    sat_l = fast_shape(pock_l * sat_drive);
    sat_r = fast_shape(pock_r * sat_drive);
    sat_out_l = (sat_l / (1.0 + 0.4 * abs(sat_l))) / sat_drive;
    sat_out_r = (sat_r / (1.0 + 0.4 * abs(sat_r))) / sat_drive;
  ) : (
    sat_out_l = pock_l; sat_out_r = pock_r;
  );"""

text = text.replace(target_sat, repl_sat)

# 3. Update Kel Pinchin threshold to -9.0 dB
text = text.replace("slider12 = -11.5;", "slider12 = -9.0;")
text = text.replace("slider12:-11.5", "slider12:-9.0")

with open(r'c:\Dev\DameiSuite\scratch\gen_instrumental_flagship_v8.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied bounded DSP updates to gen_instrumental_flagship_v8.py")
