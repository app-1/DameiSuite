import re, os

effects_dir = r"C:\Dev\DameiSuite\effects"
appdata_dir = os.path.expandvars(r"%APPDATA%\REAPER\Effects\Damei")

# ==============================================================================
# 1. GUITAR SUITE
# ==============================================================================
gtr_path = os.path.join(effects_dir, "Damei_GuitarSuite.jsfx")
t = open(gtr_path, "r", encoding="utf-8").read()

# Header p_title
old_p_title = r'''p_title = (p_m==0  ? "0: DEFAULT NEUTRAL WIRE" :
          (p_m==1  ? "1: LANCE PRENC (ALPHA WOLF)" :
          (p_m==2  ? "2: SCOTT SEIGEL (DIESECT)" :
          (p_m==3  ? "3: JONATHAN DOLESE (CANE HILL)" :
          (p_m==4  ? "4: BUSTER ODEHOLM (THROWN)" :
          (p_m==5  ? "5: KEL PINCHIN (CURRENTS)" :
          (p_m==6  ? "6: SAM GUAIANA (SILVERSTEIN)" :
          (p_m==7  ? "7: FORRESTER SAVELL (KARNIVOOL)" :
          (p_m==8  ? "8: JENS BOGREN (FASCINATION)" :
          (p_m==9  ? "9: ADAM NOLLY GETGOOD (GGD)" :
          (p_m==10 ? "10: WILL PUTNEY (FFAA)" :
          (p_m==11 ? "11: GEORGE LEVER (SLEEP TOKEN)" :
          (p_m==12 ? "12: SAM BASSAL (THORNHILL)" :
          (p_m==13 ? "13: HENRIK UDD (ARCHITECTS)" :
          (p_m==14 ? "14: JOEY STURGIS (ASKING ALEX)" :
          (p_m==15 ? "15: DAN BRAUNSTEIN (SPIRITBOX)" :
                     "16: ZAKK CERVINI (BLINK-182)"))))))))))))))));'''

new_p_title = r'''p_title = (p_m==0  ? "0: DEFAULT NEUTRAL WIRE" :
          (p_m==1  ? "1: LANCE PRENC (ALPHA WOLF)" :
          (p_m==2  ? "2: SCOTT SEIGEL (DIESECT)" :
          (p_m==3  ? "3: JONATHAN DOLESE (CANE HILL)" :
          (p_m==4  ? "4: BUSTER ODEHOLM (THROWN)" :
          (p_m==5  ? "5: KEL PINCHIN (CURRENTS)" :
          (p_m==6  ? "6: SAM GUAIANA (SILVERSTEIN)" :
          (p_m==7  ? "7: FORRESTER SAVELL (KARNIVOOL)" :
          (p_m==8  ? "8: JENS BOGREN (FASCINATION)" :
          (p_m==9  ? "9: ADAM NOLLY GETGOOD (GGD)" :
          (p_m==10 ? "10: WILL PUTNEY (FFAA)" :
          (p_m==11 ? "11: GEORGE LEVER (SLEEP TOKEN)" :
          (p_m==12 ? "12: SAM BASSAL (THORNHILL)" :
          (p_m==13 ? "13: HENRIK UDD (ARCHITECTS)" :
          (p_m==14 ? "14: JOEY STURGIS (ASKING ALEX)" :
          (p_m==15 ? "15: DAN BRAUNSTEIN (SPIRITBOX)" :
          (p_m==16 ? "16: ZAKK CERVINI (BLINK-182)" :
          (p_m==17 ? "17: ACLE KAHNEY (TESSERACT)" :
                     "18: HEAVING. (CARSICK)"))))))))))))))))));'''

if old_p_title in t:
    t = t.replace(old_p_title, new_p_title, 1)

# Header steppers & menu
t = t.replace("slider23 = min(16, slider23 + 1);", "slider23 = min(18, slider23 + 1);")
old_gtr_menu = '16: Zakk Cervini (Blink-182 / BMTH)")'
new_gtr_menu = '16: Zakk Cervini (Blink-182 / BMTH)|17: Acle Kahney (TesseracT - King)|18: heaving. (carsick / Grungegaze)")'
t = t.replace(old_gtr_menu, new_gtr_menu)

# Producer Matrix tab
t = t.replace("PRODUCER GUITAR SIGNATURE MATRIX (17 INDUSTRY REFERENCE PROFILES)", "PRODUCER GUITAR SIGNATURE MATRIX (19 INDUSTRY REFERENCE PROFILES)")
t = re.sub(r'loop\(17,(\s+row = floor\(pi / cols\);)', r'loop(19,\1', t)

