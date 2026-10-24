import os, re

base_dir = r"c:\Dev\DameiSuite\effects"

def patch_file(fname, replacements):
    fpath = os.path.join(base_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        code = f.read()
    
    applied = 0
    for old_str, new_str in replacements:
        if old_str in code:
            code = code.replace(old_str, new_str)
            applied += 1
        else:
            print(f"[{fname}] WARNING: target snippet not found:\n{old_str[:60]}...")
            
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"[{fname}] Successfully applied {applied}/{len(replacements)} replacements.")

# -------------------------------------------------------------
# 1. BASS SUITE
# -------------------------------------------------------------
bass_replacements = [
    # Slider 20 definition
    (
        "slider20:15<0,18,1{Default Neutral Wire,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Cane Hill),Buster Odeholm (thrown / Vildhjarta),Kel Pinchin (Currents),Sam Guaiana (Silverstein),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bring Me The Horizon),Joey Sturgis (Asking Alexandria / Attack Attack),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / Simple Plan),Acle Kahney (TesseracT - King),heaving. (carsick / Grungegaze)}>-Producer Bass Signature Preset",
        "slider20:15<0,19,1{Default Neutral Wire,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Cane Hill),Buster Odeholm (thrown / Vildhjarta),Kel Pinchin (Currents),Sam Guaiana (Silverstein),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bring Me The Horizon),Joey Sturgis (Asking Alexandria / Attack Attack),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / Simple Plan),Acle Kahney (TesseracT - King),Adam Cichocki (heaving. - carsick / Timber Studios),Manuel Renner (SENNA - Out Of The Blue / Überlärm Studios)}>-Producer Bass Signature Preset"
    ),
    # Menu strings & bounds
    (
        'slider20 = min(18, slider20 + 1);',
        'slider20 = min(19, slider20 + 1);'
    ),
    (
        '18: heaving. (carsick / Grungegaze)',
        '18: Adam Cichocki (heaving. - carsick / Timber Studios)|19: Manuel Renner (SENNA - Out Of The Blue / Überlärm Studios)'
    ),
    # Preset text name
    (
        """  slider20 == 17 ? "17: Acle Kahney (TesseracT)" :
  "18: heaving. (carsick)"
);
gfx_measurestr(p_name, pnw, pnh);
gfx_x = p_box_x + (p_box_w - pnw) * 0.5; gfx_y = p_box_y + 7; gfx_drawstr(p_name);""",
        """  slider20 == 17 ? "17: Acle Kahney (TesseracT)" :
  slider20 == 18 ? "18: Adam Cichocki (heaving.)" :
  "19: Manuel Renner (SENNA)"
);
p_font_sz = 11.5;
gfx_setfont(1, "Consolas", p_font_sz, 'b');
gfx_measurestr(p_name, pnw, pnh);
while (pnw > p_box_w - 52 && p_font_sz > 8.0) (
  p_font_sz -= 0.5;
  gfx_setfont(1, "Consolas", p_font_sz, 'b');
  gfx_measurestr(p_name, pnw, pnh);
);
gfx_x = p_box_x + (p_box_w - pnw) * 0.5; gfx_y = p_box_y + 7; gfx_drawstr(p_name);"""
    ),
    # sync pill auto-fit
    (
        """gfx_measurestr(r_str, rsw, rsh);
gfx_x = sync_x + (sync_w - rsw) * 0.5; gfx_y = sync_y + 7; gfx_drawstr(r_str);""",
        """r_font_sz = 11.5;
gfx_setfont(1, "Orbitron", r_font_sz, 'b');
gfx_measurestr(r_str, rsw, rsh);
while (rsw > sync_w - 14 && r_font_sz > 8.0) (
  r_font_sz -= 0.5;
  gfx_setfont(1, "Orbitron", r_font_sz, 'b');
  gfx_measurestr(r_str, rsw, rsh);
);
gfx_x = sync_x + (sync_w - rsw) * 0.5; gfx_y = sync_y + 7; gfx_drawstr(r_str);"""
    ),
    # In apply_bass_preset
    (
        """  ) : p_idx == 18 ? (
    // 18: heaving. (carsick / Grungegaze) - Crushed Shoegaze Sub-Rumble & Fuzz Body
    slider2  = -18.0; slider3  = 65;  slider4  = 80;   slider5  = 2.2;
    slider6  = 40;   slider7  = 180; slider8  = 30;   slider9  = 45;
    slider10 = 2.4;  slider11 = -0.5; slider12 = -1.2; slider13 = -0.8;
    slider14 = 0.0;  slider15 = 0;   slider19 = -0.6;
    slider23 = 45;   slider24 = 40;  slider25 = 35;
  );""",
        """  ) : p_idx == 18 ? (
    // 18: Adam Cichocki (heaving. - carsick / Timber Studios) - Crushed Shoegaze Sub-Rumble & Fuzz Body
    slider2  = -18.0; slider3  = 65;  slider4  = 80;   slider5  = 2.2;
    slider6  = 40;   slider7  = 180; slider8  = 30;   slider9  = 45;
    slider10 = 2.4;  slider11 = -0.5; slider12 = -1.2; slider13 = -0.8;
    slider14 = 0.0;  slider15 = 0;   slider19 = -0.6;
    slider23 = 45;   slider24 = 40;  slider25 = 35;
  ) : p_idx == 19 ? (
    // 19: Manuel Renner (SENNA - Out Of The Blue / Überlärm Studios) - Hyper-Clean Laser Mono Sub & Clank Attack
    slider2  = -18.0; slider3  = 55;  slider4  = 85;   slider5  = 2.0;
    slider6  = 35;   slider7  = 160; slider8  = 32;   slider9  = 42;
    slider10 = 2.0;  slider11 = -0.8; slider12 = -1.8; slider13 = -0.5;
    slider14 = 0.0;  slider15 = 0;   slider19 = -0.8;
    slider23 = 30;   slider24 = 35;  slider25 = 25;
  );"""
    )
]
patch_file("Damei_BassSuite.jsfx", bass_replacements)

