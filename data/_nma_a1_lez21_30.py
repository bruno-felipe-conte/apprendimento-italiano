import json, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

a1 = next(m for m in data['moduli'] if m['id'] == 'A1')
by_id = {u['id']: u for u in a1['unidades']}

# ── Lezione XXI — Il gerundio e i participi ──────────────────
u = by_id['a1-lez21']
u['alerta'] = "O gerúndio e os particípios são formas não-finitas que permitem construir frases complexas sem usar conjunções. São marca de estilo elevado e aparecem constantemente em textos escritos."
u['inventario'] = [
    "Gerundio presente: parl-ando | scriv-endo | dorm-endo (invariável)",
    "Gerundio passato: avendo/essendo + participio: avendo mangiato | essendo andato",
    "Stare + gerundio = azione in corso: Sto studiando. Stavamo mangiando.",
    "Gerundio come modo (simultâneo): Ascoltando musica, studio meglio.",
    "Participio presente: parl-ante / scriv-ente (aggettivo/sostantivo: uno studente, un dirigente)",
    "Participio passato: parl-ato / scriv-itto / dorm-ito — uso in tempi composti e come aggettivo",
    "Participio passato come aggettivo: una porta aperta / un compito fatto / una lettera scritta"
]
u['definicao'] = {
    "fenomeno": "*Uscendo di casa, ho dimenticato le chiavi. Sto leggendo un libro interessante.* O gerúndio cria conexão temporal sem usar conjunção.",
    "causa": "O que significa exatamente *uscendo* aqui? É simultaneidade? E por que não 'quando uscivo'?",
    "conceito": "O **gerundio** indica ação **simultânea** ou **anterior** ao verbo principal, com o **mesmo sujeito**. É mais compacto que a conjunção equivalente (*uscendo* = *mentre uscivo*). *Stare+gerundio* indica ação em curso no momento."
}
u['tecnica'] = (
    "**Como usar o gerundio:**\n\n"
    "1. Mesmos sujeito na principal e na subordinada? → use gerundio\n"
    "2. Ação simultânea: gerundio **presente** (*parlando, studiando*)\n"
    "3. Ação anterior: gerundio **passato** (*avendo mangiato, essendo uscito*)\n"
    "4. Ação em curso agora: **stare** (presente) + gerundio (*sto studiando*)\n"
    "5. Ação em corso no passado: **stare** (imperfetto) + gerundio (*stavo studiando*)\n"
    "6. O gerundio é sempre **invariável** — não muda per gênero ou número"
)
u['exemplos_prc'] = [
    {"oracao": "Studiando ogni giorno, ho imparato l'italiano in un anno.", "pergunta": "O que significa *studiando* aqui? Simultaneidade ou modo?", "resposta": "Studiando = 'estudando' (modo/mezzo) — indica como o resultado foi alcançado", "conclusao": "gerundio di modo: indica come/in che modo"},
    {"oracao": "Stavo dormendo quando è suonato il telefono.", "pergunta": "Por que *stavo dormendo* e não *dormivo*?", "resposta": "Stavo dormendo = azione in corso nel passato (enfasi sulla durata) | dormivo = imperfetto neutro", "conclusao": "stare+gerundio = azione in corso (con enfasi) | imperfetto = sfondo generico"},
    {"oracao": "Avendo finito il lavoro, Marco è uscito.", "pergunta": "Gerundio passato aqui — por que *avendo finito* e não *avendo finito*?", "resposta": "Gerundio passato (avendo+participio) = azione completata PRIMA dell'uscita di Marco", "conclusao": "gerundio passato = azione anteriore rispetto alla principale"},
]
u['ponte'] = (
    "**Em português:** 'estudando todo dia, aprendi' — gerúndio existe e funciona igual.\n\n"
    "**Stare+gerundio:** PT 'estou estudando' = IT *sto studiando* — estrutura idêntica.\n\n"
    "**Diferença:** em IT o gerúndio exige **mesmo sujeito** em ambas as orações (regra mais rigorosa que em PT coloquial).\n\n"
    "**Participio presente:** em IT ainda se usa como substantivo (*il cantante, lo studente*) — não confunda com o gerúndio."
)
u['coda'] = "Use *sto+gerundio* toda vez que quiser dizer o que está fazendo agora. É a forma mais natural para o presente contínuo em italiano."

