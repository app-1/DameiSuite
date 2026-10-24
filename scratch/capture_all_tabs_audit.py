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

artifact_dir = r"C:\Users\pityy\.gemini\antigravity-ide\brain\3c9ba815-5b40-4462-b423-397fc6dc8ce3"

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
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    bbox = (rect.left, rect.top, rect.right, rect.bottom)
    user32.ShowWindow(hwnd, 9) # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.35)
    im = ImageGrab.grab(bbox=bbox)
    out_path = os.path.join(artifact_dir, filename)
    im.save(out_path)
    print(f"Captured: {filename} ({im.size[0]}x{im.size[1]})")
    return out_path

suites_to_capture = [
    {
        "name": "Guitar Suite",
        "track_type": "track",
        "track_idx": 50,
        "fx_idx": 0,
        "param_tab": 0,
        "wnd_title": "Guitar Bus",
        "tabs": [
            (0, "guitar_tab0_overview.png"),
            (1, "guitar_tab1_chug_sculptor.png"),
            (2, "guitar_tab2_defizz_tamer.png"),
            (3, "guitar_tab3_stereo_imager.png"),
            (4, "guitar_tab4_analog_glue.png"),
            (5, "guitar_tab5_producer_matrix.png"),
            (6, "guitar_tab6_ear_candy.png"),
        ]
    },
    {
        "name": "Drum Suite",
        "track_type": "track",
        "track_idx": 15,
        "fx_idx": 0,
        "param_tab": 0,
        "wnd_title": "Drum Bus",
        "tabs": [
            (0, "drum_tab0_overview.png"),
            (1, "drum_tab1_beat_leveler.png"),
            (2, "drum_tab2_cymbal_silk.png"),
            (3, "drum_tab3_shell_weight.png"),
            (4, "drum_tab4_bsa_bus.png"),
            (5, "drum_tab5_transient_snap.png"),
            (6, "drum_tab6_producer_matrix.png"),
        ]
    },
    {
        "name": "Bass Suite",
        "track_type": "track",
        "track_idx": 68,
        "fx_idx": 0,
        "param_tab": 0,
        "wnd_title": "Bass Bus",
        "tabs": [
            (0, "bass_tab0_overview.png"),
            (1, "bass_tab1_trackspacer.png"),
            (2, "bass_tab2_sub_anchor.png"),
            (3, "bass_tab3_split_chain.png"),
            (4, "bass_tab4_phase_radar.png"),
            (5, "bass_tab5_analog_glue.png"),
            (6, "bass_tab6_producer_matrix.png"),
        ]
    },
    {
        "name": "Vocal Suite",
        "track_type": "track",
        "track_idx": 3,
        "fx_idx": 0,
        "param_tab": 0,
        "wnd_title": "Vocal Sovereign",
        "tabs": [
            (0, "vocal_tab0_aura_stems.png"),
            (1, "vocal_tab1_ear_candy.png"),
            (2, "vocal_tab2_dual_dynamics.png"),
            (3, "vocal_tab3_ms_pocket.png"),
            (4, "vocal_tab4_analog_air.png"),
            (5, "vocal_tab5_producer_matrix.png"),
        ]
    },
    {
        "name": "Synth Suite",
        "track_type": "track",
        "track_idx": 39,
        "fx_idx": 0,
        "param_tab": 0,
        "wnd_title": "Synth Bus",
        "tabs": [
            (0, "synth_tab0_overview.png"),
            (1, "synth_tab1_pockets_dev.png"),
            (2, "synth_tab2_asase_synbass.png"),
            (3, "synth_tab3_3d_horizon.png"),
            (4, "synth_tab4_multiband_eq.png"),
            (5, "synth_tab5_britson_sheen.png"),
            (6, "synth_tab6_producer_codex.png"),
            (7, "synth_tab7_ear_candy.png"),
        ]
    },
    {
        "name": "Mixing Suite",
        "track_type": "master",
        "track_idx": 0,
        "fx_idx": 0,
        "param_tab": 0,
        "wnd_title": "Mixing Suite",
        "tabs": [
            (0, "mix_tab0_overview.png"),
            (1, "mix_tab1_eq_deess.png"),
            (2, "mix_tab2_comp_punch.png"),
            (3, "mix_tab3_color_tape.png"),
            (4, "mix_tab4_stereo_space.png"),
            (5, "mix_tab5_ai_assist.png"),
        ]
    },
    {
        "name": "Sankofa Oracle",
        "track_type": "master",
        "track_idx": 0,
        "fx_idx": 1,
        "param_tab": 14,
        "wnd_title": "Sankofa",
        "tabs": [
            (0, "sankofa_view0_matrix.png"),
            (1, "sankofa_view1_library.png"),
            (2, "sankofa_view2_mastering.png"),
            (3, "sankofa_view3_ollama_ai.png"),
            (4, "sankofa_view4_stem_ab.png"),
            (5, "sankofa_view5_producer_dna.png"),
        ]
    }
]

