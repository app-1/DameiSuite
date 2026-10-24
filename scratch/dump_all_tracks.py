import sys
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

code = """
local cnt = reaper.CountTracks(0)
local lines = {"Total tracks: " .. tostring(cnt)}
for i = 0, cnt - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, name = reaper.GetTrackName(tr)
    local fx_c = reaper.TrackFX_GetCount(tr)
    local depth = reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH")
    local fx_names = {}
    for f = 0, fx_c - 1 do
        local _, fn = reaper.TrackFX_GetFXName(tr, f, "")
        local en = reaper.TrackFX_GetEnabled(tr, f)
        table.insert(fx_names, fn .. (en and "" or " [BYPASSED]"))
    end
    local fx_str = #fx_names > 0 and (" | FX: " .. table.concat(fx_names, ", ")) or ""
    table.insert(lines, string.format("Tr %2d: %s (depth=%d)%s", i+1, name, depth, fx_str))
end
return table.concat(lines, "\\n")
"""

res = run_lua(code)
with open("c:/Dev/DameiSuite/scratch/all_tracks_dump.txt", "w", encoding="utf-8") as f:
    f.write(str(res))
print("Saved to c:/Dev/DameiSuite/scratch/all_tracks_dump.txt")
print(str(res)[:2000])