# ── Lezione XXII — La forma passiva ──────────────────────────
u = by_id['a1-lez22']
u['alerta'] = "A voz passiva é indispensável em textos formais, jornalísticos e científicos. Sem ela, você não consegue compreender a maioria dos textos escritos em italiano."
u['inventario'] = [
    "Formazione: essere (in qualsiasi tempo) + participio passato (concordato col soggetto)",
    "Presente: Il libro è scritto da Marco.",
    "Passato prossimo: Il libro è stato scritto da Marco.",
    "Imperfetto: Il libro era scritto a mano.",
    "Futuro: Il libro sarà pubblicato a maggio.",
    "Agente: introdotto da 'da' (scritto DA Marco) | causa: introdotto da 'da' (colpito DAL fulmine)",
    "Alternativa con venire (solo tempi semplici): Il libro viene scritto = è scritto",
    "Alternativa con si passivante: Si vende casa. Si parla italiano."
]
u['definicao'] = {
    "fenomeno": "*Il romanzo **è stato scritto** da Manzoni nel 1827.* O sujeito (*il romanzo*) sofre a ação em vez de praticá-la.",
    "causa": "Como transformar 'Manzoni scrisse il romanzo' em voz passiva? O que muda na estrutura?",
    "conceito": "Na **forma passiva**, o objeto direto da frase ativa se torna o sujeito. O agente (quem pratica a ação) aparece introduzido por **da**. O verbo usa **essere** + participio concordado com o novo sujeito."
}
u['tecnica'] = (
    "**Como formar e usar a passiva:**\n\n"
    "1. Identifique: sujeito ativo → agente passivo (*da*) | objeto direto → sujeito passivo\n"
    "2. Conjugue **essere** no tempo desejado\n"
    "3. Adicione o participio concordado com o novo sujeito\n"
    "4. Alternativa: **venire** + participio (só tempi semplici; não funciona con p.prossimo)\n"
    "5. **Si passivante** (impessoal): si + verbo 3ª sg/pl (*si vende / si vendono*)\n"
    "6. Com essere: participio sempre concorda com soggetto (f.sg → -a, m.pl → -i)"
)
u['exemplos_prc'] = [
    {"oracao": "La torta è stata mangiata dai bambini.", "pergunta": "Como identificar que é passiva? Quem pratica a ação?", "resposta": "è stata mangiata = essere (p.prossimo) + participio | dai bambini = agente (da+i bambini)", "conclusao": "essere+participio+da = passiva | soggetto = la torta (sofre a ação)"},
    {"oracao": "In Italia si parla italiano.", "pergunta": "Esta é uma passiva com si? Como reconhecê-la?", "resposta": "si + verbo 3ª sg = si passivante impersonale (equivale: 'l'italiano viene parlato')", "conclusao": "si passivante = forma impessoal de passiva"},
    {"oracao": "La legge verrà approvata domani.", "pergunta": "Por que *verrà* (venire) em vez de *sarà* (essere) aqui?", "resposta": "venire enfatiza o processo/ação (atto puntuale) | essere é mais neutro — ambas são corretas", "conclusao": "venire (tempi semplici) = passiva com ênfase no processo"},
]
u['ponte'] = (
    "**Em português:** 'o livro foi escrito por Machado' = *il libro è stato scritto da Machado* — estrutura idêntica.\n\n"
    "**Diferença:** o PT usa 'por' como agente; o IT usa **da** (que também é origem, mas aqui é agente).\n\n"
    "**Si passivante:** PT 'fala-se português' = IT *si parla italiano* — mesma construção com 'se/si'.\n\n"
    "**Atenção:** em IT *essere+participio* pode ser passiva ('il libro è scritto') OU descrição de stato ('il libro è aperto') — o contexto decide."
)
u['coda'] = "Em textos jornalísticos e científicos, a passiva aparece a cada parágrafo. Reconhecê-la é tão importante quanto usá-la."

# ── Lezione XXIII — I verbi modali ───────────────────────────
u = by_id['a1-lez23']
u['alerta'] = "Potere, volere e dovere são os três verbos mais usados depois di essere e avere. Sem eles, você não consegue expressar permissão, obrigação, vontade ou capacidade."
u['inventario'] = [
    "Potere: posso/puoi/può/possiamo/potete/possono — capacidade/permissão",
    "Volere: voglio/vuoi/vuole/vogliamo/volete/vogliono — vontade/desejo",
    "Dovere: devo/devi/deve/dobbiamo/dovete/devono — obrigação/necessidade",
    "Sapere (+ inf.): so/sai/sa/sappiamo/sapete/sanno — habilidade aprendida",
    "Auxiliar nei tempi composti: seguem l'ausiliare del verbo infinito che segue (potere+andare → essere)",
    "Eccezione: se modal + verbo transitivo → avere (ho potuto mangiare)",
    "Posizione: modale conjugado + infinitivo (senza preposizione): Posso venire."
]
u['definicao'] = {
    "fenomeno": "*Non **posso** venire stasera. **Devo** lavorare. **Voglio** dormire.* Três verbos diferentes para 'não posso / devo / quero'.",
    "causa": "Quando usar *potere* vs *sapere*? E como escolher o auxiliar no passato prossimo (*ho potuto* vs *sono potuto*)?",
    "conceito": "Os **verbi modali** modificam o significado do infinitivo que os segue. *Potere* = capacidade física/permissão | *sapere+inf.* = habilidade adquirida | *dovere* = obrigação. Nos tempi composti, o auxiliar segue o verbo infinito que segue."
}
u['tecnica'] = (
    "**Como usar os modais:**\n\n"
    "1. Modal + **infinitivo** (sempre sem preposição): *posso venire*, *devo lavorare*\n"
    "2. Potere = 'poder' (permissão/capacidade física) | Sapere + inf. = 'saber' (habilidade)\n"
    "3. Nei tempi composti: o auxiliar segue o verbo que acompanha:\n"
    "   - Modal + verbo che usa AVERE → **ho** potuto mangiare\n"
    "   - Modal + verbo che usa ESSERE → **sono** potuto andare\n"
    "4. *Volere* nel condizionale → **vorrei** (educato) | *voglio* (diretto)\n"
    "5. *Dovere* nel condizionale → **dovrei** = 'deveria'"
)
u['exemplos_prc'] = [
    {"oracao": "So parlare italiano ma non so suonare il pianoforte.", "pergunta": "Por que *so* (sapere) e não *posso* (potere) para habilidade?", "resposta": "sapere+inf. = habilidade adquirida (aprendida) | potere = capacidade física/permissão", "conclusao": "habilidade aprendida → sapere+inf. | capacidade/permissão → potere"},
    {"oracao": "Non sono potuto andare alla festa.", "pergunta": "Por que *sono* (essere) e não *ho* (avere) com *potere*?", "resposta": "andare usa essere → modal+andare → essere: sono potuto andare", "conclusao": "modal+verbo di moto (essere) → sono/era/sarò potuto"},
    {"oracao": "Dovresti studiare di più.", "pergunta": "*Dovresti* é presente ou condizionale? Cosa significa?", "resposta": "Condizionale presente di dovere: dovresti = 'deverias / você deveria' (conselho educado)", "conclusao": "dovere condizionale = conselho/obrigazione attenuata"},
]
u['ponte'] = (
    "**Em português:** 'posso / devo / quero' — modais existem com mesma função.\n\n"
    "**Potere vs Sapere:** PT 'eu sei nadar' = IT *so nuotare* (sapere, não potere). Em PT 'saber' é habilidade, igual ao IT *sapere+infinito*.\n\n"
    "**Auxiliar nos tempi composti:** em PT 'pude ir' = *sono potuto andare* (essere, não avere). Isso confunde quem vem do PT.\n\n"
    "**Volere → Vorrei:** em contextos formais (restaurante, loja), substitua sempre *voglio* por *vorrei*."
)
u['coda'] = "Aprenda *potere, volere, dovere, sapere* com suas conjugações irregolari de cor. Eles aparecem em praticamente toda frase comunicativa."

