# Patch gen_instrumental_flagship_v8.py with 1st-order stable sidechain HPF and calibrated threshold
with open(r'c:\Dev\DameiSuite\scratch\gen_instrumental_flagship_v8.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace biquad calculation for sc in update_filters
old_filter = """  // 8. Bus Glue Sidechain Detector HPF (slider16 - Butterworth 2nd order at 39/60/85 Hz)
  sc_w0 = 2.0 * M_PI * clamp(slider16, 20.0, 250.0) / srate;
  sc_cos = cos(sc_w0); sc_sin = sin(sc_w0);
  sc_alpha = sc_sin / (2.0 * 0.7071);
  sc_b0 = (1.0 + sc_cos) * 0.5;
  sc_b1 = -(1.0 + sc_cos);
  sc_b2 = (1.0 + sc_cos) * 0.5;
  sc_a0 = 1.0 + sc_alpha;
  sc_a1 = -2.0 * sc_cos;
  sc_a2 = 1.0 - sc_alpha;"""

new_filter = """  // 8. Bus Glue Sidechain Detector HPF (slider16 - Unconditionally Stable 1st-Order at 39/60/85 Hz)
  sc_alpha = exp(-2.0 * M_PI * clamp(slider16, 20.0, 250.0) / srate);"""

content = content.replace(old_filter, new_filter)

# Replace filter state in @sample
old_sample = """    sc_in = (sat_out_l + sat_out_r) * 0.5;
    // Sidechain Detector HPF (slider16: 39Hz Nolly/Pinchin, 60Hz Sam Guaiana)
    sc_det = (sc_b0 * sc_in + sc_b1 * sc_x1 + sc_b2 * sc_x2 - sc_a1 * sc_y1 - sc_a2 * sc_y2) / sc_a0;
    sc_x2 = sc_x1; sc_x1 = sc_in; sc_y2 = sc_y1; sc_y1 = sc_det;"""

new_sample = """    sc_in = (sat_out_l + sat_out_r) * 0.5;
    // Unconditionally Stable Sidechain Detector HPF (39Hz Nolly/Pinchin, 60Hz Sam Guaiana)
    sc_det = sc_alpha * (sc_det + sc_in - sc_prev_in);
    sc_prev_in = sc_in;"""

content = content.replace(old_sample, new_sample)

# Update threshold in Split Chain preset
content = content.replace("slider12 = -14.5; // Threshold calibrated for authentic 1.2-1.8 dB musical glue!",
                          "slider12 = -11.5; // Threshold calibrated for authentic 1.2-1.8 dB musical glue!")
content = content.replace("slider12:-14.5<-36.0,0.0,0.5>-Bus Glue Threshold (dB)",
                          "slider12:-11.5<-36.0,0.0,0.5>-Bus Glue Threshold (dB)")

with open(r'c:\Dev\DameiSuite\scratch\gen_instrumental_flagship_v8.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched gen_instrumental_flagship_v8.py successfully")
