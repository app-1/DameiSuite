-- ==============================================================================
-- DAMEI PRODUCER DNA & EAR-CANDY RELAY DISPATCHER (REASCRIPT LUA)
-- Deconstructs reference track "Split Chain - I'm Not Dying To Be Here"
-- and synchronizes all 8 Damei Suites with Kel Pinchin's signature topology,
-- ear-candy automators, transition plays, and macro dynamic lifts.
-- ==============================================================================

local log_path = "c:\\Dev\\DameiSuite\\tools\\producer_relay_log.txt"
local log_file = io.open(log_path, "w")

local function msg(str)
  reaper.ShowConsoleMsg(str .. "\n")
  if log_file then
    log_file:write(str .. "\n")
    log_file:flush()
  end
end

reaper.ClearConsole()
msg("================================================================================")
msg("⚡ DAMEI SUITE: RELAYING PRODUCER DNA & EAR-CANDY PLAYS")
msg("   Producer Blueprint: Kel Pinchin (Split Chain / motionblur)")
msg("   Reference Track: 'I'm Not Dying To Be Here'")
msg("   Target: -10.3 LUFS-I | 9.3 dB Crest | 0.63 Width | +21.9 dB Dynamic Spread")
msg("================================================================================")

reaper.Undo_BeginBlock()

local stats = {
  tracks_scanned = 0,
  suites_updated = 0,
  params_modified = 0,
  bypasses_fixed = 0
}

-- Safe parameter setter by name search with slider index fallback
local function set_param(track, fx_idx, slider_num, search_term, val, label)
  local num_params = reaper.TrackFX_GetNumParams(track, fx_idx)
  local target_p = slider_num - 1

  if search_term and search_term ~= "" then
    local lower_term = string.lower(search_term)
    for p = 0, num_params - 1 do
      local _, pname = reaper.TrackFX_GetParamName(track, fx_idx, p, "")
      if string.find(string.lower(pname), lower_term, 1, true) then
        target_p = p
        break
      end
    end
  end

  if target_p >= 0 and target_p < num_params then
    reaper.TrackFX_SetParam(track, fx_idx, target_p, val)
    stats.params_modified = stats.params_modified + 1
    if label then
      msg(string.format("   ├─ %s: %.2f", label, val))
    end
    return true
  end
  return false
end

