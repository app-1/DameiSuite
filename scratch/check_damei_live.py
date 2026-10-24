import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua = """
local tr = reaper.GetTrack(0, 14)
reaper.SetEditCurPos(28.0, false, false)
reaper.CSurf_OnPlay()
"""
run_lua(lua)
time.sleep(1.0)

check_damei = """
local tr = reaper.GetTrack(0, 14)
-- Query slider values from Damei Suite (FX 5)
local res = {}
local num = reaper.TrackFX_GetNumParams(tr, 5)
for p = 0, num - 1 do
    local _, p_name = reaper.TrackFX_GetParamName(tr, 5, p, '')
    local val = reaper.TrackFX_GetParam(tr, 5, p)
    local _, val_str = reaper.TrackFX_GetFormattedParamValue(tr, 5, p, '')
    table.insert(res, string.format('p%d: %s = %s (%.2f)', p, p_name, val_str, val))
end
return table.concat(res, '\\n')
"""
print(run_lua(check_damei))

time.sleep(0.5)
run_lua("reaper.CSurf_OnStop()")
