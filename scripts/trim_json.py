import json

# Read current file
with open(r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the closing brackets to insert new stories
content = content.rstrip()
content = content[:-2]  # Remove } and ]

with open(r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie_trimmed.json', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done trimming")