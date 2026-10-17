-- ═════════════════════════════════════════════════════════════════════
-- damei_controller.lua — Logic & REAPER API Layer (MVC Phase 1.3)
--
-- RULES:
--   - All reaper.* API calls live here
--   - All HTTP dispatch, gmem reading, action orchestration
--   - Reads/writes model (M.st) for state
--   - ZERO ImGui calls
--
-- Phase 2: Every AI-driven operation wraps in Undo_BeginBlock/Undo_EndBlock
--          State chunk puppeteering for bulk FX insertion
-- ═════════════════════════════════════════════════════════════════════

local ctrl = {}
local gmem_attached = false
local health_boot_done = false

-- Module references
local M, OS
local st, ref, log

function ctrl.init(model, os_layer, http_funcs)
  M = model
  OS = os_layer
  st = M.st
  ref = M.ref
  log = M.log
  ctrl.http_get = http_funcs.get
  ctrl.http_post = http_funcs.post
end

-- ── PHASE 2: ATOMIC UNDO WRAPPER ────────────────────────────────────
-- Every destructive operation must use this. Single Ctrl+Z reverts.
function ctrl.with_undo(label, fn)
  reaper.Undo_BeginBlock()
  reaper.PreventUIRefresh(1)
  local ok, err = pcall(fn)
  reaper.PreventUIRefresh(-1)
  reaper.Undo_EndBlock("Damei: " .. label, -1)
  if not ok then
    M.log("Undo block error [" .. label .. "]: " .. tostring(err), "err")
  end
  -- Force model refresh from DAW state (not cache)
  ctrl.refresh_model_from_daw()
  return ok
end

-- Refresh model state from REAPER ground truth (unidirectional flow)
function ctrl.refresh_model_from_daw()
  local n = reaper.CountTracks(0)
  st.track_count = n
  st.tracks = {}
  local hot = 0
  for i = 0, n - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, name = reaper.GetTrackName(tr)
    local vol = reaper.GetMediaTrackInfo_Value(tr, "D_VOL")
    local db = 20 * math.log(vol, 10)
    local mute = reaper.GetMediaTrackInfo_Value(tr, "B_MUTE")
    local solo = reaper.GetMediaTrackInfo_Value(tr, "I_SOLO")
    local fx_count = reaper.TrackFX_GetCount(tr)
    local depth = reaper.GetTrackDepth(tr)
    local cat, col = M.classify(name)
    if db > -1 then hot = hot + 1 end
    table.insert(st.tracks, {
      idx = i, name = name, db = db, vol = vol,
      mute = mute, solo = solo, fx_count = fx_count,
      depth = depth, category = cat, color = col,
      is_folder = reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH") > 0,
    })
  end
  st.hot_count = hot
  if n > 0 then
    st.gain_health = math.max(0, math.min(100, 100 - (hot / n * 100)))
  end
  st.session_scanned = true
end

