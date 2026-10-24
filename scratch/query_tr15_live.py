import sys
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

lua = """
local tr = reaper.GetTrack(0, 14) -- Track 15
if not tr then return "Track 15 not found" end
local out = {}
for i = 0, reaper.TrackFX_GetCount(tr)-1 do
    local _, name = reaper.TrackFX_GetFXName(tr, i, "")
    local en = reaper.TrackFX_GetEnabled(tr, i)
    table.insert(out, string.format("FX %d: %s [enabled=%s]", i, name, tostring(en)))
    local num_params = reaper.TrackFX_GetNumParams(tr, i)
    for p = 0, num_params-1 do
        local _, pname = reaper.TrackFX_GetParamName(tr, i, p, "")
        local val = reaper.TrackFX_GetParam(tr, i, p)
        local _, fmt = reaper.TrackFX_GetFormattedParamValue(tr, i, p, "")
        if i == 4 or i == 3 or i == 0 or i == 2 then
            table.insert(out, string.format("   [%d] %s = %.3f ('%s')", p, pname, val, fmt))
        end
    end
end
return table.concat(out, "\\n")
"""

res = run_lua(lua)
print(res)
