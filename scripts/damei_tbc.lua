-- ============================================================================
-- Damei Mix Assistant -- Tonal Balance Control (Passive Standalone)
-- File: damei_tbc.lua
-- Architecture: 100% Passive | Non-Destructive | Zero Chain Staging
-- ============================================================================
local reaper = reaper

if not reaper.ImGui_CreateContext then
  reaper.MB("ReaImGui is required.\nInstall via ReaPack.", "Damei TBC", 0)
  return
end

local SCRIPT_DIR = ({ reaper.get_action_context() })[2]:match("^(.*[/\\])") or ""
package.path = SCRIPT_DIR .. "?.lua;" .. package.path

if not _G.ImGui then
  _G.ImGui = setmetatable({}, { __index = function(_, k) return reaper["ImGui_" .. k] end })
end

local TARGETS, VIEW, BRIDGE = {}, {}, nil

local ok_t, m_t = pcall(dofile, SCRIPT_DIR .. "damei_tbc_targets.lua")
if ok_t and type(m_t) == "table" then TARGETS = m_t end

local ok_v, m_v = pcall(dofile, SCRIPT_DIR .. "damei_tbc_view.lua")
if ok_v and type(m_v) == "table" then VIEW = m_v end
_G.VIEW = VIEW

local ok_b, m_b = pcall(dofile, SCRIPT_DIR .. "damei_tbc_bridge.lua")
if ok_b and type(m_b) == "table" then BRIDGE = m_b end
_G.BRIDGE = BRIDGE

-- ============================================================================
-- CONSTANTS
-- ============================================================================
local GMEM_NS    = "DameiMetering"
local GMEM_HB    = 456
local GMEM_BINS  = 200
local GMEM_WID   = 460
local GMEM_CREST = 461
local GMEM_LCRE  = 462
local GMEM_LUFS  = 790
local N_BINS     = 256
local DISP_SMOOTH = 0.85

-- ImGui color constants (numeric literals - avoids Col_Button() API version issues)
local COL_BUTTON         = 21
local COL_BUTTON_HOVERED = 22
local COL_BUTTON_ACTIVE  = 23

-- ============================================================================
-- STATE
-- ============================================================================
local st = {
  engine_alive        = false,
  last_hb             = -1,
  last_hb_time        = 0.0,
  last_play_pos       = 0.0,
  view_mode           = "Broad",
  genre               = "Modern",
  corridor_scale      = 1.0,
  active_track_name   = "None",
  active_fx_idx       = -1,
  lufs                = -70.0,
  width               = 1.0,
  crest_full          = 12.0,
  crest_low           = 8.0,
  broad               = {0.0, 0.0, 0.0, 0.0},
  broad_smooth        = {0.0, 0.0, 0.0, 0.0},
  display_bins        = {},
  _verr               = false,
}
do for i = 1, N_BINS do st.display_bins[i] = -90.0 end end

-- ============================================================================
-- PERSISTENCE
-- ============================================================================
local function save_project_state()
  reaper.SetProjExtState(0, "DameiMix", "TBC_State",
    string.format("%s;%.2f;%s", st.genre, st.corridor_scale, st.view_mode))
end

local function load_project_state()
  local ok, p = reaper.GetProjExtState(0, "DameiMix", "TBC_State")
  if ok and p ~= "" then
    local g, sc, vm = p:match("([^;]+);([^;]+);([^;]+)")
    if g  then st.genre          = g                   end
    if sc then st.corridor_scale = tonumber(sc) or 1.0 end
    if vm then st.view_mode      = vm                  end
  end
end
load_project_state()

-- ============================================================================
-- GMEM HELPERS
-- ============================================================================
reaper.gmem_attach(GMEM_NS)
local function gmem_r(i)   return reaper.gmem_read(i) or 0  end
local function gmem_w(i,v) reaper.gmem_write(i, v or 0)     end
_G.gmem_r = gmem_r
_G.gmem_w = gmem_w

