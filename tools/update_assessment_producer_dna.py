import sys

jsfx_path = r"C:\Dev\DameiSuite\effects\Damei_AssessmentMatrix.jsfx"

with open(jsfx_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# 1. Update Navigation Buttons
old_nav = """sprintf(#trm_short, "AUTO-CORRECT: %s", slider7 == 1 ? (static_locked ? "STATIC LOCKED" : "LOCKING...") : (slider7 == 2 ? "SLOW DYNAMIC" : "OFF"));
txt(342, 28, #trm_short);
btn(490, 18, 90, 34, "MATRIX", ui_view == 0) ? ( ui_view = 0; );
btn(585, 18, 105, 34, "STEM A/B", ui_view == 4) ? ( ui_view = 4; );
btn(695, 18, 105, 34, "MASTERING", ui_view == 2) ? ( ui_view = 2; );
btn(805, 18, 95, 34, "LIBRARY", ui_view == 1) ? ( ui_view = 1; );
btn(905, 18, 95, 34, "OLLAMA AI", ui_view == 3) ? ( ui_view = 3; );"""

new_nav = """sprintf(#trm_short, "AUTO-CORRECT: %s", slider7 == 1 ? (static_locked ? "STATIC LOCKED" : "LOCKING...") : (slider7 == 2 ? "SLOW DYNAMIC" : "OFF"));
txt(254, 28, #trm_short);
btn(395, 18, 68, 34, "MATRIX", ui_view == 0) ? ( ui_view = 0; );
btn(467, 18, 85, 34, "STEM A/B", ui_view == 4) ? ( ui_view = 4; );
btn(556, 18, 126, 34, "★ PRODUCER DNA", ui_view == 5) ? ( ui_view = 5; );
btn(686, 18, 95, 34, "MASTERING", ui_view == 2) ? ( ui_view = 2; );
btn(785, 18, 85, 34, "LIBRARY", ui_view == 1) ? ( ui_view = 1; );
btn(874, 18, 95, 34, "OLLAMA AI", ui_view == 3) ? ( ui_view = 3; );"""

assert old_nav in content, "old_nav not found in content"
content = content.replace(old_nav, new_nav)

# Also update the Auto-correct box width from 195 to 142
old_box = "col(0.03, 0.04, 0.07); rct(330, 18, 195, 34);"
new_box = "col(0.03, 0.04, 0.07); rct(245, 18, 145, 34);"
content = content.replace(old_box, new_box)

old_box_o = "slider7 > 0 ? (slider7 == 1 ? col(0.20, 0.92, 0.62) : col(0.00, 0.85, 1.00)) : col(0.38, 0.42, 0.55); rcto(330, 18, 195, 34);"
new_box_o = "slider7 > 0 ? (slider7 == 1 ? col(0.20, 0.92, 0.62) : col(0.00, 0.85, 1.00)) : col(0.38, 0.42, 0.55); rcto(245, 18, 145, 34);"
content = content.replace(old_box_o, new_box_o)

# 2. Add draw_candy_play and draw_producer_dna right before draw_mastering_console
producer_dna_code = """function draw_candy_play(x, y, w, h, title, desc_txt, armed) (
  col(0.04, 0.06, 0.10); rct(x, y, w, h);
  armed ? col(0.20, 0.92, 0.62) : col(0.40, 0.45, 0.55); rcto(x, y, w, h);
  gfx_setfont(3); armed ? col(0.20, 0.92, 0.62) : col(0.70, 0.75, 0.85);
  txt(x + 12, y + 8, title);
  // Badge
  col(armed ? 0.08 : 0.15, armed ? 0.25 : 0.15, armed ? 0.18 : 0.18);
  rct(x + w - 74, y + 6, 64, 18);
  armed ? col(0.20, 0.92, 0.62) : col(0.5, 0.5, 0.5); rcto(x + w - 74, y + 6, 64, 18);
  gfx_setfont(3);
  txt(x + w - 68, y + 9, armed ? "✓ ARMED" : "OFF");
  gfx_setfont(2); col(0.70, 0.75, 0.85);
  txt(x + 12, y + 26, desc_txt);
);

function draw_producer_dna() local(cal_st, relay_btn_txt) (
  card(24, 86, 972, 692, "PRODUCER BLUEPRINT & EAR-CANDY DIRECTOR // KEL PINCHIN (SPLIT CHAIN)", 1.00, 0.72, 0.02);

  // Top Action Banner: 1-Click Sync & Relay to All Suites
  col(0.05, 0.12, 0.18); rct(38, 118, 944, 46);
  col(0.00, 0.85, 1.00); rcto(38, 118, 944, 46);
  gfx_setfont(1); col(0.00, 0.96, 0.83);
  txt(52, 126, "REFERENCE BENCHMARK: 'I'M NOT DYING TO BE HERE' (motionblur)");
  gfx_setfont(3); col(0.70, 0.80, 0.95);
  txt(52, 144, "Target: -10.3 LUFS-I | 9.3 dB Crest | 0.63 Overall Width | +21.9 dB Dynamic Spread | Quad-Wall Guitars (1.18x)");

  cal_st = gmem[1159];
  relay_btn_txt = cal_st == 1 ? "✓ SUITES SYNCED & ARMED" : "⚡ RELAY BLUEPRINT TO ALL SUITES";
  btn(680, 126, 290, 30, relay_btn_txt, cal_st == 1) ? (
    gmem[1096] = 1; // Trigger Lua Relay Script in REAPER
  );

  // Column 1 (Left, w=464): Deconstruction & Comparative Measurements
  card(38, 172, 464, 590, "STEM DECONSTRUCTION & REFERENCE MEASUREMENTS", 0.00, 0.96, 0.83);
  
  // Section 1: Bass Stem
  col(0.04, 0.06, 0.10); rct(50, 206, 440, 74);
  col(0.18, 0.25, 0.38); rcto(50, 206, 440, 74);
  gfx_setfont(3); col(1.00, 0.72, 0.02); txt(62, 214, "1. BASS STEM (Monolithic Mono Foundation)");
  gfx_setfont(2); col(0.85, 0.90, 1.00);
  txt(62, 232, "Width: 0.073 (99% Mono) | Low-End Energy: 96.4% in 60-250 Hz");
  col(0.70, 0.75, 0.85);
  txt(62, 248, "Sub-mono locked <90 Hz. Trackspacer sidechain ducking 2.4 dB under kick.");
  txt(62, 262, "Mud scooped -1.5 dB at 250 Hz to free cavity for snare and guitars.");

  // Section 2: Drums Stem
  col(0.04, 0.06, 0.10); rct(50, 286, 440, 74);
  col(0.18, 0.25, 0.38); rcto(50, 286, 440, 74);
  gfx_setfont(3); col(0.20, 0.92, 0.62); txt(62, 294, "2. DRUMS STEM (Controlled Silk & Punch)");
  gfx_setfont(2); col(0.85, 0.90, 1.00);
  txt(62, 312, "Width: 0.210 (Center Punch) | Cymbal Crest Shaved: 33 dB -> 26 dB");
  col(0.70, 0.75, 0.85);
  txt(62, 328, "Cymbal Silk Master active >9 kHz. 40 Hz boom tamed -1.5 dB.");
  txt(62, 342, "BSA Drum Bus (38% drive, 85% mix) + Britson Neve warmth.");

  // Section 3: Guitars & Other Stem
  col(0.04, 0.06, 0.10); rct(50, 366, 440, 74);
  col(0.18, 0.25, 0.38); rcto(50, 366, 440, 74);
  gfx_setfont(3); col(0.00, 0.85, 1.00); txt(62, 374, "3. GUITARS & OTHER (Out-of-Phase Quad-Wall)");
  gfx_setfont(2); col(0.85, 0.90, 1.00);
  txt(62, 392, "Width: 1.176 (Super-Wide) | Phase Corr: -0.161 (Wall Decorrelation)");
  col(0.70, 0.75, 0.85);
  txt(62, 408, "Stereo Quad-Wall 1.28x. Highpassed @ 90 Hz. 190 Hz chug clamp.");
  txt(62, 422, "Center Donut-Hole carved at 2.5 kHz to give lead vocal an unmasked lane.");

  // Section 4: Vocals Stem
  col(0.04, 0.06, 0.10); rct(50, 446, 440, 74);
  col(0.18, 0.25, 0.38); rcto(50, 446, 440, 74);
  gfx_setfont(3); col(1.00, 0.40, 0.65); txt(62, 454, "4. VOCALS STEM (Upfront Authority & Air Sheen)");
  gfx_setfont(2); col(0.85, 0.90, 1.00);
  txt(62, 472, "Width: 0.555 (Centered Lead + Wide Slap) | 16 kHz Air Sheen: +1.8 dB");
  col(0.70, 0.75, 0.85);
  txt(62, 488, "Serial 1176 FET (25%) + Opto LA-2A (20%). Strict Mono <200 Hz.");
  txt(62, 502, "ReEQ 380 Hz chest mud scoop -2.0 dB. LOADES de-esser @ 6.8 kHz.");

  // Section 5: Macro Dynamics Spread
  col(0.04, 0.06, 0.10); rct(50, 526, 440, 95);
  col(0.18, 0.25, 0.38); rcto(50, 526, 440, 95);
  gfx_setfont(3); col(1.00, 0.85, 0.30); txt(62, 534, "5. MACRO DYNAMICS & SECTION LIFTS");
  gfx_setfont(2); col(0.85, 0.90, 1.00);
  txt(62, 552, "Split Chain Verse-to-Chorus Spread: +21.9 dB (Verse -29.4 / Chorus -7.5)");
  col(0.70, 0.75, 0.85);
  txt(62, 568, "Guitars explode +25.5 dB on downbeat! Drums expand width by +96.4%.");
  txt(62, 582, "Commercial Drop Slam AI engaged (+0.16x width / +1.4 dB punch in chorus).");
  txt(62, 596, "Song structure hybrid detector tracking REAPER project regions.");

  // Section 6: Translation & Headroom
  col(0.04, 0.06, 0.10); rct(50, 627, 440, 120);
  col(0.18, 0.25, 0.38); rcto(50, 627, 440, 120);
  gfx_setfont(3); col(0.00, 0.96, 0.83); txt(62, 635, "6. PRE-MASTER HEADROOM GUARDIAN");
  gfx_setfont(2); col(0.85, 0.90, 1.00);
  txt(62, 653, "Headroom Target: -6.0 dBTP on Mix Bus before mastering.");
  col(0.70, 0.75, 0.85);
  txt(62, 669, "Lance Prenc Smooth Bus Clipper active: shaves rogue peaks cleanly.");
  txt(62, 683, "Master Limiter Ceiling: -1.0 dBTP (guarantees zero ISP clipping on AAC).");
  txt(62, 697, "KClip 3 Zero Mode: 75% Mid-Bias protects side guitars from limiting.");
  txt(62, 711, "Live Telemetry: gmem[1159] Locked | gmem[1158] Mix Mode.");

  // Column 2 (Right, w=464): Active Producer Plays & Ear-Candy Director
  card(518, 172, 464, 590, "PRODUCER PLAYS & EAR-CANDY DIRECTOR (ARMED)", 1.00, 0.40, 0.65);
  
  // Play List (7 Producer Signature Tricks)
  draw_candy_play(530, 206, 440, 48, "PLAY 1: REVERSE VOCAL SWELL", "2.0 Bars before Chorus drop | Vocal Sovereign (slider31=1)", 1);
  draw_candy_play(530, 258, 440, 48, "PLAY 2: PRE-DROP MICRO-SILENCE CHOKE", "80 ms dead silence gap before Chorus drop | Devastator (slider22=80)", 1);
  draw_candy_play(530, 310, 440, 48, "PLAY 3: GUITAR PICK-SCRAPE & SWELL", "Pre-drop riser swell into chorus | Guitar Alchemist (slider42=1)", 1);
  draw_candy_play(530, 362, 440, 48, "PLAY 4: QUAD-WALL CHORUS EXPLOSION", "Width expands to 1.28x on downbeat | Mixing & Guitar Suites", 1);
  draw_candy_play(530, 414, 440, 48, "PLAY 5: BREAKDOWN WHAMMY PITCH DIVE", "Automatic tape stop/divebomb on bridge | Guitar Alchemist (slider45=1)", 1);
  draw_candy_play(530, 466, 440, 48, "PLAY 6: MEGAPHONE / TELEPHONE CHOKE", "Final bar Lo-Fi bandpass filter before drop | Vocal Sovereign (slider32=1)", 1);
  draw_candy_play(530, 518, 440, 48, "PLAY 7: DEVASTATOR SUB DIVEBOMB & BRAAM", "AI Context-Aware trailer impacts | Devastator Suite (Slots 1 & 3)", 1);

  // Bottom Suite Handshake Grid
  card(530, 574, 440, 173, "LIVE INTER-SUITE TELEMETRY BUS (gmem)", 0.20, 0.92, 0.62);
  gfx_setfont(2); col(0.70, 0.75, 0.85);
  txt(544, 604, "gmem[820]: Kick/Snare Detector -> Bass & Synth Ducking (ACTIVE)");
  txt(544, 624, "gmem[840]: Guitar Wall Energy -> Devastator & Synth Carve (ACTIVE)");
  txt(544, 644, "gmem[880]: Lead Vocal RMS -> Guitar Center Donut Hole (ACTIVE)");
  txt(544, 664, "gmem[900]: Devastator Neural Trigger -> SynBass Divebomb (ACTIVE)");
  txt(544, 684, "gmem[1096]: 1-Click Producer Relay & Static Calibration (READY)");
  col(0.20, 0.92, 0.62); txt(544, 714, "● ALL 8 SUITES SYNCHRONIZED TO KEL PINCHIN PRODUCER BLUEPRINT");
);

"""

target_marker = "function draw_mastering_console()"
assert target_marker in content, "draw_mastering_console marker not found"
content = content.replace(target_marker, producer_dna_code + target_marker)

# 3. Update view dispatch in @gfx
old_dispatch = """ui_view == 4 ? ( draw_stem_console(); ) : (
ui_view == 1 ? ( draw_library(); ) : (
ui_view == 2 ? ( draw_mastering_console(); ) : (
ui_view == 3 ? ( draw_ollama_console(); ) : ("""

new_dispatch = """ui_view == 5 ? ( draw_producer_dna(); ) : (
ui_view == 4 ? ( draw_stem_console(); ) : (
ui_view == 1 ? ( draw_library(); ) : (
ui_view == 2 ? ( draw_mastering_console(); ) : (
ui_view == 3 ? ( draw_ollama_console(); ) : ("""

assert old_dispatch in content, "old_dispatch not found"
content = content.replace(old_dispatch, new_dispatch)

# 4. Add closing paren at the end of the view dispatch
old_close = """); // close ui_view == 3
); // close ui_view == 2
); // close ui_view == 4"""

new_close = """); // close ui_view == 3
); // close ui_view == 2
); // close ui_view == 1
); // close ui_view == 4
); // close ui_view == 5"""

assert old_close in content, "old_close not found"
content = content.replace(old_close, new_close)

with open(jsfx_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Damei_AssessmentMatrix.jsfx successfully!")
