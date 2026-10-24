import sys, time
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

code = """
reaper.gmem_attach("DameiMixMetering")
local t_now = reaper.time_precise()

-- Instrumental Bus: gmem[1400..1449]
local ib_time = reaper.gmem_read(1400)
local ib_alive = (t_now - ib_time) < 1.0
local ib_active = reaper.gmem_read(1401)
local ib_rms = reaper.gmem_read(1402)
local ib_peak = reaper.gmem_read(1403)
local ib_crest = reaper.gmem_read(1404)
local ib_sub_peak = reaper.gmem_read(1405)
local ib_prof = reaper.gmem_read(1407)

-- Vocal Bus: gmem[1450..1499]
local vb_time = reaper.gmem_read(1450)
local vb_alive = (t_now - vb_time) < 1.0
local vb_active = reaper.gmem_read(1451)
local vb_rms = reaper.gmem_read(1452)
local vb_peak = reaper.gmem_read(1453)
local vb_crest = reaper.gmem_read(1454)
local vb_corridor = reaper.gmem_read(1455)
local vb_prof = reaper.gmem_read(1457)

return {
    inst_bus = {
        time_diff = t_now - ib_time,
        alive = ib_alive,
        active = ib_active,
        rms = ib_rms,
        peak = ib_peak,
        crest = ib_crest,
        profile = ib_prof
    },
    vocal_bus = {
        time_diff = t_now - vb_time,
        alive = vb_alive,
        active = vb_active,
        rms = vb_rms,
        peak = vb_peak,
        crest = vb_crest,
        profile = vb_prof
    }
}
"""

res = run_lua(code)
import pprint
print("--- GMEM BIDIRECTIONAL BUS INTERLOCK TELEMETRY ---")
pprint.pprint(res)
