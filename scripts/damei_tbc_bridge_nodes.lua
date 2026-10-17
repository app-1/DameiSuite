-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
-- Damei TBC â€” EQ Node Interaction Controller
-- damei_tbc_bridge_nodes.lua
--
-- Zero-allocation interactive EQ band node loop for Fine Mode canvas.
-- Features:
--   â€¢ Hover glow + crosshair hairlines
--   â€¢ Drag: direct tracking (normal) + 4Ã— precision (Shift held)
--   â€¢ Double-click: instant gain reset to 0.0 dB with undo point
--   â€¢ Mouse wheel: Q adjustment (exponential step, 1.12Ã—/0.89Ã—)
--   â€¢ Q bandwidth guide wings (âˆ’3 dB BW from M.q_to_bw_oct)
--   â€¢ Band number label + floating HUD tooltip
--   â€¢ REAPER undo begin/end block around drag
--   â€¢ Z-index hit testing (reverse order: top band takes priority)
--
-- Arguments to draw_and_process():
--   ctx, ImGui       â€” ReaImGui context + module
--   dl               â€” ImGui DrawList (from ImGui.GetWindowDrawList)
--   cx, cy, cw, ch   â€” Canvas bounding box (screen pixels)
--   disp_min_db      â€” Canvas bottom dB value (e.g. -30)
--   disp_max_db      â€” Canvas top    dB value (e.g. +18)
--   bands            â€” BRIDGE.bands table (mutated in-place)
--   track, fx_idx    â€” REAPER FX target
--   M                â€” BRIDGE.M math module
--   dispatch         â€” BRIDGE.dispatch (set_band_frequency/gain/q)
-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

local NODES = {}

-- â”€â”€ Persistent Interaction State (one per session, no per-frame alloc) â”€
local S = {
  hovered    = nil,     -- band index under cursor (or nil)
  dragging   = nil,     -- band index being dragged (or nil)
  drag_orig_hz  = 0.0,  -- Hz at drag start (for Shift relative mode)
  drag_orig_db  = 0.0,  -- dB at drag start
  drag_start_mx = 0.0,  -- mouse X at drag start
  drag_start_my = 0.0,  -- mouse Y at drag start
  undo_open  = false,
  popup_band = nil,   -- band for right-click shape popup
}

-- â”€â”€ Visual constants â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
local R_NORMAL   = 7.0
local R_HOVER    = 9.5
local R_HIT      = 14.0   -- squared below: 196
local R_HIT_SQ   = 196.0

-- Colors (RRGGBBAA)
local C_GUIDE    = 0xFFFFFF1A   -- crosshair hairline
local C_TEXT     = 0xFFFFFFFF
local C_TOOLTIP  = 0x0D1117EF   -- tooltip background
local C_OUTLINE  = 0xFFFFFF33   -- tooltip border

-- Per-band color palette (Modern DAW, 8-color cycle)
local BAND_COLORS = {
  0xE05353FF, 0xE08A3CFF, 0xE0C83CFF, 0x50C878FF,
  0x3CA0E0FF, 0x5C6CE0FF, 0x9B59B6FF, 0xE05CA0FF,
}

local function clamp(v, lo, hi) return math.max(lo, math.min(hi, v)) end

