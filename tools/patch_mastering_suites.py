import os, shutil

repo_effects = r"C:\Dev\DameiSuite\effects"
appdata_effects = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei"

# =============================================================================
# 1. PATCH Damei_OzoneSuite.jsfx
# =============================================================================
ozone_path = os.path.join(repo_effects, "Damei_OzoneSuite.jsfx")
with open(ozone_path, "r", encoding="utf-8", errors="ignore") as f:
    ozone_txt = f.read()

# Update slider33 range and list
old_s33 = "slider33:0<0,21,1{Default Modern Metal Clean (2026 Clarity & Punch),Lance Prenc (Alpha Wolf / Prenc Audio Master),Scott Seigel (DIESECT Full Production Master),Jonathan Dolese (Mirrorcell / Konkrete Studios Master),Buster Odeholm (thrown / Odeholm Audio Master),Grant Berry (blanket / Love Is Noise / Fader Mastering),Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master),Ted Jensen (Don Broco / Sterling Sound Master),Robin Schmidt (Static Dress / 24-96 Mastering),Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master),Nick Townsend (Heavenward / Townsend Mastering),Randy Merrill (City Of Souls / Sterling Sound Master),Leon Schmidt & Christian Donaldson (SUNBORN Master),Ermin Hamidovic (Systematic Mastering Guide Benchmark),Will Putney (Fit For An Autopsy / Knocked Loose signature),George Lever (Loathe / Sleep Token signature),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bleed From Within signature),Dan Braunstein (Spiritbox / Keep Sweet),Zakk Cervini & Erik Ron (Bad Omens),Jens Bogren (Fascination Street Master),Nolly (Periphery / GGD Systematic)}>-Mastering Engineer Signature Preset"
new_s33 = "slider33:0<0,23,1{Default Modern Metal Clean (2026 Clarity & Punch),Lance Prenc (Alpha Wolf / Prenc Audio Master),Scott Seigel (DIESECT Full Production Master),Jonathan Dolese (Mirrorcell / Konkrete Studios Master),Buster Odeholm (thrown / Odeholm Audio Master),Grant Berry (blanket / Love Is Noise / Fader Mastering),Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master),Ted Jensen (Don Broco / Sterling Sound Master),Robin Schmidt (Static Dress / 24-96 Mastering),Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master),Nick Townsend (Heavenward / Townsend Mastering),Randy Merrill (City Of Souls / Sterling Sound Master),Leon Schmidt & Christian Donaldson (SUNBORN Master),Ermin Hamidovic (Systematic Mastering Guide Benchmark),Will Putney (Fit For An Autopsy / Knocked Loose signature),George Lever (Loathe / Sleep Token signature),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bleed From Within signature),Dan Braunstein (Spiritbox / Keep Sweet),Zakk Cervini & Erik Ron (Bad Omens),Jens Bogren (Fascination Street Master),Nolly (Periphery / GGD Systematic),Acle Kahney (TesseracT - King),heaving. (carsick / Grungegaze)}>-Mastering Engineer Signature Preset"

assert old_s33 in ozone_txt, "slider33 not found in Damei_OzoneSuite.jsfx"
ozone_txt = ozone_txt.replace(old_s33, new_s33)

# Add p_idx 22 and 23 to apply_producer_master_preset
old_apply = """  ) : p_idx == 21 ? (
    // 21. Nolly - Adam Getgood (Periphery / GGD - Systematic/Ermin master reference)
    lim_ceil = -1.0; max_drive = 4.0; auto_norm = 1;
    clip_drive = 0.9; kclip_mode = 0; kclip_knee = 0.35; // Smooth Zero
    comp_thresh = -12.5; comp_ratio = 2.0; comp_attack = 30.0; comp_release = 0.0; comp_makeup = 0.6; sc_hpf_f = 125.0;
    imager_mono = 105.0; imager_wid = 1.20;
    eq_hp_f = 28.0; eq_b2_g = -1.6; eq_b3_g = 1.0; eq_b4_g = 1.6;
    slider43 = 3; slider44 = 1.0; slider45 = 0.4;
  ) : ("""

