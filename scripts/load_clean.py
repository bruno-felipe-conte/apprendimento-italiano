import json

# Read current file
with open(r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data['storie'])} stories")

# Save as clean JSON
with open(r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie_clean.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Clean JSON saved")