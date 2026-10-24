import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

def audit_range(start_pos, duration):
    lua = f"""
    local tr = reaper.GetTrack(0, 14)
    local function run_chain(use_suite)
        for i = 0, 4 do reaper.TrackFX_SetEnabled(tr, i, not use_suite) end
        reaper.TrackFX_SetEnabled(tr, 5, use_suite)
        if use_suite then
            reaper.TrackFX_SetParam(tr, 5, 1, 6) -- Kel Pinchin
        end

        reaper.SetEditCurPos({start_pos}, false, false)
        reaper.CSurf_OnPlay()
        local t0 = reaper.time_precise()
        while reaper.time_precise() - t0 < 0.35 do end

        local pl, pr = 0, 0
        local sum_l, sum_r, count = 0, 0, 0
        local t1 = reaper.time_precise()
        while reaper.time_precise() - t1 < {duration} do
            local p0 = reaper.Track_GetPeakInfo(tr, 0)
            local p1 = reaper.Track_GetPeakInfo(tr, 1)
            if p0 > pl then pl = p0 end
            if p1 > pr then pr = p1 end
            sum_l = sum_l + p0*p0
            sum_r = sum_r + p1*p1
            count = count + 1
            local w = reaper.time_precise()
            while reaper.time_precise() - w < 0.02 do end
        end
        reaper.CSurf_OnStop()
        return 20.0*math.log(math.max(pl, 0.00001), 10),
               20.0*math.log(math.max(pr, 0.00001), 10),
               20.0*math.log(math.max(math.sqrt(sum_l/count), 0.00001), 10),
               20.0*math.log(math.max(math.sqrt(sum_r/count), 0.00001), 10)
    end

    local l_pl, l_pr, l_rl, l_rr = run_chain(false)
    local s_pl, s_pr, s_rl, s_rr = run_chain(true)

    -- Restore Suite
    for i = 0, 4 do reaper.TrackFX_SetEnabled(tr, i, false) end
    reaper.TrackFX_SetEnabled(tr, 5, true)

    return string.format("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f",
        l_pl, l_pr, l_rl, l_rr, s_pl, s_pr, s_rl, s_rr)
    """
    res = run_lua(lua)
    p = [float(x) for x in res.strip().split(',')]
    return {
        'leg_pl': p[0], 'leg_pr': p[1], 'leg_rl': p[2], 'leg_rr': p[3],
        'sui_pl': p[4], 'sui_pr': p[5], 'sui_rl': p[6], 'sui_rr': p[7],
    }

print("="*95)
print(f"{'SECTION':25s} | {'LEGACY RMS':14s} | {'SUITE RMS':14s} | {'RMS DELTA':14s} | {'PEAK DELTA':12s}")
print("="*95)

tests = [
    ("Verse (11s - 15s)", 11.0, 3.0),
    ("Pre-Chorus (18s - 22s)", 18.0, 3.0),
    ("Chorus 1 (26s - 34s)", 26.0, 6.0),
]

for name, start, dur in tests:
    d = audit_range(start, dur)
    leg_rms = (d['leg_rl'] + d['leg_rr']) * 0.5
    sui_rms = (d['sui_rl'] + d['sui_rr']) * 0.5
    d_rms = sui_rms - leg_rms
    leg_peak = max(d['leg_pl'], d['leg_pr'])
    sui_peak = max(d['sui_pl'], d['sui_pr'])
    d_peak = sui_peak - leg_peak
    print(f"{name:25s} | {leg_rms:6.2f} dBFS    | {sui_rms:6.2f} dBFS    | {d_rms:+6.2f} dB       | {d_peak:+6.2f} dB")
print("="*95)
