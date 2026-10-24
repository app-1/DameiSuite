import sys
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua = r"""
local res = {}
local master = reaper.GetMasterTrack(0)
for j = 0, reaper.TrackFX_GetCount(master) - 1 do
    local _, name = reaper.TrackFX_GetFXName(master, j, "")
    table.insert(res, string.format("Master FX %d: %s", j, name))
    if string.find(name, "Damei") or string.find(name, "Matrix") or string.find(name, "Oracle") then
        reaper.TrackFX_SetOffline(master, j, true)
        reaper.TrackFX_SetOffline(master, j, false)
    end
end

for i = 0, reaper.CountTracks(0) - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, tr_name = reaper.GetTrackName(tr)
    for j = 0, reaper.TrackFX_GetCount(tr) - 1 do
        local _, name = reaper.TrackFX_GetFXName(tr, j, "")
        if string.find(name, "Matrix") or string.find(name, "Mixing") or string.find(name, "Oracle") or string.find(name, "Instrumental") then
            table.insert(res, string.format("Track %d (%s) FX %d: %s", i+1, tr_name, j, name))
            reaper.TrackFX_SetOffline(tr, j, true)
            reaper.TrackFX_SetOffline(tr, j, false)
        end
    end
end
return table.concat(res, "\n")
"""

result = run_lua(lua)
print(result)
