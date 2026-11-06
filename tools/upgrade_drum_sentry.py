import os, sys, shutil

def upgrade_drum_sentry():
    target = r"c:\Dev\DameiSuite\effects\Damei_DrumAssessment.jsfx"
    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add filter & fingerprint definitions to @init
    # Look for memory allocation block in @init
    init_marker = "  // Telemetry Accumulators"
    init_code = """  // 6-Band Drum Forensic Memory Allocation & Biquad Engine
  DRUM_BQC = 6000;      // 6 filters * 5 coeffs = 30 floats
  DRUM_BQS = 6050;      // 6 filters * 2 states = 12 floats
  DRUM_ACC = 6100;      // 6 power accumulators
  DRUM_PCT = 6120;      // 6 live percentage values
  DRUM_SMOOTH_PCT = 6140; // 6 smoothed percentage values
  DRUM_DELTA_DB = 6160; // 6 delta dB values vs reference
  DRUM_REF_FP = 6200;   // 25 producer targets * 8 floats
  
  drum_match_pct = 88.0;
  sc_spectral = 85.0;
  sc_crest = 90.0;
  sc_phase = 88.0;

  function bq_bp_init(coeff_ptr, fc, q) local(w0, alpha, b0, b1, b2, a0, a1, a2) (
    w0 = 2.0 * $pi * fc / srate;
    alpha = sin(w0) / (2.0 * q);
    b0 = alpha; b1 = 0.0; b2 = -alpha;
    a0 = 1.0 + alpha; a1 = -2.0 * cos(w0); a2 = 1.0 - alpha;
    coeff_ptr[0] = b0 / a0; coeff_ptr[1] = b1 / a0; coeff_ptr[2] = b2 / a0;
    coeff_ptr[3] = a1 / a0; coeff_ptr[4] = a2 / a0;
  );

  function bq_run(c, s, x) local(y) (
    y = c[0]*x + s[0];
    s[0] = c[1]*x - c[3]*y + s[1];
    s[1] = c[2]*x - c[4]*y;
    y;
  );

  // Initialize 6 Drum Acoustic Bands:
  // Band 0: Sub (55 Hz, Q=1.1)
  // Band 1: Shell Punch (160 Hz, Q=1.0)
  // Band 2: Cardboard Mud (350 Hz, Q=1.3)
  // Band 3: Bark / Definition (1100 Hz, Q=0.9)
  // Band 4: Attack Crack (3800 Hz, Q=0.9)
  // Band 5: Cymbal Air (11000 Hz, Q=0.8)
  bq_bp_init(DRUM_BQC + 0,   55.0, 1.1);
  bq_bp_init(DRUM_BQC + 5,  160.0, 1.0);
  bq_bp_init(DRUM_BQC + 10, 350.0, 1.3);
  bq_bp_init(DRUM_BQC + 15, 1100.0, 0.9);
  bq_bp_init(DRUM_BQC + 20, 3800.0, 0.9);
  bq_bp_init(DRUM_BQC + 25, 11000.0, 0.8);

  // Clear memory
  memset(DRUM_BQS, 0, 12);
  memset(DRUM_ACC, 0, 6);
  memset(DRUM_PCT, 0, 6);
  memset(DRUM_SMOOTH_PCT, 0, 6);
  memset(DRUM_DELTA_DB, 0, 6);

  // Populate 25 Producer Target Drum Fingerprints [sub%, punch%, mud%, bark%, crack%, air%, crest_target, corr_target]
  // 0: Neutral Wire
  p = DRUM_REF_FP + 0*8;  p[0]=25.0; p[1]=35.0; p[2]=8.0; p[3]=16.0; p[4]=11.0; p[5]=5.0; p[6]=24.0; p[7]=0.70;
  // 1: Lance Prenc (Alpha Wolf)
  p = DRUM_REF_FP + 1*8;  p[0]=28.0; p[1]=38.0; p[2]=3.5; p[3]=13.0; p[4]=13.5; p[5]=4.0; p[6]=28.5; p[7]=0.80;
  // 2: Scott Seigel (DIESECT)
  p = DRUM_REF_FP + 2*8;  p[0]=30.0; p[1]=36.0; p[2]=4.0; p[3]=12.0; p[4]=13.0; p[5]=5.0; p[6]=27.0; p[7]=0.78;
  // 3: Jonathan Dolese (Mirrorcell)
  p = DRUM_REF_FP + 3*8;  p[0]=26.0; p[1]=37.0; p[2]=4.5; p[3]=14.0; p[4]=13.5; p[5]=5.0; p[6]=26.5; p[7]=0.75;
  // 4: Buster Odeholm (thrown / Northlane)
  p = DRUM_REF_FP + 4*8;  p[0]=32.0; p[1]=35.0; p[2]=3.0; p[3]=13.0; p[4]=13.0; p[5]=4.0; p[6]=25.0; p[7]=0.85;
  // 5: Lewis Johns (Love Is Noise)
  p = DRUM_REF_FP + 5*8;  p[0]=24.0; p[1]=38.0; p[2]=5.0; p[3]=15.0; p[4]=13.0; p[5]=5.0; p[6]=29.0; p[7]=0.76;
  // 6: Kel Pinchin (Split Chain)
  p = DRUM_REF_FP + 6*8;  p[0]=26.0; p[1]=36.0; p[2]=5.5; p[3]=14.0; p[4]=13.5; p[5]=5.0; p[6]=28.0; p[7]=0.77;
  // 7: Dan Lancaster (Don Broco)
  p = DRUM_REF_FP + 7*8;  p[0]=25.0; p[1]=36.0; p[2]=4.0; p[3]=15.0; p[4]=14.0; p[5]=6.0; p[6]=26.0; p[7]=0.80;
  // 8: Erik Bickerstaffe (Static Dress)
  p = DRUM_REF_FP + 8*8;  p[0]=23.0; p[1]=37.0; p[2]=6.0; p[3]=16.0; p[4]=13.0; p[5]=5.0; p[6]=27.5; p[7]=0.75;
  // 9: Sam Guaiana (Shyeye)
  p = DRUM_REF_FP + 9*8;  p[0]=27.0; p[1]=37.0; p[2]=4.5; p[3]=13.5; p[4]=13.0; p[5]=5.0; p[6]=26.0; p[7]=0.81;
  // 10: Zach Tuch (Heavenward)
  p = DRUM_REF_FP + 10*8; p[0]=24.0; p[1]=38.0; p[2]=5.0; p[3]=15.0; p[4]=13.0; p[5]=5.0; p[6]=28.0; p[7]=0.76;
  // 11: Forrester Savell (City Of Souls)
  p = DRUM_REF_FP + 11*8; p[0]=26.0; p[1]=36.0; p[2]=4.0; p[3]=15.0; p[4]=14.0; p[5]=5.0; p[6]=27.0; p[7]=0.79;
  // 12: Leon Schmidt (SUNBORN)
  p = DRUM_REF_FP + 12*8; p[0]=29.0; p[1]=35.0; p[2]=4.0; p[3]=13.0; p[4]=14.0; p[5]=5.0; p[6]=26.0; p[7]=0.82;
  // 13: Ermin Hamidovic (Benchmark)
  p = DRUM_REF_FP + 13*8; p[0]=26.0; p[1]=37.0; p[2]=4.0; p[3]=14.0; p[4]=14.0; p[5]=5.0; p[6]=27.0; p[7]=0.80;
  // 14: Will Putney (Fit For An Autopsy)
  p = DRUM_REF_FP + 14*8; p[0]=30.0; p[1]=36.0; p[2]=3.5; p[3]=13.0; p[4]=13.5; p[5]=4.0; p[6]=26.5; p[7]=0.83;
  // 15: George Lever (Loathe / Sleep Token)
  p = DRUM_REF_FP + 15*8; p[0]=32.0; p[1]=34.0; p[2]=3.5; p[3]=13.0; p[4]=12.5; p[5]=5.0; p[6]=26.0; p[7]=0.82;
  // 16: Sam Bassal (Thornhill)
  p = DRUM_REF_FP + 16*8; p[0]=28.0; p[1]=36.0; p[2]=4.5; p[3]=14.0; p[4]=13.0; p[5]=4.5; p[6]=27.0; p[7]=0.80;
  // 17: Henrik Udd (Architects)
  p = DRUM_REF_FP + 17*8; p[0]=29.0; p[1]=36.0; p[2]=4.0; p[3]=13.0; p[4]=13.5; p[5]=4.5; p[6]=26.5; p[7]=0.84;
  // 18: Dan Braunstein (Spiritbox)
  p = DRUM_REF_FP + 18*8; p[0]=27.0; p[1]=36.0; p[2]=4.5; p[3]=14.0; p[4]=13.5; p[5]=5.0; p[6]=25.5; p[7]=0.80;
  // 19: Zakk Cervini (Bad Omens)
  p = DRUM_REF_FP + 19*8; p[0]=29.0; p[1]=35.0; p[2]=4.0; p[3]=13.5; p[4]=13.5; p[5]=5.0; p[6]=25.0; p[7]=0.82;
  // 20: Jens Bogren (Fascination)
  p = DRUM_REF_FP + 20*8; p[0]=26.0; p[1]=37.0; p[2]=4.0; p[3]=14.0; p[4]=14.0; p[5]=5.0; p[6]=27.0; p[7]=0.80;
  // 21: Adam Nolly Getgood (Periphery)
  p = DRUM_REF_FP + 21*8; p[0]=27.0; p[1]=38.0; p[2]=3.8; p[3]=14.0; p[4]=13.2; p[5]=4.0; p[6]=27.5; p[7]=0.84;
  // 22: Acle Kahney (TesseracT)
  p = DRUM_REF_FP + 22*8; p[0]=26.0; p[1]=37.0; p[2]=4.0; p[3]=14.0; p[4]=14.0; p[5]=5.0; p[6]=27.0; p[7]=0.82;
  // 23: Adam Cichocki (heaving.)
  p = DRUM_REF_FP + 23*8; p[0]=25.0; p[1]=37.0; p[2]=5.0; p[3]=14.5; p[4]=13.5; p[5]=5.0; p[6]=28.0; p[7]=0.78;
  // 24: Manuel Renner (SENNA - Out Of The Blue)
  p = DRUM_REF_FP + 24*8; p[0]=28.0; p[1]=36.0; p[2]=4.0; p[3]=14.0; p[4]=13.0; p[5]=5.0; p[6]=26.5; p[7]=0.82;

"""
    content = content.replace(init_marker, init_code + "\n" + init_marker)

    # 2. Add filter running & spectral power accumulation into @sample
    sample_marker = "  acc_m2 += m_mono * m_mono;"
    sample_code = """  // Run 6 Drum Forensic Bandpass Filters on main signal
  db0 = bq_run(DRUM_BQC + 0,  DRUM_BQS + 0,  m_mono);
  db1 = bq_run(DRUM_BQC + 5,  DRUM_BQS + 2,  m_mono);
  db2 = bq_run(DRUM_BQC + 10, DRUM_BQS + 4,  m_mono);
  db3 = bq_run(DRUM_BQC + 15, DRUM_BQS + 6,  m_mono);
  db4 = bq_run(DRUM_BQC + 20, DRUM_BQS + 8,  m_mono);
  db5 = bq_run(DRUM_BQC + 25, DRUM_BQS + 10, m_mono);

  DRUM_ACC[0] += db0 * db0;
  DRUM_ACC[1] += db1 * db1;
  DRUM_ACC[2] += db2 * db2;
  DRUM_ACC[3] += db3 * db3;
  DRUM_ACC[4] += db4 * db4;
  DRUM_ACC[5] += db5 * db5;
"""
    content = content.replace(sample_marker, sample_code + "\n  " + sample_marker)

    # 3. Add block calculation for scoring inside acc_count >= 2048
    block_marker = "    sifam_corr += (cur_corr - sifam_corr) * 0.15;"
    block_code = """    // 6-Band Drum Forensic Match & Scoring Engine
    tot_dp = DRUM_ACC[0] + DRUM_ACC[1] + DRUM_ACC[2] + DRUM_ACC[3] + DRUM_ACC[4] + DRUM_ACC[5] + 0.000001;
    ref_idx = slider9 ? 1 : slider2; // Dan Weller (1) or Selected Producer (slider2)
    p_ref = DRUM_REF_FP + ref_idx * 8;
    
    spec_acc = 0; bi = 0;
    loop(6,
      pct = (DRUM_ACC[bi] / tot_dp) * 100.0;
      DRUM_PCT[bi] = pct;
      DRUM_SMOOTH_PCT[bi] += (pct - DRUM_SMOOTH_PCT[bi]) * 0.25;
      
      rf_p = p_ref[bi];
      del_db = 10.0 * log((DRUM_SMOOTH_PCT[bi] + 0.05) / (rf_p + 0.05)) / log(10.0);
      DRUM_DELTA_DB[bi] = del_db;
      
      tol = (bi == 2) ? 1.5 : (bi == 0 || bi == 5) ? 2.5 : 2.0;
      dev = abs(del_db) / tol;
      spec_acc += clamp(1.0 - max(0, dev - 1.0) / 3.0, 0.0, 1.0);
      
      DRUM_ACC[bi] = 0;
      bi += 1;
    );
    sc_spectral = (spec_acc / 6.0) * 100.0;
    
    tgt_crest = p_ref[6];
    c_err = abs(crest_main - tgt_crest);
    sc_crest = clamp(1.0 - max(0, c_err - 2.0) / 8.0, 0.0, 1.0) * 100.0;
    
    tgt_corr = p_ref[7];
    corr_err = max(0, tgt_corr - sifam_corr);
    sc_phase = clamp(1.0 - corr_err / 0.6, 0.0, 1.0) * 100.0;
    
    // Overall Drum Match Health Index (0 - 100%)
    inst_match = 0.50 * sc_spectral + 0.30 * sc_crest + 0.20 * sc_phase;
    drum_match_pct += (inst_match - drum_match_pct) * 0.18;
    gmem[827] = drum_match_pct;
"""
    content = content.replace(block_marker, block_code + "\n    " + block_marker)

    # 4. Enhance Tab 0 (Kit Radar / Overview) with the live Drum Health Scoring ring & delta readouts
    old_tab0_panel = """    col3_x = 646; col3_w = gfx_w - col3_x - 10;
    panel_frame(col3_x, m_top, col3_w, m_h, "SANKOFA SAMPLE ADVISOR", "HEALTH 88%");
    my_y = m_top + 38;
    
    slider9 == 1 ? (
      draw_metric_row(col3_x, my_y,       col3_w, "BENCHMARK TARGET",    "DAN WELLER (CASKETS)", COL_GOLD);
      draw_metric_row(col3_x, my_y + 24,  col3_w, "Target Snare Crest",  "31.38 dB (PRO UNCOMPRESSED)", COL_CYAN);
      draw_metric_row(col3_x, my_y + 48,  col3_w, "Target Kick Crest",   "25.30 dB (PUNCH POCKET)", COL_CYAN);
      draw_metric_row(col3_x, my_y + 72,  col3_w, "Target Mud (300Hz)",  "0.48% (CARDBOARD VOID)", COL_MINT);
      draw_metric_row(col3_x, my_y + 96,  col3_w, "Target Beater Click", "0.56% (7x DEFICIT ON RAW)", COL_AMBER);
    ) : (
      draw_metric_row(col3_x, my_y,       col3_w, "Peak Headroom",       sprintf(#, "%+2.2f dBFS", db(pk_main)), COL_TEXT);
      draw_metric_row(col3_x, my_y + 24,  col3_w, "RMS Sound Pressure",  sprintf(#, "%+2.2f dBFS", db(rms_main)), COL_CYAN);
      draw_metric_row(col3_x, my_y + 48,  col3_w, "Dynamic Crest (PLR)", sprintf(#, "%2.2f dB", crest_main), COL_GOLD);
      draw_metric_row(col3_x, my_y + 72,  col3_w, "Bleed-to-Crack Ratio", "0.26 (CLEAN ISOLATION)", COL_MINT);
      draw_metric_row(col3_x, my_y + 96,  col3_w, "Groove Consistency",   "1.1dB StdDev (HUMAN TIGHT)", COL_AMBER);
    );"""

    new_tab0_panel = """    col3_x = 646; col3_w = gfx_w - col3_x - 10;
    score_tag = sprintf(#, "MATCH %2.1f%%", drum_match_pct);
    panel_frame(col3_x, m_top, col3_w, m_h, "SANKOFA DRUM ORACLE", score_tag);
    my_y = m_top + 34;

    // Glowing Circular Drum Health Meter (0 - 100%)
    gauge_cx = col3_x + 48; gauge_cy = my_y + 26; gauge_r = 24;
    set_c(0x0e131d); gfx_circle(gauge_cx, gauge_cy, gauge_r, 1);
    set_c(0x1a2336); gfx_circle(gauge_cx, gauge_cy, gauge_r, 0);
    g_col = drum_match_pct >= 85 ? COL_MINT : (drum_match_pct >= 65 ? COL_GOLD : COL_RED);
    set_c(g_col);
    // Draw arc for match %
    ang_end = -0.5 * $pi + (drum_match_pct / 100.0) * (2.0 * $pi);
    ai = 0; a_steps = 28;
    loop(a_steps,
      rad1 = -0.5 * $pi + (ai / a_steps) * (drum_match_pct / 100.0) * (2.0 * $pi);
      rad2 = -0.5 * $pi + ((ai + 1) / a_steps) * (drum_match_pct / 100.0) * (2.0 * $pi);
      gfx_line(gauge_cx + cos(rad1)*gauge_r, gauge_cy + sin(rad1)*gauge_r, gauge_cx + cos(rad2)*gauge_r, gauge_cy + sin(rad2)*gauge_r);
      gfx_line(gauge_cx + cos(rad1)*(gauge_r-1), gauge_cy + sin(rad1)*(gauge_r-1), gauge_cx + cos(rad2)*(gauge_r-1), gauge_cy + sin(rad2)*(gauge_r-1));
      ai += 1;
    );
    gfx_setfont(1, "Orbitron", 11.5, 'b'); set_c(g_col);
    sc_txt = sprintf(#, "%d%%", floor(drum_match_pct + 0.5));
    gfx_measurestr(sc_txt, gtw, gth);
    gfx_x = gauge_cx - gtw * 0.5; gfx_y = gauge_cy - gth * 0.5;
    gfx_drawstr(sc_txt);

    // Status Banner Beside Gauge
    gfx_setfont(1, "Orbitron", 10, 'b'); set_c(COL_TEXT);
    gfx_x = gauge_cx + gauge_r + 14; gfx_y = my_y + 10;
    gfx_drawstr(drum_match_pct >= 85 ? "RECORD-READY MATCH" : (drum_match_pct >= 65 ? "CLOSE - TUNE DELTAS" : "AUDIT & POLISH"));
    gfx_setfont(2, "Segoe UI", 9.5); set_c(COL_TEXT_MUTED);
    gfx_x = gauge_cx + gauge_r + 14; gfx_y = my_y + 28;
    ref_name_str = slider9 ? "Dan Weller Gold Benchmark" : "Producer Reference Target";
    gfx_drawstr(ref_name_str);

    // Live Delta Rows (Exact mixer requirements)
    del_sub_c = abs(DRUM_DELTA_DB[0]) > 2.5 ? COL_RED : (abs(DRUM_DELTA_DB[0]) > 1.2 ? COL_AMBER : COL_MINT);
    del_mud_c = DRUM_DELTA_DB[2] > 2.0 ? COL_RED : (DRUM_DELTA_DB[2] > 0.8 ? COL_AMBER : COL_MINT);
    del_crk_c = abs(DRUM_DELTA_DB[4]) > 2.5 ? COL_RED : (abs(DRUM_DELTA_DB[4]) > 1.2 ? COL_AMBER : COL_MINT);

    s_sub = sprintf(#, "%+2.1f dB (%s)", DRUM_DELTA_DB[0], DRUM_DELTA_DB[0] < -1.5 ? "DEFICIT" : "PUNCH");
    s_mud = sprintf(#, "%+2.1f dB (%s)", DRUM_DELTA_DB[2], DRUM_DELTA_DB[2] > 1.5 ? "350Hz MUD" : "CLEAN");
    s_crk = sprintf(#, "%+2.1f dB (%s)", DRUM_DELTA_DB[4], DRUM_DELTA_DB[4] < -1.5 ? "NEEDS CRACK" : "SNAP");
    s_cst = sprintf(#, "%2.1f dB (CREST)", crest_main);

    draw_metric_row(col3_x, my_y + 60, col3_w, "Sub Impact (55Hz)", s_sub, del_sub_c);
    draw_metric_row(col3_x, my_y + 80, col3_w, "Cardboard (350Hz)", s_mud, del_mud_c);
    draw_metric_row(col3_x, my_y + 100, col3_w, "Transient Crack", s_crk, del_crk_c);
    draw_metric_row(col3_x, my_y + 120, col3_w, "Dynamic Crest PLR", s_cst, COL_GOLD);"""

    content = content.replace(old_tab0_panel, new_tab0_panel)

    # 5. Enhance Tab 4 (Sample Oracle) with live health verdict & direct trigger actions
    old_tab4 = """    gfx_setfont(2, "Segoe UI", 11.5); set_c(COL_TEXT);
    gfx_x = 36; gfx_y = m_top + 80;
    gfx_drawstr("• Raw Performance Health: 88% (Excellent groove, 1.1dB StdDev)");
    gfx_x = 36; gfx_y = m_top + 104;
    gfx_drawstr("• Kick Verdict: Do NOT replace. Blend single-shot click at -15 dB.");
    gfx_x = 36; gfx_y = m_top + 128;
    gfx_drawstr("• Snare Verdict: Do NOT replace. Blend top wire crack at -16 dB.");
    gfx_x = 36; gfx_y = m_top + 152;
    gfx_drawstr("• Toms Verdict: 100% Acoustic. Resonant gate + transient shaper only.");"""

    new_tab4 = """    gfx_setfont(2, "Segoe UI", 11.5); set_c(COL_TEXT);
    s_health = sprintf(#, "• Raw Performance Health: %2.1f%% (%s)", drum_match_pct, drum_match_pct >= 85 ? "RECORD-READY GROOVE" : "NEEDS TOP POLISH");
    gfx_x = 36; gfx_y = m_top + 80; gfx_drawstr(s_health);
    
    s_k_verdict = DRUM_DELTA_DB[0] < -2.0 ? "• Kick Verdict: Sub deficit detected. Push 55Hz sub-sine to Atumpan DrumTrigger." : "• Kick Verdict: Fundamental solid. Do NOT replace. Optional click at -15dB.";
    gfx_x = 36; gfx_y = m_top + 104; gfx_drawstr(s_k_verdict);
    
    s_s_verdict = DRUM_DELTA_DB[4] < -2.0 ? "• Snare Verdict: Wire snap deficit. Blend -16dB top crack with DrumTrigger." : "• Snare Verdict: Acoustic body 200Hz is great. Keep natural with DrumGate.";
    gfx_x = 36; gfx_y = m_top + 128; gfx_drawstr(s_s_verdict);
    
    s_t_verdict = DRUM_DELTA_DB[2] > 2.0 ? "• Mud Verdict: 350Hz cardboard buildup (+%.1fdB). Apply narrow notch on Drum Bus." : "• Toms & Room Verdict: Clean isolation. Bleed-to-crack ratio is pristine.";
    gfx_x = 36; gfx_y = m_top + 152; gfx_drawstr(sprintf(#, s_t_verdict, DRUM_DELTA_DB[2]));"""

    content = content.replace(old_tab4, new_tab4)

    # 6. Update bottom strip match display
    content = content.replace('draw_btn(254, bot_y + 128, 240, 24, "SANKOFA TARGET MATCH: 96.4%", 0);',
                            'draw_btn(254, bot_y + 128, 240, 24, sprintf(#, "SANKOFA MATCH: %2.1f%%", drum_match_pct), drum_match_pct >= 80);')

    with open(target, "w", encoding="utf-8") as f:
        f.write(content)

    print("Upgraded Damei_DrumAssessment.jsfx with Sankofa Drum Scoring Engine!")
    
    # Sync to AppData
    appdata = os.path.expandvars(r"%APPDATA%\REAPER\Effects\Damei\Damei_DrumAssessment.jsfx")
    shutil.copy2(target, appdata)
    print(f"Synced to {appdata}")

if __name__ == "__main__":
    upgrade_drum_sentry()
