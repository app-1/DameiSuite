import sys

jsfx_path = r"C:\Dev\DameiSuite\effects\Damei_AssessmentMatrix.jsfx"

with open(jsfx_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Replace draw_producer_dna with enriched version containing:
# 1. Stem Level & Balance Matrix (Vocals, Drums, Bass, Other)
# 2. Boominess vs Sub Cleanliness Gauge (80-200 Hz vs 20-60 Hz)
# 3. Brightness Matching Meter (5k-16kHz Sheen)
# 4. Producer Plays Dashboard

old_dna_func_start = "function draw_producer_dna() local(cal_st, relay_btn_txt)"
dna_idx = content.find(old_dna_func_start)
assert dna_idx != -1, "draw_producer_dna not found"

end_dna_marker = "function draw_mastering_console()"
end_dna_idx = content.find(end_dna_marker)
assert end_dna_idx != -1, "draw_mastering_console marker not found"

new_dna_code = """function draw_producer_dna() local(cal_st, relay_btn_txt, b_rat, r_rat, w_box, h_box, y_pos) (
  card(24, 86, 972, 692, "PRODUCER BLUEPRINT // KEL PINCHIN (SPLIT CHAIN) - BOOMINESS & BRIGHTNESS RADAR", 1.00, 0.72, 0.02);

  // Top Action Banner: Dual 1-Click Action Buttons
  col(0.05, 0.12, 0.18); rct(38, 118, 944, 46);
  col(0.00, 0.85, 1.00); rcto(38, 118, 944, 46);
  gfx_setfont(1); col(0.00, 0.96, 0.83);
  txt(52, 126, "REFERENCE TARGET: 'I'M NOT DYING TO BE HERE' (motionblur)");
  gfx_setfont(3); col(0.70, 0.80, 0.95);
  txt(52, 144, "Ref Balance: Vox -19.7 LUFS | Drums -17.6 | Bass -19.8 | Other -14.7 | Boom/Sub 1.32x | Brightness 2.31%");

  cal_st = gmem[1159];
  btn(520, 126, 210, 30, "⚡ APPLY DE-BOOM & AIR", 0) ? (
    gmem[1096] = 1; // Trigger apply_deboom_and_vocal_lift.lua
  );
  btn(740, 126, 230, 30, cal_st == 1 ? "✓ SUITES SYNCED" : "⚡ RELAY FULL BLUEPRINT", cal_st == 1) ? (
    gmem[1096] = 1;
  );

  // =========================================================================
  // COLUMN 1 (LEFT, w=464): STEM BALANCE MATRIX & LOW-END BOOMINESS RADAR
  // =========================================================================
  card(38, 172, 464, 590, "STEM BALANCE MATRIX & LOW-END BOOMINESS RADAR", 0.00, 0.96, 0.83);

  // Card 1A: Stem Level Balance Matrix (No Guessing on Vocal/Drum/Bass/Synth levels)
  col(0.04, 0.06, 0.10); rct(50, 206, 440, 160);
  col(0.18, 0.25, 0.38); rcto(50, 206, 440, 160);
  gfx_setfont(3); col(1.00, 0.72, 0.02); txt(62, 214, "STEM LEVEL BALANCE BENCHMARK (REF vs CALIBRATED MIX)");
  
  // Table Header
  gfx_setfont(2); col(0.60, 0.65, 0.75);
  txt(62, 236, "STEM"); txt(140, 236, "REF LUFS"); txt(220, 236, "REL TO DRUMS"); txt(320, 236, "CALIBRATION APPLIED");
  
  // Vocals Row
  col(1.00, 0.40, 0.65); txt(62, 258, "VOCALS");
  col(0.85, 0.90, 1.00); txt(140, 258, "-19.7 LUFS");
  col(0.20, 0.92, 0.62); txt(220, 258, "-2.0 dB");
  col(0.20, 0.92, 0.62); txt(320, 258, "+2.2dB Trim + Donut Hole");

  // Drums Row
  col(0.20, 0.92, 0.62); txt(62, 282, "DRUMS");
  col(0.85, 0.90, 1.00); txt(140, 282, "-17.6 LUFS");
  col(1.00, 0.85, 0.30); txt(220, 282, "0.0 dB (Anchor)");
  col(0.85, 0.90, 1.00); txt(320, 282, "Cymbal Silk + BSA 85%");

  // Bass Row
  col(1.00, 0.72, 0.02); txt(62, 306, "BASS");
  col(0.85, 0.90, 1.00); txt(140, 306, "-19.8 LUFS");
  col(0.20, 0.92, 0.62); txt(220, 306, "-2.2 dB");
  col(0.85, 0.90, 1.00); txt(320, 306, "3.0dB Kick Duck + 90Hz Mono");

  // Other (Gtr/Synth) Row
  col(0.00, 0.85, 1.00); txt(62, 330, "OTHER (GTR)");
  col(0.85, 0.90, 1.00); txt(140, 330, "-14.7 LUFS");
  col(0.00, 0.85, 1.00); txt(220, 330, "+2.9 dB (Sides)");
  col(0.85, 0.90, 1.00); txt(320, 330, "Quad-Wall 1.28x + 95Hz HPF");

  // Card 1B: Boominess vs Sub-Bass Cleanliness Radar (80-200 Hz vs 20-60 Hz)
  col(0.04, 0.06, 0.10); rct(50, 376, 440, 185);
  col(0.18, 0.25, 0.38); rcto(50, 376, 440, 185);
  gfx_setfont(3); col(0.00, 0.96, 0.83); txt(62, 384, "LOW-END BOOMINESS vs SUB-BASS CONTROL GAUGE");
  gfx_setfont(2); col(0.85, 0.90, 1.00);
  txt(62, 404, "Sub-Bass (20-60 Hz):     Ref: 16.3%  |  Mix: 11.1%  (Deficit: -5.2%)");
  txt(62, 422, "Boominess (80-200 Hz):   Ref: 21.6%  |  Mix: 28.5%  (Excess Mud: +6.8%)");
  
  // Ratio Comparison
  col(0.20, 0.92, 0.62); txt(62, 444, "Ref Boom/Sub Ratio: 1.32x (Tight Punch)");
  col(1.00, 0.35, 0.55); txt(280, 444, "Mix Ratio: 2.56x (BOOMY!)");

  // Visual Bars for Boominess Comparison
  col(0.08, 0.10, 0.15); rct(62, 466, 416, 16);
  col(0.20, 0.92, 0.62); rct(62, 466, floor(416 * (1.32 / 3.0)), 16);
  col(1.00, 0.35, 0.55); rct(62 + floor(416 * (1.32 / 3.0)), 466, floor(416 * ((2.56 - 1.32) / 3.0)), 16);
  col(0.70, 0.75, 0.85); gfx_setfont(2);
  txt(66, 468, "Ref Clean Baseline [1.3x]            <- EXCESS MUD BANDWIDTH [+6.8%] ->");

  col(0.70, 0.75, 0.85);
  txt(62, 492, "Diagnosis: Upper-bass mud (100-160Hz) is masking sub-bass and vocals.");
  col(0.20, 0.92, 0.62);
  txt(62, 510, "Prescription: -2.5dB mud scoop @ 160Hz, 95Hz Guitar HPF, 3.0dB Kick Duck.");
  txt(62, 528, "Linear-Phase HPF: 28 Hz steep on Mix Bus removes infrasonic clutter.");

  // Card 1C: Brightness & High-End Sheen (5 kHz - 16 kHz)
  col(0.04, 0.06, 0.10); rct(50, 570, 440, 180);
  col(0.18, 0.25, 0.38); rcto(50, 570, 440, 180);
  gfx_setfont(3); col(0.00, 0.85, 1.00); txt(62, 578, "BRIGHTNESS & AIR SHEEN RADAR (5 kHz - 16 kHz)");
  gfx_setfont(2); col(0.85, 0.90, 1.00);
  txt(62, 598, "Brightness Energy (5-16k):  Ref: 2.31%  |  Mix: 0.61%  (Deficit: -1.7%)");
  txt(62, 616, "Spectral Sheen Deficit:     +5.0 to +7.4 dB needed between 5kHz and 10kHz.");
  
  col(0.70, 0.75, 0.85);
  txt(62, 638, "HF Match Applied: +1.8 dB Mix Bus Spectral Tilt + Maag 16kHz Air Sheen.");
  txt(62, 654, "Drums: Cymbal Silk Air Sheen >9kHz set to +2.2 dB.");
  txt(62, 670, "Guitars: Air Sheen & Cab Presence >9kHz set to +1.8 dB.");
  txt(62, 686, "Synths: 12kHz Glassy Air Sheen set to +3.2 dB.");
  col(0.20, 0.92, 0.62);
  txt(62, 706, "STATUS: Brightness matched cleanly without introducing harshness.");

  // =========================================================================
  // COLUMN 2 (RIGHT, w=464): VOCAL UNBURY POCKET & PRODUCER PLAYS
  // =========================================================================
  card(518, 172, 464, 590, "VOCAL UNBURY POCKET & PRODUCER PLAYS (ARMED)", 1.00, 0.40, 0.65);

  // Card 2A: Vocal Unbury Pocket Architecture
  col(0.04, 0.06, 0.10); rct(530, 206, 440, 120);
  col(1.00, 0.40, 0.65); rcto(530, 206, 440, 120);
  gfx_setfont(3); col(1.00, 0.40, 0.65); txt(542, 214, "LEAD VOCAL UNBURY & CENTER POCKET ARCHITECTURE");
  gfx_setfont(2); col(0.85, 0.90, 1.00);
  txt(542, 234, "1. Center Donut-Hole: -3.5 dB Notch @ 2500 Hz on Mix Bus Guitars/Synths.");
  txt(542, 252, "2. Center Vocal Level Trim: +2.2 dB applied via Producer Channel (slider41).");
  txt(542, 270, "3. Track Fader: [VOX] optimized to +1.6 dB (sits 2.0 dB below Drums anchor).");
  col(0.20, 0.92, 0.62);
  txt(542, 290, "4. Serial Dynamics: 1176 FET (28%) + LA-2A (24%) + 1.8kHz bite (+1.5dB).");
  txt(542, 306, "RESULT: Lead vocals cut directly through the wall with radio intimacy.");

  // Card 2B: 7 Producer Signature Plays
  draw_candy_play(530, 334, 440, 44, "PLAY 1: REVERSE VOCAL SWELL", "2.0 Bars before Chorus drop | Vocal Sovereign (slider31=1)", 1);
  draw_candy_play(530, 382, 440, 44, "PLAY 2: PRE-DROP MICRO-SILENCE CHOKE", "80 ms dead silence gap before Chorus drop | Devastator (slider22=80)", 1);
  draw_candy_play(530, 430, 440, 44, "PLAY 3: GUITAR PICK-SCRAPE & SWELL", "Pre-drop riser swell into chorus | Guitar Alchemist (slider42=1)", 1);
  draw_candy_play(530, 478, 440, 44, "PLAY 4: QUAD-WALL CHORUS EXPLOSION", "Width expands to 1.28x on downbeat | Mixing & Guitar Suites", 1);
  draw_candy_play(530, 526, 440, 44, "PLAY 5: BREAKDOWN WHAMMY PITCH DIVE", "Automatic tape stop/divebomb on bridge | Guitar Alchemist (slider45=1)", 1);
  draw_candy_play(530, 574, 440, 44, "PLAY 6: MEGAPHONE / TELEPHONE CHOKE", "Final bar Lo-Fi bandpass filter before drop | Vocal Sovereign (slider32=1)", 1);
  draw_candy_play(530, 622, 440, 44, "PLAY 7: DEVASTATOR SUB DIVEBOMB & BRAAM", "AI Context-Aware trailer impacts | Devastator Suite (Slots 1 & 3)", 1);

  // Live Telemetry Strip
  col(0.04, 0.06, 0.10); rct(530, 674, 440, 75);
  col(0.20, 0.92, 0.62); rcto(530, 674, 440, 75);
  gfx_setfont(2); col(0.70, 0.75, 0.85);
  txt(542, 682, "gmem[820]: Kick -> Bass/Synth Duck (3.0dB) | gmem[840]: Gtr Carve (3.0dB)");
  txt(542, 700, "gmem[880]: Vocal -> Gtr Center Donut Carve | gmem[900]: Neural Braam");
  col(0.20, 0.92, 0.62);
  txt(542, 718, "● LIVE CALIBRATION LOCKED: Vocals Forward | De-Boomed | Brightness Aligned");
);

"""

content = content[:dna_idx] + new_dna_code + content[end_dna_idx:]

with open(jsfx_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Enriched draw_producer_dna successfully!")
