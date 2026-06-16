import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'\?v=\d+', '?v=67', c)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

with open('sw.js', 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'\?v=\d+', '?v=67', c)
c = re.sub(r'italiano-v\d+', 'italiano-v88', c)
with open('sw.js', 'w', encoding='utf-8') as f:
    f.write(c)
