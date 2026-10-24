local log_path = "c:\\Dev\\DameiSuite\\tools\\reaper_session_status.txt"
local f = io.open(log_path, "w")

local function log(str)
  if f then f:write(str .. "\n") end
end

log("REAPER SESSION STATUS QUERY")
log("Time: " .. os.date())

local proj, proj_path = reaper.EnumProjects(-1)
log("Active Project: " .. tostring(proj_path))

local master_tr = reaper.GetMasterTrack(0)
local m_fx_cnt = reaper.TrackFX_GetCount(master_tr)
log(string.format("Master Track FX Count: %d", m_fx_cnt))
for i = 0, m_fx_cnt - 1 do
  local _, fx_name = reaper.TrackFX_GetFXName(master_tr, i, "")
  log(string.format("  Master FX %d: %s", i, fx_name))
end

local tr_cnt = reaper.CountTracks(0)
log(string.format("Total Tracks: %d", tr_cnt))
for t = 0, tr_cnt - 1 do
  local tr = reaper.GetTrack(0, t)
  local _, tr_name = reaper.GetTrackName(tr, "")
  local fx_cnt = reaper.TrackFX_GetCount(tr)
  log(string.format("Track %d: '%s' (FX Count: %d)", t + 1, tr_name, fx_cnt))
  for i = 0, fx_cnt - 1 do
    local _, fx_name = reaper.TrackFX_GetFXName(tr, i, "")
    log(string.format("   FX %d: %s", i, fx_name))
  end
end

reaper.gmem_attach("DameiMixMetering")
log(string.format("gmem[1159] (Static Calib Locked): %d", reaper.gmem_read(1159) or 0))
log(string.format("gmem[1158] (Shootout Monitor Mode): %d", reaper.gmem_read(1158) or 0))

if f then f:close() end
