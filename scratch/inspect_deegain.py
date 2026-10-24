import sys
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

lua_code = """
local tr15 = reaper.GetTrack(0, 14)
local count = reaper.TrackFX_GetNumParams(tr15, 2)
local params = {}
for p = 0, count - 1 do
    local _, pname = reaper.TrackFX_GetParamName(tr15, 2, p, "")
    local val = reaper.TrackFX_GetParam(tr15, 2, p)
    local fmt = reaper.TrackFX_GetFormattedParamValue(tr15, 2, p, "")
    table.insert(params, {p = p, name = pname, val = val, fmt = fmt})
end
return params
"""

res = run_lua(lua_code)
import json
print(json.dumps(res, indent=2))
