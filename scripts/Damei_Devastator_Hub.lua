-- ==============================================================================
-- DAMEI DEVASTATOR AI CREATIVE CO-PILOT & ASSET PLACEMENT ENGINE (v3.5)
-- Multi-Producer Sound Reasoning // 560+ KeepForest Devastator Asset Catalog
-- Key-Matched Braams, Pads, Downers, Suckbacks & Pre-Drop Choke Transitions
-- ==============================================================================

local function msg(str)
  reaper.ShowConsoleMsg(tostring(str) .. "\n")
end

local DEVASTATOR_ROOT = [[E:\Reaper Sound Library\Evolution - Devastator Deathmatch (WAV)\Keepforest - Devastator Deathmatch EXP (WAV)]]

local CATEGORIES = {
  TRAILER_BRASS   = DEVASTATOR_ROOT .. [[\06. Trailer Brass]],
  SUCKBACKS       = DEVASTATOR_ROOT .. [[\15. Reversed & Suckbacks]],
  DOWNERS         = DEVASTATOR_ROOT .. [[\11. Downer]],
  TRAILER_HITS    = DEVASTATOR_ROOT .. [[\03. Trailer Hits]],
  FAR_HITS        = DEVASTATOR_ROOT .. [[\04. Far Hits]],
  GRITTY_HITS     = DEVASTATOR_ROOT .. [[\05. Gritty Hits]],
  DISTORTIONS     = DEVASTATOR_ROOT .. [[\07. Devastator Distortions]],
  BASS_NOISES     = DEVASTATOR_ROOT .. [[\08. Distortions Bass & Noises]],
  SIGNATURES      = DEVASTATOR_ROOT .. [[\09. Signatures One-Shot]],
  SIGNATURES_DEL  = DEVASTATOR_ROOT .. [[\10. Signatures Deleyed]],
  PADS_ATMOS      = DEVASTATOR_ROOT .. [[\12. Pads & Atmos]],
  AMBIENCES       = DEVASTATOR_ROOT .. [[\13. Noises & Ambiences]]
}

local KEY_NAMES = {"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"}

