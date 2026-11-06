import os
import re

# Read current Pulse.jsfx
source_path = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Pulse\Pulse.jsfx"
with open(source_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update mask_decay in @slider: change 0.120 to 0.200
code = code.replace(
    "mask_decay = exp(-1.0 / (srate * 0.120)); // 120ms Slate Trigger 2 exponential retrigger mask",
    "mask_decay = exp(-1.0 / (srate * 0.200)); // 200ms Slate Trigger 2 exponential retrigger mask"
)

# 2. Update cur_preset 24 (Manuel Renner) in @slider to use calibrated values
old_preset24 = """      cur_preset == 24 ? (
        slider2 = 30; slider3 = 55; slider4 = 35;
        slider5 = 60; slider6 = 9000; slider56 = 1;
      );"""

new_preset24 = """      cur_preset == 24 ? (
        slider61 == 36 ? (
          slider2 = 22; slider3 = 55; slider4 = 55;
          slider5 = 45; slider6 = 280; slider56 = 1;
        ) : (
          slider2 = 20; slider3 = 55; slider4 = 55;
          slider5 = 140; slider6 = 4500; slider56 = 2;
        );
      );"""
code = code.replace(old_preset24, new_preset24)

# 3. Update Augmentation Mode formula in @sample:
old_mix_block = """    dry_l = spl0 * dry_gain;
    dry_r = spl1 * dry_gain;
    spl0 = dry_l * (1.0 - mix) + total_sample_l * mix;
    spl1 = dry_r * (1.0 - mix) + total_sample_r * mix;"""

new_mix_block = """    dry_l = spl0 * dry_gain;
    dry_r = spl1 * dry_gain;
    (aug_mode == 1 || aug_mode == 2) ? (
      // PARALLEL AUGMENTATION MODE: Dry mic punch 100% preserved + reinforced sample at -15dB!
      spl0 = dry_l + total_sample_l;
      spl1 = dry_r + total_sample_r;
    ) : (
      spl0 = dry_l * (1.0 - mix) + total_sample_l * mix;
      spl1 = dry_r * (1.0 - mix) + total_sample_r * mix;
    );"""
code = code.replace(old_mix_block, new_mix_block)

# 4. Update the Trigger Condition in @sample:
old_trig_cond = """  // Trigger Condition:
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
      retrigger_mask = env_fast * 0.85;"""

new_trig_cond = """  // SLATE DIGITAL TRIGGER 2 DUAL-ENVELOPE ONSET & ADAPTIVE RETRIGGER MASK
  // Solves the double-triggering / flam bug by ignoring ringing tails and machine-gun re-triggers!
  onset_punch = env_fast - env_slow;

  // Trigger Condition:
  // 1. Minimum physical lockout (slider4 ms) has expired
  // 2. Fast envelope punches above absolute threshold
  // 3. Fast envelope punches above decaying mask from previous hit
  // 4. Signal has a fresh percussive onset punch (onset_punch > threshold * 0.12 or explosive rising slope)
  lockout_timer == 0 && env_fast > threshold && env_fast > retrigger_mask && (onset_punch > (threshold * 0.12) || trans_slope > (threshold * 0.12)) ? (
    is_bleed = bleed_enable && (bleed_env > bleed_thresh) && ((bleed_env * bleed_sens) > env_fast);
    is_bleed ? (
      bleed_gated_cnt = floor(srate * 0.05);
    ) : (
      // ZERO-LATENCY SAMPLE-ACCURATE INSTANT TRIGGER
      lockout_timer = retrig_samples;
      // Arm exponential decay mask at 95% of hit peak to completely ignore ringing tail
      retrigger_mask = max(retrigger_mask, env_fast * 0.95);"""

code = code.replace(old_trig_cond, new_trig_cond)

# 5. Lead silence auto-zeroing in load_slot:
old_load_slot_assign = """              slot_idx == 0 ? (
                sample_nch0 = nch; sample_sr0 = sr; sample_len0 = floor(len / nch);
                sample_path_loaded0 = path_str; sample_load_req0 = 0;
                sample_play_pos0 = 0; sample_playing0 = 0;
              ) : slot_idx == 1 ? (
                sample_nch1 = nch; sample_sr1 = sr; sample_len1 = floor(len / nch);
                sample_path_loaded1 = path_str; sample_load_req1 = 0;
                sample_play_pos1 = 0; sample_playing1 = 0;
              ) : (
                sample_nch2 = nch; sample_sr2 = sr; sample_len2 = floor(len / nch);
                sample_path_loaded2 = path_str; sample_load_req2 = 0;
                sample_play_pos2 = 0; sample_playing2 = 0;
              );
              file_mem(handle, buf_off, len);"""

new_load_slot_assign = """              file_mem(handle, buf_off, len);
              // Auto-zero lead silence to eliminate acoustic flams between dry mic & sample
              lead_off = 0;
              while (lead_off < min(len, 4800) && abs(buf_off[lead_off]) < 0.001) (
                lead_off += nch;
              );
              lead_samp = floor(lead_off / nch);

              slot_idx == 0 ? (
                sample_nch0 = nch; sample_sr0 = sr; sample_len0 = floor(len / nch);
                sample_start0 = lead_samp;
                sample_path_loaded0 = path_str; sample_load_req0 = 0;
                sample_play_pos0 = lead_samp; sample_playing0 = 0;
              ) : slot_idx == 1 ? (
                sample_nch1 = nch; sample_sr1 = sr; sample_len1 = floor(len / nch);
                sample_start1 = lead_samp;
                sample_path_loaded1 = path_str; sample_load_req1 = 0;
                sample_play_pos1 = lead_samp; sample_playing1 = 0;
              ) : (
                sample_nch2 = nch; sample_sr2 = sr; sample_len2 = floor(len / nch);
                sample_start2 = lead_samp;
                sample_path_loaded2 = path_str; sample_load_req2 = 0;
                sample_play_pos2 = lead_samp; sample_playing2 = 0;
              );"""

code = code.replace(old_load_slot_assign, new_load_slot_assign)

# Arm sample at sample_start0 instead of 0
code = code.replace(
    "sample_playing0 = 1; sample_play_pos0 = 0; attack_phase0 = 0; env_gain0 = 0;",
    "sample_playing0 = 1; sample_play_pos0 = sample_start0; attack_phase0 = 0; env_gain0 = 0;"
)
code = code.replace(
    "sample_playing1 = 1; sample_play_pos1 = 0; attack_phase1 = 0; env_gain1 = 0;",
    "sample_playing1 = 1; sample_play_pos1 = sample_start1; attack_phase1 = 0; env_gain1 = 0;"
)
code = code.replace(
    "sample_playing2 = 1; sample_play_pos2 = 0; attack_phase2 = 0; env_gain2 = 0;",
    "sample_playing2 = 1; sample_play_pos2 = sample_start2; attack_phase2 = 0; env_gain2 = 0;"
)

# 6. Default slider values in header definition:
code = code.replace("slider2:32<0,100,1>-Detail / Threshold (-dB)", "slider2:22<0,100,1>-Detail / Threshold (-dB)")
code = code.replace("slider4:35<5,250,1>-Retrigger Lockout (ms)", "slider4:55<5,250,1>-Retrigger Lockout (ms)")

# Write to all 5 target locations
targets = [
    r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Pulse\Pulse.jsfx",
    r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Pulse.jsfx",
    r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_DrumTrigger.jsfx",
    r"c:\Dev\DameiSuite\effects\Pulse.jsfx",
    r"c:\Dev\DameiSuite\effects\Damei_DrumTrigger.jsfx",
]

for t in targets:
    os.makedirs(os.path.dirname(t), exist_ok=True)
    with open(t, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Updated {t}")

print("\nAll 5 DrumTrigger JSFX files successfully updated with Dual-Envelope engine!")
