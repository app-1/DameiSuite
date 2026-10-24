with open(r'effects/Damei_InstrumentalSuite.jsfx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

text = "".join(lines)
p_stack = []
b_stack = []
i = 0
n = len(text)
line = 1

while i < n:
    ch = text[i]
    if ch == '\n':
        line += 1
        i += 1
    elif ch == '/' and i + 1 < n and text[i+1] == '/':
        while i < n and text[i] != '\n':
            i += 1
    elif ch == '"':
        i += 1
        while i < n:
            if text[i] == '\n': line += 1
            if text[i] == '"':
                i += 1
                break
            if text[i] == '\\' and i + 1 < n:
                i += 2
            else:
                i += 1
    elif ch == '(':
        p_stack.append((line, text[max(0, i-20):i+30].replace('\n', ' ')))
        i += 1
    elif ch == ')':
        if p_stack:
            p_stack.pop()
        else:
            print(f'Extra ) at line {line}')
        i += 1
    elif ch == '[':
        b_stack.append(line)
        i += 1
    elif ch == ']':
        if b_stack:
            b_stack.pop()
        else:
            print(f'Extra ] at line {line}')
        i += 1
    else:
        i += 1

print('Remaining unclosed parens:')
for l, snippet in p_stack:
    print(f'Line {l}: {snippet}')
