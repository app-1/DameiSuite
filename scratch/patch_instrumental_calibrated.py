import re, os, subprocess

src_path = r"c:\Dev\DameiSuite\scratch\gen_instrumental_flagship_v5.py"
with open(src_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add Band 3b (90Hz) in update_filters
old_f = """  // 3. 202Hz Mud Scoop (slider20) - Matches TB EQ Band 4"""
new_f = """  // 2b. 90Hz Glue Body Bell (+0.25 dB, Q=1.0 - Matches TB EQ Band 3)
  A_b90 = exp(0.25 * 0.0575646273);
  w0_b90 = 2.0 * M_PI * 90.0 / srate;
  alpha_b90 = sin(w0_b90) / (2.0 * 1.0);
  b90_b0 = 1.0 + alpha_b90 * A_b90;
  b90_b1 = -2.0 * cos(w0_b90);
  b90_b2 = 1.0 - alpha_b90 * A_b90;
  b90_a0 = 1.0 + alpha_b90 / A_b90;
  b90_a1 = -2.0 * cos(w0_b90);
  b90_a2 = 1.0 - alpha_b90 / A_b90;

  // 3. 202Hz Mud Scoop (slider20) - Matches TB EQ Band 4"""

if old_f in code and "90Hz Glue Body Bell" not in code:
    code = code.replace(old_f, new_f, 1)
    print("Added 90Hz filter to update_filters")

# 2. In @sample: apply 90Hz Bell + Liteon waveshaper before 202Hz
old_sample = """  // Band 3: 202Hz Mud Scoop Notch
  m_l = (s200_b0 * s_l + s200_b1 * s200_x1_l + s200_b2 * s200_x2_l - s200_a1 * s200_y1_l - s200_a2 * s200_y2_l) / s200_a0;
  s200_x2_l = s200_x1_l; s200_x1_l = s_l; s200_y2_l = s200_y1_l; s200_y1_l = m_l;
  m_r = (s200_b0 * s_r + s200_b1 * s200_x1_r + s200_b2 * s200_x2_r - s200_a1 * s200_y1_r - s200_a2 * s200_y2_r) / s200_a0;
  s200_x2_r = s200_x1_r; s200_x1_r = s_r; s200_y2_r = s200_y1_r; s200_y1_r = m_r;"""

new_sample = """  // Band 2b: 90Hz Body Glue Bell
  b90_l = (b90_b0 * s_l + b90_b1 * b90_x1_l + b90_b2 * b90_x2_l - b90_a1 * b90_y1_l - b90_a2 * b90_y2_l) / b90_a0;
  b90_x2_l = b90_x1_l; b90_x1_l = s_l; b90_y2_l = b90_y1_l; b90_y1_l = b90_l;
  b90_r = (b90_b0 * s_r + b90_b1 * b90_x1_r + b90_b2 * b90_x2_r - b90_a1 * b90_y1_r - b90_a2 * b90_y2_r) / b90_a0;
  b90_x2_r = b90_x1_r; b90_x1_r = s_r; b90_y2_r = b90_y1_r; b90_y1_r = b90_r;

  // Liteon Bass Manager 25% Drive Rational Waveshaper
  drv_k = 0.223;
  ws_l = (1.0 + drv_k) * b90_l / (1.0 + drv_k * abs(b90_l));
  ws_r = (1.0 + drv_k) * b90_r / (1.0 + drv_k * abs(b90_r));

  // Band 3: 202Hz Mud Scoop Notch
  m_l = (s200_b0 * ws_l + s200_b1 * s200_x1_l + s200_b2 * s200_x2_l - s200_a1 * s200_y1_l - s200_a2 * s200_y2_l) / s200_a0;
  s200_x2_l = s200_x1_l; s200_x1_l = ws_l; s200_y2_l = s200_y1_l; s200_y1_l = m_l;
  m_r = (s200_b0 * ws_r + s200_b1 * s200_x1_r + s200_b2 * s200_x2_r - s200_a1 * s200_y1_r - s200_a2 * s200_y2_r) / s200_a0;
  s200_x2_r = s200_x1_r; s200_x1_r = ws_r; s200_y2_r = s200_y1_r; s200_y1_r = m_r;"""

if old_sample in code and "Band 2b: 90Hz Body Glue Bell" not in code:
    code = code.replace(old_sample, new_sample, 1)
    print("Added 90Hz Bell and Liteon waveshaper to @sample")

# 3. Fast feedback transient catch in Bus Glue
old_comp = """    atk_coeff = exp(-1.0 / (srate * (slider14 * 0.001)));
    rel_time = slider15 == 0 ? 0.100 : (slider15 == 1 ? 0.300 : (slider15 == 2 ? 0.600 : (slider15 == 3 ? 1.200 : 0.450)));
    rel_coeff = exp(-1.0 / (srate * rel_time));"""

new_comp = """    // Dual-stage / program-dependent transient catch:
    // If detector overshoot exceeds threshold by > 1.2 dB, clamp with fast 0.4ms attack
    (sc_db - comp_env > 1.2) ? (
      effective_atk = 0.0004;
    ) : (
      effective_atk = slider14 * 0.001;
    );
    atk_coeff = exp(-1.0 / (srate * effective_atk));
    rel_time = slider15 == 0 ? 0.100 : (slider15 == 1 ? 0.300 : (slider15 == 2 ? 0.600 : (slider15 == 3 ? 1.200 : 0.450)));
    rel_coeff = exp(-1.0 / (srate * rel_time));"""

if old_comp in code and "Dual-stage / program-dependent" not in code:
    code = code.replace(old_comp, new_comp, 1)
    print("Added fast transient catch to Bus Glue")

# 4. Output Diode Soft-Clip Limiter
old_out = """  slider5 ? (
    ceil_lin = exp(-6.0 * 0.1151292546);
    final_l = clamp(final_l, -ceil_lin, ceil_lin);
    final_r = clamp(final_r, -ceil_lin, ceil_lin);
  );"""

new_out = """  // Analog Peak Catcher & Diode Soft-Clip Ceiling (Matches Liteon 0.98 limiter & BUSTERse soft-knee)
  lim_th = 0.98; // -0.18 dBFS
  abs(final_l) > lim_th ? (
    final_l = sign(final_l) * (lim_th + (1.0 - lim_th) * tanh((abs(final_l) - lim_th) / (1.0 - lim_th)));
  );
  abs(final_r) > lim_th ? (
    final_r = sign(final_r) * (lim_th + (1.0 - lim_th) * tanh((abs(final_r) - lim_th) / (1.0 - lim_th)));
  );

  slider5 ? (
    ceil_lin = exp(-6.0 * 0.1151292546);
    final_l = clamp(final_l, -ceil_lin, ceil_lin);
    final_r = clamp(final_r, -ceil_lin, ceil_lin);
  );"""

if old_out in code and "Analog Peak Catcher & Diode Soft-Clip Ceiling" not in code:
    code = code.replace(old_out, new_out, 1)
    print("Added analog peak catcher ceiling to output")

with open(src_path, "w", encoding="utf-8") as f:
    f.write(code)

print("gen_instrumental_flagship_v5.py patched successfully.")
