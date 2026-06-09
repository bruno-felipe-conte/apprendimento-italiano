import json

# Load existing data
with open(r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Existing stories: {len(data['storie'])}")
print(f"Last story ID: {data['storie'][-1]['id']}")
print(f"Last story title: {data['storie'][-1]['titulo']}")