# ── Lezione XXIV — Pronomi diretti e indiretti combinati (ripasso) ──
u = by_id['a1-lez24']
u['alerta'] = "Esta lição consolida o sistema completo dos pronomes. Dominar pronomi diretti, indiretti e combinati é o que distingue um falante intermediário de um avançado."
u['inventario'] = [
    "Sistema completo: diretti (lo/la/li/le) + indiretti (mi/ti/gli/le/ci/vi) + combinati (me lo/te la/glielo...)",
    "Ne: partitivo e di+pronome: Ne ho comprati due. Ne parla spesso (= di questo).",
    "Ne con essere: Quanti libri hai? — Ne ho tre. / Quanti studenti ci sono? — Ce ne sono venti.",
    "Ordine fisso: indiretto + diretto | ne sempre in ultima posizione dopo gli altri",
    "Posição: prima del verbo coniugato | dopo infinito (enclítico) | dopo imperativo",
    "Accordo del participio: con lo/la/li/le/ne nei tempi composti con avere"
]
u['definicao'] = {
    "fenomeno": "*'Quanti caffè vuoi?' — 'Ne voglio due.'* A partícula *ne* substituiu 'caffè' parcialmente, mantendo o número.",
    "causa": "O que exatamente *ne* substitui? É sempre 'de algo'? Como posicioná-lo com outros pronomes?",
    "conceito": "**Ne** substitui complementi introdotti da *di* ou expressa quantidade partitiva. Combina com outros pronomes: *ce ne sono* (ci+ne), *gliene parlo* (gli+ne). Nos tempi composti, o participio concorda com *ne* se for oggetto diretto."
}
u['tecnica'] = (
    "**Como usar ne:**\n\n"
    "1. Substitui 'di + qualcosa': *Parlo di sport → **Ne** parlo*\n"
    "2. Partitivo (quantidade): *Vuoi del pane? — Sì, **ne** voglio un po'*\n"
    "3. Con essere: *Ci sono molti studenti → Ce **ne** sono molti* (ci+ne=ce ne)\n"
    "4. Posição: antes do verbo conjugado | enclítico dopo infinito (*parlarne*)\n"
    "5. Tempi composti: participio concorda: *Ho comprato tre libri → **Ne** ho comprati tre* (-i, m.pl)"
)
u['exemplos_prc'] = [
    {"oracao": "Hai dei fratelli? — Sì, ne ho due.", "pergunta": "O que *ne* substitui aqui? É partitivo?", "resposta": "ne = 'di fratelli' (partitivo di quantità): due fratelli → ne+due", "conclusao": "ne partitivo: sostituisce 'di+nome' con quantità"},
    {"oracao": "Ce ne sono ancora molti da leggere.", "pergunta": "Da onde vem *ce ne*? Quais dois pronomes são?", "resposta": "ci (locativo) + ne (partitivo) → ci→ce prima di ne: ce ne", "conclusao": "ci+ne = ce ne (sempre questa forma)"},
    {"oracao": "Gliene ho parlato ieri.", "pergunta": "*Gliene* — quais são os dois pronomes combinados?", "resposta": "gli (indiretto, a lui/lei/loro) + ne (di questo argomento): gli+ne=gliene", "conclusao": "gli+ne=gliene | posizione: prima del verbo"},
]
u['ponte'] = (
    "**Em português:** 'tenho dois' (sem repetir o substantivo) — em IT usa-se *ne*: *ne ho due*.\n\n"
    "**Ne partitivo:** PT 'quero um pouco' sem repetir = IT *ne voglio un po'* — ne substitui o substantivo.\n\n"
    "**Maior dificuldade:** o sistema completo (diretti+indiretti+ne+combinati) não tem equivalente sistemático em PT. É preciso memorizar os blocos."
)
u['coda'] = "Ne é a partícula mais elegante do italiano. Usá-la corretamente — *Ne ho parlato. Ce ne sono molti* — é sinal imediato de domínio avançado."

