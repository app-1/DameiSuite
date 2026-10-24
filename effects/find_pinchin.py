with open(r"C:\Dev\DameiSuite\effects\Damei_VocalSuite.jsfx", "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if "pinchin" in line.lower() or "producer vocal signature" in line.lower() or "apply_producer_preset" in line.lower():
            print(f"Line {idx+1}: {line.strip()}")
