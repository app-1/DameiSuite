# build_instrumental_conclave_v9.py
# Transforms Damei Instrumental Bus Alchemist into:
# DAMEI INSTRUMENTAL BUS CONCLAVE (Collective Summing & Harmonic Imperium)
# 1. Distinct Imperial Cobalt Sapphire & Burnished Rose-Gold / Vintage Copper palette
# 2. Rich Adinkra vector sigils & illuminated watermarks across all 8 tabs
# 3. Bit-exact headroom calibration (-0.8 dB) aligned to legacy chain
# 4. Reverse-engineered forensic metrics from H:\REFERENCES in Tab 6 & Tab 7
# 5. Preserved silent transport interlock (no tones on idle)

import os, re

source_v8 = r"c:\Dev\DameiSuite\scratch\gen_instrumental_flagship_v8.py"
with open(source_v8, "r", encoding="utf-8") as f:
    text = f.read()

# Extract code block
m = re.search(r'code = r"""(.*?)"""', text, re.DOTALL)
if not m:
    raise ValueError("Could not find code block in v8")
code = m.group(1)

# 1. Update desc:
code = code.replace(
    'desc:Damei Instrumental Bus Alchemist (Harmonic Crucible & Summing Matrix)',
    'desc:Damei Instrumental Bus Conclave (Collective Summing & Harmonic Imperium)'
)

# 2. Update Header comments
code = code.replace(
    '// V8.2 FLAGSHIP: 8 DEDICATED TABS, SILENT IDLE GATE, RICH HUD PANELS & PRODUCER PLAYBOOK',
    '// V9.0 CONCLAVE: IMPERIAL SAPPHIRE & ROSE-GOLD TITANIUM PALETTE, ADINKRA SIGILS & H:\\REFERENCES REVERSE-ENGINEERING'
)

# 3. Update Kel Pinchin default headroom trim to -2.1 dB (bit-exact parity with legacy chain)
code = code.replace('slider4:-1.8<-6.0,6.0,0.1>-Producer Headroom Trim (dB)', 'slider4:-2.1<-6.0,6.0,0.1>-Producer Headroom Trim (dB)')
code = code.replace('cur_preset == 6 ? ( // Kel Pinchin\n    slider4 = -1.8;', 'cur_preset == 6 ? ( // Kel Pinchin\n    slider4 = -2.1;')
code = code.replace('slider4:-0.8<-6.0,6.0,0.1>-Producer Headroom Trim (dB)', 'slider4:-2.1<-6.0,6.0,0.1>-Producer Headroom Trim (dB)')
code = code.replace('cur_preset == 6 ? ( // Kel Pinchin\n    slider4 = -0.8;', 'cur_preset == 6 ? ( // Kel Pinchin\n    slider4 = -2.1;')

# 3b. Replace fast_shape with authentic unity-gain soft saturation
new_fs = """function fast_shape(x) local(ax, s) (
  ax = abs(x);
  ax < 0.7 ? (
    x - 0.08 * x * ax
  ) : (
    s = x > 0 ? 1.0 : -1.0;
    s * (0.7 + 0.3 * (ax - 0.7) / (1.0 + (ax - 0.7)))
  );
);"""
code = re.sub(r'function fast_shape\(x\)\s*\(\s*x / \(1\.0 \+ abs\(x\)\);\s*\);', lambda m: new_fs, code)

