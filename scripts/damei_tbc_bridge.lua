-- ============================================================================
-- Damei Tonal Balance -- Universal EQ Bridge
-- File: damei_tbc_bridge.lua
-- Provides: read/write access to ReaEQ, ReEQ, and FabFilter Pro-Q 3 bands
--           directly from the DTB canvas, with full Ctrl+Z undo support.
-- ============================================================================

reaper.gmem_attach("DameiMetering")

local BRIDGE = {}

-- Fingerprints for supported EQ plugins (case-insensitive partial match)
local EQ_FINGERPRINTS = {
  { tag = "reaeq",   name = "ReaEQ",    type = "reaeq"   },
  { tag = "reeq",    name = "ReEQ",     type = "reeq"    },
  { tag = "pro-q 3", name = "Pro-Q 3",  type = "proq3"   },
  { tag = "pro-q3",  name = "Pro-Q 3",  type = "proq3"   },
  -- ToneBoosters Equalizer 4 (TB Equaliser Pro)
  -- REAPER reports the FX name as e.g. "VST3: ToneBoosters Equalizer 4 (ToneBoosters)"
  -- Match on the shortest unambiguous substring across all build variants:
  { tag = "toneboosters equalizer", name = "TB Equaliser Pro", type = "tbeq" },
  { tag = "tb equalizer",           name = "TB Equaliser Pro", type = "tbeq" },
  { tag = "tb equaliser",           name = "TB Equaliser Pro", type = "tbeq" },
}

-- ReaEQ parameter index layout per band (0-based band index b):
--   b*5 + 0 = frequency (Hz, normalized 0..1 log-mapped to 20..24000)
--   b*5 + 1 = gain (dB)
--   b*5 + 2 = bandwidth (octaves)
--   b*5 + 3 = filter type (0=LP, 1=HP, 2=BP, 3=LS, 4=HS, 5=notch, 6=all, 7=peak)
--   b*5 + 4 = enabled (1=on)
local REAEQ_PARAMS_PER_BAND = 5
local REAEQ_FREQ_MIN = 20.0
local REAEQ_FREQ_MAX = 24000.0

local function reaeq_norm_to_hz(norm)
  return REAEQ_FREQ_MIN * ((REAEQ_FREQ_MAX / REAEQ_FREQ_MIN) ^ norm)
end

local function hz_to_reaeq_norm(hz)
  hz = math.max(REAEQ_FREQ_MIN, math.min(REAEQ_FREQ_MAX, hz))
  return math.log(hz / REAEQ_FREQ_MIN) / math.log(REAEQ_FREQ_MAX / REAEQ_FREQ_MIN)
end

-- ---------------------------------------------------------------------------
-- BRIDGE.scan_eq_tracks()
-- Returns an array of { track, track_name, fx_idx, plugin_type, plugin_name }
-- ---------------------------------------------------------------------------
function BRIDGE.scan_eq_tracks()
  local results = {}
  local function check_track(tr, tr_name)
    for f = 0, reaper.TrackFX_GetCount(tr) - 1 do
      local _, nm = reaper.TrackFX_GetFXName(tr, f, "")
      local lnm = nm:lower()
      for _, fp in ipairs(EQ_FINGERPRINTS) do
        if lnm:find(fp.tag, 1, true) then
          results[#results+1] = {
            track       = tr,
            track_name  = tr_name,
            fx_idx      = f,
            fx_name     = nm,
            plugin_type = fp.type,
            plugin_name = fp.name,
          }
          break  -- only first EQ per FX slot
        end
      end
    end
  end

  check_track(reaper.GetMasterTrack(0), "Master")
  for t = 0, reaper.CountTracks(0) - 1 do
    local tr = reaper.GetTrack(0, t)
    local _, nm = reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", "", false)
    check_track(tr, nm ~= "" and nm or string.format("Track %d", t+1))
  end
  return results
end

