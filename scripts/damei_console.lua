
-- === Tier 3: Visual Mixer & BassFocus Panels ===
local _vm2_loaded, VM2_MOD = false, nil
local function ensure_vm2()
  if not _vm2_loaded then
    local ok, m = pcall(require, 'damei_visual_mixer')
    if ok then VM2_MOD = m end; _vm2_loaded = true
  end
  return VM2_MOD
end
function draw_visual_mixer_panel(ctx, w, h)
  local vm = ensure_vm2()
  if not vm then reaper.ImGui_TextDisabled(ctx, 'damei_visual_mixer.lua not found'); return end
  vm.render(ctx, w, h)
end


-- === Damei A/B Gain Match Integration ===
local _ab_loaded = false
local AB_MATCH   = nil
local function ensure_ab()
  if not _ab_loaded then
    local ok, m = pcall(require, 'damei_ab_gainmatch')
    if ok then AB_MATCH = m end
    _ab_loaded = true
  end
  return AB_MATCH
end
function draw_ab_panel(ctx)
  local ab = ensure_ab()
  if not ab then reaper.ImGui_TextDisabled(ctx, 'damei_ab_gainmatch.lua not found'); return end
  ab.render(ctx)
end

-- ═════════════════════════════════════════════════════════════════════

-- === Damei Stereo Imager Integration ===
local _imager_loaded = false
local IMAGER_VIEW = nil
local function ensure_imager()
  if not _imager_loaded then
    local ok, m = pcall(require, 'damei_imager_view')
    if ok then IMAGER_VIEW = m end
    _imager_loaded = true
  end
  return IMAGER_VIEW
end
function draw_imager_panel(ctx)
  local iv = ensure_imager()
  if not iv then reaper.ImGui_TextDisabled(ctx, 'damei_imager_view.lua not found'); return end
  iv.render(ctx)
end

-- ═════════════════════════════════════════════════════════════════════

-- === Damei Precision Clipper Integration ===
local _clip_view_loaded = false
local CLIP_VIEW = nil
local function ensure_clip_view()
  if not _clip_view_loaded then
    local ok, m = pcall(require, 'damei_clipper_view')
    if ok then CLIP_VIEW = m end
    _clip_view_loaded = true
  end
  return CLIP_VIEW
end
function draw_master_clipper(ctx, ImGui)
  local cv = ensure_clip_view()
  if not cv then ImGui.TextDisabled(ctx, 'damei_clipper_view.lua not found'); return end
  if ImGui.CollapsingHeader(ctx, 'Master Peak Shaver (Clipper)##cliphdr') then
    local master_tr = reaper.GetMasterTrack(0)
    local clip_idx  = reaper.TrackFX_AddByName(master_tr, 'Damei_Clipper.jsfx', false, 0)
    if clip_idx >= 0 then
      cv.render(ctx, ImGui, master_tr, clip_idx)
    else
      if ImGui.Button(ctx, 'Insert Damei Clipper on Master') then
        reaper.TrackFX_AddByName(master_tr, 'Damei_Clipper.jsfx', false, -1)
      end
      ImGui.TextDisabled(ctx, 'Insert before ReaLimit in the FX chain.')
    end
  end
end

-- ═════════════════════════════════════════════════════════════════════
-- Damei Mix Console v4 — Orchestrator
--
-- This is the main entry point. It loads the MVC modules and runs
-- the lifecycle loop. All business logic is in the controller,
-- all rendering in the view, all state in the model.
--
-- Architecture: Model (state) → Controller (logic) → View (ImGui)
--
-- Install: Actions → Show action list → Load → select this file
-- Requires: ReaImGui, Damei_Metering.jsfx on Master Bus
-- ═════════════════════════════════════════════════════════════════════

-- ── DEPENDENCY CHECK ────────────────────────────────────────────────
if not reaper.ImGui_GetBuiltinPath then
  reaper.MB("ReaImGui is required.\nInstall via ReaPack: Extensions > ReaPack > Browse packages > ReaImGui", "Damei", 0)
  return
end

package.path = reaper.ImGui_GetBuiltinPath() .. '/?.lua'
local ImGui = require 'imgui' '0.10'

-- ── MODULE LOADING ──────────────────────────────────────────────────
local SCRIPT_DIR = reaper.GetResourcePath() .. "/Scripts/Damei"
local M    = dofile(SCRIPT_DIR .. "/damei_model.lua")
local V    = dofile(SCRIPT_DIR .. "/damei_view.lua")
local ctrl = dofile(SCRIPT_DIR .. "/damei_controller.lua")