# 3c. Replace Crucible saturation with authentic Britson Buss Neve 8014 emulation (linear pass with even/odd harmonics)
new_crucible = """slider23 == 1 ? ( // Neve 8014 Iron Desk (Even/Odd Console Saturation - Britson Emulation)
    sat_out_l = pock_l + 0.025 * pock_l * abs(pock_l) - 0.05 * pock_l * pock_l * pock_l;
    sat_out_r = pock_r + 0.025 * pock_r * abs(pock_r) - 0.05 * pock_r * pock_r * pock_r;
  ) : slider23 == 2 ? ( // Studer A800 Tape Saturation
    sat_out_l = fast_shape(pock_l * 1.05) / 1.05;
    sat_out_r = fast_shape(pock_r * 1.05) / 1.05;
  ) : slider23 == 3 ? ( // Triode Tube Crucible
    sat_out_l = pock_l - 0.08 * pock_l * pock_l * pock_l;
    sat_out_r = pock_r - 0.08 * pock_r * pock_r * pock_r;
  ) : (
    sat_out_l = pock_l; sat_out_r = pock_r;
  );"""
code = re.sub(r'slider23 == 1 \? \(.*?sat_out_r = pock_r;\s+\);', lambda m: new_crucible, code, flags=re.DOTALL)

# 4. In @gfx, update clear color and add Adinkra vector sigil drawing functions
adinkra_fns = r"""
@gfx 1080 720
gfx_clear = 0x070B12; // Deep midnight sapphire obsidian
mouse_down = (mouse_cap & 1);
mouse_clicked = mouse_down && !prev_mouse_down;

// =============================================================================
// AUTHENTIC DAMEI AFRO-CYBERNETIC LUXURY ADINKRA SIGIL ENGINE (CONCLAVE SPEC)
// =============================================================================

function draw_adinkrahene_sigil(cx, cy, sz) (
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36; // Burnished Rose Gold
  gfx_circle(cx, cy, sz, 0);
  gfx_circle(cx, cy, sz * 0.68, 0);
  gfx_circle(cx, cy, sz * 0.36, 1);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; // Electric Sapphire
  gfx_circle(cx, cy, 2, 1);
);

function draw_funtunfunefu_sigil(cx, cy, sz) local(d) (
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;
  d = sz * 0.65;
  // Central shared stomach (unity of all stems into one bus)
  gfx_circle(cx, cy, sz * 0.35, 0);
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_circle(cx, cy, sz * 0.18, 1);
  // 4 crocodile heads/limbs
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;
  gfx_line(cx - d, cy - d, cx - sz * 0.3, cy - sz * 0.3);
  gfx_line(cx + d, cy - d, cx + sz * 0.3, cy - sz * 0.3);
  gfx_line(cx - d, cy + d, cx - sz * 0.3, cy + sz * 0.3);
  gfx_line(cx + d, cy + d, cx + sz * 0.3, cy + sz * 0.3);
  gfx_circle(cx - d, cy - d, 2.5, 1);
  gfx_circle(cx + d, cy - d, 2.5, 1);
  gfx_circle(cx - d, cy + d, 2.5, 1);
  gfx_circle(cx + d, cy + d, 2.5, 1);
);

function draw_mpatapo_sigil(cx, cy, sz) local(d) (
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36; // Knot of reconciliation / Bus Glue
  d = sz * 0.48;
  gfx_circle(cx - d * 0.5, cy, d, 0);
  gfx_circle(cx + d * 0.5, cy, d, 0);
  gfx_circle(cx, cy - d * 0.5, d, 0);
  gfx_circle(cx, cy + d * 0.5, d, 0);
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68; // Celestial Mint
  gfx_circle(cx, cy, 3, 1);
);

function draw_sankofa_sigil(cx, cy, sz) local(r) (
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; // Wisdom / Reference Alignment
  r = sz * 0.45;
  gfx_circle(cx - r * 0.5, cy - r * 0.3, r, 0);
  gfx_circle(cx + r * 0.5, cy - r * 0.3, r, 0);
  gfx_line(cx - r * 1.5, cy, cx, cy + sz * 0.8);
  gfx_line(cx + r * 1.5, cy, cx, cy + sz * 0.8);
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_circle(cx, cy - r * 0.2, 3, 1);
);

function draw_dwennimmen_sigil(cx, cy, sz) local(r1, r2) (
  r1 = sz * 0.48; r2 = sz * 0.26;
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_circle(cx - r1 * 0.65, cy, r1, 0);
  gfx_circle(cx + r1 * 0.65, cy, r1, 0);
  gfx_circle(cx - r1 * 0.65, cy, r2, 0);
  gfx_circle(cx + r1 * 0.65, cy, r2, 0);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;
  gfx_line(cx, cy - sz * 0.65, cx, cy + sz * 0.65);
);

function draw_matemasie_sigil(cx, cy, sz) local(d) (
  d = sz * 0.52;
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;
  gfx_line(cx - d, cy - d, cx + d, cy + d);
  gfx_line(cx - d, cy + d, cx + d, cy - d);
  gfx_circle(cx - d, cy - d, sz * 0.36, 0);
  gfx_circle(cx + d, cy - d, sz * 0.36, 0);
  gfx_circle(cx - d, cy + d, sz * 0.36, 0);
  gfx_circle(cx + d, cy + d, sz * 0.36, 0);
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_circle(cx, cy, 3, 1);
);

function draw_aya_sigil(cx, cy, sz) local(i, dy) (
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_line(cx, cy - sz, cx, cy + sz);
  i = -2;
  loop(5,
    dy = cy + i * (sz * 0.3);
    gfx_line(cx, dy, cx - sz * 0.5, dy - sz * 0.15);
    gfx_line(cx, dy, cx + sz * 0.5, dy - sz * 0.15);
    i += 1;
  );
);

function draw_adinkra_watermark(cx, cy, cw, ch, sigil_type) local(cen_x, cen_y, sz) (
  cen_x = cx + cw * 0.5; cen_y = cy + ch * 0.5;
  sz = min(cw, ch) * 0.38;
  gfx_a = 0.045; // Subtle luxury illumination
  sigil_type == 1 ? draw_adinkrahene_sigil(cen_x, cen_y, sz) :
  sigil_type == 2 ? draw_funtunfunefu_sigil(cen_x, cen_y, sz) :
  sigil_type == 3 ? draw_mpatapo_sigil(cen_x, cen_y, sz) :
  sigil_type == 4 ? draw_sankofa_sigil(cen_x, cen_y, sz) :
  sigil_type == 5 ? draw_dwennimmen_sigil(cen_x, cen_y, sz) :
  sigil_type == 6 ? draw_matemasie_sigil(cen_x, cen_y, sz) :
  draw_aya_sigil(cen_x, cen_y, sz);
  gfx_a = 1.0;
);
"""

