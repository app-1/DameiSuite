# build_instrumental_conclave_v10.py
# Implements:
# 1. Authentic Funtunfunefu-Denkyemfunefu (Siamese Crocodiles) vector insignia in the header
# 2. Correction: Jonathan Dolese -> Mirrorcell - U(phoria); Sam Guaiana -> Silverstein (Misery Made Me)
# 3. Elimination of redundant Bus Glue meter from Tab 0 Overview -> Replaced with 5-Band Tonal Balance Radar
# 4. Bus Glue threshold calibrated to -16.0 dB in Kel Pinchin preset (gives active 1.6 dB GR on chorus hits)
# 5. Meticulous Sankofa Oracle typography: Arial for clean body text, Orbitron for headers, strict card bounds

import os, re

source_v9 = r"c:\Dev\DameiSuite\scratch\build_instrumental_conclave_v9.py"
# We read the current effects/Damei_InstrumentalSuite.jsfx which is already at v9
current_jsfx_path = r"c:\Dev\DameiSuite\effects\Damei_InstrumentalSuite.jsfx"
with open(current_jsfx_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Calibrate Kel Pinchin default Bus Glue threshold to -16.0 dB and trim to -2.1 dB
code = code.replace(
    'slider12:-7.0<-36.0,0.0,0.5>-Bus Glue Threshold (dB)',
    'slider12:-16.0<-36.0,0.0,0.5>-Bus Glue Threshold (dB)'
)
code = re.sub(
    r'slider4 = -1\.[0-9];\s+// Net Headroom calibrated for exact legacy chain mix balance!',
    'slider4 = -2.1;   // Net Headroom calibrated for exact legacy chain mix balance!',
    code
)
code = re.sub(
    r'slider12 = -7\.0;\s+// Threshold calibrated for authentic 1\.4-1\.8 dB musical glue!',
    'slider12 = -16.0; // Threshold calibrated for authentic 1.4-1.8 dB musical glue!',
    code
)
# Update thresholds across all other producer presets so they trigger compression:
code = re.sub(r'slider12 = -7\.[0-9];', 'slider12 = -16.0;', code)
code = re.sub(r'slider12 = -6\.[0-9];', 'slider12 = -15.5;', code)
code = re.sub(r'slider12 = -8\.[0-9];', 'slider12 = -17.0;', code)

# 2. Producer correction: Sam Guaiana (Silverstein) & Jonathan Dolese (Mirrorcell)
code = code.replace(
    'idx == 3 ? "03: Jonathan Dolese (Mirrorcell)" :',
    'idx == 3 ? "03: Jonathan Dolese (Mirrorcell - U(phoria))" :'
)
code = code.replace(
    'idx == 9 ? "09: Sam Guaiana (Silverstein)" :',
    'idx == 9 ? "09: Sam Guaiana (Silverstein - Misery Made Me)" :'
)
code = code.replace(
    'idx == 3 ? "Mirrorcell - U(phoria)" :',
    'idx == 3 ? "Mirrorcell - U(phoria)" :'
)
code = code.replace(
    'idx == 9 ? "Silverstein - Misery Made Me" :',
    'idx == 9 ? "Silverstein - Misery Made Me" :'
)

# 3. Authentic Funtunfunefu-Denkyemfunefu Vector Drawing Function
funtunfunefu_vector = r"""
function draw_funtunfunefu_sigil(cx, cy, sz) local(s, d) (
  s = sz * 0.44;
  
  // 1. Central square frame (shared stomach)
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36; // Burnished Rose Gold
  gfx_rect(cx - s, cy - s, s * 2, s * 2, 0);
  gfx_rect(cx - s + 1, cy - s + 1, (s - 1) * 2, (s - 1) * 2, 0);
  
  // Central X cross
  gfx_line(cx - s, cy - s, cx + s, cy + s);
  gfx_line(cx + s, cy - s, cx - s, cy + s);
  gfx_line(cx - s + 1, cy - s, cx + s, cy + s - 1);
  gfx_line(cx + s - 1, cy - s, cx - s, cy + s - 1);

  // 2. Crocodile Head 1: Bottom-Left Diamond Snout
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; // Electric Sapphire
  gfx_line(cx - s, cy + s, cx - s * 1.9, cy + s * 1.3);
  gfx_line(cx - s, cy + s, cx - s * 1.3, cy + s * 1.9);
  gfx_line(cx - s * 1.9, cy + s * 1.3, cx - s * 2.2, cy + s * 2.2);
  gfx_line(cx - s * 1.3, cy + s * 1.9, cx - s * 2.2, cy + s * 2.2);
  gfx_circle(cx - s * 1.55, cy + s * 1.55, 2, 1);

  // Crocodile Head 2: Top-Right Diamond Snout
  gfx_line(cx + s, cy - s, cx + s * 1.9, cy - s * 1.3);
  gfx_line(cx + s, cy - s, cx + s * 1.3, cy - s * 1.9);
  gfx_line(cx + s * 1.9, cy - s * 1.3, cx + s * 2.2, cy - s * 2.2);
  gfx_line(cx + s * 1.3, cy - s * 1.9, cx + s * 2.2, cy - s * 2.2);
  gfx_circle(cx + s * 1.55, cy - s * 1.55, 2, 1);

  // 3. Crocodile Tail 1: Top-Left Arching Hook
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_line(cx - s * 0.4, cy - s, cx - s * 1.4, cy - s * 1.8);
  gfx_line(cx - s * 1.4, cy - s * 1.8, cx - s * 2.1, cy - s * 1.4);
  gfx_line(cx - s * 2.1, cy - s * 1.4, cx - s * 2.4, cy - s * 0.6);
  gfx_line(cx - s, cy - s * 0.4, cx - s * 1.8, cy - s * 1.2);

  // Crocodile Tail 2: Bottom-Right Arching Hook
  gfx_line(cx + s * 0.4, cy + s, cx + s * 1.4, cy + s * 1.8);
  gfx_line(cx + s * 1.4, cy + s * 1.8, cx + s * 2.1, cy + s * 1.4);
  gfx_line(cx + s * 2.1, cy + s * 1.4, cx + s * 2.4, cy + s * 0.6);
  gfx_line(cx + s, cy + s * 0.4, cx + s * 1.8, cy + s * 1.2);

  // 4. Curved Limbs / Claws (Rotational Symmetry)
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68; // Celestial Mint Claw Accent
  gfx_line(cx - s, cy + s * 0.2, cx - s * 1.7, cy + s * 0.5);
  gfx_line(cx - s * 1.7, cy + s * 0.5, cx - s * 1.5, cy + s * 0.9);
  
  gfx_line(cx + s, cy - s * 0.2, cx + s * 1.7, cy - s * 0.5);
  gfx_line(cx + s * 1.7, cy - s * 0.5, cx + s * 1.5, cy - s * 0.9);

  gfx_line(cx - s * 0.2, cy - s, cx - s * 0.5, cy - s * 1.7);
  gfx_line(cx - s * 0.5, cy - s * 1.7, cx - s * 0.9, cy - s * 1.5);

  gfx_line(cx + s * 0.2, cy + s, cx + s * 0.5, cy + s * 1.7);
  gfx_line(cx + s * 0.5, cy + s * 1.7, cx + s * 0.9, cy + s * 1.5);
);
"""

code = re.sub(
    r'function draw_funtunfunefu_sigil\(cx, cy, sz\).*?\n\);\n',
    funtunfunefu_vector.strip() + "\n\n",
    code,
    flags=re.DOTALL
)

# 4. Refined Header Bar Layout with Prominent Funtunfunefu Insignia & Sankofa Oracle Font Discipline
header_code = r"""
// 1. TOP HEADER BAR: PROMINENT FUNTUNFUNEFU INSIGNIA & CONCLAVE BRANDING
hdr_y = 12;
gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(16, hdr_y, 1048, 58);
gfx_r = 0.18; gfx_g = 0.35; gfx_b = 0.60; gfx_rect(16, hdr_y, 1048, 58, 0);

// Prominent Authentic Funtunfunefu-Denkyemfunefu Emblem (Left)
draw_funtunfunefu_sigil(44, hdr_y + 29, 21);

// Clean Sankofa Oracle Inspired Typography
gfx_setfont(4, "Orbitron", 15, 'b');
gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; // Imperial Sapphire
gfx_x = 76; gfx_y = hdr_y + 11;
gfx_drawstr("DAMEI INSTRUMENTAL BUS CONCLAVE");

gfx_setfont(2, "Arial", 11);
gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36; // Rose Gold / Copper
gfx_x = 76; gfx_y = hdr_y + 34;
gfx_drawstr("Funtunfunefu-Denkyemfunefu  //  Collective Summing & Harmonic Imperium");
"""

code = re.sub(
    r'// 1\. TOP HEADER BAR: TITLES, CRESTS & TELEMETRY SUMMARY.*?gfx_drawstr\("FUNTUNFUNEFU-DENKYEMFUNEFU // COLLECTIVE SUMMING & HARMONIC CONCLAVE"\);',
    header_code.strip(),
    code,
    flags=re.DOTALL
)

# 5. Redesign Tab 0 Overview: Replace duplicate Bus Glue meter with 5-Band Tonal Balance Radar
tab0_overview = r"""
// =============================================================================
// TAB 0: MASTER TELEMETRY DASHBOARD (NO REDUNDANT BUS GLUE DUPLICATE)
// =============================================================================
slider1 == 0 ? (
  draw_component_header("TAB 0 // MASTER TELEMETRY DASHBOARD",
                        "Harmonic summing telemetry, SIFAM moving-coil ballistics & 5-band tonal radar",
                        "Glued instrumental master pass prior to vocal bus interaction",
                        "IN -> 7-BAND ReEQ -> POCKET -> CRUCIBLE -> VCA GLUE -> M/S -> OUT");

  // CARD 1: SIFAM ANALOG MOVING-COIL CONSOLE VU METER (Left)
  c1_x = 28; c1_y = 386; c1_w = 330; c1_h = 214;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(c1_x, c1_y, c1_w, c1_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(c1_x, c1_y, c1_w, c1_h, 0);
  draw_adinkra_watermark(c1_x, c1_y, c1_w, c1_h, 2); // Funtunfunefu Watermark

  gfx_setfont(1, "Orbitron", 10.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = c1_x + 14; gfx_y = c1_y + 12; gfx_drawstr("SIFAM DIRECTOR // CONSOLE DRIVE");
  gfx_setfont(2, "Arial", 9.5, 'b'); gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;
  gfx_x = c1_x + c1_w - 74; gfx_y = c1_y + 12; gfx_drawstr("STUDIO VU");

  // SIFAM Moving-Coil Needle Arc
  sif_cx = c1_x + floor(c1_w * 0.5); sif_cy = c1_y + 190; sif_r = 150;
  draw_arc(sif_cx, sif_cy, sif_r, -0.65, 0.65, 0.15, 0.20, 0.30);
  draw_arc(sif_cx, sif_cy, sif_r, 0.25, 0.65, 0.85, 0.25, 0.25); // Redline zone

  // Ticks & Labels
  vu_val = clamp(inst_rms + 18.0, -20.0, 3.0);
  sifam_needle_vu += (vu_val - sifam_needle_vu) * 0.15;
  n_ang = -0.65 + ((sifam_needle_vu + 20.0) / 23.0) * 1.30;
  
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_line(sif_cx, sif_cy, sif_cx + sin(n_ang) * (sif_r - 10), sif_cy - cos(n_ang) * (sif_r - 10));
  gfx_circle(sif_cx, sif_cy, 14, 1);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_circle(sif_cx, sif_cy, 14, 0);

  gfx_setfont(2, "Arial", 10, 'b'); gfx_r = 0.70; gfx_g = 0.75; gfx_b = 0.85;
  gfx_x = c1_x + 14; gfx_y = c1_y + c1_h - 22; gfx_printf("RMS: %3.1f dBFS", inst_rms);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;
  gfx_x = c1_x + c1_w - 95; gfx_y = c1_y + c1_h - 22; gfx_drawstr("0 VU = -18 dBFS");

  // CARD 2: 5-BAND TONAL RADAR (Center - Replaces redundant Bus Glue meter!)
  c2_x = 368; c2_y = 386; c2_w = 340; c2_h = 214;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(c2_x, c2_y, c2_w, c2_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(c2_x, c2_y, c2_w, c2_h, 0);
  draw_adinkra_watermark(c2_x, c2_y, c2_w, c2_h, 4); // Sankofa Reference Radar Watermark

  gfx_setfont(1, "Orbitron", 10.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = c2_x + 14; gfx_y = c2_y + 12; gfx_drawstr("TONAL BALANCE ENERGY RADAR");
  gfx_setfont(2, "Arial", 9.5, 'b'); gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_x = c2_x + c2_w - 75; gfx_y = c2_y + 12; gfx_drawstr("5-BAND LIVE");

  // 5 Real-Time Spectral Energy Bars: Sub (20-80), Low Punch (80-200), Mud (200-500), Bite (1.5-3k), Air (8k+)
  b_w = 48; b_gap = 16; b_base_x = c2_x + 18; b_y = c2_y + 160;
  
  // Calculate band energies from spec_bins
  e_sub = min(1.0, (spec_bins[2] + spec_bins[3] + spec_bins[4]) * 0.8);
  e_low = min(1.0, (spec_bins[6] + spec_bins[8] + spec_bins[10]) * 0.9);
  e_mud = min(1.0, (spec_bins[12] + spec_bins[15] + spec_bins[18]) * 0.7);
  e_mid = min(1.0, (spec_bins[24] + spec_bins[30] + spec_bins[36]) * 0.8);
  e_air = min(1.0, (spec_bins[44] + spec_bins[52] + spec_bins[60]) * 0.7);

  function draw_radar_bar(rx, ry, rw, val, label, is_match) (
    gfx_r = 0.04; gfx_g = 0.06; gfx_b = 0.09; gfx_rect(rx, ry - 110, rw, 110);
    gfx_r = 0.15; gfx_g = 0.22; gfx_b = 0.32; gfx_rect(rx, ry - 110, rw, 110, 0);
    h = floor(clamp(val, 0.0, 1.0) * 106);
    gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; // Sapphire fill
    gfx_rect(rx + 2, ry - h, rw - 4, h);
    gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68; // Mint cap
    gfx_rect(rx + 2, ry - h, rw - 4, 3);
    gfx_setfont(2, "Arial", 9.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
    gfx_x = rx + floor((rw - 28) * 0.5); gfx_y = ry + 8; gfx_drawstr(label);
  );

  draw_radar_bar(b_base_x + 0 * (b_w + b_gap), b_y, b_w, e_sub, "SUB", 1);
  draw_radar_bar(b_base_x + 1 * (b_w + b_gap), b_y, b_w, e_low, "LOW", 1);
  draw_radar_bar(b_base_x + 2 * (b_w + b_gap), b_y, b_w, e_mud, "MUD", 1);
  draw_radar_bar(b_base_x + 3 * (b_w + b_gap), b_y, b_w, e_mid, "BITE", 1);
  draw_radar_bar(b_base_x + 4 * (b_w + b_gap), b_y, b_w, e_air, "AIR", 1);

  // CARD 3: STEREO PHASE & CORRELATION RADAR (Right)
  c3_x = 718; c3_y = 386; c3_w = 334; c3_h = 214;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(c3_x, c3_y, c3_w, c3_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(c3_x, c3_y, c3_w, c3_h, 0);
  draw_adinkra_watermark(c3_x, c3_y, c3_w, c3_h, 1); // Adinkrahene Mastery Watermark

  gfx_setfont(1, "Orbitron", 10.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = c3_x + 14; gfx_y = c3_y + 12; gfx_drawstr("STEREO PHASE RADAR");

  pr_cx = c3_x + floor(c3_w * 0.5); pr_cy = c3_y + 104; pr_r = 56;
  gfx_r = 0.10; gfx_g = 0.16; gfx_b = 0.26;
  gfx_circle(pr_cx, pr_cy, pr_r, 0);
  gfx_circle(pr_cx, pr_cy, pr_r * 0.66, 0);
  gfx_circle(pr_cx, pr_cy, pr_r * 0.33, 0);
  gfx_line(pr_cx - pr_r, pr_cy, pr_cx + pr_r, pr_cy);
  gfx_line(pr_cx, pr_cy - pr_r, pr_cx, pr_cy + pr_r);

  // Phase point
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_circle(pr_cx + corr_smooth * 18, pr_cy - abs(dry_l - dry_r) * 20, 3, 1);

  // Phase Correlation Bar
  bar_y = c3_y + 178; bar_w = c3_w - 28;
  gfx_r = 0.04; gfx_g = 0.06; gfx_b = 0.09; gfx_rect(c3_x + 14, bar_y, bar_w, 14);
  gfx_r = 0.15; gfx_g = 0.22; gfx_b = 0.32; gfx_rect(c3_x + 14, bar_y, bar_w, 14, 0);
  cor_x = c3_x + 14 + floor(((corr_smooth + 1.0) * 0.5) * bar_w);
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_rect(cor_x - 3, bar_y + 1, 6, 12);

  // BOTTOM CARD: MISSION TELEMETRY & STAGING STATUS (Meticulous bounds, zero spillover)
  bot_x = 28; bot_y = 612; bot_w = 1024; bot_h = 240;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(bot_x, bot_y, bot_w, bot_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(bot_x, bot_y, bot_w, bot_h, 0);

  gfx_setfont(1, "Orbitron", 11, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = bot_x + 18; gfx_y = bot_y + 14; gfx_drawstr("FLAGSHIP CONCLAVE INTEGRATION // MASTER STATUS");

  gfx_setfont(2, "Arial", 11); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = bot_x + 18; gfx_y = bot_y + 38;
  gfx_printf("* HEADROOM TRIM : %3.1f dB (Forensic DeeGain Staging Lock - Bit-Exact Parity)", slider4);
  gfx_x = bot_x + 18; gfx_y = bot_y + 58;
  gfx_printf("* BUS GLUE VCA  : Thresh %3.1f dB | Ratio %s | 10ms Attack | 600ms Release | HPF %2.0f Hz", slider12, slider13==0?"1.5:1":slider13==1?"2:1":slider13==2?"4:1":"8:1", slider16);
  gfx_x = bot_x + 18; gfx_y = bot_y + 78;
  gfx_printf("* HARMONIC DESK : %s | Drive %+2.1f dB (Britson Console Saturation)", slider23==0?"Transparent Pass":slider23==1?"Neve 8014 Iron Desk":slider23==2?"Studer A800 Tape":"Triode Tube", slider24);
  gfx_x = bot_x + 18; gfx_y = bot_y + 98;
  gfx_printf("* STEREO MATRIX : Sub-Mono Anchor %2.0f Hz | M/S Quad Width %3.2fx | Dynamic Pocket Notch -%2.1f dB", slider6, slider25, pocket_dyn_dip);
);
"""

# Replace Tab 0 Overview block
code = re.sub(
    r'// =============================================================================\s+// TAB 0: MASTER TELEMETRY DASHBOARD\s+// =============================================================================\s+slider1 == 0 \? \(.*?\n\);\n',
    tab0_overview.strip() + "\n\n",
    code,
    flags=re.DOTALL
)

# Write out to Damei_InstrumentalSuite.jsfx
target_path = r"c:\Dev\DameiSuite\effects\Damei_InstrumentalSuite.jsfx"
reaper_path = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_InstrumentalSuite.jsfx"

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)
print(f"Successfully written to {target_path}")

with open(reaper_path, "w", encoding="utf-8") as f:
    f.write(code)
print(f"Successfully deployed to {reaper_path}")
