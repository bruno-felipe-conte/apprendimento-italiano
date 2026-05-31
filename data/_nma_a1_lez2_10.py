import json, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

a1 = next(m for m in data['moduli'] if m['id'] == 'A1')
by_id = {u['id']: u for u in a1['unidades']}

# ── Lezione II — Il presente indicativo ──────────────────────
u = by_id['a1-lez2']
u['alerta'] = "O presente indicativo é o tempo mais usado no italiano. Sem ele, você não consegue dizer sequer 'eu falo', 'você come' ou 'eles vivem'. Domine os três grupos de conjugação agora."
u['inventario'] = [
    "Verbos em -ARE (1ª conjugação): parl-are → parlo, parli, parla, parliamo, parlate, parlano",
    "Verbos em -ERE (2ª conjugação): scriv-ere → scrivo, scrivi, scrive, scriviamo, scrivete, scrivono",
    "Verbos em -IRE tipo 1 (3ª conj.): dorm-ire → dormo, dormi, dorme, dormiamo, dormite, dormono",
    "Verbos em -IRE tipo 2 com -isc-: cap-ire → capisco, capisci, capisce, capiamo, capite, capiscono",
    "Verbos irregulares essenciais: essere, avere, andare, fare, venire, uscire, sapere, potere, volere, dovere",
    "Uso: ação presente, hábito, futuro próximo ('domani parto')",
]
u['definicao'] = {
    "fenomeno": "Na rua, alguém diz: *Marco parla con Maria. Loro mangiano la pizza. Io non capisco!* Três frases simples, mas cada verbo tem uma terminação diferente.",
    "causa": "Por que *parla* termina em -a e *mangiano* termina em -iano? Quem decide a terminação? É sempre a mesma lógica?",
    "conceito": "A terminação do verbo indica **quem** faz a ação (a pessoa: io/tu/lui…) e **quando** (o tempo: presente). Cada grupo de verbos (-are/-ere/-ire) tem seu próprio conjunto de terminações. Basta aprender o padrão de cada grupo."
}
u['tecnica'] = (
    "**Como conjugar qualquer verbo regular no presente:**\n\n"
    "1. Identifique o grupo: termina em **-are**, **-ere** ou **-ire**?\n"
    "2. Retire o infinitivo (-are/-ere/-ire) — resta o **radical** (parl-, scriv-, dorm-)\n"
    "3. Adicione a terminação correta conforme a pessoa:\n"
    "   - -ARE: -o / -i / -a / -iamo / -ate / -ano\n"
    "   - -ERE: -o / -i / -e / -iamo / -ete / -ono\n"
    "   - -IRE tipo 1: -o / -i / -e / -iamo / -ite / -ono\n"
    "   - -IRE tipo 2: -isco / -isci / -isce / -iamo / -ite / -iscono\n"
    "4. Para verbos irregulares (andare, fare, etc.): memorize a forma inteira"
)
u['exemplos_prc'] = [
    {"oracao": "Io parlo italiano, ma non capisco il dialetto.", "pergunta": "Como conjugar *parlare* e *capire* na 1ª pessoa? São do mesmo grupo?", "resposta": "parlare (-are) → parlo | capire tipo 2 (-ire) → capisco", "conclusao": "Radical + terminação: parl+o / cap+isco"},
    {"oracao": "Loro mangiano la pizza ogni venerdì.", "pergunta": "Por que *mangiare* na 3ª pessoa plural é *mangiano* e não *mangono*?", "resposta": "mangiare tem radical mangi- (já com -i), então: mangi+ano = mangiano", "conclusao": "Radical termina em -i → não duplicar: mangi+ano"},
    {"oracao": "Voi uscite tardi; noi usciamo presto.", "pergunta": "Como conjugar o irregular *uscire* na 2ª e 1ª pessoa plural?", "resposta": "uscire irregular: esco, esci, esce, usciamo, uscite, escono", "conclusao": "uscire: radical muda (esc-) nas pessoas 1-3sg e 3pl"},
]
u['ponte'] = (
    "**Em português:** eu falo / tu falas / ele fala — a terminação varia por pessoa.\n\n"
    "**Em italiano:** io parlo / tu parli / lui parla — mesma lógica, terminações diferentes.\n\n"
    "**Diferença:** o italiano tem **3 grupos** de conjugação (-are/-ere/-ire) com terminações distintas. "
    "O português também tem 3 grupos, mas as terminações coincidem parcialmente.\n\n"
    "**Armadilha:** *-ire tipo 2* (capire, finire, preferire) insere **-isc-** nas pessoas 1-3sg e 3pl — não existe equivalente direto em português."
)
u['coda'] = "Quem não treinar os verbos irregulares com frases reais vai sempre hesitar na conversa. Memorize essere, avere, andare, fare como blocos fixos."