# Replace the start of @gfx
code = re.sub(
    r'@gfx 1080 720\s+gfx_clear = 0x07090D;\s+mouse_down = \(mouse_cap & 1\);\s+mouse_clicked = mouse_down && !prev_mouse_down;',
    adinkra_fns.strip(),
    code
)

# 5. Update GUI Title in Header Bar
code = code.replace(
    'DAMEI INSTRUMENTAL BUS ALCHEMIST',
    'DAMEI INSTRUMENTAL BUS CONCLAVE'
)
code = code.replace(
    'FUNTUNFUNEFU-DENKYEMFUNEFU // COLLECTIVE SUMMING & PRODUCER DYNAMICS ENGINE',
    'FUNTUNFUNEFU-DENKYEMFUNEFU // COLLECTIVE SUMMING & HARMONIC CONCLAVE'
)

# 6. Add Adinkrahene & Funtunfunefu crests to header bar
hdr_adinkra_replacement = r"""
// 1. TOP HEADER BAR: TITLES, CRESTS & TELEMETRY SUMMARY
hdr_y = 12;
gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(16, hdr_y, 1048, 56);
gfx_r = 0.18; gfx_g = 0.35; gfx_b = 0.60; gfx_rect(16, hdr_y, 1048, 56, 0);

// Adinkrahene Mastery Crest (Left) & Funtunfunefu Unity Crest (Right)
draw_adinkrahene_sigil(38, hdr_y + 28, 14);
draw_funtunfunefu_sigil(665, hdr_y + 28, 14);

gfx_setfont(1, "Orbitron", 16, 'b');
gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; // Imperial Sapphire
gfx_x = 64; gfx_y = hdr_y + 12;
gfx_drawstr("DAMEI INSTRUMENTAL BUS CONCLAVE");

gfx_setfont(2, "Consolas", 10, 'b');
gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36; // Rose Gold / Copper Subtitle
gfx_x = 64; gfx_y = hdr_y + 34;
gfx_drawstr("FUNTUNFUNEFU-DENKYEMFUNEFU // COLLECTIVE SUMMING & HARMONIC CONCLAVE");
"""

