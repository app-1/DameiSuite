-- Damei One-Click Action Installer  (v2 - includes band solo + DTB keybinds)
-- Run from Actions List to register all Damei scripts as REAPER custom actions.
-- Recommended keybinds shown in comments; assign via Actions -> Edit shortcut.

local base = reaper.GetResourcePath() .. "/Scripts/Damei"

local scripts = {
  -- Core UI panels
  { file = "damei_ozone_suite.lua",   name = "Damei: Open Ozone 12 Mastering Suite" },
  { file = "damei_console.lua",       name = "Damei: Open Mix Console" },
  { file = "damei_panel.lua",         name = "Damei: Open Floating Meter Panel" },
  { file = "damei_tbc.lua",           name = "Damei: Toggle Standalone TBC Window" },  -- F11
  -- Utility
  { file = "get_project_tracks.lua",       name = "Damei: Export Project Track Data" },
  { file = "watch_project_changes.lua",    name = "Damei: Watch Project Changes" },
  { file = "damei_startup_watcher.lua",    name = "Damei: Startup Engine Watcher" },
  { file = "damei_push_metrics.lua",       name = "Damei: Push Metrics to Backend" },
  -- Band solo auditioning (recommended: Numpad 0-4)
  { file = "damei_solo_bypass.lua",    name = "Damei: Solo Bypass - Full Mix" },      -- Numpad 0
  { file = "damei_solo_sub.lua",       name = "Damei: Solo Sub Band (Audition)" },    -- Numpad 1
  { file = "damei_solo_bass.lua",      name = "Damei: Solo Bass Band (Audition)" },   -- Numpad 2
  { file = "damei_solo_lowmid.lua",    name = "Damei: Solo Low-Mid Band (Audition)" },-- Numpad 3
  { file = "damei_solo_high.lua",      name = "Damei: Solo High Band (Audition)" },   -- Numpad 4
  -- EQ bridge
  { file = "damei_focus_eq.lua",       name = "Damei: Focus Selected Track in ReEQ Bridge" }, -- Alt+E
  -- Self
  { file = "damei_register_actions.lua", name = "Damei: Register All Actions (Installer)" },
}

local registered, skipped, failed = 0, 0, 0

local function register_script(entry)
  local path = base .. "/" .. entry.file
  local f = io.open(path, "r")
  if not f then
    reaper.ShowConsoleMsg("  [SKIP] Missing: " .. entry.file .. "\n")
    skipped = skipped + 1
    return
  end
  f:close()
  local ok = reaper.AddRemoveReaScript(true, 0, path, true)
  if ok then
    reaper.ShowConsoleMsg(string.format("  [OK]   %-45s  %s\n", entry.name, entry.file))
    registered = registered + 1
  else
    reaper.ShowConsoleMsg("  [ERR]  " .. entry.file .. "\n")
    failed = failed + 1
  end
end

reaper.ClearConsole()
reaper.ShowConsoleMsg("============================\n")
reaper.ShowConsoleMsg(" Damei Action Installer v2\n")
reaper.ShowConsoleMsg("============================\n\n")

for _, entry in ipairs(scripts) do
  local ok, err = pcall(register_script, entry)
  if not ok then
    reaper.ShowConsoleMsg("  [ERR]  " .. tostring(err) .. "\n")
    failed = failed + 1
  end
end

reaper.ShowConsoleMsg(string.format("\nDone: %d registered, %d skipped, %d errors\n", registered, skipped, failed))
reaper.ShowConsoleMsg("\nRecommended keybinds:\n")
reaper.ShowConsoleMsg("  F11       -> Damei: Toggle Standalone TBC Window\n")
reaper.ShowConsoleMsg("  Numpad 0  -> Damei: Solo Bypass - Full Mix\n")
reaper.ShowConsoleMsg("  Numpad 1  -> Damei: Solo Sub Band (Audition)\n")
reaper.ShowConsoleMsg("  Numpad 2  -> Damei: Solo Bass Band (Audition)\n")
reaper.ShowConsoleMsg("  Numpad 3  -> Damei: Solo Low-Mid Band (Audition)\n")
reaper.ShowConsoleMsg("  Numpad 4  -> Damei: Solo High Band (Audition)\n")
reaper.ShowConsoleMsg("  Alt+E     -> Damei: Focus Selected Track in ReEQ Bridge\n")
reaper.ShowConsoleMsg("\nAssign via: Actions -> Show action list -> find Damei -> Edit shortcut\n")
