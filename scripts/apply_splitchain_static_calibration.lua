-- ==============================================================================
-- DAMEI STATIC CALIBRATION AUTOMATOR (REASCRIPT LUA)
-- Automatically applies exact static calibration parameters derived from
-- Split Chain ("I'm Not Dying To Be Here") comparative assessment directly
-- into the active REAPER session across all 8 Damei Suites:
--   1. Mixing Suite      5. Vocal Sovereign
--   2. Drum Bus          6. Synth Bus Nebula
--   3. Guitar Bus        7. Devastator Suite
--   4. Bass Bus          8. Ozone Mastering Suite + Sankofa Oracle
-- ==============================================================================

local log_path = "c:\\Dev\\DameiSuite\\tools\\calibration_run_log.txt"
local log_file = io.open(log_path, "w")

local function msg(str)
  reaper.ShowConsoleMsg(str .. "\n")
  if log_file then
    log_file:write(str .. "\n")
    log_file:flush()
  end
end

reaper.ClearConsole()
msg("================================================================================")
msg("⚡ DAMEI SUITE: APPLYING SPLIT CHAIN STATIC CALIBRATION")
msg("   Target Reference: Split Chain - 'I'm Not Dying To Be Here'")
msg("   Calibration Mode: Static Precision Lock (Zero Dynamic Gain Hunting)")
msg("================================================================================")

reaper.Undo_BeginBlock()

local stats = {
  tracks_scanned = 0,
  suites_updated = 0,
  params_modified = 0
}

-- Safe parameter setter by name search with slider index fallback
local function set_suite_param(track, fx_idx, slider_num, search_term, val, label)
  local num_params = reaper.TrackFX_GetNumParams(track, fx_idx)
  local target_p = slider_num - 1 -- standard JSFX 0-indexed parameter

  -- Try to verify or find matching parameter by name
  local found = false
  if search_term and search_term ~= "" then
    local lower_term = string.lower(search_term)
    for p = 0, num_params - 1 do
      local _, pname = reaper.TrackFX_GetParamName(track, fx_idx, p, "")
      if string.find(string.lower(pname), lower_term, 1, true) then
        target_p = p
        found = true
        break
      end
    end
  end

  if target_p >= 0 and target_p < num_params then
    reaper.TrackFX_SetParam(track, fx_idx, target_p, val)
    stats.params_modified = stats.params_modified + 1
    if label then
      msg(string.format("   ├─ %s: %.2f", label, val))
    end
    return true
  end
  return false
end

