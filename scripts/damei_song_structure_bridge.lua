-- ==============================================================================
-- DAMEI SONG STRUCTURE & CHORUS IMPACT AI BRIDGE (REASCRIPT LUA)
-- damei_song_structure_bridge.lua
--
-- Features:
--   • Reads all REAPER project markers and regions (Chorus, Pre-Chorus, Verse, Drop, Bridge, etc.)
--   • Continuously calculates time-to-next-chorus, active region index, region progress, and section ID
--   • Broadcasts via gmem to BOTH DameiMetering (Mastering) & DameiMixMetering (Mixing)
--   • Seamless real-time tracking during playback and timeline positioning
--   • Zero overhead defer loop, runs transparently in background
-- ==============================================================================

local function get_song_structure()
  local play_state = reaper.GetPlayState()
  -- If playback is active (play or record), use exact audio play position; else track edit cursor
  local is_playing = (play_state & 1 == 1 or play_state & 4 == 4) and 1 or 0
  local play_pos = (is_playing == 1) and reaper.GetPlayPosition() or reaper.GetCursorPosition()
  local num_markers, num_regions = reaper.CountProjectMarkers(0)
  local total = num_markers + num_regions
  
  local cur_sec_id = 0 -- 0=Default/Idle, 1=Pre-Chorus, 2=Pre-Drop Breath, 3=Chorus/Drop, 4=Breakdown/Bridge, 5=Verse/Groove
  local next_chorus_start = -1
  local has_regions = (num_regions > 0)
  
  local cur_rgn_idx = 0
  local cur_rgn_progress = 0.0
  local cur_rgn_type = 0 -- 1=Intro, 2=Verse, 3=Pre-Chorus, 4=Chorus, 5=Bridge/Breakdown, 6=Outro, 7=Other
  local cur_rgn_time_left = 0.0

  -- 1. Pass 1: Find next upcoming chorus & its start time
  for i = 0, total - 1 do
    local retval, isrgn, pos, rgnend, name, markrgnindexnumber = reaper.EnumProjectMarkers3(0, i)
    if retval > 0 then
      local n = name:lower()
      if (n:find("chorus") and not n:find("pre")) or n:find("drop") or n:find("hook") or n:find("refrain") then
        if pos > play_pos and (next_chorus_start == -1 or pos < next_chorus_start) then
          next_chorus_start = pos
        end
      end
    end
  end
  
  local dist_to_chorus = (next_chorus_start > play_pos) and (next_chorus_start - play_pos) or -1.0
  
  -- 2. Pass 2: Match active region and markers
  for i = 0, total - 1 do
    local retval, isrgn, pos, rgnend, name, markrgnindexnumber = reaper.EnumProjectMarkers3(0, i)
    if retval > 0 then
      local n = name:lower()
      if isrgn then
        if play_pos >= pos and play_pos < rgnend then
          cur_rgn_idx = markrgnindexnumber
          cur_rgn_progress = math.max(0.0, math.min(1.0, (play_pos - pos) / math.max(0.001, rgnend - pos)))
          cur_rgn_time_left = math.max(0.0, rgnend - play_pos)

          if (n:find("chorus") and not n:find("pre")) or n:find("drop") or n:find("hook") or n:find("refrain") then
            cur_sec_id = 3 -- ⚡ CHORUS IMPACT
            cur_rgn_type = 4
          elseif n:find("pre") or n:find("build") then
            -- Pre-chorus / build: musical tension build, no artificial volume drops
            cur_sec_id = 1
            cur_rgn_type = 3
          elseif n:find("bridge") or n:find("break") or n:find("middle") or n:find("solo") then
            -- Bridge / breakdown: musical breakdown flow
            cur_sec_id = 4
            cur_rgn_type = 5
          elseif n:find("verse") or n:find("groove") or n:find("main") then
            cur_sec_id = 5 -- ■ VERSE / GROOVE
            cur_rgn_type = 2
          elseif n:find("intro") then
            cur_sec_id = 5 -- ■ INTRO (Steady-state groove baseline, zero macro level cliff into Verse)
            cur_rgn_type = 1
          elseif n:find("outro") then
            cur_sec_id = 5 -- ■ OUTRO
            cur_rgn_type = 6
          else
            cur_sec_id = 5 -- Any custom section label
            cur_rgn_type = 7
          end
        end
      else
        -- Markers as transition triggers if not inside an explicit region
        if cur_sec_id == 0 then
          if (n:find("chorus") and not n:find("pre")) or n:find("drop") or n:find("hook") then
            if math.abs(play_pos - pos) < 1.0 then
              cur_sec_id = 3
              cur_rgn_type = 4
            end
          elseif (n:find("pre") or n:find("build")) and math.abs(play_pos - pos) < 4.0 and play_pos >= pos then
            cur_sec_id = 1
            cur_rgn_type = 3
          elseif (n:find("bridge") or n:find("break")) and math.abs(play_pos - pos) < 1.0 then
            cur_sec_id = 4
            cur_rgn_type = 5
          elseif n:find("verse") and math.abs(play_pos - pos) < 1.0 then
            cur_sec_id = 5
            cur_rgn_type = 2
          end
        end
      end
    end
  end

  -- Pre-Intro: Play naturally with continuous full-fidelity audio (vacuum cut removed)
  
  local bridge_active = (has_regions or num_markers > 0) and 1 or 0
  
  -- 1. Broadcast to Damei Mixing Suite
  reaper.gmem_attach("DameiMixMetering")
  reaper.gmem_write(100, bridge_active)       -- Bridge Active Flag (1 = Online)
  reaper.gmem_write(101, cur_sec_id)          -- Current Section ID (1=Pre, 2=Breath, 3=Chorus, 4=Breakdown, 5=Verse)
  reaper.gmem_write(102, dist_to_chorus)      -- Seconds to Next Chorus Drop (-1 if none)
  reaper.gmem_write(103, num_regions)         -- Total Project Regions Count
  reaper.gmem_write(104, cur_rgn_idx)         -- Active Region Index Number
  reaper.gmem_write(105, cur_rgn_progress)    -- Active Region Progress (0.0 to 1.0)
  reaper.gmem_write(106, cur_rgn_type)        -- Region Type (1=Intro, 2=Verse, 3=Pre, 4=Chorus, 5=Bridge, 6=Outro, 7=Other)
  reaper.gmem_write(107, is_playing)          -- Playback State (1=Playing, 0=Stopped)
  reaper.gmem_write(108, cur_rgn_time_left)   -- Seconds left in active region
  reaper.gmem_write(109, reaper.time_precise()) -- Bridge heartbeat (suites treat >2 s old as a stale bridge)

  -- 2. Broadcast to Damei Ozone Mastering Suite
  reaper.gmem_attach("DameiMetering")
  reaper.gmem_write(100, bridge_active)
  reaper.gmem_write(101, cur_sec_id)
  reaper.gmem_write(102, dist_to_chorus)
  reaper.gmem_write(103, num_regions)
  reaper.gmem_write(104, cur_rgn_idx)
  reaper.gmem_write(105, cur_rgn_progress)
  reaper.gmem_write(106, cur_rgn_type)
  reaper.gmem_write(107, is_playing)
  reaper.gmem_write(108, cur_rgn_time_left)
  reaper.gmem_write(109, reaper.time_precise())

  -- Restore default attachment to DameiMixMetering
  reaper.gmem_attach("DameiMixMetering")
