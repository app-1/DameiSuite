-- ============================================================================
-- Damei Mix Assistant -- Loudness-Compensated A/B Gain Matcher
-- File: damei_ab_gainmatch.lua
-- Location: %APPDATA%/REAPER/Scripts/Damei/damei_ab_gainmatch.lua
-- Architecture: ReaScript / ReaImGui | Zero-Allocation Audio-Level Compensator
-- ============================================================================
-- GMEM map:
--   DameiMetering namespace  -> bank = gmem[127]==0?0:32
--     [bank+0] = Momentary LUFS M    [bank+1] = Short-term LUFS S
--   DameiRefMetering namespace -> same layout, independent namespace
-- One-pole ballistics: smooth_offset = alpha*prev + (1-alpha)*delta
--   alpha = exp(-dt / BALLISTICS_TC),  TC = 1.8s
-- Silence gate: freeze trim when either stream < -55 LUFS
-- ============================================================================

local AB_MATCH = {}

-- ----------------------------------------------------------------------------
-- 1. MODULE STATE
-- ----------------------------------------------------------------------------
local St = {
  enabled          = false,
  mode             = 1,     -- 1=Trim Reference to match Mix, 2=Trim Mix to match Reference
  smooth_offset_db = 0.0,   -- Ballistics-smoothed gain trim in dB
  target_delta_db  = 0.0,   -- Raw instantaneous LUFS delta (Mix - Ref)
  ref_track_guid   = nil,   -- Cached GUID of track hosting Damei_RefMetering.jsfx
  last_calc_time   = 0.0,
  active_monitor   = "A",   -- "A" = Mix/Master,  "B" = Reference
  gate_active      = false, -- True when signal < silence floor
}

-- Calibration constants
local SILENCE_FLOOR_LUFS = -55.0  -- Freeze trim during silence/breaks
local BALLISTICS_TC      = 1.8    -- Time constant (s) -- prevents level pumping
local MAX_TRIM_DB        = 18.0   -- Hard clamp ±18 dB

-- Color palette
local COL_ACTIVE_A = 0x50C878FF  -- Green (working mix)
local COL_ACTIVE_B = 0x3CA0E0FF  -- Cyan/blue (reference)
local COL_TRIM     = 0xD4A24CFF  -- Gold (trim readout)
local COL_MUTED    = 0x888888AA  -- Disabled / gated
local COL_WARN     = 0xE04444FF  -- Red (mismatch warning)

-- ----------------------------------------------------------------------------
-- 2. TRACK RESOLUTION (GUID-anchored, no numeric indices)
-- ----------------------------------------------------------------------------
--- Locate the track hosting Damei_RefMetering.jsfx
-- Uses cached GUID for O(1) lookup on repeated frames
function AB_MATCH.resolve_ref_track()
  -- Fast path: verify cached GUID still valid
  if St.ref_track_guid then
    for t = 0, reaper.CountTracks(0) - 1 do
      local tr = reaper.GetTrack(0, t)
      if reaper.GetTrackGUID(tr) == St.ref_track_guid then
        return tr
      end
    end
    St.ref_track_guid = nil  -- GUID stale (track deleted)
  end

  -- Slow path: scan FX chains for Damei_RefMetering
  for t = 0, reaper.CountTracks(0) - 1 do
    local tr = reaper.GetTrack(0, t)
    for f = 0, reaper.TrackFX_GetCount(tr) - 1 do
      local _, nm = reaper.TrackFX_GetFXName(tr, f, "")
      if nm:find("Damei_RefMetering") or nm:find("RefMetering") then
        St.ref_track_guid = reaper.GetTrackGUID(tr)
        return tr
      end
    end
  end

  return nil
end

