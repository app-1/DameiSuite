import sys
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua
import json

lua_code = """
local function inspect_track(tr_idx)
    local tr = reaper.GetTrack(0, tr_idx)
    if not tr then return nil end
    local _, tr_name = reaper.GetTrackName(tr, "")
    local vol = reaper.GetMediaTrackInfo_Value(tr, "D_VOL")
    local pan = reaper.GetMediaTrackInfo_Value(tr, "D_PAN")
    local mute = reaper.GetMediaTrackInfo_Value(tr, "B_MUTE")
    local fx_count = reaper.TrackFX_GetCount(tr)
    local fxs = {}
    for i = 0, fx_count - 1 do
        local _, name = reaper.TrackFX_GetFXName(tr, i, "")
        local enabled = reaper.TrackFX_GetEnabled(tr, i)
        local num_params = reaper.TrackFX_GetNumParams(tr, i)
        local params = {}
        for p = 0, math.min(num_params - 1, 15) do
            local _, pname = reaper.TrackFX_GetParamName(tr, i, p, "")
            local val = reaper.TrackFX_GetParam(tr, i, p)
            local _, fmt = reaper.TrackFX_GetFormattedParamValue(tr, i, p, "")
            table.insert(params, {p = p, name = pname, val = val, fmt = fmt})
        end
        table.insert(fxs, {idx = i, name = name, enabled = enabled, num_params = num_params, params = params})
    end
    return {name = tr_name, vol = vol, pan = pan, mute = mute, fxs = fxs}
end

return {
    tr4 = inspect_track(3),  -- Track 4 (0-indexed: 3) VOX
    tr15 = inspect_track(14), -- Track 15 (0-indexed: 14) INSTRUMENTAL//BUSS
}
"""

res = run_lua(lua_code)
for tkey, tr in res.items():
    print(f"=== {tr['name']} (vol: {tr['vol']}, mute: {tr['mute']}) ===")
    for fx in tr['fxs']:
        print(f"  FX [{fx['idx']}] {fx['name']} -> Enabled: {fx['enabled']}")
        for p in fx['params'][:6]:
            print(f"      param {p['p']}: {p['name']} = {p['fmt']} ({p['val']:.4f})")
