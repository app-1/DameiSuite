# format_all_suites_mir.py
import os, sys, re

appdata = os.environ.get("APPDATA")
reaper_effects = os.path.join(appdata, "REAPER", "Effects", "Damei")

suites = {
    "drums": r"c:\Dev\DameiAPI\reaper_scripts\Damei_DrumSuite.jsfx",
    "bass": r"c:\Dev\DameiAPI\reaper_scripts\Damei_BassSuite.jsfx",
    "guitar": r"c:\Dev\DameiAPI\reaper_scripts\Damei_GuitarSuite.jsfx",
    "vocal": r"c:\Dev\DameiAPI\reaper_scripts\Damei_VocalSuite.jsfx",
    "oracle": r"c:\Dev\DameiAPI\reaper_scripts\Damei_AssessmentMatrix.jsfx"
}

# 1. Update DrumSuite Card 2 with MIR Sidecar badge
with open(suites["drums"], "r", encoding="utf-8") as f:
    d_code = f.read()

old_d_link = """gfx_setfont(1, "Consolas", 11, 'b');
gmem[800] > -80.0 ? (
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_measurestr("LINK: ONLINE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("LINK: ONLINE");
) : (
  gfx_r = 0.70; gfx_g = 0.75; gfx_b = 0.80;
  gfx_measurestr("STANDALONE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("STANDALONE");
);"""

new_d_link = """gfx_setfont(1, "Consolas", 10.5, 'b');
gmem[1090] == 3 ? (
  gfx_r = 0.15; gfx_g = 0.95; gfx_b = 0.45;
  mir_tag = "MIR DNA: LINKED";
  gfx_measurestr(mir_tag, lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr(mir_tag);
) : gmem[800] > -80.0 ? (
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_measurestr("LINK: ONLINE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("LINK: ONLINE");
) : (
  gfx_r = 0.70; gfx_g = 0.75; gfx_b = 0.80;
  gfx_measurestr("STANDALONE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("STANDALONE");
);"""

if old_d_link in d_code:
    d_code = d_code.replace(old_d_link, new_d_link, 1)
    with open(suites["drums"], "w", encoding="utf-8") as f:
        f.write(d_code)
    print("Drums Suite MIR badge formatted!")

# 2. Update BassSuite Card 2 with MIR Sidecar badge
with open(suites["bass"], "r", encoding="utf-8") as f:
    b_code = f.read()

old_b_link = """gfx_setfont(1, "Consolas", 11, 'b');
gmem[820] == 1 ? (
  gfx_r = 0.00; gfx_g = 0.92; gfx_b = 0.85;
  gfx_measurestr("KICK: LINKED", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6; gfx_drawstr("KICK: LINKED");
) : (
  gfx_r = 0.70; gfx_g = 0.75; gfx_b = 0.80;
  gfx_measurestr("STANDALONE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6; gfx_drawstr("STANDALONE");
);"""

new_b_link = """gfx_setfont(1, "Consolas", 10.5, 'b');
gmem[1090] == 3 ? (
  gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50;
  mir_b_tag = "MIR DNA: LINKED";
  gfx_measurestr(mir_b_tag, lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6; gfx_drawstr(mir_b_tag);
) : gmem[820] == 1 ? (
  gfx_r = 0.00; gfx_g = 0.92; gfx_b = 0.85;
  gfx_measurestr("KICK: LINKED", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6; gfx_drawstr("KICK: LINKED");
) : (
  gfx_r = 0.70; gfx_g = 0.75; gfx_b = 0.80;
  gfx_measurestr("STANDALONE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6; gfx_drawstr("STANDALONE");
);"""

if old_b_link in b_code:
    b_code = b_code.replace(old_b_link, new_b_link, 1)
    with open(suites["bass"], "w", encoding="utf-8") as f:
        f.write(b_code)
    print("Bass Suite MIR badge formatted!")

# 3. Update GuitarSuite Card 2 with MIR Sidecar badge
with open(suites["guitar"], "r", encoding="utf-8") as f:
    g_code = f.read()

old_g_link = """gfx_setfont(1, "Consolas", 11, 'b');
gmem[800] > -80.0 ? (
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_measurestr("LINK: ONLINE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("LINK: ONLINE");
) : (
  gfx_r = 0.70; gfx_g = 0.75; gfx_b = 0.80;
  gfx_measurestr("STANDALONE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("STANDALONE");
);"""

new_g_link = """gfx_setfont(1, "Consolas", 10.5, 'b');
gmem[1090] == 3 ? (
  gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.25;
  mir_g_tag = "MIR DNA: LINKED";
  gfx_measurestr(mir_g_tag, lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr(mir_g_tag);
) : gmem[800] > -80.0 ? (
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_measurestr("LINK: ONLINE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("LINK: ONLINE");
) : (
  gfx_r = 0.70; gfx_g = 0.75; gfx_b = 0.80;
  gfx_measurestr("STANDALONE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("STANDALONE");
);"""

if old_g_link in g_code:
    g_code = g_code.replace(old_g_link, new_g_link, 1)
    with open(suites["guitar"], "w", encoding="utf-8") as f:
        f.write(g_code)
    print("Guitar Suite MIR badge formatted!")

# 4. Update VocalSuite Card 2 with MIR Sidecar badge
with open(suites["vocal"], "r", encoding="utf-8") as f:
    v_code = f.read()

old_v_link = """gfx_setfont(1, "Consolas", 11, 'b');
gmem[840] == 1 ? (
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_measurestr("GTR LINK: ONLINE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("GTR LINK: ONLINE");
) : (
  gfx_r = 0.70; gfx_g = 0.75; gfx_b = 0.80;
  gfx_measurestr("STANDALONE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("STANDALONE");
);"""

new_v_link = """gfx_setfont(1, "Consolas", 10.5, 'b');
gmem[1090] == 3 ? (
  gfx_r = 1.00; gfx_g = 0.40; gfx_b = 0.75;
  mir_v_tag = "MIR DNA: LINKED";
  gfx_measurestr(mir_v_tag, lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr(mir_v_tag);
) : gmem[840] == 1 ? (
  gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_measurestr("GTR LINK: ONLINE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("GTR LINK: ONLINE");
) : (
  gfx_r = 0.70; gfx_g = 0.75; gfx_b = 0.80;
  gfx_measurestr("STANDALONE", lnk_w, lnk_h);
  gfx_x = c2_x + card_w - lnk_w - 8; gfx_y = card_y + 6;
  gfx_drawstr("STANDALONE");
);"""

if old_v_link in v_code:
    v_code = v_code.replace(old_v_link, new_v_link, 1)
    with open(suites["vocal"], "w", encoding="utf-8") as f:
        f.write(v_code)
    print("Vocal Suite MIR badge formatted!")

# Deploy all to REAPER APPDATA Effects
import shutil
for name, p in suites.items():
    dst = os.path.join(reaper_effects, os.path.basename(p))
    shutil.copy2(p, dst)
    print(f"Deployed {os.path.basename(p)} to REAPER Effects")

print("\nAll suites formatted and deployed successfully!")
