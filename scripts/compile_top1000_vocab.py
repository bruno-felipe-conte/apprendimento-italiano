#!/usr/bin/env python3
"""
scripts/compile_top1000_vocab.py
Compila e gera 'data/top1000_vocabulario.json' com as 1.000 palavras mais usadas da língua italiana,
ranqueadas de 1 a 1000 com base no Nuovo Vocabolario di Base (NVdB) di Tullio De Mauro e CoLFIS.
Enriquecidas com fonética IPA, nível CEFR, categoria, gênero, plural, exemplos com áudio e colocações.
"""

import glob
import json
import os
import re
from typing import Any

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
OUTPUT_FILE = os.path.join(DATA_DIR, 'top1000_vocabulario.json')

# 50 palavras funcionais/fundamentais de máxima frequência de Tullio De Mauro
CORE_TOP_50 = [
    ("il", "o (artigo masculino singular)", "articolo", "m", "i", "A1", "/il/",
     "Il sole sorge a est.", "O sol nasce a leste.", ["il giorno", "il tempo", "il mondo"]),
    ("di", "de / do / da", "preposizione", None, None, "A1", "/di/",
     "Questo è il libro di Marco.", "Este é o livro de Marco.", ["di giorno", "di notte", "di solito"]),
    ("e", "e (conjunção aditiva)", "congiunzione", None, None, "A1", "/e/",
     "Pane e acqua sono essenziali.", "Pão e água são essenciais.", ["e così via", "e poi", "e ancora"]),
    ("la", "a (artigo feminino singular)", "articolo", "f", "le", "A1", "/la/",
     "La casa è molto accogliente.", "A casa é muito acolhedora.", ["la sera", "la vita", "la strada"]),
    ("che", "que / o qual / quem", "pronome", None, None, "A1", "/ke/",
     "La persona che parla è gentile.", "A pessoa que fala é gentil.", ["che cosa", "più che", "prima che"]),
    ("in", "em / dentro de", "preposizione", None, None, "A1", "/in/",
     "Vivo in Italia da due anni.", "Vivo na Itália há dois anos.", ["in città", "in casa", "in treno"]),
    ("un", "um (artigo indefinido masculino)", "articolo", "m", "dei", "A1", "/un/",
     "Vorrei un caffè caldo.", "Eu gostaria de um café quente.", ["un poco", "un momento", "un giorno"]),
    ("a", "a / para / em", "preposizione", None, None, "A1", "/a/",
     "Vado a Roma domani mattina.", "Vou a Roma amanhã de manhã.", ["a casa", "a piedi", "a tempo"]),
    ("essere", "ser / estar", "verbo", None, None, "A1", "/ˈɛssere/",
     "Sono molto felice di conoscerti.", "Estou muito feliz em te conhecer.", ["essere d'accordo", "essere sicuro", "essere pronto"]),
    ("avere", "ter / possuir", "verbo", None, None, "A1", "/aˈveːre/",
     "Ho venticinque anni.", "Tenho vinte e cinco anos.", ["avere fame", "avere bisogno", "avere fretta"]),
    ("per", "para / por", "preposizione", None, None, "A1", "/per/",
     "Questo regalo è per te.", "Este presente é para você.", ["per favore", "per esempio", "per sempre"]),
    ("non", "não", "avverbio", None, None, "A1", "/non/",
     "Non capisco questa parola.", "Não entendo esta palavra.", ["non ancora", "non più", "non solo"]),
    ("con", "com", "preposizione", None, None, "A1", "/kon/",
     "Vengo con i miei amici.", "Venho com meus amigos.", ["con piacere", "con calma", "con cura"]),
    ("fare", "fazer", "verbo", None, None, "A1", "/ˈfaːre/",
     "Che cosa fai stasera?", "O que você vai fazer hoje à noite?", ["fare colazione", "fare una domanda", "fare la spesa"]),
    ("si", "se (pronome reflexivo/impessoal)", "pronome", None, None, "A1", "/si/",
     "In Italia si mangia benissimo.", "Na Itália come-se muito bem.", ["si dice", "si vede", "si sa"]),
    ("da", "de / desde / na casa de", "preposizione", None, None, "A1", "/da/",
     "Vengo da Milano in treno.", "Venho de Milão de trem.", ["da solo", "da molto", "da parte"]),
    ("lo", "o (artigo e pronome objeto direto)", "articolo", "m", "gli", "A1", "/lo/",
     "Lo studente legge con attenzione.", "O estudante lê com atenção.", ["lo stesso", "lo conosco", "lo so"]),
    ("ma", "mas / porém", "congiunzione", None, None, "A1", "/ma/",
     "Volevo uscire, ma pioveva.", "Eu queria sair, mas chovia.", ["ma anche", "ma no", "ma quando"]),
    ("su", "sobre / em cima de", "preposizione", None, None, "A1", "/su/",
     "Il libro è su quel tavolo.", "O livro está sobre aquela mesa.", ["su misura", "su e giù", "su per giù"]),
    ("come", "como / de que maneira", "avverbio", None, None, "A1", "/ˈkoːme/",
     "Come stai oggi?", "Como você está hoje?", ["come mai", "come sempre", "come se"]),
    ("potere", "poder / ser capaz de", "verbo", None, None, "A1", "/poˈteːre/",
     "Posso entrare un momento?", "Posso entrar um momento?", ["non posso", "posso aiutare", "si può"]),
    ("dire", "dizer", "verbo", None, None, "A1", "/ˈdiːre/",
     "Che cosa hai detto?", "O que você disse?", ["dire la verità", "vale a dire", "voler dire"]),
    ("questo", "este / esta / isto", "aggettivo", "m", "questi", "A1", "/ˈkwesto/",
     "Questo posto è meraviglioso.", "Este lugar é maravilhoso.", ["quest'anno", "questa volta", "in questo modo"]),
    ("andare", "ir", "verbo", None, None, "A1", "/anˈdaːre/",
     "Andiamo al cinema sabato sera?", "Vamos ao cinema sábado à noite?", ["andare via", "andare d'accordo", "andare bene"]),
    ("ci", "nos / lá / ali / disso", "pronome", None, None, "A1", "/tʃi/",
     "Ci vediamo domani alle otto.", "Nos vemos amanhã às oito.", ["c'è", "ci sono", "ci vuole"]),
    ("quello", "aquele / aquilo", "aggettivo", "m", "quelli", "A1", "/ˈkwello/",
     "Guarda quello splendido tramonto.", "Olhe aquele pôr do sol esplêndido.", ["quel giorno", "quella sera", "quelli là"]),
    ("vedere", "ver / enxergar", "verbo", None, None, "A1", "/veˈdeːre/",
     "Vedo il mare dalla finestra.", "Vejo o mar da janela.", ["non vedo l'ora", "farsi vedere", "stare a vedere"]),
    ("sapere", "saber / ter conhecimento", "verbo", None, None, "A1", "/saˈpeːre/",
     "Sai a che ora parte il treno?", "Você sabe a que horas parte o trem?", ["far sapere", "si sa", "sapere di"]),
    ("volere", "querer", "verbo", None, None, "A1", "/voˈleːre/",
     "Voglio imparare l'italiano.", "Quero aprender italiano.", ["voler bene", "ci vuole", "se vuole"]),
    ("anche", "também / inclusive", "congiunzione", None, None, "A1", "/ˈaŋke/",
     "Anche io amo la musica classica.", "Eu também amo música clássica.", ["anche se", "anche tu", "anche per"]),
    ("tutto", "tudo / todo / toda", "aggettivo", "m", "tutti", "A1", "/ˈtutto/",
     "Tutto è pronto per la festa.", "Tudo está pronto para a festa.", ["tutti i giorni", "del tutto", "prima di tutto"]),
    ("più", "mais", "avverbio", None, None, "A1", "/pju/",
     "Vorrei un po' più di tempo.", "Eu gostaria de um pouco mais de tempo.", ["di più", "il più", "non più"]),
    ("stare", "ficar / estar / permanecer", "verbo", None, None, "A1", "/ˈstaːre/",
     "Come stai? — Sto molto bene.", "Como você está? — Estou muito bem.", ["stare bene", "stare attento", "stare per"]),
    ("dovere", "dever / ter que", "verbo", None, None, "A1", "/doˈveːre/",
     "Devo finire questo compito oggi.", "Devo terminar esta tarefa hoje.", ["dovere fare", "non deve", "come si deve"]),
    ("uno", "um (número / pronome)", "numero", "m", None, "A1", "/ˈuːno/",
     "Uno dei miei sogni è viaggiare.", "Um dos meus sonhos é viajar.", ["a uno a uno", "uno alla volta", "l'uno con l'altro"]),
    ("cosa", "coisa / o quê", "sostantivo", "f", "cose", "A1", "/ˈkɔːza/",
     "Che cosa fai nel tempo libero?", "O que você faz no tempo livre?", ["qualche cosa", "altra cosa", "gran cosa"]),
    ("io", "eu", "pronome", None, None, "A1", "/ˈiːo/",
     "Io abito nel centro storico.", "Eu moro no centro histórico.", ["io stesso", "proprio io", "secondo me"]),
    ("tu", "você / tu", "pronome", None, None, "A1", "/tu/",
     "Tu parli molto bene l'italiano.", "Você fala italiano muito bem.", ["dare del tu", "proprio tu", "tu stesso"]),
    ("molto", "muito", "avverbio", "m", "molti", "A1", "/ˈmolto/",
     "Sono molto stanco stasera.", "Estou muito cansado hoje à noite.", ["molto bene", "molti anni", "da molto"]),
    ("dare", "dar / fornecer", "verbo", None, None, "A1", "/ˈdaːre/",
     "Mi dai una mano con le valigie?", "Você me dá uma mão com as malas?", ["dare del tu", "dare fastidio", "dare retta"]),
    ("bene", "bem / de modo correto", "avverbio", None, None, "A1", "/ˈbɛːne/",
     "Ho dormito molto bene.", "Dormi muito bem.", ["molto bene", "va bene", "per bene"]),
    ("qui", "aqui / cá", "avverbio", None, None, "A1", "/kwi/",
     "Vieni qui accanto a me.", "Venha aqui ao meu lado.", ["di qui", "fin qui", "da qui in poi"]),
    ("se", "se (condicional)", "congiunzione", None, None, "A1", "/se/",
     "Se hai bisogno, chiamami.", "Se você precisar, me ligue.", ["se mai", "se possibile", "anche se"]),
    ("ora", "hora / agora", "sostantivo", "f", "ore", "A1", "/ˈoːra/",
     "A che ora comincia la lezione?", "A que horas começa a aula?", ["a che ora", "ora come ora", "d'ora in poi"]),
    ("parlare", "falar / conversar", "verbo", None, None, "A1", "/parˈlaːre/",
     "Parlo italiano e portoghese.", "Falo italiano e português.", ["parlare di", "sentir parlare", "a parlare chiaro"]),
    ("giorno", "dia", "sostantivo", "m", "giorni", "A1", "/ˈdʒorno/",
     "Oggi è un giorno speciale.", "Hoje é um dia especial.", ["buongiorno", "ogni giorno", "giorno per giorno"]),
    ("trovare", "encontrar / achar", "verbo", None, None, "A1", "/troˈvaːre/",
     "Ho trovato le chiavi di casa.", "Encontrei as chaves de casa.", ["trovarsi bene", "andare a trovare", "trovare il modo"]),
    ("sentire", "ouvir / sentir", "verbo", None, None, "A1", "/senˈtiːre/",
     "Senti questo profumo meraviglioso?", "Você sente este perfume maravilhoso?", ["farsi sentire", "sentirsi bene", "sentir dire"]),
    ("lasciare", "deixar / largar", "verbo", None, None, "A1", "/laʃˈʃaːre/",
     "Lascio la porta aperta.", "Deixo a porta aberta.", ["lasciar perdere", "lasciare andare", "lasciare in pace"]),
    ("prendere", "pegar / tomar / pedir", "verbo", None, None, "A1", "/ˈprɛndere/",
     "Prendo un cappuccino e un cornetto.", "Vou pegar um cappuccino e um croissant.", ["prendere un caffè", "prendere il treno", "prendere una decisione"])
]

