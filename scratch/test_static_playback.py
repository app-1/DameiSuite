import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua = r"""
-- Play for 1.5 seconds at bar 28
reaper.SetEditCurPos(52.683, false, false)
reaper.OnPlayButton()
local t0 = reaper.time_precise()
while reaper.time_precise() - t0 < 1.5 do end
reaper.OnStopButton()

-- Read gmem values via a small temporary probe or direct inspect
-- Let's check Track 15 Instrumental Suite parameters
local tr15 = reaper.GetTrack(0, 14)
local s8 = reaper.TrackFX_GetParam(tr15, 5, 2)  -- slider8
local s9 = reaper.TrackFX_GetParam(tr15, 5, 3)  -- slider9
local s12 = reaper.TrackFX_GetParam(tr15, 5, 6) -- slider12 (threshold)
local s25 = reaper.TrackFX_GetParam(tr15, 5, 17) -- slider25 (width)

return string.format("Playback test complete at 52.683s. S8: %.2f, S9: %.2f, S12: %.2f, S25: %.2f", s8, s9, s12, s25)
"""

print(run_lua(lua))