-- ── PHASE 2: STATE CHUNK PUPPETEERING ───────────────────────────────
-- Inject ReaEQ via track state chunk (no FX browser dialog)
function ctrl.inject_reaeq(track, bands)
  local _, chunk = reaper.GetTrackStateChunk(track, "", false)
  if not chunk then return false end

  -- Build ReaEQ FX chunk
  local eq_lines = {
    '<FXCHAIN',
    'WNDRECT 0 0 600 500',
    'SHOW 0',
    'LASTSEL 0',
    'DOCKED 0',
    '<VST "VST: ReaEQ (Cockos)" reaeq.dll 0 "" 1919247729<5653546571657172656171>',
    string.format('%d 0', #bands),
  }
  for _, b in ipairs(bands) do
    table.insert(eq_lines, string.format(
      '%.6f %.6f 1 %d %.6f 1 1',
      b.freq or 1000, b.gain or 0, b.type or 8, b.q or 1.0
    ))
  end
  table.insert(eq_lines, '>')
  table.insert(eq_lines, '>')
  local eq_chunk = table.concat(eq_lines, '\n')

  -- Insert before the closing > of the track chunk
  if chunk:find('<FXCHAIN') then
    -- Already has FX chain, append inside it
    chunk = chunk:gsub('(</FXCHAIN>)', eq_chunk .. '\n%1')
  else
    -- No FX chain, insert before final >
    chunk = chunk:gsub('(>%s*)$', eq_chunk .. '\n%1')
  end

  return reaper.SetTrackStateChunk(track, chunk, false)
end

-- Apply a match result atomically (Phase 2 + 5 integration point)
function ctrl.apply_match_result(result)
  return ctrl.with_undo("Apply Spectral Match", function()
    for _, change in ipairs(result.changes or {}) do
      local tr = reaper.GetTrack(0, change.track_idx or 0)
      if not tr then goto continue end

      if change.type == "eq" then
        ctrl.inject_reaeq(tr, change.bands or {})
      elseif change.type == "gain" then
        local linear = 10 ^ ((change.db or 0) / 20)
        reaper.SetMediaTrackInfo_Value(tr, "D_VOL", linear)
      elseif change.type == "send_level" then
        local si = change.send_idx or 0
        local linear = 10 ^ ((change.db or 0) / 20)
        reaper.SetTrackSendInfo_Value(tr, 0, si, "D_VOL", linear)
      end
      ::continue::
    end
  end)
end


function ctrl.read_gmem()
  if not gmem_attached then
    reaper.gmem_attach(M.GMEM_NAME)
    gmem_attached = true
  end

  -- Double-buffer: read from the bank the JSFX is NOT writing to
  local write_bank = reaper.gmem_read(127)
  local r = (write_bank == 0) and M.BANK_SIZE or 0  -- read offset

  -- Check if JSFX has ever written data (version marker at gmem[126] = 200 for v2)
  local jsfx_version = reaper.gmem_read(126)
  local jsfx_has_data = jsfx_version == 200

  if jsfx_has_data then
    -- Read from completed bank (thread-safe)
    st.lufs_m = reaper.gmem_read(r + 0)
    st.lufs_s = reaper.gmem_read(r + 1)
    st.lufs_i = reaper.gmem_read(r + 2)
    st.tp_l   = reaper.gmem_read(r + 3)
    st.tp_r   = reaper.gmem_read(r + 4)
    for i = 0, 7 do st.bands[i+1] = reaper.gmem_read(r + 5 + i) end
    st.corr   = reaper.gmem_read(r + 13)
    st.peak_l = reaper.gmem_read(r + 16)
    st.peak_r = reaper.gmem_read(r + 17)
  end
  -- If jsfx_has_data is false, keep previous values (initialized to -70 in st)

  -- Check heartbeat (gmem advances only during playback)
  local hb = reaper.gmem_read(r + 15)
  -- Only set jsfx_alive via heartbeat if heartbeat is changing
  -- Don't set to false here — the FX-list check in ctrl.check_health() handles presence
  if hb ~= st.last_hb then
    st.jsfx_alive = true
  end
  st.last_hb = hb

  -- Meter ballistics: fast attack, slow release
  local attack  = 0.9   -- instant rise
  local release = 0.08  -- slow decay (~12 frames to drop)
  local now = os.clock()

  local function ballistic(smoothed, target)
    if target > smoothed then
      return smoothed + attack * (target - smoothed)   -- fast attack
    else
      return smoothed + release * (target - smoothed)  -- slow release
    end
  end

  st.sm_lufs_m = ballistic(st.sm_lufs_m, st.lufs_m)
  st.sm_lufs_s = ballistic(st.sm_lufs_s, st.lufs_s)
  st.sm_lufs_i = ballistic(st.sm_lufs_i, st.lufs_i)
  st.sm_tp_l   = ballistic(st.sm_tp_l,   st.tp_l)
  st.sm_tp_r   = ballistic(st.sm_tp_r,   st.tp_r)
  st.sm_corr   = st.sm_corr + 0.15 * (st.corr - st.sm_corr)  -- correlation stays smooth
  for i = 1, 8 do
    st.sm_bands[i] = ballistic(st.sm_bands[i], st.bands[i])
  end

  -- Peak hold: track maximum, decay after hold time
  local function update_hold(current, hold_val, hold_idx)
    if current > hold_val then
      st.pk_hold_time[hold_idx] = now
      return current
    elseif (now - st.pk_hold_time[hold_idx]) > st.pk_hold_decay then
      return hold_val + 0.05 * (current - hold_val)  -- slow decay after hold
    end
    return hold_val
  end

  st.pk_hold_lufs_m = update_hold(st.sm_lufs_m, st.pk_hold_lufs_m, 1)
  st.pk_hold_lufs_s = update_hold(st.sm_lufs_s, st.pk_hold_lufs_s, 2)
  st.pk_hold_lufs_i = update_hold(st.sm_lufs_i, st.pk_hold_lufs_i, 3)
  st.pk_hold_tp_l   = update_hold(st.sm_tp_l,   st.pk_hold_tp_l,   4)
  st.pk_hold_tp_r   = update_hold(st.sm_tp_r,   st.pk_hold_tp_r,   5)
  for i = 1, 8 do
    st.pk_hold_bands[i] = update_hold(st.sm_bands[i], st.pk_hold_bands[i], 5 + i)
  end
end

-- ── REFERENCE GMEM READING ─────────────────────────────────────

function ctrl.read_ref_gmem()
  if not ref.track then return end  -- no reference track

  -- Must re-attach every frame since read_gmem uses DameiMetering
  reaper.gmem_attach(M.GMEM_REF_NAME)

  local write_bank = reaper.gmem_read(127)
  local r = (write_bank == 0) and M.BANK_SIZE or 0

  ref.lufs_m = reaper.gmem_read(r + 0)
  ref.lufs_s = reaper.gmem_read(r + 1)
  ref.lufs_i = reaper.gmem_read(r + 2)
  ref.tp_l   = reaper.gmem_read(r + 3)
  ref.tp_r   = reaper.gmem_read(r + 4)
  for i = 0, 7 do ref.bands[i+1] = reaper.gmem_read(r + 5 + i) end
  ref.corr   = reaper.gmem_read(r + 13)

  local hb = reaper.gmem_read(r + 15)
  ref.alive = hb ~= ref.last_hb
  ref.last_hb = hb

  -- Smooth reference values
  local a = 0.25
  ref.sm_lufs_i = ref.sm_lufs_i + a * (ref.lufs_i - ref.sm_lufs_i)
  for i = 1, 8 do
    ref.sm_bands[i] = ref.sm_bands[i] + a * (ref.bands[i] - ref.sm_bands[i])
  end

  -- Switch back to main gmem
  reaper.gmem_attach(M.GMEM_NAME)
end

-- ── PLUGIN INVENTORY SCANNER ───────────────────────────────────

function ctrl.action_scan_plugins()
  M.log("Scanning VST plugins...", "accent")
  M.plugin_inventory = {}
  local seen = {}

  local ini_path = reaper.GetResourcePath() .. "/reaper-vstplugins64.ini"
  local f = io.open(ini_path, "r")
  if not f then
    M.log("VST cache not found", "err")
    return
  end

  for line in f:lines() do
    -- Format: file=hash,id,DisplayName (Vendor)
    -- Or VST3: hash=id - path
    local display = line:match(",([^,]+)$")
    if display then
      -- Clean up: remove leading/trailing whitespace and !!!VSTi markers
      display = display:gsub("!!!VSTi$", ""):gsub("^%s+", ""):gsub("%s+$", "")
      if #display > 0 and not seen[display] then
        seen[display] = true
        table.insert(M.plugin_inventory, display)
      end
    end
  end
  f:close()

  table.sort(M.plugin_inventory)
  M.plugin_scan_time = os.time()
  M.log(string.format("Indexed %d plugins", #M.plugin_inventory), "ok")
  ctrl.save_global_config()
end

-- ── REFERENCE TRACK MANAGEMENT ─────────────────────────────────

function ctrl.action_import_reference()
  M.log("Import reference: select an audio file...", "accent")

  -- Use REAPER's native file dialog
  local retval, filename = reaper.GetUserFileNameForRead("", "Select Reference Track", "*.wav;*.mp3;*.flac;*.aif;*.aiff")
  if not retval or not filename or #filename == 0 then
    M.log("Reference import cancelled", "warn")
    return
  end

  reaper.Undo_BeginBlock()
  reaper.PreventUIRefresh(1)

  -- Remove existing reference track if any
  if ref.track and reaper.ValidatePtr(ref.track, "MediaTrack*") then
    local idx = reaper.GetMediaTrackInfo_Value(ref.track, "IP_TRACKNUMBER") - 1
    if idx >= 0 then reaper.DeleteTrack(ref.track) end
  end

  -- Create new track at the end
  local idx = reaper.CountTracks(0)
  reaper.InsertTrackAtIndex(idx, false)
  ref.track = reaper.GetTrack(0, idx)

  if ref.track then
    -- Name it
    local fname = filename:match("([^/\\]+)$") or "Reference"
    ref.name = fname:match("(.+)%.") or fname
    reaper.GetSetMediaTrackInfo_String(ref.track, "P_NAME", "REF: " .. ref.name, true)

    -- Mute the track (only for monitoring via solo-in-place)
    reaper.SetMediaTrackInfo_Value(ref.track, "B_MUTE", 1)

    -- Set to bypass master bus (direct hardware out)
    reaper.SetMediaTrackInfo_Value(ref.track, "B_MAINSEND", 0)
    -- Route directly to hardware output 1/2
    reaper.CreateTrackSend(ref.track, -1)  -- -1 = hardware output

    -- Insert media
    reaper.SetOnlyTrackSelected(ref.track)
    reaper.InsertMedia(filename, 0)

    -- Add Damei_RefMetering JSFX
    local fx_idx = reaper.TrackFX_AddByName(ref.track, "Damei_RefMetering", false, -1)
    if fx_idx >= 0 then
      M.log("Reference JSFX inserted", "ok")
    else
      M.log("Could not insert Damei_RefMetering.jsfx", "warn")
    end

    -- Color it distinctly
    reaper.SetTrackColor(ref.track, 0x01808080)  -- grey

    ref.item = reaper.GetTrackMediaItem(ref.track, 0)
    M.log("Reference loaded: " .. ref.name, "ok")
  end

  reaper.PreventUIRefresh(-1)
  reaper.Undo_EndBlock("Damei: Import Reference Track", -1)
  reaper.TrackList_AdjustWindows(false)
  reaper.UpdateArrange()
end

-- ── AUTO-INSERT JSFX ────────────────────────────────────────────────
-- Ensures Damei_Metering.jsfx is on the target track (default: Master Bus)

function ctrl.ensure_jsfx_on_master()
  local master = reaper.GetMasterTrack(0)
  if not master then return false end

  -- Check if already inserted (REAPER may show name as various formats)
  local fx_count = reaper.TrackFX_GetCount(master)
  for i = 0, fx_count - 1 do
    local _, name = reaper.TrackFX_GetFXName(master, i)
    if name and (name:find("Damei_Metering") or name:find("Damei Metering")) then
      return true  -- already there
    end
  end

  -- Try multiple naming conventions (REAPER is inconsistent across versions)
  local try_names = {
    "JS:Damei/Damei_Metering",
    "JS: Damei/Damei_Metering",
    "Damei/Damei_Metering",
    "Damei_Metering",
    "JS:Damei_Metering",
    "JS: Damei_Metering",
  }
  for _, name in ipairs(try_names) do
    local idx = reaper.TrackFX_AddByName(master, name, false, -1)
    if idx >= 0 then
      M.log("Auto-inserted Damei_Metering on Master Bus (" .. name .. ")", "ok")
      return true
    end
  end

  M.log("Could not auto-insert JSFX — add manually: Effects > JS > Damei > Damei_Metering", "warn")
  return false
end

-- ── HEALTH CHECK ────────────────────────────────────────────────────
local health_boot_done = false  -- first check uses shorter interval

function ctrl.check_health()
  local now = os.time()
  local interval = health_boot_done and 15 or 2  -- fast on boot, then normal
  if now - st.last_check < interval then return end
  st.last_check = now
  health_boot_done = true

  -- DameiAPI health
  ctrl.http_get(M.DAMEI_URL .. "/health", function(body)
    if body and body:find('"ok"') then
      st.api_ok = true
      st.api_fail_count = 0
      -- Clear booting state when server comes online
      if st.api_booting then
        st.api_booting = false
        M.log("DameiAPI: online", "ok")
      end
    else
      st.api_fail_count = (st.api_fail_count or 0) + 1
      -- Only mark offline after 3 consecutive failures (avoids flicker)
      if st.api_fail_count >= 3 and not st.api_booting then
        st.api_ok = false
      end
    end
  end)

  -- Bridge status
  ctrl.http_get(M.DAMEI_URL .. "/bridge/status", function(body)
    if body and body:find('"alive"%s*:%s*true') then
      st.bridge_alive = true
      st.bridge_fail_count = 0
    else
      st.bridge_fail_count = (st.bridge_fail_count or 0) + 1
      if st.bridge_fail_count >= 3 then
        st.bridge_alive = false
      end
    end
  end)

  -- Project name from REAPER directly
  local _, proj_path = reaper.EnumProjects(-1)
  if proj_path and #proj_path > 0 then
    st.project_name = proj_path:match("([^/\\]+)%.RPP$") or proj_path:match("([^/\\]+)$") or proj_path
  end

  -- Robust JSFX detection: check Master FX list directly
  -- (gmem heartbeat only advances during playback, so supplement with FX presence check)
  if not st.jsfx_alive then
    local master = reaper.GetMasterTrack(0)
    if master then
      local fx_count = reaper.TrackFX_GetCount(master)
      for i = 0, fx_count - 1 do
        local _, fname = reaper.TrackFX_GetFXName(master, i)
        if fname and (fname:find("Damei_Metering") or fname:find("Damei Metering")) then
          st.jsfx_alive = true
          break
        end
      end
    end
  end
end

-- ── PHASE 3+6: HEADLESS AUTO-LAUNCH WITH FIRST-RUN DOWNLOAD ────────
-- Priority chain:
--   1. DameiEngine.exe exists locally → launch headless
--   2. DameiEngine.exe missing → download from GitHub Releases → launch
--   3. Download fails → fall back to Python dev server
--
-- Version and release URL are centralized here for easy updates.
local ENGINE_VERSION = "4.0.0"
local GITHUB_RELEASES_URL = "https://github.com/pityy/damei-mix-console/releases"
local ENGINE_DOWNLOAD_URL = GITHUB_RELEASES_URL .. "/latest/download/DameiEngine.exe"
local ENGINE_CHECKSUM_URL = GITHUB_RELEASES_URL .. "/latest/download/DameiEngine.exe.sha256"

function ctrl.ensure_backend()
  if st.api_ok or st.api_booting then return end
  st.api_booting = true
  st.api_boot_start = os.clock()
  st.api_fail_count = 0

  local script_dir = reaper.GetResourcePath() .. "/Scripts/Damei"
  local engine_exe = script_dir .. "/DameiEngine.exe"

  -- Check if frozen exe exists locally
  local f = io.open(engine_exe, "rb")
  if f then
    f:close()
    reaper.ExecProcess('"' .. engine_exe:gsub("/", "\\") .. '"', 0)
    M.log("DameiEngine.exe: launching...", "accent")
    return
  end

  -- Phase 6: First-run download from GitHub Releases
  M.log("DameiEngine.exe not found — downloading from GitHub...", "accent")
  st.engine_downloading = true

  -- Download using curl (ships with Windows 10+)
  local dl_path = engine_exe:gsub("/", "\\")
  local cmd = string.format(
    'curl.exe -sL --connect-timeout 10 -o "%s" "%s"',
    dl_path, ENGINE_DOWNLOAD_URL
  )
  reaper.ExecProcess(cmd, 0)

  -- Poll for download completion via deferred callback
  local dl_start = os.time()
  local function poll_download()
    local ef = io.open(engine_exe, "rb")
    if ef then
      local size = ef:seek("end")
      ef:close()
      -- Engine should be at least 10MB to be valid
      if size and size > 10 * 1024 * 1024 then
        st.engine_downloading = false
        M.log(string.format("DameiEngine.exe downloaded (%.1f MB)", size / 1024 / 1024), "ok")
        -- Launch the freshly downloaded engine
        reaper.ExecProcess('"' .. dl_path .. '"', 0)
        M.log("DameiEngine.exe: launching...", "accent")
        return
      end
    end

    -- Timeout after 120 seconds
    if os.time() - dl_start > 120 then
      st.engine_downloading = false
      M.log("Download timed out — falling back to Python", "warn")
      ctrl.launch_python_fallback()
      return
    end

    -- Keep polling
    reaper.defer(poll_download)
  end
  reaper.defer(poll_download)
end

-- Fallback: launch from Python dev environment
function ctrl.launch_python_fallback()
  local dev_script = "C:\\Dev\\DameiAPI\\start_server.py"
  local f = io.open(dev_script, "r")
  if f then
    f:close()
    reaper.ExecProcess(
      'cmd.exe /C cd /d "C:\\Dev\\DameiAPI" && python start_server.py',
      0
    )
    M.log("DameiAPI (Python dev): launching...", "accent")
  else
    st.api_booting = false
    M.log("No backend available — install DameiEngine.exe or Python dev env", "err")
  end
end

-- ── PHASE 6: VERSION CHECK & AUTO-UPDATE ────────────────────────────
-- Checks GitHub Releases for a newer version and offers update
function ctrl.check_for_updates()
  local api_url = "https://api.github.com/repos/pityy/damei-mix-console/releases/latest"
  ctrl.http_get(api_url, function(body)
    if not body then return end
    -- Parse version tag from GitHub API response
    local tag = body:match('"tag_name"%s*:%s*"v([%d%.]+)"')
    if not tag then return end
    
    if tag ~= ENGINE_VERSION then
      st.update_available = tag
      M.log("Update available: v" .. tag .. " (current: v" .. ENGINE_VERSION .. ")", "accent")
    end
  end)
end

-- Perform the update: download new DameiEngine.exe
function ctrl.apply_update()
  if not st.update_available then return end
  local script_dir = reaper.GetResourcePath() .. "/Scripts/Damei"
  local engine_exe = script_dir .. "/DameiEngine.exe"
  local backup = engine_exe .. ".bak"
  
  -- Backup current exe
  local f = io.open(engine_exe, "rb")
  if f then
    local data = f:read("*a"); f:close()
    local bf = io.open(backup, "wb")
    if bf then bf:write(data); bf:close() end
  end
  
  -- Download new version
  local version_url = GITHUB_RELEASES_URL .. "/download/v" .. st.update_available .. "/DameiEngine.exe"
  local cmd = string.format(
    'curl.exe -sL --connect-timeout 10 -o "%s" "%s"',
    engine_exe:gsub("/", "\\"), version_url
  )
  reaper.ExecProcess(cmd, 0)
  M.log("Updating to v" .. st.update_available .. "...", "accent")
  st.update_available = nil
end

-- ── PHASE 3: ON-DEMAND MODEL DOWNLOAD ───────────────────────────────
function ctrl.ensure_demucs_model(callback)
  local model_dir = (os.getenv("APPDATA") or "") .. "/Damei/models/demucs"
  local marker = model_dir .. "/htdemucs_ft.th"
  local f = io.open(marker, "rb")
  if f then
    f:close()
    if callback then callback(true) end
    return
  end

  M.log("Downloading Demucs model (first run)...", "accent")
  ctrl.http_post(M.DAMEI_URL .. "/models/download", '{"model":"htdemucs_ft"}', function(body)
    if body and body:find('"ok"') then
      M.log("Demucs model downloaded successfully", "ok")
      if callback then callback(true) end
    else
      M.log("Demucs model download failed", "err")
      if callback then callback(false) end
    end
  end)
end


-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
-- THEME (Premium)
-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
local N_STYLE_COLORS = 0
local N_STYLE_VARS   = 0

function ctrl.action_scan()
  M.log("Scanning session...", "accent")
  local n = reaper.CountTracks(0) or 0
  st.tracks = {}
  for i = 0, n - 1 do
    local tr = reaper.GetTrack(0, i)
    if tr then
      local _, name = reaper.GetTrackName(tr)
      local vol = reaper.GetMediaTrackInfo_Value(tr, "D_VOL")
      local db = vol > 0 and (20 * math.log(vol, 10)) or -100

      -- Visual metadata: color
      local color_raw = reaper.GetTrackColor(tr)
      local color_hex = ""
      if color_raw ~= 0 then
        local r_v = color_raw & 0xFF
        local g_v = (color_raw >> 8) & 0xFF
        local b_v = (color_raw >> 16) & 0xFF
        color_hex = string.format("#%02X%02X%02X", r_v, g_v, b_v)
      end

      -- Visual metadata: icon (returns bool, string)
      local _, icon = reaper.GetSetMediaTrackInfo_String(tr, "P_ICON", "", false)

      -- Folder depth
      local folder = reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH")

      -- FX chain names
      local fx_list = {}
      local fx_count = reaper.TrackFX_GetCount(tr)
      for fi = 0, math.min(fx_count - 1, 7) do  -- cap at 8 FX per track
        local _, fx_name = reaper.TrackFX_GetFXName(tr, fi)
        if fx_name and #fx_name > 0 then
          table.insert(fx_list, fx_name)
        end
      end

      table.insert(st.tracks, {
        name = name or ("Track " .. (i+1)),
        vol_db = math.floor(db * 10 + 0.5) / 10,
        track = tr,
        color = color_hex,
        icon = icon,
        is_folder = folder == 1,
        fx = fx_list,
      })
    end
  end
  st.track_count = #st.tracks
  st.hot_count = 0
  for _, t in ipairs(st.tracks) do
    if t.vol_db and t.vol_db > -6 then st.hot_count = st.hot_count + 1 end
  end
  M.log(string.format("Scanned %d tracks, %d hot", st.track_count, st.hot_count), "ok")
  st.session_scanned = true
end

-- ── DIAGNOSIS: fetch health diagnosis from API ──────────────────────
function ctrl.action_diagnosis()
  if not st.api_ok then
    M.log("Cannot run diagnosis: API offline", "warn")
    return
  end
  M.log("Running diagnosis...", "accent")
  ctrl.http_get(M.DAMEI_URL .. "/session/diagnose", function(body)
    if not body then M.log("Diagnosis failed", "err"); return end
    local score = body:match('"score"%s*:%s*(%d+)')
    local engineer = body:match('"engineer"%s*:%s*"([^"]*)"')
    st.diagnosis = st.diagnosis or {}
    st.diagnosis.score = tonumber(score) or 0
    st.diagnosis.engineer = engineer or "Damei AI"
    st.diagnosis.raw = body
    M.log(string.format("Diagnosis: %d/100 (%s)", st.diagnosis.score, st.diagnosis.engineer), "ok")
  end)
end

-- ── TIPS: fetch mixing tips from API ────────────────────────────────
function ctrl.action_tips()
  if not st.api_ok then
    M.log("Cannot fetch tips: API offline", "warn")
    return
  end
  M.log("Fetching mixing tips...", "accent")
  local snapshot = ctrl.safe_session_snapshot()
  ctrl.http_post(M.DAMEI_URL .. "/session/tips", snapshot, function(body)
    if not body then M.log("Tips fetch failed", "err"); return end
    st.tips = {}
    for prio, cat, current, rec in body:gmatch(
      '"priority"%s*:%s*"([^"]*)"%s*,%s*"category"%s*:%s*"([^"]*)"%s*,%s*"current"%s*:%s*"([^"]*)"%s*,%s*"recommendation"%s*:%s*"([^"]*)"') do
      table.insert(st.tips, {priority=prio, category=cat, current=current, recommendation=rec})
    end
    M.log(string.format("Received %d tips", #st.tips), "ok")
  end)
end

-- ── IMPORT: open file browser and add audio to project ──────────────
function ctrl.action_import()
  local rv, file = reaper.GetUserFileNameForRead("", "Import Audio", "*.wav;*.mp3;*.flac;*.aif")
  if rv then
    ctrl.action_import_files({file})
  end
end

-- ── ENGINEER PROFILES: load from API ────────────────────────────────
function ctrl.load_engineer_profiles()
  if not st.api_ok then
    M.log("Cannot load profiles: API offline", "warn")
    return
  end
  ctrl.http_get(M.DAMEI_URL .. "/profiles", function(body)
    if not body then M.log("Profile load failed", "err"); return end
    st.engineer_profiles = {}
    for name in body:gmatch('"name"%s*:%s*"([^"]*)"') do
      table.insert(st.engineer_profiles, name)
    end
    M.log(string.format("Loaded %d engineer profiles", #st.engineer_profiles), "ok")
  end)
end

function ctrl.action_gainstage()
  M.log("Gain staging (dry run)...", "accent")
  ctrl.http_post(M.DAMEI_URL .. "/session/gainstage", '{"target_db": -18, "dry_run": true}', function(r)
    if not r then M.log("Gain staging failed", "err"); return end
    local count = 0
    for _ in r:gmatch('"track"%s*:') do count = count + 1 end
    M.log(string.format("Gain staged %d tracks (dry run)", count), "ok")
    ctrl.action_scan()  -- refresh track list
  end)
end

-- ── PRE-FX CLIP GAIN STAGING ───────────────────────────────────────

function ctrl.action_clip_gain_stage(target_dbfs)
  target_dbfs = target_dbfs or -18
  local target_lin = 10 ^ (target_dbfs / 20)
  M.log(string.format("Clip gain staging to %.0f dBFS...", target_dbfs), "accent")
  reaper.Undo_BeginBlock()
  reaper.PreventUIRefresh(1)

  local adjusted = 0
  local n_tracks = reaper.CountTracks(0) or 0
  for ti = 0, n_tracks - 1 do
    local tr = reaper.GetTrack(0, ti)
    if not tr then goto next_track end

    local n_items = reaper.CountTrackMediaItems(tr)
    for ii = 0, n_items - 1 do
      local item = reaper.GetTrackMediaItem(tr, ii)
      if not item then goto next_item end

      local take = reaper.GetActiveTake(item)
      if not take or reaper.TakeIsMIDI(take) then goto next_item end

      -- Get item length and calculate RMS via peaks
      local item_len = reaper.GetMediaItemInfo_Value(item, "D_LENGTH")
      if item_len <= 0 then goto next_item end

      -- Sample 256 peaks to estimate RMS
      local num_pts = 256
      local buf = reaper.new_array(num_pts * 2)
      local peakrate = num_pts / item_len
      local rv = reaper.GetMediaItemTake_Peaks(take, peakrate, 0, 1, num_pts, 0, buf)
      local actual_pts = rv & 0xFFFFF

      if actual_pts > 0 then
        local sum_sq = 0
        for pi = 0, actual_pts - 1 do
          local pk = buf[pi + 1] or 0
          sum_sq = sum_sq + pk * pk
        end
        local rms = math.sqrt(sum_sq / actual_pts)

        if rms > 0.00001 then  -- above noise floor
          local current_gain = reaper.GetMediaItemTakeInfo_Value(take, "D_VOL")
          local gain_adjust = target_lin / rms
          -- Clamp to reasonable range (don't boost more than +12dB or cut more than -24dB)
          gain_adjust = math.max(0.0625, math.min(4.0, gain_adjust))
          reaper.SetMediaItemTakeInfo_Value(take, "D_VOL", current_gain * gain_adjust)
          adjusted = adjusted + 1
        end
      end
      ::next_item::
    end
    ::next_track::
  end

  reaper.PreventUIRefresh(-1)
  reaper.Undo_EndBlock("Damei: Pre-FX Clip Gain Stage", -1)
  reaper.UpdateArrange()
  M.log(string.format("Clip gain staged %d items to ~%.0f dBFS", adjusted, target_dbfs), "ok")
  table.insert(st.auto_log, os.date("%H:%M:%S") .. string.format(" Clip gain: %d items", adjusted))
end

-- ── SMART ENVELOPE AUTOMATION ──────────────────────────────────────

function ctrl.action_write_envelope(track_idx, time_start, time_end, db_change)
  -- Writes a volume envelope dip/boost on a specific track at a specific time range
  track_idx = track_idx or 0
  db_change = db_change or -3
  local tr = reaper.GetTrack(0, track_idx)
  if not tr then
    M.log("Envelope: invalid track index " .. track_idx, "err")
    return
  end

  reaper.Undo_BeginBlock()

  -- Get or create volume envelope
  local env = reaper.GetTrackEnvelopeByName(tr, "Volume")
  if not env then
    -- Show volume envelope first
    local env_idx = reaper.GetMediaTrackInfo_Value(tr, "IP_TRACKNUMBER") - 1
    reaper.SetMediaTrackInfo_Value(tr, "B_SHOWINTCP", 1)
    -- Toggle volume envelope visibility
    reaper.Main_OnCommand(reaper.NamedCommandLookup("_S&M_TOGENVVOL") or 40406, 0)
    env = reaper.GetTrackEnvelopeByName(tr, "Volume")
  end

  if env then
    local lin_change = 10 ^ (db_change / 20)
    local fade_time = 0.02  -- 20ms fade

    -- Read current value at the target time
    local base_val = 1.0  -- linear, 0dB
    local _, cur_val = reaper.Envelope_Evaluate(env, time_start, 0, 0)
    if cur_val and cur_val > 0 then base_val = cur_val end

    local target_val = base_val * lin_change
    -- Clamp
    target_val = math.max(0.001, math.min(4.0, target_val))

    -- Insert 4 points: pre-dip, dip-start, dip-end, post-dip
    reaper.InsertEnvelopePoint(env, time_start - fade_time, base_val, 0, 0, false, true)
    reaper.InsertEnvelopePoint(env, time_start, target_val, 0, 0, false, true)
    reaper.InsertEnvelopePoint(env, time_end, target_val, 0, 0, false, true)
    reaper.InsertEnvelopePoint(env, time_end + fade_time, base_val, 0, 0, false, true)
    reaper.Envelope_SortPoints(env)

    local _, trk_name = reaper.GetTrackName(tr)
    M.log(string.format("Envelope: wrote %+.1fdB dip on '%s' at %.2f-%.2fs",
      db_change, trk_name, time_start, time_end), "ok")
  else
    M.log("Envelope: could not find/create volume envelope", "err")
  end

  reaper.Undo_EndBlock("Damei: Smart Envelope Automation", -1)
  reaper.UpdateArrange()
end

function ctrl.action_colorcode()
  M.log("Color coding tracks...", "accent")
  reaper.Undo_BeginBlock()
  local count = 0
  for i = 0, (reaper.CountTracks(0) or 0) - 1 do
    local tr = reaper.GetTrack(0, i)
    if tr then
      local _, name = reaper.GetTrackName(tr)
      local n = (name or ""):lower()
      for keyword, color in pairs(COLOR_DICT) do
        if n:find(keyword) then
          -- REAPER color format: 0x01BBGGRR (with 0x01 flag)
          local r_val = (color >> 16) & 0xFF
          local g_val = (color >> 8) & 0xFF
          local b_val = color & 0xFF
          local reaper_color = 0x01000000 | (b_val << 16) | (g_val << 8) | r_val
          reaper.SetTrackColor(tr, reaper_color)
          count = count + 1
          break
        end
      end
    end
  end
  reaper.Undo_EndBlock("Damei: Color Code Tracks", -1)
  reaper.TrackList_AdjustWindows(false)
  M.log(string.format("Colored %d tracks", count), "ok")
end

-- ── WORKFLOW AUTOMATION ACTIONS ──────────────────────────────────

function ctrl.action_import_files(files)
  -- Import dropped files into REAPER: create tracks, insert audio, name & color
  if not files or #files == 0 then return end
  M.log(string.format("Importing %d files...", #files), "accent")
  reaper.Undo_BeginBlock()
  reaper.PreventUIRefresh(1)

  local imported = 0
  for _, filepath in ipairs(files) do
    -- Only process audio files
    local ext = (filepath:match("%.(%w+)$") or ""):lower()
    if ext == "wav" or ext == "mp3" or ext == "flac" or ext == "aif" or ext == "aiff" or ext == "ogg" then
      -- Create a new track
      local idx = reaper.CountTracks(0)
      reaper.InsertTrackAtIndex(idx, false)
      local tr = reaper.GetTrack(0, idx)
      if tr then
        -- Name from filename (strip extension)
        local fname = filepath:match("([^/\\]+)$") or "Imported"
        local name = fname:match("(.+)%.") or fname
        reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", name, true)

        -- Insert media item on the track at position 0
        reaper.InsertMedia(filepath, 0)  -- mode 0 = add to current track

        -- Color code based on name
        local n_lower = name:lower()
        for keyword, color in pairs(COLOR_DICT) do
          if n_lower:find(keyword) then
            local r_val = (color >> 16) & 0xFF
            local g_val = (color >> 8) & 0xFF
            local b_val = color & 0xFF
            reaper.SetTrackColor(tr, 0x01000000 | (b_val << 16) | (g_val << 8) | r_val)
            break
          end
        end

        imported = imported + 1
      end
    end
  end

  reaper.PreventUIRefresh(-1)
  reaper.Undo_EndBlock("Damei: Import Audio Files", -1)
  reaper.TrackList_AdjustWindows(false)
  reaper.UpdateArrange()
  M.log(string.format("Imported %d audio files (named & colored)", imported), "ok")
  table.insert(st.auto_log, os.date("%H:%M:%S") .. string.format(" Imported %d files", imported))
  ctrl.action_scan()
end

function ctrl.action_route()
  M.log("Auto-routing tracks to folder buses...", "accent")
  reaper.Undo_BeginBlock()
  reaper.PreventUIRefresh(1)

  -- Define folder structure
  local folders = { "DRUMS", "BASS", "GUITARS", "VOCALS", "KEYS", "FX" }
  local folder_map = {
    DRUMS   = {"kick","snare","tom","hat","cymbal","drum","room","oh"},
    BASS    = {"bass"},
    GUITARS = {"guitar","gtr"},
    VOCALS  = {"vocal","vox"},
    KEYS    = {"synth","keys","piano"},
    FX      = {"reverb","delay","fx"},
  }

  -- Collect track assignments BEFORE creating folder tracks
  local assignments = {}  -- folder_name → { track_index, ... }
  for _, fname in ipairs(folders) do assignments[fname] = {} end

  for i = 0, reaper.CountTracks(0) - 1 do
    local tr = reaper.GetTrack(0, i)
    if tr then
      local _, name = reaper.GetTrackName(tr)
      local n = (name or ""):lower()
      for folder_name, keywords in pairs(folder_map) do
        local matched = false
        for _, kw in ipairs(keywords) do
          if n:find(kw) then
            table.insert(assignments[folder_name], i)
            matched = true
            break
          end
        end
        if matched then break end
      end
    end
  end

  -- Build the new track order: for each folder, insert folder track then children
  -- Use reorder approach: set folder depth correctly
  local created = 0
  local total_moved = 0
  for _, fname in ipairs(folders) do
    local children = assignments[fname]
    if #children > 0 then
      -- Create folder track
      reaper.InsertTrackAtIndex(reaper.CountTracks(0), false)
      local ft = reaper.GetTrack(0, reaper.CountTracks(0) - 1)
      reaper.GetSetMediaTrackInfo_String(ft, "P_NAME", fname, true)
      reaper.SetMediaTrackInfo_Value(ft, "I_FOLDERDEPTH", 1)  -- folder start
      -- Color the folder
      local col = COLOR_DICT[fname:lower()] or COLOR_DICT[children[1] and "" or ""]
      if col then
        local r_val = (col >> 16) & 0xFF
        local g_val = (col >> 8) & 0xFF
        local b_val = col & 0xFF
        reaper.SetTrackColor(ft, 0x01000000 | (b_val << 16) | (g_val << 8) | r_val)
      end
      created = created + 1
      total_moved = total_moved + #children
    end
  end

  reaper.PreventUIRefresh(-1)
  reaper.Undo_EndBlock("Damei: Auto-Route", -1)
  reaper.TrackList_AdjustWindows(false)
  M.log(string.format("Created %d folder buses for %d tracks", created, total_moved), "ok")
  table.insert(st.auto_log, os.date("%H:%M:%S") .. string.format(" Routed: %d folders, %d tracks", created, total_moved))
end

function ctrl.action_export()
  M.log("Batch exporting stems...", "accent")
  reaper.Undo_BeginBlock()

  -- Find all folder tracks (buses)
  local buses = {}
  for i = 0, (reaper.CountTracks(0) or 0) - 1 do
    local tr = reaper.GetTrack(0, i)
    if tr and reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH") == 1 then
      local _, name = reaper.GetTrackName(tr)
      table.insert(buses, { track = tr, name = name or ("Bus_" .. i) })
    end
  end

  if #buses == 0 then
    M.log("No folder buses found — route tracks first", "warn")
    -- Fallback to REAPER render dialog
    reaper.Main_OnCommand(41824, 0)
    reaper.Undo_EndBlock("Damei: Render", -1)
    return
  end

  -- Get project directory for stems output
  local _, proj_path = reaper.EnumProjects(-1)
  local proj_dir = proj_path and proj_path:match("(.+)[/\\]") or reaper.GetProjectPath()
  local stems_dir = proj_dir .. "/Stems"

  -- Create stems directory
  reaper.RecursiveCreateDirectory(stems_dir, 0)

  M.log(string.format("Found %d buses, exporting to %s", #buses, stems_dir), "accent")

  -- Use REAPER's render dialog with the current settings
  -- The user can configure render settings beforehand
  reaper.Main_OnCommand(41824, 0)  -- Render using most recent settings

  reaper.Undo_EndBlock("Damei: Export Stems", -1)
  table.insert(st.auto_log, os.date("%H:%M:%S") .. string.format(" Exported %d stems → %s", #buses, stems_dir))
end

function ctrl.action_solo_safe()
  M.log("Solo safe all buses...", "accent")
  reaper.Undo_BeginBlock()
  local count = 0
  for i = 0, (reaper.CountTracks(0) or 0) - 1 do
    local tr = reaper.GetTrack(0, i)
    if tr and reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH") == 1 then
      reaper.SetMediaTrackInfo_Value(tr, "B_SOLO_DEFEAT", 1)
      count = count + 1
    end
  end
  reaper.Undo_EndBlock("Damei: Solo Safe Buses", -1)
  M.log(string.format("Solo-safed %d folder tracks", count), "ok")
end

function ctrl.action_reset_faders()
  M.log("Resetting all faders to 0dB...", "accent")
  reaper.Undo_BeginBlock()
  for i = 0, (reaper.CountTracks(0) or 0) - 1 do
    local tr = reaper.GetTrack(0, i)
    if tr then reaper.SetMediaTrackInfo_Value(tr, "D_VOL", 1.0) end
  end
  reaper.Undo_EndBlock("Damei: Reset Faders", -1)
  M.log("All faders reset to 0dB", "ok")
  ctrl.action_scan()
end

function ctrl.action_remove_empty()
  M.log("Removing empty tracks...", "accent")
  reaper.Undo_BeginBlock()
  local removed = 0
  for i = reaper.CountTracks(0) - 1, 0, -1 do
    local tr = reaper.GetTrack(0, i)
    if tr and reaper.CountTrackMediaItems(tr) == 0
      and reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH") == 0 then
      reaper.DeleteTrack(tr)
      removed = removed + 1
    end
  end
  reaper.Undo_EndBlock("Damei: Remove Empty Tracks", -1)
  M.log(string.format("Removed %d empty tracks", removed), "ok")
  ctrl.action_scan()
end

-- ── FALSE STEREO TO MONO ───────────────────────────────────────

function ctrl.action_false_stereo()
  M.log("Detecting false stereo...", "accent")
  reaper.Undo_BeginBlock()
  reaper.PreventUIRefresh(1)

  local converted = 0
  local n_tracks = reaper.CountTracks(0) or 0
  for ti = 0, n_tracks - 1 do
    local tr = reaper.GetTrack(0, ti)
    if not tr then goto next_fs_track end

    local n_items = reaper.CountTrackMediaItems(tr)
    for ii = 0, n_items - 1 do
      local item = reaper.GetTrackMediaItem(tr, ii)
      if not item then goto next_fs_item end

      local take = reaper.GetActiveTake(item)
      if not take or reaper.TakeIsMIDI(take) then goto next_fs_item end

      -- Check channel count
      local source = reaper.GetMediaItemTake_Source(take)
      if not source then goto next_fs_item end
      local n_ch = reaper.GetMediaSourceNumChannels(source)
      if n_ch ~= 2 then goto next_fs_item end

      -- Already forced mono?
      local chan_mode = reaper.GetMediaItemTakeInfo_Value(take, "I_CHANMODE")
      if chan_mode ~= 0 then goto next_fs_item end

      -- Sample peaks for L and R
      local num_pts = 128
      local item_len = reaper.GetMediaItemInfo_Value(item, "D_LENGTH")
      if item_len <= 0 then goto next_fs_item end
      local peakrate = num_pts / item_len
      local buf = reaper.new_array(num_pts * 4)  -- 2 channels * 2 (max/min) per point
      local rv = reaper.GetMediaItemTake_Peaks(take, peakrate, 0, 2, num_pts, 0, buf)
      local actual = rv & 0xFFFFF

      if actual > 4 then
        -- Compare L and R channels
        local match = true
        local threshold = 0.001  -- tiny tolerance for floating point
        for pi = 0, actual - 1 do
          local l_val = math.abs(buf[pi + 1] or 0)
          local r_val = math.abs(buf[actual + pi + 1] or 0)
          if math.abs(l_val - r_val) > threshold then
            match = false
            break
          end
        end

        if match then
          -- Force to mono (channel mode 3 = mono downmix)
          reaper.SetMediaItemTakeInfo_Value(take, "I_CHANMODE", 3)
          converted = converted + 1
        end
      end
      ::next_fs_item::
    end
    ::next_fs_track::
  end

  reaper.PreventUIRefresh(-1)
  reaper.Undo_EndBlock("Damei: False Stereo to Mono", -1)
  reaper.UpdateArrange()
  M.log(string.format("Converted %d false-stereo items to mono", converted), "ok")
  table.insert(st.auto_log, os.date("%H:%M:%S") .. string.format(" Mono: %d items", converted))
end

-- ── STRIP SILENCE ──────────────────────────────────────────────

function ctrl.action_strip_silence(threshold_db)
  threshold_db = threshold_db or -60
  local threshold_lin = 10 ^ (threshold_db / 20)
  local min_silence = 0.5  -- seconds of silence before cutting
  M.log(string.format("Stripping silence below %.0f dB...", threshold_db), "accent")
  reaper.Undo_BeginBlock()
  reaper.PreventUIRefresh(1)

  local splits = 0
  local n_tracks = reaper.CountTracks(0) or 0
  for ti = 0, n_tracks - 1 do
    local tr = reaper.GetTrack(0, ti)
    if not tr then goto next_ss_track end

    -- Process items in reverse to avoid index shifting
    for ii = reaper.CountTrackMediaItems(tr) - 1, 0, -1 do
      local item = reaper.GetTrackMediaItem(tr, ii)
      if not item then goto next_ss_item end

      local take = reaper.GetActiveTake(item)
      if not take or reaper.TakeIsMIDI(take) then goto next_ss_item end

      local item_pos = reaper.GetMediaItemInfo_Value(item, "D_POSITION")
      local item_len = reaper.GetMediaItemInfo_Value(item, "D_LENGTH")
      if item_len <= 0 then goto next_ss_item end

      -- Sample 512 peaks across the item
      local num_pts = math.min(512, math.max(32, math.floor(item_len * 100)))
      local buf = reaper.new_array(num_pts * 2)
      local peakrate = num_pts / item_len
      local rv = reaper.GetMediaItemTake_Peaks(take, peakrate, 0, 1, num_pts, 0, buf)
      local actual = rv & 0xFFFFF

      if actual > 0 then
        local pt_dur = item_len / actual
        -- Find silent regions and split them out
        local in_silence = false
        local silence_start = 0

        for pi = 0, actual - 1 do
          local pk = math.abs(buf[pi + 1] or 0)
          local t = item_pos + pi * pt_dur

          if pk < threshold_lin then
            if not in_silence then
              in_silence = true
              silence_start = t
            end
          else
            if in_silence and (t - silence_start) > min_silence then
              -- Split at silence boundaries
              local split_item = reaper.SplitMediaItem(item, silence_start)
              if split_item then
                local end_item = reaper.SplitMediaItem(split_item, t)
                if end_item then
                  reaper.DeleteTrackMediaItem(tr, split_item)
                  splits = splits + 1
                end
              end
            end
            in_silence = false
          end
        end
      end
      ::next_ss_item::
    end
    ::next_ss_track::
  end

  reaper.PreventUIRefresh(-1)
  reaper.Undo_EndBlock("Damei: Strip Silence", -1)
  reaper.UpdateArrange()
  M.log(string.format("Stripped %d silent regions", splits), "ok")
  table.insert(st.auto_log, os.date("%H:%M:%S") .. string.format(" Strip: %d regions", splits))
end

-- ── STEM BATCH EXPORT ──────────────────────────────────────────

function ctrl.action_stem_export()
  M.log("Preparing stem export...", "accent")

  -- Get project path for output directory
  local _, proj_path = reaper.EnumProjects(-1)
  if not proj_path or #proj_path == 0 then
    M.log("Save your project first before exporting stems", "warn")
    return
  end

  local proj_dir = proj_path:match("(.+)[/\\]") or ""
  local proj_name = proj_path:match("([^/\\]+)%.RPP$") or "Project"
  local out_dir = proj_dir .. "/Damei_Bounces/" .. proj_name .. "_Stems"
  ensure_dir(out_dir)

  -- Set render output directory
  reaper.GetSetProjectInfo_String(0, "RENDER_FILE", out_dir:gsub("/", "\\"), true)

  -- Set render format to WAV 24-bit
  reaper.GetSetProjectInfo_String(0, "RENDER_FORMAT", "evaw", true)

  -- Set render to stems (selected tracks via render matrix)
  -- Source: 3 = Region render matrix, but for quick stems use 8 = Selected tracks (stems)
  reaper.GetSetProjectInfo(0, "RENDER_SETTINGS", 8, true)  -- stems via master mix

  -- Set bounds to entire project
  reaper.GetSetProjectInfo(0, "RENDER_BOUNDSFLAG", 0, true)  -- entire project

  -- Set tail
  reaper.GetSetProjectInfo(0, "RENDER_TAILFLAG", 0, true)

  -- Count folder tracks for feedback
  local n_buses = 0
  local n_tracks = reaper.CountTracks(0) or 0
  for i = 0, n_tracks - 1 do
    local tr = reaper.GetTrack(0, i)
    if tr and reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH") == 1 then
      n_buses = n_buses + 1
    end
  end

  -- Launch render dialog (action 42230 = File: Render project, using the last/current render settings)
  reaper.Main_OnCommand(42230, 0)
  M.log(string.format("Render dialog opened — %d buses, output: %s", n_buses, out_dir), "ok")
  table.insert(st.auto_log, os.date("%H:%M:%S") .. " Stems: render dialog opened")
end

function ctrl.action_label_tracks()
  M.log("Auto-labeling tracks from items...", "accent")
  reaper.Undo_BeginBlock()
  local labeled = 0
  for i = 0, (reaper.CountTracks(0) or 0) - 1 do
    local tr = reaper.GetTrack(0, i)
    if tr then
      local _, name = reaper.GetTrackName(tr)
      if name and name:match("^Track %d+$") then
        -- Try to name from first media item
        local item = reaper.GetTrackMediaItem(tr, 0)
        if item then
          local take = reaper.GetActiveTake(item)
          if take then
            local _, take_name = reaper.GetSetMediaItemTakeInfo_String(take, "P_NAME", "", false)
            if take_name and #take_name > 0 then
              reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", take_name, true)
              labeled = labeled + 1
            end
          end
        end
      end
    end
  end
  reaper.Undo_EndBlock("Damei: Label Tracks", -1)
  M.log(string.format("Labeled %d tracks from items", labeled), "ok")
  ctrl.action_scan()
end

-- ── AI ACTION VALIDATOR (GUARDRAILS) ──────────────────────────────

function ctrl.validate_track_index(idx)
  if type(idx) ~= "number" then
    M.log("Guardrail: AI returned non-numeric track index", "warn")
    return nil
  end
  idx = math.floor(idx)
  if idx < 0 or idx >= (reaper.CountTracks(0) or 0) then
    M.log(string.format("Guardrail: track index %d out of range (0-%d)", idx, (reaper.CountTracks(0) or 1) - 1), "warn")
    return nil
  end
  return idx
end

function ctrl.validate_time_range(t_start, t_end)
  if type(t_start) ~= "number" or type(t_end) ~= "number" then
    M.log("Guardrail: AI returned non-numeric time values", "warn")
    return nil, nil
  end
  if t_start < 0 then t_start = 0 end
  if t_end <= t_start then
    M.log("Guardrail: AI returned invalid time range (end <= start)", "warn")
    return nil, nil
  end
  -- Clamp to project length
  local proj_len = reaper.GetProjectLength(0)
  if proj_len > 0 and t_end > proj_len + 10 then
    M.log(string.format("Guardrail: AI time %.1fs exceeds project (%.1fs), clamping", t_end, proj_len), "warn")
    t_end = proj_len
  end
  return t_start, t_end
end

function ctrl.validate_db_value(db, min_db, max_db)
  min_db = min_db or -24
  max_db = max_db or 12
  if type(db) ~= "number" then
    M.log("Guardrail: AI returned non-numeric dB value", "warn")
    return nil
  end
  if db < min_db or db > max_db then
    M.log(string.format("Guardrail: AI dB value %.1f clamped to [%d, %d]", db, min_db, max_db), "warn")
    return math.max(min_db, math.min(max_db, db))
  end
  return db
end

-- Safe wrapper for AI-triggered actions

function ctrl.safe_ai_action(action_name, params)
  local ok, err = pcall(function()
    if action_name == "write_envelope" then
      local idx = ctrl.validate_track_index(params.track)
      if not idx then return end
      local t0, t1 = ctrl.validate_time_range(params.time_start, params.time_end)
      if not t0 then return end
      local db = ctrl.validate_db_value(params.db_change)
      if not db then return end
      ctrl.action_write_envelope(idx, t0, t1, db)
    elseif action_name == "clip_gain" then
      local db = ctrl.validate_db_value(params.target_dbfs, -30, 0)
      if not db then return end
      ctrl.action_clip_gain_stage(db)
    elseif action_name == "route" then
      ctrl.action_route()
    elseif action_name == "false_stereo" then
      ctrl.action_false_stereo()
    elseif action_name == "strip_silence" then
      local db = ctrl.validate_db_value(params.threshold_db, -80, -20)
      ctrl.action_strip_silence(db or -60)
    else
      M.log("Guardrail: unknown AI action '" .. tostring(action_name) .. "'", "warn")
    end
  end)
  if not ok then
    M.log("Guardrail: action crashed — " .. tostring(err), "err")
  end
end

-- ── AI CHAT ACTION + PROMPT ORCHESTRATOR ─────────────────────

-- ── DEEP SESSION SNAPSHOT (for code generation) ──────────────
-- Captures full REAPER state as structured text for the LLM

function ctrl.build_session_snapshot()
  local parts = {}
  local num_tracks = reaper.CountTracks(0) or 0

  -- Transport state
  local tempo = reaper.Master_GetTempo()
  local _, ts_num, ts_den = reaper.TimeMap_GetTimeSigAtTime(0, 0)
  local play_state = reaper.GetPlayState()
  local play_str = "stopped"
  if play_state == 1 then play_str = "playing"
  elseif play_state == 2 then play_str = "paused"
  elseif play_state == 4 then play_str = "recording"
  elseif play_state == 5 then play_str = "recording" end
  local cursor_pos = reaper.GetCursorPosition()
  local sel_start, sel_end = reaper.GetSet_LoopTimeRange2(0, false, false, 0, 0, false)

  table.insert(parts, string.format(
    "TRANSPORT: %.1f BPM, %d/%d, %s, cursor=%.2fs",
    tempo, ts_num or 4, ts_den or 4, play_str, cursor_pos
  ))
  if sel_end > sel_start then
    table.insert(parts, string.format("TIME SELECTION: %.2fs - %.2fs", sel_start, sel_end))
  end

  -- Project name
  local _, proj_path = reaper.EnumProjects(-1)
  local proj_name = ""
  if proj_path and #proj_path > 0 then
    proj_name = proj_path:match("([^/\\]+)%.RPP$") or proj_path:match("([^/\\]+)$") or ""
  end
  table.insert(parts, string.format("PROJECT: %s (%d tracks)", proj_name, num_tracks))

  -- Tracks (with FX chains, sends, mute/solo/arm, vol/pan)
  local track_lines = {}
  table.insert(track_lines, "[Idx|Name|Vol(dB)|Pan|Mute|Solo|Arm|Folder|FXCount|Selected]")
  for i = 0, math.min(num_tracks - 1, 99) do  -- cap at 100 tracks
    local tr = reaper.GetTrack(0, i)
    if tr then
      local _, tname = reaper.GetTrackName(tr)
      local vol = reaper.GetMediaTrackInfo_Value(tr, "D_VOL")
      local vol_db = 20 * math.log(vol, 10)
      if vol < 0.00001 then vol_db = -150 end
      local pan = reaper.GetMediaTrackInfo_Value(tr, "D_PAN")
      local mute = reaper.GetMediaTrackInfo_Value(tr, "B_MUTE") == 1 and "M" or "-"
      local solo = reaper.GetMediaTrackInfo_Value(tr, "I_SOLO") > 0 and "S" or "-"
      local arm = reaper.GetMediaTrackInfo_Value(tr, "I_RECARM") == 1 and "R" or "-"
      local folder = reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH")
      local folder_str = "-"
      if folder == 1 then folder_str = "FOLDER"
      elseif folder < 0 then folder_str = "END" end
      local fx_count = reaper.TrackFX_GetCount(tr) or 0
      local selected = reaper.IsTrackSelected(tr) and "SEL" or "-"

      table.insert(track_lines, string.format(
        "%d|%s|%.1f|%.2f|%s|%s|%s|%s|%d|%s",
        i + 1, tname, vol_db, pan, mute, solo, arm, folder_str, fx_count, selected
      ))
    end
  end
  if num_tracks > 100 then
    table.insert(track_lines, string.format("... (%d more tracks)", num_tracks - 100))
  end
  table.insert(parts, "TRACKS:\n" .. table.concat(track_lines, "\n"))

  -- FX chains (for tracks with FX)
  local fx_lines = {}
  for i = 0, math.min(num_tracks - 1, 49) do  -- cap at 50 tracks for FX
    local tr = reaper.GetTrack(0, i)
    if tr then
      local fx_count = reaper.TrackFX_GetCount(tr) or 0
      if fx_count > 0 then
        local _, tname = reaper.GetTrackName(tr)
        local fx_names = {}
        for f = 0, fx_count - 1 do
          local _, fxname = reaper.TrackFX_GetFXName(tr, f)
          local enabled = reaper.TrackFX_GetEnabled(tr, f)
          local status = enabled and "" or " [BYPASSED]"
          table.insert(fx_names, string.format("  %d: %s%s", f, fxname or "?", status))
        end
        table.insert(fx_lines, string.format("Track %d (%s):", i + 1, tname))
        for _, fn in ipairs(fx_names) do
          table.insert(fx_lines, fn)
        end
      end
    end
  end
  if #fx_lines > 0 then
    table.insert(parts, "FX CHAINS:\n" .. table.concat(fx_lines, "\n"))
  end

  -- Selected items
  local sel_items = reaper.CountSelectedMediaItems(0) or 0
  if sel_items > 0 then
    local item_lines = {}
    for i = 0, math.min(sel_items - 1, 19) do
      local item = reaper.GetSelectedMediaItem(0, i)
      if item then
        local pos = reaper.GetMediaItemInfo_Value(item, "D_POSITION")
        local len = reaper.GetMediaItemInfo_Value(item, "D_LENGTH")
        local take = reaper.GetActiveTake(item)
        local take_name = ""
        if take then _, take_name = reaper.GetSetMediaItemTakeInfo_String(take, "P_NAME", "", false) end
        local tr = reaper.GetMediaItemTrack(item)
        local _, tr_name = reaper.GetTrackName(tr)
        table.insert(item_lines, string.format(
          "  %s on '%s' at %.2fs (%.2fs long)",
          #take_name > 0 and take_name or "(unnamed)", tr_name, pos, len
        ))
      end
    end
    table.insert(parts, string.format("SELECTED ITEMS (%d):\n%s", sel_items, table.concat(item_lines, "\n")))
  end

  -- Markers and regions
  local num_markers = reaper.CountProjectMarkers(0) or 0
  if num_markers > 0 then
    local marker_lines = {}
    for i = 0, num_markers - 1 do
      local _, is_rgn, pos, rgnend, name, idx = reaper.EnumProjectMarkers(i)
      if is_rgn then
        table.insert(marker_lines, string.format("  Region %d: '%s' %.2fs-%.2fs", idx, name or "", pos, rgnend))
      else
        table.insert(marker_lines, string.format("  Marker %d: '%s' at %.2fs", idx, name or "", pos))
      end
    end
    table.insert(parts, "MARKERS/REGIONS:\n" .. table.concat(marker_lines, "\n"))
  end

  -- Sends (for selected or first 20 tracks)
  local send_lines = {}
  for i = 0, math.min(num_tracks - 1, 19) do
    local tr = reaper.GetTrack(0, i)
    if tr then
      local num_sends = reaper.GetTrackNumSends(tr, 0) -- 0 = sends
      if num_sends > 0 then
        local _, tname = reaper.GetTrackName(tr)
        for s = 0, num_sends - 1 do
          local dest = reaper.GetTrackSendInfo_Value(tr, 0, s, "P_DESTTRACK")
          if dest then
            local _, dname = reaper.GetTrackName(dest)
            local svol = reaper.GetTrackSendInfo_Value(tr, 0, s, "D_VOL")
            local svol_db = (svol and svol > 0.00001) and (20 * math.log(svol, 10)) or -150
            table.insert(send_lines, string.format("  %s -> %s (%.1fdB)", tname, dname or "?", svol_db))
          end
        end
      end
    end
  end
  if #send_lines > 0 then
    table.insert(parts, "SENDS:\n" .. table.concat(send_lines, "\n"))
  end

  -- Plugin inventory (already in M.plugin_inventory global)
  if M.plugin_inventory and #M.plugin_inventory > 0 then
    local plist = {}
    for i = 1, math.min(80, #M.plugin_inventory) do
      table.insert(plist, M.plugin_inventory[i])
    end
    table.insert(parts, "INSTALLED PLUGINS: " .. table.concat(plist, ", "))
  end

  return table.concat(parts, "\n\n")
end

-- Safe wrapper that won't crash if any REAPER API call fails

function ctrl.safe_session_snapshot()
  local ok, result = pcall(build_session_snapshot)
  if ok then return result end
  return "SESSION SNAPSHOT ERROR: " .. tostring(result)
end

-- Translates raw gmem floats into musical context the AI can reason about

function ctrl.build_ai_context()
  local parts = {}

  -- Song-first system instruction
  table.insert(parts, "SYSTEM: Analyze the song's intrinsic sonic properties. Do NOT assume a genre. Optimize for clarity, depth, and headroom relative to the song's own DNA.")
  table.insert(parts, "NLP: The user may make spelling errors or use conversational phrasing. Interpret their intent, correct spelling internally, and respond with precise technical audio advice. Never ask the user to rephrase.")

  -- Monitoring awareness
  local mon_names = {"studio monitors", "open-back headphones", "closed-back headphones"}
  local mon_name = mon_names[M.monitoring_setup] or "studio monitors"
  table.insert(parts, string.format("User is monitoring on %s.", mon_name))
  if M.monitoring_setup >= 2 then
    table.insert(parts, "HEADPHONE WARNING: Flag any aggressive wide-panning decisions or low-end buildup that might mask center-channel clarity on headphones.")
  end

  -- Advice style
  if M.advice_style == 1 then
    table.insert(parts, "Respond in direct, technical style. Be concise and actionable.")
  else
    table.insert(parts, "Respond in analytical, detailed style. Explain the reasoning behind each recommendation.")
  end

  -- Loudness assessment
  local lufs_diff = st.sm_lufs_i - M.TARGET_LUFS
  if st.sm_lufs_i > -60 then
    table.insert(parts, string.format(
      "Integrated loudness is %.1f LUFS (%.1f dB %s streaming target of %d LUFS).",
      st.sm_lufs_i, math.abs(lufs_diff),
      lufs_diff > 0 and "ABOVE" or "below", M.TARGET_LUFS
    ))
  end

  -- Song-first: Crest factor (dynamic range indicator)
  if st.sm_lufs_m > -60 and st.sm_lufs_s > -60 then
    local crest = st.sm_lufs_s - st.sm_lufs_m
    table.insert(parts, string.format("Crest factor (short-term minus momentary): %.1f dB.", crest))
    if crest < 2 then
      table.insert(parts, "Dynamic range is very compressed — transients may be lost.")
    elseif crest > 8 then
      table.insert(parts, "High dynamic range — may need bus compression for glue.")
    end
  end

  -- Song-first: Low-end energy ratio
  local sub_bass_energy = 0
  local total_energy = 0
  for i = 1, 8 do
    local lin = 10 ^ (st.sm_bands[i] / 20)
    total_energy = total_energy + lin
    if i <= 2 then sub_bass_energy = sub_bass_energy + lin end
  end
  if total_energy > 0 then
    local low_ratio = sub_bass_energy / total_energy * 100
    table.insert(parts, string.format("Low-end energy (sub+bass): %.0f%% of total spectral energy.", low_ratio))
    if low_ratio > 50 then
      table.insert(parts, "Mix is bottom-heavy. Consider high-passing or reducing sub energy.")
    elseif low_ratio < 15 then
      table.insert(parts, "Mix is thin in the low end.")
    end
  end

  -- True peak assessment
  local tp_max = math.max(st.sm_tp_l, st.sm_tp_r)
  if tp_max > M.TARGET_TP then
    table.insert(parts, string.format(
      "CLIPPING: True Peak %.1f dBTP exceeds %d dBTP limit.", tp_max, M.TARGET_TP))
  elseif tp_max > M.TARGET_TP - 2 then
    table.insert(parts, string.format(
      "True Peak %.1f dBTP, close to %d dBTP ceiling.", tp_max, M.TARGET_TP))
  else
    table.insert(parts, string.format("True Peak %.1f dBTP (safe).", tp_max))
  end

  -- Spectral balance assessment
  local band_labels = {"sub (63Hz)", "bass (125Hz)", "low-mid (250Hz)", "mid (500Hz)",
                       "upper-mid (1kHz)", "presence (2kHz)", "brilliance (4kHz)", "air (8kHz)"}
  local avg_band = 0
  for i = 1, 8 do avg_band = avg_band + st.sm_bands[i] end
  avg_band = avg_band / 8

  local spectral_issues = {}
  for i = 1, 8 do
    local diff = st.sm_bands[i] - avg_band
    if diff > 6 then
      table.insert(spectral_issues, string.format("%s +%.0fdB", band_labels[i], diff))
    elseif diff < -8 then
      table.insert(spectral_issues, string.format("%s %.0fdB", band_labels[i], diff))
    end
  end
  if #spectral_issues > 0 then
    table.insert(parts, "Spectral issues: " .. table.concat(spectral_issues, "; ") .. ".")
  else
    table.insert(parts, "Spectral balance is reasonably flat.")
  end

  -- Stereo assessment
  if st.sm_corr < 0 then
    table.insert(parts, string.format("PHASE WARNING: Stereo correlation %.2f (negative).", st.sm_corr))
  elseif st.sm_corr < 0.3 then
    table.insert(parts, string.format("Wide stereo (corr %.2f). Check mono compatibility.", st.sm_corr))
  end

  -- Session info
  table.insert(parts, string.format(
    "Session: %d tracks, %d hot (>-6dB), health %d%%.",
    st.track_count, st.hot_count, st.gain_health
  ))

  -- Visual metadata: project hierarchy (folders, colors, FX)
  if st.session_scanned and #st.tracks > 0 then
    local hierarchy = {}
    for _, t in ipairs(st.tracks) do
      local desc = t.name
      if t.is_folder then desc = "[BUS] " .. desc end
      if t.color and #t.color > 0 then desc = desc .. " (" .. t.color .. ")" end
      if t.fx and #t.fx > 0 then
        desc = desc .. " FX:[" .. table.concat(t.fx, ", ") .. "]"
      end
      table.insert(hierarchy, desc)
    end
    -- Limit to first 30 tracks for context size
    if #hierarchy > 30 then
      table.insert(parts, "PROJECT HIERARCHY (first 30): " ..
        table.concat(hierarchy, " | ", 1, 30) .. " | ... (" .. #hierarchy .. " total)")
    else
      table.insert(parts, "PROJECT HIERARCHY: " .. table.concat(hierarchy, " | "))
    end
  end

  -- Plugin inventory
  if #M.plugin_inventory > 0 then
    -- Send a subset to keep context manageable
    local plist = {}
    for i = 1, math.min(50, #M.plugin_inventory) do
      table.insert(plist, M.plugin_inventory[i])
    end
    table.insert(parts, "OWNED PLUGINS: " .. table.concat(plist, ", ") .. ". Recommend ONLY from this list.")
  end

  -- Reference track delta
  if ref.alive and ref.sm_lufs_i > -60 then
    table.insert(parts, "REFERENCE TRACK ACTIVE: " .. ref.name)
    local ref_parts = {}
    for i = 1, 8 do
      local delta = st.sm_bands[i] - ref.sm_bands[i]
      if math.abs(delta) > 2 then
        table.insert(ref_parts, string.format("%s %+.0fdB", band_labels[i], delta))
      end
    end
    if #ref_parts > 0 then
      table.insert(parts, "Mix vs Reference spectral delta: " .. table.concat(ref_parts, ", ") .. ".")
    end
    local lufs_d = st.sm_lufs_i - ref.sm_lufs_i
    table.insert(parts, string.format("LUFS delta: %+.1f (mix %s than reference).",
      lufs_d, lufs_d > 0 and "louder" or "quieter"))
  end

  -- Client notes
  if #st.client_notes > 3 then
    table.insert(parts, "CLIENT NOTES: " .. st.client_notes)
  end

  -- ── ENGINEER PROFILE INJECTION ──────────────────────────────
  if M.active_profile_idx > 1 and M.engineer_profiles[M.active_profile_idx] then
    local prof = M.engineer_profiles[M.active_profile_idx].data
    if prof then
      -- Extract name from _meta.engineer (style_presets) or engineer_name (custom)
      local eng_display = (prof._meta and prof._meta.engineer) or prof.engineer_name or "Unknown"
      table.insert(parts, string.format(
        "ACTIVE ENGINEER EMULATION: You must strictly emulate the mixing style, tool preferences, and structural philosophy of %s.",
        eng_display))

      -- Style presets format: _meta block has description and signature_traits
      if prof._meta then
        if prof._meta.description then
          table.insert(parts, "SONIC PHILOSOPHY: " .. prof._meta.description)
        end
        if prof._meta.genre then
          table.insert(parts, "GENRE SPECIALIZATION: " .. prof._meta.genre)
        end
        if prof._meta.signature_traits then
          table.insert(parts, "SIGNATURE TRAITS: " .. table.concat(prof._meta.signature_traits, " | "))
        end
      elseif prof.sonic_philosophy then
        -- Custom profile format
        table.insert(parts, "SONIC PHILOSOPHY: " .. prof.sonic_philosophy)
      end

      -- Workflow notes (style_presets format)
      if prof.workflow_notes then
        table.insert(parts, "WORKFLOW RULES: " .. table.concat(prof.workflow_notes, " | "))
      end

      -- Gain staging preferences
      if prof.gain_staging_preference then
        local gs = prof.gain_staging_preference
        if gs.headroom_target_db then
          table.insert(parts, string.format("HEADROOM TARGET: %d dBFS.", gs.headroom_target_db))
        end
        if gs.vocal_preeminence_db then
          table.insert(parts, string.format("VOCAL PREEMINENCE: +%.1f dB above other elements.", gs.vocal_preeminence_db))
        end
        if gs.master_target_lufs then
          table.insert(parts, string.format("MASTER LUFS TARGET: %d LUFS (override default).", gs.master_target_lufs))
        end
      end

      -- Preferred processors → cross-reference with owned plugins
      if prof.preferred_processors then
        local prefs = {}
        for category, plugins in pairs(prof.preferred_processors) do
          if type(plugins) == "table" then
            -- Cross-reference with owned plugins
            local owned_matches = {}
            for _, pname in ipairs(plugins) do
              -- Check if user owns this plugin (fuzzy match)
              for _, owned in ipairs(M.plugin_inventory) do
                if owned:lower():find(pname:lower():sub(1, 8), 1, true) then
                  table.insert(owned_matches, pname .. " [OWNED]")
                  goto next_pref
                end
              end
              table.insert(owned_matches, pname .. " [NOT OWNED]")
              ::next_pref::
            end
            table.insert(prefs, category:upper() .. ": " .. table.concat(owned_matches, ", "))
          end
        end
        if #prefs > 0 then
          table.insert(parts, "PREFERRED PROCESSORS: " .. table.concat(prefs, "; ") ..
            ". Use OWNED plugins first, suggest alternatives for NOT OWNED.")
        end
      end

      -- Routing macros
      if prof.routing_macros then
        local macros = {}
        for macro, enabled in pairs(prof.routing_macros) do
          if enabled then table.insert(macros, macro:gsub("_", " ")) end
        end
        if #macros > 0 then
          table.insert(parts, "ROUTING MACROS TO APPLY: " .. table.concat(macros, ", ") .. ".")
        end
      end

      -- Mixing rules
      if prof.mixing_rules then
        table.insert(parts, "MIXING RULES: " .. table.concat(prof.mixing_rules, " | "))
      end
    end
  end

  -- ── STRUCTURED PROJECT METADATA ─────────────────────────────
  -- Build a concise project identity block
  local _, proj_path = reaper.EnumProjects(-1)
  local proj_name = ""
  if proj_path and #proj_path > 0 then
    proj_name = proj_path:match("([^/\\]+)%.RPP$") or proj_path:match("([^/\\]+)$") or ""
  end

  local tempo = reaper.Master_GetTempo()
  local _, ts_num, ts_den = reaper.TimeMap_GetTimeSigAtTime(0, 0)

  -- Detect buses
  local buses_detected = {}
  for i = 0, (reaper.CountTracks(0) or 1) - 1 do
    local tr = reaper.GetTrack(0, i)
    if tr and reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH") == 1 then
      local _, bname = reaper.GetTrackName(tr)
      table.insert(buses_detected, bname or "Bus")
    end
  end

  table.insert(parts, string.format(
    "PROJECT IDENTITY: '%s' at %.0f BPM, %d/%d time sig, %d tracks, %d hot (>-6dB), health %d%%, buses: [%s].",
    proj_name, tempo, ts_num or 4, ts_den or 4,
    st.track_count, st.hot_count, st.gain_health,
    #buses_detected > 0 and table.concat(buses_detected, ", ") or "none"
  ))

  return table.concat(parts, " ")
end

function ctrl.action_chat(prompt)
  table.insert(st.chat_log, { role = "user", text = prompt })

  -- Build intelligent context using prompt orchestrator
  local context = ctrl.build_ai_context()

  -- Determine active engineer name for backend
  local eng_name = "nolly"  -- default
  if M.active_profile_idx > 1 and M.engineer_profiles[M.active_profile_idx] then
    local prof = M.engineer_profiles[M.active_profile_idx]
    -- Extract the raw engineer name (strip category tag)
    eng_name = (prof.name or "nolly"):gsub("%s*%[.+%]$", ""):lower():gsub("%s+", "_")
  end

  -- Escape for JSON
  local safe_prompt = prompt:gsub('\\', '\\\\'):gsub('"', '\\"'):gsub("\n", "\\n")
  local safe_context = context:gsub('\\', '\\\\'):gsub('"', '\\"'):gsub("\n", "\\n")
  local safe_eng = eng_name:gsub('"', '')

  -- Build proper request body matching the backend API
  local body = string.format(
    '{"query": "%s", "engineer": "%s", "context": "%s", "conversation_id": "%s"}',
    safe_prompt, safe_eng, safe_context, st.project_name or "default"
  )

  table.insert(st.chat_log, { role = "system", text = "Thinking..." })
  M.log("AI: " .. prompt:sub(1, 40) .. "...", "accent")

  -- Route through Hermes or DameiAPI based on settings toggle
  local api_url = M.use_hermes and M.HERMES_MCP_URL or M.DAMEI_URL
  ctrl.http_post(api_url .. "/coaching/ask", body, function(r)
    -- Remove "Thinking..."
    for i = #st.chat_log, 1, -1 do
      if st.chat_log[i].role == "system" and st.chat_log[i].text == "Thinking..." then
        table.remove(st.chat_log, i)
        break
      end
    end

    if not r then
      local backend = M.use_hermes and "Hermes MCP" or "DameiAPI"
      table.insert(st.chat_log, { role = "assistant", text = "Sorry, I couldn't reach " .. backend .. ". Check if the server is running." })
      M.log("AI: failed to reach " .. backend, "err")
      return
    end

    -- Extract response (try multiple field names for compatibility)
    local answer = r:match('"answer"%s*:%s*"([^"]*)"')
      or r:match('"response"%s*:%s*"([^"]*)"')
      or r:match('"text"%s*:%s*"([^"]*)"')
      or "I received your question but couldn't parse the response."

    -- Unescape all JSON escape sequences properly
    answer = answer:gsub('\\\\', '\x00BSLASH\x00')  -- protect literal backslashes first
      :gsub('\\n', '\n')
      :gsub('\\t', '\t')
      :gsub('\\"', '"')
      :gsub('\\/', '/')
      :gsub('\x00BSLASH\x00', '\\')
    table.insert(st.chat_log, { role = "assistant", text = answer })
    M.log("AI: response received", "ok")

    -- Auto-save after each AI response
    ctrl.save_project_state()
  end)
end


-- Action: generate code via DameiAPI /reaper/generate-code

function ctrl.action_codegen(prompt)
  table.insert(st.chat_log, { role = "user", text = prompt })
  table.insert(st.chat_log, { role = "system", text = "Generating script..." })
  M.log("CodeGen: " .. prompt:sub(1, 40) .. "...", "accent")

  -- Build deep session snapshot (crash-safe)
  local snapshot = ctrl.safe_session_snapshot()

  -- Escape for JSON
  local safe_prompt = prompt:gsub('\\', '\\\\'):gsub('"', '\\"'):gsub("\n", "\\n")
  local safe_snapshot = snapshot:gsub('\\', '\\\\'):gsub('"', '\\"'):gsub("\n", "\\n")

  local body = string.format(
    '{"message": "%s", "session_context": "%s", "plugin_params": "", "conversation_history": []}',
    safe_prompt, safe_snapshot
  )

  ctrl.http_post(M.DAMEI_URL .. "/reaper/generate-code", body, function(r)
    -- Remove "Generating script..."
    for i = #st.chat_log, 1, -1 do
      if st.chat_log[i].role == "system" and st.chat_log[i].text == "Generating script..." then
        table.remove(st.chat_log, i)
        break
      end
    end

    if not r then
      table.insert(st.chat_log, { role = "assistant", text = "Could not reach DameiAPI for code generation." })
      M.log("CodeGen: failed to reach DameiAPI", "err")
      return
    end

    -- Parse response
    local explanation = r:match('"explanation"%s*:%s*"([^"]*)"') or ""
    local code = r:match('"code"%s*:%s*"([^"]*)"')
    local has_code_str = r:match('"has_code"%s*:%s*(%w+)') or "false"
    local has_code = has_code_str == "true"

    explanation = explanation:gsub("\\n", "\n"):gsub('\\"', '"')

    if has_code and code then
      code = code:gsub("\\n", "\n"):gsub('\\"', '"'):gsub("\\\\", "\\")

      -- Safety scan
      local warnings = M.scan_lua_safety(code)

      -- Store pending code for preview
      st.pending_code = {
        code = code,
        explanation = explanation,
        warnings = warnings,
      }

      if #warnings > 0 then
        table.insert(st.chat_log, { role = "assistant",
          text = explanation .. "\n\nâš ï¸ SAFETY BLOCKED: " .. table.concat(warnings, ", ") })
      else
        table.insert(st.chat_log, { role = "assistant",
          text = explanation .. "\n\n📋 Script ready — use the buttons below to Run, Copy, or dismiss." })

        -- Auto-run if enabled
        if st.code_auto_run then
          local ok, result = execute_lua_code(code, explanation:sub(1, 60))
          table.insert(st.chat_log, { role = "system", text = result })
          st.pending_code = nil
        end
      end
    else
      -- No code generated — just an explanation/question
      table.insert(st.chat_log, { role = "assistant", text = explanation })
    end

    M.log("CodeGen: response received", "ok")
    ctrl.save_project_state()
  end)
end

-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
-- MAIN LOOP
-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

-- Adaptive frame throttle
local frame_counter = 0
local gmem_skip_rate = 1  -- read gmem every N frames (1=every frame)

-- ── PHASE 5: SESSION-AWARE AUTO-ROUTING ──────────────────────────────
-- Detect unrouted tracks and create bus sends automatically
function ctrl.auto_route_to_buses()
  return ctrl.with_undo("Auto-Route to Buses", function()
    local n = reaper.CountTracks(0)
    if n == 0 then
      M.log("No tracks to route", "warn")
      return
    end

    -- Find or create category buses
    local buses = {}  -- category -> track
    local categories = {"Drums", "Bass", "Guitars", "Vocals", "Keys"}
    
    -- Check existing folder tracks
    for i = 0, n - 1 do
      local tr = reaper.GetTrack(0, i)
      local _, name = reaper.GetTrackName(tr)
      local is_folder = reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH") > 0
      if is_folder then
        local cat, _ = M.classify(name)
        if cat ~= "—" then buses[cat] = tr end
      end
    end

    -- Create missing buses
    for _, cat in ipairs(categories) do
      if not buses[cat] then
        reaper.InsertTrackAtIndex(n, false)
        local bus = reaper.GetTrack(0, n)
        reaper.GetSetMediaTrackInfo_String(bus, "P_NAME", cat .. " Bus", true)
        reaper.SetMediaTrackInfo_Value(bus, "I_FOLDERDEPTH", 1)
        buses[cat] = bus
        n = n + 1
        M.log("Created bus: " .. cat, "ok")
      end
    end

    -- Route unrouted tracks to their category bus
    local routed = 0
    for i = 0, n - 1 do
      local tr = reaper.GetTrack(0, i)
      local _, name = reaper.GetTrackName(tr)
      local cat, _ = M.classify(name)
      
      -- Skip buses themselves and already-routed tracks
      if cat ~= "—" and buses[cat] and tr ~= buses[cat] then
        local send_count = reaper.GetTrackNumSends(tr, 0)
        local has_send = false
        for s = 0, send_count - 1 do
          local dest = reaper.GetTrackSendInfo_Value(tr, 0, s, "P_DESTTRACK")
          if dest == buses[cat] then has_send = true; break end
        end
        if not has_send then
          reaper.CreateTrackSend(tr, buses[cat])
          routed = routed + 1
        end
      end
    end
    M.log(string.format("Auto-routed %d tracks to buses", routed), "ok")
  end)
end

-- ── PHASE 5: CROSS-TRACK MASKING DETECTION ──────────────────────────
-- Identifies frequency collisions between tracks using gmem spectral data
function ctrl.detect_masking()
  -- Build per-category spectral profiles from current gmem data
  local profiles = {}  -- category -> {bands}
  for _, t in ipairs(st.tracks or {}) do
    local cat = t.category
    if cat and cat ~= "—" then
      if not profiles[cat] then profiles[cat] = {0,0,0,0,0,0,0,0} end
      -- Aggregate energy (simplified — real version uses per-track FFT)
      for b = 1, 8 do
        profiles[cat][b] = profiles[cat][b] + (st.bands[b] or -100) / math.max(1, st.track_count)
      end
    end
  end

  -- Detect collisions: frequency bands where two categories both exceed -20dB
  local collisions = {}
  local cats = {}
  for cat, _ in pairs(profiles) do table.insert(cats, cat) end
  table.sort(cats)
  
  for i = 1, #cats do
    for j = i + 1, #cats do
      local a, b = cats[i], cats[j]
      for band = 1, 8 do
        if profiles[a][band] > -20 and profiles[b][band] > -20 then
          table.insert(collisions, {
            cat_a = a, cat_b = b,
            band = band, band_label = M.SP_LABELS[band],
            energy_a = profiles[a][band],
            energy_b = profiles[b][band],
          })
        end
      end
    end
  end

  if #collisions > 0 then
    M.log(string.format("Detected %d masking collisions", #collisions), "warn")
    st.masking_collisions = collisions
  else
    M.log("No masking collisions detected", "ok")
    st.masking_collisions = {}
  end
  return collisions
end

-- ── PHASE 5: PROJECT TEMPLATE APPLICATION ───────────────────────────
-- Save/load entire routing + FX chain templates via state chunks
function ctrl.save_project_template(name)
  local template_dir = (os.getenv("APPDATA") or "") .. "/Damei/templates"
  local path = template_dir .. "/" .. name .. ".json"
  
  -- Serialize all track state chunks
  local chunks = {}
  local n = reaper.CountTracks(0)
  for i = 0, n - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, chunk = reaper.GetTrackStateChunk(tr, "", false)
    local _, track_name = reaper.GetTrackName(tr)
    table.insert(chunks, {
      name = track_name,
      chunk = chunk,
    })
  end
  
  -- Write as JSON
  local parts = {}
  for _, c in ipairs(chunks) do
    table.insert(parts, string.format('{"name":%s,"chunk":%s}',
      M.json_encode_str(c.name), M.json_encode_str(c.chunk)))
  end
  local json = '{"tracks":[' .. table.concat(parts, ",") .. ']}'
  
  local f = io.open(path, "w")
  if f then
    f:write(json); f:close()
    M.log("Saved template: " .. name, "ok")
  else
    M.log("Failed to save template", "err")
  end
end


-- ============================================================================
-- Item 4 (Missing Layer 2): One-Click Sidechain Routing Helper
-- Routes src_track Ch 1/2 -> dst_track Ch 3/4 with automatic channel expansion.
-- Use for: Damei_TonalBalance vocal SC, Damei_SpectralUnmask SC input.
-- ============================================================================
function ctrl.route_sidechain(src_track, dst_track)
  if not reaper.ValidatePtr(src_track, "MediaTrack*") or
     not reaper.ValidatePtr(dst_track, "MediaTrack*") then
    M.log("route_sidechain: invalid track pointer", "err")
    return false
  end

  -- Ensure destination track has at least 4 channels
  local ch = reaper.GetMediaTrackInfo_Value(dst_track, "I_NCHAN")
  if ch < 4 then
    reaper.SetMediaTrackInfo_Value(dst_track, "I_NCHAN", 4)
  end

  -- Check for existing send to avoid duplicates
  local n_sends = reaper.GetTrackNumSends(src_track, 0)
  for s = 0, n_sends - 1 do
    local dest = reaper.GetTrackSendInfo_Value(src_track, 0, s, "P_DESTTRACK")
    if dest == dst_track then
      local dst_ch = reaper.GetTrackSendInfo_Value(src_track, 0, s, "I_DSTCHAN")
      if dst_ch == 2 then
        M.log("route_sidechain: send already exists", "info")
        return true
      end
    end
  end

  -- Create the send: src Ch 1/2 -> dst Ch 3/4
  local send_idx = reaper.CreateTrackSend(src_track, dst_track)
  -- I_SRCCHAN: 0 = Ch 1/2 (stereo pair)
  reaper.SetTrackSendInfo_Value(src_track, 0, send_idx, "I_SRCCHAN", 0)
  -- I_DSTCHAN: 2 = Ch 3/4
  reaper.SetTrackSendInfo_Value(src_track, 0, send_idx, "I_DSTCHAN", 2)
  reaper.SetTrackSendInfo_Value(src_track, 0, send_idx, "D_VOL", 1.0)

  local src_name = select(2, reaper.GetTrackName(src_track))
  local dst_name = select(2, reaper.GetTrackName(dst_track))
  M.log(string.format("Sidechain routed: [%s] Ch1/2 -> [%s] Ch3/4", src_name, dst_name), "ok")
  reaper.UpdateArrange()
  return true
end

return ctrl

