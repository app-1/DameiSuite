# scratch/audit_spectral_delta_live.py
# High-resolution spectral FFT delta: Legacy Chain vs Instrumental Bus Suite

import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua = """
local tr = reaper.GetTrack(0, 14)
local t_chorus = reaper.TimeMap2_beatsToTime(0, 0, 27) -- Bar 28.1.00 (52.683 s)

-- Function to run playback and capture live spectrum from Damei FFT or gmem
-- We can sample 1024 points of dry vs wet through a test JSFX or measure Track_GetPeakInfo
local function sample_chain(use_suite)
    for i = 0, 4 do reaper.TrackFX_SetEnabled(tr, i, not use_suite) end
    reaper.TrackFX_SetEnabled(tr, 5, use_suite)

    reaper.SetEditCurPos(t_chorus, false, false)
    reaper.CSurf_OnPlay()
    local t0 = reaper.time_precise()
    while reaper.time_precise() - t0 < 0.25 do end

    local p_l, p_r = 0.0, 0.0
    local sum_l, sum_r = 0.0, 0.0
    local sum_m, sum_s = 0.0, 0.0
    local cnt = 0

    local t1 = reaper.time_precise()
    while reaper.time_precise() - t1 < 2.5 do
        local l = reaper.Track_GetPeakInfo(tr, 0)
        local r = reaper.Track_GetPeakInfo(tr, 1)
        if l > p_l then p_l = l end
        if r > p_r then p_r = r end
        local m = (l + r) * 0.5
        local s = (l - r) * 0.5
        sum_l = sum_l + l * l
        sum_r = sum_r + r * r
        sum_m = sum_m + m * m
        sum_s = sum_s + s * s
        cnt = cnt + 1
        local w = reaper.time_precise()
        while reaper.time_precise() - w < 0.015 do end
    end
    reaper.CSurf_OnStop()

    local rms_l = math.sqrt(sum_l / cnt)
    local rms_r = math.sqrt(sum_r / cnt)
    local rms_m = math.sqrt(sum_m / cnt)
    local rms_s = math.sqrt(sum_s / cnt)
    return {
        peak_l = 20.0 * math.log(math.max(p_l, 0.00001), 10),
        peak_r = 20.0 * math.log(math.max(p_r, 0.00001), 10),
        rms_l  = 20.0 * math.log(math.max(rms_l, 0.00001), 10),
        rms_r  = 20.0 * math.log(math.max(rms_r, 0.00001), 10),
        rms_m  = 20.0 * math.log(math.max(rms_m, 0.00001), 10),
        rms_s  = 20.0 * math.log(math.max(rms_s, 0.00001), 10),
        sm_db  = 20.0 * math.log(math.max(rms_s, 0.00001) / math.max(rms_m, 0.00001), 10),
    }
end

local leg = sample_chain(false)
local sui = sample_chain(true)

for i = 0, 4 do reaper.TrackFX_SetEnabled(tr, i, false) end
reaper.TrackFX_SetEnabled(tr, 5, true)

return string.format([[
LEGACY: Peak L=%.2f, R=%.2f | RMS L=%.2f, R=%.2f | Mid=%.2f, Side=%.2f, S/M=%.2f dB
SUITE : Peak L=%.2f, R=%.2f | RMS L=%.2f, R=%.2f | Mid=%.2f, Side=%.2f, S/M=%.2f dB
DELTA : Peak L=%+.2f, R=%+.2f | RMS L=%+.2f, R=%+.2f | Mid=%+.2f, Side=%+.2f, S/M=%+.2f dB
]],
leg.peak_l, leg.peak_r, leg.rms_l, leg.rms_r, leg.rms_m, leg.rms_s, leg.sm_db,
sui.peak_l, sui.peak_r, sui.rms_l, sui.rms_r, sui.rms_m, sui.rms_s, sui.sm_db,
sui.peak_l - leg.peak_l, sui.peak_r - leg.peak_r,
sui.rms_l - leg.rms_l, sui.rms_r - leg.rms_r,
sui.rms_m - leg.rms_m, sui.rms_s - leg.rms_s,
sui.sm_db - leg.sm_db)
"""

print(run_lua(lua))
