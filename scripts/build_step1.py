import json

# Load existing trimmed file
with open(r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie_trimmed.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse it - it's missing the closing }] so we need to add them back temporarily
content_fixed = content + "\n  ]\n}"
data = json.loads(content_fixed)

print(f"Loaded {len(data['storie'])} stories")
# Now we'll add new stories one by one in subsequent steps
with open(r'C:\Users\bruno\Documents\italian-learning-app-pro\scripts\step1.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

print("Step 1 done")