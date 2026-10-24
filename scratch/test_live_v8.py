import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

test_lua = """
local tr = reaper.GetTrack(0, 14)

-- Set preset to 06: Kel Pinchin (Split Chain)
reaper.TrackFX_SetParam(tr, 5, 1, 6)

-- Play at 28.0 (Chorus)
reaper.SetEditCurPos(28.0, false, false)
reaper.CSurf_OnPlay()
"""
run_lua(test_lua)
time.sleep(1.5)

meter_lua = """
local tr = reaper.GetTrack(0, 14)
local p_l = reaper.Track_GetPeakInfo(tr, 0)
local p_r = reaper.Track_GetPeakInfo(tr, 1)
local db_l = 20.0 * math.log(math.max(p_l, 0.00001), 10)
local db_r = 20.0 * math.log(math.max(p_r, 0.00001), 10)

local res = {}
table.insert(res, string.format("Live Chorus Peak: L=%.2f dBFS, R=%.2f dBFS", db_l, db_r))

-- Read params from FX 5
local params_to_check = {
    {0, "Active Tab"},
    {1, "Producer Preset"},
    {3, "Headroom Trim (dB)"},
    {9, "Bus Glue Engaged"},
    {11, "Bus Glue Threshold (dB)"},
    {12, "Bus Glue Ratio"},
    {13, "Bus Glue Attack (ms)"},
    {14, "Bus Glue Release"},
    {15, "Bus Glue HPF (Hz)"},
    {23, "Harmonic Desk Drive (dB)"},
    {24, "Stereo Imager Width"},
    {37, "Ear-Candy Director Mode"},
    {38, "Ear-Candy Intensity %"}
}

for _, item in ipairs(params_to_check) do
    local p_idx, p_name = item[1], item[2]
    local val = reaper.TrackFX_GetParam(tr, 5, p_idx)
    local _, val_str = reaper.TrackFX_GetFormattedParamValue(tr, 5, p_idx, "")
    table.insert(res, string.format("   [%d] %s: %s (raw=%.2f)", p_idx, p_name, val_str, val))
end

reaper.CSurf_OnStop()
return table.concat(res, "\\n")
"""

print(run_lua(meter_lua))
