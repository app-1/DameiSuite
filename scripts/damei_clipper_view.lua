-- ===========================================================================
-- damei_clipper_view.lua  --  Damei Precision Clipper ReaImGui Front-End
-- ---------------------------------------------------------------------------
-- Renders: K-Clip style transfer curve, shaved-peak meter, controls
-- Designed for zero GC allocation (all polyline buffers pre-allocated).
-- ===========================================================================

local CLIP_VIEW = {}

-- Pre-allocated polyline buffers (NEVER reallocated per frame)
-- Polyline buffers: reaper_array required by ImGui_DrawList_AddPolyline.
-- PTS_CURVE: 64 points = 128 slots (x,y pairs). PTS_IDEAL: same.
local _c_init = {}
for i = 1, 128 do _c_init[i] = 0.0 end
local PTS_CURVE = reaper.new_array(_c_init)
local PTS_IDEAL = reaper.new_array(_c_init)
-- Color palette
local COL_GRID       = 0xFFFFFF15
local COL_BASELINE   = 0xFFFFFF33
local COL_CURVE_HARD = 0xD4A24CFF  -- Gold (hard clip)
local COL_CURVE_SOFT = 0xE06C3CFF  -- Coral (soft knee)
local COL_SHAVE      = 0xE04444FF  -- Red (shave meter)
local COL_CEILING    = 0xFF3333AA  -- Ceiling marker
local COL_BG         = 0x101014FF
local COL_BORDER     = 0xFFFFFF22
local COL_DELTA_ACTIVE = 0xB83232FF

--- Clipping kernel (mirrors JSFX math, runs in Lua for the curve display only)
local function clip_kernel(x, x_low, x_high, thresh, span)
  local ax = math.abs(x)
  local sg = x < 0 and -1.0 or 1.0
  if ax <= x_low then
    return x
  elseif ax <= x_high then
    local dx = ax - x_low
    return sg * (x_low + dx - (dx * dx) / span)
  else
    return sg * thresh
  end
end

