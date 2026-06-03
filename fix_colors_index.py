import os

def fix_colors(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace hardcoded colors with CSS variables to support dark mode
    content = content.replace('color: #888;', 'color: var(--cor-pietra);')
    content = content.replace('color: #2C2C2C;', 'color: var(--cor-inchiostro);')
    content = content.replace('color: #9B2335;', 'color: var(--cor-veneziano-escuro);')
    content = content.replace('color: #D4A843;', 'color: var(--cor-toscano);')
    content = content.replace('background: white;', 'background: var(--cor-marmore);')
    content = content.replace('background: #F5EDD8;', 'background: var(--cor-pergaminho);')
    content = content.replace('background: #eee;', 'background: var(--cor-marmore-escuro);')
    content = content.replace('color: #555;', 'color: var(--cor-inchiostro);')
    content = content.replace('background: #f0f0f0;', 'background: var(--cor-marmore-escuro);')
    content = content.replace('color: #333;', 'color: var(--cor-inchiostro);')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_colors('index.html')

print("Cores hardcoded substituídas por variáveis CSS no index.html.")
