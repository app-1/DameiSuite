"""Add the Matrix energy-lane consumer (soft density shaper) to the instrument suites. Idempotent.

Reads gmem[1300 + lane*16 + 9] (0..1 density request published by Damei_AssessmentMatrix) and applies a
unity-small-signal soft peak shaper y = x / (1 + k|x|), k <= 0.25, at the end of mtrim_process().
Peaks drop more than RMS, so crest falls toward the reference. Only suites the Matrix weights > 0 receive a
non-zero request (drums, guitar, synth, devastator at half); bass and vocal are patched too but stay at 0.
"""
import os, shutil
D = r"C:\Dev\DameiAPI\reaper_scripts"
BK = os.path.join(D, "backups_preenergy")
os.makedirs(BK, exist_ok=True)
SUITES = ["Damei_DrumSuite.jsfx", "Damei_GuitarSuite.jsfx", "Damei_BassSuite.jsfx",
          "Damei_VocalSuite.jsfx", "Damei_SynthSuite.jsfx", "Damei_DevastatorSuite.jsfx"]
TAG = "// ENERGY LANE"


def patch(fn):
    p = os.path.join(D, fn)
    raw = open(p, encoding="utf-8", newline="").read()
    if TAG in raw:
        return fn + ": already patched"
    shutil.copyfile(p, os.path.join(BK, fn))
    crlf = "\r\n" in raw
    t = raw.replace("\r\n", "\n")

    def sub1(t, a, b):
        assert t.count(a) == 1, (fn, a, t.count(a))
        return t.replace(a, b)

    t = sub1(t, "mtrim_on = 0; mtrim_cnt = 0;\n",
             "mtrim_on = 0; mtrim_cnt = 0;\n" + TAG + " state: smoothed density request (0..1) + shaper coefficient\n"
             "mtrim_ed = 0; mtrim_ek = 0;\n")
    t = sub1(t, "  mtrim_on = any;\n",
             "  mtrim_on = any;\n"
             "  mtrim_ed += ((ok ? gmem[mtrim_lane + 9] : 0) - mtrim_ed) * 0.02;   // ~1 s ramp\n"
             "  mtrim_ek = max(0, min(1, mtrim_ed)) * 0.25;\n")
    t = sub1(t, "    spl0 = mm + ss; spl1 = mm - ss;\n  );\n);\n// ===== MATRIX TRIM END",
             "    spl0 = mm + ss; spl1 = mm - ss;\n  );\n"
             "  mtrim_ek > 0.002 ? (\n"
             "    spl0 = spl0 / (1 + mtrim_ek * abs(spl0));\n"
             "    spl1 = spl1 / (1 + mtrim_ek * abs(spl1));\n"
             "  );\n);\n// ===== MATRIX TRIM END")
    out = t.replace("\n", "\r\n") if crlf else t
    open(p, "w", encoding="utf-8", newline="").write(out)
    return fn + ": patched"


for f in SUITES:
    print(patch(f))