# ── Lezione III — Le preposizioni semplici e articolate ──────
u = by_id['a1-lez3']
u['alerta'] = "As preposições são as palavras mais curtas e mais problemáticas do italiano. Errar *a*, *di*, *da*, *in*, *su* pode mudar completamente o sentido de uma frase."
u['inventario'] = [
    "Preposizioni semplici: di, a, da, in, con, su, per, tra/fra",
    "Preposizioni articolate: preposição + artigo fundidos (del, al, dal, nel, sul…)",
    "Tabela: di+il=del, di+lo=dello, di+la=della, di+l'=dell', di+i=dei, di+gli=degli, di+le=delle",
    "A + artigo: al, allo, alla, all', ai, agli, alle",
    "Da + artigo: dal, dallo, dalla, dall', dai, dagli, dalle",
    "In + artigo: nel, nello, nella, nell', nei, negli, nelle",
    "Su + artigo: sul, sullo, sulla, sull', sui, sugli, sulle",
    "Con+il=col (opcional); per, tra, fra não se contraem"
]
u['definicao'] = {
    "fenomeno": "Você lê: *Il libro **del** professore è **sul** tavolo. Vengo **dall'** università.* As palavras *del*, *sul*, *dall'* não existem no dicionário isoladamente.",
    "causa": "De onde vêm *del*, *sul*, *dall'*? Por que não se diz *di il* ou *su il*?",
    "conceito": "Em italiano, certas preposições (**di, a, da, in, su**) se **fundem obrigatoriamente** com o artigo determinativo seguinte, formando uma palavra só chamada *preposizione articolata*. Não é opcional — é regra."
}
u['tecnica'] = (
    "**Como usar preposições articuladas:**\n\n"
    "1. Identifique a preposição necessária: di / a / da / in / su\n"
    "2. Veja qual artigo acompanha o nome seguinte: il / lo / l' / la / i / gli / le\n"
    "3. Funda os dois: di+il = **del** | a+la = **alla** | da+gli = **dagli** | in+l' = **nell'**\n"
    "4. Con, per, tra, fra: **não se contraem** — ficam separados do artigo\n"
    "5. Dica: se o nome não tem artigo determinativo, use a preposição simples (vado **in** Italia)"
)
u['exemplos_prc'] = [
    {"oracao": "Il libro del professore è sulla scrivania.", "pergunta": "Por que *del* e *sulla*? Qual preposição + qual artigo?", "resposta": "di+il=del (posse) | su+la=sulla (localização)", "conclusao": "di+il=del | su+la=sulla"},
    {"oracao": "Vengo dall'università alle tre.", "pergunta": "Por que *dall'* e *alle*? Quais são as preposições base?", "resposta": "da+l'=dall' (origem) | a+le=alle (tempo)", "conclusao": "da+l'=dall' | a+le=alle"},
    {"oracao": "Parlo con gli studenti del corso.", "pergunta": "Por que *con gli* fica separado mas *del* funde?", "resposta": "con não se contrai: con+gli fica separado | di+i=dei, di+gli=degli", "conclusao": "con nunca contrai | di+gli=degli"},
]
u['ponte'] = (
    "**Em português:** 'do professor' = de+o | 'no livro' = em+o — também há contração.\n\n"
    "**Em italiano:** o sistema é mais completo — **5 preposições** contraem com **7 artigos** = 35+ formas.\n\n"
    "**Analogia direta:** PT 'do'=IT 'del' | PT 'no'=IT 'nel' | PT 'ao'=IT 'al' | PT 'da'=IT 'dalla'.\n\n"
    "**Diferença:** em italiano *su* (sobre) também se contrai: sul, sulla, sullo — sem equivalente direto em português."
)
u['coda'] = "As preposições articuladas são automáticas em italiano — quem as usar corretamente soará nativo imediatamente."

