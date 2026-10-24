import sys, math, time, urllib.request
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

def test(bypass):
    run_lua(f"""
    local tr4 = reaper.GetTrack(0, 3)
    reaper.TrackFX_SetEnabled(tr4, 0, {str(not bypass).lower()})
    """)
    url = 'http://127.0.0.1:8080/_/SET/POS/26.0;1007'
    with urllib.request.urlopen(url) as r: r.read()
    time.sleep(2.5)
    with urllib.request.urlopen('http://127.0.0.1:8080/_/TRACK/4;TRACK/5;1016') as r:
        lines = r.read().decode('utf-8').strip().splitlines()
    for l in lines:
        parts = l.split("\t")
        if len(parts) >= 8 and parts[0] == "TRACK":
            p = max(float(parts[6]), float(parts[7])) / 10.0
            print(f"[{'BYPASSED' if bypass else 'ENABLED'}] Track {parts[1]} ({parts[2]}): {p:+.1f} dB")

print("Testing with FX 0 ENABLED:")
test(False)
print("\nTesting with FX 0 BYPASSED:")
test(True)
# Restore enabled
run_lua("reaper.TrackFX_SetEnabled(reaper.GetTrack(0, 3), 0, true)")
