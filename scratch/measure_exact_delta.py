import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua = """
local tr = reaper.GetTrack(0, 14)

-- 1. Enable legacy chain (FX 0..4), disable FX 5
for i = 0, 4 do reaper.TrackFX_SetEnabled(tr, i, true) end
reaper.TrackFX_SetEnabled(tr, 5, false)
reaper.SetEditCurPos(28.0, false, false)
reaper.CSurf_OnPlay()
local t0 = reaper.time_precise()
while reaper.time_precise() - t0 < 1.0 do end

local p_l1 = reaper.Track_GetPeakInfo(tr, 0)
local p_r1 = reaper.Track_GetPeakInfo(tr, 1)
local leg_l = 20.0 * math.log(math.max(p_l1, 0.00001), 10)
local leg_r = 20.0 * math.log(math.max(p_r1, 0.00001), 10)

-- 2. Disable legacy chain, enable FX 5 (Damei Suite)
for i = 0, 4 do reaper.TrackFX_SetEnabled(tr, i, false) end
reaper.TrackFX_SetEnabled(tr, 5, true)
t0 = reaper.time_precise()
while reaper.time_precise() - t0 < 1.0 do end

local p_l2 = reaper.Track_GetPeakInfo(tr, 0)
local p_r2 = reaper.Track_GetPeakInfo(tr, 1)
local dam_l = 20.0 * math.log(math.max(p_l2, 0.00001), 10)
local dam_r = 20.0 * math.log(math.max(p_r2, 0.00001), 10)

reaper.CSurf_OnStop()
return string.format("Legacy Chain: L=%.2f dBFS, R=%.2f dBFS\\nDamei Suite : L=%.2f dBFS, R=%.2f dBFS\\nDelta L=%.2f dB, Delta R=%.2f dB",
    leg_l, leg_r, dam_l, dam_r, dam_l - leg_l, dam_r - leg_r)
"""

print(run_lua(lua))
