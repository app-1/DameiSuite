"""Compute reference fingerprints for every producer preset and inject them into Damei_AssessmentMatrix.jsfx.

Usage: python gen_fingerprints.py            (uses cache fp_cache.json when present)
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import assess_matrix as am

REF = r"H:\REFERENCES"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "fp_cache.json")
JSFX = os.path.join(os.path.dirname(HERE), "effects", "Damei_AssessmentMatrix.jsfx")

# producer preset index (Mixing Suite slider39) -> reference file
PRESET_REF = {
    1: "Alpha Wolf, Holding Absence - Alpha Wolf - 60cm Of Steel (feat. Holding Absence).wav",
    2: "DIESECT - TOO MANY SCARS.wav",
    3: "Mirrorcell - U(phoria).wav",
    4: "thrown - on the verge.wav",
    5: "blanket - Blur.wav",
    6: "Split Chain - motionblur - 03 I'm Not Dying To Be Here.wav",
    7: "Don Broco - Endorphins.wav",
    8: "Static Dress - face..wav",
    9: "Shyeye, Showing Teeth - Knot feat. Showing Teeth - Remix.wav",
    10: "Heavenward - Tangerine.wav",
    11: "City Of Souls - Cruelty.wav",
    12: "SUNBORN - Nebula.wav",
    14: "Fit For An Autopsy - Walk With Me In Hell.wav",
    15: "Loathe - Agressive Evolution.wav",
    16: "Thornhill - nerv.wav",
    17: "8. Gravity.flac",
    18: "Spiritbox - Keep Sweet.wav",
    19: "Bad Omens - THE DEATH OF PEACE OF MIND.wav",
    22: "TesseracT - King.wav",
    23: "heaving. - why are you still dreaming- - 03 carsick.wav",
    24: "SENNA - Out of The Blue.flac",
}
KEYS = ["lufs", "plr", "crest", "lra", "corr", "width"]

# Full reference library shown in the Assessment Matrix: (file, display name, producer preset index or -1)
LIBRARY = [
    (PRESET_REF[1],  "Alpha Wolf - 60cm Of Steel", 1),
    (PRESET_REF[2],  "DIESECT - Too Many Scars", 2),
    (PRESET_REF[3],  "Mirrorcell - U(phoria)", 3),
    (PRESET_REF[4],  "thrown - on the verge", 4),
    (PRESET_REF[5],  "blanket - Blur", 5),
    (PRESET_REF[6],  "Split Chain - I'm Not Dying To Be Here", 6),
    (PRESET_REF[7],  "Don Broco - Endorphins", 7),
    (PRESET_REF[8],  "Static Dress - face.", 8),
    (PRESET_REF[9],  "Shyeye - Knot (Remix)", 9),
    (PRESET_REF[10], "Heavenward - Tangerine", 10),
    (PRESET_REF[11], "City Of Souls - Cruelty", 11),
    (PRESET_REF[12], "SUNBORN - Nebula", 12),
    (PRESET_REF[14], "Fit For An Autopsy - Walk With Me In Hell", 14),
    (PRESET_REF[15], "Loathe - Aggressive Evolution", 15),
    (PRESET_REF[16], "Thornhill - nerv", 16),
    (PRESET_REF[17], "Architects - Gravity", 17),
    (PRESET_REF[18], "Spiritbox - Keep Sweet", 18),
    (PRESET_REF[19], "Bad Omens - Death Of Peace Of Mind", 19),
    (PRESET_REF[22], "TesseracT - King", 22),
    (PRESET_REF[23], "heaving. - carsick (Adam Cichocki)", 23),
    ("Northlane - Evian.wav", "Northlane - Evian", -1),
    ("Love Is Noise - All Eyes Shut - Hole In Me (24-bit HD audio) - 02 Hole In Me.wav", "Love Is Noise - Hole In Me", -1),
    ("01 The End of All We Know.flac", "The End Of All We Know", -1),
    ("Flake - Grief.wav", "Flake - Grief", -1),
    (PRESET_REF[24], "SENNA - Out Of The Blue (Manuel Renner)", 24),
]
BN = [b[0] for b in am.BANDS]


def main():
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    for fn in [f for f, _, _ in LIBRARY]:
        if fn in cache:
            continue
        p = os.path.join(REF, fn)
        print("analysing", fn, flush=True)
        s = am.stats(p)
        cache[fn] = {k: float(s[k]) for k in KEYS}
        cache[fn]["pct"] = [float(s["pct"][b]) for b in BN]
        cache[fn]["bw"] = [float(s["bwidth"][b]) for b in BN]
        json.dump(cache, open(CACHE, "w"), indent=1)

    rows = {i: cache[f] for i, f in PRESET_REF.items()}
    avg = {k: float(np.mean([r[k] for r in rows.values()])) for k in KEYS}
    avg["pct"] = list(np.mean([r["pct"] for r in rows.values()], axis=0))
    avg["bw"] = list(np.mean([r["bw"] for r in rows.values()], axis=0))

    lines = []
    for idx in range(0, 25):
        r = rows.get(idx, avg)
        has = 1 if idx in rows else 0
        vals = [r[k] for k in KEYS] + r["pct"] + r["bw"]
        body = " ".join(f"p[{j}]={v:.4f};" for j, v in enumerate(vals))
        lines.append(f"  p = FP + {idx}*32; {body} p[31]={has};")
    block = "\n".join(lines)

    src = open(JSFX, encoding="utf-8").read()
    a, b = "// <<FP_BEGIN>>", "// <<FP_END>>"
    i, j = src.index(a) + len(a), src.index(b)
    out = src[:i] + "\n" + block + "\n  " + src[j:]

    # ---- full reference library block (22 tracks: stats, producer link, names)
    lib_lines, names = [], []
    for k, (fn, nm, pre) in enumerate(LIBRARY):
        r = cache[fn]
        vals = [r[kk] for kk in KEYS] + r["pct"] + r["bw"]
        body = " ".join(f"p[{jj}]={v:.4f};" for jj, v in enumerate(vals))
        lib_lines.append(f"  p = LIB + {k}*32; {body} p[31]=1; LPR[{k}]={pre};")
        names.append(nm.replace('"', "'"))
    chain = " :\n    ".join(f'i == {k} ? strcpy(out, "{n}")' for k, n in enumerate(names))
    lib_lines.append("  function lib_name(i, out) (\n    " + chain + " :\n    strcpy(out, \"?\");\n  );")
    la, lb = "// <<LIB_BEGIN>>", "// <<LIB_END>>"
    i2, j2 = out.index(la) + len(la), out.index(lb)
    out = out[:i2] + "\n" + "\n".join(lib_lines) + "\n  " + out[j2:]
    open(JSFX, "w", encoding="utf-8", newline="").write(out)
    print("fingerprints injected:", len(rows), "preset refs +", len(LIBRARY), "library tracks")


if __name__ == "__main__":
    main()