# ── Lezione IV — Il passato prossimo ─────────────────────────
u = by_id['A1-04']
u['alerta'] = "O passato prossimo é o tempo do passado mais usado na conversação italiana. Sem ele, você não consegue contar o que fez hoje, ontem ou na semana passada."
u['inventario'] = [
    "Formação: AVERE ou ESSERE (presente) + participio passato",
    "Participio de -are: parl-are → parlato | Participio de -ere: scriv-ere → scritto (irregular) | Participio de -ire: dorm-ire → dormito",
    "Verbos com AVERE: a maioria dos transitivos (mangiare, vedere, fare, dire, volere, potere…)",
    "Verbos com ESSERE: movimento, stato, cambiamento de estado + tutti i riflessivi (andare, venire, partire, nascere, morire…)",
    "Com ESSERE: participio concorda em gênero e número com o sujeito (lei è andata / loro sono andati)",
    "Com AVERE: participio é invariável (ho mangiato, abbiamo mangiato)",
    "Participi irregolari essenziali: fatto, detto, scritto, letto, visto, aperto, chiuso, messo, preso, venuto, stato"
]
u['definicao'] = {
    "fenomeno": "Maria diz: *Ieri **ho mangiato** la pizza e **sono andata** al cinema.* Dois verbos no passado, mas um usa *ho* e o outro *sono*.",
    "causa": "Por que *ho mangiato* usa *ho* (avere) e *sono andata* usa *sono* (essere)? Como decidir qual auxiliar usar?",
    "conceito": "O **passato prossimo** é formado por auxiliar + participio. A escolha do auxiliar depende do verbo: **transitivos** → avere | **intransitivos de movimento/estado** → essere. Com essere, o participio **concorda** com o sujeito."
}
u['tecnica'] = (
    "**Como formar o passato prossimo:**\n\n"
    "1. O verbo é transitivo (tem objeto direto)? → auxiliar **avere**\n"
    "2. O verbo indica movimento, estado, nascimento, morte? → auxiliar **essere**\n"
    "3. Forme o participio: -are → **-ato** | -ere → **-uto** (ou irregular) | -ire → **-ito**\n"
    "4. Se usou **essere**: ajuste o participio: -o (m.sg) / -a (f.sg) / -i (m.pl) / -e (f.pl)\n"
    "5. Se usou **avere**: participio invariável em -o\n"
    "6. Dúvida sobre o auxiliar? Teste: 'fiz/comi algo' → avere | 'fui/cheguei' → essere"
)
u['exemplos_prc'] = [
    {"oracao": "Ieri ho mangiato la pasta e ho bevuto il vino.", "pergunta": "Por que *ho mangiato* e *ho bevuto* — ambos com avere?", "resposta": "mangiare e bere são transitivos (têm objeto: la pasta, il vino)", "conclusao": "transitivo + objeto → avere | participio invariável"},
    {"oracao": "Maria è andata a Roma e è tornata stanotte.", "pergunta": "Por que *è andata* e *è tornata* usam essere? E por que -a no final?", "resposta": "andare/tornare = movimento → essere | Maria é feminina → participio em -a", "conclusao": "essere + sujeito fem. sg. → participio em -a"},
    {"oracao": "I ragazzi sono partiti presto; le ragazze sono partite tardi.", "pergunta": "Por que *partiti* (m.pl) e *partite* (f.pl)?", "resposta": "partire usa essere → participio concorda: ragazzi (m.pl) → -i | ragazze (f.pl) → -e", "conclusao": "essere: participio concorda em gênero e número com sujeito"},
]
u['ponte'] = (
    "**Em português:** 'eu comi / eu fui' — um único auxiliar 'ter' para tudo.\n\n"
    "**Em italiano:** dois auxiliares — **avere** e **essere** — com escolha obrigatória.\n\n"
    "**Principal diferença:** a concordância do participio com essere não existe em português. "
    "'Ela foi' = *lei è andata* (participio -a) | 'eles foram' = *loro sono andati* (participio -i).\n\n"
    "**Dica prática:** memorizem os verbos de essere como lista fechada: andare, venire, partire, arrivare, entrare, uscire, nascere, morire, restare, stare, essere, diventare, salire, scendere."
)
u['coda'] = "O aluno que não memorizar os verbos que pedem essere vai errar a concordância do participio indefinidamente. Estude a lista como vocabulário, não como gramática."

