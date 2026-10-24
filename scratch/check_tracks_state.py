import sys
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

code = """
local trk_count = reaper.CountTracks(0)
local trk15 = reaper.GetTrack(0, 14) -- 0-indexed for track 15
local trk15_name = ""
if trk15 then
    local _, name = reaper.GetTrackName(trk15)
    trk15_name = name
end

local trk4 = reaper.GetTrack(0, 3) -- 0-indexed for track 4
local trk4_name = ""
if trk4 then
    local _, name = reaper.GetTrackName(trk4)
    trk4_name = name
end

local function get_fx_list(trk)
    local list = {}
    if trk then
        local fx_count = reaper.TrackFX_GetCount(trk)
        for i = 0, fx_count - 1 do
            local _, fx_name = reaper.TrackFX_GetFXName(trk, i, "")
            local enabled = reaper.TrackFX_GetEnabled(trk, i)
            table.insert(list, {idx = i, name = fx_name, enabled = enabled})
        end
    end
    return list
end

return {
    track_count = trk_count,
    track15 = {name = trk15_name, fx = get_fx_list(trk15)},
    track4 = {name = trk4_name, fx = get_fx_list(trk4)}
}
"""

res = run_lua(code)
import pprint
pprint.pprint(res)
