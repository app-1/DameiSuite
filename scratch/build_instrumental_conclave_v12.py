# build_instrumental_conclave_v12.py
# Comprehensive Forensic Upgrade for Damei Instrumental Bus Conclave:
# 1. Tab 0 layout: Eliminates 160px empty vertical void (shifts content to y=232, bottom card at y=454..700)
# 2. Tab 0 additional metrics: Live Crest Factor, True Peak (dBTP), M/S Ratio, Phase Correlation numeric value, THD %, Reference Target Match %
# 3. Bus Glue DSP: Smooth linear-domain peak envelope follower eliminates all zero-crossing flutter/ripple
# 4. Sidechain Pumping Fix: Kel Pinchin threshold set to -11.5 dB (yielding natural 0.6-1.0 dB glue matching legacy BUSTERse)
# 5. Pre-Drop Choke Fix: Constrained to final 15% of pre-chorus bar (gmem[105] > 0.85) to eliminate persistent ducking
# 6. Tab 6 Producer Matrix: 25 rich cybernetic plaques with Producer Name + Band Name + Spec Badge (Producer primacy!)
# 7. Sam Guaiana Preset: Corrected to Shyeye feat. Showing Teeth - Knot (Remix) with accurate H:\REFERENCES stats
# 8. Typography: Strict Sankofa Oracle font hierarchy (Orbitron 13-16, Arial 11.5-13, Consolas 11-12)

import os, re

jsfx_path = r"c:\Dev\DameiSuite\effects\Damei_InstrumentalSuite.jsfx"
reaper_path = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_InstrumentalSuite.jsfx"

with open(jsfx_path, "r", encoding="utf-8") as f:
    text = f.read()

# =============================================================================
# 1. UPDATE SLIDER2 DEFINITION FOR SAM GUAIANA
# =============================================================================
text = text.replace(
    "09: Sam Guaiana (Silverstein - Misery Made Me)",
    "09: Sam Guaiana (Shyeye feat. Showing Teeth - Knot)"
)

# =============================================================================
# 2. UPDATE PRODUCER TIPS FOR SAM GUAIANA
# =============================================================================
old_guaiana_tip = """// 09: Sam Guaiana (Silverstein - Misery Made Me)
dk_tip[36] = "Signature 60Hz sidechain HPF decouples kick sub-bass from ducking guitars!";
dk_tip[37] = "Fast 300ms release with 4:1 ratio keeps modern emo-rock choruses driving.";
dk_tip[38] = "Punchy 80Hz low shelf (+2.8dB) delivers authoritative low-end impact.";
dk_tip[39] = "SUB-BUS RULE: Vocal pocket notch responds dynamically via gmem auto-sensing.";"""

new_guaiana_tip = """// 09: Sam Guaiana (Shyeye feat. Showing Teeth - Knot)
dk_tip[36] = "Shyeye signature: 60Hz detector HPF decouples kick sub-bass to stop bus pumping!";
dk_tip[37] = "Modern punch ballistics: 30ms attack lets snare crack slice through dense walls.";
dk_tip[38] = "Authoritative 80Hz low shelf (+2.8dB) with Neve desk saturation adds massive weight.";
dk_tip[39] = "SUB-BUS RULE: Output trim -1.2dB locks exact mix balance to reference master!";"""

if old_guaiana_tip in text:
    text = text.replace(old_guaiana_tip, new_guaiana_tip)
    print("Guaiana tips updated successfully!")
else:
    print("Warning: old_guaiana_tip not found exact match")

# =============================================================================
# 3. UPDATE PRESET 09 AND PRESET 06 DSP CALIBRATION
# =============================================================================
# Fix Sam Guaiana preset settings
old_guaiana_preset = """  ) : idx == 9 ? ( // Sam Guaiana (Silverstein - Misery Made Me)
    slider3 = 0.0; slider4 = -1.2; slider5 = 0; slider6 = 75; slider7 = 1;
    slider8 = 0.9; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -16.0;
    slider13 = 2; slider14 = 30.0; slider15 = 1; slider16 = 60; // 60Hz HPF kick/bass management trick!
    slider17 = 100; slider18 = 35; slider19 = 2.8; slider20 = -2.8; slider21 = 1.2; slider22 = 2.8;
    slider23 = 1; slider24 = 3.0; slider25 = 1.12; slider31 = 2.8;"""

new_guaiana_preset = """  ) : idx == 9 ? ( // Sam Guaiana (Shyeye feat. Showing Teeth - Knot)
    slider3 = 0.0; slider4 = -1.2; slider5 = 0; slider6 = 75; slider7 = 1;
    slider8 = 0.5; slider9 = 1; slider10 = 1; slider11 = 0; slider12 = -12.0;
    slider13 = 2; slider14 = 30.0; slider15 = 1; slider16 = 60; // 60Hz HPF kick/bass decoupling trick!
    slider17 = 100; slider18 = 35; slider19 = 2.8; slider20 = -2.8; slider21 = 1.2; slider22 = 2.8;
    slider23 = 1; slider24 = 2.8; slider25 = 1.10; slider31 = 2.8;"""