# ── Lezione XXV — Il discorso indiretto ──────────────────────
u = by_id['a1-lez25']
u['alerta'] = "O discurso indireto é fundamental para relatar o que alguém disse. Errar os tempos verbais nessa estrutura torna a narrativa confusa e incorreta."
u['inventario'] = [
    "Verbi introduttori: dire, chiedere, rispondere, spiegare, affermare, raccontare, domandare",
    "Discorso diretto → indiretto: trasformazione dei tempi verbali",
    "Presente → imperfetto: 'Sono stanco' → Ha detto che era stanco.",
    "Passato prossimo → trapassato: 'Ho mangiato' → Ha detto che aveva mangiato.",
    "Futuro → condizionale: 'Verrò' → Ha detto che sarebbe venuto.",
    "Imperativo → di + infinitivo: 'Vieni!' → Mi ha detto di venire.",
    "Cambiamento di persone e deittici: io→lui/lei | qui→lì | oggi→quel giorno | domani→il giorno dopo"
]
u['definicao'] = {
    "fenomeno": "*Marco dice: 'Sono stanco.'* → *Marco dice che **è** stanco.* / *Marco ha detto che **era** stanco.* O tempo do verbo muda conforme o verbo introdutório.",
    "causa": "Por que *è* quando o verbo é *dice* (presente), mas *era* quando é *ha detto* (passato)?",
    "conceito": "No discorso indiretto, os tempos mudam de acordo com a **concordanza dei tempi**. Verbo introdutório no **presente** → tempos originais mantidos. No **passato** → recuam um grau (presente→imperfetto, p.prossimo→trapassato, futuro→condizionale)."
}
u['tecnica'] = (
    "**Como transformar discorso diretto em indiretto:**\n\n"
    "1. Verbo introdutório no **presente**: mantenha os tempos originais\n"
    "2. Verbo introdutório no **passato**: aplique a concordanza:\n"
    "   - presente → **imperfetto**\n"
    "   - passato prossimo → **trapassato prossimo**\n"
    "   - futuro → **condizionale**\n"
    "   - imperativo → **di + infinitivo**\n"
    "3. Mude os deittici: io→lui/lei | qui→lì | adesso→allora | oggi→quel giorno | domani→il giorno dopo\n"
    "4. Mude i pronomi: 'mio'→suo | 'ti chiamo'→lo/la chiamò"
)
u['exemplos_prc'] = [
    {"oracao": "Luca ha detto: 'Parto domani.' → Luca ha detto che sarebbe partito il giorno dopo.", "pergunta": "Por que *sarebbe partito* (condizionale composto) e *il giorno dopo*?", "resposta": "Futuro (parto) no passado → condizionale composto | domani → il giorno dopo (deittico)", "conclusao": "futuro → condizionale | deittici mudam: domani→il giorno dopo"},
    {"oracao": "La prof ha chiesto: 'Avete studiato?' → ha chiesto se avevamo studiato.", "pergunta": "Por que *se* (e não *che*) e *avevamo studiato*?", "resposta": "Pergunta diretta (sì/no) → indiretto com SE | p.prossimo → trapassato", "conclusao": "domanda sì/no → se + frase | p.prossimo → trapassato"},
    {"oracao": "Mi ha detto di aspettare.", "pergunta": "Che forma ha l'imperativo nel discorso indiretto?", "resposta": "Imperativo → di + infinitivo: 'Aspetta!' → mi ha detto DI aspettare", "conclusao": "imperativo diretto → di+infinito nel discorso indiretto"},
]
u['ponte'] = (
    "**Em português:** 'ele disse que estava cansado' = *ha detto che era stanco* — mesma lógica de concordância.\n\n"
    "**Diferença:** em PT coloquial, os tempos frequentemente não recuam ('ele disse que ele ESTÁ cansado'). Em IT formal, o recuo é obrigatório.\n\n"
    "**Se para perguntas:** PT 'perguntou se você tinha estudado' = IT *ha chiesto se avevi studiato* — idêntico."
)
u['coda'] = "Pratique o discorso indiretto relatando diálogos reais: 'O professor disse que..., perguntou se..., pediu para...'. É o treino mais natural para essa estrutura."

