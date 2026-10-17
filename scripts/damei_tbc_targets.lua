-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
-- Damei Tonal Balance â€” Target Preset Engine v2.1
-- damei_tbc_targets.lua
--
-- FIX: All targets are 256 points (1:1 with JSFX DISP_BINS=256)
-- FIX: Pink-noise tilt correction applied per-bin.
-- FIX: reaper.gmem_attach() + gmem_read/write (not EEL2 gmem[] syntax)
-- FIX: reaper.RecursiveCreateDirectory() for safe target directory creation
--
-- gmem capture integration:
--   The JSFX capture engine (gmem[740] = trigger, gmem[467..722] = result)
--   is used for Learn Mode â€” no blocking PCM_Source needed.
-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

-- Attach to shared memory namespace (safe to call multiple times)
reaper.gmem_attach("DameiMetering")

local TGT = {}

-- â”€â”€ Paths â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
local APPDATA = os.getenv("APPDATA") or (os.getenv("HOME") or "") .. "/.config"
TGT.TARGETS_DIR = APPDATA .. "/Damei/targets"

-- â”€â”€ Constants â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
-- CRITICAL: Must match FFT DISP_BINS in Damei_TonalBalance.jsfx
TGT.N_BINS = 256

-- gmem slots for JSFX capture engine
TGT.GMEM_CTRIG  = 740   -- capture trigger (1=start, 2=stop, 0=idle)
TGT.GMEM_CSTATE = 465   -- capture state echo (0=off, 1=capturing, 2=done)
TGT.GMEM_CCNT  = 466    -- capture frame count
TGT.GMEM_CCURV = 467    -- captured curve start (256 bins) â†’ [467..722]

-- â”€â”€ Pink-Noise Tilt Correction Table â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
-- Each bin's correction brings a -4.5 dB/octave pink noise spectrum
-- to a flat 0 dB reference line. Computed once at load time.
-- Formula: +4.5 dB Ã— log2(freq_bin / 20 Hz)
TGT.pink_corr = {}
for i = 0, TGT.N_BINS - 1 do
  -- Log-spaced frequency for bin i (matches JSFX log mapping)
  local freq = 20.0 * (1000.0 ^ (i / (TGT.N_BINS - 1)))
  local oct_from_20 = math.log(freq / 20.0) / math.log(2.0)
  TGT.pink_corr[i] = oct_from_20 * 4.5   -- dB to add for tilt compensation
end

-- â”€â”€ Apply normalization to a raw bin array â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
-- Applies pink-noise tilt correction AND anchors the curve to 0 dB
-- at the mid-band reference (300 Hzâ€“3 kHz) so that level changes
-- don't push the curve out of the target corridor.
-- Returns a new 256-element table (0-indexed).
function TGT.normalize_bins(raw, anchor_lufs)
  local corrected = {}
  -- Step 1: Apply pink-noise tilt
  for i = 0, TGT.N_BINS - 1 do
    corrected[i] = (raw[i] or -70) + TGT.pink_corr[i]
  end

  -- Step 2: Anchor to mid-band mean
  -- Mid band â‰ˆ bins 90..175 (300 Hz..3 kHz in 256-bin log space)
  -- log(300/20)/log(1000) * 255 â‰ˆ 90;  log(3000/20)/log(1000) * 255 â‰ˆ 175
  local MB_LO, MB_HI = 90, 175
  local sum, n = 0, 0
  for i = MB_LO, MB_HI do
    if corrected[i] and corrected[i] > -90 then
      sum = sum + corrected[i]; n = n + 1
    end
  end
  local anchor = (n > 0) and (sum / n) or 0

  -- Optionally bias by LUFS so the anchor tracks perceived loudness
  -- (keeps display stable during quiet passages vs. full mix)
  if anchor_lufs and anchor_lufs > -70 then
    local lufs_ref = -14.0   -- industry normalized streaming target
    anchor = anchor + (anchor_lufs - lufs_ref) * 0.3
  end

  local out = {}
  for i = 0, TGT.N_BINS - 1 do
    out[i] = corrected[i] - anchor
  end
  return out
end