# -------------------------------------------------------------
# 2. VOCAL SUITE
# -------------------------------------------------------------
vocal_replacements = [
    # Slider 18 definition
    (
        "slider18:15<0,18,1{Default Neutral Wire,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Cane Hill),Buster Odeholm (thrown / Vildhjarta),Kel Pinchin (Currents),Sam Guaiana (Silverstein),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bring Me The Horizon),Joey Sturgis (Asking Alexandria / Attack Attack),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / Machine Gun Kelly),Acle Kahney (TesseracT - King),heaving. (carsick / Grungegaze)}>-Producer Vocal Signature Preset",
        "slider18:15<0,19,1{Default Neutral Wire,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Cane Hill),Buster Odeholm (thrown / Vildhjarta),Kel Pinchin (Currents),Sam Guaiana (Silverstein),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bring Me The Horizon),Joey Sturgis (Asking Alexandria / Attack Attack),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / Machine Gun Kelly),Acle Kahney (TesseracT - King),Adam Cichocki (heaving. - carsick / Timber Studios),Manuel Renner (SENNA - Out Of The Blue / Überlärm Studios)}>-Producer Vocal Signature Preset"
    ),
    (
        'slider18 = min(18, slider18 + 1);',
        'slider18 = min(19, slider18 + 1);'
    ),
    (
        '18: heaving. (carsick / Grungegaze)',
        '18: Adam Cichocki (heaving. - carsick / Timber Studios)|19: Manuel Renner (SENNA - Out Of The Blue / Überlärm Studios)'
    ),
    # Preset text name
    (
        """  slider18 == 17 ? "17: Acle Kahney (TesseracT)" :
  "18: heaving. (carsick)"
);
gfx_measurestr(p_name, pnw, pnh);
gfx_x = p_box_x + (p_box_w - pnw) * 0.5; gfx_y = p_box_y + 7; gfx_drawstr(p_name);""",
        """  slider18 == 17 ? "17: Acle Kahney (TesseracT)" :
  slider18 == 18 ? "18: Adam Cichocki (heaving.)" :
  "19: Manuel Renner (SENNA)"
);
p_font_sz = 11.5;
gfx_setfont(1, "Consolas", p_font_sz, 'b');
gfx_measurestr(p_name, pnw, pnh);
while (pnw > p_box_w - 52 && p_font_sz > 8.0) (
  p_font_sz -= 0.5;
  gfx_setfont(1, "Consolas", p_font_sz, 'b');
  gfx_measurestr(p_name, pnw, pnh);
);
gfx_x = p_box_x + (p_box_w - pnw) * 0.5; gfx_y = p_box_y + 7; gfx_drawstr(p_name);"""
    ),
    # sync pill auto-fit
    (
        """gfx_measurestr(r_str, rsw, rsh);
gfx_x = sync_x + (sync_w - rsw) * 0.5; gfx_y = sync_y + 7; gfx_drawstr(r_str);""",
        """r_font_sz = 11.5;
gfx_setfont(1, "Orbitron", r_font_sz, 'b');
gfx_measurestr(r_str, rsw, rsh);
while (rsw > sync_w - 14 && r_font_sz > 8.0) (
  r_font_sz -= 0.5;
  gfx_setfont(1, "Orbitron", r_font_sz, 'b');
  gfx_measurestr(r_str, rsw, rsh);
);
gfx_x = sync_x + (sync_w - rsw) * 0.5; gfx_y = sync_y + 7; gfx_drawstr(r_str);"""
    ),
    # In apply_vocal_preset
    (
        """  ) : p_idx == 18 ? (
    // heaving. (carsick / Grungegaze) - Embedded Shoegaze Vocal Halo & Saturated Bloom
    slider2  = -18.0; slider3  = 3.5;  slider4  = 2;    slider5  = 45;
    slider6  = 120;  slider7  = 110;  slider8  = -1.8; slider9  = 1.5;
    slider10 = 2.0;  slider11 = -1.2; slider12 = 0.5;  slider13 = 1.0;
    slider17 = -0.5; slider24 = -1.5; slider25 = -2.5; slider26 = 25;
    slider27 = -3.5; slider28 = 2.0;  slider40 = 25;
  );""",
        """  ) : p_idx == 18 ? (
    // Adam Cichocki (heaving. - carsick / Timber Studios) - Embedded Shoegaze Vocal Halo & Saturated Bloom
    slider2  = -18.0; slider3  = 3.5;  slider4  = 2;    slider5  = 45;
    slider6  = 120;  slider7  = 110;  slider8  = -1.8; slider9  = 1.5;
    slider10 = 2.0;  slider11 = -1.2; slider12 = 0.5;  slider13 = 1.0;
    slider17 = -0.5; slider24 = -1.5; slider25 = -2.5; slider26 = 25;
    slider27 = -3.5; slider28 = 2.0;  slider40 = 25;
  ) : p_idx == 19 ? (
    // Manuel Renner (SENNA - Out Of The Blue / Überlärm Studios) - Ultra-Modern Pristine Metalcore Vocal Presence & Polish
    slider2  = -18.0; slider3  = 4.2;  slider4  = 3;    slider5  = 55;
    slider6  = 140;  slider7  = 100;  slider8  = -2.2; slider9  = 2.2;
    slider10 = 2.5;  slider11 = -1.8; slider12 = 1.2;  slider13 = 1.5;
    slider17 = -0.8; slider24 = 0.0;  slider25 = -2.0; slider26 = 18;
    slider27 = -3.2; slider28 = -1.0; slider40 = 20;
  );"""
    )
]
patch_file("Damei_VocalSuite.jsfx", vocal_replacements)