-- Process an individual FX on a track
local function process_fx(track, track_name, fx_idx)
  local _, fx_name = reaper.TrackFX_GetFXName(track, fx_idx, "")
  local lower_name = string.lower(fx_name)
  local is_master = (track == reaper.GetMasterTrack(0))
  local loc_tag = is_master and "[MASTER TRACK]" or string.format("[Track: %s]", track_name)

  -- 1. DAMEI MIXING SUITE
  if string.find(lower_name, "mixingsuite", 1, true) or string.find(lower_name, "mixing suite", 1, true) then
    msg(string.format("✔ FOUND MIXING SUITE on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    set_suite_param(track, fx_idx, 39, "Producer Signature", 6, "Producer Preset (Kel Pinchin / Split Chain)")
    set_suite_param(track, fx_idx, 6, "Sub-Bass Mono-Anchor", 100, "Sub-Bass Mono Cutoff (100 Hz)")
    set_suite_param(track, fx_idx, 7, "Stereo Dimension", 1.18, "Stereo Width Expander (1.18x)")
    set_suite_param(track, fx_idx, 16, "Spectral Tilt", 0.8, "Spectral Tilt Sheen (+0.8 dB)")
    set_suite_param(track, fx_idx, 3, "Headroom Target", -6.0, "Pre-Master Headroom Target (-6.0 dBTP)")
    set_suite_param(track, fx_idx, 40, "Mix Bus Headroom", 1, "Mix Bus Clipper (Lance Prenc Soft Clip)")
    set_suite_param(track, fx_idx, 8, "Compressor Topology", 0, "Comp Topology (British VCA)")
    set_suite_param(track, fx_idx, 10, "Comp Ratio", 1, "Comp Ratio (2:1)")
    set_suite_param(track, fx_idx, 11, "Comp Attack", 30, "Comp Attack (30 ms)")
    set_suite_param(track, fx_idx, 12, "Comp Release", 0, "Comp Release (Auto)")
  end

  -- 2. DAMEI DRUM BUS ARCHITECT
  if string.find(lower_name, "drumsuite", 1, true) or string.find(lower_name, "drum bus", 1, true) then
    msg(string.format("✔ FOUND DRUM BUS ARCHITECT on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    set_suite_param(track, fx_idx, 25, "Producer Drum", 5, "Producer Preset (Kel Pinchin)")
    set_suite_param(track, fx_idx, 30, "Cymbal Silk", 1, "Cymbal Silk Master (Active)")
    set_suite_param(track, fx_idx, 40, "Dynamic Boom", -1.5, "Sub-Kick Boom Tamer 40Hz (-1.5 dB)")
    set_suite_param(track, fx_idx, 42, "Matrix Trim", 1, "Matrix Auto-Correct Lane (Active)")
    set_suite_param(track, fx_idx, 12, "Cymbal De-Trash", -1.8, "Cymbal De-Trash Resonance (-1.8 dB)")
    set_suite_param(track, fx_idx, 13, "Cymbal Silk Air", 1.2, "Cymbal Silk Air Sheen (+1.2 dB)")
  end

  -- 3. DAMEI GUITAR BUS ALCHEMIST
  if string.find(lower_name, "guitarsuite", 1, true) or string.find(lower_name, "guitar bus", 1, true) then
    msg(string.format("✔ FOUND GUITAR BUS ALCHEMIST on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    set_suite_param(track, fx_idx, 23, "Producer Guitar", 5, "Producer Preset (Kel Pinchin)")
    set_suite_param(track, fx_idx, 16, "Quad-Wall", 1.28, "Stereo Quad-Wall Width (1.28x)")
    set_suite_param(track, fx_idx, 9, "Highpass Anchor", 90, "Sub-Guitar Highpass Anchor (90 Hz)")
    set_suite_param(track, fx_idx, 10, "Low-Mid Mud", -1.0, "Mud Box Scoop 380Hz (-1.0 dB)")
    set_suite_param(track, fx_idx, 28, "De-Fizz Master", 1, "De-Fizz Master Engine (Active)")
    set_suite_param(track, fx_idx, 11, "Harsh Fizz Notch 1", -1.5, "De-Fizz Notch 3.2kHz (-1.5 dB)")
    set_suite_param(track, fx_idx, 12, "Harsh Fizz Notch 2", -1.8, "De-Fizz Notch 4.2kHz (-1.8 dB)")
  end

  -- 4. DAMEI BASS BUS ENGINE
  if string.find(lower_name, "basssuite", 1, true) or string.find(lower_name, "bass bus", 1, true) then
    msg(string.format("✔ FOUND BASS BUS ENGINE on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    set_suite_param(track, fx_idx, 20, "Producer Bass", 5, "Producer Preset (Kel Pinchin)")
    set_suite_param(track, fx_idx, 3, "Sub-Mono Elliptical", 90, "Sub-Mono Elliptical Anchor (90 Hz)")
    set_suite_param(track, fx_idx, 4, "Kick Ducking Depth", 2.4, "Kick Ducking Depth (2.4 dB)")
    set_suite_param(track, fx_idx, 12, "Mud Box Scoop", -1.5, "Mud Box Scoop 250Hz (-1.5 dB)")
    set_suite_param(track, fx_idx, 35, "Matrix Trim", 1, "Matrix Auto-Correct Lane (Active)")
  end

  -- 5. DAMEI VOCAL SOVEREIGN
  if string.find(lower_name, "vocalsuite", 1, true) or string.find(lower_name, "vocal sovereign", 1, true) then
    msg(string.format("✔ FOUND VOCAL SOVEREIGN on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    set_suite_param(track, fx_idx, 18, "Producer Vocal", 5, "Producer Preset (Kel Pinchin)")
    set_suite_param(track, fx_idx, 29, "Master Vocal Engine", 1, "Master Vocal Engine (Active)")
    set_suite_param(track, fx_idx, 9, "Center Lead Channel", 1, "Center Lead Lock 100% Mono <200Hz")
    set_suite_param(track, fx_idx, 48, "Chest Mud", -2.0, "ReEQ 380Hz Chest Mud Scoop (-2.0 dB)")
    set_suite_param(track, fx_idx, 10, "Air Band", 1.8, "Maag 16kHz Air Band (+1.8 dB)")
    set_suite_param(track, fx_idx, 35, "Matrix Trim", 1, "Matrix Auto-Correct Lane (Active)")
  end

  -- 6. DAMEI SYNTH BUS NEBULA
  if string.find(lower_name, "synthsuite", 1, true) or string.find(lower_name, "synth bus", 1, true) then
    msg(string.format("✔ FOUND SYNTH BUS NEBULA on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    set_suite_param(track, fx_idx, 15, "Producer Synth", 10, "Producer Blueprint (Kel Pinchin)")
    set_suite_param(track, fx_idx, 8, "Stereo Horizon", 1.45, "Stereo Horizon Width (1.45x)")
    set_suite_param(track, fx_idx, 4, "Sub Foundation", 1, "Sub Mono Lock <90Hz (Active)")
    set_suite_param(track, fx_idx, 34, "Band 2", -1.5, "Multiband Low-Mid Scoop (-1.5 dB)")
    set_suite_param(track, fx_idx, 36, "Band 4", 2.5, "Multiband Glassy Air Sheen (+2.5 dB)")
    set_suite_param(track, fx_idx, 27, "Matrix Trim", 1, "Matrix Auto-Correct Lane (Active)")
  end

  -- 7. DAMEI DEVASTATOR SUITE
  if string.find(lower_name, "devastatorsuite", 1, true) or string.find(lower_name, "devastator", 1, true) then
    msg(string.format("✔ FOUND DEVASTATOR SUITE on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    set_suite_param(track, fx_idx, 2, "Producer Cinematic", 8, "Producer Blueprint (Kel Pinchin)")
    set_suite_param(track, fx_idx, 5, "Master Sub-Bed", -13.0, "Sub-Bed Trim (-13.0 dB)")
    set_suite_param(track, fx_idx, 46, "Sub Mono Anchor", 1, "Sub Mono Anchor <90Hz (Active)")
    set_suite_param(track, fx_idx, 47, "Spatial Widener", 1.25, "M/S Spatial Widener (1.25x)")
  end

  -- 8. DAMEI OZONE 12 MASTERING SUITE
  if string.find(lower_name, "ozonesuite", 1, true) or string.find(lower_name, "mastering suite", 1, true) then
    msg(string.format("✔ FOUND OZONE MASTERING SUITE on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    set_suite_param(track, fx_idx, 33, "Mastering Engineer", 6, "Mastering Preset (R. Schmidt & G. Berry - Split Chain)")
    set_suite_param(track, fx_idx, 1, "Platform Target", 0, "Platform Target (CD -8.5 LUFS / Reference Mode)")
    set_suite_param(track, fx_idx, 5, "Limiter Ceiling", -1.0, "Limiter Ceiling (-1.0 dBTP)")
    set_suite_param(track, fx_idx, 6, "Mono-Maker", 105, "Mono-Maker Cutoff (105 Hz)")
    set_suite_param(track, fx_idx, 7, "Stereo Width", 1.15, "Stereo Width Multiplier (1.15x)")
    set_suite_param(track, fx_idx, 21, "Clipper Algorithm", 0, "KClip Mode (Smooth Zero)")
    set_suite_param(track, fx_idx, 23, "KClip Mid/Side Focus", 75, "KClip Mid Bias (75% - protects guitars)")
  end

  -- 9. DAMEI ASSESSMENT MATRIX (SANKOFA ORACLE)
  if string.find(lower_name, "assessmentmatrix", 1, true) or string.find(lower_name, "sankofa oracle", 1, true) then
    msg(string.format("✔ FOUND SANKOFA ORACLE on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    set_suite_param(track, fx_idx, 3, "Library Ref Target", 2, "Library Preset (Split Chain)")
    set_suite_param(track, fx_idx, 9, "Reference Preset", 6, "Reference Benchmark (Split Chain)")
    set_suite_param(track, fx_idx, 7, "Static Calibration Lock", 1, "Static Calibration Lock (Engaged)")
    set_suite_param(track, fx_idx, 12, "Monitor Mode", 0, "Shootout Monitor Mode (MIX)")
  end
end

-- Scan Master Track
local master_tr = reaper.GetMasterTrack(0)
stats.tracks_scanned = stats.tracks_scanned + 1
for fx = 0, reaper.TrackFX_GetCount(master_tr) - 1 do
  process_fx(master_tr, "MASTER", fx)
end

-- Scan All Regular Tracks
local num_tracks = reaper.CountTracks(0)
for t = 0, num_tracks - 1 do
  local tr = reaper.GetTrack(0, t)
  stats.tracks_scanned = stats.tracks_scanned + 1
  local _, tr_name = reaper.GetTrackName(tr, "")
  for fx = 0, reaper.TrackFX_GetCount(tr) - 1 do
    process_fx(tr, tr_name, fx)
  end
end

-- Update Telemetry Memory Bus
reaper.gmem_attach("DameiMixMetering")
reaper.gmem_write(1159, 1) -- Static Calibration Locked Flag
reaper.gmem_write(1158, 0) -- Shootout Mode: Mix

reaper.Undo_EndBlock("Apply Split Chain Static Calibration", -1)

msg("--------------------------------------------------------------------------------")
msg(string.format("⚡ CALIBRATION APPLIED: %d Suites Updated | %d Parameters Modified", stats.suites_updated, stats.params_modified))
msg("   Telemetries locked in gmem:DameiMixMetering (gmem[1159] = 1).")
msg("   Audition Mode: Use spacebar to play. Toggle A/B on Mixing Suite or Sankofa Oracle.")
msg("================================================================================")
if log_file then log_file:close() end
