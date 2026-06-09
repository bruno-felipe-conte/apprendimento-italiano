"""
Merge script: pega arquivos new_fil_*.json em scripts/ e substitui o campo
"testo" das histórias correspondentes em data/storie.json.
"""
import json
import glob
import shutil
import os
from pathlib import Path

ROOT = Path(r"C:\Users\bruno\Documents\italian-learning-app-pro")
DATA_FILE = ROOT / "data" / "storie.json"
BACKUP_FILE = ROOT / "data" / "storie.json.bak"
SCRIPTS_DIR = ROOT / "scripts"

print("[merge] Lendo storie.json...")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    storie = json.load(f)

print(f"[merge] storie.json tem {len(storie)} histórias no nível raiz")

# Garante que storie seja uma lista (se for dict, pegar lista interna)
if isinstance(storie, dict):
    # pode ter chaves como 'storie' ou 'data'
    if "storie" in storie and isinstance(storie["storie"], list):
        storie_list = storie["storie"]
    else:
        # tentar achar a primeira lista de dicts
        storie_list = None
        for k, v in storie.items():
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict) and "id" in v[0]:
                storie_list = v
                print(f"[merge] Lista de histórias encontrada em chave '{k}'")
                break
        if storie_list is None:
            raise SystemExit("[merge] Não achei lista de histórias em storie.json")
else:
    storie_list = storie

# Acha todas as histórias fil_ atuais
fil_ids = {s["id"] for s in storie_list if s.get("id", "").startswith("fil_")}
print(f"[merge] {len(fil_ids)} histórias fil_ encontradas em storie.json: {sorted(fil_ids)[:5]}...")

# Backup
shutil.copy2(DATA_FILE, BACKUP_FILE)
print(f"[merge] Backup criado em {BACKUP_FILE}")

# Encontra arquivos new_fil_*.json
new_files = sorted(glob.glob(str(SCRIPTS_DIR / "new_fil_*.json")))
print(f"[merge] Encontrados {len(new_files)} arquivos new_fil_*.json")

# Para cada arquivo, valida estrutura e mergeia
updated = 0
skipped = 0
errors = []
for new_file in new_files:
    with open(new_file, "r", encoding="utf-8") as f:
        new_data = json.load(f)
    story_id = new_data.get("id")
    testo = new_data.get("testo")
    if not story_id or not testo:
        skipped += 1
        errors.append(f"{new_file}: sem id ou testo")
        continue
    if not isinstance(testo, list) or len(testo) != 15:
        skipped += 1
        errors.append(f"{new_file}: testo não é lista de 15 (é {type(testo).__name__}, len={len(testo) if isinstance(testo, list) else '?'})")
        continue
    # valida ids sequenciais p0..p14
    ids = [p.get("id") for p in testo]
    expected = [f"p{i}" for i in range(15)]
    if ids != expected:
        skipped += 1
        errors.append(f"{new_file}: ids não são p0..p14, são {ids[:3]}...")
        continue
    # busca na lista
    found = False
    for s in storie_list:
        if s.get("id") == story_id:
            old_len = len(s.get("testo", [])) if isinstance(s.get("testo"), list) else "?"
            s["testo"] = testo
            new_len = len(s["testo"])
            print(f"[merge] OK {story_id}: {old_len} -> {new_len} parágrafos")
            updated += 1
            found = True
            break
    if not found:
        skipped += 1
        errors.append(f"{new_file}: história '{story_id}' não encontrada em storie.json")

# Salva
print(f"[merge] Salvando storie.json...")
# Se storie era dict (envoltório), mantém a estrutura
if isinstance(storie, dict):
    # atualiza a chave correta
    for k, v in storie.items():
        if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict) and "id" in v[0]:
            storie[k] = storie_list
            break
    final_data = storie
else:
    final_data = storie_list

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"[merge] Salvo: {updated} atualizadas, {skipped} ignoradas, {updated+skipped} total")
if errors:
    print(f"[merge] ERROS/AVISOS:")
    for e in errors:
        print(f"  - {e}")

# Validação final
print("[merge] Validação final: conta histórias fil_ com 15 parágrafos...")
ok = 0
generic = 0
for s in storie_list:
    if s.get("id", "").startswith("fil_"):
        testo = s.get("testo")
        if isinstance(testo, list) and len(testo) == 15:
            ok += 1
        else:
            generic += 1
            print(f"  - {s.get('id')}: {len(testo) if isinstance(testo, list) else type(testo).__name__} parágrafos")
print(f"[merge] Resultado: {ok} histórias fil_ com 15 parágrafos, {generic} restantes")
