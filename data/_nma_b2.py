"""
Adiciona campos NMA às 5 unidades do módulo B2.
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

b2 = next(m for m in data['moduli'] if m['id'] == 'B2')

# ─── b2-i: L'italiano letterario e la tradizione culturale ───
u = next(x for x in b2['unidades'] if x['id'] == 'b2-i')
u['alerta'] = (
    "A literatura italiana não é ornamento cultural — é a fundação da própria língua. "
    "Dante, Petrarca e Boccaccio escreveram os textos que moldaram o italiano standard. "
    "Esta unidade conecta a língua viva à sua herança literária."
)
u['inventario'] = [
    "Trecento: Dante (Divina Commedia), Petrarca (Canzoniere), Boccaccio (Decameron)",
    "Figure retoriche: metafora, similitudine, allitterazione, personificazione, iperbole, ossimoro",
    "Gêneros literários: il romanzo, il racconto, la poesia, il saggio, il teatro",
    "Analisi del testo: il narratore, il protagonista, il tema, il simbolo, la struttura",
    "Congiuntivo imperfetto: credesse, avesse, fosse — in discorso indiretto e periodo ipotetico",
    "Periodo ipotetico dell'irrealtà: se fosse stato / se avesse avuto → sarebbe stato / avrebbe avuto",
    "Trapassato prossimo: aveva scritto / era partito — azione anteriore a un'altra nel passato",
    "Linguaggio letterario: arcaismi, inversioni sintattiche, costruzioni latineggianti"
]
u['definicao'] = {
    "fenomeno": (
        "Você lê no Canto I do Inferno de Dante: *'Nel mezzo del cammin di nostra vita / "
        "mi ritrovai per una selva oscura, / ché la diritta via era smarrita.'* "
        "Você entende as palavras mas sente que a linguagem é diferente do italiano moderno."
    ),
    "causa": (
        "O que é *ché* neste contexto? Por que *diritta via* em vez de *via diritta* "
        "(inversão da ordem normal)? "
        "E *era smarrita* — é passato prossimo, imperfetto ou passivo?"
    ),
    "conceito": (
        "**Ché** = arcaismo de *perché* (porque) — frequente na poesia medieval. "
        "**Inversão sintática** (adjetivo antes do substantivo) é marca do estilo literário elevado "
        "— ainda usada em poesia e prosa formal contemporânea. "
        "**Era smarrita** = trapassato prossimo passivo (era + stato + participio), "
        "indicando estado resultante de ação anterior."
    )
}
u['tecnica'] = (
    "**Como analisar um texto literário em italiano:**\n\n"
    "1. Identificar figura retorica: **metafora** (A é B) | **similitudine** (A como B) | **personificazione** (coisa age como pessoa)\n"
    "2. Trapassato: **aveva/era + participio** = ação concluída ANTES de outra ação passada\n"
    "3. Periodo ipotetico irreale (passado): **se** + congiuntivo trapassato → **condizionale passato**\n"
    "   → *se avesse studiato, avrebbe superato l'esame*\n"
    "4. Discorso indiretto al passato: disse che **era** (não è) / credeva che **fosse** (congiuntivo imp.)\n"
    "5. Para citar: *come scrive [autore], '…' (opera, anno, canto/capitolo)*"
)
u['exemplos_prc'] = [
    {
        "oracao": "Se Dante fosse vissuto oggi, avrebbe scritto un blog invece della Commedia.",
        "pergunta": "Identifique o tempo de *fosse vissuto* e *avrebbe scritto*. Que tipo de hipótese é esta?",
        "resposta": "fosse vissuto = congiuntivo trapassato; avrebbe scritto = condizionale passato. Período hipotético irreale no passado — condição impossível de se realizar",
        "conclusao": "hipótese irreale passada: se + cong. trapassato → condizionale passato"
    },
    {
        "oracao": "Petrarca diceva che l'amore fosse una dolce prigione.",
        "pergunta": "Por que *fosse* (congiuntivo imperfetto) depois de *diceva*?",
        "resposta": "discorso indiretto al passato: diceva (passato) + che → congiuntivo imperfetto na subordinada. Se fosse presente: 'dice che l'amore sia'",
        "conclusao": "discorso indiretto: tempo principale passato → congiuntivo imperfetto"
    },
    {
        "oracao": "La selva oscura è una metafora del peccato e della confusione spirituale.",
        "pergunta": "Qual é a diferença entre *metafora* e *similitudine* no contexto literário italiano?",
        "resposta": "metafora: A = B (identidade direta, sem como). similitudine: A come B (comparação explícita com 'come')",
        "conclusao": "metafora = A è B (sem 'come') | similitudine = A come B (com 'come')"
    }
]
u['ponte'] = (
    "**Em português:** 'Se Dante tivesse vivido hoje, teria escrito um blog.'\n\n"
    "**Em italiano:** *Se Dante fosse vissuto oggi, avrebbe scritto un blog* — estrutura paralela.\n\n"
    "**Diferença:** o português usa 'tivesse vivido' (pl. mais-q-perf. do subj.), "
    "o italiano usa *fosse vissuto* (congiuntivo trapassato). "
    "Ambos têm a mesma função — condição irrealizável no passado."
)
u['coda'] = (
    "Leia pelo menos os primeiros 10 versos da Divina Commedia — não para entender tudo, "
    "mas para ouvir como soa o italiano que moldou uma civilização."
)

# ─── b2-ii: Il linguaggio dei media e del giornalismo ───
u = next(x for x in b2['unidades'] if x['id'] == 'b2-ii')
u['alerta'] = (
    "O italiano jornalístico tem convenções próprias que diferem do italiano cotidiano: "
    "manchetes sem verbo, passivo onipresente, nominalizações densas. "
    "Esta unidade decodifica o código da imprensa italiana."
)
u['inventario'] = [
    "Manchetes: titoli nominali (sem verbo), verbo al presente (azione in corso), infinito (ordine/proposta)",
    "Estrutura notícia: lead (chi, cosa, quando, dove, perché) + sviluppo + conclusione",
    "Registro: formale/neutro — sem gírias, frases curtas, passivo frequente",
    "Verbos jornalísticos: affermare, dichiarare, sostenere, confermare, smentire, rivelare",
    "Nominalizações: la dichiarazione, l'approvazione, il crollo, l'aumento, la riduzione",
    "Passivo in notizie: il provvedimento è stato approvato / la legge verrà modificata",
    "Congiuntivo em discurso indireto: ha dichiarato che fosse / sostiene che sia",
    "Fonti: secondo fonti / stando a quanto dichiarato / come riportato da"
]
u['definicao'] = {
    "fenomeno": (
        "Você lê una manchete del Corriere della Sera: "
        "*'Governo: approvato il decreto. Opposizione all'attacco.'* "
        "Não há verbo principal, não há soggetto explícito — "
        "mas você entende a notícia imediatamente."
    ),
    "causa": (
        "Como um título sem verbo pode ser compreensível? "
        "Que informação está implícita? "
        "E por que *all'attacco* em vez de *attacca*?"
    ),
    "conceito": (
        "**Titoli nominali** omitem o verbo *essere* e o soggetto — "
        "o contexto (governo italiano, situação política) preenche as lacunas. "
        "São econômicos e impactantes: *Crollo dei mercati* = 'i mercati sono crollati'. "
        "**All'attacco** = locuzione prepositiva que indica posição/atitude — "
        "mais dinâmica do que o verbo simples."
    )
}
u['tecnica'] = (
    "**Como ler e escrever em estilo jornalístico italiano:**\n\n"
    "1. Titolo: **sostantivo + participio** → *Governo: approvata la legge* (concordância com oggetto)\n"
    "2. Lead: responde **Chi? Cosa? Quando? Dove? Perché?** na primeira frase\n"
    "3. Citações: **ha dichiarato che** + congiuntivo (se reportando opinião) ou + indicativo (se fato)\n"
    "4. Fonte: **secondo** + fonte | **stando a** + fonte | **come riferisce** + fonte\n"
    "5. Passivo para despersonalizar: *è stato approvato* (sem agente) vs *il Parlamento ha approvato*"
)
u['exemplos_prc'] = [
    {
        "oracao": "Il ministro ha dichiarato che la situazione fosse sotto controllo.",
        "pergunta": "Por que *fosse* (congiuntivo imperfetto) e não *era* (indicativo)?",
        "resposta": "dichiarare nel passato + che → congiuntivo. O jornalista reporta a opinião/declaração do ministro sem afirmar que é verdade — o congiuntivo marca distância da fonte",
        "conclusao": "discorso indiretto giornalistico: cong. marca distância/não-verificação pelo jornalista"
    },
    {
        "oracao": "Crollo dei mercati: persi 200 miliardi in un giorno.",
        "pergunta": "Reconstitua essa manchete como frase completa com soggetto e verbo.",
        "resposta": "I mercati sono crollati: sono stati persi 200 miliardi in un giorno. O titulo omite essere e il soggetto para impacto máximo",
        "conclusao": "titolo nominale = versão comprimida da notícia sem essere e soggetto"
    },
    {
        "oracao": "Secondo fonti governative, il provvedimento verrà modificato entro la settimana.",
        "pergunta": "Que função cumpre *secondo fonti governative* no início? E *verrà modificato*?",
        "resposta": "Secondo fonti = atribui a informação a uma fonte sem identificar — proteção jornalística. Verrà modificato = futuro passivo (verbo essere al futuro + participio)",
        "conclusao": "secondo fonti = fonte anônima | verrà + participio = futuro passivo"
    }
]
u['ponte'] = (
    "**Em português:** 'Mercados em queda: perdidos 200 bilhões' — títulos nominais existem também.\n\n"
    "**Em italiano:** *Crollo dei mercati: persi 200 miliardi* — a mesma compressão, "
    "mas com concordância do participio com o objeto (*persi* concorda com *miliardi*, masculino plural).\n\n"
    "**Armadilha:** em italiano o participio passado em construções passivas e absolutas "
    "concorda em gênero e número com o substantivo — diferente do português."
)
u['coda'] = (
    "Leia uma manchete italiana por dia — basta o título e o lead. "
    "Em três meses você decodificará o italiano jornalístico automaticamente."
)

# ─── b2-iii: Economia e mondo degli affari ───
u = next(x for x in b2['unidades'] if x['id'] == 'b2-iii')
u['alerta'] = (
    "O italiano econômico e empresarial é um subsistema linguístico preciso: "
    "cada termo tem significado técnico específico. "
    "Esta unidade equipa quem precisa ler documentos, negociar ou trabalhar "
    "em contextos de negócios italianos."
)
u['inventario'] = [
    "Macroeconomia: il PIL (Prodotto Interno Lordo), l'inflazione, la recessione, la ripresa",
    "Empresa: la sede legale, il consiglio di amministrazione, il bilancio, il fatturato, l'utile",
    "Comércio: la trattativa, il contratto, la clausola, la penale, la fideiussione",
    "Banco: il conto corrente, il fido, il mutuo, il tasso di interesse, la rata",
    "Verbo CRESCERE: è cresciuto (intransitivo) | ha aumentato (transitivo)",
    "Congiuntivo in clausole contrattuali: è previsto che / si richiede che + congiuntivo",
    "Condizionale in trattative: potremmo offrire / sarebbe possibile concordare",
    "Nominalizações densas: la ristrutturazione del debito / l'ottimizzazione dei processi"
]
u['definicao'] = {
    "fenomeno": (
        "Você lê um contratto commerciale italiano: "
        "*'Le parti si impegnano affinché vengano rispettati i termini di consegna. "
        "Qualora una delle parti non adempia agli obblighi contrattuali, "
        "sarà dovuta una penale pari al 10% del valore del contratto.'* "
        "Você entende as palavras individualmente, mas não o conjunto."
    ),
    "causa": (
        "O que é *affinché*? Por que *vengano rispettati* está no congiuntivo? "
        "E *qualora* — é uma conjunção? O que indica?"
    ),
    "conceito": (
        "**Affinché** = conjunção final que indica finalidade, sempre seguida de congiuntivo: "
        "*affinché vengano rispettati* = 'para que sejam respeitados'. "
        "**Qualora** = conjunção hipotética formal = 'no caso de que / caso', "
        "seguida de congiuntivo: *qualora non adempia* = 'caso não cumpra'. "
        "São marcadores do **registro burocratico-legale** italiano."
        )
}
u['tecnica'] = (
    "**Como ler e escrever em italiano de negócios:**\n\n"
    "1. Finalidade formal: **affinché** + congiuntivo → *affinché tutto proceda regolarmente*\n"
    "2. Hipótese formal: **qualora** + congiuntivo → *qualora non sia possibile*\n"
    "3. Congiuntivo em cláusulas: *è previsto che / si richiede che / è necessario che* + congiuntivo\n"
    "4. Negociação com condizionale: *potremmo considerare / sarebbe possibile concordare*\n"
    "5. Aumentos/quedas: *è aumentato/cresciuto* (intrans.) | *ha aumentato i prezzi* (trans.)\n"
    "   → *il fatturato è cresciuto* | *l'azienda ha aumentato il fatturato*"
)
u['exemplos_prc'] = [
    {
        "oracao": "Le parti si impegnano affinché vengano rispettati i termini.",
        "pergunta": "Por que *vengano rispettati* e não *vengono rispettati*? O que muda o modo?",
        "resposta": "affinché + congiuntivo — conjunções de finalidade sempre requerem congiuntivo. Vengono seria indicativo (fato); vengano indica finalidade/intenção",
        "conclusao": "affinché (finalidade) → congiuntivo presente"
    },
    {
        "oracao": "Qualora l'acquirente non provveda al pagamento, scatterà la penale.",
        "pergunta": "Que registro linguístico indica *qualora*? Como seria em italiano informal?",
        "resposta": "qualora = registro burocratico-legale (muito formal). Em italiano informal: 'se l'acquirente non paga, scatta la penale'",
        "conclusao": "qualora = se (apenas em contexto formal/legal/contratos)"
    },
    {
        "oracao": "Il fatturato è cresciuto del 15% rispetto all'anno scorso.",
        "pergunta": "Por que *è cresciuto* (essere) e não *ha cresciuto*? E o que é *rispetto a*?",
        "resposta": "crescere intransitivo = essere. Ha cresciuto seria erro. Rispetto a = 'em comparação com / em relação a'",
        "conclusao": "crescere intransitivo = essere | rispetto a = em comparação com"
    }
]
u['ponte'] = (
    "**Em português:** 'O faturamento cresceu 15% em comparação ao ano passado.'\n\n"
    "**Em italiano:** *Il fatturato è cresciuto del 15% rispetto all'anno scorso* — paralelo.\n\n"
    "**Diferença:** em português 'cresceu' é transitivo e intransitivo. "
    "Em italiano, *crescere* é sempre intransitivo (essere) — "
    "*ha cresciuto* é erro gramatical."
)
u['coda'] = (
    "Leia pelo menos uma seção do Sole 24 Ore (jornal econômico italiano) por semana. "
    "É o melhor treino para vocabulário econômico em contexto real."
)

# ─── b2-iv: Politica e istituzioni italiane ───
u = next(x for x in b2['unidades'] if x['id'] == 'b2-iv')
u['alerta'] = (
    "A Itália tem um dos sistemas políticos mais complexos da Europa: "
    "bicameralismo perfetto, multipartidarismo extremo, frequentes mudanças de governo. "
    "Entender as instituições é essencial para entender o noticiário e a cultura italiana."
)
u['inventario'] = [
    "Istituzioni: il Parlamento (Camera + Senato), il Governo, il Presidente della Repubblica, la Corte Costituzionale",
    "Camera dei Deputati: 400 deputati, eletti per 5 anni",
    "Senato della Repubblica: 200 senatori + senatori a vita",
    "Governo: il Presidente del Consiglio (premier), i ministri, il Consiglio dei Ministri",
    "Verbo ELEGGERE: eleggo → eletto (participio irregolare)",
    "Passivo burocratico: è stato nominato / verrà approvato / è stato promulgato",
    "Congiuntivo in discorso politico: il premier ha affermato che sia necessario / si teme che",
    "Espressioni: fiducia al governo / mozione di sfiducia / sciogliere le Camere / andare alle urne"
]
u['definicao'] = {
    "fenomeno": (
        "Você lê: *'Il Governo ha ottenuto la fiducia della Camera con 320 voti favorevoli "
        "e 180 contrari. Il Senato si pronuncierà domani.'* "
        "Você sabe o que é Camera e Senato, mas por que há duas votações?"
    ),
    "causa": (
        "O que é o *bicameralismo perfetto*? "
        "Por que a Itália precisa que Camera E Senato aprovem a mesma lei? "
        "E o que acontece se os dois votarem diferente?"
    ),
    "conceito": (
        "O **bicameralismo perfetto** italiano exige aprovação idêntica de ambas as câmaras "
        "para qualquer lei. Se o Senato modifica o testo aprovado pela Camera, "
        "volta para a Camera — processo chamado *navette*. "
        "É mais lento que o unicameralismo, mas garante maior debate. "
        "A **fiducia** é o voto de confiança que mantém o governo em exercício."
    )
}
u['tecnica'] = (
    "**Como falar sobre política italiana:**\n\n"
    "1. Processo legislativo: **proposta di legge** → Camera → Senato → promulgazione dal Presidente\n"
    "2. Crisi di governo: *il governo ha perso la fiducia* → *si va alle elezioni* ou *nuovo governo*\n"
    "3. Passivo institucional: *è stato approvato / è stato promulgato / è stato nominato*\n"
    "4. Discorso indiretto político: *il ministro ha dichiarato che* + congiuntivo (se opinião)\n"
    "5. Expressões-chave: *fiducia* (confiança) | *sfiducia* (desconfiança) | *urne* (urnas) | *seggio* (assento/vaga)"
)
u['exemplos_prc'] = [
    {
        "oracao": "La legge è stata promulgata dal Presidente della Repubblica.",
        "pergunta": "Identifique o passivo. Qual é o agente? Como seria na voz ativa?",
        "resposta": "è stata promulgata = passivo (essere + participio). Agente: dal Presidente. Voz ativa: 'Il Presidente della Repubblica ha promulgato la legge'",
        "conclusao": "passivo: essere + participio | dal + agente (pode ser omitido)"
    },
    {
        "oracao": "Si teme che il governo cada prima delle elezioni.",
        "pergunta": "Por que *cada* (congiuntivo) e não *cade* (indicativo)?",
        "resposta": "si teme che = verbo de medo/preocupação → congiuntivo. Também: si spera che, si teme che, si dubita che + congiuntivo",
        "conclusao": "si teme/spera/dubita che → congiuntivo"
    },
    {
        "oracao": "Il Presidente del Consiglio ha ricevuto l'incarico di formare il nuovo governo.",
        "pergunta": "Qual é a diferença entre *Presidente della Repubblica* e *Presidente del Consiglio*?",
        "resposta": "Presidente della Repubblica = chefe de estado (figura mais ceremonial, eleito pelo Parlamento). Presidente del Consiglio = chefe de governo (premier/primeiro-ministro, detém poder executivo)",
        "conclusao": "Presidente della Repubblica (chefe de estado) ≠ Presidente del Consiglio (premier/chefe de governo)"
    }
]
u['ponte'] = (
    "**Em português:** 'A lei foi promulgada pelo Presidente' — passivo direto.\n\n"
    "**Em italiano:** *La legge è stata promulgata dal Presidente* — estrutura idêntica.\n\n"
    "**Diferença institucional:** no Brasil o Presidente é chefe de estado E de governo. "
    "Na Itália são papéis separados: *Presidente della Repubblica* (cerimonial) "
    "e *Presidente del Consiglio* (poder executivo real)."
)
u['coda'] = (
    "A política italiana é complexa, mas o vocabulário é consistente. "
    "Acompanhe o noticiário de la Repubblica ou il Corriere — "
    "os mesmos termos repetem-se e você os interiorizará naturalmente."
)

# ─── b2-v: Cinema e arte italiana ───
u = next(x for x in b2['unidades'] if x['id'] == 'b2-v')
u['alerta'] = (
    "O cinema e a arte italiana não são apenas cultura — são janelas para o pensamento, "
    "a estética e a alma italiana. Fellini, Visconti, Pasolini, Michelangelo, Caravaggio: "
    "conhecê-los abre dimensões da língua que o estudo gramatical não alcança."
)
u['inventario'] = [
    "Neorealismo: Rossellini, De Sica, Visconti — realtà sociale, riprese in esterni, attori non professionisti",
    "Registi: Fellini (8½, La dolce vita), Antonioni, Pasolini, i fratelli Taviani",
    "Critica cinematografica: la regia, la sceneggiatura, la fotografia, il montaggio, la colonna sonora",
    "Arte rinascimentale: prospettiva, chiaroscuro, sfumato (Leonardo), manierismo",
    "Verbo GIRARE (un film): ha girato / il film è stato girato a Roma",
    "Congiuntivo in critica: si ritiene che il neorealismo sia / è considerato che abbia influenzato",
    "Superlativo assoluto letterario: bellissimo, grandiosissimo, impeccabile, magistrale",
    "Espressioni critiche: capolavoro, cult, pietra miliare, svolta stilistica, influenza duratura"
]
u['definicao'] = {
    "fenomeno": (
        "Você assiste a *Ladri di biciclette* (1948, De Sica) e nota: "
        "atores desconhecidos, ruas de Roma destruída pela guerra, câmera que segue pessoas reais. "
        "Depois assiste a *8½* (1963, Fellini) e tudo parece diferente: "
        "onírico, autobiográfico, difuso entre realidade e fantasia."
    ),
    "causa": (
        "O que define o *neorealismo* como movimento? "
        "E como o cinema de Fellini é classificado — é pós-neorealismo? Algo diferente? "
        "Que vocabulário crítico descreve essas diferenças?"
    ),
    "conceito": (
        "O **neorealismo** (1945–1952) reagiu ao cinema fascista com: "
        "riprese in esterni (filmagens externas), attori non professionisti, "
        "temi sociali (pobreza, guerra, resistenza). "
        "Fellini começou no neorealismo mas evoluiu para um cinema pessoal e onírico — "
        "chamado de **cinema d'autore**: visão única e reconhecível do regista "
        "como *autore* (autor) da obra."
    )
}
u['tecnica'] = (
    "**Como fazer crítica cinematográfica em italiano:**\n\n"
    "1. Atribuir obra: **è stato girato da** | **è diretto da** | **la regia è di** + nome\n"
    "2. Classificar: **appartiene al/alla** + movimento/genere | **è considerato un** + categoria\n"
    "3. Descrever estilo: **si caratterizza per** + caratteristica | **è noto per** + elemento\n"
    "4. Influência: **ha influenzato** | **ha segnato una svolta** | **ha aperto la strada a**\n"
    "5. Opinião crítica: **a mio avviso** | **si potrebbe affermare che** + congiuntivo | **è indubbio che** + indicativo"
)
u['exemplos_prc'] = [
    {
        "oracao": "Ladri di biciclette è considerato uno dei capolavori del neorealismo italiano.",
        "pergunta": "Por que *considerato* e não *considerato come*? E o que é *uno dei capolavori*?",
        "resposta": "considerare + aggettivo/sostantivo: sem 'come' em italiano (diferente de 'considered as' em inglês). Uno dei = 'um dos' — superlativo relativo implícito",
        "conclusao": "considerare + categoría: sem 'come' | uno dei/delle = um dos/uma das"
    },
    {
        "oracao": "Si ritiene che il neorealismo abbia rivoluzionato il linguaggio cinematografico.",
        "pergunta": "Por que *abbia rivoluzionato* (congiuntivo passato) e não *ha rivoluzionato*?",
        "resposta": "si ritiene che = verbo impessoal di opinione → congiuntivo. Abbia rivoluzionato = congiuntivo passato (ação concluída antes do momento de fala)",
        "conclusao": "si ritiene/si sostiene/si crede che → congiuntivo (anche al passato)"
    },
    {
        "oracao": "Fellini ha saputo trasformare i ricordi personali in immagini universali.",
        "pergunta": "Que valor tem *saputo* aqui? É simplesmente passato di sapere?",
        "resposta": "sapere + infinito = 'saber fazer algo' (competência/habilidade). Aqui: 'teve a habilidade de transformar'. Diferente de conoscere (conhecer) ou potere (poder)",
        "conclusao": "sapere + infinito = ter a habilidade/capacidade de fazer algo"
    }
]
u['ponte'] = (
    "**Em português:** 'Fellini soube transformar memórias pessoais em imagens universais.'\n\n"
    "**Em italiano:** *Fellini ha saputo trasformare i ricordi personali in immagini universali* — paralelo.\n\n"
    "**Diferença:** *sapere* em italiano pode significar 'saber' (conhecimento), "
    "'saber fazer' (habilidade) ou 'ter conseguido' (numa narrativa). "
    "O contexto determina qual sentido está ativo."
)
u['coda'] = (
    "Assista a pelo menos um filme do neorealismo italiano — *Ladri di biciclette*, *Roma città aperta*, "
    "ou *Umberto D.* — com legendas em italiano. "
    "É o exercício de escuta mais completo que existe para o B2."
)

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Módulo B2 atualizado com campos NMA.")
