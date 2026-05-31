import json, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

a1 = next(m for m in data['moduli'] if m['id'] == 'A1')
by_id = {u['id']: u for u in a1['unidades']}

# ── Lezione XI — I pronomi combinati ─────────────────────────
u = by_id['a1-lez11']
u['alerta'] = "Os pronomes combinados (direto+indireto juntos) são o maior sinal de fluência no italiano. Dominá-los transforma frases longas em expressões compactas e naturais."
u['inventario'] = [
    "Combinação: indiretto + diretto juntos: mi+lo=me lo | ti+lo=te lo | gli+lo=glielo | le+lo=glielo",
    "Tabela: mi→me, ti→te, gli/le→glie, ci→ce, vi→ve, loro→glielo (antes de lo/la/li/le/ne)",
    "Ordem: sempre indiretto antes de diretto: me lo dai (não: lo mi dai)",
    "Glielo = gli+lo | gliela = gli+la | glieli = gli+li | gliele = gli+le (vale para gli e le)",
    "Posição: igual a pronomes simples — antes do verbo | enclítico após infinitivo/gerundio/imperativo",
    "Nei tempi composti: participio concorda col pronome diretto (me l'ha data)"
]
u['definicao'] = {
    "fenomeno": "*'Puoi darmi il libro?' — 'Sì, **te lo** do subito.'* Dois pronomes numa palavra só: *te* (a te) + *lo* (il libro).",
    "causa": "Como se formam *te lo*, *me la*, *glielo*? Por que *mi* vira *me* antes de *lo*?",
    "conceito": "Quando indiretto e diretto aparecem juntos, o indiretto **muda forma** (mi→me, ti→te, ci→ce, vi→ve, gli/le→glie) e precede o diretto, formando um bloco único."
}
u['tecnica'] = (
    "**Como formar pronomes combinados:**\n\n"
    "1. Identifique os dois objetos: indiretto (a quem) + diretto (o quê)\n"
    "2. Transforme o indiretto: mi→**me** | ti→**te** | ci→**ce** | vi→**ve** | gli/le→**glie**\n"
    "3. Junte com o diretto: me+lo=**me lo** | te+la=**te la** | glie+lo=**glielo**\n"
    "4. Posição: antes do verbo conjugado | depois do infinitivo (darmelo)\n"
    "5. Tempi composti: participio concorda com lo/la/li/le: *me l'ha data* (la lettera→data)"
)
u['exemplos_prc'] = [
    {"oracao": "Puoi prestarmi il libro? — Te lo presto volentieri.", "pergunta": "Como se forma *te lo* aqui? Quais são os dois pronomes originais?", "resposta": "ti (a te, indiretto) + lo (il libro, diretto): ti→te, te+lo=te lo", "conclusao": "ti→te + lo = te lo"},
    {"oracao": "Gli ho mandato la lettera. — Gliel'ho mandata.", "pergunta": "Por que *gliel'* e não *gli la*? E por que *mandata*?", "resposta": "gli+la=gliela; antes de vocale: gliela→gliel'ho | participio concorda: lettera (f.sg) → mandata", "conclusao": "gli+la=gliela | concordanza: mandata (f.sg)"},
    {"oracao": "Vuole spiegarci la regola? — Ce la spiega?", "pergunta": "De onde vem *ce la*? Qual é o indiretto e o diretto?", "resposta": "ci (a noi, indiretto) + la (la regola, diretto): ci→ce, ce+la=ce la", "conclusao": "ci→ce + la = ce la"},
]
u['ponte'] = (
    "**Em português:** 'me dê o livro' → 'dê-me-o' (raro e formal) ou 'me dê ele' (informal).\n\n"
    "**Em italiano:** o sistema de pronomes combinados é mais sistemático e obrigatório: *me lo dai*.\n\n"
    "**Dificuldade:** *glielo* é ambíguo — pode ser 'a ele+lo', 'a ela+lo' ou 'a eles+lo'. O contexto resolve.\n\n"
    "**Prática:** o jeito mais rápido de aprender é repetir a tabela inteira como música: me lo, te lo, glielo, ce lo, ve lo, glielo."
)
u['coda'] = "Não tente deduzir os combinados na hora da fala — memorize os blocos inteiros. A tabela tem apenas 20 combinações possíveis."

