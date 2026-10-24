# patch_and_rebuild_suites.py
import re, os, subprocess

# 1. Update gen_instrumental_flagship.py
with open(r"c:\Dev\DameiSuite\scratch\gen_instrumental_flagship.py", "r", encoding="utf-8") as f:
    inst_code = f.read()

# Mouse handling replacement at start of @gfx
mouse_init_block = """@gfx 1080 700
// =============================================================================
// LUXURY SIFAM CONSOLE SURFACE ARCHITECTURE
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

// Background Obsidian Titanium Enclosure"""

inst_code = re.sub(
    r"@gfx 1080 700\s*// =+\s*// LUXURY SIFAM CONSOLE SURFACE ARCHITECTURE\s*// =+\s*// Background Obsidian Titanium Enclosure",
    mouse_init_block,
    inst_code
)

# Header block replacement in instrumental
old_inst_hdr_pattern = r"// Master Title Ribbon[\s\S]*?// Navigation Tabs Ribbon"
new_inst_hdr = """// Master Title Ribbon
hdr_h = 52;
gfx_r = 0.025; gfx_g = 0.032; gfx_b = 0.042;
gfx_rect(16, 16, gfx_w - 32, hdr_h);
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
gfx_rect(16, 16, gfx_w - 32, hdr_h, 0);

// Funtunfunefu Emblem
gfx_r = 0.95; gfx_g = 0.75; gfx_b = 0.20;
gfx_circle(36, 16 + hdr_h * 0.5, 12, 0);
gfx_circle(36, 16 + hdr_h * 0.5, 7, 0);
gfx_circle(36, 16 + hdr_h * 0.5, 3, 1);

gfx_setfont(1, "Orbitron", 14, 'b');
gfx_r = 0.98; gfx_g = 0.88; gfx_b = 0.70;
title_str = "DAMEI // INST BUS";
gfx_measurestr(title_str, tw, th);
gfx_x = 58; gfx_y = 16 + floor((hdr_h - th) * 0.5);
gfx_drawstr(title_str);

// Producer Benchmark Dropdown Selector Header
btn_y = 24; btn_h = 36;
p_bx = 58 + tw + 34;
p_bw = 240;

// Arrow buttons: dark slate background, gold border, high-contrast text
arr_hov_l = (mouse_x >= p_bx - 26 && mouse_x <= p_bx - 2 && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);
gfx_r = arr_hov_l ? 0.09 : 0.025; gfx_g = arr_hov_l ? 0.12 : 0.032; gfx_b = arr_hov_l ? 0.16 : 0.044;
gfx_rect(p_bx - 26, btn_y, 24, btn_h);
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
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
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
gfx_rect(p_bx, btn_y, p_bw, btn_h, 0);

gfx_setfont(1, "Orbitron", 12.5, 'b');
gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
p_str = get_producer_short_name(slider2);
gfx_measurestr(p_str, pw, ph);
gfx_x = p_bx + floor((p_bw - pw) * 0.5); gfx_y = btn_y + floor((btn_h - ph) * 0.5);
gfx_drawstr(p_str);

// Right Arrow
arr_hov_r = (mouse_x >= p_bx + p_bw + 2 && mouse_x <= p_bx + p_bw + 26 && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);
gfx_r = arr_hov_r ? 0.09 : 0.025; gfx_g = arr_hov_r ? 0.12 : 0.032; gfx_b = arr_hov_r ? 0.16 : 0.044;
gfx_rect(p_bx + p_bw + 2, btn_y, 24, btn_h);
gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
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
slider27 ? (gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;) : (gfx_r = 0.50; gfx_g = 0.50; gfx_b = 0.50;);
gfx_rect(b5_x, btn_y, b5_w, btn_h, 0);
gfx_setfont(2, "Orbitron", 10.5, 'b');
eng_str = slider27 ? "ENGAGED" : "BYPASS";
gfx_measurestr(eng_str, ew, eh);
gfx_x = b5_x + floor((b5_w - ew) * 0.5); gfx_y = btn_y + floor((btn_h - eh) * 0.5);
gfx_drawstr(eng_str);
mouse_clicked && b5_hov ? (
  slider27 = !slider27; slider_automate();
);

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
mode_str = "MODE: STEREO";
gfx_measurestr(mode_str, mw, mh);
gfx_x = b3_x + floor((b3_w - mw) * 0.5); gfx_y = btn_y + floor((btn_h - mh) * 0.5);
gfx_drawstr(mode_str);

// 2. Vocal Relay Link
b2_w = 94; b2_x = b3_x - 6 - b2_w;
vox_rms = gmem[1452];
gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.022; gfx_rect(b2_x, btn_y, b2_w, btn_h);
gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_rect(b2_x, btn_y, b2_w, btn_h, 0);
v_str = sprintf(#, "VOX: %4.1fdB", vox_rms);
gfx_measurestr(v_str, vw, vh);
gfx_x = b2_x + floor((b2_w - vw) * 0.5); gfx_y = btn_y + floor((btn_h - vh) * 0.5);
gfx_drawstr(v_str);

// 1. Chorus Sync
b1_w = 90; b1_x = b2_x - 6 - b1_w;
gfx_r = 0.012; gfx_g = 0.016; gfx_b = 0.022; gfx_rect(b1_x, btn_y, b1_w, btn_h);
gfx_r = 0.00; gfx_g = 0.85; gfx_b = 0.45; gfx_rect(b1_x, btn_y, b1_w, btn_h, 0);
gfx_setfont(2, "Consolas", 10.5, 'b');
ch_str = "⚡ CHORUS";
gfx_measurestr(ch_str, chw, chh);
gfx_x = b1_x + floor((b1_w - chw) * 0.5); gfx_y = btn_y + floor((btn_h - chh) * 0.5);
gfx_drawstr(ch_str);

// Navigation Tabs Ribbon"""