# ── Lezione V — La particella "ci" ───────────────────────────
u = by_id['A1-05']
u['alerta'] = "A partícula *ci* tem múltiplos usos e é uma das mais frequentes no italiano falado. Ignorá-la significa não entender metade das conversas cotidianas."
u['inventario'] = [
    "ci = 'lá/aqui' locativo: Vai a Roma? Sì, ci vado domani.",
    "ci = 'nós' pronome (nos, a nós): Ci vediamo! / Il professore ci ha salutato.",
    "ci + essere = c'è / ci sono: C'è un problema. Ci sono molte persone.",
    "ci + verbi di pensiero: pensarci (pensar nisso), tenerci (dar importância), crederci (acreditar nisso)",
    "ci vuole / ci vogliono: ci vuole un'ora. Ci vogliono due ore.",
    "Posição: antes do verbo conjugado | depois do infinitivo | depois dell'imperativo"
]
u['definicao'] = {
    "fenomeno": "Você ouve: *'Vai spesso al mercato?' — 'Sì, **ci** vado ogni sabato.'* A palavra *ci* substituiu 'al mercato' inteiramente.",
    "causa": "O que exatamente *ci* substitui nessa frase? Pode sempre substituir um lugar? Quais outros usos tem?",
    "conceito": "**Ci** é uma partícula multiuso: (1) pronome locativo que substitui um **lugar** já mencionado ('lá', 'aqui'); (2) pronome de 1ª pessoa plural ('nos'); (3) parte de locuções verbais fixas (*ci vuole*, *c'è*)."
}
u['tecnica'] = (
    "**Como usar ci corretamente:**\n\n"
    "1. Substitui um **lugar**: 'Vai in centro?' → 'Sì, ci vado' (ci = in centro)\n"
    "2. Pronome **noi**: 'Il professore ci ha visto' (ci = nós, objeto direto)\n"
    "3. **C'è / ci sono**: sempre antes de essere para indicar existência\n"
    "4. Verbos fixos: *pensarci* (pensar nisso) | *tenerci* (importar-se) | *volerci* (ser necessário)\n"
    "5. Posição: **antes** do verbo finito | **depois** do infinitivo (andarci) | **depois** do imperativo (Vacci!)"
)
u['exemplos_prc'] = [
    {"oracao": "Sei mai stato a Venezia? — Sì, ci sono stato l'anno scorso.", "pergunta": "O que *ci* substitui aqui? É locativo?", "resposta": "ci = a Venezia (lugar já mencionado)", "conclusao": "ci locativo substitui 'a + luogo'"},
    {"oracao": "Ci vuole coraggio per parlare in pubblico.", "pergunta": "O que significa *ci vuole* aqui? Qual é o sujeito?", "resposta": "ci vuole = 'é necessário' | sujeito = coraggio (singular → vuole)", "conclusao": "ci vuole + sg. | ci vogliono + pl."},
    {"oracao": "Non ci credo! È impossibile.", "pergunta": "O que *ci* substitui em *non ci credo*?", "resposta": "ci = 'nisso' (na coisa mencionada antes)", "conclusao": "ci com verbi di pensiero = pronome neutro 'nisso/naquilo'"},
]
u['ponte'] = (
    "**Em português:** não existe equivalente direto de *ci* como partícula única.\n\n"
    "Traduz-se como: 'lá' (locativo) | 'nos' (pronome) | 'há' (c'è/ci sono) | 'é preciso' (ci vuole).\n\n"
    "**Armadilha:** em português dizemos 'Você vai ao mercado? — Sim, vou lá' mas o 'lá' é opcional. "
    "Em italiano, *ci* é obrigatório: *'Vai al mercato?' — 'Sì, **ci** vado'* (sem ci soa incompleto)."
)
u['coda'] = "Quem souber usar *ci* naturalmente parecerá nativo. Treine com frases do cotidiano: *Ci sei? Ci vado. C'è qualcuno?*"