# -------------------------------------------------------------
# 3. SYNTH SUITE
# -------------------------------------------------------------
synth_replacements = [
    # Slider 15 definition
    (
        "slider15:0<0,19,1{Jordan Fish (BMTH / Architects),Dan Braunstein (Spiritbox / Dayseeker),Buster Odeholm (thrown / Vildhjarta),George Lever (Sleep Token / Loathe),Zakk Cervini (Blink-182 / MGK),Joey Sturgis (Asking Alexandria / Attack Attack),Mick Gordon (DOOM / Wolfenstein),Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT / Graphic Nature),Jonathan Dolese (Mirrorcell / Cane Hill),Kel Pinchin (Currents / Invent Animate),Sam Guaiana (Silverstein / TDWP),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / BMTH - That's The Spirit),Acle Kahney (TesseracT - King),heaving. (carsick / Grungegaze)}>-Producer Synth Blueprint",
        "slider15:0<0,20,1{Jordan Fish (BMTH / Architects),Dan Braunstein (Spiritbox / Dayseeker),Buster Odeholm (thrown / Vildhjarta),George Lever (Sleep Token / Loathe),Zakk Cervini (Blink-182 / MGK),Joey Sturgis (Asking Alexandria / Attack Attack),Mick Gordon (DOOM / Wolfenstein),Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT / Graphic Nature),Jonathan Dolese (Mirrorcell / Cane Hill),Kel Pinchin (Currents / Invent Animate),Sam Guaiana (Silverstein / TDWP),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / BMTH - That's The Spirit),Acle Kahney (TesseracT - King),Adam Cichocki (heaving. - carsick / Timber Studios),Manuel Renner (SENNA - Out Of The Blue / Überlärm Studios)}>-Producer Synth Blueprint"
    ),
    (
        '20. heaving. (carsick / Grungegaze)',
        '20. Adam Cichocki (heaving. - carsick / Timber Studios)|21. Manuel Renner (SENNA - Out Of The Blue / Überlärm Studios)'
    ),
    (
        """  p_idx_c == 18 ? "19. Acle Kahney (TesseracT)" :
                  "20. heaving. (carsick)"
);
gfx_measurestr(p_name_hdr, pnw, pnh);
gfx_x = p_pill_x + (p_pill_w - pnw) * 0.5; gfx_y = p_pill_y + 9;
gfx_drawstr(p_name_hdr);""",
        """  p_idx_c == 18 ? "19. Acle Kahney (TesseracT)" :
  p_idx_c == 19 ? "20. Adam Cichocki (heaving.)" :
                  "21. Manuel Renner (SENNA)"
);
p_font_sz = 12.0;
gfx_setfont(1, "Orbitron", p_font_sz, 'b');
gfx_measurestr(p_name_hdr, pnw, pnh);
while (pnw > p_pill_w - 16 && p_font_sz > 8.0) (
  p_font_sz -= 0.5;
  gfx_setfont(1, "Orbitron", p_font_sz, 'b');
  gfx_measurestr(p_name_hdr, pnw, pnh);
);
gfx_x = p_pill_x + (p_pill_w - pnw) * 0.5; gfx_y = p_pill_y + 9;
gfx_drawstr(p_name_hdr);"""
    ),
    (
        """gfx_measurestr(rgn_txt, rpw, rph);
gfx_x = rgn_pill_x + (rgn_pill_w - rpw) * 0.5; gfx_y = rgn_pill_y + 9;
gfx_drawstr(rgn_txt);""",
        """r_font_sz = 12.0;
gfx_setfont(1, "Orbitron", r_font_sz, 'b');
gfx_measurestr(rgn_txt, rpw, rph);
while (rpw > rgn_pill_w - 16 && r_font_sz > 8.0) (
  r_font_sz -= 0.5;
  gfx_setfont(1, "Orbitron", r_font_sz, 'b');
  gfx_measurestr(rgn_txt, rpw, rph);
);
gfx_x = rgn_pill_x + (rgn_pill_w - rpw) * 0.5; gfx_y = rgn_pill_y + 9;
gfx_drawstr(rgn_txt);"""
    )
]
patch_file("Damei_SynthSuite.jsfx", synth_replacements)

