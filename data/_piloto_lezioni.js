// ============================================================
// _piloto_lezioni.js — Didática para iniciantes absolutos
// Linguagem: sem jargão, como explicar para um amigo
// Exercícios: frases simples, cognatos, tradução em tudo
// Novo: tabela_visual (cola colorida durante os exercícios)
// ============================================================

const fs   = require('fs');
const path = require('path');
const GRAMMAR_PATH = path.join(__dirname, 'grammar.json');
const grammar = JSON.parse(fs.readFileSync(GRAMMAR_PATH, 'utf8'));

// ── a1-lez1 ── Nome, Articolo e Aggettivo ──────────────────
const lez1 = {
  id:       'a1-lez1',
  titulo:   'Nome, Articolo e Aggettivo',
  subtitulo:'O artigo — a peça que muda tudo',
  nivel:    'A1',

  // ── Tabela visual (cola durante os exercícios) ──────────
  tabela_visual: `<p class="tabela-intro">Use durante os exercícios — não precisa decorar agora!</p>
<div class="artigo-cards">
  <div class="artigo-card ac-azul">
    <div class="ac-titulo">🔵 IL &nbsp;·&nbsp; UN</div>
    <div class="ac-regra">Masculino · letra normal<br><small>(b, c, d, f, g, l, m, n, p, r, t, v...)</small></div>
    <div class="ac-exemplos">il <strong>gatto</strong> (gato) · il <strong>libro</strong> (livro)<br>un <strong>caffè</strong> · un <strong>piano</strong></div>
  </div>
  <div class="artigo-card ac-amarelo">
    <div class="ac-titulo">🟡 LO &nbsp;·&nbsp; UNO</div>
    <div class="ac-regra">Masculino · começa por:<br><strong>ST, SP, SC, SN, Z, GN, PS</strong></div>
    <div class="ac-exemplos">lo <strong>zaino</strong> (mochila) · lo <strong>studente</strong><br>uno <strong>zaino</strong> · uno <strong>studente</strong></div>
  </div>
  <div class="artigo-card ac-rosa">
    <div class="ac-titulo">🔴 LA &nbsp;·&nbsp; UNA</div>
    <div class="ac-regra">Feminino · qualquer consoante</div>
    <div class="ac-exemplos">la <strong>pizza</strong> · la <strong>casa</strong> · la <strong>musica</strong><br>una <strong>pizza</strong> · una <strong>mamma</strong></div>
  </div>
  <div class="artigo-card ac-verde">
    <div class="ac-titulo">🟢 L' &nbsp;·&nbsp; UN'</div>
    <div class="ac-regra">Masc. ou fem. · começa por <strong>vogal</strong><br><small>(a, e, i, o, u)</small></div>
    <div class="ac-exemplos">l'<strong>amico</strong> (amigo) · l'<strong>università</strong><br>un'<strong>amica</strong> (amiga) · un'<strong>ora</strong> (hora)</div>
  </div>
</div>
<div class="tabela-plural">📌 <strong>Plural:</strong> IL → <strong>I</strong> &nbsp;·&nbsp; LO → <strong>GLI</strong> &nbsp;·&nbsp; LA → <strong>LE</strong> &nbsp;·&nbsp; L' → <strong>GLI</strong> (masc.) ou <strong>LE</strong> (fem.)</div>`,

  // ── NMA em linguagem de conversa ───────────────────────
  alerta: 'Quando você chega na Itália e pede "un caffè", está certo. Mas se pedir "uno caffè" — todo italiano sorri. Um artigo errado é o primeiro sinal de quem não sabe o idioma.',

  inventario: [
    'IL e UN — para palavras masculinas que começam por letra normal',
    'LO e UNO — para palavras masculinas que começam por ST, SP, SC, Z...',
    'LA e UNA — para palavras femininas que começam por consoante',
    "L' e UN' — para qualquer palavra que começa por vogal (a, e, i, o, u)",
    'No plural: IL vira I · LO vira GLI · LA vira LE',
  ],

  definicao: {
    fenomeno: 'il gatto · la pizza · lo zaino · l\'amico',
    causa:    'Por que 4 artigos diferentes? Estão falando de coisas diferentes?',
    conceito: 'Não! São 4 formas de dizer "o/a" em italiano. Qual usar depende do gênero da palavra (masculino ou feminino) e da letra com que ela começa.',
  },

  tecnica: `Como escolher o artigo em 3 passos simples:

**Passo 1** — A palavra é masculina ou feminina?
(Se não souber, consulte o dicionário ou veja a tabela acima)

**Passo 2** — Olhe a primeira letra da palavra:
- Começa por **ST, SP, SC, SN, SL, Z, GN, PS**? → use **LO / GLI / UNO**
- Começa por **vogal (A, E, I, O, U)**? → use **L' / GLI ou LE / UN'**
- Todos os outros casos? → use **IL / LA / I / LE / UN / UNA**

**Passo 3** — Singular ou plural?
- Masculino: IL → I · LO → GLI
- Feminino: LA → LE · L' → LE (ou GLI se masc.)`,

  exemplos_prc: [
    {
      oracao:   'Il libro è sul tavolo.',
      pergunta: 'LIBRO começa por qual letra? É masculino ou feminino?',
      resposta: 'Começa por L (letra normal). É masculino (livro = masc. em italiano).',
      conclusao: 'Masculino + letra normal → IL. "il libro" ✓',
    },
    {
      oracao:   'Lo zaino è pesante.',
      pergunta: 'ZAINO começa por qual letra? Por que LO e não IL?',
      resposta: 'Começa por Z. Palavras com Z sempre usam LO, não IL.',
      conclusao: 'Masculino + Z → LO. "lo zaino" ✓ (pesante = pesado)',
    },
    {
      oracao:   'La pizza è buonissima!',
      pergunta: 'PIZZA começa por qual letra? É masculino ou feminino?',
      resposta: 'Começa por P (consoante normal). É feminino.',
      conclusao: 'Feminino + consoante → LA. "la pizza" ✓',
    },
    {
      oracao:   "Un'amica di Marco abita qui.",
      pergunta: 'AMICA começa por vogal ou consoante? É masculino ou feminino?',
      resposta: 'Começa por A (vogal!). É feminino (amiga).',
      conclusao: "Feminino + vogal → UN' (com apostrofo). \"un'amica\" ✓ (abita = mora)",
    },
  ],

  ponte: `Em português você diz: "o gato / a pizza / o estudante / o amigo" — simples, né?

Em italiano funciona igual, mas a letra inicial da palavra também muda o artigo:
- "o gato" → **il gatto** (g = letra normal → IL)
- "o estudante" → **lo studente** (st = começa por S+consoante → LO, não IL)
- "a pizza" → **la pizza** (feminino + consoante → LA)
- "o amigo" → **l'amico** (começa por vogal → L')

**Armadilhas para brasileiros:**
- "il PROBLEMA" (não "la problema" — problema é masculino em italiano!)
- "la MANO" (não "il mano" — mão é feminino em italiano!)
- "uno STUDENTE" (não "un studente" — ST exige UNO, não UN)`,

  coda: 'Daqui em diante: aprenda cada palavra nova COM o artigo. Não diga só "gatto" — diga sempre "il gatto". O artigo FAZ PARTE da palavra.',

  observacao_cards: [
    { italiano: 'il gatto', traducao: 'o gato', artigo: 'il', genero: 'masculino', motivo: 'Masculino + letra normal (g) → IL' },
    { italiano: 'lo zaino', traducao: 'a mochila', artigo: 'lo', genero: 'masculino', motivo: 'Masculino + Z → LO' },
    { italiano: 'la pizza', traducao: 'a pizza', artigo: 'la', genero: 'feminino', motivo: 'Feminino + consoante → LA' },
    { italiano: "l'amico", traducao: 'o amigo', artigo: "l'", genero: 'masculino', motivo: "Começa por vogal → L'" }
  ],

  armadilhas: [
    { errado: 'la problema', certo: 'il problema', motivo: '"problema" é masculino em italiano' },
    { errado: 'il mano', certo: 'la mano', motivo: '"mão" é feminino em italiano' },
    { errado: 'un studente', certo: 'uno studente', motivo: 'ST exige UNO, não UN' }
  ],

  // ── Exercícios ─────────────────────────────────────────
  exercicios: [

    // ── BLOCO 1: escolha — reconhecimento (ex 1–5) ─────
    {
      tipo: 'escolha',
      pergunta: 'Qual é o artigo certo?\n\n"Questo è ___ libro di italiano."\n(= Este é um livro de italiano.)',
      opcoes: ['un', 'uno', 'una', 'il'],
      resposta: 0,
      explicacao: 'LIBRO começa por L (letra normal) e é masculino → use UN. "Uno" é só para ST, Z, SP... "Una" é só para feminino. ✓ un libro.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Qual é o artigo certo?\n\n"Sul tavolo c\'è ___ penna rossa."\n(= Na mesa tem uma caneta vermelha.)',
      opcoes: ['un', 'uno', 'una', 'il'],
      resposta: 2,
      explicacao: 'PENNA (caneta) é feminino e começa por P (consoante) → use UNA. "Un/uno" são só para masculino. ✓ una penna.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Qual é o artigo certo?\n\n"Marco è ___ studente universitario."\n(= Marco é um estudante universitário.)',
      opcoes: ['un', 'uno', 'una', 'il'],
      resposta: 1,
      explicacao: 'STUDENTE começa por ST → obrigatoriamente UNO, nunca "un". Regra: ST, SP, SC, SN, Z, GN, PS → sempre UNO. ✓ uno studente.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Qual é o artigo certo?\n\n"___ pizza napoletana è famosa nel mondo."\n(= A pizza napolitana é famosa no mundo.)',
      opcoes: ['Il', 'Lo', 'La', "L'"],
      resposta: 2,
      explicacao: 'PIZZA é feminino (como "a pizza" em português) e começa por P → LA. Artigo DEFINIDO porque falamos da pizza em geral. ✓ La pizza.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Qual é o artigo certo?\n\n"Dove sono ___ occhiali di Sofia?"\n(= Onde estão os óculos de Sofia?\nocchiali = óculos)',
      opcoes: ['i', 'gli', 'le', "l'"],
      resposta: 1,
      explicacao: 'OCCHIALI começa por O (vogal!) e é masculino plural → GLI. Regra: masculino plural + vogal = GLI. Compare: i libri (L = consoante) ≠ gli occhiali (O = vogal). ✓ gli occhiali.',
    },

    // ── BLOCO 2: digitar — produção (ex 6–10) ──────────
    {
      tipo: 'digitar',
      pergunta: 'Complete com o artigo DEFINIDO:\n\n"In Italia, ___ pizza è deliziosa!"\n(= Na Itália, a pizza é deliciosa!)',
      resposta: 'la pizza',
      dica: 'PIZZA = feminino, começa por P (consoante) — consulte a tabela!',
      explicacao: 'PIZZA é feminino + começa por P → LA. "La pizza" ✓. Dica: pense em português "A pizza" → em italiano "La pizza". Mesma lógica!',
      variantes: ['la'],
    },
    {
      tipo: 'digitar',
      pergunta: 'Complete com o artigo INDEFINIDO:\n\n"Ho ___ zaino rosso."\n(= Tenho uma mochila vermelha.\nzaino = mochila, rosso = vermelho)',
      resposta: 'uno zaino',
      dica: 'ZAINO começa por Z — veja a linha amarela na tabela!',
      explicacao: 'ZAINO começa por Z → obrigatoriamente UNO (nunca "un"). Regra amarela: Z, ST, SP... → sempre UNO. ✓ Ho uno zaino.',
      variantes: ['uno'],
    },
    {
      tipo: 'digitar',
      pergunta: 'Complete com o artigo DEFINIDO PLURAL:\n\n"In classe ci sono ___ studenti."\n(= Na aula tem os estudantes.)',
      resposta: 'gli studenti',
      dica: 'STUDENTI começa por ST — veja a linha amarela!',
      explicacao: 'STUDENTI (plural de studente) começa por ST → GLI. Linha amarela no plural: LO vira GLI. ✓ gli studenti.',
      variantes: ['gli'],
    },
    {
      tipo: 'digitar',
      pergunta: "Complete com o artigo INDEFINIDO:\n\n\"Ho ___ amica italiana. Si chiama Giulia.\"\n(= Tenho uma amiga italiana. Ela se chama Giulia.)",
      resposta: "un'amica",
      dica: 'AMICA começa por A (vogal!) e é feminino — veja a linha verde!',
      explicacao: "AMICA começa por A (vogal) e é feminino → UN' (com apostrofo). Linha verde: qualquer vogal = L' ou UN'. ✓ un'amica.",
      variantes: ["un'amica", "un' amica"],
    },
    {
      tipo: 'digitar',
      pergunta: 'Complete com o artigo DEFINIDO PLURAL:\n\n"Sul tavolo ci sono ___ libri di Marco."\n(= Na mesa estão os livros de Marco.)',
      resposta: 'i libri',
      dica: 'LIBRI (= livros) começa por L (letra normal) — linha azul no plural!',
      explicacao: 'LIBRI começa por L (consoante normal) e é masculino plural → I. Linha azul no plural: IL vira I. ✓ i libri.',
      variantes: ['i'],
    },

    // ── BLOCO 3: revelar — mini-diálogos (ex 11–14) ────
    {
      tipo: 'revelar',
      pergunta: 'Na aula — complete os artigos. Tente antes de revelar!\n\n«In classe c\'è ___ tavolo grande.\nSul tavolo c\'è ___ libro e ___ penna.\n___ libro è rosso, ___ penna è blu.»\n\n(tavolo=mesa · libro=livro · penna=caneta · rosso=vermelho · blu=azul)',
      resposta: 'un · un · una · Il · la',
      explicacao: '"un tavolo, un libro, una penna" = primeira vez que menciona → artigo INDEFINIDO. "Il libro, la penna" = segunda menção, já sabemos de qual → artigo DEFINIDO. Padrão: primeira vez = UN/UNA, depois = IL/LA.',
    },
    {
      tipo: 'revelar',
      pergunta: 'Apresentando alguém — complete os artigos:\n\n«Questo è ___ mio amico Marco.\nÈ ___ studente di medicina.\n___ sua università è a Roma.»\n\n(questo=este · amico=amigo · medicina=medicina · università=universidade)',
      resposta: 'il · uno · La',
      explicacao: '"il mio amico" = possessivo masculino → IL. "uno studente" = ST → UNO. "La sua università" = possessivo feminino → LA. Em italiano, com possessivos (meu, seu, nosso) o artigo é quase sempre obrigatório!',
    },
    {
      tipo: 'revelar',
      pergunta: 'A família — complete os artigos:\n\n«Sofia ha ___ mamma e ___ papà.\n___ mamma si chiama Anna, ___ papà si chiama Luca.\nHa anche ___ fratello.»\n\n(ha=tem · mamma=mãe · papà=pai · fratello=irmão)',
      resposta: 'una · un · La · il · un',
      explicacao: '"una mamma, un papà, un fratello" = primeira menção → INDEFINIDO. "La mamma, il papà" = segunda menção → DEFINIDO. Este é o padrão mais comum: primeira vez = indefinido, depois = definido.',
    },
    {
      tipo: 'revelar',
      pergunta: 'Na Itália — complete os artigos:\n\n«Roma è ___ città bellissima.\n___ Colosseo è famoso in tutto il mondo.\nE ___ gelato italiano è il migliore del mondo!»\n\n(città=cidade · bellissima=belíssima · famoso=famoso · gelato=sorvete · migliore=melhor)',
      resposta: "una · Il · il",
      explicacao: '"una città" = indefinido (uma de muitas cidades bonitas). "Il Colosseo" = lugar único e famoso → sempre definido. "il gelato" = produto famoso em geral → definido. Lugares e produtos famosos únicos = sempre IL/LA.',
    },

    // ── BLOCO 4: síntese — tradução (ex 15) ────────────
    {
      tipo: 'digitar',
      pergunta: 'Traduza para o italiano:\n\n"Tenho um gato e uma mochila velha."\n\n(gatto = gato · zaino = mochila · vecchio = velho)',
      resposta: 'Ho un gatto e uno zaino vecchio.',
      dica: 'GATTO: letra normal → UN | ZAINO: começa por Z → UNO',
      explicacao: '"un gatto" = G é letra normal → UN. "uno zaino" = Z → UNO (não "un"!). O artigo muda por causa da primeira letra de CADA palavra. ✓ Ho un gatto e uno zaino vecchio.',
      variantes: [
        'Ho un gatto e uno zaino vecchio',
        'Ho uno zaino vecchio e un gatto.',
        'Ho uno zaino vecchio e un gatto',
      ],
    },
  ],
};

