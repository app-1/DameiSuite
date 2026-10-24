import sys
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

script = """
local out = {}
local count = reaper.CountTracks(0)
for i = 0, count - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, name = reaper.GetTrackName(tr)
    local fx_count = reaper.TrackFX_GetCount(tr)
    local is_vox = false
    if string.find(string.upper(name), "VOX") or string.find(string.upper(name), "VOCAL") then
        is_vox = true
    end
    for f = 0, fx_count - 1 do
        local _, fx_name = reaper.TrackFX_GetFXName(tr, f, "")
        if string.find(string.upper(fx_name), "VOCAL") or string.find(string.upper(fx_name), "EMPRESS") or string.find(string.upper(fx_name), "SOVEREIGN") then
            is_vox = true
        end
    end
    if is_vox then
        table.insert(out, string.format("Track %d: '%s' (FX count: %d)", i + 1, name, fx_count))
        for f = 0, fx_count - 1 do
            local _, fx_name = reaper.TrackFX_GetFXName(tr, f, "")
            local en = reaper.TrackFX_GetEnabled(tr, f)
            table.insert(out, string.format("    FX %d: %s [enabled=%s]", f, fx_name, tostring(en)))
        end
    end
end
return table.concat(out, "\\n")
"""

res = run_lua(script)
print(res)