old_gtr_lbl = r'''      pi == 15 ? "15: Dan Braunstein (Spiritbox)" :
      "16: Zakk Cervini (Blink-182)"'''
new_gtr_lbl = r'''      pi == 15 ? "15: Dan Braunstein (Spiritbox)" :
      pi == 16 ? "16: Zakk Cervini (Blink-182)" :
      pi == 17 ? "17: Acle Kahney (TesseracT)" :
      "18: heaving. (carsick)"'''
t = t.replace(old_gtr_lbl, new_gtr_lbl)

open(gtr_path, "w", encoding="utf-8").write(t)
open(os.path.join(appdata_dir, "Damei_GuitarSuite.jsfx"), "w", encoding="utf-8").write(t)
print("Guitar Suite GUI patched.")

# ==============================================================================
# 2. BASS SUITE
# ==============================================================================
bass_path = os.path.join(effects_dir, "Damei_BassSuite.jsfx")
t = open(bass_path, "r", encoding="utf-8").read()

t = t.replace("slider20 = min(16, slider20 + 1);", "slider20 = min(18, slider20 + 1);")

old_bass_pname = r'''  slider20 == 15 ? "15: Dan Braunstein (Spiritbox)" :
  "16: Zakk Cervini (Blink-182)"
);'''
new_bass_pname = r'''  slider20 == 15 ? "15: Dan Braunstein (Spiritbox)" :
  slider20 == 16 ? "16: Zakk Cervini (Blink-182)" :
  slider20 == 17 ? "17: Acle Kahney (TesseracT)" :
  "18: heaving. (carsick)"
);'''
t = t.replace(old_bass_pname, new_bass_pname)

# Producer matrix tab
t = t.replace("PRODUCER BASS SIGNATURE MATRIX (17 INDUSTRY REFERENCE PROFILES)", "PRODUCER BASS SIGNATURE MATRIX (19 INDUSTRY REFERENCE PROFILES)")
t = re.sub(r'loop\(17,(\s+row = floor\(pi / cols\);)', r'loop(19,\1', t)

old_bass_lbl = r'''      pi == 15 ? "15: Dan Braunstein (Spiritbox)" :
      "16: Zakk Cervini (Blink-182)"'''
new_bass_lbl = r'''      pi == 15 ? "15: Dan Braunstein (Spiritbox)" :
      pi == 16 ? "16: Zakk Cervini (Blink-182)" :
      pi == 17 ? "17: Acle Kahney (TesseracT)" :
      "18: heaving. (carsick)"'''
t = t.replace(old_bass_lbl, new_bass_lbl)

# Add dropdown click handler on p_box in Bass Suite
old_bass_click = r'''mouse_clicked && right_hov ? (
  slider20 = min(18, slider20 + 1); apply_bass_preset(slider20); slider_automate();
);'''
new_bass_click = r'''mouse_clicked && right_hov ? (
  slider20 = min(18, slider20 + 1); apply_bass_preset(slider20); slider_automate();
);
mouse_clicked && (mouse_x > p_box_x + p_btn_w && mouse_x < p_box_x + p_box_w - p_btn_w && mouse_y >= p_box_y && mouse_y <= p_box_y + p_box_h) ? (
  b_choice = gfx_showmenu("0: Default Neutral Wire|1: Lance Prenc (Alpha Wolf / Polaris)|2: Scott Seigel (DIESECT)|3: Jonathan Dolese (Cane Hill)|4: Buster Odeholm (thrown / Vildhjarta)|5: Kel Pinchin (Currents)|6: Sam Guaiana (Silverstein)|7: Forrester Savell (Karnivool)|8: Jens Bogren (Fascination Street)|9: Adam Nolly Getgood (Periphery)|10: Will Putney (Fit For An Autopsy)|11: George Lever (Sleep Token)|12: Sam Bassal (Thornhill)|13: Henrik Udd (Architects)|14: Joey Sturgis (Asking Alexandria)|15: Dan Braunstein (Spiritbox)|16: Zakk Cervini (Blink-182)|17: Acle Kahney (TesseracT - King)|18: heaving. (carsick / Grungegaze)");
  b_choice > 0 ? (slider20 = b_choice - 1; apply_bass_preset(slider20); slider_automate(););
);'''
t = t.replace(old_bass_click, new_bass_click)

open(bass_path, "w", encoding="utf-8").write(t)
open(os.path.join(appdata_dir, "Damei_BassSuite.jsfx"), "w", encoding="utf-8").write(t)
print("Bass Suite GUI patched.")