new_apply = """  ) : p_idx == 21 ? (
    // 21. Nolly - Adam Getgood (Periphery / GGD - Systematic/Ermin master reference)
    lim_ceil = -1.0; max_drive = 4.0; auto_norm = 1;
    clip_drive = 0.9; kclip_mode = 0; kclip_knee = 0.35; // Smooth Zero
    comp_thresh = -12.5; comp_ratio = 2.0; comp_attack = 30.0; comp_release = 0.0; comp_makeup = 0.6; sc_hpf_f = 125.0;
    imager_mono = 105.0; imager_wid = 1.20;
    eq_hp_f = 28.0; eq_b2_g = -1.6; eq_b3_g = 1.0; eq_b4_g = 1.6;
    slider43 = 3; slider44 = 1.0; slider45 = 0.4;
  ) : p_idx == 22 ? (
    // 22. Acle Kahney (TesseracT - King / Djent Master Reference)
    lim_ceil = -1.0; max_drive = 3.6; auto_norm = 1;
    clip_drive = 0.7; kclip_mode = 0; kclip_knee = 0.35; // Smooth Zero
    comp_thresh = -13.0; comp_ratio = 2.0; comp_attack = 30.0; comp_release = 0.0; comp_makeup = 0.5; sc_hpf_f = 125.0;
    imager_mono = 100.0; imager_wid = 1.18;
    eq_hp_f = 26.0; eq_b2_g = -2.0; eq_b3_g = 1.2; eq_b4_g = 1.4;
    slider43 = 3; slider44 = 1.2; slider45 = 0.8;
  ) : p_idx == 23 ? (
    // 23. heaving. (carsick / Heavy Grungegaze Master Reference)
    lim_ceil = -1.0; max_drive = 5.2; auto_norm = 1;
    clip_drive = 1.4; kclip_mode = 4; kclip_knee = 0.25; // Flatline 2 Hybrid
    comp_thresh = -11.0; comp_ratio = 3.0; comp_attack = 10.0; comp_release = 0.0; comp_makeup = 1.2; sc_hpf_f = 110.0;
    imager_mono = 110.0; imager_wid = 1.22;
    eq_hp_f = 30.0; eq_b2_g = -1.2; eq_b3_g = 1.6; eq_b4_g = 2.0;
    slider43 = 3; slider44 = 1.4; slider45 = 0.9;
  ) : ("""

assert old_apply in ozone_txt, "apply_producer_master_preset block not found in Damei_OzoneSuite.jsfx"
ozone_txt = ozone_txt.replace(old_apply, new_apply)

# Update p_title
old_ptitle = """p_title = (slider33==0  ? "DEFAULT 2026 (Clean CD)" :
          (slider33==1  ? "LANCE PRENC (Alpha Wolf)" :
          (slider33==2  ? "SCOTT SEIGEL (DIESECT)" :
          (slider33==3  ? "JONATHAN DOLESE (Mirrorcell)" :
          (slider33==4  ? "BUSTER ODEHOLM (thrown)" :
          (slider33==5  ? "GRANT BERRY (blanket/Fader)" :
          (slider33==6  ? "R. SCHMIDT / BERRY (Split)" :
          (slider33==7  ? "TED JENSEN (Don Broco)" :
          (slider33==8  ? "ROBIN SCHMIDT (Static Dress)" :
          (slider33==9  ? "MIKE KALAJIAN (Silverstein)" :
          (slider33==10 ? "NICK TOWNSEND (Heavenward)" :
          (slider33==11 ? "RANDY MERRILL (City Of Souls)" :
          (slider33==12 ? "C. DONALDSON / SCHMIDT" :
          (slider33==13 ? "ERMIN HAMIDOVIC SYSTEMATIC" :
          (slider33==14 ? "WILL PUTNEY (FFAA/Knocked Loose)" :
          (slider33==15 ? "GEORGE LEVER (Loathe)" :
          (slider33==16 ? "SAM BASSAL (Thornhill)" :
          (slider33==17 ? "HENRIK UDD (Architects)" :
          (slider33==18 ? "DAN BRAUNSTEIN (Spiritbox)" :
          (slider33==19 ? "CERVINI / RON (Bad Omens)" :
          (slider33==20 ? "JENS BOGREN (Fascination St.)" :
          "NOLLY (Periphery/GGD)")))))))))))))))))))));"""

new_ptitle = """p_title = (slider33==0  ? "DEFAULT 2026 (Clean CD)" :
          (slider33==1  ? "LANCE PRENC (Alpha Wolf)" :
          (slider33==2  ? "SCOTT SEIGEL (DIESECT)" :
          (slider33==3  ? "JONATHAN DOLESE (Mirrorcell)" :
          (slider33==4  ? "BUSTER ODEHOLM (thrown)" :
          (slider33==5  ? "GRANT BERRY (blanket/Fader)" :
          (slider33==6  ? "R. SCHMIDT / BERRY (Split)" :
          (slider33==7  ? "TED JENSEN (Don Broco)" :
          (slider33==8  ? "ROBIN SCHMIDT (Static Dress)" :
          (slider33==9  ? "MIKE KALAJIAN (Silverstein)" :
          (slider33==10 ? "NICK TOWNSEND (Heavenward)" :
          (slider33==11 ? "RANDY MERRILL (City Of Souls)" :
          (slider33==12 ? "C. DONALDSON / SCHMIDT" :
          (slider33==13 ? "ERMIN HAMIDOVIC SYSTEMATIC" :
          (slider33==14 ? "WILL PUTNEY (FFAA/Knocked Loose)" :
          (slider33==15 ? "GEORGE LEVER (Loathe)" :
          (slider33==16 ? "SAM BASSAL (Thornhill)" :
          (slider33==17 ? "HENRIK UDD (Architects)" :
          (slider33==18 ? "DAN BRAUNSTEIN (Spiritbox)" :
          (slider33==19 ? "CERVINI / RON (Bad Omens)" :
          (slider33==20 ? "JENS BOGREN (Fascination St.)" :
          (slider33==21 ? "NOLLY (Periphery/GGD)" :
          (slider33==22 ? "ACLE KAHNEY (TesseracT)" :
          "HEAVING. (carsick)")))))))))))))))))))))));"""