// ── a1-lez2 ── Il presente indicativo ──────────────────────
const lez2 = {
  id:       'a1-lez2',
  titulo:   'Il presente indicativo',
  subtitulo:'Como dizer o que você faz agora, todo dia ou em breve',
  nivel:    'A1',

  // ── Tabela visual (cola durante os exercícios) ──────────
  tabela_visual: `<p class="tabela-intro">Use durante os exercícios — a terminação do verbo já diz quem faz a ação!</p>
<div class="artigo-cards">
  <div class="artigo-card ac-azul">
    <div class="ac-titulo">🔵 -ARE</div>
    <div class="ac-regra">falar, comer, morar, estudar...<br><small>parlare · mangiare · abitare · studiare</small></div>
    <div class="ac-exemplos">
      eu → parl<strong>o</strong> · você → parl<strong>i</strong> · ele/ela → parl<strong>a</strong><br>
      nós → parl<strong>iamo</strong> · vocês → parl<strong>ate</strong> · eles → parl<strong>ano</strong>
    </div>
  </div>
  <div class="artigo-card ac-verde">
    <div class="ac-titulo">🟢 -ERE</div>
    <div class="ac-regra">ler, escrever, viver, pegar...<br><small>leggere · scrivere · vivere · prendere</small></div>
    <div class="ac-exemplos">
      eu → legg<strong>o</strong> · você → legg<strong>i</strong> · ele/ela → legg<strong>e</strong><br>
      nós → legg<strong>iamo</strong> · vocês → legg<strong>ete</strong> · eles → legg<strong>ono</strong>
    </div>
  </div>
  <div class="artigo-card ac-rosa">
    <div class="ac-titulo">🔴 -IRE</div>
    <div class="ac-regra">dormir, partir, entender...<br><small>dormire · partire · capire · finire</small></div>
    <div class="ac-exemplos">
      eu → dorm<strong>o</strong> · você → dorm<strong>i</strong> · ele/ela → dorm<strong>e</strong><br>
      nós → dorm<strong>iamo</strong> · vocês → dorm<strong>ite</strong> · eles → dorm<strong>ono</strong>
    </div>
  </div>
  <div class="artigo-card ac-cinza">
    <div class="ac-titulo">⚠️ Irregulares — decorar à parte!</div>
    <div class="ac-exemplos">
      <strong>essere</strong> (ser/estar): sono · sei · <strong>è</strong> · siamo · siete · sono<br>
      <strong>avere</strong> (ter): ho · hai · ha · abbiamo · avete · hanno<br>
      <strong>fare</strong> (fazer): faccio · fai · fa · facciamo · fate · fanno<br>
      <strong>andare</strong> (ir): vado · vai · va · andiamo · andate · vanno
    </div>
  </div>
</div>
<div class="tabela-plural">📌 <strong>Como usar:</strong> Tire -ARE/-ERE/-IRE e adicione a terminação certa. Ex: parl<em>are</em> → parl + <strong>o</strong> = <strong>parlo</strong> (eu falo)</div>`,

  // ── NMA em linguagem de conversa ───────────────────────
  alerta: 'Em italiano, "Parlo" já significa "Eu falo" — sem precisar falar "eu". A terminação da palavra (-o, -i, -a...) já conta quem faz a ação. Por isso os italianos falam mais rápido!',

  inventario: [
    'Verbos terminados em -ARE: parlare (falar), mangiare (comer), studiare (estudar)',
    'Verbos terminados em -ERE: leggere (ler), scrivere (escrever), prendere (pegar)',
    'Verbos terminados em -IRE: dormire (dormir), finire (terminar), capire (entender)',
    'Verbos irregulares (decorar!): essere (ser/estar), avere (ter), fare (fazer), andare (ir)',
    'Segredo: em italiano não precisa falar "eu/você/ele" — a terminação já diz!',
  ],

  definicao: {
    fenomeno: 'Parlo italiano. (Eu falo italiano.)\nParli italiano. (Você fala italiano.)\nParla italiano. (Ele/ela fala italiano.)',
    causa:    'Por que "parlo", "parli" e "parla"? Cadê o "eu", "você", "ele"?',
    conceito: 'A terminação do verbo já identifica quem faz a ação! Em italiano, o "eu/você/ele" é opcional — a terminação diz tudo. Isso facilita (você fala menos palavras) mas precisa aprender as terminações.',
  },

  tecnica: `Como conjugar um verbo regular em 2 passos:

**Passo 1** — Tire a terminação do infinitivo:
- PARL**ARE** → PARL- (tire o -ARE)
- LEGG**ERE** → LEGG- (tire o -ERE)
- DORM**IRE** → DORM- (tire o -IRE)

**Passo 2** — Adicione a terminação certa (consulte a tabela!):

| Quem faz? | -ARE | -ERE | -IRE |
|-----------|------|------|------|
| eu (io)       | -**o** | -**o** | -**o** |
| você (tu)     | -**i** | -**i** | -**i** |
| ele/ela       | -**a** | -**e** | -**e** |
| nós (noi)     | -**iamo** | -**iamo** | -**iamo** |
| vocês (voi)   | -**ate** | -**ete** | -**ite** |
| eles (loro)   | -**ano** | -**ono** | -**ono** |

**Para irregulares** (essere, avere, fare, andare): não tem jeito, precisa decorar. Veja a linha cinza na tabela!`,

  exemplos_prc: [
    {
      oracao:   'Studio italiano ogni giorno.',
      pergunta: 'STUDIARE: quem faz a ação? Como conjugar?',
      resposta: 'Não tem sujeito explícito → é "eu" (io). -ARE + eu = -o. STUDI + O = STUDIO.',
      conclusao: '"Studio" = eu estudo. A terminação -O diz que sou eu. (ogni giorno = todo dia)',
    },
    {
      oracao:   'Marco mangia la pizza ogni venerdì.',
      pergunta: 'MANGIARE: por que "mangia" e não "mangio" ou "mangiano"?',
      resposta: 'Marco = ele. -ARE + ele/ela = -a. MANGI + A = MANGIA.',
      conclusao: '"Mangia" = ele come. Terminação -A = ele/ela. (venerdì = sexta-feira)',
    },
    {
      oracao:   'Noi abitiamo a Roma.',
      pergunta: 'ABITARE: por que "abitiamo" para "nós"?',
      resposta: 'Nós = noi. -ARE + noi = -iamo. ABIT + IAMO = ABITIAMO.',
      conclusao: '"Abitiamo" = nós moramos. Terminação -IAMO = nós. (abitare = morar)',
    },
    {
      oracao:   'Dove vai con tanta fretta?',
      pergunta: '"Vai" — de qual verbo vem? Por que não segue a regra?',
      resposta: 'Vem de ANDARE (ir) — é irregular! Não segue -ARE. Paradigma: vado/vai/va/andiamo/andate/vanno.',
      conclusao: '"Vai" = você vai. ANDARE é irregular — memorize como vocabulário. (fretta = pressa)',
    },
  ],

  ponte: `Em português você fala "EU falo / VOCÊ fala / ELE fala" — sempre com o pronome.

Em italiano, o pronome é OPCIONAL porque a terminação já diz tudo:
- "falo" → **parlo** (sem "eu" — o -O já diz que sou eu)
- "você fala" → **parli** (sem "você" — o -I já diz que é você)
- "ele fala" → **parla** (sem "ele" — o -A já diz que é ele)

Quando usar o pronome em italiano? Só para dar ênfase:
"**Io** vado a Roma, **tu** rimani qui." (EU vou a Roma, VOCÊ fica aqui — enfatizando a diferença)

**Cuidado:** "essere" em italiano é tanto "ser" quanto "estar"!
- "Sono italiano" = Sou italiano (SER)
- "Sono stanco" = Estou cansado (ESTAR)
Um verbo para os dois!`,

  coda: 'Todo dia, fale em voz alta 3 verbos completos: eu falo / você fala / ele fala / nós falamos / vocês falam / eles falam. Em 5 minutos, a terminação vira automática.',

  observacao_cards: [
    { italiano: 'io parlo', traducao: 'eu falo', artigo: '-o', genero: 'io', motivo: 'Verbo -ARE no presente: termina em -O para eu.' },
    { italiano: 'tu parli', traducao: 'você fala', artigo: '-i', genero: 'tu', motivo: 'Verbo -ARE no presente: termina em -I para você.' },
    { italiano: 'lui parla', traducao: 'ele fala', artigo: '-a', genero: 'ele/ela', motivo: 'Verbo -ARE no presente: termina em -A para ele/ela.' },
    { italiano: 'noi parliamo', traducao: 'nós falamos', artigo: '-iamo', genero: 'nós', motivo: 'Verbo -ARE no presente: termina em -IAMO para nós.' }
  ],

  armadilhas: [
    { errado: 'io parlo italiano', certo: 'parlo italiano', motivo: 'Não precisa usar "io" em italiano — a terminação já diz tudo.' },
    { errado: 'noi parliano', certo: 'noi parliamo', motivo: 'A terminação correta para nós é -iamo, não -iano.' },
    { errado: 'voi parli', certo: 'voi parlate', motivo: 'Para "voi" (vocês) a terminação é -ate para verbos -ARE.' }
  ],

  // ── Exercícios ─────────────────────────────────────────
  exercicios: [

    // ── BLOCO 1: escolha — reconhecimento (ex 1–6) ─────
    {
      tipo: 'escolha',
      pergunta: 'Qual a forma certa?\n\n"Giulia ___ italiano all\'università."\n(= Giulia estuda italiano na universidade.)',
      opcoes: ['studia', 'studi', 'studiate', 'studio'],
      resposta: 0,
      explicacao: 'Giulia = ela. STUDIARE é -ARE. Ela/-ARE → terminação -A. STUDI + A = STUDIA. ✓ studia. ("studi" seria você, "studio" seria eu, "studiate" seria vocês)',
    },
    {
      tipo: 'escolha',
      pergunta: 'Qual a forma certa?\n\n"Io non ___ il caffè, preferisco il tè."\n(= Eu não bebo café, prefiro chá.)',
      opcoes: ['bevo', 'bevi', 'beve', 'beviamo'],
      resposta: 0,
      explicacao: 'Eu = io. BERE (beber) é irregular! Paradigma: BEVO / bevi / beve / beviamo / bevete / bevono. Eu → BEVO. ✓ bevo. ("bevi" seria você)',
    },
    {
      tipo: 'escolha',
      pergunta: 'Qual a forma certa?\n\n"Marco e Luca ___ la pizza ogni venerdì."\n(= Marco e Luca comem pizza toda sexta.)',
      opcoes: ['mangiano', 'mangia', 'mangiate', 'mangiamo'],
      resposta: 0,
      explicacao: 'Marco e Luca = eles (loro). MANGIARE é -ARE. Eles/-ARE → terminação -ANO. MANGI + ANO = MANGIANO. ✓ mangiano. ("mangia" seria ele/ela)',
    },
    {
      tipo: 'escolha',
      pergunta: 'Qual a forma certa?\n\n"— Voi ___ l\'italiano da quanto tempo?"\n(= Vocês estudam italiano há quanto tempo?)',
      opcoes: ['studiate', 'studiano', 'studiamo', 'studi'],
      resposta: 0,
      explicacao: 'Vocês = voi. STUDIARE é -ARE. Vocês/-ARE → terminação -ATE. STUDI + ATE = STUDIATE. ✓ studiate. ("studiano" seria eles, "studiamo" seria nós)',
    },
    {
      tipo: 'escolha',
      pergunta: 'Qual a forma certa?\n\n"Noi ___ a Roma ogni estate."\n(= Nós vamos a Roma todo verão.\nestate = verão)',
      opcoes: ['andiamo', 'vanno', 'vado', 'andate'],
      resposta: 0,
      explicacao: 'Nós = noi. ANDARE (ir) é irregular! Paradigma: vado/vai/va/ANDIAMO/andate/vanno. Nós → ANDIAMO. ✓ andiamo. (Para "nós" e "vocês" o ANDARE usa a raiz "and-", diferente do resto)',
    },
    {
      tipo: 'escolha',
      pergunta: 'Qual a forma certa?\n\n"— Tu ___ molto bene l\'italiano!"\n(= Você fala muito bem italiano!)',
      opcoes: ['parli', 'parla', 'parlate', 'parlo'],
      resposta: 0,
      explicacao: 'Você = tu. PARLARE é -ARE. Você/-ARE → terminação -I. PARL + I = PARLI. ✓ parli. ("parla" seria ele/ela, "parlo" seria eu)',
    },

    // ── BLOCO 2: digitar — produção (ex 7–12) ──────────
    {
      tipo: 'digitar',
      pergunta: 'Complete o verbo:\n\n"Maria ___ (abitare = morar) a Roma con la famiglia."\n(= Maria mora em Roma com a família.)',
      resposta: 'abita',
      dica: 'Maria = ela. ABITARE é -ARE. Consulte a tabela!',
      explicacao: 'Maria = ela. ABITARE (-ARE) + ela → terminação -A. ABIT + A = ABITA. ✓ abita.',
    },
    {
      tipo: 'digitar',
      pergunta: 'Complete o verbo:\n\n"— Come ti chiami?\n— Mi ___ (chiamare = chamar-se) Sofia."\n(= Como você se chama? — Me chamo Sofia.)',
      resposta: 'chiamo',
      dica: 'Eu = io. CHIAMARE é -ARE. O "mi" já está na frase!',
      explicacao: 'Eu = io. CHIAMARE (-ARE) + eu → -O. CHIAM + O = CHIAMO. "Mi chiamo" = Me chamo. O "mi" fica antes, você só conjuga o verbo. ✓ chiamo.',
    },
    {
      tipo: 'digitar',
      pergunta: 'Complete o verbo:\n\n"Ogni giorno noi ___ (mangiare = comer) la pasta."\n(= Todo dia nós comemos macarrão.)',
      resposta: 'mangiamo',
      dica: 'Nós = noi. MANGIARE é -ARE. Consulte a tabela!',
      explicacao: 'Nós = noi. MANGIARE (-ARE) + nós → -IAMO. MANGI + AMO = MANGIAMO. ✓ mangiamo.',
    },
    {
      tipo: 'digitar',
      pergunta: 'Complete o verbo:\n\n"I bambini ___ (dormire = dormir) otto ore ogni notte."\n(= As crianças dormem oito horas toda noite.\nbambini = crianças · ore = horas · notte = noite)',
      resposta: 'dormono',
      dica: 'Crianças = eles (loro). DORMIRE é -IRE (linha rosa na tabela).',
      explicacao: 'Eles (loro). DORMIRE (-IRE) + eles → -ONO. DORM + ONO = DORMONO. ✓ dormono.',
    },
    {
      tipo: 'digitar',
      pergunta: 'Complete o verbo:\n\n"— Quanto ___ (costare = custar) un caffè in Italia?"\n(= Quanto custa um café na Itália?)',
      resposta: 'costa',
      dica: 'O café = ele (il caffè). COSTARE é -ARE.',
      explicacao: 'O café = ele. COSTARE (-ARE) + ele → -A. COST + A = COSTA. "Quanto costa?" = Quanto custa? — uma das frases mais úteis na Itália! ✓ costa.',
    },
    {
      tipo: 'digitar',
      pergunta: 'Complete o verbo:\n\n"Noi ___ (essere = ser/estar) pronti per la lezione!"\n(= Nós estamos prontos para a aula!)',
      resposta: 'siamo',
      dica: 'Nós = noi. ESSERE é irregular — veja a linha cinza na tabela!',
      explicacao: 'ESSERE é irregular! Paradigma: sono / sei / è / SIAMO / siete / sono. Nós → SIAMO. "Siamo" = nós somos / nós estamos. ✓ siamo.',
    },

    // ── BLOCO 3: revelar — mini-diálogos (ex 13–16) ────
    {
      tipo: 'revelar',
      pergunta: 'Um dia típico — complete os verbos (consulte a tabela!):\n\n«Marco ___ (svegliarsi → si sveglia = acorda) alle sette.\n___ (fare → fa = faz) colazione.\nPoi ___ (andare → va = vai) all\'università.\nAll\'università ___ (studiare → studia = estuda) italiano.»',
      resposta: 'si sveglia · fa · va · studia',
      explicacao: 'Todos os verbos falam de Marco (ele). si sveglia = verbo reflexivo irregular. fa = FARE irregular (ele faz). va = ANDARE irregular (ele vai). studia = STUDIARE -ARE regular (ele estuda). Anote: FARE e ANDARE são irregulares — decorar!',
    },
    {
      tipo: 'revelar',
      pergunta: 'Em família — complete os verbos:\n\n«— Papà, dove ___ (lavorare = trabalhar) tu?\n— Io ___ (lavorare) in banca.\n— E tu, cosa ___ (studiare) all\'università?\n— ___ (studiare) lingue straniere!\n(lingue straniere = línguas estrangeiras)»',
      resposta: 'lavori · lavoro · studi · Studio',
      explicacao: 'lavori = você (tu) -ARE → -I. lavoro = eu (io) -ARE → -O. studi = você (tu) -ARE → -I. Studio = eu (io) -ARE → -O (maiúsculo porque é início de frase). Veja como a terminação muda: eu = -O, você = -I.',
    },
    {
      tipo: 'revelar',
      pergunta: 'Num bar italiano — complete os verbos:\n\n«— ___ (voi, volere = querer) un caffè?\n— Sì, grazie! Io ___ (volere) un caffè e Mario ___ (volere) un cappuccino.»',
      resposta: 'Volete · voglio · vuole',
      explicacao: 'VOLERE é irregular! Paradigma: voglio / vuoi / vuole / vogliamo / VOLETE / vogliono. Vocês (voi) → VOLETE. Eu (io) → VOGLIO. Ele (lui) → VUOLE. ✓ Volete · voglio · vuole.',
    },
    {
      tipo: 'revelar',
      pergunta: 'Na escola de idiomas — complete:\n\n«Io e Marco ___ (studiare) italiano insieme.\nLa professoressa ___ (chiamarsi) Paola.\nLei ___ (essere) molto brava!\nVoi ___ (capire = entender) tutto?\n(insieme=juntos · brava=ótima · tutto=tudo)»',
      resposta: 'studiamo · si chiama · è · capite',
      explicacao: 'studiamo = nós (noi) -ARE → -IAMO. si chiama = reflexivo 3ª pess. (ela se chama). è = ESSERE irregular (ela é/está). capite = vocês (voi) -IRE → -ITE. ✓',
    },

    // ── BLOCO 4: síntese — tradução (ex 17–18) ─────────
    {
      tipo: 'digitar',
      pergunta: 'Complete os dois verbos:\n\n"Di solito io ___ (mangiare) la pizza e tu ___ (bere) il vino."\n(= Normalmente eu como pizza e você bebe vinho.\ndi solito = normalmente · vino = vinho)',
      resposta: 'mangio · bevi',
      dica: 'mangiare: eu -ARE | bere: você (irregular!)',
      explicacao: '"mangio" = eu (io) -ARE → -O. "bevi" = você (tu), BERE irregular → BEVI. Dois sujeitos diferentes = duas terminações diferentes. ✓ mangio · bevi.',
      variantes: ['mangio, bevi', 'mangio · bevi', 'mangio  bevi'],
    },
    {
      tipo: 'digitar',
      pergunta: 'Traduza para o italiano:\n\n"Nós moramos em Roma e estudamos medicina."\n\n(abitare = morar · medicina = medicina)',
      resposta: 'Abitiamo a Roma e studiamo medicina.',
      dica: 'Nós = noi. Dois verbos -ARE. Cidades não têm artigo!',
      explicacao: '"abitiamo" = nós -ARE → -IAMO. "studiamo" = nós -ARE → -IAMO. "a Roma" sem artigo — cidades sempre sem artigo. O "nós" (noi) pode ser omitido — a terminação -IAMO já diz! ✓',
      variantes: [
        'Noi abitiamo a Roma e studiamo medicina.',
        'abitiamo a Roma e studiamo medicina.',
        'Abitiamo a Roma e studiamo medicina',
      ],
    },
  ],
};

// ── Aplicar no grammar.json ────────────────────────────────
const modulo0 = grammar.moduli[0];

function aplicar(novaUnidade) {
  const idx = modulo0.unidades.findIndex(u => u.id === novaUnidade.id);
  if (idx === -1) { console.error(`Unidade ${novaUnidade.id} não encontrada!`); process.exit(1); }
  modulo0.unidades[idx] = { ...modulo0.unidades[idx], ...novaUnidade };
  delete modulo0.unidades[idx].teoria;
  delete modulo0.unidades[idx].exemplos;
  console.log(`✓ ${novaUnidade.id}: ${novaUnidade.exercicios.length} exercícios · tabela_visual: ${!!novaUnidade.tabela_visual}`);
}

aplicar(lez1);
aplicar(lez2);

fs.writeFileSync(GRAMMAR_PATH, JSON.stringify(grammar, null, 2), 'utf8');
console.log('\ngrammar.json atualizado!');