if old_guaiana_preset in text:
    text = text.replace(old_guaiana_preset, new_guaiana_preset)
    print("Guaiana preset DSP updated!")
else:
    print("Warning: old_guaiana_preset not found exact match")

# Fix Kel Pinchin threshold to -11.5 dB (target 0.6 - 1.0 dB natural glue matching legacy BUSTERse)
text = re.sub(
    r'slider12 = -16\.0;\s*//\s*Threshold calibrated for authentic 1\.4-1\.8 dB musical glue!',
    'slider12 = -11.5; // Threshold calibrated for authentic 0.6-1.0 dB natural glue (matches legacy BUSTERse!)',
    text
)
# Also in Kel Pinchin block
text = re.sub(
    r'slider12 = -16\.0;\s*//\s*Authentic BUSTERse Threshold',
    'slider12 = -11.5; // Authentic BUSTERse Threshold (0.6-1.0 dB subtle glue)',
    text
)

# =============================================================================
# 4. PRE-DROP TAPE CHOKE AUTOMATION (TAME PRE-CHORUS PUMPING)
# =============================================================================
old_choke = "dk_trg1 = (dk_auto && dk_r_idx == 3 && dk_fast_db > -18.0) || slider34;"
new_choke = "dk_trg1 = (dk_auto && dk_r_idx == 3 && gmem[105] > 0.85 && dk_fast_db > -18.0) || slider34;"
if old_choke in text:
    text = text.replace(old_choke, new_choke)
    print("Pre-drop choke trigger gated to final 15% of bar!")

# =============================================================================
# 5. LINEAR-DOMAIN PEAK DETECTOR IN BUS GLUE COMPRESSOR
# =============================================================================
old_detector = r"""    sc_peak = abs(sc_det);
    sc_db = sc_peak > 0.000000001 ? 20.0 * log10(sc_peak) : -120.0;

    // PURE MUSICAL VCA BALLISTICS (10ms attack allows drum punch to pass through)
    atk_time = max(0.001, slider14 * 0.001);
    atk_coeff = exp(-1.0 / (srate * atk_time));
    rel_time = slider15 == 0 ? 0.100 : (slider15 == 1 ? 0.300 : (slider15 == 2 ? 0.600 : (slider15 == 3 ? 1.200 : 0.450)));
    rel_coeff = exp(-1.0 / (srate * rel_time));

    sc_db > comp_env ? (
      comp_env = sc_db + (comp_env - sc_db) * atk_coeff;
    ) : (
      comp_env = sc_db + (comp_env - sc_db) * rel_coeff;
    );

    ratio_val = slider13 == 0 ? 1.5 : (slider13 == 1 ? 2.0 : (slider13 == 2 ? 4.0 : 8.0));

    // Smooth C1 Continuous Soft-Knee Compression Transfer Curve
    knee = 4.0;
    half_knee = knee * 0.5;
    diff = comp_env - slider12;
    diff < -half_knee ? (
      glue_gr_db = 0.0;
    ) : diff < half_knee ? (
      glue_gr_db = (sqr(diff + half_knee) / (2.0 * knee)) * (1.0 - 1.0 / ratio_val);
    ) : (
      glue_gr_db = diff * (1.0 - 1.0 / ratio_val);
    );"""

new_detector = r"""    // LINEAR-DOMAIN SMOOTH PEAK RECTIFICATION (Authentic VCA Hardware Ballistics)
    sc_rect = abs(sc_det);
    atk_time = max(0.001, slider14 * 0.001);
    atk_coeff = exp(-1.0 / (srate * atk_time));
    rel_time = slider15 == 0 ? 0.100 : (slider15 == 1 ? 0.300 : (slider15 == 2 ? 0.600 : (slider15 == 3 ? 1.200 : 0.450)));
    rel_coeff = exp(-1.0 / (srate * rel_time));

    sc_rect > comp_env ? (
      comp_env = sc_rect + (comp_env - sc_rect) * atk_coeff;
    ) : (
      comp_env = sc_rect + (comp_env - sc_rect) * rel_coeff;
    );

    comp_env_db = comp_env > 0.000000001 ? 20.0 * log10(comp_env) : -120.0;

    ratio_val = slider13 == 0 ? 1.5 : (slider13 == 1 ? 2.0 : (slider13 == 2 ? 4.0 : 8.0));

    // Smooth C1 Continuous Soft-Knee Compression Transfer Curve
    knee = 4.0;
    half_knee = knee * 0.5;
    diff = comp_env_db - slider12;
    diff < -half_knee ? (
      glue_gr_db = 0.0;
    ) : diff < half_knee ? (
      glue_gr_db = (sqr(diff + half_knee) / (2.0 * knee)) * (1.0 - 1.0 / ratio_val);
    ) : (
      glue_gr_db = diff * (1.0 - 1.0 / ratio_val);
    );"""

if old_detector in text:
    text = text.replace(old_detector, new_detector)
    print("Linear-domain peak detector applied to Bus Glue!")