assert old_ptitle in ozone_txt, "p_title not found in Damei_OzoneSuite.jsfx"
ozone_txt = ozone_txt.replace(old_ptitle, new_ptitle)

# Update steppers and menu
ozone_txt = ozone_txt.replace(
    "slider33 = (slider33 - 1 + 22) % 22;",
    "slider33 = (slider33 - 1 + 24) % 24;"
)
ozone_txt = ozone_txt.replace(
    "slider33 = (slider33 + 1) % 22;",
    "slider33 = (slider33 + 1) % 24;"
)

old_menu_gen = 'menu_gen = gfx_showmenu("Default Modern Metal Clean (2026 Clarity & Punch)|Lance Prenc (Alpha Wolf / Prenc Audio Master)|Scott Seigel (DIESECT Full Production Master)|Jonathan Dolese (Mirrorcell / Konkrete Studios Master)|Buster Odeholm (thrown / Odeholm Audio Master)|Grant Berry (blanket / Love Is Noise / Fader Mastering)|Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master)|Ted Jensen (Don Broco / Sterling Sound Master)|Robin Schmidt (Static Dress / 24-96 Mastering)|Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master)|Nick Townsend (Heavenward / Townsend Mastering)|Randy Merrill (City Of Souls / Sterling Sound Master)|Leon Schmidt & Christian Donaldson (SUNBORN Master)|Ermin Hamidovic (Systematic Mastering Guide Benchmark)|Will Putney (Fit For An Autopsy / Knocked Loose signature)|George Lever (Loathe / Sleep Token signature)|Sam Bassal (Thornhill / Ocean Grove)|Henrik Udd (Architects / Bleed From Within signature)|Dan Braunstein (Spiritbox / Keep Sweet)|Zakk Cervini & Erik Ron (Bad Omens)|Jens Bogren (Fascination Street Master)|Nolly (Periphery / GGD Systematic)");'
new_menu_gen = 'menu_gen = gfx_showmenu("Default Modern Metal Clean (2026 Clarity & Punch)|Lance Prenc (Alpha Wolf / Prenc Audio Master)|Scott Seigel (DIESECT Full Production Master)|Jonathan Dolese (Mirrorcell / Konkrete Studios Master)|Buster Odeholm (thrown / Odeholm Audio Master)|Grant Berry (blanket / Love Is Noise / Fader Mastering)|Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master)|Ted Jensen (Don Broco / Sterling Sound Master)|Robin Schmidt (Static Dress / 24-96 Mastering)|Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master)|Nick Townsend (Heavenward / Townsend Mastering)|Randy Merrill (City Of Souls / Sterling Sound Master)|Leon Schmidt & Christian Donaldson (SUNBORN Master)|Ermin Hamidovic (Systematic Mastering Guide Benchmark)|Will Putney (Fit For An Autopsy / Knocked Loose signature)|George Lever (Loathe / Sleep Token signature)|Sam Bassal (Thornhill / Ocean Grove)|Henrik Udd (Architects / Bleed From Within signature)|Dan Braunstein (Spiritbox / Keep Sweet)|Zakk Cervini & Erik Ron (Bad Omens)|Jens Bogren (Fascination Street Master)|Nolly (Periphery / GGD Systematic)|Acle Kahney (TesseracT - King)|heaving. (carsick / Grungegaze)");'

assert old_menu_gen in ozone_txt, "menu_gen not found in Damei_OzoneSuite.jsfx"
ozone_txt = ozone_txt.replace(old_menu_gen, new_menu_gen)

# Update genre_lbl
old_genrelbl = """  genre_lbl = (slider33==0  ? "Default 2026 Metal" :
              (slider33==1  ? "Lance Prenc (Alpha Wolf)" :
              (slider33==2  ? "Scott Seigel (DIESECT)" :
              (slider33==3  ? "Jonathan Dolese" :
              (slider33==4  ? "Buster Odeholm (thrown)" :
              (slider33==5  ? "Grant Berry (Fader)" :
              (slider33==6  ? "R. Schmidt & G. Berry" :
              (slider33==7  ? "Ted Jensen (Don Broco)" :
              (slider33==8  ? "Robin Schmidt (24-96)" :
              (slider33==9  ? "Mike Kalajian (Rogue)" :
              (slider33==10 ? "Nick Townsend" :
              (slider33==11 ? "Randy Merrill (Sterling)" :
              (slider33==12 ? "Donaldson & Schmidt" :
              (slider33==13 ? "Ermin Hamidovic Systematic" :
              (slider33==14 ? "Will Putney (FFAA/Knocked Loose)" :
              (slider33==15 ? "George Lever (Loathe)" :
              (slider33==16 ? "Sam Bassal (Thornhill)" :
              (slider33==17 ? "Henrik Udd (Architects)" :
              (slider33==18 ? "Dan Braunstein (Spiritbox)" :
              (slider33==19 ? "Cervini & Ron (Bad Omens)" :
              (slider33==20 ? "Jens Bogren (Fascination St.)" :
              "Nolly (Periphery/GGD)")))))))))))))))))))));"""