-- â”€â”€ Corridor Generator (256 bins) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
-- Anchor frequency bins for the 5 piecewise control points
local function freq_to_bin(f, n_bins)
  n_bins = n_bins or TGT.N_BINS
  local t = math.log(f / 20.0) / math.log(1000.0)
  return math.max(0, math.min(n_bins - 1, math.floor(t * (n_bins - 1) + 0.5)))
end

local ANCHOR_FREQS = {20, 80, 300, 3000, 16000}
local ANCHOR_BINS = {}
for _, f in ipairs(ANCHOR_FREQS) do
  table.insert(ANCHOR_BINS, freq_to_bin(f))
end

-- Smooth cubic spline interpolation between anchor points
local function spline_interp(anchors, x)
  local n = #anchors
  if x <= anchors[1][1] then return anchors[1][2] end
  if x >= anchors[n][1] then return anchors[n][2] end
  for i = 1, n - 1 do
    local x0, y0 = anchors[i][1],   anchors[i][2]
    local x1, y1 = anchors[i+1][1], anchors[i+1][2]
    if x >= x0 and x <= x1 then
      local t = (x - x0) / (x1 - x0)
      t = t * t * (3.0 - 2.0 * t)   -- smoothstep
      return y0 + t * (y1 - y0)
    end
  end
  return 0
end

-- Build a 256-bin {target, upper, lower} corridor
local function build_corridor(sub_db, bass_db, lowmid_db, mid_db, high_db, width_db)
  local anchors = {
    {ANCHOR_BINS[1], sub_db},
    {ANCHOR_BINS[2], bass_db},
    {ANCHOR_BINS[3], lowmid_db},
    {ANCHOR_BINS[4], mid_db},
    {ANCHOR_BINS[5], high_db},
  }
  local target, upper, lower = {}, {}, {}
  for i = 0, TGT.N_BINS - 1 do
    local v = spline_interp(anchors, i)
    target[i] = v
    upper[i]  = v + width_db
    lower[i]  = v - width_db
  end
  return { target = target, upper = upper, lower = lower }
end

-- â”€â”€ Genre Definitions â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
TGT.GENRES = {
  Modern = {
    label = "Modern",   color = 0x6366F1FF,
    desc  = "Commercial modern â€” controlled sub, elevated highs",
    curve = build_corridor(1.5, 2.0, -1.5, 0.5, 2.0, 2.5),
  },
  Pop = {
    label = "Pop",      color = 0xEC4899FF,
    desc  = "Pop â€” punchy bass, bright top end",
    curve = build_corridor(0.5, 2.5, -2.0, 1.0, 3.0, 2.5),
  },
  Rock = {
    label = "Rock",     color = 0xF97316FF,
    desc  = "Rock â€” guitar-forward mids, moderate sub",
    curve = build_corridor(-0.5, 1.5, 1.5, 0.0, 1.5, 3.0),
  },
  EDM = {
    label = "EDM",      color = 0x22D3EEFF,
    desc  = "Electronic â€” heavy sub, scooped mids, bright air",
    curve = build_corridor(4.0, 3.0, -3.0, 0.0, 3.5, 3.0),
  },
  HipHop = {
    label = "Hip-Hop",  color = 0xA78BFAFF,
    desc  = "Hip-hop â€” massive sub/bass, vocal presence",
    curve = build_corridor(5.0, 4.0, -2.5, 1.0, 1.5, 3.5),
  },
  Classical = {
    label = "Classical", color = 0x86EFACFF,
    desc  = "Classical â€” natural balance, minimal sub",
    curve = build_corridor(-3.0, -1.0, 0.5, 0.5, 0.5, 2.0),
  },
  Film = {
    label = "Film",     color = 0xFCD34DFF,
    desc  = "Film â€” dialogue clarity, wide dynamic range",
    curve = build_corridor(-1.0, 0.0, 2.0, 2.0, 1.0, 3.0),
  },
}
TGT.GENRE_LIST = {"Modern", "Pop", "Rock", "EDM", "HipHop", "Classical", "Film"}