inst_code = re.sub(old_inst_hdr_pattern, new_inst_hdr, inst_code)

# Add prev_mouse_down = mouse_down at end of @gfx in instrumental
if "prev_mouse_down = mouse_down;" not in inst_code:
    inst_code = re.sub(
        r"(\s*gfx_printf\(\"• Spatial / Sub   : Mono Anchor %dHz \| Stereo Width %4.2fx\", slider6, slider25\);\s*\);\s*)(\"\"\"\))",
        r"\1  prev_mouse_down = mouse_down;\n);\n\2",
        inst_code
    )

with open(r"c:\Dev\DameiSuite\scratch\gen_instrumental_flagship.py", "w", encoding="utf-8") as f:
    f.write(inst_code)


# 2. Update gen_vocal_flagship.py
with open(r"c:\Dev\DameiSuite\scratch\gen_vocal_flagship.py", "r", encoding="utf-8") as f:
    vox_code = f.read()

vox_mouse_init_block = """@gfx 1080 700
// =============================================================================
// LUXURY SIFAM CONSOLE SURFACE ARCHITECTURE
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

// Background Obsidian Titanium Enclosure"""

vox_code = re.sub(
    r"@gfx 1080 700\s*// =+\s*// LUXURY SIFAM CONSOLE SURFACE ARCHITECTURE\s*// =+\s*// Background Obsidian Titanium Enclosure",
    vox_mouse_init_block,
    vox_code
)

old_vox_hdr_pattern = r"// Master Title Ribbon[\s\S]*?// Navigation Tabs Ribbon"
new_vox_hdr = """// Master Title Ribbon
hdr_h = 52;
gfx_r = 0.024; gfx_g = 0.026; gfx_b = 0.038;
gfx_rect(16, 16, gfx_w - 32, hdr_h);
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
gfx_rect(16, 16, gfx_w - 32, hdr_h, 0);

// Duafe Comb Royal Emblem
gfx_r = 0.88; gfx_g = 0.25; gfx_b = 0.65;
gfx_circle(36, 16 + hdr_h * 0.5, 12, 0);
gfx_circle(36, 16 + hdr_h * 0.5, 7, 0);
gfx_circle(36, 16 + hdr_h * 0.5, 3, 1);

gfx_setfont(1, "Orbitron", 14, 'b');
gfx_r = 0.98; gfx_g = 0.88; gfx_b = 0.95;
title_str = "DAMEI // VOCAL BUS";
gfx_measurestr(title_str, tw, th);
gfx_x = 58; gfx_y = 16 + floor((hdr_h - th) * 0.5);
gfx_drawstr(title_str);

// Producer Benchmark Dropdown Selector Header
btn_y = 24; btn_h = 36;
p_bx = 58 + tw + 34;
p_bw = 240;

// Arrow buttons: dark slate background, magenta border, high-contrast text
arr_hov_l = (mouse_x >= p_bx - 26 && mouse_x <= p_bx - 2 && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);
gfx_r = arr_hov_l ? 0.09 : 0.025; gfx_g = arr_hov_l ? 0.12 : 0.032; gfx_b = arr_hov_l ? 0.16 : 0.044;
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
gfx_r = arr_hov_r ? 0.09 : 0.025; gfx_g = arr_hov_r ? 0.12 : 0.032; gfx_b = arr_hov_r ? 0.16 : 0.044;
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

// Navigation Tabs Ribbon"""

vox_code = re.sub(old_vox_hdr_pattern, new_vox_hdr, vox_code)

if "prev_mouse_down = mouse_down;" not in vox_code:
    vox_code = re.sub(
        r"(\s*gfx_printf\(\"• Spatial Dimension: %4.2f x Width \(Lead Center Lock\)\", slider21\);\s*\);\s*)(\"\"\"\))",
        r"\1  prev_mouse_down = mouse_down;\n);\n\2",
        vox_code
    )

with open(r"c:\Dev\DameiSuite\scratch\gen_vocal_flagship.py", "w", encoding="utf-8") as f:
    f.write(vox_code)

print("Both generator scripts patched successfully.")
