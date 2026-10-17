-- =============================================================================
-- DAMEI PROJECT STATE RELAY
-- Copies the consolidated Project State Bus published by the Mixing Suite
-- (DameiMixMetering gmem 1000-1039) into the Mastering Suite namespace
-- (DameiMetering gmem 1600-1639). JSFX can only attach one gmem namespace, so
-- this relay is the safe, additive link: it never touches any existing slot.
-- Loaded as a module by damei_song_structure_bridge.lua (always-on bridge).
-- Every call is wrapped in pcall by the caller, so a failure here cannot break
-- the structure bridge or any suite.
-- =============================================================================
local M = {}

local SRC_NS, DST_NS = "DameiMixMetering", "DameiMetering"
local SRC_BASE, DST_BASE, COUNT = 1000, 1600, 40
local last_run = 0.0

function M.step()
  local now = reaper.time_precise()
  if now - last_run < 0.05 then return end
  last_run = now

  reaper.gmem_attach(SRC_NS)
  if reaper.gmem_read(SRC_BASE) ~= 1 then
    reaper.gmem_attach(SRC_NS)
    return
  end

  local buf = {}
  for i = 0, COUNT - 1 do buf[i] = reaper.gmem_read(SRC_BASE + i) end

  reaper.gmem_attach(DST_NS)
  for i = 0, COUNT - 1 do reaper.gmem_write(DST_BASE + i, buf[i]) end

  -- Restore the default attachment used by the bridge
  reaper.gmem_attach(SRC_NS)
end

return M
