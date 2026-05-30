// ============================================================
// _piloto_lezioni.js
// Padrão didático para iniciantes ZERO em italiano:
//   • Vocabulário: APENAS cognatos (pizza, caffè) ou palavras
//     deduzíveis pelo português (libro=livro, gatto=gato, casa)
//   • Tradução entre parênteses para qualquer palavra nova
//   • Frases simples: só "è" e "c'è" na lez1; presente simples na lez2
//   • NMA teoria: 7 camadas, em português, sem jargão
//   • Exercícios: reconhecimento → produção → mini-diálogo → síntese
// ============================================================

const fs = require('fs');
const path = require('path');

const GRAMMAR_PATH = path.join(__dirname, 'grammar.json');
const grammar = JSON.parse(fs.readFileSync(GRAMMAR_PATH, 'utf8'));

// ── a1-lez1 ── Nome, Articolo e Aggettivo ──────────────────
const lez1 = {
  id: 'a1-lez1',
  titulo: 'Nome, Articolo e Aggettivo',
  subtitulo: 'Il cuore del nome italiano',
  nivel: 'A1',

  alerta: 'Sem artigo correto, um italiano entende o que você diz — mas sabe imediatamente que você é estrangeiro. O artigo é o primeiro teste visível do seu italiano.',

  inventario: [
    'Nomes masculinos (il/lo/un/uno) e femininos (la/una)',
    'Artigos definidos singulares: il · lo · la · l\'',
    'Artigos definidos plurais: i · gli · le',
    'Artigos indefinidos: un · uno · una · un\'',
    'Acordo do adjetivo com o nome',
  ],

  definicao: {
    fenomeno: 'il gatto · la pizza · lo studente · l\'amico',
    causa: 'Por que quatro artigos diferentes para quatro nomes?',
    conceito: 'O artigo concorda com o gênero (masc./fem.) e com a letra inicial do nome. O som da primeira letra decide entre il/lo ou la/l\'.',
  },

  tecnica: '1. Determine o gênero: masculino ou feminino.\n2. Olhe a primeira letra/som do nome:\n   • Masc. sing.: consoante normal → il | s+consoante, z, gn, ps → lo | vogal → l\'\n   • Fem. sing.: consoante → la | vogal → l\'\n3. No plural: il→i · lo→gli · la→le · l\'→i(masc.) ou le(fem.)\n4. Indefinido: il→un · lo→uno · la→una · l\'→un\'(fem.) ou un(masc.)',

  exemplos_prc: [
    {
      oracao: 'Il libro è sul tavolo.',
      pergunta: 'Por que "il" e não "lo" ou "la"?',
      resposta: '"libro" é masculino e começa por "l" — consoante normal',
      conclusao: 'Masc. sing. + consoante normal → il. (libro = livro)',
    },
    {
      oracao: 'Lo studente legge.',
      pergunta: 'Por que "lo" e não "il"?',
      resposta: '"studente" começa por "st" — s seguido de consoante (t)',
      conclusao: 'Masc. sing. + s+consoante → lo, nunca il. (studente = estudante)',
    },
    {
      oracao: 'La pizza è buonissima!',
      pergunta: 'Por que "la"?',
      resposta: '"pizza" é feminino e começa por consoante (p)',
      conclusao: 'Fem. sing. + consoante → la. Pizza é feminino em italiano.',
    },
    {
      oracao: 'Un\'amica di Marco abita qui.',
      pergunta: 'Por que "un\'" e não "una"?',
      resposta: '"amica" é feminino e começa por vogal (a)',
      conclusao: 'Art. indef. fem. + vogal: una → un\' (apostrofo). (amica = amiga)',
    },
  ],

  ponte: 'Em português: "o livro / a pizza" — em italiano: "il libro / la pizza". A lógica é a mesma!\nMas cuidado com as exceções: *il problema* (não "la" — problema é masculino em italiano), *la mano* (não "il" — mão é feminino), *il cinema* (masculino).\nOutro cuidado: "um estudante" em italiano → *uno studente* (não "un"), porque "st" exige "lo/uno".',

  coda: 'A partir de hoje: memorize cada palavra nova COM o artigo. Não "gatto" — mas "il gatto". Não "pizza" — mas "la pizza". O artigo é parte do vocabulário.',

  exercicios: [

    // ── BLOCO 1: escolha — reconhecimento (ex 1–5) ──────────
    // Vocabulário: APENAS cognatos e palavras deduzíveis
    {
      tipo: 'escolha',
      pergunta: 'Questo è ___ libro di italiano.\n(= Este é um livro de italiano.)',
      opcoes: ['un', 'uno', 'una', 'il'],
      resposta: 0,
      explicacao: '"libro" (livro) = masculino, começa por "l" (consoante normal) → art. indef. masc. = un. "uno" seria para s+consoante/z/gn/ps. "una" é feminino.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Sul tavolo c\'è ___ penna rossa.\n(= Na mesa tem uma caneta vermelha.)',
      opcoes: ['un', 'uno', 'una', 'il'],
      resposta: 2,
      explicacao: '"penna" (caneta) = feminino, começa por consoante (p) → art. indef. fem. = una. "un/uno" são masculinos. Feminino sempre: una (consoante) ou un\' (vogal).',
    },
    {
      tipo: 'escolha',
      pergunta: 'Marco è ___ studente universitario.\n(= Marco é um estudante universitário.)',
      opcoes: ['un', 'uno', 'una', 'il'],
      resposta: 1,
      explicacao: '"studente" (estudante) começa por "st" — s seguido de consoante → art. indef. masc. = uno. Compare: un libro (consoante normal) ≠ uno studente (s+C).',
    },
    {
      tipo: 'escolha',
      pergunta: '___ pizza napoletana è famosa in tutto il mondo.\n(= A pizza napolitana é famosa em todo o mundo.)',
      opcoes: ['Il', 'Lo', 'La', 'L\''],
      resposta: 2,
      explicacao: '"pizza" = feminino, começa por consoante (p) → art. def. fem. sing. = la. Aqui usamos art. DEFINIDO porque falamos da pizza napolitana em geral — um conceito conhecido.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Dove sono ___ occhiali di Sofia?\n(= Onde estão os óculos de Sofia?\nocchiali = óculos)',
      opcoes: ['i', 'gli', 'le', 'l\''],
      resposta: 1,
      explicacao: '"occhiali" (óculos) = masculino plural, começa por vogal (o) → gli. Regra: masc. pl. + vogal → gli (não i). Compare: i libri (consoante) ≠ gli occhiali (vogal).',
    },

    // ── BLOCO 2: digitar — produção (ex 6–10) ───────────────
    {
      tipo: 'digitar',
      pergunta: 'In Italia, ___ (art. def.) pizza è deliziosa!\n(= Na Itália, a pizza é deliciosa!)',
      resposta: 'la pizza',
      dica: 'pizza = feminino, começa por consoante',
      explicacao: '"pizza" = fem. + consoante → la. Art. definido porque falamos da pizza em geral (conceito conhecido). "la pizza" é uma das primeiras frases que você vai usar em italiano!',
      variantes: ['la'],
    },
    {
      tipo: 'digitar',
      pergunta: 'Ho ___ (art. ind.) zaino rosso.\n(= Tenho uma mochila vermelha.\nzaino = mochila, rosso = vermelho)',
      resposta: 'uno zaino',
      dica: 'zaino começa por z — atenção ao artigo!',
      explicacao: '"zaino" (mochila) começa por z → art. indef. masc. = uno (não "un"). Regra z: lo zaino (def.) → uno zaino (ind.).',
      variantes: ['uno'],
    },
    {
      tipo: 'digitar',
      pergunta: 'In classe ci sono ___ (art. def. pl.) studenti internazionali.\n(= Na aula tem os estudantes internacionais.)',
      resposta: 'gli studenti',
      dica: 'studenti = masc. pl., começa por "st"',
      explicacao: '"studenti" (estudantes) = masc. pl., começa por "st" (s+consoante) → gli. Cadeia: lo studente (sing.) → gli studenti (pl.).',
      variantes: ['gli'],
    },
    {
      tipo: 'digitar',
      pergunta: 'Ho ___ (art. ind.) amica italiana. Si chiama Giulia.\n(= Tenho uma amiga italiana. Ela se chama Giulia.)',
      resposta: "un'amica",
      dica: 'amica = feminino, começa por vogal (a)',
      explicacao: '"amica" (amiga) = fem. + vogal → art. indef. = un\' (apostrofo). "una amica" seria feio por causa da vogal dupla → un\'amica.',
      variantes: ["un'amica", "un' amica"],
    },
    {
      tipo: 'digitar',
      pergunta: 'Sul tavolo ci sono ___ (art. def. pl.) libri di Marco.\n(= Na mesa estão os livros de Marco.)',
      resposta: 'i libri',
      dica: 'libri = masc. pl., "l" = consoante normal',
      explicacao: '"libri" (livros) = masc. pl. + consoante normal (l) → i. Compare: i libri (consoante) / gli occhiali (vogal) / gli zaini (z).',
      variantes: ['i'],
    },

    // ── BLOCO 3: revelar — contexto real (ex 11–14) ─────────
    {
      tipo: 'revelar',
      pergunta: 'In classe (Na aula) — completa gli articoli:\n\n«In classe c\'è ___ tavolo grande.\nSul tavolo c\'è ___ libro e ___ penna.\n___ libro è rosso, ___ penna è blu.»\n\n(tavolo=mesa · grande=grande · libro=livro · penna=caneta · rosso=vermelho · blu=azul)',
      resposta: 'un · un · una · Il · la',
      explicacao: '"un tavolo, un libro, una penna" = artigo INDEFINIDO (primeira menção, não sabemos ainda qual). "Il libro, la penna" = artigo DEFINIDO (segunda menção — já sabemos de qual livro e de qual caneta falamos).',
    },
    {
      tipo: 'revelar',
      pergunta: 'Chi è? (Quem é?) — completa:\n\n«Questo è ___ mio amico Marco.\nÈ ___ studente di medicina.\n___ sua università è a Roma.»\n\n(questo=este · amico=amigo · medicina=medicina · università=universidade)',
      resposta: 'il · uno · La',
      explicacao: '"il mio amico" = possessivo masc. → artigo definido "il". "uno studente" = profissão com art. indef., s+C → uno. "La sua università" = possessivo fem. → artigo definido "la". (Com possessivos italianos, o artigo é quase sempre obrigatório.)',
    },
    {
      tipo: 'revelar',
      pergunta: 'La famiglia (A família) — completa:\n\n«Sofia ha ___ mamma e ___ papà.\n___ mamma si chiama Anna, ___ papà si chiama Luca.\nHa anche ___ fratello. ___ fratello si chiama Marco.»\n\n(ha=tem · mamma=mãe · papà=pai · fratello=irmão · si chiama=se chama)',
      resposta: 'una · un · La · il · un · Il',
      explicacao: '"una mamma, un papà, un fratello" = INDEFINIDO (primeira menção). "La mamma, il papà, Il fratello" = DEFINIDO (segunda menção — já sabemos quem são). Este é o padrão mais comum: indefinido na primeira vez, definido depois.',
    },
    {
      tipo: 'revelar',
      pergunta: 'In Italia (Na Itália) — completa:\n\n«Roma è ___ città bellissima.\n___ Colosseo è famoso in tutto il mondo.\nE ___ gelato italiano è il migliore del mondo!»\n\n(città=cidade · bellissima=belíssima · famoso=famoso · mondo=mundo · migliore=melhor)',
      resposta: "una · Il · il",
      explicacao: '"una città" = indefinido (uma de muitas cidades bonitas). "Il Colosseo" = definido (monumento único e conhecido). "il gelato" = definido (produto específico falado em geral). Nomes icônicos e únicos → sempre artigo definido.',
    },

    // ── BLOCO 4: digitar — síntese (ex 15) ──────────────────
    {
      tipo: 'digitar',
      pergunta: 'Traduza para o italiano:\n"Tenho um gato e uma mochila velha."\n\n(gatto=gato · zaino=mochila · vecchio=velho)',
      resposta: 'Ho un gatto e uno zaino vecchio.',
      dica: 'gatto: masc., consoante normal → un | zaino: masc., z → uno',
      explicacao: '"un gatto" (g = consoante normal → un). "uno zaino" (z → uno, não "un"). Observe: o mesmo objeto "mochila" muda o artigo de "un" para "uno" porque começa por z. Sempre verifique a PRIMEIRA LETRA da próxima palavra.',
      variantes: ['Ho un gatto e uno zaino vecchio', 'Ho uno zaino vecchio e un gatto.', 'Ho uno zaino vecchio e un gatto'],
    },
  ],
};