# ── Lezione XII — I verbi riflessivi ─────────────────────────
u = by_id['a1-lez12']
u['alerta'] = "Os verbos reflexivos são muito mais comuns em italiano do que em português. Muitas ações cotidianas (levantar-se, vestir-se, chamar-se) são obrigatoriamente reflexivas."
u['inventario'] = [
    "Pronomi riflessivi: mi / ti / si / ci / vi / si",
    "Coniugazione: mi sveglio / ti svegli / si sveglia / ci svegliamo / vi svegliate / si svegliano",
    "Verbi riflessivi propri: lavarsi, vestirsi, alzarsi, sedersi, chiamarsi, sentirsi, annoiarsi",
    "Verbi riflessivi reciproci: conoscersi, vedersi, amarsi, salutarsi (azione reciproca tra due persone)",
    "Nei tempi composti: sempre ESSERE + participio concorda col soggetto",
    "Verbi pronominali (simil-riflessivi): accorgersi, dimenticarsi, ricordarsi, fidarsi, vergognarsi"
]
u['definicao'] = {
    "fenomeno": "*La mattina mi **sveglio** alle sette, mi **alzo**, mi **lavo** e mi **vesto**.* Quatro verbos, todos com *mi* antes.",
    "causa": "O que significa esse *mi* em cada verbo? Por que não se diz apenas *sveglio*, *alzo*, *lavo*?",
    "conceito": "O verbo reflexivo indica que o sujeito pratica e recebe a ação ao mesmo tempo (*sveglio me stesso*). O pronome reflexivo (mi/ti/si/ci/vi/si) é parte obrigatória do verbo — não pode ser omitido."
}
u['tecnica'] = (
    "**Como usar verbos reflexivos:**\n\n"
    "1. Identifique o sujeito: io/tu/lui/noi/voi/loro\n"
    "2. Escolha o pronome reflexivo correspondente: mi/ti/si/ci/vi/si\n"
    "3. Posição: **antes** do verbo conjugado (*mi sveglio*)\n"
    "4. Com infinitivo: pronome **enclítico** (lavarsi, vestirsi)\n"
    "5. Tempi composti: sempre **essere** + participio concorda col soggetto (*mi sono svegliato/a*)\n"
    "6. Imperativo: pronome enclítico (*Alzati! Siediti!*) ou separado (*Si alzi!, forma di cortesia*)"
)
u['exemplos_prc'] = [
    {"oracao": "Mi sono svegliato tardi e mi sono vestito in fretta.", "pergunta": "Por que *essere* (non *avere*)? E por que *svegliato* (non *svegliata*)?", "resposta": "Riflessivi usano sempre essere | svegliato = m.sg concordando col soggetto maschile", "conclusao": "riflessivo + essere | participio concorda col soggetto"},
    {"oracao": "Come ti chiami? — Mi chiamo Marco.", "pergunta": "O que significa *chiamarsi* aqui? É reflexivo propriu senso?", "resposta": "Chiamarsi = chamar-se (ação volta sobre si): 'io chiamo me stesso: Marco'", "conclusao": "chiamarsi = verbo riflessivo proprio (ação sobre si mesmo)"},
    {"oracao": "Marco e Maria si sono conosciuti a Roma.", "pergunta": "É reflexivo ou reciproco? *si* aqui significa o quê?", "resposta": "Reciproco: Marco conosce Maria E Maria conosce Marco → si = 'um ao outro'", "conclusao": "si recíproco = ação mútua entre dois ou mais sujeitos"},
]
u['ponte'] = (
    "**Em português:** 'eu me levanto / você se veste' — mesma estrutura reflexiva existe.\n\n"
    "**Diferença:** em italiano o uso de verbos reflexivos é **muito mais amplo**. "
    "Muitos verbos que em PT não são reflexivos, em IT são: *ricordarsi* (lembrar-se), *dimenticarsi* (esquecer-se), *fidarsi* (confiar).\n\n"
    "**Tempi composti:** em PT usamos 'ter' + participio para reflexivos ('eu me levantei' = ho/sono?). "
    "Em IT: sempre **essere**: *mi sono alzato*, nunca *ho alzato*."
)
u['coda'] = "Aprenda os verbos reflexivos cotidianos como fórmulas completas: *mi sveglio, mi alzo, mi lavo, mi vesto, mi chiamo*. Eles formam o roteiro da manhã italiana."

