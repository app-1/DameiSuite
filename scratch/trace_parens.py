with open(r'effects/Damei_InstrumentalSuite.jsfx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(2259, 2405):
    l_num = idx + 1
    line = lines[idx]
    # filter out strings and comments
    code = ""
    in_s = False
    for j, c in enumerate(line):
        if c == '"' and (j == 0 or line[j-1] != '\\'):
            in_s = not in_s
        elif not in_s:
            if c == '/' and j + 1 < len(line) and line[j+1] == '/':
                break
            code += c
    o = code.count('(')
    c = code.count(')')
    if o or c:
        print(f'{l_num}: (+{o}, -{c}) {line.strip()[:60]}')
