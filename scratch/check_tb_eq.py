import sys
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua = """
local tr = reaper.GetTrack(0, 14)
local res = {}
for p = 0, 50 do
    local _, p_name = reaper.TrackFX_GetParamName(tr, 1, p, '')
    local val = reaper.TrackFX_GetParam(tr, 1, p)
    local _, val_str = reaper.TrackFX_GetFormattedParamValue(tr, 1, p, '')
    table.insert(res, string.format('p%d: %s = %s (raw=%.3f)', p, p_name, val_str, val))
end
return table.concat(res, '\\n')
"""
print(run_lua(lua))