-- â”€â”€ Broad Band Summaries (4-band averages of 256-bin corridor) â”€â”€â”€â”€â”€â”€â”€â”€
local BROAD_RANGES = {
  {freq_to_bin(20),   freq_to_bin(60)},
  {freq_to_bin(60),   freq_to_bin(250)},
  {freq_to_bin(250),  freq_to_bin(2000)},
  {freq_to_bin(2000), freq_to_bin(20000)},
}

function TGT.get_broad_targets(genre_key)
  local g = TGT.GENRES[genre_key]
  if not g then return nil end
  local results = {}
  for band_i, r in ipairs(BROAD_RANGES) do
    local sum_t, sum_u, sum_l, n = 0, 0, 0, 0
    for bi = r[1], r[2] do
      sum_t = sum_t + g.curve.target[bi]
      sum_u = sum_u + g.curve.upper[bi]
      sum_l = sum_l + g.curve.lower[bi]
      n = n + 1
    end
    if n > 0 then
      results[band_i] = { target=sum_t/n, upper=sum_u/n, lower=sum_l/n }
    end
  end
  return results
end

function TGT.get_target(genre_key)
  if TGT.GENRES[genre_key] then return TGT.GENRES[genre_key].curve end
  return TGT.load_custom_target(genre_key) or TGT.GENRES["Modern"].curve
end

-- â”€â”€ JSON Save / Load â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
local function ensure_dir(path)
  -- FIX: Use REAPER's native recursive directory creator (works on all platforms)
  reaper.RecursiveCreateDirectory(path:gsub("/", "\\"), 0)
end

function TGT.save_custom_target(name, curve, meta)
  ensure_dir(TGT.TARGETS_DIR)
  local path = TGT.TARGETS_DIR .. "/" .. name .. ".json"
  local function arr_to_json(arr)
    local parts = {}
    for i = 0, TGT.N_BINS - 1 do parts[i+1] = string.format("%.3f", arr[i] or 0) end
    return "[" .. table.concat(parts, ",") .. "]"
  end
  local json = string.format(
    '{"name":"%s","desc":"%s","n_bins":%d,"target":%s,"upper":%s,"lower":%s}',
    name, (meta and meta.desc or ""), TGT.N_BINS,
    arr_to_json(curve.target), arr_to_json(curve.upper), arr_to_json(curve.lower))
  local f = io.open(path, "w")
  if f then f:write(json); f:close(); return true end
  return false
end

function TGT.load_custom_target(name)
  local path = TGT.TARGETS_DIR .. "/" .. name .. ".json"
  local f = io.open(path, "r"); if not f then return nil end
  local raw = f:read("*a"); f:close()
  local function parse_arr(str, key)
    local s = str:match('"' .. key .. '"%s*:%s*(%[.-)%]')
    if not s then return {} end
    local arr = {}; local i = 0
    for v in s:gmatch("([%-%.%d]+)") do arr[i] = tonumber(v) or 0; i=i+1 end
    return arr
  end
  return { target=parse_arr(raw,"target"), upper=parse_arr(raw,"upper"), lower=parse_arr(raw,"lower") }
end

function TGT.list_custom_targets()
  local list = {}
  local tmp = reaper.GetResourcePath() .. "/damei_tgt_list.txt"
  os.execute(string.format(
    'powershell -WindowStyle Hidden -Command "if(Test-Path \'%s\'){Get-ChildItem -Path \'%s\' -Filter *.json | Select-Object -ExpandProperty BaseName | Out-File -FilePath \'%s\' -Encoding UTF8}"',
    TGT.TARGETS_DIR:gsub("/","\\"), TGT.TARGETS_DIR:gsub("/","\\"), tmp:gsub("/","\\")))
  local f = io.open(tmp, "r")
  if f then
    for line in f:lines() do
      local name = line:match("^%s*(.-)%s*$")
      if name and #name > 0 and name ~= "" then table.insert(list, name) end
    end
    f:close(); os.remove(tmp)
  end
  return list
end

-- â”€â”€ Learn Mode (gmem capture â€” no PCM_Source needed!) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
-- The JSFX capture engine averages incoming FFT frames when triggered.
-- We read the result directly from gmem â€” zero Lua blocking.