-- ---------------------------------------------------------------------------
-- BRIDGE.get_bands(track, fx_idx, plugin_type)
-- Returns array of { freq_hz, gain_db, q, filter_type, enabled, param_base }
-- ---------------------------------------------------------------------------
function BRIDGE.get_bands(track, fx_idx, plugin_type)
  if not track or fx_idx < 0 then return {} end
  local bands = {}

  if plugin_type == "reaeq" or plugin_type == "reeq" then
    -- ReaEQ: param 0 = num_bands, then bands at offsets
    local n_bands = math.floor(reaper.TrackFX_GetParamNormalized(track, fx_idx, 0) * 64 + 0.5)
    n_bands = math.max(1, math.min(n_bands, 64))
    for b = 0, n_bands - 1 do
      local base = 1 + b * REAEQ_PARAMS_PER_BAND
      local fn   = reaper.TrackFX_GetParamNormalized(track, fx_idx, base)
      local gn   = reaper.TrackFX_GetParamNormalized(track, fx_idx, base + 1)
      local bwn  = reaper.TrackFX_GetParamNormalized(track, fx_idx, base + 2)
      local ftn  = reaper.TrackFX_GetParamNormalized(track, fx_idx, base + 3)
      local en   = reaper.TrackFX_GetParamNormalized(track, fx_idx, base + 4)
      -- ReaEQ gain is normalized 0..1 mapping to -36..+36 dB
      local gain_db = (gn * 72.0) - 36.0
      -- Bandwidth normalized 0..1 -> 0.01..8.0 octaves
      local bw = math.max(0.01, bwn * 8.0)
      local q  = bw > 0 and (math.sqrt(2^bw) / (2^bw - 1)) or 1.0
      bands[#bands+1] = {
        freq_hz     = reaeq_norm_to_hz(fn),
        gain_db     = gain_db,
        q           = q,
        filter_type = math.floor(ftn * 7 + 0.5),
        enabled     = en > 0.5,
        param_base  = base,
        band_index  = b,
      }
    end

  elseif plugin_type == "proq3" then
    -- Pro-Q 3: 24 bands, each at fixed offsets. Param 0 = output gain.
    -- Band params: freq(norm), gain(norm), q(norm), shape, slope, stereoplace, enabled
    -- Normalized freq: log2(hz/20) / log2(24000/20), gain: (val-0.5)*90 dB, q: 0..1->0.025..40
    local PROQ3_PARAMS_PER_BAND = 7
    local PROQ3_BAND_BASE       = 2   -- first band starts at param index 2
    local n = 24
    for b = 0, n - 1 do
      local base = PROQ3_BAND_BASE + b * PROQ3_PARAMS_PER_BAND
      local fn   = reaper.TrackFX_GetParamNormalized(track, fx_idx, base)
      local gn   = reaper.TrackFX_GetParamNormalized(track, fx_idx, base + 1)
      local qn   = reaper.TrackFX_GetParamNormalized(track, fx_idx, base + 2)
      local en   = reaper.TrackFX_GetParamNormalized(track, fx_idx, base + 6)
      if en > 0.5 and fn > 0.001 then
        local hz     = 20.0 * (1200.0 ^ fn)
        local gain   = (gn - 0.5) * 90.0
        local q_val  = 0.025 * (1600.0 ^ qn)
        bands[#bands+1] = {
          freq_hz    = hz,
          gain_db    = gain,
          q          = q_val,
          enabled    = true,
          param_base = base,
          band_index = b,
        }
      end
    end
  elseif plugin_type == "tbeq" then
    -- ToneBoosters Equalizer 4 (TB Equaliser Pro)
    -- Param names are enumerated at runtime; no fixed index map.
    -- Match patterns: "band N frequency", "band N gain", "band N q"
    -- Supports up to 64 named bands (TB EQ 4 ships with up to 8 active by default).
    local n_params = reaper.TrackFX_GetNumParams(track, fx_idx)
    -- First pass: collect all freq/gain/q/bypass params grouped by band number
    local band_params = {}  -- band_params[N] = { freq_idx, gain_idx, q_idx, bypass_idx }
    for p = 0, n_params - 1 do
      local _, pname = reaper.TrackFX_GetParamName(track, fx_idx, p, "")
      local lp = pname:lower()
      -- Match "band N frequency" / "band N freq"
      local bn = lp:match("band%s+(%d+)%s+freq")
      if bn then
        local n = tonumber(bn)
        if n then
          band_params[n] = band_params[n] or {}
          band_params[n].freq_idx  = p
          band_params[n].freq_name = pname
        end
      end
      -- Match "band N gain" / "band N level"
      bn = lp:match("band%s+(%d+)%s+gain") or lp:match("band%s+(%d+)%s+level")
      if bn then
        local n = tonumber(bn)
        if n then
          band_params[n] = band_params[n] or {}
          band_params[n].gain_idx = p
        end
      end
      -- Match "band N q" / "band N bandwidth" / "band N resonance"
      bn = lp:match("band%s+(%d+)%s+q$") or
           lp:match("band%s+(%d+)%s+bandwidth") or
           lp:match("band%s+(%d+)%s+resonance")
      if bn then
        local n = tonumber(bn)
        if n then
          band_params[n] = band_params[n] or {}
          band_params[n].q_idx = p
        end
      end
      -- Match "band N bypass" / "band N enable" / "band N on"
      bn = lp:match("band%s+(%d+)%s+bypass") or
           lp:match("band%s+(%d+)%s+enable") or
           lp:match("band%s+(%d+)%s+on$")
      if bn then
        local n = tonumber(bn)
        if n then
          band_params[n] = band_params[n] or {}
          band_params[n].bypass_idx = p
        end
      end
    end

    -- Second pass: build band array for bands that have at least freq + gain
    -- ToneBoosters EQ 4 normalizes frequency as log2(hz/20) / log2(24000/20)
    -- Gain is normalized 0..1 -> -36..+36 dB (72 dB range, center = 0.5)
    -- Q is normalized 0..1 -> 0.025..40 (similar to Pro-Q 3)
    local TB_FREQ_MIN = 20.0
    local TB_FREQ_MAX = 24000.0
    local TB_FREQ_LOG = math.log(TB_FREQ_MAX / TB_FREQ_MIN) / math.log(2)
    local TB_GAIN_RANGE = 36.0   -- +/- dB
    local TB_Q_MIN, TB_Q_MAX = 0.025, 40.0

    local band_indices = {}
    for bn in pairs(band_params) do band_indices[#band_indices+1] = bn end
    table.sort(band_indices)

    for _, n in ipairs(band_indices) do
      local bp = band_params[n]
      if bp.freq_idx and bp.gain_idx then
        local fn = reaper.TrackFX_GetParamNormalized(track, fx_idx, bp.freq_idx)
        local gn = reaper.TrackFX_GetParamNormalized(track, fx_idx, bp.gain_idx)
        local qn = bp.q_idx and reaper.TrackFX_GetParamNormalized(track, fx_idx, bp.q_idx) or 0.5
        local en = bp.bypass_idx and reaper.TrackFX_GetParamNormalized(track, fx_idx, bp.bypass_idx) or 1.0

        -- Frequency decode: log-normalized
        local hz = TB_FREQ_MIN * (2 ^ (fn * TB_FREQ_LOG))
        -- Gain decode: center 0.5 = 0 dB
        local gain_db = (gn - 0.5) * (TB_GAIN_RANGE * 2)
        -- Q decode: exponential
        local q_val = TB_Q_MIN * ((TB_Q_MAX / TB_Q_MIN) ^ qn)
        -- Bypass: TB EQ uses 1=enabled, 0=bypassed (some versions invert this)
        local enabled = en > 0.5

        if enabled and hz >= TB_FREQ_MIN and hz <= TB_FREQ_MAX then
          bands[#bands+1] = {
            freq_hz    = hz,
            gain_db    = gain_db,
            q          = q_val,
            enabled    = true,
            param_base = bp.freq_idx,  -- freq param idx used as band identity
            band_index = n - 1,        -- 0-based for compat
            -- TB-specific: store gain/q indices for set_band_gain
            _gain_idx  = bp.gain_idx,
            _q_idx     = bp.q_idx,
            _tb_gain_range = TB_GAIN_RANGE,
          }
        end
      end
    end

  end

  return bands
end

-- ---------------------------------------------------------------------------
-- BRIDGE.set_band_gain(entry, band, gain_db)
-- Writes a new gain to a single band with undo support.
-- ---------------------------------------------------------------------------
function BRIDGE.set_band_gain(entry, band, gain_db)
  if not entry or not band then return end
  local tr = entry.track; local fx = entry.fx_idx
  local gain_norm
  if entry.plugin_type == "reaeq" or entry.plugin_type == "reeq" then
    gain_norm = math.max(0, math.min(1, (gain_db + 36.0) / 72.0))
    reaper.TrackFX_SetParamNormalized(tr, fx, band.param_base + 1, gain_norm)
  elseif entry.plugin_type == "proq3" then
    gain_norm = math.max(0, math.min(1, (gain_db / 90.0) + 0.5))
    reaper.TrackFX_SetParamNormalized(tr, fx, band.param_base + 1, gain_norm)
  elseif entry.plugin_type == "tbeq" then
    -- TB EQ 4: use the stored _gain_idx and _tb_gain_range from get_bands
    local gr = band._tb_gain_range or 36.0
    gain_norm = math.max(0, math.min(1, (gain_db / (gr * 2)) + 0.5))
    local gain_param = band._gain_idx or (band.param_base + 1)
    reaper.TrackFX_SetParamNormalized(tr, fx, gain_param, gain_norm)
  end
  reaper.Undo_OnStateChangeEx2(0,
    string.format("DTB: %s band %.0f Hz %+.1f dB", entry.plugin_name, band.freq_hz, gain_db),
    -1, -1)
end

-- ---------------------------------------------------------------------------
-- BRIDGE.poll(now)
-- Per-frame update: refreshes band list for the active EQ entry.
-- Called from tbc.lua when EQ bridge panel is visible.
-- ---------------------------------------------------------------------------
BRIDGE._eq_entries    = {}
BRIDGE._active_entry  = nil
BRIDGE._active_bands  = {}
BRIDGE._drag_band     = nil
BRIDGE._drag_start_y  = 0
BRIDGE._drag_start_db = 0

function BRIDGE.poll(now)
  -- Rescan track list every 2 seconds
  if not BRIDGE._last_scan or (now - BRIDGE._last_scan) > 2.0 then
    BRIDGE._eq_entries = BRIDGE.scan_eq_tracks()
    BRIDGE._last_scan  = now
    -- Revalidate active entry
    if BRIDGE._active_entry then
      local found = false
      for _, e in ipairs(BRIDGE._eq_entries) do
        if e.track == BRIDGE._active_entry.track and e.fx_idx == BRIDGE._active_entry.fx_idx then
          BRIDGE._active_entry = e; found = true; break
        end
      end
      if not found then BRIDGE._active_entry = nil end
    end
  end
  -- Refresh band data every frame if an entry is selected
  if BRIDGE._active_entry then
    BRIDGE._active_bands = BRIDGE.get_bands(
      BRIDGE._active_entry.track,
      BRIDGE._active_entry.fx_idx,
      BRIDGE._active_entry.plugin_type)
    BRIDGE.bands_b = BRIDGE._active_bands
  else
    BRIDGE.bands_b = nil
  end
end

return BRIDGE