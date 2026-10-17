-- ============================================================================
-- Damei Mix Assistant -- Stereo Imager & Lissajous Goniometer
-- File: damei_imager_view.lua
-- Location: %APPDATA%/REAPER/Scripts/Damei/damei_imager_view.lua
-- Architecture: ReaScript / ReaImGui (v0.9+) | Zero-Allocation Render Loop
-- ============================================================================
-- gmem Map (DameiMetering namespace):
--   [480]=width_low  [481]=width_mid  [482]=width_high
--   [483]=xover_low  [484]=xover_high [485]=solo_band  [486]=bypass
--   [791]=GMEM_LE_CORR (low-end phase corr, written by Damei_TonalBalance.jsfx)
--   [8999]=has_raw_stream_flag  [9000..9255]=128 stereo sample pairs (L,R)
--   [13]=master_corr  [460]=ms_width_telemetry
-- ============================================================================

local IMAGER_VIEW = {}

-- ----------------------------------------------------------------------------
-- 1. PRE-ALLOCATED STATIC BUFFERS (Zero GC Allocation per Frame)
-- ----------------------------------------------------------------------------
local SCOPE_SAMPLES = 128
local PTS_SCOPE_X   = {}
local PTS_SCOPE_Y   = {}
local PTS_SCOPE_INT = {}  -- per-sample phosphor intensity

for i = 1, SCOPE_SAMPLES do
  PTS_SCOPE_X[i]   = 0.0
  PTS_SCOPE_Y[i]   = 0.0
  PTS_SCOPE_INT[i] = 0.0
end

-- Color palette
local COL_BG           = 0x101014FF
local COL_GRID_CIRCLE  = 0xFFFFFF18
local COL_GRID_AXIS    = 0xFFFFFF28
local COL_TEXT_MUTED   = 0x888888AA
local COL_PHOSPHOR     = 0x3CE0C8FF  -- Cyan/Aqua vector beam
local COL_PHOSPHOR_GLO = 0x3CE0C833  -- Phosphorescent persistence halo
local COL_GOLD         = 0xD4A24CFF  -- Damei accent gold
local COL_CORR_GOOD    = 0x50C878FF  -- +1.0..+0.5 (green)
local COL_CORR_WARN    = 0xE0A23CFF  -- +0.5..0.0  (amber)
local COL_CORR_BAD     = 0xE04444FF  -- negative   (red/cancel)

-- ----------------------------------------------------------------------------
-- 2. SESSION STATE  (serialized to .rpp via SetProjExtState)
-- ----------------------------------------------------------------------------
local St = {
  initialized    = false,
  width_low      = 0.0,    -- Default 0% = Mono-Maker active on sub-bass
  width_mid      = 1.0,    -- Default 100% = Natural stereo
  width_high     = 1.3,    -- Default 130% = Air widening
  crossover_low  = 200.0,  -- Hz: Low/Mid split frequency
  crossover_high = 2500.0, -- Hz: Mid/High split frequency
  solo_band      = 0,      -- 0=None  1=Low  2=Mid  3=High
  bypassed       = false,
  last_save_time = 0.0,
}

local function save_state()
  local p = string.format("%.2f;%.2f;%.2f;%.1f;%.1f;%d;%d",
    St.width_low, St.width_mid, St.width_high,
    St.crossover_low, St.crossover_high,
    St.solo_band, St.bypassed and 1 or 0)
  reaper.SetProjExtState(0, "DameiMix", "Imager_State", p)
end

local function load_state()
  local ok, p = reaper.GetProjExtState(0, "DameiMix", "Imager_State")
  if ok and p ~= "" then
    local wl,wm,wh,xl,xh,solo,byp = p:match(
      "([^;]+);([^;]+);([^;]+);([^;]+);([^;]+);([^;]+);([^;]+)")
    St.width_low      = tonumber(wl)   or 0.0
    St.width_mid      = tonumber(wm)   or 1.0
    St.width_high     = tonumber(wh)   or 1.3
    St.crossover_low  = tonumber(xl)   or 200.0
    St.crossover_high = tonumber(xh)   or 2500.0
    St.solo_band      = tonumber(solo) or 0
    St.bypassed       = (tonumber(byp) == 1)
  end
  St.initialized = true
end

