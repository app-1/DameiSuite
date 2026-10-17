-- Damei Push Metrics Logger

local M = {}

local log_dir = "C:/Dev/DameiAPI/logs"
local log_file = log_dir .. "/damei_push_metrics.log"

local function ensure_dir(path)
  reaper.RecursiveCreateDirectory(path, 0)
end

local function write_line(line)
  ensure_dir(log_dir)
  local f = io.open(log_file, "a")
  if not f then return end
  f:write(line .. "\n")
  f:close()
end

function M.log_push(success, code, bytes)
  local t = os.date("%Y-%m-%d %H:%M:%S")
  local status = success and "success" or "failure"
  local msg = string.format(
    "[%s] status=%s code=%s bytes=%d",
    t, status, tostring(code), tonumber(bytes or 0)
  )
  write_line(msg)
end

return M
