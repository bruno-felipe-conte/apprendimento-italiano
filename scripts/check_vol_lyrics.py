import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all song objects
song_pattern = re.compile(r'"id"\s*:\s*"(can_\d+)".*?"lyrics"\s*:\s*"(.*?)"', re.DOTALL)
matches = song_pattern.findall(content)

print(f"Total songs found: {len(matches)}")

generic_songs = []
for sid, lyrics in matches:
    num = int(sid.split('_')[1])
    if 51 <= num <= 150:
        if 'Questo è un verso' in lyrics or lyrics.strip() == '' or 'placeholder' in lyrics.lower():
            generic_songs.append((sid, lyrics[:80]))

print(f"\nGeneric Vol songs (can_051-can_150): {len(generic_songs)}")
if generic_songs:
    print("\nFirst 5 samples:")
    for sid, lyr in generic_songs[:5]:
        print(f"  {sid}: {lyr}")
