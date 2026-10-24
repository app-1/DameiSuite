import sys
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua = """
local tr = reaper.GetTrack(0, 14)
local res = {}
for p = 35, 250 do
    local _, p_name = reaper.TrackFX_GetParamName(tr, 1, p, '')
    if p_name:find('Frequency') or p_name:find('Gain') or p_name:find('Type') or p_name:find('Enable') or p_name:find('Q') then
        local _, val_str = reaper.TrackFX_GetFormattedParamValue(tr, 1, p, '')
        table.insert(res, string.format('p%d: %s = %s', p, p_name, val_str))
    end
end
return table.concat(res, '\\n')
"""
print(run_lua(lua))