# ── Lezione XXVI — I numeri, la data e l'ora ─────────────────
u = by_id['a1-lez26']
u['alerta'] = "Números, datas e horas são usados em absolutamente toda interação cotidiana. Hesitar nesses elementos é o marcador mais óbvio de principiante."
u['inventario'] = [
    "Numeri cardinali: uno/due/tre/.../dieci/undici/dodici/tredici/.../venti/ventuno/ventidue/.../cento/mille/un milione",
    "Numeri ordinali: primo/secondo/terzo/quarto/quinto/sesto/settimo/ottavo/nono/decimo → poi: undicesimo, dodicesimo...",
    "L'ora: Che ore sono? / Che ora è? — Sono le tre. / È l'una. / È mezzogiorno. / È mezzanotte.",
    "Ore e minuti: Sono le tre e un quarto (3:15) / e mezza (3:30) / meno un quarto (3:45)",
    "La data: Oggi è il tre maggio duemilaventisei. / Sono nato il quindici marzo millenovecentonovanta.",
    "I giorni: lunedì/martedì/mercoledì/giovedì/venerdì/sabato/domenica (minúsculas)",
    "I mesi: gennaio/febbraio/marzo/aprile/maggio/giugno/luglio/agosto/settembre/ottobre/novembre/dicembre"
]
u['definicao'] = {
    "fenomeno": "*'Che ore sono?' — 'Sono le tre e mezza.'* *'Quando sei nato?' — 'Il quindici marzo millenovecentonovanta.'* Dois sistemas numéricos em contextos diferentes.",
    "causa": "Por que *le tre* (plurale) mas *l'una* (singolare)? Por que *sono* para as horas mas *è* para mezzogiorno?",
    "conceito": "As horas em italiano usam **essere** + articolo + numero. L'una (singolare → è) | tutte le altre (plurale → sono). Os números nos anos e nas datas seguem regras específicas de formação."
}
u['tecnica'] = (
    "**Como ler horas e datas:**\n\n"
    "**Ore:**\n"
    "- 1:00 → **È l'una** | 2:00–12:00 → **Sono le** due/tre.../dodici\n"
    "- :15 → **e un quarto** | :30 → **e mezza** | :45 → **meno un quarto**\n"
    "- :xx minuti → *sono le tre e venti* | meno: *sono le quattro meno dieci*\n\n"
    "**Date:**\n"
    "- Oggi è **il** + numero cardinale + mese (non ordinale, exceto 1°: **il primo**)\n"
    "- Anno: millenovecentonovanta | duemila | duemilaventisei\n\n"
    "**Numeri composti:** venti+uno=ventuno (non: ventIuno) | cento+uno=centouno"
)
u['exemplos_prc'] = [
    {"oracao": "Sono le otto e un quarto di mattina.", "pergunta": "Por que *sono* (pl) e não *è* (sg)?", "resposta": "Le otto = plurale → sono | solo l'una è singolare → è l'una", "conclusao": "1 = è l'una | tutte le altre = sono le due/tre..."},
    {"oracao": "Il corso inizia il primo settembre e finisce il trenta giugno.", "pergunta": "Por que *il primo* mas *il trenta* (non *il trentesimo*)?", "resposta": "Nelle date: primo (ordinale) per il 1° | tutti gli altri: cardinale (trenta, non trentesimo)", "conclusao": "data: il PRIMO (ord.) | tutti gli altri: cardinale (il due, il trenta...)"},
    {"oracao": "Sono nato il ventitrè novembre millenovecentonovantadue.", "pergunta": "Come si legge l'anno '1992' in italiano?", "resposta": "mille+novecento+novanta+due = millenovecentonovantadue (tutto attaccato)", "conclusao": "anni: mille+novecento+... tutto in una parola sola"},
]
u['ponte'] = (
    "**Em português:** 'são três horas e meia' = *sono le tre e mezza* — mesma estrutura.\n\n"
    "**Diferença 1:** IT usa *sono le* para todas exceto l'una (è). PT usa 'é' para 1h, 'são' para as outras — mesma lógica!\n\n"
    "**Diferença 2:** nas datas, IT usa cardinais (il tre, il quindici) onde PT também usa ('o dia três, o dia quinze').\n\n"
    "**Atenção:** dias da semana e meses em IT são sempre **minúsculos** (lunedì, gennaio) — diferente do inglês."
)
u['coda'] = "Treine dizer a hora atual e a data de hoje em italiano todos os dias. Em 2 semanas será automático."

