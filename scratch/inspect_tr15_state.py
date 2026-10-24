import sys
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

lua_code = """
local tr15 = reaper.GetTrack(0, 14) -- Track 15 INSTRUMENTAL//BUSS

local vol15 = reaper.GetMediaTrackInfo_Value(tr15, "D_VOL")
local pan15 = reaper.GetMediaTrackInfo_Value(tr15, "D_PAN")

local count = reaper.TrackFX_GetCount(tr15)
local fxs = {}
for i = 0, count - 1 do
    local _, name = reaper.TrackFX_GetFXName(tr15, i, "")
    local enabled = reaper.TrackFX_GetEnabled(tr15, i)
    table.insert(fxs, {idx = i, name = name, enabled = enabled})
end

-- Also check child bus faders:
-- Tr 16 DRUMS, Tr 40 SYNTHS, Tr 51 GUITAR, Tr 69 BASS
local tr16 = reaper.GetTrack(0, 15)
local tr40 = reaper.GetTrack(0, 39)
local tr51 = reaper.GetTrack(0, 50)
local tr69 = reaper.GetTrack(0, 68)

local vol16 = reaper.GetMediaTrackInfo_Value(tr16, "D_VOL")
local vol40 = reaper.GetMediaTrackInfo_Value(tr40, "D_VOL")
local vol51 = reaper.GetMediaTrackInfo_Value(tr51, "D_VOL")
local vol69 = reaper.GetMediaTrackInfo_Value(tr69, "D_VOL")

return {
    tr15 = {vol = vol15, pan = pan15, fxs = fxs},
    buses = {
        drums = vol16,
        synths = vol40,
        guitar = vol51,
        bass = vol69
    }
}
"""

res = run_lua(lua_code)
import json, math
def to_db(v): return f"{20*math.log10(v):+.2f} dB" if v > 0.00001 else "-inf"

print("Track 15 Vol:", res["tr15"]["vol"], f"({to_db(res['tr15']['vol'])})")
for k, v in res["buses"].items():
    print(f"  {k:8s} fader: {v:.4f} ({to_db(v)})")
print("Track 15 FX:")
for fx in res["tr15"]["fxs"]:
    print(f"  [{fx['idx']}] {fx['name']} (enabled: {fx['enabled']})")