--- Main render function
-- @param ctx     ImGui_Context
-- @param ImGui   ImGui wrapper table (local alias)
-- @param track   MediaTrack   REAPER track holding the clipper FX
-- @param fx_idx  integer      FX chain index of Damei_Clipper.jsfx
function CLIP_VIEW.render(ctx, ImGui, track, fx_idx)
  local dl = ImGui.GetWindowDrawList(ctx)

  -- ── 1. Read live parameters directly from FX chain ─────────────────────
  local drive_db,   _ = reaper.TrackFX_GetParam(track, fx_idx, 0)
  local ceiling_db, _ = reaper.TrackFX_GetParam(track, fx_idx, 1)
  local knee_pct,   _ = reaper.TrackFX_GetParam(track, fx_idx, 2)
  local os_mode_f,  _ = reaper.TrackFX_GetParam(track, fx_idx, 3)
  local auto_gain_f,_ = reaper.TrackFX_GetParam(track, fx_idx, 4)
  local delta_f,    _ = reaper.TrackFX_GetParam(track, fx_idx, 5)
  local os_mode    = math.floor(os_mode_f   + 0.5)
  local auto_gain  = auto_gain_f > 0.5
  local delta_mode = delta_f     > 0.5
  local shave_db   = reaper.gmem_read(4416) or 0.0
  local hb         = reaper.gmem_read(4417) or 0
  local alive      = (reaper.time_precise() - hb) < 0.5

  -- ── 2. Header ────────────────────────────────────────────────────────────
  ImGui.TextColored(ctx, 0xD4A24CFF, "DAMEI PRECISION CLIPPER  v2")
  ImGui.SameLine(ctx, 0, 8)
  ImGui.TextDisabled(ctx, alive and "| Engine Active" or "| Engine Offline")
  ImGui.Separator(ctx)

  -- ── 3. Drive / Ceiling / Knee controls ───────────────────────────────────
  ImGui.BeginGroup(ctx)
  ImGui.SetNextItemWidth(ctx, 170)
  local cd, nd = ImGui.SliderDouble(ctx, "Drive##drv", drive_db, -12.0, 24.0, "%+.1f dB")
  if cd then reaper.TrackFX_SetParam(track, fx_idx, 0, nd) end

  ImGui.SetNextItemWidth(ctx, 170)
  local cc, nc = ImGui.SliderDouble(ctx, "Ceiling##ceil", ceiling_db, -12.0, 0.0, "%.1f dBFS")
  if cc then reaper.TrackFX_SetParam(track, fx_idx, 1, nc) end

  ImGui.SetNextItemWidth(ctx, 170)
  local ck, nk = ImGui.SliderDouble(ctx, "Softness##knee", knee_pct, 0.0, 100.0, "%.0f%%  (0=Hard / 100=Soft)")
  if ck then reaper.TrackFX_SetParam(track, fx_idx, 2, nk) end
  ImGui.EndGroup(ctx)

  ImGui.SameLine(ctx, 0, 16)

  -- ── 4. Right column: toggles + oversampling ───────────────────────────────
  ImGui.BeginGroup(ctx)
  local cag, nag = ImGui.Checkbox(ctx, "Auto-Gain Match", auto_gain)
  if cag then reaper.TrackFX_SetParam(track, fx_idx, 4, nag and 1.0 or 0.0) end

  if delta_mode then ImGui.PushStyleColor(ctx, 0x4, COL_DELTA_ACTIVE) end
  if ImGui.Button(ctx, delta_mode and "DELTA  (listening...)" or "Delta Listen##dlt") then
    reaper.TrackFX_SetParam(track, fx_idx, 5, delta_mode and 0.0 or 1.0)
  end
  if delta_mode then ImGui.PopStyleColor(ctx, 1) end
  if ImGui.IsItemHovered(ctx) then
    ImGui.SetTooltip(ctx, "Outputs only the clipped-off material (transient spikes).\nAlt+click on any EQ node to route delta to Delta Listen.")
  end

  ImGui.SetNextItemWidth(ctx, 125)
  local os_items = "1x (Zero Latency)\00 2x (High Quality)\00 4x (Mastering)\00"
  local cos, nos = ImGui.Combo(ctx, "OS##os", os_mode, os_items)
  if cos then reaper.TrackFX_SetParam(track, fx_idx, 3, nos) end
  ImGui.EndGroup(ctx)

  ImGui.SameLine(ctx, 0, 16)

  -- ── 5. Vertical shaved-peak meter ────────────────────────────────────────
  ImGui.BeginGroup(ctx)
  ImGui.TextDisabled(ctx, "SHAVE")
  local mx, my = ImGui.GetCursorScreenPos(ctx)
  local mw, mh = 16, 80
  ImGui.DrawList_AddRectFilled(dl, mx, my, mx+mw, my+mh, COL_BG, 2)
  local norm = math.min(shave_db / 12.0, 1.0)  -- 0..12 dB range
  if norm > 0.01 then
    ImGui.DrawList_AddRectFilled(dl, mx, my, mx+mw, my+(norm*mh), COL_SHAVE, 2)
  end
  ImGui.DrawList_AddRect(dl, mx, my, mx+mw, my+mh, COL_BORDER, 2)
  ImGui.Dummy(ctx, mw, mh)
  ImGui.Text(ctx, string.format("%.1fdB", shave_db))
  ImGui.EndGroup(ctx)

  ImGui.Spacing(ctx)

  -- ── 6. Transfer curve canvas (K-Clip style) ───────────────────────────────
  local cw, ch = 300, 130
  local cx, cy = ImGui.GetCursorScreenPos(ctx)

  ImGui.DrawList_AddRectFilled(dl, cx, cy, cx+cw, cy+ch, COL_BG, 4)
  ImGui.DrawList_AddRect      (dl, cx, cy, cx+cw, cy+ch, COL_BORDER, 4)

  -- Grid lines
  ImGui.DrawList_AddLine(dl, cx, cy+ch*0.5, cx+cw, cy+ch*0.5, COL_GRID, 1)
  ImGui.DrawList_AddLine(dl, cx+cw*0.5, cy, cx+cw*0.5, cy+ch, COL_GRID, 1)
  -- 1:1 diagonal reference
  ImGui.DrawList_AddLine(dl, cx, cy+ch, cx+cw, cy, COL_BASELINE, 1)

  -- Compute actual transfer curve in real-time
  local ceil_lin = 10^(ceiling_db/20.0)
  local kv       = knee_pct * 0.01
  local xl       = ceil_lin * (1.0 - kv)
  local xh       = ceil_lin * (1.0 + kv)
  local span     = math.max(4.0 * kv * ceil_lin, 1e-9)
  local N        = 64
  local inp_max  = 1.6  -- display up to +4 dB FS input

  local idx = 1
  for pt = 1, N do
    local in_lin  = (pt-1) / (N-1) * inp_max
    local out_lin = clip_kernel(in_lin, xl, xh, ceil_lin, span)
    PTS_CURVE[idx]   = cx + (in_lin  / inp_max * cw)
    PTS_CURVE[idx+1] = cy + ch - (math.min(out_lin, inp_max) / inp_max * ch)
    idx = idx + 2
  end
  local col_curve = (knee_pct > 5) and COL_CURVE_SOFT or COL_CURVE_HARD
  ImGui.DrawList_AddPolyline(dl, PTS_CURVE, col_curve, 0, 2.0)

  -- Ceiling hairline
  local ceil_screen_y = cy + ch - (ceil_lin / inp_max * ch)
  ImGui.DrawList_AddLine(dl, cx, ceil_screen_y, cx+cw, ceil_screen_y, COL_CEILING, 1)
  ImGui.DrawList_AddText(dl, cx+4, ceil_screen_y-14, 0xFF3333FF,
    string.format("Ceil: %.1f dBFS", ceiling_db))

  -- Knee boundary indicators
  if kv > 0 then
    local xl_screen = cx + (xl / inp_max * cw)
    local xh_screen = cx + (xh / inp_max * cw)
    ImGui.DrawList_AddLine(dl, xl_screen, cy, xl_screen, cy+ch, 0xD4A24C55, 1)
    ImGui.DrawList_AddLine(dl, xh_screen, cy, xh_screen, cy+ch, 0xE06C3C55, 1)
  end

  ImGui.Dummy(ctx, cw, ch)

  -- ── 7. Chain guide ────────────────────────────────────────────────────────
  ImGui.Spacing(ctx)
  ImGui.TextDisabled(ctx, "Chain: [Drive] -> [Clipper] -> [ReaLimit] -> [Output]")
end

return CLIP_VIEW