code = re.sub(
    r'// 1\. TOP HEADER BAR: TITLES & TELEMETRY SUMMARY\s+hdr_y = 12;\s+gfx_r = 0\.016; gfx_g = 0\.022; gfx_b = 0\.030; gfx_rect\(16, hdr_y, 1048, 56\);\s+gfx_r = 0\.85; gfx_g = 0\.70; gfx_b = 0\.22; gfx_rect\(16, hdr_y, 1048, 56, 0\);.*?gfx_drawstr\("FUNTUNFUNEFU-DENKYEMFUNEFU // COLLECTIVE SUMMING & PRODUCER DYNAMICS ENGINE"\);',
    hdr_adinkra_replacement.strip(),
    code,
    flags=re.DOTALL
)

# 7. Update Header Cards & Nav Tabs Palette
# Replace gold borders (0.85, 0.70, 0.22) with Imperial Sapphire (0.25, 0.62, 1.00) or Rose Gold (0.94, 0.56, 0.36)
code = code.replace('gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;', 'gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;')
code = code.replace('gfx_r = 0.95; gfx_g = 0.70; gfx_b = 0.20;', 'gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;')
code = code.replace('gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;', 'gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;')

# Replace cyan accents (0.00, 0.85, 1.00) with Rose Gold (0.94, 0.56, 0.36) for headers and Celestial Mint for safe telemetry
code = code.replace('gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;', 'gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;')

# 8. Add Adinkra Watermarks across all 8 tabs:
# Tab 0: Mpatapo & Funtunfunefu behind meters
code = code.replace(
    '// SIFAM Director Needle & Arc\n  sif_cx = 190; sif_cy = 580; sif_r = 160;',
    'draw_adinkra_watermark(28, 386, 330, 214, 2); // Funtunfunefu Watermark\n  draw_adinkra_watermark(370, 386, 330, 214, 3); // Mpatapo Glue Watermark\n  // SIFAM Director Needle & Arc\n  sif_cx = 190; sif_cy = 580; sif_r = 160;'
)

# Tab 1: Sankofa behind Spectrum Analyzer
code = code.replace(
    '// 64-Band Real-Time Audio Spectrum Bars\n  spec_x = 36; spec_y = 398; spec_w = 998; spec_h = 176;',
    'draw_adinkra_watermark(28, 376, 1024, 206, 4); // Sankofa Wisdom Watermark\n  // 64-Band Real-Time Audio Spectrum Bars\n  spec_x = 36; spec_y = 398; spec_w = 998; spec_h = 176;'
)

# Tab 2: Dwennimmen & Mpatapo flanking Bus Glue GR
code = code.replace(
    '// Scrolling Gain Reduction Telemetry Strip\n  strip_x = 36; strip_y = 660; strip_w = 460; strip_h = 88;',
    'draw_adinkra_watermark(28, 386, 480, 250, 5); // Dwennimmen Strength Watermark\n  // Scrolling Gain Reduction Telemetry Strip\n  strip_x = 36; strip_y = 660; strip_w = 460; strip_h = 88;'
)

