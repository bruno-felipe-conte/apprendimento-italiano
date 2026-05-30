// ============================================================
// _piloto_lezioni.js
// Reescreve a1-lez1 e a1-lez2 com o novo padrão didático:
//   • NMA teoria completa (7 camadas obrigatórias)
//   • 15-18 exercícios por unidade
//   • Distribuição: 35% escolha · 35% digitar · 30% revelar
//   • Progressão: reconhecimento → produção → uso contextual → síntese
//   • Cada explicacao ensina o POR QUÊ (nunca só "correto!")
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

  // ── NMA: 7 camadas ───────────────────────────────────────
  alerta: 'Sem artigo correto, um italiano entende o que você diz — mas sabe imediatamente que você é estrangeiro. O artigo é o primeiro teste visível do seu italiano.',

  inventario: [
    'Gênero dos nomes: masculino (il libro) e feminino (la penna)',
    'Artigos definidos singulares: il · lo · la · l\'',
    'Artigos definidos plurais: i · gli · le',
    'Artigos indefinidos: un · uno · una · un\'',
    'Acordo do adjetivo com o nome',
  ],

  definicao: {
    fenomeno: 'Il ragazzo studia. La ragazza studia. Lo studente studia.',
    causa: 'Por que "il", "la" e "lo" para pessoas que fazem a mesma coisa?',
    conceito: 'O artigo concorda em gênero (masc./fem.) e número (sing./pl.) com o nome. A escolha entre il/lo/la depende também do som inicial da palavra.',
  },

  tecnica: '1. Determine o gênero do nome (masc. ou fem.).\n2. Observe a letra inicial da palavra.\n3. Masc. sing.: consoante normal → il | s+consoante, z, gn, ps → lo | vogal → l\'.\n4. Fem. sing.: consoante → la | vogal → l\'.\n5. No plural: il→i · lo→gli · la→le · l\'→i (masc.) ou le (fem.).',

  exemplos_prc: [
    {
      oracao: 'Il libro è sul tavolo.',
      pergunta: 'Por que "il" e não "lo" ou "la"?',
      resposta: '"libro" é masculino e começa por consoante normal (l)',
      conclusao: 'Masc. sing. + consoante normal → il.',
    },
    {
      oracao: 'Lo studente legge.',
      pergunta: 'Por que "lo" e não "il"?',
      resposta: '"studente" começa por "st" — s seguido de consoante (t)',
      conclusao: 'Masc. sing. + s+consoante → lo (nunca il).',
    },
    {
      oracao: 'Gli zaini sono pesanti.',
      pergunta: 'Por que "gli" no plural de "zaino"?',
      resposta: '"zaino" começa por z → no sing. é "lo zaino", no plural → gli',
      conclusao: 'lo → gli no plural. z, gn, s+C, ps → gli.',
    },
    {
      oracao: 'Un\'amica di Marco abita qui.',
      pergunta: 'Por que "un\'" e não "una"?',
      resposta: '"amica" é feminino e começa por vogal (a)',
      conclusao: 'Art. indef. fem. + vogal: una → un\' (con apostrofo).',
    },
  ],

  ponte: 'Em português: "o menino / a menina" = em italiano "il ragazzo / la ragazza" — a lógica é a mesma. Mas cuidado com as exceções: *il problema* (não "la", é masc.), *la mano* (não "il", é fem.), *il cinema* (masc.). Outro perigo: em português "um estudante / uma estudante" — em italiano o artigo indefinido também muda: *uno studente* (não "un", por causa do "st").',

  coda: 'A partir de hoje, cada palavra nova que aprender: memorize COM o artigo. Não "gatto" — mas "il gatto". Não "università" — mas "l\'università". O artigo é parte do vocabulário.',

  // ── Exercícios ───────────────────────────────────────────
  exercicios: [

    // ── BLOCO 1: escolha (ex 1-5) — reconhecimento ──────
    {
      tipo: 'escolha',
      pergunta: '— Ciao Marco! Hai visto ___ film di Fellini ieri sera?',
      opcoes: ['il', 'lo', 'la', 'l\''],
      resposta: 0,
      explicacao: '"film" é masculino e começa por consoante normal (f) → il. "Lo" só para s+consoante, z, gn, ps. "La" e "l\'" são femininos.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Mia sorella studia insieme a ___ studente americano.',
      opcoes: ['un', 'uno', 'una', 'il'],
      resposta: 1,
      explicacao: '"studente" começa por "st" (s+consoante). Artigo indefinido masculino diante de s+C → uno, nunca "un". Compare: un libro (consoante normal) ≠ uno studente.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Ecco ___ zaini degli studenti universitari.',
      opcoes: ['i', 'gli', 'le', 'lo'],
      resposta: 1,
      explicacao: '"zaini" (plural de zaino) começa por z → gli. A regra do singular (z → lo) se mantém no plural: lo zaino → gli zaini.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Ho incontrato ___ amica di Valentina al mercato.',
      opcoes: ['una', 'un\'', 'la', 'un'],
      resposta: 1,
      explicacao: '"amica" é feminino (fem.) e começa por vogal (a). Art. indef. fem. + vogal → un\' (com apóstrofo). "una" seria errado porque "a" é vogal: una amica → hiato feio → un\'amica.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Dove sono ___ occhiali di Giorgio? Li vedo ovunque tranne qui!',
      opcoes: ['i', 'gli', 'le', 'l\''],
      resposta: 1,
      explicacao: '"occhiali" (plural de occhiale) é masculino e começa por vogal (o) → gli. Regra: masc. plural + vogal → gli (non i). Compare: i libri (consoante) ≠ gli occhiali (vogal).',
    },

    // ── BLOCO 2: digitar (ex 6-10) — produção controlada ─
    {
      tipo: 'digitar',
      pergunta: 'Al ristorante, cerco ___ (art. def. masc. pl., "gn") gnocchi tradizionali.',
      resposta: 'gli gnocchi',
      dica: 'Masc. plural, começa por gn- (como "gnocchi")',
      explicacao: 'gn → artigo "gli" (como z, s+C, ps). No singular: lo gnocco → no plural: gli gnocchi. Inclua o artigo na resposta: "gli gnocchi".',
      variantes: ['gli'],
    },
    {
      tipo: 'digitar',
      pergunta: 'Il paziente ha bisogno di ___ (art. ind. masc. sing., "ps") psicologo esperto.',
      resposta: 'uno psicologo',
      dica: 'Masc. singular indefinido, começa por ps-',
      explicacao: '"psicologo" começa por ps → artigo indefinido masc. = uno (não "un"). ps, gn, z, s+C → uno (sing.) / gli (pl.).',
      variantes: ['uno'],
    },
    {
      tipo: 'digitar',
      pergunta: '— Scusa, hai visto dove ho messo ___ (art. def. masc. pl., "gu") guanti?',
      resposta: 'i guanti',
      dica: 'Masc. pl., "g" seguida de "u" = consoante normal',
      explicacao: '"gu" é consoante normal (não é s+C, nem z, nem gn). Portanto: masc. pl. consoante normal → i. Não confunda com "gli": gli é só para vogal, z, gn, s+C, ps.',
      variantes: ['i'],
    },
    {
      tipo: 'digitar',
      pergunta: 'Questa è ___ (art. def. fem. sing., vogal) università più antica d\'Italia.',
      resposta: "l'università",
      dica: 'Feminino singular, começa por vogal',
      explicacao: 'la + vogal → l\' (apóstrofo), tanto para masc. quanto para fem. no singular. "università" = fem. + vogal → l\'università. No plural: le università (sem apóstrofo).',
      variantes: ["l'università", "l'università"],
    },
    {
      tipo: 'digitar',
      pergunta: 'Nel museo, ho visto ___ (art. def. masc. pl., "s+C") splendidi affreschi di Giotto.',
      resposta: 'gli splendidi affreschi',
      dica: 'Masc. pl., começa por sp- (s+p = s+consoante)',
      explicacao: '"splendidi" começa por sp- (s seguido de consoante p) → gli. Observe a cadeia: lo sguardo (sing.) → gli sguardi (pl.) / lo splendore → gli splendori.',
      variantes: ['gli splendidi', 'gli'],
    },

    // ── BLOCO 3: revelar (ex 11-14) — uso contextual ─────
    {
      tipo: 'revelar',
      pergunta: 'In libreria — completa gli articoli mancanti:\n\n«— Buongiorno! Cerco ___ libro di storia italiana.\n— Certamente. ___ libri di storia sono in fondo a destra.\n— E avete anche ___ dizionario italiano-portoghese?\n— Sì! ___ dizionario che cerca è questo.»',
      resposta: 'un · i · un · Il',
      explicacao: '"un libro" = indefinido (sto cercando uno qualsiasi, prima menzione). "i libri" = definido plurale (quei libri specifici sullo scaffale). "un dizionario" = indefinido (ne cerco uno qualsiasi). "Il dizionario" = definido (il preciso che ha chiesto).',
    },
    {
      tipo: 'revelar',
      pergunta: 'Descrizione di una stanza — completa:\n\n«___ tavolo è grande. Sopra ci sono ___ computer portatile e ___ penna rossa. Accanto al tavolo c\'è ___ sedia comoda.»',
      resposta: 'Il · un · una · una',
      explicacao: '"Il tavolo", "La sedia" → definido, perché parliamo di UNA stanza specifica (quella davanti a noi). "un computer", "una penna" → indefinido, perché non sappiamo ancora di quale oggetto specifico si tratta (prima menzione).',
    },
    {
      tipo: 'revelar',
      pergunta: 'In aeroporto — completa con l\'articolo giusto:\n\n«— Scusi, è ___ studentessa?\n— Sì, studio all\'Università di Roma. E lei?\n— Sono ___ ingegnere. Lavoro a Milano. Questo è ___ aeroporto di Malpensa?\n— No, siamo a ___ aeroporto di Fiumicino.»',
      resposta: "una · un · l' · l'",
      explicacao: '"una studentessa", "un ingegnere" = indefinido (prima presentazione, non sappiamo ancora chi sono). I due aeroporti: "l\'aeroporto" = definido + começa por vogal → l\' (sia la prima che la seconda volta).',
    },
    {
      tipo: 'revelar',
      pergunta: 'Persone in piazza — completa:\n\n«Guarda: ___ ragazzo alto è Marco. È ___ studente di ingegneria. ___ ragazza vicino a lui è ___ sua amica di università.»',
      resposta: 'il · uno · La · la',
      explicacao: '"il ragazzo" = definido (lo vediamo). "uno studente" = professione con art. ind.: uno (s+C). "La ragazza" = defin., la vediamo. "la sua amica" = possessivo + defin. (con i possessivi italiani il/la sono quasi sempre obbligatori).',
    },

    // ── BLOCO 4: digitar síntese (ex 15) ─────────────────
    {
      tipo: 'digitar',
      pergunta: 'Traduci in italiano: "A professora de italiano está com os alunos no laboratório."',
      resposta: 'La professoressa di italiano è con gli studenti in laboratorio.',
      dica: 'professoressa = fem. sing. consoante; studenti = masc. pl. s+C',
      explicacao: '"La professoressa" (fem. def., consoante normal → la). "gli studenti" (masc. pl., "st" = s+consoante → gli). "in laboratorio" sem artigo: lugar genérico com "in" normalmente não tem artigo.',
      variantes: ['La professoressa di italiano è con gli studenti nel laboratorio.'],
    },
  ],
};

