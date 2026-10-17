"""Assessment matrix: HexGyal mix/master vs reference (loudness-matched)."""
import sys, json
import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import butter, sosfilt, resample_poly

BANDS = [("sub 20-60", 20, 60), ("low 60-250", 60, 250), ("lowmid 250-800", 250, 800),
         ("mid 800-2.5k", 800, 2500), ("hmid 2.5-6k", 2500, 6000), ("high 6-10k", 6000, 10000),
         ("air 10-18k", 10000, 18000)]


def load(p, sr=44100):
    x, s = sf.read(p, always_2d=True)
    x = x[:, :2] if x.shape[1] >= 2 else np.repeat(x, 2, 1)
    if s != sr:
        from math import gcd
        g = gcd(sr, s)
        x = resample_poly(x, sr // g, s // g, axis=0)
    return x.astype(np.float64), sr


def band(x, sr, lo, hi):
    # 2nd-order HP @lo then 2nd-order LP @hi : identical to the Damei_AssessmentMatrix JSFX band splitter
    hp = butter(2, lo, btype="high", fs=sr, output="sos")
    lp = butter(2, min(hi, sr * 0.45), btype="low", fs=sr, output="sos")
    return sosfilt(lp, sosfilt(hp, x, axis=0), axis=0)


def stats(path):
    x, sr = load(path)
    m = pyln.Meter(sr)
    lufs = m.integrated_loudness(x)
    mono = x.mean(1)
    peak = 20 * np.log10(np.max(np.abs(x)) + 1e-12)
    rms = 20 * np.log10(np.sqrt(np.mean(mono ** 2)) + 1e-12)
    # short-term LUFS distribution (3s windows, 1s hop) -> LRA-like
    w = 3 * sr
    st = [m.integrated_loudness(x[i:i + w]) for i in range(0, len(x) - w, sr)]
    st = np.array([v for v in st if np.isfinite(v) and v > -60])
    lra = np.percentile(st, 95) - np.percentile(st, 10) if len(st) > 5 else float("nan")
    # per-band energy share, crest, width
    mid, side = (x[:, 0] + x[:, 1]) / 2, (x[:, 0] - x[:, 1]) / 2
    energies, crest, width = {}, {}, {}
    tot = 0
    for n, lo, hi in BANDS:
        b = band(x, sr, lo, hi)
        e = np.mean(b ** 2)
        energies[n] = e
        tot += e
        bm = band(mid[:, None], sr, lo, hi)[:, 0]
        bs = band(side[:, None], sr, lo, hi)[:, 0]
        r = np.sqrt(np.mean(b ** 2))
        crest[n] = 20 * np.log10(np.max(np.abs(b)) / (r + 1e-12) + 1e-12)
        width[n] = np.sqrt(np.mean(bs ** 2)) / (np.sqrt(np.mean(bm ** 2)) + 1e-12)
    pct = {n: 100 * e / tot for n, e in energies.items()}
    # transient density: fraction of 10ms frames where envelope rises >6dB over previous 50ms
    env = np.abs(mono)
    f = int(0.01 * sr)
    fr = 20 * np.log10(np.sqrt(np.add.reduceat(env ** 2, np.arange(0, len(env) - f, f)) / f) + 1e-9)
    rise = fr[5:] - np.max(np.vstack([fr[i:len(fr) - 5 + i] for i in range(5)]), axis=0)
    trans = 100 * np.mean(rise > 6)
    corr = np.corrcoef(x[:, 0], x[:, 1])[0, 1]
    return dict(lufs=lufs, tp_approx=peak, rms=rms, crest=peak - rms, plr=peak - lufs, lra=lra,
                corr=corr, width=np.sqrt(np.mean(side ** 2)) / (np.sqrt(np.mean(mid ** 2)) + 1e-12),
                trans=trans, pct=pct, bcrest=crest, bwidth=width, sr=sr, dur=len(x) / sr)


def main():
    ref = stats(sys.argv[1])
    out = {}
    for tag, p in zip(sys.argv[2::2], sys.argv[3::2]):
        out[tag] = stats(p)
    out["ref"] = ref
    json.dump(out, open(sys.argv[0] + ".json", "w"), indent=1, default=float)
    names = ["ref"] + [k for k in out if k != "ref"]
    print(f"{'Metric':26}" + "".join(f"{n:>14}" for n in names))
    for k in ["lufs", "tp_approx", "rms", "crest", "plr", "lra", "corr", "width", "trans"]:
        print(f"{k:26}" + "".join(f"{out[n][k]:14.2f}" for n in names))
    for grp, key in [("% energy", "pct"), ("crest dB", "bcrest"), ("S/M width", "bwidth")]:
        for b, _, _ in BANDS:
            print(f"{grp+' '+b:26}" + "".join(f"{out[n][key][b]:14.2f}" for n in names))


if __name__ == "__main__":
    main()