local num_markers, num_regions = reaper.CountProjectMarkers(0)
local total = num_markers + num_regions

local f = io.open("c:/Dev/DameiAPI/project_markers_dump.txt", "w")
if f then
  f:write(string.format("Project Markers Count: %d markers, %d regions (Total: %d)\n", num_markers, num_regions, total))
  for i = 0, total - 1 do
    local retval, isrgn, pos, rgnend, name, markrgnindexnumber, color = reaper.EnumProjectMarkers3(0, i)
    f:write(string.format("[%d] isrgn=%s pos=%.3f rgnend=%.3f name='%s' idx=%d\n", i, tostring(isrgn), pos, rgnend, name, markrgnindexnumber))
  end
  f:close()
end
reaper.ShowConsoleMsg("Dumped project markers to c:/Dev/DameiAPI/project_markers_dump.txt\n")
