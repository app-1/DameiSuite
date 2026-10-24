import sys
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

code = """
local tr = reaper.GetTrack(0, 14)
if not tr then return "Track 14 is nil" end
local _, name = reaper.GetTrackName(tr)
local fx_c = reaper.TrackFX_GetCount(tr)
local lines = {"Track 15 name: " .. name .. " FX count: " .. tostring(fx_c)}
for i = 0, fx_c - 1 do
    local _, fxname = reaper.TrackFX_GetFXName(tr, i, "")
    table.insert(lines, "  FX " .. tostring(i) .. ": " .. fxname)
end
return table.concat(lines, "\\n")
"""

print(run_lua(code))