new_genrelbl = """  genre_lbl = (slider33==0  ? "Default 2026 Metal" :
              (slider33==1  ? "Lance Prenc (Alpha Wolf)" :
              (slider33==2  ? "Scott Seigel (DIESECT)" :
              (slider33==3  ? "Jonathan Dolese" :
              (slider33==4  ? "Buster Odeholm (thrown)" :
              (slider33==5  ? "Grant Berry (Fader)" :
              (slider33==6  ? "R. Schmidt & G. Berry" :
              (slider33==7  ? "Ted Jensen (Don Broco)" :
              (slider33==8  ? "Robin Schmidt (24-96)" :
              (slider33==9  ? "Mike Kalajian (Rogue)" :
              (slider33==10 ? "Nick Townsend" :
              (slider33==11 ? "Randy Merrill (Sterling)" :
              (slider33==12 ? "Donaldson & Schmidt" :
              (slider33==13 ? "Ermin Hamidovic Systematic" :
              (slider33==14 ? "Will Putney (FFAA/Knocked Loose)" :
              (slider33==15 ? "George Lever (Loathe)" :
              (slider33==16 ? "Sam Bassal (Thornhill)" :
              (slider33==17 ? "Henrik Udd (Architects)" :
              (slider33==18 ? "Dan Braunstein (Spiritbox)" :
              (slider33==19 ? "Cervini & Ron (Bad Omens)" :
              (slider33==20 ? "Jens Bogren (Fascination St.)" :
              (slider33==21 ? "Nolly (Periphery/GGD)" :
              (slider33==22 ? "Acle Kahney (TesseracT)" :
              "heaving. (carsick)")))))))))))))))))))))));"""

assert old_genrelbl in ozone_txt, "genre_lbl not found in Damei_OzoneSuite.jsfx"
ozone_txt = ozone_txt.replace(old_genrelbl, new_genrelbl)

# Update sec_sauce
old_secsauce = """  sec_sauce = (slider33==0  ? "Pre-Limiter Clip Shaves Transients (-1.0dBTP Guard)" :
              (slider33==1  ? "Center Flatline (+1.4dB) Retains Snare Transient Crack" :
              (slider33==2  ? "320Hz De-Box (-2.6dB) Reclaims 2.4dB Limiter Headroom" :
              (slider33==3  ? "Tube Valve Saturation Tames Sibilance & Snare Crest" :
              (slider33==4  ? "Pre-Limiter Hard Clip (15% Knee) Stops Pumping" :
              (slider33==5  ? "Sub-Mono 95Hz Anchor Frees 1.18x Width Headroom" :
              (slider33==6  ? "105Hz Sub Anchor + 1.15x Stereo Panoramic Field" :
              (slider33==7  ? "Pultec Silk (+1.8dB 11k) Smoothes Digital Glare" :
              (slider33==8  ? "Analog Tape Mode 2 Rounds Off Square Wave Edges" :
              (slider33==9  ? "Dynamic Crest +1.3dB into Crisp Clipper Focus" :
              (slider33==10 ? "Lacquer Console Warmth + Gentle 110Hz HPF" :
              (slider33==11 ? "24Hz Infrasonic Filter Prevents False ISP Peaks" :
              (slider33==12 ? "Progressive Transient Lock + Tape Sheen" :
              (slider33==13 ? "Strict Mathematical Gain Staging Benchmark" :
              (slider33==14 ? "Crisp Clip + 320Hz Scoop Keeps Chugs Tight" :
              (slider33==15 ? "Wide Smooth-Zero Clip Preserves Dynamic Swell" :
              (slider33==16 ? "Flatline Clip + 1.18x Width For Modern Air" :
              (slider33==17 ? "Flatline Clip + 125Hz Guard For Dense Layers" :
              (slider33==18 ? "Tape Warmth + 11k Silk Keeps Vocals Forward" :
              (slider33==19 ? "Tube Valve Drive Adds Weight Under Pop Hooks" :
              (slider33==20 ? "Gentle Zero-Clip + 24Hz HPF Preserves Headroom" :
              "Smooth Zero Clip + 1.20x Width Clean Benchmark")))))))))))))))))))));"""

