import sys, os

gf_path = r"c:\Dev\DameiSuite\effects\Damei_GullfossMaster.jsfx"

with open(gf_path, 'r', encoding='utf-8') as f:
    gf_code = f.read()

# 1. Add slider13 if not present
if "slider13:" not in gf_code:
    target_slider = "slider12:6<0,24,1{Default Modern Metal Clean"
    pos = gf_code.find(target_slider)
    end_slider12 = gf_code.find("\n", pos)
    slider13_def = "\nslider13:0<0,1,1{Auditory De-Masking Engine,Mastering Engineer Matrix}>-Suite Tab View"
    gf_code = gf_code[:end_slider12] + slider13_def + gf_code[end_slider12:]

# 2. Add helper functions
helpers_code = '''
function get_gullfoss_short_name(p_idx) (
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

function get_gullfoss_preset_notes(p_idx) (
  p_idx == 0  ? "Pristine auditory neutrality. 20% recover, 20% tame, flat bias. Transparent dynamic clarity." :
  p_idx == 1  ? "Aggressive Prenc bite: 32% recover, 38% tame, -5% bias, +16% brightness sheen. Fast response." :
  p_idx == 2  ? "Dense industrial weight: 26% recover, 35% tame, -8% bias, +14% sub weight. Controlled punch." :
  p_idx == 3  ? "Glossy modern polish: 34% recover, 28% tame, +6% recover bias, +14% brightness air sheen." :
  p_idx == 4  ? "Buster Odeholm extreme thall clamp: 22% recover, 42% heavy resonance tame, -12% bias, 75% speed." :
  p_idx == 5  ? "Lush ambient shoegaze unmasking: 25% recover, 22% tame, +4% bias, +15% brightness shimmer." :
  p_idx == 6  ? "Split Chain master: 28% recover, 32% tame, +8% bias, +12% bright, +10% boost. Reference lock." :
  p_idx == 7  ? "Sterling Sound arena rock: 30% recover, 26% tame, +5% bias, +15% brightness, 80Hz cut." :
  p_idx == 8  ? "24-96 post-hardcore raw punch: 30% recover, 34% tame, +10% brightness, +12% low weight." :
  p_idx == 9  ? "Rogue Planet upfront punch: 35% recover, 30% tame, +8% bias, +18% brightness, 65% speed." :
  p_idx == 10 ? "Townsend warm analog depth: 24% recover, 20% gentle tame, +10% low weight, 65Hz cut." :
  p_idx == 11 ? "City of Souls audiophile clarity: 26% recover, 24% tame, +12% brightness, 50% speed." :
  p_idx == 12 ? "Hyper-modern metalcore: 36% recover, 36% tame, +16% brightness sheen, 70% fast reaction." :
  p_idx == 13 ? "Systematic Mastering Guide benchmark: 22% recover, 22% tame, 0% bias, linear reference." :
  p_idx == 14 ? "Putney signature aggression: 28% recover, 40% harshness tame, -10% bias, +8% brightness." :
  p_idx == 15 ? "Loathe / Sleep Token atmospheric depth: 32% recover, 24% tame, +10% bias, +16% low boost." :
  p_idx == 16 ? "Thornhill modern alternative: 28% recover, 30% tame, +14% brightness, +8% low boost." :
  p_idx == 17 ? "Architects massive UK arena: 30% recover, 35% tame, +15% brightness, +10% low weight." :
  p_idx == 18 ? "Spiritbox modern pop-metal: 34% recover, 28% tame, +18% pristine top-end air, 60% speed." :
  p_idx == 19 ? "Bad Omens radio polish: 32% recover, 32% tame, +16% brightness, +10% sub boost." :
  p_idx == 20 ? "Fascination Street Nordic metal: 25% recover, 38% resonance tame, -8% bias, +12% low weight." :
  p_idx == 21 ? "Nolly clean djent: 30% recover, 35% tame, -5% bias, +14% sheen, 85Hz HPF cut." :
  p_idx == 22 ? "TesseracT progressive transparency: 28% recover, 26% tame, +12% brightness, 70Hz low cut." :
  p_idx == 23 ? "Timber Studios grungegaze fuzz bloom: 36% recover, 28% tame, +10% bias, +18% high sheen." :
  "Uberlarm hyper-modern metalcore: 35% recover, 34% tame, +16% brightness, +12% kick punch, 90Hz mono anchor.";
);
'''

