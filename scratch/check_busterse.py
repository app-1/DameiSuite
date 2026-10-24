import sys
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua = """
local tr = reaper.GetTrack(0, 14)
local res = {}
local num_params = reaper.TrackFX_GetNumParams(tr, 4)
for p = 16, num_params - 1 do
    local _, p_name = reaper.TrackFX_GetParamName(tr, 4, p, '')
    local val = reaper.TrackFX_GetParam(tr, 4, p)
    local _, val_str = reaper.TrackFX_GetFormattedParamValue(tr, 4, p, '')
    table.insert(res, 'p' .. p .. ': ' .. p_name .. ' = ' .. val_str .. ' (' .. string.format('%.3f', val) .. ')')
end
return table.concat(res, '\\n')
"""
print(run_lua(lua))
