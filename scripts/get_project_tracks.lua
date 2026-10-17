-- Damei Auto-Pull: get_project_tracks.lua
-- Collects REAPER project + track data and sends to DameiAPI /pull
-- No external dependencies. Uses JS_ReaScriptAPI.

local function safe(value)
    return tostring(value or "")
end

local function collect_tracks()
    local tracks = {}
    local count = reaper.CountTracks(0)

    for i = 0, count - 1 do
        local track = reaper.GetTrack(0, i)
        local _, name = reaper.GetSetMediaTrackInfo_String(track, "P_NAME", "", false)

        tracks[#tracks + 1] = {
            number = i + 1,
            name = safe(name)
        }
    end

    return tracks
end

local function autopull()
    if type(reaper.JS_JSON_Encode) ~= "function" then
        reaper.ShowConsoleMsg("ERROR: JS_ReaScriptAPI not loaded.\n")
        return
    end

    local project_path = reaper.GetProjectPath("") or "UnknownProject"
    local payload = {
        project = project_path,
        tracks = collect_tracks()
    }

    local json = reaper.JS_JSON_Encode(payload)
    reaper.JS_HTTP_Transfer("POST", "http://127.0.0.1:8765/pull", json, "Content-Type: application/json")

    reaper.ShowConsoleMsg("Damei Auto-Pull sent project + tracks.\n")
end

autopull()
