"""Phase 0 mix-balance regression gate.

Compare two renders (before/after a change) of the same project region.
  python tools/mix_regression.py before.wav after.wav [--tol-band 0.1] [--tol-lufs 0.1]

Checks (all must pass):
  1. Null depth      : residual (after - before) RMS vs before RMS   (Preset-0 gate wants <= -60 dB)
  2. Integrated LUFS : |delta| <= tol-lufs
  3. PLR / crest     : |delta| <= 0.2 dB
  4. 7-band energy   : each band |delta in dB| <= tol-band
Exit code 0 = PASS, 1 = FAIL.
"""
import sys, os, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assess_matrix as am
import soundfile as sf


def load(p):
    x, sr = sf.read(p, always_2d=True)
    return x.astype(np.float64), sr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("before"); ap.add_argument("after")
    ap.add_argument("--tol-lufs", type=float, default=0.1)
    ap.add_argument("--tol-band", type=float, default=0.1)
    ap.add_argument("--null-db", type=float, default=-60.0)
    a = ap.parse_args()

    xb, srb = load(a.before); xa, sra = load(a.after)
    if srb != sra:
        print("FAIL: sample-rate mismatch"); return 1
    n = min(len(xb), len(xa)); xb, xa = xb[:n], xa[:n]
    rms = lambda v: float(np.sqrt(np.mean(v ** 2)) + 1e-12)
    null_db = 20 * np.log10(rms(xa - xb) / rms(xb))

    sb, sa = am.stats(a.before), am.stats(a.after)
    ok = True
    def row(name, v, lim, cond):
        nonlocal ok
        flag = "PASS" if cond else "FAIL"
        ok &= cond
        print(f"{flag}  {name:22} {v:+8.3f}   (limit {lim})")

    row("null depth (dB)", null_db, f"<= {a.null_db}", null_db <= a.null_db)
    row("LUFS delta", sa["lufs"] - sb["lufs"], f"+-{a.tol_lufs}", abs(sa["lufs"] - sb["lufs"]) <= a.tol_lufs)
    row("PLR delta", sa["plr"] - sb["plr"], "+-0.2", abs(sa["plr"] - sb["plr"]) <= 0.2)
    row("crest delta", sa["crest"] - sb["crest"], "+-0.2", abs(sa["crest"] - sb["crest"]) <= 0.2)
    for band in [b[0] for b in am.BANDS]:
        d = 10 * np.log10((sa["pct"][band] + 1e-9) / (sb["pct"][band] + 1e-9))
        row(f"band {band}", d, f"+-{a.tol_band}", abs(d) <= a.tol_band)
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