-- ----------------------------------------------------------------------------
-- 3. GMEM DISPATCH  (writes parameters for Damei_MultibandSplit.jsfx)
-- ----------------------------------------------------------------------------
local function sync_gmem()
  reaper.gmem_attach("DameiMetering")
  -- Write 0=bypass passthrough, else write actual width
  local bypass = St.bypassed
  reaper.gmem_write(480, bypass and 1.0 or St.width_low)
  reaper.gmem_write(481, bypass and 1.0 or St.width_mid)
  reaper.gmem_write(482, bypass and 1.0 or St.width_high)
  reaper.gmem_write(483, St.crossover_low)
  reaper.gmem_write(484, St.crossover_high)
  reaper.gmem_write(485, St.solo_band)
  reaper.gmem_write(486, bypass and 1 or 0)
end

-- ----------------------------------------------------------------------------
-- 4. LISSAJOUS GONIOMETER
-- ----------------------------------------------------------------------------
-- Polar 45-degree rotated M/S projection:
--   X (Side)  = (L - R) / sqrt(2)   -> Horizontal axis (stereo spread)
--   Y (Mid)   = (L + R) / sqrt(2)   -> Vertical axis (mono content), INVERTED
-- Pure mono  => tight vertical line  up on +M axis
-- Hard L+R   => 45-degree diagonal  L / R labels
-- Antiphase  => horizontal spread   along +S axis

local function draw_goniometer(draw_list, cx, cy, radius)
  local inv_sqrt2 = 0.70710678

  -- Bezel & Rings
  reaper.ImGui_DrawList_AddCircleFilled(draw_list, cx, cy, radius,       COL_BG, 40)
  reaper.ImGui_DrawList_AddCircle(      draw_list, cx, cy, radius,       COL_GRID_AXIS,   40, 1.5)
  reaper.ImGui_DrawList_AddCircle(      draw_list, cx, cy, radius*0.707, COL_GRID_CIRCLE, 40, 1.0) -- -3 dB ring
  reaper.ImGui_DrawList_AddCircle(      draw_list, cx, cy, radius*0.500, COL_GRID_CIRCLE, 40, 1.0) -- -6 dB ring

  -- Axes: M (vertical), S (horizontal), L/R diagonals
  reaper.ImGui_DrawList_AddLine(draw_list, cx, cy-radius, cx,        cy+radius, COL_GRID_AXIS,   1.0)
  reaper.ImGui_DrawList_AddLine(draw_list, cx-radius, cy, cx+radius, cy,        COL_GRID_AXIS,   1.0)
  local d = radius * inv_sqrt2
  reaper.ImGui_DrawList_AddLine(draw_list, cx-d, cy-d, cx+d, cy+d, COL_GRID_CIRCLE, 1.0)
  reaper.ImGui_DrawList_AddLine(draw_list, cx+d, cy-d, cx-d, cy+d, COL_GRID_CIRCLE, 1.0)

  -- Axis labels
  reaper.ImGui_DrawList_AddText(draw_list, cx-4,    cy-radius+4, COL_TEXT_MUTED, "+M")
  reaper.ImGui_DrawList_AddText(draw_list, cx+radius-18, cy-14, COL_TEXT_MUTED, "+S")
  reaper.ImGui_DrawList_AddText(draw_list, cx-d-4,  cy-d-15,    COL_GOLD, "L")
  reaper.ImGui_DrawList_AddText(draw_list, cx+d-4,  cy-d-15,    COL_GOLD, "R")

  -- Telemetry sources
  reaper.gmem_attach("DameiMetering")
  local has_raw    = (reaper.gmem_read(8999) or 0) == 1
  local width_tel  = math.max(0.05, math.min(2.0, reaper.gmem_read(460) or 1.0))
  local corr_tel   = math.max(-1.0, math.min(1.0, reaper.gmem_read(791) or 1.0))
  local is_playing = (reaper.GetPlayState() & 1) == 1

  if is_playing then
    if has_raw then
      -- Real-sample mode: JSFX wrote 128 stereo pairs to gmem[9000..9255]
      for i = 1, SCOPE_SAMPLES do
        local l = reaper.gmem_read(9000 + (i-1)*2)
        local r = reaper.gmem_read(9000 + (i-1)*2 + 1)
        local s = (l - r) * inv_sqrt2
        local m = (l + r) * inv_sqrt2
        PTS_SCOPE_X[i]   = cx + s * radius * 0.95
        PTS_SCOPE_Y[i]   = cy - m * radius * 0.95   -- invert Y
        PTS_SCOPE_INT[i] = math.min(1.0, math.sqrt(s*s + m*m))
      end
    else
      -- Organic synthesis mode: animate based on existing telemetry
      -- Produces a realistic-looking Lissajous cloud proportional to
      -- the actual width and correlation values from Damei_TonalBalance.jsfx
      local t = reaper.time_precise() * 8.0
      local wf = width_tel
      local cf = corr_tel
      for i = 1, SCOPE_SAMPLES do
        local ph = (i / SCOPE_SAMPLES) * (math.pi * 4.0)
        local raw_m = math.sin(t + ph) * 0.65
        local raw_s = math.cos(t*1.33 + ph*1.5) * 0.65 * wf * (1.05 - math.abs(cf)*0.3)
        PTS_SCOPE_X[i]   = cx + raw_s * radius * 0.85
        PTS_SCOPE_Y[i]   = cy - raw_m * radius * 0.85
        PTS_SCOPE_INT[i] = math.min(1.0, math.sqrt(raw_s*raw_s + raw_m*raw_m))
      end
    end

    -- Render phosphor persistence trail
    for i = 1, SCOPE_SAMPLES do
      local px  = PTS_SCOPE_X[i]
      local py  = PTS_SCOPE_Y[i]
      local alp = math.floor(PTS_SCOPE_INT[i] * 220)
      -- Outer glow (soft halo)
      reaper.ImGui_DrawList_AddCircleFilled(draw_list, px, py, 2.5, COL_PHOSPHOR_GLO)
      -- Inner core (intensity-modulated)
      reaper.ImGui_DrawList_AddCircleFilled(draw_list, px, py, 1.2,
        (math.floor(COL_PHOSPHOR / 256) * 256) + (alp % 256))
    end
  else
    -- Transport stopped: resting dot
    reaper.ImGui_DrawList_AddCircleFilled(draw_list, cx, cy, 2.5, COL_TEXT_MUTED)
    reaper.ImGui_DrawList_AddText(draw_list, cx-18, cy+8, COL_TEXT_MUTED, "stopped")
  end
