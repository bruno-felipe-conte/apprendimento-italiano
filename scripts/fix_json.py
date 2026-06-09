import json

for fname in ['stories_batch2.json', 'stories_batch4.json']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    result = []
    i = 0
    in_string = False
    escape_next = False

    while i < len(content):
        c = content[i]

        if escape_next:
            result.append(c)
            escape_next = False
            i += 1
            continue

        if c == '\\':
            result.append(c)
            escape_next = True
            i += 1
            continue

        if c == '"':
            if not in_string:
                in_string = True
                result.append(c)
            else:
                # Peek ahead to see if this closes the string
                j = i + 1
                while j < len(content) and content[j] == ' ':
                    j += 1
                next_char = content[j] if j < len(content) else ''

                if next_char in (',', '}', ']', ':', '\n', '\r'):
                    in_string = False
                    result.append(c)
                else:
                    # Internal quote — escape it
                    result.append('\\"')
            i += 1
            continue

        result.append(c)
        i += 1

    fixed = ''.join(result)

    try:
        json.loads(fixed)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print(fname + ': Fixed OK')
    except json.JSONDecodeError as e:
        print(fname + f': Still error at {e.lineno}:{e.colno} - {e.msg}')
        start = max(0, e.pos - 100)
        print('Context:', repr(fixed[start:e.pos+100]))
