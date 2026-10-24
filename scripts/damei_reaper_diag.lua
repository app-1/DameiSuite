local f = io.open("c:\\Dev\\DameiSuite\\tools\\reaper_diag.txt", "w")
local function log(s) f:write(s .. "\n") end
log("DIAG " .. os.date())
log("REAPER version: " .. reaper.GetAppVersion())
local i = 0
while true do
  local proj, path = reaper.EnumProjects(i)
  if not proj then break end
  local act = (reaper.EnumProjects(-1) == proj) and "  <-- ACTIVE" or ""
  log(string.format("Project[%d] path='%s' tracks=%d%s", i, tostring(path), reaper.CountTracks(proj), act))
  local mt = reaper.GetMasterTrack(proj)
  local function dump(tr, label)
    local n = reaper.TrackFX_GetCount(tr)
    local nm = reaper.TrackFX_GetRecCount and reaper.TrackFX_GetRecCount(tr) or 0
    log(string.format("  %s: fx=%d inputfx=%d", label, n, nm))
    for k = 0, n - 1 do
      local _, name = reaper.TrackFX_GetFXName(tr, k, "")
      log("     " .. k .. ": " .. name)
    end
  end
  dump(mt, "MASTER")
  for t = 0, reaper.CountTracks(proj) - 1 do
    local tr = reaper.GetTrack(proj, t)
    local _, tn = reaper.GetTrackName(tr, "")
    dump(tr, "Track " .. (t + 1) .. " '" .. tn .. "'")
  end
  i = i + 1
end
f:close()
