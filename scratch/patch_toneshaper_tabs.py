import sys, os

ts_path = r"c:\Dev\DameiSuite\effects\Damei_ToneShaper.jsfx"
gf_path = r"c:\Dev\DameiSuite\effects\Damei_GullfossMaster.jsfx"

# 1. PATCH TONYSHAPER
with open(ts_path, 'r', encoding='utf-8') as f:
    ts_code = f.read()

# Add slider8 if not present
if "slider8:" not in ts_code:
    target_slider = "slider7:6<0,24,1{Default Modern Metal Clean"
    pos = ts_code.find(target_slider)
    end_slider7 = ts_code.find("\n", pos)
    slider8_def = "\nslider8:0<0,1,1{Analog Tone & Body Shaper,Mastering Engineer Matrix}>-Suite Tab View"
    ts_code = ts_code[:end_slider7] + slider8_def + ts_code[end_slider7:]

# Add short name and preset notes helper functions before update_circuit
helpers_code = '''
function get_toneshaper_short_name(p_idx) (
  p_idx == 0  ? "0: DEFAULT" :
  p_idx == 1  ? "1: PRENC" :
  p_idx == 2  ? "2: SEIGEL" :
  p_idx == 3  ? "3: DOLESE" :
  p_idx == 4  ? "4: ODEHOLM" :
  p_idx == 5  ? "5: BERRY" :
  p_idx == 6  ? "6: SPLITCHAIN" :
  p_idx == 7  ? "7: JENSEN" :
  p_idx == 8  ? "8: SCHMIDT" :
  p_idx == 9  ? "9: KALAJIAN" :
  p_idx == 10 ? "10: TOWNSEND" :
  p_idx == 11 ? "11: MERRILL" :
  p_idx == 12 ? "12: DONALDSON" :
  p_idx == 13 ? "13: HAMIDOVIC" :
  p_idx == 14 ? "14: PUTNEY" :
  p_idx == 15 ? "15: LEVER" :
  p_idx == 16 ? "16: BASSAL" :
  p_idx == 17 ? "17: UDD" :
  p_idx == 18 ? "18: BRAUNSTEIN" :
  p_idx == 19 ? "19: CERVINI" :
  p_idx == 20 ? "20: BOGREN" :
  p_idx == 21 ? "21: NOLLY" :
  p_idx == 22 ? "22: ACLE" :
  p_idx == 23 ? "23: CICHOCKI" :
  "24: RENNER";
);

function get_toneshaper_preset_notes(p_idx) (
  p_idx == 0  ? "Pristine transparent passive balance. 0dB tone tilt, 0dB body weight. Linear phase clarity." :
  p_idx == 1  ? "Aggressive modern metal bite: +2.2dB tone tilt, -1.0dB body clean scoop. Transformer warmth." :
  p_idx == 2  ? "Heavy industrial grit: +1.4dB tone, +1.8dB low-mid body thickness. Transformer glue." :
  p_idx == 3  ? "Konkrete modern polish: +2.4dB tone sheen, +0.6dB punch body. Pure transparent circuit." :
  p_idx == 4  ? "Extreme thall clarity: +1.8dB tone sheen, -1.4dB mud clamp. Punchy passive curve." :
  p_idx == 5  ? "Fader mastering UK alternative: +1.5dB tone air, +1.2dB lush body bloom." :
  p_idx == 6  ? "Split Chain signature: +1.6dB 10k air sheen, +1.0dB 260Hz weight, subtle transformer glue." :
  p_idx == 7  ? "Sterling Sound arena gloss: +2.6dB high sheen, +0.8dB low-end punch. High headroom." :
  p_idx == 8  ? "24-96 post-hardcore raw punch: +1.2dB tone, +2.0dB midrange body thrust." :
  p_idx == 9  ? "Rogue Planet upfront punch: +2.0dB presence sheen, -0.8dB low-mid scoop." :
  p_idx == 10 ? "Townsend warm analog shoegaze: +0.8dB high air, +2.2dB warm body bloom." :
  p_idx == 11 ? "City of Souls audiophile polish: +1.8dB silk sheen, +0.5dB transparent weight." :
  p_idx == 12 ? "Hyper-modern metal balance: +2.5dB high sheen, -1.2dB clean pocket scoop." :
  p_idx == 13 ? "Systematic Mastering Guide benchmark: +1.0dB subtle sheen, +0.0dB flat body. Reference flat." :
  p_idx == 14 ? "Putney signature slam: +1.6dB high bite, +1.5dB low-mid density. Transformer on." :
  p_idx == 15 ? "Loathe / Sleep Token atmospheric depth: +1.2dB silk air, +2.0dB chest warmth." :
  p_idx == 16 ? "Thornhill modern alternative: +1.8dB presence, +1.2dB tape weight." :
  p_idx == 17 ? "Architects massive UK arena: +2.2dB air sheen, +1.0dB sub-low weight." :
  p_idx == 18 ? "Spiritbox modern pop-metal: +2.4dB pristine sheen, -0.6dB vocal pocket scoop." :
  p_idx == 19 ? "Bad Omens radio sheen: +2.6dB radio top, -1.0dB surgical mud scoop." :
  p_idx == 20 ? "Fascination Street Nordic metal: +1.5dB presence, +1.8dB low-mid body thrust." :
  p_idx == 21 ? "GGD / Nolly clean djent: +2.0dB tone sheen, -1.5dB surgical 280Hz scoop." :
  p_idx == 22 ? "TesseracT progressive transparency: +1.6dB high air, +0.4dB dynamic low end." :
  p_idx == 23 ? "Timber Studios grungegaze fuzz bloom: +2.8dB high air sheen, +1.2dB warm body bloom. Transformer on." :
  "Uberlarm hyper-modern metalcore: +2.4dB pick attack bite, -1.2dB mud scoop, laser center punch.";
);
'''

