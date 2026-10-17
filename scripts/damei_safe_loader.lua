-- Damei Safe Loader
-- Waits for JS_ReaScriptAPI to load, then runs Auto-Pull

local AUTO_PULL_CMD = "_RS_REPLACE_ME"

local function js_ready()
    return type(reaper.JS_JSON_Encode) == "function"
end

local function run_autopull()
    reaper.Main_OnCommand(reaper.NamedCommandLookup(AUTO_PULL_CMD), 0)
end

local function wait_for_js()
    if js_ready() then
        run_autopull()
    else
        reaper.defer(wait_for_js)
    end
end

wait_for_js()
