-- ============================================================================
-- Damei Mix Assistant -- 2D Soundstage Visual Mixer
-- File: damei_visual_mixer.lua
-- Location: %APPDATA%/REAPER/Scripts/Damei/damei_visual_mixer.lua
-- Architecture: ReaScript / ReaImGui (v0.9+) | Zero-Allocation Spatial Canvas
-- ============================================================================
-- Controls:
--   Drag puck left/right  -> D_PAN  (-1.0 .. +1.0)
--   Drag puck up/down     -> D_VOL  (+6 dB near, -48 dB far)
--   Shift + Drag          -> 4x precision fine-tune mode
--   Double-Click          -> Snap to center pan (0) + unity gain (0 dB)
-- Track puck halo pulses with RMS energy; stretches wide with stereo width.
-- Halos driven by Damei_Relay.jsfx gmem[1000..4099] when relay present;
-- falls back to Track_GetPeakInfo() for any relay-less track.
-- ============================================================================

local VISUAL_MIXER = {}

-- ----------------------------------------------------------------------------
-- 1. CONSTANTS & PALETTE
-- ----------------------------------------------------------------------------
local PUCK_R          = 14.0   -- Base puck radius
local PUCK_HIT_R      = 18.0   -- Mouse hit-box radius (slightly larger for grab comfort)
local MAX_TRACKS      = 128    -- Maximum tracks in pre-allocated puck cache

local DB_NEAR         =  6.0   -- +6 dB at canvas bottom (foreground / loud)
local DB_FAR          = -48.0  -- -48 dB at canvas top (background / distant)
local DB_SPAN         = DB_NEAR - DB_FAR   -- 54 dB full range

local COL_BG          = 0x0E0E12FF
local COL_GRID        = 0xFFFFFF12
local COL_CENTER_AXIS = 0xFFFFFF28
local COL_BORDER      = 0xFFFFFF20
local COL_WHITE       = 0xFFFFFFFF
local COL_MUTED_TEXT  = 0x888888AA
local COL_SEL_RING    = 0xFFFFFFEE
local COL_SOLO_RING   = 0xD4A24CEE
local COL_MUTE_FILL   = 0x24242AEE
local COL_DEFAULT_PUCK= 0x5C6CE0FF

-- ----------------------------------------------------------------------------
-- 2. PRE-ALLOCATED PUCK CACHE (zero GC per frame)
-- ----------------------------------------------------------------------------
local Pucks = {}
for i = 1, MAX_TRACKS do
  Pucks[i] = {
    guid       = "", track_ptr  = nil, name = "", num = 0,
    color_rgba = COL_DEFAULT_PUCK,
    screen_x   = 0.0, screen_y  = 0.0,
    pan        = 0.0, vol_db    = 0.0,
    rms_db     = -100.0, width_ratio = 1.0,
    is_solo    = false,  is_mute     = false,
    has_relay  = false,  relay_slot  = 0,
  }
end
local ActiveCount = 0

-- Drag interaction state (module-level, no allocation per frame)
local Drag = {
  idx          = nil,   -- puck index being dragged
  start_mx     = 0.0,   start_my     = 0.0,
  orig_pan     = 0.0,   orig_vol_db  = 0.0,
  undo_opened  = false,
}

-- ----------------------------------------------------------------------------
-- 3. MATH HELPERS (all pure function, zero allocation)
-- ----------------------------------------------------------------------------
local function db2lin(db)  return 10.0 ^ (db / 20.0) end
local function lin2db(v)
  return v > 0.000001 and (20.0 * math.log(v) / math.log(10.0)) or -120.0
end
local function clamp(v, lo, hi) return math.max(lo, math.min(hi, v)) end

-- Pan <-> Screen X
local function pan_to_x(pan, x0, w) return x0 + ((pan + 1.0) * 0.5) * w end
local function x_to_pan(x, x0, w)
  return clamp(((x - x0) / w) * 2.0 - 1.0, -1.0, 1.0)
end

-- Volume dB <-> Screen Y (Y=0 at top, Y=h at bottom)
local function vol_to_y(db, y0, h)
  local norm = (DB_NEAR - clamp(db, DB_FAR, DB_NEAR)) / DB_SPAN
  return y0 + norm * h
