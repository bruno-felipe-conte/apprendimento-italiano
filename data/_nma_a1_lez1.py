"""
Adiciona campos NMA (método Napoleão Mendes de Almeida) à Lezione I do módulo A1.
Campos adicionados: alerta, inventario, definicao, tecnica, exemplos_prc, ponte, coda
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

a1 = next(m for m in data['moduli'] if m['id'] == 'A1')
lez1 = next(u for u in a1['unidades'] if u['id'] == 'a1-lez1')

lez1['alerta'] = (
    "Esta lição contém os três pilares de toda frase italiana: "
    "o nome com seu gênero, o artigo que o acompanha, e o adjetivo que o qualifica. "
    "Dominar estas três estruturas é a base de 80% do vocabulário cotidiano."
)

lez1['inventario'] = [
    "Nome (sostantivo): masculino (-o → -i) ou feminino (-a → -e) no plural",
    "Nome em -e: único plural possível é -i, para ambos os gêneros",
    "Artigo determinativo: il / lo / l' / la / i / gli / le",
    "Artigo indeterminativo: un / uno / una / un'",
    "Aggettivo variável em gênero e número: rosso / rossa / rossi / rosse",
    "Aggettivo variável só no número: grande → grandi",
    "Aggettivo invariável: blu, rosa, viola (não muda nunca)",
    "Verbo ESSERE: io sono / tu sei / lui-lei è / noi siamo / voi siete / loro sono",
    "C'è (há, singular) / Ci sono (há, plural)"
]

lez1['definicao'] = {
    "fenomeno": (
        "Na sua cidade você vê: *un libro* sobre a mesa, *la studentessa* estudando, "
        "*gli zaini* no chão. Cada coisa tem um nome — e esse nome vem sempre "
        "acompanhado de um artigo que muda conforme o gênero e o número do objeto."
    ),
    "causa": (
        "O que determina qual artigo usar? "
        "Qual é o plural de *il libro*? E de *lo studente*? "
        "Por que *la chiave* vira *le chiavi* mas *il padre* vira *i padri*? "
        "Quem decide essa forma?"
    ),
    "conceito": (
        "O **gênero** (masculino/feminino) e a **terminação** do nome determinam "
        "o artigo e o plural. Regra central: **-o → -i** (m.), **-a → -e** (f.), **-e → -i** (m. e f.). "
        "O artigo segue o gênero e a letra inicial da palavra seguinte."
    )
}

lez1['tecnica'] = (
    "**Como descobrir o gênero e o plural de qualquer nome:**\n\n"
    "1. Olhe a terminação: **-o** → masculino → plural **-i** | **-a** → feminino → plural **-e** | **-e** → veja o dicionário → plural **-i**\n"
    "2. Para o artigo determinativo: masculino singular com vogal → **l'** | com s+consoante, z, gn → **lo** | demais → **il**\n"
    "3. Para o artigo indeterminativo: masculino com vogal → **un** (sem apóstrofe!) | com s+cons., z → **uno** | demais → **un**\n"
    "4. Para o adjetivo: concorda em gênero e número com o nome → use a mesma lógica de terminação\n"
    "5. Para c'è / ci sono: **c'è** + singular | **ci sono** + plural"
)

lez1['exemplos_prc'] = [
    {
        "oracao": "Lo studente studia; gli studenti studiano.",
        "pergunta": "Que artigo usa *studente* no singular? E no plural? Por que *lo* e não *il*?",
        "resposta": "lo (começa com st- = s + consoante) → gli no plural",
        "conclusao": "s + consoante → lo (sg.) / gli (pl.)"
    },
    {
        "oracao": "L'ufficio è grande; gli uffici sono grandi.",
        "pergunta": "Por que o artigo é *l'* e não *il* ou *lo*? E por que o plural é *gli*?",
        "resposta": "ufficio começa com vogal (u) → l' no singular, gli no plural",
        "conclusao": "vogal → l' (sg.) / gli (pl.) para masculinos"
    },
    {
        "oracao": "Una chiave, un'ora — sono articoli indeterminativi.",
        "pergunta": "Por que *un'* tem apóstrofe e *una* não? Qual é a regra?",
        "resposta": "un' é usado antes de palavra feminina que começa com vogal",
        "conclusao": "feminino + vogal → un' | feminino + consoante → una"
    },
    {
        "oracao": "C'è un libro sul tavolo. Ci sono dei libri sul tavolo.",
        "pergunta": "Quando uso *c'è* e quando uso *ci sono*?",
        "resposta": "c'è para um único objeto (singular); ci sono para vários (plural)",
        "conclusao": "c'è + singular | ci sono + plural"
    }
]

lez1['ponte'] = (
    "**Em português:** 'o livro / os livros / a lição / as lições' — o artigo **concorda** com o nome.\n\n"
    "**Em italiano:** a mesma lógica, mas com **7 formas** de artigo determinativo (il, lo, l', la, i, gli, le) "
    "contra apenas 4 do português (o, a, os, as). A variação extra em italiano depende da **letra inicial** "
    "da palavra seguinte, não apenas do gênero.\n\n"
    "**Armadilha:** *lo* nunca existe em português — em italiano ele aparece antes de z, s+cons., gn, ps, x, y. "
    "Memorize os contextos de *lo/gli* como um bloco separado."
)

lez1['coda'] = (
    "O aluno que decorar apenas as tabelas e não treinar com exemplos reais "
    "saberá as regras mas não conseguirá usá-las. Faça os exercícios acima antes de prosseguir."
)

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Lezione I atualizada com campos NMA.")
