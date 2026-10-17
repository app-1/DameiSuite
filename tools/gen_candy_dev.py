"""Devastator Suite: Producer Trailer Playbook (smart, region + energy aware trigger rules per producer)."""
import re
import gen_candy as gc

P = gc.DIR + r'\Damei_DevastatorSuite.jsfx'

# producers in slider2 order: (flags 1=SUCK-BACK 2=CHORUS DIVE 4=BREAKDOWN DIVE, escalation rule, signature event, min dB, tips)
PB = [
 ('Jordan Fish', 3, 1, 1, -44, ["Builds the album like a film: first chorus held back.",
                                "Suck-back leads into each later chorus, then the sub hits.",
                                "Signature move: the pull-back before the biggest drop.",
                                "Subtle sub divebomb only when the chorus is truly bigger."]),
 ('Mick Gordon', 6, 0, 2, -40, ["Hits, not builds: sub divebomb on every chorus entry.",
                                "Breakdown entrances get the same weight.",
                                "No suck-back: the impact IS the transition.",
                                "Everything fires at full conviction, nothing washy."]),
 ('Chris Bedan', 7, 3, 1, -44, ["Cinematic tension: suck-back before later choruses.",
                                "Sub divebomb only when the energy is rising vs the song.",
                                "Breakdowns get a dive when the groove is still building.",
                                "Restraint then release: it waits for the real peak."]),
 ('Dan Braunstein', 1, 2, 1, -46, ["Elegant restraint: suck-back on every second chorus only.",
                                   "No sub bombs; the vocal stays the star.",
                                   "The pull-back is quiet and short, never theatrical.",
                                   "Silence before the hook does the real work."]),
 ('Buster Odeholm', 6, 0, 4, -40, ["Djent weight: sub divebomb on every breakdown entrance.",
                                   "Chorus hits get the same low-end drop.",
                                   "No risers or suck-backs; just silence then impact.",
                                   "Signature move: the breakdown drop."]),
 ('Bad Omens', 3, 3, 1, -44, ["Dark pop tension: suck-back before later choruses.",
                              "Sub divebomb only when the chorus out-energies the song.",
                              "Skips the first chorus; the second is the payoff.",
                              "Pull back, then punch. Never both at once."]),
 ('Lance Prenc', 6, 1, 2, -40, ["Heavy and precise: sub divebomb on chorus and breakdown.",
                                "Skips the first chorus; the later ones hit harder.",
                                "No suck-back; straight into the impact.",
                                "Signature move: the chorus divebomb."]),
 ('George Lever', 1, 1, 1, -48, ["Slow burn: a long suck-back, but only from chorus two on.",
                                 "No sub bombs; the drop stays organic.",
                                 "Keeps it rare so every fire feels earned.",
                                 "Signature move: the pull-back before the final chorus."]),
]
ESC = ['every chorus', 'skips first chorus', 'every 2nd chorus', 'escalates with energy']
for r in PB:
    bad = [x for x in r[5] if len(x) > 58]
    assert len(r[5]) == 4 and not bad, (r[0], bad)

TABLES = []
for i, (nm, fl, esc, sig, thr, tips) in enumerate(PB):
    TABLES.append('pb_f[%d] = %d; pb_e[%d] = %d; pb_s[%d] = %d; pb_t[%d] = %d;' % (i, fl, i, esc, i, sig, i, thr))
    TABLES.append('pb_n[%d] = "%s";' % (i, nm))
    for n, tp in enumerate(tips):
        TABLES.append('pb_tip[%d] = "%s";' % (i * 4 + n, tp))
for i, e in enumerate(ESC):
    TABLES.append('pb_er[%d] = "%s";' % (i, e))