end
local function y_to_vol(y, y0, h)
  return clamp(DB_NEAR - ((y - y0) / h) * DB_SPAN, DB_FAR, DB_NEAR)
end

-- REAPER native color (packed BGR) -> RGBA 32-bit for ImGui
local function native_to_rgba(c)
  if c == 0 then return COL_DEFAULT_PUCK end
  local r, g, b = reaper.ColorFromNative(c)
  -- Lua 5.3 bitwise OR (REAPER runtime is LuaJIT/5.3+)
  return (r << 24) | (g << 16) | (b << 8) | 0xFF
end

-- Pan value -> display string
local function pan_str(pan)
  if math.abs(pan) < 0.005 then return "Center" end
  local pct = math.floor(math.abs(pan) * 100.0 + 0.5)
  return pan < 0 and (pct .. "% L") or (pct .. "% R")
end

-- ----------------------------------------------------------------------------
-- 4. TRACK SCAN & RELAY TELEMETRY SYNC
-- ----------------------------------------------------------------------------
local function refresh_pucks()
  reaper.gmem_attach("DameiMetering")
  local n = reaper.CountTracks(0)
  ActiveCount = math.min(n, MAX_TRACKS)

  for i = 1, ActiveCount do
    local tr = reaper.GetTrack(0, i - 1)
    local p  = Pucks[i]

    p.track_ptr = tr
    p.guid      = reaper.GetTrackGUID(tr)
    p.num       = i
    local _, nm = reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", "", false)
    p.name      = (nm ~= "") and nm or ("T" .. i)

    p.pan        = reaper.GetMediaTrackInfo_Value(tr, "D_PAN")
    p.vol_db     = lin2db(reaper.GetMediaTrackInfo_Value(tr, "D_VOL"))
    p.is_mute    = reaper.GetMediaTrackInfo_Value(tr, "B_MUTE") == 1
    p.is_solo    = reaper.GetMediaTrackInfo_Value(tr, "I_SOLO") > 0
    p.color_rgba = native_to_rgba(reaper.GetTrackColor(tr))

    -- Check for Damei_Relay.jsfx (reads telemetry slot from slider6)
    p.has_relay = false
    for f = 0, reaper.TrackFX_GetCount(tr) - 1 do
      local _, fx = reaper.TrackFX_GetFXName(tr, f, "")
      if fx:find("Damei_Relay") then
        p.has_relay  = true
        local slot_v, _ = reaper.TrackFX_GetParam(tr, f, 5)  -- slider6 = auto slot
        p.relay_slot = math.floor((slot_v or 0) + 0.5)
        break
      end
    end

    -- Ingest telemetry: prefer Relay gmem, fall back to peak meter
    if p.has_relay then
      local base    = 1000 + p.relay_slot * 10
      p.rms_db      = reaper.gmem_read(base + 1) or -80   -- RMS L (dB)
      p.width_ratio = reaper.gmem_read(base + 3) or 1.0   -- M/S width ratio
    else
      local peak = reaper.Track_GetPeakInfo(tr, 0)
      p.rms_db      = lin2db(peak) - 3.0
      p.width_ratio = 1.0
    end
  end
end

-- ----------------------------------------------------------------------------
-- 5. STAGE BACKDROP & GRID
-- ----------------------------------------------------------------------------
local function draw_stage(dl, x0, y0, w, h)
  local x1 = x0 + w
  local y1 = y0 + h
  local cx  = x0 + w * 0.5

  reaper.ImGui_DrawList_AddRectFilled(dl, x0, y0, x1, y1, COL_BG, 4)
  reaper.ImGui_DrawList_AddRect(      dl, x0, y0, x1, y1, COL_BORDER, 4)

  -- Horizontal depth contour lines at 5 equal dB steps
  for step = 0, 4 do
    local ay = y0 + step * (h / 4.0)
    reaper.ImGui_DrawList_AddLine(dl, x0, ay, x1, ay, COL_GRID, 1)
    local db_val = DB_FAR + ((4 - step) * (DB_SPAN / 4.0))
    reaper.ImGui_DrawList_AddText(dl, x1 - 48, ay - 14, COL_MUTED_TEXT,
      string.format("%+.0f dB", db_val))
  end

  -- Vertical pan guidelines: center + 50%L + 50%R
  reaper.ImGui_DrawList_AddLine(dl, cx,              y0, cx,              y1, COL_CENTER_AXIS, 1.5)
  reaper.ImGui_DrawList_AddLine(dl, x0 + w * 0.25,  y0, x0 + w * 0.25,  y1, COL_GRID, 1)
  reaper.ImGui_DrawList_AddLine(dl, x0 + w * 0.75,  y0, x0 + w * 0.75,  y1, COL_GRID, 1)

  -- Stage labels
  reaper.ImGui_DrawList_AddText(dl, x0 + 6,  y1 - 20, COL_MUTED_TEXT, "LEFT")
  reaper.ImGui_DrawList_AddText(dl, cx - 18, y1 - 20, COL_MUTED_TEXT, "CENTER")
  reaper.ImGui_DrawList_AddText(dl, x1 - 44, y1 - 20, COL_MUTED_TEXT, "RIGHT")
  reaper.ImGui_DrawList_AddText(dl, x0 + 6,  y0 +  6, COL_MUTED_TEXT, "DISTANT")
  reaper.ImGui_DrawList_AddText(dl, x0 + 6,  y1 - 36, COL_MUTED_TEXT, "FOREGROUND")