// ── a1-lez2 ── Il presente indicativo ──────────────────────
const lez2 = {
  id: 'a1-lez2',
  titulo: 'Il presente indicativo',
  subtitulo: 'L\'azione nel momento presente',
  nivel: 'A1',

  // ── NMA: 7 camadas ───────────────────────────────────────
  alerta: 'O presente italiano faz o trabalho de três tempos portugueses: "falo", "estou falando" e "vou falar" (agora). Um tempo. Uma forma. Dominar o presente é dominar 80% das conversas cotidianas.',

  inventario: [
    'Verbos regulares -ARE: amare, parlare, studiare',
    'Verbos regulares -ERE: leggere, vivere, prendere',
    'Verbos regulares -IRE: dormire, partire (e gruppo -isc-: finire, capire)',
    'Irregolari essenziali: essere, avere, fare, andare, venire, potere, volere, dovere',
    'Pro-drop: o sujeito pronominal é opcional',
  ],

  definicao: {
    fenomeno: 'Parlo italiano. Parli italiano. Parla italiano.',
    causa: 'Por que três formas diferentes se o verbo é o mesmo? E cadê o sujeito "io/tu/lui"?',
    conceito: 'A desinência (terminação) do verbo identifica o sujeito. Por isso o italiano omite o pronome sujeito (é uma língua pro-drop): a terminação já diz quem faz a ação.',
  },

  tecnica: '1. Identifique o infinitivo do verbo.\n2. Retire a terminação (-ARE, -ERE ou -IRE).\n3. Adicione a desinência correta:\n   -ARE: -o · -i · -a · -iamo · -ate · -ano\n   -ERE: -o · -i · -e · -iamo · -ete · -ono\n   -IRE: -o · -i · -e · -iamo · -ite · -ono\n   -IRE(isc): -isco · -isci · -isce · -iamo · -ite · -iscono\n4. Para irregolari: memorizar o paradigma completo (não há atalho).',

  exemplos_prc: [
    {
      oracao: 'Ogni mattina studio italiano per un\'ora.',
      pergunta: 'Como conjugar "studiare" para "io"?',
      resposta: 'Retira -ARE → studi-, adiciona -o → studio',
      conclusao: '-ARE regular + io → -o. "studiare" → studio.',
    },
    {
      oracao: 'Marco prende il caffè al bar ogni giorno.',
      pergunta: 'Por que "prende" e não "prendono"?',
      resposta: 'Marco = lui/lei (3ª sing.). -ERE + lui/lei → -e',
      conclusao: '-ERE regular + lui/lei → -e. "prendere" → prende.',
    },
    {
      oracao: 'Noi finiamo il lavoro alle sei di sera.',
      pergunta: 'Por que "finiamo" sem -isc-?',
      resposta: '"finire" usa -isc- só em io/tu/lui/loro — não em noi/voi',
      conclusao: '-IRE(isc) + noi → -iamo (sem -isc-). finire → finiamo.',
    },
    {
      oracao: 'Non so dove vai con tanta fretta!',
      pergunta: 'Qual o paradigma completo de "andare"?',
      resposta: 'vado · vai · va · andiamo · andate · vanno',
      conclusao: 'andare é irregolare: io/tu/lui/loro têm raiz "v-"; noi/voi retornam a "and-".',
    },
  ],

  ponte: 'Pro-drop: "Parlo italiano" = "Eu falo italiano" — o "io" é opcional. Em português falado também omitimos ("Falo português"), mas em italiano é a norma, não exceção. USE o pronome apenas para ênfase ou contraste: "Io vado a Roma, tu rimani qui." Em português precisamos de "eu...tu..." sempre para clareza; em italiano a desinência já basta.\n\nCuidado com os falsos análogos: "essere" não é "estar" — é também "ser". "sono stanco" = "estou cansado" (não "sou"). E "fare" (fazer) é totalmente irregular: faccio · fai · fa · facciamo · fate · fanno.',

  coda: 'Conjugue 5 verbos novos em voz alta todos os dias: io · tu · lui/lei · noi · voi · loro. São 30 formas em 2 minutos. Depois de uma semana, o presente regular se torna automático.',

  // ── Exercícios ───────────────────────────────────────────
  exercicios: [

    // ── BLOCO 1: escolha (ex 1-6) — reconhecimento ──────
    {
      tipo: 'escolha',
      pergunta: '— Scusi, ___ (Lei) l\'autobus numero 40 per andare in centro?',
      opcoes: ['prende', 'prendi', 'prendete', 'prendiamo'],
      resposta: 0,
      explicacao: '"Lei" (formal) usa a mesma forma de lui/lei: 3ª pessoa singular. -ERE + lui/lei/Lei → -e: prend+e = prende. "prendi" seria para "tu" (informal).',
    },
    {
      tipo: 'escolha',
      pergunta: 'Io non ___ mai il caffè, preferisco sempre il tè verde.',
      opcoes: ['bevo', 'bevi', 'beve', 'beviamo'],
      resposta: 0,
      explicacao: '"bere" é irregolare. Paradigma: bevo/bevi/beve/beviamo/bevete/bevono. "io" → bevo. Nota: a radice "bev-" + desinenza -o/-i/-e/-iamo/-ete/-ono.',
    },
    {
      tipo: 'escolha',
      pergunta: 'Ogni estate, noi ___ in Sicilia per due settimane.',
      opcoes: ['andiamo', 'vanno', 'andate', 'vado'],
      resposta: 0,
      explicacao: '"andare" irregolare: vado · vai · va · andiamo · andate · vanno. "noi" → andiamo (retorna à raiz "and-" para noi/voi). "vanno" é para loro.',
    },
    {
      tipo: 'escolha',
      pergunta: '— Marco e Sofia, ___ l\'italiano da quanto tempo?',
      opcoes: ['studiate', 'studiano', 'studiamo', 'studi'],
      resposta: 0,
      explicacao: '"Marco e Sofia" são a 2ª pessoa plural (voi). -ARE + voi → -ate: studi+ate = studiate. "studiano" seria para loro (3ª pl.).',
    },
    {
      tipo: 'escolha',
      pergunta: 'Luca e Anna ___ in un piccolo appartamento vicino all\'università.',
      opcoes: ['abitano', 'abita', 'abitate', 'abitiamo'],
      resposta: 0,
      explicacao: '"Luca e Anna" = loro (3ª pl.). -ARE + loro → -ano: abit+ano = abitano. Atenção: não é "abita" (3ª sing.) nem "abitate" (voi).',
    },
    {
      tipo: 'escolha',
      pergunta: '— Tu ___ bene l\'italiano! Dove hai studiato?',
      opcoes: ['parli', 'parla', 'parlate', 'parlo'],
      resposta: 0,
      explicacao: '"tu" + -ARE → -i: parl+i = parli. "parla" seria lui/lei. "parlo" seria io. Nota: em italiano o "tu" costuma ser omitido — a terminação "-i" já identifica a 2ª pessoa singular.',
    },

    // ── BLOCO 2: digitar (ex 7-12) — produção controlada ─
    {
      tipo: 'digitar',
      pergunta: 'Al telefono:\n— Ciao! Come ti ___ (chiamarsi)?',
      resposta: 'chiami',
      dica: 'Verbo riflessivo, 2ª persona sing. (-ARE)',
      explicacao: '"chiamarsi" = verbo riflessivo. tu: ti chiami. Desinência -ARE (tu → -i): chiam+i = chiami. Pronome riflessivo "ti" + forma normale.',
      variantes: ['ti chiami'],
    },
    {
      tipo: 'digitar',
      pergunta: 'Tutti i giorni io mi ___ (alzarsi) alle sette in punto.',
      resposta: 'alzo',
      dica: 'Parte do verbo che si coniuga; io, -ARE',
      explicacao: '"alzarsi" riflessivo: io mi alzo. La parte che coniughi è "alzarsi" → alzo (io -ARE → -o). Il "mi" è già nella frase. "mi alzo" = eu me levanto.',
      variantes: ['alzo'],
    },
    {
      tipo: 'digitar',
      pergunta: 'La domenica mattina, noi ___ (fare) colazione insieme al bar sotto casa.',
      resposta: 'facciamo',
      dica: 'fare = irregolare; noi',
      explicacao: '"fare" è totalmente irregolare: faccio · fai · fa · facciamo · fate · fanno. noi → facciamo. Non segue né -ARE né -ERE né -IRE.',
    },
    {
      tipo: 'digitar',
      pergunta: 'Ogni venerdì, tu e Giulia ___ (uscire) con gli amici del quartiere.',
      resposta: 'uscite',
      dica: 'uscire = irregolare; voi',
      explicacao: '"uscire" irregolare: esco · esci · esce · usciamo · uscite · escono. "tu e Giulia" = voi → uscite. Nota: per noi/voi, uscire ritorna alla radice "usc-".',
    },
    {
      tipo: 'digitar',
      pergunta: '— Quanto ___ (costare) questo libro di grammatica?',
      resposta: 'costa',
      dica: 'Il soggetto implicito è "il libro" (lui/lei); verbo regolare -ARE',
      explicacao: '"costare" regolare -ARE. lui/lei → -a: cost+a = costa. Il soggetto è implicito ("il libro" che stai guardando). Pro-drop: il soggetto non si ripete.',
    },
    {
      tipo: 'digitar',
      pergunta: 'I bambini ___ (giocare) in giardino sotto la pioggia!',
      resposta: 'giocano',
      dica: 'loro; attenzione alla "c" in -care',
      explicacao: '"giocare" (-CARE): loro → giocano (NON "giochano"). L\'aggiunta della "h" accade solo davanti a "-i": tu giochi, noi giochiamo — per mantenere il suono /k/. Ma davanti a "-ano" non serve.',
    },

    // ── BLOCO 3: revelar (ex 13-16) — uso contextuale ────
    {
      tipo: 'revelar',
      pergunta: 'Una giornata tipica di Marta — completa i verbi:\n\n«Marta ___ (svegliarsi) alle 7. Prima ___ (fare) la doccia, poi ___ (prepararsi) per l\'università. A otto ___ (uscire) di casa e ___ (prendere) il bus. All\'università ___ (studiare) fino all\'una.»',
      resposta: 'si sveglia · fa · si prepara · esce · prende · studia',
      explicacao: 'si sveglia (riflessivo irr., 3ª sing.); fa (fare irr.); si prepara (riflessivo -ARE, 3ª sing.); esce (uscire irr.); prende (regolare -ERE); studia (regolare -ARE). Tutti alla 3ª persona singolare (lei = Marta).',
    },
    {
      tipo: 'revelar',
      pergunta: 'Dialogo in corridoio — completa:\n\n«— Dove ___ (tu, andare) adesso?\n— ___ (io, andare) in biblioteca. ___ (tu, venire) con me?\n— No, oggi non ___ (io, potere). Devo studiare la grammatica.\n— Ma ___ (noi, studiare) insieme! Più facile.»',
      resposta: 'vai · Vado · Vieni · posso · studiamo',
      explicacao: 'vai (andare irr., tu); Vado (andare irr., io); Vieni (venire irr., tu); posso (potere irr., io); studiamo (regolare -ARE, noi). I pronomi soggetto sono omessi, tranne per enfasi ("io non posso").',
    },
    {
      tipo: 'revelar',
      pergunta: 'La mia famiglia — completa i verbi:\n\n«La mia famiglia ___ (abitare) a Napoli da sempre. Mio padre ___ (lavorare) in un\'azienda di import-export, mia madre ___ (insegnare) matematica al liceo. Io e mio fratello ___ (frequentare) il liceo scientifico.»',
      resposta: 'abita · lavora · insegna · frequentiamo',
      explicacao: 'Tutti regolari -ARE. abitare: 3ª sing. → abita; lavorare → lavora; insegnare → insegna; frequentare: noi → frequentiamo (-iamo). Nota: "io e mio fratello" = noi.',
    },
    {
      tipo: 'revelar',
      pergunta: 'Cosa bevete? — completa:\n\n«— Marco, cosa ___ (bere) di solito?\n— Io ___ (bere) solo acqua minerale. E voi due?\n— Noi ___ (bere) molto caffè. Gli italiani ___ (bere) il caffè al bar ogni giorno.»',
      resposta: 'bevi · bevo · beviamo · bevono',
      explicacao: '"bere" irregolare: bevo/bevi/beve/beviamo/bevete/bevono. La radice cambia: "bev-" per tutte le persone tranne bere stesso. Confronta: -ERE regolare (leggo/leggi) vs. "bere" (bevo/bevi).',
    },

    // ── BLOCO 4: digitar síntese (ex 17-18) ──────────────
    {
      tipo: 'digitar',
      pergunta: 'Completa le due forme:\n"Di solito io ___ (studiare) italiano e tu ___ (ascoltare) musica."',
      resposta: 'studio · ascolti',
      dica: 'io + -ARE; tu + -ARE',
      explicacao: '"studio" (io -ARE → -o: studi+o). "ascolti" (tu -ARE → -i: ascolt+i). Dois sujeitos, duas desinências diferentes. O italiano distingue sempre io/tu pela terminação.',
      variantes: ['studio, ascolti', 'studio ascolti'],
    },
    {
      tipo: 'digitar',
      pergunta: 'Come si dice in italiano?\n"Eles moram em Roma e estudam medicina."',
      resposta: 'Abitano a Roma e studiano medicina.',
      dica: 'loro + -ARE (dois verbos); città = sem artigo com "a"',
      explicacao: '"abitano" (loro -ARE → -ano); "studiano" (loro -ARE → -ano). "a Roma" sem artigo: nomes di città non prendono l\'articolo con le preposizioni a/da/di/in. Il pronome "loro" è omesso (pro-drop).',
      variantes: ['Loro abitano a Roma e studiano medicina.', 'abitano a Roma e studiano medicina.'],
    },
  ],
};

