import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

# Recompile / reload FX 5 on Track 15
recompile_lua = """
local tr = reaper.GetTrack(0, 14)
-- Toggle offline / online to force JSFX recompile from disk
reaper.TrackFX_SetOffline(tr, 5, true)
local t0 = reaper.time_precise()
while reaper.time_precise() - t0 < 0.2 do end
reaper.TrackFX_SetOffline(tr, 5, false)
reaper.TrackFX_SetEnabled(tr, 5, true)

-- Ensure legacy FX (0..4) are bypassed
for i = 0, 4 do
    reaper.TrackFX_SetEnabled(tr, i, false)
end

local _, name = reaper.TrackFX_GetFXName(tr, 5, "")
local num_params = reaper.TrackFX_GetNumParams(tr, 5)
return string.format("Reloaded FX 5: %s (Num Params: %d)", name, num_params)
"""

print(run_lua(recompile_lua))