// ── a1-lez2 ── Il presente indicativo ──────────────────────
const lez2 = {
  id: 'a1-lez2',
  titulo: 'Il presente indicativo',
  subtitulo: 'L\'azione nel momento presente',
  nivel: 'A1',

  alerta: 'O presente italiano faz o trabalho de três tempos portugueses: "falo", "estou falando" e "vou falar agora". Um tempo. Uma forma. Dominar o presente é dominar 80% das conversas cotidianas.',

  inventario: [
    'Verbos regulares -ARE: parlare (falar), mangiare (comer), studiare (estudar)',
    'Verbos regulares -ERE: leggere (ler), scrivere (escrever), prendere (pegar/tomar)',
    'Verbos regulares -IRE: dormire (dormir), finire (terminar), capire (entender)',
    'Irregolari essenziais: essere (ser/estar), avere (ter), fare (fazer), andare (ir)',
    'Pro-drop: o pronome sujeito é opcional — a terminação já identifica a pessoa',
  ],

  definicao: {
    fenomeno: 'Parlo italiano. (Eu falo italiano.) / Parli italiano. (Você fala.) / Parla italiano. (Ele/ela fala.)',
    causa: 'Por que três formas diferentes se o verbo é o mesmo? E cadê o "eu/você/ele"?',
    conceito: 'A terminação do verbo identifica quem faz a ação. Por isso o italiano omite o pronome sujeito: a terminação já diz tudo. Isso se chama "pro-drop".',
  },

  tecnica: '1. Pegue o infinitivo: parlare, leggere, dormire.\n2. Retire a terminação: parl- / legg- / dorm-.\n3. Adicione a desinência correta:\n   -ARE → -o · -i · -a · -iamo · -ate · -ano\n   -ERE → -o · -i · -e · -iamo · -ete · -ono\n   -IRE → -o · -i · -e · -iamo · -ite · -ono\n4. Para irregolari (essere, avere, fare, andare): memorizar o paradigma completo — não há atalho.',

  exemplos_prc: [
    {
      oracao: 'Studio italiano ogni giorno.',
      pergunta: 'Como conjugar "studiare" para "io"?',
      resposta: 'studiare → retira -ARE → studi- → adiciona -o → studio',
      conclusao: '-ARE + io → -o. "studio" = eu estudo. Sem "io" — a terminação -o já diz que sou eu.',
    },
    {
      oracao: 'Marco mangia la pizza ogni venerdì.',
      pergunta: 'Por que "mangia" e não "mangiano"?',
      resposta: 'Marco = lui (3ª sing.). -ARE + lui/lei → -a: mangi+a = mangia',
      conclusao: '-ARE + lui/lei → -a. "mangia" = ele come. (venerdì = sexta-feira)',
    },
    {
      oracao: 'Noi abitiamo a Roma.',
      pergunta: 'Como conjugar -ARE para "noi"?',
      resposta: '-ARE + noi → -iamo: abit+iamo = abitiamo',
      conclusao: '-ARE + noi → -iamo. "abitiamo" = nós moramos. (abitare = morar)',
    },
    {
      oracao: 'Dove vai con tanta fretta?',
      pergunta: '"vai" — de que verbo vem? Por que não "vai" regular?',
      resposta: '"andare" (ir) é irregular: vado · vai · va · andiamo · andate · vanno',
      conclusao: 'andare é irregular. "vai" = você vai. (fretta = pressa — frase muito usada!)',
    },
  ],

  ponte: 'Pro-drop na prática: "Parlo italiano" = "Eu falo italiano" — o "io" é opcional. Em português informal também fazemos isso ("Falo português"), mas em italiano é regra, não exceção. USE o pronome só para ênfase: "Io vado a Roma, tu rimani qui." (Eu vou a Roma, você fica aqui.)\n\nCuidado com "essere": não é só "estar" — é também "ser". "Sono stanco" = "Estou cansado". "Sono italiano" = "Sou italiano". Um verbo para os dois!\n\n"Fare" (fazer) é totalmente irregular: faccio · fai · fa · facciamo · fate · fanno. Decore como vocabulário.',

  coda: 'Todo dia, conjugue 3 verbos novos em voz alta: io · tu · lui · noi · voi · loro. São 18 formas em 1 minuto. Depois de uma semana, o presente regular vira automático.',

  exercicios: [

    // ── BLOCO 1: escolha — reconhecimento (ex 1–6) ──────────
    {
      tipo: 'escolha',
      pergunta: 'Giulia ___ italiano all\'università.\n(= Giulia estuda italiano na universidade.)',
      opcoes: ['studia', 'studi', 'studiate', 'studio'],
      resposta: 0,
      explicacao: 'Giulia = lui/lei (3ª sing.). -ARE + lui/lei → -a: studi+a = studia. "studi" seria tu, "studiate" seria voi, "studio" seria io.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Io non ___ il caffè, preferisco il tè.\n(= Eu não bebo café, prefiro chá.)',
      opcoes: ['bevo', 'bevi', 'beve', 'beviamo'],
      resposta: 0,
      explicacao: '"bere" (beber) é irregular. Paradigma: bevo/bevi/beve/beviamo/bevete/bevono. io → bevo. "bevi" seria tu, "beve" seria lui/lei.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Marco e Luca ___ la pizza ogni venerdì.\n(= Marco e Luca comem pizza toda sexta-feira.)',
      opcoes: ['mangiano', 'mangia', 'mangiate', 'mangiamo'],
      resposta: 0,
      explicacao: '"Marco e Luca" = loro (3ª pl.). -ARE + loro → -ano: mangi+ano = mangiano. "mangia" seria lui/lei, "mangiate" seria voi.',
    },
    {
      tipo: 'escolha',
      pergunta: '— Voi ___ l\'italiano da quanto tempo?\n(= Vocês estudam italiano há quanto tempo?)',
      opcoes: ['studiate', 'studiano', 'studiamo', 'studi'],
      resposta: 0,
      explicacao: 'voi + -ARE → -ate: studi+ate = studiate. "studiano" seria loro (3ª pl.), "studiamo" seria noi, "studi" seria tu.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Noi ___ a Roma ogni estate.\n(= Nós vamos a Roma todo verão.\nestate = verão)',
      opcoes: ['andiamo', 'vanno', 'vado', 'andate'],
      resposta: 0,
      explicacao: '"andare" (ir) é irregular: vado/vai/va/andiamo/andate/vanno. noi → andiamo. Atenção: noi/voi retornam à raiz "and-", mas io/tu/lui/loro usam "v-".',
    },
    {
      tipo: 'escolha',
      pergunta: '— Tu ___ molto bene l\'italiano!\n(= Você fala muito bem italiano!)',
      opcoes: ['parli', 'parla', 'parlate', 'parlo'],
      resposta: 0,
      explicacao: 'tu + -ARE → -i: parl+i = parli. "parla" seria lui/lei, "parlo" seria io. Em italiano o "tu" é geralmente omitido — a terminação "-i" já diz que é você.',
    },

    // ── BLOCO 2: digitar — produção (ex 7–12) ───────────────
    {
      tipo: 'digitar',
      pergunta: 'Maria ___ (abitare) a Roma con la famiglia.\n(= Maria mora em Roma com a família.)',
      resposta: 'abita',
      dica: 'Maria = lui/lei; -ARE regular',
      explicacao: '"abitare" (morar) -ARE, lui/lei → -a: abit+a = abita. "Maria abita a Roma" — pro-drop: não repetimos "lei" porque "abita" já identifica a 3ª pessoa.',
    },
    {
      tipo: 'digitar',
      pergunta: '— Come ti chiami?\n— Mi ___ (chiamare) Sofia.\n(= Como você se chama? — Me chamo Sofia.)',
      resposta: 'chiamo',
      dica: 'io, -ARE regular; "mi" já está na frase',
      explicacao: '"chiamare" -ARE, io → -o: chiam+o = chiamo. "Mi chiamo" = Me chamo (literalmente: "me chamo"). O "mi" é o pronome reflexivo — já está na frase, você só conjuga o verbo.',
    },
    {
      tipo: 'digitar',
      pergunta: 'Ogni giorno noi ___ (mangiare) la pasta.\n(= Todo dia nós comemos macarrão.)',
      resposta: 'mangiamo',
      dica: 'noi, -ARE; atenção ao radical',
      explicacao: '"mangiare" -ARE, noi → -iamo: mangi+amo = mangiamo. Note: radical já termina em "i" (mangi-), então fica mangiamo (não "mangiamo" com dois "i").',
    },
    {
      tipo: 'digitar',
      pergunta: 'I bambini ___ (dormire) otto ore ogni notte.\n(= As crianças dormem oito horas toda noite.\nbambini=crianças · ore=horas · notte=noite)',
      resposta: 'dormono',
      dica: 'loro, -IRE (grupo regular, NÃO -isc-)',
      explicacao: '"dormire" -IRE regular (não -isc-), loro → -ono: dorm+ono = dormono. Grupo "finire" usaria -iscono. Como saber? finire/capire/pulire usam -isc-; dormire/partire/aprire não usam.',
    },
    {
      tipo: 'digitar',
      pergunta: '— Quanto ___ (costare) un caffè in Italia?\n(= Quanto custa um café na Itália?)',
      resposta: 'costa',
      dica: 'il caffè = lui/lei; -ARE regular',
      explicacao: '"costare" -ARE, lui/lei → -a: cost+a = costa. "Quanto costa?" é uma das frases mais usadas em italiano — vai precisar todo dia de viagem!',
    },
    {
      tipo: 'digitar',
      pergunta: 'Noi ___ (essere) pronti per la lezione!\n(= Nós estamos prontos para a aula!)',
      resposta: 'siamo',
      dica: 'essere = irregolare; noi',
      explicacao: '"essere" (ser/estar) é totalmente irregular. Paradigma: sono/sei/è/siamo/siete/sono. noi → siamo = nós somos/estamos. Decore: siamo = somos/estamos.',
    },

    // ── BLOCO 3: revelar — contexto real (ex 13–16) ─────────
    {
      tipo: 'revelar',
      pergunta: 'Una giornata tipica (Um dia típico) — completa i verbi:\n\n«Marco ___ (svegliarsi → si sveglia = acorda) alle sette.\n___ (fare → fa = faz) colazione con la famiglia.\nPoi ___ (andare → va = vai) all\'università.\nAll\'università ___ (studiare → studia = estuda) italiano.»',
      resposta: 'si sveglia · fa · va · studia',
      explicacao: 'si sveglia (reflexivo, 3ª sing.); fa (fare irr., 3ª sing.); va (andare irr., 3ª sing.); studia (-ARE regular, 3ª sing.). Todos na 3ª pessoa singular porque o sujeito é Marco.',
    },
    {
      tipo: 'revelar',
      pergunta: 'In famiglia (Na família) — completa:\n\n«— Papà, dove ___ (lavorare = trabalhar) tu?\n— Io ___ (lavorare) in banca. E tu, cosa ___ (studiare) all\'università?\n— ___ (studiare) lingue straniere!\n(lingue straniere = línguas estrangeiras)»',
      resposta: 'lavori · lavoro · studi · Studio',
      explicacao: 'lavori (tu -ARE → -i); lavoro (io -ARE → -o); studi (tu -ARE → -i); Studio (io -ARE → -o, início de frase → maiúscula). Note como a TERMINAÇÃO muda a cada pessoa: -i para tu, -o para io.',
    },
    {
      tipo: 'revelar',
      pergunta: 'In un bar italiano (Num bar italiano) — completa:\n\n«— ___ (voi, volere = querer) un caffè?\n— Sì, grazie! Io ___ (volere) un caffè e Mario ___ (volere) un cappuccino.»',
      resposta: 'Volete · voglio · vuole',
      explicacao: '"volere" (querer) é irregular: voglio/vuoi/vuole/vogliamo/volete/vogliono. voi → volete; io → voglio; lui → vuole. Observe: a raiz muda muito — "vol-" para noi/voi, "vogl-" para io, "vuo-" para tu/lui.',
    },
    {
      tipo: 'revelar',
      pergunta: 'La scuola di lingue (A escola de idiomas) — completa:\n\n«Io e Marco ___ (studiare = estudar) italiano insieme.\nLa professoressa ___ (chiamarsi = chamar-se) Paola.\nLei ___ (essere = ser/estar) molto brava!\nVoi ___ (capire = entender) tutto?\n(insieme=juntos · brava=ótima · tutto=tudo)»',
      resposta: 'studiamo · si chiama · è · capite',
      explicacao: 'studiamo (noi -ARE → -iamo); si chiama (reflexivo 3ª sing., chiamarsi); è (essere irr., 3ª sing.); capite (voi, -IRE do grupo -isc- → capisce singular, mas voi → -ite: cap+ite = capite).',
    },

    // ── BLOCO 4: digitar — síntese (ex 17–18) ────────────────
    {
      tipo: 'digitar',
      pergunta: 'Completa:\n"Di solito io ___ (mangiare) la pizza e tu ___ (bere) il vino."\n(= Normalmente eu como pizza e você bebe vinho.\ndi solito = normalmente · vino = vinho)',
      resposta: 'mangio · bevo',
      dica: 'mangiare: io, -ARE | bere: io → bevo (irregular)',
      explicacao: '"mangio" (io -ARE → -o). "bevi" seria "tu beve"... espera: "tu ___ (bere)" → bevi. Mas aqui é "io" na segunda lacuna? Não — releia: "tu ___ (bere)" → bevi. "io mangio" (-o) / "tu bevi" (bere irr., tu → bevi).',
      variantes: ['mangio, bevi', 'mangio · bevi', 'mangio  bevi'],
    },
    {
      tipo: 'digitar',
      pergunta: 'Traduza para o italiano:\n"Nós moramos em Roma e estudamos medicina."\n\n(abitare=morar · medicina=medicina · Roma=Roma)',
      resposta: 'Abitiamo a Roma e studiamo medicina.',
      dica: 'noi + dois verbos -ARE; cidades não têm artigo',
      explicacao: '"abitiamo" (noi -ARE → -iamo); "studiamo" (noi -ARE → -iamo). "a Roma" sem artigo: nomes de cidade não recebem artigo. Pro-drop: "noi" omitido — as terminações -iamo já dizem que somos nós.',
      variantes: ['Noi abitiamo a Roma e studiamo medicina.', 'abitiamo a Roma e studiamo medicina.', 'Abitiamo a Roma e studiamo medicina'],
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
  console.log(`✓ ${novaUnidade.id}: ${novaUnidade.exercicios.length} exercícios, 7 camadas NMA`);
}

aplicar(lez1);
aplicar(lez2);

fs.writeFileSync(GRAMMAR_PATH, JSON.stringify(grammar, null, 2), 'utf8');
console.log('\ngrammar.json atualizado!');
