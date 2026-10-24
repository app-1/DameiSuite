import sys, time
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

code = """
-- Start playback around chorus (e.g., position 85 seconds)
local cur_pos = reaper.GetCursorPosition()
local play_state = reaper.GetPlayState()
local is_playing = (play_state & 1) == 1

if not is_playing then
    reaper.SetEditCurPos(85.0, false, false)
    reaper.OnPlayButton()
end

-- Wait a moment to sample meters and telemetry
local trk15 = reaper.GetTrack(0, 14)
local trk4 = reaper.GetTrack(0, 3)

local function get_meters(trk)
    if not trk then return {peak_l = -100, peak_r = -100} end
    local peak_l = reaper.Track_GetPeakInfo(trk, 0)
    local peak_r = reaper.Track_GetPeakInfo(trk, 1)
    local db_l = peak_l > 0 and (20 * math.log(peak_l, 10)) or -100
    local db_r = peak_r > 0 and (20 * math.log(peak_r, 10)) or -100
    return {peak_l = db_l, peak_r = db_r}
end

-- Sample gmem via JSFX parameters or gmem
-- In JSFX, gmem[1400..1449] is Instrumental Bus, gmem[1450..1499] is Vocal Bus
-- Let's query TrackFX param values
local m15 = get_meters(trk15)
local m4 = get_meters(trk4)

return {
    cur_pos = reaper.GetPlayPosition(),
    is_playing = (reaper.GetPlayState() & 1) == 1,
    track15_meters = m15,
    track4_meters = m4
}
"""

print("Starting live playback test...")
res1 = run_lua(code)
time.sleep(2.0)

code_sample = """
local trk15 = reaper.GetTrack(0, 14)
local trk4 = reaper.GetTrack(0, 3)

local function get_meters(trk)
    if not trk then return {peak_l = -100, peak_r = -100} end
    local peak_l = reaper.Track_GetPeakInfo(trk, 0)
    local peak_r = reaper.Track_GetPeakInfo(trk, 1)
    local db_l = peak_l > 0 and (20 * math.log(peak_l, 10)) or -100
    local db_r = peak_r > 0 and (20 * math.log(peak_r, 10)) or -100
    return {peak_l = db_l, peak_r = db_r}
end

return {
    cur_pos = reaper.GetPlayPosition(),
    is_playing = (reaper.GetPlayState() & 1) == 1,
    track15_meters = get_meters(trk15),
    track4_meters = get_meters(trk4)
}
"""

res2 = run_lua(code_sample)
time.sleep(1.0)
res3 = run_lua(code_sample)

# Stop playback after test
run_lua("reaper.OnStopButton()")

import pprint
print("Sample at t+0s:")
pprint.pprint(res1)
print("Sample at t+2s:")
pprint.pprint(res2)
print("Sample at t+3s:")
pprint.pprint(res3)
