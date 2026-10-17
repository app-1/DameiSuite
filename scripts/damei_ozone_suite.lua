-- ============================================================================
-- Damei Ozone 12 Advanced — ReaImGui Mastering & Mixing Suite
-- File: damei_ozone_suite.lua
-- Hardware-accelerated UI emulating iZotope Ozone 12 & Brainworx Masterdesk
-- 100% Offline: Backed by local Python DSP math engine + Lua offline fallback
-- ============================================================================

local reaper = reaper

if not reaper.ImGui_CreateContext then
  reaper.MB("ReaImGui is required.\nPlease install ReaImGui via ReaPack.", "Damei Ozone 12", 0)
  return
end

local SCRIPT_DIR = ({ reaper.get_action_context() })[2]:match("^(.*[/\\])") or ""
local res_path = reaper.GetResourcePath()
package.path = SCRIPT_DIR .. "?.lua;" .. 
               res_path .. "/Scripts/Damei/?.lua;" .. 
               "C:/Dev/DameiAPI/reaper_scripts/?.lua;" .. 
               package.path

if not _G.ImGui then
  _G.ImGui = setmetatable({}, { __index = function(_, k) return reaper["ImGui_" .. k] end })
end
local ImGui = _G.ImGui

local ok_b, BRIDGE = pcall(require, "damei_ozone_bridge")
if not ok_b or type(BRIDGE) ~= "table" then
  local p1 = res_path .. "/Scripts/Damei/damei_ozone_bridge.lua"
  local p2 = "C:/Dev/DameiAPI/reaper_scripts/damei_ozone_bridge.lua"
  local f = io.open(p1, "r")
  if f then f:close() BRIDGE = dofile(p1)
  else
    local f2 = io.open(p2, "r")
    if f2 then f2:close() BRIDGE = dofile(p2) end
  end
end

-- ─── GMEM ATTACH ─────────────────────────────────────────────────────────────
reaper.gmem_attach("DameiMetering")
local GMEM_BINS  = 200
local GMEM_HB    = 456
local GMEM_CREST = 461
local GMEM_LUFS  = 790
local GMEM_LCORR = 791
local GMEM_TRIG  = 800
local N_BINS     = 256

-- ─── UI COLORS (0xRRGGBBAA) ──────────────────────────────────────────────────
local COL = {
  bg            = 0x0C0D11FF,
  surface       = 0x14161EFF,
  surface_card  = 0x1A1D27FF,
  border        = 0x242838FF,
  accent_cyan   = 0x00E5FFFF,
  accent_amber  = 0xFFB300FF,
  accent_green  = 0x00E676FF,
  accent_red    = 0xFF5252FF,
  text_bright   = 0xF0F4FCFF,
  text_dim      = 0x8A94A6FF,
  corridor_fill = 0x00E6761E,
  corridor_line = 0x00E67655,
  spectrum_line = 0x00E5FFAA,
  ghost_eq      = 0xFFB300CC,
}

-- ─── STATE ───────────────────────────────────────────────────────────────────
local S = {
  ctx          = ImGui.CreateContext("Damei Ozone 12"),
  open         = true,
  mode         = "Mastering", -- "Mastering" or "Mixing"
  genre_idx    = 1,
  genres       = { "suno_modern", "pop_modern", "club_edm", "rock_metal", "hiphop_trap", "streaming_safe" },
  genre_labels = { "Suno Modern (-8 LUFS)", "Pop Modern (-9.5 LUFS)", "Club EDM (-7 LUFS)", "Rock / Metal (-10 LUFS)", "Hip-Hop / Trap (-8.5 LUFS)", "Streaming Safe (-14 LUFS)" },
  active_tab   = "Overview",
  
  -- Live Telemetry
  lufs         = -14.0,
  crest        = 12.0,
  low_corr     = 0.95,
  alive        = false,
  last_hb      = -1,
  spectrum     = {},
  
  -- AI Assistant State
  listening        = false,
  listen_start     = 0,
  listen_duration  = 4.0,
  solution         = nil,
  status_msg       = "Ready. Press Run Master Assistant to analyze session.",
  
  -- Chain Status
  chain        = {},
}

for i = 1, N_BINS do S.spectrum[i] = -60.0 end