for s in suites_to_capture:
    print(f"\n=== Capturing {s['name']} Tabs ===")
    
    # 1. Hot-reload effect and show window
    if s["track_type"] == "master":
        lua_open = f"""
        local master = reaper.GetMasterTrack(0)
        reaper.TrackFX_SetOffline(master, {s['fx_idx']}, true)
        reaper.TrackFX_SetOffline(master, {s['fx_idx']}, false)
        reaper.TrackFX_Show(master, {s['fx_idx']}, 3)
        """
    else:
        lua_open = f"""
        local tr = reaper.GetTrack(0, {s['track_idx']})
        reaper.TrackFX_SetOffline(tr, {s['fx_idx']}, true)
        reaper.TrackFX_SetOffline(tr, {s['fx_idx']}, false)
        reaper.TrackFX_Show(tr, {s['fx_idx']}, 3)
        """
    run_lua(lua_open)
    time.sleep(0.6)
    
    hwnd = find_window_by_substr(s["wnd_title"])
    if not hwnd:
        print(f"Could not find window for {s['name']}")
        continue

    for tab_idx, filename in s["tabs"]:
        if s["track_type"] == "master":
            lua_tab = f"""
            local master = reaper.GetMasterTrack(0)
            reaper.TrackFX_SetParam(master, {s['fx_idx']}, {s['param_tab']}, {float(tab_idx)})
            """
        else:
            lua_tab = f"""
            local tr = reaper.GetTrack(0, {s['track_idx']})
            reaper.TrackFX_SetParam(tr, {s['fx_idx']}, {s['param_tab']}, {float(tab_idx)})
            """
        run_lua(lua_tab)
        time.sleep(0.3)
        capture_window(hwnd, filename)

    # Close window and reset to tab 0
    if s["track_type"] == "master":
        run_lua(f"""
        local master = reaper.GetMasterTrack(0)
        reaper.TrackFX_SetParam(master, {s['fx_idx']}, {s['param_tab']}, 0.0)
        reaper.TrackFX_Show(master, {s['fx_idx']}, 2)
        """)
    else:
        run_lua(f"""
        local tr = reaper.GetTrack(0, {s['track_idx']})
        reaper.TrackFX_SetParam(tr, {s['fx_idx']}, {s['param_tab']}, 0.0)
        reaper.TrackFX_Show(tr, {s['fx_idx']}, 2)
        """)

# Also capture Ozone Suite all tabs
print("\n=== Capturing Ozone 12 Mastering Suite Tabs ===")
run_lua(r"""
local master = reaper.GetMasterTrack(0)
local idx = reaper.TrackFX_AddByName(master, "Damei_OzoneSuite.jsfx", false, -1)
reaper.TrackFX_Show(master, idx, 3)
""")
time.sleep(0.8)
ozone_hwnd = find_window_by_substr("Ozone 12")
if ozone_hwnd:
    ozone_tabs = [
        (0, "ozone_tab0_overview.png"),
        (1, "ozone_tab1_tonal_bal.png"),
        (2, "ozone_tab2_master_eq.png"),
        (3, "ozone_tab3_dynamics.png"),
        (4, "ozone_tab4_imager.png"),
        (5, "ozone_tab5_maximizer.png"),
        (6, "ozone_tab6_playbook.png"),
    ]
    for tab_idx, filename in ozone_tabs:
        run_lua(f"""
        local master = reaper.GetMasterTrack(0)
        -- Find ozone idx
        local cnt = reaper.TrackFX_GetCount(master)
        for i = 0, cnt-1 do
            local ret, name = reaper.TrackFX_GetFXName(master, i)
            if string.find(name:lower(), "ozone") then
                reaper.TrackFX_SetParam(master, i, 1, {float(tab_idx)}) -- slider2 is Active Module
            end
        end
        """)
        time.sleep(0.3)
        capture_window(ozone_hwnd, filename)

    # Remove temporary ozone instance
    run_lua(r"""
    local master = reaper.GetMasterTrack(0)
    local cnt = reaper.TrackFX_GetCount(master)
    for i = cnt-1, 0, -1 do
        local ret, name = reaper.TrackFX_GetFXName(master, i)
        if string.find(name:lower(), "ozone") then
            reaper.TrackFX_Delete(master, i)
        end
    end
    """)

print("\nAll tabs across all suites successfully captured!")