# ── Lezione XIII — Il condizionale semplice e composto ───────
u = by_id['a1-lez13']
u['alerta'] = "O condizionale é o tempo da cortesia, dos desejo e das hipóteses. Em italiano, pedir algo no condizionale (vorrei) é obrigatório em contextos formais — o imperativo soa rude."
u['inventario'] = [
    "Condizionale presente: radical futuro + terminações -ei/-esti/-ebbe/-emmo/-este/-ebbero",
    "Parl-are → parlerei | scriver-e → scriverei | dorm-ire → dormirei",
    "Irregolari (mesmo radical do futuro): sarei/avrei/andrei/farei/verrei/vorrei/potrei/dovrei/saprei",
    "Uso 1 — cortesia: Vorrei un caffè. Potrebbe aiutarmi?",
    "Uso 2 — desejo/preferenza: Mi piacerebbe vivere a Roma.",
    "Uso 3 — periodo ipotetico (se + imperfetto cong. → condizionale): Se avessi tempo, studierei.",
    "Condizionale composto: condizionale di avere/essere + participio (avrei mangiato, sarei andato)"
]
u['definicao'] = {
    "fenomeno": "Al bar: *'**Vorrei** un cappuccino, per favore.'* In ufficio: *'**Potresti** aiutarmi?'* Nessuno dei due dice direttamente 'voglio' o 'puoi'.",
    "causa": "Por que usar *vorrei* e não *voglio*? *Potresti* e não *puoi*? O que muda no significado?",
    "conceito": "O **condizionale** suaviza pedidos e desejos, tornando-os educados e hipotéticos. *Voglio* = quero (direto, pode soar exigente) | *vorrei* = gostaria (condicional, educado). Em contextos formais, o condizionale é a norma."
}
u['tecnica'] = (
    "**Como formar o condizionale presente:**\n\n"
    "1. Use o mesmo radical do **futuro** (já conhecido)\n"
    "2. Adicione as terminações: **-ei / -esti / -ebbe / -emmo / -este / -ebbero**\n"
    "3. Irregolari: mesmos do futuro — vorrei, sarei, avrei, andrei, farei, verrei, potrei, dovrei\n"
    "4. Para cortesia: substitua voglio→**vorrei** | posso→**potrei** | devo→**dovrei**\n"
    "5. Condizionale composto: avrei/sarei + participio (para hipóteses no passado)"
)
u['exemplos_prc'] = [
    {"oracao": "Vorrei prenotare un tavolo per due persone.", "pergunta": "Por que *vorrei* e não *voglio*? Qual é a nuance?", "resposta": "vorrei = gostaria (condizionale, educado) | voglio = quero (diretto, pode soar rude ao desconhecido)", "conclusao": "pedido formal/cortês → condizionale (vorrei, non voglio)"},
    {"oracao": "Se avessi più tempo, studierei l'italiano ogni giorno.", "pergunta": "Qual é a estrutura do periodo ipotetico aqui?", "resposta": "se + congiuntivo imperfetto (avessi) + condizionale presente (studierei)", "conclusao": "ipotesi irreale: se+congiuntivo imperfetto → condizionale"},
    {"oracao": "Avrei dovuto studiare di più per l'esame.", "pergunta": "O que significa *avrei dovuto*? É condizionale composto?", "resposta": "Sim: avrei (cond. di avere) + dovuto (participio di dovere) = 'averia deverido' = deveria ter", "conclusao": "condizionale composto: rimpianto nel passato"},
]
u['ponte'] = (
    "**Em português:** 'eu gostaria / poderia / deveria' — condicional existe e funciona igual.\n\n"
    "**Analogia direta:** vorrei=gostaria | potrei=poderia | dovrei=deveria | sarei=seria.\n\n"
    "**Periodo ipotetico:** PT 'se eu tivesse tempo, estudaria' = IT 'se avessi tempo, studierei' — estrutura idêntica.\n\n"
    "**Diferença prática:** em italiano o condizionale é mais exigido em contextos formais (bar, restaurante, loja) do que em português, onde o presente é mais aceito."
)
u['coda'] = "Use *vorrei* toda vez que pedir algo a um desconhecido. É o sinal mais imediato de educação no italiano cotidiano."

# ── Lezione XIV — I pronomi relativi e interrogativi ─────────
u = by_id['a1-lez14']
u['alerta'] = "Os pronomes relativos conectam orações e evitam repetições. Sem eles, você é forçado a fazer frases curtas e desconexas. Com eles, seu italiano ganha coesão e elegância."
u['inventario'] = [
    "Che: substitui soggetto ou oggetto diretto (invariável): Il libro che leggo è interessante.",
    "Cui: substitui complemento preposizionale: Il professore con cui studio è bravo.",
    "Il quale/la quale/i quali/le quali: alternativa a che/cui, concordando em gênero e número",
    "Chi: 'quem' (pronome relativo+antecedente insieme): Chi studia, impara.",
    "Interrogativi: chi? (quem) | che cosa? / cosa? / che? (o quê?) | quale/i? (qual/quais?) | quanto/a/i/e? (quanto?)",
    "Quanto come esclamativo: Quanto sei bravo! / Quante persone!"
]
u['definicao'] = {
    "fenomeno": "*Il libro **che** ho comprato ieri è fantastico. Il professore **con cui** studio è molto bravo.* Duas orações ligadas por um pronome relativo.",
    "causa": "Por que *che* numa frase e *cui* na outra? Quando usar cada um?",
    "conceito": "**Che** substitui sujeito ou objeto direto (sem preposição). **Cui** substitui qualquer complemento **com preposição** (con cui, a cui, di cui, in cui). A escolha depende da função sintática do pronome na oração relativa."
}
u['tecnica'] = (
    "**Como escolher o pronome relativo:**\n\n"
    "1. O pronome substitui sujeito ou objeto direto? → **che**\n"
    "2. O pronome substitui um complemento com preposição? → prep. + **cui**\n"
    "3. Quer ser mais formal ou eliminar ambiguidade? → **il quale / la quale / i quali / le quali**\n"
    "4. Para perguntar: pessoa → **chi**? | coisa → **che cosa / cosa**? | escolha → **quale/i**?\n"
    "5. Che pode ser sia relativo ('o livro que li') sia interrogativo ('o que você quer?')"
)
u['exemplos_prc'] = [
    {"oracao": "La ragazza che ho incontrato ieri si chiama Sofia.", "pergunta": "Por que *che* e não *cui*? Qual é a função de *che* aqui?", "resposta": "che = oggetto diretto di 'incontrato' (ho incontrato la ragazza) → che (sem preposição)", "conclusao": "oggetto diretto → che"},
    {"oracao": "Il paese in cui sono nato è piccolo.", "pergunta": "Por que *in cui* e não *che*?", "resposta": "sono nato IN un paese → a preposição 'in' é obrigatória → in+cui (não se pode dizer 'in che')", "conclusao": "complemento com preposição → prep.+cui"},
    {"oracao": "Chi non risica, non rosica.", "pergunta": "Que tipo de pronome é *chi* aqui? Tem antecedente?", "resposta": "Chi = pronome relativo-indefinito sem antecedente explícito = 'colui che' (quem/aquele que)", "conclusao": "chi sem antecedente = 'quem/aquele que' (generalização)"},
]
u['ponte'] = (
    "**Em português:** 'o livro que li' = *il libro che ho letto* | 'o professor com quem estudo' = *il professore con cui studio*.\n\n"
    "**Diferença:** em PT 'com quem' usa 'quem' (relativo de pessoa). Em IT, tanto pessoa quanto coisa usam **cui** com preposição.\n\n"
    "**Armadilha:** *che* é invariável — não muda para concordar com o antecedente, diferente do PT 'o qual/a qual'."
)
u['coda'] = "Pratique construir uma frase com *che* e uma com *cui* sobre qualquer tema. A fluência nas relativas eleva imediatamente seu nível percebido."

