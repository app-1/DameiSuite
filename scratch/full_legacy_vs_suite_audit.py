# scratch/full_legacy_vs_suite_audit.py
import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

sections = [
    ("Verse (Bar 12)", 12.0),
    ("Pre-Chorus (Bar 20)", 20.0),
    ("Chorus Drop (Bar 27)", 27.0),
    ("Full Chorus Wall (Bar 30)", 30.0),
]

def audit_section(name, pos):
    lua = f"""
    local tr = reaper.GetTrack(0, 14)

    local function measure(use_suite)
        for i = 0, 4 do reaper.TrackFX_SetEnabled(tr, i, not use_suite) end
        reaper.TrackFX_SetEnabled(tr, 5, use_suite)
        if use_suite then reaper.TrackFX_SetParam(tr, 5, 1, 6) end -- Kel Pinchin

        reaper.SetEditCurPos({pos}, false, false)
        reaper.CSurf_OnPlay()
        local t0 = reaper.time_precise()
        while reaper.time_precise() - t0 < 0.2 do end

        local p_l_max, p_r_max = 0.0, 0.0
        local sum_l, sum_r = 0.0, 0.0
        local count = 0

        local t1 = reaper.time_precise()
        while reaper.time_precise() - t1 < 1.2 do
            local pl = reaper.Track_GetPeakInfo(tr, 0)
            local pr = reaper.Track_GetPeakInfo(tr, 1)
            if pl > p_l_max then p_l_max = pl end
            if pr > p_r_max then p_r_max = pr end
            sum_l = sum_l + pl * pl
            sum_r = sum_r + pr * pr
            count = count + 1
            local w = reaper.time_precise()
            while reaper.time_precise() - w < 0.02 do end
        end
        reaper.CSurf_OnStop()

        local rms_l = math.sqrt(sum_l / count)
        local rms_r = math.sqrt(sum_r / count)
        return 20.0 * math.log(math.max(p_l_max, 0.00001), 10),
               20.0 * math.log(math.max(p_r_max, 0.00001), 10),
               20.0 * math.log(math.max(rms_l, 0.00001), 10),
               20.0 * math.log(math.max(rms_r, 0.00001), 10)
    end

    local leg_pl, leg_pr, leg_rl, leg_rr = measure(false)
    local sui_pl, sui_pr, sui_rl, sui_rr = measure(true)

    -- Restore
    for i = 0, 4 do reaper.TrackFX_SetEnabled(tr, i, false) end
    reaper.TrackFX_SetEnabled(tr, 5, true)

    return string.format("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f",
        leg_pl, leg_pr, leg_rl, leg_rr, sui_pl, sui_pr, sui_rl, sui_rr)
    """
    res = run_lua(lua)
    parts = [float(x) for x in res.strip().split(',')]
    return {
        "name": name,
        "leg_pl": parts[0], "leg_pr": parts[1], "leg_rl": parts[2], "leg_rr": parts[3],
        "sui_pl": parts[4], "sui_pr": parts[5], "sui_rl": parts[6], "sui_rr": parts[7],
    }

print("="*105)
print(f"{'SECTION':28s} | {'CHAIN':8s} | {'PEAK L':7s} | {'PEAK R':7s} | {'RMS L':7s} | {'RMS R':7s} | {'PEAK BAL':8s} | {'RMS BAL':8s}")
print("="*105)

for name, pos in sections:
    d = audit_section(name, pos)
    leg_pbal = d['leg_pl'] - d['leg_pr']
    leg_rbal = d['leg_rl'] - d['leg_rr']
    sui_pbal = d['sui_pl'] - d['sui_pr']
    sui_rbal = d['sui_rl'] - d['sui_rr']

    print(f"{name:28s} | Legacy   | {d['leg_pl']:6.2f}  | {d['leg_pr']:6.2f}  | {d['leg_rl']:6.2f}  | {d['leg_rr']:6.2f}  | L-R: {leg_pbal:+4.2f} | L-R: {leg_rbal:+4.2f}")
    print(f"{'':28s} | Suite    | {d['sui_pl']:6.2f}  | {d['sui_pr']:6.2f}  | {d['sui_rl']:6.2f}  | {d['sui_rr']:6.2f}  | L-R: {sui_pbal:+4.2f} | L-R: {sui_rbal:+4.2f}")
    
    d_pl = d['sui_pl'] - d['leg_pl']
    d_pr = d['sui_pr'] - d['leg_pr']
    d_rl = d['sui_rl'] - d['leg_rl']
    d_rr = d['sui_rr'] - d['leg_rr']
    print(f"{'':28s} | DELTA    | {d_pl:+6.2f}  | {d_pr:+6.2f}  | {d_rl:+6.2f}  | {d_rr:+6.2f}  | Delta: {sui_pbal - leg_pbal:+3.2f} | Delta: {sui_rbal - leg_rbal:+3.2f}")
    print("-"*105)