-- ----------------------------------------------------------------------------
-- 3. REAL-TIME LUFS POLLING & BALLISTICS ENGINE
-- ----------------------------------------------------------------------------
--- Poll gmem, compute smoothed loudness delta, optionally apply trim.
-- Call once per defer frame (called internally by render).
-- Zero table allocations: all values are module-scope primitives.
function AB_MATCH.update()
  if reaper.GetPlayState() == 0 then return end

  local now = reaper.time_precise()
  local dt  = math.min(now - (St.last_calc_time > 0 and St.last_calc_time or now), 0.1)
  St.last_calc_time = now

  -- 1. Read working mix LUFS from DameiMetering
  reaper.gmem_attach("DameiMetering")
  local bm       = (reaper.gmem_read(127) or 0) == 0 and 0 or 32
  local mix_s    = reaper.gmem_read(bm + 1) or -70   -- Short-term 3s
  local mix_m    = reaper.gmem_read(bm + 0) or -70   -- Momentary 400ms
  local mix_lufs = mix_s > -60 and mix_s or mix_m

  -- 2. Read reference LUFS from DameiRefMetering (independent namespace)
  reaper.gmem_attach("DameiRefMetering")
  local br       = (reaper.gmem_read(127) or 0) == 0 and 0 or 32
  local ref_s    = reaper.gmem_read(br + 1) or -70
  local ref_m    = reaper.gmem_read(br + 0) or -70
  local ref_lufs = ref_s > -60 and ref_s or ref_m

  -- 3. Silence gating: freeze trim if either stream is inaudible
  if mix_lufs < SILENCE_FLOOR_LUFS or ref_lufs < SILENCE_FLOOR_LUFS then
    St.gate_active = true
    return
  end
  St.gate_active = false

  -- 4. Raw loudness delta: positive = Mix is louder than Ref
  --    Example: Mix=-14, Ref=-9 -> delta=-5 (Ref is 5 dB hotter)
  local delta = mix_lufs - ref_lufs
  St.target_delta_db = delta

  -- 5. One-pole ballistics filter (prevents audible pumping on transients)
  --    alpha approaches 1 as TC increases -> slower tracking
  local alpha = math.exp(-dt / BALLISTICS_TC)
  St.smooth_offset_db = alpha * St.smooth_offset_db + (1.0 - alpha) * delta
  St.smooth_offset_db = math.max(-MAX_TRIM_DB, math.min(MAX_TRIM_DB, St.smooth_offset_db))

  -- 6. Apply trim to reference track volume (when match is enabled)
  if St.enabled then
    local ref_tr = AB_MATCH.resolve_ref_track()
    if ref_tr then
      if St.mode == 1 then
        -- Mode 1: Trim Reference DOWN when Ref is louder, UP when quieter
        -- target_trim = +smooth_offset  (positive delta = mix louder = boost ref)
        -- IEEE 754 guard: clamp before db->lin conversion
        local trim_db  = math.max(-MAX_TRIM_DB, math.min(MAX_TRIM_DB, St.smooth_offset_db))
        local lin_vol  = 10.0 ^ (trim_db / 20.0)
        reaper.SetMediaTrackInfo_Value(ref_tr, "D_VOL", lin_vol)
      end
      -- Mode 2 (trim mix): would write to master volume - reserved for future Ozone-mode
    end
  end
end

-- ----------------------------------------------------------------------------
-- 4. INSTANT A/B MONITOR ROUTING
-- ----------------------------------------------------------------------------
--- Toggle between working mix (A) and reference track (B) auditioning
-- @param target string|nil  "A", "B", or nil (toggles)
function AB_MATCH.toggle_monitor(target)
  local ref_tr = AB_MATCH.resolve_ref_track()
  if not ref_tr then return end

  St.active_monitor = target or (St.active_monitor == "A" and "B" or "A")

  reaper.PreventUIRefresh(1)
  if St.active_monitor == "A" then
    -- Return to working mix: un-solo and mute reference
    reaper.SetMediaTrackInfo_Value(ref_tr, "I_SOLO", 0)
    reaper.SetMediaTrackInfo_Value(ref_tr, "B_MUTE", 1)
  else
    -- Audition reference: solo in place, un-mute
    reaper.SetMediaTrackInfo_Value(ref_tr, "B_MUTE", 0)
    reaper.SetMediaTrackInfo_Value(ref_tr, "I_SOLO", 2)  -- Solo in Place
  end
  reaper.PreventUIRefresh(-1)
  reaper.TrackList_AdjustWindows(false)
end