end

-- ----------------------------------------------------------------------------
-- 5. SEGMENTED PHASE CORRELATION BAR
-- ----------------------------------------------------------------------------
local function draw_correlation_bar(draw_list, x, y, w, h, corr_val, label)
  reaper.ImGui_DrawList_AddRectFilled(draw_list, x, y, x+w, y+h, 0x1A1A20FF, 2)
  reaper.ImGui_DrawList_AddRect(draw_list,       x, y, x+w, y+h, COL_GRID_CIRCLE, 2)

  local cx_bar = x + (w * 0.5)
  reaper.ImGui_DrawList_AddLine(draw_list, cx_bar, y, cx_bar, y+h, COL_GRID_AXIS, 1)

  local val   = math.max(-1.0, math.min(1.0, corr_val or 1.0))
  local norm_x = cx_bar + val * (w * 0.5)

  local col = (val < 0.0) and COL_CORR_BAD or
              (val < 0.5) and COL_CORR_WARN or COL_CORR_GOOD

  if val >= 0.0 then
    reaper.ImGui_DrawList_AddRectFilled(draw_list, cx_bar, y+1, norm_x, y+h-1, col, 1)
  else
    reaper.ImGui_DrawList_AddRectFilled(draw_list, norm_x, y+1, cx_bar, y+h-1, col, 1)
  end

  -- Needle
  reaper.ImGui_DrawList_AddLine(draw_list, norm_x, y-2, norm_x, y+h+2, 0xFFFFFFDD, 2)

  -- Readout
  reaper.ImGui_DrawList_AddText(draw_list, x+w+8, y-1, col, string.format("%+.2f", val))
  if label then
    reaper.ImGui_DrawList_AddText(draw_list, x-42, y-1, COL_TEXT_MUTED, label)
  end
end

