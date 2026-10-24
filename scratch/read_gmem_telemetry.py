import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

play_lua = """
local tr = reaper.GetTrack(0, 14)
reaper.TrackFX_SetParam(tr, 5, 1, 6) -- Kel Pinchin (Split Chain)
reaper.SetEditCurPos(28.0, false, false)
reaper.CSurf_OnPlay()
"""
run_lua(play_lua)
time.sleep(1.2)

read_lua = """
reaper.gmem_attach('DameiMixMetering')
local gr = reaper.gmem_read(10)
local rms = reaper.gmem_read(11)
local peak = reaper.gmem_read(12)
local width = reaper.gmem_read(13)
local pocket = reaper.gmem_read(14)
reaper.CSurf_OnStop()
return string.format("Live Chorus Telemetry:\\n  Studio Bus Glue GR : %.2f dB\\n  Instrumental RMS   : %.2f dBFS\\n  Peak               : %.2f (%.2f dBFS)\\n  Stereo Width       : %.2fx\\n  Vocal Pocket Dip   : -%.2f dB",
  gr, rms, peak, 20.0 * math.log(math.max(peak, 0.00001), 10), width, pocket)
"""

print(run_lua(read_lua))
