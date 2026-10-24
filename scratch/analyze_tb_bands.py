import json

with open('c:/Dev/DameiSuite/scratch/tr15_legacy_chain_dump.json') as f:
    d = json.load(f)

tb = d[1]
print(f"TB Equalizer Pro Plugin: {tb['fx_name']}")

# Search all enabled bands
for i in range(1, 17):
    en = [p for p in tb['params'] if p['name'] == f'Enable{i}']
    freq = [p for p in tb['params'] if p['name'] == f'Frequency{i}']
    gain = [p for p in tb['params'] if p['name'] == f'Gain{i}']
    q = [p for p in tb['params'] if p['name'] == f'Q{i}']
    typ = [p for p in tb['params'] if p['name'] == f'Type{i}']
    order = [p for p in tb['params'] if p['name'] == f'Order{i}']
    dyn = [p for p in tb['params'] if f'Dyn{i}' in p['name'] or f'Dynamic{i}' in p['name']]
    if en and en[0]['val'] == 1:
        t_str = typ[0]['fmt'] if typ else '?'
        f_str = freq[0]['fmt'] if freq else '?'
        g_str = gain[0]['fmt'] if gain else '?'
        q_str = q[0]['fmt'] if q else '?'
        o_str = order[0]['fmt'] if order else '?'
        print(f"Band {i:2d}: Type={t_str:10s} Order={o_str:6s} Freq={f_str:8s} Hz, Gain={g_str:8s} dB, Q={q_str}")
        if dyn:
            for dp in dyn:
                if dp['val'] != 0:
                    print(f"    Dynamic param: {dp['name']} = {dp['val']} ('{dp['fmt']}')")
