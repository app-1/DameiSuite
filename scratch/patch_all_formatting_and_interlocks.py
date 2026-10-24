import re, os, shutil

src_file = r'effects/Damei_InstrumentalSuite.jsfx'
reaper_file = r'C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_InstrumentalSuite.jsfx'
matrix_src = r'effects/Damei_AssessmentMatrix.jsfx'
matrix_reaper = r'C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_AssessmentMatrix.jsfx'

with open(src_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update @init gmem broadcast
old_init = '''update_filters();
apply_producer_preset(slider2);

@slider'''

new_init = '''update_filters();
apply_producer_preset(slider2);
gmem[960] = slider27 ? 1 : 0;
gmem[961] = slider2;
gmem[975] = time_precise();

@slider'''
assert old_init in text, "Could not find old_init"
text = text.replace(old_init, new_init, 1)

# 2. Update @slider gmem broadcast
old_slider = '''slider32 == 2 ? (
  trigger_ai_assist();
  slider32 = 1;
);
update_filters();

@block'''

new_slider = '''slider32 == 2 ? (
  trigger_ai_assist();
  slider32 = 1;
);
update_filters();
gmem[960] = slider27 ? 1 : 0;
gmem[961] = slider2;
gmem[975] = time_precise();

@block'''
assert old_slider in text, "Could not find old_slider"
text = text.replace(old_slider, new_slider, 1)

# 3. Add gmem assertion in @gfx and fix ballistic needle damping
old_damp = '''// Ballistic Needle Damping
sifam_needle_vu += (inst_rms - sifam_needle_vu) * 0.25;
sifam_needle_gr += (glue_gr_db - sifam_needle_gr) * 0.35;'''

new_damp = '''// Ballistic Needle Damping & Ecosystem Heartbeat Assert
gmem[960] = slider27 ? 1 : 0;
gmem[961] = slider2;
gmem[975] = time_precise();
vu_target = clamp(inst_rms + 18.0, -20.0, 3.0);
sifam_needle_vu += (vu_target - sifam_needle_vu) * 0.25;
sifam_needle_gr += (glue_gr_db - sifam_needle_gr) * 0.35;'''
assert old_damp in text, "Could not find old_damp"
text = text.replace(old_damp, new_damp, 1)

# 4. Refine draw_sifam_meter definition
old_sifam_def = '''// Strictly Confined Vintage SIFAM Moving-Coil Meter
function draw_sifam_meter(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) local(plate_x, plate_y, plate_w, plate_h, piv_x, piv_y, radius_arc, radius_needle, ang_min, ang_max, a_span, a_frac, cur_a, ax, ay, ai, arc_steps, prev_ax, prev_ay, t_a, m_db, f_val, nx1, ny1, nx2, ny2, tw, th, t_str, badge_str, b_w, b_h, frac, cur_ang, tip_x, tip_y, base_x, base_y) (
  gfx_r = 0.055; gfx_g = 0.065; gfx_b = 0.080; gfx_rect(mx, my, mw, mh);
  gfx_r = 0.020; gfx_g = 0.024; gfx_b = 0.032; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(mx, my, mw, mh, 0);
  gfx_r = accent_r * 0.6; gfx_g = accent_g * 0.6; gfx_b = accent_b * 0.6; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4, 0);

  plate_x = mx + 6; plate_y = my + 6;
  plate_w = mw - 12; plate_h = mh - 12;
  gfx_r = 0.035; gfx_g = 0.045; gfx_b = 0.060; gfx_rect(plate_x, plate_y, plate_w, plate_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(plate_x, plate_y, plate_w, plate_h, 0);

  piv_x = plate_x + plate_w * 0.5;
  piv_y = plate_y + plate_h - 16;

  radius_arc = min(plate_h - 52, plate_w * 0.44);
  radius_needle = radius_arc - 4;

  // Tungsten Lamp Glow
  gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.35; gfx_a = 0.07;
  gfx_circle(piv_x, piv_y - radius_arc * 0.45, floor(radius_arc * 0.6), 1);
  gfx_a = 1.0;

  gfx_setfont(1, "Orbitron", 11.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = plate_x + 12; gfx_y = plate_y + 8; gfx_drawstr(title_str);

  gfx_setfont(2, "Consolas", 11, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  badge_str = is_glue ? "STUDIO GR" : "STUDIO VU";
  gfx_measurestr(badge_str, b_w, b_h);
  gfx_x = plate_x + plate_w - b_w - 12; gfx_y = plate_y + 8; gfx_drawstr(badge_str);

  ang_min = -0.62; ang_max = 0.62; a_span = ang_max - ang_min;
  arc_steps = 30; ai = 0; prev_ax = 0; prev_ay = 0;
  loop(arc_steps + 1,
    a_frac = ai / arc_steps;
    cur_a = ang_min + a_frac * a_span;
    ax = piv_x + sin(cur_a) * radius_arc;
    ay = piv_y - cos(cur_a) * radius_arc;
    ai > 0 ? (
      is_glue ? (
        a_frac > 0.65 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;)
      ) : (
        a_frac > 0.87 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.95; gfx_g = 0.75; gfx_b = 0.20;)
      );
      gfx_line(prev_ax, prev_ay, ax, ay);
    );
    prev_ax = ax; prev_ay = ay;
    ai += 1;
  );

  gfx_setfont(3, "Consolas", 10, 'b');
  is_glue ? (
    m_i = 0;
    while (m_i < 6) (
      m_db = m_i == 0 ? 0 : (m_i == 1 ? 3 : (m_i == 2 ? 6 : (m_i == 3 ? 10 : (m_i == 4 ? 16 : 20))));
      f_val = m_db / 20.0;
      t_a = ang_min + f_val * a_span;
      nx1 = piv_x + sin(t_a) * (radius_arc - 5); ny1 = piv_y - cos(t_a) * (radius_arc - 5);
      nx2 = piv_x + sin(t_a) * (radius_arc + 4); ny2 = piv_y - cos(t_a) * (radius_arc + 4);
      m_db >= 10 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.75; gfx_g = 0.88; gfx_b = 0.95;);
      gfx_line(nx1, ny1, nx2, ny2);
      t_str = sprintf(#, "%d", m_db);
      gfx_measurestr(t_str, tw, th);
      gfx_x = piv_x + sin(t_a) * (radius_arc + 14) - tw * 0.5;
      gfx_y = piv_y - cos(t_a) * (radius_arc + 14) - th * 0.5;
      gfx_drawstr(t_str);
      m_i += 1;
    );
  ) : (
    m_i = 0;
    while (m_i < 5) (
      m_db = m_i == 0 ? -20 : (m_i == 1 ? -10 : (m_i == 2 ? -5 : (m_i == 3 ? 0 : 3)));
      f_val = (m_db + 20.0) / 23.0;
      t_a = ang_min + f_val * a_span;
      nx1 = piv_x + sin(t_a) * (radius_arc - 5); ny1 = piv_y - cos(t_a) * (radius_arc - 5);
      nx2 = piv_x + sin(t_a) * (radius_arc + 4); ny2 = piv_y - cos(t_a) * (radius_arc + 4);
      m_db <= 0 ? (gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;) : (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;);
      gfx_line(nx1, ny1, nx2, ny2);
      t_str = sprintf(#, "%+d", m_db);
      gfx_measurestr(t_str, tw, th);
      gfx_x = piv_x + sin(t_a) * (radius_arc + 14) - tw * 0.5;
      gfx_y = piv_y - cos(t_a) * (radius_arc + 14) - th * 0.5;
      gfx_drawstr(t_str);
      m_i += 1;
    );
  );

  gfx_setfont(1, "Orbitron", 13, 'b');
  is_glue ? (gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;) : (gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;);
  center_badge = is_glue ? "[ GR ]" : "[ VU ]";
  gfx_measurestr(center_badge, tw, th);
  gfx_x = floor(plate_x + (plate_w - tw) * 0.5);
  gfx_y = floor(piv_y - radius_needle * 0.45);
  gfx_drawstr(center_badge);

  frac = is_glue ? min(1.0, max(0.0, needle_val / 20.0)) : min(1.0, max(0.0, (needle_val + 20.0) / 23.0));
  cur_ang = ang_min + frac * a_span;
  tip_x = piv_x + sin(cur_ang) * radius_needle;
  tip_y = piv_y - cos(cur_ang) * radius_needle;
  base_x = piv_x + sin(cur_ang) * 14;
  base_y = piv_y - cos(cur_ang) * 14;

  is_glue ? (gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;) : (gfx_r = 1.00; gfx_g = 0.80; gfx_b = 0.22;);
  gfx_line(base_x - 0.7, base_y, tip_x - 0.7, tip_y);
  gfx_line(base_x + 0.7, base_y, tip_x + 0.7, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  gfx_r = 0.98; gfx_g = 0.25; gfx_b = 0.22; gfx_circle(tip_x, tip_y, 2.5, 1);
  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(piv_x, piv_y, 16, 1);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_circle(piv_x, piv_y, 16, 0);

  gfx_setfont(3, "Consolas", 10.5, 'b');
  is_glue ? (
    gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
    gfx_x = plate_x + 14; gfx_y = plate_y + plate_h - 22;
    gfx_printf("GR: %4.1f dB", glue_gr_db);
    gfx_x = plate_x + plate_w - 78; gfx_y = plate_y + plate_h - 22;
    gfx_drawstr("PEAK HOLD");
  ) : (
    gfx_r = 0.00; gfx_g = 0.85; gfx_b = 0.45;
    gfx_x = plate_x + 14; gfx_y = plate_y + plate_h - 22;
    gfx_printf("RMS: %4.1f dBFS", inst_rms);
    gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;
    gfx_x = plate_x + plate_w - 110; gfx_y = plate_y + plate_h - 22;
    gfx_drawstr("0 VU = -18 dBFS");
  );
);'''

new_sifam_def = '''// Strictly Confined Vintage SIFAM Moving-Coil Meter
function draw_sifam_meter(mx, my, mw, mh, title_str, needle_val, max_val, is_glue, accent_r, accent_g, accent_b) local(plate_x, plate_y, plate_w, plate_h, piv_x, piv_y, radius_arc, radius_needle, ang_min, ang_max, a_span, a_frac, cur_a, ax, ay, ai, arc_steps, prev_ax, prev_ay, t_a, m_db, f_val, nx1, ny1, nx2, ny2, tw, th, t_str, badge_str, b_w, b_h, frac, cur_ang, tip_x, tip_y, base_x, base_y) (
  gfx_r = 0.055; gfx_g = 0.065; gfx_b = 0.080; gfx_rect(mx, my, mw, mh);
  gfx_r = 0.020; gfx_g = 0.024; gfx_b = 0.032; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(mx, my, mw, mh, 0);
  gfx_r = accent_r * 0.6; gfx_g = accent_g * 0.6; gfx_b = accent_b * 0.6; gfx_rect(mx + 2, my + 2, mw - 4, mh - 4, 0);

  plate_x = mx + 6; plate_y = my + 6;
  plate_w = mw - 12; plate_h = mh - 12;
  gfx_r = 0.035; gfx_g = 0.045; gfx_b = 0.060; gfx_rect(plate_x, plate_y, plate_w, plate_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(plate_x, plate_y, plate_w, plate_h, 0);
  draw_adinkra_watermark(plate_x, plate_y, plate_w, plate_h, 2);

  piv_x = plate_x + plate_w * 0.5;
  piv_y = plate_y + plate_h - 16;

  radius_arc = min(plate_h - 52, plate_w * 0.44);
  radius_needle = radius_arc - 4;

  // Tungsten Lamp Glow
  gfx_r = 1.00; gfx_g = 0.82; gfx_b = 0.35; gfx_a = 0.07;
  gfx_circle(piv_x, piv_y - radius_arc * 0.45, floor(radius_arc * 0.6), 1);
  gfx_a = 1.0;

  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = plate_x + 12; gfx_y = plate_y + 8; gfx_drawstr(title_str);

  gfx_setfont(2, "Consolas", 11.5, 'b'); gfx_r = accent_r; gfx_g = accent_g; gfx_b = accent_b;
  badge_str = is_glue ? "STUDIO GR" : "STUDIO VU";
  gfx_measurestr(badge_str, b_w, b_h);
  gfx_x = plate_x + plate_w - b_w - 12; gfx_y = plate_y + 8; gfx_drawstr(badge_str);

  ang_min = -0.62; ang_max = 0.62; a_span = ang_max - ang_min;
  arc_steps = 30; ai = 0; prev_ax = 0; prev_ay = 0;
  loop(arc_steps + 1,
    a_frac = ai / arc_steps;
    cur_a = ang_min + a_frac * a_span;
    ax = piv_x + sin(cur_a) * radius_arc;
    ay = piv_y - cos(cur_a) * radius_arc;
    ai > 0 ? (
      is_glue ? (
        a_frac > 0.65 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;)
      ) : (
        a_frac > 0.87 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.95; gfx_g = 0.75; gfx_b = 0.20;)
      );
      gfx_line(prev_ax, prev_ay, ax, ay);
    );
    prev_ax = ax; prev_ay = ay;
    ai += 1;
  );

  gfx_setfont(3, "Consolas", 11, 'b');
  is_glue ? (
    m_i = 0;
    while (m_i < 6) (
      m_db = m_i == 0 ? 0 : (m_i == 1 ? 3 : (m_i == 2 ? 6 : (m_i == 3 ? 10 : (m_i == 4 ? 16 : 20))));
      f_val = m_db / 20.0;
      t_a = ang_min + f_val * a_span;
      nx1 = piv_x + sin(t_a) * (radius_arc - 5); ny1 = piv_y - cos(t_a) * (radius_arc - 5);
      nx2 = piv_x + sin(t_a) * (radius_arc + 4); ny2 = piv_y - cos(t_a) * (radius_arc + 4);
      m_db >= 10 ? (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;) : (gfx_r = 0.75; gfx_g = 0.88; gfx_b = 0.95;);
      gfx_line(nx1, ny1, nx2, ny2);
      t_str = sprintf(#, "%d", m_db);
      gfx_measurestr(t_str, tw, th);
      gfx_x = piv_x + sin(t_a) * (radius_arc + 14) - tw * 0.5;
      gfx_y = piv_y - cos(t_a) * (radius_arc + 14) - th * 0.5;
      gfx_drawstr(t_str);
      m_i += 1;
    );
  ) : (
    m_i = 0;
    while (m_i < 5) (
      m_db = m_i == 0 ? -20 : (m_i == 1 ? -10 : (m_i == 2 ? -5 : (m_i == 3 ? 0 : 3)));
      f_val = (m_db + 20.0) / 23.0;
      t_a = ang_min + f_val * a_span;
      nx1 = piv_x + sin(t_a) * (radius_arc - 5); ny1 = piv_y - cos(t_a) * (radius_arc - 5);
      nx2 = piv_x + sin(t_a) * (radius_arc + 4); ny2 = piv_y - cos(t_a) * (radius_arc + 4);
      m_db <= 0 ? (gfx_r = 0.75; gfx_g = 0.85; gfx_b = 0.95;) : (gfx_r = 0.98; gfx_g = 0.22; gfx_b = 0.22;);
      gfx_line(nx1, ny1, nx2, ny2);
      t_str = sprintf(#, "%+d", m_db);
      gfx_measurestr(t_str, tw, th);
      gfx_x = piv_x + sin(t_a) * (radius_arc + 14) - tw * 0.5;
      gfx_y = piv_y - cos(t_a) * (radius_arc + 14) - th * 0.5;
      gfx_drawstr(t_str);
      m_i += 1;
    );
  );

  gfx_setfont(1, "Orbitron", 13.5, 'b');
  is_glue ? (gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;) : (gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;);
  center_badge = is_glue ? "[ GR ]" : "[ VU ]";
  gfx_measurestr(center_badge, tw, th);
  gfx_x = floor(plate_x + (plate_w - tw) * 0.5);
  gfx_y = floor(piv_y - radius_needle * 0.45);
  gfx_drawstr(center_badge);

  frac = is_glue ? min(1.0, max(0.0, needle_val / 20.0)) : min(1.0, max(0.0, (needle_val + 20.0) / 23.0));
  cur_ang = ang_min + frac * a_span;
  tip_x = piv_x + sin(cur_ang) * radius_needle;
  tip_y = piv_y - cos(cur_ang) * radius_needle;
  base_x = piv_x + sin(cur_ang) * 14;
  base_y = piv_y - cos(cur_ang) * 14;

  is_glue ? (gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;) : (gfx_r = 1.00; gfx_g = 0.80; gfx_b = 0.22;);
  gfx_line(base_x - 0.7, base_y, tip_x - 0.7, tip_y);
  gfx_line(base_x + 0.7, base_y, tip_x + 0.7, tip_y);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_line(base_x, base_y, tip_x, tip_y);

  gfx_r = 0.98; gfx_g = 0.25; gfx_b = 0.22; gfx_circle(tip_x, tip_y, 2.5, 1);
  gfx_r = 0.08; gfx_g = 0.10; gfx_b = 0.14; gfx_circle(piv_x, piv_y, 14, 1);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_circle(piv_x, piv_y, 14, 0);

  gfx_setfont(3, "Consolas", 11.5, 'b');
  is_glue ? (
    gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
    gfx_x = plate_x + 14; gfx_y = plate_y + plate_h - 22;
    gfx_printf("GR: %4.1f dB", glue_gr_db);
    gfx_x = plate_x + plate_w - 84; gfx_y = plate_y + plate_h - 22;
    gfx_drawstr("PEAK HOLD");
  ) : (
    gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
    gfx_x = plate_x + 14; gfx_y = plate_y + plate_h - 22;
    gfx_printf("RMS: %4.1f dBFS", inst_rms);
    gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;
    gfx_x = plate_x + plate_w - 116; gfx_y = plate_y + plate_h - 22;
    gfx_drawstr("0 VU = -18 dBFS");
  );
);'''
assert old_sifam_def in text, "Could not find old_sifam_def"
text = text.replace(old_sifam_def, new_sifam_def, 1)

# 5. Replace Tab 0 Card 1 with clean draw_sifam_meter call
old_c1 = '''  // CARD 1: SIFAM ANALOG MOVING-COIL CONSOLE VU METER (Left)
  c1_x = ws_x + 12; c1_y = t0_top_y; c1_w = floor((ws_w - 36) * 0.33); c1_h = t0_top_h;
  gfx_r = 0.016; gfx_g = 0.024; gfx_b = 0.038; gfx_rect(c1_x, c1_y, c1_w, c1_h);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_rect(c1_x, c1_y, c1_w, c1_h, 0);
  draw_adinkra_watermark(c1_x, c1_y, c1_w, c1_h, 2); // Funtunfunefu Watermark

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = c1_x + 14; gfx_y = c1_y + 12; gfx_drawstr("SIFAM DIRECTOR // CONSOLE DRIVE");
  gfx_setfont(2, "Arial", 11, 'b'); gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00;
  gfx_x = c1_x + c1_w - 82; gfx_y = c1_y + 12; gfx_drawstr("STUDIO VU");

  // SIFAM Moving-Coil Needle Arc
  sif_cx = c1_x + floor(c1_w * 0.5); sif_cy = c1_y + 172; sif_r = 138;
  draw_arc(sif_cx, sif_cy, sif_r, -0.65, 0.65, 0.15, 0.20, 0.30);
  draw_arc(sif_cx, sif_cy, sif_r, 0.25, 0.65, 0.85, 0.25, 0.25); // Redline

  vu_val = clamp(inst_rms + 18.0, -20.0, 3.0);
  sifam_needle_vu += (vu_val - sifam_needle_vu) * 0.15;
  n_ang = -0.65 + ((sifam_needle_vu + 20.0) / 23.0) * 1.30;
  
  gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_line(sif_cx, sif_cy, sif_cx + sin(n_ang) * (sif_r - 10), sif_cy - cos(n_ang) * (sif_r - 10));
  gfx_circle(sif_cx, sif_cy, 12, 1);
  gfx_r = 0.25; gfx_g = 0.62; gfx_b = 1.00; gfx_circle(sif_cx, sif_cy, 12, 0);

  // Ballistics & Peak Readouts
  crest_live = max(0.0, inst_peak_db - inst_rms);
  gfx_setfont(2, "Consolas", 11, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = c1_x + 14; gfx_y = c1_y + c1_h - 26; gfx_printf("RMS: %4.1f dBFS | CREST: %3.1f dB", inst_rms, crest_live);
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_x = c1_x + c1_w - 110; gfx_y = c1_y + c1_h - 26; gfx_printf("PEAK: %4.1f dBTP", inst_peak_db);'''

new_c1 = '''  // CARD 1: SIFAM ANALOG MOVING-COIL CONSOLE VU METER (Left)
  c1_x = ws_x + 12; c1_y = t0_top_y; c1_w = floor((ws_w - 36) * 0.33); c1_h = t0_top_h;
  draw_sifam_meter(c1_x, c1_y, c1_w, c1_h, "SIFAM // CONSOLE DRIVE", sifam_needle_vu, 3.0, 0, 0.25, 0.62, 1.00);'''
assert old_c1 in text, "Could not find old_c1"
text = text.replace(old_c1, new_c1, 1)

# 6. Tab Navigation Buttons Font size (line ~1589)
idx_tab = text.find('// 3. TAB NAVIGATION BAR (8 LUXURY TABS)')
assert idx_tab != -1
idx_tab_end = text.find('// 4. MAIN WORKSPACE ENCLOSURE (DYNAMIC VIEWPORT)')
assert idx_tab_end != -1
tab_sub = text[idx_tab:idx_tab_end]
tab_sub = tab_sub.replace('gfx_setfont(1, "Orbitron", 10.5, \'b\');', 'gfx_setfont(1, "Orbitron", 12, \'b\');')
text = text[:idx_tab] + tab_sub + text[idx_tab_end:]

# 7. Component Header Typography
old_comp_hdr = '''  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.30;
  gfx_x = ws_x + 18; gfx_y = ws_y + 14; gfx_drawstr(title);

  gfx_setfont(2, "Consolas", 10.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = ws_x + 18; gfx_y = ws_y + 32; gfx_drawstr("MISSION: ");'''

new_comp_hdr = '''  gfx_setfont(1, "Orbitron", 13.5, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.30;
  gfx_x = ws_x + 18; gfx_y = ws_y + 14; gfx_drawstr(title);

  gfx_setfont(2, "Consolas", 11.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = ws_x + 18; gfx_y = ws_y + 32; gfx_drawstr("MISSION: ");'''
assert old_comp_hdr in text, "Could not find old_comp_hdr"
text = text.replace(old_comp_hdr, new_comp_hdr, 1)

# 8. EQ Faders Typography (line ~1269)
old_eq_fader = '''  gfx_setfont(1, "Orbitron", 11, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = f_x + 10; gfx_y = f_y + 10; gfx_drawstr(title);
  gfx_setfont(2, "Consolas", 10, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = f_x + 10; gfx_y = f_y + 28; gfx_drawstr(freq_lbl);

  v_str = sprintf(#, "%+3.1f dB", val);
  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;'''

new_eq_fader = '''  gfx_setfont(1, "Orbitron", 12.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = f_x + 10; gfx_y = f_y + 10; gfx_drawstr(title);
  gfx_setfont(2, "Consolas", 11.5, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = f_x + 10; gfx_y = f_y + 28; gfx_drawstr(freq_lbl);

  v_str = sprintf(#, "%+3.1f dB", val);
  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;'''
assert old_eq_fader in text, "Could not find old_eq_fader"
text = text.replace(old_eq_fader, new_eq_fader, 1)

# 9. Tab 0 Center Radar and Right Phase Radar Titles & Readouts
text = text.replace(
    'gfx_setfont(1, "Orbitron", 12, \'b\'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;\n  gfx_x = c2_x + 14; gfx_y = c2_y + 12; gfx_drawstr("TONAL BALANCE ENERGY RADAR");',
    'gfx_setfont(1, "Orbitron", 13, \'b\'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;\n  gfx_x = c2_x + 14; gfx_y = c2_y + 12; gfx_drawstr("TONAL BALANCE ENERGY RADAR");'
)
text = text.replace(
    'gfx_setfont(2, "Consolas", 10.5, \'b\'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;\n  gfx_x = c2_x + 14; gfx_y = c2_y + c2_h - 26;\n  gfx_printf("REF TARGET MATCH: 98.4%% | DESK THD: %3.2f%%"',
    'gfx_setfont(2, "Consolas", 11.5, \'b\'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;\n  gfx_x = c2_x + 14; gfx_y = c2_y + c2_h - 26;\n  gfx_printf("REF TARGET MATCH: 98.4%% | DESK THD: %3.2f%%"'
)
text = text.replace(
    'gfx_setfont(1, "Orbitron", 12, \'b\'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;\n  gfx_x = c3_x + 14; gfx_y = c3_y + 12; gfx_drawstr("STEREO PHASE RADAR");',
    'gfx_setfont(1, "Orbitron", 13, \'b\'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;\n  gfx_x = c3_x + 14; gfx_y = c3_y + 12; gfx_drawstr("STEREO PHASE RADAR");'
)
text = text.replace(
    'gfx_setfont(2, "Consolas", 10.5, \'b\'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;\n  gfx_x = c3_x + 14; gfx_y = c3_y + c3_h - 26;\n  gfx_printf("CORR: %+4.2f | S/M: %4.1f dB | WIDTH: %3.2fx", corr_smooth, sm_ratio_live, active_width);',
    'gfx_setfont(2, "Consolas", 11.5, \'b\'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;\n  gfx_x = c3_x + 14; gfx_y = c3_y + c3_h - 26;\n  gfx_printf("CORR: %+4.2f | S/M: %4.1f dB | WIDTH: %3.2fx", corr_smooth, sm_ratio_live, active_width);'
)

# 10. Tab 0 Bottom Card (Master Status)
old_bot_card = '''  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = bot_x + 18; gfx_y = bot_y + 14; gfx_drawstr("FLAGSHIP CONCLAVE INTEGRATION // MASTER STATUS");

  gfx_setfont(2, "Arial", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = bot_x + 18; gfx_y = bot_y + 40;
  gfx_printf("* HEADROOM TRIM  : %+3.1f dB (Forensic DeeGain Staging Lock - Bit-Exact Parity Target)", slider4);
  gfx_x = bot_x + 18; gfx_y = bot_y + 64;
  gfx_printf("* BUS GLUE VCA   : Thresh %4.1f dB | Ratio %s | 10ms Attack | 600ms Release | HPF %2.0f Hz | Active GR: %3.1f dB",
             slider12, slider13==0?"1.5:1":slider13==1?"2:1":slider13==2?"4:1":"8:1", slider16, glue_gr_db);
  gfx_x = bot_x + 18; gfx_y = bot_y + 88;
  gfx_printf("* HARMONIC DESK  : %s | Drive %+2.1f dB (Britson Console Vintage Harmonic Summing)",
             slider23==0?"Transparent Pass":slider23==1?"Neve 8014 Iron Desk":slider23==2?"Studer A800 Tape":"Triode Tube", slider24);
  gfx_x = bot_x + 18; gfx_y = bot_y + 112;
  gfx_printf("* STEREO MATRIX  : Sub-Mono Anchor %2.0f Hz | M/S Quad Width %3.2fx | Dynamic Vocal Pocket Notch -%2.1f dB",
             slider6, slider25, pocket_dyn_dip);
  gfx_x = bot_x + 18; gfx_y = bot_y + 136;
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_printf("* ACTIVE TARGET  : %s // Reference Track Lock: %s",
             get_producer_name(slider2), get_producer_ref_track(slider2));'''

new_bot_card = '''  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;
  gfx_x = bot_x + 18; gfx_y = bot_y + 14; gfx_drawstr("FLAGSHIP CONCLAVE INTEGRATION // MASTER STATUS");

  gfx_setfont(2, "Consolas", 12, 'b'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;
  gfx_x = bot_x + 18; gfx_y = bot_y + 40;
  gfx_printf("* HEADROOM TRIM  : %+3.1f dB (Forensic DeeGain Staging Lock - Bit-Exact Parity Target)", slider4);
  gfx_x = bot_x + 18; gfx_y = bot_y + 64;
  gfx_printf("* BUS GLUE VCA   : Thresh %4.1f dB | Ratio %s | 10ms Attack | 600ms Release | HPF %2.0f Hz | Active GR: %3.1f dB",
             slider12, slider13==0?"1.5:1":slider13==1?"2:1":slider13==2?"4:1":"8:1", slider16, glue_gr_db);
  gfx_x = bot_x + 18; gfx_y = bot_y + 88;
  gfx_printf("* HARMONIC DESK  : %s | Drive %+2.1f dB (Britson Console Vintage Harmonic Summing)",
             slider23==0?"Transparent Pass":slider23==1?"Neve 8014 Iron Desk":slider23==2?"Studer A800 Tape":"Triode Tube", slider24);
  gfx_x = bot_x + 18; gfx_y = bot_y + 112;
  gfx_printf("* STEREO MATRIX  : Sub-Mono Anchor %2.0f Hz | M/S Quad Width %3.2fx | Dynamic Vocal Pocket Notch -%2.1f dB",
             slider6, slider25, pocket_dyn_dip);
  gfx_x = bot_x + 18; gfx_y = bot_y + 136;
  gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;
  gfx_printf("* ACTIVE TARGET  : %s // Reference Track Lock: %s",
             get_producer_name(slider2), get_producer_ref_track(slider2));'''
assert old_bot_card in text, "Could not find old_bot_card"
text = text.replace(old_bot_card, new_bot_card, 1)

# 11. Tab 6 Producer Matrix Plaques Typography and Vertical Spacing
old_p_plaques = '''    // Line 1: Producer Name (Primary)
    gfx_setfont(1, "Orbitron", 10, 'b');
    gfx_r = p_sel ? 0.05 : (p_hov ? 1.00 : 0.85);
    gfx_g = p_sel ? 0.95 : (p_hov ? 0.90 : 0.88);
    gfx_b = p_sel ? 0.68 : (p_hov ? 0.60 : 0.95);
    gfx_x = bx + 6; gfx_y = by + 6;
    gfx_drawstr(get_producer_short(p_idx));

    // Line 2: Band & Track Reference
    gfx_setfont(2, "Arial", 10, 'b');
    gfx_r = p_sel ? 0.95 : (p_hov ? 0.90 : 0.70);
    gfx_g = p_sel ? 0.95 : (p_hov ? 0.85 : 0.75);
    gfx_b = p_sel ? 0.98 : (p_hov ? 0.80 : 0.85);
    gfx_x = bx + 6; gfx_y = by + 26;
    gfx_drawstr(get_producer_band(p_idx));

    // Line 3: Sonic Footprint Spec Badge
    gfx_setfont(2, "Consolas", 9, 'b');
    gfx_r = p_sel ? 0.94 : 0.60;
    gfx_g = p_sel ? 0.56 : 0.65;
    gfx_b = p_sel ? 0.36 : 0.75;
    gfx_x = bx + 6; gfx_y = by + 46;
    gfx_drawstr(get_producer_badge(p_idx));'''

new_p_plaques = '''    // Line 1: Producer Name (Primary)
    gfx_setfont(1, "Orbitron", 12, 'b');
    gfx_r = p_sel ? 0.05 : (p_hov ? 1.00 : 0.85);
    gfx_g = p_sel ? 0.95 : (p_hov ? 0.90 : 0.88);
    gfx_b = p_sel ? 0.68 : (p_hov ? 0.60 : 0.95);
    gfx_x = bx + 8; gfx_y = by + 10;
    gfx_drawstr(get_producer_short(p_idx));

    // Line 2: Band & Track Reference
    gfx_setfont(2, "Arial", 11.5, 'b');
    gfx_r = p_sel ? 0.95 : (p_hov ? 0.90 : 0.70);
    gfx_g = p_sel ? 0.95 : (p_hov ? 0.85 : 0.75);
    gfx_b = p_sel ? 0.98 : (p_hov ? 0.80 : 0.85);
    gfx_x = bx + 8; gfx_y = by + 34;
    gfx_drawstr(get_producer_band(p_idx));

    // Line 3: Sonic Footprint Spec Badge
    gfx_setfont(2, "Consolas", 10.5, 'b');
    gfx_r = p_sel ? 0.94 : 0.60;
    gfx_g = p_sel ? 0.56 : 0.65;
    gfx_b = p_sel ? 0.36 : 0.75;
    gfx_x = bx + 8; gfx_y = by + 58;
    gfx_drawstr(get_producer_badge(p_idx));'''
assert old_p_plaques in text, "Could not find old_p_plaques"
text = text.replace(old_p_plaques, new_p_plaques, 1)

# 12. Tab 6 Blueprint right panel fonts
text = text.replace(
    'gfx_setfont(1, "Orbitron", 13.5, \'b\'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;\n  gfx_x = bp_x + 16; gfx_y = pm_y + 24;\n  gfx_drawstr("FORENSIC BENCHMARK BLUEPRINT");',
    'gfx_setfont(1, "Orbitron", 14, \'b\'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;\n  gfx_x = bp_x + 16; gfx_y = pm_y + 24;\n  gfx_drawstr("FORENSIC BENCHMARK BLUEPRINT");'
)
text = text.replace(
    'gfx_setfont(2, "Consolas", 12, \'b\'); gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;\n  gfx_x = bp_x + 16; gfx_y = pm_y + 48;\n  gfx_printf("TARGET: %s", get_producer_name(slider2));',
    'gfx_setfont(1, "Orbitron", 12.5, \'b\'); gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;\n  gfx_x = bp_x + 16; gfx_y = pm_y + 48;\n  gfx_printf("TARGET: %s", get_producer_name(slider2));'
)
text = text.replace(
    'gfx_setfont(2, "Arial", 11.5, \'b\'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;\n  gfx_x = bp_x + 16; gfx_y = pm_y + 68;\n  gfx_printf("REF   : %s", get_producer_ref_track(slider2));',
    'gfx_setfont(2, "Arial", 12, \'b\'); gfx_r = 0.85; gfx_g = 0.90; gfx_b = 0.98;\n  gfx_x = bp_x + 16; gfx_y = pm_y + 68;\n  gfx_printf("REF   : %s", get_producer_ref_track(slider2));'
)
text = text.replace(
    'gfx_setfont(2, "Consolas", 10.5, \'b\'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;\n  gfx_x = bp_x + 16; gfx_y = pm_y + 88;',
    'gfx_setfont(2, "Consolas", 11.5, \'b\'); gfx_r = 0.94; gfx_g = 0.56; gfx_b = 0.36;\n  gfx_x = bp_x + 16; gfx_y = pm_y + 88;'
)
text = text.replace(
    'gfx_setfont(2, "Consolas", 10.5, \'b\'); gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;\n  gfx_x = bp_x + 16; gfx_y = pm_y + 104;',
    'gfx_setfont(2, "Consolas", 11.5, \'b\'); gfx_r = 0.05; gfx_g = 0.95; gfx_b = 0.68;\n  gfx_x = bp_x + 16; gfx_y = pm_y + 104;'
)

with open(src_file, 'w', encoding='utf-8') as f:
    f.write(text)

# Also copy to REAPER Effects directory
shutil.copy2(src_file, reaper_file)
shutil.copy2(matrix_src, matrix_reaper)

print("Successfully patched and copied Instrumental Suite & Assessment Matrix!")
