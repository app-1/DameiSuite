-- Standalone launcher for the Project State relay (use when the structure bridge
-- is already running an older copy). Safe to run once per REAPER session.
local ok, mod = pcall(dofile, [[c:\Dev\DameiAPI\reaper_scripts\damei_project_state_relay.lua]])
if not ok or type(mod) ~= "table" then
  reaper.ShowConsoleMsg("Damei relay launcher: could not load relay module\n")
  return
end
if reaper.GetExtState("damei_relay", "running") == "1" and reaper.GetExtState("damei_relay", "hb") ~= "" then
  local age = reaper.time_precise() - (tonumber(reaper.GetExtState("damei_relay", "hb")) or 0)
  if age < 2.0 then return end
end
local function loop()
  pcall(mod.step)
  reaper.SetExtState("damei_relay", "running", "1", false)
  reaper.SetExtState("damei_relay", "hb", tostring(reaper.time_precise()), false)
  reaper.defer(loop)
end
loop()
