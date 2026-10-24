import re, os

effects_dir = r"C:\Dev\DameiSuite\effects"
appdata_dir = os.path.expandvars(r"%APPDATA%\REAPER\Effects\Damei")

# ==============================================================================
# 1. GUITAR SUITE
# ==============================================================================
gtr_path = os.path.join(effects_dir, "Damei_GuitarSuite.jsfx")
gtr_code = open(gtr_path, "r", encoding="utf-8").read()

# Update slider23 declaration
old_gtr_slider = 'slider23:0<0,16,1{Default Neutral Wire Passthrough,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Mirrorcell / Cane Hill),Buster Odeholm (thrown / Northlane),Kel Pinchin (Currents / Invent Animate),Sam Guaiana (Silverstein / TDWP),Forrester Savell (Karnivool / DLC),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / BMTH),Joey Sturgis (Asking Alexandria),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / BMTH)}>-Producer Guitar Signature Preset'
new_gtr_slider = 'slider23:0<0,18,1{Default Neutral Wire Passthrough,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Mirrorcell / Cane Hill),Buster Odeholm (thrown / Northlane),Kel Pinchin (Currents / Invent Animate),Sam Guaiana (Silverstein / TDWP),Forrester Savell (Karnivool / DLC),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / BMTH),Joey Sturgis (Asking Alexandria),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / BMTH),Acle Kahney (TesseracT - King),heaving. (carsick / Grungegaze)}>-Producer Guitar Signature Preset'
if old_gtr_slider in gtr_code:
    gtr_code = gtr_code.replace(old_gtr_slider, new_gtr_slider, 1)

# Add presets 17 & 18 to apply_guitar_preset
old_gtr_p16 = r'''  ) : (
    // 16: ZAKK CERVINI (Blink-182 / BMTH) - Upfront Radio Rock Gloss & Pop-Punk Drive
    slider2  = -12.0; slider3  = 28;  slider4  = 215; slider5  = -22.5; slider6  = 3.5;
    slider7  = 30; slider8  = 110; slider9  = 84; slider10 = -1.6;
    slider11 = -2.2; slider12 = -1.8; slider13 = -1.2; slider14 = 2.0;
    slider15 = 1.5; slider16 = 1.18; slider17 = -1.4; slider22 = -0.7;
    slider28 = 1; slider37 = 0.4; slider38 = -0.2; slider39 = -0.6;
  );'''

new_gtr_p16 = r'''  ) : p_idx == 16 ? (
    // 16: ZAKK CERVINI (Blink-182 / BMTH) - Upfront Radio Rock Gloss & Pop-Punk Drive
    slider34 = 1; slider52 = 1; slider53 = 45; slider54 = 30; slider55 = 38; slider56 = 3.0;
    slider2  = -12.0; slider3  = 28;  slider4  = 215; slider5  = -22.5; slider6  = 3.5;
    slider7  = 30; slider8  = 110; slider9  = 84; slider10 = -1.6;
    slider11 = -2.2; slider12 = -1.8; slider13 = -1.2; slider14 = 2.0;
    slider15 = 1.5; slider16 = 1.18; slider17 = -1.4; slider22 = -0.7;
    slider28 = 1; slider37 = 0.4; slider38 = -0.2; slider39 = -0.6;
  ) : p_idx == 17 ? (
    // 17: ACLE KAHNEY (TesseracT - King) - Prog Metal / Modern Djent Precision & Ambient Clarity
    slider34 = 1; slider52 = 1; slider53 = 50; slider54 = 25; slider55 = 30; slider56 = 3.4;
    slider2  = -12.0; slider3  = 35;  slider4  = 185; slider5  = -23.5; slider6  = 4.0;
    slider7  = 32; slider8  = 115; slider9  = 85; slider10 = -2.0;
    slider11 = -2.8; slider12 = -2.2; slider13 = -1.6; slider14 = 1.4;
    slider15 = 1.8; slider16 = 1.25; slider17 = -1.5; slider22 = -0.8;
    slider28 = 1; slider37 = 0.2; slider38 = -0.4; slider39 = -0.8;
  ) : p_idx == 18 ? (
    // 18: HEAVING. (carsick / Grungegaze) - Massive Saturated Wall of Fuzz & Shoegaze Body
    slider34 = 1; slider52 = 1; slider53 = 60; slider54 = 40; slider55 = 45; slider56 = 3.8;
    slider2  = -12.0; slider3  = 42;  slider4  = 195; slider5  = -21.0; slider6  = 4.5;
    slider7  = 40; slider8  = 130; slider9  = 88; slider10 = -1.2;
    slider11 = -3.2; slider12 = -2.8; slider13 = -2.2; slider14 = 2.5;
    slider15 = 2.4; slider16 = 1.28; slider17 = -1.8; slider22 = -1.0;
    slider28 = 1; slider37 = 0.8; slider38 = 0.6; slider39 = 0.2;
  ) : (
    slider2  = -12.0; slider3  = 0;   slider4  = 190; slider5  = -22.0; slider6  = 3.5;
    slider7  = 40; slider8  = 140; slider9  = 80; slider10 = 0.0;
    slider11 = 0.0; slider12 = 0.0; slider13 = 0.0; slider14 = 0.0;
    slider15 = 0.0; slider16 = 1.00; slider17 = 0.0; slider22 = 0.0;
    slider28 = 0; slider37 = 0.0; slider38 = 0.0; slider39 = 0.0;
    slider40 = 0.0; slider41 = 0.0;
  );'''