if "get_toneshaper_short_name" not in ts_code:
    target_pos = ts_code.find("function update_circuit()")
    ts_code = ts_code[:target_pos] + helpers_code + "\n" + ts_code[target_pos:]

# Update ToneShaper @gfx
# Replace @gfx 760 380 with @gfx 780 430
ts_code = ts_code.replace("@gfx 760 380", "@gfx 780 430")

# In @gfx, right after Tandem Sync button (line ~430), add tab bar and conditional branches
tab_bar_insertion = '''
// Tab Bar Navigation (Overview & Active Shaper vs Mastering Engineer Matrix)
tab_y = 52;
tab_h = 24;
tab_w = floor((disp_w - 24) / 2);
ti = 0;
loop(2,
  tx = 12 + ti * tab_w;
  sel = (slider8 == ti);
  sel ? (
    gfx_r = 0.09; gfx_g = 0.14; gfx_b = 0.20;
  ) : (
    gfx_r = 0.035; gfx_g = 0.045; gfx_b = 0.060;
  );
  gfx_rect(tx, tab_y, tab_w - 4, tab_h);
  sel ? (
    gfx_r = 0.00; gfx_g = 0.95; gfx_b = 0.65;
    gfx_rect(tx, tab_y + tab_h - 2, tab_w - 4, 2);
    gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  ) : (
    gfx_r = 0.55; gfx_g = 0.65; gfx_b = 0.75;
  );
  gfx_setfont(2);
  t_lbl = (ti == 0 ? "ANALOG TONE & BODY SHAPER" : "MASTERING ENGINEER MATRIX");
  gfx_measurestr(t_lbl, tlw, tlh);
  gfx_x = floor(tx + (tab_w - 4 - tlw) * 0.5); gfx_y = tab_y + 5;
  gfx_drawstr(t_lbl);
  (mouse_cap & 1) && !prev_mouse_cap && (mouse_x >= tx && mouse_x <= tx + tab_w - 4 && mouse_y >= tab_y && mouse_y <= tab_y + tab_h) ? (
    slider8 = ti;
    slider_automate(128);
  );
  ti += 1;
);

slider8 == 0 ? (
'''

# Find insertion point in ToneShaper GFX
pos_graph_comment = ts_code.find("// Graph Display Area")
if pos_graph_comment != -1 and "tab_y = 52;" not in ts_code:
    ts_code = ts_code[:pos_graph_comment] + tab_bar_insertion + "\n" + ts_code[pos_graph_comment:]

