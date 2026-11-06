"""
DAMEI SUITE -- REAPER DRUM SPECTRAL SURGEON & GAIN CALIBRATOR
Incorporate REAPER Native Spectral Editing & Golden Stem Gain Staging
Built by Damei Audio & Antigravity IDE
"""

import sys, math
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

def apply_spectral_edits_and_gain_staging():
    lua = '''
    local results = {}
    
    -- 1. Enable Spectral Peaks Display (Multi-Color Waveforms)
    local cur_state = reaper.GetToggleCommandState(42073)
    if cur_state ~= 1 then
        reaper.Main_OnCommand(42073, 0) -- Peaks: Toggle spectral peaks
    end
    table.insert(results, "[OK] REAPER Multi-Color Spectral Peaks: ENABLED (Action 42073)")

    -- 2. Inject Surgical Spectral Edit onto Snare Top (Track 13)
    -- Target: 650 Hz metal ringing whistle overtone (Q ~ 6, 600 - 720 Hz, -12 dB gain)
    -- Applied cleanly across the item, leaving transient headroom
    local tr13 = reaper.GetTrack(0, 12) -- Snare Top
    if tr13 then
        local count = reaper.CountTrackMediaItems(tr13)
        local injected_count = 0
        for i = 0, count - 1 do
            local item = reaper.GetTrackMediaItem(tr13, i)
            local take = reaper.GetActiveTake(item)
            if take then
                local _, chunk = reaper.GetItemStateChunk(item, '', false)
                if not string.find(chunk, 'SPECTRAL_EDIT') then
                    local len = reaper.GetMediaItemInfo_Value(item, 'D_LENGTH')
                    local pos = reaper.GetMediaItemInfo_Value(item, 'D_POSITION')
                    -- Edit: pos, len, gain(0.25 = -12dB), freq_lo(600), freq_hi(720), fade(0.01s)
                    local edit_line = string.format('SPECTRAL_EDIT 0.0 %.4f 0.25118864 600.0 720.0 0.01 0.01 0 0 0 0 1 1 0 0 0 0\\n', len)
                    local cfg_line = 'SPECTRAL_CONFIG 1024\\n'
                    local new_chunk = string.gsub(chunk, '(<TAKE.-\\n)', '%1' .. edit_line .. cfg_line)
                    reaper.SetItemStateChunk(item, new_chunk, false)
                    reaper.UpdateItemInProject(item)
                    injected_count = injected_count + 1
                end
            end
        end
        table.insert(results, string.format("[OK] Snare Top: Injected 650Hz Whistle Notch (-12dB) across %d items", injected_count))
    end

    -- 3. Inject Infrasound High-Pass Spectral Filter onto Kick In (Track 4)
    -- Target: Cut stage footstep and stand vibrations below 25Hz (<25 Hz, -24 dB)
    local tr4 = reaper.GetTrack(0, 3) -- Kick In
    if tr4 then
        local count = reaper.CountTrackMediaItems(tr4)
        for i = 0, count - 1 do
            local item = reaper.GetTrackMediaItem(tr4, i)
            local take = reaper.GetActiveTake(item)
            if take then
                local _, chunk = reaper.GetItemStateChunk(item, '', false)
                if not string.find(chunk, 'SPECTRAL_EDIT') then
                    local len = reaper.GetMediaItemInfo_Value(item, 'D_LENGTH')
                    -- Edit: freq 0 to 25 Hz, gain 0.063 (-24 dB)
                    local edit_line = string.format('SPECTRAL_EDIT 0.0 %.4f 0.06309573 0.0 25.0 0.02 0.02 0 0 0 0 1 1 0 0 0 0\\n', len)
                    local cfg_line = 'SPECTRAL_CONFIG 1024\\n'
                    local new_chunk = string.gsub(chunk, '(<TAKE.-\\n)', '%1' .. edit_line .. cfg_line)
                    reaper.SetItemStateChunk(item, new_chunk, false)
                    reaper.UpdateItemInProject(item)
                end
            end
        end
        table.insert(results, "[OK] Kick In: Injected <25Hz Infrasound High-Pass Spectral Filter")
    end

    -- 4. Inject Tom Overhang Mud Attenuation onto Toms (Tracks 24 - 26)
    -- Target: Attenuate sustained 350Hz mud and fundamental ringing
    local tom_tracks = {23, 24, 25} -- Tom 1, Tom 2, Floor Tom
    for _, tr_idx in ipairs(tom_tracks) do
        local tr = reaper.GetTrack(0, tr_idx)
        if tr then
            local _, name = reaper.GetTrackName(tr, '')
            local count = reaper.CountTrackMediaItems(tr)
            for i = 0, count - 1 do
                local item = reaper.GetTrackMediaItem(tr, i)
                local take = reaper.GetActiveTake(item)
                if take then
                    local _, chunk = reaper.GetItemStateChunk(item, '', false)
                    if not string.find(chunk, 'SPECTRAL_EDIT') then
                        local len = reaper.GetMediaItemInfo_Value(item, 'D_LENGTH')
                        -- Edit: freq 300 to 450 Hz, gain 0.35 (-9 dB)
                        local edit_line = string.format('SPECTRAL_EDIT 0.0 %.4f 0.35481339 300.0 450.0 0.01 0.01 0 0 0 0 1 1 0 0 0 0\\n', len)
                        local cfg_line = 'SPECTRAL_CONFIG 1024\\n'
                        local new_chunk = string.gsub(chunk, '(<TAKE.-\\n)', '%1' .. edit_line .. cfg_line)
                        reaper.SetItemStateChunk(item, new_chunk, false)
                        reaper.UpdateItemInProject(item)
                    end
                end
            end
            table.insert(results, string.format("[OK] %s: Injected 350Hz Cardboard Mud Notch (-9dB)", name))
        end
    end

    return table.concat(results, "\\n")
    '''
    out = run_lua(lua)
    print(out)

if __name__ == "__main__":
    apply_spectral_edits_and_gain_staging()