# ── Lezione XV — Il comparativo e il superlativo ─────────────
u = by_id['a1-lez15']
u['alerta'] = "Comparativos e superlativos permitem avaliar, classificar e exagerar — são essenciais para qualquer conversa que vá além do básico."
u['inventario'] = [
    "Comparativo di maggioranza: più + agg. + di/che (Marco è più alto di Luca.)",
    "Comparativo di minoranza: meno + agg. + di/che",
    "Comparativo di uguaglianza: (così) + agg. + come / (tanto) + agg. + quanto",
    "Uso di 'di' vs 'che': di = confronto fra due sostantivi | che = confronto fra due aggettivi/verbi/avverbi",
    "Superlativo relativo: il/la/i/le più + agg. (+ di/tra): È il più bello della classe.",
    "Superlativo assoluto: agg. + -issimo/a/i/e: bellissimo | oppure: molto + agg.: molto bello",
    "Forme irregolari: buono→migliore/ottimo | cattivo→peggiore/pessimo | grande→maggiore/massimo | piccolo→minore/minimo"
]
u['definicao'] = {
    "fenomeno": "*Marco è **più alto** di Luca. Sofia è **la più intelligente** della classe. Questo caffè è **buonissimo**!* Três graus diferentes do adjetivo.",
    "causa": "Como se formam *più alto*, *la più intelligente* e *buonissimo*? Quando usar *di* vs *che* depois do comparativo?",
    "conceito": "Os graus do adjetivo indicam intensidade relativa (comparativo) ou absoluta (superlativo). **Di** compara dois **substantivos/pronomes** entre si. **Che** compara dois **adjetivos, verbos ou advérbios** referentes ao mesmo sujeito."
}
u['tecnica'] = (
    "**Como formar comparativos e superlativos:**\n\n"
    "1. Comparativo: **più/meno/così** + adjetivo + **di/che**\n"
    "2. Di ou che? Se compara dois *nomes*: **di** | Se compara duas *qualidades* ou *ações* do mesmo sujeito: **che**\n"
    "3. Superlativo relativo: artigo + **più/meno** + adjetivo (+ *di/tra* + grupo de referência)\n"
    "4. Superlativo assoluto: adjetivo + **-issimo** (retira a vogal final: bello→bell+issimo)\n"
    "5. Irregolari: buono→**migliore** (comp.) / **ottimo** (superl.) | cattivo→**peggiore/pessimo**"
)
u['exemplos_prc'] = [
    {"oracao": "Roma è più grande di Firenze.", "pergunta": "Por que *di* e não *che* aqui?", "resposta": "Compara dois substantivos (Roma vs Firenze) → di", "conclusao": "comparação entre dois nomes → di"},
    {"oracao": "È più facile studiare che lavorare.", "pergunta": "Por que *che* aqui e não *di*?", "resposta": "Compara duas ações (studiare vs lavorare), mesmo sujeito implícito → che", "conclusao": "comparação entre ações/qualidades → che"},
    {"oracao": "Questo è il miglior ristorante della città.", "pergunta": "Por que *miglior* e não *il più buono*?", "resposta": "migliore/miglior é a forma irregolare di 'più buono' — entrambe são corrette", "conclusao": "buono→migliore (irregolare) = più buono (regolare)"},
]
u['ponte'] = (
    "**Em português:** 'mais alto do que' = *più alto di/che* — mesma estrutura.\n\n"
    "**Di vs che:** em PT 'do que' é sempre usado. Em IT a escolha entre *di* e *che* é **obrigatória** e depende do que se compara.\n\n"
    "**Superlativo absoluto:** -issimo é uma terminação latina viva no italiano. Em PT equivale a 'belíssimo/ótimo/péssimo'.\n\n"
    "**Irregolari:** migliore/ottimo/peggiore/pessimo são herdados do latim e não seguem a regra -issimo."
)
u['coda'] = "Memorize os quatro irregolari (migliore, ottimo, peggiore, pessimo) hoje — são os mais usados em qualquer avaliação."