# ==============================================================================
# 3. DRUM SUITE
# ==============================================================================
drum_path = os.path.join(effects_dir, "Damei_DrumSuite.jsfx")
t = open(drum_path, "r", encoding="utf-8").read()

old_drum_ptitle = r'''p_title = (p_m==0  ? "0: GGD MODERN & MASSIVE (1:1 PASS)" :
          (p_m==1  ? "1: LANCE PRENC (RIMSHOT CRACK)" :
          (p_m==2  ? "2: SCOTT SEIGEL (TIGHT POCKET)" :
          (p_m==3  ? "3: JONATHAN DOLESE (SHELL WEIGHT)" :
          (p_m==4  ? "4: BUSTER ODEHOLM (THALL SNAP)" :
          (p_m==5  ? "5: KEL PINCHIN (PROG POCKET)" :
          (p_m==6  ? "6: SAM GUAIANA (MID EXPLOSION)" :
          (p_m==7  ? "7: FORRESTER SAVELL (PROG DEPTH)" :
          (p_m==8  ? "8: JENS BOGREN (NORDIC WEIGHT)" :
          (p_m==9  ? "9: NOLLY GETGOOD (SURGICAL)" :
          (p_m==10 ? "10: WILL PUTNEY (RAW SLAM)" :
          (p_m==11 ? "11: GEORGE LEVER (CINEMATIC AIR)" :
          (p_m==12 ? "12: SAM BASSAL (GRUNGE PUNCH)" :
          (p_m==13 ? "13: HENRIK UDD (MASSIVE UK)" :
          (p_m==14 ? "14: JOEY STURGIS (HYPER SLAM)" :
          (p_m==15 ? "15: DAN BRAUNSTEIN (SILK PUNCH)" :
                     "16: ZAKK CERVINI (RADIO CRACK)"))))))))))))))));'''

new_drum_ptitle = r'''p_title = (p_m==0  ? "0: GGD MODERN & MASSIVE (1:1 PASS)" :
          (p_m==1  ? "1: LANCE PRENC (RIMSHOT CRACK)" :
          (p_m==2  ? "2: SCOTT SEIGEL (TIGHT POCKET)" :
          (p_m==3  ? "3: JONATHAN DOLESE (SHELL WEIGHT)" :
          (p_m==4  ? "4: BUSTER ODEHOLM (THALL SNAP)" :
          (p_m==5  ? "5: KEL PINCHIN (PROG POCKET)" :
          (p_m==6  ? "6: SAM GUAIANA (MID EXPLOSION)" :
          (p_m==7  ? "7: FORRESTER SAVELL (PROG DEPTH)" :
          (p_m==8  ? "8: JENS BOGREN (NORDIC WEIGHT)" :
          (p_m==9  ? "9: NOLLY GETGOOD (SURGICAL)" :
          (p_m==10 ? "10: WILL PUTNEY (RAW SLAM)" :
          (p_m==11 ? "11: GEORGE LEVER (CINEMATIC AIR)" :
          (p_m==12 ? "12: SAM BASSAL (GRUNGE PUNCH)" :
          (p_m==13 ? "13: HENRIK UDD (MASSIVE UK)" :
          (p_m==14 ? "14: JOEY STURGIS (HYPER SLAM)" :
          (p_m==15 ? "15: DAN BRAUNSTEIN (SILK PUNCH)" :
          (p_m==16 ? "16: ZAKK CERVINI (RADIO CRACK)" :
          (p_m==17 ? "17: ACLE KAHNEY (TESSERACT)" :
                     "18: HEAVING. (CARSICK)"))))))))))))))))));'''

if old_drum_ptitle in t:
    t = t.replace(old_drum_ptitle, new_drum_ptitle, 1)

t = t.replace("slider25 = min(16, slider25 + 1);", "slider25 = min(18, slider25 + 1);")
old_drum_menu = '16: Zakk Cervini (Blink-182 / BMTH)")'
new_drum_menu = '16: Zakk Cervini (Blink-182 / BMTH)|17: Acle Kahney (TesseracT - King)|18: heaving. (carsick / Grungegaze)")'
t = t.replace(old_drum_menu, new_drum_menu)

# Producer matrix tab
t = re.sub(r'loop\(17,(\s+px = disp_x \+ 10 \+ pi \* \(pill_w \+ 4\);)', r'loop(19,\1', t)
old_drum_pname = r'''             pi == 15? "15: BRAUNSTEIN" :
                       "16: CERVINI";'''
new_drum_pname = r'''             pi == 15? "15: BRAUNSTEIN" :
             pi == 16? "16: CERVINI" :
             pi == 17? "17: ACLE" :
                       "18: HEAVING";'''
t = t.replace(old_drum_pname, new_drum_pname)

