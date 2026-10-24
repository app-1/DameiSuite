# Move draw_eq_fader to top level of @gfx
with open(r'c:\Dev\DameiSuite\scratch\gen_instrumental_flagship_v8.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Definition of draw_eq_fader
fader_def = """function draw_eq_fader(f_idx, f_x, f_y, f_w, f_h, title, freq_lbl, val, min_v, max_v, s_idx) local(v_str, trk_y, trk_h, trk_x, f_frac, th_y, hov, new_frac) (
  gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(f_x, f_y, f_w - 6, f_h);
  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(f_x, f_y, f_w - 6, f_h, 0);

  gfx_setfont(1, "Orbitron", 11, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
  gfx_x = f_x + 10; gfx_y = f_y + 10; gfx_drawstr(title);
  gfx_setfont(2, "Consolas", 10, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
  gfx_x = f_x + 10; gfx_y = f_y + 28; gfx_drawstr(freq_lbl);

  v_str = sprintf(#, "%+3.1f dB", val);
  gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = f_x + 10; gfx_y = f_y + 48; gfx_drawstr(v_str);

  // Track & Thumb
  trk_y = f_y + 80; trk_h = f_h - 96;
  trk_x = f_x + floor((f_w - 6) * 0.5) - 3;
  gfx_r = 0.04; gfx_g = 0.06; gfx_b = 0.08; gfx_rect(trk_x, trk_y, 6, trk_h);
  gfx_r = 0.30; gfx_g = 0.40; gfx_b = 0.55; gfx_rect(trk_x, trk_y, 6, trk_h, 0);

  f_frac = clamp((val - min_v) / (max_v - min_v), 0.0, 1.0);
  th_y = trk_y + trk_h - floor(f_frac * trk_h);

  gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
  gfx_rect(trk_x - 14, th_y - 8, 34, 16);
  gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0; gfx_rect(trk_x - 14, th_y - 8, 34, 16, 0);

  // Interactive Drag
  hov = (mouse_x >= f_x && mouse_x <= f_x + f_w - 6 && mouse_y >= trk_y - 10 && mouse_y <= trk_y + trk_h + 10);
  mouse_clicked && hov ? eq_drag_slider = s_idx;
  eq_drag_slider == s_idx && mouse_down ? (
    new_frac = clamp((trk_y + trk_h - mouse_y) / trk_h, 0.0, 1.0);
    slider(s_idx) = min_v + new_frac * (max_v - min_v);
    update_filters(); slider_automate();
  );
);"""

# Remove old function definition from Tab 1
old_in_tab1 = """  function draw_eq_fader(f_idx, f_x, title, freq_lbl, val, min_v, max_v, s_idx) (
    gfx_r = 0.016; gfx_g = 0.022; gfx_b = 0.030; gfx_rect(f_x, f_y, f_w - 6, f_h);
    gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22; gfx_rect(f_x, f_y, f_w - 6, f_h, 0);

    gfx_setfont(1, "Orbitron", 11, 'b'); gfx_r = 1.0; gfx_g = 0.85; gfx_b = 0.30;
    gfx_x = f_x + 10; gfx_y = f_y + 10; gfx_drawstr(title);
    gfx_setfont(2, "Consolas", 10, 'b'); gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00;
    gfx_x = f_x + 10; gfx_y = f_y + 28; gfx_drawstr(freq_lbl);

    v_str = sprintf(#, "%+3.1f dB", val);
    gfx_setfont(1, "Orbitron", 13, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
    gfx_x = f_x + 10; gfx_y = f_y + 48; gfx_drawstr(v_str);

    // Track & Thumb
    trk_y = f_y + 80; trk_h = f_h - 96;
    trk_x = f_x + floor((f_w - 6) * 0.5) - 3;
    gfx_r = 0.04; gfx_g = 0.06; gfx_b = 0.08; gfx_rect(trk_x, trk_y, 6, trk_h);
    gfx_r = 0.30; gfx_g = 0.40; gfx_b = 0.55; gfx_rect(trk_x, trk_y, 6, trk_h, 0);

    f_frac = clamp((val - min_v) / (max_v - min_v), 0.0, 1.0);
    th_y = trk_y + trk_h - floor(f_frac * trk_h);

    gfx_r = 0.85; gfx_g = 0.70; gfx_b = 0.22;
    gfx_rect(trk_x - 14, th_y - 8, 34, 16);
    gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0; gfx_rect(trk_x - 14, th_y - 8, 34, 16, 0);

    // Interactive Drag
    hov = (mouse_x >= f_x && mouse_x <= f_x + f_w - 6 && mouse_y >= trk_y - 10 && mouse_y <= trk_y + trk_h + 10);
    mouse_clicked && hov ? eq_drag_slider = s_idx;
    eq_drag_slider == s_idx && mouse_down ? (
      new_frac = clamp((trk_y + trk_h - mouse_y) / trk_h, 0.0, 1.0);
      slider(s_idx) = min_v + new_frac * (max_v - min_v);
      update_filters(); slider_automate();
    );
  );"""

text = text.replace(old_in_tab1, "")

# Insert fader_def right before draw_sifam_meter
target_insert = "// Strictly Confined Vintage SIFAM Moving-Coil Meter"
text = text.replace(target_insert, fader_def + "\n\n" + target_insert)

# Update calls in Tab 1 to pass f_y, f_w, f_h
text = text.replace('draw_eq_fader(0, ws_x + 12 + 0 * f_w, "HPF SUB-CUT"',
                    'draw_eq_fader(0, ws_x + 12 + 0 * f_w, f_y, f_w, f_h, "HPF SUB-CUT"')
text = text.replace('draw_eq_fader(1, ws_x + 12 + 1 * f_w, "LOW SHELF"',
                    'draw_eq_fader(1, ws_x + 12 + 1 * f_w, f_y, f_w, f_h, "LOW SHELF"')
text = text.replace('draw_eq_fader(2, ws_x + 12 + 2 * f_w, "MUD SCOOP"',
                    'draw_eq_fader(2, ws_x + 12 + 2 * f_w, f_y, f_w, f_h, "MUD SCOOP"')
text = text.replace('draw_eq_fader(3, ws_x + 12 + 3 * f_w, "MID BODY"',
                    'draw_eq_fader(3, ws_x + 12 + 3 * f_w, f_y, f_w, f_h, "MID BODY"')
text = text.replace('draw_eq_fader(4, ws_x + 12 + 4 * f_w, "PICK BITE"',
                    'draw_eq_fader(4, ws_x + 12 + 4 * f_w, f_y, f_w, f_h, "PICK BITE"')
text = text.replace('draw_eq_fader(5, ws_x + 12 + 5 * f_w, "AIR SHEEN"',
                    'draw_eq_fader(5, ws_x + 12 + 5 * f_w, f_y, f_w, f_h, "AIR SHEEN"')

with open(r'c:\Dev\DameiSuite\scratch\gen_instrumental_flagship_v8.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Moved draw_eq_fader to top level successfully")