# ── Lezione VI — Il futuro semplice e composto ───────────────
u = by_id['A1-06']
u['alerta'] = "O futuro italiano é mais simples do que parece, mas tem irregulares muito usados. Dominar o futuro abre o caminho para planos, promessas e previsões."
u['inventario'] = [
    "Futuro semplice de -ARE: parl-are → parlerò, parlerai, parlerà, parleremo, parlerete, parleranno",
    "Futuro de -ERE: scriv-ere → scriverò, scriverai, scriverà…",
    "Futuro de -IRE: dorm-ire → dormirò, dormirai, dormirà…",
    "Irregolari: essere→sarò | avere→avrò | andare→andrò | fare→farò | venire→verrò | volere→vorrò | potere→potrò | dovere→dovrò | sapere→saprò",
    "Futuro composto: futuro di avere/essere + participio (avrò mangiato, sarò andato)",
    "Uso: azione futura | ipotesi nel presente ('Avrà 30 anni') | dopo 'quando/se' in frasi subordinate"
]
u['definicao'] = {
    "fenomeno": "Você lê: *Domani **andrò** a Milano. Quando **arriverò**, ti **chiamerò**.* Três verbos no futuro, todos com terminações em -ò, -ò, -ò.",
    "causa": "Como se forma *andrò*? Por que não é *anderò*? Como reconhecer um verbo no futuro?",
    "conceito": "O futuro simples se forma pelo **infinitivo sem -e** + terminações **-ò/-ai/-à/-emo/-ete/-anno**. Verbos em -are mudam a vogal temática: parl**a**re → parler-. Alguns verbos são irregulares e contraem o radical."
}
u['tecnica'] = (
    "**Como formar o futuro semplice:**\n\n"
    "1. Tome o infinitivo e retire o **-e** final: parlare → parlar- | scrivere → scriver- | dormire → dormir-\n"
    "2. Para verbos em **-are**: substitua a -a- por -e-: parlare → parler-\n"
    "3. Adicione as terminações: **-ò / -ai / -à / -emo / -ete / -anno**\n"
    "4. Irregolari com radical contraído: and**r**- | av**r**- | sar- | far- | verr- | vorr- | pot**r**- | dov**r**- | sap**r**-\n"
    "5. Para o **futuro composto**: avrò/sarò + participio passato"
)
u['exemplos_prc'] = [
    {"oracao": "Domani andrò a Roma e vedrò il Colosseo.", "pergunta": "Como se forma *andrò* e *vedrò*? São regulares?", "resposta": "andare irregular: andr-+ò=andrò | vedere irregular: vedr-+ò=vedrò", "conclusao": "andr-+ò | vedr-+ò (radicais irregulares contraídos)"},
    {"oracao": "Quando arriverò, ti chiamerò subito.", "pergunta": "Por que usar futuro depois de 'quando'? Em português usaríamos presente.", "resposta": "Em italiano, 'quando' em referência ao futuro exige futuro (não presente)", "conclusao": "quando + futuro (regra italiana) ≠ português (quando + presente)"},
    {"oracao": "Avrà almeno quarant'anni, quel signore.", "pergunta": "É uma frase sobre o futuro? O que significa *avrà* aqui?", "resposta": "Não é futuro real — é futuro de probabilidade/suposição no presente", "conclusao": "futuro di probabilità: avrà = 'deve ter / provavelmente tem'"},
]
u['ponte'] = (
    "**Em português:** 'falarei / comerei / partirei' — terminações diretas no infinitivo.\n\n"
    "**Em italiano:** mesma lógica, mas verbos em -are mudam -a- para -e- (parlare → parler-).\n\n"
    "**Diferença:** a construção 'ir + infinitivo' (vou falar) é muito usada em PT mas menos formal em IT "
    "(*sto per parlare* = estou prestes a falar | *parto domani* = presente pro futuro próximo).\n\n"
    "**Futuro di probabilità** não existe em português — traduz-se por 'deve ter / provavelmente tem'."
)
u['coda'] = "Memorize os 9 irregolari do futuro como lista fixa. Eles são os verbos mais usados do italiano."

# ── Lezione VII — I possessivi ───────────────────────────────
u = by_id['a1-lez7']
u['alerta'] = "Os possessivos italianos concordam em gênero e número com a *coisa possuída*, não com o possuidor. Este é o erro mais comum dos falantes de português."
u['inventario'] = [
    "Possessivi: mio/mia/miei/mie | tuo/tua/tuoi/tue | suo/sua/suoi/sue | nostro/nostra/nostri/nostre | vostro/vostra/vostri/vostre | loro (invariável)",
    "Concordância: com o nome possuído (il mio libro, la mia penna, i miei libri, le mie penne)",
    "Artigo: obrigatório antes do possessivo, exceto com parentes singulares próximos",
    "Parenti singolari sem artigo: mio padre, tua sorella, nostro fratello (mas: i miei genitori, la mia famiglia)",
    "Loro: sempre con artigo (il loro libro, la loro casa)",
    "Uso enfático ou predicativo: Questo libro è mio. (sem artigo após essere)"
]
u['definicao'] = {
    "fenomeno": "*Il **mio** libro è sul tavolo. La **mia** penna è qui. I **miei** libri sono pesanti.* O mesmo 'meu/minha/meus' muda de forma três vezes.",
    "causa": "Por que *mio* vira *mia* e depois *miei*? O que muda — quem possui ou o que é possuído?",
    "conceito": "O possessivo italiano concorda em **gênero e número** com o **objeto possuído** (não com o possuidor). *Mio* = masculino singular | *mia* = feminino singular | *miei* = masculino plural | *mie* = feminino plural."
}
u['tecnica'] = (
    "**Como usar os possessivos:**\n\n"
    "1. Identifique o nome possuído e seu gênero/número\n"
    "2. Escolha a forma correta: masc.sg=-o | fem.sg=-a | masc.pl=-i | fem.pl=-e (exceto *loro*)\n"
    "3. Coloque o **artigo** antes: *il/la/i/le* + possessivo\n"
    "4. Com parentes próximos (pai, mãe, irmão, irmã, filho) no **singular**: sem artigo (*mio padre*)\n"
    "5. Com *loro*: sempre com artigo, sempre invariável (*il loro libro*, *le loro case*)"
)
u['exemplos_prc'] = [
    {"oracao": "Il mio zaino è rosso; la mia borsa è nera.", "pergunta": "Por que *mio* muda para *mia*? O possuidor mudou?", "resposta": "Não — o possuidor é sempre 'io'. Mudou o gênero do possuído: zaino (m.) → mio | borsa (f.) → mia", "conclusao": "possessivo concorda com o possuído, não com o possuidor"},
    {"oracao": "Mia sorella studia medicina; mio fratello lavora.", "pergunta": "Por que não há artigo antes de *mia sorella* e *mio fratello*?", "resposta": "Parenti stretti singolari + possessivo de 1ª/2ª/3ª sg. → sem artigo (exceto loro)", "conclusao": "parenti sg. → sem artigo: mia sorella (não: la mia sorella)"},
    {"oracao": "I loro genitori vivono a Milano.", "pergunta": "Por que *loro* não muda forma e mantém o artigo?", "resposta": "loro é invariável (sem flexão de gênero/número) e sempre exige artigo", "conclusao": "loro: invariável, sempre com artigo"},
]
u['ponte'] = (
    "**Em português:** 'meu livro / minha caneta' — possessivo concorda com o possuído. Mesma lógica.\n\n"
    "**Diferença 1:** em italiano o artigo é quase sempre obrigatório antes do possessivo (exceto parentes).\n\n"
    "**Diferença 2:** *suo/sua* pode ser ambíguo (dele/dela/de você formal). O contexto resolve.\n\n"
    "**Diferença 3:** 'deles/delas' = *loro* invariável — diferente do PT onde concordamos: 'seu/sua/seus/suas'."
)
u['coda'] = "Quem usar os possessivos sem artigo vai soar estrangeiro. Pratique: *il mio, la mia, i miei, le mie* até ser automático."

