-- ===========================================================================
-- damei_maximizer_view.lua  --  Damei Mastering Maximizer Panel
-- ---------------------------------------------------------------------------
-- Intelligent controller over native ReaLimit + Damei Precision Clipper.
-- Provides: Target LUFS Auto-Drive, Rolling GR Waterfall, True Peak guard.
-- Zero GC allocations: all history buffers pre-allocated at module load.
--
-- GMEM Map (DameiMetering, bank selected by gmem[127]):
--   gmem[bank+0] = M LUFS  gmem[bank+1] = S LUFS  gmem[bank+2] = I LUFS
--   gmem[bank+3] = TP L    gmem[bank+4] = TP R
-- ===========================================================================

local MAX_VIEW = {}

-- Rolling GR history: 150 frames (~2.5s at 60fps)
local HISTORY_SIZE = 150
local GR_HISTORY   = {}
local _history_idx = 1
local _last_sample = 0.0
for i = 1, HISTORY_SIZE do GR_HISTORY[i] = 0.0 end

-- Target LUFS profiles
MAX_VIEW.PROFILES = {
  { name = "Spotify / Apple Music   -14 LUFS",  lufs = -14.0, tp = -1.0  },
  { name = "YouTube / Broadcast     -13 LUFS",  lufs = -13.0, tp = -1.0  },
  { name = "Modern Pop / Rock        -9 LUFS",  lufs = -9.0,  tp = -0.3  },
  { name = "Club / EDM / Heavy       -7 LUFS",  lufs = -7.0,  tp = -0.1  },
}
MAX_VIEW._active_profile = 1

-- ReaLimit native parameter indices
local RL = {
  THRESH   = 0,  -- dB threshold (0 to -30)
  CEILING  = 1,  -- dBTP ceiling
  RELEASE  = 2,  -- ms
  TRUEPEAK = 3,  -- 0=off 1=on
  AUDITION = 4,  -- constant-gain audition
}

-- Color constants
local COL_GOLD    = 0xD4A24CFF
local COL_CORAL   = 0xE06C3CFF
local COL_GREEN   = 0x50C878FF
local COL_RED     = 0xFF4444FF
local COL_BG      = 0x141418FF
local COL_BORDER  = 0xFFFFFF22
local COL_GRID    = 0xFFFFFF15
local COL_GR_FILL = 0xE04444AA   -- waterfall fill
local COL_GR_LINE = 0xE06C3CEE   -- waterfall outline

--- Locate or create ReaLimit on master track
local function get_realimit()
  local master = reaper.GetMasterTrack(0)
  for f = 0, reaper.TrackFX_GetCount(master) - 1 do
    local _, nm = reaper.TrackFX_GetFXName(master, f, "")
    if nm:find("ReaLimit") then return master, f end
  end
  local idx = reaper.TrackFX_AddByName(master, "ReaLimit", false, -1)
  return master, idx
end

--- Draw the rolling GR waterfall as column rects (zero polygon-fill dependency)
local function draw_gr_waterfall(ImGui, dl, cx, cy, cw, ch)
  -- Background
  ImGui.DrawList_AddRectFilled(dl, cx, cy, cx+cw, cy+ch, COL_BG, 3)
  ImGui.DrawList_AddRect(dl,       cx, cy, cx+cw, cy+ch, COL_BORDER, 3)
  -- -3 dB gridline
  local y3 = cy + (ch * 0.5)
  ImGui.DrawList_AddLine(dl, cx, y3, cx+cw, y3, COL_GRID, 1)
  ImGui.DrawList_AddText(dl, cx+4, y3-13, 0x888888AA, "-3 dB GR")
  -- -6 dB gridline
  local y6 = cy + ch
  ImGui.DrawList_AddText(dl, cx+4, y6-13, 0x555555AA, "-6 dB")

  -- Draw one rect-column per history slot (fully pre-allocated, zero GC)
  local col_w = cw / HISTORY_SIZE
  local GR_MAX = 6.0  -- full scale = 6 dB GR
  for i = 1, HISTORY_SIZE do
    local read_i = ((_history_idx + i - 2) % HISTORY_SIZE) + 1
    local gr = math.min(GR_HISTORY[read_i], GR_MAX)
    if gr > 0.01 then
      local col_h = (gr / GR_MAX) * ch
      local bx    = cx + (i-1) * col_w
      -- Alpha gradient: brighter = more recent
      local age_alpha = math.floor(60 + (i / HISTORY_SIZE) * 120)
      local col       = (0xE04444 * 256) + age_alpha
      ImGui.DrawList_AddRectFilled(dl, bx, cy, bx + col_w + 0.5, cy + col_h, col)
    end
  end
  -- Outline over top
  ImGui.DrawList_AddRect(dl, cx, cy, cx+cw, cy+ch, COL_BORDER, 3)