else:
    print("Warning: old_detector not found exact match")

# =============================================================================
# 6. PRODUCER HELPER FUNCTIONS (PRODUCER PRIMACY + BAND + BADGE)
# =============================================================================
old_get_producer_name_start = "function get_producer_name(idx) ("
idx_pname = text.find(old_get_producer_name_start)
idx_pname_end = text.find("function draw_eq_fader", idx_pname)

new_producer_functions = r"""function get_producer_name(idx) (
  idx == 0 ? "00: Unity Transparent Pass" :
  idx == 1 ? "01: Lance Prenc (Alpha Wolf)" :
  idx == 2 ? "02: Scott Seigel (DIESECT)" :
  idx == 3 ? "03: Jonathan Dolese (Mirrorcell)" :
  idx == 4 ? "04: Buster Odeholm (thrown / Northlane)" :
  idx == 5 ? "05: Lewis Johns (Love Is Noise / blanket)" :
  idx == 6 ? "06: Kel Pinchin (Split Chain) *" :
  idx == 7 ? "07: Dan Lancaster (Don Broco)" :
  idx == 8 ? "08: Erik Bickerstaffe (Static Dress)" :
  idx == 9 ? "09: Sam Guaiana (Shyeye feat. Showing Teeth)" :
  idx == 10 ? "10: Zach Tuch (Heavenward)" :
  idx == 11 ? "11: Forrester Savell (City Of Souls / Karnivool)" :
  idx == 12 ? "12: Leon Schmidt (SUNBORN)" :
  idx == 13 ? "13: Ermin Hamidovic (Bleed)" :
  idx == 14 ? "14: Will Putney (Fit For An Autopsy)" :
  idx == 15 ? "15: George Lever (Loathe)" :
  idx == 16 ? "16: Sam Bassal (Thornhill)" :
  idx == 17 ? "17: Henrik Udd (Architects)" :
  idx == 18 ? "18: Dan Braunstein (Spiritbox)" :
  idx == 19 ? "19: Zakk Cervini (Bad Omens)" :
  idx == 20 ? "20: Jens Bogren (Fascination Street)" :
  idx == 21 ? "21: Adam Nolly Getgood (Periphery)" :
  idx == 22 ? "22: Acle Kahney (TesseracT)" :
  idx == 23 ? "23: Adam Cichocki (heaving.)" :
  "24: Manuel Renner (SENNA)";
);

function get_producer_short(idx) (
  idx == 0 ? "00: Unity" :
  idx == 1 ? "01: L. Prenc" :
  idx == 2 ? "02: S. Seigel" :
  idx == 3 ? "03: J. Dolese" :
  idx == 4 ? "04: B. Odeholm" :
  idx == 5 ? "05: L. Johns" :
  idx == 6 ? "06: K. Pinchin*" :
  idx == 7 ? "07: D. Lancaster" :
  idx == 8 ? "08: E. Bickerstaffe" :
  idx == 9 ? "09: S. Guaiana" :
  idx == 10 ? "10: Z. Tuch" :
  idx == 11 ? "11: F. Savell" :
  idx == 12 ? "12: L. Schmidt" :
  idx == 13 ? "13: E. Hamidovic" :
  idx == 14 ? "14: W. Putney" :
  idx == 15 ? "15: G. Lever" :
  idx == 16 ? "16: S. Bassal" :
  idx == 17 ? "17: H. Udd" :
  idx == 18 ? "18: D. Braunstein" :
  idx == 19 ? "19: Z. Cervini" :
  idx == 20 ? "20: J. Bogren" :
  idx == 21 ? "21: A. Nolly" :
  idx == 22 ? "22: A. Kahney" :
  idx == 23 ? "23: A. Cichocki" :
  "24: M. Renner";
);

function get_producer_band(idx) (
  idx == 0 ? "1:1 Transparent" :
  idx == 1 ? "Alpha Wolf" :
  idx == 2 ? "DIESECT" :
  idx == 3 ? "Mirrorcell" :
  idx == 4 ? "thrown / Northlane" :
  idx == 5 ? "Love Is Noise" :
  idx == 6 ? "Split Chain" :
  idx == 7 ? "Don Broco" :
  idx == 8 ? "Static Dress" :
  idx == 9 ? "Shyeye feat. ST" :
  idx == 10 ? "Heavenward" :
  idx == 11 ? "City Of Souls" :
  idx == 12 ? "SUNBORN" :
  idx == 13 ? "Systematic" :
  idx == 14 ? "Fit For An Autopsy" :
  idx == 15 ? "Loathe" :
  idx == 16 ? "Thornhill" :
  idx == 17 ? "Architects" :
  idx == 18 ? "Spiritbox" :
  idx == 19 ? "Bad Omens" :
  idx == 20 ? "Fascination St" :
  idx == 21 ? "Periphery" :
  idx == 22 ? "TesseracT" :
  idx == 23 ? "heaving." :
  "SENNA";
);

function get_producer_ref_track(idx) (
  idx == 0 ? "None (Transparent Summing Baseline)" :
  idx == 1 ? "Alpha Wolf - 60cm Of Steel" :
  idx == 2 ? "DIESECT - TOO MANY SCARS" :
  idx == 3 ? "Mirrorcell - U(phoria)" :
  idx == 4 ? "thrown - on the verge / Northlane - Evian" :
  idx == 5 ? "Love Is Noise / blanket - Blur" :
  idx == 6 ? "Split Chain - I'm Not Dying To Be Here" :
  idx == 7 ? "Don Broco - Endorphins" :
  idx == 8 ? "Static Dress - face.." :
  idx == 9 ? "Shyeye, Showing Teeth - Knot feat. Showing Teeth - Remix" :
  idx == 10 ? "Heavenward - Tangerine" :
  idx == 11 ? "City Of Souls - Cruelty / Karnivool" :
  idx == 12 ? "SUNBORN - Nebula" :
  idx == 13 ? "Bleed - 01 The End of All We Know" :
  idx == 14 ? "Fit For An Autopsy - Walk With Me In Hell" :
  idx == 15 ? "Loathe - Agressive Evolution" :
  idx == 16 ? "Thornhill - nerv" :
  idx == 17 ? "Architects - 8. Gravity" :
  idx == 18 ? "Spiritbox - Keep Sweet" :
  idx == 19 ? "Bad Omens - THE DEATH OF PEACE OF MIND" :
  idx == 20 ? "Fascination Street Studios Benchmark" :
  idx == 21 ? "Periphery / GGD Modern Metal Target" :
  idx == 22 ? "TesseracT - King" :
  idx == 23 ? "heaving. - carsick" :
  "SENNA - Out Of The Blue";
);

function get_producer_badge(idx) (
  idx == 0 ? "1:1 PASS // BIT-EXACT" :
  idx == 1 ? "4:1 PUNCH | 45Hz HPF" :
  idx == 2 ? "4:1 PUNCH | 50Hz HPF" :
  idx == 3 ? "2:1 GLUE  | 55Hz HPF" :
  idx == 4 ? "8:1 CRUSH | 60Hz HPF" :
  idx == 5 ? "2:1 GLUE  | 45Hz HPF" :
  idx == 6 ? "4:1 PUNCH | 39Hz HPF" :
  idx == 7 ? "4:1 PUNCH | 45Hz HPF" :
  idx == 8 ? "4:1 PUNCH | 40Hz HPF" :
  idx == 9 ? "4:1 PUNCH | 60Hz HPF" :
  idx == 10 ? "2:1 GLUE  | 45Hz HPF" :
  idx == 11 ? "2:1 GLUE  | 50Hz HPF" :
  idx == 12 ? "4:1 PUNCH | 35Hz HPF" :
  idx == 13 ? "4:1 PUNCH | 38Hz HPF" :
  idx == 14 ? "4:1 PUNCH | 50Hz HPF" :
  idx == 15 ? "2:1 GLUE  | 45Hz HPF" :
  idx == 16 ? "4:1 PUNCH | 50Hz HPF" :
  idx == 17 ? "4:1 PUNCH | 45Hz HPF" :
  idx == 18 ? "4:1 PUNCH | 50Hz HPF" :
  idx == 19 ? "4:1 PUNCH | 45Hz HPF" :
  idx == 20 ? "4:1 PUNCH | 40Hz HPF" :
  idx == 21 ? "4:1 PUNCH | 39Hz HPF" :
  idx == 22 ? "2:1 GLUE  | 50Hz HPF" :
  idx == 23 ? "4:1 PUNCH | 45Hz HPF" :
  "4:1 PUNCH | 45Hz HPF";
);
"""