end

-- Project State relay (Mixing Suite bus -> Mastering Suite namespace). pcall-guarded, additive.
local _relay = nil
do
  local candidates = {
    reaper.GetResourcePath() .. "/Scripts/Damei/damei_project_state_relay.lua",
    [[c:\Dev\DameiAPI\reaper_scripts\damei_project_state_relay.lua]],
  }
  for _, p in ipairs(candidates) do
    if reaper.file_exists(p) then
      local ok, mod = pcall(dofile, p)
      if ok and type(mod) == "table" and mod.step then _relay = mod break end
    end
  end
end

local function loop()
  get_song_structure()
  if _relay then pcall(_relay.step) end
  reaper.gmem_attach("DameiMixMetering")
  -- Devastator AI Auto-Placement trigger from JSFX (1 or 3 = Bake to Timeline, 4 = Clear Track)
  reaper.gmem_attach("DameiMixMetering")
  local dev_trigger = reaper.gmem_read(990)
  if dev_trigger == 1 or dev_trigger == 3 then
    reaper.gmem_write(990, 0) -- Clear trigger
    local hub_path = [[c:\Dev\DameiAPI\reaper_scripts\Damei_Devastator_Hub.lua]]
    if reaper.file_exists(hub_path) then
      dofile(hub_path)
      reaper.gmem_write(990, 2) -- 2 = Placement Complete
    end
  elseif dev_trigger == 4 then
    reaper.gmem_write(990, 0)
    local tr_cnt = reaper.CountTracks(0)
    for i = 0, tr_cnt - 1 do
      local tr = reaper.GetTrack(0, i)
      local _, name = reaper.GetTrackName(tr, "")
      if name:find("CINEMATIC FX", 1, true) or name:find("DEVASTATOR", 1, true) then
        local cnt = reaper.CountTrackMediaItems(tr)
        for it_idx = cnt - 1, 0, -1 do
          local it = reaper.GetTrackMediaItem(tr, it_idx)
          reaper.DeleteTrackMediaItem(tr, it)
        end
        reaper.UpdateArrange()
        break
      end
    end
    reaper.gmem_write(990, 2) -- 2 = Action Complete
  end

  reaper.defer(loop)
end

loop()