# ── Lezione XVI — Il passato remoto ──────────────────────────
u = by_id['a1-lez16']
u['alerta'] = "O passato remoto é usado no sul da Itália e na língua escrita para eventos distantes no tempo. Ao ler literatura ou documentos históricos, você o encontrará em cada página."
u['inventario'] = [
    "Formazione -ARE: parlai / parlasti / parlò / parlammo / parlaste / parlarono",
    "Formazione -ERE: scrissi / scrivesti / scrisse / scrivemmo / scriveste / scrissero (irregolare)",
    "Formazione -IRE: dormii / dormisti / dormì / dormimmo / dormiste / dormirono",
    "Molti -ERE sono irregolari: vedere→vidi | leggere→lessi | rispondere→risposi | mettere→misi",
    "Essere: fui/fosti/fu/fummo/foste/furono | Avere: ebbi/avesti/ebbe/avemmo/aveste/ebbero",
    "Uso geografico: nord Italia → passato prossimo | sud Italia + Toscana → passato remoto",
    "Nella scrittura: sempre passato remoto per fatti storici lontani"
]
u['definicao'] = {
    "fenomeno": "*Dante **nacque** a Firenze nel 1265. Napoleone **morì** nel 1821.* Eventos históricos usam sempre esse tempo.",
    "causa": "Por que *nacque* e não *è nato* para Dante? Qual é a diferença entre passato remoto e passato prossimo?",
    "conceito": "O **passato remoto** indica ações **definitivamente concluídas** no passado, sem ligação com o presente. É obrigatório na escrita histórica e literária. Na fala, o Norte usa o passato prossimo mesmo para eventos remotos; o Sul usa o passato remoto para tudo."
}
u['tecnica'] = (
    "**Como usar e formar o passato remoto:**\n\n"
    "1. Na **escrita** (história, literatura, narrativa): use passato remoto\n"
    "2. Na **fala**: depende da região — Norte → passato prossimo | Sul/Toscana → passato remoto\n"
    "3. Verbos regulares: radical + terminações (-ai/-asti/-ò/-ammo/-aste/-arono para -are)\n"
    "4. Verbos irregolari em -ere: muitos têm forma especial — memorize: vidi, lessi, scrissi, misi, presi, chiesi\n"
    "5. Essere: **fui** (forma única — diferente do presente sono e do passato prossimo è stato)"
)
u['exemplos_prc'] = [
    {"oracao": "Garibaldi nacque a Nizza nel 1807 e morì a Caprera nel 1882.", "pergunta": "Por que passato remoto aqui e não passato prossimo?", "resposta": "Fatos históricos distantes, sem ligação com o presente → passato remoto obrigatório na escrita", "conclusao": "fato histórico distante → passato remoto (escrita)"},
    {"oracao": "Dante scrisse la Divina Commedia tra il 1308 e il 1320.", "pergunta": "Como se forma *scrisse*? É regular?", "resposta": "scrivere é irregular: scriv- → scrissi/scrivesti/scrisse/scrivemmo/scriveste/scrissero", "conclusao": "scrivere: scrivo→scrissi (irregolare del p.remoto)"},
    {"oracao": "Quando vidi Marco, capii subito che c'era un problema.", "pergunta": "Dois passati remoti numa frase: *vidi* e *capii*. Como se formam?", "resposta": "vedere irregolare: vidi | capire regular tipo 2: capii (io capii, non capiscii)", "conclusao": "vedere→vidi (irr.) | capire→capii (reg.)"},
]
u['ponte'] = (
    "**Em português:** o pretérito perfeito simples ('falei, comi, parti') corresponde ao passato remoto.\n\n"
    "**Diferença principal:** em IT o passato remoto e o passato prossimo têm distribuição geográfica e de registro. Em PT há apenas um tempo para isso (a distinção PT perfeito simples vs composto é diferente).\n\n"
    "**Para leitura:** memorize as formas irregolari mais comuns — vidi, lessi, scrissi, fui, ebbi, venne, disse — você as encontrará em qualquer texto literário."
)
u['coda'] = "Não use o passato remoto na fala cotidiana se você está no Norte da Itália — soará artificial. Mas leia-o e reconheça-o para compreender qualquer texto literário."