new_secsauce = """  sec_sauce = (slider33==0  ? "Pre-Limiter Clip Shaves Transients (-1.0dBTP Guard)" :
              (slider33==1  ? "Center Flatline (+1.4dB) Retains Snare Transient Crack" :
              (slider33==2  ? "320Hz De-Box (-2.6dB) Reclaims 2.4dB Limiter Headroom" :
              (slider33==3  ? "Tube Valve Saturation Tames Sibilance & Snare Crest" :
              (slider33==4  ? "Pre-Limiter Hard Clip (15% Knee) Stops Pumping" :
              (slider33==5  ? "Sub-Mono 95Hz Anchor Frees 1.18x Width Headroom" :
              (slider33==6  ? "105Hz Sub Anchor + 1.15x Stereo Panoramic Field" :
              (slider33==7  ? "Pultec Silk (+1.8dB 11k) Smoothes Digital Glare" :
              (slider33==8  ? "Analog Tape Mode 2 Rounds Off Square Wave Edges" :
              (slider33==9  ? "Dynamic Crest +1.3dB into Crisp Clipper Focus" :
              (slider33==10 ? "Lacquer Console Warmth + Gentle 110Hz HPF" :
              (slider33==11 ? "24Hz Infrasonic Filter Prevents False ISP Peaks" :
              (slider33==12 ? "Progressive Transient Lock + Tape Sheen" :
              (slider33==13 ? "Strict Mathematical Gain Staging Benchmark" :
              (slider33==14 ? "Crisp Clip + 320Hz Scoop Keeps Chugs Tight" :
              (slider33==15 ? "Wide Smooth-Zero Clip Preserves Dynamic Swell" :
              (slider33==16 ? "Flatline Clip + 1.18x Width For Modern Air" :
              (slider33==17 ? "Flatline Clip + 125Hz Guard For Dense Layers" :
              (slider33==18 ? "Tape Warmth + 11k Silk Keeps Vocals Forward" :
              (slider33==19 ? "Tube Valve Drive Adds Weight Under Pop Hooks" :
              (slider33==20 ? "Gentle Zero-Clip + 24Hz HPF Preserves Headroom" :
              (slider33==21 ? "Smooth Zero Clip + 1.20x Width Clean Benchmark" :
              (slider33==22 ? "Djent Transient Precision + 26Hz Sub Anchor & 1.18x Width" :
              "Flatline 2 Wall-of-Sound Saturation + 1.22x Grungegaze Field")))))))))))))))))))))));"""

assert old_secsauce in ozone_txt, "sec_sauce not found in Damei_OzoneSuite.jsfx"
ozone_txt = ozone_txt.replace(old_secsauce, new_secsauce)

with open(ozone_path, "w", encoding="utf-8") as f:
    f.write(ozone_txt)
print("Updated Damei_OzoneSuite.jsfx in repo")

# =============================================================================
# 2. PATCH Damei_GullfossMaster.jsfx
# =============================================================================
gf_path = os.path.join(repo_effects, "Damei_GullfossMaster.jsfx")
with open(gf_path, "r", encoding="utf-8", errors="ignore") as f:
    gf_txt = f.read()

old_gf_s12 = "slider12:6<0,21,1{Default Modern Metal Clean (2026 Clarity & Punch),Lance Prenc (Alpha Wolf / Prenc Audio Master),Scott Seigel (DIESECT Full Production Master),Jonathan Dolese (Mirrorcell / Konkrete Studios Master),Buster Odeholm (thrown / Odeholm Audio Master),Grant Berry (blanket / Love Is Noise / Fader Mastering),Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master),Ted Jensen (Don Broco / Sterling Sound Master),Robin Schmidt (Static Dress / 24-96 Mastering),Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master),Nick Townsend (Heavenward / Townsend Mastering),Randy Merrill (City Of Souls / Sterling Sound Master),Leon Schmidt & Christian Donaldson (SUNBORN Master),Ermin Hamidovic (Systematic Mastering Guide Benchmark),Will Putney (Fit For An Autopsy / Knocked Loose signature),George Lever (Loathe / Sleep Token signature),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bleed From Within signature),Dan Braunstein (Spiritbox / Keep Sweet),Zakk Cervini & Erik Ron (Bad Omens),Jens Bogren (Fascination Street Master),Nolly (Periphery / GGD Systematic)}>-Mastering Engineer Signature Preset"
new_gf_s12 = "slider12:6<0,23,1{Default Modern Metal Clean (2026 Clarity & Punch),Lance Prenc (Alpha Wolf / Prenc Audio Master),Scott Seigel (DIESECT Full Production Master),Jonathan Dolese (Mirrorcell / Konkrete Studios Master),Buster Odeholm (thrown / Odeholm Audio Master),Grant Berry (blanket / Love Is Noise / Fader Mastering),Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master),Ted Jensen (Don Broco / Sterling Sound Master),Robin Schmidt (Static Dress / 24-96 Mastering),Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master),Nick Townsend (Heavenward / Townsend Mastering),Randy Merrill (City Of Souls / Sterling Sound Master),Leon Schmidt & Christian Donaldson (SUNBORN Master),Ermin Hamidovic (Systematic Mastering Guide Benchmark),Will Putney (Fit For An Autopsy / Knocked Loose signature),George Lever (Loathe / Sleep Token signature),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bleed From Within signature),Dan Braunstein (Spiritbox / Keep Sweet),Zakk Cervini & Erik Ron (Bad Omens),Jens Bogren (Fascination Street Master),Nolly (Periphery / GGD Systematic),Acle Kahney (TesseracT - King),heaving. (carsick / Grungegaze)}>-Mastering Engineer Signature Preset"