-- Find or Create Track 49 (CINEMATIC FX)
function get_or_create_devastator_track()
  local tr_cnt = reaper.CountTracks(0)
  for i = 0, tr_cnt - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, name = reaper.GetTrackName(tr, "")
    if name:find("CINEMATIC FX", 1, true) or name:find("DEVASTATOR", 1, true) then
      return tr, i
    end
  end

  local insert_idx = 49
  if insert_idx > tr_cnt then insert_idx = tr_cnt end
  reaper.InsertTrackAtIndex(insert_idx, false)
  local tr = reaper.GetTrack(0, insert_idx)
  reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", "CINEMATIC FX (Devastator // KeepForest)", true)

  local col = reaper.ColorToNative(180, 20, 45) | 0x1000000
  reaper.SetMediaTrackInfo_Value(tr, "I_CUSTOMCOLOR", col)
  reaper.SetMediaTrackInfo_Value(tr, "B_MAINSEND", 1.0)
  return tr, insert_idx
end

-- Clear Existing Automated FX Items on Devastator Track
function clear_devastator_items(track)
  local cnt = reaper.CountTrackMediaItems(track)
  for i = cnt - 1, 0, -1 do
    local it = reaper.GetTrackMediaItem(track, i)
    reaper.DeleteTrackMediaItem(track, it)
  end
end

-- Insert Sample with Millisecond Alignment and Vital Envelope Crossfades
function insert_sample_at(track, file_path, target_time, is_suckback, vol_db, custom_fade_in, custom_fade_out)
  if not reaper.file_exists(file_path) then return nil end
  
  local src = reaper.PCM_Source_CreateFromFile(file_path)
  if not src then return nil end
  local len = reaper.GetMediaSourceLength(src)
  reaper.PCM_Source_Destroy(src)

  local pos = target_time
  if is_suckback then
    pos = target_time - len
    if pos < 0 then pos = 0 end
  end

  local item = reaper.AddMediaItemToTrack(track)
  reaper.SetMediaItemInfo_Value(item, "D_POSITION", pos)
  reaper.SetMediaItemInfo_Value(item, "D_LENGTH", len)
  
  local lin_vol = 10.0 ^ ((vol_db or 0.0) / 20.0)
  reaper.SetMediaItemInfo_Value(item, "D_VOL", lin_vol)

  -- Vital-Style Fade-In & Fade-Out Envelopes
  reaper.SetMediaItemInfo_Value(item, "D_FADEINLEN", custom_fade_in or 0.02)
  reaper.SetMediaItemInfo_Value(item, "D_FADEOUTLEN", custom_fade_out or 0.08)

  local take = reaper.AddTakeToMediaItem(item)
  local take_src = reaper.PCM_Source_CreateFromFile(file_path)
  reaper.SetMediaItemTake_Source(take, take_src)
  
  local fn = file_path:match("[^\\]+$") or file_path
  reaper.GetSetMediaItemTakeInfo_String(take, "P_NAME", fn, true)

  return item, len
end

-- Find Key-Matched Asset in Category
local function find_key_matched_file(dir_path, key_idx)
  local root_name = KEY_NAMES[(key_idx or 0) + 1] or "C"
  local files = {}
  local p = 0
  while true do
    local fn = reaper.EnumerateFiles(dir_path, p)
    if not fn then break end
    if fn:lower():sub(-4) == ".wav" then
      table.insert(files, fn)
    end
    p = p + 1
  end

  -- Search for exact key match first
  for _, fn in ipairs(files) do
    if fn:find("-" .. root_name .. "1") or fn:find("-" .. root_name .. "0") or fn:find("-" .. root_name .. " ") or fn:find("-" .. root_name .. "%.") then
      return dir_path .. "\\" .. fn
    end
  end

  -- Fallback to first available wav file
  if #files > 0 then
    return dir_path .. "\\" .. files[1]
  end
  return nil
end

-- Main AI Placement Execution Function
function execute_devastator_ai_placement(dev_tr, bp_idx, root_key)
  local _, num_markers, num_regions = reaper.CountProjectMarkers(0)
  local regions = {}
  for i = 0, num_markers + num_regions - 1 do
    local _, is_reg, pos, r_end, name, markr_idx = reaper.EnumProjectMarkers2(0, i)
    if is_reg then
      table.insert(regions, {
        id = markr_idx,
        name = name:gsub("^%s*(.-)%s*$", "%1"):upper(),
        start = pos,
        ['end'] = r_end
      })
    end
  end

  clear_devastator_items(dev_tr)

  local decisions = {}
  local placed_count = 0

  -- Producer Profile Defaults
  -- 0=Jordan Fish, 1=Mick Gordon, 2=Chris Bedan, 3=Dan Braunstein, 4=Buster Odeholm, 5=Bad Omens, 6=Lance Prenc, 7=George Lever
  local trim_db = -13.0
  if bp_idx == 0 then trim_db = -6.0
  elseif bp_idx == 1 then trim_db = -5.5
  elseif bp_idx == 2 then trim_db = -6.5
  elseif bp_idx == 3 then trim_db = -13.0 -- Dan Braunstein subtle standard
  elseif bp_idx == 4 then trim_db = -5.8
  elseif bp_idx == 5 then trim_db = -6.8
  elseif bp_idx == 6 then trim_db = -6.0
  elseif bp_idx == 7 then trim_db = -7.5
  end

  -- Read custom Vital-style envelopes from Devastator Suite if available
  local slot1_atk = 0.02
  local slot1_rel = 3.2
  local slot2_atk = 0.8
  local slot2_choke = 0.08
  local slot3_atk = 0.005
  local slot3_dec = 1.6
  local slot4_atk = 1.2
  local slot4_dec = 2.5

  local fx_cnt = reaper.TrackFX_GetCount(dev_tr)
  for f = 0, fx_cnt - 1 do
    local _, fn = reaper.TrackFX_GetFXName(dev_tr, f, "")
    if fn:find("Damei Devastator Suite", 1, true) then
      slot1_atk = (reaper.TrackFX_GetParam(dev_tr, f, 15) or 30) / 1000.0
      slot1_rel = (reaper.TrackFX_GetParam(dev_tr, f, 16) or 3200) / 1000.0
      slot2_atk = (reaper.TrackFX_GetParam(dev_tr, f, 23) or 850) / 1000.0
      slot2_choke = (reaper.TrackFX_GetParam(dev_tr, f, 24) or 80) / 1000.0
      slot3_atk = (reaper.TrackFX_GetParam(dev_tr, f, 31) or 8) / 1000.0
      slot3_dec = (reaper.TrackFX_GetParam(dev_tr, f, 32) or 1800) / 1000.0
      slot4_atk = (reaper.TrackFX_GetParam(dev_tr, f, 37) or 1200) / 1000.0
      slot4_dec = (reaper.TrackFX_GetParam(dev_tr, f, 38) or 2500) / 1000.0
      break
    end
  end

  -- Region-by-Region Transition Reasoning
  for i = 1, #regions do
    local curr = regions[i]
    local next_r = regions[i+1]

    -- 1. Intro Downbeat Atmosphere (if start of song has an Intro)
    if i == 1 and curr.name:find("INTRO") then
      if bp_idx == 3 or bp_idx == 7 then -- Dan Braunstein / George Lever: Ethereal Pad Bed
        local pad = find_key_matched_file(CATEGORIES.PADS_ATMOS, root_key)
        if pad then
          insert_sample_at(dev_tr, pad, curr.start, false, trim_db - 3.0, slot4_atk, slot4_dec)
          placed_count = placed_count + 1
          table.insert(decisions, {pos = curr.start, section = "INTRO", action = "Atmospheric Pad Bed", reason = "Ethereal spatial foundation"})
        end
      end
    end

    if next_r then
      local t_pos = next_r.start
      local trans_type = curr.name .. " -> " .. next_r.name

      -- 2. Pre-Chorus -> Chorus Transitions
      if curr.name:find("PRE") and next_r.name:find("CHORUS") then
        if i <= 3 then -- Pre-Chorus 1 -> Chorus 1 (Smooth, Controlled Tension)
          local sb_file = CATEGORIES.SUCKBACKS .. [[\KFDT - Reversed & Suckback - 01.wav]]
          insert_sample_at(dev_tr, sb_file, t_pos, true, trim_db + 1.5, slot2_atk, slot2_choke)
          placed_count = placed_count + 1
          table.insert(decisions, {pos = t_pos, section = trans_type, action = "KFDT Suckback 01 (Smooth)", reason = "Subtle pre-drop tension into Chorus 1"})

        else -- Pre-Chorus 2 -> Chorus 2 (Elevated Escalation)
          if bp_idx == 3 or bp_idx == 5 then -- Dan Braunstein / Bad Omens: Smooth Suckback + Sub Downer
            local sb_file = CATEGORIES.SUCKBACKS .. [[\KFDT - Reversed & Suckback - 03.wav]]
            insert_sample_at(dev_tr, sb_file, t_pos, true, trim_db + 2.0, slot2_atk, slot2_choke)
            local downer = CATEGORIES.DOWNERS .. [[\KFDT -  Downer 02.wav]]
            insert_sample_at(dev_tr, downer, t_pos, false, trim_db, slot3_atk, slot3_dec)
            placed_count = placed_count + 2
            table.insert(decisions, {pos = t_pos, section = trans_type, action = "Suckback 03 + Sub Downer 02", reason = "Elevated impact with smooth downbeat anchor"})
          else -- Jordan Fish / Mick Gordon / Buster: Hard Trailer Hit & Cyber Suckback
            local sb_file = CATEGORIES.SUCKBACKS .. [[\KFDT - Reversed & Suckback - 03.wav]]
            insert_sample_at(dev_tr, sb_file, t_pos, true, trim_db + 3.0, slot2_atk, slot2_choke)
            local hit = CATEGORIES.TRAILER_HITS .. [[\KFDT - Trailer Hit - 01.wav]]
            insert_sample_at(dev_tr, hit, t_pos, false, trim_db + 1.0, 0.005, 0.20)
            placed_count = placed_count + 2
            table.insert(decisions, {pos = t_pos, section = trans_type, action = "Suckback 03 + Trailer Hit 01", reason = "Heavy cyber downbeat detonation"})
          end
        end

      -- 3. Bridge -> Final Chorus / Breakdown (THE CLIMAX DROP)
      elseif curr.name:find("BRIDGE") and next_r.name:find("CHORUS") then
        local braam = find_key_matched_file(CATEGORIES.TRAILER_BRASS, root_key) or (CATEGORIES.TRAILER_BRASS .. [[\KFDT - Trailer Brass - 01 - C1.wav]])
        insert_sample_at(dev_tr, braam, t_pos, false, trim_db + 2.0, slot1_atk, slot1_rel)
        local downer = CATEGORIES.DOWNERS .. [[\KFDT -  Downer 01.wav]]
        insert_sample_at(dev_tr, downer, t_pos, false, trim_db, slot3_atk, slot3_dec)
        placed_count = placed_count + 2
        table.insert(decisions, {pos = t_pos, section = trans_type, action = "Key-Matched Trailer Brass + Downer 01", reason = "Song climax; maximum cinematic impact"})

      -- 4. Chorus -> Verse / Bridge (Drop in Energy -> RESPECT INTENTIONAL SILENCE)
      elseif curr.name:find("CHORUS") and (next_r.name:find("VERSE") or next_r.name:find("BRIDGE")) then
        table.insert(decisions, {pos = t_pos, section = trans_type, action = "INTENTIONAL SILENCE / BREATH", reason = "Allows mix to breathe, preventing fatigue"})

      -- 5. Verse -> Pre-Chorus (Groove Continuation)
      elseif curr.name:find("VERSE") and next_r.name:find("PRE") then
        table.insert(decisions, {pos = t_pos, section = trans_type, action = "BAND GROOVE PRESERVED", reason = "Rhythm section drives momentum"})
      end
    end
  end

  -- Calibrate Devastator Suite on Track 49 with Producer Settings
  local fx_cnt = reaper.TrackFX_GetCount(dev_tr)
  for f = 0, fx_cnt - 1 do
    local _, fn = reaper.TrackFX_GetFXName(dev_tr, f, "")
    if fn:find("Damei Devastator Suite", 1, true) then
      reaper.TrackFX_SetParam(dev_tr, f, 1, bp_idx or 3)
      reaper.TrackFX_SetParam(dev_tr, f, 4, trim_db)
      reaper.TrackFX_SetParam(dev_tr, f, 5, 1.0) -- Drum Bus Duck
      reaper.TrackFX_SetParam(dev_tr, f, 6, 1.0) -- Vocal Pocket Carve
      reaper.TrackFX_SetParam(dev_tr, f, 7, 1.0) -- Guitar Handshake
    end
  end

  reaper.UpdateArrange()
  return decisions, placed_count
end

-- If executed directly as ReaScript
if reaper.GetProjectName(0, "") ~= "" then
  reaper.Undo_BeginBlock()
  local dev_tr, _ = get_or_create_devastator_track()
  
  -- Read blueprint from Track 49 Devastator Suite if present
  local bp = 3
  local rk = 0
  local fx_cnt = reaper.TrackFX_GetCount(dev_tr)
  for f = 0, fx_cnt - 1 do
    local _, fn = reaper.TrackFX_GetFXName(dev_tr, f, "")
    if fn:find("Damei Devastator Suite", 1, true) then
      bp = math.floor(reaper.TrackFX_GetParam(dev_tr, f, 1) + 0.5)
      rk = math.floor(reaper.TrackFX_GetParam(dev_tr, f, 2) + 0.5)
    end
  end

  local decisions, cnt = execute_devastator_ai_placement(dev_tr, bp, rk)
  reaper.Undo_EndBlock("Damei Devastator AI Auto-Placement", -1)
  
  msg("=================================================================")
  msg("⚡ DAMEI DEVASTATOR AI AUTO-PLACEMENT COMPLETE ⚡")
  msg(string.format("PRODUCER BLUEPRINT: #%d (%s) | ROOT KEY: %s", bp, ({"Jordan Fish", "Mick Gordon", "Chris Bedan", "Dan Braunstein", "Buster Odeholm", "Bad Omens", "Lance Prenc", "George Lever"})[bp+1] or "Unknown", KEY_NAMES[rk+1] or "C"))
  msg(string.format("ASSETS PLACED: %d KeepForest Samples with Millisecond Timing", cnt))
  msg("=================================================================")
  for _, d in ipairs(decisions) do
    msg(string.format("• [@ %.2fs] %s: %s (%s)", d.pos, d.section, d.action, d.reason))
  end
  msg("=================================================================")
end