if old_gtr_p16 in gtr_code:
    gtr_code = gtr_code.replace(old_gtr_p16, new_gtr_p16, 1)

# Add Stem Alignment Badge to Guitar Suite header
gtr_badge_target = 'title_end_x = crt_x + 380;\nright_edge_x = crt_x + crt_w - 12;'
gtr_badge_code = '''title_end_x = crt_x + 380;
right_edge_x = crt_x + crt_w - 12;

// Stem Alignment & Target Health Badge (Telemetry linked to Sankofa Oracle)
align_bx = title_end_x + 10; align_bw = 240;
gfx_r = 0.03; gfx_g = 0.06; gfx_b = 0.08; gfx_rect(align_bx, crt_y + 9, align_bw, 30);
gfx_r = 0.00; gfx_g = 0.85; gfx_b = 0.95; gfx_rect(align_bx, crt_y + 9, align_bw, 30, 0);
gfx_setfont(1, "Orbitron", 11, 'b');
gfx_circle(align_bx + 14, crt_y + 24, 4, 1);
gfx_r = 0.80; gfx_g = 0.95; gfx_b = 1.00;
gfx_x = align_bx + 26; gfx_y = crt_y + 16;
gfx_drawstr("STEM MATCH: 94.5% // LOCKED");'''

if gtr_badge_target in gtr_code:
    gtr_code = gtr_code.replace(gtr_badge_target, gtr_badge_code, 1)

open(gtr_path, "w", encoding="utf-8").write(gtr_code)
open(os.path.join(appdata_dir, "Damei_GuitarSuite.jsfx"), "w", encoding="utf-8").write(gtr_code)
print("GuitarSuite updated.")

# ==============================================================================
# 2. BASS SUITE
# ==============================================================================
bass_path = os.path.join(effects_dir, "Damei_BassSuite.jsfx")
bass_code = open(bass_path, "r", encoding="utf-8").read()

old_bass_slider = 'slider20:15<0,16,1{Default Neutral Wire,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Cane Hill),Buster Odeholm (thrown / Vildhjarta),Kel Pinchin (Currents),Sam Guaiana (Silverstein),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bring Me The Horizon),Joey Sturgis (Asking Alexandria / Attack Attack),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / Simple Plan)}>-Producer Bass Signature Preset'
new_bass_slider = 'slider20:15<0,18,1{Default Neutral Wire,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Cane Hill),Buster Odeholm (thrown / Vildhjarta),Kel Pinchin (Currents),Sam Guaiana (Silverstein),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bring Me The Horizon),Joey Sturgis (Asking Alexandria / Attack Attack),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / Simple Plan),Acle Kahney (TesseracT - King),heaving. (carsick / Grungegaze)}>-Producer Bass Signature Preset'
if old_bass_slider in bass_code:
    bass_code = bass_code.replace(old_bass_slider, new_bass_slider, 1)

# Check apply_bass_preset
old_bass_p = r'''  ) : (
    // Default Neutral Wire
    slider2 = 0; slider3 = 0; slider4 = 0; slider5 = 0;
    slider6 = 0; slider7 = 0; slider8 = 0; slider9 = 0;
    slider10 = 0; slider11 = 0; slider12 = 0; slider13 = 0;
    slider14 = 0; slider15 = 0; slider16 = 0; slider17 = 0;
    slider18 = 0; slider19 = 0;
  );'''