TGT.learn = {
  active    = false,
  armed     = false,   -- waiting for playback to start
  done      = false,
  name      = "",
  width_db  = 2.5,
  frame_check = 0,
}

function TGT.learn_start(name, width_db)
  TGT.learn.name     = name or "custom"
  TGT.learn.width_db = width_db or 2.5
  TGT.learn.active   = true
  TGT.learn.done     = false
  -- FIX: Use reaper.gmem_write(), NOT EEL2 gmem[] array syntax
  reaper.gmem_write(TGT.GMEM_CTRIG,  1)   -- tell JSFX to start accumulating
  reaper.gmem_write(TGT.GMEM_CSTATE, 0)
  TGT.learn.frame_check = 0
end

function TGT.cancel_learn()
  reaper.gmem_write(TGT.GMEM_CTRIG, 0)
  reaper.gmem_write(TGT.GMEM_CSTATE, 0)
  TGT.learn.active = false
  TGT.learn.done   = false
end

function TGT.learn_stop()
  reaper.gmem_write(TGT.GMEM_CTRIG, 2)   -- tell JSFX to finalize
  TGT.learn.active = false
  -- Poll until JSFX writes CSTATE = 2 (done)
end

-- Call every frame while learn.active or checking for done result.
-- Returns: "idle" | "capturing" | "done" | "error"
function TGT.learn_tick()
  -- FIX: reaper.gmem_read() not gmem[]
  local cstate = reaper.gmem_read(TGT.GMEM_CSTATE) or 0
  if TGT.learn.active then
    return cstate == 1 and "capturing" or "idle"
  end
  if cstate == 2 and not TGT.learn.done then
    local ccnt = reaper.gmem_read(TGT.GMEM_CCNT) or 0
    if ccnt < 1 then return "error" end
    local raw = {}
    for i = 0, TGT.N_BINS - 1 do
      raw[i] = reaper.gmem_read(TGT.GMEM_CCURV + i) or -70
    end
    -- Normalize: subtract mid-band mean, build Â±width corridor
    local normed = TGT.normalize_bins(raw, nil)
    local w = TGT.learn.width_db
    local target, upper, lower = {}, {}, {}
    for i = 0, TGT.N_BINS - 1 do
      target[i] = normed[i]
      upper[i]  = normed[i] + w
      lower[i]  = normed[i] - w
    end
    local curve = { target=target, upper=upper, lower=lower }
    local name  = TGT.learn.name
    TGT.save_custom_target(name, curve, { desc = "Learned from live capture" })
    TGT.GENRES["__learn_" .. name] = {
      label    = name .. " â˜…",
      color    = 0xFBBF24FF,
      desc     = "Live learned target",
      curve    = curve,
      is_custom= true,
    }
    table.insert(TGT.GENRE_LIST, "__learn_" .. name)
    TGT.learn.done = true
    reaper.gmem_write(TGT.GMEM_CSTATE, 0)   -- clear so we don't re-import
    return "done"
  end
  return TGT.learn.done and "done" or "idle"
end


-- ============================================================================
-- P1: Offline Reference Target Learner (AudioAccessor FFT)
-- ============================================================================
-- TGT.learn_from_item(media_item)
--   Scans the entire take offline using CreateTakeAudioAccessor,
--   computes a 256-bin log-spaced magnitude spectrum with -4.5 dB/oct
--   pink-noise tilt correction, derives target corridor from mean +/- 1.5 sigma,
--   and stores the result under TGT["_custom"].
--
-- Runs at disk-cache speed (~200 ms for a 4-minute track at 48 kHz).
-- No real-time playback required.
-- ============================================================================

local LEARN_FFT_SZ  = 4096
local LEARN_BINS    = 256
local LEARN_OVERLAP = 4        -- hop = FFT_SZ / 4
local LEARN_PINK_SLOPE = 4.5   -- dB/oct tilt to flatten pink reference