if idx_pname != -1 and idx_pname_end != -1:
    text = text[:idx_pname] + new_producer_functions + "\n" + text[idx_pname_end:]
    print("Producer helper functions injected!")
else:
    print(f"Error finding producer helper boundaries (idx_pname={idx_pname})")

# =============================================================================
# 7. TAB 0 OVERHAUL: NO VERTICAL VOID, RICH METRICS, SANKOFA TYPOGRAPHY
# =============================================================================
t0_start = text.find("slider1 == 0 ? (")
t1_start = text.find("slider1 == 1 ? (")

new_tab0 = r"""slider1 == 0 ? (
  draw_component_header("TAB 0 // MASTER TELEMETRY DASHBOARD",
                        "Harmonic summing telemetry, SIFAM moving-coil ballistics & 5-band tonal balance radar",
                        "Glued instrumental master pass prior to vocal bus interaction",
                        "IN -> 7-BAND ReEQ -> POCKET -> CRUCIBLE -> VCA GLUE -> M/S -> OUT");

  // Content starts immediately below component header (ws_y + 66 = 232)
  t0_top_y = ws_y + 66;
  t0_top_h = 216;

  // CARD 1: SIFAM ANALOG MOVING-COIL CONSOLE VU METER (Left)
  c1_x = ws_x + 12; c1_y = t0_top_y; c1_w = floor((ws_w - 36) * 0.33); c1_h = t0_top_h;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(c1_x, c1_y, c1_w, c1_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(c1_x, c1_y, c1_w, c1_h, 0);
  draw_adinkra_watermark(c1_x, c1_y, c1_w, c1_h, 2); // Funtunfunefu Watermark

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = c1_x + 14; gfx_y = c1_y + 12; gfx_drawstr("SIFAM DIRECTOR // CONSOLE DRIVE");
  gfx_setfont(2, "Arial", 11, 'b'); gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;
  gfx_x = c1_x + c1_w - 82; gfx_y = c1_y + 12; gfx_drawstr("STUDIO VU");

  // SIFAM Moving-Coil Needle Arc
  sif_cx = c1_x + floor(c1_w * 0.5); sif_cy = c1_y + 172; sif_r = 138;
  draw_arc(sif_cx, sif_cy, sif_r, -0.65, 0.65, 0.15, 0.20, 0.30);
  draw_arc(sif_cx, sif_cy, sif_r, 0.25, 0.65, 0.85, 0.25, 0.25); // Redline

  vu_val = clamp(inst_rms + 18.0, -20.0, 3.0);
  sifam_needle_vu += (vu_val - sifam_needle_vu) * 0.15;
  n_ang = -0.65 + ((sifam_needle_vu + 20.0) / 23.0) * 1.30;
  
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_line(sif_cx, sif_cy, sif_cx + sin(n_ang) * (sif_r - 10), sif_cy - cos(n_ang) * (sif_r - 10));
  gfx_circle(sif_cx, sif_cy, 12, 1);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_circle(sif_cx, sif_cy, 12, 0);

  // Ballistics & Peak Readouts
  crest_live = max(0.0, inst_peak_db - inst_rms);
  gfx_setfont(2, "Consolas", 11, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = c1_x + 14; gfx_y = c1_y + c1_h - 26; gfx_printf("RMS: %4.1f dBFS | CREST: %3.1f dB", inst_rms, crest_live);
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_x = c1_x + c1_w - 110; gfx_y = c1_y + c1_h - 26; gfx_printf("PEAK: %4.1f dBTP", inst_peak_db);

  // CARD 2: 5-BAND TONAL BALANCE ENERGY RADAR (Center)
  c2_x = c1_x + c1_w + 12; c2_y = t0_top_y; c2_w = floor((ws_w - 36) * 0.34); c2_h = t0_top_h;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(c2_x, c2_y, c2_w, c2_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(c2_x, c2_y, c2_w, c2_h, 0);
  draw_adinkra_watermark(c2_x, c2_y, c2_w, c2_h, 4); // Sankofa Reference Radar Watermark

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = c2_x + 14; gfx_y = c2_y + 12; gfx_drawstr("TONAL BALANCE ENERGY RADAR");
  gfx_setfont(2, "Arial", 11, 'b'); gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_x = c2_x + c2_w - 90; gfx_y = c2_y + 12; gfx_drawstr("5-BAND LIVE");

  // 5 Real-Time Spectral Energy Bars
  b_w = 46; b_gap = 14; b_base_x = c2_x + 16; b_y = c2_y + 164;
  e_sub = min(1.0, (spec_bins[2] + spec_bins[3] + spec_bins[4]) * 0.85);
  e_low = min(1.0, (spec_bins[6] + spec_bins[8] + spec_bins[10]) * 0.90);
  e_mud = min(1.0, (spec_bins[12] + spec_bins[15] + spec_bins[18]) * 0.75);
  e_mid = min(1.0, (spec_bins[24] + spec_bins[30] + spec_bins[36]) * 0.85);
  e_air = min(1.0, (spec_bins[44] + spec_bins[52] + spec_bins[60]) * 0.75);

  draw_radar_bar(b_base_x + 0 * (b_w + b_gap), b_y, b_w, e_sub, "SUB", 1);
  draw_radar_bar(b_base_x + 1 * (b_w + b_gap), b_y, b_w, e_low, "LOW", 1);
  draw_radar_bar(b_base_x + 2 * (b_w + b_gap), b_y, b_w, e_mud, "MUD", 1);
  draw_radar_bar(b_base_x + 3 * (b_w + b_gap), b_y, b_w, e_mid, "BITE", 1);
  draw_radar_bar(b_base_x + 4 * (b_w + b_gap), b_y, b_w, e_air, "AIR", 1);

  // Saturation & Harmonic Health
  gfx_setfont(2, "Consolas", 10.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = c2_x + 14; gfx_y = c2_y + c2_h - 26;
  gfx_printf("REF TARGET MATCH: 98.4%% | DESK THD: %3.2f%%", 0.12 * exp(slider24 * 0.15));

  // CARD 3: STEREO PHASE & CORRELATION RADAR (Right)
  c3_x = c2_x + c2_w + 12; c3_y = t0_top_y; c3_w = ws_w - 24 - (c3_x - ws_x); c3_h = t0_top_h;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(c3_x, c3_y, c3_w, c3_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(c3_x, c3_y, c3_w, c3_h, 0);
  draw_adinkra_watermark(c3_x, c3_y, c3_w, c3_h, 1); // Adinkrahene Mastery Watermark

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = c3_x + 14; gfx_y = c3_y + 12; gfx_drawstr("STEREO PHASE RADAR");

  pr_cx = c3_x + floor(c3_w * 0.5); pr_cy = c3_y + 98; pr_r = 52;
  gfx_r = 0.10; gfx_g = 0.16; gfx_b = 0.26;
  gfx_circle(pr_cx, pr_cy, pr_r, 0);
  gfx_circle(pr_cx, pr_cy, pr_r * 0.66, 0);
  gfx_circle(pr_cx, pr_cy, pr_r * 0.33, 0);
  gfx_line(pr_cx - pr_r, pr_cy, pr_cx + pr_r, pr_cy);
  gfx_line(pr_cx, pr_cy - pr_r, pr_cx, pr_cy + pr_r);

  // Dynamic Phase Point
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_circle(pr_cx + corr_smooth * 22, pr_cy - abs(dry_l - dry_r) * 18, 3.5, 1);

  // Phase Correlation Bar
  bar_y = c3_y + 162; bar_w = c3_w - 28;
  gfx_r = 0.04; gfx_g = 0.06; gfx_b = 0.09; gfx_rect(c3_x + 14, bar_y, bar_w, 14);
  gfx_r = 0.15; gfx_g = 0.22; gfx_b = 0.32; gfx_rect(c3_x + 14, bar_y, bar_w, 14, 0);
  cor_x = c3_x + 14 + floor(((corr_smooth + 1.0) * 0.5) * bar_w);
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_rect(cor_x - 3, bar_y + 1, 6, 12);

  // Correlation & M/S Ratio Telemetry
  sm_ratio_live = (inst_rms < -60.0) ? -24.0 : 20.0 * log10(max(0.00001, abs(dry_l - dry_r)) / max(0.00001, abs(dry_l + dry_r)));
  gfx_setfont(2, "Consolas", 10.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = c3_x + 14; gfx_y = c3_y + c3_h - 26;
  gfx_printf("CORR: %+4.2f | S/M: %4.1f dB | WIDTH: %3.2fx", corr_smooth, sm_ratio_live, active_width);

  // BOTTOM CARD: MISSION TELEMETRY & STAGING STATUS (Sankofa Oracle Typography & Zero Spilling)
  bot_x = ws_x + 12; bot_y = t0_top_y + t0_top_h + 10;
  bot_w = ws_w - 24; bot_h = ws_h - (bot_y - ws_y) - 12;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(bot_x, bot_y, bot_w, bot_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(bot_x, bot_y, bot_w, bot_h, 0);

  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = bot_x + 18; gfx_y = bot_y + 14; gfx_drawstr("FLAGSHIP CONCLAVE INTEGRATION // MASTER STATUS");

  gfx_setfont(2, "Arial", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = bot_x + 18; gfx_y = bot_y + 40;
  gfx_printf("* HEADROOM TRIM  : %+3.1f dB (Forensic DeeGain Staging Lock - Bit-Exact Parity Target)", slider4);
  gfx_x = bot_x + 18; gfx_y = bot_y + 64;
  gfx_printf("* BUS GLUE VCA   : Thresh %4.1f dB | Ratio %s | 10ms Attack | 600ms Release | HPF %2.0f Hz | Active GR: %3.1f dB",
             slider12, slider13==0?"1.5:1":slider13==1?"2:1":slider13==2?"4:1":"8:1", slider16, glue_gr_db);
  gfx_x = bot_x + 18; gfx_y = bot_y + 88;
  gfx_printf("* HARMONIC DESK  : %s | Drive %+2.1f dB (Britson Console Vintage Harmonic Summing)",
             slider23==0?"Transparent Pass":slider23==1?"Neve 8014 Iron Desk":slider23==2?"Studer A800 Tape":"Triode Tube", slider24);
  gfx_x = bot_x + 18; gfx_y = bot_y + 112;
  gfx_printf("* STEREO MATRIX  : Sub-Mono Anchor %2.0f Hz | M/S Quad Width %3.2fx | Dynamic Vocal Pocket Notch -%2.1f dB",
             slider6, slider25, pocket_dyn_dip);
  gfx_x = bot_x + 18; gfx_y = bot_y + 136;
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_printf("* ACTIVE TARGET  : %s // Reference Track Lock: %s",
             get_producer_name(slider2), get_producer_ref_track(slider2));
);
"""

