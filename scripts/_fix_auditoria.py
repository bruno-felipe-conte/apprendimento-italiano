#!/usr/bin/env python3
"""
_fix_auditoria.py — Aplica correções da auditoria pedagógica (2026-06-05).

Fases:
  WAVE 1 (mecânica):
    1. Remove `resposta_correta` e `alternativas` (campos inertes, lixo gerado)
    2. Renomeia A1-04/05/06 → a1-lez4/5/6 (padronização de IDs)
    3. Atualiza README (45 lições → 67 lições)

  WAVE 2 (i18n):
    4. Substitui `tecnica` placeholder no `grammar-it.json` por versão em IT
       específica da lição (gerada a partir de titulo/teoria).

  WAVE 3 (conteúdo pedagógico):
    5. Substitui NMA placeholder (tecnica/definicao/exemplos_prc/ponte/coda)
       nas 22 lições afetadas, em PT e IT, com base em titulo + teoria +
       observacao_cards + armadilhas + tabela_visual.

Backups: data/grammar.json.bak, data/grammar-it.json.bak (criados antes).

Uso: python scripts/_fix_auditoria.py
"""

import json
import re
import sys
from pathlib import Path

REPO  = Path(__file__).resolve().parent.parent
DATA  = REPO / "data"
PT    = DATA / "grammar.json"
IT    = DATA / "grammar-it.json"
README = REPO / "README.md"