# ── Lezione XVII — Il trapassato prossimo ────────────────────
u = by_id['a1-lez17']
u['alerta'] = "O trapassato prossimo é o tempo do 'antes do passado'. Sem ele, você não consegue narrar sequências de eventos passados com precisão temporal."
u['inventario'] = [
    "Formazione: imperfetto di avere/essere + participio passato",
    "Con avere: avevo/avevi/aveva/avevamo/avevate/avevano + participio",
    "Con essere: ero/eri/era/eravamo/eravate/erano + participio (concordanza col soggetto)",
    "Uso principale: azione passata ANTERIORE a un'altra azione passata",
    "Segnali temporali: dopo che, quando, appena, già, non ancora",
    "Equivale al: 'tinha feito / havia dito / tinha chegado' em português"
]
u['definicao'] = {
    "fenomeno": "*Quando sono arrivato, Marco **era già partito**.* Dois eventos passados: chegar e partir. Partir aconteceu **antes** de chegar.",
    "causa": "Como indicar que uma ação passada aconteceu **antes** de outra ação passada? O passato prossimo não resolve isso?",
    "conceito": "O **trapassato prossimo** indica uma ação **anterior a outro momento passado**. É o 'passado do passado': quando você narra dois eventos passados em sequência, o anterior vai no trapassato."
}
u['tecnica'] = (
    "**Como usar o trapassato prossimo:**\n\n"
    "1. Identifique duas ações passadas: qual aconteceu **primeiro**?\n"
    "2. A ação mais **antiga** vai no trapassato | a mais recente vai no passato prossimo ou imperfetto\n"
    "3. Forme com: **aveva/era** (imperfetto di avere/essere) + participio\n"
    "4. Com essere: participio concorda com o sujeito\n"
    "5. Segnali que pedem trapassato: *dopo che, quando, appena, già, non ancora, perché*"
)
u['exemplos_prc'] = [
    {"oracao": "Quando sono arrivato al cinema, il film era già iniziato.", "pergunta": "Por que *era già iniziato* (trapassato) e *sono arrivato* (p.prossimo)?", "resposta": "Il film iniziò PRIMA che io arrivassi → film = trapassato | arrivo = p.prossimo", "conclusao": "evento anterior → trapassato | evento posterior → p.prossimo"},
    {"oracao": "Non avevo mai mangiato il sushi prima di quel giorno.", "pergunta": "Por que trapassato aqui? Qual é o 'outro momento passado' de referimento?", "resposta": "'quel giorno' é o ponto de referência no passado; 'mai mangiato' é ainda mais remoto → trapassato", "conclusao": "mai+trapassato = experiência nunca vivida até um momento passado"},
    {"oracao": "Siamo usciti dopo che aveva finito di piovere.", "pergunta": "Por que *aveva finito* (trapassato) e *siamo usciti* (p.prossimo)?", "resposta": "A chuva terminou ANTES de sairmos: piovere finì → trapassato | uscita → p.prossimo", "conclusao": "dopo che + trapassato (azione precedente)"},
]
u['ponte'] = (
    "**Em português:** 'tinha feito / havia chegado / tinha comido' — o pretérito mais-que-perfeito composto.\n\n"
    "**Analogia direta:** avevo mangiato = tinha comido | ero andato = tinha ido.\n\n"
    "**Diferença:** em PT o mais-que-perfeito simples ('fizera, comera') existe mas é raro. Em IT o trapassato prossimo é a única forma padrão para esse sentido."
)
u['coda'] = "O trapassato é simples de formar mas difícil de lembrar de usar. Toda vez que narrar dois eventos passados, pergunte: qual aconteceu primeiro? Esse vai no trapassato."

# ── Lezione XVIII — Le preposizioni (avanzato) ───────────────
u = by_id['a1-lez18']
u['alerta'] = "As preposições italianas são o maior obstáculo para falar com naturalidade. Não há regra universal — cada verbo e cada expressão pede a sua. Memorize os blocos, não as regras abstratas."
u['inventario'] = [
    "A: localização em cidades (vivo a Roma), hora (alle tre), movimento para cidade (vado a Napoli)",
    "In: países/regiões/continentes (in Italia, in Europa), meios de transporte (in treno, in auto), locais (in ufficio, in cucina)",
    "Da: origem (vengo da Milano), tempo desde (studio italiano da due anni), característica (una ragazza dai capelli rossi)",
    "Di: posse (il libro di Marco), matéria (una borsa di pelle), argomento (parlo di sport)",
    "Per: scopo (studio per imparare), durata (parto per tre giorni), destinatario (un regalo per te)",
    "Su: posizione (sul tavolo), argomento (un libro sul cinema), età approssimativa (ha sui trent'anni)",
    "Tra/Fra: posizione fra due cose (tra me e te), tempo futuro (arrivo fra cinque minuti)"
]
u['definicao'] = {
    "fenomeno": "*Vivo **a** Roma ma lavoro **in** un'azienda **di** Milano. Vengo **da** Napoli e studio **per** migliorare.* Cinco preposições diferentes numa única frase.",
    "causa": "Por que *a* Roma mas *in* Italia? Por que *di* Milano mas *a* Milano? A mesma preposição serve para tudo?",
    "conceito": "Cada preposição italiana tem **usos específicos** que não seguem sempre a lógica do português. A distribuição *a/in* para lugar, *da* para origem/duração, *di* para posse são padrões que precisam ser memorizados como blocos de uso."
}
u['tecnica'] = (
    "**Guia rápido de escolha:**\n\n"
    "- Cidade onde mora/vai: **a** (vivo a Roma | vado a Milano)\n"
    "- País/região/continente: **in** (in Italia | in Europa | in Toscana)\n"
    "- Origem: **da** (vengo da Roma | sono di Roma)\n"
    "- Posse/argomento: **di** (il libro di Marco | parlo di sport)\n"
    "- Meio de transporte: **in** (in treno/auto/aereo) ou **a** (a piedi, a cavallo)\n"
    "- Finalidade: **per** (studio per imparare)\n"
    "- Localização sopra: **su** → contrai (sul tavolo, sulla sedia)"
)
u['exemplos_prc'] = [
    {"oracao": "Abito a Firenze ma lavoro in Toscana.", "pergunta": "Por que *a* Firenze mas *in* Toscana?", "resposta": "Cidade → a | Região/país → in (regola fondamentale)", "conclusao": "città → a | regione/paese → in"},
    {"oracao": "Studio l'italiano da tre anni.", "pergunta": "O que significa *da* aqui? É origem ou duração?", "resposta": "Da + durata = ação que começou no passado e continua: 'há três anos que estudo' (presente em IT)", "conclusao": "da + durata = ação em curso desde o passado (não passato)"},
    {"oracao": "Ho comprato un regalo per mia madre.", "pergunta": "Poderia ser *a* mia madre em vez de *per*? Qual a diferença?", "resposta": "per = destinatário do presente | a = dar diretamente (ho dato un regalo a mia madre)", "conclusao": "per = 'para/destinado a' | a = 'para (ação direta de dar)'"},
]
u['ponte'] = (
    "**Armadilhas a/in/da:**\n"
    "- PT 'em Roma' → IT *a Roma* (cidade) | PT 'na Itália' → IT *in Italia* (país)\n"
    "- PT 'faz dois anos' → IT *da due anni* (com presente, não passato!)\n"
    "- PT 'de Pedro' → IT *di Pietro* (posse) | PT 'da/de Roma' → IT *da Roma* (origine)\n\n"
    "**Dica:** muitos verbos italianos têm a preposição 'embutida' no significado — aprenda sempre o verbo com sua preposição: *parlare di*, *pensare a*, *dipendere da*, *credere in*."
)
u['coda'] = "Não tente descobrir a preposição por lógica — aprenda os blocos fixos: *a piedi, in treno, da tre anni, di pelle, per favore*. A intuição vem com a exposição."