if "get_gullfoss_short_name" not in gf_code:
    target_pos = gf_code.find("function apply_gullfoss_master_preset")
    gf_code = gf_code[:target_pos] + helpers_code + "\n" + gf_code[target_pos:]

# Update Gullfoss @gfx size
gf_code = gf_code.replace("@gfx 820 440", "@gfx 840 470")

# Tab bar insertion below header
tab_bar_insertion = '''
// Tab Bar Navigation (Auditory Engine vs Mastering Engineer Matrix)
tab_y = hdr_y + hdr_h + 6;
tab_h = 24;
tab_w = floor((disp_w - 24) / 2);
ti = 0;
loop(2,
  tx = disp_x + 12 + ti * tab_w;
  sel = (slider13 == ti);
  sel ? (
    gfx_r = 0.09; gfx_g = 0.14; gfx_b = 0.20;
  ) : (
    gfx_r = 0.035; gfx_g = 0.045; gfx_b = 0.060;
  );
  gfx_rect(tx, tab_y, tab_w - 4, tab_h);
  sel ? (
    gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
    gfx_rect(tx, tab_y + tab_h - 2, tab_w - 4, 2);
    gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  ) : (
    gfx_r = 0.55; gfx_g = 0.65; gfx_b = 0.75;
  );
  gfx_setfont(2);
  t_lbl = (ti == 0 ? "AUDITORY DE-MASKING ENGINE" : "MASTERING ENGINEER MATRIX");
  gfx_measurestr(t_lbl, tlw, tlh);
  gfx_x = floor(tx + (tab_w - 4 - tlw) * 0.5); gfx_y = tab_y + 5;
  gfx_drawstr(t_lbl);
  (mouse_cap & 1) && !prev_mouse_cap && (mouse_x >= tx && mouse_x <= tx + tab_w - 4 && mouse_y >= tab_y && mouse_y <= tab_y + tab_h) ? (
    slider13 = ti;
    slider_automate(4096);
  );
  ti += 1;
);

slider13 == 0 ? (
'''

# Find insertion point before Graph Display
pos_gp_comment = gf_code.find("// 2. CENTRAL GULLFOSS AUDITORY EQ GRAPH DISPLAY")
if pos_gp_comment != -1 and "tab_y = hdr_y + hdr_h + 6;" not in gf_code:
    gf_code = gf_code[:pos_gp_comment] + tab_bar_insertion + "\n" + gf_code[pos_gp_comment:]

# Update gp_y and gp_h so it starts below tab bar
gf_code = gf_code.replace("gp_y = hdr_y + hdr_h + 8;\ngp_w = disp_w - 16;\ngp_h = 200;", "gp_y = tab_y + tab_h + 6;\ngp_w = disp_w - 16;\ngp_h = 180;")

