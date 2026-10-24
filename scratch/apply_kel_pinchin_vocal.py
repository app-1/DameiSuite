import sys, math
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

lua_code = """
local tr4 = reaper.GetTrack(0, 3) -- Track 4 VOX
local tr5 = reaper.GetTrack(0, 4) -- Track 5 Lead Vox
local tr15 = reaper.GetTrack(0, 14) -- Track 15 INST BUS
local master = reaper.GetMasterTrack(0)

-- 1. Reload VocalSuite to catch the new Kel Pinchin code
reaper.TrackFX_SetOffline(tr4, 0, true)
reaper.TrackFX_SetOffline(tr4, 0, false)

-- 2. Calibrate Track 5 fader: 0.85 (-1.4 dB)
reaper.SetMediaTrackInfo_Value(tr5, "D_VOL", 0.85)

-- 3. Calibrate Track 4 fader: 1.0 (0.0 dB Unity)
reaper.SetMediaTrackInfo_Value(tr4, "D_VOL", 1.0)

-- 4. Apply Kel Pinchin Preset 5 on VocalSuite
reaper.TrackFX_SetParam(tr4, 0, 17, 5) -- slider18 = 5 (Kel Pinchin)

-- Ensure Kel Pinchin parameters are set:
reaper.TrackFX_SetParam(tr4, 0, 38, 1) -- slider43 = 1 (FET 8:1)
reaper.TrackFX_SetParam(tr4, 0, 39, 0) -- slider44 = 0 (Opto Compress)
reaper.TrackFX_SetParam(tr4, 0, 40, 1) -- slider45 = 1 (LA-2A Sidechain Emphasis)
reaper.TrackFX_SetParam(tr4, 0, 41, 1) -- slider46 = 1 (LOADES Split-Band)
reaper.TrackFX_SetParam(tr4, 0, 42, 95) -- slider47 = 95 Hz HPF
reaper.TrackFX_SetParam(tr4, 0, 43, -2.5) -- slider48 = -2.5 dB @ 380 Hz
reaper.TrackFX_SetParam(tr4, 0, 44, -2.2) -- slider49 = -2.2 dB @ 5.2 kHz
reaper.TrackFX_SetParam(tr4, 0, 2, 6600) -- slider3 = 6600 Hz De-Esser
reaper.TrackFX_SetParam(tr4, 0, 3, -23.0) -- slider4 = -23 dBFS Threshold
reaper.TrackFX_SetParam(tr4, 0, 4, 3.8) -- slider5 = 3.8 dB Max GR
reaper.TrackFX_SetParam(tr4, 0, 5, 28) -- slider6 = 28% FET
reaper.TrackFX_SetParam(tr4, 0, 6, 24) -- slider7 = 24% Opto
reaper.TrackFX_SetParam(tr4, 0, 7, 1.20) -- slider8 = 1.20 Stereo Backing Width
reaper.TrackFX_SetParam(tr4, 0, 8, 1) -- slider9 = 1 Center Lead Lock
reaper.TrackFX_SetParam(tr4, 0, 9, 2.0) -- slider10 = +2.0 dB Maag 16kHz Air
reaper.TrackFX_SetParam(tr4, 0, 10, 1.4) -- slider11 = +1.4 dB 1.8kHz Presence
reaper.TrackFX_SetParam(tr4, 0, 13, 1) -- slider14 = 1 Hermite Soft-Clip
reaper.TrackFX_SetParam(tr4, 0, 14, -0.5) -- slider15 = -0.5 dBTP Ceiling
reaper.TrackFX_SetParam(tr4, 0, 15, 1) -- slider16 = 1 Strict Ceiling Guardian
reaper.TrackFX_SetParam(tr4, 0, 16, 1.8) -- slider17 = +1.8 dB Output Makeup Trim (Sankofa pocket balance)
reaper.TrackFX_SetParam(tr4, 0, 34, 1) -- slider39 = 1 Ear-Candy Director
reaper.TrackFX_SetParam(tr4, 0, 35, 35) -- slider40 = 35% Ear-Candy Amount
reaper.TrackFX_SetParam(tr4, 0, 36, 12607) -- slider41 = 12607 Kel Pinchin Palette
reaper.TrackFX_SetParam(tr4, 0, 37, 1) -- slider42 = 1 Follow Producer

-- 5. Set MixingSuite Center Donut Hole & Vocal Pocket on Master FX 0
local _, mix_name = reaper.TrackFX_GetFXName(master, 0, "")
if mix_name:find("Mixing Suite") then
    -- Find slider28 (Donut-Hole Notch) and slider41 (Vocal Trim)
    for p = 0, reaper.TrackFX_GetNumParams(master, 0) - 1 do
        local _, pname = reaper.TrackFX_GetParamName(master, 0, p, "")
        local pl = pname:lower()
        if pl:find("donut") or pl:find("carve") or pl:find("center notch") then
            reaper.TrackFX_SetParam(master, 0, p, 2) -- Deep Cut -3.5 dB @ 2500 Hz
        elseif pl:find("vocal trim") or pl:find("vox trim") then
            reaper.TrackFX_SetParam(master, 0, p, 0.5) -- +0.5 dB Balanced Pocket
        end
    end
end

-- 6. Check Guitar Suite on Track 51 for Center Vocal Pocket Carve
local tr51 = reaper.GetTrack(0, 50)
for f = 0, reaper.TrackFX_GetCount(tr51) - 1 do
    local _, gname = reaper.TrackFX_GetFXName(tr51, f, "")
    if gname:find("Guitar") then
        for p = 0, reaper.TrackFX_GetNumParams(tr51, f) - 1 do
            local _, pname = reaper.TrackFX_GetParamName(tr51, f, p, "")
            if pname:lower():find("pocket") or pname:lower():find("unmask") then
                reaper.TrackFX_SetParam(tr51, f, p, 1)
            end
        end
    end
end

-- 7. Check Synth Suite on Track 40
local tr40 = reaper.GetTrack(0, 39)
for f = 0, reaper.TrackFX_GetCount(tr40) - 1 do
    local _, sname = reaper.TrackFX_GetFXName(tr40, f, "")
    if sname:find("Synth") then
        for p = 0, reaper.TrackFX_GetNumParams(tr40, f) - 1 do
            local _, pname = reaper.TrackFX_GetParamName(tr40, f, p, "")
            if pname:lower():find("pocket") or pname:lower():find("unmask") then
                reaper.TrackFX_SetParam(tr40, f, p, 1)
            end
        end
    end
end

return {ok = true}
"""

res = run_lua(lua_code)
import json
print(json.dumps(res, indent=2))
