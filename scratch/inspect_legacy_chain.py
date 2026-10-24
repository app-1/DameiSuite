import sys
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua = """
local tr = reaper.GetTrack(0, 14)
local res = {}
for fx = 0, 4 do
    local _, fx_name = reaper.TrackFX_GetFXName(tr, fx, '')
    table.insert(res, '=== FX ' .. fx .. ': ' .. fx_name .. ' ===')
    local num = reaper.TrackFX_GetNumParams(tr, fx)
    for p = 0, num - 1 do
        local _, p_name = reaper.TrackFX_GetParamName(tr, fx, p, '')
        local val = reaper.TrackFX_GetParam(tr, fx, p)
        local _, val_str = reaper.TrackFX_GetFormattedParamValue(tr, fx, p, '')
        -- Only print non-zero or notable params
        if val ~= 0 or string.len(val_str) > 0 and val_str ~= "0" and val_str ~= "0.0" and val_str ~= "Off" then
            table.insert(res, string.format('   p%d: %s = %s (%.3f)', p, p_name, val_str, val))
        end
    end
end
return table.concat(res, '\\n')
"""
print(run_lua(lua))
