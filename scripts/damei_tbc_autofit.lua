-- ============================================================================
-- Damei Tonal Balance (DTB) -- Autonomous "Fit to Target" Auto-EQ Engine
-- File: damei_tbc_autofit.lua
-- Location: %APPDATA%/REAPER/Scripts/Damei/damei_tbc_autofit.lua
-- Architecture: Lua 5.3+ | Numerical Residual Clustering & Parameter Synthesis
-- ============================================================================
-- Algorithm summary:
--   1. Compute residual delta (Target - Master) across 256 log-spaced bins
--   2. 1/3-octave triangular smoothing removes micro-comb tooth noise
--   3. Extrema extraction ranks clusters by amplitude * sqrt(integrated_area)
--   4. Non-colliding band selector enforces >= 0.55-octave separation
--   5. -3 dB bandwidth traces Q = f0 / delta_f, clamped to musical mastering range
--   6. Gains clamped to +/-max_gain_db * strength, applied to JS:ReEQ or ReaEQ
-- ============================================================================

local AUTOFIT = {}

-- Load Bridge dependencies (graceful fail if bridge not yet loaded)
local resource_path = reaper.GetResourcePath()
package.path = package.path .. ";" .. resource_path .. "/Scripts/Damei/?.lua"
local bridge_ok, BRIDGE = pcall(require, "damei_tbc_bridge")
if not bridge_ok or type(BRIDGE) ~= "table" then BRIDGE = nil end

-- ----------------------------------------------------------------------------
-- 1. CONFIGURATION CONSTANTS
-- ----------------------------------------------------------------------------
local DISP_BINS = 256
local F_MIN     = 20.0
local F_MAX     = 20000.0
local LOG_RATIO = math.log(F_MAX / F_MIN)   -- ln(1000) ≈ 6.9078

-- Safety limits (mastering grade -- prevents unnatural comb filtering)
local DEFAULT_STRENGTH      = 0.85   -- Correction scale applied to raw delta
local DEFAULT_MAX_GAIN_DB   = 3.5    -- Hard ceiling for any single band cut/boost
local DEFAULT_MIN_GAIN_DB   = 0.4    -- Noise floor: deviations below this ignored
local MIN_ALLOWED_Q         = 0.70   -- Broad musical minimum Q
local MAX_ALLOWED_Q         = 4.50   -- Maximum surgical Q for tonal balance
local MIN_OCTAVE_SEPARATION = 0.55   -- ~1/2 octave minimum between bands
local SMOOTH_HALF_WIN       = 4      -- 9-bin triangular kernel ≈ 1/3-octave in 256-bin log space

-- Analysis range: skip sub-rumble and ultrasonic hash
local BIN_MIN = 12   -- ~31 Hz
local BIN_MAX = 245  -- ~16.2 kHz

-- Pre-allocated static scratchpads (zero GC per call)
local _residual_raw    = {}
local _residual_smooth = {}
for i = 1, DISP_BINS do
  _residual_raw[i]    = 0.0
  _residual_smooth[i] = 0.0
end

-- ----------------------------------------------------------------------------
-- 2. FREQUENCY & LOG BIN TRANSFORMS
-- ----------------------------------------------------------------------------
local function bin_to_freq(b)
  return F_MIN * (1000.0 ^ ((b - 1.0) / (DISP_BINS - 1.0)))
end

local function freq_separation_octaves(f1, f2)
  return math.abs(math.log(math.max(f1, 1e-9) / math.max(f2, 1e-9)) / math.log(2.0))
end

-- ----------------------------------------------------------------------------
-- 3. 1/3-OCTAVE TRIANGULAR SMOOTHING
-- In a 256-bin log space across 10 octaves: 1 octave = 25.6 bins.
-- 1/3-octave = 8.5 bins -> half-window = 4 -> 9-bin kernel. Constant per bin.
-- ----------------------------------------------------------------------------
local function smooth_residual(src, dst)
  for i = 1, DISP_BINS do
    local sum_w, sum_v = 0.0, 0.0
    for k = -SMOOTH_HALF_WIN, SMOOTH_HALF_WIN do
      local idx = i + k
      if idx >= 1 and idx <= DISP_BINS then
        local w = 1.0 - math.abs(k) / (SMOOTH_HALF_WIN + 1.0)
        sum_v = sum_v + src[idx] * w
        sum_w = sum_w + w
      end
    end
    dst[i] = (sum_w > 0) and (sum_v / sum_w) or 0.0
  end