-- ── LOCAL ALIASES ───────────────────────────────────────────────────
local st  = M.st
local log = M.log
local sanitize_path = M.sanitize_path
local has_sws = reaper.CF_GetClipboard ~= nil

-- Config aliases (may be mutated by load_global_config)
local DAMEI_URL        = M.DAMEI_URL
local HERMES_MCP_URL   = M.HERMES_MCP_URL
local HERMES_MCP_SCRIPT= M.HERMES_MCP_SCRIPT
local EXTSTATE_SECTION = M.EXTSTATE_SECTION
local APPDATA_DIR      = M.APPDATA_DIR
local GLOBAL_CONFIG    = M.GLOBAL_CONFIG
local TARGET_LUFS      = M.TARGET_LUFS
local TARGET_TP        = M.TARGET_TP
local use_hermes       = M.use_hermes
local monitoring_setup = M.monitoring_setup
local advice_style     = M.advice_style
local MONITOR_LABELS   = M.MONITOR_LABELS
local ADVICE_LABELS    = M.ADVICE_LABELS
local PROFILES_DIR     = M.PROFILES_DIR
local STYLE_PRESETS_DIR= M.STYLE_PRESETS_DIR
local plugin_inventory = M.plugin_inventory
local engineer_profiles= M.engineer_profiles

-- ── OS ABSTRACTION LAYER ───────────────────────────────────────────
local OS = {}
OS.platform = "windows"

function OS.path_to_shell(p)
  p = p:gsub("/", "\\")
  if p:find(" ") then p = '"' .. p .. '"' end
  return p
end

function OS.http_get_cmd(url, out_file)
  return string.format(
    'curl.exe -s --connect-timeout 4 "%s" -o "%s"',
    url, out_file:gsub("/", "\\"))
end

function OS.http_post_cmd(url, body, out_file)
  local body_file = reaper.GetResourcePath() .. "/damei_post_body_tmp.json"
  local bf = io.open(body_file, "w")
  if bf then bf:write(body); bf:close() end
  return string.format(
    'curl.exe -s -X POST -H "Content-Type: application/json" --data-binary @"%s" "%s" -o "%s"',
    body_file:gsub("/", "\\"), url, out_file:gsub("/", "\\"))
end

function OS.launch_detached(script_path, window_title)
  reaper.ExecProcess(
    'cmd.exe /C cd /d "' .. script_path:match("(.+)[/\\]") .. '" && python "' .. script_path .. '"',
    0
  )
end

function OS.kill_pid(pid)
  reaper.ExecProcess('wmic process where ProcessId="' .. pid .. '" call terminate', 0)
end

function OS.find_pid_by_title(title, out_file)
  reaper.ExecProcess(
    'cmd.exe /C wmic process where "name=\'python.exe\' and CommandLine like \'%%' .. title .. '%%\'" get ProcessId /format:value > "' .. out_file:gsub("/", "\\") .. '"',
    0
  )
end

function OS.open_file(path)
  reaper.ExecProcess('cmd.exe /C start "" "' .. path .. '"', 0)
end

local function ensure_dir(dir)
  dir = sanitize_path(dir)
  reaper.RecursiveCreateDirectory(dir:gsub("/", "\\"), 0)
end

-- ── HTTP (silent, file-based, async) ────────────────────────────────
local pending_http = {}

local function http_get(url, callback)
  local id = tostring(os.clock()):gsub("%.","") .. tostring(math.random(9999))
  local resp = reaper.GetResourcePath() .. "/damei_resp_" .. id .. ".json"
  os.remove(resp)
  reaper.ExecProcess(OS.http_get_cmd(url, resp), 0)
  pending_http[id] = { file = resp, cb = callback, t0 = os.time() }
end

local function http_post(url, body, callback)
  local id = tostring(os.clock()):gsub("%.","") .. tostring(math.random(9999))
  local resp = reaper.GetResourcePath() .. "/damei_resp_" .. id .. ".json"
  local body_file = reaper.GetResourcePath() .. "/damei_body_" .. id .. ".json"
  os.remove(resp)
  local bf = io.open(body_file, "w")
  if bf then bf:write(body); bf:close() end
  local cmd = string.format(
    'curl.exe -s -X POST -H "Content-Type: application/json" --data-binary @"%s" "%s" -o "%s"',
    body_file:gsub("/", "\\"), url, resp:gsub("/", "\\")
  )
  reaper.ExecProcess(cmd, 0)
  pending_http[id] = { file = resp, body_file = body_file, cb = callback, t0 = os.time() }
