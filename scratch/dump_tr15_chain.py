import sys, json
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

code = """
local tr15 = reaper.GetTrack(0, 14)
if not tr15 then return {error = 'No track 15'} end

local count = reaper.TrackFX_GetCount(tr15)
local report = {}
for i = 0, count - 1 do
    local _, fxname = reaper.TrackFX_GetFXName(tr15, i, '')
    local enabled = reaper.TrackFX_GetEnabled(tr15, i)
    local num_params = reaper.TrackFX_GetNumParams(tr15, i)
    local params = {}
    for p = 0, num_params - 1 do
        local _, pname = reaper.TrackFX_GetParamName(tr15, i, p, '')
        local val = reaper.TrackFX_GetParam(tr15, i, p)
        local _, fmt = reaper.TrackFX_GetFormattedParamValue(tr15, i, p, '')
        table.insert(params, {idx = p, name = pname, val = val, fmt = fmt})
    end
    table.insert(report, {
        fx_idx = i,
        fx_name = fxname,
        enabled = enabled,
        num_params = num_params,
        params = params
    })
end
return report
"""

res = run_lua(code)
with open(r'c:\Dev\DameiSuite\scratch\tr15_legacy_chain_dump.json', 'w') as f:
    json.dump(res, f, indent=2)

for fx in res:
    print(f"=== FX {fx['fx_idx']}: {fx['fx_name']} (Enabled: {fx['enabled']}, Params: {fx['num_params']}) ===")
    for p in fx['params']:
        name_l = p['name'].lower()
        # print non-zero or notable params
        if abs(p['val']) > 0.0001 or any(k in name_l for k in ['gain', 'thresh', 'drive', 'boost', 'on', 'freq', 'ratio', 'attack', 'release', 'hpf', 'fat', 'trim', 'wet']):
            print(f"   [{p['idx']:2d}] {p['name']:32s} = {p['fmt']} (raw: {p['val']:.4f})")
