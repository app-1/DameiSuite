"""
DAMEI SUITE -- DRUM STEM GAIN STAGING & RECONCILIATION ENGINE
Calibrates Raw Drum Stems to the Golden Producer Preset Operating Window
Built by Damei Audio & Antigravity IDE
"""

import sys, math
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

def calibrate_drum_stems():
    lua = '''
    local targets = {
        {idx=3,  name='Kick In',    target_pk_db = -9.0},
        {idx=4,  name='Kick Out',   target_pk_db = -9.0},
        {idx=12, name='Snare Top',  target_pk_db = -9.0},
        {idx=13, name='Snare Bot',  target_pk_db = -11.0},
        {idx=23, name='Tom 1',      target_pk_db = -9.0},
        {idx=24, name='Tom 2',      target_pk_db = -9.0},
        {idx=25, name='Floor Tom',  target_pk_db = -9.0},
        {idx=28, name='OH L',       target_pk_db = -13.0},
        {idx=29, name='OH R',       target_pk_db = -13.0},
        {idx=32, name='Room Mic',   target_pk_db = -14.0},
        {idx=33, name='Room Dyn',   target_pk_db = -12.0}
    }

    -- 1. Scan true max peaks across the timeline
    local test_positions = {15.0, 35.0, 55.0, 75.0, 95.0, 120.0, 150.0, 180.0, 210.0, 250.0}
    local max_pks = {}
    for _, entry in ipairs(targets) do max_pks[entry.idx] = 0.00001 end

    for _, pos in ipairs(test_positions) do
        reaper.SetEditCurPos(pos, false, false)
        reaper.CSurf_OnPlay()
        local t0 = reaper.time_precise()
        while reaper.time_precise() - t0 < 0.20 do end
        for _, entry in ipairs(targets) do
            local tr = reaper.GetTrack(0, entry.idx)
            if tr then
                local pk = reaper.Track_GetPeakInfo(tr, 0)
                if pk > max_pks[entry.idx] then max_pks[entry.idx] = pk end
            end
        end
    end
    reaper.CSurf_OnPause()

    -- 2. Adjust Item Take Gain on each track
    local ret = 'CALIBRATED DRUM STEM GAIN STAGING:\\n'
    for _, entry in ipairs(targets) do
        local tr = reaper.GetTrack(0, entry.idx)
        if tr then
            local raw_pk_db = 20 * math.log(max_pks[entry.idx], 10)
            local delta_db = entry.target_pk_db - raw_pk_db
            local gain_mult = 10 ^ (delta_db / 20.0)

            local item_count = reaper.CountTrackMediaItems(tr)
            for it_i = 0, item_count - 1 do
                local item = reaper.GetTrackMediaItem(tr, it_i)
                local take = reaper.GetActiveTake(item)
                if take then
                    local cur_vol = reaper.GetMediaItemTakeInfo_Value(take, 'D_VOL')
                    local new_vol = cur_vol * gain_mult
                    reaper.SetMediaItemTakeInfo_Value(take, 'D_VOL', new_vol)
                    reaper.UpdateItemInProject(item)
                end
            end
            ret = ret .. string.format('  Track %2d (%-10s): Raw = %+5.1f dBFS -> Calibrated = %+5.1f dBFS (Adjustment: %+5.1f dB across %d items)\\n',
                entry.idx + 1, entry.name, raw_pk_db, entry.target_pk_db, delta_db, item_count)
        end
    end
    return ret
    '''
    result = run_lua(lua)
    print(result)

if __name__ == "__main__":
    calibrate_drum_stems()
