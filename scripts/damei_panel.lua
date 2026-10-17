-- ═══════════════════════════════════════════════════════════════════
-- Damei Mix Assistant — ReaImGui Panel v2
--
-- Premium dockable panel for REAPER with full ImGui widgets.
-- Communicates with DameiAPI at localhost:8001.
--
-- ReaImGui API patterns learned from ReaImGui_Demo.lua:
--   - BeginChild: EndChild goes INSIDE the if-block
--   - BeginChild flags: use ImGui.ChildFlags_Borders (number, not bool)
--   - No SetWindowFontScale — use CreateFont + PushFont
--   - Colors are 0xRRGGBBAA integers
--
-- Install: Actions → Show action list → Load → select this file
-- Dock:    Right-click the window tab → Dock in Docker
-- ═══════════════════════════════════════════════════════════════════

package.path = reaper.ImGui_GetBuiltinPath() .. '/?.lua'
local ImGui = require 'imgui' '0.10'

-- ── Config ──────────────────────────────────────────────────────────
local DAMEI_URL  = "http://127.0.0.1:8001"
local REAPER_URL = "http://127.0.0.1:8090"
local DAMEI_UI   = DAMEI_URL .. "/ui/"

-- ── Colors (Amber/Gold theme - 0xRRGGBBAA) ─────────────────────────
local COL = {
  accent      = 0xD4A24CFF,
  accent_hover= 0xE8B85CFF,
  accent_dim  = 0xD4A24C30,
  bg_dark     = 0x0A0A0CFF,
  surface     = 0x18181EFF,
  surface2    = 0x1E1E26FF,
  border      = 0x26262EFF,
  text        = 0xE8E8ECFF,
  text_dim    = 0x9898A0FF,
  text_muted  = 0x5C5C66FF,
  ok          = 0x4ADE80FF,
  warn        = 0xFBBF24FF,
  danger      = 0xF87171FF,
  info        = 0x60A5FAFF,
  drums       = 0xFF4444FF,
  bass        = 0x44AAFFFF,
  guitars     = 0x44FF88FF,
  vocals      = 0xFF44FFFF,
  keys        = 0xFFFF44FF,
  fx          = 0xFF8800FF,
  bus_col     = 0x888888FF,
  master_col  = 0xFFFFFFFF,
  unknown     = 0xAAAAAAFF,
}

-- ── State ───────────────────────────────────────────────────────────
local ctx = ImGui.CreateContext('Damei')
local state = {
  connected      = false,
  bridge_alive   = false,
  last_check     = 0,
  check_interval = 12,
  track_count    = 0,
  hot_count      = 0,
  gain_health    = 0,
  plugin_count   = 0,
  project_name   = "",
  data_age       = "—",
  tracks         = {},
  diagnosis      = nil,
  tips           = {},
  project_status = nil,
  log            = {},
}

-- ── Logging ─────────────────────────────────────────────────────────
local function log(msg, level)
  level = level or "info"
  table.insert(state.log, { time = os.date("%H:%M:%S"), msg = msg, level = level })
  if #state.log > 80 then table.remove(state.log, 1) end
end
log("Damei initialized", "ok")

-- ── HTTP (silent, file-based) ───────────────────────────────────────
local pending = {}

local function async_get(url, callback)
  local id = tostring(os.clock()):gsub("%.","") .. tostring(math.random(9999))
  local resp = reaper.GetResourcePath() .. "/damei_resp_" .. id .. ".json"
  os.remove(resp)
  reaper.ExecProcess(string.format(
    'powershell -WindowStyle Hidden -Command "try { Invoke-WebRequest -Uri \'%s\' -UseBasicParsing -OutFile \'%s\' -TimeoutSec 3 } catch {}"',
    url, resp:gsub("\\", "/")
  ), 0)
  pending[id] = { file = resp, callback = callback, started = os.time() }
end

