// ============================================================
// diagnostico.js — Teste Completo de Nível de Italiano
// Avaliação Lexical Adaptativa (Abbott CAT) + 25 Frases em Contexto (A1→C1)
// Feature F10 / Milestone 3: "O Espelho" (The Mirror)
// ============================================================

const VocabDiagnostic = {
  _ativo: false,
  _respostasVocab: [],
  _respostasFrases: [],
  _itensVocab: [],
  _itensFrases: [],
  _faseAtual: 1, // 1 = Vocabulário, 2 = Frases em Contexto
  _indiceAtual: 0,
  _inicioTimestamp: 0,

  // ── 1. Banco Calibrado de Pseudopalavras (Catch Trials) ──────
  PSEUDOPALAVRAS: [
    'strugolo', 'ventare', 'basticcio', 'frunare',
    'spindolo', 'luffo', 'grabello', 'spugnare',
    'talpone', 'salpino', 'nartello', 'corbino'
  ],

  // ── 2. Banco Expandido de Palavras Autênticas Desafiadoras (+25) ──
  PALAVRAS_AVANCADAS: [
    { w: 'tramonto', b: 2, n: 'B1' },
    { w: 'sbadiglio', b: 2, n: 'B1' },
    { w: 'sciopero', b: 2, n: 'B1' },
    { w: 'faccenda', b: 2, n: 'B1' },
    { w: 'sopportare', b: 2, n: 'B1' },
    { w: 'rammarico', b: 3, n: 'B2' },
    { w: 'malgrado', b: 3, n: 'B2' },
    { w: 'prodigio', b: 3, n: 'B2' },
    { w: 'accattivante', b: 3, n: 'B2' },
    { w: 'disinvolto', b: 3, n: 'B2' },
    { w: 'ciononostante', b: 3, n: 'B2' },
    { w: 'sgomento', b: 3, n: 'B2' },
    { w: 'scetticismo', b: 3, n: 'B2' },
    { w: 'scaturire', b: 3, n: 'C1' },
    { w: 'imprescindibile', b: 3, n: 'C1' },
    { w: 'biasimare', b: 3, n: 'C1' },
    { w: 'celare', b: 3, n: 'C1' },
    { w: 'effimero', b: 3, n: 'C1' },
    { w: 'assennato', b: 3, n: 'C1' },
    { w: 'ribadire', b: 3, n: 'C1' },
    { w: 'travisare', b: 3, n: 'C1' },
    { w: 'vanificare', b: 3, n: 'C1' },
    { w: 'anacronistico', b: 3, n: 'C1' },
    { w: 'imperterrito', b: 3, n: 'C1' },
    { w: 'sviscerare', b: 3, n: 'C1' }
  ],

  // ── 3. Banco de 25 Frases Autênticas em Contexto (A1 a C1) ──
  FRASI_DIAGNOSTICO: [
    // ── A1 (Iniciante / Básico) ──
    {
      id: 'frase_a1_1',
      nivel: 'A1',
      frase: '— Come ti chiami?\n— _____ Marco, piacere di conoscerti!',
      pergunta: 'Quale opzione completa correttamente la presentazione?',
      opcoes: ['Mi chiamo', 'Ti chiami', 'Si chiama', 'Ci chiamiamo'],
      resposta_idx: 0,
      explicacao: 'Usa-se o pronome reflexivo de primeira pessoa "mi chiamo" para se apresentar.'
    },
    {
      id: 'frase_a1_2',
      nivel: 'A1',
      frase: 'Noi _____ a Roma in treno domani mattina per lavoro.',
      pergunta: 'Scegli la forma corretta del verbo "andare":',
      opcoes: ['andiamo', 'vado', 'va', 'vanno'],
      resposta_idx: 0,
      explicacao: 'A 1ª pessoa do plural do verbo "andare" no presente é "noi andiamo".'
    },
    {
      id: 'frase_a1_3',
      nivel: 'A1',
      frase: 'A che ora _____ la colazione di solito durante la settimana?',
      pergunta: 'Scegli la forma corretta del verbo "fare":',
      opcoes: ['fai', 'fanno', 'facciamo', 'fare'],
      resposta_idx: 0,
      explicacao: '"Tu fai" é a 2ª pessoa do singular do verbo "fare".'
    },
    {
      id: 'frase_a1_4',
      nivel: 'A1',
      frase: 'Questo libro è davvero bello, _____ leggo ogni sera prima di dormire.',
      pergunta: 'Quale pronome diretto sostituisce "il libro"?',
      opcoes: ['lo', 'la', 'li', 'le'],
      resposta_idx: 0,
      explicacao: '"Il libro" é masculino singular, logo substituído pelo pronome direto "lo".'
    },
    {
      id: 'frase_a1_5',
      nivel: 'A1',
      frase: '— Di dove siete voi?\n— Noi _____ italiani, nati a Firenze.',
      pergunta: 'Scegli la forma corretta del verbo "essere":',
      opcoes: ['siamo', 'sono', 'siete', 'è'],
      resposta_idx: 0,
      explicacao: 'A 1ª pessoa do plural do presente de "essere" é "noi siamo".'
    },

    // ── A2 (Elementar / Vida Cotidiana) ──
    {
      id: 'frase_a2_1',
      nivel: 'A2',
      frase: 'Ieri sera io e Francesca _____ una pizza eccellente nel centro storico.',
      pergunta: 'Scegli il passato prossimo corretto del verbo "mangiare":',
      opcoes: ['abbiamo mangiato', 'hanno mangiato', 'siamo mangiati', 'mangiavamo'],
      resposta_idx: 0,
      explicacao: '"Mangiare" é transitivo e conjuga com o auxiliar "avere": abbiamo mangiato.'
    },
    {
      id: 'frase_a2_2',
      nivel: 'A2',
      frase: '— Vuoi ancora un po\' di caffè?\n— No grazie, _____ ho già bevuto due tazze.',
      pergunta: 'Quale particella pronominale partitiva è corretta?',
      opcoes: ['ne', 'ci', 'lo', 'la'],
      resposta_idx: 0,
      explicacao: 'A partícula partitiva "ne" expressa quantidade determinada ("duas xícaras dele").'
    },
    {
      id: 'frase_a2_3',
      nivel: 'A2',
      frase: 'Quando sono arrivato alla stazione, purtroppo il treno _____ già partito.',
      pergunta: 'Scegli il trapassato prossimo con l\'ausiliare corretto:',
      opcoes: ['era', 'ha', 'sia', 'fu'],
      resposta_idx: 0,
      explicacao: '"Partire" é intransitivo de movimento, auxiliado por "essere" no imperfetto: era partito.'
    },
    {
      id: 'frase_a2_4',
      nivel: 'A2',
      frase: 'Vado spesso _____ cinema con i colleghi dopo il lavoro.',
      pergunta: 'Quale preposizione articolata è richiesta da "andare al cinema"?',
      opcoes: ['al', 'nel', 'sul', 'dal'],
      resposta_idx: 0,
      explicacao: 'A locução fixa italiana de destino cultural é "andare al cinema" (a + il).'
    },
    {
      id: 'frase_a2_5',
      nivel: 'A2',
      frase: 'Ieri non sono potuto venire alla riunione perché _____ una forte emicrania.',
      pergunta: 'Scegli il tempo verbale per descrivere uno stato fisico passato:',
      opcoes: ['avevo', 'ebbi', 'avessi', 'avrei'],
      resposta_idx: 0,
      explicacao: 'Descrições de estados físicos ou condições no passado pedem o imperfetto: avevo.'
    },

    // ── B1 (Intermediário / Autonomia Prática) ──
    {
      id: 'frase_b1_1',
      nivel: 'B1',
      frase: 'Mentre io _____ la cena in cucina, è squillato all\'improvviso il citofono.',
      pergunta: 'Scegli l\'azione continuata di sfondo al passato:',
      opcoes: ['preparavo', 'ho preparato', 'preparai', 'avrei preparato'],
      resposta_idx: 0,
      explicacao: 'Ação em andamento no passado (enquanto) exige o imperfetto indicativo (preparavo).'
    },
    {
      id: 'frase_b1_2',
      nivel: 'B1',
      frase: '— Hai dato le chiavi dell\'ufficio a Matteo?\n— Sì, _____ ho date prima che uscisse.',
      pergunta: 'Quale pronome combinato (a lui + le chiavi) è corretto?',
      opcoes: ['gliele', 'glielo', 'mele', 'cele'],
      resposta_idx: 0,
      explicacao: '"Gli" + "le" (chiavi f. pl.) fundem-se em "gliele", com concordância no particípio (date).'
    },
    {
      id: 'frase_b1_3',
      nivel: 'B1',
      frase: 'Se avessi più tempo libero nei fine settimana, _____ volentieri un corso di pittura.',
      pergunta: 'Completa l\'apodosi del periodo ipotetico della possibilità (2° tipo):',
      opcoes: ['comincerei', 'comincio', 'avrei cominciato', 'cominciassi'],
      resposta_idx: 0,
      explicacao: 'Se + congiuntivo imperfetto (avessi) pede condizionale presente na oração principal (comincerei).'
    },
    {
      id: 'frase_b1_4',
      nivel: 'B1',
      frase: 'Non sono affatto convinto che Marco _____ tutta la verità sui fatti.',
      pergunta: 'Quale modo verbale esprime dubbio o incertezza dopo "non essere convinto che"?',
      opcoes: ['dica', 'dice', 'diceva', 'dirà'],
      resposta_idx: 0,
      explicacao: 'Verbos e locuções de dúvida/opinião negativa exigem o congiuntivo presente (dica).'
    },
    {
      id: 'frase_b1_5',
      nivel: 'B1',
      frase: 'Firenze è una città magnifica, _____ nei mesi estivi è soffocata dal turismo di massa.',
      pergunta: 'Quale connettivo avversativo formale è appropriato?',
      opcoes: ['tuttavia', 'perché', 'quindi', 'affinché'],
      resposta_idx: 0,
      explicacao: '"Tuttavia" é o conector avversativo adequado que expressa contraste elegante.'
    },

    // ── B2 (Intermediário Superior / Nuances & Sintaxe Complexa) ──
    {
      id: 'frase_b2_1',
      nivel: 'B2',
      frase: 'Benché _____ un vento gelido, gli escursionisti decisero di proseguire verso la vetta.',
      pergunta: 'Quale tempo del congiuntivo richiede la congiunzione concessiva "benché" al passato?',
      opcoes: ['facesse', 'faceva', 'fa', 'avrebbe fatto'],
      resposta_idx: 0,
      explicacao: '"Benché" rege obrigatoriamente o congiuntivo; no passado em correlação com "decisero", congiuntivo imperfetto (facesse).'
    },
    {
      id: 'frase_b2_2',
      nivel: 'B2',
      frase: 'È assolutamente imprescindibile che ciascun partecipante _____ il modulo d\'iscrizione.',
      pergunta: 'Quale forma del congiuntivo presente completa la proposizione oggettiva/soggettiva?',
      opcoes: ['compili', 'compila', 'compilerà', 'compilasse'],
      resposta_idx: 0,
      explicacao: '"È imprescindibile che" expressa necessidade impessoal presente, exigindo congiuntivo presente (compili).'
    },
    {
      id: 'frase_b2_3',
      nivel: 'B2',
      frase: 'Se me lo avessi comunicato con maggior anticipo, ti _____ senza esitazione.',
      pergunta: 'Periodo ipotetico dell\'irrealtà nel passato (3° tipo): completa l\'apodosi:',
      opcoes: ['avrei aiutato', 'avessi aiutato', 'aiuterei', 'aiutassi'],
      resposta_idx: 0,
      explicacao: 'Se + congiuntivo trapassato (avessi comunicato) pede condizionale composto (avrei aiutato).'
    },
    {
      id: 'frase_b2_4',
      nivel: 'B2',
      frase: 'Temo seriamente che il documento non _____ ancora stato recapitato all\'ufficio competente.',
      pergunta: 'Verbo di timore al presente: quale forma passiva del congiuntivo passato occorre?',
      opcoes: ['sia', 'è', 'fosse', 'sarà'],
      resposta_idx: 0,
      explicacao: '"Temere che" pede congiuntivo; anterioridade em relação ao presente pede congiuntivo passato passivo (sia stato recapitato).'
    },
    {
      id: 'frase_b2_5',
      nivel: 'B2',
      frase: '_____ la crisi energetica globale, l\'azienda ha saputo mantenere solida la produzione.',
      pergunta: 'Quale connettivo di concessione con valore preposizionale regge il sintagma nominale?',
      opcoes: ['Malgrado', 'Purché', 'Affinché', 'Nel caso che'],
      resposta_idx: 0,
      explicacao: '"Malgrado" (ou "nonostante") introduz um sintagma nominal com valor concessivo ("apesar de").'
    },

    // ── C1/C2 (Avançado / Proficiência e Registros Cultos) ──
    {
      id: 'frase_c1_1',
      nivel: 'C1',
      frase: 'Qualora dovessero insorgere discrepanze normative, vi preghiamo di _____ tempestivamente.',
      pergunta: 'Quale costrutto verbale formale completa l\'infinito con pronome enclitico?',
      opcoes: ['avvisarci', 'avvisandoci', 'avvisati', 'ci avvisare'],
      resposta_idx: 0,
      explicacao: 'A regência preposicional "di" exige o infinito com pronome enclítico incorporado: "avvisarci".'
    },
    {
      id: 'frase_c1_2',
      nivel: 'C1',
      frase: 'Non ritengo affatto plausibile che le sue giustificazioni _____ a dissipare i sospetti.',
      pergunta: 'Subordinata completiva dopo opinione negativa: quale forma del congiuntivo presente serve?',
      opcoes: ['bastino', 'basteranno', 'basterebbero', 'bastano'],
      resposta_idx: 0,
      explicacao: '"Non ritenere plausibile che" regge strettamente il congiuntivo presente (bastino).'
    },
    {
      id: 'frase_c1_3',
      nivel: 'C1',
      frase: 'Se solo me ne fossi avveduto a tempo debito, non _____ a conclusioni così affrettate.',
      pergunta: 'Condizionale passato per esprimere un rammarico retrospettivo nell\'irrealtà:',
      opcoes: ['sarei giunto', 'fossi giunto', 'giunsi', 'giungessi'],
      resposta_idx: 0,
      explicacao: 'Verbo intransitivo "giungere" forma il condizionale composto con "essere": sarei giunto.'
    },
    {
      id: 'frase_c1_4',
      nivel: 'C1',
      frase: 'Occorre analizzare a fondo la perizia tecnica _____ non sussista alcun dubbio interpretativo.',
      pergunta: 'Quale congiunzione finale richiede il modo congiuntivo?',
      opcoes: ['affinché', 'sebbene', 'malgrado', 'giacché'],
      resposta_idx: 0,
      explicacao: '"Affinché" (a fim de que) é a conjunção subordinativa final por excelência e rege congiuntivo.'
    },
    {
      id: 'frase_c1_5',
      nivel: 'C1',
      frase: 'Il diplomatico ha manifestato un palese senso di _____ di fronte all\'intransigenza della controparte.',
      pergunta: 'Quale termine culto indica sgomento misto a profondo rammarico e costernazione?',
      opcoes: ['sgomento', 'sbadiglio', 'sciopero', 'faccenda'],
      resposta_idx: 0,
      explicacao: '"Sgomento" denota profunda consternação e desconcerto em registro culto.'
    }
  ],

  /**
   * Correção psicométrica de Abbott para acertos casuais e viés de resposta:
   * Adj = (HitRate - FalseAlarmRate) / (1 - FalseAlarmRate)
   * Se FalseAlarmRate >= 0.5 (fraude/chute em massa), penalidade zera o score.
   */
  calcularAbbott(hitRate, falseAlarmRate) {
    if (typeof falseAlarmRate !== 'number' || falseAlarmRate >= 0.5) return 0;
    if (typeof hitRate !== 'number') return 0;
    const adj = (hitRate - falseAlarmRate) / (1 - falseAlarmRate);
    return Math.max(0, Math.min(1.0, adj));
  },

  /**
   * Calcula o score psicométrico integrado:
   * Combina a amostragem lexical com o desempenho real nas 25 frases de contexto.
   */
  calcularScore(respostas, respostasFrases = []) {
    if (!Array.isArray(respostas) || respostas.length === 0) {
      return {
        estimativa_passiva: 0,
        estimativa_ativa: 0,
        nivel_cefr: 'A1',
        total_testado: 0,
        false_alarm_rate: 0,
        confiavel: true,
        frasi_score: { total: 0, acertos: 0, por_nivel: {} },
        ultimo_teste: Date.now()
      };
    }

    const pseudoWords = respostas.filter(r => r.isPseudoword);
    const realWords = respostas.filter(r => !r.isPseudoword);

    const falseAlarms = pseudoWords.filter(r => r.known).length;
    const falseAlarmRate = pseudoWords.length > 0 ? (falseAlarms / pseudoWords.length) : 0;
    const confiavel = falseAlarmRate < 0.5;

    let estimativaPassiva = 0;
    const bands = [1, 2, 3, 4, 5];

    const hasBands = realWords.some(r => r.band !== undefined);
    if (hasBands) {
      bands.forEach(b => {
        const bandItems = realWords.filter(r => r.band === b);
        if (bandItems.length === 0) return;
        const hits = bandItems.filter(r => r.known).length;
        const hitRate = hits / bandItems.length;
        const adjustedRate = this.calcularAbbott(hitRate, falseAlarmRate);
        estimativaPassiva += adjustedRate * 1000;
      });
    } else {
      const hits = realWords.filter(r => r.known).length;
      const hitRate = realWords.length > 0 ? (hits / realWords.length) : 0;
      const adjustedRate = this.calcularAbbott(hitRate, falseAlarmRate);
      estimativaPassiva = Math.round(adjustedRate * 3000);
    }

    estimativaPassiva = Math.max(0, Math.round(estimativaPassiva));
    const estimativaAtiva = Math.round(estimativaPassiva * 0.65);

    // ── Análise detalhada das 25 frases sintáticas ──
    const frasiInfo = {
      total: respostasFrases.length,
      acertos: respostasFrases.filter(f => f.correto).length,
      por_nivel: {
        A1: { total: 0, acertos: 0 },
        A2: { total: 0, acertos: 0 },
        B1: { total: 0, acertos: 0 },
        B2: { total: 0, acertos: 0 },
        C1: { total: 0, acertos: 0 }
      }
    };

    respostasFrases.forEach(f => {
      const n = f.nivel || 'A1';
      if (!frasiInfo.por_nivel[n]) frasiInfo.por_nivel[n] = { total: 0, acertos: 0 };
      frasiInfo.por_nivel[n].total++;
      if (f.correto) frasiInfo.por_nivel[n].acertos++;
    });

    // ── Determinação Integrada do CEFR (Léxico + Sintaxe) ──
    let nivelCefr = 'A1';
    if (respostasFrases.length >= 10) {
      const acertosA1 = frasiInfo.por_nivel.A1.acertos;
      const acertosA2 = frasiInfo.por_nivel.A2.acertos;
      const acertosB1 = frasiInfo.por_nivel.B1.acertos;
      const acertosB2 = frasiInfo.por_nivel.B2.acertos;
      const acertosC1 = frasiInfo.por_nivel.C1.acertos;

      if (acertosC1 >= 3 && acertosB2 >= 4 && estimativaPassiva >= 2800) {
        nivelCefr = 'C1/C2';
      } else if (acertosB2 >= 3 && acertosB1 >= 4 && estimativaPassiva >= 1800) {
        nivelCefr = 'B2';
      } else if (acertosB1 >= 3 && acertosA2 >= 4 && estimativaPassiva >= 1000) {
        nivelCefr = 'B1';
      } else if (acertosA2 >= 3 && estimativaPassiva >= 500) {
        nivelCefr = 'A2';
      } else {
        nivelCefr = 'A1';
      }
    } else {
      // Fallback clássico por amplitude de vocabulário
      if (estimativaPassiva >= 4000) nivelCefr = 'C1/C2';
      else if (estimativaPassiva >= 2800) nivelCefr = 'B2';
      else if (estimativaPassiva >= 1800) nivelCefr = 'B1';
      else if (estimativaPassiva >= 800) nivelCefr = 'A2';
    }

    return {
      estimativa_passiva: estimativaPassiva,
      estimativa_ativa: estimativaAtiva,
      nivel_cefr: nivelCefr,
      total_testado: respostas.length + respostasFrases.length,
      total_palavras: respostas.length,
      total_frases: respostasFrases.length,
      false_alarm_rate: Number(falseAlarmRate.toFixed(3)),
      confiavel,
      frasi_score: frasiInfo,
      ultimo_teste: Date.now()
    };
  },

  /**
   * Gera a lista completa de itens de vocabulário (40+ palavras reais incluindo as +25 avançadas + catch trials).
   */
  gerarItensVocab() {
    const itens = [];
    const freqClient = (typeof FrequencyBandClient !== 'undefined' && typeof FrequencyBandClient.getSampleByBand === 'function')
      ? FrequencyBandClient
      : null;

    if (freqClient) {
      for (let b = 1; b <= 3; b++) {
        const sample = freqClient.getSampleByBand(b, 10);
        sample.forEach(lemma => {
          itens.push({ word: lemma, isPseudoword: false, band: b });
        });
      }
    } else {
      const lemasBase = [
        { w: 'casa', b: 1 }, { w: 'giorno', b: 1 }, { w: 'cosa', b: 1 }, { w: 'anno', b: 1 },
        { w: 'uomo', b: 1 }, { w: 'tempo', b: 1 }, { w: 'donna', b: 1 }, { w: 'vita', b: 1 },
        { w: 'mondo', b: 2 }, { w: 'occhio', b: 2 }, { w: 'ora', b: 2 }, { w: 'signore', b: 2 },
        { w: 'accordo', b: 2 }, { w: 'strada', b: 2 }, { w: 'figlio', b: 2 }, { w: 'notte', b: 2 },
        { w: 'luogo', b: 3 }, { w: 'parte', b: 3 }, { w: 'fine', b: 3 }, { w: 'specie', b: 3 },
        { w: 'mente', b: 3 }, { w: 'ragione', b: 3 }, { w: 'governo', b: 3 }, { w: 'piano', b: 3 }
      ];
      lemasBase.forEach(item => {
        itens.push({ word: item.w, isPseudoword: false, band: item.b });
      });
    }

    // Incorpora as 25 palavras autênticas desafiadoras adicionais
    this.PALAVRAS_AVANCADAS.forEach(item => {
      // Evita duplicatas se já existirem no freqClient
      if (!itens.some(it => it.word === item.w)) {
        itens.push({ word: item.w, isPseudoword: false, band: item.b, nivel: item.n });
      }
    });

    // Adiciona 8 pseudopalavras fonotaticamente válidas para controle de chute
    const pseudoEmbaralhadas = [...this.PSEUDOPALAVRAS].sort(() => Math.random() - 0.5).slice(0, 8);
    pseudoEmbaralhadas.forEach(p => {
      itens.push({ word: p, isPseudoword: true });
    });

    return itens.sort(() => Math.random() - 0.5);
  },

  /**
   * Gera a lista ordenada e equilibrada das 25 frases de avaliação em contexto.
   */
  gerarItensFrases() {
    // Embaralha as alternativas de cada frase preservando o rastreio da opção correta
    return this.FRASI_DIAGNOSTICO.map(item => {
      const textoCorreto = item.opcoes[item.resposta_idx];
      const opcoesEmbaralhadas = [...item.opcoes].sort(() => Math.random() - 0.5);
      const novoRespostaIdx = opcoesEmbaralhadas.indexOf(textoCorreto);

      return {
        ...item,
        opcoes: opcoesEmbaralhadas,
        resposta_idx: novoRespostaIdx,
        texto_correto: textoCorreto
      };
    });
  },

  /**
   * Inicia o teste diagnóstico completo e robusto.
   */
  iniciar() {
    this._respostasVocab = [];
    this._respostasFrases = [];
    this._itensVocab = this.gerarItensVocab();
    this._itensFrases = this.gerarItensFrases();
    this._faseAtual = 1;
    this._indiceAtual = 0;
    this._inicioTimestamp = Date.now();
    this._ativo = true;

    this._abrirModal();
    this._renderizarItem();
  },

  _abrirModal() {
    let modal = document.getElementById('modal-diagnostico-vocab');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'modal-diagnostico-vocab';
      modal.className = 'modal-backdrop-diagnostico ativo';
      modal.setAttribute('role', 'dialog');
      modal.setAttribute('aria-modal', 'true');
      modal.setAttribute('aria-label', 'Teste Completo de Nível de Italiano');
      modal.innerHTML = `
        <div class="modal-card-diagnostico">
          <div class="diag-header">
            <div>
              <h3>🔬 O Espelho — Teste Completo de Nível</h3>
              <span id="diag-fase-indicator" class="diag-fase-indicator">Fase 1: Vocabulário Amplo</span>
            </div>
            <button type="button" class="btn-fechar-modal" onclick="VocabDiagnostic.fechar()" title="Fechar">✖</button>
          </div>
          <div class="diag-progresso-bar">
            <div id="diag-progresso-fill" style="width: 0%;"></div>
          </div>
          <div id="diag-conteudo-palco" class="diag-palco"></div>
        </div>
      `;
      document.body.appendChild(modal);
    } else {
      modal.classList.add('ativo');
    }
  },

  _renderizarItem() {
    const palco = document.getElementById('diag-conteudo-palco');
    const fill = document.getElementById('diag-progresso-fill');
    const faseIndicator = document.getElementById('diag-fase-indicator');
    if (!palco) return;

    // ── FASE 1: Vocabulário ──
    if (this._faseAtual === 1) {
      if (this._indiceAtual >= this._itensVocab.length) {
        // Transição suave para a Fase 2 (Frases)
        this._faseAtual = 2;
        this._indiceAtual = 0;
        this._renderizarTransicaoFase();
        return;
      }

      if (faseIndicator) {
        faseIndicator.textContent = `Fase 1 de 2: Vocabulário (${this._indiceAtual + 1}/${this._itensVocab.length})`;
      }

      const item = this._itensVocab[this._indiceAtual];
      const totalGlobal = this._itensVocab.length + this._itensFrases.length;
      const progressoGlobal = Math.round((this._indiceAtual / totalGlobal) * 100);
      if (fill) fill.style.width = `${progressoGlobal}%`;

      palco.innerHTML = `
        <div class="diag-item-box">
          <div class="diag-badge-nivel-item">${item.nivel ? `Palavra nível ${item.nivel}` : 'Léxico Italiano'}</div>
          <span class="diag-step-counter">Item ${this._indiceAtual + 1} de ${this._itensVocab.length}</span>
          <h2 class="diag-palavra-destaque">${item.word}</h2>
          <p class="diag-pergunta-prompt">Você conhece com certeza o significado desta palavra?</p>
          <div class="diag-botoes-row">
            <button type="button" class="btn-diag-nao" onclick="VocabDiagnostic.responderVocab(false)">
              ❌ Não conheço
            </button>
            <button type="button" class="btn-diag-sim" onclick="VocabDiagnostic.responderVocab(true)">
              ✅ Conheço
            </button>
          </div>
          <div class="diag-dica-honestidade">
            💡 Seja honesto: o teste contém palavras-armadilha para calibrar o viés de chute.
          </div>
        </div>
      `;
      return;
    }

    // ── FASE 2: Frases em Contexto ──
    if (this._faseAtual === 2) {
      if (this._indiceAtual >= this._itensFrases.length) {
        this._finalizar();
        return;
      }

      if (faseIndicator) {
        faseIndicator.textContent = `Fase 2 de 2: Frases & Gramática (${this._indiceAtual + 1}/${this._itensFrases.length})`;
      }

      const item = this._itensFrases[this._indiceAtual];
      const concluido = this._itensVocab.length + this._indiceAtual;
      const totalGlobal = this._itensVocab.length + this._itensFrases.length;
      const progressoGlobal = Math.round((concluido / totalGlobal) * 100);
      if (fill) fill.style.width = `${progressoGlobal}%`;

      // Formata a frase destacando a lacuna
      const fraseFormatada = item.frase
        .replace(/\n/g, '<br>')
        .replace(/_____/g, '<span class="diag-lacuna-destaque">_____</span>');

      palco.innerHTML = `
        <div class="diag-frase-box">
          <div class="diag-frase-header-row">
            <span class="diag-nivel-pill nivel-${item.nivel.toLowerCase()}">${item.nivel}</span>
            <span class="diag-step-counter">Frase ${this._indiceAtual + 1} de ${this._itensFrases.length}</span>
          </div>

          <div class="diag-frase-texto-card">
            ${fraseFormatada}
          </div>

          <p class="diag-frase-pergunta">${item.pergunta}</p>

          <div class="diag-opcoes-grid" id="diag-frase-opcoes">
            ${item.opcoes.map((opcao, idx) => `
              <button type="button" class="btn-diag-opcao" onclick="VocabDiagnostic.responderFrase(${idx})">
                <span class="diag-opcao-letra">${String.fromCharCode(65 + idx)}</span>
                <span class="diag-opcao-texto">${opcao}</span>
              </button>
            `).join('')}
          </div>
        </div>
      `;
    }
  },

  _renderizarTransicaoFase() {
    const palco = document.getElementById('diag-conteudo-palco');
    if (!palco) return;

    palco.innerHTML = `
      <div class="diag-transicao-card">
        <div class="diag-transicao-icon">🎯</div>
        <h3>Fase 1 Concluída!</h3>
        <p>
          Agora vamos colocar seu conhecimento à prova em <strong>25 frases autênticas</strong> (do A1 ao C1).
          Aqui você não apenas diz se sabe, mas demonstra domínio real de gramática, preposições e concordância em contexto!
        </p>
        <button type="button" class="btn-primario btn-comecar-frases" onclick="VocabDiagnostic._iniciarFase2()">
          Começar as 25 Frases →
        </button>
      </div>
    `;
  },

  _iniciarFase2() {
    this._faseAtual = 2;
    this._indiceAtual = 0;
    this._renderizarItem();
  },

  responderVocab(conhece) {
    if (!this._ativo || this._faseAtual !== 1) return;
    const item = this._itensVocab[this._indiceAtual];
    this._respostasVocab.push({
      word: item.word,
      isPseudoword: item.isPseudoword,
      known: Boolean(conhece),
      band: item.band,
      nivel: item.nivel
    });

    this._indiceAtual++;
    this._renderizarItem();
  },

  // Mantém retrocompatibilidade para quem chama responder(conhece) diretamente
  responder(conhece) {
    if (this._faseAtual === 1) {
      this.responderVocab(conhece);
    }
  },

  responderFrase(opcaoEscolhidaIdx) {
    if (!this._ativo || this._faseAtual !== 2) return;
    const item = this._itensFrases[this._indiceAtual];
    const acertou = opcaoEscolhidaIdx === item.resposta_idx;

    this._respostasFrases.push({
      id: item.id,
      nivel: item.nivel,
      correto: acertou,
      escolhida: item.opcoes[opcaoEscolhidaIdx],
      correta: item.texto_correto,
      explicacao: item.explicacao
    });

    this._indiceAtual++;
    this._renderizarItem();
  },

  _finalizar() {
    this._ativo = false;
    const resultado = this.calcularScore(this._respostasVocab, this._respostasFrases);

    // Persiste no AppState
    if (typeof AppState !== 'undefined' && AppState.estado && AppState.estado.progresso) {
      AppState.estado.progresso.vocab_diagnostico = resultado;
      if (typeof AppState.salvarProgresso === 'function') {
        AppState.salvarProgresso();
      }
    }

    // Recompensa generosa de XP pelo teste completo (100 XP)
    if (typeof AppXP !== 'undefined' && typeof AppXP.ganharXP === 'function') {
      AppXP.ganharXP(100);
    }

    const palco = document.getElementById('diag-conteudo-palco');
    const fill = document.getElementById('diag-progresso-fill');
    if (fill) fill.style.width = '100%';

    if (palco) {
      let alertaBlefe = '';
      if (!resultado.confiavel) {
        alertaBlefe = `
          <div class="diag-alerta-blefe">
            ⚠️ <strong>Atenção ao Viés:</strong> Detectamos taxa de falso alarme elevada (${Math.round(resultado.false_alarm_rate * 100)}%). Palavras fictícias foram marcadas como conhecidas. O algoritmo recalibrou seu score para neutralizar chutes.
          </div>
        `;
      }

      // Detalhamento dos acertos nas frases por nível
      const pn = resultado.frasi_score?.por_nivel || {};
      const niveis = ['A1', 'A2', 'B1', 'B2', 'C1'];
      const htmlBreakdown = niveis.map(lvl => {
        const dados = pn[lvl] || { total: 5, acertos: 0 };
        const pct = dados.total > 0 ? Math.round((dados.acertos / dados.total) * 100) : 0;
        return `
          <div class="diag-breakdown-row">
            <span class="diag-lvl-tag">${lvl}</span>
            <div class="diag-lvl-bar-track">
              <div class="diag-lvl-bar-fill lvl-${lvl.toLowerCase()}" style="width: ${pct}%;"></div>
            </div>
            <span class="diag-lvl-val">${dados.acertos}/${dados.total} (${pct}%)</span>
          </div>
        `;
      }).join('');

      palco.innerHTML = `
        <div class="diag-resultado-box">
          <div class="diag-cefr-badge">${resultado.nivel_cefr}</div>
          <h3 class="diag-res-titulo">Seu Nível de Italiano Comprovado</h3>
          <p class="diag-res-sub">Avaliação profunda: Vocabulário Real + 25 Frases Autênticas em Contexto</p>

          ${alertaBlefe}

          <div class="diag-breakdown-card">
            <h4>📊 Desempenho Sintático por Nível (25 Frases):</h4>
            <div class="diag-breakdown-list">
              ${htmlBreakdown}
            </div>
            <div class="diag-total-frases-acertos">
              Total de acertos nas frases: <strong>${resultado.frasi_score?.acertos || 0} de ${resultado.frasi_score?.total || 25}</strong>
            </div>
          </div>

          <div class="diag-metricas-grid">
            <div class="diag-metrica-card">
              <span class="diag-val">${resultado.estimativa_passiva.toLocaleString()}</span>
              <span class="diag-lbl">Vocabulário Passivo Estimado</span>
            </div>
            <div class="diag-metrica-card">
              <span class="diag-val">${resultado.estimativa_ativa.toLocaleString()}</span>
              <span class="diag-lbl">Produção Ativa Estimada</span>
            </div>
          </div>

          <div class="diag-laufer-comparativo">
            <h4>📖 Comparativo com o Limiar de Laufer (95% para leitura autônoma):</h4>
            <p>
              Para ler literatura, notícias e compreender canções sem recorrer ao dicionário, são necessários <strong>3.000 a 4.000 lemas</strong>.
              Você alcançou <strong>${Math.round((resultado.estimativa_passiva / 3000) * 100)}%</strong> dessa meta com sintaxe testada.
            </p>
          </div>

          <div class="diag-acoes-resultado">
            <button type="button" class="btn-primario" onclick="VocabDiagnostic.fechar(); if (typeof App !== 'undefined' && App.navegar) App.navegar('canzoni');">
              🎵 Explorar Canções do Seu Nível
            </button>
            <button type="button" class="btn-secondario" onclick="VocabDiagnostic.fechar();">
              Concluir Teste
            </button>
          </div>
        </div>
      `;
    }

    // Atualiza perfil caso visível
    if (typeof Profilo !== 'undefined' && typeof Profilo.renderizar === 'function') {
      try { Profilo.renderizar(); } catch (_) {}
    }
  },

  fechar() {
    this._ativo = false;
    const modal = document.getElementById('modal-diagnostico-vocab');
    if (modal) modal.classList.remove('ativo');
  }
};

// Exportação global e para testes
if (typeof window !== 'undefined') {
  window.VocabDiagnostic = VocabDiagnostic;
}
if (typeof globalThis !== 'undefined') {
  globalThis.VocabDiagnostic = VocabDiagnostic;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = VocabDiagnostic;
}
