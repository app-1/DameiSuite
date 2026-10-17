-- ===========================================================================
-- damei_heuristics.lua  --  Damei Offline Heuristic Rule Engine
-- Provides actionable mix advice from live gmem data with zero network
-- dependency. Called when IPC.state == "DISCONNECTED" (HermesAgent offline).
-- Returns: list of { severity, band, message, action }
--   severity: "warn" | "info" | "ok"
--   band:     "sub" | "bass" | "mid" | "high" | "global"
-- ===========================================================================

local H = {}

-- gmem indices (must match Damei_TonalBalance.jsfx @init)
local GMEM_LCRE      = 462
local GMEM_CREST     = 461
local GMEM_WID       = 460
local GMEM_LUFS      = 790
local GMEM_VOC       = 463
local GMEM_VACT      = 464
local GMEM_LE_CORR   = 791
local GMEM_MONO_WARN = 793
local GMEM_BROAD_S   = 468
local GMEM_BROAD_B   = 469
local GMEM_BROAD_LM  = 470
local GMEM_BROAD_H   = 471
local GMEM_HB        = 456

-- Thresholds
local SUB_CREST_WARN   = 14.0
local SUB_CREST_DANGER = 20.0
local SUB_HOT_WARN     =  4.0
local SUB_COLD_WARN    = -6.0
local FULL_CREST_WARN  = 18.0
local WIDTH_NARROW     = 0.08
local WIDTH_WIDE       = 0.75
local LE_CORR_WARN     = 0.35
local LUFS_OVER        = -6.0
local LUFS_UNDER       = -24.0
local HIGH_LOW_RATIO   =  8.0

local function gmem(i)  return reaper.gmem_read(i) or 0  end
local function rule(t, sev, band, msg, act)
  table.insert(t, { severity=sev, band=band, message=msg, action=act })
end

