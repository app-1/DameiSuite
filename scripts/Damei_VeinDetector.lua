-- ==============================================================================
-- DAMEI ACOUSTIC VEIN DETECTOR & PRODUCER CO-PILOT PLAYBOOK (v1.0)
-- Intelligent Session Vibe Analysis & Tasteful Multi-Tier Transition Engine
-- Zero 3rd-Party Dependencies // Pure 64-bit REAPER Native DSP
-- ==============================================================================

local function msg(str)
  reaper.ShowConsoleMsg(tostring(str) .. "\n")
end

-- 1. Vein Archetypes Catalog
local VEIN_ARCHETYPES = {
  [1] = {
    id = "THALL_HEAVY_DJENT",
    name = "Thall & Heavy Modern Djent",
    producers = "Buster Odeholm (thrown) / Lance Prenc (Alpha Wolf)",
    bpm_min = 100, bpm_max = 145,
    p_idx = 4, -- Buster Odeholm in Vocal Sovereign
    tier1_trick = "Dry Syllable Snap & Tight 1/8D Ping-Pong",
    tier2_trick = "Low-Mid Choke & Sub-Drop Handshake",
    tier3_trick = "Silence Guillotine (1/8th note total drop) + Sub Divebomb",
    eq_preset = { hp = 450, lp = 4000, air = 0.0 }
  },
  [2] = {
    id = "MODERN_ALT_METAL",
    name = "Modern Alt-Metal & Post-Hardcore",
    producers = "Dan Braunstein (Spiritbox) / Henrik Udd (Architects)",
    bpm_min = 115, bpm_max = 155,
    p_idx = 15, -- Dan Braunstein in Vocal Sovereign
    tier1_trick = "Atmospheric 1/4-Note Ambient Ping-Pong Throw",
    tier2_trick = "Pre-Chorus Telephone Filter (500Hz-3.5kHz) + Reverse Swell",
    tier3_trick = "Silence Guillotine + 16kHz Maag Air Sheen & Stereo Double Bloom",
    eq_preset = { hp = 500, lp = 3500, air = 2.5 }
  },
  [3] = {
    id = "POP_ROCK_SKATE_PUNK",
    name = "Energetic Pop-Rock & Skate Punk",
    producers = "Zakk Cervini (Blink-182) / Sam Guaiana (Silverstein)",
    bpm_min = 155, bpm_max = 210,
    p_idx = 16, -- Zakk Cervini
    tier1_trick = "1/4-Note Slap Throw with 1.25x Stereo Backing Bloom",
    tier2_trick = "Megaphone Bandpass Snap onto Beat 1",
    tier3_trick = "Stereo Width Explosion (70% mono pre-drop -> 140% chorus bloom)",
    eq_preset = { hp = 600, lp = 4500, air = 3.0 }
  },
  [4] = {
    id = "2010S_METALCORE",
    name = "Classic 2010s Metalcore & Rise Core",
    producers = "Joey Sturgis (Asking Alexandria / TDWP)",
    bpm_min = 130, bpm_max = 175,
    p_idx = 14, -- Joey Sturgis
    tier1_trick = "Heavy 1176 Peak Clamped 1/4T Tape Throw",
    tier2_trick = "1.8kHz Presence Push + Reverse Cymbal Choke",
    tier3_trick = "Snare Acceleration Roll + High-Pass Sweep Drop into Breakdown",
    eq_preset = { hp = 400, lp = 5000, air = 2.0 }
  },
  [5] = {
    id = "ATMOSPHERIC_PROG",
    name = "Atmospheric Prog & Ambient Post-Metal",
    producers = "George Lever (Sleep Token) / Forrester Savell (Karnivool)",
    bpm_min = 65, bpm_max = 110,
    p_idx = 11, -- George Lever
    tier1_trick = "Subtle Intimate Dry Vocal Lead",
    tier2_trick = "3D Reverb Freeze Wash into Intimate Verse Bed",
    tier3_trick = "Massive Cinematic Swell + Center Lead Pocket Explosion",
    eq_preset = { hp = 300, lp = 4500, air = 1.8 }
  }
}

-- 2. Detect Project Vein
local function detect_project_vein()
  local bpm = reaper.Master_GetTempo()
  local tr_cnt = reaper.CountTracks(0)
  
  -- Scan track names for clues
  local has_heavy_guitars = false
  local has_synth = false
  for i = 0, tr_cnt - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, name = reaper.GetTrackName(tr, "")
    local uname = name:upper()
    if uname:find("GUITAR") or uname:find("GTR") or uname:find("RHYTHM") then
      has_heavy_guitars = true
    end
    if uname:find("SYNTH") or uname:find("PAD") or uname:find("KEYS") then
      has_synth = true
    end
  end

  local detected = VEIN_ARCHETYPES[2] -- Default to Modern Alt-Metal (Spiritbox / Braunstein)

  if bpm >= 155 then
    detected = VEIN_ARCHETYPES[3] -- Pop-Rock / Skate Punk (Cervini)
  elseif bpm < 110 and has_synth then
    detected = VEIN_ARCHETYPES[5] -- Atmospheric Prog (Lever / Savell)
  elseif bpm >= 120 and bpm <= 145 and has_heavy_guitars then
    detected = VEIN_ARCHETYPES[2] -- Modern Alt-Metal (Braunstein / Udd)
  elseif bpm >= 130 and bpm <= 150 then
    detected = VEIN_ARCHETYPES[4] -- 2010s Metalcore (Sturgis)
  end

  return detected, bpm
