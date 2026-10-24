-- ============================================================================
-- Damei Mix Assistant -- 1-Key A/B & Stem Shootout Cycle Action
-- File: damei_stem_cycle_action.lua
-- Architecture: Cockos REAPER ReaScript (Lua)
-- Description: Instant hotkey-driven comparative auditioning tool.
--              - Full Mix Mode: Toggles Sankofa Oracle between Mix and
--                Loudness-Matched Reference (zero latency, zero mute clicks).
--              - Stem Focus Mode: If an isolated stem is selected (e.g. Drums),
--                instantly flips solo between My Stem and Reference Stem.
-- ============================================================================

local function show_hud(text)
  reaper.theme_tellcache = text
  local x, y = reaper.GetMousePosition()
  reaper.TrackCtl_SetToolTip(tostring(text), x + 15, y + 15, true)
end

reaper.Undo_BeginBlock()

local master_tr = reaper.GetMasterTrack(0)
local oracle_idx = -1

for fx = 0, reaper.TrackFX_GetCount(master_tr) - 1 do
  local _, fx_name = reaper.TrackFX_GetFXName(master_tr, fx, "")
  if fx_name:find("AssessmentMatrix") or fx_name:find("Sankofa Oracle") then
    oracle_idx = fx
    break
  end
end

-- Helper: Map of stem counterparts
local STEM_PAIRS = {
  ["MY_VOCALS"]  = "REF_VOCALS",
  ["REF_VOCALS"] = "MY_VOCALS",
  ["MY_DRUMS"]   = "REF_DRUMS",
  ["REF_DRUMS"]  = "MY_DRUMS",
  ["MY_BASS"]    = "REF_BASS",
  ["REF_BASS"]   = "MY_BASS",
  ["MY_OTHER"]   = "REF_OTHER",
  ["REF_OTHER"]  = "MY_OTHER"
}

-- Check if user has an isolated stem selected
local sel_track = reaper.GetSelectedTrack(0, 0)
local stem_toggled = false

if sel_track and reaper.CountSelectedTracks(0) == 1 then
  local _, tr_name = reaper.GetTrackName(sel_track)
  local norm_name = string.upper(tr_name:gsub("%s+", "_"))
  local target_counterpart = STEM_PAIRS[norm_name]
  
  if target_counterpart then
    -- Find the partner track
    for t = 0, reaper.CountTracks(0) - 1 do
      local other_tr = reaper.GetTrack(0, t)
      local _, other_name = reaper.GetTrackName(other_tr)
      local other_norm = string.upper(other_name:gsub("%s+", "_"))
      
      if other_norm == target_counterpart then
        -- Flip selection and exclusive solo
        reaper.SetTrackSelected(sel_track, false)
        reaper.SetTrackSelected(other_tr, true)
        
        -- Exclusive solo on counterpart
        reaper.Main_OnCommand(40340, 0) -- Track: Solo exclusive for selected tracks
        show_hud("🎯 [STEM SHOOTOUT] Auditioning: " .. other_name)
        stem_toggled = true
        break
      end
    end
  end
end

-- If not toggling a specific stem pair, toggle Full Mix A/B in Sankofa Oracle
if not stem_toggled then
  if oracle_idx >= 0 then
    -- Param 11 is slider12 (Monitor Output Mode)
    -- 0 = Monitor Mix (Pins 1/2)
    -- 1 = Monitor Ref Matched (Pins 3/4 + Auto LUFS offset)
    local cur_mode = math.floor(reaper.TrackFX_GetParam(master_tr, oracle_idx, 11) + 0.5)
    
    if cur_mode == 0 then
      reaper.TrackFX_SetParam(master_tr, oracle_idx, 11, 1) -- Switch to Ref Matched
      show_hud("🔊 [SHOOTOUT] REFERENCE (LUFS-MATCHED)")
    else
      reaper.TrackFX_SetParam(master_tr, oracle_idx, 11, 0) -- Switch to My Mix
      show_hud("🟢 [SHOOTOUT] MY MIX (1/2)")
    end
  else
    -- Fallback: Toggle Mute between [MY MIX] and [REFERENCE MIX] parent tracks
    local my_mix_tr, _ = nil, nil
    local ref_mix_tr, _ = nil, nil
    for t = 0, reaper.CountTracks(0) - 1 do
      local tr = reaper.GetTrack(0, t)
      local _, nm = reaper.GetTrackName(tr)
      if nm == "[MY MIX]" then my_mix_tr = tr end
      if nm == "[REFERENCE MIX]" then ref_mix_tr = tr end
    end
    
    if my_mix_tr and ref_mix_tr then
      local my_mute = reaper.GetMediaTrackInfo_Value(my_mix_tr, "B_MUTE")
      if my_mute == 0 then
        reaper.SetMediaTrackInfo_Value(my_mix_tr, "B_MUTE", 1)
        reaper.SetMediaTrackInfo_Value(ref_mix_tr, "B_MUTE", 0)
        reaper.SetMediaTrackInfo_Value(ref_mix_tr, "B_MAINSEND", 1)
        show_hud("🔊 [SHOOTOUT] REFERENCE MIX")
      else
        reaper.SetMediaTrackInfo_Value(my_mix_tr, "B_MUTE", 0)
        reaper.SetMediaTrackInfo_Value(ref_mix_tr, "B_MUTE", 1)
        show_hud("🟢 [SHOOTOUT] MY MIX")
      end
    else
      show_hud("⚠ [SHOOTOUT] Insert Sankofa Oracle on Master Track for Instant A/B.")
    end
  end
end

reaper.TrackList_AdjustWindows(false)
reaper.UpdateArrange()
reaper.Undo_EndBlock("Damei: Toggle Stem Shootout A/B", -1)