local function async_post(url, json_body, callback)
  local id = tostring(os.clock()):gsub("%.","") .. tostring(math.random(9999))
  local resp = reaper.GetResourcePath() .. "/damei_resp_" .. id .. ".json"
  os.remove(resp)
  reaper.ExecProcess(string.format(
    'powershell -WindowStyle Hidden -Command "try { Invoke-RestMethod -Uri \'%s\' -Method Post -ContentType \'application/json\' -Body \'%s\' | ConvertTo-Json -Depth 10 | Set-Content -Path \'%s\' } catch {}"',
    url, json_body, resp:gsub("\\", "/")
  ), 0)
  pending[id] = { file = resp, callback = callback, started = os.time() }
end

local function poll_pending()
  for id, p in pairs(pending) do
    local f = io.open(p.file, "r")
    if f then
      local body = f:read("*a")
      f:close()
      if body and #body > 2 then
        os.remove(p.file)
        p.callback(body)
        pending[id] = nil
      elseif os.time() - p.started > 8 then
        os.remove(p.file)
        p.callback(nil)
        pending[id] = nil
      end
    elseif os.time() - p.started > 8 then
      p.callback(nil)
      pending[id] = nil
    end
  end
end

-- ── Health Check ────────────────────────────────────────────────────
local function check_health()
  local now = os.time()
  if now - state.last_check < state.check_interval then return end
  state.last_check = now

  -- 1. DameiAPI health
  async_get(DAMEI_URL .. "/health", function(body)
    state.connected = body ~= nil and body:find('"ok"') ~= nil
  end)

  -- 2. Bridge liveness + data age
  async_get(DAMEI_URL .. "/bridge/status", function(body)
    if body then
      state.bridge_alive = body:find('"alive"%s*:%s*true') ~= nil
      state.track_count = tonumber(body:match('"track_count"%s*:%s*(%d+)')) or state.track_count
      local ts = body:match('"timestamp"%s*:%s*"([^"]*)')
      if ts then
        state.data_age = ts:sub(1, 16):gsub("T", " ")
      end
    end
  end)

  -- 3. Project name directly from REAPER
  local _, proj_path = reaper.EnumProjects(-1)
  if proj_path and #proj_path > 0 then
    state.project_name = proj_path:match("([^/\\]+)%.RPP$") or proj_path:match("([^/\\]+)$") or proj_path
  end
end

-- ── Track Classification ────────────────────────────────────────────
local function classify_track(name)
  local n = name:lower()
  if n:find("kick") or n:find("snare") or n:find("tom") or n:find("hat")
    or n:find("cymbal") or n:find("drum") or n:find("room") then
    return "drums", COL.drums
  elseif n:find("bass") then return "bass", COL.bass
  elseif n:find("guitar") or n:find("gtr") then return "guitars", COL.guitars
  elseif n:find("vocal") or n:find("vox") then return "vocals", COL.vocals
  elseif n:find("synth") or n:find("keys") or n:find("piano") then return "keys", COL.keys
  elseif n:find("bus") or n:find("group") then return "bus", COL.bus_col
  elseif n:find("master") then return "master", COL.master_col
  else return "?", COL.unknown end
end