end

local function poll_http()
  for id, p in pairs(pending_http) do
    local f = io.open(p.file, "r")
    if f then
      local body = f:read("*a"); f:close()
      if body and #body > 2 then
        os.remove(p.file)
        if p.body_file then os.remove(p.body_file) end
        p.cb(body)
        pending_http[id] = nil
      elseif os.time() - p.t0 > 30 then
        os.remove(p.file)
        if p.body_file then os.remove(p.body_file) end
        p.cb(nil)
        pending_http[id] = nil
      end
    elseif os.time() - p.t0 > 30 then
      if p.body_file then os.remove(p.body_file) end
      p.cb(nil)
      pending_http[id] = nil
    end
  end
end

-- ── STATE PERSISTENCE ───────────────────────────────────────────────
local function save_project_state()
  local data = M.serialize_project_state()
  reaper.SetProjExtState(0, EXTSTATE_SECTION, "chat_log", data.chat_log)
  reaper.SetProjExtState(0, EXTSTATE_SECTION, "gain_health", data.gain_health)
  reaper.SetProjExtState(0, EXTSTATE_SECTION, "target_lufs", data.target_lufs)
  reaper.SetProjExtState(0, EXTSTATE_SECTION, "client_notes", data.client_notes)
end

local function load_project_state()
  local _, chat_json = reaper.GetProjExtState(0, EXTSTATE_SECTION, "chat_log")
  M.deserialize_chat_json(chat_json)
  local _, health = reaper.GetProjExtState(0, EXTSTATE_SECTION, "gain_health")
  if health and #health > 0 then st.gain_health = tonumber(health) or 0 end
  local _, notes = reaper.GetProjExtState(0, EXTSTATE_SECTION, "client_notes")
  if notes and #notes > 0 then st.client_notes = notes end
end

local function save_global_config()
  ensure_dir(APPDATA_DIR)
  local f = io.open(GLOBAL_CONFIG:gsub("/", "\\"), "w")
  if f then f:write(M.serialize_global_config()); f:close() end
end

local function load_global_config()
  local f = io.open(GLOBAL_CONFIG:gsub("/", "\\"), "r")
  if f then
    local data = f:read("*a"); f:close()
    M.deserialize_global_config(data)
    DAMEI_URL = M.DAMEI_URL
    TARGET_LUFS = M.TARGET_LUFS
    TARGET_TP = M.TARGET_TP
  end
end

-- ── ENGINEER PROFILE LOADER ─────────────────────────────────────────
local function load_engineer_profiles()
  local profiles = {}
  M.engineer_profiles = profiles
  table.insert(profiles, { name = "None", data = nil })
  local parse = M.parse_json_simple
  local dirs = {
    { dir = STYLE_PRESETS_DIR .. "/mix", cat = "Mix" },
    { dir = STYLE_PRESETS_DIR .. "/master", cat = "Master" },
    { dir = STYLE_PRESETS_DIR .. "/producer", cat = "Producer" },
  }
  for _, pd in ipairs(dirs) do
    local j = 0
    while true do
      local file = reaper.EnumerateFiles(pd.dir:gsub("/", "\\"), j)
      if not file then break end
      j = j + 1
      if file:match("%.json$") and not file:match("backup") then
        local f = io.open(pd.dir .. "/" .. file, "r")
        if f then
          local data = parse(f:read("*a")); f:close()
          if data then
            local name = (data._meta and data._meta.engineer)
              or data.engineer_name or file:gsub("%.json$", ""):gsub("_", " ")
            name = name:gsub("(%a)([%w]*)", function(a, b) return a:upper() .. b end)
            table.insert(profiles, { name = name .. " [" .. pd.cat .. "]", data = data, file = file, category = pd.cat })
          end
        end
      end
    end
  end
  local k = 0
  while true do
    local file = reaper.EnumerateFiles(PROFILES_DIR:gsub("/", "\\"), k)
    if not file then break end
    k = k + 1
    if file:match("%.json$") then
      local f = io.open(PROFILES_DIR .. "/" .. file, "r")
      if f then
        local data = parse(f:read("*a")); f:close()
        if data and data.engineer_name then
          table.insert(profiles, { name = data.engineer_name .. " [Custom]", data = data, file = file, category = "Custom" })
        end
      end
    end
  end
  engineer_profiles = profiles
end