INIT = r'''
// ===== TRAILER PLAYBOOK BEGIN (producer-specific, region + energy aware trigger rules) =====
// Per producer: which of the three trailer events may fire (pre-chorus suck-back, chorus sub divebomb,
// breakdown sub divebomb), an escalation rule (every chorus / skip first / every 2nd / only when energy rises)
// and a minimum master level. The playbook decides at each region entrance; every decision is logged.
pb_f = 1900000; pb_e = 1900010; pb_s = 1900020; pb_t = 1900030; pb_n = 1900040;
pb_er = 1900060; pb_tip = 1900100;
@@TABLES@@
dv_ch_seen = 0; dv_cnt_rgn = -1; dv_brk_rgn = -1; dv_song_db = -30.0; dv_p = 0;
strcpy(#dv_w1, "Waiting for playback..."); strcpy(#dv_w2, ""); strcpy(#dv_w3, "");

function dv_log(ev, fired, n) (
  strcpy(#dv_w3, #dv_w2); strcpy(#dv_w2, #dv_w1);
  sprintf(#dv_w1, "%s %s  |  chorus %d  |  %s", fired ? "FIRED" : "HELD ",
          ev == 1 ? "suck-back" : (ev == 2 ? "sub divebomb" : "breakdown dive"), n, pb_er[pb_e[dv_p]]);
);

function dv_pb_rule(ev) local(ok) (
  ok = ((pb_f[dv_p] & ev) != 0);
  (slider68 == 0) ? ( ok = (pb_s[dv_p] == ev); );
  (slider68 == 2) ? ( ok = 1; );
  ok;
);

function dv_pb_esc(ev, n) local(e, g) (
  e = pb_e[dv_p]; g = 1;
  (e == 1) ? ( g = (n >= 2); );
  (e == 2) ? ( g = ((n % 2) == 0); );
  (e == 3) ? (
    (ev == 1) ? ( g = (n >= 2); ) : ( g = (mst_rms >= dv_song_db + 1.0); );
  );
  (ev == 4 && (e == 1 || e == 2)) ? ( g = 1; );
  (slider68 == 2) ? ( g = 1; );
  g;
);

function dv_playbook() local(n, lvl, go) (
  dv_p = max(0, min(7, floor(slider2 + 0.5)));
  lvl = (mst_rms > pb_t[dv_p]);

  // 1) pre-chorus suck-back: timed to land on the chorus downbeat; evaluated once per upcoming chorus
  (g_to_chorus_sec > 0.05 && g_to_chorus_sec <= slider21 + 0.03 && g_to_chorus_sec >= slider21 - 0.25 && !suck_active) ? (
    dv_chorus_abs = play_position + g_to_chorus_sec;
    n = dv_ch_seen + 1;
    (abs(dv_chorus_abs - dv_fire_chorus_abs) > 1.0 && dv_cool) ? (
      go = dv_pb_rule(1) && dv_pb_esc(1, n);
      go ? ( trigger_reversed_suckback(); dv_last_fire_t = time_precise(); );
      dv_fire_chorus_abs = dv_chorus_abs;
      dv_log(1, go, n);
    );
  );

  // 2) chorus entrance: count it, then sub divebomb if the playbook allows
  (g_sec_id == 3 && g_rgn_progress < 0.08 && g_cur_rgn != dv_cnt_rgn) ? (
    n = dv_ch_seen + 1; dv_ch_seen = n; dv_cnt_rgn = g_cur_rgn;
    go = dv_pb_rule(2) && dv_pb_esc(2, n) && lvl && !sub_active;
    go ? ( trigger_sub_divebomb(); );
    dv_log(2, go, n);
  );

  // 3) breakdown entrance
  (g_sec_id == 4 && g_rgn_progress < 0.06 && g_cur_rgn != dv_brk_rgn) ? (
    dv_brk_rgn = g_cur_rgn;
    go = dv_pb_rule(4) && dv_pb_esc(4, dv_ch_seen) && lvl && !sub_active;
    go ? ( trigger_sub_divebomb(); );
    dv_log(4, go, dv_ch_seen);
  );
);
// ===== TRAILER PLAYBOOK END =====

'''.replace('@@TABLES@@', '\n'.join(TABLES))

