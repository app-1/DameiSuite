import sys
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

code = """
-- Reload Track 15 FX 5 (Damei Instrumental Bus Alchemist)
local trk15 = reaper.GetTrack(0, 14)
if trk15 then
    local fx_cnt = reaper.TrackFX_GetCount(trk15)
    for i = fx_cnt - 1, 0, -1 do
        local _, name = reaper.TrackFX_GetFXName(trk15, i, "")
        if name:find("Instrumental Bus") or name:find("Damei_InstrumentalSuite") then
            reaper.TrackFX_Delete(trk15, i)
        end
    end
    -- Add the fresh new one
    local new_idx = reaper.TrackFX_AddByName(trk15, "Damei_InstrumentalSuite.jsfx", false, -1)
    reaper.TrackFX_Show(trk15, new_idx, 3)
end

-- Reload Track 4 FX 1 (Damei Vocal Empress)
local trk4 = reaper.GetTrack(0, 3)
if trk4 then
    local fx_cnt = reaper.TrackFX_GetCount(trk4)
    for i = fx_cnt - 1, 0, -1 do
        local _, name = reaper.TrackFX_GetFXName(trk4, i, "")
        if name:find("Vocal Empress") or name:find("Damei_VocalBus") then
            reaper.TrackFX_Delete(trk4, i)
        end
    end
    -- Add the fresh new one
    local new_idx = reaper.TrackFX_AddByName(trk4, "Damei_VocalBus.jsfx", false, -1)
    reaper.TrackFX_Show(trk4, new_idx, 3)
end

return "RELOADED"
"""

res = run_lua(code)
print("Reload result:", res)