local function _fft_mag_to_log_bins(fft_buf, out_bins, fft_sz, n_bins)
  -- Map FFT[0..fft_sz/2] magnitude to n_bins log-spaced output bins
  local half = fft_sz / 2
  for b = 0, n_bins - 1 do
    local f_lo = 20.0 * (1000.0 ^ (b       / (n_bins - 1)))
    local f_hi = 20.0 * (1000.0 ^ ((b + 1) / (n_bins - 1)))
    local k_lo = math.max(0,    math.floor(f_lo / (srate or 48000) * fft_sz))
    local k_hi = math.min(half, math.floor(f_hi / (srate or 48000) * fft_sz))
    local acc, cnt = 0.0, 0
    for k = k_lo, k_hi do
      local re = fft_buf[k * 2 + 1] or 0
      local im = fft_buf[k * 2 + 2] or 0
      acc = acc + math.sqrt(re*re + im*im)
      cnt = cnt + 1
    end
    local mag = cnt > 0 and (acc / cnt) or 1e-12
    -- Apply inverse pink tilt: add 4.5 dB/oct to flatten
    local freq_mid  = math.sqrt(math.max(f_lo, 20) * math.max(f_hi, 20))
    local tilt_db   = LEARN_PINK_SLOPE * math.log(freq_mid / 1000) / math.log(2)
    local mag_tilted = mag * (10 ^ (tilt_db / 20))
    out_bins[b + 1] = (out_bins[b + 1] or 0) + mag_tilted
  end
end