GUI = r'''// ===== TRAILER PLAYBOOK GUI BEGIN =====
function dv_pb_row(x, y, w, lbl, on) local(tw, th) (
  gfx_setfont(1, "Consolas", 13, 'b'); gfx_r = 0.88; gfx_g = 0.92; gfx_b = 0.98;
  gfx_x = x; gfx_y = y; gfx_drawstr(lbl);
  on ? ( gfx_r = 0.20; gfx_g = 0.95; gfx_b = 0.55; ) : ( gfx_r = 0.45; gfx_g = 0.45; gfx_b = 0.52; );
  gfx_measurestr(on ? "ARMED" : "OFF", tw, th);
  gfx_x = x + w - tw; gfx_y = y; gfx_drawstr(on ? "ARMED" : "OFF");
  gfx_r = 0.12; gfx_g = 0.14; gfx_b = 0.20; gfx_line(x, y + 20, x + w, y + 20);
);

function dv_pb_gui(gx, gy, gw, gh) local(cw, lx, rx, ty, p, i, k, tw, th, sx, bw, hv, f, e, s) (
  gfx_r = 0.016; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(gx, gy, gw, gh);
  gfx_r = 0.70; gfx_g = 0.12; gfx_b = 0.24; gfx_rect(gx, gy, gw, gh, 0);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.30;
  gfx_x = gx + 16; gfx_y = gy + 12; gfx_drawstr("TRAILER PLAYBOOK  //  PRODUCER-AWARE TRIGGERS");
  gfx_setfont(1, "Consolas", 12, 'b'); gfx_r = 0.62; gfx_g = 0.68; gfx_b = 0.78;
  gfx_x = gx + 16; gfx_y = gy + 36; gfx_drawstr("Fires only while playing, only at section entrances, only when the producer's rules and the energy agree.");

  p = max(0, min(7, floor(slider2 + 0.5)));
  cw = floor((gw - 48) / 2); lx = gx + 16; rx = lx + cw + 16; ty = gy + 64;

  // mode toggle
  pill_toggle(lx, ty, cw, 28, slider67 ? "PLAYBOOK ON: REGION + ENERGY AWARE" : "CLASSIC SMART TRIGGERS", slider67) ? (
    slider67 = !slider67; slider_automate();
  );

  // intensity selector
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.95; gfx_g = 0.90; gfx_b = 0.95;
  gfx_x = lx; gfx_y = ty + 42; gfx_drawstr("INTENSITY");
  bw = floor((cw - 12) / 3);
  i = 0;
  loop(3,
    sx = lx + i * (bw + 6);
    pill_toggle(sx, ty + 64, bw, 26, i == 0 ? "SIGNATURE" : (i == 1 ? "PLAYBOOK" : "FULL"), slider68 == i) ? (
      slider68 = i; slider_automate();
    );
    i += 1;
  );

  // rules for the active producer
  f = pb_f[p]; e = pb_e[p]; s = pb_s[p];
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.00; gfx_g = 0.20; gfx_b = 0.30;
  gfx_x = lx; gfx_y = ty + 106; gfx_drawstr(pb_n[p]);
  gfx_setfont(1, "Consolas", 12, 'b'); gfx_r = 0.62; gfx_g = 0.68; gfx_b = 0.78;
  gfx_x = lx; gfx_y = ty + 124; gfx_drawstr("(change the producer in the Hub view)");
  dv_pb_row(lx, ty + 148, cw, (s == 1) ? "* Pre-chorus suck-back" : "  Pre-chorus suck-back", (f & 1) != 0 || slider68 == 2);
  dv_pb_row(lx, ty + 172, cw, (s == 2) ? "* Chorus sub divebomb" : "  Chorus sub divebomb", (f & 2) != 0 || slider68 == 2);
  dv_pb_row(lx, ty + 196, cw, (s == 4) ? "* Breakdown sub divebomb" : "  Breakdown sub divebomb", (f & 4) != 0 || slider68 == 2);
  gfx_setfont(1, "Consolas", 13, 'b'); gfx_r = 0.88; gfx_g = 0.92; gfx_b = 0.98;
  gfx_x = lx; gfx_y = ty + 224; gfx_drawstr("Rule:");
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.30; gfx_x = lx + 60; gfx_drawstr(slider68 == 2 ? "every event (full arsenal)" : pb_er[e]);
  gfx_r = 0.88; gfx_g = 0.92; gfx_b = 0.98; gfx_x = lx; gfx_y = ty + 246; gfx_drawstr("Min level:");
  gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.30; gfx_x = lx + 100; sprintf(#dv_ml, "%d dB", pb_t[p]); gfx_drawstr(#dv_ml);

  // right: tips + live decision log
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.00; gfx_g = 0.85; gfx_b = 0.30;
  gfx_x = rx; gfx_y = ty; gfx_drawstr("PRODUCER PLAYBOOK");
  gfx_setfont(1, "Consolas", 12, 'b');
  k = 0;
  loop(4,
    gfx_r = 0.20; gfx_g = 0.95; gfx_b = 0.85;
    gfx_x = rx; gfx_y = ty + 26 + k * 22; gfx_drawstr("- "); gfx_drawstr(pb_tip[p * 4 + k]);
    k += 1;
  );
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 1.00; gfx_g = 0.20; gfx_b = 0.30;
  gfx_x = rx; gfx_y = ty + 130; gfx_drawstr("LIVE DECISIONS");
  gfx_setfont(1, "Consolas", 12, 'b'); gfx_r = 0.62; gfx_g = 0.68; gfx_b = 0.78;
  gfx_x = rx; gfx_y = ty + 154; sprintf(#dv_st, "transport: %s   choruses seen: %d   song level: %d dB", dv_playing ? "PLAYING" : "stopped", dv_ch_seen, floor(dv_song_db));
  gfx_drawstr(#dv_st);
  gfx_r = 0.95; gfx_g = 0.97; gfx_b = 1.00; gfx_x = rx; gfx_y = ty + 180; gfx_drawstr(#dv_w1);
  gfx_r = 0.70; gfx_g = 0.74; gfx_b = 0.82; gfx_x = rx; gfx_y = ty + 200; gfx_drawstr(#dv_w2);
  gfx_r = 0.50; gfx_g = 0.54; gfx_b = 0.62; gfx_x = rx; gfx_y = ty + 220; gfx_drawstr(#dv_w3);

  // manual fire buttons (always available)
  pill_toggle(rx, ty + 252, floor((cw - 8) / 2), 26, "FIRE SUCK-BACK", 0) ? ( trigger_reversed_suckback(); );
  pill_toggle(rx + floor((cw - 8) / 2) + 8, ty + 252, floor((cw - 8) / 2), 26, "FIRE SUB DIVE", 0) ? ( trigger_sub_divebomb(); );
);
// ===== TRAILER PLAYBOOK GUI END =====

'''


