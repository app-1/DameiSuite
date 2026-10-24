import json

with open('c:/Dev/DameiSuite/scratch/tr15_legacy_chain_dump.json') as f:
    d = json.load(f)

for fx in d:
    print(f"=== FX {fx['fx_idx']}: {fx['fx_name']} ===")
    if fx['fx_idx'] in [0, 2, 3, 4]:
        for p in fx['params']:
            print(f"  [{p['idx']}] {p['name']}: {p['val']} ('{p['fmt']}')")
    elif fx['fx_idx'] == 1: # TB Equalizer Pro
        active_bands = []
        for p in fx['params']:
            if p['val'] != 0.0 and p['val'] != 0:
                # filter out non-zero
                active_bands.append(p)
        print(f"  Non-zero params ({len(active_bands)}):")
        for p in active_bands[:40]:
            print(f"    [{p['idx']}] {p['name']}: {p['val']} ('{p['fmt']}')")