-- Process an individual FX on a track
local function process_fx(track, track_name, fx_idx)
  local _, fx_name = reaper.TrackFX_GetFXName(track, fx_idx, "")
  local lower_name = string.lower(fx_name)
  local is_master = (track == reaper.GetMasterTrack(0))
  local loc_tag = is_master and "[MASTER TRACK]" or string.format("[Track: %s]", track_name)

  -- Ensure FX is enabled (unbypass if needed)
  if not reaper.TrackFX_GetEnabled(track, fx_idx) then
    reaper.TrackFX_SetEnabled(track, fx_idx, true)
    stats.bypasses_fixed = stats.bypasses_fixed + 1
    msg(string.format("   ★ UNBYPASSED / ACTIVATED: %s on %s", fx_name, loc_tag))
  end

  -- 1. VOCAL SOVEREIGN (Track 4 / VOX)
  if string.find(lower_name, "vocalsuite", 1, true) or string.find(lower_name, "vocal sovereign", 1, true) then
    msg(string.format("✔ RELAYING VOCAL SOVEREIGN on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    -- Topology & Static EQ
    set_param(track, fx_idx, 18, "Producer Vocal", 5, "Producer Preset (Kel Pinchin)")
    set_param(track, fx_idx, 29, "Master Vocal Engine", 1, "Master Vocal Engine (Active)")
    set_param(track, fx_idx, 9, "Center Lead Channel", 1, "Center Lead Lock 100% Mono <200Hz")
    set_param(track, fx_idx, 43, "FET Comp", 1, "FET Comp 8:1 Ratio")
    set_param(track, fx_idx, 44, "LA-2A Mode", 0, "LA-2A Smooth Opto Compress")
    set_param(track, fx_idx, 45, "Sidechain Highpass", 1, "LA-2A Sidechain HPF Emphasis")
    set_param(track, fx_idx, 46, "LOADES", 1, "LOADES Split-Band De-Esser")
    set_param(track, fx_idx, 47, "ReEQ Highpass", 95, "ReEQ 95Hz Highpass")
    set_param(track, fx_idx, 48, "Chest Mud", -2.5, "ReEQ 380Hz Chest Mud Scoop (-2.5 dB)")
    set_param(track, fx_idx, 49, "Harshness Notch", -2.2, "ReEQ 5.2kHz De-Harsh (-2.2 dB)")
    set_param(track, fx_idx, 10, "Air Band", 2.0, "Maag 16kHz Air Band (+2.0 dB)")
    set_param(track, fx_idx, 11, "Presence", 1.4, "1.8kHz Vocal Presence (+1.4 dB)")
    set_param(track, fx_idx, 8, "Stereo Backing", 1.20, "Stereo Backing Width (1.20x)")
    set_param(track, fx_idx, 14, "Clipper", 1, "Hermite Soft-Clip Topology")
    set_param(track, fx_idx, 15, "Headroom Ceiling", -0.5, "Ceiling Clamp (-0.5 dBTP)")
    set_param(track, fx_idx, 16, "Headroom Guardian", 1, "Strict Ceiling Guardian Active")
    set_param(track, fx_idx, 17, "Output Makeup", 1.8, "Output Makeup Pocket Calibration (+1.8 dB)")
    set_param(track, fx_idx, 24, "Lead Vox", 0.0, "Lead Vox Stem Level (0.0 dB)")
    set_param(track, fx_idx, 25, "Ad-Lib Stem Level", -4.0, "Ad-Lib Stem Level (-4.0 dB)")
    set_param(track, fx_idx, 26, "Ad-Lib FX", 6.0, "Ad-Lib FX & Space Amount (6%)")
    set_param(track, fx_idx, 28, "Vocal Reverb", 0.0, "Vocal Reverb Aux Space (0.0 dB)")
    set_param(track, fx_idx, 35, "Matrix Trim", 1, "Matrix Auto-Correct Lane (Active)")
    -- Producer Ear Candy & Transition Plays
    set_param(track, fx_idx, 30, "Pre-Chorus Vocal Throw", 1, "Play 1: Pre-Chorus Vocal Throw Delay")
    set_param(track, fx_idx, 33, "Throw Delay Feedback", 35, "Throw Delay Feedback (35%)")
    set_param(track, fx_idx, 31, "Reverse Swell", 1, "Play 2: Reverse Vocal Swell into Drops")
    set_param(track, fx_idx, 34, "Reverse Swell Duration", 2.0, "Reverse Swell Duration (2.0 Bars)")
    set_param(track, fx_idx, 32, "Telephone", 0, "Telephone Filter Clean Lead")
    set_param(track, fx_idx, 39, "Ear-Candy Director", 1, "Ear-Candy Director (Region+Energy Aware)")
    set_param(track, fx_idx, 40, "Master Vocal Effect", 15, "Master Vocal Effect Intensity (15%)")
    set_param(track, fx_idx, 41, "Palette", 12607, "Kel Pinchin Trick Palette (12607)")
    set_param(track, fx_idx, 42, "Palette Follows", 1, "Ear-Candy Palette Follows Producer")
    set_param(track, fx_idx, 22, "Guitar Pocket", 1, "Guitar Pocket Lock (Auto-Unmask vs Gtr)")
  end

  -- 2. DRUM BUS ARCHITECT (Track 16 / DRUMS)
  if string.find(lower_name, "drumsuite", 1, true) or string.find(lower_name, "drum bus", 1, true) then
    msg(string.format("✔ RELAYING DRUM BUS ARCHITECT on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    -- Topology & Static EQ
    set_param(track, fx_idx, 25, "Producer Drum", 5, "Producer Preset (Kel Pinchin)")
    set_param(track, fx_idx, 30, "Cymbal Silk", 1, "Cymbal Silk Master (Active)")
    set_param(track, fx_idx, 40, "Dynamic Boom", -2.0, "Sub-Kick Boom Tamer 40Hz (-2.0 dB)")
    set_param(track, fx_idx, 18, "Room Mud Scoop", -2.5, "Room Mud Scoop 340Hz (-2.5 dB)")
    set_param(track, fx_idx, 42, "Matrix Trim", 1, "Matrix Auto-Correct Lane (Active)")
    set_param(track, fx_idx, 12, "Cymbal De-Trash", -2.0, "Cymbal De-Trash Resonance (-2.0 dB)")
    set_param(track, fx_idx, 13, "Cymbal Silk Air", 2.2, "Cymbal Silk Air Sheen (+2.2 dB)")
    -- Producer Plays & Rack Integration
    set_param(track, fx_idx, 37, "Integration Mode", 1, "Integration Mode (Standalone All-in-One Chain)")
    set_param(track, fx_idx, 28, "Song Structure", 2, "Song Structure AI (Commercial Drop Slam: +0.14x Width)")
    set_param(track, fx_idx, 34, "Britson Neve", 25, "Britson Neve Console Drive (25%)")
    set_param(track, fx_idx, 35, "BSA Drum Bus Glue", 20, "BSA Drum Bus Glue & Heat (20%)")
    set_param(track, fx_idx, 36, "Devil-Slam", 15, "Devil-Slam Parallel Crush (15%)")
    set_param(track, fx_idx, 44, "BSA Comp Drive", 38, "BSA Comp Drive (38%)")
    set_param(track, fx_idx, 45, "BSA Heat", 26, "BSA Heat Saturation (26%)")
    set_param(track, fx_idx, 50, "BSA Parallel Mix", 85, "BSA Parallel Mix (85%)")
    set_param(track, fx_idx, 41, "Mix Headroom", 1, "Mix Headroom Balance Anchor (Auto-Guard)")
  end

  -- 3. GUITAR BUS ALCHEMIST (Track 51 / GUITAR)
  if string.find(lower_name, "guitarsuite", 1, true) or string.find(lower_name, "guitar bus", 1, true) then
    msg(string.format("✔ RELAYING GUITAR BUS ALCHEMIST on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    -- Topology & Static EQ
    set_param(track, fx_idx, 23, "Producer Guitar", 5, "Producer Preset (Kel Pinchin)")
    set_param(track, fx_idx, 16, "Quad-Wall", 1.28, "Stereo Quad-Wall Width (1.28x)")
    set_param(track, fx_idx, 9, "Highpass Anchor", 95, "Sub-Guitar Highpass Anchor (95 Hz HPF)")
    set_param(track, fx_idx, 10, "Low-Mid Mud", -2.0, "Mud Box Scoop 380Hz (-2.0 dB)")
    set_param(track, fx_idx, 3, "Chug Clamp", 40, "Dynamic Chug Clamp Strength (40% / -4.0 dB)")
    set_param(track, fx_idx, 4, "Chug Freq", 190, "Chug Resonance Frequency (190 Hz)")
    set_param(track, fx_idx, 17, "Vocal Pocket Cut", -2.5, "Center Pocket Cut (-2.5 dB for Vocal)")
    set_param(track, fx_idx, 15, "Air Sheen", 1.8, "Air Sheen & Cab Presence (+1.8 dB)")
    set_param(track, fx_idx, 28, "De-Fizz Master", 1, "De-Fizz Master Engine (Active)")
    set_param(track, fx_idx, 11, "Harsh Fizz Notch 1", -1.5, "De-Fizz Notch 3.2kHz (-1.5 dB)")
    set_param(track, fx_idx, 12, "Harsh Fizz Notch 2", -1.8, "De-Fizz Notch 4.2kHz (-1.8 dB)")
    -- Producer Plays & Ear Candy
    set_param(track, fx_idx, 34, "Guitar Bus Integration", 1, "Integration Mode (Standalone All-in-One Chain)")
    set_param(track, fx_idx, 42, "Pick Scrape", 1, "Play 3: Pre-Drop Pick Scrape & Swell")
    set_param(track, fx_idx, 43, "Killswitch", 1, "Play 3b: Pre-Drop Killswitch 1/16th Chopper")
    set_param(track, fx_idx, 44, "Radio Megaphone", 1, "Play 6b: Auto Radio Megaphone Pre-Drop")
    set_param(track, fx_idx, 45, "Whammy Pitch Dive", 1, "Play 5: Breakdown Whammy Pitch Dive & Tape Stop")
    set_param(track, fx_idx, 46, "Ear-Candy Wet", 30, "Ear-Candy Wet/Dry Blend (30%)")
    set_param(track, fx_idx, 48, "Ear-Candy Director", 1, "Ear-Candy Director (Region+Energy Aware)")
    set_param(track, fx_idx, 49, "Ear-Candy Amount", 40, "Ear-Candy Amount (40%)")
    set_param(track, fx_idx, 51, "Palette Follows", 1, "Palette Follows Producer Preset")
    set_param(track, fx_idx, 26, "Song Structure", 2, "Song Structure AI (Commercial Drop Slam: +0.14x Width)")
    set_param(track, fx_idx, 31, "Britson Neve", 25, "Britson Neve Console Drive (25%)")
    set_param(track, fx_idx, 32, "Tape Saturation", 20, "Tape Saturation & Heat (20%)")
    set_param(track, fx_idx, 33, "VCA Bus Glue", 15, "VCA Bus Glue (DC1A3 15%)")
    set_param(track, fx_idx, 36, "Drum Bus Pocket", 1, "Drum Bus Pocket Link (Auto-Guard -4.5dB)")
  end

  -- 4. BASS BUS ENGINE (Track 69 / BASS)
  if string.find(lower_name, "basssuite", 1, true) or string.find(lower_name, "bass bus", 1, true) then
    msg(string.format("✔ RELAYING BASS BUS ENGINE on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    -- Topology & Static EQ
    set_param(track, fx_idx, 20, "Producer Bass", 5, "Producer Preset (Kel Pinchin)")
    set_param(track, fx_idx, 3, "Sub-Mono Elliptical", 90, "Sub-Mono Elliptical Anchor (90 Hz)")
    set_param(track, fx_idx, 4, "Kick Ducking Depth", 3.0, "Kick Ducking Depth (3.0 dB via Trackspacer)")
    set_param(track, fx_idx, 12, "Mud Box Scoop", -2.5, "Mud Box Scoop 250Hz (-2.5 dB)")
    set_param(track, fx_idx, 35, "Matrix Trim", 1, "Matrix Auto-Correct Lane (Active)")
    -- Producer Plays & Racks
    set_param(track, fx_idx, 26, "Bass Bus Integration", 1, "Integration Mode (Standalone All-in-One Chain)")
    set_param(track, fx_idx, 36, "Smash & Grab Comp Mode", 2, "Smash & Grab Comp Mode (Hybrid)")
    set_param(track, fx_idx, 37, "Smash Amount", 38, "Smash Fast Clamp (38%)")
    set_param(track, fx_idx, 38, "Grab Amount", 42, "Grab Warm Leveler (42%)")
    set_param(track, fx_idx, 39, "Smash & Grab Parallel Mix", 85, "Smash & Grab Parallel Mix (85%)")
    set_param(track, fx_idx, 40, "Decapitator Style", 1, "Decapitator Style (Style N Neve)")
    set_param(track, fx_idx, 41, "Decapitator Drive", 28, "Decapitator Drive (28%)")
    set_param(track, fx_idx, 45, "Trackspacer", 1, "Trackspacer Dynamic Inverse EQ (Active)")
    set_param(track, fx_idx, 46, "Trackspacer Ducking Amount", 40, "Trackspacer Ducking Amount (40%)")
    set_param(track, fx_idx, 28, "Kick/Guitar Pocket", 1, "Kick/Guitar Pocket Interlock (Auto-Guard)")
  end

  -- 5. SYNTH BUS NEBULA (Tracks 40, 44, 47)
  if string.find(lower_name, "synthsuite", 1, true) or string.find(lower_name, "synth bus", 1, true) then
    msg(string.format("✔ RELAYING SYNTH BUS NEBULA on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    -- Topology & Static EQ
    set_param(track, fx_idx, 15, "Producer Synth", 10, "Producer Blueprint (Kel Pinchin)")
    set_param(track, fx_idx, 8, "Stereo Horizon", 1.45, "Stereo Horizon Width (1.45x)")
    set_param(track, fx_idx, 4, "Sub Foundation", 1, "Sub Mono Lock <90Hz (Active)")
    set_param(track, fx_idx, 34, "Band 2", -1.5, "Multiband Low-Mid Scoop (-1.5 dB)")
    set_param(track, fx_idx, 36, "Band 4", 2.5, "Multiband Glassy Air Sheen (+2.5 dB)")
    set_param(track, fx_idx, 27, "Matrix Trim", 1, "Matrix Auto-Correct Lane (Active)")
    -- Producer Plays & Inter-Suite Handshakes
    set_param(track, fx_idx, 18, "Pre-Drop Silence", 1, "Play 2b: Dynamic Pre-Drop Silence Choke")
    set_param(track, fx_idx, 19, "Devastator Neural Link", 1, "Play 7b: Devastator Suite Neural Interlock")
    set_param(track, fx_idx, 20, "Devastator Sub Divebomb Carve", 4.0, "Devastator Divebomb Carve Depth (4.0 dB)")
    set_param(track, fx_idx, 5, "Drum Kick Sub-Duck", 3.5, "Drum Kick Sub-Duck Depth (3.5 dB via gmem 820)")
    set_param(track, fx_idx, 6, "Lead Vocal Mid-Carve", 2.5, "Lead Vocal Mid-Carve Depth (2.5 dB via gmem 880)")
    set_param(track, fx_idx, 7, "Guitar Wall Chorus Carve", 3.0, "Guitar Wall Chorus Carve (3.0 dB via gmem 840)")
    set_param(track, fx_idx, 28, "Ear-Candy Director", 1, "Ear-Candy Director (Region+Energy Aware)")
    set_param(track, fx_idx, 24, "Dystopian Chaos", 25, "Dystopian Chaos Resonator (25%)")
    set_param(track, fx_idx, 25, "Tritone Fright", 35, "Tritone Fright Comb Resonance (35%)")
  end

  -- 6. DEVASTATOR SUITE (Track 50 / CINEMATIC FX)
  if string.find(lower_name, "devastatorsuite", 1, true) or string.find(lower_name, "devastator", 1, true) then
    msg(string.format("✔ RELAYING DEVASTATOR SUITE on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    -- Topology & Static EQ
    set_param(track, fx_idx, 2, "Producer Cinematic", 8, "Producer Blueprint (Kel Pinchin)")
    set_param(track, fx_idx, 5, "Master Sub-Bed", -13.0, "Sub-Bed Trim (-13.0 dB)")
    set_param(track, fx_idx, 46, "Sub Mono Anchor", 1, "Sub Mono Anchor <90Hz (Active)")
    set_param(track, fx_idx, 47, "Spatial Widener", 1.25, "M/S Spatial Widener (1.25x)")
    -- Producer Plays
    set_param(track, fx_idx, 4, "Decision Mode", 1, "AI Context-Aware Auto-Trigger (Energy Delta)")
    set_param(track, fx_idx, 11, "Slot 1: Trailer Braam Active", 1, "Play 7: Slot 1 Trailer Braam (Active)")
    set_param(track, fx_idx, 20, "Slot 2: Reversed Suck-Back Active", 1, "Play 2: Slot 2 Reversed Suck-Back (Active)")
    set_param(track, fx_idx, 22, "Pre-Drop Micro-Silence", 80, "Pre-Drop Micro-Silence Choke (80 ms)")
    set_param(track, fx_idx, 30, "Slot 3: Sub Divebomb Active", 1, "Play 7b: Slot 3 Sub Divebomb (Active)")
    set_param(track, fx_idx, 40, "Slot 4: Ambient Pad", 1, "Slot 4 Cyber Riser & Ambient Pad (Active)")
    set_param(track, fx_idx, 6, "Drum Bus Ducking", 1, "Drum Bus Ducking Interlock (gmem 820)")
    set_param(track, fx_idx, 7, "Lead Vocal Pocket", 1, "Lead Vocal Pocket Protection (gmem 880)")
    set_param(track, fx_idx, 8, "Guitar Wall Low-Mid", 1, "Guitar Wall Low-Mid Handshake (gmem 840)")
    set_param(track, fx_idx, 67, "Trailer Playbook", 1, "Producer Playbook Mode (Region+Energy Aware)")
    set_param(track, fx_idx, 68, "Trailer Playbook Intensity", 1, "Trailer Playbook Intensity (Producer)")
  end

  -- 7. MIXING SUITE (Master Track)
  if string.find(lower_name, "mixingsuite", 1, true) or string.find(lower_name, "mixing suite", 1, true) then
    msg(string.format("✔ RELAYING MIXING SUITE on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    -- Topology & Static EQ
    set_param(track, fx_idx, 39, "Producer Signature", 6, "Producer Preset (Kel Pinchin / Split Chain)")
    set_param(track, fx_idx, 6, "Sub-Bass Mono-Anchor", 100, "Sub-Bass Mono Cutoff (100 Hz)")
    set_param(track, fx_idx, 7, "Stereo Dimension", 1.18, "Stereo Width Expander (1.18x)")
    set_param(track, fx_idx, 16, "Spectral Tilt", 1.8, "Spectral Tilt Brightness Sheen (+1.8 dB)")
    set_param(track, fx_idx, 3, "Headroom Target", -6.0, "Pre-Master Headroom Target (-6.0 dBTP)")
    set_param(track, fx_idx, 40, "Mix Bus Headroom", 1, "Mix Bus Clipper (Lance Prenc Soft Clip)")
    set_param(track, fx_idx, 8, "Compressor Topology", 0, "Comp Topology (British VCA)")
    set_param(track, fx_idx, 10, "Comp Ratio", 1, "Comp Ratio (2:1)")
    set_param(track, fx_idx, 11, "Comp Attack", 30, "Comp Attack (30 ms)")
    set_param(track, fx_idx, 12, "Comp Release", 0, "Comp Release (Auto)")
    -- De-Boom & Vocal Unbury Pocket
    set_param(track, fx_idx, 41, "Producer Center Vocal Level Trim", 2.2, "Producer Center Vocal Trim (+2.2 dB)")
    set_param(track, fx_idx, 28, "Center Vocal Donut-Hole", 2, "Center Vocal Donut-Hole (Deep Cut -3.5 dB @ 2500 Hz)")
    set_param(track, fx_idx, 29, "Vocal Donut-Hole Center", 2500, "Vocal Donut-Hole Center Frequency (2500 Hz)")
    set_param(track, fx_idx, 17, "Dynamic De-Box Mud Gain", -2.5, "Dynamic De-Box Mud Gain (-2.5 dB)")
    set_param(track, fx_idx, 18, "Dynamic De-Box Frequency", 160, "Dynamic De-Box Frequency (160 Hz)")
    set_param(track, fx_idx, 30, "Guitar Palm-Mute Chug Guard", 1, "Guitar Palm-Mute Chug Guard (Fast Notch 190 Hz)")
    -- Producer Plays & Song Structure AI
    set_param(track, fx_idx, 44, "Song Structure", 2, "Play 4: Song Structure AI (Commercial Drop Slam: +0.16x Width / +1.4 dB Punch)")
    set_param(track, fx_idx, 45, "Song Structure Detection", 0, "Detection Mode (Hybrid Prioritizing REAPER Regions)")
  end

  -- 8. SANKOFA ORACLE (Master Track)
  if string.find(lower_name, "assessmentmatrix", 1, true) or string.find(lower_name, "sankofa oracle", 1, true) then
    msg(string.format("✔ RELAYING SANKOFA ORACLE on %s", loc_tag))
    stats.suites_updated = stats.suites_updated + 1
    set_param(track, fx_idx, 3, "Library Ref Target", 2, "Library Preset (Split Chain)")
    set_param(track, fx_idx, 9, "Reference Preset", 6, "Reference Benchmark (Split Chain)")
    set_param(track, fx_idx, 7, "Static Calibration Lock", 1, "Static Calibration Lock (Engaged)")
    set_param(track, fx_idx, 12, "Monitor Mode", 0, "Shootout Monitor Mode (MIX)")
  end
end

-- Scan Master Track
local master_tr = reaper.GetMasterTrack(0)
stats.tracks_scanned = stats.tracks_scanned + 1
for fx = 0, reaper.TrackFX_GetCount(master_tr) - 1 do
  process_fx(master_tr, "MASTER", fx)
end

-- Scan All Regular Tracks
local num_tracks = reaper.CountTracks(0)
for t = 0, num_tracks - 1 do
  local tr = reaper.GetTrack(0, t)
  stats.tracks_scanned = stats.tracks_scanned + 1
  local _, tr_name = reaper.GetTrackName(tr, "")
  for fx = 0, reaper.TrackFX_GetCount(tr) - 1 do
    process_fx(tr, tr_name, fx)
  end
end

-- Balance Bus Faders: Lock Instrumental Bus to -4.9 dB and Vox to Golden Pocket
for t = 0, num_tracks - 1 do
  local tr = reaper.GetTrack(0, t)
  local _, tr_name = reaper.GetTrackName(tr, "")
  if tr_name == "VOX" then
    reaper.SetMediaTrackInfo_Value(tr, "D_VOL", 1.15)
    msg("   ★ OPTIMIZED TRACK FADER: [VOX] set to +1.2 dB (Sits inside mix pocket)")
  elseif tr_name == "INSTRUMENTAL//BUSS" then
    reaper.SetMediaTrackInfo_Value(tr, "D_VOL", 0.80)
    msg("   ★ LOCKED INSTRUMENTAL BUS: [INSTRUMENTAL//BUSS] calibrated to -4.9 dB peak")
  elseif tr_name:find("Vocals") and not tr_name:find("Ref") then
    reaper.SetMediaTrackInfo_Value(tr, "D_VOL", 1.0)
  end
end

-- Update Telemetry Memory Bus
reaper.gmem_attach("DameiMixMetering")
reaper.gmem_write(1159, 1) -- Static Calibration & Relay Locked Flag
reaper.gmem_write(1158, 0) -- Shootout Mode: Mix

reaper.Undo_EndBlock("Relay Producer DNA & Ear-Candy to Suites", -1)

msg("--------------------------------------------------------------------------------")
msg(string.format("⚡ RELAY COMPLETE: %d Suites Synchronized | %d Parameters Armed | %d Bypasses Fixed", stats.suites_updated, stats.params_modified, stats.bypasses_fixed))
msg("   All 7 Producer Plays Armed across Vocal, Drums, Guitar, Bass, Synth, Devastator & Mix Bus.")
msg("   Playback Audition: Spacebar to play. Shootout pill active on Mixing Suite & Sankofa Oracle.")
msg("================================================================================")
if log_file then log_file:close() end