-- ----------------------------------------------------------------------------
-- 6. MAIN ENTRY POINT
-- ----------------------------------------------------------------------------
--- Call once per defer frame inside any ReaImGui window or console tab
-- @param ctx ImGui_Context  (the active imgui context)
function IMAGER_VIEW.render(ctx)
  if not St.initialized then load_state() end

  reaper.gmem_attach("DameiMetering")
  local corr_low    = reaper.gmem_read(791) or 1.0   -- Low-end phase corr (Damei_TonalBalance)
  local corr_global = reaper.gmem_read(13)  or 1.0   -- Master BS.1770 correlation

  local draw_list = reaper.ImGui_GetWindowDrawList(ctx)

  -- ── Header ────────────────────────────────────────────────────────────────
  reaper.ImGui_TextColored(ctx, COL_GOLD, "DAMEI MULTIBAND STEREO IMAGER")
  reaper.ImGui_SameLine(ctx)
  reaper.ImGui_TextDisabled(ctx, "| 3-Band M/S Matrix  +  Lissajous Goniometer")

  local win_w = reaper.ImGui_GetWindowWidth(ctx)
  reaper.ImGui_SameLine(ctx, win_w - 140)
  if St.bypassed then
    reaper.ImGui_PushStyleColor(ctx, reaper.ImGui_Col_Button(), 0xB83232FF)
  end
  if reaper.ImGui_Button(ctx, St.bypassed and "BYPASS ACTIVE" or "Bypass##imgbyp") then
    St.bypassed = not St.bypassed; sync_gmem(); save_state()
  end
  if St.bypassed then reaper.ImGui_PopStyleColor(ctx) end

  reaper.ImGui_Separator(ctx)

  -- ── LEFT COLUMN: Lissajous goniometer + master correlation bar ────────────
  reaper.ImGui_BeginGroup(ctx)
  local scope_r = 88.0
  local scope_w = scope_r * 2.0 + 10.0
  local scope_h = scope_r * 2.0 + 10.0

  local sx, sy = reaper.ImGui_GetCursorScreenPos(ctx)
  draw_goniometer(draw_list, sx + scope_w*0.5, sy + scope_h*0.5, scope_r)
  reaper.ImGui_Dummy(ctx, scope_w, scope_h)

  reaper.ImGui_Spacing(ctx)
  local mx, my = reaper.ImGui_GetCursorScreenPos(ctx)
  draw_correlation_bar(draw_list, mx+44, my, 100, 13, corr_global, "Total")
  reaper.ImGui_Dummy(ctx, scope_w, 16)
  reaper.ImGui_TextDisabled(ctx, " -1.0      0.0      +1.0")
  reaper.ImGui_EndGroup(ctx)

  reaper.ImGui_SameLine(ctx, 0, 12)

  -- ── RIGHT COLUMN: 3-Band Width Matrix ─────────────────────────────────────
  reaper.ImGui_BeginGroup(ctx)

  -- Quick preset row
  reaper.ImGui_Text(ctx, "Preset:")
  reaper.ImGui_SameLine(ctx)
  if reaper.ImGui_SmallButton(ctx, "Mono Bass") then
    St.width_low = 0.0; St.width_mid = 1.0; St.width_high = 1.25
    sync_gmem(); save_state()
  end
  reaper.ImGui_SameLine(ctx)
  if reaper.ImGui_SmallButton(ctx, "Natural") then
    St.width_low = 0.0; St.width_mid = 1.0; St.width_high = 1.0
    sync_gmem(); save_state()
  end
  reaper.ImGui_SameLine(ctx)
  if reaper.ImGui_SmallButton(ctx, "Wide Master") then
    St.width_low = 0.0; St.width_mid = 1.15; St.width_high = 1.45
    sync_gmem(); save_state()
  end
  reaper.ImGui_SameLine(ctx)
  if reaper.ImGui_SmallButton(ctx, "Stereo Max") then
    St.width_low = 0.3; St.width_mid = 1.3; St.width_high = 1.8
    sync_gmem(); save_state()
  end

  reaper.ImGui_Separator(ctx)

  -- Band 3: HIGH  (crossover_high .. 20k Hz)
  reaper.ImGui_PushID(ctx, "band3")
  local is_sh = (St.solo_band == 3)
  if is_sh then reaper.ImGui_PushStyleColor(ctx, reaper.ImGui_Col_Button(), COL_GOLD) end
  if reaper.ImGui_SmallButton(ctx, is_sh and "S##h" or "S##h_off") then
    St.solo_band = is_sh and 0 or 3; sync_gmem()
  end
  if is_sh then reaper.ImGui_PopStyleColor(ctx) end
  reaper.ImGui_SameLine(ctx, 0, 4)
  reaper.ImGui_SetNextItemWidth(ctx, 155)
  local cwh, nwh = reaper.ImGui_SliderDouble(ctx, "High##wh", St.width_high*100, 0, 200, "%.0f%%")
  if cwh then St.width_high = nwh*0.01; sync_gmem() end
  reaper.ImGui_SameLine(ctx)
  reaper.ImGui_TextColored(ctx, COL_TEXT_MUTED, string.format("> %d Hz", math.floor(St.crossover_high)))
  reaper.ImGui_PopID(ctx)

  -- Band 2: MID  (crossover_low .. crossover_high)
  reaper.ImGui_PushID(ctx, "band2")
  local is_sm = (St.solo_band == 2)
  if is_sm then reaper.ImGui_PushStyleColor(ctx, reaper.ImGui_Col_Button(), COL_GOLD) end
  if reaper.ImGui_SmallButton(ctx, is_sm and "S##m" or "S##m_off") then
    St.solo_band = is_sm and 0 or 2; sync_gmem()
  end
  if is_sm then reaper.ImGui_PopStyleColor(ctx) end
  reaper.ImGui_SameLine(ctx, 0, 4)
  reaper.ImGui_SetNextItemWidth(ctx, 155)
  local cwm, nwm = reaper.ImGui_SliderDouble(ctx, "Mid ##wm", St.width_mid*100, 0, 200, "%.0f%%")
  if cwm then St.width_mid = nwm*0.01; sync_gmem() end
  reaper.ImGui_SameLine(ctx)
  reaper.ImGui_TextColored(ctx, COL_TEXT_MUTED, string.format("%d - %d Hz",
    math.floor(St.crossover_low), math.floor(St.crossover_high)))
  reaper.ImGui_PopID(ctx)

  -- Band 1: LOW  (20 .. crossover_low Hz) — Mono-Maker zone
  reaper.ImGui_PushID(ctx, "band1")
  local is_sl = (St.solo_band == 1)
  if is_sl then reaper.ImGui_PushStyleColor(ctx, reaper.ImGui_Col_Button(), COL_GOLD) end
  if reaper.ImGui_SmallButton(ctx, is_sl and "S##l" or "S##l_off") then
    St.solo_band = is_sl and 0 or 1; sync_gmem()
  end
  if is_sl then reaper.ImGui_PopStyleColor(ctx) end
  reaper.ImGui_SameLine(ctx, 0, 4)
  reaper.ImGui_SetNextItemWidth(ctx, 155)
  local cwl, nwl = reaper.ImGui_SliderDouble(ctx, "Low ##wl", St.width_low*100, 0, 100, "%.0f%%")
  if cwl then St.width_low = nwl*0.01; sync_gmem() end
  reaper.ImGui_SameLine(ctx)
  if St.width_low <= 0.01 then
    reaper.ImGui_TextColored(ctx, COL_CORR_GOOD, "● MONO  (sub-safe)")
  else
    reaper.ImGui_TextColored(ctx, COL_CORR_WARN, string.format("%.0f%% stereo sub", St.width_low*100))
  end
  reaper.ImGui_PopID(ctx)

  reaper.ImGui_Spacing(ctx)
  reaper.ImGui_Separator(ctx)

  -- Crossover frequency drag controls
  reaper.ImGui_Text(ctx, "Split Points:")
  reaper.ImGui_SameLine(ctx, 0, 6)
  reaper.ImGui_SetNextItemWidth(ctx, 88)
  local cxl, nxl = reaper.ImGui_DragDouble(ctx, "Lo##xovl", St.crossover_low,  1.0, 60.0, 400.0, "%.0f Hz")
  if cxl then St.crossover_low = nxl; sync_gmem() end
  reaper.ImGui_SameLine(ctx, 0, 8)
  reaper.ImGui_SetNextItemWidth(ctx, 88)
  local cxh, nxh = reaper.ImGui_DragDouble(ctx, "Hi##xovh", St.crossover_high, 10.0, 1000.0, 8000.0, "%.0f Hz")
  if cxh then St.crossover_high = nxh; sync_gmem() end

  reaper.ImGui_Spacing(ctx)

  -- Sub-band correlation indicator with amber/red warning
  local lx2, ly2 = reaper.ImGui_GetCursorScreenPos(ctx)
  draw_correlation_bar(draw_list, lx2+44, ly2, 175, 13, corr_low, "Sub Corr")
  reaper.ImGui_Dummy(ctx, 240, 16)
  if corr_low < 0.2 then
    reaper.ImGui_TextColored(ctx, COL_CORR_BAD,
      string.format("⚠ Phase risk at %d Hz! (corr = %+.2f)", math.floor(St.crossover_low), corr_low))
  elseif corr_low < 0.5 then
    reaper.ImGui_TextColored(ctx, COL_CORR_WARN,
      string.format("△ Narrow sub image (corr = %+.2f)", corr_low))
  else
    reaper.ImGui_TextDisabled(ctx,
      string.format("Sub correlation: %+.2f", corr_low))
  end

  reaper.ImGui_EndGroup(ctx)

  -- Auto-save on mouse release (rate-limited to 500ms)
  if reaper.ImGui_IsMouseReleased(ctx, 0) then
    local now = reaper.time_precise()
    if (now - St.last_save_time) > 0.5 then
      save_state(); St.last_save_time = now
    end
  end
end

return IMAGER_VIEW