assert old_gf_s12 in gf_txt, "slider12 not found in Damei_GullfossMaster.jsfx"
gf_txt = gf_txt.replace(old_gf_s12, new_gf_s12)

old_gf_names = """  p_idx == 20 ? "Jens Bogren (Fascination St.)" :
  "Nolly (Periphery / GGD)";"""

new_gf_names = """  p_idx == 20 ? "Jens Bogren (Fascination St.)" :
  p_idx == 21 ? "Nolly (Periphery / GGD)" :
  p_idx == 22 ? "Acle Kahney (TesseracT)" :
  "heaving. (carsick)";"""

assert old_gf_names in gf_txt, "engineer names not found in Damei_GullfossMaster.jsfx"
gf_txt = gf_txt.replace(old_gf_names, new_gf_names)

old_gf_apply = """  ) : p_idx == 21 ? ( // Nolly (Periphery / GGD)
    slider2 = 28; slider3 = 34; slider4 = 0; slider5 = 12; slider6 = 8; slider7 = 75; slider8 = 18500; slider9 = 60;
  ) : ( // Default Modern Metal Clean"""

new_gf_apply = """  ) : p_idx == 21 ? ( // Nolly (Periphery / GGD)
    slider2 = 28; slider3 = 34; slider4 = 0; slider5 = 12; slider6 = 8; slider7 = 75; slider8 = 18500; slider9 = 60;
  ) : p_idx == 22 ? ( // Acle Kahney (TesseracT - King)
    slider2 = 30; slider3 = 32; slider4 = -2; slider5 = 14; slider6 = 12; slider7 = 75; slider8 = 19000; slider9 = 62;
  ) : p_idx == 23 ? ( // heaving. (carsick / Grungegaze)
    slider2 = 36; slider3 = 28; slider4 = 10; slider5 = 18; slider6 = 15; slider7 = 70; slider8 = 19500; slider9 = 56;
  ) : ( // Default Modern Metal Clean"""

assert old_gf_apply in gf_txt, "apply_gullfoss_master_preset block not found in Damei_GullfossMaster.jsfx"
gf_txt = gf_txt.replace(old_gf_apply, new_gf_apply)

gf_txt = gf_txt.replace("slider12 = (slider12 - 1 + 22) % 22;", "slider12 = (slider12 - 1 + 24) % 24;")
gf_txt = gf_txt.replace("slider12 = (slider12 + 1) % 22;", "slider12 = (slider12 + 1) % 24;")

old_gf_menu = 'm_choice = gfx_showmenu("0: Default Modern Metal Clean (2026 Clarity & Punch)|1: Lance Prenc (Alpha Wolf / Prenc Audio Master)|2: Scott Seigel (DIESECT Full Production Master)|3: Jonathan Dolese (Mirrorcell / Konkrete Studios Master)|4: Buster Odeholm (thrown / Odeholm Audio Master)|5: Grant Berry (blanket / Love Is Noise / Fader Mastering)|6: Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master)|7: Ted Jensen (Don Broco / Sterling Sound Master)|8: Robin Schmidt (Static Dress / 24-96 Mastering)|9: Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master)|10: Nick Townsend (Heavenward / Townsend Mastering)|11: Randy Merrill (City Of Souls / Sterling Sound Master)|12: Leon Schmidt & Christian Donaldson (SUNBORN Master)|13: Ermin Hamidovic (Systematic Mastering Guide Benchmark)|14: Will Putney (Fit For An Autopsy / Knocked Loose signature)|15: George Lever (Loathe / Sleep Token signature)|16: Sam Bassal (Thornhill / Ocean Grove)|17: Henrik Udd (Architects / Bleed From Within signature)|18: Dan Braunstein (Spiritbox / Keep Sweet)|19: Zakk Cervini & Erik Ron (Bad Omens)|20: Jens Bogren (Fascination Street Master)|21: Nolly (Periphery / GGD Systematic)");'
new_gf_menu = 'm_choice = gfx_showmenu("0: Default Modern Metal Clean (2026 Clarity & Punch)|1: Lance Prenc (Alpha Wolf / Prenc Audio Master)|2: Scott Seigel (DIESECT Full Production Master)|3: Jonathan Dolese (Mirrorcell / Konkrete Studios Master)|4: Buster Odeholm (thrown / Odeholm Audio Master)|5: Grant Berry (blanket / Love Is Noise / Fader Mastering)|6: Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master)|7: Ted Jensen (Don Broco / Sterling Sound Master)|8: Robin Schmidt (Static Dress / 24-96 Mastering)|9: Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master)|10: Nick Townsend (Heavenward / Townsend Mastering)|11: Randy Merrill (City Of Souls / Sterling Sound Master)|12: Leon Schmidt & Christian Donaldson (SUNBORN Master)|13: Ermin Hamidovic (Systematic Mastering Guide Benchmark)|14: Will Putney (Fit For An Autopsy / Knocked Loose signature)|15: George Lever (Loathe / Sleep Token signature)|16: Sam Bassal (Thornhill / Ocean Grove)|17: Henrik Udd (Architects / Bleed From Within signature)|18: Dan Braunstein (Spiritbox / Keep Sweet)|19: Zakk Cervini & Erik Ron (Bad Omens)|20: Jens Bogren (Fascination Street Master)|21: Nolly (Periphery / GGD Systematic)|22: Acle Kahney (TesseracT - King)|23: heaving. (carsick / Grungegaze)");'

