import sys
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

script = r"""
local cnt = reaper.CountTracks(0)
local res = {}
for t = 0, cnt - 1 do
    local tr = reaper.GetTrack(0, t)
    local _, name = reaper.GetTrackName(tr, "")
    local fx_cnt = reaper.TrackFX_GetCount(tr)
    for f = 0, fx_cnt - 1 do
        local _, fx_name = reaper.TrackFX_GetFXName(tr, f, "")
        if string.find(fx_name, "Damei") then
            table.insert(res, string.format("Track %d (%s) FX %d: %s", t + 1, name, f, fx_name))
        end
    end
end
return table.concat(res, "\n")
"""
print(run_lua(script))
