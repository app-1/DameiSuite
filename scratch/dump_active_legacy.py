import json

with open(r"c:\Dev\DameiSuite\scratch\tr15_legacy_chain_dump.json") as f:
    data = json.load(f)

for fx in data:
    print(f"\n==================== FX {fx['fx_idx']} ====================")
    for p in fx["params"]:
        name = p.get("name", "")
        fmt = str(p.get("fmt", ""))
        val = p.get("val", 0)
        # Skip purely zero / default / empty if not informative
        if fmt != "" and fmt != "Off" and fmt != "normal" and val != 0:
            print(f"  [{p['idx']:3d}] {name:30s} = {val:10.4f}  | {fmt}")
        elif "band" in name.lower() or "gain" in name.lower() or "freq" in name.lower() or "thresh" in name.lower():
            if val != 0:
                print(f"  [{p['idx']:3d}] {name:30s} = {val:10.4f}  | {fmt}")