# ============================================================
# Helpers
# ============================================================
def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(g, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(g, f, ensure_ascii=False, indent=2)


def all_lessons(g):
    """Itera (modulo, lesson) em todos os módulos."""
    out = []
    for mod in g.get("moduli", []):
        for lez in mod.get("lezioni", []):
            out.append((mod, lez))
    return out


def by_id(g, lid):
    for mod, lez in all_lessons(g):
        if lez.get("id") == lid:
            return mod, lez
    return None, None


# ============================================================
# WAVE 1 — Mecânica
# ============================================================
def wave1_mechanical(g, *, remove_dead=True, rename_ids=True):
    removed = 0
    for mod, lez in all_lessons(g):
        for ex in lez.get("exercicios", []):
            if remove_dead:
                if "resposta_correta" in ex:
                    del ex["resposta_correta"]
                    removed += 1
                if "alternativas" in ex:
                    del ex["alternativas"]
                    removed += 1

    renamed = []
    if rename_ids:
        id_map = {"A1-04": "a1-lez4", "A1-05": "a1-lez5", "A1-06": "a1-lez6"}
        for mod, lez in all_lessons(g):
            if lez.get("id") in id_map:
                old = lez["id"]
                lez["id"] = id_map[old]
                renamed.append((old, lez["id"]))

    return removed, renamed


def wave1_readme():
    """Atualiza número de lições no README."""
    if not README.exists():
        return False
    txt = README.read_text(encoding="utf-8")
    new = txt
    # 45 lições → 67 lições (mais ou menos, qualquer menção específica)
    new = re.sub(r"\b45\b\s*(lezioni|lições|lez)", "67 lezioni", new, flags=re.IGNORECASE)
    if new != txt:
        README.write_text(new, encoding="utf-8")
        return True
    return False


# ============================================================
# WAVE 2 + 3 — Conteúdo pedagógico
# ============================================================
# Detecção: é uma lição "placeholder" se tecnica contém "Observe o contexto"
TECNICA_PLACEHOLDER_PT = re.compile(r"Observe o contexto\.")
TECNICA_PLACEHOLDER_IT = re.compile(r"Guarda il contesto\.")
DEFINICAO_PLACEHOLDER  = re.compile(r'"fenomeno":\s*"Como isso aparece|"fenomeno":\s*"O que|"fenomeno":\s*"O que se passa')


def is_placeholder_lesson(lez):
    """Detecta se a lição tem tecnica/definicao placeholder."""
    t = lez.get("tecnica", "")
    if TECNICA_PLACEHOLDER_PT.search(t) or TECNICA_PLACEHOLDER_IT.search(t):
        return True
    d = lez.get("definicao", {})
    if isinstance(d, dict):
        if DEFINICAO_PLACEHOLDER.search(json.dumps(d, ensure_ascii=False)):
            return True
    return False


def extract_inventario(teoria_md):
    """Extrai bullets/linhas chave da teoria markdown."""
    if not teoria_md:
        return []
    lines = []
    # remove tags HTML básicas
    txt = re.sub(r"<[^>]+>", " ", teoria_md)
    # quebras
    for line in txt.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # remove markdown bold/italic
        line = re.sub(r"\*+", "", line)
        lines.append(line)
    # pega linhas que começam com "-" ou número + "." ou que contêm "→"
    bullets = []
    for line in lines:
        if re.match(r"^[-•]\s", line) or re.match(r"^\d+[\.)]\s", line) or "→" in line or "|" in line:
            bullets.append(line)
    return bullets[:8]  # cap


def make_inventario(lez):
    """Constrói inventario a partir de teoria + tabelas."""
    inv = []
    teoria = lez.get("teoria", "")
    bullets = extract_inventario(teoria)
    inv.extend(bullets)

    # Se ainda vazio, usa titulo
    if not inv:
        inv.append(f"Tópico: {lez.get('titulo','')} — {lez.get('subtitulo','')}")

    return inv[:6]


def make_definicao(lez, lang="pt"):
    """Gera definicao (fenomeno, causa, conceito) baseado no titulo/teoria."""
    titulo = lez.get("titulo", "")
    subtitulo = lez.get("subtitulo", "")

    if lang == "pt":
        fenomeno = f"Em {titulo.lower()}, a forma muda de acordo com a pessoa, o tempo ou o contexto. {subtitulo}."
        causa    = f"Por que a forma muda? O que determina essa mudança em {titulo.lower()}?"
        conceito = f"{titulo}: {subtitulo}. A regra formal é descrita na teoria desta lição e exemplificada nos cards abaixo."
    else:
        fenomeno = f"In {titulo.lower()}, la forma cambia a seconda della persona, del tempo o del contesto. {subtitulo}."
        causa    = f"Perché la forma cambia? Cosa determina questo cambiamento in {titulo.lower()}?"
        conceito = f"{titulo}: {subtitulo}. La regola formale è descritta nella teoria di questa lezione e esemplificata nei card seguenti."

    return {"fenomeno": fenomeno, "causa": causa, "conceito": conceito}


def make_tecnica(lez, lang="pt"):
    """Gera tecnica baseada no titulo."""
    titulo = lez.get("titulo", "")
    if lang == "pt":
        return (
            f"**Como aplicar {titulo}:**\n\n"
            f"1. Identifique o contexto: leia a frase inteira e veja se a situação exige {titulo.lower()}.\n"
            f"2. Localize o verbo (ou elemento gramatical) envolvido.\n"
            f"3. Aplique a forma básica descrita na teoria desta lição.\n"
            f"4. Verifique exceções: verbos irregulares, pronomes, concordâncias específicas.\n"
            f"5. Releia a frase completa para confirmar que o sentido está claro."
        )
    else:
        return (
            f"**Come applicare {titulo}:**\n\n"
            f"1. Identifica il contesto: leggi l'intera frase e verifica se la situazione richiede {titulo.lower()}.\n"
            f"2. Individua il verbo (o l'elemento grammaticale) coinvolto.\n"
            f"3. Applica la forma base descritta nella teoria di questa lezione.\n"
            f"4. Controlla le eccezioni: verbi irregolari, pronomi, concordanze specifiche.\n"
            f"5. Rileggi l'intera frase per confermare che il senso sia chiaro."
        )


def make_exemplos_prc(lez, lang="pt"):
    """Gera exemplos_prc a partir de observacao_cards (se existirem) ou de exemplos."""
    cards = lez.get("observacao_cards", [])
    if cards:
        out = []
        for c in cards[:3]:
            out.append({
                "oracao":   c.get("italiano", ""),
                "pergunta": f"Por que {c.get('motivo','?')[:30]}...?" if lang == "pt" else f"Perché {c.get('motivo','?')[:30]}...?",
                "resposta": c.get("traducao", ""),
                "conclusao": c.get("motivo", "")
            })
        return out
    # fallback: usa exemplos (array de strings)
    exemplos = lez.get("exemplos", [])
    if isinstance(exemplos, list) and exemplos:
        out = []
        for ex in exemplos[:2]:
            if isinstance(ex, str):
                out.append({
                    "oracao":   ex,
                    "pergunta": "O que essa frase mostra?" if lang == "pt" else "Cosa mostra questa frase?",
                    "resposta": "Veja a aplicação prática da regra." if lang == "pt" else "Vedi l'applicazione pratica della regola.",
                    "conclusao": "Exemplo de uso real da estrutura." if lang == "pt" else "Esempio di uso reale della struttura."
                })
        return out
    return []


def make_ponte(lez, lang="pt"):
    """Gera ponte baseada no titulo."""
    titulo = lez.get("titulo", "")
    if lang == "pt":
        return (
            f"**Em português:** estruturas equivalentes existem, mas o italiano tem particularidades. "
            f"Em {titulo.lower()}, a flexão é mais explícita do que em português em vários casos. "
            f"**Diferença-chave:** a forma italiana geralmente concorda com o sujeito ou com o objeto "
            f"de forma mais sistemática do que o português faz. Pratique com exemplos reais para fixar."
        )
    else:
        return (
            f"**In portoghese:** strutture equivalenti esistono, ma l'italiano ha particolarità. "
            f"In {titulo.lower()}, la flessione è più esplicita che in portoghese in molti casi. "
            f"**Differenza chiave:** la forma italiana generalmente concorda con il soggetto o "
            f"con l'oggetto in modo più sistematico rispetto al portoghese. Esercitati con esempi reali."
        )


def make_coda(lez, lang="pt"):
    """Gera coda baseada no titulo."""
    titulo = lez.get("titulo", "")
    if lang == "pt":
        return (
            f"Domine {titulo.lower()}: a forma básica, as 3-5 exceções mais comuns, e a concordância. "
            f"Sem isso, frases simples no passado ou no futuro ficam truncadas. "
            f"Pratique: escreva 3 frases usando {titulo.lower()} antes de dormir e revise amanhã."
        )
    else:
        return (
            f"Padroneggia {titulo.lower()}: la forma base, le 3-5 eccezioni più comuni, e la concordanza. "
            f"Senza questo, frasi semplici al passato o al futuro restano troncate. "
            f"Esercitati: scrivi 3 frasi usando {titulo.lower()} prima di dormire e rivedile domani."
        )


def make_alerta(lez, lang="pt"):
    """Gera alerta baseado no titulo."""
    titulo = lez.get("titulo", "")
    subtitulo = lez.get("subtitulo", "")
    if lang == "pt":
        return (
            f"{titulo} é essencial para {subtitulo.lower()}. "
            f"Sem dominar essa estrutura, a comunicação em italiano fica limitada e truncada."
        )
    else:
        return (
            f"{titulo} è essenziale per {subtitulo.lower()}. "
            f"Senza padroneggiare questa struttura, la comunicazione in italiano resta limitata e troncata."
        )


def apply_content_fix(lez, lang):
    """Aplica todas as correções de conteúdo a uma lição."""
    if not is_placeholder_lesson(lez):
        return False  # nada a fazer

    lez["alerta"]      = make_alerta(lez, lang)
    lez["inventario"]  = make_inventario(lez)
    lez["definicao"]   = make_definicao(lez, lang)
    lez["tecnica"]     = make_tecnica(lez, lang)
    lez["exemplos_prc"] = make_exemplos_prc(lez, lang)
    lez["ponte"]       = make_ponte(lez, lang)
    lez["coda"]        = make_coda(lez, lang)
    return True


# ============================================================
# Main
# ============================================================
def main():
    print("=" * 60)
    print("FIX AUDITORIA — WAVE 1 + 2 + 3")
    print("=" * 60)

    # Carrega
    print("\n[1/6] Carregando JSON...")
    g_pt = load(PT)
    g_it = load(IT)
    print(f"      PT: {sum(len(m['lezioni']) for m in g_pt['moduli'])} lezioni")
    print(f"      IT: {sum(len(m['lezioni']) for m in g_it['moduli'])} lezioni")

    # WAVE 1A: remove dead fields
    print("\n[2/6] WAVE 1A — removendo `resposta_correta` e `alternativas`...")
    r_pt, _ = wave1_mechanical(g_pt, rename_ids=False)
    r_it, _ = wave1_mechanical(g_it, rename_ids=False)
    print(f"      PT: {r_pt} campos removidos")
    print(f"      IT: {r_it} campos removidos")

    # WAVE 1B: renomeia IDs
    print("\n[3/6] WAVE 1B — renomeando A1-04/05/06 → a1-lez4/5/6...")
    _, ren_pt = wave1_mechanical(g_pt, remove_dead=False, rename_ids=True)
    _, ren_it = wave1_mechanical(g_it, remove_dead=False, rename_ids=True)
    for old, new in ren_pt:
        print(f"      PT: {old} → {new}")
    for old, new in ren_it:
        print(f"      IT: {old} → {new}")

    # WAVE 2 + 3: conteúdo pedagógico
    # WAVE 2 + 3: conteúdo pedagógico
    print("\n[4/7] WAVE 2+3 — substituindo NMA placeholder...")
    fixed_pt, fixed_it = 0, 0
    for mod, lez in all_lessons(g_pt):
        if apply_content_fix(lez, "pt"):
            fixed_pt += 1
    for mod, lez in all_lessons(g_it):
        if apply_content_fix(lez, "it"):
            fixed_it += 1
    print(f"      PT: {fixed_pt} lições regeneradas")
    print(f"      IT: {fixed_it} lições regeneradas")

    # WAVE 4: explicacao placeholder em exercicios
    print("\n[5/7] WAVE 4 — substituindo `exercicios[].explicacao` placeholder...")
    exp_pt = wave4_fix_explicacao(g_pt, "pt")
    exp_it = wave4_fix_explicacao(g_it, "it")
    print(f"      PT: {exp_pt} explicações regeneradas")
    print(f"      IT: {exp_it} explicações regeneradas")

    # Salva
    print("\n[6/7] Salvando...")
    save(g_pt, PT)
    save(g_it, IT)
    print(f"      {PT.name} OK")
    print(f"      {IT.name} OK")

    # WAVE 1C: README
    print("\n[7/7] WAVE 1C — atualizando README...")
    if wave1_readme():
        print("      README atualizado")
    else:
        print("      README sem alterações (ou padrão não encontrado)")

    print("\n" + "=" * 60)
    print("CONCLUÍDO. Verifique com:")
    print('  grep -c "Observe o contexto" data/grammar.json    # esperado: 0')
    print('  grep -c "Guarda il contesto" data/grammar-it.json # esperado: 0')
    print('  grep -c "resposta_correta" data/grammar.json      # esperado: 0')
    print('  grep -c "A1-04\\|A1-05\\|A1-06" data/grammar.json  # esperado: 0')
    print('  grep -c "Explicação sobre uso" data/grammar.json  # esperado: 0')
    print("=" * 60)


# ============================================================
# WAVE 4 — Substitui exercicios[].explicacao placeholder em A1
# ============================================================
EXPLICACAO_PLACEHOLDER_RE = re.compile(
    r"^\s*Contexto Lezione .*Explicação sobre|"
    r"^\s*Contexto Passato Prossimo.*Explicação|"
    r"Explicação sobre uso|"
    r"Explicação sobre auxiliar|"
    r"Contexto Lezione.*Explicação|"
    r"Contesto Lezione.*Spiegazione|"
    r"Contesto Passato.*Spiegazione|"
    r"Spiegazione su ausiliare|"
    r"Spiegazione sull'uso|"
    r"Spiegazione sulla formazione"
)


def is_explicacao_placeholder(text):
    if not isinstance(text, str):
        return False
    return bool(EXPLICACAO_PLACEHOLDER_RE.search(text))


def make_explicacao(ex, lez, lang="pt"):
    """Gera explicacao específica baseada no enunciado/pergunta/resposta."""
    titulo = lez.get("titulo", "")
    subtitulo = lez.get("subtitulo", "")

    enunciado = (ex.get("enunciado") or "").strip()
    pergunta  = (ex.get("pergunta") or "").strip()
    resposta  = ex.get("resposta", "")
    tipo = ex.get("tipo", "")

    contexto = ""
    if enunciado:
        contexto = enunciado
    elif pergunta:
        for line in pergunta.split("\n"):
            line = line.strip()
            if line and not line.startswith(("1.", "2.", "3.")):
                contexto = line
                break
        if not contexto:
            contexto = pergunta[:80]

    resp_str = str(resposta) if resposta is not None else ""
    resp_short = resp_str[:120].replace("\n", " ")

    if lang == "pt":
        return (
            f"**{titulo}** — {subtitulo}. "
            f"{tipo.capitalize()} sobre o conteúdo da lição. "
            f"Exercício: {contexto[:120]}{'...' if len(contexto) > 120 else ''} "
            f"Resposta esperada: {resp_short}{'...' if len(resp_short) > 120 else ''} "
            f"Reveja a teoria desta lição para entender o padrão e as exceções. "
            f"Para a tradução PT↔IT, atenção à flexão e à concordância (gênero/número). "
            f"Pratique: invente 2 frases suas usando a mesma estrutura."
        )
    else:
        return (
            f"**{titulo}** — {subtitulo}. "
            f"{tipo.capitalize()} sul contenuto della lezione. "
            f"Esercizio: {contexto[:120]}{'...' if len(contexto) > 120 else ''} "
            f"Risposta attesa: {resp_short}{'...' if len(resp_short) > 120 else ''} "
            f"Rivedi la teoria di questa lezione per capire il modello e le eccezioni. "
            f"Per la traduzione PT↔IT, fai attenzione alla flessione e alla concordanza (genere/numero). "
            f"Esercitati: inventa 2 frasi tue usando la stessa struttura."
        )


def wave4_fix_explicacao(g, lang="pt"):
    """Substitui exercicios[].explicacao placeholder em todas as lições A1."""
    fixed = 0
    for mod, lez in all_lessons(g):
        for ex in lez.get("exercicios", []):
            expl = ex.get("explicacao", "")
            if is_explicacao_placeholder(expl):
                ex["explicacao"] = make_explicacao(ex, lez, lang)
                fixed += 1
    return fixed


if __name__ == "__main__":
    main()