-- â”€â”€ Band color helper â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
local function band_col(idx)
  return BAND_COLORS[((idx - 1) % #BAND_COLORS) + 1]
end

-- Apply alpha to an RRGGBBAA color
local function col_alpha(col, a)
  return (col & 0xFFFFFF00) | (clamp(a, 0, 255) & 0xFF)
end

-- â”€â”€ Draw Q bandwidth guide wings â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
local function draw_q_wings(dl, ImGui, b, bx, by, cx, cy, cw, ch, disp_min, disp_max, M, col)
  if not b.q or b.q < 0.01 then return end
  local bw = M.q_to_bw_oct(b.q)
  local f_lo = clamp(b.freq * (2.0 ^ (-bw * 0.5)), M.F_MIN, M.F_MAX)
  local f_hi = clamp(b.freq * (2.0 ^ ( bw * 0.5)), M.F_MIN, M.F_MAX)
  local x_lo = M.freq_to_x(f_lo, cx, cw, M.F_MIN, M.F_MAX)
  local x_hi = M.freq_to_x(f_hi, cx, cw, M.F_MIN, M.F_MAX)
  local wc   = col_alpha(col, 0x44)
  -- Horizontal span line at gain level
  ImGui.DrawList_AddLine(dl, x_lo, by, x_hi, by, wc, 2.0)
  -- Marker dots at -3 dB bandwidth edges
  ImGui.DrawList_AddCircle(dl, x_lo, by, 3.0, wc, 8, 1.0)
  ImGui.DrawList_AddCircle(dl, x_hi, by, 3.0, wc, 8, 1.0)
  -- Vertical tick at each edge
  ImGui.DrawList_AddLine(dl, x_lo, by - 6, x_lo, by + 6, wc, 1.0)
  ImGui.DrawList_AddLine(dl, x_hi, by - 6, x_hi, by + 6, wc, 1.0)
end

-- â”€â”€ Floating HUD tooltip â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
-- Pre-allocated scratch string (Lua strings are immutable â€” format creates
-- one string per call, which is unavoidable, but there is only one per frame).
local function draw_tooltip(dl, ImGui, b, bx, by, cx, cy, cw, ch, i)
  local hz_str
  if b.freq >= 1000.0 then
    hz_str = string.format("%.2f kHz", b.freq / 1000.0)
  else
    hz_str = string.format("%d Hz", math.floor(b.freq + 0.5))
  end
  local tip = string.format("Band %d  â€¢  %s  â€¢  %+.1f dB  â€¢  Q %.2f",
    i, hz_str, b.gain, b.q or 1.0)

  -- Offset tip right+up from node; flip if clipped
  local tx = bx + 14.0
  local ty = by - 28.0
  local tip_w = 192.0; local tip_h = 20.0
  if tx + tip_w > cx + cw then tx = bx - tip_w - 8.0 end
  if ty < cy              then ty = by + 14.0         end

  ImGui.DrawList_AddRectFilled(dl, tx-4, ty-2, tx+tip_w, ty+tip_h, C_TOOLTIP, 4.0)
  ImGui.DrawList_AddRect(dl, tx-4, ty-2, tx+tip_w, ty+tip_h, C_OUTLINE, 4.0)
  ImGui.DrawList_AddText(dl, tx, ty+1, C_TEXT, tip)
end

-- â”€â”€ Main interaction + render function â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function NODES.draw_and_process(ctx, ImGui,
  dl, cx, cy, cw, ch,
  disp_min_db, disp_max_db,
  bands, track, fx_idx, M, dispatch)

  if not bands or #bands == 0 then return end

  local cx1 = cx + cw
  local cy1 = cy + ch

  -- â”€â”€ Mouse state â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  local mx, my    = ImGui.GetMousePos(ctx)
  local m_down    = ImGui.IsMouseDown(ctx, 0)
  local m_click   = ImGui.IsMouseClicked(ctx, 0)
  local m_dbl     = ImGui.IsMouseDoubleClicked(ctx, 0)
  local vw, _     = ImGui.GetMouseWheel(ctx)   -- returns (vert, horiz)
  local is_shift  = ImGui.IsKeyDown(ctx, ImGui.Key_LeftShift())
                 or ImGui.IsKeyDown(ctx, ImGui.Key_RightShift())

  local mouse_in = (mx >= cx and mx <= cx1 and my >= cy and my <= cy1)

  -- â”€â”€ 1. Hit-testing / Hover detection â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  -- Only run when not actively dragging. Reverse iteration â†’ top node wins.
  if S.dragging == nil then
    S.hovered = nil
    if mouse_in then
      for i = #bands, 1, -1 do
        local b = bands[i]
        if b.enabled then
          local bx = M.freq_to_x(b.freq, cx, cw, M.F_MIN, M.F_MAX)
          local by = M.gain_to_y(b.gain, cy, ch, disp_min_db, disp_max_db)
          local dx = mx - bx; local dy = my - by
          if (dx*dx + dy*dy) <= R_HIT_SQ then
            S.hovered = i; break
          end
        end
      end
    end
  end

  -- â”€â”€ 2. Click intent: drag start or double-click reset â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  if S.hovered and S.dragging == nil then
    local b = bands[S.hovered]

    if m_dbl then
      -- Double-click: reset gain to 0 dB, distinct undo point
      dispatch.set_band_gain(track, fx_idx, b.param_gain, 0.0)
      b.gain = 0.0
      reaper.Undo_OnStateChangeEx2(0, "Reset EQ Band " .. S.hovered .. " Gain", 1, -1)

    elseif m_click then
      -- Start drag
      S.dragging    = S.hovered
      S.drag_start_mx = mx
      S.drag_start_my = my
      S.drag_orig_hz  = b.freq
      S.drag_orig_db  = b.gain
      if not S.undo_open then
        reaper.Undo_BeginBlock2(0)
        S.undo_open = true
      end
    end
  end

  -- â”€â”€ 3. Active drag â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  if S.dragging ~= nil then
    local b = bands[S.dragging]

    if m_down then
      local target_x, target_y

      if is_shift then
        -- Precision mode: apply 0.25Ã— damped delta from drag origin
        local DAMPEN = 0.25
        local dx = (mx - S.drag_start_mx) * DAMPEN
        local dy = (my - S.drag_start_my) * DAMPEN
        -- Compute origin screen coords
        local ox = M.freq_to_x(S.drag_orig_hz, cx, cw, M.F_MIN, M.F_MAX)
        local oy = M.gain_to_y(S.drag_orig_db, cy, ch, disp_min_db, disp_max_db)
        target_x = clamp(ox + dx, cx, cx1)
        target_y = clamp(oy + dy, cy, cy1)
      else
        -- Direct tracking: node center follows cursor exactly
        target_x = clamp(mx, cx, cx1)
        target_y = clamp(my, cy, cy1)
      end

      local new_hz = M.x_to_freq(target_x, cx, cw, M.F_MIN, M.F_MAX)
      local new_db = M.y_to_gain(target_y, cy, ch, disp_min_db, disp_max_db)
      new_hz = clamp(new_hz, b.freq_lo or M.F_MIN, b.freq_hi or M.F_MAX)
      new_db = clamp(new_db, b.gain_lo or M.G_MIN, b.gain_hi or M.G_MAX)

      -- Write to plugin (real-time, every frame while dragging)
      dispatch.set_band_frequency(track, fx_idx, b.param_freq, new_hz)
      dispatch.set_band_gain(track, fx_idx, b.param_gain, new_db)

      b.freq = new_hz
      b.gain = new_db

    else
      -- Mouse released â€” close undo block
      S.dragging = nil
      if S.undo_open then
        reaper.Undo_EndBlock2(0, "Adjust EQ Band " .. (b and b.id or "?"), -1)
        S.undo_open = false
      end
    end
  end

  -- â”€â”€ 4. Mouse wheel: Q adjustment on focused node â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  local focus = S.dragging or S.hovered
  if focus and vw ~= 0.0 then
    local b = bands[focus]
    if b.param_q then
      -- Exponential step: 1.12Ã— up, 0.89Ã— down â€” natural musical feel
      local step = (vw > 0) and 1.12 or 0.89
      local new_q = clamp(b.q * step,
        b.q_lo or M.Q_MIN, b.q_hi or M.Q_MAX)
      dispatch.set_band_q(track, fx_idx, b.param_q, new_q)
      b.q = new_q
    end
  end

  -- â”€â”€ 5. Render all nodes â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  for i, b in ipairs(bands) do
    if b.enabled then
      local bx  = M.freq_to_x(b.freq, cx, cw, M.F_MIN, M.F_MAX)
      local by  = M.gain_to_y(b.gain, cy, ch, disp_min_db, disp_max_db)
      local col = band_col(i)
      local hot = (S.hovered == i or S.dragging == i)

      -- Hover/drag decorations
      if hot then
        -- Crosshair hairlines to canvas edges
        ImGui.DrawList_AddLine(dl, bx, cy,  bx, cy1, C_GUIDE, 1.0)
        ImGui.DrawList_AddLine(dl, cx, by,  cx1, by, C_GUIDE, 1.0)
        -- Q bandwidth wings
        draw_q_wings(dl, ImGui, b, bx, by, cx, cy, cw, ch,
          disp_min_db, disp_max_db, M, col)
      end

      -- Node circle
      local r        = hot and R_HOVER or R_NORMAL
      local fill_a   = hot and 0xEE or 0xCC
      local ring_col = hot and C_TEXT or col_alpha(col, 0x99)

      ImGui.DrawList_AddCircleFilled(dl, bx, by, r, col_alpha(col, fill_a))
      ImGui.DrawList_AddCircle(dl, bx, by, r, ring_col, 16, hot and 2.0 or 1.5)

      -- Outer glow ring when dragging
      if S.dragging == i then
        ImGui.DrawList_AddCircle(dl, bx, by, r + 4.0, col_alpha(col, 0x44), 24, 3.0)
      end

      -- Band number label (centered)
      local lbl = tostring(b.id or i)
      ImGui.DrawList_AddText(dl, bx - 3.5, by - 5.5, C_TEXT, lbl)

      -- HUD tooltip
      if hot then
        draw_tooltip(dl, ImGui, b, bx, by, cx, cy, cw, ch, i)
      end
    end
  end
end


-- ── Item 3: Right-click shape popup (call inside draw_and_process after nodes loop) ──
-- This function is called within draw_and_process after the node render loop.
-- It reads S.popup_band set by the right-click handler and renders the ImGui popup.
local function draw_shape_popup(ctx, ImGui, bands, track, fx_idx, bridge, dispatch)
  if not ImGui.BeginPopup(ctx, "##dtb_band_shape") then
    if S.popup_band and not ImGui.IsPopupOpen(ctx, "##dtb_band_shape") then
      S.popup_band = nil
    end
    return
  end
  local b = S.popup_band and bands[S.popup_band]
  if b then
    ImGui.TextDisabled(ctx, string.format("Band %d — Filter Type", S.popup_band))
    ImGui.Separator(ctx)
    local shapes = {"Bell","Low Shelf","High Shelf","Low Pass","High Pass","Notch","Band Pass"}
    for si, sname in ipairs(shapes) do
      local is_cur = (b.type_idx == si - 1)
      if ImGui.MenuItem(ctx, sname, nil, is_cur) then
        local tr2, fi2
        if bridge and bridge.resolve_inst and bridge.selected_inst then
          tr2, fi2 = bridge.resolve_inst(bridge.eq_instances[bridge.selected_inst])
        end
        tr2 = tr2 or track; fi2 = fi2 or fx_idx
        if tr2 and dispatch.set_band_shape then
          dispatch.set_band_shape(tr2, fi2, b.param_type, si - 1, #shapes)
        end
        b.type_idx = si - 1; b.type_name = sname
        reaper.Undo_OnStateChangeEx2(0,
          "EQ Band " .. S.popup_band .. " Type: " .. sname, 1, -1)
      end
    end
  end
  ImGui.EndPopup(ctx)
end
-- Wire popup call into NODES module
local _orig_dap = NODES.draw_and_process
NODES.draw_and_process = function(ctx, ImGui, dl, cx, cy, cw, ch, dmin, dmax, bands, track, fi, M, dispatch, bridge)
  _orig_dap(ctx, ImGui, dl, cx, cy, cw, ch, dmin, dmax, bands, track, fi, M, dispatch, bridge)
  draw_shape_popup(ctx, ImGui, bands, track, fi, bridge, dispatch)
end


-- ============================================================================
-- Feature D: Delta Audition (Alt+Click toggles gmem[4500] = 1 while held)
-- When active, Damei_SatelliteEQ outputs processed-minus-dry (difference signal).
-- ============================================================================
local DELTA_FLAG = 4500
local _delta_active = false

function NODES.poll_delta_audition(ImGui, bridge)
  -- Check alt key (modifier 2 = Alt in ReaImGui)
  local alt_held = ImGui.IsKeyDown and ImGui.IsKeyDown(ImGui.Key_ModAlt)
  local lmb      = ImGui.IsMouseDown and ImGui.IsMouseDown(ImGui.MouseButton_Left)
  local should_delta = (alt_held and lmb)
  if should_delta ~= _delta_active then
    _delta_active = should_delta
    reaper.gmem_write(DELTA_FLAG, should_delta and 1 or 0)
  end
  return _delta_active
end

return NODES


