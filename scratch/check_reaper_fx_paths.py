import sys
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

script = r"""
local tr = reaper.GetMasterTrack(0)
local _, str = reaper.GetTrackStateChunk(tr, "", false)
local res = {}
for line in string.gmatch(str, "([^\r\n]+)") do
    if string.find(line, "<JS") or string.find(line, "Damei") then
        table.insert(res, line)
    end
end
return table.concat(res, "\n")
"""
print(run_lua(script))
