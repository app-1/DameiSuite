-- ============================================================================
-- Damei Ozone 12 & Masterdesk — Master Chain Bridge & Controller
-- File: damei_ozone_bridge.lua
-- Bridges ReaImGui UI to REAPER native plugins:
--   - ReEQ / ReaEQ
--   - ReaComp
--   - ReaXComp
--   - JS: RBJ Stereo Image Filter
--   - JS: Clipper / Damei_Clipper
--   - ReaLimit
--   - JS: Volume Adjustment
-- ============================================================================

local reaper = reaper
local BRIDGE = {}

-- Fingerprints for matching plugins
local PLUGINS = {
  anchor   = { name = "Damei Ozone Anchor", pattern = "ozone" },
  trim     = { name = "JS: Volume Adjustment", pattern = "volume adjustment" },
  reeq     = { name = "JS: ReEQ", pattern = "reeq" },
  reaeq    = { name = "ReaEQ", pattern = "reaeq" },
  imager   = { name = "JS: RBJ Stereo Image Filter", pattern = "rbj stereo image" },
  reacomp  = { name = "ReaComp", pattern = "reacomp" },
  reaxcomp = { name = "ReaXComp", pattern = "reaxcomp" },
  clipper  = { name = "JS: Clipper", pattern = "clipper" },
  realimit = { name = "ReaLimit", pattern = "realimit" },
}

-- ---------------------------------------------------------------------------
-- Scan track for suite modules
-- ---------------------------------------------------------------------------
function BRIDGE.scan_chain(track)
  track = track or reaper.GetMasterTrack(0)
  local found = {}
  local count = reaper.TrackFX_GetCount(track)

  for i = 0, count - 1 do
    local _, name = reaper.TrackFX_GetFXName(track, i, "")
    local lname = name:lower()

    for key, spec in pairs(PLUGINS) do
      if lname:find(spec.pattern, 1, true) and not found[key] then
        found[key] = { idx = i, name = name }
      end
    end
  end

  return found
end

-- ---------------------------------------------------------------------------
-- Helper to add FX if missing
-- ---------------------------------------------------------------------------
local function ensure_fx(track, name, ident)
  local idx = reaper.TrackFX_AddByName(track, ident, false, -1)
  if idx < 0 then
    -- Fallback generic
    idx = reaper.TrackFX_AddByName(track, name, false, -1)
  end
  return idx
end

-- ---------------------------------------------------------------------------
-- Setup Complete Mastering Chain in standard signal order
-- ---------------------------------------------------------------------------
function BRIDGE.setup_master_chain(track)
  track = track or reaper.GetMasterTrack(0)
  reaper.Undo_BeginBlock()
  reaper.PreventUIRefresh(1)

  local cur = BRIDGE.scan_chain(track)

  -- Order: Trim -> ReEQ -> Imager -> ReaComp -> ReaXComp -> Clipper -> ReaLimit -> Anchor
  if not cur.trim then
    reaper.TrackFX_AddByName(track, "JS: Volume Adjustment", false, -1)
  end
  if not cur.reeq and not cur.reaeq then
    local r = reaper.TrackFX_AddByName(track, "JS: ReEQ (by Justin)", false, -1)
    if r < 0 then reaper.TrackFX_AddByName(track, "ReaEQ", false, -1) end
  end
  if not cur.imager then
    reaper.TrackFX_AddByName(track, "JS: RBJ Stereo Image Filter", false, -1)
  end
  if not cur.reacomp then
    reaper.TrackFX_AddByName(track, "ReaComp", false, -1)
  end
  if not cur.reaxcomp then
    reaper.TrackFX_AddByName(track, "ReaXComp", false, -1)
  end
  if not cur.clipper then
    local c = reaper.TrackFX_AddByName(track, "JS: Damei_Clipper", false, -1)
    if c < 0 then reaper.TrackFX_AddByName(track, "JS: Clipper", false, -1) end
  end
  if not cur.realimit then
    reaper.TrackFX_AddByName(track, "ReaLimit", false, -1)
  end
  if not cur.anchor then
    reaper.TrackFX_AddByName(track, "JS: Damei_OzoneSuite", false, -1)
  end

  reaper.PreventUIRefresh(-1)
  reaper.Undo_EndBlock("Damei: Setup Ozone 12 Mastering Chain", -1)
  return BRIDGE.scan_chain(track)
end

