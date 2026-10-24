import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

def measure_section(pos, trim, thresh):
    lua = f"""
    local tr = reaper.GetTrack(0, 14)
    local function run(use_suite)
        for i = 0, 4 do reaper.TrackFX_SetEnabled(tr, i, not use_suite) end
        reaper.TrackFX_SetEnabled(tr, 5, use_suite)
        if use_suite then
            reaper.TrackFX_SetParam(tr, 5, 1, 6) -- Kel Pinchin
            reaper.TrackFX_SetParam(tr, 5, 3, {trim}) -- Trim
            reaper.TrackFX_SetParam(tr, 5, 11, {thresh}) -- Thresh
        end
        reaper.SetEditCurPos({pos}, false, false)
        reaper.CSurf_OnPlay()
        local t0 = reaper.time_precise()
        while reaper.time_precise() - t0 < 0.2 do end

        local pl, pr = 0, 0
        local sum_l, sum_r, count = 0, 0, 0
        local t1 = reaper.time_precise()
        while reaper.time_precise() - t1 < 0.6 do
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
    local l_pl, l_pr, l_rl, l_rr = run(false)
    local s_pl, s_pr, s_rl, s_rr = run(true)
    for i = 0, 4 do reaper.TrackFX_SetEnabled(tr, i, false) end
    reaper.TrackFX_SetEnabled(tr, 5, true)
    return string.format("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f",
        l_pl, l_pr, l_rl, l_rr, s_pl, s_pr, s_rl, s_rr)
    """
    res = run_lua(lua)
    p = [float(x) for x in res.strip().split(',')]
    return {'leg_p': (p[0]+p[1])*0.5, 'leg_r': (p[2]+p[3])*0.5,
            'sui_p': (p[4]+p[5])*0.5, 'sui_r': (p[6]+p[7])*0.5}

print("Testing Bar 30 with trim=-3.6, thresh=-14.5...")
d = measure_section(30.0, -3.6, -14.5)
print(f"Legacy: Peak={d['leg_p']:.2f}, RMS={d['leg_r']:.2f}")
print(f"Suite : Peak={d['sui_p']:.2f}, RMS={d['sui_r']:.2f}")
print(f"DELTA : Peak={d['sui_p'] - d['leg_p']:+.2f} dB, RMS={d['sui_r'] - d['leg_r']:+.2f} dB")
