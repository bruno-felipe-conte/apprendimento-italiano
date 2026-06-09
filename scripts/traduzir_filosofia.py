"""
traduzir_filosofia.py — Traduz parágrafos das histórias de filosofia (it → pt-BR)
usando a API do Claude (Haiku 4.5 — rápido e barato para tradução em lote).
"""
import json, os, time
from pathlib import Path
import anthropic

SRC = Path(__file__).parent.parent / 'data' / 'storie.json'

SYSTEM = (
    "Sei un traduttore esperto di testi filosofici italiani in portoghese brasiliano (pt-BR). "
    "Traduci fedelmente, mantenendo il tono filosofico e l'eleganza letteraria. "
    "Rispondi SOLO con la traduzione in portoghese, senza commenti, spiegazioni o virgolette."
)

def traduzir(client: anthropic.Anthropic, testo: str) -> str:
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Traduci in portoghese brasiliano:\n\n{testo}"}],
    )
    return resp.content[0].text.strip()

def main():
    client = anthropic.Anthropic()  # lê ANTHROPIC_API_KEY do ambiente
    data = json.loads(SRC.read_text(encoding="utf-8"))

    total = 0
    traduzidos = 0

    for storia in data["storie"]:
        if not storia.get("id", "").startswith("fil_"):
            continue
        for para in storia.get("testo", []):
            total += 1
            if para.get("portugues"):
                continue  # já traduzido
            italiano = para.get("italiano", "").strip()
            if not italiano:
                continue
            try:
                pt = traduzir(client, italiano)
                para["portugues"] = pt
                traduzidos += 1
                print(f"  [{traduzidos}/{total}] {storia['titulo'][:40]:40s} | {italiano[:40]}...")
                time.sleep(0.1)  # pequena pausa para não estourar rate limit
            except Exception as e:
                print(f"  ERRO: {e}")
                time.sleep(2)

    SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nConcluido: {traduzidos} paragrafos traduzidos de {total} total.")

if __name__ == "__main__":
    main()