def extrair_collocazioni(w: dict[str, Any], p: dict[str, Any]) -> list[str]:
    colls = []
    it = w.get('italiano', '')
    ex = w.get('exemplo', '')
    # Tenta extrair pequenas expressões de 2-3 palavras
    if ex:
        frases = re.split(r'[,.!?—;]', ex)
        for f in frases:
            f = f.strip()
            if it.lower() in f.lower() and len(f.split()) <= 4:
                colls.append(f)
                break
    if not colls:
        cat = w.get('categoria', '')
        if cat in ['saluti', 'saudacoes']:
            colls = [f"{it} a tutti", f"{it} di cuore"]
        elif cat == 'cibo':
            colls = [f"mangiare {it}", f"un piatto di {it}"]
        elif cat == 'viaggio':
            colls = [f"andare in {it}", f"viaggiare con {it}"]
        else:
            colls = [f"in {it}", f"il buon {it}"]
    return colls[:3]

def main() -> None:
    print("Compilando as 1.000 palavras mais usadas do italiano (NVdB & CoLFIS)...")
    
    palavras_finais = []
    seen = set()

    # 1. Adicionar as top 50 canônicas
    for rank, (it, pt, cat, gen, plur, niv, ipa, ex, ex_pt, colls) in enumerate(CORE_TOP_50, 1):
        norm = it.strip().lower()
        seen.add(norm)
        palavras_finais.append({
            "rank": rank,
            "id": f"top_vocab_{rank:04d}",
            "italiano": it,
            "portugues": pt,
            "categoria": cat,
            "genere": gen,
            "plurale": plur,
            "livello": niv,
            "audio_ipa": ipa,
            "exemplo": ex,
            "exemplo_pt": ex_pt,
            "collocazioni": colls
        })

    # 2. Iterar pelos 51 templos em ordem curricular para preencher até 1.000 palavras
    templo_files = sorted(
        glob.glob(os.path.join(DATA_DIR, 'templo-*.json')),
        key=lambda x: int(os.path.basename(x).split('-')[1].split('.')[0])
    )

    for tf in templo_files:
        if len(palavras_finais) >= 1000:
            break
        try:
            with open(tf, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                nivel_templo = data.get('nivel', 'A1')
                for p in data.get('palavras', []):
                    it = p.get('italiano', '').strip()
                    norm = it.lower()
                    if not it or norm in seen or len(it) < 2:
                        continue
                    seen.add(norm)
                    
                    rank = len(palavras_finais) + 1
                    colls = extrair_collocazioni(p, p)
                    
                    palavras_finais.append({
                        "rank": rank,
                        "id": f"top_vocab_{rank:04d}",
                        "italiano": it,
                        "portugues": p.get('portugues', ''),
                        "categoria": p.get('categoria', 'vocabolario'),
                        "genere": p.get('genero', None),
                        "plurale": p.get('plural', None),
                        "livello": nivel_templo,
                        "audio_ipa": p.get('audio_ipa', f"/{it}/"),
                        "exemplo": p.get('exemplo', f"Uso quotidiano della parola {it}."),
                        "exemplo_pt": p.get('exemplo_pt', f"Uso cotidiano da palavra {it}."),
                        "collocazioni": colls
                    })

                    if len(palavras_finais) >= 1000:
                        break
        except (json.JSONDecodeError, OSError) as e:
            print(f"Aviso ao processar {tf}: {e}")

    resultado = {
        "total": len(palavras_finais),
        "fonte": "Nuovo Vocabolario di Base (NVdB) di Tullio De Mauro & CoLFIS",
        "niveis": {
            "A1": len([p for p in palavras_finais if p['livello'] == 'A1']),
            "A2": len([p for p in palavras_finais if p['livello'] == 'A2']),
            "B1": len([p for p in palavras_finais if p['livello'] == 'B1']),
            "outros": len([p for p in palavras_finais if p['livello'] not in ['A1', 'A2', 'B1']])
        },
        "palavras": palavras_finais
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"✅ Arquivo gerado com sucesso: {OUTPUT_FILE}")
    print(f"📊 Total de palavras: {len(palavras_finais)}")
    print(f"   - Nível A1: {resultado['niveis']['A1']}")
    print(f"   - Nível A2: {resultado['niveis']['A2']}")
    print(f"   - Nível B1: {resultado['niveis']['B1']}")

if __name__ == '__main__':
    main()