# ── Lezione XIX — La concordanza dei tempi ───────────────────
u = by_id['a1-lez19']
u['alerta'] = "A concordância dos tempos é o que permite narrar com precisão. Errar a sequência temporal torna a frase ambígua ou incorreta, mesmo que o vocabulário esteja certo."
u['inventario'] = [
    "Presente → subordinata: presente (so che parli italiano) ou futuro (credo che verrà)",
    "Passato → subordinata: imperfetto para contemporâneo (sapevo che studiava) ou trapassato para anterior (sapevo che aveva studiato)",
    "Futuro → subordinata: futuro (penso che partirà) ou presente (quando arrivi, chiama)",
    "Dopo che + trapassato prossimo (azione anteriore): dopo che aveva mangiato, uscì",
    "Prima di + infinitivo (stesso soggetto): prima di partire, ha chiamato",
    "Quando + futuro (riferimento futuro): quando arriverò, ti chiamerò"
]
u['definicao'] = {
    "fenomeno": "*Sapevo che Marco **studiava** ogni giorno.* vs *Sapevo che Marco **aveva studiato** tutta la notte.* Mesmo verbo principale, tempos diferentes na subordinata.",
    "causa": "Por que *studiava* numa frase e *aveva studiato* na outra? O que muda?",
    "conceito": "A **concordância dos tempos** alinha o tempo da oração subordinada com o da principal. Ação **simultânea** ao passado → imperfetto. Ação **anterior** ao passado → trapassato prossimo."
}
u['tecnica'] = (
    "**Regras de concordância:**\n\n"
    "1. Verbo principal no **presente**: subordinata pode usar qualquer tempo lógico\n"
    "2. Verbo principal no **passato**: subordinata usa —\n"
    "   - Ação simultânea: **imperfetto** (*sapevo che parlava*)\n"
    "   - Ação anterior: **trapassato** (*sapevo che aveva parlato*)\n"
    "   - Ação posterior: **condizionale** (*sapevo che sarebbe venuto*)\n"
    "3. **Dopo che** sempre + trapassato (a ação 'depois' é a mais recente)\n"
    "4. **Quando** + referência futura → futuro (não presente como em PT)"
)
u['exemplos_prc'] = [
    {"oracao": "Credevo che tu fossi stanco. / Credo che tu sia stanco.", "pergunta": "Por que *fossi* (passato) mas *sia* (presente) do congiuntivo?", "resposta": "credevo (passato) → concordanza: fossi (imperfetto cong.) | credo (presente) → sia (presente cong.)", "conclusao": "principal no passato → subordinata no passato (concordanza)"},
    {"oracao": "Quando sarò a Roma, ti chiamerò.", "pergunta": "Por que *sarò* (futuro) e não *sono* (presente) depois de 'quando'?", "resposta": "Em italiano, 'quando' com referência futura exige futuro (≠ português que usa presente)", "conclusao": "quando + futuro (regola IT ≠ PT)"},
    {"oracao": "Dopo che aveva finito il lavoro, Marco è uscito.", "pergunta": "Por que *aveva finito* (trapassato) e *è uscito* (p.prossimo)?", "resposta": "Finire = azione anteriore all'uscita → trapassato | Uscita = azione posteriore → p.prossimo", "conclusao": "dopo che + trapassato (azione precedente)"},
]
u['ponte'] = (
    "**Em português:** as regras de concordância existem mas são mais relaxadas na fala coloquial.\n\n"
    "**Em italiano:** a concordância dos tempos é mais rigorosa, especialmente na escrita.\n\n"
    "**Armadilha 'quando':** PT 'quando chegar' (presente do subjuntivo) = IT 'quando arriverò' (futuro). "
    "Em italiano usa-se o futuro, não o presente nem o subjuntivo."
)
u['coda'] = "A concordância dos tempos se aprende lendo, não estudando tabelas. Leia textos narrativos em italiano e observe como os tempos se encadeiam."

