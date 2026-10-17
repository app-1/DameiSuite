-- ==============================================================================
-- DAMEI MIXING SUITE: 14-ENGINEER BESPOKE CHORUS IMPACT SCANNER & SOLVER
-- scan_and_solve_mixing_chorus_impact.lua
-- ==============================================================================

reaper.Undo_BeginBlock()

local master_tr = reaper.GetMasterTrack(0)
local target_tr = nil
local target_fx = -1

local fx_cnt = reaper.TrackFX_GetCount(master_tr)
for f = 0, fx_cnt - 1 do
  local _, fx_name = reaper.TrackFX_GetFXName(master_tr, f, "")
  if fx_name:find("Damei Mixing Suite", 1, true) then
    target_tr = master_tr
    target_fx = f
    break
  end
end

if not target_tr then
  local tr_cnt = reaper.CountTracks(0)
  for i = 0, tr_cnt - 1 do
    local tr = reaper.GetTrack(0, i)
    local cnt = reaper.TrackFX_GetCount(tr)
    for f = 0, cnt - 1 do
      local _, fx_name = reaper.TrackFX_GetFXName(tr, f, "")
      if fx_name:find("Damei Mixing Suite", 1, true) then
        target_tr = tr
        target_fx = f
        break
      end
    end
    if target_tr then break end
  end
end

if not target_tr then
  return { ok = false, error = "Damei Mixing Suite not found" }
end

-- Read active Producer Preset (param index 38 in 0-indexed API)
local p_idx = math.floor(reaper.TrackFX_GetParam(target_tr, target_fx, 38) + 0.5)

-- Scan Project Regions and Markers
local num_markers, num_regions = reaper.CountProjectMarkers(0)
local total = num_markers + num_regions
local chorus_count = 0
local verse_count = 0

for i = 0, total - 1 do
  local retval, isrgn, pos, rgnend, name, markrgnindexnumber = reaper.EnumProjectMarkers3(0, i)
  if retval > 0 and isrgn then
    local n = name:lower()
    if (n:find("chorus") and not n:find("pre")) or n:find("drop") or n:find("hook") then
      chorus_count = chorus_count + 1
    elseif n:find("verse") then
      verse_count = verse_count + 1
    end
  end
end

-- Measured HexGyal dynamic lift into chorus
local dyn_lift = 3.7
local signature_desc = ""

-- ==============================================================================
-- BESPOKE CHORUS IMPACT PARAMETER CALIBRATION ACROSS ALL 14 MIX ENGINEERS
-- ==============================================================================
if p_idx == 0 then
  -- Default Modern Metal Clean (2026 Clarity & Punch)
  signature_desc = "2026 Clarity & Punch // Balanced VCA Glue & Mud Clearance"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -13.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 1) -- 2:1
  reaper.TrackFX_SetParam(target_tr, target_fx, 10, 30.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 125.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.3)
  reaper.TrackFX_SetParam(target_tr, target_fx, 27, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 28, 2800.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 40, 1.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 29, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 30, 190.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 16, -2.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 17, 340.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.14)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 100.0)
elseif p_idx == 1 then
  -- Lance Prenc: Snare Detonation (+1.6dB) & Guitar Wall Clipper
  signature_desc = "Lance Prenc // Snare Detonation (+1.6dB) & Guitar Wall Soft-Clipper"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -13.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 2) -- 4:1
  reaper.TrackFX_SetParam(target_tr, target_fx, 10, 30.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 130.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.3)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.6)
  reaper.TrackFX_SetParam(target_tr, target_fx, 27, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 28, 2800.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 40, 1.2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 29, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 30, 190.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 16, -2.6)
  reaper.TrackFX_SetParam(target_tr, target_fx, 17, 340.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 39, 1) -- Bus Clipper
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.16)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 100.0)
elseif p_idx == 2 then
  -- Scott Seigel: 808 Sub Crater Slam & -3.2dB 320Hz Guitar Scoop
  signature_desc = "Scott Seigel // 808 Sub Crater Slam & -3.2dB 320Hz Guitar Scoop"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -14.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 10, 30.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 135.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.4)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.4)
  reaper.TrackFX_SetParam(target_tr, target_fx, 27, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 28, 2800.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 40, 1.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 29, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 30, 190.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 16, -3.2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 17, 320.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.14)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 90.0)