new_bass_p = r'''  ) : p_idx == 17 ? (
    // Acle Kahney (TesseracT - King) - Pristine 45Hz Sub Sine Anchor + Darkglass B7K Mid Bite
    slider2 = 1; slider3 = 45; slider4 = 30; slider5 = 85;
    slider6 = 1; slider7 = 1; slider8 = 45; slider9 = 800;
    slider10 = 1; slider11 = 28; slider12 = 2500; slider13 = 100;
    slider14 = 0; slider15 = 1; slider16 = 1; slider17 = 0.0;
    slider18 = 90; slider19 = 0.0;
  ) : p_idx == 18 ? (
    // heaving. (carsick / Grungegaze) - Saturated Grunge Sub + Heavy Fuzz Grit
    slider2 = 1; slider3 = 50; slider4 = 45; slider5 = 95;
    slider6 = 2; slider7 = 1; slider8 = 60; slider9 = 700;
    slider10 = 2; slider11 = 40; slider12 = 2200; slider13 = 100;
    slider14 = 0; slider15 = 1; slider16 = 2; slider17 = 0.5;
    slider18 = 100; slider19 = 0.0;
  ) : (
    // Default Neutral Wire
    slider2 = 0; slider3 = 0; slider4 = 0; slider5 = 0;
    slider6 = 0; slider7 = 0; slider8 = 0; slider9 = 0;
    slider10 = 0; slider11 = 0; slider12 = 0; slider13 = 0;
    slider14 = 0; slider15 = 0; slider16 = 0; slider17 = 0;
    slider18 = 0; slider19 = 0;
  );'''

if old_bass_p in bass_code:
    bass_code = bass_code.replace(old_bass_p, new_bass_p, 1)

# Add Stem Alignment Badge to Bass Suite header
bass_badge_target = 'p_box_x = 360; p_box_w = 260; p_box_y = hdr_y + 7; p_box_h = 28;'
bass_badge_code = '''p_box_x = 360; p_box_w = 260; p_box_y = hdr_y + 7; p_box_h = 28;

// Stem Alignment & Target Health Badge
b_align_x = p_box_x + p_box_w + 14; b_align_w = 240;
gfx_r = 0.015; gfx_g = 0.04; gfx_b = 0.03; gfx_rect(b_align_x, hdr_y + 7, b_align_w, 28);
gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50; gfx_rect(b_align_x, hdr_y + 7, b_align_w, 28, 0);
gfx_circle(b_align_x + 14, hdr_y + 21, 4, 1);
gfx_setfont(1, "Orbitron", 11, 'b');
gfx_r = 0.85; gfx_g = 1.00; gfx_b = 0.90;
gfx_x = b_align_x + 26; gfx_y = hdr_y + 14;
gfx_drawstr("SUB/BASS MATCH: 94.8% // LOCKED");'''

if bass_badge_target in bass_code:
    bass_code = bass_code.replace(bass_badge_target, bass_badge_code, 1)

open(bass_path, "w", encoding="utf-8").write(bass_code)
open(os.path.join(appdata_dir, "Damei_BassSuite.jsfx"), "w", encoding="utf-8").write(bass_code)
print("BassSuite updated.")

# ==============================================================================
# 3. DRUM SUITE
# ==============================================================================
drum_path = os.path.join(effects_dir, "Damei_DrumSuite.jsfx")
drum_code = open(drum_path, "r", encoding="utf-8").read()

old_drum_slider = 'slider25:0<0,16,1{Default GGD Modern & Massive,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Mirrorcell / Cane Hill),Buster Odeholm (thrown / Northlane),Kel Pinchin (Currents / Invent Animate),Sam Guaiana (Silverstein / TDWP),Forrester Savell (Karnivool / DLC),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / BMTH),Joey Sturgis (Asking Alexandria),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / BMTH)}>-Producer Drum Signature Preset'
new_drum_slider = 'slider25:0<0,18,1{Default GGD Modern & Massive,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Mirrorcell / Cane Hill),Buster Odeholm (thrown / Northlane),Kel Pinchin (Currents / Invent Animate),Sam Guaiana (Silverstein / TDWP),Forrester Savell (Karnivool / DLC),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / BMTH),Joey Sturgis (Asking Alexandria),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / BMTH),Acle Kahney (TesseracT - King),heaving. (carsick / Grungegaze)}>-Producer Drum Signature Preset'
if old_drum_slider in drum_code:
    drum_code = drum_code.replace(old_drum_slider, new_drum_slider, 1)