-- ---------------------------------------------------------------------------
-- Apply AI Solution to plugins atomically
-- ---------------------------------------------------------------------------
function BRIDGE.apply_solution(track, sol)
  track = track or reaper.GetMasterTrack(0)
  if not sol then return false end

  reaper.Undo_BeginBlock()
  reaper.PreventUIRefresh(1)

  local chain = BRIDGE.scan_chain(track)

  -- 1. Corrective EQ (ReEQ / ReaEQ)
  local eq_slot = chain.reeq or chain.reaeq
  if eq_slot and sol.reeq then
    local fx = eq_slot.idx
    -- Apply up to 6 bands
    for _, band in ipairs(sol.reeq) do
      local b = (band.idx or 1) - 1
      local p_base = b * 3 -- typical JS ReEQ base or ReaEQ
      -- ReaEQ mapping:
      -- Frequency: log mapped
      if eq_slot == chain.reaeq then
        local norm_f = math.log(math.max(20, math.min(24000, band.freq)) / 20.0) / math.log(24000.0 / 20.0)
        reaper.TrackFX_SetParamNormalized(track, fx, b * 5 + 0, norm_f)
        -- Gain: dB (-24 to +24)
        local norm_g = (math.max(-24, math.min(24, band.gain_db)) + 24.0) / 48.0
        reaper.TrackFX_SetParamNormalized(track, fx, b * 5 + 1, norm_g)
        -- Q / Bandwidth (approx 2.0 / Q)
        local bw = math.max(0.1, math.min(4.0, 2.0 / (band.q or 1.4)))
        local norm_bw = (bw - 0.1) / 3.9
        reaper.TrackFX_SetParamNormalized(track, fx, b * 5 + 2, norm_bw)
      else
        -- JS ReEQ parameter mapping (slider access)
        -- Band 1 freq, gain, q
        reaper.TrackFX_SetParam(track, fx, b * 3 + 0, band.freq)
        reaper.TrackFX_SetParam(track, fx, b * 3 + 1, band.gain_db)
        reaper.TrackFX_SetParam(track, fx, b * 3 + 2, band.q)
      end
    end
  end

  -- 2. Bus Compressor (ReaComp)
  if chain.reacomp and sol.reacomp then
    local fx = chain.reacomp.idx
    -- Param 0 = Threshold (dB), Param 1 = Ratio, Param 2 = Attack (ms), Param 3 = Release (ms)
    if sol.reacomp.enabled then
      reaper.TrackFX_SetParam(track, fx, 0, sol.reacomp.threshold_db or -14.0)
      reaper.TrackFX_SetParam(track, fx, 1, sol.reacomp.ratio or 1.5)
      reaper.TrackFX_SetParam(track, fx, 2, sol.reacomp.attack_ms or 30.0)
      reaper.TrackFX_SetParam(track, fx, 3, sol.reacomp.release_ms or 120.0)
      reaper.TrackFX_SetParam(track, fx, 6, 0.0) -- Dry
      reaper.TrackFX_SetParam(track, fx, 7, 0.0) -- Wet
      reaper.TrackFX_SetEnabled(track, fx, true)
    else
      reaper.TrackFX_SetEnabled(track, fx, false) -- bypass if not needed
    end
  end

  -- 3. Transient Clipper (Clipper)
  if chain.clipper and sol.clipper then
    local fx = chain.clipper.idx
    -- Slider 1: Drive / Gain (dB)
    reaper.TrackFX_SetParam(track, fx, 0, sol.clipper.drive_db or 0.0)
    -- Slider 2: Ceiling
    reaper.TrackFX_SetParam(track, fx, 1, sol.clipper.ceiling_db or -0.2)
  end

  -- 4. Maximizer (ReaLimit)
  if chain.realimit and sol.realimit then
    local fx = chain.realimit.idx
    -- Param 0: Threshold / Makeup (dB)
    reaper.TrackFX_SetParam(track, fx, 0, sol.realimit.threshold_db or 0.0)
    -- Param 1: Ceiling (dB)
    reaper.TrackFX_SetParam(track, fx, 1, sol.realimit.ceiling_db or -0.3)
    -- Param 2: True Peak mode (1 = on)
    reaper.TrackFX_SetParam(track, fx, 2, 1.0)
  end

  -- 5. Stereo Imager (RBJ Stereo Image Filter)
  if chain.imager and sol.imager then
    local fx = chain.imager.idx
    -- Mono maker cutoff
    if sol.imager.mono_maker_hz and sol.imager.mono_maker_hz > 20 then
      reaper.TrackFX_SetParam(track, fx, 0, sol.imager.mono_maker_hz)
    end
  end

  reaper.PreventUIRefresh(-1)
  reaper.Undo_EndBlock("Damei Ozone 12: Apply AI Master Resolution", -1)
  return true
end

return BRIDGE