# ── Lezione VIII — I pronomi diretti ─────────────────────────
u = by_id['a1-lez8']
u['alerta'] = "Os pronomes diretos eliminam a repetição e são essenciais para conversas fluidas. Sem eles, você repete o objeto a cada frase, o que soa muito estranho em italiano."
u['inventario'] = [
    "Pronomi diretti: mi / ti / lo / la / ci / vi / li / le",
    "Lo = ele / isso (m.sg) | la = ela / isso (f.sg) | li = eles (m.pl) | le = elas (f.pl)",
    "Mi = me (1ª sg) | ti = te (2ª sg) | ci = nos (1ª pl) | vi = vos (2ª pl)",
    "Posição átona: antes do verbo conjugado (Lo vedo) | depois do infinitivo (Voglio vederlo)",
    "Com tempi composti (avere): il participio concorda col pronome: Ho vista Maria → L'ho vista",
    "La cortesia: La = Lei formale (La ringrazio, professore)"
]
u['definicao'] = {
    "fenomeno": "*'Hai visto Marco?' — 'Sì, **lo** ho visto ieri.'* A palavra *lo* substituiu 'Marco' completamente.",
    "causa": "O que exatamente *lo* substitui? E se fosse 'Maria'? E 'i libri'? Como escolher entre lo/la/li/le?",
    "conceito": "O pronome direto substitui o **complemento objeto direto** (quem sofre a ação, sem preposição). A escolha depende do gênero e número do nome substituído: lo (m.sg) / la (f.sg) / li (m.pl) / le (f.pl)."
}
u['tecnica'] = (
    "**Como substituir um objeto direto por pronome:**\n\n"
    "1. Identifique o objeto direto (sem preposição)\n"
    "2. Verifique gênero e número: m.sg → **lo** | f.sg → **la** | m.pl → **li** | f.pl → **le**\n"
    "3. Posicione o pronome **antes** do verbo conjugado: *Vedo Marco → **Lo** vedo*\n"
    "4. Com infinitivo: o pronome vai **depois**, attachado: *Voglio vedere Marco → Voglio veder**lo***\n"
    "5. Nos tempi composti com avere: participio concorda com lo/la/li/le: *Ho visto Maria → **L'ho vista***"
)
u['exemplos_prc'] = [
    {"oracao": "Conosci Marco? — Sì, lo conosco bene.", "pergunta": "O que *lo* substitui? Por que não *la* ou *li*?", "resposta": "Marco = masculino singular → lo", "conclusao": "m.sg → lo | pronome antes do verbo"},
    {"oracao": "Hai comprato le mele? — Sì, le ho comprate.", "pergunta": "Por que *comprate* (com -e) e não *comprato*?", "resposta": "le (f.pl) precede avere → participio concorda: compr-ate (f.pl)", "conclusao": "pronome diretto (la/le/lo/li) + avere → participio concorda"},
    {"oracao": "Devo chiamare Maria. — Devo chiamarla.", "pergunta": "Por que o pronome vai depois do verbo nesse caso?", "resposta": "Depois de infinitivo o pronome se enclitiza (junta-se ao final)", "conclusao": "infinitivo → pronome enclítico: chiamare+la=chiamarla"},
]
u['ponte'] = (
    "**Em português:** 'Você viu o Marco? — Sim, **o** vi.' — pronome direto antes do verbo.\n\n"
    "**Em italiano:** *'Hai visto Marco? — Sì, **lo** ho visto.'* — mesma posição.\n\n"
    "**Diferença:** concordância do participio com o pronome (*l'ho vista*) não existe em português.\n\n"
    "**Armadilha:** *la* pode ser pronome direto (a ela), artigo (la casa) ou pronome de cortesia (La ringrazio). O contexto distingue."
)
u['coda'] = "Pratique substituir objetos por pronomes em todas as frases que você treinar. A fluência vem da automatização, não da memorização das regras."

