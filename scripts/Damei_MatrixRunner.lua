-- Damei Matrix Runner
-- 1) Renders the master mix + bus stems (DRUMS, GUITAR, BASS, VOX, SYNTHS, CINEMATIC FX) to MatrixRender\
-- 2) Optionally plays the whole project through Damei Assessment Matrix (on the master) and saves its live
--    readings (gmem) to MatrixRender\matrix_live.json so Python can verify the JSFX against its own analysis.
-- Run from REAPER: Actions > Show action list > New action > Load ReaScript...  (open HexGyal.rpp first)

local OUT = "H:\\HexGirls2\\HexGyal\\MatrixRender"
local BUSES = { ["DRUMS"]=1, ["GUITAR"]=1, ["BASS"]=1, ["VOX"]=1, ["SYNTHS"]=1, ["CINEMATIC FX"]=1 }

reaper.RecursiveCreateDirectory(OUT, 0)

-- select the bus tracks (stems render the selected tracks)
reaper.Main_OnCommand(40297, 0) -- unselect all tracks
local picked = {}
for i = 0, reaper.CountTracks(0) - 1 do
  local tr = reaper.GetTrack(0, i)
  local _, name = reaper.GetTrackName(tr)
  if BUSES[string.upper(name)] then
    reaper.SetTrackSelected(tr, true)
    picked[#picked + 1] = name
  end
end

if #picked == 0 then
  reaper.MB("No bus tracks found (expected DRUMS, GUITAR, BASS, VOX, SYNTHS, CINEMATIC FX).", "Matrix Runner", 0)
  return
end

local ok = reaper.MB("Render master + " .. #picked .. " bus stems to:\n" .. OUT ..
  "\n\nBuses: " .. table.concat(picked, ", ") .. "\n\nContinue?", "Damei Matrix Runner", 1)
if ok ~= 1 then return end

reaper.GetSetProjectInfo(0, "RENDER_SETTINGS", 1, true)      -- master mix + stems (selected tracks)
reaper.GetSetProjectInfo(0, "RENDER_BOUNDSFLAG", 1, true)    -- entire project
reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 2, true)
reaper.GetSetProjectInfo(0, "RENDER_SRATE", 44100, true)
reaper.GetSetProjectInfo_String(0, "RENDER_FILE", OUT, true)
reaper.GetSetProjectInfo_String(0, "RENDER_PATTERN", "$track", true)
reaper.Main_OnCommand(42230, 0) -- render using most recent settings, auto-close dialog

-- live capture through the Assessment Matrix
local go = reaper.MB("Render finished.\n\nNow play the whole project in real time through the Assessment Matrix " ..
  "and save its live readings?\n(Needs Damei Assessment Matrix on the master. Takes the song's length.)",
  "Damei Matrix Runner", 4)
if go ~= 6 then return end

reaper.gmem_attach("DameiMixMetering")
local len = reaper.GetProjectLength(0)
reaper.SetEditCurPos(0, true, false)
reaper.OnPlayButton()
local t0 = reaper.time_precise()

local function save()
  local keys = {
    "active", "overall", "tonal", "stereo", "dynamics", "preset", "stage",
    "dev0", "dev1", "dev2", "dev3", "dev4", "dev5", "dev6",
    "wdev0", "wdev1", "wdev2", "wdev3", "wdev4", "wdev5", "wdev6",
    "lufs", "plr", "corr", "heartbeat",
  }
  local parts = {}
  for i, k in ipairs(keys) do
    parts[#parts + 1] = string.format('"%s": %.6f', k, reaper.gmem_read(1099 + i))
  end
  local f = io.open(OUT .. "\\matrix_live.json", "w")
  if f then f:write("{\n  " .. table.concat(parts, ",\n  ") .. "\n}\n"); f:close() end
end

local function loop()
  local pos = reaper.GetPlayPosition()
  if reaper.GetPlayState() & 1 == 0 or pos >= len - 0.05 or reaper.time_precise() - t0 > len + 30 then
    reaper.OnStopButton()
    if reaper.gmem_read(1100) == 1 then
      save()
      reaper.MB("Saved live Matrix readings to:\n" .. OUT .. "\\matrix_live.json", "Damei Matrix Runner", 0)
    else
      reaper.MB("Assessment Matrix was not detected on the master (gmem inactive).", "Damei Matrix Runner", 0)
    end
    return
  end
  reaper.defer(loop)
end
loop()