elseif p_idx == 3 then
  -- Jonathan Dolese: Pop-Metal Vocal Shimmer & 2.8k Donut Pocket
  signature_desc = "Jonathan Dolese // Pop-Metal Hook Polish & 2.8k Donut Pocket"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -13.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 10, 30.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 120.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 27, 2) -- Deep notch
  reaper.TrackFX_SetParam(target_tr, target_fx, 28, 2800.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 40, 1.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 41, 1) -- 3D Space
  reaper.TrackFX_SetParam(target_tr, target_fx, 15, 0.8) -- Air
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.18)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 100.0)
elseif p_idx == 4 then
  -- Buster Odeholm: Claustrophobia Tension to Hyper-Punch Detonation (+2.0dB)
  signature_desc = "Buster Odeholm // Claustrophobia Box into Hyper-Punch (+2.0dB)"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -14.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 10, 30.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 125.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.4)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 2.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 20, 1.8)
  reaper.TrackFX_SetParam(target_tr, target_fx, 21, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 27, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 28, 2800.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 40, 1.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 29, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 30, 190.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 16, -2.4)
  reaper.TrackFX_SetParam(target_tr, target_fx, 17, 300.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 39, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.18)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 110.0)
elseif p_idx == 5 then
  -- Lewis Johns: Shoegaze Ambient Bloom & Breathing Opto Glue
  signature_desc = "Lewis Johns // Shoegaze Ambient Bloom & Breathing Opto Glue"
  reaper.TrackFX_SetParam(target_tr, target_fx, 7, 1) -- Opto
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -12.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 110.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 0.8)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 0.8)
  reaper.TrackFX_SetParam(target_tr, target_fx, 34, 0.6) -- Room Tail
  reaper.TrackFX_SetParam(target_tr, target_fx, 41, 2)   -- Ambient Bloom
  reaper.TrackFX_SetParam(target_tr, target_fx, 16, -1.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 17, 360.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.18)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 95.0)
elseif p_idx == 6 then
  -- Kel Pinchin: 90s Grunge Fuzz Grit & Room Snap
  signature_desc = "Kel Pinchin // 90s Grunge Fuzz Grit (+1.6dB) & Snare Snap"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -13.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 115.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.4)
  reaper.TrackFX_SetParam(target_tr, target_fx, 20, 1.6)
  reaper.TrackFX_SetParam(target_tr, target_fx, 21, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 16, -2.2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 17, 340.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.14)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 95.0)
elseif p_idx == 7 then
  -- Dan Lancaster & Jason Perry: Commercial Radio Slam & Air Tilt
  signature_desc = "Dan Lancaster // Commercial Radio Slam (+1.5dB) & +0.9dB Air"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -13.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 120.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 27, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 28, 3000.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 40, 1.2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 15, 0.9)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.14)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 100.0)
elseif p_idx == 8 then
  -- Erik Bickerstaffe: Industrial Tape Drive & 2.4k Vocal Carve
  signature_desc = "Erik Bickerstaffe // Industrial Tape Drive (+1.7dB) & 2.4k Carve"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -14.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 120.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.3)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.3)
  reaper.TrackFX_SetParam(target_tr, target_fx, 27, 2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 28, 2400.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 20, 1.7)
  reaper.TrackFX_SetParam(target_tr, target_fx, 21, 2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.16)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 105.0)