assert old_gf_menu in gf_txt, "m_choice menu not found in Damei_GullfossMaster.jsfx"
gf_txt = gf_txt.replace(old_gf_menu, new_gf_menu)

with open(gf_path, "w", encoding="utf-8") as f:
    f.write(gf_txt)
print("Updated Damei_GullfossMaster.jsfx in repo")

# =============================================================================
# 3. PATCH Damei_ToneShaper.jsfx
# =============================================================================
ts_path = os.path.join(repo_effects, "Damei_ToneShaper.jsfx")
with open(ts_path, "r", encoding="utf-8", errors="ignore") as f:
    ts_txt = f.read()

old_ts_s7 = "slider7:6<0,21,1{Default Modern Metal Clean (2026 Clarity & Punch),Lance Prenc (Alpha Wolf / Prenc Audio Master),Scott Seigel (DIESECT Full Production Master),Jonathan Dolese (Mirrorcell / Konkrete Studios Master),Buster Odeholm (thrown / Odeholm Audio Master),Grant Berry (blanket / Love Is Noise / Fader Mastering),Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master),Ted Jensen (Don Broco / Sterling Sound Master),Robin Schmidt (Static Dress / 24-96 Mastering),Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master),Nick Townsend (Heavenward / Townsend Mastering),Randy Merrill (City Of Souls / Sterling Sound Master),Leon Schmidt & Christian Donaldson (SUNBORN Master),Ermin Hamidovic (Systematic Mastering Guide Benchmark),Will Putney (Fit For An Autopsy / Knocked Loose signature),George Lever (Loathe / Sleep Token signature),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bleed From Within signature),Dan Braunstein (Spiritbox / Keep Sweet),Zakk Cervini & Erik Ron (Bad Omens),Jens Bogren (Fascination Street Master),Nolly (Periphery / GGD Systematic)}>-Mastering Engineer Signature Preset"
new_ts_s7 = "slider7:6<0,23,1{Default Modern Metal Clean (2026 Clarity & Punch),Lance Prenc (Alpha Wolf / Prenc Audio Master),Scott Seigel (DIESECT Full Production Master),Jonathan Dolese (Mirrorcell / Konkrete Studios Master),Buster Odeholm (thrown / Odeholm Audio Master),Grant Berry (blanket / Love Is Noise / Fader Mastering),Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master),Ted Jensen (Don Broco / Sterling Sound Master),Robin Schmidt (Static Dress / 24-96 Mastering),Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master),Nick Townsend (Heavenward / Townsend Mastering),Randy Merrill (City Of Souls / Sterling Sound Master),Leon Schmidt & Christian Donaldson (SUNBORN Master),Ermin Hamidovic (Systematic Mastering Guide Benchmark),Will Putney (Fit For An Autopsy / Knocked Loose signature),George Lever (Loathe / Sleep Token signature),Sam Bassal (Thornhill / Ocean Grove),Henrik Udd (Architects / Bleed From Within signature),Dan Braunstein (Spiritbox / Keep Sweet),Zakk Cervini & Erik Ron (Bad Omens),Jens Bogren (Fascination Street Master),Nolly (Periphery / GGD Systematic),Acle Kahney (TesseracT - King),heaving. (carsick / Grungegaze)}>-Mastering Engineer Signature Preset"

assert old_ts_s7 in ts_txt, "slider7 not found in Damei_ToneShaper.jsfx"
ts_txt = ts_txt.replace(old_ts_s7, new_ts_s7)

old_ts_names = """  p_idx == 20 ? "Jens Bogren (Fascination St.)" :
  "Nolly (Periphery / GGD)";"""

new_ts_names = """  p_idx == 20 ? "Jens Bogren (Fascination St.)" :
  p_idx == 21 ? "Nolly (Periphery / GGD)" :
  p_idx == 22 ? "Acle Kahney (TesseracT)" :
  "heaving. (carsick)";"""

assert old_ts_names in ts_txt, "ts engineer names not found in Damei_ToneShaper.jsfx"
ts_txt = ts_txt.replace(old_ts_names, new_ts_names)

old_ts_apply = """  ) : p_idx == 21 ? ( // Nolly (Periphery / GGD): systematic definition & surgical body
    slider2 = 2.2; slider3 = -1.0; slider4 = 0.0; slider5 = 0;
  ) : ( // Default Modern Metal Clean"""

