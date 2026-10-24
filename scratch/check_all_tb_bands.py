import sys
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua = """
local tr = reaper.GetTrack(0, 14)
local res = {}
for b = 1, 8 do
    local offset = 36 + (b - 1) * 82
    local _, f_str = reaper.TrackFX_GetFormattedParamValue(tr, 1, offset + 5, '')
    local _, g_str = reaper.TrackFX_GetFormattedParamValue(tr, 1, offset + 6, '')
    local _, q_str = reaper.TrackFX_GetFormattedParamValue(tr, 1, offset + 8, '')
    local _, t_str = reaper.TrackFX_GetFormattedParamValue(tr, 1, offset + 1, '')
    local _, e_str = reaper.TrackFX_GetFormattedParamValue(tr, 1, offset + 3, '')
    table.insert(res, string.format('Band %d: Type=%s Enable=%s Freq=%s Gain=%s Q=%s', b, t_str, e_str, f_str, g_str, q_str))
end
return table.concat(res, '\\n')
"""
print(run_lua(lua))
