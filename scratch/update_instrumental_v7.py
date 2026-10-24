# update_instrumental_v7.py
import re

path = r"c:\Dev\DameiSuite\scratch\gen_instrumental_flagship_v6_ai_header.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update window dimensions and header geometry
old_gfx_init = """// Master Title Ribbon
hdr_h = 52;
gfx_r = 0.025; gfx_g = 0.032; gfx_b = 0.042;
gfx_rect(16, 16, gfx_w - 32, hdr_h);
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
gfx_rect(16, 16, gfx_w - 32, hdr_h, 0);"""

new_gfx_init = """// Master Title Ribbon
hdr_h = 46;
gfx_r = 0.025; gfx_g = 0.032; gfx_b = 0.042;
gfx_rect(14, 12, gfx_w - 28, hdr_h);
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
gfx_rect(14, 12, gfx_w - 28, hdr_h, 0);"""

text = text.replace(old_gfx_init, new_gfx_init)

# Update emblem and title coordinates in header
text = text.replace('sig_cy = 16 + hdr_h * 0.5;', 'sig_cy = 12 + hdr_h * 0.5;')
text = text.replace('gfx_x = 64; gfx_y = 16 + floor((hdr_h - 18) * 0.5);', 'gfx_x = 64; gfx_y = 12 + floor((hdr_h - 18) * 0.5);')
text = text.replace('btn_y = 16 + floor((hdr_h - btn_h) * 0.5);', 'btn_y = 12 + floor((hdr_h - btn_h) * 0.5);')

# 2. Update card_y, tab_y, and ws_y
old_card_grid = """card_y = 16 + hdr_h + 6;
card_w = floor((gfx_w - 32 - 18) / 4);
card_h = 60;"""

new_card_grid = """card_y = 12 + hdr_h + 5;
card_w = floor((gfx_w - 28 - 18) / 4);
card_h = 58;"""

text = text.replace(old_card_grid, new_card_grid)
text = text.replace('c1_x = 16;', 'c1_x = 14;')

old_tab_grid = """// Navigation Tabs Ribbon
tab_y = card_y + card_h + 6; tab_h = 34;
num_tabs = 7;
tab_w = floor((gfx_w - 32) / num_tabs);"""

new_tab_grid = """// Navigation Tabs Ribbon
tab_y = card_y + card_h + 5; tab_h = 30;
num_tabs = 7;
tab_w = floor((gfx_w - 28) / num_tabs);"""

text = text.replace(old_tab_grid, new_tab_grid)
text = text.replace('tx = 16 + ti * tab_w;', 'tx = 14 + ti * tab_w;')

old_ws_grid = """ws_x = 16; ws_y = 126; ws_w = gfx_w - 32; ws_h = gfx_h - 142;"""
new_ws_grid = """ws_x = 14; ws_y = tab_y + tab_h + 6; ws_w = gfx_w - 28; ws_h = gfx_h - ws_y - 12;"""

text = text.replace(old_ws_grid, new_ws_grid)

# 3. Update Tab 0 Top Row height so meters and lower cards fit within workspace
old_tab0_row = "top_row_h = 236;"
new_tab0_row = "top_row_h = 216;"
text = text.replace(old_tab0_row, new_tab0_row)

old_mod_y = "mod_y = ws_y + top_row_h + 16;"
new_mod_y = "mod_y = ws_y + top_row_h + 8;"
text = text.replace(old_mod_y, new_mod_y)

# 4. In Tab 6: full-width Forensic Producer Blueprint Card
old_tab6_bottom = """  // Left: AI Mix Assistant Card
  ai_x = ws_x + 8; ai_y = b_grid_y + b_grid_h + 10;
  ai_w = floor((ws_w - 24) * 0.48);
  ai_h = ws_h - (ai_y - ws_y) - 8;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(ai_x, ai_y, ai_w, ai_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(ai_x, ai_y, ai_w, ai_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = ai_x + 14; gfx_y = ai_y + 12;
  gfx_drawstr("LOCAL OLLAMA & HF AI ASSISTANT // COGNITIVE BUS REASONING");

  gfx_setfont(3, "Consolas", 11.5); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.95;
  gfx_x = ai_x + 16; gfx_y = ai_y + 44; gfx_drawstr("• Engine       : damei-cognitive-engineer:latest (DirectML RTX 3060)");
  gfx_x = ai_x + 16; gfx_y = ai_y + 70; gfx_drawstr("• DNA Model    : laion/clap-htsat-fused (Acoustic Cosine Vector)");
  gfx_x = ai_x + 16; gfx_y = ai_y + 96; gfx_drawstr("• Structure    : ccmusic-database/music_structure (Chorus Impact Sync)");
  gfx_x = ai_x + 16; gfx_y = ai_y + 122; gfx_drawstr("• Balance Guard: ACTIVE (Strict ±0.5dB Max Safe Auto-Calibration Lock)");

  btn_w = ai_w - 32; btn_h = 32;
  btn_bx = ai_x + 16; btn_by = ai_y + ai_h - 44;
  btn_hov = (mouse_x >= btn_bx && mouse_x <= btn_bx + btn_w && mouse_y >= btn_by && mouse_y <= btn_by + btn_h);
  gfx_r = btn_hov ? 0.00 : 0.00; gfx_g = btn_hov ? 1.00 : 0.85; gfx_b = 1.00;
  gfx_rect(btn_bx, btn_by, btn_w, btn_h);
  gfx_setfont(1, "Orbitron", 11, 'b'); gfx_r = 0.02; gfx_g = 0.02; gfx_b = 0.04;
  btn_txt = "RUN COGNITIVE AI AUTO-CALIBRATE (±0.5dB SAFE LOCK)";
  gfx_measurestr(btn_txt, bw_t, bh_t);
  gfx_x = btn_bx + floor((btn_w - bw_t) * 0.5); gfx_y = btn_by + floor((btn_h - bh_t) * 0.5);
  gfx_drawstr(btn_txt);
  mouse_clicked && btn_hov ? ( trigger_ai_assist(); );

  // Right: Forensic Reference Blueprint Target Card
  bp_x = ai_x + ai_w + 8; bp_y = ai_y;
  bp_w = ws_w - 16 - ai_w - 8; bp_h = ai_h;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(bp_x, bp_y, bp_w, bp_h);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(bp_x, bp_y, bp_w, bp_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.25;
  gfx_x = bp_x + 14; gfx_y = bp_y + 12;
  gfx_drawstr("FORENSIC PRODUCER BLUEPRINT & REFERENCE TARGET");

  gfx_setfont(3, "Consolas", 11.5);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = bp_x + 16; gfx_y = bp_y + 44;
  ref_name = get_producer_ref_track(slider2);
  gfx_printf("• REF TARGET : %s", ref_name);

  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.95;
  gfx_x = bp_x + 16; gfx_y = bp_y + 70; gfx_printf("• Output Trim: %+.1f dB (DeeGain & Staging)", slider4);
  gfx_x = bp_x + 16; gfx_y = bp_y + 96; gfx_printf("• Tonal Forge: 80Hz %+.1fdB | 202Hz %+.1fdB | 1.5k %+.1fdB", slider19, slider20, slider21);
  gfx_x = bp_x + 16; gfx_y = bp_y + 122; gfx_printf("• Upper Tonal: 3.0k %+.1fdB | 8.0k %+.1fdB (High Shelf)", slider22, slider31);
  gfx_x = bp_x + 16; gfx_y = bp_y + 148; gfx_printf("• Bus Glue   : Thresh %+.1fdB | 4:1 Ratio | %.0fms / 600ms", slider12, slider14);
  gfx_x = bp_x + 16; gfx_y = bp_y + 174; gfx_printf("• Spatial/Sub: Mono Anchor %.0fHz | Stereo Width %.2fx", slider6, slider25);"""

