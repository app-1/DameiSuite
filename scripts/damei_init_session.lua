-- ============================================================================
-- Damei Mix Assistant -- One-Click Session Initializer & Provisioner
-- File: damei_init_session.lua
-- Location: %APPDATA%/REAPER/Scripts/Damei/damei_init_session.lua
-- Role: Automated Master Bus staging, Relay slot auto-addressing & bootstrap
-- ============================================================================
-- Keybind: Ctrl+Shift+D  (assign in REAPER Action List)
--
-- What this script does on each run (fully idempotent):
--   1. stage_master_bus()       : Audits the Master Track FX chain and
--                                 reorders/inserts the 7 required plugins in
--                                 the correct sequence. Uses a two-pass index-
--                                 stable algorithm that collects positions
--                                 first, then moves from high->low index.
--   2. provision_track_relays() : Scans all audio tracks (skips Master Track),
--                                 mounts Damei_Relay.jsfx on any unequipped
--                                 track, and assigns sequential gmem telemetry
--                                 slots (0..309). Already-assigned slots are
--                                 not clobbered (idempotent re-run safety).
--   3. launch_dtb()             : Opens damei_tbc.lua as independent action via AddRemoveReaScript to start
--                                 the master mix controller.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. MASTER BUS CHAIN SPECIFICATION
-- Target order: TonalBalance -> ReEQ -> BassFocus -> MultibandSplit ->
--               Clipper -> ReaLimit -> Metering
-- ----------------------------------------------------------------------------
local CHAIN = {
  -- patterns: fuzzy case-insensitive matches against TrackFX_GetFXName() output
  -- add_name: path for TrackFX_AddByName (relative to Effects/ directory)
  {
    patterns = { "tonal balance", "tonalbalance", "damei_tonalbalance" },
    add_name = "Damei/Damei_TonalBalance.jsfx",
  },
  {
    patterns = { "reeq", "reaeq" },
    add_name = "ReaEQ",      fallback = "VST: ReaEQ",
  },
  {
    patterns = { "bass focus", "bassfocus", "damei_bassfocus" },
    add_name = "Damei/Damei_BassFocus.jsfx",
  },
  {
    patterns = { "multiband split", "multibandsplit", "damei_multibandsplit" },
    add_name = "Damei/Damei_MultibandSplit.jsfx",
  },
  {
    patterns = { "damei clipper", "damei_clipper" },
    add_name = "Damei/Damei_Clipper.jsfx",
  },
  {
    patterns = { "realimit", "rea limit" },
    add_name = "VST: ReaLimit", fallback = "ReaLimit",
  },
  {
    patterns = { "damei metering", "damei_metering" },
    add_name = "Damei/Damei_Metering.jsfx",
  },
}

local LOG = {}  -- Accumulates log lines; flushed to ShowConsoleMsg at end

