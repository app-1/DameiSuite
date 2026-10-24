import sys
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua_fx = """
local tr = reaper.GetTrack(0, 14)
if not tr then return 'Track 15 not found' end
local _, tr_name = reaper.GetTrackName(tr)
local fx_cnt = reaper.TrackFX_GetCount(tr)
local res = {}
table.insert(res, 'Track 15: ' .. tr_name .. ' FX Count: ' .. fx_cnt)
for i = 0, fx_cnt - 1 do
    local _, fx_name = reaper.TrackFX_GetFXName(tr, i, '')
    local enabled = reaper.TrackFX_GetEnabled(tr, i)
    table.insert(res, 'FX ' .. i .. ': ' .. fx_name .. ' enabled=' .. tostring(enabled))
    local num_params = reaper.TrackFX_GetNumParams(tr, i)
    for p = 0, math.min(num_params - 1, 15) do
        local _, p_name = reaper.TrackFX_GetParamName(tr, i, p, '')
        local val = reaper.TrackFX_GetParam(tr, i, p)
        local _, val_str = reaper.TrackFX_GetFormattedParamValue(tr, i, p, '')
        table.insert(res, '   p' .. p .. ': ' .. p_name .. ' = ' .. val_str .. ' (' .. string.format('%.3f', val) .. ')')
    end
end
return table.concat(res, '\\n')
"""

output = run_lua(lua_fx)
print(output)