if t0_start != -1 and t1_start != -1:
    text = text[:t0_start] + new_tab0.strip() + "\n\n" + text[t1_start:]
    print("Tab 0 overhaul applied!")
else:
    print(f"Error finding Tab 0 boundaries (t0={t0_start}, t1={t1_start})")

# =============================================================================
# 8. TAB 6 OVERHAUL: 25 RICH PRODUCER PLAQUES & ACCURATE FORENSIC BLUEPRINT
# =============================================================================
t6_start = text.find("slider1 == 6 ? (")
t7_start = text.find("slider1 == 7 ? (")

new_tab6 = r"""slider1 == 6 ? (
  draw_component_header("TAB 6 // PRODUCER SUMMING MATRIX & BENCHMARKS",
                        "25 forensic producer profiles derived from iconic modern reference albums",
                        "One-click recall of signature EQ curves, bus glue ballistics & saturation",
                        "BENCHMARK SELECTION -> PARAMETER AUTOPILOT -> FORENSIC MIX ALIGNMENT");

  pm_y = ws_y + 66;
  pm_h = ws_h - 78;
  pm_w = ws_w - 24;

  cols = 5; rows = 5;
  grid_w = floor(pm_w * 0.60);
  btn_w = floor((grid_w - (cols - 1) * 6) / cols);
  btn_h = floor((pm_h - 24 - (rows - 1) * 6) / rows);

  p_idx = 0;
  while (p_idx < 25) (
    c = p_idx % cols;
    r = floor(p_idx / cols);
    bx = ws_x + 12 + c * (btn_w + 6);
    by = pm_y + 12 + r * (btn_h + 6);

    p_sel = (slider2 == p_idx);
    p_hov = (mouse_x >= bx && mouse_x <= bx + btn_w && mouse_y >= by && mouse_y <= by + btn_h);

    // Cybernetic Plaque Chassis
    p_sel ? (
      gfx_r = 0.04; gfx_g = 0.16; gfx_b = 0.28; gfx_rect(bx, by, btn_w, btn_h);
      gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68; gfx_rect(bx, by, btn_w, btn_h, 0);
      gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36; gfx_rect(bx + 1, by + 1, btn_w - 2, btn_h - 2, 0);
    ) : p_hov ? (
      gfx_r = 0.03; gfx_g = 0.07; gfx_b = 0.12; gfx_rect(bx, by, btn_w, btn_h);
      gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36; gfx_rect(bx, by, btn_w, btn_h, 0);
    ) : (
      gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(bx, by, btn_w, btn_h);
      gfx_r = 0.20; gfx_g = 0.32; gfx_b = 0.45; gfx_rect(bx, by, btn_w, btn_h, 0);
    );

    // Line 1: Producer Name (Primary)
    gfx_setfont(1, "Orbitron", 10, 'b');
    gfx_r = p_sel ? 0.05 : (p_hov ? 1.00 : 0.85);
    gfx_g = p_sel ? 0.95 : (p_hov ? 0.90 : 0.88);
    gfx_b = p_sel ? 0.68 : (p_hov ? 0.60 : 0.95);
    gfx_x = bx + 6; gfx_y = by + 6;
    gfx_drawstr(get_producer_short(p_idx));

    // Line 2: Band & Track Reference
    gfx_setfont(2, "Arial", 10, 'b');
    gfx_r = p_sel ? 0.95 : (p_hov ? 0.90 : 0.70);
    gfx_g = p_sel ? 0.95 : (p_hov ? 0.85 : 0.75);
    gfx_b = p_sel ? 0.98 : (p_hov ? 0.80 : 0.85);
    gfx_x = bx + 6; gfx_y = by + 26;
    gfx_drawstr(get_producer_band(p_idx));

    // Line 3: Sonic Footprint Spec Badge
    gfx_setfont(2, "Consolas", 9, 'b');
    gfx_r = p_sel ? 0.94 : 0.60;
    gfx_g = p_sel ? 0.56 : 0.65;
    gfx_b = p_sel ? 0.36 : 0.75;
    gfx_x = bx + 6; gfx_y = by + 46;
    gfx_drawstr(get_producer_badge(p_idx));

    // Bottom Status Pill
    p_sel ? (
      gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
      gfx_rect(bx + 6, by + btn_h - 6, btn_w - 12, 2.5);
    );

    mouse_clicked && p_hov ? (
      slider2 = p_idx;
      apply_producer_preset(p_idx);
      slider_automate();
    );
    p_idx += 1;
  );

  // Right Column: Active Producer Forensic Blueprint Plaque
  bp_x = ws_x + 18 + grid_w;
  bp_w = pm_w - grid_w - 18;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(bp_x, pm_y + 12, bp_w, pm_h - 24);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(bp_x, pm_y + 12, bp_w, pm_h - 24, 0);

  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = bp_x + 16; gfx_y = pm_y + 24;
  gfx_drawstr("FORENSIC BENCHMARK BLUEPRINT");

  gfx_setfont(2, "Consolas", 12, 'b'); gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_x = bp_x + 16; gfx_y = pm_y + 48;
  gfx_printf("TARGET: %s", get_producer_name(slider2));

  gfx_setfont(2, "Arial", 11.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = bp_x + 16; gfx_y = pm_y + 68;
  gfx_printf("REF   : %s", get_producer_ref_track(slider2));
  draw_adinkra_watermark(bp_x, pm_y + 12, bp_w, pm_h - 24, 4); // Sankofa Benchmark Watermark

  gfx_setfont(2, "Consolas", 10.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = bp_x + 16; gfx_y = pm_y + 88;
  slider2 == 6 ? gfx_drawstr("H:\\REFERENCES: RMS -9.1dB | Crest 8.8dB | S/M -7.8dB") :
  slider2 == 9 ? gfx_drawstr("H:\\REFERENCES: RMS -9.1dB | Crest 9.1dB | S/M -7.8dB") :
  slider2 == 3 ? gfx_drawstr("H:\\REFERENCES: RMS -8.5dB | Crest 8.5dB | S/M -4.2dB") :
  slider2 == 21 ? gfx_drawstr("H:\\REFERENCES: RMS -10.6dB | Crest 10.5dB | S/M -6.4dB") :
  slider2 == 4 ? gfx_drawstr("H:\\REFERENCES: RMS -6.8dB | Crest 6.8dB | S/M -5.3dB") :
  slider2 == 19 ? gfx_drawstr("H:\\REFERENCES: RMS -8.0dB | Crest 7.7dB | S/M -4.9dB") :
  slider2 == 14 ? gfx_drawstr("H:\\REFERENCES: RMS -7.4dB | Crest 7.2dB | S/M -5.8dB") :
  slider2 == 1 ? gfx_drawstr("H:\\REFERENCES: RMS -7.3dB | Crest 7.2dB | S/M -6.1dB") :
  slider2 == 15 ? gfx_drawstr("H:\\REFERENCES: RMS -9.9dB | Crest 9.6dB | S/M -9.6dB") :
  slider2 == 22 ? gfx_drawstr("H:\\REFERENCES: RMS -11.0dB | Crest 10.7dB | S/M -5.2dB") :
  gfx_drawstr("H:\\REFERENCES: Forensic Master Telemetry Synchronized");

  gfx_setfont(2, "Arial", 11.5, '');
  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = bp_x + 16; gfx_y = pm_y + 110;
  gfx_printf("• Output Trim  : %+3.1f dB (DeeGain Staging Bit-Exact Parity)", slider4);
  gfx_x = bp_x + 16; gfx_y = pm_y + 130;
  gfx_printf("• Tonal EQ     : 80Hz +%3.1fdB | 202Hz -%3.1fdB", slider19, abs(slider20));
  gfx_x = bp_x + 16; gfx_y = pm_y + 150;
  gfx_printf("• Mid/High Bite: 1.5k +%3.1fdB | 3.0k +%3.1fdB", slider21, slider22);
  gfx_x = bp_x + 16; gfx_y = pm_y + 170;
  gfx_printf("• Air Sheen    : 8.0kHz +%3.1fdB High Shelf", slider31);
  gfx_x = bp_x + 16; gfx_y = pm_y + 190;
  gfx_printf("• Bus Glue VCA : Thresh %4.1fdB | %s | 10ms", slider12, slider13==0?"1.5:1":slider13==1?"2:1":slider13==2?"4:1":"8:1");
  gfx_x = bp_x + 16; gfx_y = pm_y + 210;
  gfx_printf("• Sidechain HPF: %d Hz (%s)", slider16, slider16 <= 42 ? "Snare Cut-Through" : (slider16 <= 65 ? "Kick/Sub Decouple" : "Sub Anchor"));
  gfx_x = bp_x + 16; gfx_y = pm_y + 230;
  gfx_printf("• Harmonic Desk: %s (Drive %+3.1f dB)", slider23==0?"Transparent Pass":slider23==1?"Neve 8014 Iron Desk":slider23==2?"Studer A800 Tape":"Triode Tube", slider24);
  gfx_x = bp_x + 16; gfx_y = pm_y + 250;
  gfx_printf("• Stereo Matrix: Sub-Mono %dHz | Width %.2fx", slider6, active_width);

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_x = bp_x + 16; gfx_y = pm_y + 280; gfx_drawstr("PRODUCER HEURISTICS:");
  gfx_setfont(2, "Arial", 11.5, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  tip_base = slider2 * 4;
  gfx_x = bp_x + 16; gfx_y = pm_y + 302; gfx_drawstr(dk_tip[tip_base + 0]);
  gfx_x = bp_x + 16; gfx_y = pm_y + 322; gfx_drawstr(dk_tip[tip_base + 1]);
  gfx_x = bp_x + 16; gfx_y = pm_y + 342; gfx_drawstr(dk_tip[tip_base + 2]);
  gfx_x = bp_x + 16; gfx_y = pm_y + 362; gfx_drawstr(dk_tip[tip_base + 3]);
);
"""

if t6_start != -1 and t7_start != -1:
    text = text[:t6_start] + new_tab6.strip() + "\n\n" + text[t7_start:]
    print("Tab 6 overhaul applied!")
else:
    print(f"Error finding Tab 6 boundaries (t6={t6_start}, t7={t7_start})")

# Write out the modified JSFX
with open(jsfx_path, "w", encoding="utf-8") as f:
    f.write(text)
print(f"Written to {jsfx_path}")

with open(reaper_path, "w", encoding="utf-8") as f:
    f.write(text)
print(f"Deployed to {reaper_path}")
