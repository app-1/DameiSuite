import json

with open(r'c:\Dev\DameiSuite\scratch\tr15_legacy_chain_dump.json', 'r') as f:
    data = json.load(f)

fx = data[1]
print("TB EQ Param Count:", len(fx['params']))
for p in fx['params']:
    pname = p['name']
    val = p['val']
    fmt = p['fmt']
    if any(k in pname.lower() for k in ['frequency', 'freq', 'q', 'filter', 'type', 'gain', 'enable', 'bypass', 'order', 'shape', 'bw']):
        if fmt and fmt not in ['0', 'Off', 'normal']:
            print(f"  {pname}: {val} | '{fmt}'")