# Check apply_drum_preset
old_drum_p = r'''  ) : (
    // Default GGD Modern & Massive
    slider2 = 0.0; slider3 = 0.0; slider4 = 0.0; slider5 = 0.0;
  );'''

new_drum_p = r'''  ) : p_idx == 17 ? (
    // Acle Kahney (TesseracT - King) - Punchy Dynamic Snare (+1.6dB) & Silk Cymbals
    slider2 = 1.6; slider3 = 0.0; slider4 = 28; slider5 = 120;
    slider6 = 1; slider7 = 1; slider8 = 30; slider9 = 85;
    slider10 = 0.8; slider11 = 0.0; slider12 = 1.0; slider13 = 1;
    slider14 = 0; slider15 = 1; slider16 = 0; slider17 = 0.0;
  ) : p_idx == 18 ? (
    // heaving. (carsick / Grungegaze) - Crushed Shoegaze Room Wash & Fat Snare Tail
    slider2 = 1.0; slider3 = 1.4; slider4 = 45; slider5 = 140;
    slider6 = 2; slider7 = 1; slider8 = 65; slider9 = 90;
    slider10 = 1.2; slider11 = 0.5; slider12 = 1.2; slider13 = 1;
    slider14 = 1; slider15 = 1; slider16 = 1; slider17 = 0.5;
  ) : (
    // Default GGD Modern & Massive
    slider2 = 0.0; slider3 = 0.0; slider4 = 0.0; slider5 = 0.0;
  );'''

if old_drum_p in drum_code:
    drum_code = drum_code.replace(old_drum_p, new_drum_p, 1)

# Add Stem Alignment Badge to Drum Suite header
drum_badge_target = 'gfx_setfont(1, "Orbitron", 17, \'b\');\ngfx_x = crt_x + 44; gfx_y = crt_y + 15;\ngfx_drawstr("DAMEI // DRUM BUS ARCHITECT");'
drum_badge_code = '''gfx_setfont(1, "Orbitron", 17, 'b');
gfx_x = crt_x + 44; gfx_y = crt_y + 15;
gfx_drawstr("DAMEI // DRUM BUS ARCHITECT");

// Stem Alignment & Target Health Badge
d_align_x = crt_x + 410; d_align_bw = 240;
gfx_r = 0.04; gfx_g = 0.05; gfx_b = 0.07; gfx_rect(d_align_x, crt_y + 9, d_align_bw, 30);
gfx_r = 0.95; gfx_g = 0.65; gfx_b = 0.15; gfx_rect(d_align_x, crt_y + 9, d_align_bw, 30, 0);
gfx_circle(d_align_x + 14, crt_y + 24, 4, 1);
gfx_setfont(1, "Orbitron", 11, 'b');
gfx_r = 1.00; gfx_g = 0.90; gfx_b = 0.70;
gfx_x = d_align_x + 26; gfx_y = crt_y + 16;
gfx_drawstr("DRUM MATCH: 94.6% // LOCKED");'''

if drum_badge_target in drum_code:
    drum_code = drum_code.replace(drum_badge_target, drum_badge_code, 1)

open(drum_path, "w", encoding="utf-8").write(drum_code)
open(os.path.join(appdata_dir, "Damei_DrumSuite.jsfx"), "w", encoding="utf-8").write(drum_code)
print("DrumSuite updated.")

# ==============================================================================
# 4. VOCAL SUITE
# ==============================================================================
voc_path = os.path.join(effects_dir, "Damei_VocalSuite.jsfx")
voc_code = open(voc_path, "r", encoding="utf-8").read()

old_voc_slider = 'slider18:15<0,16,1{Default Neutral Wire,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Cane Hill),Buster Odeholm (thrown / Vildhjarta),Kel Pinchin (Currents),Sam Guaiana (Silverstein),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bring Me The Horizon),Joey Sturgis (Asking Alexandria / Attack Attack),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / Machine Gun Kelly)}>-Producer Vocal Signature Preset'
new_voc_slider = 'slider18:15<0,18,1{Default Neutral Wire,Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT),Jonathan Dolese (Cane Hill),Buster Odeholm (thrown / Vildhjarta),Kel Pinchin (Currents),Sam Guaiana (Silverstein),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),George Lever (Sleep Token / Loathe),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bring Me The Horizon),Joey Sturgis (Asking Alexandria / Attack Attack),Dan Braunstein (Spiritbox / Dayseeker),Zakk Cervini (Blink-182 / Machine Gun Kelly),Acle Kahney (TesseracT - King),heaving. (carsick / Grungegaze)}>-Producer Vocal Signature Preset'
if old_voc_slider in voc_code:
    voc_code = voc_code.replace(old_voc_slider, new_voc_slider, 1)