# Tab 1 for GullfossMaster
tab1_gullfoss = '''
) : (
  // =============================================================================
  // TAB 1: MASTERING ENGINEER SIGNATURE MATRIX (25 COMMERCIAL BENCHMARKS)
  // =============================================================================
  mat_y = tab_y + tab_h + 8;
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; gfx_setfont(1, "Orbitron", 14, 'b');
  gfx_x = disp_x + 14; gfx_y = mat_y;
  gfx_drawstr("MASTERING ENGINEER SIGNATURE MATRIX // 25 REFERENCE BENCHMARKS");

  // 25 Pills arranged in 4 rows (7 per row for rows 0..2, 4 in row 3)
  pi = 0;
  pill_w = floor((disp_w - 32 - 36) / 7);
  pill_h = 30;
  loop(25,
    p_row = floor(pi / 7); p_col = pi % 7;
    px = disp_x + 12 + p_col * (pill_w + 6);
    py = mat_y + 26 + p_row * (pill_h + 6);
    is_sel = (slider12 == pi);
    p_hov = (mouse_x >= px && mouse_x <= px + pill_w && mouse_y >= py && mouse_y <= py + pill_h);

    gfx_r = is_sel ? 0.16 : (p_hov ? 0.08 : 0.035);
    gfx_g = is_sel ? 0.26 : (p_hov ? 0.12 : 0.045);
    gfx_b = is_sel ? 0.36 : (p_hov ? 0.18 : 0.060);
    gfx_rect(px, py, pill_w, pill_h);

    gfx_r = is_sel ? 0.00 : (p_hov ? 0.40 : 0.18);
    gfx_g = is_sel ? 0.85 : (p_hov ? 0.50 : 0.24);
    gfx_b = is_sel ? 1.00 : (p_hov ? 0.65 : 0.32);
    gfx_rect(px, py, pill_w, pill_h, 0);

    gfx_setfont(3);
    is_sel ? (gfx_r = 0.00; gfx_g = 0.95; gfx_b = 1.00;) : (gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;);
    p_sname = get_gullfoss_short_name(pi);
    gfx_measurestr(p_sname, psw, psh);
    gfx_x = floor(px + (pill_w - psw) * 0.5); gfx_y = py + 7;
    gfx_drawstr(p_sname);

    (mouse_cap & 1) && !prev_mouse_cap && p_hov ? (
      slider12 = pi;
      slider10 = 0; // Manual select clears tandem lock
      apply_gullfoss_master_preset(slider12);
      slider_automate(2048 | 512);
    );
    pi += 1;
  );

  // Active Engineer Profile Plaque
  plaque_y = mat_y + 174;
  plaque_w = disp_w - 24;
  plaque_h = disp_h - plaque_y - 12;

  gfx_r = 0.025; gfx_g = 0.032; gfx_b = 0.044;
  gfx_rect(disp_x + 12, plaque_y, plaque_w, plaque_h);
  gfx_r = 0.14; gfx_g = 0.22; gfx_b = 0.32;
  gfx_rect(disp_x + 12, plaque_y, plaque_w, plaque_h, 0);

  gfx_setfont(1, "Orbitron", 12, 'b');
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = disp_x + 24; gfx_y = plaque_y + 10;
  gfx_printf("ACTIVE SIGNATURE: %02d - %s", slider12, get_engineer_name(slider12));

  gfx_setfont(3);
  gfx_r = 0.80; gfx_g = 0.88; gfx_b = 0.98;
  gfx_x = disp_x + 24; gfx_y = plaque_y + 32;
  gfx_printf("RECOVER: %d%% | TAME: %d%% | BIAS: %+d%% | BRIGHT: %+d%% | BOOST: %d%% | SPEED: %d%% | LIMITS: %dHz - %dkHz",
    eff_recover, eff_tame, eff_bias, eff_bright, eff_boost, eff_speed, eff_low_limit, eff_high_limit/1000);

  gfx_setfont(4);
  gfx_r = 0.55; gfx_g = 0.70; gfx_b = 0.85;
  gfx_x = disp_x + 24; gfx_y = plaque_y + 54;
  gfx_drawstr(get_gullfoss_preset_notes(slider12));
);
'''

# Find end of file where prev_mouse_cap = mouse_cap is located
pos_prev_mouse = gf_code.rfind("prev_mouse_cap = mouse_cap;")
if pos_prev_mouse != -1 and "TAB 1: MASTERING ENGINEER" not in gf_code:
    gf_code = gf_code[:pos_prev_mouse] + tab1_gullfoss + "\n" + gf_code[pos_prev_mouse:]

with open(gf_path, 'w', encoding='utf-8') as f:
    f.write(gf_code)

print("GullfossMaster patched successfully.")