old_drum_rec = r'''          p_sel == 15? "DAN BRAUNSTEIN // Spiritbox / Volumes Standard: Snare Weight +3.2dB, Scoop -2.8dB, Silk +2.0dB" :
                       "ZAKK CERVINI // Blink-182 / BMTH: Upfront Radio Rimshot Crack +3.2dB, Stick +2.0dB";'''
new_drum_rec = r'''          p_sel == 15? "DAN BRAUNSTEIN // Spiritbox: Snare Weight +3.2dB, Scoop -2.8dB, Silk +2.0dB" :
          p_sel == 16? "ZAKK CERVINI // Blink-182 / BMTH: Upfront Radio Rimshot Crack +3.2dB, Stick +2.0dB" :
          p_sel == 17? "ACLE KAHNEY // TesseracT: Snare Snap (+1.6dB), 120ms Dynamic Punch, Silk Cymbals" :
                       "HEAVING. // carsick: Crushed Shoegaze Room Wash, Heavy Fat Snare (+1.4dB Tail)";'''
t = t.replace(old_drum_rec, new_drum_rec)

open(drum_path, "w", encoding="utf-8").write(t)
open(os.path.join(appdata_dir, "Damei_DrumSuite.jsfx"), "w", encoding="utf-8").write(t)
print("Drum Suite GUI patched.")

# ==============================================================================
# 4. VOCAL SUITE
# ==============================================================================
voc_path = os.path.join(effects_dir, "Damei_VocalSuite.jsfx")
t = open(voc_path, "r", encoding="utf-8").read()

t = t.replace("slider18 = min(16, slider18 + 1);", "slider18 = min(18, slider18 + 1);")

old_voc_pname = r'''  slider18 == 15 ? "15: Dan Braunstein (Spiritbox)" :
  "16: Zakk Cervini (Blink-182)"
);'''
new_voc_pname = r'''  slider18 == 15 ? "15: Dan Braunstein (Spiritbox)" :
  slider18 == 16 ? "16: Zakk Cervini (Blink-182)" :
  slider18 == 17 ? "17: Acle Kahney (TesseracT)" :
  "18: heaving. (carsick)"
);'''
t = t.replace(old_voc_pname, new_voc_pname)

# Producer matrix tab
t = t.replace("PRODUCER VOCAL SIGNATURE MATRIX (17 INDUSTRY REFERENCE PROFILES)", "PRODUCER VOCAL SIGNATURE MATRIX (19 INDUSTRY REFERENCE PROFILES)")
t = re.sub(r'loop\(17,(\s+row = floor\(pi / cols\);)', r'loop(19,\1', t)

old_voc_lbl = r'''      pi == 15 ? "15: Dan Braunstein (Spiritbox)" :
      "16: Zakk Cervini (Blink-182)"'''
new_voc_lbl = r'''      pi == 15 ? "15: Dan Braunstein (Spiritbox)" :
      pi == 16 ? "16: Zakk Cervini (Blink-182)" :
      pi == 17 ? "17: Acle Kahney (TesseracT)" :
      "18: heaving. (carsick)"'''
t = t.replace(old_voc_lbl, new_voc_lbl)

# Add dropdown on center of p_box
old_voc_click = r'''mouse_clicked && right_hov ? (
  slider18 = min(18, slider18 + 1); apply_vocal_preset(slider18); slider_automate();
);'''
new_voc_click = r'''mouse_clicked && right_hov ? (
  slider18 = min(18, slider18 + 1); apply_vocal_preset(slider18); slider_automate();
);
mouse_clicked && (mouse_x > p_box_x + p_btn_w && mouse_x < p_box_x + p_box_w - p_btn_w && mouse_y >= p_box_y && mouse_y <= p_box_y + p_box_h) ? (
  v_choice = gfx_showmenu("0: Default Neutral Wire|1: Lance Prenc (Alpha Wolf / Polaris)|2: Scott Seigel (DIESECT)|3: Jonathan Dolese (Cane Hill)|4: Buster Odeholm (thrown / Vildhjarta)|5: Kel Pinchin (Currents)|6: Sam Guaiana (Silverstein)|7: Forrester Savell (Karnivool)|8: Jens Bogren (Fascination Street)|9: Adam Nolly Getgood (Periphery)|10: Will Putney (Fit For An Autopsy)|11: George Lever (Sleep Token)|12: Sam Bassal (Thornhill)|13: Henrik Udd (Architects)|14: Joey Sturgis (Asking Alexandria)|15: Dan Braunstein (Spiritbox)|16: Zakk Cervini (Blink-182)|17: Acle Kahney (TesseracT - King)|18: heaving. (carsick / Grungegaze)");
  v_choice > 0 ? (slider18 = v_choice - 1; apply_vocal_preset(slider18); slider_automate(););
);'''
t = t.replace(old_voc_click, new_voc_click)

