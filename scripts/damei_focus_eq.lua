-- Damei: Focus Selected Track in ReEQ Bridge
-- Alt+E keybind: binds the EQ on the currently selected track to DTB
local ok, BRIDGE
local sd = reaper.GetResourcePath() .. '/Scripts/Damei'
package.path = package.path .. ';' .. sd .. '/?.lua'
ok, BRIDGE = pcall(require, 'damei_tbc_bridge')
if not ok then
  reaper.ShowConsoleMsg('[Damei] damei_tbc_bridge not found\n')
  return
end
local sel = reaper.GetSelectedTrack(0, 0)
if not sel then
  reaper.ShowConsoleMsg('[Damei] No track selected\n')
  return
end
BRIDGE.scan_project()
local g = reaper.GetTrackGUID(sel)
local insts = BRIDGE.eq_instances or {}
for i, inst in ipairs(insts) do
  if inst.track_guid == g then
    BRIDGE.selected_idx = i
    if BRIDGE.read_bands then BRIDGE.read_bands() end
    reaper.ShowConsoleMsg('[Damei] EQ focus: track ' .. select(2, reaper.GetTrackName(sel)) .. '\n')
    return
  end
end
reaper.ShowConsoleMsg('[Damei] No JS:ReEQ / ReaEQ found on selected track\n')
