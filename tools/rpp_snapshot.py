"""Static snapshot of Damei FX state straight from a saved .rpp (no REAPER API needed, read-only).

  python tools/rpp_snapshot.py [path_to.rpp]
Writes tools/session_snapshots/rpp_latest.json and prints a summary.
"""
import sys, os, re, json, time

RPP = sys.argv[1] if len(sys.argv) > 1 else r"H:\HexGirls2\HexGyal\HexGyal.rpp"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "session_snapshots")
os.makedirs(OUT, exist_ok=True)

PRESET_SLIDER = {  # suite -> slider number holding the producer preset index
    "Damei_MixingSuite": 39, "Damei_OzoneSuite": 33, "Damei_GuitarSuite": 23,
    "Damei_BassSuite": 20, "Damei_DrumSuite": 25, "Damei_VocalSuite": 18,
    "Damei_SynthSuite": 15, "Damei_GullfossMaster": 12, "Damei_ToneShaper": 7,
    "Damei_AssessmentMatrix": 2, "Damei_DevastatorSuite": 2,
    "Damei_InstrumentalSuite": 2, "Damei_VocalBus": 2,
}

def tok(s):
    return s.split()

def main():
    pm = json.load(open(os.path.join(HERE, "preset_map.json"), encoding="utf-8"))
    fx_out, depth_stack = [], []
    track_name, track_idx = "MASTER/none", -1
    in_fx = None  # dict while inside <JS ...>
    got_values = False
    with open(RPP, encoding="utf-8", errors="ignore") as f:
        pending_bypass = None
        for raw in f:
            line = raw.strip()
            if line.startswith("<TRACK"):
                track_idx += 1; track_name = f"track{track_idx+1}"
            elif line.startswith("<MASTERFXCHAIN"):
                track_name = "MASTER"
            elif line.startswith("NAME ") and in_fx is None and depth_stack[-1:] == ["TRACK"]:
                track_name = line[5:].strip().strip('"')
            if line.startswith("BYPASS "):
                pending_bypass = line
            m = re.match(r'<JS\s+(\S+)', line)
            if m and "Damei" in m.group(1):
                in_fx = {"track": track_name, "file": m.group(1), "bypass": pending_bypass, "values": None}
                got_values = False
                depth_stack.append("JS"); continue
            if line.startswith("<"):
                depth_stack.append(line[1:].split()[0] if len(line) > 1 else "?")
                continue
            if line == ">":
                if depth_stack:
                    top = depth_stack.pop()
                    if top == "JS" and in_fx is not None:
                        fx_out.append(in_fx); in_fx = None
                continue
            if in_fx is not None and not got_values and line:
                in_fx["values"] = tok(line); got_values = True
    snap = {"source": RPP, "time": time.strftime("%Y-%m-%d %H:%M:%S"), "fx": fx_out}
    json.dump(snap, open(os.path.join(OUT, "rpp_latest.json"), "w"), indent=1)

    print(f"{len(fx_out)} Damei FX instances in {os.path.basename(RPP)}\n")
    canon = pm["canon_order"]
    for fx in fx_out:
        base = os.path.basename(fx["file"]).replace(".jsfx", "")
        vals = fx["values"] or []
        line = f"{fx['track']:<22} {base:<24}"
        sn = PRESET_SLIDER.get(base)
        if sn and len(vals) >= sn and vals[sn - 1] not in ("-",):
            try:
                idx = int(float(vals[sn - 1]))
                suite = pm["suites"].get(base + ".jsfx")
                cid = suite["canon"][idx] if suite and 0 <= idx < len(suite["canon"]) else "?"
                line += f" preset idx={idx:<3} -> {cid}"
            except ValueError:
                pass
        print(line)

if __name__ == "__main__":
    main()
