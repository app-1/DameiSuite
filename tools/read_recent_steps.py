import json

with open(r'C:\Users\pityy\.gemini\antigravity-ide\brain\328c4ccd-e72c-4931-b325-85fce2a131a1\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            d = json.loads(line)
            idx = d.get('step_index', 0)
            if idx >= 900:
                tool_calls = d.get('tool_calls', [])
                if tool_calls:
                    for tc in tool_calls:
                        name = tc.get('name')
                        args = tc.get('args', {})
                        summary = args.get('toolSummary', '') or args.get('toolAction', '')
                        cmd = args.get('CommandLine', '')
                        target = args.get('TargetFile', '') or args.get('AbsolutePath', '')
                        print(f"Step {idx}: {name} -> {summary} | target: {target} | cmd: {cmd[:100]}")
        except Exception:
            pass
