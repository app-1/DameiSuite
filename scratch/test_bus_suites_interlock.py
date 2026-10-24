import sys, time
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

code = """
-- 1. Track 15: Bypass all plugins except Damei Instrumental Bus Alchemist
local trk15 = reaper.GetTrack(0, 14)
local trk15_state = {}
if trk15 then
    local fx_cnt = reaper.TrackFX_GetCount(trk15)
    for i = 0, fx_cnt - 1 do
        local _, name = reaper.TrackFX_GetFXName(trk15, i, "")
        local was_enabled = reaper.TrackFX_GetEnabled(trk15, i)
        local is_alchemist = name:find("Instrumental Bus") or name:find("Damei_InstrumentalSuite")
        table.insert(trk15_state, {idx = i, name = name, was_enabled = was_enabled, keep_enabled = is_alchemist ~= nil})
        if is_alchemist then
            reaper.TrackFX_SetEnabled(trk15, i, true)
            -- Ensure it is engaged (slider27 = 1) and in unity baseline (slider2 = 0)
            reaper.TrackFX_SetParam(trk15, i, 26, 1.0) -- slider27: 0=bypass, 1=engaged
            reaper.TrackFX_SetParam(trk15, i, 1, 0.0)  -- slider2: preset 0
        else
            reaper.TrackFX_SetEnabled(trk15, i, false) -- Bypass all others
        end
    end
end

-- 2. Track 4: Verify Vocal Sovereign and Vocal Empress
local trk4 = reaper.GetTrack(0, 3)
local trk4_state = {}
if trk4 then
    local fx_cnt = reaper.TrackFX_GetCount(trk4)
    for i = 0, fx_cnt - 1 do
        local _, name = reaper.TrackFX_GetFXName(trk4, i, "")
        local was_enabled = reaper.TrackFX_GetEnabled(trk4, i)
        table.insert(trk4_state, {idx = i, name = name, was_enabled = was_enabled})
        -- Ensure Vocal Empress is enabled, engaged, and in unity baseline
        if name:find("Vocal Empress") or name:find("Damei_VocalBus") then
            reaper.TrackFX_SetEnabled(trk4, i, true)
            reaper.TrackFX_SetParam(trk4, i, 21, 1.0) -- slider22: 1=engaged
            reaper.TrackFX_SetParam(trk4, i, 1, 0.0)  -- slider2: preset 0 (Unity Baseline)
        end
    end
end

return {
    track15 = trk15_state,
    track4 = trk4_state
}
"""

res = run_lua(code)
import pprint
print("--- PRE-TEST STAGING ---")
pprint.pprint(res)
