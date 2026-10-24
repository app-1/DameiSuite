-- ==============================================================================
-- Damei Session Snapshot (Phase 0 regression tool)
-- Dumps every parameter of every Damei JSFX on every track + master to JSON.
-- Used to (a) derive bus Preset 6 from the REAL current calibration and
--         (b) prove later phases did not alter the active mix.
-- Output: c:\Dev\DameiSuite\tools\session_snapshots\snapshot_<time>.json and latest.json
-- ==============================================================================
local OUT_DIR = "c:\\Dev\\DameiSuite\\tools\\session_snapshots\\"
reaper.RecursiveCreateDirectory(OUT_DIR, 0)

local function esc(s) return (tostring(s):gsub('[%c"\\]', function(c) return string.format("\\u%04x", c:byte()) end)) end

local parts = {}
local function scan(track, label)
  local n = reaper.TrackFX_GetCount(track)
  for fx = 0, n - 1 do
    local _, name = reaper.TrackFX_GetFXName(track, fx, "")
    if name:lower():find("damei", 1, true) then
      local params = {}
      for p = 0, reaper.TrackFX_GetNumParams(track, fx) - 1 do
        local _, pn = reaper.TrackFX_GetParamName(track, fx, p, "")
        local v, mn, mx = reaper.TrackFX_GetParam(track, fx, p)
        params[#params + 1] = string.format('{"i":%d,"name":"%s","v":%.6f,"min":%.6f,"max":%.6f}', p, esc(pn), v, mn, mx)
      end
      parts[#parts + 1] = string.format('{"track":"%s","fx_index":%d,"fx":"%s","enabled":%s,"params":[%s]}',
        esc(label), fx, esc(name), tostring(reaper.TrackFX_GetEnabled(track, fx)), table.concat(params, ","))
    end
  end
end

scan(reaper.GetMasterTrack(0), "MASTER")
for t = 0, reaper.CountTracks(0) - 1 do
  local tr = reaper.GetTrack(0, t)
  local _, nm = reaper.GetTrackName(tr, "")
  scan(tr, nm)
end

local json = '{"time":"' .. os.date("%Y-%m-%d %H:%M:%S") .. '","fx":[' .. table.concat(parts, ",") .. "]}"
for _, fname in ipairs({ "snapshot_" .. os.date("%Y%m%d_%H%M%S") .. ".json", "latest.json" }) do
  local f = io.open(OUT_DIR .. fname, "w")
  if f then f:write(json); f:close() end
end
reaper.ShowConsoleMsg(string.format("Damei snapshot: %d FX instances saved.\n", #parts))
