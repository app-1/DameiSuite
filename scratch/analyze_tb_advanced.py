import json

with open('c:/Dev/DameiSuite/scratch/tr15_legacy_chain_dump.json') as f:
    d = json.load(f)

tb = d[1]
keywords = ['dyn', 'auto', 'sat', 'driv', 'comp', 'limit', 'clip', 'gain', 'peak', 'soft', 'analog']
matches = []
for p in tb['params']:
    for k in keywords:
        if k in p['name'].lower() and p['val'] != 0.0:
            matches.append(p)
            break

print(f"Matched {len(matches)} parameters:")
for p in matches:
    print(f"[{p['idx']}] {p['name']}: {p['val']} ('{p['fmt']}')")