end

-- ----------------------------------------------------------------------------
-- 4. -3 dB BANDWIDTH -> Q ESTIMATION
-- Traces outward from a peak/trough to find where the error drops to half-power.
-- ----------------------------------------------------------------------------
local function estimate_q(res, center_idx, is_positive)
  local f0      = bin_to_freq(center_idx)
  local peak    = res[center_idx]
  local half_pw = peak * 0.7071   -- -3 dB point

  local left_bin = BIN_MIN
  for i = center_idx - 1, BIN_MIN, -1 do
    left_bin = i
    if is_positive and (res[i] <= half_pw or res[i] <= 0.0) then break end
    if not is_positive and (res[i] >= half_pw or res[i] >= 0.0) then break end
  end

  local right_bin = BIN_MAX
  for i = center_idx + 1, BIN_MAX do
    right_bin = i
    if is_positive and (res[i] <= half_pw or res[i] <= 0.0) then break end
    if not is_positive and (res[i] >= half_pw or res[i] >= 0.0) then break end
  end

  local f_lo    = bin_to_freq(left_bin)
  local f_hi    = bin_to_freq(right_bin)
  local delta_f = math.max(f_hi - f_lo, f0 * 0.15)   -- floor: prevents div/0
  local raw_q   = f0 / delta_f
  return math.max(MIN_ALLOWED_Q, math.min(MAX_ALLOWED_Q, raw_q))
end

-- ----------------------------------------------------------------------------
-- 5. EXTREMA EXTRACTION & SCORING
-- Detects local maxima / minima, integrates area under each error blob,
-- scores by amplitude * sqrt(integrated_area) for statistical significance.
-- ----------------------------------------------------------------------------
local function extract_clusters(res, min_threshold)
  local clusters = {}

  for i = BIN_MIN + 1, BIN_MAX - 1 do
    local prev = res[i - 1]
    local curr = res[i]
    local next = res[i + 1]

    local is_peak   = curr > prev  and curr >= next and curr >=  min_threshold
    local is_trough = curr < prev  and curr <= next and curr <= -min_threshold

    if is_peak or is_trough then
      -- Integrate absolute area under the error blob until zero-crossing
      local area = 0.0
      local l = i
      while l >= BIN_MIN do
        if is_peak   and res[l] <= 0.0 then break end
        if is_trough and res[l] >= 0.0 then break end
        area = area + math.abs(res[l]); l = l - 1
      end
      local r = i + 1
      while r <= BIN_MAX do
        if is_peak   and res[r] <= 0.0 then break end
        if is_trough and res[r] >= 0.0 then break end
        area = area + math.abs(res[r]); r = r + 1
      end

      clusters[#clusters + 1] = {
        bin      = i,
        freq     = bin_to_freq(i),
        raw_gain = curr,
        q        = estimate_q(res, i, is_peak),
        area     = area,
        score    = math.abs(curr) * math.sqrt(area + 1.0),
        is_boost = is_peak,
      }
    end
  end

  -- Sort descending by error score (most significant problem first)
  table.sort(clusters, function(a, b) return a.score > b.score end)
  return clusters
end