open(voc_path, "w", encoding="utf-8").write(t)
open(os.path.join(appdata_dir, "Damei_VocalSuite.jsfx"), "w", encoding="utf-8").write(t)
print("Vocal Suite GUI patched.")

# ==============================================================================
# 5. SYNTH SUITE
# ==============================================================================
syn_path = os.path.join(effects_dir, "Damei_SynthSuite.jsfx")
t = open(syn_path, "r", encoding="utf-8").read()

t = t.replace("min(17, floor(slider15 + 0.5))", "min(19, floor(slider15 + 0.5))")

old_syn_hdr = r'''  p_idx_c == 16 ? "17. Sam Bassal (Thornhill)" :
                  "18. Henrik Udd (Architects)"
);'''
new_syn_hdr = r'''  p_idx_c == 16 ? "17. Sam Bassal (Thornhill)" :
  p_idx_c == 17 ? "18. Henrik Udd (Architects)" :
  p_idx_c == 18 ? "19. Acle Kahney (TesseracT)" :
                  "20. heaving. (carsick)"
);'''
t = t.replace(old_syn_hdr, new_syn_hdr)

old_prod_short = r'''  i == 16 ? "17. Sam Bassal" :
            "18. Henrik Udd";'''
new_prod_short = r'''  i == 16 ? "17. Sam Bassal" :
  i == 17 ? "18. Henrik Udd" :
  i == 18 ? "19. Acle Kahney" :
            "20. heaving.";'''
t = t.replace(old_prod_short, new_prod_short)

old_prod_full = r'''  i == 17 ? "HENRIK UDD (Architects / Bring Me The Horizon - That's The Spirit)" :
            "PRODUCER BLUEPRINT";'''
new_prod_full = r'''  i == 17 ? "HENRIK UDD (Architects / Bring Me The Horizon - That's The Spirit)" :
  i == 18 ? "ACLE KAHNEY (TesseracT - King / 4D Sounds)" :
  i == 19 ? "HEAVING. (carsick / Grungegaze)" :
            "PRODUCER BLUEPRINT";'''
t = t.replace(old_prod_full, new_prod_full)

t = t.replace("PRODUCER REFERENCE ROSTER (18 BLUEPRINTS)", "PRODUCER REFERENCE ROSTER (20 BLUEPRINTS)")
t = t.replace("while (pi < 18)", "while (pi < 20)")

# Add dropdown on p_pill click in Synth Suite
old_syn_click = r'''// Pinned Project Region Sync Pill'''
new_syn_click = r'''// Dropdown selector on p_pill click
mouse_clicked && (mouse_x >= p_pill_x && mouse_x <= p_pill_x + p_pill_w && mouse_y >= p_pill_y && mouse_y <= p_pill_y + p_pill_h) ? (
  s_choice = gfx_showmenu("1. Jordan Fish (BMTH / Architects)|2. Dan Braunstein (Spiritbox / Dayseeker)|3. Buster Odeholm (thrown / Vildhjarta)|4. George Lever (Sleep Token / Loathe)|5. Zakk Cervini (Blink-182 / MGK)|6. Joey Sturgis (Asking Alexandria)|7. Mick Gordon (DOOM / Wolfenstein)|8. Lance Prenc (Alpha Wolf / Polaris)|9. Scott Seigel (DIESECT / Graphic Nature)|10. Jonathan Dolese (Mirrorcell / Cane Hill)|11. Kel Pinchin (Currents / Invent Animate)|12. Sam Guaiana (Silverstein / TDWP)|13. Forrester Savell (Karnivool / DLC)|14. Jens Bogren (Fascination Street)|15. Adam Nolly Getgood (Periphery)|16. Will Putney (Fit For An Autopsy)|17. Sam Bassal (Thornhill / Ocean Grove)|18. Henrik Udd (Architects / BMTH)|19. Acle Kahney (TesseracT - King)|20. heaving. (carsick / Grungegaze)");
  s_choice > 0 ? (apply_synth_preset(s_choice - 1); slider_automate(););
);

// Pinned Project Region Sync Pill'''
t = t.replace(old_syn_click, new_syn_click)

open(syn_path, "w", encoding="utf-8").write(t)
open(os.path.join(appdata_dir, "Damei_SynthSuite.jsfx"), "w", encoding="utf-8").write(t)
print("Synth Suite GUI patched.")

print("All GUI preset lists fully patched!")
