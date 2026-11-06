import os, sys, shutil

def apply_elevation():
    pulse_file = r"c:\Dev\DameiSuite\effects\Pulse.jsfx"
    with open(pulse_file, "r", encoding="utf-8") as f:
        p_code = f.read()

    # 1. Update Description header
    p_code = p_code.replace("desc:JS: Pulse", "desc:JS: Damei Atumpan DrumTrigger (Slate Trigger 2 Multi-Sample Engine)")
    
    # 2. Add mask_decay in @slider
    old_slider_end = "sub_decay_coeff = exp(-1.0 / (srate * (slider46 / 1000.0)));"
    new_slider_end = """sub_decay_coeff = exp(-1.0 / (srate * (slider46 / 1000.0)));
  mask_decay = exp(-1.0 / (srate * 0.120)); // 120ms Slate Trigger 2 exponential retrigger mask"""
    if old_slider_end in p_code and "mask_decay" not in p_code:
        p_code = p_code.replace(old_slider_end, new_slider_end)

    # 3. Replace trigger detection block with Slate Trigger 2 Adaptive Mask & Derivative
    old_det_marker = "  trig_flag ? ("
    # We want to replace the whole trigger block from retrig_cnt > retrig_samples to the end of trig_flag
    old_detection_section = """  retrig_cnt > retrig_samples ? (
    env_fast > threshold && env_slow > 0.00001 && (env_fast / max(env_slow, 0.000001) > sensitivity) ? (
      is_bleed = bleed_enable && (bleed_env > bleed_thresh) && ((bleed_env * bleed_sens) > env_fast);
      is_bleed ? (
        bleed_gated_cnt = floor(srate * 0.05);
      ) : (
        trig_flag = 1;
        retrig_cnt = 0;
        smpl_cnt = 0;
        peak_smpl = 0;
        lockout_timer = retrig_samples;
      );
    );
  );

  bleed_gated_cnt > 0 ? bleed_gated_cnt -= 1;
  lockout_timer > 0 ? lockout_timer -= 1;

  // ZERO-LATENCY INSTANTANEOUS FIRING (SLATE TRIGGER 2 ENGINE)
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

    new_detection_section = """  // SLATE DIGITAL TRIGGER 2 ADAPTIVE EXPONENTIAL MASK & TRANSIENT DERIVATIVE
  // Solves the double-triggering / flam bug by ignoring ringing tails and machine-gun re-triggers!
  retrigger_mask *= mask_decay;
  lockout_timer > 0 ? lockout_timer -= 1;
  bleed_gated_cnt > 0 ? bleed_gated_cnt -= 1;

  // Transient onset slope (rising edge derivative)
  trans_slope = env_fast - last_env_fast;
  last_env_fast = env_fast;

  // Trigger Condition:
  // 1. Minimum physical lockout (slider4 ms) has expired
  // 2. Fast envelope punches above absolute threshold
  // 3. Fast envelope punches above decaying mask from previous hit
  // 4. Signal is on an EXPLOSIVE RISING EDGE (trans_slope > threshold * 0.10)
  lockout_timer == 0 && env_fast > threshold && env_fast > retrigger_mask && trans_slope > (threshold * 0.10) ? (
    is_bleed = bleed_enable && (bleed_env > bleed_thresh) && ((bleed_env * bleed_sens) > env_fast);
    is_bleed ? (
      bleed_gated_cnt = floor(srate * 0.05);
    ) : (
      // ZERO-LATENCY SAMPLE-ACCURATE INSTANT TRIGGER
      lockout_timer = retrig_samples;
      // Arm exponential decay mask at 85% of hit peak to completely ignore ringing tail
      retrigger_mask = env_fast * 0.85;

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
        note_off ? midisend(block_pos, 128, note_pitch, 0);
        midisend(block_pos, 144, note_pitch, velo);
        note_off = 1;
        note_off_timer = 0;
      );
    );
  );"""

    p_code = p_code.replace(old_detection_section, new_detection_section)

    # 4. Save local files
    with open(pulse_file, "w", encoding="utf-8") as f:
        f.write(p_code)
    with open(r"c:\Dev\DameiSuite\effects\Damei_DrumTrigger.jsfx", "w", encoding="utf-8") as f:
        f.write(p_code)

    # 5. SYNC TO ALL REAPER DIRECTORIES
    pulse_app = os.path.expandvars(r"%APPDATA%\REAPER\Effects\Pulse\Pulse.jsfx")
    damei_pulse = os.path.expandvars(r"%APPDATA%\REAPER\Effects\Damei\Pulse.jsfx")
    damei_trig = os.path.expandvars(r"%APPDATA%\REAPER\Effects\Damei\Damei_DrumTrigger.jsfx")
    
    os.makedirs(os.path.dirname(pulse_app), exist_ok=True)
    os.makedirs(os.path.dirname(damei_pulse), exist_ok=True)
    
    shutil.copy2(pulse_file, pulse_app)
    shutil.copy2(pulse_file, damei_pulse)
    shutil.copy2(pulse_file, damei_trig)
    print("Successfully upgraded Pulse.jsfx and synced to all AppData paths.")

if __name__ == "__main__":
    apply_elevation()