-- ── Theme ───────────────────────────────────────────────────────────
local function push_theme()
  ImGui.PushStyleColor(ctx, ImGui.Col_WindowBg,        COL.bg_dark)
  ImGui.PushStyleColor(ctx, ImGui.Col_ChildBg,          COL.surface)
  ImGui.PushStyleColor(ctx, ImGui.Col_PopupBg,          COL.surface)
  ImGui.PushStyleColor(ctx, ImGui.Col_Border,           COL.border)
  ImGui.PushStyleColor(ctx, ImGui.Col_Text,             COL.text)
  ImGui.PushStyleColor(ctx, ImGui.Col_TextDisabled,     COL.text_muted)
  ImGui.PushStyleColor(ctx, ImGui.Col_Button,           COL.accent_dim)
  ImGui.PushStyleColor(ctx, ImGui.Col_ButtonHovered,    COL.accent)
  ImGui.PushStyleColor(ctx, ImGui.Col_ButtonActive,     COL.accent_hover)
  ImGui.PushStyleColor(ctx, ImGui.Col_Header,           COL.accent_dim)
  ImGui.PushStyleColor(ctx, ImGui.Col_HeaderHovered,    0xD4A24C50)
  ImGui.PushStyleColor(ctx, ImGui.Col_HeaderActive,     COL.accent)
  ImGui.PushStyleColor(ctx, ImGui.Col_Tab,              COL.surface2)
  ImGui.PushStyleColor(ctx, ImGui.Col_TabSelected,      COL.accent_dim)
  ImGui.PushStyleColor(ctx, ImGui.Col_TabHovered,       0xD4A24C50)
  ImGui.PushStyleColor(ctx, ImGui.Col_FrameBg,          COL.surface2)
  ImGui.PushStyleColor(ctx, ImGui.Col_FrameBgHovered,   COL.border)
  ImGui.PushStyleColor(ctx, ImGui.Col_FrameBgActive,    COL.accent_dim)
  ImGui.PushStyleColor(ctx, ImGui.Col_Separator,        COL.border)
  ImGui.PushStyleColor(ctx, ImGui.Col_TableHeaderBg,    COL.surface2)
  ImGui.PushStyleColor(ctx, ImGui.Col_TableBorderStrong, COL.border)
  ImGui.PushStyleColor(ctx, ImGui.Col_TableBorderLight, 0x26262E80)
  ImGui.PushStyleColor(ctx, ImGui.Col_TableRowBg,       0x00000000)
  ImGui.PushStyleColor(ctx, ImGui.Col_TableRowBgAlt,    0x0A0A0C80)
  ImGui.PushStyleColor(ctx, ImGui.Col_ScrollbarBg,      0x0A0A0C80)
  ImGui.PushStyleColor(ctx, ImGui.Col_ScrollbarGrab,    COL.border)
  ImGui.PushStyleVar(ctx, ImGui.StyleVar_WindowRounding,   8)
  ImGui.PushStyleVar(ctx, ImGui.StyleVar_FrameRounding,    4)
  ImGui.PushStyleVar(ctx, ImGui.StyleVar_TabRounding,      4)
  ImGui.PushStyleVar(ctx, ImGui.StyleVar_ChildRounding,    6)
  ImGui.PushStyleVar(ctx, ImGui.StyleVar_WindowPadding,    12, 12)
  ImGui.PushStyleVar(ctx, ImGui.StyleVar_FramePadding,     8, 5)
  ImGui.PushStyleVar(ctx, ImGui.StyleVar_ItemSpacing,      8, 6)
end

local function pop_theme()
  ImGui.PopStyleVar(ctx, 7)
  ImGui.PopStyleColor(ctx, 26)
end