local function log(msg) LOG[#LOG + 1] = msg end

-- ----------------------------------------------------------------------------
-- UTILITY: Locate FX on a track by partial ident (case-insensitive literal)
-- Returns: 0-based FX index, or -1 if not found
-- ----------------------------------------------------------------------------
-- Locate FX by any of several fuzzy patterns (handles descriptive vs filename names).
-- REAPER returns descriptive names like 'JS: Damei Tonal Balance - 256-bin...'
-- not filenames, so single-string ident matching is fragile.
local function find_fx(track, patterns_or_str)
  local patterns = type(patterns_or_str) == "table"
                   and patterns_or_str
                   or  { tostring(patterns_or_str) }
  local count = reaper.TrackFX_GetCount(track)
  for f = 0, count - 1 do
    local _, name = reaper.TrackFX_GetFXName(track, f, "")
    local lname = name:lower()
    for _, pat in ipairs(patterns) do
      if lname:find(pat:lower(), 1, true) then return f, name end
    end
  end
  return -1, nil
end

-- Tolerant add: tries subfolder path, then JS: prefixed, then fallback
local function add_tolerant(track, add_name, fallback, pos)
  local idx = reaper.TrackFX_AddByName(track, add_name, false, pos)
  if idx ~= -1 then return idx end
  -- Try without 'JS: ' prefix (REAPER sometimes needs bare path)
  local bare = add_name:gsub("^JS: ", "")
  if bare ~= add_name then
    idx = reaper.TrackFX_AddByName(track, bare, false, pos)
    if idx ~= -1 then return idx end
  end
  if fallback then
    idx = reaper.TrackFX_AddByName(track, fallback, false, pos)
  end
  return idx or -1
end

-- ----------------------------------------------------------------------------
-- PHASE 1: MASTER BUS STAGING
-- Algorithm: two-pass, index-stable
--   Pass A: Collect current positions of all 7 chain plugins.
--   Pass B: Process each target slot in REVERSE order to avoid index shifts.
--           If a plugin is found at a wrong position, use TrackFX_CopyToTrack
--           with move=true to relocate it.  If not found, insert it.
-- ----------------------------------------------------------------------------
local function stage_master_bus()
  log("── Master Bus Chain ──────────────────────────")
  local master = reaper.GetMasterTrack(0)
  reaper.PreventUIRefresh(1)

  -- Pass A: snapshot current FX positions
  local current_pos = {}  -- current_pos[chain_idx] = fx_slot or -1
  for i, spec in ipairs(CHAIN) do
    current_pos[i] = find_fx(master, spec.patterns)
  end

  -- Pass B: process in REVERSE so high-index moves don't shift lower targets
  for i = #CHAIN, 1, -1 do
    local spec     = CHAIN[i]
    local want_pos = i - 1          -- 0-based target position in the chain
    local have_pos = current_pos[i]

    if have_pos == -1 then
      -- Plugin not present: insert at target position
      local ok = add_tolerant(master, spec.add_name, spec.fallback, want_pos)
      if ok == -1 and spec.fallback then
        -- (fallback handled inside add_tolerant)
      end
      if ok ~= -1 then
        log(string.format("  [ADD] %s  at slot %d", spec.add_name, want_pos))
      else
        log(string.format("  [ERR] Could not add %s (not installed?)", spec.add_name))
      end

    elseif have_pos ~= want_pos then
      -- Plugin present but misaligned: move to correct slot
      -- TrackFX_CopyToTrack(src_tr, src_idx, dst_tr, dst_idx, move)
      reaper.TrackFX_CopyToTrack(master, have_pos, master, want_pos, true)
      log(string.format("  [MOV] %s  %d -> %d", spec.add_name, have_pos, want_pos))

    else
      log(string.format("  [OK ] %s  at slot %d", spec.add_name, want_pos))
    end
  end

  reaper.PreventUIRefresh(-1)
  reaper.TrackList_AdjustWindows(false)
end

-- ----------------------------------------------------------------------------
-- PHASE 2: TRACK RELAY PROVISIONING
-- For each audio track (Master Track explicitly excluded):
--   a) If Damei_Relay.jsfx is absent: insert at FX chain position 0.
--   b) Read the current telemetry slot from slider6 (param index 5).
--   c) If slot is unassigned (< 0, > 309, or conflicts already seen),
--      assign the next sequential slot.  Otherwise keep existing slot.
-- Returns: number of tracks processed
-- ----------------------------------------------------------------------------
local function provision_track_relays()
  -- Guard: skip entirely if Damei_Relay.jsfx does not exist on this system.
  -- TonalBalance works standalone and does not require Relay for core features.
  local _rp = reaper.GetResourcePath()
  local _rf = io.open(_rp .. '/Effects/Damei/Damei_Relay.jsfx', 'r')
  if not _rf then
    table.insert(log_lines or LOG, '[INFO] Damei_Relay.jsfx not present -- skipping relay provisioning.')
    table.insert(log_lines or LOG, '[INFO] Tonal Balance runs standalone. Relay only needed for Visual Mixer.')
    return 0
  end
  _rf:close()
  log("── Track Relay Provisioning ──────────────────")
  local master      = reaper.GetMasterTrack(0)
  local track_count = reaper.CountTracks(0)
  if track_count == 0 then
    log("  No audio tracks found.")
    return 0
  end

  reaper.PreventUIRefresh(1)

  local slots_seen  = {}  -- tracks assigned slots -> avoid duplicates
  local next_slot   = 0   -- sequential slot counter for new assignments
  local provisioned = 0

  for t = 0, track_count - 1 do
    local tr = reaper.GetTrack(0, t)

    -- Skip Master Track (safety guard -- should never appear in CountTracks,
    -- but explicit check is cheap and defensive)
    if tr == master then goto continue end

    local relay_idx = find_fx(tr, "Damei_Relay")

    if relay_idx == -1 then
      -- Mount relay as first plugin in the FX chain (pre-trim position)
      relay_idx = reaper.TrackFX_AddByName(tr, "Damei/Damei_Relay.jsfx", false, 0)
      if relay_idx == -1 then
        log(string.format("  [ERR] Track %d: Damei_Relay.jsfx not installed", t + 1))
        goto continue
      end
      log(string.format("  [ADD] Track %d: relay mounted", t + 1))
    end

    -- Read currently assigned slot (param 5 = slider6, 0-based API index)
    local current_slot_v = reaper.TrackFX_GetParam(tr, relay_idx, 5)
    local current_slot   = math.floor(current_slot_v + 0.5)

    -- Idempotency: keep slot if it's valid and not duplicated in this session
    local slot_valid = (current_slot >= 0) and (current_slot <= 309)
                        and not slots_seen[current_slot]

    if slot_valid then
      -- Slot already correctly assigned from a prior run
      slots_seen[current_slot] = true
      -- Advance next_slot past any pre-existing assignments
      if current_slot >= next_slot then next_slot = current_slot + 1 end
      log(string.format("  [OK ] Track %d: slot %d (kept)", t + 1, current_slot))
    else
      -- Assign next available sequential slot
      while slots_seen[next_slot] do next_slot = next_slot + 1 end
      if next_slot > 309 then
        log(string.format("  [ERR] Track %d: slot pool exhausted (>309)", t + 1))
        goto continue
      end
      reaper.TrackFX_SetParam(tr, relay_idx, 5, next_slot)
      -- Also update slider7 (relay active flag, param index 6) to 1 (active)
      reaper.TrackFX_SetParam(tr, relay_idx, 6, 1)
      slots_seen[next_slot] = true
      log(string.format("  [SET] Track %d: slot %d (new)", t + 1, next_slot))
      next_slot = next_slot + 1
    end

    provisioned = provisioned + 1
    ::continue::
  end

  reaper.PreventUIRefresh(-1)
  reaper.TrackList_AdjustWindows(false)

  log(string.format("  %d track(s) provisioned across %d available slots.",
      provisioned, next_slot))
  return provisioned
