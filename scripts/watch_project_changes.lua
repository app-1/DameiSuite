-- Damei Project-Change Watcher (Startup Delay + Debounce)

local last_state = reaper.GetProjectStateChangeCount(0)
local debounce_ms = 500
local last_trigger_time = 0

local startup_delay = 3.0
local start_time = reaper.time_precise()

local function run_autopull()
  local script_path = reaper.GetResourcePath() .. "/Scripts/get_project_tracks.lua"
  local alt_path = "C:/Dev/DameiAPI/reaper_scripts/get_project_tracks.lua"

  local f = io.open(script_path, "r")
  if f then f:close() dofile(script_path) return end

  local f2 = io.open(alt_path, "r")
  if f2 then f2:close() dofile(alt_path) return end

  reaper.ShowConsoleMsg("Damei Watcher: Could not find get_project_tracks.lua\n")
end

local function watcher()
  local now = reaper.time_precise()

  if now - start_time < startup_delay then
    reaper.defer(watcher)
    return
  end

  local state = reaper.GetProjectStateChangeCount(0)

  if state ~= last_state then
    if (now - last_trigger_time) * 1000 > debounce_ms then
      run_autopull()
      last_trigger_time = now
    end
    last_state = state
  end

  reaper.defer(watcher)
end

reaper.ShowConsoleMsg("Damei Watcher started.\n")
watcher()
