import re

# Update upgrade_instrumental_suite.py
with open(r"c:\Dev\DameiSuite\scratch\upgrade_instrumental_suite.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Replace tanh with fast_shape
text = text.replace("tanh(over0 * 2.5)", "fast_shape(over0 * 2.5)")
text = text.replace("tanh(over1 * 2.5)", "fast_shape(over1 * 2.5)")

# 2. Fix quick style pills in Tab 2
old_pills = """  // Quick Style Pills row
  sp_y = cg_y + cg_h - 44;
  sp_w = floor((left_w - 48 - 16) / 3);
  loop(3,
    sp_i = _1;"""

new_pills = """  // Quick Style Pills row
  sp_y = cg_y + cg_h - 44;
  sp_w = floor((left_w - 48 - 16) / 3);
  sp_i = 0;
  loop(3,"""
text = text.replace(old_pills, new_pills)
text = text.replace("_1 += 1;", "sp_i += 1;")

# 3. Add padding to Tab 3 guidance
text = text.replace("adv_y = sat_y + 424; adv_h = sat_h - 438;", "adv_y = sat_y + 420; adv_h = sat_h - 430;")

# 4. Fill Tab 6 plaque with rich dual-column forensic readout
old_plaque = """  gfx_setfont(3, "Segoe UI", 13.5); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = ws_x + 38; gfx_y = plaque_y + 75;
  gfx_drawstr("Full producer acoustic DNA matching the central preset registry. Recalls authentic console harmonic saturation,");
  gfx_x = ws_x + 38; gfx_y = plaque_y + 100;
  gfx_drawstr("VCA/Diode bus glue ballistics, and surgical tonal balance targets tailored for high-energy modern metal and rock.");
  gfx_x = ws_x + 38; gfx_y = plaque_y + 125;
  gfx_drawstr("Kel Pinchin (Preset 06) is forensically calibrated to directly replace and exceed the legacy Track 15 plugin chain.");"""

new_plaque = """  gfx_setfont(3, "Segoe UI", 13.5); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
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
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 110; gfx_printf("Vocal Pocket Carve: -%.1f dB @ 2.2 kHz", pocket_depth);"""
text = text.replace(old_plaque, new_plaque)

with open(r"c:\Dev\DameiSuite\scratch\upgrade_instrumental_suite.py", "w", encoding="utf-8") as f:
    f.write(text)

# Update upgrade_vocal_bus.py
with open(r"c:\Dev\DameiSuite\scratch\upgrade_vocal_bus.py", "r", encoding="utf-8") as f:
    v_text = f.read()

v_text = v_text.replace("tanh(over0 * 2.5)", "fast_shape(over0 * 2.5)")
v_text = v_text.replace("tanh(over1 * 2.5)", "fast_shape(over1 * 2.5)")

# Fix quick style pills in Tab 2
v_old_pills = """  // Quick Style Pills row
  sp_y = vg_y + vg_h - 44;
  sp_w = floor((left_w - 48 - 16) / 3);
  loop(3,
    sp_i = _1;"""
v_new_pills = """  // Quick Style Pills row
  sp_y = vg_y + vg_h - 44;
  sp_w = floor((left_w - 48 - 16) / 3);
  sp_i = 0;
  loop(3,"""
v_text = v_text.replace(v_old_pills, v_new_pills)
v_text = v_text.replace("_1 += 1;", "sp_i += 1;")

# Fix Tab 3 De-Esser layout so it doesn't touch bottom
v_text = v_text.replace("top_h = 230;", "top_h = 180;")
v_text = v_text.replace("de_y + 288", "de_y + 238")
v_text = v_text.replace("de_y + 360", "de_y + 308")
v_text = v_text.replace("de_y + 432", "de_y + 378")
v_text = v_text.replace("de_y + 504", "de_y + 448")

# Fill Tab 6 plaque with rich dual-column forensic readout
v_old_plaque = """  gfx_setfont(3, "Segoe UI", 13.5); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = ws_x + 38; gfx_y = plaque_y + 75;
  gfx_drawstr("Full master vocal forensic acoustic profile matching reference benchmarks. Recalls authentic Fairchild variable-mu glue,");
  gfx_x = ws_x + 38; gfx_y = plaque_y + 100;
  gfx_drawstr("tube saturation warmth, precision Baxandall tone curves, and high-frequency sibilance suppression.");
  gfx_x = ws_x + 38; gfx_y = plaque_y + 125;
  gfx_drawstr("Kel Pinchin (Preset 06) delivers pristine modern vocal sheen, transparent sibilance clamping, and forward presence.");"""

v_new_plaque = """  gfx_setfont(3, "Segoe UI", 13.5); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
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
  gfx_x = ws_x + 58 + sub_w; gfx_y = sub_y + 110; gfx_printf("Corridor Broadcast: %s", slider27 ? "ACTIVE RELAY" : "STANDBY");"""
v_text = v_text.replace(v_old_plaque, v_new_plaque)

with open(r"c:\Dev\DameiSuite\scratch\upgrade_vocal_bus.py", "w", encoding="utf-8") as f:
    f.write(v_text)

print("Applied precision polish to both builder scripts.")
