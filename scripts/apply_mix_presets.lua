-- Damei Apply Mix Presets (Stub)
-- This script calls DameiAPI /mix/apply and receives preset instructions.

local http = "curl -s -X POST -H \"Content-Type: application/json\""
local url  = "http://127.0.0.1:8765/mix/apply"

local analysis_file = reaper.GetResourcePath() .. "/damei_last_analysis.json"

local f = io.open(analysis_file, "r")
if not f then
  reaper.ShowConsoleMsg("No analysis file found.\n")
  return
end

local analysis_json = f:read("*a")
f:close()

local tmp = reaper.GetResourcePath() .. "/damei_mix_request.json"
local out = io.open(tmp, "w")
out:write("{\"analysis\": " .. analysis_json .. "}")
out:close()

local cmd = string.format("%s --data-binary @\"%s\" \"%s\"", http, tmp, url)
local result = reaper.ExecProcess(cmd, 0)

reaper.ShowConsoleMsg("Mix preset result:\n" .. tostring(result) .. "\n")