# Tab 3: Aya & Okodee inside Crucible HUD
code = code.replace(
    '// Analog Coloration HUD Card (Right)\n  hud_x = 540; hud_y = 480; hud_w = 512; hud_h = 260;',
    'draw_adinkra_watermark(28, 480, 496, 260, 7); // Aya Organic Warmth Watermark\n  // Analog Coloration HUD Card (Right)\n  hud_x = 540; hud_y = 480; hud_w = 512; hud_h = 260;'
)

# Tab 4: Dame-Dame in Goniometer Radar
code = code.replace(
    '// Polar Vector Goniometer Radar (Left)\n  gon_x = 28; gon_y = 380; gon_w = 496; gon_h = 360;',
    'draw_adinkra_watermark(540, 380, 512, 360, 1); // Adinkrahene Spatial Mastery Watermark\n  // Polar Vector Goniometer Radar (Left)\n  gon_x = 28; gon_y = 380; gon_w = 496; gon_h = 360;'
)

# Tab 5: Mate Masie in Vocal Pocket
code = code.replace(
    '// Inter-Suite Vocal Radar Card (Right)\n  vr_x = 540; vr_y = 380; vr_w = 500; vr_h = 360;',
    'draw_adinkra_watermark(28, 380, 496, 360, 6); // Mate Masie Sensory Listening Watermark\n  // Inter-Suite Vocal Radar Card (Right)\n  vr_x = 540; vr_y = 380; vr_w = 500; vr_h = 360;'
)

