import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

# Enable legacy chain (FX 0..4), disable Damei (FX 5)
setup_legacy = """
local tr = reaper.GetTrack(0, 14)
reaper.TrackFX_SetEnabled(tr, 0, true)
reaper.TrackFX_SetEnabled(tr, 1, true)
reaper.TrackFX_SetEnabled(tr, 2, true)
reaper.TrackFX_SetEnabled(tr, 3, true)
reaper.TrackFX_SetEnabled(tr, 4, true)
reaper.TrackFX_SetEnabled(tr, 5, false)
reaper.SetEditCurPos(28.0, false, false)
reaper.CSurf_OnPlay()
return "Legacy chain active & playing"
"""
print(run_lua(setup_legacy))
time.sleep(1.2)

measure_legacy = """
local tr = reaper.GetTrack(0, 14)
local p_l = reaper.Track_GetPeakInfo(tr, 0)
local p_r = reaper.Track_GetPeakInfo(tr, 1)
local db_l = 20.0 * math.log(math.max(p_l, 0.00001), 10)
local db_r = 20.0 * math.log(math.max(p_r, 0.00001), 10)
-- Check BUSTERse gain reduction if exposed, or parameter 1 (meter)
local _, meter_str = reaper.TrackFX_GetFormattedParamValue(tr, 4, 1, '')
local raw_meter = reaper.TrackFX_GetParam(tr, 4, 1)
return string.format("Legacy Out: L=%.2f dBFS, R=%.2f dBFS | BUSTERse meter: %s (raw=%.3f)", db_l, db_r, meter_str, raw_meter)
"""
print(run_lua(measure_legacy))

# Now disable legacy chain, enable Damei (FX 5)
setup_damei = """
local tr = reaper.GetTrack(0, 14)
reaper.TrackFX_SetEnabled(tr, 0, false)
reaper.TrackFX_SetEnabled(tr, 1, false)
reaper.TrackFX_SetEnabled(tr, 2, false)
reaper.TrackFX_SetEnabled(tr, 3, false)
reaper.TrackFX_SetEnabled(tr, 4, false)
reaper.TrackFX_SetEnabled(tr, 5, true)
return "Damei Suite active & playing"
"""
print(run_lua(setup_damei))
time.sleep(1.2)

measure_damei = """
local tr = reaper.GetTrack(0, 14)
local p_l = reaper.Track_GetPeakInfo(tr, 0)
local p_r = reaper.Track_GetPeakInfo(tr, 1)
local db_l = 20.0 * math.log(math.max(p_l, 0.00001), 10)
local db_r = 20.0 * math.log(math.max(p_r, 0.00001), 10)
reaper.CSurf_OnStop()
return string.format("Damei Out: L=%.2f dBFS, R=%.2f dBFS", db_l, db_r)
"""
print(run_lua(measure_damei))
