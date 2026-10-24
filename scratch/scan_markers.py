import sys
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

lua = """
local res = {}
local _, num_markers, num_regions = reaper.CountProjectMarkers(0)
for i = 0, num_markers + num_regions - 1 do
    local _, isrgn, pos, rgnend, name, markrgnindexnumber = reaper.EnumProjectMarkers(i)
    table.insert(res, string.format("[%s] pos=%.2f end=%.2f name='%s'", isrgn and "RGN" or "MRK", pos, rgnend, name))
end
return table.concat(res, "\\n")
"""
print(run_lua(lua))