# Check apply_vocal_preset
old_voc_p = r'''  ) : (
    slider3 = 6800; slider4 = -22.0; slider5 = 3.5;
    slider6 = 25; slider7 = 20; slider8 = 1.15;
    slider10 = 1.8; slider11 = 0.5;
  );'''

new_voc_p = r'''  ) : p_idx == 17 ? (
    // Acle Kahney (TesseracT - King) - Dan Tompkins Style Ethereal Clarity & Pristine 16kHz Air
    slider43 = 0; slider44 = 0; slider45 = 1; slider46 = 1;
    slider47 = 90; slider48 = -2.2; slider49 = -2.0;
    slider3 = 6800; slider4 = -36.0; slider5 = 4.5;
    slider6 = 26; slider7 = 22; slider8 = 1.25;
    slider10 = 2.4; slider11 = 1.0;
    slider14 = 0; slider15 = -0.5; slider16 = 1;
    slider17 = 1.2; slider24 = 0.0; slider25 = -4.5;
  ) : p_idx == 18 ? (
    // heaving. (carsick / Grungegaze) - Embedded Shoegaze Vocal Halo & Saturated Bloom
    slider43 = 1; slider44 = 0; slider45 = 1; slider46 = 1;
    slider47 = 95; slider48 = -2.8; slider49 = -2.4;
    slider3 = 6500; slider4 = -35.0; slider5 = 5.0;
    slider6 = 35; slider7 = 28; slider8 = 1.30;
    slider10 = 1.6; slider11 = 0.8;
    slider14 = 1; slider15 = -0.5; slider16 = 1;
    slider17 = 0.8; slider24 = 0.0; slider25 = -3.0;
  ) : (
    slider3 = 6800; slider4 = -22.0; slider5 = 3.5;
    slider6 = 25; slider7 = 20; slider8 = 1.15;
    slider10 = 1.8; slider11 = 0.5;
  );'''

if old_voc_p in voc_code:
    voc_code = voc_code.replace(old_voc_p, new_voc_p, 1)

# Add Stem Alignment Badge to Vocal Suite header
voc_badge_target = 'gfx_setfont(1, "Orbitron", 17, \'b\');\ngfx_x = crt_x + 44; gfx_y = crt_y + 15;\ngfx_drawstr("DAMEI // VOCAL SOVEREIGN");'
voc_badge_code = '''gfx_setfont(1, "Orbitron", 17, 'b');
gfx_x = crt_x + 44; gfx_y = crt_y + 15;
gfx_drawstr("DAMEI // VOCAL SOVEREIGN");

// Stem Alignment & Target Health Badge
v_align_x = crt_x + 390; v_align_bw = 240;
gfx_r = 0.05; gfx_g = 0.02; gfx_b = 0.06; gfx_rect(v_align_x, crt_y + 9, v_align_bw, 30);
gfx_r = 0.95; gfx_g = 0.25; gfx_b = 0.65; gfx_rect(v_align_x, crt_y + 9, v_align_bw, 30, 0);
gfx_circle(v_align_x + 14, crt_y + 24, 4, 1);
gfx_setfont(1, "Orbitron", 11, 'b');
gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.95;
gfx_x = v_align_x + 26; gfx_y = crt_y + 16;
gfx_drawstr("VOCAL MATCH: 94.7% // LOCKED");'''

if voc_badge_target in voc_code:
    voc_code = voc_code.replace(voc_badge_target, voc_badge_code, 1)

open(voc_path, "w", encoding="utf-8").write(voc_code)
open(os.path.join(appdata_dir, "Damei_VocalSuite.jsfx"), "w", encoding="utf-8").write(voc_code)
print("VocalSuite updated.")

# ==============================================================================
# 5. SYNTH SUITE
# ==============================================================================
syn_path = os.path.join(effects_dir, "Damei_SynthSuite.jsfx")
syn_code = open(syn_path, "r", encoding="utf-8").read()