-- ============================================================================
-- PASSIVE DISCOVERY (never touches FX chains)
-- ============================================================================
local function find_tbc_on_track(tr)
  if not tr then return -1 end
  for f = 0, reaper.TrackFX_GetCount(tr) - 1 do
    local _, nm = reaper.TrackFX_GetFXName(tr, f, "")
    local ln = nm:lower()
    if ln:find("tonal balance", 1, true) or ln:find("tonalbalance", 1, true) then
      return f
    end
  end
  return -1
end

local function resolve_binding()
  local sel = reaper.GetSelectedTrack(0, 0)
  if sel then
    local fx = find_tbc_on_track(sel)
    if fx ~= -1 then
      local _, nm = reaper.GetSetMediaTrackInfo_String(sel, "P_NAME", "", false)
      st.active_track_name = nm ~= "" and nm or "Selected Track"
      st.active_fx_idx = fx; return true
    end
  end
  local master = reaper.GetMasterTrack(0)
  local mfx = find_tbc_on_track(master)
  if mfx ~= -1 then
    st.active_track_name = "Master Track"
    st.active_fx_idx = mfx; return true
  end
  for t = 0, reaper.CountTracks(0) - 1 do
    local tr = reaper.GetTrack(0, t)
    local fx = find_tbc_on_track(tr)
    if fx ~= -1 then
      local _, nm = reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", "", false)
      st.active_track_name = nm ~= "" and nm or string.format("Track %d", t + 1)
      st.active_fx_idx = fx; return true
    end
  end
  st.active_track_name = "None"
  st.active_fx_idx = -1
  return false
end

-- ============================================================================
-- TELEMETRY (read-only gmem)
-- ============================================================================
local function update_telemetry()
  local found = resolve_binding()
  if not found then st.engine_alive = false; return end

  reaper.gmem_attach(GMEM_NS)
  local hb         = gmem_r(GMEM_HB)
  local play_state = reaper.GetPlayState()
  local now        = reaper.time_precise()

  -- Seek auto-flush
  local cur_pos = reaper.GetPlayPosition()
  if play_state > 0 and (cur_pos - st.last_play_pos) < -0.25 then
    gmem_w(457, (gmem_r(457) + 1) % 65536)
  end
  st.last_play_pos = cur_pos

  -- Unified heartbeat: tick -> alive; playing+stalled -> dead; stopped -> keep state
  if hb ~= st.last_hb then
    st.last_hb = hb; st.last_hb_time = now; st.engine_alive = true
  elseif play_state > 0 then
    if (now - (st.last_hb_time or 0)) > 1.5 then st.engine_alive = false end
  end

  if not st.engine_alive then return end

  for i = 0, N_BINS - 1 do st.display_bins[i+1] = gmem_r(GMEM_BINS + i) end
  st.width      = gmem_r(GMEM_WID)
  st.crest_full = gmem_r(GMEM_CREST)
  st.crest_low  = gmem_r(GMEM_LCRE)
  st.lufs       = gmem_r(GMEM_LUFS)

  local bs = st.broad_smooth
  for b, idx in ipairs({468, 469, 470, 471}) do
    bs[b] = bs[b] * DISP_SMOOTH + gmem_r(idx) * (1 - DISP_SMOOTH)
    st.broad[b] = bs[b]
  end
end