# ── Lezione IX — L'imperfetto indicativo ─────────────────────
u = by_id['a1-lez9']
u['alerta'] = "O imperfeito é o tempo das ações habituais e das descrições no passado. Confundi-lo com o passato prossimo é o erro mais frequente em narrativas italianas."
u['inventario'] = [
    "Formação: radical do presente (1ª pl. sem -iamo) + terminações -avo/-avi/-ava/-avamo/-avate/-avano (-ARE)",
    "Terminações -ERE/-IRE: -evo/-evi/-eva/-evamo/-evate/-evano | -ivo/-ivi/-iva/-ivamo/-ivate/-ivano",
    "Irregolari: essere→ero/eri/era/eravamo/eravate/erano | fare→facevo | bere→bevevo | dire→dicevo",
    "Uso 1 — azione abituale nel passato: Da bambino giocavo ogni giorno.",
    "Uso 2 — descrizione/stato nel passato: Era tardi, faceva freddo, eravamo stanchi.",
    "Uso 3 — azione in corso interrotta: Dormivo quando è arrivato.",
    "Imperfetto vs passato prossimo: imperfetto = durata/abitudine | p.prossimo = azione conclusa/puntuale"
]
u['definicao'] = {
    "fenomeno": "*Da bambino, **giocavo** in giardino ogni pomeriggio. Un giorno, mentre **giocavo**, **è caduto** un albero.* Dois tempos do passado na mesma narrativa.",
    "causa": "Por que *giocavo* (imperfetto) e não *ho giocato* (passato prossimo) para o hábito? E por que *è caduto* (p.prossimo) para a queda da árvore?",
    "conceito": "O **imperfetto** descreve o **cenário de fundo**: ações habituais, estados, situações em andamento. O **passato prossimo** marca **eventos pontuais** que interrompem ou ocorrem nesse cenário."
}
u['tecnica'] = (
    "**Como escolher entre imperfetto e passato prossimo:**\n\n"
    "1. A ação é **habitual** ('costumava', 'sempre fazia')? → **imperfetto**\n"
    "2. É uma **descrição** de estado, clima, aparência, sentimento? → **imperfetto**\n"
    "3. É uma **ação concluída** e pontual? → **passato prossimo**\n"
    "4. É o **pano de fundo** enquanto outra coisa acontece? → **imperfetto**\n"
    "5. Teste: substituível por 'costumava + infinitivo'? → imperfetto\n\n"
    "**Formação:** radical da 1ª pessoa plural presente (parliamo→parl-) + -avo/-evi/-ivo"
)
u['exemplos_prc'] = [
    {"oracao": "Quando ero piccolo, andavo al mare ogni estate.", "pergunta": "Por que *ero* e *andavo* estão no imperfetto?", "resposta": "Ero = estado no passado | andavo = ação habitual repetida ('ogni estate')", "conclusao": "estado + hábito passado → imperfetto"},
    {"oracao": "Dormivo quando il telefono ha squillato.", "pergunta": "Por que *dormivo* (imperfetto) e *ha squillato* (p.prossimo) na mesma frase?", "resposta": "dormivo = ação em curso (cenário) | ha squillato = evento pontual que interrompe", "conclusao": "azione in corso = imperfetto | interruzione = passato prossimo"},
    {"oracao": "Era una bella giornata: il sole splendeva e la gente passeggiava.", "pergunta": "Por que todas as ações estão no imperfetto?", "resposta": "São descrições de cenário/estado simultâneo, não eventos pontuais sequenciais", "conclusao": "descrizione di scenario → sempre imperfetto"},
]
u['ponte'] = (
    "**Em português:** 'eu brincava / eu estava dormindo' — corresponde ao imperfeito/pretérito imperfeito.\n\n"
    "**Em italiano:** *giocavo / dormivo* — praticamente a mesma lógica de uso.\n\n"
    "**Diferença:** em português usamos o pretérito imperfeito tanto para hábito quanto para descrição. "
    "Em italiano o imperfetto faz o mesmo, mas a distinção com o passato prossimo é mais rigorosa na escrita.\n\n"
    "**Irregular essencial:** *essere* no imperfeito — *ero, eri, era, eravamo, eravate, erano* — use todo dia."
)
u['coda'] = "A confusão entre imperfetto e passato prossimo é o maior marcador de nível A1/A2. Domine esta distinção e seu italiano dará um salto imediato."

