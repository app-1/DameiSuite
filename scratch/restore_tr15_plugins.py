import sys
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

lua_code = """
local tr15 = reaper.GetTrack(0, 14) -- Track 15 INSTRUMENTAL//BUSS
if tr15 then
    local count = reaper.TrackFX_GetCount(tr15)
    for i = 0, count - 1 do
        local _, name = reaper.TrackFX_GetFXName(tr15, i, "")
        -- Re-enable Britson Buss, TB Equalizer Pro, DeeGain, Bass Manager, BUSTERse
        if not (name:find("Instrumental Bus") or name:find("Damei_InstrumentalSuite")) then
            reaper.TrackFX_SetEnabled(tr15, i, true)
        end
    end
end

-- Verify all FX on Track 15
local fxs15 = {}
if tr15 then
    local count = reaper.TrackFX_GetCount(tr15)
    for i = 0, count - 1 do
        local _, name = reaper.TrackFX_GetFXName(tr15, i, "")
        local en = reaper.TrackFX_GetEnabled(tr15, i)
        table.insert(fxs15, {idx = i, name = name, enabled = en})
    end
end

-- Verify Track 4
local tr4 = reaper.GetTrack(0, 3)
local fxs4 = {}
if tr4 then
    local count = reaper.TrackFX_GetCount(tr4)
    for i = 0, count - 1 do
        local _, name = reaper.TrackFX_GetFXName(tr4, i, "")
        local en = reaper.TrackFX_GetEnabled(tr4, i)
        table.insert(fxs4, {idx = i, name = name, enabled = en})
    end
end

return {
    tr15 = fxs15,
    tr4 = fxs4
}
"""

res = run_lua(lua_code)
print("--- TRACK 15 FX RESTORATION ---")
for fx in res["tr15"]:
    print(f"  [{fx['idx']}] {fx['name']} -> Enabled: {fx['enabled']}")

print("--- TRACK 4 FX STATUS ---")
for fx in res["tr4"]:
    print(f"  [{fx['idx']}] {fx['name']} -> Enabled: {fx['enabled']}")