# -------------------------------------------------------------
# 4. MIXING SUITE
# -------------------------------------------------------------
mixing_replacements = [
    # auto-fit rgn_str
    (
        """gfx_measurestr(rgn_str, rsw, rsh);
gfx_x = floor(rgn_pill_x + (rgn_pill_w - rsw) * 0.5); gfx_y = crt_y + 17;
gfx_drawstr(rgn_str);""",
        """r_font_sz = 11.0;
gfx_setfont(1, "Orbitron", r_font_sz, 'b');
gfx_measurestr(rgn_str, rsw, rsh);
while (rsw > rgn_pill_w - 14 && r_font_sz > 8.0) (
  r_font_sz -= 0.5;
  gfx_setfont(1, "Orbitron", r_font_sz, 'b');
  gfx_measurestr(rgn_str, rsw, rsh);
);
gfx_x = floor(rgn_pill_x + (rgn_pill_w - rsw) * 0.5); gfx_y = crt_y + 17;
gfx_drawstr(rgn_str);"""
    ),
    # auto-fit p_title
    (
        """is_user_customized ? (p_title = sprintf(#, "%s [C]", p_title););
gfx_drawstr(p_title);""",
        """is_user_customized ? (p_title = sprintf(#, "%s [C]", p_title););
pt_sz = 12.0;
gfx_setfont(1, "Segoe UI", pt_sz, 'b');
gfx_measurestr(p_title, ptw, pth);
while (ptw > bar_w - 22 && pt_sz > 8.0) (
  pt_sz -= 0.5;
  gfx_setfont(1, "Segoe UI", pt_sz, 'b');
  gfx_measurestr(p_title, ptw, pth);
);
gfx_drawstr(p_title);"""
    )
]
patch_file("Damei_MixingSuite.jsfx", mixing_replacements)

# -------------------------------------------------------------
# 5. OZONE SUITE
# -------------------------------------------------------------
ozone_replacements = [
    # Slider 33 definition
    (
        "heaving. (carsick / Grungegaze)}>-Mastering Engineer Signature Preset",
        "Adam Cichocki (heaving. - carsick / Timber Studios),Manuel Renner (SENNA - Out Of The Blue / Überlärm Studios)}>-Mastering Engineer Signature Preset"
    ),
    (
        "slider33:0<0,23,1{",
        "slider33:0<0,24,1{"
    ),
    # auto-fit p_title
    (
        """gfx_r = 1.00; gfx_g = 0.72; gfx_b = 0.15;
gfx_setfont(1, "Segoe UI", 12, 'b');
gfx_x = bar_x + 8; gfx_y = 31;""",
        """gfx_r = 1.00; gfx_g = 0.72; gfx_b = 0.15;
pt_sz = 12.0;
gfx_setfont(1, "Segoe UI", pt_sz, 'b');
gfx_measurestr(p_title, ptw, pth);
while (ptw > bar_w - 22 && pt_sz > 8.0) (
  pt_sz -= 0.5;
  gfx_setfont(1, "Segoe UI", pt_sz, 'b');
  gfx_measurestr(p_title, ptw, pth);
);
gfx_x = bar_x + 8; gfx_y = 31;"""
    )
]
patch_file("Damei_OzoneSuite.jsfx", ozone_replacements)

print("All suite formatting and metadata patches completed!")