def patch_dev():
    t, crlf = gc.rd(P)
    assert 'TRAILER PLAYBOOK BEGIN' not in t, 'already patched; restore backup first'
    # sliders
    t = gc.sub1(t, 'slider1:0<0,2,1{1. Devastator Hub & Vital Envelopes,2. Reactor Core & DSP Sound Bays,3. Mix-Fit ReEQ & Master Compressor}>',
                'slider1:0<0,3,1{1. Devastator Hub & Vital Envelopes,2. Reactor Core & DSP Sound Bays,3. Mix-Fit ReEQ & Master Compressor,4. Producer Trailer Playbook}>')
    t = gc.sub1(t, 'slider66:1<0,1,1{Off,On}>-Matrix Trim (applies Assessment Matrix auto-correct lane)\n',
                'slider66:1<0,1,1{Off,On}>-Matrix Trim (applies Assessment Matrix auto-correct lane)\n'
                'slider67:1<0,1,1{Classic Smart Triggers,Producer Playbook (Region + Energy Aware)}>-Trailer Playbook Mode\n'
                'slider68:1<0,2,1{Signature Only,Producer Playbook,Full Arsenal}>-Trailer Playbook Intensity\n')
    # init: kernel before the blueprint function
    t = gc.sub1(t, 'function apply_producer_blueprint(p_idx) (\n', INIT + 'function apply_producer_blueprint(p_idx) (\n')
    # block: reset counters on stop; route to the playbook
    t = gc.sub1(t, 'dv_cool = (time_precise() - dv_last_fire_t) > 6.0;\n',
                '!dv_playing ? ( dv_ch_seen = 0; dv_cnt_rgn = -1; dv_brk_rgn = -1; );\n'
                'dv_jump ? ( dv_cnt_rgn = -1; dv_brk_rgn = -1; );\n'
                '(dv_playing && mst_active) ? ( dv_song_db += (mst_rms - dv_song_db) * 0.0008; );\n'
                'dv_cool = (time_precise() - dv_last_fire_t) > 6.0;\n')
    a = t.index('(slider4 >= 1 && slider49 == 0 && dv_playing')
    b = t.index('\ngmem[900] = 1;', a)
    old = t[a:b]
    head = '(slider4 >= 1 && slider49 == 0 && dv_playing && dv_bridge_ok && mst_active && mst_rms > -48.0) ? (\n'
    assert old.startswith(head)
    inner = old[len(head):].rstrip()
    assert inner.endswith(');')
    inner = inner[:-2].rstrip('\n')
    new = head + '  slider67 == 1 ? (\n    dv_playbook();\n  ) : (\n' + inner + '\n  );\n);\n'
    t = t[:a] + new + t[b:]
    # header: view buttons (compact so 4 fit next to the title) + new button
    a = t.index('vm3_w = 135;')
    b = t.index('// 1. HUB BUTTON')
    t = t[:a] + (
        'vm4_w = 98;\n'
        'vm4_x = bake_x - vm4_w - 12;\n'
        'vm4_act = (slider1 == 3);\n'
        'vm4_hov = (mouse_x >= vm4_x && mouse_x <= vm4_x + vm4_w && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);\n\n'
        'vm3_w = 84;\n'
        'vm3_x = vm4_x - vm3_w - 6;\n'
        'vm3_act = (slider1 == 2);\n'
        'vm3_hov = (mouse_x >= vm3_x && mouse_x <= vm3_x + vm3_w && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);\n\n'
        'vm2_w = 62;\n'
        'vm2_x = vm3_x - vm2_w - 6;\n'
        'vm2_act = (slider1 == 1);\n'
        'vm2_hov = (mouse_x >= vm2_x && mouse_x <= vm2_x + vm2_w && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);\n\n'
        'vm1_w = 56;\n'
        'vm1_x = vm2_x - vm1_w - 6;\n'
        'vm1_act = (slider1 == 0);\n'
        'vm1_hov = (mouse_x >= vm1_x && mouse_x <= vm1_x + vm1_w && mouse_y >= btn_y && mouse_y <= btn_y + btn_h);\n\n') + t[b:]
    t = gc.sub1(t, 'v1_lbl = "1. HUB";', 'v1_lbl = "HUB";')
    t = gc.sub1(t, 'v2_lbl = "2. DSP BAYS";', 'v2_lbl = "BAYS";')
    t = gc.sub1(t, 'v3_lbl = "3. EQ & COMP";', 'v3_lbl = "MIX-FIT";')
    btn4 = (
        '// 4. PLAYBOOK BUTTON\n'
        'gfx_r = vm4_act ? 0.70 : (vm4_hov ? 0.25 : 0.08);\n'
        'gfx_g = vm4_act ? 0.12 : (vm4_hov ? 0.28 : 0.10);\n'
        'gfx_b = vm4_act ? 0.25 : (vm4_hov ? 0.36 : 0.14);\n'
        'gfx_rect(vm4_x, btn_y, vm4_w, btn_h);\n'
        'gfx_r = vm4_act ? 1.00 : 0.35; gfx_g = vm4_act ? 0.85 : 0.40; gfx_b = vm4_act ? 0.30 : 0.50;\n'
        'gfx_rect(vm4_x, btn_y, vm4_w, btn_h, 0);\n'
        'gfx_setfont(1, "Orbitron", 12, \'b\'); gfx_r = vm4_act ? 1.0 : 0.85; gfx_g = vm4_act ? 1.0 : 0.88; gfx_b = 1.0;\n'
        'v4_lbl = "PLAYBOOK";\n'
        'gfx_measurestr(v4_lbl, v4w, v4h);\n'
        'gfx_x = vm4_x + (vm4_w - v4w) * 0.5; gfx_y = btn_y + 8;\n'
        'gfx_drawstr(v4_lbl);\n\n'
        'mouse_clicked && vm4_hov ? (slider1 = 3; slider_automate(););\n\n')
    t = gc.sub1(t, '// ⚡ HYBRID ENGINE BUTTON: [ ⤓ BAKE TRACK ]', btn4 + '// ⚡ HYBRID ENGINE BUTTON: [ ⤓ BAKE TRACK ]')
    # gui view
    t = gc.sub1(t, 'slider1 == 2 ? (\n  dsp_dirty = 0;',
                GUI + 'slider1 == 3 ? (\n  dv_pb_gui(14, main_y, gfx_w - 28, main_h);\n);\n\nslider1 == 2 ? (\n  dsp_dirty = 0;')
    gc.wr(P, t, crlf)
    print('devastator ok')


if __name__ == '__main__':
    patch_dev()