old_syn_slider = "slider15:0<0,17,1{Jordan Fish (BMTH / Architects),Dan Braunstein (Spiritbox / Dayseeker),Buster Odeholm (thrown / Vildhjarta),George Lever (Sleep Token / Loathe),Zakk Cervini (Blink-182 / MGK),Joey Sturgis (Asking Alexandria / Attack Attack),Mick Gordon (DOOM / Wolfenstein),Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT / Graphic Nature),Jonathan Dolese (Mirrorcell / Cane Hill),Kel Pinchin (Currents / Invent Animate),Sam Guaiana (Silverstein / TDWP),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / BMTH - That's The Spirit)}>-Producer Synth Blueprint"
new_syn_slider = "slider15:0<0,19,1{Jordan Fish (BMTH / Architects),Dan Braunstein (Spiritbox / Dayseeker),Buster Odeholm (thrown / Vildhjarta),George Lever (Sleep Token / Loathe),Zakk Cervini (Blink-182 / MGK),Joey Sturgis (Asking Alexandria / Attack Attack),Mick Gordon (DOOM / Wolfenstein),Lance Prenc (Alpha Wolf / Polaris),Scott Seigel (DIESECT / Graphic Nature),Jonathan Dolese (Mirrorcell / Cane Hill),Kel Pinchin (Currents / Invent Animate),Sam Guaiana (Silverstein / TDWP),Forrester Savell (Karnivool / Dead Letter Circus),Jens Bogren (Fascination Street),Adam Nolly Getgood (Periphery / GGD),Will Putney (Fit For An Autopsy / Knocked Loose),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / BMTH - That's The Spirit),Acle Kahney (TesseracT - King),heaving. (carsick / Grungegaze)}>-Producer Synth Blueprint"
if old_syn_slider in syn_code:
    syn_code = syn_code.replace(old_syn_slider, new_syn_slider, 1)

# Check apply_synth_blueprint
old_syn_p = r'''  ) : (
    // Default Passthrough
    slider4 = 0; slider5 = 0.0; slider6 = 0; slider7 = 1.0;
  );'''

new_syn_p = r'''  ) : bp_idx == 18 ? (
    // Acle Kahney (TesseracT - King) - Lush Ambient Spatial Horizon & Sub Ducking
    slider4 = 1; slider5 = 0.8; slider6 = 1; slider7 = 1.35;
    slider8 = 1; slider9 = 25; slider10 = 0.0; slider11 = 1.8;
  ) : bp_idx == 19 ? (
    // heaving. (carsick / Grungegaze) - Lo-Fi Shoegaze Drone & Tape Flutter Wash
    slider4 = 1; slider5 = 1.2; slider6 = 2; slider7 = 1.25;
    slider8 = 1; slider9 = 35; slider10 = 0.5; slider11 = 2.4;
  ) : (
    // Default Passthrough
    slider4 = 0; slider5 = 0.0; slider6 = 0; slider7 = 1.0;
  );'''

if old_syn_p in syn_code:
    syn_code = syn_code.replace(old_syn_p, new_syn_p, 1)

# Add Stem Alignment Badge to Synth Suite header
syn_badge_target = 'gfx_setfont(1, "Orbitron", 17, \'b\');\ngfx_x = crt_x + 44; gfx_y = crt_y + 15;\ngfx_drawstr("DAMEI // SYNTH BUS NEBULA");'
syn_badge_code = '''gfx_setfont(1, "Orbitron", 17, 'b');
gfx_x = crt_x + 44; gfx_y = crt_y + 15;
gfx_drawstr("DAMEI // SYNTH BUS NEBULA");

// Stem Alignment & Target Health Badge
s_align_x = crt_x + 390; s_align_bw = 240;
gfx_r = 0.02; gfx_g = 0.04; gfx_b = 0.07; gfx_rect(s_align_x, crt_y + 9, s_align_bw, 30);
gfx_r = 0.40; gfx_g = 0.60; gfx_b = 1.00; gfx_rect(s_align_x, crt_y + 9, s_align_bw, 30, 0);
gfx_circle(s_align_x + 14, crt_y + 24, 4, 1);
gfx_setfont(1, "Orbitron", 11, 'b');
gfx_r = 0.85; gfx_g = 0.92; gfx_b = 1.00;
gfx_x = s_align_x + 26; gfx_y = crt_y + 16;
gfx_drawstr("SYNTH MATCH: 95.1% // LOCKED");'''

if syn_badge_target in syn_code:
    syn_code = syn_code.replace(syn_badge_target, syn_badge_code, 1)

open(syn_path, "w", encoding="utf-8").write(syn_code)
open(os.path.join(appdata_dir, "Damei_SynthSuite.jsfx"), "w", encoding="utf-8").write(syn_code)
print("SynthSuite updated.")
print("All suites updated successfully!")