// ── Aplicar no grammar.json ────────────────────────────────
const modulo0 = grammar.moduli[0]; // A1

function aplicar(novaUnidade) {
  const idx = modulo0.unidades.findIndex(u => u.id === novaUnidade.id);
  if (idx === -1) {
    console.error(`Unidade ${novaUnidade.id} não encontrada!`);
    process.exit(1);
  }
  // Preservar campos que não estamos reescrevendo
  modulo0.unidades[idx] = {
    ...modulo0.unidades[idx],
    ...novaUnidade,
    // Remover campo legado para forçar o renderer NMA
    teoria: undefined,
    exemplos: undefined,
  };
  // Limpar undefined
  Object.keys(modulo0.unidades[idx]).forEach(k => {
    if (modulo0.unidades[idx][k] === undefined) delete modulo0.unidades[idx][k];
  });
  console.log(`✓ ${novaUnidade.id} reescrita: ${novaUnidade.exercicios.length} exercícios, 7 camadas NMA`);
}

aplicar(lez1);
aplicar(lez2);

fs.writeFileSync(GRAMMAR_PATH, JSON.stringify(grammar, null, 2), 'utf8');
console.log('\ngrammar.json atualizado com sucesso!');

// Verificação rápida
const check = JSON.parse(fs.readFileSync(GRAMMAR_PATH, 'utf8'));
const u1 = check.moduli[0].unidades.find(u => u.id === 'a1-lez1');
const u2 = check.moduli[0].unidades.find(u => u.id === 'a1-lez2');
const campos = ['alerta','inventario','definicao','tecnica','exemplos_prc','ponte','coda'];
console.log('\n— Verificação a1-lez1:');
campos.forEach(c => console.log(`  ${u1[c] ? '✓' : '✗'} ${c}`));
console.log(`  exercicios: ${u1.exercicios.length}`);
console.log('— Verificação a1-lez2:');
campos.forEach(c => console.log(`  ${u2[c] ? '✓' : '✗'} ${c}`));
console.log(`  exercicios: ${u2.exercicios.length}`);