end

-- ----------------------------------------------------------------------------
-- 6. MAIN RENDER ENTRY POINT
-- ----------------------------------------------------------------------------
--- Call once per defer frame inside any ReaImGui window.
-- @param ctx     ImGui_Context
-- @param cw      number  Canvas width  (default 640)
-- @param ch      number  Canvas height (default 360)
function VISUAL_MIXER.render(ctx, cw, ch)
  refresh_pucks()
  cw = cw or 640.0
  ch = ch or 360.0

  local x0, y0 = reaper.ImGui_GetCursorScreenPos(ctx)
  local x1, y1 = x0 + cw, y0 + ch
  local dl = reaper.ImGui_GetWindowDrawList(ctx)

  draw_stage(dl, x0, y0, cw, ch)

  local mx, my    = reaper.ImGui_GetMousePos(ctx)
  local in_canvas = mx >= x0 and mx <= x1 and my >= y0 and my <= y1
  local m_down    = reaper.ImGui_IsMouseDown(ctx, 0)
  local m_shift   = reaper.ImGui_IsKeyDown(ctx, reaper.ImGui_Mod_Shift())
  local m_dbl     = reaper.ImGui_IsMouseDoubleClicked(ctx, 0)

  -- Pre-compute screen positions
  for i = 1, ActiveCount do
    local p = Pucks[i]
    p.screen_x = pan_to_x(p.pan,    x0, cw)
    p.screen_y = vol_to_y(p.vol_db, y0, ch)
  end

  -- ── A. HIT-TEST & DRAG INITIATION ─────────────────────────────────────────
  if not Drag.idx and in_canvas then
    for i = ActiveCount, 1, -1 do  -- reverse order = top-most puck has priority
      local p  = Pucks[i]
      local dx = mx - p.screen_x
      local dy = my - p.screen_y
      if dx*dx + dy*dy <= PUCK_HIT_R * PUCK_HIT_R then
        if m_dbl then
          -- Double-click: snap to center + unity
          reaper.SetMediaTrackInfo_Value(p.track_ptr, "D_PAN", 0.0)
          reaper.SetMediaTrackInfo_Value(p.track_ptr, "D_VOL", 1.0)
          reaper.Undo_OnStateChangeEx2(0, "Reset " .. p.name .. " Pan/Vol", 1, -1)
          break
        elseif reaper.ImGui_IsMouseClicked(ctx, 0) then
          Drag.idx        = i
          Drag.start_mx   = mx;  Drag.start_my   = my
          Drag.orig_pan   = p.pan; Drag.orig_vol_db = p.vol_db
          reaper.SetOnlyTrackSelected(p.track_ptr)
          if not Drag.undo_opened then
            reaper.Undo_BeginBlock2(0); Drag.undo_opened = true
          end
          break
        end
      end
    end
  end

  -- ── B. DRAG PROCESSING ────────────────────────────────────────────────────
  if Drag.idx then
    local p = Pucks[Drag.idx]
    if m_down then
      if m_shift then
        -- Precision mode (4x slower)
        local sens = 0.25
        p.pan    = clamp(Drag.orig_pan    + (mx - Drag.start_mx) / cw * 2.0 * sens, -1.0, 1.0)
        p.vol_db = clamp(Drag.orig_vol_db - (my - Drag.start_my) / ch * DB_SPAN * sens, DB_FAR, DB_NEAR)
      else
        -- Absolute tracking
        p.pan    = x_to_pan(mx, x0, cw)
        p.vol_db = y_to_vol(my, y0, ch)
      end
      reaper.SetMediaTrackInfo_Value(p.track_ptr, "D_PAN", p.pan)
      reaper.SetMediaTrackInfo_Value(p.track_ptr, "D_VOL", db2lin(p.vol_db))
    else
      Drag.idx = nil
      if Drag.undo_opened then
        reaper.Undo_EndBlock2(0, "Visual Mixer: Adjust Soundstage", -1)
        Drag.undo_opened = false
      end
    end
  end

  -- ── C. PUCK RENDERING ─────────────────────────────────────────────────────
  for i = 1, ActiveCount do
    local p = Pucks[i]
    local px, py = p.screen_x, p.screen_y
    local is_drag = (Drag.idx == i)

    -- Dynamic RMS energy halo (ellipse stretched by stereo width)
    if p.rms_db > -45.0 and not p.is_mute then
      local energy  = clamp((p.rms_db + 45.0) / 45.0, 0.0, 1.0)
      local hr      = PUCK_R + energy * 14.0              -- radial component
      local hw      = hr * clamp(p.width_ratio, 0.7, 1.7) -- horizontal stretch
      local h_alpha = math.floor(energy * 85)
      local hcol    = (math.floor(p.color_rgba / 256) * 256) + h_alpha

      -- Use ellipse if API available (ReaImGui 0.9.3+), else circle fallback
      local ok = pcall(reaper.ImGui_DrawList_AddEllipseFilled, dl, px, py, hw, hr, hcol, 24)
      if not ok then
        reaper.ImGui_DrawList_AddCircleFilled(dl, px, py, hr, hcol, 24)
      end
    end

    -- Puck body
    local fill = p.is_mute and COL_MUTE_FILL or p.color_rgba
    reaper.ImGui_DrawList_AddCircleFilled(dl, px, py, PUCK_R, fill, 24)

    -- Status ring
    local ring_col, ring_w = COL_BORDER, 1.5
    if is_drag or reaper.IsTrackSelected(p.track_ptr) then
      ring_col, ring_w = COL_SEL_RING, 2.5
    elseif p.is_solo then
      ring_col, ring_w = COL_SOLO_RING, 2.0
    end
    reaper.ImGui_DrawList_AddCircle(dl, px, py, PUCK_R, ring_col, 24, ring_w)

    -- Track number glyph
    reaper.ImGui_DrawList_AddText(dl, px - 3.5, py - 6.5, COL_WHITE, tostring(p.num))

    -- Floating name tag (truncate at 10 chars)
    local display_name = #p.name > 10 and p.name:sub(1, 8) .. ".." or p.name
    reaper.ImGui_DrawList_AddText(dl, px - 16, py + PUCK_R + 3, COL_MUTED_TEXT, display_name)

    -- Hover/drag HUD tooltip
    local dx, dy = mx - px, my - py
    if dx*dx + dy*dy <= PUCK_HIT_R * PUCK_HIT_R or is_drag then
      local hud = string.format("[%d] %s  •  %s  •  %+.1f dB", p.num, p.name, pan_str(p.pan), p.vol_db)
      local tx  = px + 16;  local ty = py - 22
      if tx + 180 > x1 then tx = px - 184 end
      if ty < y0       then ty = py + 14  end
      reaper.ImGui_DrawList_AddRectFilled(dl, tx-4, ty-2, tx+178, ty+18, 0x1A1A22EE, 3)
      reaper.ImGui_DrawList_AddRect(      dl, tx-4, ty-2, tx+178, ty+18, 0xFFFFFF22, 3)
      reaper.ImGui_DrawList_AddText(dl, tx, ty, COL_WHITE, hud)
    end
  end

  -- Consume canvas space in ImGui layout
  reaper.ImGui_Dummy(ctx, cw, ch)

  -- Footer hint
  reaper.ImGui_TextDisabled(ctx, "Drag=Pan/Vol   Shift+Drag=Precision   Dbl-Click=Reset")
end

return VISUAL_MIXER