-- ----------------------------------------------------------------------------
-- 6. NON-COLLIDING BAND SELECTOR
-- Enforces minimum octave separation between selected bands.
-- ----------------------------------------------------------------------------
local function select_bands(clusters, count, min_sep)
  local selected = {}
  for _, c in ipairs(clusters) do
    if #selected >= count then break end
    local collides = false
    for _, s in ipairs(selected) do
      if freq_separation_octaves(c.freq, s.freq) < min_sep then
        collides = true; break
      end
    end
    if not collides then selected[#selected + 1] = c end
  end
  -- Sort ascending by frequency (sub -> high)
  table.sort(selected, function(a, b) return a.freq < b.freq end)
  return selected
end

-- ----------------------------------------------------------------------------
-- 7. CORE COMPUTE: produces synthesized band table
-- @param master_bins  table  256 dB values (normalized, 0-indexed) from VIEW._master_norm
-- @param target_bins  table  256 dB values (target corridor center curve)
-- @param opts         table  { strength, max_gain, bands_count }
-- @return table|nil   synthesized_bands = { {id,freq,gain,q,raw_diff}, ... }
-- @return string|nil  error/status message
-- ----------------------------------------------------------------------------
function AUTOFIT.compute(master_bins, target_bins, opts)
  if not master_bins or not target_bins then
    return nil, "Missing spectral data"
  end

  opts = opts or {}
  local strength   = opts.strength    or DEFAULT_STRENGTH
  local max_gain   = opts.max_gain    or DEFAULT_MAX_GAIN_DB
  local band_count = opts.bands_count or 4

  -- Silence guard: check mid-band mean energy (bins 60-180 ~120Hz-4kHz)
  local mean_e = 0.0
  for i = 60, 180 do mean_e = mean_e + (master_bins[i] or -70) end
  if (mean_e / 121.0) < -45.0 then
    return nil, "Master bus too quiet -- play audio to enable Fit."
  end

  -- 1. Residual delta: positive = master deficient (boost), negative = excess (cut)
  for i = 1, DISP_BINS do
    -- master_bins is 0-indexed (from display_bins / VIEW._master_norm)
    _residual_raw[i] = (target_bins[i] or 0) - (master_bins[i] or -70)
  end

  -- 2. 1/3-octave smooth to remove comb-filter micro-noise
  smooth_residual(_residual_raw, _residual_smooth)

  -- 3. Extract + score error clusters
  local clusters = extract_clusters(_residual_smooth, DEFAULT_MIN_GAIN_DB)
  if #clusters == 0 then
    return {}, "Mix is already within the target corridor."
  end

  -- 4. Select top 4 non-colliding bands
  local selected = select_bands(clusters, band_count, MIN_OCTAVE_SEPARATION)

  -- 5. Synthesize biquad parameters with safety clamps
  local bands = {}
  for i, c in ipairs(selected) do
    local gain = math.max(-max_gain, math.min(max_gain, c.raw_gain * strength))
    bands[#bands + 1] = {
      id       = i,
      freq     = math.floor(c.freq + 0.5),
      gain     = tonumber(string.format("%.2f", gain)),
      q        = tonumber(string.format("%.2f", c.q)),
      raw_diff = c.raw_gain,
    }
  end

  return bands, nil
end

-- ----------------------------------------------------------------------------
-- 8. APPLY: writes synthesized bands to JS:ReEQ or ReaEQ
-- @param track   MediaTrack
-- @param fx_idx  integer    FX chain index of the EQ
-- @param master_bins  table (same as AUTOFIT.compute)
-- @param target_bins  table (same as AUTOFIT.compute)
-- @param opts    table
-- @return boolean, string
-- ----------------------------------------------------------------------------
function AUTOFIT.apply(track, fx_idx, master_bins, target_bins, opts)
  if not track or not fx_idx or fx_idx < 0 then
    return false, "No target EQ instance selected."
  end

  local bands, err = AUTOFIT.compute(master_bins, target_bins, opts)
  if not bands then return false, err or "Fit calculation failed." end
  if #bands == 0 then return true, err or "Curve already balanced." end

  reaper.Undo_BeginBlock2(0)

  local _, fx_name = reaper.TrackFX_GetFXName(track, fx_idx, "")
  local is_reeq    = fx_name:lower():find("reeq") and not fx_name:lower():find("reaeq")

  for i, b in ipairs(bands) do
    if is_reeq then
      -- JS:ReEQ: band params stride 5 from base 0
      -- Band i: enable=(i-1)*5, type=(i-1)*5+1, freq=(i-1)*5+2, gain=(i-1)*5+3, Q=(i-1)*5+4
      local base = (i - 1) * 5
      reaper.TrackFX_SetParam(track, fx_idx, base + 0, 1.0)      -- Enable
      reaper.TrackFX_SetParam(track, fx_idx, base + 1, 0.0)      -- Bell/Peak
      reaper.TrackFX_SetParam(track, fx_idx, base + 2, b.freq)   -- Frequency (Hz)
      reaper.TrackFX_SetParam(track, fx_idx, base + 3, b.gain)   -- Gain (dB)
      reaper.TrackFX_SetParam(track, fx_idx, base + 4, b.q)      -- Q
    else
      -- ReaEQ fallback: normalized frequency, bands at stride 3 from param 0
      local base = (i - 1) * 3
      if BRIDGE and BRIDGE.M and BRIDGE.M.freq_to_norm then
        local norm_f = BRIDGE.M.freq_to_norm(b.freq, 20.0, 20000.0)
        reaper.TrackFX_SetParamNormalized(track, fx_idx, base + 0, norm_f)
        reaper.TrackFX_SetParam(track, fx_idx, base + 1, b.gain)
        reaper.TrackFX_SetParam(track, fx_idx, base + 2, b.q)
      else
        -- Minimum fallback: just write gain
        reaper.TrackFX_SetParam(track, fx_idx, base + 1, b.gain)
      end
    end
  end

  -- Build summary string
  local summary = string.format("Auto-Fit: %d bands applied  ", #bands)
  for _, b in ipairs(bands) do
    summary = summary .. string.format("[%d Hz %+.1f dB Q%.1f] ", b.freq, b.gain, b.q)
  end

  reaper.Undo_EndBlock2(0, "DTB Fit to Target Corridor", -1)
  return true, summary
end

-- ----------------------------------------------------------------------------
-- 9. PREVIEW RENDER (zero-allocation ReaImGui overlay)
-- Call from VIEW.draw_fine() when st.autofit_preview_bands is populated.
-- Draws proposed band markers as dashed vertical hairlines over the spectrum.
-- @param ImGui  wrapper  @param dl  draw_list  @param x0,y0,w,h  canvas bounds
-- @param db_floor,db_ceil  axis limits
-- @param bands  table  result of AUTOFIT.compute()
-- ----------------------------------------------------------------------------
function AUTOFIT.draw_preview(ImGui, dl, x0, y0, w, h, db_floor, db_ceil, bands)
  if not bands or #bands == 0 then return end

  local span_db = db_ceil - db_floor
  local F_RATIO = math.log(F_MAX / F_MIN)

  for _, b in ipairs(bands) do
    if b.freq and b.gain then
      -- X position: log-frequency mapping
      local norm_x = math.log(b.freq / F_MIN) / F_RATIO
      local px     = x0 + norm_x * w

      -- Y position of the gain node on the spectrum canvas
      local gain_clamped = math.max(db_floor, math.min(db_ceil, b.gain * 6))
      local norm_y       = (db_ceil - gain_clamped) / span_db
      local py           = y0 + norm_y * h

      -- Color: boost=cyan, cut=amber
      local col = b.gain >= 0 and 0x3CE0C8CC or 0xE0A23CCC

      -- Dashed vertical hairline (5px segments)
      local seg = 5.0
      local yy  = y0
      while yy < y0 + h do
        ImGui.DrawList_AddLine(dl, px, yy, px, math.min(yy + seg, y0+h), col, 1.0)
        yy = yy + seg * 2.0
      end

      -- Node circle
      ImGui.DrawList_AddCircle(dl, px, py, 5.0, col, 12, 1.5)
      ImGui.DrawList_AddCircleFilled(dl, px, py, 2.5, col)

      -- Frequency + gain label
      local label = string.format("%dHz %+.1fdB", b.freq, b.gain)
      ImGui.DrawList_AddText(dl, px + 6, py - 14, col, label)
    end
  end
end

return AUTOFIT