# ── Lezione XXVII — Gli aggettivi e i pronomi indefiniti ─────
u = by_id['a1-lez27']
u['alerta'] = "Os indefinidos permitem falar de quantidades vagas e pessoas/coisas não específicas. Sem eles, seu italiano fica artificialmente preciso e formal."
u['inventario'] = [
    "Aggettivi indefiniti (+ nome): qualche (sg.!) | alcuni/alcune (pl.) | ogni (sg.) | tutto/a/i/e | molto/poco/tanto/troppo",
    "Pronomi indefiniti (sem nome): qualcuno | qualcosa | nessuno | ognuno | tutto/tutti | chiunque",
    "Qualche: sempre singolare! qualche libro (non: qualche libri)",
    "Alcuni/alcune: sempre plurale — alcuni libri / alcune ragazze",
    "Nessuno: sempre singolare + negazione: Non c'è nessuno. (non: Non c'è nessuno. → correto!)",
    "Tutto + articolo: tutta la classe / tutto il giorno / tutti i giorni / tutte le persone",
    "Molto/poco/tanto/troppo: concordano col nome (molto lavoro / molte persone)"
]
u['definicao'] = {
    "fenomeno": "*Ho **qualche** problema. Ho **alcuni** problemi. **Ogni** studente deve studiare. **Nessuno** è venuto.* Quatro parole para quantidades vagas.",
    "causa": "Por que *qualche problema* (singular) mas *alcuni problemi* (plural)? Quando usar cada um?",
    "conceito": "**Qualche** indica quantidade imprecisa e usa sempre o **singular**. **Alcuni/alcune** indica 'alguns' no plural. **Ogni** (cada) usa sempre o singular. **Nessuno** (ninguém) usa o singular e requer dupla negazione (*non... nessuno*)."
}
u['tecnica'] = (
    "**Guia de escolha:**\n\n"
    "- Quantidade vaga (singular): **qualche** + nome sg (*qualche libro*)\n"
    "- Quantidade vaga (plural): **alcuni/alcune** + nome pl (*alcuni libri*)\n"
    "- Totalidade: **tutto/tutta/tutti/tutte** + articolo + nome\n"
    "- Distribuição: **ogni** + nome sg (*ogni giorno*)\n"
    "- Negação: **nessuno** + nome sg / **non...nessuno** (doppia negazione italiana)\n"
    "- Quantità variabile: molto/poco/tanto/troppo — concordano: molto lavoro / molte ore"
)
u['exemplos_prc'] = [
    {"oracao": "Ho qualche domanda da fare.", "pergunta": "Por que *domanda* (singular) e não *domande* (plural) depois de *qualche*?", "resposta": "Qualche è sempre seguito dal singolare — è la regola invariabile", "conclusao": "qualche + SEMPRE singolare (non plurale)"},
    {"oracao": "Non è venuto nessuno alla festa.", "pergunta": "Por que *non* E *nessuno* juntos? Não é dupla negação proibida?", "resposta": "In italiano la doppia negazione è OBBLIGATORIA con nessuno, niente, mai dopo non", "conclusao": "IT: non...nessuno (doppia negazione obbligatoria) ≠ PT regra"},
    {"oracao": "Tutti i giorni studio un'ora d'italiano.", "pergunta": "Por que *tutti i giorni* e não *ogni giorno* aqui? São intercambiáveis?", "resposta": "Sono quasi sinonimi: tutti i giorni (tutti+articolo) ≈ ogni giorno | ogni = mais distributivo", "conclusao": "tutti i giorni ≈ ogni giorno (quasi sinonimi)"},
]
u['ponte'] = (
    "**Em português:** 'algum livro' (sg) = *qualche libro* | 'alguns livros' (pl) = *alcuni libri* — mesma distinção.\n\n"
    "**Dupla negação:** PT 'não veio ninguém' = IT *non è venuto nessuno* — a dupla negação existe em ambas as línguas na fala coloquial.\n\n"
    "**Diferença:** *qualche* é sempre singular em IT, mesmo que o significado seja plural. Em PT 'algum/alguma' segue o mesmo padrão."
)
u['coda'] = "Memorize: qualche=sempre sg | alcuni=sempre pl | ogni=sempre sg | nessuno+non (doppia negazione). Esses quatro pontos eliminam a maioria dos erros com indefinidos."

# ── Lezione XXVIII — Le congiunzioni e le proposizioni subordinate ──
u = by_id['a1-lez28']
u['alerta'] = "As conjunções são a 'cola' da língua — sem elas, suas frases ficam fragmentadas e simplistas. Com elas, você constrói argumentos complexos e textos coesos."
u['inventario'] = [
    "Coordinanti: e/ed (e), ma (mas), o/oppure (ou), però (porém), quindi/dunque (portanto), anzi (aliás/pelo contrário)",
    "Subordinanti causali: perché, poiché, siccome, dato che, visto che (porque/já que)",
    "Subordinanti temporali: quando, mentre, dopo che, prima che, appena, finché",
    "Subordinanti finali: affinché, perché + congiuntivo (para que)",
    "Subordinanti concessive: anche se, sebbene, benché, nonostante + congiuntivo (embora)",
    "Subordinanti condizionali: se, a condizione che, purché + congiuntivo",
    "Subordinanti consecutive: così...che, tanto...che (tão...que)"
]
u['definicao'] = {
    "fenomeno": "*Studio **perché** voglio imparare. **Sebbene** sia difficile, continuo. **Finché** ho energia, vado avanti.* Três conjunções, três tipos de relação lógica.",
    "causa": "Por que *perché* (causa) vs *affinché* (finalidade)? E por que *sebbene* pede o congiuntivo?",
    "conceito": "As conjunções subordinantes estabelecem **relações lógicas** entre orações: causa, finalidade, concessão, condição, tempo. Algumas (*sebbene, benché, affinché, purché*) exigem o **congiuntivo** na subordinata."
}
u['tecnica'] = (
    "**Guia de relações lógicas:**\n\n"
    "- Causa (porque): **perché/poiché/siccome** + indicativo\n"
    "- Finalidade (para que): **perché/affinché** + congiuntivo\n"
    "- Concessão (embora): **sebbene/benché/nonostante** + congiuntivo | *anche se* + indicativo\n"
    "- Condição (se): **se** + indicativo (tipo 1) | **purché/a condizione che** + congiuntivo\n"
    "- Tempo: **quando** (quando) | **mentre** (enquanto) | **appena** (assim que) | **finché** (enquanto/até que)\n"
    "- Consequência: **così...che / tanto...che** + indicativo"
)
u['exemplos_prc'] = [
    {"oracao": "Studio italiano perché voglio lavorare in Italia.", "pergunta": "Por que *perché* + indicativo aqui e não congiuntivo?", "resposta": "perché de causa (porque) + indicativo | perché de finalidade (para que) + congiuntivo — aqui é causa", "conclusao": "perché causa → indicativo | perché finalità → congiuntivo"},
    {"oracao": "Sebbene sia stanco, continuo a lavorare.", "pergunta": "Por que *sia* (congiuntivo) depois de *sebbene*?", "resposta": "sebbene/benché = congiunzioni concessive che reggono SEMPRE il congiuntivo", "conclusao": "sebbene/benché + congiuntivo (obbligatorio)"},
    {"oracao": "Appena arriverò a casa, ti chiamerò.", "pergunta": "Por que *arriverò* (futuro) depois de *appena*?", "resposta": "appena con riferimento futuro → futuro (come quando): appena arriverò (non: arrivo)", "conclusao": "appena/quando + riferimento futuro → futuro"},
]
u['ponte'] = (
    "**Em português:** 'porque' = causa (*perché*+ind.) | 'para que' = finalidade (*perché/affinché*+cong.).\n\n"
    "**Congiuntivo obrigatório:** sebbene/benché/nonostante = embora/apesar de → em PT também pedem subjuntivo.\n\n"
    "**Diferença:** *mentre* = enquanto (simultaneidade) ≠ *ma* = mas (contraste). Em PT 'enquanto' pode ter ambos os sentidos; em IT são conjunções distintas."
)
u['coda'] = "Use *perché, quindi, però, quando* todo dia. Eles são as conjunções mais frequentes e o começo natural para construir frases complexas."