-- ============================================================================
-- TOOLBAR
-- ============================================================================
local function draw_toolbar()
  local Im = _G.ImGui

  -- Status LED
  if st.engine_alive then
    Im.TextColored(ctx, 0x50C878FF, "[*] Online: " .. st.active_track_name)
  else
    Im.TextColored(ctx, 0xE05252FF, "[!] Offline -- add Damei_TonalBalance.jsfx to any track")
  end
  Im.SameLine(ctx, 0, 12)

  -- LUFS
  local lufs_str = (st.engine_alive and st.lufs > -65.0)
    and string.format("%+.1f LUFS", st.lufs) or "---.- LUFS"
  Im.TextColored(ctx, 0x40E0D0FF, lufs_str)
  Im.SameLine(ctx, 0, 8)
  Im.TextDisabled(ctx, string.format("W %.0f%%", (st.width or 1.0) * 100))
  Im.SameLine(ctx, 0, 16)

  -- View mode buttons
  if Im.Button(ctx, st.view_mode == "Broad" and "[ Broad ]" or "  Broad  ", 58, 22) then
    st.view_mode = "Broad"; save_project_state()
  end
  Im.SameLine(ctx, 0, 4)
  if Im.Button(ctx, st.view_mode == "Fine" and "[ Fine ]" or "  Fine  ", 52, 22) then
    st.view_mode = "Fine"; save_project_state()
  end
  Im.SameLine(ctx, 0, 10)

  -- Genre selector
  Im.SetNextItemWidth(ctx, 108)
  if Im.BeginCombo(ctx, "##genre", st.genre) then
    for _, g in ipairs({"Modern","Bass Heavy","Rock","Pop","EDM","Acoustic"}) do
      if Im.Selectable(ctx, g, st.genre == g) then
        st.genre = g; save_project_state()
      end
    end
    Im.EndCombo(ctx)
  end
  Im.SameLine(ctx, 0, 8)

  -- Corridor scale (SliderDouble - universally supported in ReaImGui)
  Im.SetNextItemWidth(ctx, 72)
  local sc, nc = false, st.corridor_scale
  local ok_sd = pcall(function()
    sc, nc = Im.SliderDouble(ctx, "##corr", st.corridor_scale, 0.5, 2.0, "x%.2f")
  end)
  if not ok_sd then
    -- Absolute fallback: plain text + +/- buttons
    Im.Text(ctx, string.format("x%.2f", st.corridor_scale))
  end
  if sc and nc then st.corridor_scale = nc; save_project_state() end
  Im.SameLine(ctx, 0, 16)

  -- [Learn Ref] (P1)
  local sel_tr   = reaper.GetSelectedTrack(0, 0)
  local has_item = sel_tr and reaper.GetTrackNumMediaItems(sel_tr) > 0
  if not has_item then Im.BeginDisabled(ctx) end
  if Im.Button(ctx, "[Learn Ref]", 76, 22) then
    local item = has_item and reaper.GetTrackMediaItem(sel_tr, 0)
    if item and TARGETS and TARGETS.learn_from_item then
      local curve, err = TARGETS.learn_from_item(item, "Custom Reference")
      if curve then
        st.genre = "Custom Reference"; save_project_state()
        reaper.ShowConsoleMsg("[DTB] Custom reference learned.\n")
      else
        reaper.ShowConsoleMsg("[DTB] Learn failed: " .. tostring(err) .. "\n")
      end
    end
  end
  if not has_item then Im.EndDisabled(ctx) end
  Im.SameLine(ctx, 0, 6)

  -- [EQ Bridge] (P4)
  local bridge_on = BRIDGE and BRIDGE._active_entry ~= nil
  if bridge_on then Im.PushStyleColor(ctx, COL_BUTTON, 0x1A4A2AFF) end
  if Im.Button(ctx, "[EQ Bridge]", 70, 22) then
    if BRIDGE then
      local ents = BRIDGE.scan_eq_tracks()
      if #ents > 0 then
        local cur = BRIDGE._active_entry
        local nxt = 1
        if cur then
          for i, e in ipairs(ents) do
            if e.track == cur.track and e.fx_idx == cur.fx_idx then
              nxt = (i % #ents) + 1; break
            end
          end
        end
        BRIDGE._active_entry = ents[nxt]
      else
        BRIDGE._active_entry = nil
      end
    end
  end
  if bridge_on then Im.PopStyleColor(ctx) end

  Im.Separator(ctx)
end

-- Offline placeholder canvas
local function draw_offline_canvas(aw, ah)
  local Im = _G.ImGui
  local cx = (aw - 380) * 0.5
  local cy = (ah - 44) * 0.42
  Im.SetCursorPos(ctx, cx > 0 and cx or 0, cy > 0 and cy or 0)
  Im.PushStyleColor(ctx, COL_BUTTON,         0x1A2A3AFF)
  Im.PushStyleColor(ctx, COL_BUTTON_HOVERED, 0x243550FF)
  Im.Button(ctx, "  Drop Damei_TonalBalance.jsfx on any track to begin  ", 380, 44)
  Im.PopStyleColor(ctx, 2)
  Im.SetCursorPos(ctx, cx > 0 and cx or 0, (cy > 0 and cy or 0) + 54)
  Im.TextColored(ctx, 0x5A6470FF, "No FX chain modification required.")
end

-- ============================================================================
-- MAIN DEFERRED LOOP
-- ============================================================================
ctx = reaper.ImGui_CreateContext("Damei Tonal Balance Control")
local font_ui = reaper.ImGui_CreateFont("sans-serif", 13)
reaper.ImGui_Attach(ctx, font_ui)

local function loop()
  if not reaper.ImGui_ValidatePtr(ctx, "ImGui_Context*") then
    save_project_state(); return
  end

  update_telemetry()

  if BRIDGE and BRIDGE._active_entry then
    pcall(BRIDGE.poll, reaper.time_precise())
  end

  local Im = _G.ImGui
  Im.SetNextWindowSize(ctx, 940, 490, Im.Cond_FirstUseEver())
  local vis, open = Im.Begin(ctx, "Damei Tonal Balance Control", true)

  if vis then
    local ok_font = pcall(Im.PushFont, ctx, font_ui, 0)

    local ok_tb, err_tb = pcall(draw_toolbar)
    if not ok_tb then
      Im.TextColored(ctx, 0xFF4444FF, "[DTB] toolbar error: " .. tostring(err_tb))
      if not st._tb_err then reaper.ShowConsoleMsg("[DTB] toolbar: " .. tostring(err_tb) .. "\n"); st._tb_err = true end
    else st._tb_err = false end

    local aw, ah = Im.GetContentRegionAvail(ctx)
    local x0, y0 = Im.GetCursorScreenPos(ctx)
    local dl     = Im.GetWindowDrawList(ctx)

    if st.active_fx_idx == -1 then
      draw_offline_canvas(aw, ah)
    else
      -- Always draw a background rect so we know the canvas is active
      Im.DrawList_AddRectFilled(dl, x0, y0, x0+aw, y0+ah, 0x0A0E14FF, 0)

      local tgt = TARGETS[st.genre]
      if st.view_mode == "Broad" and VIEW.draw_broad then
        local ok_v, ev = pcall(VIEW.draw_broad, ctx, Im, dl, x0, y0, aw, ah-50, st, tgt and tgt.broad or nil)
        if not ok_v then
          Im.DrawList_AddText(dl, x0+8, y0+8, 0xFF4444FF, "draw_broad err: " .. tostring(ev))
          if not st._verr then reaper.ShowConsoleMsg("[DTB] draw_broad: " .. tostring(ev) .. "\n"); st._verr=true end
        else st._verr=false end
      elseif VIEW.draw_fine then
        local ok_v, ev = pcall(VIEW.draw_fine, ctx, Im, dl, x0, y0, aw, ah, st, tgt and tgt.fine or nil, BRIDGE)
        if not ok_v then
          Im.DrawList_AddText(dl, x0+8, y0+8, 0xFF4444FF, "draw_fine err: " .. tostring(ev))
          if not st._verr then reaper.ShowConsoleMsg("[DTB] draw_fine: " .. tostring(ev) .. "\n"); st._verr=true end
        else st._verr=false end
      end
    end

    if ok_font then Im.PopFont(ctx) end
    Im.End(ctx)
  end

  if open then
    reaper.defer(loop)
  else
    save_project_state()
  end
end

reaper.atexit(save_project_state)
reaper.defer(loop)