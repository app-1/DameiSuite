import sys, time, urllib.request
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

def test_config(desc, lua_setup):
    run_lua(f"""
    local tr4 = reaper.GetTrack(0, 3)
    {lua_setup}
    """)
    url = 'http://127.0.0.1:8080/_/SET/POS/26.0;1007'
    with urllib.request.urlopen(url) as r: r.read()
    time.sleep(2.0)
    with urllib.request.urlopen('http://127.0.0.1:8080/_/TRACK/4;1016') as r:
        lines = r.read().decode('utf-8').strip().splitlines()
    for l in lines:
        parts = l.split("\t")
        if len(parts) >= 8 and parts[0] == "TRACK":
            p = max(float(parts[6]), float(parts[7])) / 10.0
            print(f"{desc:35s}: {p:+.1f} dB")

print("--- ISOLATING VOCAL SUITE ATTENUATION ---")
# 1. Base
test_config("1. Current Base", "")

# 2. ReEQ mud & harsh off
test_config("2. ReEQ cuts = 0", """
reaper.TrackFX_SetParam(tr4, 0, 43, 0)
reaper.TrackFX_SetParam(tr4, 0, 44, 0)
""")

# 3. FET & Opto off (slider6=0, slider7=0)
test_config("3. FET/Opto = 0", """
reaper.TrackFX_SetParam(tr4, 0, 5, 0)
reaper.TrackFX_SetParam(tr4, 0, 6, 0)
""")

# 4. De-Esser off (slider5=0)
test_config("4. De-Esser depth = 0", """
reaper.TrackFX_SetParam(tr4, 0, 4, 0)
""")

# 5. Center lead lock off (slider9=0)
test_config("5. Center Lead Lock = 0", """
reaper.TrackFX_SetParam(tr4, 0, 8, 0)
""")

# 6. Ear-Candy off (slider39=0)
test_config("6. Ear-Candy = 0", """
reaper.TrackFX_SetParam(tr4, 0, 34, 0)
""")

# 7. Matrix Trim off (slider35=0)
test_config("7. Matrix Trim = 0", """
reaper.TrackFX_SetParam(tr4, 0, 33, 0)
""")

# 8. ReEQ HPF = 50Hz
test_config("8. ReEQ HPF = 50Hz", """
reaper.TrackFX_SetParam(tr4, 0, 42, 50)
""")
