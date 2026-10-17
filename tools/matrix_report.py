"""Damei Matrix Report - stem comparison, plugin cross-check, optional perceptual layer.

python matrix_report.py [--preset 18] [--dir H:\\HexGirls2\\HexGyal\\MatrixRender] [--perceptual]

Inputs (made by Damei_MatrixRunner.lua): bus stems + master render, optional matrix_live.json.
Reference stems come from Demucs (htdemucs_ft, local weights) and are cached in H:\\REFERENCES\\_stems.
"""
import argparse, json, os, sys, re
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assess_matrix as am
import gen_fingerprints as gf

REFDIR = r"H:\REFERENCES"
BN = [b[0] for b in am.BANDS]
GROUPS = {  # HexGyal bus keyword -> demucs stem
    "drum": "drums", "bass": "bass", "vox": "vocals", "vocal": "vocals",
    "guitar": "other", "synth": "other", "cinematic": "other",
}
# which suite owns which demucs stem (for naming the gap)
OWNER = {"drums": "Drum Bus Architect", "bass": "Bass Bus Engine", "vocals": "Vocal Sovereign",
         "other": "Guitar Bus Alchemist / Synth Bus Nebula / Devastator"}
BAND_HINT = {
    "drums": ["kick sub weight", "kick/shell body (200 Hz)", "box/boxiness", "snare body", "snare crack/attack", "cymbal body", "cymbal air"],
    "bass": ["sub anchor", "bass fundamentals", "low-mid bloom", "pick/growl mids", "pick bite", "fizz", "air"],
    "vocals": ["rumble", "chest/proximity", "mud/boxy", "nasal mids", "presence", "sibilance/air lift", "air band"],
    "other": ["sub (should be thin)", "chug/low guitars", "mud", "guitar body mids", "bite/presence", "fizz/sheen", "air/sheen"],
}


def band_metrics(x, sr):
    mid, side = (x[:, 0] + x[:, 1]) / 2, (x[:, 0] - x[:, 1]) / 2
    pct, bw, tot = [], [], 0
    es = []
    for _, lo, hi in am.BANDS:
        m = am.band(mid[:, None], sr, lo, hi)[:, 0]
        s = am.band(side[:, None], sr, lo, hi)[:, 0]
        em, ess = np.mean(m ** 2), np.mean(s ** 2)
        es.append(em + ess)
        bw.append(float(np.sqrt(ess / (em + 1e-30))))
    tot = sum(es)
    pct = [100 * e / (tot + 1e-30) for e in es]
    power = float(np.mean(mid ** 2) + np.mean(side ** 2))
    peak = 20 * np.log10(np.max(np.abs(x)) + 1e-12)
    rms = 10 * np.log10(np.mean(mid ** 2) + 1e-18) if False else 10 * np.log10(np.mean(mid ** 2) + 1e-18)
    return dict(pct=pct, bw=bw, power=power, crest=float(peak - rms))


def load44(p):
    x, sr = am.load(p)
    return x, sr


def classify(folder):
    stems, master, files = {}, None, [f for f in os.listdir(folder) if f.lower().endswith((".wav", ".flac"))]
    for f in files:
        low = f.lower()
        key = next((v for k, v in GROUPS.items() if k in low), None)
        if key:
            stems.setdefault(key, []).append(os.path.join(folder, f))
        else:
            p = os.path.join(folder, f)
            if master is None or os.path.getsize(p) > os.path.getsize(master):
                master = p
    return stems, master


def sum_files(paths):
    xs = [load44(p)[0] for p in paths]
    n = max(len(x) for x in xs)
    out = np.zeros((n, 2))
    for x in xs:
        out[: len(x)] += x
    return out


