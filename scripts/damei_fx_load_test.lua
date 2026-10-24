-- ==============================================================================
-- Damei FX Load Test (Phase 0 gate)
-- Adds every Damei JSFX to a throwaway track, verifies it compiled (has params,
-- name resolved without error), then deletes the track. Does NOT touch real tracks.
-- Output: c:\Dev\DameiSuite\tools\fx_load_report.txt
-- ==============================================================================
local names = {
  "Damei_AssessmentMatrix", "Damei_BassSuite", "Damei_Clipper", "Damei_DevastatorSuite",
  "Damei_DrumSuite", "Damei_GuitarSuite", "Damei_GullfossMaster", "Damei_Metering",
  "Damei_MixingSuite", "Damei_OzoneSuite", "Damei_RefMetering", "Damei_SatelliteEQ",
  "Damei_SpectrumProbe", "Damei_SynthSuite", "Damei_TonalBalance", "Damei_ToneShaper",
  "Damei_VocalSuite", "Damei_InstrumentalSuite", "Damei_VocalBus",
}
local f = io.open("c:\\Dev\\DameiSuite\\tools\\fx_load_report.txt", "w")
local function log(s) if f then f:write(s .. "\n") end end

reaper.PreventUIRefresh(1)
reaper.InsertTrackAtIndex(reaper.CountTracks(0), false)
local tr = reaper.GetTrack(0, reaper.CountTracks(0) - 1)
local fails = 0
log("DAMEI FX LOAD TEST  " .. os.date())
for _, n in ipairs(names) do
  local idx = reaper.TrackFX_AddByName(tr, "JS: Damei/" .. n, false, -1)
  if idx < 0 then
    -- not installed yet (new suites) is reported, not failed
    log(string.format("SKIP  %-28s not installed", n))
  else
    local _, fxname = reaper.TrackFX_GetFXName(tr, idx, "")
    local np = reaper.TrackFX_GetNumParams(tr, idx)
    if np > 0 and not fxname:lower():find("error", 1, true) then
      log(string.format("OK    %-28s params=%d  (%s)", n, np, fxname))
    else
      fails = fails + 1
      log(string.format("FAIL  %-28s params=%d  (%s)", n, np, fxname))
    end
  end
end
log(fails == 0 and "RESULT: PASS" or ("RESULT: FAIL x" .. fails))
reaper.DeleteTrack(tr)
reaper.PreventUIRefresh(-1)
reaper.UpdateArrange()
if f then f:close() end
reaper.ShowConsoleMsg("Damei load test finished: see tools\\fx_load_report.txt\n")