function H.evaluate(st, TGT)
  local results = {}

  -- Engine health
  if reaper.gmem_read(GMEM_HB) == nil then
    rule(results, "warn", "global",
      "Engine not responding",
      "Mount Damei_TonalBalance.jsfx on Master bus and press Play.")
    return results
  end

  local crest_low  = gmem(GMEM_LCRE)
  local crest_full = gmem(GMEM_CREST)
  local width      = gmem(GMEM_WID)
  local lufs       = gmem(GMEM_LUFS)
  local le_corr    = gmem(GMEM_LE_CORR)
  local mono_warn  = gmem(GMEM_MONO_WARN)
  local sub_rms    = gmem(GMEM_BROAD_S)
  local high_rms   = gmem(GMEM_BROAD_H)
  local voc_bal    = gmem(GMEM_VOC)
  local voc_act    = gmem(GMEM_VACT)

  -- Rule 1: Sub-bass crest factor
  if crest_low > SUB_CREST_DANGER then
    rule(results, "warn", "sub",
      string.format("Sub-bass dynamics very wide (%.1f dB crest)", crest_low),
      "Apply 3:1 compression below 80 Hz or hard-clip at -6 dBFS.")
  elseif crest_low > SUB_CREST_WARN then
    rule(results, "warn", "sub",
      string.format("Sub-bass dynamics unconstrained (%.1f dB crest)", crest_low),
      "Apply gentle 2:1 compression below 80 Hz (attack 40ms, fast release).")
  end

  -- Rule 2: Sub energy vs genre corridor
  if TGT and st and TGT.GENRES and TGT.GENRES[st.genre] then
    local g = TGT.GENRES[st.genre]
    local sub_rel = sub_rms - (g.low_rms or 0.0)
    if sub_rel > SUB_HOT_WARN then
      rule(results, "warn", "sub",
        string.format("Excessive sub buildup: +%.1f dB above %s envelope", sub_rel, st.genre),
        "Insert high-pass at 28-35 Hz on Master or sub bus.")
    elseif sub_rel < SUB_COLD_WARN then
      rule(results, "info", "sub",
        string.format("Sub energy light: %.1f dB below %s target", math.abs(sub_rel), st.genre),
        "Boost 40-60 Hz by 2-3 dB or reduce HP filter frequency.")
    end
  elseif sub_rms > -6.0 then
    rule(results, "warn", "sub",
      string.format("Sub level very high (%.1f dB)", sub_rms),
      "High-pass at 28 Hz and compress sub bus.")
  end

  -- Rule 3: Mono warning / low-end correlation
  if mono_warn > 0 then
    rule(results, "warn", "sub",
      "Wide stereo energy below 100 Hz detected",
      "Insert Damei_MonoMaker below 100 Hz to prevent mono phase cancellation.")
  elseif le_corr < LE_CORR_WARN and le_corr > -0.1 then
    rule(results, "warn", "sub",
      string.format("Low-end L/R correlation low (%.2f)", le_corr),
      "Check for flipped polarity on sub bus or out-of-phase samples below 120 Hz.")
  end

  -- Rule 4: Full-band crest factor
  if crest_full > FULL_CREST_WARN then
    rule(results, "info", "global",
      string.format("Mix dynamics very wide (%.1f dB crest)", crest_full),
      "Apply gentle bus compression (2:1, slow attack) or parallel limiting.")
  end

  -- Rule 5: Stereo width
  if width < WIDTH_NARROW then
    rule(results, "info", "global",
      string.format("Mix is very narrow (%.0f%% width)", width * 100),
      "Widen mid-high with stereo imaging. Check for collapsed sends.")
  elseif width > WIDTH_WIDE then
    rule(results, "warn", "global",
      string.format("Mix is excessively wide (%.0f%% width)", width * 100),
      "Narrow stereo image above 8 kHz. Check mid-side balance. Verify mono compatibility.")
  end

  -- Rule 6: LUFS loudness
  if lufs > LUFS_OVER then
    rule(results, "warn", "global",
      string.format("Level too hot (%.1f LUFS-M)", lufs),
      "Reduce master fader or insert limiter ceiling at -1.0 dBTP.")
  elseif lufs < LUFS_UNDER and lufs > -60 then
    rule(results, "info", "global",
      string.format("Level low (%.1f LUFS-M)", lufs),
      "Gain-stage up. Target -18 to -12 LUFS-M for mix work.")
  end

  -- Rule 7: Spectral tilt (high vs sub)
  if sub_rms > -70 then
    local hs_diff = high_rms - sub_rms
    if hs_diff > HIGH_LOW_RATIO then
      rule(results, "info", "high",
        string.format("High-end bright vs sub (diff +%.1f dB)", hs_diff),
        "De-emphasize 8-12 kHz by 2 dB on Master bus.")
    elseif hs_diff < -HIGH_LOW_RATIO then
      rule(results, "info", "high",
        string.format("High-end dull vs sub (diff %.1f dB)", hs_diff),
        "Gently lift air 12-16 kHz. Check that high-shelf is not accidentally engaged.")
    end
  end

  -- Rule 8: Vocal balance (sidechain active)
  if voc_act > 0 then
    if voc_bal > 0.7 then
      rule(results, "warn", "mid",
        string.format("Vocals too dominant (%.0f%%)", voc_bal * 100),
        "Reduce vocal bus 1-2 dB or add 3 kHz dip on lead vocal.")
    elseif voc_bal < 0.2 then
      rule(results, "info", "mid",
        string.format("Vocals buried in balance (%.0f%%)", voc_bal * 100),
        "Lift vocal bus or cut 1-3 kHz on guitars/synths.")
    end
  end

  -- Clean bill of health
  if #results == 0 then
    rule(results, "ok", "global",
      "Tonal balance within normal range",
      "No offline heuristic concerns detected.")
  end

  return results
end

-- ImGui color map (0xRRGGBBAA)
H.SEV_COLORS = {
  warn = 0xFBBF24FF,
  info = 0x60A5FAFF,
  ok   = 0x4ADE80FF,
}

return H
