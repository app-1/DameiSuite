# patch_bass_trackspacer.py
import sys, re, os, shutil

src = r"c:\Dev\DameiAPI\reaper_scripts\Damei_BassSuite.jsfx"
with open(src, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update slider1
old_s1 = "slider1:0<0,5,1{Bass Folder Overview,Sub Anchor & Kick Pocket,3-Way Crossover Sculptor,Phase Alignment & Correlation,Smash & Grab + Decapitator Rack,Producer Matrix & Session Blueprints}>-Active Module"
new_s1 = "slider1:0<0,6,1{Bass Folder Overview,Trackspacer Dynamic Inverse EQ,Sub Anchor & Kick Pocket,3-Way Crossover Sculptor,Phase Alignment & Correlation,Smash & Grab + Decapitator Rack,Producer Matrix & Session Blueprints}>-Active Module"

assert old_s1 in code, "slider1 definition not found"
code = code.replace(old_s1, new_s1, 1)

# 2. Add Trackspacer sliders after slider44
old_s44 = "slider44:8500<3000,18000,500>-Decapitator High Cut (Hz)\n"
new_sliders = """slider44:8500<3000,18000,500>-Decapitator High Cut (Hz)
// =============================================================================
// TRACKSPACER (WAVESFACTORY MODELED DYNAMIC INVERSE EQUALIZER)
// =============================================================================
slider45:1<0,1,1{Bypassed,Active Dynamic Inverse EQ}>-Trackspacer Engine Master Toggle
slider46:35<0,100,1>-Trackspacer Ducking Amount (%)
slider47:35<20,800,5>-Trackspacer Low Cut Filter (Hz)
slider48:650<100,16000,20>-Trackspacer High Cut Filter (Hz)
slider49:15<1,100,1>-Trackspacer Attack Time (ms)
slider50:65<10,400,5>-Trackspacer Release Time (ms)
slider51:0<0,2,1{Mid Channel (Center),Stereo Linked (L/R),Side Channel (Stereo)}> -Trackspacer Processing Mode
slider52:0<0,2,1{Normal Passthrough,Audition Kick Sidechain,Audition Carved Delta}>-Trackspacer Audition Mode
"""
assert old_s44 in code, "slider44 not found"
code = code.replace(old_s44, new_sliders, 1)

# 3. Add serialization
old_ser = "file_var(0, slider40); file_var(0, slider41); file_var(0, slider42); file_var(0, slider43); file_var(0, slider44);"
new_ser = """file_var(0, slider40); file_var(0, slider41); file_var(0, slider42); file_var(0, slider43); file_var(0, slider44);
file_var(0, slider45); file_var(0, slider46); file_var(0, slider47); file_var(0, slider48);
file_var(0, slider49); file_var(0, slider50); file_var(0, slider51); file_var(0, slider52);"""
assert old_ser in code, "slider40..44 serialize not found"
code = code.replace(old_ser, new_ser, 1)

# 4. Add Trackspacer State & Filter definitions in @init
init_marker = "ext_noinit = 1.0;"
ts_init = """ext_noinit = 1.0;

// =============================================================================
// TRACKSPACER DYNAMIC INVERSE EQ STATE & FILTER INITIALIZATION
// =============================================================================
ts_num_bands = 8;
ts_freqs = 30000;
ts_freqs[0] = 42;  ts_freqs[1] = 68;  ts_freqs[2] = 110; ts_freqs[3] = 180;
ts_freqs[4] = 300; ts_freqs[5] = 600; ts_freqs[6] = 1400; ts_freqs[7] = 3200;

ts_sc_env = 30020;    // live kick sidechain envelope per band (0..7)
ts_gr_db  = 30040;    // live dynamic gain reduction per band (0..7)
ts_smooth_gr = 30060; // smoothed GR per band
ts_band_wt   = 30080; // window weight (low cut -> high cut)

// Biquad state arrays for 8 bands:
// Sidechain Bandpass: sc_bp_x1, sc_bp_x2, sc_bp_y1, sc_bp_y2
ts_sc_x1 = 30100; ts_sc_x2 = 30120; ts_sc_y1 = 30140; ts_sc_y2 = 30160;
// Dynamic Peaking EQ (Mid / Left): eq_x1_l, eq_x2_l, eq_y1_l, eq_y2_l
ts_eq_x1_l = 30200; ts_eq_x2_l = 30220; ts_eq_y1_l = 30240; ts_eq_y2_l = 30260;
// Dynamic Peaking EQ (Right channel for stereo mode): eq_x1_r, eq_x2_r, eq_y1_r, eq_y2_r
ts_eq_x1_r = 30300; ts_eq_x2_r = 30320; ts_eq_y1_r = 30340; ts_eq_y2_r = 30360;

ts_max_gr_live = 0.0;
ts_avg_gr_live = 0.0;

ti_init = 0;
loop(ts_num_bands,
  ts_sc_env[ti_init] = 0.0;
  ts_gr_db[ti_init] = 0.0;
  ts_smooth_gr[ti_init] = 0.0;
  ts_band_wt[ti_init] = 1.0;
  ts_sc_x1[ti_init] = 0; ts_sc_x2[ti_init] = 0; ts_sc_y1[ti_init] = 0; ts_sc_y2[ti_init] = 0;
  ts_eq_x1_l[ti_init] = 0; ts_eq_x2_l[ti_init] = 0; ts_eq_y1_l[ti_init] = 0; ts_eq_y2_l[ti_init] = 0;
  ts_eq_x1_r[ti_init] = 0; ts_eq_x2_r[ti_init] = 0; ts_eq_y1_r[ti_init] = 0; ts_eq_y2_r[ti_init] = 0;
  ti_init += 1;
);
"""
assert init_marker in code, "ext_noinit marker not found"
code = code.replace(init_marker, ts_init, 1)

# 5. Add update_trackspacer_filters()
filter_func_marker = "function update_bass_filters() ("
ts_filter_code = """function update_trackspacer_filters() local(bi, f, w_lo, w_hi) (
  ts_att_c = exp(-1.0 / (max(0.001, slider49 * 0.001) * srate));
  ts_rel_c = exp(-1.0 / (max(0.010, slider50 * 0.001) * srate));

  bi = 0;
  loop(ts_num_bands,
    f = ts_freqs[bi];
    w_lo = 1.0 / (1.0 + sqr(max(20.0, slider47) / f) * sqr(max(20.0, slider47) / f));
    w_hi = 1.0 / (1.0 + sqr(f / max(100.0, slider48)) * sqr(f / max(100.0, slider48)));
    ts_band_wt[bi] = w_lo * w_hi;
    bi += 1;
  );
);

"""
assert filter_func_marker in code
code = code.replace(filter_func_marker, ts_filter_code + filter_func_marker, 1)

# Add update_trackspacer_filters() call inside update_bass_filters()
update_call_marker = "update_bass_filters();\n"
code = code.replace(update_call_marker, "update_bass_filters();\nupdate_trackspacer_filters();\n", 1)

# In apply_bass_preset, add trackspacer preset calibrations
p15_marker = "p_idx == 15 ? ("
ts_p15 = """p_idx == 15 ? (
    // Trackspacer Dan Braunstein Signature Pocket Calibration
    slider45 = 1;  // Trackspacer Active
    slider46 = 35; // 35% Dynamic Carve
    slider47 = 35; // 35 Hz Low Cut
    slider48 = 650;// 650 Hz High Cut (leaves bass upper bite intact)
    slider49 = 15; // 15ms Fast Clamp Attack
    slider50 = 65; // 65ms Musical Decay
    slider51 = 0;  // Mid-Only (protects stereo width)
    slider52 = 0;  // Normal
"""
assert p15_marker in code
code = code.replace(p15_marker, ts_p15, 1)

# 6. Add Trackspacer DSP in @sample
# We place it right around line 455 where mid and side are calculated, before sub and top filters
sample_marker = "slider34 ? (\n  s_l = mid + hp_side;\n  s_r = mid - hp_side;\n);"
ts_sample_code = """slider34 ? (
  s_l = mid + hp_side;
  s_r = mid - hp_side;
);

// =============================================================================
// TRACKSPACER DYNAMIC INVERSE EQUALIZER DSP ENGINE
// =============================================================================
slider45 ? (
  // 1. Obtain Sidechain Kick Signal
  slider9 == 0 ? (
    ts_kick_sig = (spl2 + spl3) * 0.5;
  ) : (
    ts_kick_sig = exp(gmem[825] * 0.11512925);
  );

  ts_max_gr_live = 0.0;
  ts_tot_gr = 0.0;
  ts_delta_m = 0.0;

  // Mid/Side split of incoming signal
  ts_mid = (s_l + s_r) * 0.5;
  ts_side = (s_l - s_r) * 0.5;
  ts_orig_mid = ts_mid;
  ts_orig_l = s_l;
  ts_orig_r = s_r;

  ts_b = 0;
  loop(ts_num_bands,
    ts_fc = ts_freqs[ts_b];

    // 2. Sidechain 2nd-Order Bandpass Detector
    ts_w0 = 2.0 * $pi * ts_fc / srate;
    ts_sin = sin(ts_w0); ts_cos = cos(ts_w0);
    ts_alpha = ts_sin / (2.0 * 1.5); // Q = 1.5
    ts_b0_bp = ts_alpha;
    ts_b1_bp = 0.0;
    ts_b2_bp = -ts_alpha;
    ts_a0_bp = 1.0 + ts_alpha;
    ts_a1_bp = -2.0 * ts_cos;
    ts_a2_bp = 1.0 - ts_alpha;

    ts_sc_out = (ts_b0_bp * ts_kick_sig + ts_b1_bp * ts_sc_x1[ts_b] + ts_b2_bp * ts_sc_x2[ts_b] - ts_a1_bp * ts_sc_y1[ts_b] - ts_a2_bp * ts_sc_y2[ts_b]) / ts_a0_bp;
    ts_sc_x2[ts_b] = ts_sc_x1[ts_b]; ts_sc_x1[ts_b] = ts_kick_sig;
    ts_sc_y2[ts_b] = ts_sc_y1[ts_b]; ts_sc_y1[ts_b] = ts_sc_out;

    // 3. Dynamic Ballistics & Envelope
    ts_sc_mag = abs(ts_sc_out);
    ts_sc_env[ts_b] = (ts_sc_mag > ts_sc_env[ts_b]) ? (ts_sc_env[ts_b] * ts_att_c + ts_sc_mag * (1.0 - ts_att_c)) : (ts_sc_env[ts_b] * ts_rel_c);

    // 4. Calculate Dynamic Inverse Notch Gain (dB)
    ts_sc_db = ts_sc_env[ts_b] > 0.00001 ? 20.0 * log10(ts_sc_env[ts_b]) : -90.0;
    ts_kick_over = max(0.0, ts_sc_db - (-28.0));
    ts_target_gr = -min(12.0, ts_kick_over * (slider46 * 0.01) * 0.65) * ts_band_wt[ts_b];
    ts_smooth_gr[ts_b] = ts_smooth_gr[ts_b] * 0.88 + ts_target_gr * 0.12;
    ts_gr_db[ts_b] = ts_smooth_gr[ts_b];

    ts_max_gr_live = min(ts_max_gr_live, ts_gr_db[ts_b]);
    ts_tot_gr += ts_gr_db[ts_b];

    // 5. Apply Dynamic Inverse Notch Filter to Bass
    abs(ts_gr_db[ts_b]) > 0.05 ? (
      ts_A = exp(ts_gr_db[ts_b] * 0.05756462); // 10^(dB/40)
      ts_a0_eq = 1.0 + ts_alpha / ts_A;
      ts_b0_eq = (1.0 + ts_alpha * ts_A) / ts_a0_eq;
      ts_b1_eq = (-2.0 * ts_cos) / ts_a0_eq;
      ts_b2_eq = (1.0 - ts_alpha * ts_A) / ts_a0_eq;
      ts_a1_eq = (-2.0 * ts_cos) / ts_a0_eq;
      ts_a2_eq = (1.0 - ts_alpha / ts_A) / ts_a0_eq;

      // Channel mode: 0=Mid Only, 1=Stereo, 2=Side Only
      slider51 == 0 ? (
        ts_m_out = ts_b0_eq * ts_mid + ts_b1_eq * ts_eq_x1_l[ts_b] + ts_b2_eq * ts_eq_x2_l[ts_b] - ts_a1_eq * ts_eq_y1_l[ts_b] - ts_a2_eq * ts_eq_y2_l[ts_b];
        ts_eq_x2_l[ts_b] = ts_eq_x1_l[ts_b]; ts_eq_x1_l[ts_b] = ts_mid;
        ts_eq_y2_l[ts_b] = ts_eq_y1_l[ts_b]; ts_eq_y1_l[ts_b] = ts_m_out;
        ts_mid = ts_m_out;
      ) : slider51 == 1 ? (
        ts_l_out = ts_b0_eq * s_l + ts_b1_eq * ts_eq_x1_l[ts_b] + ts_b2_eq * ts_eq_x2_l[ts_b] - ts_a1_eq * ts_eq_y1_l[ts_b] - ts_a2_eq * ts_eq_y2_l[ts_b];
        ts_eq_x2_l[ts_b] = ts_eq_x1_l[ts_b]; ts_eq_x1_l[ts_b] = s_l;
        ts_eq_y2_l[ts_b] = ts_eq_y1_l[ts_b]; ts_eq_y1_l[ts_b] = ts_l_out;
        s_l = ts_l_out;

        ts_r_out = ts_b0_eq * s_r + ts_b1_eq * ts_eq_x1_r[ts_b] + ts_b2_eq * ts_eq_x2_r[ts_b] - ts_a1_eq * ts_eq_y1_r[ts_b] - ts_a2_eq * ts_eq_y2_r[ts_b];
        ts_eq_x2_r[ts_b] = ts_eq_x1_r[ts_b]; ts_eq_x1_r[ts_b] = s_r;
        ts_eq_y2_r[ts_b] = ts_eq_y1_r[ts_b]; ts_eq_y1_r[ts_b] = ts_r_out;
        s_r = ts_r_out;
      ) : (
        ts_s_out = ts_b0_eq * ts_side + ts_b1_eq * ts_eq_x1_l[ts_b] + ts_b2_eq * ts_eq_x2_l[ts_b] - ts_a1_eq * ts_eq_y1_l[ts_b] - ts_a2_eq * ts_eq_y2_l[ts_b];
        ts_eq_x2_l[ts_b] = ts_eq_x1_l[ts_b]; ts_eq_x1_l[ts_b] = ts_side;
        ts_eq_y2_l[ts_b] = ts_eq_y1_l[ts_b]; ts_eq_y1_l[ts_b] = ts_s_out;
        ts_side = ts_s_out;
      );
    );

    ts_b += 1;
  );

  slider51 == 0 ? (
    ts_delta_m = ts_orig_mid - ts_mid;
    s_l = ts_mid + ts_side;
    s_r = ts_mid - ts_side;
  ) : slider51 == 2 ? (
    ts_delta_m = ts_orig_mid - (ts_mid);
    s_l = ts_mid + ts_side;
    s_r = ts_mid - ts_side;
  ) : (
    ts_delta_m = ((ts_orig_l + ts_orig_r) - (s_l + s_r)) * 0.5;
  );

  // Audition Modes:
  // 1 = Audition Kick Sidechain Detector
  // 2 = Audition Dynamic Carve Delta (what is being removed from bass)
  slider52 == 1 ? (
    s_l = ts_kick_sig;
    s_r = ts_kick_sig;
  ) : slider52 == 2 ? (
    s_l = ts_delta_m;
    s_r = ts_delta_m;
  );
);
"""
assert sample_marker in code, "sample_marker not found"
code = code.replace(sample_marker, ts_sample_code, 1)

# 7. Update Navigation Tabs in @gfx
# Change loop(6) to loop(7) and update tab names
old_tab_loop = """tab_w = floor((gfx_w - 28) / 6);
ti = 0;
loop(6,
  tx = 14 + ti * tab_w;
  is_sel = (slider1 == ti);
  is_hov = (mouse_x >= tx && mouse_x <= tx + tab_w && mouse_y >= tab_y && mouse_y <= tab_y + tab_h);

  gfx_r = is_sel ? 0.06 : (is_hov ? 0.04 : 0.022);
  gfx_g = is_sel ? 0.16 : (is_hov ? 0.09 : 0.032);
  gfx_b = is_sel ? 0.14 : (is_hov ? 0.08 : 0.040);
  gfx_rect(tx, tab_y, tab_w, tab_h);

  is_sel ? (
    gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50;
    gfx_line(tx, tab_y + tab_h - 2, tx + tab_w, tab_y + tab_h - 2);
    gfx_line(tx, tab_y + tab_h - 1, tx + tab_w, tab_y + tab_h - 1);
  );

  gfx_setfont(1, "Orbitron", 12.5, 'b');
  gfx_r = is_sel ? 0.15 : (is_hov ? 0.50 : 0.40);
  gfx_g = is_sel ? 0.96 : (is_hov ? 0.80 : 0.60);
  gfx_b = is_sel ? 0.60 : (is_hov ? 0.70 : 0.55);

  t_name = (
    ti == 0 ? "Folder Overview" :
    ti == 1 ? "Sub Anchor & Pocket" :
    ti == 2 ? "3-Way Crossover" :
    ti == 3 ? "Phase Alignment" :
    ti == 4 ? "Analog Glue" :
    "Producer Matrix"
  );"""

new_tab_loop = """tab_w = floor((gfx_w - 28) / 7);
ti = 0;
loop(7,
  tx = 14 + ti * tab_w;
  is_sel = (slider1 == ti);
  is_hov = (mouse_x >= tx && mouse_x <= tx + tab_w && mouse_y >= tab_y && mouse_y <= tab_y + tab_h);

  gfx_r = is_sel ? 0.06 : (is_hov ? 0.04 : 0.022);
  gfx_g = is_sel ? 0.16 : (is_hov ? 0.09 : 0.032);
  gfx_b = is_sel ? 0.14 : (is_hov ? 0.08 : 0.040);
  gfx_rect(tx, tab_y, tab_w, tab_h);

  is_sel ? (
    gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50;
    gfx_line(tx, tab_y + tab_h - 2, tx + tab_w, tab_y + tab_h - 2);
    gfx_line(tx, tab_y + tab_h - 1, tx + tab_w, tab_y + tab_h - 1);
  );

  gfx_setfont(1, "Orbitron", 11.5, 'b');
  gfx_r = is_sel ? 0.15 : (is_hov ? 0.50 : 0.40);
  gfx_g = is_sel ? 0.96 : (is_hov ? 0.80 : 0.60);
  gfx_b = is_sel ? 0.60 : (is_hov ? 0.70 : 0.55);

  t_name = (
    ti == 0 ? "Overview" :
    ti == 1 ? "Trackspacer EQ" :
    ti == 2 ? "Sub Anchor" :
    ti == 3 ? "3-Way Split" :
    ti == 4 ? "Phase Radar" :
    ti == 5 ? "Analog Glue" :
    "Producer Matrix"
  );"""

assert old_tab_loop in code, "old_tab_loop not found"
code = code.replace(old_tab_loop, new_tab_loop, 1)

# Shift existing tabs 1..5 to 2..6
# We must do this from 5 down to 1 so we don't accidentally cascade
code = code.replace("slider1 == 5 ?", "slider1 == 6 ?")
code = code.replace("slider1 == 4 ?", "slider1 == 5 ?")
code = code.replace("slider1 == 3 ?", "slider1 == 4 ?")
code = code.replace("slider1 == 2 ?", "slider1 == 3 ?")
code = code.replace("slider1 == 1 ?", "slider1 == 2 ?")

# 8. Now insert TAB 1: TRACKSPACER DYNAMIC INVERSE EQUALIZER before TAB 2
tab2_marker = "// =============================================================================\n// TAB 1: SUB ANCHOR & KICK POCKET ENGINE (OSCILLOSCOPE COLLISION DISPLAY)"
trackspacer_tab_gui = """// =============================================================================
// TAB 1: WAVESFACTORY TRACKSPACER DYNAMIC INVERSE EQUALIZER RACK
// =============================================================================
slider1 == 1 ? (
  ts_y = disp_y; ts_h = disp_h; ts_w = disp_w;
  gfx_r = 0.020; gfx_g = 0.028; gfx_b = 0.036; gfx_rect(disp_x, ts_y, ts_w, ts_h);
  gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50; gfx_rect(disp_x, ts_y, ts_w, ts_h, 0);

  // Top Section: Title & Master Toggle Pill
  gfx_setfont(1, "Orbitron", 16, 'b'); gfx_r = 0.15; gfx_g = 0.96; gfx_b = 0.60;
  gfx_x = disp_x + 16; gfx_y = ts_y + 12;
  gfx_drawstr("WAVESFACTORY TRACKSPACER // DYNAMIC INVERSE EQUALIZER");

  gfx_setfont(1, "Consolas", 12.5, 'b'); gfx_r = 0.70; gfx_g = 0.85; gfx_b = 0.88;
  gfx_x = disp_x + 16; gfx_y = ts_y + 34;
  gfx_drawstr("Real-time 32-point spectral carve-out: Dynamically notches bass ONLY when and where kick strikes.");

  // Master Engine Toggle Pill (Top Right)
  tog_w = 140; tog_h = 28; tog_x = disp_x + ts_w - tog_w - 16; tog_y = ts_y + 12;
  tog_hov = (mouse_x >= tog_x && mouse_x <= tog_x + tog_w && mouse_y >= tog_y && mouse_y <= tog_y + tog_h);
  gfx_r = slider45 ? 0.06 : 0.22; gfx_g = slider45 ? 0.24 : 0.08; gfx_b = slider45 ? 0.16 : 0.08;
  gfx_rect(tog_x, tog_y, tog_w, tog_h);
  gfx_r = slider45 ? 0.06 : 0.98; gfx_g = slider45 ? 0.88 : 0.22; gfx_b = slider45 ? 0.50 : 0.22;
  gfx_rect(tog_x, tog_y, tog_w, tog_h, 0);
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  tog_txt = slider45 ? "● TRACKSPACER: ON" : "○ BYPASSED";
  gfx_measurestr(tog_txt, tgw, tgh);
  gfx_x = tog_x + (tog_w - tgw) * 0.5; gfx_y = tog_y + 7; gfx_drawstr(tog_txt);
  mouse_clicked && tog_hov ? (slider45 = !slider45; slider_automate(););

  // Layout: Left/Center Main Spectrum Visualizer (64% width), Right Dial Rack (36% width)
  spec_w = floor((ts_w - 44) * 0.65);
  spec_h = ts_h - 160;
  spec_x = disp_x + 16;
  spec_y = ts_y + 58;

  rack_x = spec_x + spec_w + 12;
  rack_w = ts_w - spec_w - 44;
  rack_h = spec_h;
  rack_y = spec_y;

  // ---------------------------------------------------------------------------
  // 1. DYNAMIC INVERSE SPECTRUM SCOPE (WAVESFACTORY STYLE)
  // ---------------------------------------------------------------------------
  gfx_r = 0.012; gfx_g = 0.018; gfx_b = 0.024; gfx_rect(spec_x, spec_y, spec_w, spec_h);
  gfx_r = 0.14; gfx_g = 0.28; gfx_b = 0.32; gfx_rect(spec_x, spec_y, spec_w, spec_h, 0);

  // Frequency grid lines (20Hz, 50Hz, 100Hz, 250Hz, 500Hz, 1kHz, 3kHz, 10kHz)
  grid_f = 0;
  loop(8,
    g_hz = (grid_f == 0 ? 20 : grid_f == 1 ? 50 : grid_f == 2 ? 100 : grid_f == 3 ? 250 : grid_f == 4 ? 500 : grid_f == 5 ? 1000 : grid_f == 6 ? 3000 : 10000);
    g_frac = (log(g_hz) - log(20.0)) / (log(20000.0) - log(20.0));
    gx = spec_x + floor(g_frac * spec_w);
    gfx_r = 0.04; gfx_g = 0.08; gfx_b = 0.12; gfx_line(gx, spec_y + 1, gx, spec_y + spec_h - 18);
    gfx_setfont(1, "Consolas", 10, 'b'); gfx_r = 0.25; gfx_g = 0.40; gfx_b = 0.45;
    g_lbl = (g_hz >= 1000 ? sprintf(#, "%dk", g_hz / 1000) : sprintf(#, "%d", g_hz));
    gfx_x = gx - 8; gfx_y = spec_y + spec_h - 15; gfx_drawstr(g_lbl);
    grid_f += 1;
  );

  // dB Grid (0dB baseline at 40px down, -3dB, -6dB, -12dB)
  zero_db_y = spec_y + 45;
  gfx_r = 0.08; gfx_g = 0.18; gfx_b = 0.22;
  gfx_line(spec_x, zero_db_y, spec_x + spec_w, zero_db_y);
  gfx_setfont(1, "Consolas", 10, 'b'); gfx_r = 0.35; gfx_g = 0.60; gfx_b = 0.65;
  gfx_x = spec_x + 6; gfx_y = zero_db_y - 12; gfx_drawstr("0 dB");

  d6_y = zero_db_y + floor((spec_h - 70) * 0.45);
  gfx_r = 0.03; gfx_g = 0.07; gfx_b = 0.10; gfx_line(spec_x, d6_y, spec_x + spec_w, d6_y);
  gfx_x = spec_x + 6; gfx_y = d6_y - 6; gfx_drawstr("-6 dB");

  d12_y = zero_db_y + floor((spec_h - 70) * 0.90);
  gfx_r = 0.03; gfx_g = 0.07; gfx_b = 0.10; gfx_line(spec_x, d12_y, spec_x + spec_w, d12_y);
  gfx_x = spec_x + 6; gfx_y = d12_y - 6; gfx_drawstr("-12 dB");

  // Shaded Low Cut Curtain (0 to Low Cut)
  lc_frac = max(0.0, min(1.0, (log(max(20.0, slider47)) - log(20.0)) / (log(20000.0) - log(20.0))));
  lc_x = spec_x + floor(lc_frac * spec_w);
  gfx_r = 0.01; gfx_g = 0.01; gfx_b = 0.02; gfx_a = 0.70;
  gfx_rect(spec_x + 1, spec_y + 1, lc_x - spec_x, spec_h - 18);
  gfx_a = 1.0;
  // Low Cut Vertical Boundary Line
  gfx_r = 0.98; gfx_g = 0.35; gfx_b = 0.20;
  gfx_line(lc_x, spec_y + 1, lc_x, spec_y + spec_h - 18);
  gfx_line(lc_x + 1, spec_y + 1, lc_x + 1, spec_y + spec_h - 18);
  gfx_setfont(1, "Orbitron", 10.5, 'b'); gfx_r = 0.98; gfx_g = 0.55; gfx_b = 0.30;
  lc_str = sprintf(#, "LOW CUT %dHz", slider47);
  gfx_measurestr(lc_str, lcw, lch);
  gfx_x = max(spec_x + 4, lc_x - lcw - 4); gfx_y = spec_y + 8; gfx_drawstr(lc_str);

  // Shaded High Cut Curtain (High Cut to 20kHz)
  hc_frac = max(0.0, min(1.0, (log(min(20000.0, slider48)) - log(20.0)) / (log(20000.0) - log(20.0))));
  hc_x = spec_x + floor(hc_frac * spec_w);
  gfx_r = 0.01; gfx_g = 0.01; gfx_b = 0.02; gfx_a = 0.70;
  gfx_rect(hc_x, spec_y + 1, spec_x + spec_w - hc_x, spec_h - 18);
  gfx_a = 1.0;
  // High Cut Vertical Boundary Line
  gfx_r = 0.00; gfx_g = 0.92; gfx_b = 0.85;
  gfx_line(hc_x, spec_y + 1, hc_x, spec_y + spec_h - 18);
  gfx_line(hc_x + 1, spec_y + 1, hc_x + 1, spec_y + spec_h - 18);
  gfx_setfont(1, "Orbitron", 10.5, 'b'); gfx_r = 0.00; gfx_g = 0.92; gfx_b = 0.85;
  hc_str = sprintf(#, "HIGH CUT %dHz", slider48);
  gfx_x = min(spec_x + spec_w - 90, hc_x + 6); gfx_y = spec_y + 8; gfx_drawstr(hc_str);

  // Active Carve Zone Ribbon at Top
  gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50; gfx_a = 0.15;
  gfx_rect(lc_x, spec_y + 1, hc_x - lc_x, 20);
  gfx_a = 1.0;
  gfx_setfont(1, "Orbitron", 11, 'b'); gfx_r = 0.40; gfx_g = 1.00; gfx_b = 0.70;
  cz_txt = "● ACTIVE DYNAMIC INVERSE CARVE ZONE";
  gfx_measurestr(cz_txt, czw, czh);
  gfx_x = lc_x + max(4, floor((hc_x - lc_x - czw) * 0.5)); gfx_y = spec_y + 4;
  (hc_x - lc_x > czw + 10) ? gfx_drawstr(cz_txt);

  // Real-Time Curves:
  // Curve A: Incoming Sidechain Kick Spectral Contour (Cyan / White luminous spline)
  // Curve B: Dynamic Inverse Carve-Out Notch Curve (Glowing Acid Emerald line dipping down)
  prev_sc_x = spec_x; prev_sc_y = zero_db_y;
  prev_gr_x = spec_x; prev_gr_y = zero_db_y;

  bi = 0;
  loop(ts_num_bands,
    bf = ts_freqs[bi];
    b_frac = (log(bf) - log(20.0)) / (log(20000.0) - log(20.0));
    bx = spec_x + floor(b_frac * spec_w);

    // Sidechain Kick Energy Bar & Point
    k_env = ts_sc_env[bi];
    k_db = k_env > 0.0001 ? 20.0 * log10(k_env) : -90.0;
    k_norm = max(0.0, min(1.0, (k_db - (-40.0)) / 40.0));
    ky = zero_db_y - floor(k_norm * 36);

    // Carve-out Gain Reduction Point
    g_db = ts_gr_db[bi]; // negative value (e.g. -4.5dB)
    g_y = zero_db_y - floor((g_db / 12.0) * ((spec_h - 70) * 0.90));
    g_y = max(zero_db_y, min(spec_y + spec_h - 22, g_y));

    // Draw dynamic carve-out gradient fill to baseline
    (g_db < -0.1) ? (
      gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50; gfx_a = 0.25;
      gfx_rect(bx - 16, zero_db_y + 1, 32, g_y - zero_db_y);
      gfx_a = 1.0;
    );

    bi > 0 ? (
      // Sidechain contour
      gfx_r = 0.00; gfx_g = 0.92; gfx_b = 0.85; gfx_a = 0.70;
      gfx_line(prev_sc_x, prev_sc_y, bx, ky);
      gfx_a = 1.0;

      // Inverted EQ Carve line
      gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50;
      gfx_line(prev_gr_x, prev_gr_y, bx, g_y);
      gfx_line(prev_gr_x, prev_gr_y + 1, bx, g_y + 1);
    );

    // Node circles
    gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50;
    gfx_circle(bx, g_y, 4, 1);
    (g_db < -0.3) ? (
      gfx_r = 0.98; gfx_g = 0.35; gfx_b = 0.15;
      gfx_circle(bx, g_y, 2, 1);
    );

    prev_sc_x = bx; prev_sc_y = ky;
    prev_gr_x = bx; prev_gr_y = g_y;
    bi += 1;
  );

  // Mouse drag on Low Cut & High Cut handles in the spectrum
  mouse_down && (mouse_x >= spec_x && mouse_x <= spec_x + spec_w && mouse_y >= spec_y && mouse_y <= spec_y + spec_h) ? (
    m_frac = (mouse_x - spec_x) / spec_w;
    m_hz = exp(log(20.0) + m_frac * (log(20000.0) - log(20.0)));
    // If closer to low cut, adjust low cut; else adjust high cut
    abs(mouse_x - lc_x) < abs(mouse_x - hc_x) ? (
      slider47 = max(20, min(slider48 - 50, floor(m_hz)));
    ) : (
      slider48 = max(slider47 + 50, min(16000, floor(m_hz)));
    );
    update_trackspacer_filters(); slider_automate();
  );

  // ---------------------------------------------------------------------------
  // 2. ICONIC WAVESFACTORY TRACKSPACER AMOUNT DIAL (RIGHT RACK)
  // ---------------------------------------------------------------------------
  gfx_r = 0.026; gfx_g = 0.036; gfx_b = 0.046; gfx_rect(rack_x, rack_y, rack_w, rack_h);
  gfx_r = 0.14; gfx_g = 0.28; gfx_b = 0.32; gfx_rect(rack_x, rack_y, rack_w, rack_h, 0);

  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.15; gfx_g = 0.96; gfx_b = 0.60;
  gfx_x = rack_x + 14; gfx_y = rack_y + 12;
  gfx_drawstr("DUCKING DEPTH AMOUNT");

  // Giant Circular Amount Knob (Radius 56px)
  dial_cx = rack_x + floor(rack_w * 0.5);
  dial_cy = rack_y + 92;
  dial_rad = 54;

  // Background Dial Well
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.032; gfx_circle(dial_cx, dial_cy, dial_rad + 6, 1);
  gfx_r = 0.10; gfx_g = 0.18; gfx_b = 0.22; gfx_circle(dial_cx, dial_cy, dial_rad + 6, 0);

  // Outer Arc Progress Ring
  amt_frac = slider46 / 100.0;
  start_ang = -2.356; end_ang = start_ang + amt_frac * 4.712; // 270 degree arc
  gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50;
  arc_step = 0.08; cur_ang = start_ang;
  loop(floor((end_ang - start_ang) / arc_step),
    ax1 = dial_cx + cos(cur_ang) * dial_rad;
    ay1 = dial_cy + sin(cur_ang) * dial_rad;
    ax2 = dial_cx + cos(cur_ang + arc_step) * dial_rad;
    ay2 = dial_cy + sin(cur_ang + arc_step) * dial_rad;
    gfx_line(ax1, ay1, ax2, ay2);
    gfx_line(ax1 * 0.98 + dial_cx * 0.02, ay1 * 0.98 + dial_cy * 0.02, ax2 * 0.98 + dial_cx * 0.02, ay2 * 0.98 + dial_cy * 0.02);
    cur_ang += arc_step;
  );

  // Center Metallic Cap
  gfx_r = 0.04; gfx_g = 0.06; gfx_b = 0.08; gfx_circle(dial_cx, dial_cy, dial_rad - 8, 1);
  gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50; gfx_circle(dial_cx, dial_cy, dial_rad - 8, 0);

  // Numeric Percentage Readout
  gfx_setfont(1, "Orbitron", 24, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  pct_txt = sprintf(#, "%d%%", slider46);
  gfx_measurestr(pct_txt, pcw, pch);
  gfx_x = dial_cx - floor(pcw * 0.5); gfx_y = dial_cy - 16; gfx_drawstr(pct_txt);

  // Dynamic Live Reduction Readout inside Knob
  gfx_setfont(1, "Orbitron", 11.5, 'b');
  (ts_max_gr_live < -0.2) ? (
    gfx_r = 0.98; gfx_g = 0.35; gfx_b = 0.15;
    gr_txt = sprintf(#, "%+.1f dB", ts_max_gr_live);
  ) : (
    gfx_r = 0.40; gfx_g = 0.65; gfx_b = 0.70;
    gr_txt = "READY";
  );
  gfx_measurestr(gr_txt, grw, grh);
  gfx_x = dial_cx - floor(grw * 0.5); gfx_y = dial_cy + 10; gfx_drawstr(gr_txt);

  // Amount Knob Interaction (Drag vertically or horizontally)
  knob_hov = (mouse_x >= dial_cx - dial_rad && mouse_x <= dial_cx + dial_rad && mouse_y >= dial_cy - dial_rad && mouse_y <= dial_cy + dial_rad);
  mouse_down && (knob_hov || (mouse_y >= dial_cy + dial_rad && mouse_y <= dial_cy + dial_rad + 28 && mouse_x >= rack_x + 14 && mouse_x <= rack_x + rack_w - 14)) ? (
    new_amt = max(0, min(100, floor((mouse_x - (dial_cx - dial_rad)) / (dial_rad * 2.0) * 100.0)));
    slider46 = new_amt; slider_automate();
  );

  // Horizontal Quick Slider below Knob
  as_x = rack_x + 20; as_y = dial_cy + dial_rad + 14; as_w = rack_w - 40; as_h = 16;
  gfx_r = 0.018; gfx_g = 0.026; gfx_b = 0.034; gfx_rect(as_x, as_y, as_w, as_h);
  gfx_r = 0.14; gfx_g = 0.28; gfx_b = 0.32; gfx_rect(as_x, as_y, as_w, as_h, 0);
  gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50;
  gfx_rect(as_x + 1, as_y + 1, floor((slider46 / 100.0) * (as_w - 2)), as_h - 2);

  // ---------------------------------------------------------------------------
  // 3. BOTTOM RACK: BALLISTICS, MODES & BLUEPRINTS
  // ---------------------------------------------------------------------------
  btm_y = spec_y + spec_h + 12;
  btm_h = ts_h - (btm_y - ts_y) - 14;
  btm_w = ts_w - 32;
  btm_x = disp_x + 16;

  gfx_r = 0.026; gfx_g = 0.036; gfx_b = 0.046; gfx_rect(btm_x, btm_y, btm_w, btm_h);
  gfx_r = 0.14; gfx_g = 0.28; gfx_b = 0.32; gfx_rect(btm_x, btm_y, btm_w, btm_h, 0);

  col3_w = floor((btm_w - 32) / 3);

  // Col 1: Ballistics (Attack / Release)
  c1_x = btm_x + 12;
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.15; gfx_g = 0.96; gfx_b = 0.60;
  gfx_x = c1_x; gfx_y = btm_y + 10; gfx_drawstr("BALLISTICS TIMING");

  gfx_setfont(1, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.94; gfx_b = 0.92;
  gfx_x = c1_x; gfx_y = btm_y + 32;
  att_txt = sprintf(#, "ATTACK: %d ms", slider49); gfx_drawstr(att_txt);

  // Attack Slider Bar
  at_bx = c1_x; at_by = btm_y + 48; at_bw = col3_w - 20; at_bh = 14;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.032; gfx_rect(at_bx, at_by, at_bw, at_bh);
  gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50;
  gfx_rect(at_bx + 1, at_by + 1, floor(((slider49 - 1) / 99.0) * at_bw), at_bh - 2);
  mouse_down && (mouse_x >= at_bx && mouse_x <= at_bx + at_bw && mouse_y >= at_by && mouse_y <= at_by + at_bh) ? (
    slider49 = max(1, min(100, floor(1 + ((mouse_x - at_bx) / at_bw) * 99.0)));
    update_trackspacer_filters(); slider_automate();
  );

  gfx_setfont(1, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.94; gfx_b = 0.92;
  gfx_x = c1_x; gfx_y = btm_y + 70;
  rel_txt = sprintf(#, "RELEASE: %d ms", slider50); gfx_drawstr(rel_txt);

  // Release Slider Bar
  rl_bx = c1_x; rl_by = btm_y + 86; rl_bw = col3_w - 20; rl_bh = 14;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.032; gfx_rect(rl_bx, rl_by, rl_bw, rl_bh);
  gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50;
  gfx_rect(rl_bx + 1, rl_by + 1, floor(((slider50 - 10) / 390.0) * rl_bw), rl_bh - 2);
  mouse_down && (mouse_x >= rl_bx && mouse_x <= rl_bx + rl_bw && mouse_y >= rl_by && mouse_y <= rl_by + rl_bh) ? (
    slider50 = max(10, min(400, floor(10 + ((mouse_x - rl_bx) / rl_bw) * 390.0)));
    update_trackspacer_filters(); slider_automate();
  );

  // Col 2: Channel Mode & Audition
  c2_x = c1_x + col3_w + 8;
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.15; gfx_g = 0.96; gfx_b = 0.60;
  gfx_x = c2_x; gfx_y = btm_y + 10; gfx_drawstr("CHANNEL MODE");

  // 3 Mode Pills: Mid (Center), Stereo, Side
  cm_w = floor((col3_w - 24) / 3);
  cmi = 0;
  loop(3,
    cm_px = c2_x + cmi * (cm_w + 6); cm_py = btm_y + 32;
    is_cm = (slider51 == cmi);
    cm_hov = (mouse_x >= cm_px && mouse_x <= cm_px + cm_w && mouse_y >= cm_py && mouse_y <= cm_py + 26);
    gfx_r = is_cm ? 0.06 : (cm_hov ? 0.04 : 0.02);
    gfx_g = is_cm ? 0.26 : (cm_hov ? 0.12 : 0.04);
    gfx_b = is_cm ? 0.20 : (cm_hov ? 0.10 : 0.05);
    gfx_rect(cm_px, cm_py, cm_w, 26);
    gfx_r = is_cm ? 0.06 : 0.14; gfx_g = is_cm ? 0.88 : 0.28; gfx_b = is_cm ? 0.50 : 0.32;
    gfx_rect(cm_px, cm_py, cm_w, 26, 0);
    gfx_setfont(1, "Orbitron", 10.5, 'b'); gfx_r = is_cm ? 1.0 : 0.70; gfx_g = is_cm ? 1.0 : 0.75; gfx_b = is_cm ? 1.0 : 0.80;
    cm_lbl = (cmi == 0 ? "MID" : cmi == 1 ? "STEREO" : "SIDE");
    gfx_measurestr(cm_lbl, cmw, cmh);
    gfx_x = cm_px + floor((cm_w - cmw) * 0.5); gfx_y = cm_py + 6; gfx_drawstr(cm_lbl);
    mouse_clicked && cm_hov ? (slider51 = cmi; slider_automate(););
    cmi += 1;
  );

  // Audition Pills (Normal / Listen Kick / Delta Carve)
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.15; gfx_g = 0.96; gfx_b = 0.60;
  gfx_x = c2_x; gfx_y = btm_y + 68; gfx_drawstr("AUDITION LISTENING");

  aud_w = floor((col3_w - 24) / 3);
  audi = 0;
  loop(3,
    aud_px = c2_x + audi * (aud_w + 6); aud_py = btm_y + 86;
    is_aud = (slider52 == audi);
    aud_hov = (mouse_x >= aud_px && mouse_x <= aud_px + aud_w && mouse_y >= aud_py && mouse_y <= aud_py + 26);
    gfx_r = is_aud ? (audi == 0 ? 0.06 : 0.28) : (aud_hov ? 0.04 : 0.02);
    gfx_g = is_aud ? (audi == 0 ? 0.26 : 0.12) : (aud_hov ? 0.12 : 0.04);
    gfx_b = is_aud ? (audi == 0 ? 0.20 : 0.10) : (aud_hov ? 0.10 : 0.05);
    gfx_rect(aud_px, aud_py, aud_w, 26);
    gfx_r = is_aud ? (audi == 0 ? 0.06 : 0.98) : 0.14; gfx_g = is_aud ? (audi == 0 ? 0.88 : 0.35) : 0.28; gfx_b = is_aud ? (audi == 0 ? 0.50 : 0.15) : 0.32;
    gfx_rect(aud_px, aud_py, aud_w, 26, 0);
    gfx_setfont(1, "Orbitron", 10, 'b'); gfx_r = is_aud ? 1.0 : 0.70; gfx_g = is_aud ? 1.0 : 0.75; gfx_b = is_aud ? 1.0 : 0.80;
    aud_lbl = (audi == 0 ? "NORMAL" : audi == 1 ? "KICK SC" : "DELTA");
    gfx_measurestr(aud_lbl, adw, adh);
    gfx_x = aud_px + floor((aud_w - adw) * 0.5); gfx_y = aud_py + 6; gfx_drawstr(aud_lbl);
    mouse_clicked && aud_hov ? (slider52 = audi; slider_automate(););
    audi += 1;
  );

  // Col 3: Quick Producer Profiles
  c3_x = c2_x + col3_w + 8;
  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.15; gfx_g = 0.96; gfx_b = 0.60;
  gfx_x = c3_x; gfx_y = btm_y + 10; gfx_drawstr("QUICK SIGNATURE PRESETS");

  qpi = 0;
  loop(3,
    qp_y = btm_y + 32 + qpi * 26; qp_w = col3_w - 20;
    qp_hov = (mouse_x >= c3_x && mouse_x <= c3_x + qp_w && mouse_y >= qp_y && mouse_y <= qp_y + 22);
    gfx_r = qp_hov ? 0.06 : 0.025; gfx_g = qp_hov ? 0.18 : 0.035; gfx_b = qp_hov ? 0.14 : 0.045;
    gfx_rect(c3_x, qp_y, qp_w, 22);
    gfx_r = 0.06; gfx_g = 0.88; gfx_b = 0.50; gfx_rect(c3_x, qp_y, qp_w, 22, 0);
    gfx_setfont(1, "Orbitron", 10.5, 'b'); gfx_r = qp_hov ? 1.0 : 0.85; gfx_g = qp_hov ? 1.0 : 0.94; gfx_b = qp_hov ? 1.0 : 0.92;
    qp_lbl = (qpi == 0 ? "1. DAN BRAUNSTEIN (35% | 35-650Hz | Mid)" : qpi == 1 ? "2. MODERN THALL (45% | 40-350Hz | Mid)" : "3. CLEAN GLUE (25% | 30-1.2kHz | Stereo)");
    gfx_x = c3_x + 8; gfx_y = qp_y + 4; gfx_drawstr(qp_lbl);
    mouse_clicked && qp_hov ? (
      qpi == 0 ? (slider46 = 35; slider47 = 35; slider48 = 650; slider49 = 15; slider50 = 65; slider51 = 0;) :
      qpi == 1 ? (slider46 = 45; slider47 = 40; slider48 = 350; slider49 = 10; slider50 = 45; slider51 = 0;) :
      (slider46 = 25; slider47 = 30; slider48 = 1200; slider49 = 20; slider50 = 85; slider51 = 1;);
      update_trackspacer_filters(); slider_automate();
    );
    qpi += 1;
  );
);

"""

assert tab2_marker in code, "tab2_marker not found"
code = code.replace(tab2_marker, trackspacer_tab_gui + tab2_marker, 1)

# Write to a test file first to run eel_check
test_file = r"c:\Dev\DameiAPI\reaper_scripts\Damei_BassSuite_test.jsfx"
with open(test_file, "w", encoding="utf-8") as f:
    f.write(code)

print("Patch applied to test file successfully! Total characters:", len(code))
