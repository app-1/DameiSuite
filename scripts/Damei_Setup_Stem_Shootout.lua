-- ============================================================================
-- Damei Setup Stem Shootout Routing
-- File: Damei_Setup_Stem_Shootout.lua
-- Architecture: Cockos REAPER ReaScript (Lua)
-- Description: Automatically provisions dual-folder stem hierarchy (Vocals,
--              Drums, Bass, Other) for both Reference and User Mix, sets up
--              4-channel sidechain routing to Master Track Pins 3/4, and
--              configures Damei Sankofa Oracle for live comparative shootout.
-- ============================================================================

local function msg(str)
  reaper.ShowConsoleMsg("[Damei Stem Shootout] " .. tostring(str) .. "\n")
end

reaper.Undo_BeginBlock()

-- Colors (Native REAPER RGB format: 0x1000000 + R + G*256 + B*65536)
local function rgb_color(r, g, b)
  return reaper.ColorToNative(r, g, b) | 0x1000000
end

local COL_REF = rgb_color(0, 160, 224)   -- Cyan / Blue
local COL_MIX = rgb_color(0, 224, 128)   -- Emerald / Green

-- Helper: Find track by exact name
local function find_track(name)
  for i = 0, reaper.CountTracks(0) - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, tr_name = reaper.GetTrackName(tr)
    if tr_name == name then
      return tr, i
    end
  end
  return nil, -1
end

-- 1. Ensure Master Track has at least 4 channels for sidechain
local master_tr = reaper.GetMasterTrack(0)
local cur_master_ch = reaper.GetMediaTrackInfo_Value(master_tr, "I_NCHAN")
if cur_master_ch < 4 then
  reaper.SetMediaTrackInfo_Value(master_tr, "I_NCHAN", 4)
  msg("Master track channels upgraded to 4 for sidechain.")
end

-- 2. Ensure Damei_AssessmentMatrix (Sankofa Oracle) is on Master Track
local oracle_idx = -1
for fx = 0, reaper.TrackFX_GetCount(master_tr) - 1 do
  local _, fx_name = reaper.TrackFX_GetFXName(master_tr, fx, "")
  if fx_name:find("AssessmentMatrix") or fx_name:find("Sankofa Oracle") then
    oracle_idx = fx
    break
  end
end

if oracle_idx == -1 then
  oracle_idx = reaper.TrackFX_AddByName(master_tr, "Damei_AssessmentMatrix.jsfx", false, -1)
  if oracle_idx >= 0 then
    msg("Inserted Damei Sankofa Oracle on Master Track.")
  end
end

if oracle_idx >= 0 then
  -- slider3 = Compare Against: set to 3 ("Live Sidechain (Pins 3/4)")
  reaper.TrackFX_SetParam(master_tr, oracle_idx, 2, 3)
  -- slider12 = Monitor Mode: set to 0 ("Monitor Mix")
  reaper.TrackFX_SetParam(master_tr, oracle_idx, 11, 0)
  msg("Sankofa Oracle set to Live Sidechain mode (Pins 3/4).")
end

-- 3. Provision [REFERENCE MIX] Folder Structure
local ref_folder, ref_idx = find_track("[REFERENCE MIX]")
if not ref_folder then
  local ins_pos = reaper.CountTracks(0)
  reaper.InsertTrackAtIndex(ins_pos, true)
  ref_folder = reaper.GetTrack(0, ins_pos)
  reaper.GetSetMediaTrackInfo_String(ref_folder, "P_NAME", "[REFERENCE MIX]", true)
  reaper.SetMediaTrackInfo_Value(ref_folder, "I_FOLDERDEPTH", 1) -- Start folder
  reaper.SetMediaTrackInfo_Value(ref_folder, "I_CUSTOMCOLOR", COL_REF)
  reaper.SetMediaTrackInfo_Value(ref_folder, "B_MAINSEND", 0)     -- Do NOT send directly to Master 1/2
  reaper.SetMediaTrackInfo_Value(ref_folder, "B_MUTE", 1)         -- Mute by default

  local ref_stems = { "Ref_Vocals", "Ref_Drums", "Ref_Bass", "Ref_Other" }
  for s = 1, #ref_stems do
    local s_pos = ins_pos + s
    reaper.InsertTrackAtIndex(s_pos, true)
    local sub_tr = reaper.GetTrack(0, s_pos)
    reaper.GetSetMediaTrackInfo_String(sub_tr, "P_NAME", ref_stems[s], true)
    reaper.SetMediaTrackInfo_Value(sub_tr, "I_CUSTOMCOLOR", COL_REF)
    if s == #ref_stems then
      reaper.SetMediaTrackInfo_Value(sub_tr, "I_FOLDERDEPTH", -1) -- Close folder
    else
      reaper.SetMediaTrackInfo_Value(sub_tr, "I_FOLDERDEPTH", 0)
    end
  end
  msg("Created [REFERENCE MIX] folder and 4 stem child tracks.")