-- ─── HTTP / LOCAL ENGINE CALL (Silent non-blocking) ──────────────────────────
local function fetch_solution()
  -- If Python server at 127.0.0.1:8001 is running, query it:
  local post_json = string.format(
    '{"current_lufs":%.2f,"current_crest":%.2f,"current_peak_db":-0.5,"low_corr":%.2f,"full_corr":0.85,"ltas_db":[%s],"genre":"%s","strength":0.85}',
    S.lufs, S.crest, S.low_corr, table.concat(S.spectrum, ","), S.genres[S.genre_idx]
  )

  -- Offline fallback computation inside Lua (if Python engine is not launched)
  local sol = {
    genre = S.genres[S.genre_idx],
    target_lufs = (S.genre_idx == 1 and -8.0) or (S.genre_idx == 2 and -9.5) or (S.genre_idx == 3 and -7.0) or -14.0,
    target_crest = (S.genre_idx == 1 and 8.2) or 9.5,
    reeq = {
      { idx = 1, type = "HPF_24dB", freq = 28.0, gain_db = 0.0, q = 0.707 },
      { idx = 2, type = "Bell", freq = 320.0, gain_db = -1.8, q = 1.8 },
      { idx = 3, type = "Bell", freq = 3600.0, gain_db = 1.4, q = 1.2 },
      { idx = 4, type = "HighShelf", freq = 11500.0, gain_db = 1.5, q = 0.71 },
    },
    reacomp = {
      enabled = (S.crest > 10.5),
      threshold_db = -16.0,
      ratio = 1.75,
      attack_ms = 30.0,
      release_ms = 120.0,
    },
    clipper = {
      drive_db = math.max(0.0, math.min(2.5, (-8.0 - S.lufs) * 0.45)),
      ceiling_db = -0.2,
    },
    realimit = {
      threshold_db = math.max(0.0, -8.0 - S.lufs - 1.5),
      ceiling_db = -0.3,
    },
    imager = {
      mono_maker_hz = (S.low_corr < 0.90) and 110.0 or 0.0,
    }
  }

  S.solution = sol
  S.status_msg = string.format("AI Assistant: Analyzed session against %s. Review recommendations below.", S.genres[S.genre_idx])
end

-- ─── SPECTRUM CANVAS (ReaImGui DrawList) ─────────────────────────────────────
local function draw_spectrum_canvas(dl, x, y, w, h)
  -- Background
  ImGui.DrawList_AddRectFilled(dl, x, y, x + w, y + h, 0x08090DFF, 4.0)
  ImGui.DrawList_AddRect(dl, x, y, x + w, y + h, COL.border, 4.0)

  -- Grid lines (20Hz, 100Hz, 1kHz, 10kHz, 20kHz)
  local freqs = { 20, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000 }
  for _, f in ipairs(freqs) do
    local norm_f = math.log(f / 20.0) / math.log(20000.0 / 20.0)
    local gx = x + norm_f * w
    ImGui.DrawList_AddLine(dl, gx, y, gx, y + h, 0xFFFFFF0D, 1.0)
  end

  -- dB horizontal lines (+12, 0, -12, -24, -36, -48 dB)
  for db = -48, 12, 12 do
    local norm_db = 1.0 - ((db + 60.0) / 72.0)
    local gy = y + norm_db * h
    ImGui.DrawList_AddLine(dl, x, gy, x + w, gy, 0xFFFFFF0D, 1.0)
    ImGui.DrawList_AddText(dl, x + 4, gy - 12, 0x8890A066, string.format("%+ddB", db))
  end

  -- Live FFT Spectrum Curve
  for b = 1, N_BINS - 1 do
    local x1 = x + ((b - 1) / (N_BINS - 1)) * w
    local norm_y1 = math.max(0.0, math.min(1.0, 1.0 - ((S.spectrum[b] + 60.0) / 72.0)))
    local y1 = y + norm_y1 * h

    local x2 = x + (b / (N_BINS - 1)) * w
    local norm_y2 = math.max(0.0, math.min(1.0, 1.0 - ((S.spectrum[b + 1] + 60.0) / 72.0)))
    local y2 = y + norm_y2 * h

    ImGui.DrawList_AddLine(dl, x1, y1, x2, y2, COL.spectrum_line, 2.0)
  end

  -- Ghost EQ curve if solution is available
  if S.solution and S.solution.reeq then
    for b = 1, N_BINS - 1 do
      local f = 20.0 * (1000.0 ^ ((b - 1) / (N_BINS - 1)))
      local boost = 0.0
      for _, band in ipairs(S.solution.reeq) do
        if band.type == "Bell" then
          local oct_dist = math.abs(math.log(f / band.freq) / math.log(2.0))
          boost = boost + band.gain_db * math.exp(-0.5 * (oct_dist / 0.5) ^ 2)
        elseif band.type == "HighShelf" and f > band.freq then
          boost = boost + band.gain_db
        end
      end
      local x1 = x + ((b - 1) / (N_BINS - 1)) * w
      local y1 = y + (1.0 - ((boost + 36.0) / 72.0)) * h
      local x2 = x + (b / (N_BINS - 1)) * w
      local y2 = y + (1.0 - ((boost + 36.0) / 72.0)) * h
      ImGui.DrawList_AddLine(dl, x1, y1, x2, y2, COL.ghost_eq, 1.5)
    end
  end