def wer(ref, hyp):
    r, h = re.findall(r"[a-z']+", ref.lower()), re.findall(r"[a-z']+", hyp.lower())
    if not r:
        return float("nan")
    d = np.arange(len(h) + 1)
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev, d[j] = d[j], cur
    return d[len(h)] / len(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", type=int, default=None)
    ap.add_argument("--dir", default=r"H:\HexGirls2\HexGyal\MatrixRender")
    ap.add_argument("--perceptual", action="store_true")
    a = ap.parse_args()

    live = None
    lp = os.path.join(a.dir, "matrix_live.json")
    if os.path.exists(lp):
        live = json.load(open(lp))
    preset = a.preset if a.preset is not None else (int(live["preset"]) if live else 18)
    ref_name = gf.PRESET_REF.get(preset)
    if not ref_name:
        sys.exit(f"Preset {preset} has no single reference track; pass --preset with one that does.")
    ref_path = os.path.join(REFDIR, ref_name)
    stems, master = classify(a.dir)
    print(f"Preset {preset}  reference: {ref_name}\nMaster render: {master}\nStems: { {k: [os.path.basename(p) for p in v] for k, v in stems.items()} }\n")

    lines = ["# HexGyal Matrix Report", f"Preset **{preset}** vs `{ref_name}`", ""]
    gaps = []

    # ---------------- master vs fingerprint + plugin cross-check ----------------------
    cache = json.load(open(gf.CACHE))
    fp = cache[ref_name]
    ms = am.stats(master)
    dev = [10 * np.log10((ms["pct"][b] + 0.02) / (fp["pct"][i] + 0.02)) for i, b in enumerate(BN)]
    wdev = [ms["bwidth"][b] - fp["bw"][i] for i, b in enumerate(BN)]
    lines += ["## Master vs reference (full mix)", "", "| Band | Master % | Ref % | Dev dB | Master S/M | Ref S/M | Diff |", "|---|---|---|---|---|---|---|"]
    for i, b in enumerate(BN):
        lines.append(f"| {b} | {ms['pct'][b]:.1f} | {fp['pct'][i]:.1f} | {dev[i]:+.1f} | {ms['bwidth'][b]:.2f} | {fp['bw'][i]:.2f} | {wdev[i]:+.2f} |")
    lines += ["", f"LUFS-I {ms['lufs']:.1f} (ref {fp['lufs']:.1f}) | PLR {ms['plr']:.1f} (ref {fp['plr']:.1f}) | "
              f"Crest {ms['crest']:.1f} (ref {fp['crest']:.1f}) | LRA {ms['lra']:.1f} (ref {fp['lra']:.1f}) | Corr {ms['corr']:.2f} (ref {fp['corr']:.2f})", ""]

    if live:
        lines += ["## Plugin cross-check (Assessment Matrix JSFX vs Python on the same render)", "",
                  "| Quantity | JSFX | Python | Diff | OK? |", "|---|---|---|---|---|"]
        rows = [(f"dev dB {BN[i]}", live[f"dev{i}"], dev[i], 0.75) for i in range(7)]
        rows += [(f"width diff {BN[i]}", live[f"wdev{i}"], wdev[i], 0.08) for i in range(7)]
        rows += [("LUFS-I", live["lufs"], ms["lufs"], 0.7), ("PLR", live["plr"], ms["plr"], 0.8), ("Correlation", live["corr"], ms["corr"], 0.05)]
        bad = 0
        for n, j, p, tol in rows:
            ok = abs(j - p) <= tol
            bad += not ok
            lines.append(f"| {n} | {j:+.2f} | {p:+.2f} | {j - p:+.2f} | {'yes' if ok else '**NO**'} |")
        lines += ["", f"**{len(rows) - bad}/{len(rows)} within tolerance.**", ""]

    # ---------------- stem comparison ---------------------------------------------------
    from demucs_sep import separate
    sd = os.path.join(REFDIR, "_stems", os.path.splitext(ref_name)[0])
    print("separating reference (cached after first run)...", flush=True)
    separate(ref_path, sd)
    ref_m, mix_m = {}, {}
    for s in ("drums", "bass", "vocals", "other"):
        x, sr = load44(os.path.join(sd, f"{s}.wav"))
        ref_m[s] = band_metrics(x, sr)
        if s in stems:
            mix_m[s] = band_metrics(sum_files(stems[s]), 44100)
    rt = sum(v["power"] for v in ref_m.values())
    mt = sum(v["power"] for v in mix_m.values())
    lines += ["## Stem comparison (HexGyal bus stems vs Demucs stems of the reference)", "",
              "_Reference stems are model-separated and carry some bleed; treat <1.5 dB as noise. Bus stems are post-suite, pre-master-suite._", ""]
    for s, mm in mix_m.items():
        rm = ref_m[s]
        lvl = 10 * np.log10(mm["power"] / mt) - 10 * np.log10(rm["power"] / rt)
        lines += [f"### {s.upper()}  -  {OWNER[s]}", f"Level in mix vs ref: **{lvl:+.1f} dB** | Crest {mm['crest']:.1f} (ref {rm['crest']:.1f})", "",
                  "| Band | Stem % | Ref % | Dev dB | S/M | Ref S/M |", "|---|---|---|---|---|---|"]
        if abs(lvl) > 1.5:
            gaps.append((abs(lvl) / 1.5, f"{OWNER[s]}: stem level {lvl:+.1f} dB vs reference balance ({'turn down' if lvl > 0 else 'turn up'})"))
        for i, b in enumerate(BN):
            d = 10 * np.log10((mm["pct"][i] + 0.02) / (rm["pct"][i] + 0.02))
            wd = mm["bw"][i] - rm["bw"][i]
            lines.append(f"| {b} | {mm['pct'][i]:.1f} | {rm['pct'][i]:.1f} | {d:+.1f} | {mm['bw'][i]:.2f} | {rm['bw'][i]:.2f} |")
            tol = 2.0 if i in (0, 6) else 1.5
            if abs(d) > tol * 1.5 and rm["pct"][i] > 0.3:
                gaps.append((abs(d) / tol, f"{OWNER[s]}: {BAND_HINT[s][i]} ({b}) {d:+.1f} dB vs ref"))
            if abs(wd) > 0.30:
                gaps.append((abs(wd) / 0.2, f"{OWNER[s]}: width at {b} {wd:+.2f} S/M vs ref ({'too wide' if wd > 0 else 'too narrow'})"))
        lines.append("")
    gaps.sort(key=lambda t: -t[0])
    lines += ["## Gap list (largest first) - each names the suite responsible", ""] + [f"{i + 1}. {g}" for i, (_, g) in enumerate(gaps[:15])] + [""]

    # ---------------- perceptual layer -----------------------------------------------------
    if a.perceptual:
        lines += ["## Perceptual layer", ""]
        try:
            import torch
            from transformers import ClapModel, ClapProcessor
            dev_t = "cuda" if torch.cuda.is_available() else "cpu"
            cm = ClapModel.from_pretrained("laion/larger_clap_music").to(dev_t).eval()
            cp = ClapProcessor.from_pretrained("laion/larger_clap_music")
            import librosa

            def emb(path):
                y, _ = librosa.load(path, sr=48000, mono=True)
                chunks = [y[i:i + 480000] for i in range(0, max(len(y) - 480000, 1), 480000 * 2)][:20]
                with torch.no_grad():
                    f = cp(audios=chunks, sampling_rate=48000, return_tensors="pt").to(dev_t)
                    e = cm.get_audio_features(**f)
                e = torch.nn.functional.normalize(e, dim=-1).mean(0)
                return torch.nn.functional.normalize(e, dim=0)
            er = emb(ref_path)
            lines.append(f"- CLAP similarity master vs reference: **{float((emb(master) * er).sum()):.3f}** (1.0 = identical embedding; compare across runs, not in isolation)")
            others = [n for n in cache if n != ref_name][:4]
            base = [float((emb(os.path.join(REFDIR, n)) * er).sum()) for n in others]
            lines.append(f"- For scale: other reference tracks vs this reference average **{np.mean(base):.3f}**")
        except Exception as e:
            lines.append(f"- CLAP skipped: {e!r}")
        try:
            from transformers import pipeline
            import torch
            asr = pipeline("automatic-speech-recognition", model="openai/whisper-medium", device=0 if torch.cuda.is_available() else -1, chunk_length_s=30)
            vox = stems.get("vocals")
            if vox:
                import librosa
                def tx(p):
                    y, _ = librosa.load(p, sr=16000, mono=True)
                    return asr({"raw": y, "sampling_rate": 16000}, return_timestamps=False)["text"]
                t_vox = tx(vox[0]) if len(vox) == 1 else tx(vox[0])
                t_mix = tx(master)
                w = wer(t_vox, t_mix)
                lines.append(f"- Whisper intelligibility: vocal-stem transcript vs full-master transcript word error **{100 * w:.0f}%** (lower = lyrics cut through the mix; heavy-genre screams inflate this, so track the change between mixes)")
        except Exception as e:
            lines.append(f"- Whisper skipped: {e!r}")
        lines.append("")

    out = os.path.join(a.dir, "matrix_report.md")
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print("\n".join(lines))
    print("\nreport saved:", out)


if __name__ == "__main__":
    main()
