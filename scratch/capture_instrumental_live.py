# capture_instrumental_live.py
import ctypes
from ctypes import wintypes
from PIL import ImageGrab
import os, time, sys, urllib.request

sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

user32 = ctypes.windll.user32
h_winsta = user32.OpenWindowStationW('winsta0', False, 0x0000037F)
user32.SetProcessWindowStation(h_winsta)
h_desktop = user32.OpenDesktopW('default', 0, False, 0x01FF)
user32.SetThreadDesktop(h_desktop)

artifact_dir = r"C:\Users\pityy\.gemini\antigravity-ide\brain\328c4ccd-e72c-4931-b325-85fce2a131a1"
os.makedirs(artifact_dir, exist_ok=True)

def find_window_by_substr(substr):
    found_hwnd = 0
    def enum_cb(hwnd, lparam):
        nonlocal found_hwnd
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                if substr.lower() in buff.value.lower():
                    found_hwnd = hwnd
                    return False
        return True
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
    return found_hwnd

def capture_window(hwnd, filename):
    if not hwnd:
        print(f"Skipping {filename}: window not found")
        return None
    user32.ShowWindow(hwnd, 9)
    user32.SetWindowPos(hwnd, 0, 40, 40, 1100, 740, 0x0040)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.4)
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    bbox = (rect.left, rect.top, rect.right, rect.bottom)
    im = ImageGrab.grab(bbox=bbox)
    out_path = os.path.join(artifact_dir, filename)
    im.save(out_path)
    print(f"Captured: {filename} ({im.size[0]}x{im.size[1]}) -> {out_path}")
    return out_path

# Open Floating FX Window for Track 15 (idx 14), FX 5
lua_open = """
local trk = reaper.GetTrack(0, 14)
if trk then
    reaper.TrackFX_Show(trk, 5, 3) -- floating window
end
return "OPENED"
"""
run_lua(lua_open)
time.sleep(1.0)

hwnd = find_window_by_substr("Alchemist")
if not hwnd:
    hwnd = find_window_by_substr("Instrumental")
print(f"Found Window HWND: {hwnd}")

# Start playback at chorus (28.0s) so live metrics are actively animating
try:
    urllib.request.urlopen("http://127.0.0.1:8080/_/SET/POS/28.0;1007")
except Exception as e:
    print("Web API play error:", e)

tabs = [
    (0, "inst_v7_tab0_overview.png"),
    (1, "inst_v7_tab1_tonal_eq.png"),
    (2, "inst_v7_tab2_bus_glue.png"),
    (3, "inst_v7_tab3_crucible.png"),
    (4, "inst_v7_tab4_stereo.png"),
    (5, "inst_v7_tab5_pocket.png"),
    (6, "inst_v7_tab6_producer.png"),
]

for tab_idx, filename in tabs:
    lua_tab = f"""
    local trk = reaper.GetTrack(0, 14)
    if trk then
        reaper.TrackFX_SetParam(trk, 5, 0, {tab_idx})
    end
    return {tab_idx}
    """
    run_lua(lua_tab)
    time.sleep(0.5)
    capture_window(hwnd, filename)

# Stop playback
try:
    urllib.request.urlopen("http://127.0.0.1:8080/_/1016")
except Exception as e:
    pass

print("Live capture sequence complete!")