# ── Lezione XXIX — Gli avverbi ───────────────────────────────
u = by_id['a1-lez29']
u['alerta'] = "Os advérbios refinam o significado de verbos, adjetivos e outras palavras. Sem eles, o italiano fica telegráfico. Com eles, você consegue expressar gradação, dúvida e precisão."
u['inventario'] = [
    "Avverbi di modo: bene/male/così/volentieri/insieme | formados de adj.: lentamente, facilmente, rapidamente",
    "Formação de -mente: adj. femminile + -mente: lenta→lentamente | adj. in -le/-re: gentile→gentilmente (sem -e)",
    "Avverbi di luogo: qui/qua (aqui) | lì/là (lá) | su (su) | giù (abaixo) | dentro/fuori | vicino/lontano",
    "Avverbi di tempo: ora/adesso/subito/presto/tardi/ancora/già/mai/sempre/spesso/di solito/a volte",
    "Avverbi di quantità: molto/poco/abbastanza/troppo/quasi/appena/proprio/solo/soltanto",
    "Posizione: dopo il verbo (parla lentamente) | prima dell'aggettivo (molto bello) | a inizio frase (Fortunatamente...)",
    "Mai in frasi negative: Non vado MAI al cinema. (doppia negazione obbligatoria)"
]
u['definicao'] = {
    "fenomeno": "*Parla **lentamente**. Studia **molto**. Arriva **sempre** in ritardo.* Três advérbios, três funções diferentes.",
    "causa": "Como se formam advérbios como *lentamente*? E onde posicioná-los na frase?",
    "conceito": "Os advérbios modificam verbos, adjetivos ou outros advérbios, indicando **modo, lugar, tempo ou quantidade**. A maioria dos advérbios de modo se forma com **aggettivo femminile + -mente**."
}
u['tecnica'] = (
    "**Como formar e posicionar advérbios:**\n\n"
    "1. Avverbio di modo: adjetivo femminile + **-mente** (*lenta→lentamente*)\n"
    "2. Adjjetivos em **-le/-re**: remove o -e antes de -mente (*gentile→gentilmente*, *facile→facilmente*)\n"
    "3. Posição: após o verbo (*parla bene*) | antes do adjetivo (*molto bello*) | início para ênfase\n"
    "4. Advérbios de tempo: **già** (già mangiato = já comeu) | **ancora** (ancora non = ainda não) | **mai** (mai = nunca, com non)\n"
    "5. **Non...mai** = nunca (doppia negazione obbligatoria)"
)
u['exemplos_prc'] = [
    {"oracao": "Parla italiano perfettamente ma scrive lentamente.", "pergunta": "Como se formam *perfettamente* e *lentamente*?", "resposta": "perfetta (f.) + -mente = perfettamente | lenta (f.) + -mente = lentamente", "conclusao": "aggettivo femminile + -mente = avverbio di modo"},
    {"oracao": "Non sono mai stato a Tokyo.", "pergunta": "Por que *non* E *mai* na mesma frase?", "resposta": "Doppia negazione obbligatoria in italiano: non+mai = 'nunca'", "conclusao": "non...mai = nunca (doppia negazione, non proibita in IT)"},
    {"oracao": "Ho già mangiato, ma ho ancora fame.", "pergunta": "O que distingue *già* de *ancora* aqui?", "resposta": "già = ação já completada antes do esperado | ancora = continuação de estado ('ainda')", "conclusao": "già = già fatto | ancora = continua a essere vero"},
]
u['ponte'] = (
    "**Em português:** lenta+mente = lentamente — a formação é **idêntica**.\n\n"
    "**Adjvetivos em -le/-re:** IT *facilmente* (não: facilEmente) = PT 'facilmente' — mesma regra de elision.\n\n"
    "**Già/ancora:** PT 'já' = *già* | PT 'ainda' = *ancora* — direto.\n\n"
    "**Diferença posição:** em IT o advérbio geralmente vem **depois** do verbo nas frases afirmativas, diferente do PT onde a posição é mais livre."
)
u['coda'] = "Aprenda os 10 advérbios mais frequentes de cor: bene, male, molto, poco, sempre, mai, già, ancora, subito, spesso. Eles cobrem 80% das situações cotidianas."

