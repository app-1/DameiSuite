with open(r"C:\Dev\DameiSuite\effects\Damei_VocalSuite.jsfx", "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if "slider2" in line:
            print(f"Line {idx+1}: {line.strip()}")