end

-- 4. Create Sidechain Send: [REFERENCE MIX] -> Master Ch 3/4
local send_found = false
local num_sends = reaper.GetTrackNumSends(ref_folder, 0)
for s = 0, num_sends - 1 do
  local dest_tr = reaper.BR_GetMediaTrackSendInfo_Track(ref_folder, 0, s, 1)
  if dest_tr == master_tr then
    send_found = true
    break
  end
end

if not send_found then
  local send_idx = reaper.CreateTrackSend(ref_folder, master_tr)
  -- Audio 1/2 -> 3/4 (I_SRCCHAN = 0 (1/2), I_DSTCHAN = 2 (3/4))
  reaper.SetTrackSendInfo_Value(ref_folder, 0, send_idx, "I_SRCCHAN", 0)
  reaper.SetTrackSendInfo_Value(ref_folder, 0, send_idx, "I_DSTCHAN", 2)
  reaper.SetTrackSendInfo_Value(ref_folder, 0, send_idx, "D_VOL", 1.0) -- Unity (0.0 dB)
  msg("Sidechain send created: [REFERENCE MIX] 1/2 -> Master 3/4.")
end

-- 5. Provision [MY MIX] Folder Structure
local mix_folder, mix_idx = find_track("[MY MIX]")
if not mix_folder then
  local ins_pos = reaper.CountTracks(0)
  reaper.InsertTrackAtIndex(ins_pos, true)
  mix_folder = reaper.GetTrack(0, ins_pos)
  reaper.GetSetMediaTrackInfo_String(mix_folder, "P_NAME", "[MY MIX]", true)
  reaper.SetMediaTrackInfo_Value(mix_folder, "I_FOLDERDEPTH", 1) -- Start folder
  reaper.SetMediaTrackInfo_Value(mix_folder, "I_CUSTOMCOLOR", COL_MIX)
  reaper.SetMediaTrackInfo_Value(mix_folder, "B_MAINSEND", 1)     -- Send to Master 1/2
  reaper.SetMediaTrackInfo_Value(mix_folder, "B_MUTE", 0)         -- Active by default

  local mix_stems = { "My_Vocals", "My_Drums", "My_Bass", "My_Other" }
  for s = 1, #mix_stems do
    local s_pos = ins_pos + s
    reaper.InsertTrackAtIndex(s_pos, true)
    local sub_tr = reaper.GetTrack(0, s_pos)
    reaper.GetSetMediaTrackInfo_String(sub_tr, "P_NAME", mix_stems[s], true)
    reaper.SetMediaTrackInfo_Value(sub_tr, "I_CUSTOMCOLOR", COL_MIX)
    if s == #mix_stems then
      reaper.SetMediaTrackInfo_Value(sub_tr, "I_FOLDERDEPTH", -1) -- Close folder
    else
      reaper.SetMediaTrackInfo_Value(sub_tr, "I_FOLDERDEPTH", 0)
    end
  end
  msg("Created [MY MIX] folder and 4 stem child tracks.")
end

reaper.TrackList_AdjustWindows(false)
reaper.UpdateArrange()
reaper.Undo_EndBlock("Damei: Setup Stem Shootout Routing", -1)

reaper.MB(
  "Stem Shootout Environment Ready!\n\n" ..
  "1. [MY MIX] (Vocals, Drums, Bass, Other) -> Active to Master 1/2.\n" ..
  "2. [REFERENCE MIX] (Vocals, Drums, Bass, Other) -> Routed to Sidechain 3/4.\n" ..
  "3. Sankofa Oracle on Master Track configured to 'Live Sidechain (Pins 3/4)'.\n\n" ..
  "Drag your stem WAV files onto the matching tracks and press Play!",
  "Damei Stem Shootout Setup",
  0
)