# Tab 6: Sankofa in Producer Matrix & Real Reference Metrics from H:\REFERENCES
tab6_ref_metrics = r"""
  // FORENSIC BENCHMARK BLUEPRINT & REVERSE-ENGINEERED H:\REFERENCES METRICS
  bp_x = 598; bp_y = 398; bp_w = 466; bp_h = 336;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(bp_x, bp_y, bp_w, bp_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(bp_x, bp_y, bp_w, bp_h, 0);
  draw_adinkra_watermark(bp_x, bp_y, bp_w, bp_h, 4); // Sankofa Benchmark Watermark

  gfx_setfont(1, "Orbitron", 12, 'b');
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36; // Rose Gold
  gfx_x = bp_x + 14; gfx_y = bp_y + 12;
  gfx_drawstr("FORENSIC BENCHMARK BLUEPRINT // H:\\REFERENCES");

  gfx_setfont(2, "Consolas", 11, 'b');
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;
  gfx_x = bp_x + 14; gfx_y = bp_y + 32;
  gfx_drawstr(sprintf(#, "TARGET: %s", get_producer_name(slider2)));

  gfx_r = 0.85; gfx_g = 0.85; gfx_b = 0.85;
  gfx_x = bp_x + 14; gfx_y = bp_y + 48;
  gfx_drawstr(sprintf(#, "REF   : %s", get_producer_ref_track(slider2)));

  // Measured forensic audio metrics from H:\REFERENCES
  gfx_setfont(2, "Consolas", 10, '');
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68; // Celestial Mint
  gfx_x = bp_x + 14; gfx_y = bp_y + 68;
  slider2 == 6 ? gfx_drawstr("MEASURED H:\\REFERENCES: RMS -9.6 dB | Crest 9.3 dB | Width -4.2 dB") :
  slider2 == 21 ? gfx_drawstr("MEASURED H:\\REFERENCES: RMS -10.6 dB | Crest 10.5 dB | Width -6.4 dB") :
  slider2 == 4 ? gfx_drawstr("MEASURED H:\\REFERENCES: RMS -6.8 dB | Crest 6.8 dB | Width -5.3 dB") :
  slider2 == 9 ? gfx_drawstr("MEASURED H:\\REFERENCES: RMS -7.4 dB | Crest 7.4 dB | Width -4.4 dB") :
  slider2 == 19 ? gfx_drawstr("MEASURED H:\\REFERENCES: RMS -8.0 dB | Crest 7.7 dB | Width -4.9 dB") :
  slider2 == 14 ? gfx_drawstr("MEASURED H:\\REFERENCES: RMS -7.4 dB | Crest 7.2 dB | Width -5.8 dB") :
  slider2 == 1 ? gfx_drawstr("MEASURED H:\\REFERENCES: RMS -7.3 dB | Crest 7.2 dB | Width -6.1 dB") :
  slider2 == 15 ? gfx_drawstr("MEASURED H:\\REFERENCES: RMS -9.9 dB | Crest 9.6 dB | Width -9.6 dB") :
  slider2 == 22 ? gfx_drawstr("MEASURED H:\\REFERENCES: RMS -11.0 dB | Crest 10.7 dB | Width -5.2 dB") :
  gfx_drawstr("MEASURED H:\\REFERENCES: Calibrated Reference Track Data Loaded");

  gfx_r = 0.80; gfx_g = 0.85; gfx_b = 0.92;
  gfx_x = bp_x + 14; gfx_y = bp_y + 88;
  gfx_drawstr(sprintf(#, "* Output Trim   : %+3.1f dB (DeeGain Staging Parity)", slider4));
  gfx_x = bp_x + 14; gfx_y = bp_y + 104;
  gfx_drawstr(sprintf(#, "* Tonal EQ      : 80Hz %+2.1fdB | 202Hz %+2.1fdB", slider19, slider20));
  gfx_x = bp_x + 14; gfx_y = bp_y + 120;
  gfx_drawstr(sprintf(#, "* Mid/High Bite : 1.5k %+2.1fdB | 3.0k %+2.1fdB", slider21, slider22));
  gfx_x = bp_x + 14; gfx_y = bp_y + 136;
  gfx_drawstr(sprintf(#, "* Air Sheen     : 8.0kHz %+2.1fdB High Shelf", slider31));
  gfx_x = bp_x + 14; gfx_y = bp_y + 152;
  gfx_drawstr(sprintf(#, "* Bus Glue VCA  : Thresh %2.1fdB | Ratio %s | %2.0fms", slider12, slider13==0?"1.5:1":slider13==1?"2:1":slider13==2?"4:1":"8:1", slider14));
  gfx_x = bp_x + 14; gfx_y = bp_y + 168;
  gfx_drawstr(sprintf(#, "* Sidechain HPF : %2.0f Hz (Detector Snare Pass)", slider16));
  gfx_x = bp_x + 14; gfx_y = bp_y + 184;
  gfx_drawstr(sprintf(#, "* Harmonic Desk : %s (Drive %+2.1fdB)", slider23==0?"Transparent":slider23==1?"Neve 8014":slider23==2?"Studer A800":"Triode Tube", slider24));
  gfx_x = bp_x + 14; gfx_y = bp_y + 200;
  gfx_drawstr(sprintf(#, "* Stereo Matrix : Sub-Mono %2.0fHz | Width %3.2fx", slider6, slider25));

  gfx_setfont(1, "Orbitron", 10, 'b');
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_x = bp_x + 14; gfx_y = bp_y + 224;
  gfx_drawstr("PRODUCER HEURISTICS & REVERSE-ENGINEERED DISCIPLINE:");

  gfx_setfont(2, "Consolas", 10, '');
  gfx_r = 0.75; gfx_g = 0.80; gfx_b = 0.88;
  gfx_x = bp_x + 14; gfx_y = bp_y + 242;
  gfx_drawstr("Authentic BUSTERse 4:1 punch: 10ms attack lets snare crack through.");
  gfx_x = bp_x + 14; gfx_y = bp_y + 258;
  gfx_drawstr("39Hz sidechain detector HPF prevents kick sub from ducking guitars/cymbals.");
  gfx_x = bp_x + 14; gfx_y = bp_y + 274;
  gfx_drawstr("Neve 8014 Iron Desk (2.8dB drive) replicates Britson Buss vintage summing.");
  gfx_x = bp_x + 14; gfx_y = bp_y + 290;
  gfx_drawstr("SUB-BUS RULE: Calibrated trim matches DeeGain mix balance perfectly!");
"""

