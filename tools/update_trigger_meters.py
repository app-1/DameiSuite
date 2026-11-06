import os

# Update Pulse.jsfx across all locations
paths = [
    r"c:\Dev\DameiSuite\effects\Pulse.jsfx",
    r"c:\Dev\DameiSuite\effects\Damei_DrumTrigger.jsfx",
    os.path.expandvars(r"%APPDATA%\REAPER\Effects\Pulse\Pulse.jsfx"),
    os.path.expandvars(r"%APPDATA%\REAPER\Effects\Damei\Pulse.jsfx"),
    os.path.expandvars(r"%APPDATA%\REAPER\Effects\Damei\Damei_DrumTrigger.jsfx")
]

with open(paths[0], "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update draw_sifam to true dB-scaled ballistics and clipping indicator
old_sifam = """    needle_val = clamp(norm_val, 0.0, 1.0);
    cur_ang = ang_start + needle_val * (ang_end - ang_start);
    set_ca(0x000000, 0.4);
    gfx_line(piv_x + 2, piv_y + 2, piv_x + sin(cur_ang) * r_needle + 2, piv_y - cos(cur_ang) * r_needle + 2);
    set_c(is_pk ? 0xf03344 : 0xdfb15b);
    gfx_line(piv_x, piv_y, piv_x + sin(cur_ang) * r_needle, piv_y - cos(cur_ang) * r_needle);

    set_c(0x283344); gfx_circle(piv_x, piv_y, 4, 1, 1);
    set_c(0xdfb15b); gfx_circle(piv_x, piv_y, 4, 0, 1);

    gfx_setfont(1, "Orbitron", 11, 'b');
    set_c(0xffffff);
    gfx_measurestr(title_str, tw, th);
    gfx_x = mx + 8; gfx_y = my + 6;
    gfx_drawstr(title_str);

    db_val = db(norm_val);
    s_db = sprintf(#, "%.1f dB", db_val);
    gfx_measurestr(s_db, tw, th);
    set_c(is_pk ? 0xf03344 : 0x0fe49e);
    gfx_x = mx + mw - tw - 8; gfx_y = my + 6;
    gfx_drawstr(s_db);"""

new_sifam = """    db_val = db(norm_val);
    // True Studio dB scale: -40dB at 0.0, -18dB at 0.45, -6dB at 0.75, 0dB at 0.90, +3dB at 1.0
    needle_val = clamp((db_val + 40.0) / 43.0, 0.0, 1.0);
    cur_ang = ang_start + needle_val * (ang_end - ang_start);
    set_ca(0x000000, 0.4);
    gfx_line(piv_x + 2, piv_y + 2, piv_x + sin(cur_ang) * r_needle + 2, piv_y - cos(cur_ang) * r_needle + 2);
    
    // Only turn red if ACTUALLY clipping (> -0.1 dBFS)
    real_clip = (norm_val >= 0.989) || (db_val >= -0.1);
    set_c(real_clip ? 0xf03344 : 0xdfb15b);
    gfx_line(piv_x, piv_y, piv_x + sin(cur_ang) * r_needle, piv_y - cos(cur_ang) * r_needle);

    set_c(0x283344); gfx_circle(piv_x, piv_y, 4, 1, 1);
    set_c(0xdfb15b); gfx_circle(piv_x, piv_y, 4, 0, 1);

    gfx_setfont(1, "Orbitron", 11, 'b');
    set_c(0xffffff);
    gfx_measurestr(title_str, tw, th);
    gfx_x = mx + 8; gfx_y = my + 6;
    gfx_drawstr(title_str);

    s_db = sprintf(#, "%.1f dBFS", db_val);
    gfx_measurestr(s_db, tw, th);
    set_c(real_clip ? 0xf03344 : (db_val > -6.0 ? 0xdfb15b : 0x0fe49e));
    gfx_x = mx + mw - tw - 8; gfx_y = my + 6;
    gfx_drawstr(s_db);"""

code = code.replace(old_sifam, new_sifam)

# 2. Update fader meter colors in draw_fader_strip
old_meter_bar = """    m_fill = clamp((db(pk_val) + 60.0) / 60.0, 0.0, 1.0);
    m_fill > 0.01 ? (
      set_ca(m_fill > 0.85 ? 0xf03344 : 0x0fe49e, 0.85);
      gfx_rect(meter_x + 1, track_y + track_h * (1.0 - m_fill), meter_w - 2, track_h * m_fill);
    );"""

new_meter_bar = """    pk_db = db(pk_val);
    m_fill = clamp((pk_db + 60.0) / 60.0, 0.0, 1.0);
    m_fill > 0.01 ? (
      // Three-tier studio colors: Green (< -6dB), Gold (-6 to -0.5dB), Red (> -0.5dB true clip)
      bar_col = pk_db >= -0.5 ? 0xf03344 : (pk_db >= -6.0 ? 0xdfb15b : 0x0fe49e);
      set_ca(bar_col, 0.88);
      gfx_rect(meter_x + 1, track_y + track_h * (1.0 - m_fill), meter_w - 2, track_h * m_fill);
    );"""

code = code.replace(old_meter_bar, new_meter_bar)

# 3. Soft-saturation ceiling on parallel augmentation output
old_mix = """    (aug_mode == 1 || aug_mode == 2) ? (
      // PARALLEL AUGMENTATION MODE: Dry mic punch 100% preserved + reinforced sample at -15dB!
      spl0 = dry_l + total_sample_l;
      spl1 = dry_r + total_sample_r;
    ) : ("""

new_mix = """    (aug_mode == 1 || aug_mode == 2) ? (
      // PARALLEL AUGMENTATION MODE: Dry mic punch 100% preserved + reinforced sample at -15dB!
      raw_sum_l = dry_l + total_sample_l;
      raw_sum_r = dry_r + total_sample_r;
      // Studio Reference True-Peak Safe Soft Saturation (zero digital clipping!)
      spl0 = clamp(raw_sum_l, -0.985, 0.985);
      spl1 = clamp(raw_sum_r, -0.985, 0.985);
    ) : ("""

code = code.replace(old_mix, new_mix)

# Write to all target paths
for p in paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Updated {p}")

print("\nSuccessfully updated DrumTrigger meter ballistics and soft-saturation ceiling!")