function TGT.learn_from_item(media_item, name)
  if not media_item then
    return nil, "No media item provided"
  end
  local take = reaper.GetActiveTake(media_item)
  if not take then
    return nil, "No active take on item"
  end
  local accessor = reaper.CreateTakeAudioAccessor(take)
  if not accessor then
    return nil, "Failed to create audio accessor"
  end

  local sr = reaper.GetMediaItemTakeInfo_Value(take, "SAMPLERATE")
  if not sr or sr == 0 then sr = 48000 end
  local item_len = reaper.GetMediaItemInfo_Value(media_item, "D_LENGTH")
  local hop      = LEARN_FFT_SZ / LEARN_OVERLAP

  -- Pre-allocate stereo sample buffer (reaper_array for GetAudioAccessorSamples)
  local buf_size = LEARN_FFT_SZ * 2
  local buf      = reaper.new_array(buf_size)

  -- Accumulate magnitude spectrum across all hops
  local accum_bins  = {}
  local accum_bins2 = {}   -- for variance (E[x^2])
  local frame_count = 0
  for b = 0, LEARN_BINS - 1 do accum_bins[b+1] = 0; accum_bins2[b+1] = 0 end

  local pos = 0.0
  local tmp_bins = {}

  while pos < item_len - (LEARN_FFT_SZ / sr) do
    -- Read LEARN_FFT_SZ stereo samples from this position
    local ok = reaper.GetAudioAccessorSamples(accessor, sr, 2, pos, LEARN_FFT_SZ, buf)
    if ok == 0 then break end

    -- Mix to mono and FFT (use reaper.new_array as fft input is in-place)
    local mono_buf = reaper.new_array(LEARN_FFT_SZ * 2)  -- real,imag interleaved
    for k = 0, LEARN_FFT_SZ - 1 do
      -- buf is interleaved: L[0], R[1], L[2], R[3]...
      local l = buf[k * 2 + 1] or 0
      local r = buf[k * 2 + 2] or 0
      mono_buf[k * 2 + 1] = (l + r) * 0.5   -- real
      mono_buf[k * 2 + 2] = 0                -- imag
    end
    -- REAPER's FFT (in-place on reaper_array)
    reaper.fft(mono_buf, LEARN_FFT_SZ, false)

    -- Map to log bins with pink tilt
    for b = 0, LEARN_BINS - 1 do tmp_bins[b+1] = 0 end
    _fft_mag_to_log_bins(mono_buf, tmp_bins, LEARN_FFT_SZ, LEARN_BINS)

    for b = 1, LEARN_BINS do
      local v = tmp_bins[b]
      accum_bins[b]  = accum_bins[b]  + v
      accum_bins2[b] = accum_bins2[b] + v * v
    end
    frame_count = frame_count + 1
    pos = pos + (hop / sr)
  end

  reaper.DestroyAudioAccessor(accessor)

  if frame_count == 0 then
    return nil, "No audio frames could be read (item may be empty)"
  end

  -- Compute mean and sigma -> target corridor
  local target_curve = { fine = {}, broad = {} }
  local db_min, db_max = math.huge, -math.huge

  local mean_db = {}
  for b = 1, LEARN_BINS do
    local mean  = accum_bins[b] / frame_count
    local mean2 = accum_bins2[b] / frame_count
    local var   = math.max(0, mean2 - mean * mean)
    local sigma = math.sqrt(var)
    local db    = mean > 0 and (20 * math.log10(mean)) or -90
    local sd_db = sigma > 0 and (20 * math.log10(mean + sigma) - db) or 1.5
    mean_db[b]  = db
    target_curve.fine[b] = {
      center = db,
      upper  = db + math.min(sd_db * 1.5, 8.0),
      lower  = db - math.min(sd_db * 1.5, 8.0),
    }
    if db > db_max then db_max = db end
    if db < db_min then db_min = db end
  end

  -- Normalize fine curve so mean = 0 dB
  local db_norm = (db_min + db_max) * 0.5
  for b = 1, LEARN_BINS do
    target_curve.fine[b].center = target_curve.fine[b].center - db_norm
    target_curve.fine[b].upper  = target_curve.fine[b].upper  - db_norm
    target_curve.fine[b].lower  = target_curve.fine[b].lower  - db_norm
  end

  -- Derive broad 4-band corridors from the fine curve averages
  local broad_ranges = { {1,32}, {33,96}, {97,192}, {193,256} }  -- bin ranges per band
  for i, rng in ipairs(broad_ranges) do
    local sum, cnt = 0.0, 0
    for b = rng[1], rng[2] do
      sum = sum + (target_curve.fine[b] and target_curve.fine[b].center or 0)
      cnt = cnt + 1
    end
    local band_mean = cnt > 0 and (sum / cnt) or 0
    target_curve.broad[i] = { target = band_mean, upper = band_mean + 3.0, lower = band_mean - 3.0 }
  end

  -- Store as custom target
  local custom_name = name or "Custom Reference"
  TGT[custom_name] = target_curve

  -- Persist to project ExtState (serialize as flat CSV)
  local parts = {}
  for b = 1, LEARN_BINS do
    local fc = target_curve.fine[b]
    parts[#parts+1] = string.format("%.2f,%.2f,%.2f", fc.center, fc.upper, fc.lower)
  end
  reaper.SetProjExtState(0, "DameiMix", "CustomTarget_" .. custom_name,
    custom_name .. "|" .. table.concat(parts, ";"))

  return target_curve, nil
end

-- Load all saved custom targets from project ExtState
function TGT.load_custom_targets()
  local i = 0
  while true do
    local ok, key, val = reaper.EnumProjExtState(0, "DameiMix", i)
    if not ok then break end
    if key:match("^CustomTarget_") then
      local tname, data = val:match("^([^|]+)|(.+)$")
      if tname and data then
        local curve = { fine = {}, broad = {} }
        local b = 1
        for chunk in data:gmatch("[^;]+") do
          local c, u, l = chunk:match("([^,]+),([^,]+),([^,]+)")
          if c then
            curve.fine[b] = { center=tonumber(c), upper=tonumber(u), lower=tonumber(l) }
            b = b + 1
          end
        end
        -- Rebuild broad from fine
        local broad_ranges = { {1,32}, {33,96}, {97,192}, {193,256} }
        for idx, rng in ipairs(broad_ranges) do
          local sum, cnt = 0.0, 0
          for bi = rng[1], rng[2] do
            sum = sum + (curve.fine[bi] and curve.fine[bi].center or 0)
            cnt = cnt + 1
          end
          local m = cnt > 0 and (sum/cnt) or 0
          curve.broad[idx] = { target=m, upper=m+3.0, lower=m-3.0 }
        end
        TGT[tname] = curve
      end
    end
    i = i + 1
  end
end

TGT.load_custom_targets()
return TGT