new_tab6_bottom = """  // Full-Width Forensic Producer Blueprint & Cognitive Ecosystem Dock
  bp_x = ws_x + 8; bp_y = b_grid_y + b_grid_h + 8;
  bp_w = ws_w - 16; bp_h = ws_h - (bp_y - ws_y) - 6;
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(bp_x, bp_y, bp_w, bp_h);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(bp_x, bp_y, bp_w, bp_h, 0);

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.25;
  gfx_x = bp_x + 14; gfx_y = bp_y + 10;
  gfx_drawstr("FORENSIC PRODUCER BLUEPRINT // 25-REFERENCE BENCHMARK ECOSYSTEM");

  // Dual Column Layout inside card
  col1_w = floor((bp_w - 36) * 0.52);
  col2_x = bp_x + 18 + col1_w + 10;

  // Left Column: Reference Target & Forensic Staging
  gfx_setfont(3, "Consolas", 11.5);
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = bp_x + 16; gfx_y = bp_y + 36;
  ref_name = get_producer_ref_track(slider2);
  gfx_printf("• ACTIVE TARGET : %s", ref_name);

  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.95;
  gfx_x = bp_x + 16; gfx_y = bp_y + 60; gfx_printf("• Staging Trim  : %+.1f dB (DeeGain Calibrated Staging)", slider4);
  gfx_x = bp_x + 16; gfx_y = bp_y + 84; gfx_printf("• ReEQ Low Forge: 80Hz Low-Shelf %+.1fdB | 90Hz Body Glue +0.25dB", slider19);
  gfx_x = bp_x + 16; gfx_y = bp_y + 108; gfx_printf("• ReEQ Mud Scoop: 202Hz Mud Notch %+.1fdB (Q=1.2) | 1.5k Body %+.1fdB", slider20, slider21);
  gfx_x = bp_x + 16; gfx_y = bp_y + 132; gfx_printf("• ReEQ High Top : 3.0k Pick Bite %+.1fdB | 8.0k Air Sheen %+.1fdB", slider22, slider31);

  // Right Column: Bus Glue & Sub-Bass Architecture
  gfx_x = col2_x; gfx_y = bp_y + 36;
  gfx_r = 0.15; gfx_g = 0.95; gfx_b = 0.45;
  gfx_drawstr("• ECOSYSTEM AI  : DirectML RTX 3060 // laion/clap-htsat Cosine Guard");
  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.95;
  gfx_x = col2_x; gfx_y = bp_y + 60; gfx_printf("• Bus Glue VCA  : Thresh %+.1fdB | Ratio 4:1 | Attack %.0fms / 600ms", slider12, slider14);
  gfx_x = col2_x; gfx_y = bp_y + 84; gfx_printf("• Sub Waveshaper: Liteon 25%% Rational Waveshaper (k=0.223) | Limiter -0.18dBFS");
  gfx_x = col2_x; gfx_y = bp_y + 108; gfx_printf("• Mono Anchor   : %.0fHz Linkwitz-Riley 24dB/oct | Quad Width %.2fx", slider6, slider25);
  gfx_x = col2_x; gfx_y = bp_y + 132; gfx_printf("• Vocal Corridor: Dynamic 2.2kHz Notch Depth %+.1fdB (gmem[1401] Interlock)", -pocket_depth);"""

text = text.replace(old_tab6_bottom, new_tab6_bottom)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

# Also execute generator
exec(compile(text, path, 'exec'))
print("Successfully generated and executed update_instrumental_v7!")