new_ts_apply = """  ) : p_idx == 21 ? ( // Nolly (Periphery / GGD): systematic definition & surgical body
    slider2 = 2.2; slider3 = -1.0; slider4 = 0.0; slider5 = 0;
  ) : p_idx == 22 ? ( // Acle Kahney (TesseracT - King): clean precision, scooped body, ultra clear
    slider2 = 2.5; slider3 = -1.5; slider4 = 0.1; slider5 = 0;
  ) : p_idx == 23 ? ( // heaving. (carsick / Grungegaze): intense tone tilt, thick body, transformer glue
    slider2 = 2.8; slider3 = 1.2; slider4 = 0.3; slider5 = 1;
  ) : ( // Default Modern Metal Clean"""

assert old_ts_apply in ts_txt, "apply_toneshaper_master_preset block not found in Damei_ToneShaper.jsfx"
ts_txt = ts_txt.replace(old_ts_apply, new_ts_apply)

ts_txt = ts_txt.replace("slider7 = (slider7 - 1 + 22) % 22;", "slider7 = (slider7 - 1 + 24) % 24;")
ts_txt = ts_txt.replace("slider7 = (slider7 + 1) % 22;", "slider7 = (slider7 + 1) % 24;")

old_ts_menu = 'ts_choice = gfx_showmenu("0: Default Modern Metal Clean (2026 Clarity & Punch)|1: Lance Prenc (Alpha Wolf / Prenc Audio Master)|2: Scott Seigel (DIESECT Full Production Master)|3: Jonathan Dolese (Mirrorcell / Konkrete Studios Master)|4: Buster Odeholm (thrown / Odeholm Audio Master)|5: Grant Berry (blanket / Love Is Noise / Fader Mastering)|6: Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master)|7: Ted Jensen (Don Broco / Sterling Sound Master)|8: Robin Schmidt (Static Dress / 24-96 Mastering)|9: Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master)|10: Nick Townsend (Heavenward / Townsend Mastering)|11: Randy Merrill (City Of Souls / Sterling Sound Master)|12: Leon Schmidt & Christian Donaldson (SUNBORN Master)|13: Ermin Hamidovic (Systematic Mastering Guide Benchmark)|14: Will Putney (Fit For An Autopsy / Knocked Loose signature)|15: George Lever (Loathe / Sleep Token signature)|16: Sam Bassal (Thornhill / Ocean Grove)|17: Henrik Udd (Architects / Bleed From Within signature)|18: Dan Braunstein (Spiritbox / Keep Sweet)|19: Zakk Cervini & Erik Ron (Bad Omens)|20: Jens Bogren (Fascination Street Master)|21: Nolly (Periphery / GGD Systematic)");'
new_ts_menu = 'ts_choice = gfx_showmenu("0: Default Modern Metal Clean (2026 Clarity & Punch)|1: Lance Prenc (Alpha Wolf / Prenc Audio Master)|2: Scott Seigel (DIESECT Full Production Master)|3: Jonathan Dolese (Mirrorcell / Konkrete Studios Master)|4: Buster Odeholm (thrown / Odeholm Audio Master)|5: Grant Berry (blanket / Love Is Noise / Fader Mastering)|6: Robin Schmidt & Grant Berry (Split Chain / UK Grunge Master)|7: Ted Jensen (Don Broco / Sterling Sound Master)|8: Robin Schmidt (Static Dress / 24-96 Mastering)|9: Mike Kalajian (Silverstein / Shyeye / Rogue Planet Master)|10: Nick Townsend (Heavenward / Townsend Mastering)|11: Randy Merrill (City Of Souls / Sterling Sound Master)|12: Leon Schmidt & Christian Donaldson (SUNBORN Master)|13: Ermin Hamidovic (Systematic Mastering Guide Benchmark)|14: Will Putney (Fit For An Autopsy / Knocked Loose signature)|15: George Lever (Loathe / Sleep Token signature)|16: Sam Bassal (Thornhill / Ocean Grove)|17: Henrik Udd (Architects / Bleed From Within signature)|18: Dan Braunstein (Spiritbox / Keep Sweet)|19: Zakk Cervini & Erik Ron (Bad Omens)|20: Jens Bogren (Fascination Street Master)|21: Nolly (Periphery / GGD Systematic)|22: Acle Kahney (TesseracT - King)|23: heaving. (carsick / Grungegaze)");'

assert old_ts_menu in ts_txt, "ts_choice menu not found in Damei_ToneShaper.jsfx"
ts_txt = ts_txt.replace(old_ts_menu, new_ts_menu)

with open(ts_path, "w", encoding="utf-8") as f:
    f.write(ts_txt)
print("Updated Damei_ToneShaper.jsfx in repo")

# Synchronize to AppData
for fname in ["Damei_OzoneSuite.jsfx", "Damei_GullfossMaster.jsfx", "Damei_ToneShaper.jsfx"]:
    src = os.path.join(repo_effects, fname)
    dst = os.path.join(appdata_effects, fname)
    shutil.copy2(src, dst)
    print(f"Synchronized {fname} to {dst}")