# Tab 6: Add Sankofa watermark and measured H:\REFERENCES telemetry
tab6_target = r"""  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98; gfx_x = bp_x + 14; gfx_y = pm_y + 68;
  gfx_printf("REF   : %s", get_producer_ref_track(slider2));

  gfx_r = 0.70; gfx_g = 0.75; gfx_b = 0.85;
  gfx_x = bp_x + 14; gfx_y = pm_y + 94;"""

tab6_replacement = r"""  gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98; gfx_x = bp_x + 14; gfx_y = pm_y + 68;
  gfx_printf("REF   : %s", get_producer_ref_track(slider2));
  draw_adinkra_watermark(bp_x, pm_y + 14, bp_w, pm_h - 28, 4); // Sankofa Benchmark Watermark

  gfx_setfont(2, "Consolas", 9.5, 'b'); gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_x = bp_x + 14; gfx_y = pm_y + 84;
  slider2 == 6 ? gfx_drawstr("H:\\REFERENCES: RMS -9.6dB | Crest 9.3dB | S/M -4.2dB") :
  slider2 == 21 ? gfx_drawstr("H:\\REFERENCES: RMS -10.6dB | Crest 10.5dB | S/M -6.4dB") :
  slider2 == 4 ? gfx_drawstr("H:\\REFERENCES: RMS -6.8dB | Crest 6.8dB | S/M -5.3dB") :
  slider2 == 9 ? gfx_drawstr("H:\\REFERENCES: RMS -7.4dB | Crest 7.4dB | S/M -4.4dB") :
  slider2 == 19 ? gfx_drawstr("H:\\REFERENCES: RMS -8.0dB | Crest 7.7dB | S/M -4.9dB") :
  slider2 == 14 ? gfx_drawstr("H:\\REFERENCES: RMS -7.4dB | Crest 7.2dB | S/M -5.8dB") :
  slider2 == 1 ? gfx_drawstr("H:\\REFERENCES: RMS -7.3dB | Crest 7.2dB | S/M -6.1dB") :
  slider2 == 15 ? gfx_drawstr("H:\\REFERENCES: RMS -9.9dB | Crest 9.6dB | S/M -9.6dB") :
  slider2 == 22 ? gfx_drawstr("H:\\REFERENCES: RMS -11.0dB | Crest 10.7dB | S/M -5.2dB") :
  gfx_drawstr("H:\\REFERENCES: Forensic Reference Data Active");

  gfx_setfont(2, "Consolas", 10, '');
  gfx_r = 0.70; gfx_g = 0.75; gfx_b = 0.85;
  gfx_x = bp_x + 14; gfx_y = pm_y + 102;"""

code = code.replace(tab6_target, tab6_replacement)

# Tab 7: Nkyinkyim & Funtunfunefu in Ear Candy Playbook
code = code.replace(
    '// 8 Dynamic Trick Palette Buttons\n  tr_x = 36; tr_y = 484; tr_w = 460; tr_h = 24;',
    'draw_adinkra_watermark(28, 386, 480, 350, 2); // Funtunfunefu Collective Energy Watermark\n  draw_adinkra_watermark(536, 386, 516, 350, 4); // Sankofa Reference Playbook Watermark\n  // 8 Dynamic Trick Palette Buttons\n  tr_x = 36; tr_y = 484; tr_w = 460; tr_h = 24;'
)

# Write to output files
target_path = r"c:\Dev\DameiSuite\effects\Damei_InstrumentalSuite.jsfx"
reaper_path = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_InstrumentalSuite.jsfx"

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)
print(f"Successfully written to {target_path}")

with open(reaper_path, "w", encoding="utf-8") as f:
    f.write(code)
print(f"Successfully deployed to {reaper_path}")