end

-- ----------------------------------------------------------------------------
-- PHASE 3: LAUNCH DTB MASTER CONTROLLER
-- Uses dofile() into REAPER's main Lua context so that the dtb defer() loop
-- registers correctly. Validates path before execution.
-- ----------------------------------------------------------------------------
local function launch_dtb()
  log("-- DTB Launch --")
  local tbc_path = reaper.GetResourcePath() .. "/Scripts/Damei/damei_tbc.lua"

  -- Verify the script exists before registering
  local f = io.open(tbc_path, "r")
  if not f then
    log("  [ERR] damei_tbc.lua not found at: " .. tbc_path)
    return
  end
  f:close()

  -- Register as independent REAPER action and launch in its own thread.
  -- Using dofile() would run DTB inside this script's context: when
  -- damei_init_session.lua exits, REAPER destroys the ImGui_Context*,
  -- causing 'expected a valid ImGui_Context*' on the next defer tick.
  local cmd_id = reaper.AddRemoveReaScript(true, 0, tbc_path, true)
  if cmd_id and cmd_id > 0 then
    reaper.Main_OnCommand(cmd_id, 0)
    log("  [OK ] damei_tbc.lua launched as independent action (cmd " .. tostring(cmd_id) .. ").")
  else
    -- Registration failed (REAPER version too old or path issue); log and abort.
    log("  [ERR] AddRemoveReaScript failed -- damei_tbc.lua not launched.")
    log("        Workaround: open Actions > Show Action List > load damei_tbc.lua manually.")
  end
end

-- ----------------------------------------------------------------------------
-- ENTRY POINT
-- ----------------------------------------------------------------------------
reaper.Undo_BeginBlock2(0)

log("╔══════════════════════════════════════════════")
log("║  Damei Mix Assistant — Session Initializer")
log("╚══════════════════════════════════════════════")
log("")

stage_master_bus()
log("")
local provisioned_count = provision_track_relays()
log("")
launch_dtb()

reaper.Undo_EndBlock2(0, "Damei: Initialize Session & Stage Master Bus", -1)

-- Flush log to REAPER console
local log_text = table.concat(LOG, "\n") .. "\n\n"
reaper.ShowConsoleMsg(log_text)

-- Summary banner via REAPER message box (non-blocking in defer context)
-- Only shown on first run (not if DTB was already live)
reaper.gmem_attach("DameiMetering")
if reaper.gmem_read(456) == 0 then
  reaper.MB(
    string.format(
      "Damei Mix Assistant initialized.\n\n" ..
      "  Master Bus: 7-engine chain staged.\n" ..
      "  Track Relays: %d track(s) provisioned.\n" ..
      "  DTB: Master controller online.\n\n" ..
      "Press F11 to toggle DTB. Press F12 for console.",
      provisioned_count or 0
    ),
    "Damei: Session Ready", 0
  )
end