# ── Lezione XXX — Ripasso generale ───────────────────────────
u = by_id['a1-lez30']
u['alerta'] = "Esta é a lição final do módulo A1. O ripasso não é revisão passiva — é síntese ativa. Identifique seus pontos fracos e trabalhe especificamente neles antes de avançar para o A2."
u['inventario'] = [
    "Morfologia nominal: gênero, número, artigos (determinativi e indeterminativi)",
    "Morfologia verbal: presente, passato prossimo, imperfetto, futuro, condizionale, congiuntivo básico",
    "Pronomi: soggetto, diretti, indiretti, combinati, riflessivi, relativi, ne, ci",
    "Preposizioni: semplici e articolate (di/a/da/in/su/con/per/tra)",
    "Strutture avanzate: periodo ipotetico (3 tipi), passiva, discorso indiretto, gerundio",
    "Accordo: participio passato con pronomi diretti | aggettivi con sostantivi | possessivi con posseduto",
    "Errori frequenti: ausiliare avere/essere | qualche+sg | doppia negazione | quando+futuro"
]
u['definicao'] = {
    "fenomeno": "Você chegou ao final do A1 com 30 lições, 9 tempos verbais, o sistema completo de pronomes e as estruturas fundamentais da sintaxe italiana.",
    "causa": "Quais são os pontos que ainda geram hesitação? Onde a automatização ainda não aconteceu?",
    "conceito": "A consolidação do A1 exige **reconhecimento automático** de estruturas, não apenas conhecimento declarativo. O teste real é: você consegue produzir frases complexas sem pausar para calcular regras?"
}
u['tecnica'] = (
    "**Checklist de consolidação A1:**\n\n"
    "1. Conjugar qualquer verbo regular (-are/-ere/-ire) no presente sem hesitar\n"
    "2. Escolher avere vs essere nos tempi composti automaticamente\n"
    "3. Usar pronomi diretti e indiretti (e combinati) sem pensar na posição\n"
    "4. Construir o periodo ipotetico tipo 1, 2 e 3 corretamente\n"
    "5. Transformar discorso diretto em indiretto com a concordanza dos tempos\n"
    "6. Usar preposizioni articuladas (del/al/dal/nel/sul) sem pensar\n"
    "7. **Se você hesita em algum destes:** volte à lição específica antes de avançar"
)
u['exemplos_prc'] = [
    {"oracao": "Se avessi studiato di più, sarei riuscito nell'esame.", "pergunta": "Qual tipo de periodo ipotetico? Identifique os dois tempos verbali.", "resposta": "Tipo 3 (irreale nel passato): se+cong.trapassato (avessi studiato) + condiz.composto (sarei riuscito)", "conclusao": "tipo 3: se+cong.trapass. → condiz.composto"},
    {"oracao": "Gliel'ho già mandata ieri.", "pergunta": "Decomponga *gliel'ho mandata*: quais pronomes? Por que *mandata*?", "resposta": "gli (indiretto) + la (diretta, la lettera) → gliela, elide: gliel' | mandata: participio concorda con 'la' (f.sg)", "conclusao": "gli+la=gliela | participio concorda col pronome diretto (f.sg→-a)"},
    {"oracao": "Stavo leggendo quando è arrivato Marco.", "pergunta": "Identifique os dois tempi verbali e explique a função de cada um.", "resposta": "stavo leggendo = azione in corso (imperfetto progressivo) | è arrivato = evento puntuale che interrompe (p.prossimo)", "conclusao": "imperfetto progressivo = sfondo | p.prossimo = evento puntuale"},
]
u['ponte'] = (
    "**Síntese comparativa PT→IT:**\n"
    "- Artigos: PT 4 formas → IT 7 formas (il/lo/l'/la/i/gli/le)\n"
    "- Pronomi: PT sistema simples → IT 4 categorias (diretti/indiretti/combinati/riflessivi)\n"
    "- Auxiliar: PT só TER → IT AVERE ou ESSERE (escolha obrigatória)\n"
    "- Preposições contraem: PT 4 (do/no/ao/da) → IT 35+ combinações\n"
    "- Tempos verbais: PT e IT têm correspondência direta em quase todos os casos\n\n"
    "**O que você ganhou:** a estrutura completa do italiano padrão. O A2 trabalha a fluência; o B1, a sofisticação."
)
u['coda'] = "Avançar para o A2 sem consolidar o A1 é construir sobre areia. Faça o checklist acima, identifique as lacunas, e feche-as antes de prosseguir."

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Lezioni XXI–XXX atualizadas com campos NMA.")
