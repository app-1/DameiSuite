-- Damei Startup Watcher Launcher

local function start_watcher()
  local script_path = reaper.GetResourcePath() .. "/Scripts/watch_project_changes.lua"
  local alt_path = "C:/Dev/DameiAPI/reaper_scripts/watch_project_changes.lua"

  local f = io.open(script_path, "r")
  if f then f:close() dofile(script_path) return end

  local f2 = io.open(alt_path, "r")
  if f2 then f2:close() dofile(alt_path) return end

  reaper.ShowConsoleMsg("Damei Startup: Could not find watch_project_changes.lua\n")
end

local ok, err = pcall(start_watcher)
if not ok then
  reaper.ShowConsoleMsg("Damei Startup error: " .. tostring(err) .. "\n")
end