# ── Lezione X — I pronomi indiretti ──────────────────────────
u = by_id['a1-lez10']
u['alerta'] = "Os pronomes indiretos são tão frequentes quanto os diretos, mas funcionam de forma diferente. Confundi-los é um dos erros mais visíveis no italiano intermediário."
u['inventario'] = [
    "Pronomi indiretti: mi / ti / gli / le / ci / vi / gli (loro)",
    "Gli = a lui / a loro (m.sg e pl.) | Le = a lei / a Lei formale (f.sg)",
    "Diferença de direto para indireto: lo/la/li/le → mi/ti/gli/le/ci/vi/gli",
    "Posição: igual aos diretos — antes do verbo conjugado, enclítico após infinitivo",
    "Verbos que exigem indiretto: dare, dire, chiedere, mandare, telefonare, rispondere, piacere, sembrare, bastare",
    "Piacere + indiretto: Mi piace il caffè. Gli piacciono i libri.",
    "Dopo avere nei tempi composti: nessuna concordanza col participio (diferente dos diretti)"
]
u['definicao'] = {
    "fenomeno": "*Ho telefonato a Marco. **Gli** ho detto la verità.* A palavra *gli* substituiu 'a Marco' — mas não é o objeto direto, é o objeto indireto.",
    "causa": "O que é exatamente o pronome indireto? Por que *gli* aqui e não *lo*? Como distinguir objeto direto de indireto?",
    "conceito": "O pronome indireto substitui o **complemento objeto indireto** (precedido por 'a'). Se a ação é feita **para/a** alguém: use indiretto. Se a ação age **diretamente** sobre alguém/algo: use diretto."
}
u['tecnica'] = (
    "**Como distinguir e usar direto vs indireto:**\n\n"
    "1. Pergunte ao verbo: 'fiz isso **a** alguém'? → objeto **indireto** → pronome indiretto\n"
    "2. 'Fiz isso diretamente (sem preposição)?' → objeto **direto** → pronome diretto\n"
    "3. Escolha a forma: mi/ti/**gli**(m.sg+pl)/le(f.sg)/ci/vi\n"
    "4. Com **piacere**: sujeito é a coisa que agrada → *Mi piace il libro* (livro=sujeito, mi=indiretto)\n"
    "5. Nos tempi composti: o participio **não concorda** com o pronome indiretto"
)
u['exemplos_prc'] = [
    {"oracao": "Ho scritto a Maria. — Le ho scritto una lettera.", "pergunta": "Por que *le* e não *la*? Qual a diferença?", "resposta": "scrivere a qualcuno → objeto indireto (a Maria) → le (indiretto f.sg)", "conclusao": "verbo + 'a' + pessoa → pronome indiretto (le, non la)"},
    {"oracao": "Mi piace la pizza. Mi piacciono i dolci.", "pergunta": "Por que *piace* (sg) vs *piacciono* (pl)? Quem é o sujeito?", "resposta": "la pizza = sujeito sg → piace | i dolci = sujeito pl → piacciono | mi = complemento indiretto", "conclusao": "piacere: soggetto = coisa | indiretto = pessoa que aprecia"},
    {"oracao": "Gli ho detto la verità, ma non mi ha risposto.", "pergunta": "Gli e mi são diretos ou indiretos aqui?", "resposta": "dire qualcosa a qualcuno: gli = indiretto (a lui) | rispondere a qualcuno: mi = indiretto (a me)", "conclusao": "dire/rispondere sempre + indiretto"},
]
u['ponte'] = (
    "**Em português:** 'telefonei **para** ele' → *gli ho telefonato* | 'vi ele' → *l'ho visto*.\n\n"
    "**Distinção:** se em português você diz 'fiz algo **a/para** alguém' → indiretto em italiano.\n\n"
    "**Piacere:** 'eu gosto de pizza' em IT = *mi piace la pizza* (literalmente: 'a mim agrada a pizza'). "
    "A pizza é o sujeito — isso é o oposto do português e causa muita confusão.\n\n"
    "**Gli para plural:** 'escrevi para eles' = *gli ho scritto* — o mesmo *gli* de 'para ele'."
)
u['coda'] = "Memorize os verbos que exigem indiretto como lista fixa: dare, dire, chiedere, rispondere, telefonare, scrivere, piacere. Eles são os mais frequentes."

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Lezioni II–X atualizadas com campos NMA.")