-- ══════════════════════════════════════════════════════════════════════
-- DASHBOARD TAB
-- ══════════════════════════════════════════════════════════════════════
local function draw_dashboard()
  -- Status block: API / Bridge / Project
  local api_col = state.connected and COL.ok or COL.danger
  local api_txt = state.connected and "DameiAPI Connected" or "DameiAPI Offline"
  ImGui.PushStyleColor(ctx, ImGui.Col_Text, api_col)
  ImGui.Bullet(ctx)
  ImGui.SameLine(ctx)
  ImGui.Text(ctx, api_txt)
  ImGui.PopStyleColor(ctx)

  local brg_col = state.bridge_alive and COL.ok or COL.warn
  local brg_txt = state.bridge_alive and "Bridge Live" or "Bridge Offline (data may be stale)"
  ImGui.PushStyleColor(ctx, ImGui.Col_Text, brg_col)
  ImGui.Bullet(ctx)
  ImGui.SameLine(ctx)
  ImGui.Text(ctx, brg_txt)
  ImGui.PopStyleColor(ctx)

  -- Project name
  if state.project_name and #state.project_name > 0 then
    ImGui.PushStyleColor(ctx, ImGui.Col_Text, COL.accent)
    ImGui.Bullet(ctx)
    ImGui.SameLine(ctx)
    ImGui.Text(ctx, state.project_name)
    ImGui.PopStyleColor(ctx)
  end

  -- Data age
  if state.data_age and state.data_age ~= "—" then
    ImGui.SameLine(ctx)
    ImGui.TextDisabled(ctx, "(" .. state.data_age .. ")")
  end

  ImGui.Separator(ctx)
  ImGui.Spacing(ctx)

  -- Metrics as a simple 2-column table
  if ImGui.BeginTable(ctx, "metrics", 2, ImGui.TableFlags_Borders) then
    ImGui.TableSetupColumn(ctx, "Metric")
    ImGui.TableSetupColumn(ctx, "Value")
    ImGui.TableHeadersRow(ctx)

    local function row(label, val, col)
      ImGui.TableNextRow(ctx)
      ImGui.TableNextColumn(ctx)
      ImGui.Text(ctx, label)
      ImGui.TableNextColumn(ctx)
      if col then ImGui.PushStyleColor(ctx, ImGui.Col_Text, col) end
      ImGui.Text(ctx, tostring(val))
      if col then ImGui.PopStyleColor(ctx) end
    end

    row("Tracks", state.track_count, COL.accent)
    row("Hot (>-6dB)", state.hot_count, state.hot_count > 0 and COL.danger or COL.ok)
    row("Gain Health", string.format("%d%%", state.gain_health),
      state.gain_health > 70 and COL.ok or state.gain_health > 40 and COL.warn or COL.danger)
    row("Plugins", state.plugin_count, COL.info)

    ImGui.EndTable(ctx)
  end

  ImGui.Spacing(ctx)

  -- Health bar
  local bar_col = COL.ok
  if state.gain_health <= 40 then bar_col = COL.danger
  elseif state.gain_health <= 70 then bar_col = COL.warn end
  ImGui.PushStyleColor(ctx, ImGui.Col_PlotHistogram, bar_col)
  ImGui.ProgressBar(ctx, state.gain_health / 100, -1, 18,
    string.format("Gain Health: %d%%", state.gain_health))
  ImGui.PopStyleColor(ctx)

  ImGui.Spacing(ctx)
  ImGui.SeparatorText(ctx, "Quick Actions")

  if ImGui.Button(ctx, "Run Diagnosis", -1, 28) then
    run_diagnosis()
  end

  if ImGui.BeginTable(ctx, "btns", 2) then
    ImGui.TableNextColumn(ctx)
    if ImGui.Button(ctx, "Gain Stage All", -1, 24) then run_gain_staging() end
    ImGui.TableNextColumn(ctx)
    if ImGui.Button(ctx, "Color Code", -1, 24) then run_color_coding() end
    ImGui.EndTable(ctx)
  end

  ImGui.Spacing(ctx)
  ImGui.SeparatorText(ctx, "Activity Log")

  -- Log as scrollable child (correct pattern from demo)
  if ImGui.BeginChild(ctx, "log_child", 0, 120, ImGui.ChildFlags_Borders) then
    for i = #state.log, math.max(1, #state.log - 30), -1 do
      local e = state.log[i]
      if e then
        local col = COL.text_dim
        if e.level == "ok" then col = COL.ok
        elseif e.level == "err" then col = COL.danger
        elseif e.level == "warn" then col = COL.warn
        elseif e.level == "accent" then col = COL.accent end
        ImGui.PushStyleColor(ctx, ImGui.Col_Text, COL.text_muted)
        ImGui.Text(ctx, e.time)
        ImGui.PopStyleColor(ctx)
        ImGui.SameLine(ctx)
        ImGui.PushStyleColor(ctx, ImGui.Col_Text, col)
        ImGui.Text(ctx, e.msg)
        ImGui.PopStyleColor(ctx)
      end
    end
    ImGui.EndChild(ctx)
  end
