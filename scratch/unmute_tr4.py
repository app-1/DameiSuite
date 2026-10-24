import sys
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

lua_code = """
local tr4 = reaper.GetTrack(0, 3)
reaper.SetMediaTrackInfo_Value(tr4, "B_MUTE", 0)
return {unmuted = true}
"""

res = run_lua(lua_code)
import json
print(json.dumps(res))
