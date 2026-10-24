import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

play_and_measure = """
local tr = reaper.GetTrack(0, 14)
reaper.TrackFX_SetParam(tr, 5, 1, 6) -- Kel Pinchin (Split Chain)
reaper.SetEditCurPos(28.0, false, false)
reaper.CSurf_OnPlay()
local t0 = reaper.time_precise()
while reaper.time_precise() - t0 < 1.5 do end

reaper.gmem_attach('DameiMixMetering')
local gr = reaper.gmem_read(10)
local rms = reaper.gmem_read(11)
local peak = reaper.gmem_read(12)
local in_l = reaper.gmem_read(20)
local final_l = reaper.gmem_read(31)

local p_l = reaper.Track_GetPeakInfo(tr, 0)
local p_r = reaper.Track_GetPeakInfo(tr, 1)
local db_l = 20.0 * math.log(math.max(p_l, 0.00001), 10)
local db_r = 20.0 * math.log(math.max(p_r, 0.00001), 10)

reaper.CSurf_OnStop()

return string.format([[
Live Playback Telemetry at Chorus 28.0:
  Track 15 Master Out   : L=%.2f dBFS, R=%.2f dBFS
  Studio Bus Glue GR    : %.2f dB
  Instrumental RMS      : %.2f dBFS
  Instrumental Peak     : %.2f (%.2f dBFS)
  DSP Final L sample    : %.4f
  DSP In L sample       : %.4f
]], db_l, db_r, gr, rms, peak, 20.0 * math.log(math.max(peak, 0.00001), 10), final_l, in_l)
"""

print(run_lua(play_and_measure))
