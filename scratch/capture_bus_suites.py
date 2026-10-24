import ctypes
from ctypes import wintypes
from PIL import ImageGrab
import os, time, sys

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
    rect = wintypes.RECT()
    user32.ShowWindow(hwnd, 9) # SW_RESTORE
    user32.SetWindowPos(hwnd, 0, 40, 40, 1100, 740, 0x0040)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    bbox = (rect.left, rect.top, rect.right, rect.bottom)
    im = ImageGrab.grab(bbox=bbox)
    out_path = os.path.join(artifact_dir, filename)
    im.save(out_path)
    print(f"Captured: {filename} ({im.size[0]}x{im.size[1]}) -> {out_path}")
    return out_path

suites_to_capture = [
    {
        "name": "Instrumental Bus Alchemist",
        "track_idx": 14, # Track 15 (0-indexed 14)
        "fx_idx": 5,
        "wnd_title": "Instrumental Bus",
        "tabs": [
            (0, "inst_bus_tab0_overview.png"),
            (1, "inst_bus_tab1_tonal_eq.png"),
            (2, "inst_bus_tab2_bus_glue.png"),
            (3, "inst_bus_tab3_crucible.png"),
            (4, "inst_bus_tab4_stereo.png"),
            (5, "inst_bus_tab5_pocket.png"),
            (6, "inst_bus_tab6_producer.png"),
        ]
    },
    {
        "name": "Vocal Empress",
        "track_idx": 3, # Track 4 (0-indexed 3)
        "fx_idx": 1,
        "wnd_title": "Vocal Empress",
        "tabs": [
            (0, "vocal_bus_tab0_overview.png"),
            (1, "vocal_bus_tab1_baxandall.png"),
            (2, "vocal_bus_tab2_vocal_glue.png"),
            (3, "vocal_bus_tab3_deesser.png"),
            (4, "vocal_bus_tab4_spatial.png"),
            (5, "vocal_bus_tab5_presence.png"),
            (6, "vocal_bus_tab6_producer.png"),
        ]
    }
]

for suite in suites_to_capture:
    t_idx = suite["track_idx"]
    fx_idx = suite["fx_idx"]
    
    # 1. Close any other open FX windows and open this one floating
    lua_open = f"""
    local trk = reaper.GetTrack(0, {t_idx})
    if trk then
        reaper.TrackFX_Show(trk, {fx_idx}, 3) -- 3 = show floating window
    end
    return "OPENED"
    """
    run_lua(lua_open)
    time.sleep(1.0)
    
    hwnd = find_window_by_substr(suite["wnd_title"])
    if not hwnd:
        # Fallback to search by "JS:" or partial name
        hwnd = find_window_by_substr("Alchemist") if "Instrumental" in suite["name"] else find_window_by_substr("Empress")
    
    print(f"Suite: {suite['name']} -> HWND: {hwnd}")
    
    for tab_idx, filename in suite["tabs"]:
        lua_tab = f"""
        local trk = reaper.GetTrack(0, {t_idx})
        if trk then
            reaper.TrackFX_SetParam(trk, {fx_idx}, 0, {tab_idx})
        end
        return {tab_idx}
        """
        run_lua(lua_tab)
        time.sleep(0.35)
        capture_window(hwnd, filename)

print("All screenshots capture sequence complete.")