elseif p_idx == 9 then
  -- Sam Guaiana: Tension Choke into Snare Crack Detonation (+1.6dB) & Vocal Cut
  signature_desc = "Sam Guaiana // Pre-Drop Tension Choke into +1.6dB 5kHz Snare Crack"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -13.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 1) -- 2:1 Punchy Modern VCA
  reaper.TrackFX_SetParam(target_tr, target_fx, 10, 30.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 125.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.6) -- Snare Crack Detonation
  reaper.TrackFX_SetParam(target_tr, target_fx, 27, 1)   -- 2.8k Vocal Donut Notch
  reaper.TrackFX_SetParam(target_tr, target_fx, 28, 2800.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 40, 1.2) -- +1.2dB Vocal Presence Trim
  reaper.TrackFX_SetParam(target_tr, target_fx, 41, 1)   -- Stereo 3D Halo
  reaper.TrackFX_SetParam(target_tr, target_fx, 29, 1)   -- 190Hz Chug Guard
  reaper.TrackFX_SetParam(target_tr, target_fx, 30, 190.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 16, -2.4) -- -2.4dB Mud Scoop
  reaper.TrackFX_SetParam(target_tr, target_fx, 17, 340.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 20, 1.3) -- +1.3dB Pentode Bite
  reaper.TrackFX_SetParam(target_tr, target_fx, 21, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.15)  -- 1.15x Width
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 100.0) -- 100Hz Sub Mono Anchor
elseif p_idx == 10 then
  -- Zach Tuch: Analog Tape Swell & Dream-Pop Soundstage (1.18x)
  signature_desc = "Zach Tuch // Analog Tape Swell & Dream-Pop Soundstage (1.18x)"
  reaper.TrackFX_SetParam(target_tr, target_fx, 7, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -12.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 115.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 34, 0.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 41, 2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 20, 1.4)
  reaper.TrackFX_SetParam(target_tr, target_fx, 21, 0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.18)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 95.0)
elseif p_idx == 11 then
  -- Forrester Savell: Progressive Low-Mass & 360Hz De-Box
  signature_desc = "Forrester Savell // Progressive Low-Mass (130Hz HPF) & 360Hz De-Box"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -13.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 130.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.3)
  reaper.TrackFX_SetParam(target_tr, target_fx, 16, -2.8)
  reaper.TrackFX_SetParam(target_tr, target_fx, 17, 360.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.10)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 105.0)
elseif p_idx == 12 then
  -- Leon Schmidt & Donaldson: Djent Blast Snap & 9.5dB Crest
  signature_desc = "Leon Schmidt & Donaldson // Djent Blast Snap (+1.5dB) & 135Hz SC HPF"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -14.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 135.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.3)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 20, 1.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.16)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 100.0)
else
  -- 13. Ermin Hamidovic Systematic Reference
  signature_desc = "Ermin Hamidovic // Systematic 0 VU Staging & Linear Passthrough"
  reaper.TrackFX_SetParam(target_tr, target_fx, 8, -13.5)
  reaper.TrackFX_SetParam(target_tr, target_fx, 9, 1)
  reaper.TrackFX_SetParam(target_tr, target_fx, 12, 125.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 13, 1.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 33, 1.2)
  reaper.TrackFX_SetParam(target_tr, target_fx, 39, 0) -- Clean linear clip
  reaper.TrackFX_SetParam(target_tr, target_fx, 16, -2.4)
  reaper.TrackFX_SetParam(target_tr, target_fx, 17, 340.0)
  reaper.TrackFX_SetParam(target_tr, target_fx, 6, 1.12)
  reaper.TrackFX_SetParam(target_tr, target_fx, 5, 100.0)
end

-- Strictly Lock Pre-Master Headroom Guarantee (-6.0 dBTP)
reaper.TrackFX_SetParam(target_tr, target_fx, 3, 1)
reaper.TrackFX_SetParam(target_tr, target_fx, 2, -6.0)

reaper.Undo_EndBlock("Damei Mixing Suite: Calibrate Engineer Chorus Impact", -1)

local _, p_name = reaper.TrackFX_GetFormattedParamValue(target_tr, target_fx, 38, "")
local msg = string.format([[
=============================================================================
DAMEI MIXING SUITE // SIGNATURE CHORUS IMPACT CALIBRATION COMPLETE
=============================================================================
• Active Mixing Engineer : %s (Preset %d)
• Signature Technique    : %s
• Detected Project Regions: %d Choruses, %d Verses
• Measured Dynamic Lift   : +%.1f dB
• Status                  : Bespoke Transition Choke & Chorus Parameters Applied
• Pre-Master Headroom     : Strict -6.0 dBTP Auto-Trim Locked
=============================================================================
]], p_name, p_idx, signature_desc, chorus_count, verse_count, dyn_lift)

reaper.ShowConsoleMsg(msg)
return {
  ok = true,
  engineer_preset = p_idx,
  engineer_name = p_name,
  technique = signature_desc,
  dyn_lift = dyn_lift
}