end

-- ══════════════════════════════════════════════════════════════════════
-- SESSION TAB
-- ══════════════════════════════════════════════════════════════════════
local function draw_session()
  if ImGui.Button(ctx, "Scan Session", 120, 24) then scan_session() end
  ImGui.SameLine(ctx)
  if ImGui.Button(ctx, "Gain Stage", 100, 24) then run_gain_staging() end
  ImGui.SameLine(ctx)
  if ImGui.Button(ctx, "Color Code", 100, 24) then run_color_coding() end

  ImGui.Spacing(ctx)
  ImGui.SeparatorText(ctx, string.format("Tracks (%d)", #state.tracks))

  if #state.tracks == 0 then
    ImGui.TextDisabled(ctx, "Click 'Scan Session' to analyze your REAPER project")
    return
  end

  local flags = ImGui.TableFlags_Borders | ImGui.TableFlags_RowBg
    | ImGui.TableFlags_Resizable | ImGui.TableFlags_ScrollY
  if ImGui.BeginTable(ctx, "tracks", 4, flags, 0, 260) then
    ImGui.TableSetupColumn(ctx, "Track", ImGui.TableColumnFlags_WidthStretch)
    ImGui.TableSetupColumn(ctx, "Type", ImGui.TableColumnFlags_WidthFixed, 70)
    ImGui.TableSetupColumn(ctx, "Level", ImGui.TableColumnFlags_WidthFixed, 65)
    ImGui.TableSetupColumn(ctx, "Status", ImGui.TableColumnFlags_WidthFixed, 40)
    ImGui.TableHeadersRow(ctx)

    for _, t in ipairs(state.tracks) do
      ImGui.TableNextRow(ctx)
      local cat, col = classify_track(t.name or "")

      ImGui.TableNextColumn(ctx)
      ImGui.PushStyleColor(ctx, ImGui.Col_Text, col)
      ImGui.Bullet(ctx)
      ImGui.PopStyleColor(ctx)
      ImGui.SameLine(ctx)
      ImGui.Text(ctx, t.name or "?")

      ImGui.TableNextColumn(ctx)
      ImGui.TextDisabled(ctx, cat)

      ImGui.TableNextColumn(ctx)
      local peak = t.peak_db
      if peak then
        local lc = COL.ok
        if peak > -6 then lc = COL.danger elseif peak < -30 then lc = COL.info end
        ImGui.PushStyleColor(ctx, ImGui.Col_Text, lc)
        ImGui.Text(ctx, string.format("%.1f", peak))
        ImGui.PopStyleColor(ctx)
      else
        ImGui.TextDisabled(ctx, "---")
      end

      ImGui.TableNextColumn(ctx)
      if peak and peak > -6 then
        ImGui.PushStyleColor(ctx, ImGui.Col_Text, COL.danger)
        ImGui.Text(ctx, "HOT")
        ImGui.PopStyleColor(ctx)
      else
        ImGui.PushStyleColor(ctx, ImGui.Col_Text, COL.ok)
        ImGui.Text(ctx, "OK")
        ImGui.PopStyleColor(ctx)
      end
    end
    ImGui.EndTable(ctx)
  end
end

-- ══════════════════════════════════════════════════════════════════════
-- DIAGNOSIS TAB
-- ══════════════════════════════════════════════════════════════════════
local function draw_diagnosis()
  if ImGui.Button(ctx, "Run Diagnosis", 130, 24) then run_diagnosis() end
  ImGui.SameLine(ctx)
  if ImGui.Button(ctx, "Refresh Tips", 100, 24) then fetch_tips() end

  ImGui.Spacing(ctx)

  if not state.diagnosis then
    ImGui.TextDisabled(ctx, "Click 'Run Diagnosis' to analyze your mix")
    return
  end

  local d = state.diagnosis

  -- Health breakdown bars
  ImGui.SeparatorText(ctx, string.format("Session Health: %d/100", d.score or 0))

  local breakdown = d.breakdown or {}
  local categories = {"gain_staging", "eq_balance", "dynamics", "stereo", "routing"}
  for _, cat in ipairs(categories) do
    local val = breakdown[cat] or 0
    local bar_col = COL.ok
    if val <= 40 then bar_col = COL.danger
    elseif val <= 70 then bar_col = COL.warn end
    ImGui.PushStyleColor(ctx, ImGui.Col_PlotHistogram, bar_col)
    ImGui.ProgressBar(ctx, val / 100, -1, 16, string.format("%s: %d%%", cat:gsub("_", " "), val))
    ImGui.PopStyleColor(ctx)
  end

  -- Engineer
  if d.engineer then
    ImGui.Spacing(ctx)
    ImGui.SeparatorText(ctx, "Coaching as: " .. d.engineer)
  end

  -- Tips
  if state.tips and #state.tips > 0 then
    ImGui.Spacing(ctx)
    ImGui.SeparatorText(ctx, string.format("Tips (%d)", #state.tips))
    for i, t in ipairs(state.tips) do
      if i > 15 then
        ImGui.TextDisabled(ctx, string.format("... and %d more", #state.tips - 15))
        break
      end
      local pc = COL.info
      if t.priority == "high" then pc = COL.danger
      elseif t.priority == "medium" then pc = COL.warn end
      ImGui.PushStyleColor(ctx, ImGui.Col_Text, pc)
      ImGui.Bullet(ctx)
      ImGui.PopStyleColor(ctx)
      ImGui.SameLine(ctx)
      ImGui.Text(ctx, string.format("[%s] %s", t.category or "?", t.current or ""))
      if t.recommendation and #t.recommendation > 0 then
        ImGui.TextDisabled(ctx, "  " .. t.recommendation)
      end
    end
  end
end

-- ══════════════════════════════════════════════════════════════════════
-- MASTERING TAB
-- ══════════════════════════════════════════════════════════════════════
local function draw_mastering()
  if ImGui.Button(ctx, "Check Project Status", 160, 24) then fetch_project_status() end
  ImGui.SameLine(ctx)
  if ImGui.Button(ctx, "Open Web Dashboard", 160, 24) then
    reaper.ExecProcess('cmd /C start "" "' .. DAMEI_UI .. '"', 0)
  end

  ImGui.Spacing(ctx)

  if state.project_status then
    local ps = state.project_status
    ImGui.SeparatorText(ctx, "Project Status")
    if ImGui.BeginTable(ctx, "proj", 2, ImGui.TableFlags_Borders) then
      local function row(l, v, col)
        ImGui.TableNextRow(ctx)
        ImGui.TableNextColumn(ctx)
        ImGui.TextDisabled(ctx, l)
        ImGui.TableNextColumn(ctx)
        if col then ImGui.PushStyleColor(ctx, ImGui.Col_Text, col) end
        ImGui.Text(ctx, tostring(v))
        if col then ImGui.PopStyleColor(ctx) end
      end
      row("Status", ps.status or "?", ps.status == "ready" and COL.ok or COL.warn)
      row("Stems Directory", ps.stems_directory or "—")
      row("Stems Found", ps.stems_found or 0, (ps.stems_found or 0) > 0 and COL.ok or COL.text_muted)
      row("References Dir", ps.references_directory or "—")
      row("References Found", ps.references_found or 0, (ps.references_found or 0) > 0 and COL.ok or COL.text_muted)
      ImGui.EndTable(ctx)
    end
  else
    ImGui.TextDisabled(ctx, "Click 'Check Project Status' to see stem & reference info")
  end

  ImGui.Spacing(ctx)
  ImGui.SeparatorText(ctx, "Mastering")
  ImGui.TextDisabled(ctx, "Reference-based mastering via Matchering")
  ImGui.TextDisabled(ctx, 'Trigger via Discord: "master with reference"')
end

-- ══════════════════════════════════════════════════════════════════════
-- API ACTIONS — wired to real DameiAPI endpoints
-- ══════════════════════════════════════════════════════════════════════

function run_diagnosis()
  log("Fetching mix health...", "accent")
  async_get(DAMEI_URL .. "/coaching/health", function(resp)
    if not resp then log("Health check failed", "err"); return end
    local d = {}
    d.score = tonumber(resp:match('"score"%s*:%s*(%d+)')) or 0
    d.engineer = resp:match('"engineer"%s*:%s*"([^"]*)"')
    d.breakdown = {
      gain_staging = tonumber(resp:match('"gain_staging"%s*:%s*(%d+)')) or 0,
      eq_balance = tonumber(resp:match('"eq_balance"%s*:%s*(%d+)')) or 0,
      dynamics = tonumber(resp:match('"dynamics"%s*:%s*(%d+)')) or 0,
      stereo = tonumber(resp:match('"stereo"%s*:%s*(%d+)')) or 0,
      routing = tonumber(resp:match('"routing"%s*:%s*(%d+)')) or 0,
    }
    local tip_count = tonumber(resp:match('"tip_count"%s*:%s*(%d+)')) or 0

    state.diagnosis = d
    state.gain_health = d.score
    log(string.format("Health: %d/100 | %s | %d tips", d.score, d.engineer or "?", tip_count), "ok")

    -- Also fetch tips
    fetch_tips()
  end)
end

function fetch_tips()
  log("Fetching tips...", "accent")
  async_get(DAMEI_URL .. "/coaching/tips", function(resp)
    if not resp then log("Tips fetch failed", "err"); return end
    state.tips = {}
    -- Parse tip entries
    for priority, category, current, recommendation in resp:gmatch(
      '"priority"%s*:%s*"([^"]*)"%s*,%s*"category"%s*:%s*"([^"]*)"%s*,%s*"element"%s*:%s*"[^"]*"%s*,%s*"current"%s*:%s*"([^"]*)"%s*,%s*"recommendation"%s*:%s*"([^"]*)"'
    ) do
      table.insert(state.tips, {
        priority = priority,
        category = category,
        current = current,
        recommendation = recommendation,
      })
    end
    log(string.format("Got %d tips", #state.tips), "ok")
  end)
end

function scan_session()
  log("Scanning session...", "accent")

  -- Try reading tracks directly from REAPER (always fresh)
  local num_tracks = reaper.CountTracks(0) or 0
  if num_tracks > 0 then
    state.tracks = {}
    for i = 0, num_tracks - 1 do
      local track = reaper.GetTrack(0, i)
      if track then
        local _, name = reaper.GetTrackName(track)
        local vol = reaper.GetMediaTrackInfo_Value(track, "D_VOL")
        local vol_db = 20 * math.log(vol, 10)
        table.insert(state.tracks, {
          name = name or ("Track " .. (i+1)),
          peak_db = math.floor(vol_db * 10 + 0.5) / 10,
        })
      end
    end
    state.track_count = #state.tracks
    local hot = 0
    for _, t in ipairs(state.tracks) do
      if t.peak_db and t.peak_db > -6 then hot = hot + 1 end
    end
    state.hot_count = hot
    log(string.format("Scanned %d tracks directly from REAPER", #state.tracks), "ok")
  else
    log("No tracks found in current project", "warn")
  end

  -- Also refresh health from DameiAPI
  async_get(DAMEI_URL .. "/coaching/health", function(resp)
    if not resp then return end
    state.gain_health = tonumber(resp:match('"score"%s*:%s*(%d+)')) or state.gain_health
  end)
end

function run_gain_staging()
  log("Gain staging (dry run)...", "accent")
  async_post(DAMEI_URL .. "/session/gainstage",
    '{"target_db": -18, "dry_run": true}',
    function(resp)
      if not resp then log("Gain staging failed", "err"); return end
      -- Parse adjustments
      state.tracks = {}
      for track, orig, new_db, delta in resp:gmatch(
        '"track"%s*:%s*"([^"]*)"%s*,%s*"original_db"%s*:%s*([%-%.%d]+)%s*,%s*"new_db"%s*:%s*([%-%.%d]+)%s*,%s*"delta"%s*:%s*([%-%.%d]+)'
      ) do
        table.insert(state.tracks, {
          name = track,
          peak_db = tonumber(orig),
          new_db = tonumber(new_db),
          delta = tonumber(delta),
        })
      end
      state.track_count = #state.tracks
      local hot = 0
      for _, t in ipairs(state.tracks) do
        if t.peak_db and t.peak_db > -6 then hot = hot + 1 end
      end
      state.hot_count = hot
      log(string.format("Gain staged %d tracks (dry run)", #state.tracks), "ok")
    end)
end

function run_color_coding()
  log("Color coding not yet wired to API", "warn")
end

function fetch_project_status()
  log("Checking project status...", "accent")
  async_get(DAMEI_URL .. "/coaching/project-status", function(resp)
    if not resp then log("Project status failed", "err"); return end
    state.project_status = {
      status = resp:match('"status"%s*:%s*"([^"]*)"'),
      stems_directory = resp:match('"stems_directory"%s*:%s*"([^"]*)"'),
      stems_found = tonumber(resp:match('"stems_found"%s*:%s*(%d+)')) or 0,
      references_directory = resp:match('"references_directory"%s*:%s*"([^"]*)"'),
      references_found = tonumber(resp:match('"references_found"%s*:%s*(%d+)')) or 0,
    }
    log(string.format("Project: %s | %d stems, %d refs",
      state.project_status.status or "?",
      state.project_status.stems_found,
      state.project_status.references_found), "ok")
  end)
end

-- ══════════════════════════════════════════════════════════════════════
-- MAIN LOOP
-- ══════════════════════════════════════════════════════════════════════

local function loop()
  poll_pending()
  check_health()
  push_theme()

  local visible, open = ImGui.Begin(ctx, "Damei Mix Assistant", true, ImGui.WindowFlags_NoCollapse)

  if visible then
    if ImGui.BeginTabBar(ctx, "tabs") then
      if ImGui.BeginTabItem(ctx, "Dashboard") then
        draw_dashboard()
        ImGui.EndTabItem(ctx)
      end
      if ImGui.BeginTabItem(ctx, "Session") then
        draw_session()
        ImGui.EndTabItem(ctx)
      end
      if ImGui.BeginTabItem(ctx, "Diagnosis") then
        draw_diagnosis()
        ImGui.EndTabItem(ctx)
      end
      if ImGui.BeginTabItem(ctx, "Mastering") then
        draw_mastering()
        ImGui.EndTabItem(ctx)
      end
      ImGui.EndTabBar(ctx)
    end
    ImGui.End(ctx)
  end

  pop_theme()

  if open then
    reaper.defer(loop)
  end
end

-- Auto-fetch health on startup + read project name directly
reaper.defer(function()
  -- Get project name directly from REAPER (we're running inside it!)
  local _, proj_name = reaper.EnumProjects(-1)
  if proj_name and #proj_name > 0 then
    state.project_name = proj_name:match("([^/\\]+)%.RPP$") or proj_name:match("([^/\\]+)$") or proj_name
  end
  run_diagnosis()
  scan_session()
  reaper.defer(loop)
end)
