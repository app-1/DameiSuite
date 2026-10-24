import sys
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

lua_code = """
local tr4 = reaper.GetTrack(0, 3)
local tr5 = reaper.GetTrack(0, 4)

local mute4 = reaper.GetMediaTrackInfo_Value(tr4, "B_MUTE")
local solo4 = reaper.GetMediaTrackInfo_Value(tr4, "I_SOLO")
local mute5 = reaper.GetMediaTrackInfo_Value(tr5, "B_MUTE")
local solo5 = reaper.GetMediaTrackInfo_Value(tr5, "I_SOLO")

return {
    tr4 = {mute = mute4, solo = solo4},
    tr5 = {mute = mute5, solo = solo5}
}
"""

res = run_lua(lua_code)
import json
print(json.dumps(res, indent=2))