-- ── STARTUP INIT ────────────────────────────────────────────────────
load_engineer_profiles()
load_global_config()

-- ImGui context and fonts
local ctx = ImGui.CreateContext('DameiConsole')
local FONT_DIR = SCRIPT_DIR .. "/fonts/"
local font_main, font_mono
do
  local f1 = io.open(FONT_DIR .. "Inter-Regular.ttf", "rb")
  if f1 then
    f1:close()
    font_main = ImGui.CreateFontFromFile(FONT_DIR .. "Inter-Regular.ttf")
    ImGui.Attach(ctx, font_main)
  end
  local f2 = io.open(FONT_DIR .. "RobotoMono-Regular.ttf", "rb")
  if f2 then
    f2:close()
    font_mono = ImGui.CreateFontFromFile(FONT_DIR .. "RobotoMono-Regular.ttf")
    ImGui.Attach(ctx, font_mono)
  end
end

-- Initialize modules
V.init(M, ImGui, ctx, {
  main = font_main, mono = font_mono,
  size_main = 14, size_mono = 13,
}, ctrl)

ctrl.init(M, OS, { get = http_get, post = http_post })

-- Expose save/load to controller for action handlers that need it
ctrl.save_project_state = save_project_state
ctrl.save_global_config = save_global_config

log("Damei Mix Console v4 initialized", "ok")

-- ── MAIN LOOP ───────────────────────────────────────────────────────
local frame_counter = 0
local gmem_skip_rate = 1

local function loop()
  frame_counter = frame_counter + 1
  poll_http()

  -- Adaptive throttle based on playstate
  local playstate = reaper.GetPlayState()
  gmem_skip_rate = playstate == 5 and 3 or playstate == 1 and 1 or 2

  if frame_counter % gmem_skip_rate == 0 then
    ctrl.read_gmem()
    ctrl.read_ref_gmem()
  end
  if frame_counter % 4 == 0 then
    ctrl.check_health()
  end

  -- ── RENDER ──────────────────────────────────────────────────────
  V.push_theme()
  ImGui.SetNextWindowSize(ctx, 800, 560, ImGui.Cond_FirstUseEver)
  local visible, open = ImGui.Begin(ctx, "Damei Mix Console v4", true, ImGui.WindowFlags_NoCollapse)

  if visible then
    V.draw_main(ctrl, {
      use_hermes = use_hermes,
      DAMEI_URL = DAMEI_URL,
      HERMES_MCP_URL = HERMES_MCP_URL,
      monitoring_setup = monitoring_setup,
      advice_style = advice_style,
      MONITOR_LABELS = MONITOR_LABELS,
      ADVICE_LABELS = ADVICE_LABELS,
      TARGET_LUFS = TARGET_LUFS,
      TARGET_TP = TARGET_TP,
      plugin_inventory = plugin_inventory,
      engineer_profiles = engineer_profiles,
      save_project_state = save_project_state,
      save_global_config = save_global_config,
      OS = OS,
    })
    ImGui.End(ctx)
  end

  V.pop_theme()

  if open then
    reaper.defer(loop)
  else
    save_project_state()
    save_global_config()
    if st.mcp_pid then
      OS.kill_pid(st.mcp_pid)
      st.mcp_pid = nil
    end
    log("State saved", "ok")
  end
end

-- ── DEFERRED STARTUP ────────────────────────────────────────────────
reaper.defer(function()
  local _, proj = reaper.EnumProjects(-1)
  if proj and #proj > 0 then
    st.project_name = proj:match("([^/\\]+)%.RPP$") or proj:match("([^/\\]+)$") or proj
  end

  load_project_state()
  if #st.chat_log > 0 then
    log(string.format("Restored %d chat messages", #st.chat_log), "ok")
  end

  local jsfx_ok = ctrl.ensure_jsfx_on_master()
  if jsfx_ok then
    log("Damei_Metering active on Master Bus", "ok")
  end

  -- MCP server boot
  http_get(HERMES_MCP_URL .. "/health", function(body)
    if body then
      st.mcp_alive = true
      log("Hermes MCP: connected", "ok")
    else
      if not st.mcp_alive and not st.mcp_booting then
        st.mcp_booting = true
        log("Booting Hermes MCP...", "accent")
        OS.launch_detached(HERMES_MCP_SCRIPT, "DameiMCP")
      end
    end
  end)

  reaper.defer(function()
    ctrl.action_scan()
    log("Damei Mix Console ready", "ok")
  end)
  reaper.defer(loop)
end)