-- ----------------------------------------------------------------------------
-- 5. REAIMGUI PRESENTATION
-- ----------------------------------------------------------------------------
--- Render the A/B Matcher strip inside any ReaImGui window
-- @param ctx ImGui_Context
function AB_MATCH.render(ctx)
  AB_MATCH.update()

  local ref_tr     = AB_MATCH.resolve_ref_track()
  local ref_online = (ref_tr ~= nil)

  reaper.ImGui_BeginGroup(ctx)

  -- ── Header ────────────────────────────────────────────────────────────────
  reaper.ImGui_TextColored(ctx, COL_TRIM, "LOUDNESS-MATCHED A/B")
  reaper.ImGui_SameLine(ctx)
  if ref_online then
    reaper.ImGui_TextColored(ctx, COL_ACTIVE_A, "  ● Ref Linked")
  else
    reaper.ImGui_TextColored(ctx, COL_MUTED,    "  ○ No Damei_RefMetering Found")
    reaper.ImGui_EndGroup(ctx)
    return
  end
  reaper.ImGui_Separator(ctx)

  -- ── A / B Monitor Selector ────────────────────────────────────────────────
  reaper.ImGui_PushStyleVar(ctx, reaper.ImGui_StyleVar_FrameRounding(), 4.0)

  -- [A] Mix button
  local is_a = (St.active_monitor == "A")
  reaper.ImGui_PushStyleColor(ctx, reaper.ImGui_Col_Button(),
    is_a and COL_ACTIVE_A or 0x24242CFF)
  reaper.ImGui_PushStyleColor(ctx, reaper.ImGui_Col_Text(),
    is_a and 0x000000FF or 0xCCCCCCFF)
  if reaper.ImGui_Button(ctx, " [A] MIX (Master) ##abm_a", 135, 26) then
    AB_MATCH.toggle_monitor("A")
  end
  reaper.ImGui_PopStyleColor(ctx, 2)

  reaper.ImGui_SameLine(ctx, 0, 4)

  -- [B] Reference button
  local is_b = (St.active_monitor == "B")
  reaper.ImGui_PushStyleColor(ctx, reaper.ImGui_Col_Button(),
    is_b and COL_ACTIVE_B or 0x24242CFF)
  reaper.ImGui_PushStyleColor(ctx, reaper.ImGui_Col_Text(),
    is_b and 0x000000FF or 0xCCCCCCFF)
  if reaper.ImGui_Button(ctx, " [B] REFERENCE ##abm_b", 120, 26) then
    AB_MATCH.toggle_monitor("B")
  end
  reaper.ImGui_PopStyleColor(ctx, 2)
  reaper.ImGui_PopStyleVar(ctx)

  reaper.ImGui_SameLine(ctx, 0, 10)

  -- ── MATCH ON/OFF Toggle ────────────────────────────────────────────────────
  reaper.ImGui_PushStyleColor(ctx, reaper.ImGui_Col_Button(),
    St.enabled and COL_TRIM or 0x2A2A34FF)
  reaper.ImGui_PushStyleColor(ctx, reaper.ImGui_Col_Text(),
    St.enabled and 0x000000FF or 0xAAAAAAFF)
  if reaper.ImGui_Button(ctx, St.enabled and "MATCH: ON##abm_en" or "MATCH:OFF##abm_en", 88, 26) then
    St.enabled = not St.enabled
    if not St.enabled and ref_tr then
      -- Reset reference to unity gain when deactivated
      reaper.SetMediaTrackInfo_Value(ref_tr, "D_VOL", 1.0)
    end
  end
  reaper.ImGui_PopStyleColor(ctx, 2)

  reaper.ImGui_SameLine(ctx, 0, 8)

  -- ── Trim Readout + Gate Status ─────────────────────────────────────────────
  if St.gate_active then
    reaper.ImGui_TextColored(ctx, COL_MUTED,
      string.format("Trim: %+.1f dB  (Gated)", St.smooth_offset_db))
  else
    local abs_delta  = math.abs(St.target_delta_db)
    local col_offset = abs_delta > 6.0 and COL_WARN or COL_TRIM
    reaper.ImGui_TextColored(ctx, col_offset,
      string.format("Trim: %+.1f dB", St.smooth_offset_db))
    if abs_delta > 6.0 then
      reaper.ImGui_SameLine(ctx, 0, 4)
      reaper.ImGui_TextColored(ctx, COL_WARN,
        string.format("  ⚠ +%.1f dB mismatch", abs_delta))
    end
  end

  if reaper.ImGui_IsItemHovered(ctx) then
    reaper.ImGui_SetTooltip(ctx,
      "Continuous ITU-R BS.1770 loudness offset applied to reference track.\n" ..
      string.format("Raw delta: %+.2f dB   Smoothed (TC=%.1fs): %+.2f dB",
        St.target_delta_db, BALLISTICS_TC, St.smooth_offset_db))
  end

  reaper.ImGui_Spacing(ctx)

  -- ── LUFS Dual Readout Strip ────────────────────────────────────────────────
  reaper.ImGui_BeginGroup(ctx)
  reaper.gmem_attach("DameiMetering")
  local bm     = (reaper.gmem_read(127) or 0) == 0 and 0 or 32
  local mix_s  = reaper.gmem_read(bm + 1) or -70
  reaper.gmem_attach("DameiRefMetering")
  local br     = (reaper.gmem_read(127) or 0) == 0 and 0 or 32
  local ref_s  = reaper.gmem_read(br + 1) or -70

  reaper.ImGui_TextColored(ctx, COL_ACTIVE_A,
    string.format("Mix (S):  %.1f LUFS", mix_s))
  reaper.ImGui_SameLine(ctx, 0, 16)
  reaper.ImGui_TextColored(ctx, COL_ACTIVE_B,
    string.format("Ref  (S): %.1f LUFS", ref_s))
  reaper.ImGui_SameLine(ctx, 0, 16)
  reaper.ImGui_TextDisabled(ctx,
    string.format("Δ = %+.1f dB", mix_s - ref_s))

  reaper.ImGui_EndGroup(ctx)
  reaper.ImGui_EndGroup(ctx)
end

-- ----------------------------------------------------------------------------
-- 6. PROJECT STATE PERSISTENCE
-- ----------------------------------------------------------------------------
function AB_MATCH.save_state()
  reaper.SetProjExtState(0, "DameiMix", "AB_State",
    string.format("%d;%d;%.3f", St.enabled and 1 or 0, St.mode, St.smooth_offset_db))
end

function AB_MATCH.load_state()
  local ok, p = reaper.GetProjExtState(0, "DameiMix", "AB_State")
  if ok and p ~= "" then
    local en, md, sm = p:match("([^;]+);([^;]+);([^;]+)")
    St.enabled          = (tonumber(en) == 1)
    St.mode             = tonumber(md) or 1
    St.smooth_offset_db = tonumber(sm) or 0.0
  end
end

AB_MATCH.load_state()
return AB_MATCH
