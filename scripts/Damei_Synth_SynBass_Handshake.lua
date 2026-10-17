-- ==============================================================================
-- DAMEI SYNTH & SYNBASS HANDSHAKE ENGINE (v1.0)
-- Deploys and Configures Damei Synth Suite on Track 44 (Synth) & Track 41 (SWDrums)
-- Coordinates Inter-Suite Telemetry (Vocal Unmasking, Kick Ducking, Reverb Bloom)
-- ==============================================================================

local function msg(str)
  reaper.ShowConsoleMsg(tostring(str) .. "\n")
end

local function find_track_by_name(target_name)
  local tr_cnt = reaper.CountTracks(0)
  for i = 0, tr_cnt - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, name = reaper.GetTrackName(tr, "")
    if name:upper():find(target_name:upper(), 1, true) then
      return tr, name, i
    end
  end
  return nil, nil, nil
end

local function add_or_configure_synth_suite(tr, track_name, mode_val)
  if not tr then return false, -1 end
  
  local fx_count = reaper.TrackFX_GetCount(tr)
  local ss_idx = -1
  for f = 0, fx_count - 1 do
    local _, fn = reaper.TrackFX_GetFXName(tr, f, "")
    if fn:find("Synth Suite", 1, true) or fn:find("Nebula Architect", 1, true) then
      ss_idx = f
      break
    end
  end

  if ss_idx < 0 then
    -- Add Damei Synth Suite JSFX
    ss_idx = reaper.TrackFX_AddByName(tr, "JS: Damei Synth Suite (Nebula Architect & SynBass Alchemist)", false, 1)
    if ss_idx < 0 then
      ss_idx = reaper.TrackFX_AddByName(tr, "JS: Damei/Damei_SynthSuite.jsfx", false, 1)
    end
    if ss_idx < 0 then
      ss_idx = reaper.TrackFX_AddByName(tr, "Damei_SynthSuite.jsfx", false, 1)
    end
  end

  if ss_idx >= 0 then
    -- slider1: Active Module (0: Nebula Scope & Telemetry)
    reaper.TrackFX_SetParam(tr, ss_idx, 0, 0.0)
    -- slider2: Producer Blueprint (0: Jordan Fish BMTH)
    reaper.TrackFX_SetParam(tr, ss_idx, 1, 0.0)
    -- slider3: Processing Mode (0: Parent Synth Bus, 1: Dedicated SynBass)
    reaper.TrackFX_SetParam(tr, ss_idx, 2, mode_val or 0.0)
    -- slider4: Sub Foundation Mono Anchor (1: Strict Mono <90Hz)
    reaper.TrackFX_SetParam(tr, ss_idx, 3, 1.0)
    -- slider5: Drum Kick Sub-Duck Depth (3.5 dB)
    reaper.TrackFX_SetParam(tr, ss_idx, 4, 3.5)
    -- slider6: Lead Vocal Mid-Carve Depth (2.5 dB)
    reaper.TrackFX_SetParam(tr, ss_idx, 5, 2.5)
    -- slider7: Guitar Wall Chorus Carve (3.0 dB)
    reaper.TrackFX_SetParam(tr, ss_idx, 6, 3.0)
    -- slider8: Stereo Horizon Width (1.45x)
    reaper.TrackFX_SetParam(tr, ss_idx, 7, 1.45)
    -- slider9: Ambient Reverb Bloom Ducking (40%)
    reaper.TrackFX_SetParam(tr, ss_idx, 8, 40.0)
    -- slider10: 12kHz Glassy Air Sheen (+2.8 dB)
    reaper.TrackFX_SetParam(tr, ss_idx, 9, 2.8)
    -- slider11: Britson Console Saturation (28%)
    reaper.TrackFX_SetParam(tr, ss_idx, 10, 28.0)
    -- slider13: Headroom Ceiling (-0.1 dBTP)
    reaper.TrackFX_SetParam(tr, ss_idx, 12, -0.1)

    return true, ss_idx
  end

  return false, -1
end

-- Main Execution
reaper.Undo_BeginBlock()

-- 1. Find tracks
local synth_tr, synth_name, synth_idx = find_track_by_name("Synth")
local swdrums_tr, swdrums_name, swdrums_idx = find_track_by_name("SWDrums")
local synbass_tr, synbass_name, synbass_idx = find_track_by_name("SynBass")

-- Fallback to index 44 and 41 if name query ambiguous
if not synth_tr and reaper.CountTracks(0) > 44 then
  synth_tr = reaper.GetTrack(0, 44)
  synth_idx = 44
  _, synth_name = reaper.GetTrackName(synth_tr)
end

if not swdrums_tr and reaper.CountTracks(0) > 41 then
  swdrums_tr = reaper.GetTrack(0, 41)
  swdrums_idx = 41
  _, swdrums_name = reaper.GetTrackName(swdrums_tr)
end

-- 2. Configure Synth Suite on Track 44 (Synth Bus)
local synth_ok, s_idx = add_or_configure_synth_suite(synth_tr, synth_name, 0.0)

-- 3. Configure Synth Suite on Track 41 (SWDrums / Sub-Bus) as requested
local drums_ok, d_idx = add_or_configure_synth_suite(swdrums_tr, swdrums_name, 2.0)

-- 4. Configure SynBass if found
if synbass_tr then
  add_or_configure_synth_suite(synbass_tr, synbass_name, 1.0)
end

reaper.Undo_EndBlock("Deploy Damei Synth Suite & SynBass Handshake", -1)
reaper.UpdateArrange()

msg("=== DAMEI SYNTH SUITE & SYNBASS HANDSHAKE READY ===")
if synth_ok then
  msg("Track " .. tostring(synth_idx + 1) .. " [" .. tostring(synth_name) .. "]: Damei Synth Suite Active (Jordan Fish Preset, Sub Mono <90Hz, 145% Horizon)")
end
if drums_ok then
  msg("Track " .. tostring(swdrums_idx + 1) .. " [" .. tostring(swdrums_name) .. "]: Damei Synth Suite Active (Hybrid Mode, Kick Interlock)")
end
if synbass_tr then
  msg("Track " .. tostring(synbass_idx + 1) .. " [" .. tostring(synbass_name) .. "]: SynBass Sub Engine Handshake Engaged")
end
msg("Inter-Suite gmem Telemetry [920..939] Live.")