# At the end of slider8 == 0 (before prev_mouse_cap = mouse_cap;), close tab 0 and add tab 1
tab1_toneshaper = '''
) : (
  // =============================================================================
  // TAB 1: MASTERING ENGINEER SIGNATURE MATRIX (25 COMMERCIAL BENCHMARKS)
  // =============================================================================
  mat_y = 84;
  gfx_r = 0.95; gfx_g = 0.85; gfx_b = 0.40; gfx_setfont(1, "Orbitron", 14, 'b');
  gfx_x = 14; gfx_y = mat_y;
  gfx_drawstr("MASTERING ENGINEER SIGNATURE MATRIX // 25 REFERENCE BENCHMARKS");

  // 25 Pills arranged in 4 rows (7 per row for rows 0..2, 4 in row 3)
  pi = 0;
  pill_w = floor((disp_w - 32 - 36) / 7);
  pill_h = 30;
  loop(25,
    p_row = floor(pi / 7); p_col = pi % 7;
    px = 12 + p_col * (pill_w + 6);
    py = mat_y + 26 + p_row * (pill_h + 6);
    is_sel = (slider7 == pi);
    p_hov = (mouse_x >= px && mouse_x <= px + pill_w && mouse_y >= py && mouse_y <= py + pill_h);

    gfx_r = is_sel ? 0.16 : (p_hov ? 0.08 : 0.035);
    gfx_g = is_sel ? 0.26 : (p_hov ? 0.12 : 0.045);
    gfx_b = is_sel ? 0.36 : (p_hov ? 0.18 : 0.060);
    gfx_rect(px, py, pill_w, pill_h);

    gfx_r = is_sel ? 0.00 : (p_hov ? 0.40 : 0.18);
    gfx_g = is_sel ? 0.95 : (p_hov ? 0.50 : 0.24);
    gfx_b = is_sel ? 0.65 : (p_hov ? 0.65 : 0.32);
    gfx_rect(px, py, pill_w, pill_h, 0);

    gfx_setfont(3);
    is_sel ? (gfx_r = 0.00; gfx_g = 1.00; gfx_b = 0.70;) : (gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;);
    p_sname = get_toneshaper_short_name(pi);
    gfx_measurestr(p_sname, psw, psh);
    gfx_x = floor(px + (pill_w - psw) * 0.5); gfx_y = py + 7;
    gfx_drawstr(p_sname);

    (mouse_cap & 1) && !prev_mouse_cap && p_hov ? (
      slider7 = pi;
      slider6 = 0; // Manual select clears tandem lock
      prev_ts_preset = slider7;
      apply_toneshaper_master_preset(slider7);
      slider_automate(64 | 32);
    );
    pi += 1;
  );

  // Active Engineer Profile Plaque
  plaque_y = mat_y + 174;
  plaque_w = disp_w - 24;
  plaque_h = disp_h - plaque_y - 12;

  gfx_r = 0.025; gfx_g = 0.032; gfx_b = 0.044;
  gfx_rect(12, plaque_y, plaque_w, plaque_h);
  gfx_r = 0.14; gfx_g = 0.22; gfx_b = 0.32;
  gfx_rect(12, plaque_y, plaque_w, plaque_h, 0);

  gfx_setfont(1, "Orbitron", 12, 'b');
  gfx_r = 0.00; gfx_g = 0.95; gfx_b = 0.65;
  gfx_x = 24; gfx_y = plaque_y + 10;
  gfx_printf("ACTIVE SIGNATURE: %02d - %s", slider7, get_toneshaper_engineer_name(slider7));

  gfx_setfont(3);
  gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.98;
  gfx_x = 24; gfx_y = plaque_y + 32;
  gfx_printf("SETTINGS: Tone: %+4.1fdB (High Sheen) | Body: %+4.1fdB (Low-Mid Weight) | Trim: %+4.1fdB | Circuit: %s",
    slider2, slider3, slider4, slider5 ? "Transformer Glue (ON)" : "Pure Transparent (0 THD)");

  gfx_setfont(4);
  gfx_r = 0.55; gfx_g = 0.70; gfx_b = 0.85;
  gfx_x = 24; gfx_y = plaque_y + 54;
  gfx_drawstr(get_toneshaper_preset_notes(slider7));
);
'''

# Adjust gp_y in tab 0 so it starts below tab bar
ts_code = ts_code.replace("gp_x = 8; gp_y = 54; gp_w = disp_w - 16; gp_h = 160;", "gp_x = 8; gp_y = 80; gp_w = disp_w - 16; gp_h = 155;")

# Find where to close tab 0
pos_prev_mouse = ts_code.rfind("prev_mouse_cap = mouse_cap;")
if pos_prev_mouse != -1 and "TAB 1: MASTERING ENGINEER" not in ts_code:
    ts_code = ts_code[:pos_prev_mouse] + tab1_toneshaper + "\n" + ts_code[pos_prev_mouse:]

with open(ts_path, 'w', encoding='utf-8') as f:
    f.write(ts_code)

print("ToneShaper patched successfully.")