# ── Lezione XX — Il periodo ipotetico ────────────────────────
u = by_id['a1-lez20']
u['alerta'] = "O período hipotético é a estrutura 'se...então' do italiano. Há três tipos com tempos diferentes, e confundi-los muda completamente o sentido da frase."
u['inventario'] = [
    "Tipo 1 — realtà (possibile): se + presente/futuro + presente/futuro/imperativo: Se hai tempo, vieni.",
    "Tipo 2 — possibilità (irreale nel presente): se + congiuntivo imperfetto + condizionale presente: Se avessi tempo, verrei.",
    "Tipo 3 — irrealtà nel passato: se + congiuntivo trapassato + condizionale composto: Se avessi avuto tempo, sarei venuto.",
    "Tipo misto: se + cong. trapassato + condizionale presente (conseguenza ancora attuale): Se fossi nato a Roma, parlerei romanesco.",
    "Nota: in italiano colloquiale, il tipo 2 usa spesso imperfetto+imperfetto: Se avevo tempo, venivo.",
    "Ordine delle proposizioni: se-clause può venire prima o dopo la principale"
]
u['definicao'] = {
    "fenomeno": "*Se **avessi** soldi, **comprerei** una casa a Roma.* A hipótese usa tempos que não são nem presente nem futuro.",
    "causa": "Por que *avessi* (e não *ho*) e *comprerei* (e não *compro*)? Que tipo de hipótese é 'se eu tivesse dinheiro'?",
    "conceito": "O **periodo ipotetico tipo 2** usa congiuntivo imperfetto + condizionale para indicar hipóteses **irreais no presente** (não acontecem agora). O tipo 1 usa tempos reais (presente/futuro) para hipóteses **possíveis**."
}
u['tecnica'] = (
    "**Como escolher o tipo:**\n\n"
    "1. A condição é **possível/real** hoje? → Tipo 1: *se + presente → presente/imperativo*\n"
    "2. A condição é **improvável/irreal** hoje? → Tipo 2: *se + cong.imperfetto → condizionale presente*\n"
    "3. A condição é **impossível** (no passado)? → Tipo 3: *se + cong.trapassato → condiz.composto*\n"
    "4. Misto (passado impossível, consequência ainda atual): *se + cong.trapassato → condiz.presente*\n"
    "5. Na fala informal tipo 2: aceita-se *se avevo + avevo* (imperfetto+imperfetto)"
)
u['exemplos_prc'] = [
    {"oracao": "Se hai fame, mangia qualcosa.", "pergunta": "Que tipo de periodo ipotetico é este? A condição é possível?", "resposta": "Tipo 1 (della realtà): condição possível, real — se+presente → imperativo", "conclusao": "tipo 1: se+presente → imperativo/presente (possibile)"},
    {"oracao": "Se avessi più soldi, viaggierei di più.", "pergunta": "Por que *avessi* (congiuntivo) e *viaggierei* (condizionale)?", "resposta": "Tipo 2 (irreale nel presente): non ho abbastanza soldi → ipotesi irreal hoje", "conclusao": "tipo 2: se+cong.imperf. → condizionale (irreale oggi)"},
    {"oracao": "Se avessi studiato di più, avrei superato l'esame.", "pergunta": "Tipo 3? Por que usa congiuntivo trapassato + condizionale composto?", "resposta": "Tipo 3 (irreale nel passato): non ho studiato → impossibile cambiare il passato", "conclusao": "tipo 3: se+cong.trapass. → condiz.composto (impossibile)"},
]
u['ponte'] = (
    "**Em português:** 'se tivesse dinheiro, compraria' = *se avessi soldi, comprerei* — estrutura quase idêntica.\n\n"
    "**Tipo 1:** PT 'se você tem fome, coma' = IT 'se hai fame, mangia' — mesma lógica.\n\n"
    "**Tipo 3:** PT 'se tivesse estudado, teria passado' = IT 'se avessi studiato, avrei superato' — idêntico.\n\n"
    "**Diferença:** o congiuntivo italiano é obrigatório nos tipos 2 e 3. Em PT coloquial se aceita o indicativo ('se eu tinha'), mas em IT formal só o congiuntivo é correto."
)
u['coda'] = "Os três tipos do periodo ipotetico são um dos testes definitivos de nível B1/B2. Domine-os e seu italiano escrito ficará imediatamente mais sofisticado."

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Lezioni XI–XX atualizadas com campos NMA.")