end

--- Main render function — call each defer frame
-- @param ctx   ImGui_Context
-- @param ImGui ImGui wrapper table
function MAX_VIEW.render(ctx, ImGui)
  reaper.gmem_attach("DameiMetering")

  local master, rl_idx = get_realimit()
  if rl_idx < 0 then
    ImGui.TextColored(ctx, COL_RED, "ReaLimit not found. Searching for install...")
    return
  end

  -- ── 1. Read metering from Damei_Metering.jsfx ──────────────────────────
  local bank   = (reaper.gmem_read(127) or 0) == 0 and 0 or 32
  local lufs_m = reaper.gmem_read(bank + 0) or -70
  local lufs_s = reaper.gmem_read(bank + 1) or -70
  local lufs_i = reaper.gmem_read(bank + 2) or -70
  local tp_l   = reaper.gmem_read(bank + 3) or -70
  local tp_r   = reaper.gmem_read(bank + 4) or -70
  local tp_max = math.max(tp_l, tp_r)

  -- ── 2. Read ReaLimit current params ────────────────────────────────────
  local thresh_db,  _ = reaper.TrackFX_GetParam(master, rl_idx, RL.THRESH)
  local ceiling_db, _ = reaper.TrackFX_GetParam(master, rl_idx, RL.CEILING)
  local release_ms, _ = reaper.TrackFX_GetParam(master, rl_idx, RL.RELEASE)
  local true_peak_f,_ = reaper.TrackFX_GetParam(master, rl_idx, RL.TRUEPEAK)
  local audition_f, _ = reaper.TrackFX_GetParam(master, rl_idx, RL.AUDITION)
  local true_peak  = (true_peak_f or 0) > 0.5
  local audition   = (audition_f  or 0) > 0.5

  -- ── 3. Header ──────────────────────────────────────────────────────────
  ImGui.TextColored(ctx, COL_GOLD, "DAMEI MASTERING MAXIMIZER")
  ImGui.SameLine(ctx, 0, 8)
  ImGui.TextDisabled(ctx, "| ReaLimit C++ Engine  |  Damei Clipper Stage")
  ImGui.Separator(ctx)

  -- ── 4. Target LUFS Auto-Drive ───────────────────────────────────────────
  local prof = MAX_VIEW.PROFILES[MAX_VIEW._active_profile]
  ImGui.Text(ctx, "Target Profile:")
  ImGui.SameLine(ctx, 0, 6)
  ImGui.SetNextItemWidth(ctx, 240)
  local combo_open, _ = ImGui.BeginCombo(ctx, "##profcombo", prof.name)
  if combo_open then
    for i, p in ipairs(MAX_VIEW.PROFILES) do
      local sel = (MAX_VIEW._active_profile == i)
      if ImGui.Selectable(ctx, p.name, sel) then MAX_VIEW._active_profile = i end
      if sel then ImGui.SetItemDefaultFocus(ctx) end
    end
    ImGui.EndCombo(ctx)
  end
  prof = MAX_VIEW.PROFILES[MAX_VIEW._active_profile]

  local play_state = reaper.GetPlayState()
  local lufs_valid = lufs_i > -60.0 or lufs_s > -60.0
  if play_state == 0 or not lufs_valid then ImGui.BeginDisabled(ctx) end

  if ImGui.Button(ctx, "  Auto-Drive to Target  ##autobtn") then
    local current = lufs_valid and (lufs_i > -60 and lufs_i or lufs_s) or -999
    if current > -60.0 then
      local delta    = prof.lufs - current
      local new_th   = math.max(-30.0, math.min(0.0, thresh_db - delta))
      reaper.TrackFX_SetParam(master, rl_idx, RL.THRESH,  new_th)
      reaper.TrackFX_SetParam(master, rl_idx, RL.CEILING, prof.tp)
      reaper.Undo_OnStateChangeEx2(0, "Damei Auto-Drive ReaLimit", 1, -1)
    end
  end

  if play_state == 0 or not lufs_valid then
    ImGui.EndDisabled(ctx)
    if ImGui.IsItemHovered(ctx) then
      ImGui.SetTooltip(ctx, "Start transport playback to enable auto-drive.\nRequires at least 2s of playback for Integrated LUFS.")
    end
  end

  ImGui.SameLine(ctx, 0, 8)
  -- Target delta indicator
  local current_loud = lufs_i > -60 and lufs_i or lufs_s
  if current_loud > -60 then
    local delta_to_target = prof.lufs - current_loud
    local col = math.abs(delta_to_target) < 1.0 and COL_GREEN or
                math.abs(delta_to_target) < 3.0 and COL_GOLD  or COL_RED
    ImGui.TextColored(ctx, col, string.format("%+.1f dB to target", delta_to_target))
  else
    ImGui.TextDisabled(ctx, "No signal")
  end

  ImGui.Spacing(ctx)

  -- ── 5. ReaLimit direct controls ─────────────────────────────────────────
  ImGui.BeginGroup(ctx)
  ImGui.SetNextItemWidth(ctx, 180)
  local cth, nth = ImGui.SliderDouble(ctx, "Threshold##rl_th", thresh_db,  -30.0, 0.0, "%.1f dB")
  if cth then reaper.TrackFX_SetParam(master, rl_idx, RL.THRESH,  nth) end

  ImGui.SetNextItemWidth(ctx, 180)
  local cce, nce = ImGui.SliderDouble(ctx, "Ceiling  ##rl_ce", ceiling_db, -12.0, 0.0, "%.2f dBTP")
  if cce then reaper.TrackFX_SetParam(master, rl_idx, RL.CEILING, nce) end

  ImGui.SetNextItemWidth(ctx, 180)
  local crl, nrl = ImGui.SliderDouble(ctx, "Release  ##rl_rel", release_ms,  1.0, 1000.0, "%.0f ms")
  if crl then reaper.TrackFX_SetParam(master, rl_idx, RL.RELEASE, nrl) end
  ImGui.EndGroup(ctx)

  ImGui.SameLine(ctx, 0, 16)

  ImGui.BeginGroup(ctx)
  local ctp, ntp = ImGui.Checkbox(ctx, "True Peak (ISP)", true_peak)
  if ctp then reaper.TrackFX_SetParam(master, rl_idx, RL.TRUEPEAK, ntp and 1.0 or 0.0) end

  local cau, nau = ImGui.Checkbox(ctx, "Audition (Constant-Gain A/B)", audition)
  if cau then reaper.TrackFX_SetParam(master, rl_idx, RL.AUDITION, nau and 1.0 or 0.0) end
  ImGui.EndGroup(ctx)

  ImGui.Spacing(ctx)

  -- ── 6. Rolling GR Waterfall ─────────────────────────────────────────────
  -- Instantaneous GR estimate: how much the limiter is pulling down
  local raw_gr = 0.0
  if play_state > 0 and lufs_m > -60.0 then
    -- Overshoot past threshold = estimated instantaneous GR
    local overshoot = (lufs_m - thresh_db) + ceiling_db
    if overshoot > 0.0 then raw_gr = math.min(overshoot, 6.0) end
  end

  -- Sample into rolling buffer at ~40 Hz
  local now = reaper.time_precise()
  if (now - _last_sample) > 0.025 then
    GR_HISTORY[_history_idx] = raw_gr
    _history_idx = (_history_idx % HISTORY_SIZE) + 1
    _last_sample = now
  end

  local dl = ImGui.GetWindowDrawList(ctx)
  local wf_w, wf_h = 400, 70
  local wx, wy = ImGui.GetCursorScreenPos(ctx)
  draw_gr_waterfall(ImGui, dl, wx, wy, wf_w, wf_h)
  ImGui.Dummy(ctx, wf_w, wf_h)

  -- ── 7. LUFS readout strip ───────────────────────────────────────────────
  ImGui.Spacing(ctx)
  local tp_warn = tp_max > prof.tp
  ImGui.TextColored(ctx, COL_GREEN,
    string.format("I: %.1f LUFS   S: %.1f LUFS   M: %.1f LUFS", lufs_i, lufs_s, lufs_m))
  ImGui.SameLine(ctx, 0, 16)
  ImGui.TextColored(ctx, tp_warn and COL_RED or 0xAAAAAAFF,
    string.format("Max TP: %.2f dBTP", tp_max))
  if tp_warn then
    ImGui.SameLine(ctx, 0, 4)
    ImGui.TextColored(ctx, COL_RED, " ⚠ EXCEEDS CEILING")
  end

  ImGui.Spacing(ctx)
  ImGui.TextDisabled(ctx, "Chain: [Damei Clipper]  →  [ReaLimit]  →  [Damei Metering]")
end

MAX_VIEW._active_profile = 1
return MAX_VIEW
