import sys
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

lua_code = """
local found = {}

-- Master
local mtr = reaper.GetMasterTrack(0)
for f = 0, reaper.TrackFX_GetCount(mtr) - 1 do
    local _, name = reaper.TrackFX_GetFXName(mtr, f, "")
    table.insert(found, {track = "MASTER", fx = name, idx = f})
end

-- Tracks
for t = 0, reaper.CountTracks(0) - 1 do
    local tr = reaper.GetTrack(0, t)
    local _, tname = reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", "", false)
    for f = 0, reaper.TrackFX_GetCount(tr) - 1 do
        local _, name = reaper.TrackFX_GetFXName(tr, f, "")
        if name:find("Damei") or name:find("Assessment") or name:find("Oracle") or name:find("Mixing") then
            table.insert(found, {track = tname .. " (" .. (t+1) .. ")", fx = name, idx = f})
        end
    end
end

return found
"""

res = run_lua(lua_code)
import json
print(json.dumps(res, indent=2))
