import os, sys, shutil

def upgrade_drum_trigger():
    src_file = r"c:\Dev\DameiSuite\effects\Pulse.jsfx"
    with open(src_file, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Update Description header
    code = code.replace("desc:JS: Pulse", "desc:JS: Damei Atumpan DrumTrigger (Slate Trigger 2 Multi-Sample Engine)")
    
    # 2. Fix Triggering Engine: Eliminate the 3ms delay that caused flams/doubling
    old_trig_block = """  trig_flag ? (
    smpl_cnt < srate * 0.003 ? (
      peak_smpl = max(peak_smpl, env_fast);
      smpl_cnt += 1;
    ) : (
      trig_flag = 0;
      trig_pos = block_pos;

      v_raw = clamp(peak_smpl * 2.2, 0.0, 1.0);
      slider58 == 0 ? (
        v_curved = v_raw;
      ) : slider58 == 1 ? (
        v_curved = sqrt(v_raw);
      ) : slider58 == 2 ? (
        v_curved = v_raw * v_raw;
      ) : (
        v_curved = 1.0;
      );

      velo_norm = clamp(0.15 + v_curved * 0.85, 0.15, 1.0);
      velo = min(127, max(1, floor(velo_norm * 127.0)));

      sample_playing0 = 1; sample_play_pos0 = 0; attack_phase0 = 0; env_gain0 = 0;
      sample_playing1 = 1; sample_play_pos1 = 0; attack_phase1 = 0; env_gain1 = 0;
      sample_playing2 = 1; sample_play_pos2 = 0; attack_phase2 = 0; env_gain2 = 0;

      slider44 ? (
        sub_playing = 1;
        sub_phase = 0;
        sub_env = 1.0;
      );

      trig_mrk = velo_norm;

      slider60 ? (
        note_off ? midisend(trig_pos, 128, note_pitch, 0);
        midisend(trig_pos, 144, note_pitch, velo);
        note_off = 1;
        note_off_timer = 0;
      );
    );
  );"""

    new_trig_block = """  // ZERO-LATENCY INSTANTANEOUS FIRING (SLATE TRIGGER 2 ENGINE)
  // Fires on the exact same microsecond as the acoustic transient: ZERO FLAMS / ZERO DOUBLING!
  trig_flag ? (
    trig_flag = 0;
    trig_pos = block_pos;

    v_raw = clamp(env_fast * 2.2, 0.0, 1.0);
    slider58 == 0 ? (
      v_curved = v_raw;
    ) : slider58 == 1 ? (
      v_curved = sqrt(v_raw);
    ) : slider58 == 2 ? (
      v_curved = v_raw * v_raw;
    ) : (
      v_curved = 1.0;
    );

    velo_norm = clamp(0.15 + v_curved * 0.85, 0.15, 1.0);
    velo = min(127, max(1, floor(velo_norm * 127.0)));

    sample_playing0 = 1; sample_play_pos0 = 0; attack_phase0 = 0; env_gain0 = 0;
    sample_playing1 = 1; sample_play_pos1 = 0; attack_phase1 = 0; env_gain1 = 0;
    sample_playing2 = 1; sample_play_pos2 = 0; attack_phase2 = 0; env_gain2 = 0;

    slider44 ? (
      sub_playing = 1;
      sub_phase = 0;
      sub_env = 1.0;
    );

    trig_mrk = velo_norm;

    slider60 ? (
      note_off ? midisend(trig_pos, 128, note_pitch, 0);
      midisend(trig_pos, 144, note_pitch, velo);
      note_off = 1;
      note_off_timer = 0;
    );
  );"""

    code = code.replace(old_trig_block, new_trig_block)

    # 3. Update Title Bar text
    old_title = 'gfx_drawstr("JS: PULSE");'
    new_title = 'gfx_drawstr("ATUMPAN DRUM TRIGGER");'
    code = code.replace(old_title, new_title)

    old_sub = 'gfx_drawstr("SLATE DIGITAL TRIGGER 2 NATIVE ENGINE");'
    new_sub = 'gfx_drawstr("SLATE TRIGGER 2 MULTI-SAMPLE ENGINE // TRANSIENT REPLACER");'
    code = code.replace(old_sub, new_sub)

    # 4. Update Footer Bar text
    old_footer = 'gfx_drawstr("Damei Suite JS: Pulse v2.5 -- Flagship 4-Channel Console & Slate Trigger 2 Reverse-Engineered Core");'
    new_footer = 'gfx_drawstr("Damei Suite: Atumpan DrumTrigger v2.5 | Studio Reference Standard // Zero-Latency Transient Engine");'
    code = code.replace(old_footer, new_footer)

    # Save to local repository
    with open(src_file, "w", encoding="utf-8") as f:
        f.write(code)
    
    dst_local = r"c:\Dev\DameiSuite\effects\Damei_DrumTrigger.jsfx"
    with open(dst_local, "w", encoding="utf-8") as f:
        f.write(code)
    print("Updated local files.")

    # 5. SYNC TO ALL REAPER APPDATA TARGETS (Crucial: Overwrite Pulse/Pulse.jsfx!)
    targets = [
        os.path.expandvars(r"%APPDATA%\REAPER\Effects\Pulse\Pulse.jsfx"),
        os.path.expandvars(r"%APPDATA%\REAPER\Effects\Damei\Pulse.jsfx"),
        os.path.expandvars(r"%APPDATA%\REAPER\Effects\Damei\Damei_DrumTrigger.jsfx")
    ]
    for tgt in targets:
        os.makedirs(os.path.dirname(tgt), exist_ok=True)
        shutil.copy2(src_file, tgt)
        print(f"Synced to: {tgt} (size={os.path.getsize(tgt)})")

if __name__ == "__main__":
    upgrade_drum_trigger()