end

-- 3. Scan Project Regions & Map the 3-Tier Escalation
local function map_transition_plan(vein)
  local _, num_markers, num_regions = reaper.CountProjectMarkers(0)
  local total = num_markers + num_regions
  local chorus_transitions = {}

  for i = 0, total - 1 do
    local _, is_reg, pos, r_end, name, markr_idx = reaper.EnumProjectMarkers2(0, i)
    if is_reg then
      local uname = name:upper()
      if uname:find("CHORUS") or uname:find("DROP") or uname:find("BREAKDOWN") then
        table.insert(chorus_transitions, {
          id = markr_idx,
          name = name:gsub("^%s*(.-)%s*$", "%1"),
          pos = pos,
          ['end'] = r_end
        })
      end
    end
  end

  -- Apply the 3-Tier Escalation Rule
  local plan = {}
  for idx, trans in ipairs(chorus_transitions) do
    local tier = (idx == 1) and 1 or ((idx == 2) and 2 or 3)
    local trick_name = (tier == 1) and vein.tier1_trick or ((tier == 2) and vein.tier2_trick or vein.tier3_trick)
    table.insert(plan, {
      tier = tier,
      target = trans.name,
      pos_sec = trans.pos,
      pos_str = string.format("%.2f s", trans.pos),
      trick = trick_name
    })
  end

  return plan
end

-- 4. Apply Playbook to Active REAPER Session
local function apply_playbook_to_session(vein, plan)
  -- 1. Find VOX track
  local tr_cnt = reaper.CountTracks(0)
  local vox_tr = nil
  local vox_idx = -1
  for i = 0, tr_cnt - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, name = reaper.GetTrackName(tr, "")
    local uname = name:upper()
    if uname == "VOX" or uname:find("VOCAL") then
      vox_tr = tr
      vox_idx = i
      break
    end
  end

  if not vox_tr then
    return false, "No VOX track found"
  end

  -- 2. Update Damei Vocal Sovereign to matching producer preset
  local fx_cnt = reaper.TrackFX_GetCount(vox_tr)
  for f = 0, fx_cnt - 1 do
    local _, fn = reaper.TrackFX_GetFXName(vox_tr, f, "")
    if fn:find("Damei Vocal Sovereign", 1, true) then
      reaper.TrackFX_SetParam(vox_tr, f, 17, vein.p_idx) -- slider18 Producer Preset
      reaper.TrackFX_SetParam(vox_tr, f, 29, 1.0)       -- slider30 Pre-Drop Throw Active
      reaper.TrackFX_SetParam(vox_tr, f, 30, 1.0)       -- slider31 Reverse Swell Active
    end
  end

  -- 3. Configure Track 5 (VOX NATIVE FX: Ear-Candy)
  local fx_tr = nil
  for i = 0, tr_cnt - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, name = reaper.GetTrackName(tr, "")
    if name:find("VOX NATIVE FX", 1, true) then
      fx_tr = tr
      break
    end
  end

  if fx_tr then
    local new_name = "VOX NATIVE FX (" .. vein.name .. ")"
    reaper.GetSetMediaTrackInfo_String(fx_tr, "P_NAME", new_name, true)
    
    -- Ensure ReaDelay & ReEQ are configured
    local dly_idx = reaper.TrackFX_AddByName(fx_tr, "ReaDelay (Cockos)", false, 0)
    if dly_idx >= 0 then
      reaper.TrackFX_SetParam(fx_tr, dly_idx, 0, 0.0) -- Dry 0%
      reaper.TrackFX_SetParam(fx_tr, dly_idx, 1, 1.0) -- Wet 100%
    end
    
    -- ReEQ is prioritized
    local reeq_idx = reaper.TrackFX_AddByName(fx_tr, "JS: ReEQ", false, 0)
    if reeq_idx < 0 then
      reeq_idx = reaper.TrackFX_AddByName(fx_tr, "JS: utility/ReJJ-1.0.11/ReEQ.jsfx", false, 0)
    end
  end

  return true, "Playbook applied successfully"
end

-- Main Execution
reaper.Undo_BeginBlock()

local vein, bpm = detect_project_vein()
local plan = map_transition_plan(vein)
local ok, status = apply_playbook_to_session(vein, plan)

reaper.Undo_EndBlock("Damei Vein Detector & Playbook", -1)
reaper.UpdateArrange()

-- Report Output
msg("=================================================================")
msg("⚡ DAMEI ACOUSTIC VEIN DETECTOR & TRANSITION PLAYBOOK ⚡")
msg("=================================================================")
msg("SESSION TEMPO: " .. string.format("%.1f BPM", bpm))
msg("DETECTED VEIN: " .. vein.name:upper())
msg("PRODUCER BLUEPRINT: " .. vein.producers)
msg("-----------------------------------------------------------------")
msg("TASTEFUL 3-TIER ESCALATION PLAN:")
for _, step in ipairs(plan) do
  msg(string.format("  • [TIER %d @ %s] -> %s: %s", step.tier, step.pos_str, step.target, step.trick))
end
msg("-----------------------------------------------------------------")
msg("STATUS: " .. status)
msg("=================================================================")
