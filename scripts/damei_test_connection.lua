-- ============================================================================
-- Damei Mix Assistant -- Connection & Integration Audit
-- File: damei_test_connection.lua
-- Run from: REAPER Actions -> Show Action List -> Load -> run once
-- ============================================================================

reaper.ClearConsole()
local out = {}
local function p(s) out[#out+1] = s end
local function sep(c) p(string.rep(c or "-", 60)) end

p("=== DAMEI SUBSYSTEM & CONNECTION AUDIT ===")
p(string.format("Time: %.3f   Play State: %d",
  reaper.time_precise(), reaper.GetPlayState()))
sep("=")

-- [1] Master Track FX Chain
p("\n[1] MASTER BUS FX CHAIN")
sep()
local master    = reaper.GetMasterTrack(0)
local fx_count  = reaper.TrackFX_GetCount(master)
local tbc_idx   = -1
local meter_idx = -1
for f = 0, fx_count - 1 do
  local _, nm = reaper.TrackFX_GetFXName(master, f, "")
  local tag = reaper.TrackFX_GetEnabled(master, f) and "[ON ]" or "[OFF]"
  p(string.format("  FX [%d] %s %s", f, tag, nm))
  if nm:find("TonalBalance", 1, true) then tbc_idx   = f end
  if nm:find("Metering",     1, true) and nm:find("Damei", 1, true) then meter_idx = f end
end
p(string.format("\n  TonalBalance slot: %s", tbc_idx >= 0 and tostring(tbc_idx) or "NOT FOUND"))
p(string.format("  Damei_Metering slot: %s", meter_idx >= 0 and tostring(meter_idx) or "NOT FOUND"))
if tbc_idx > 0 then
  p("  [!] TonalBalance not at slot 0 -- run damei_init_session.lua to stage chain.")
end
if meter_idx >= 0 and meter_idx ~= fx_count - 1 then
  p("  [!] Damei_Metering not final -- LUFS reads pre-limiter signal.")
end

-- [2] gmem Telemetry Bus
sep("=")
p("\n[2] GMEM TELEMETRY BUS (DameiMetering)")
sep()
reaper.gmem_attach("DameiMetering")
local function gmr(i) return reaper.gmem_read(i) or 0 end
local hb    = gmr(456)
local width = gmr(460)
local crest = gmr(461)
local lufs  = gmr(790)
p(string.format("  Heartbeat  [456]: %.0f  %s", hb,
  hb ~= 0 and "[non-zero: engine ran]" or "[zero: press PLAY first]"))
p(string.format("  Width      [460]: %.3f", width))
p(string.format("  Crest      [461]: %.1f dB", crest))
p(string.format("  LUFS-M     [790]: %.1f LUFS", lufs))
p(string.format("  Broad  [468-471]: Sub=%.1f  Bass=%.1f  LowMid=%.1f  High=%.1f",
  gmr(468), gmr(469), gmr(470), gmr(471)))
p(string.format("  Probe  [1198]:    %s", gmr(1198)==1 and "ACTIVE [+]" or "INACTIVE"))

-- [3] Project Track Relay Coverage
sep("=")
p("\n[3] PROJECT TRACK RELAY COVERAGE")
sep()
local track_count = reaper.CountTracks(0)
local relay_count = 0
for t = 0, track_count - 1 do
  local tr = reaper.GetTrack(0, t)
  for f = 0, reaper.TrackFX_GetCount(tr) - 1 do
    local _, fnm = reaper.TrackFX_GetFXName(tr, f, "")
    if fnm:find("Damei_Relay", 1, true) then
      relay_count = relay_count + 1
      local slot = math.floor(reaper.TrackFX_GetParam(tr, f, 5) + 0.5)
      local _, nm = reaper.GetTrackName(tr)
      p(string.format("  [slot %3d] %s", slot, nm))
      break
    end
  end
end
p(string.format("\n  Tracks: %d total, %d with Relay (%.0f%% coverage)",
  track_count, relay_count, relay_count / math.max(track_count,1) * 100))
if relay_count == 0 then
  p("  [!] Run damei_init_session.lua (Ctrl+Shift+D) to provision relays.")
end

-- [4] Project State Persistence
sep("=")
p("\n[4] PROJECT STATE (DameiMix / TBC_State)")
sep()
local ok, payload = reaper.GetProjExtState(0, "DameiMix", "TBC_State")
if ok and payload ~= "" then
  local genre, scale, ball, vmode, guid = payload:match("([^;]+);([^;]+);([^;]+);([^;]+);(.*)")
  p(string.format("  Genre: %s | Scale: %s | Ball: %s | View: %s",
    genre or "?", scale or "?", ball or "?", vmode or "?"))
  p(string.format("  EQ GUID: %s", guid ~= "" and guid or "(none saved)"))
  p("  [+] State will restore on next DTB launch.")
else
  p("  (no saved state yet -- defaults will load on first launch)")
end

-- [5] Overall Status
sep("=")
p("\n[5] OVERALL STATUS")
sep()
local issues = 0
local function chk(cond, pass_msg, fail_msg)
  if cond then p("  [+] " .. pass_msg) else p("  [X] " .. fail_msg); issues = issues + 1 end
end
chk(tbc_idx >= 0, "TonalBalance on Master Track", "TonalBalance MISSING from Master Track")
chk(meter_idx >= 0, "Damei_Metering on Master Track", "Damei_Metering MISSING")
chk(meter_idx >= 0 and meter_idx == fx_count - 1,
  "Metering is final plugin (post-limiter)", "Metering not final -- reads pre-limiter")
chk(hb ~= 0, "Heartbeat non-zero (engine ran)", "Heartbeat 0 -- press PLAY for 1+ sec then re-run")
chk(relay_count > 0,
  string.format("Relay: %d/%d tracks", relay_count, track_count),
  "No relays -- run damei_init_session.lua")
sep("=")
if issues == 0 then
  p(string.format("\n[SUCCESS] All 5 checks passed."))
  p("  Press PLAY -> watch F11 badge flip to green -> connection confirmed.")
else
  p(string.format("\n[ACTION NEEDED] %d issue(s). See [X] items above.", issues))
end
sep("=")
reaper.ShowConsoleMsg(table.concat(out, "\n") .. "\n")
