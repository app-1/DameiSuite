import sys
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

lua_code = """
local master = reaper.GetMasterTrack(0)
local count = reaper.TrackFX_GetCount(master)
local mix_fx_idx = -1
for i = 0, count - 1 do
    local _, name = reaper.TrackFX_GetFXName(master, i, "")
    if name:find("MixingSuite") or name:find("Imperial Console") then
        mix_fx_idx = i
        break
    end
end

if mix_fx_idx == -1 then return {found = false} end

local num_params = reaper.TrackFX_GetNumParams(master, mix_fx_idx)
local params = {}
for p = 0, num_params - 1 do
    local _, pname = reaper.TrackFX_GetParamName(master, mix_fx_idx, p, "")
    local val = reaper.TrackFX_GetParam(master, mix_fx_idx, p)
    local fmt = reaper.TrackFX_GetFormattedParamValue(master, mix_fx_idx, p, "")
    table.insert(params, {p = p, name = pname, val = val, fmt = fmt})
end

return {found = true, fx_idx = mix_fx_idx, params = params}
"""

res = run_lua(lua_code)
import json
if res.get("found"):
    for p in res["params"]:
        if any(k in p["name"].lower() for k in ["vox", "vocal", "pocket", "center", "tilt", "donut", "glue"]):
            print(f"P{p['p']:2d} ({p['name']:40s}): {p['val']} [{p['fmt']}]")
else:
    print("MixingSuite not found on master track")
