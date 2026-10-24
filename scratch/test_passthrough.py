import sys, math, time, urllib.request
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

jsfx_path = r"C:\Dev\DameiSuite\effects\Damei_VocalSuite.jsfx"
appdata_jsfx = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_VocalSuite.jsfx"

original_code = open(jsfx_path, "r", encoding="utf-8").read()

def measure_peak():
    url = 'http://127.0.0.1:8080/_/SET/POS/26.0;1007'
    with urllib.request.urlopen(url) as r: r.read()
    time.sleep(2.0)
    with urllib.request.urlopen('http://127.0.0.1:8080/_/TRACK/4;1016') as r:
        lines = r.read().decode('utf-8').strip().splitlines()
    for l in lines:
        parts = l.split("\t")
        if len(parts) >= 8 and parts[0] == "TRACK":
            return max(float(parts[6]), float(parts[7])) / 10.0
    return -150.0

def reload_fx():
    run_lua("""
    local tr4 = reaper.GetTrack(0, 3)
    reaper.TrackFX_SetOffline(tr4, 0, true)
    reaper.TrackFX_SetOffline(tr4, 0, false)
    """)

# Test 1: Complete passthrough @sample
passthrough_sample = """
@sample
spl0 = spl0;
spl1 = spl1;

@gfx 1080 700
"""
idx_sample = original_code.find("@sample")
idx_gfx = original_code.find("@gfx 1080 700")

code_passthrough = original_code[:idx_sample] + passthrough_sample + original_code[idx_gfx + len("@gfx 1080 700"):]
with open(appdata_jsfx, "w", encoding="utf-8") as f: f.write(code_passthrough)
reload_fx()
p_pass = measure_peak()
print(f"PASSTHROUGH Peak: {p_pass:+.1f} dB (Track 5 is -9.4 dB)")

# Restore original
with open(appdata_jsfx, "w", encoding="utf-8") as f: f.write(original_code)
reload_fx()
