import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find "Questo e un verso" pattern
idx = content.find('Questo')
if idx >= 0:
    print('Found "Questo" at', idx)
    print(repr(content[idx-100:idx+200]))
else:
    print('"Questo" not found')

# Find Vol. pattern
idx2 = content.find('Vol. 1')
if idx2 >= 0:
    print('\nFound "Vol. 1" at', idx2)
    print(repr(content[idx2-200:idx2+400]))
else:
    print('"Vol. 1" not found')

# List data dir
print('\nData dir:')
for f in os.listdir('data'):
    size = os.path.getsize(os.path.join('data', f))
    print('  ' + f + ': ' + str(size) + ' bytes')
