import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

# We can bypass FX one by one to see their exact gain contribution!
lua = """
local tr = reaper.GetTrack(0, 14)
-- Start with all legacy enabled, Damei disabled
for i=0,4 do reaper.TrackFX_SetEnabled(tr, i, true) end
reaper.TrackFX_SetEnabled(tr, 5, false)

reaper.SetEditCurPos(28.0, false, false)
reaper.CSurf_OnPlay()
"""
run_lua(lua)
time.sleep(0.5)

measure_lua = """
local tr = reaper.GetTrack(0, 14)
local function get_peak()
    local p_l = reaper.Track_GetPeakInfo(tr, 0)
    local p_r = reaper.Track_GetPeakInfo(tr, 1)
    return 20.0 * math.log(math.max(p_l, 0.00001), 10)
end

local res = {}
-- Baseline (all on)
table.insert(res, string.format("All legacy ON: Peak=%.2f dBFS", get_peak()))

-- Bypass BUSTERse (FX 4)
reaper.TrackFX_SetEnabled(tr, 4, false)
-- sleep a bit in lua
local t0 = reaper.time_precise()
while reaper.time_precise() - t0 < 0.3 do end
table.insert(res, string.format("BUSTERse BYPASSED: Peak=%.2f dBFS", get_peak()))

-- Bypass Bass Manager (FX 3)
reaper.TrackFX_SetEnabled(tr, 3, false)
t0 = reaper.time_precise()
while reaper.time_precise() - t0 < 0.3 do end
table.insert(res, string.format("Bass Manager BYPASSED: Peak=%.2f dBFS", get_peak()))

-- Bypass DeeGain (FX 2)
reaper.TrackFX_SetEnabled(tr, 2, false)
t0 = reaper.time_precise()
while reaper.time_precise() - t0 < 0.3 do end
table.insert(res, string.format("DeeGain BYPASSED: Peak=%.2f dBFS", get_peak()))

-- Bypass TB Equalizer Pro (FX 1)
reaper.TrackFX_SetEnabled(tr, 1, false)
t0 = reaper.time_precise()
while reaper.time_precise() - t0 < 0.3 do end
table.insert(res, string.format("TB EQ BYPASSED: Peak=%.2f dBFS", get_peak()))

-- Bypass Britson (FX 0) -> Raw Track 15 Input!
reaper.TrackFX_SetEnabled(tr, 0, false)
t0 = reaper.time_precise()
while reaper.time_precise() - t0 < 0.3 do end
table.insert(res, string.format("Britson BYPASSED (Raw In): Peak=%.2f dBFS", get_peak()))

-- Restore
for i=0,4 do reaper.TrackFX_SetEnabled(tr, i, false) end
reaper.TrackFX_SetEnabled(tr, 5, true)
reaper.CSurf_OnStop()
return table.concat(res, "\\n")
"""

print(run_lua(measure_lua))