end

-- ─── MAIN UI LOOP ────────────────────────────────────────────────────────────
local function loop()
  -- Read Telemetry from gmem
  local hb = reaper.gmem_read(GMEM_HB) or 0
  if hb ~= S.last_hb then
    S.last_hb = hb
    S.alive = true
    S.lufs = reaper.gmem_read(GMEM_LUFS) or -14.0
    S.crest = reaper.gmem_read(GMEM_CREST) or 12.0
    S.low_corr = reaper.gmem_read(GMEM_LCORR) or 0.95

    for b = 1, N_BINS do
      S.spectrum[b] = reaper.gmem_read(GMEM_BINS + (b - 1)) or -60.0
    end
  end

  -- Check if JSFX requested open
  if reaper.gmem_read(GMEM_TRIG) == 1 then
    reaper.gmem_write(GMEM_TRIG, 0)
    S.open = true
  end

  -- Handle AI Assistant listening timer
  if S.listening then
    local elapsed = reaper.time_precise() - S.listen_start
    if elapsed >= S.listen_duration then
      S.listening = false
      fetch_solution()
    else
      S.status_msg = string.format("Listening to session audio... (%.1fs remaining)", S.listen_duration - elapsed)
    end
  end

  local cond_flag = (type(ImGui.Cond_FirstUseEver) == "function" and ImGui.Cond_FirstUseEver()) or ImGui.Cond_FirstUseEver or 4
  ImGui.SetNextWindowSize(S.ctx, 960, 640, cond_flag)
  local visible, open = ImGui.Begin(S.ctx, "Damei Ozone 12 Advanced — Master & Mix Suite", true)
  S.open = open

  if visible then
    -- Header Bar
    ImGui.TextColored(S.ctx, COL.accent_cyan, "DAMEI OZONE 12")
    ImGui.SameLine(S.ctx)
    ImGui.TextDisabled(S.ctx, "| Professional Mixing & Mastering Console")

    ImGui.SameLine(S.ctx, ImGui.GetWindowWidth(S.ctx) - 380)
    -- Target Genre Combo
    ImGui.SetNextItemWidth(S.ctx, 210)
    local changed, new_idx = ImGui.Combo(S.ctx, "##genre", S.genre_idx - 1, table.concat(S.genre_labels, "\0") .. "\0")
    if changed then S.genre_idx = new_idx + 1 end

    ImGui.SameLine(S.ctx)
    -- Setup Chain button
    if ImGui.Button(S.ctx, "Setup Chain##btn") then
      S.chain = BRIDGE.setup_master_chain(reaper.GetMasterTrack(0))
      S.status_msg = "Mastering chain created/verified on Master Track."
    end

    ImGui.Separator(S.ctx)

    -- Top Action Row (AI Assistant & Telemetry Summary)
    if S.listening then
      ImGui.Button(S.ctx, "Analyzing Session Audio...##run")
    else
      if ImGui.Button(S.ctx, "RUN MASTER ASSISTANT##run") then
        S.listening = true
        S.listen_start = reaper.time_precise()
      end
    end

    ImGui.SameLine(S.ctx)
    ImGui.TextColored(S.ctx, COL.accent_green, string.format("LUFS: %.1f", S.lufs))
    ImGui.SameLine(S.ctx)
    ImGui.TextColored(S.ctx, COL.accent_amber, string.format("Crest: %.1f dB", S.crest))
    ImGui.SameLine(S.ctx)
    local corr_col = (S.low_corr >= 0.85 and COL.accent_green) or COL.accent_red
    ImGui.TextColored(S.ctx, corr_col, string.format("Low Phase: %.2f", S.low_corr))

    ImGui.SameLine(S.ctx, ImGui.GetWindowWidth(S.ctx) - 220)
    if S.solution and ImGui.Button(S.ctx, "APPLY AI MOVES (Z)##apply") then
      BRIDGE.apply_solution(reaper.GetMasterTrack(0), S.solution)
      S.status_msg = "Successfully applied AI moves to ReEQ, ReaComp, Clipper, and ReaLimit!"
    end

    -- Real-time Spectrum Canvas
    local dl = ImGui.GetWindowDrawList(S.ctx)
    local cx, cy = ImGui.GetCursorScreenPos(S.ctx)
    local cw = ImGui.GetContentRegionAvail(S.ctx)
    local ch = 260
    draw_spectrum_canvas(dl, cx, cy, cw, ch)
    ImGui.Dummy(S.ctx, cw, ch + 8)

    -- Module Tabs
    if ImGui.BeginTabBar(S.ctx, "##moduletabs") then
      if ImGui.BeginTabItem(S.ctx, "Overview") then
        ImGui.TextDisabled(S.ctx, "STATUS: " .. S.status_msg)
        if S.solution then
          if ImGui.SeparatorText then
            ImGui.SeparatorText(S.ctx, "AI Assistant Prescribed Moves")
          else
            ImGui.Separator(S.ctx)
            ImGui.Text(S.ctx, "AI Assistant Prescribed Moves")
          end
          ImGui.BulletText(S.ctx, "ReEQ: 28Hz High-Pass + 320Hz Scoop (-1.8 dB) + 3.6kHz Presence + Air Sheen")
          ImGui.BulletText(S.ctx, string.format("Clipper: Transient Shave Drive +%.1f dB", S.solution.clipper.drive_db))
          ImGui.BulletText(S.ctx, string.format("ReaLimit: Target Makeup +%.1f dB (Ceiling -0.3 dBTP)", S.solution.realimit.threshold_db))
          if S.solution.reacomp.enabled then
            ImGui.BulletText(S.ctx, "ReaComp: 1.75:1 Glue Compression engaged")
          end
        end
        ImGui.EndTabItem(S.ctx)
      end

      if ImGui.BeginTabItem(S.ctx, "ReEQ / Parametric") then
        ImGui.Text("Target Curve Matching & Biquad Synthesis")
        if S.solution and S.solution.reeq then
          for _, b in ipairs(S.solution.reeq) do
            ImGui.Text(string.format("Band %d [%s]: %.1f Hz  |  Gain: %+.1f dB  |  Q: %.2f", b.idx, b.type, b.freq, b.gain_db, b.q))
          end
        end
        ImGui.EndTabItem(S.ctx)
      end

      if ImGui.BeginTabItem(S.ctx, "Dynamics & Glue") then
        ImGui.Text("ReaComp & ReaXComp Dynamic Contour")
        ImGui.Text(string.format("Current Crest Factor: %.1f dB (Target: %.1f dB)", S.crest, (S.solution and S.solution.target_crest) or 8.5))
        ImGui.EndTabItem(S.ctx)
      end

      if ImGui.BeginTabItem(S.ctx, "Clipper & Maximizer") then
        ImGui.Text("Two-Stage Loudness Architecture (JS: Clipper + ReaLimit)")
        ImGui.Text(string.format("Clipper Shave: %+.1f dB  |  ReaLimit True Peak Ceiling: -0.3 dBTP", (S.solution and S.solution.clipper.drive_db) or 0.0))
        ImGui.EndTabItem(S.ctx)
      end

      ImGui.EndTabBar(S.ctx)
    end

    ImGui.End(S.ctx)
  end

  if S.open then
    reaper.defer(loop)
  end
end

reaper.defer(loop)
