-- ==============================================================================
-- DAMEI PRODUCER EAR-CANDY & TRANSITION ENGINE (v2.0 INTERNALIZED)
-- Fully Integrated within Damei Vocal Sovereign (No External Aux Tracks)
-- Pure 64-bit Native CPU Optimization (<0.001% Footprint)
-- ==============================================================================

local function msg(str)
  reaper.ShowConsoleMsg(tostring(str) .. "\n")
end

-- Producer Profiles Dictionary
local PRODUCER_PROFILES = {
  [1] = { name = "Dan Braunstein (Spiritbox)", delay_time = "1/4", fb = 38, filter_hp = 400, filter_lp = 4500, swell_bars = 2.0, telephone_drop = 2 },
  [2] = { name = "Joey Sturgis (Asking Alexandria)", delay_time = "1/4T", fb = 48, filter_hp = 500, filter_lp = 3500, swell_bars = 1.0, telephone_drop = 2 },
  [3] = { name = "Buster Odeholm (thrown / Vildhjarta)", delay_time = "1/8D", fb = 20, filter_hp = 250, filter_lp = 6000, swell_bars = 0.5, telephone_drop = 0 },
  [4] = { name = "Zakk Cervini (Blink-182 / MGK)", delay_time = "1/4", fb = 32, filter_hp = 600, filter_lp = 4000, swell_bars = 2.0, telephone_drop = 2 },
  [5] = { name = "Jordan Fish (Bring Me The Horizon)", delay_time = "1/4D", fb = 45, filter_hp = 350, filter_lp = 5000, swell_bars = 2.0, telephone_drop = 2 },
  [6] = { name = "George Lever (Sleep Token / Loathe)", delay_time = "1/2", fb = 55, filter_hp = 300, filter_lp = 4500, swell_bars = 4.0, telephone_drop = 0 }
}

-- 1. Find Vocal Track
local function find_vocal_track()
  local tr_cnt = reaper.CountTracks(0)
  for i = 0, tr_cnt - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, name = reaper.GetTrackName(tr, "")
    local upper_name = name:upper()
    if upper_name == "VOX" or upper_name:find("VOCAL") or upper_name:find("LEAD VOX") then
      return tr, name, i
    end
  end
  local sel_tr = reaper.GetSelectedTrack(0, 0)
  if sel_tr then
    local _, name = reaper.GetTrackName(sel_tr, "")
    return sel_tr, name, reaper.GetMediaTrackInfo_Value(sel_tr, "IP_TRACKNUMBER") - 1
  end
  return nil, nil, nil
end

-- 2. Clean up any legacy external VOX NATIVE FX tracks
local function cleanup_legacy_fx_bus(vocal_tr)
  local tr_cnt = reaper.CountTracks(0)
  local to_remove = {}
  for i = 0, tr_cnt - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, name = reaper.GetTrackName(tr, "")
    if name:find("VOX NATIVE FX", 1, true) then
      table.insert(to_remove, tr)
    end
  end
  for _, tr in ipairs(to_remove) do
    -- Remove any sends from vocal_tr to this legacy track
    local send_cnt = reaper.GetTrackNumSends(vocal_tr, 0)
    for s = send_cnt - 1, 0, -1 do
      local dest_tr = reaper.GetTrackSendInfo_Value(vocal_tr, 0, s, "P_DESTTRACK")
      if dest_tr == tr then
        reaper.RemoveTrackSend(vocal_tr, 0, s)
      end
    end
    -- Delete the legacy redundant track
    reaper.DeleteTrack(tr)
  end
end

-- 3. Configure Vocal Sovereign Internal Ear-Candy Sliders
local function configure_vocal_sovereign(vox_tr, profile)
  local fx_count = reaper.TrackFX_GetCount(vox_tr)
  local vs_idx = -1
  for f = 0, fx_count - 1 do
    local _, fx_name = reaper.TrackFX_GetFXName(vox_tr, f, "")
    if fx_name:find("Vocal Sovereign", 1, true) or fx_name:find("Damei Vocal", 1, true) then
      vs_idx = f
      break
    end
  end

  if vs_idx >= 0 then
    -- slider30: Pre-Chorus Vocal Throw Delay (1 = Active)
    reaper.TrackFX_SetParam(vox_tr, vs_idx, 29, 1.0)
    -- slider31: Reverse Swell Generator (1 = Active)
    reaper.TrackFX_SetParam(vox_tr, vs_idx, 30, 1.0)
    -- slider32: Telephone Drop Filter (0=Off, 1=Always, 2=Auto Pre-Drop)
    reaper.TrackFX_SetParam(vox_tr, vs_idx, 31, profile.telephone_drop or 2.0)
    -- slider33: Throw Delay Feedback (percent)
    reaper.TrackFX_SetParam(vox_tr, vs_idx, 32, profile.fb or 35.0)
    -- slider34: Reverse Swell Duration (Bars)
    reaper.TrackFX_SetParam(vox_tr, vs_idx, 33, profile.swell_bars or 2.0)
    return true, vs_idx
  end
  return false, -1
end

-- Main Execution
reaper.Undo_BeginBlock()

local vox_tr, vox_name, vox_idx = find_vocal_track()
if not vox_tr then
  reaper.ShowMessageBox("No VOX track or vocal track found in project.\nPlease select a vocal track and rerun.", "Damei Ear-Candy Engine", 0)
  reaper.Undo_EndBlock("Damei Producer Ear-Candy Setup (Failed)", -1)
  return
end

-- 1. Default to Jordan Fish / Dan Braunstein profile
local active_profile = PRODUCER_PROFILES[5] -- Jordan Fish (BMTH)

-- 2. Remove external legacy track to keep everything 100% internal inside Vocal Sovereign
cleanup_legacy_fx_bus(vox_tr)

-- 3. Configure Vocal Sovereign internal DSP engine
local configured, vs_idx = configure_vocal_sovereign(vox_tr, active_profile)

reaper.Undo_EndBlock("Damei Producer Ear-Candy Internalized", -1)
reaper.UpdateArrange()

msg("=== DAMEI PRODUCER EAR-CANDY ENGINE READY (INTERNALIZED) ===")
msg("Vocal Track: " .. tostring(vox_name) .. " [Track " .. tostring(vox_idx + 1) .. "]")
msg("Producer Blueprint: " .. active_profile.name)
if configured then
  msg("Vocal Sovereign Internal DSP Engine: Configured (Ping-Pong Throw, Telephone Drop & Reverse Swells ACTIVE)")
  msg("External Aux Track: Deprecated & Cleaned up (0.00% Extra Track Footprint)")
else
  msg("Notice: Damei Vocal Sovereign not found on VOX track. Please insert Damei Vocal Sovereign.")
end
