// ============================================================
// ia-import.js — Adição de conteúdo via IA (Prompt-Assisted Import)
// Fluxo: copiar prompt → colar no LLM → colar JSON de volta → importar
// ============================================================

const IAImport = {
  tipoAtual: null,
  origemAtual: null,

  // ── Prompts por tipo ─────────────────────────────────────
  prompts: {
    dialogo: `Crie um diálogo em italiano para estudantes brasileiros. Retorne APENAS o JSON, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. "nivel": deve ser "A1", "A2", "B1", "B2" ou "C1"
2. "contexto": descrição clara da situação prática (1-2 frases em português)
3. "turni": array ordenado de turnos de conversa:
   - Turnos do PERSONAGEM:
     * "id": número sequencial (1, 2, 3...)
     * "personaggio": nome do interlocutor (ex: "Cameriere", "Commessa", "Dottore")
     * "frase": fala natural em italiano
     * "traducao": tradução em português brasileiro
     * "audio_ipa": transcrição fonética IPA opcional (pode deixar "")
   - Turnos do "Tu" (o usuário responde):
     * "id": número sequencial
     * "personaggio": "Tu"
     * "frase": a resposta CORRETA em italiano
     * "traducao": tradução da resposta em português brasileiro
     * "audio_ipa": ""
     * "alternativas": 4 opções em italiano (a correta obrigatoriamente inclusa)
     * "resposta_correta": índice (0 a 3) indicando qual opção de "alternativas" é a correta
4. Alterne os turnos: PERSONAGEM → Tu → PERSONAGEM → Tu...
5. "vocabulario_chave": array com 3 a 5 termos principais em italiano
6. "xp_recompensa": número inteiro (ex: 50)

EXEMPLO DE ESTRUTURA (copie exatamente este formato):
{
  "id": "dial_custom_001",
  "titulo": "Al Mercato",
  "icone": "🛒",
  "nivel": "A1",
  "contexto": "Você está comprando frutas em uma feira na Itália.",
  "turni": [
    {
      "id": 1,
      "personaggio": "Venditore",
      "frase": "Buongiorno! Cosa desidera?",
      "traducao": "Bom dia! O que deseja?",
      "audio_ipa": ""
    },
    {
      "id": 2,
      "personaggio": "Tu",
      "frase": "Vorrei delle mele, per favore.",
      "traducao": "Eu gostaria de algumas maçãs, por favor.",
      "audio_ipa": "",
      "alternativas": [
        "Vorrei delle mele, per favore.",
        "Non mi piace la frutta.",
        "Dov\x27è il bagno?",
        "Quanto costa questo vestito?"
      ],
      "resposta_correta": 0
    },
    {
      "id": 3,
      "personaggio": "Venditore",
      "frase": "Certo! Quante ne vuole?",
      "traducao": "Claro! Quantas quer?",
      "audio_ipa": ""
    },
    {
      "id": 4,
      "personaggio": "Tu",
      "frase": "Un chilo, grazie.",
      "traducao": "Um quilo, obrigado.",
      "audio_ipa": "",
      "alternativas": [
        "Non lo so.",
        "Un chilo, grazie.",
        "Sono a dieta.",
        "Preferisco le banane."
      ],
      "resposta_correta": 1
    }
  ],
  "vocabulario_chave": ["desiderare", "mela", "chilo"],
  "xp_recompensa": 50
}

TEMA DO DIÁLOGO: [SUBSTITUA AQUI — ex: "fazendo check-in no hotel em Florença", "comprando bilhete de trem em Milão", "na farmácia pedindo remédio"]`,

    canzone: `# Ruolo: Transcrittore Audio con Timestamp Parola per Parola

## Obiettivo
Analizzare file audio (parlato, dialoghi, canzoni) e generare una trascrizione temporizzata con precisione parola per parola, restituendo il risultato esclusivamente in formato JSON.

## Specifiche del Formato JSON
Ogni elemento della lista deve essere un oggetto contenente:
- "w" (string): La singola parola pronunciata, inclusa l'eventuale punteggiatura associata (es. virgole, punti, punti interrogativi).
- "t" (number): Il secondo esatto in cui inizia l'emissione vocale della parola, espresso con 2 cifre decimali (es. 2.15).
- "blank" (boolean, opzionale): Impostato su true esclusivamente sull'ultima parola di un verso, frase o prima di una pausa/stacco musicale rilevante, per indicare l'interruzione della riga.

## Schema di Esempio
[
  { "w": "Parola1,", "t": 0.05 },
  { "w": "parola2", "t": 1.10 },
  { "w": "parola3.", "t": 2.15, "blank": true }
]

## Regole di Trascrizione
1. Precisione temporale: Allinea l'attacco di ciascun termine ("t") all'istante sonoro reale.
2. Segmentazione: Separa chiaramente le parole e mantieni la punteggiatura logica attaccata al termine di appartenenza.
3. Formato di output: Rispondi fornendo unicamente il blocco JSON valido, senza introduzioni o commenti aggiuntivi.`,

    storia: `Crie uma história curta em italiano para aprendizes. Retorne APENAS o JSON, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. "italiano" = parágrafo em italiano correto
2. "portugues" = tradução COMPLETA do parágrafo em português brasileiro
3. "parole" = lista com TODAS as palavras do parágrafo — SEM EXCEÇÃO
   - Inclua substantivos, verbos, adjetivos, advérbios, artigos, preposições, pronomes, conjunções
   - Cada token de palavra deve ter sua própria entrada (não pule nenhuma palavra)
   - "parola" = a palavra exatamente como aparece no texto italiano
   - "traduzione" = tradução em português (pode ser 1-3 palavras)
   - "ipa" = transcrição fonética IPA apenas da palavra isolada (ex: "/ˈsoːle/")
   - "categoria": "sostantivo", "verbo", "aggettivo", "avverbio", "articolo", "preposizione", "pronome", "congiunzione" ou "espressione"
4. Inclua de 4 a 6 parágrafos
5. "nivel" deve ser A1, A2, B1, B2, C1 ou C2

EXEMPLO COMPLETO — note que TODAS as palavras aparecem em "parole" (copie exatamente este formato):
{
  "id": "stor_custom_001",
  "titulo": "Una Mattina a Roma",
  "titulo_pt": "Uma Manhã em Roma",
  "nivel": "A1",
  "icone": "🏛️",
  "autor": "Italiano Autentico",
  "tema": "quotidiano",
  "descricao": "Marco si sveglia presto e cammina per le strade di Roma.",
  "descricao_pt": "Marco acorda cedo e caminha pelas ruas de Roma.",
  "xp_recompensa": 80,
  "testo": [
    {
      "id": "stor_custom_001_p1",
      "italiano": "Marco si sveglia alle sette. Apre la finestra e vede il sole.",
      "portugues": "Marco acorda às sete. Ele abre a janela e vê o sol.",
      "parole": [
        {"parola": "Marco",    "traduzione": "Marco",    "ipa": "/ˈmarko/",      "categoria": "sostantivo"},
        {"parola": "si",       "traduzione": "se",       "ipa": "/si/",          "categoria": "pronome"},
        {"parola": "sveglia",  "traduzione": "acorda",   "ipa": "/ˈzveʎʎa/",    "categoria": "verbo"},
        {"parola": "alle",     "traduzione": "às",       "ipa": "/ˈalle/",       "categoria": "preposizione"},
        {"parola": "sette",    "traduzione": "sete",     "ipa": "/ˈsɛtte/",      "categoria": "sostantivo"},
        {"parola": "Apre",     "traduzione": "abre",     "ipa": "/ˈaːpre/",      "categoria": "verbo"},
        {"parola": "la",       "traduzione": "a",        "ipa": "/la/",          "categoria": "articolo"},
        {"parola": "finestra", "traduzione": "janela",   "ipa": "/fiˈnɛstra/",   "categoria": "sostantivo"},
        {"parola": "e",        "traduzione": "e",        "ipa": "/e/",           "categoria": "congiunzione"},
        {"parola": "vede",     "traduzione": "vê",       "ipa": "/ˈveːde/",      "categoria": "verbo"},
        {"parola": "il",       "traduzione": "o",        "ipa": "/il/",          "categoria": "articolo"},
        {"parola": "sole",     "traduzione": "sol",      "ipa": "/ˈsoːle/",      "categoria": "sostantivo"}
      ]
    }
  ]
}

TEMA DA HISTÓRIA: [SUBSTITUA AQUI — ex: "um dia de compras num mercado em Florença", "férias numa praia da Sicília", "primeiro dia de trabalho em Milão"]`,

    imitazione: `Crie frases italianas para prática de pronúncia guiada (Shadowing). Retorne APENAS um array JSON, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. Gere de 8 a 12 frases relacionadas ao tema prático
2. "frase_italiano" = frase autêntica em italiano, com pontuação correta
3. "frase_portugues" = tradução precisa em português brasileiro
4. "contexto" = situação pragmática de uso (1-2 frases explicando quando e como usar)
5. "nivel" = "A1", "A2", "B1", "B2" ou "C1"
6. "audio_ipa" = transcrição fonética IPA entre barras (ex: "/mi ˈskuːzi/") ou string vazia ""
7. "xp_recompensa" = 15

EXEMPLO COMPLETO (copie exatamente este formato):
[
  {
    "id": "imi_custom_001",
    "frase_italiano": "Mi scusi, sa dirmi dov\x27è la stazione centrale?",
    "frase_portugues": "Com licença, o senhor sabe me dizer onde fica a estação central?",
    "nivel": "A1",
    "contexto": "Use para pedir orientações na rua com cortesia e respeito a um desconhecido.",
    "audio_ipa": "/mi ˈskuːzi sa ˈdirmi dov\x27ɛ la statˈtsjoːne tʃenˈtraːle/",
    "xp_recompensa": 15
  },
  {
    "id": "imi_custom_002",
    "frase_italiano": "Potrebbe ripetere più lentamente, per favore?",
    "frase_portugues": "Poderia repetir mais devagar, por favor?",
    "nivel": "A2",
    "contexto": "Use quando o interlocutor falar rápido e você precisar de clareza auditiva.",
    "audio_ipa": "",
    "xp_recompensa": 15
  }
]

TEMA DAS FRASES: [SUBSTITUA AQUI — ex: "pedir informações na rua", "no restaurante pedindo a conta", "expressões de cortesia formal"]`,

    vocab: `Crie palavras de vocabulário italiano no padrão dos Templos do app. Retorne APENAS um array JSON, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. Gere de 12 a 20 vocábulos relacionados ao tema
2. "genero": "m" para masculino, "f" para feminino, "m/f" para ambos, ou null para verbos/advérbios/expressões
3. "plural": forma plural italiana correta, ou null para verbos e invariáveis
4. "exemplo": frase contextual em italiano aplicando o vocábulo de forma natural
5. "exemplo_pt": tradução completa da frase de exemplo para português brasileiro
6. "categoria": categoria temática (ex: "trasporti", "ristorante", "lavoro", "salute")
7. "dificuldade": "facil" (básico), "medio" (intermediário) ou "dificil" (avançado)
8. "audio_ipa": transcrição fonética IPA entre barras obrigatórias (ex: "/ˈtrɛːno/")

EXEMPLO COMPLETO (copie exatamente este formato):
[
  {
    "id": "vocab_custom_001",
    "italiano": "treno",
    "portugues": "trem",
    "genero": "m",
    "plural": "treni",
    "exemplo": "Il treno regionale parte alle nove dalla stazione centrale.",
    "exemplo_pt": "O trem regional parte às nove da estação central.",
    "categoria": "viaggio",
    "dificuldade": "facil",
    "audio_ipa": "/ˈtrɛːno/"
  },
  {
    "id": "vocab_custom_002",
    "italiano": "prenotare",
    "portugues": "reservar",
    "genero": null,
    "plural": null,
    "exemplo": "Ho prenotato una camera doppia per il prossimo fine settimana.",
    "exemplo_pt": "Reservei um quarto duplo para o próximo fim de semana.",
    "categoria": "albergo",
    "dificuldade": "medio",
    "audio_ipa": "/prenoˈtaːre/"
  }
]

TEMA DO VOCABULÁRIO: [SUBSTITUA AQUI — ex: "viagem de trem e bilheteria", "comidas típicas e restaurante", "profissões e ambiente de trabalho"]`
  },

  // ── Títulos do modal por tipo ────────────────────────────
  titulos: {
    dialogo:    '🤖 Adicionar Diálogo via IA',
    canzone:    '🤖 Adicionar Canção via IA',
    storia:     '🤖 Adicionar História via IA',
    imitazione: '🤖 Adicionar Imitação via IA',
    vocab:      '🤖 Adicionar Vocabulário via IA',
  },

  // ── Palavras que o aluno está errando (i+1 targeting) ──
  _obterPalavrasDificeis() {
    if (typeof App === 'undefined' || !App.estado?.flashcardData || !App.estado?.vocabCache) return [];
    const candidatos = [];
    for (const [id, f] of Object.entries(App.estado.flashcardData)) {
      if ((f.lapses > 0) || (f.stability && f.stability < 15) || f.state === 'learning' || f.state === 'new') {
        candidatos.push(id);
      }
    }
    const palavras = candidatos.map(id => {
      const v = App.estado.vocabCache.find(w => w.id === id);
      return v ? (v.italiano || v.word || v.frase) : null;
    }).filter(Boolean);
    // Embaralha e retorna até 7
    for (let i = palavras.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [palavras[i], palavras[j]] = [palavras[j], palavras[i]];
    }
    return palavras.slice(0, 7);
  },

  // ── Abrir modal ──────────────────────────────────────────
  abrir(tipo, origem = null) {
    this.tipoAtual = tipo;
    this.origemAtual = origem;
    const modal = document.getElementById('ia-import-modal');
    if (!modal) return;
    document.getElementById('ia-import-titulo').textContent = this.titulos[tipo] || '🤖 Adicionar via IA';

    // Abas de livro (visíveis exclusivamente na seção storie)
    const tabsEl = document.getElementById('ia-storia-tabs');
    if (tabsEl) {
      if (tipo === 'storia') {
        tabsEl.style.display = 'flex';
        this.trocarAbaStoria('prompt');
      } else {
        tabsEl.style.display = 'none';
        const boxP = document.getElementById('ia-box-prompt');
        const boxL = document.getElementById('ia-box-livro');
        if (boxP) boxP.style.display = 'block';
        if (boxL) boxL.style.display = 'none';
      }
    }

    let prompt = this.prompts[tipo] || '';
    if (['dialogo', 'storia', 'imitazione'].includes(tipo)) {
      const dificeis = this._obterPalavrasDificeis();
      if (dificeis.length > 0) {
        prompt += `\n\n🎯 SFIDA VOCABOLARIO OBBLIGATORIA:\nDevi includere organicamente nel testo le seguenti parole (sono parole con cui lo studente sta avendo difficoltà):\n[ ${dificeis.join(', ')} ]`;
      }
    }

    document.getElementById('ia-prompt-text').textContent = prompt;
    document.getElementById('ia-paste-area').value = '';
    const fb = document.getElementById('ia-feedback');
    if (fb) { fb.textContent = ''; fb.className = 'ia-feedback'; }
    modal.style.display = 'flex';
  },

  trocarAbaStoria(aba) {
    const tabPrompt = document.getElementById('ia-tab-prompt');
    const tabLivro  = document.getElementById('ia-tab-livro');
    const boxPrompt = document.getElementById('ia-box-prompt');
    const boxLivro  = document.getElementById('ia-box-livro');
    const fb = document.getElementById('ia-feedback');
    if (fb) { fb.textContent = ''; fb.className = 'ia-feedback'; }

    if (aba === 'livro') {
      if (tabPrompt) tabPrompt.className = 'btn-secondario';
      if (tabLivro)  tabLivro.className  = 'btn-primario';
      if (boxPrompt) boxPrompt.style.display = 'none';
      if (boxLivro)  boxLivro.style.display  = 'block';
    } else {
      if (tabPrompt) tabPrompt.className = 'btn-primario';
      if (tabLivro)  tabLivro.className  = 'btn-secondario';
      if (boxPrompt) boxPrompt.style.display = 'block';
      if (boxLivro)  boxLivro.style.display  = 'none';
    }
  },

  importarLivroTextoLivre() {
    const titulo = document.getElementById('ia-livro-titulo')?.value.trim() || 'Libro Italiano';
    const autor  = document.getElementById('ia-livro-autor')?.value.trim() || 'Letteratura';
    const nivel  = document.getElementById('ia-livro-nivel')?.value || 'B1';
    const raw    = document.getElementById('ia-livro-texto')?.value.trim() || '';

    if (!raw) {
      this._setFeedback('⚠️ Cole o texto em italiano do livro primeiro.', 'warn');
      return;
    }

    // Quebra parágrafos limpos por quebras de linha duplas ou simples
    const linhas = raw.split(/\n\s*\n|\r\n\s*\r\n/).map(l => l.trim()).filter(Boolean);
    if (linhas.length === 0) {
      this._setFeedback('⚠️ Nenhum conteúdo legível encontrado.', 'warn');
      return;
    }

    const paragrafos = linhas.map((parTexto) => ({
      italiano: parTexto.replace(/\s+/g, ' '),
      portugues: '',
      parole: []
    }));

    const novoLivro = {
      id: 'book_' + Date.now(),
      titulo: titulo,
      titulo_pt: titulo,
      nivel: nivel,
      icone: '📚',
      autor: autor,
      tema: 'letteratura',
      descricao: `${titulo} di ${autor}.`,
      descricao_pt: `${titulo} de ${autor}.`,
      xp_recompensa: Math.min(paragrafos.length * 10, 300),
      testo: paragrafos,
      _custom: true
    };

    this._importarStoria(novoLivro);
    this.fechar();
    if (typeof App !== 'undefined') {
      App.notificar(`📚 Livro "${titulo}" adicionado com sucesso!`, 'sucesso');
    }
    // Abre imediatamente para leitura no leitor
    if (typeof Storie !== 'undefined') {
      setTimeout(() => Storie.abrirStoria(novoLivro.id), 150);
    }
  },

  fechar() {
    const modal = document.getElementById('ia-import-modal');
    if (modal) modal.style.display = 'none';
  },

  // ── Copiar prompt para a área de transferência ───────────
  copiarPrompt() {
    const txt = document.getElementById('ia-prompt-text')?.textContent || '';
    navigator.clipboard.writeText(txt).then(() => {
      const btn = document.querySelector('.ia-copy-btn');
      if (!btn) return;
      const orig = btn.textContent;
      btn.textContent = '✅ Copiado!';
      btn.style.background = '#27ae60';
      setTimeout(() => { btn.textContent = orig; btn.style.background = ''; }, 2000);
    }).catch(() => {
      // Fallback para navegadores sem clipboard API
      const ta = document.createElement('textarea');
      ta.value = txt;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      const btn = document.querySelector('.ia-copy-btn');
      if (btn) { btn.textContent = '✅ Copiado!'; setTimeout(() => btn.textContent = '📋 Copiar Prompt', 2000); }
    });
  },

  // ── Importar JSON colado pelo usuário ────────────────────
  importar() {
    const raw = document.getElementById('ia-paste-area')?.value.trim() || '';
    const fb = document.getElementById('ia-feedback');
    if (!raw) {
      this._setFeedback('⚠️ Cole o conteúdo gerado pela IA primeiro.', 'warn');
      return;
    }

    let data;
    try {
      // Extrai JSON mesmo que o LLM adicione texto introdutório antes/depois
      const match = raw.match(/(\[[\s\S]*\]|\{[\s\S]*\})/);
      if (!match) throw new Error('Nenhum JSON encontrado na resposta.');
      data = JSON.parse(match[1]);
    } catch (e) {
      this._setFeedback('❌ JSON inválido. Verifique se a IA gerou o formato correto e tente novamente.', 'error');
      return;
    }

    try {
      switch (this.tipoAtual) {
        case 'dialogo':    this._importarDialogo(data); break;
        case 'canzone':    this._importarCanzone(data); break;
        case 'storia':     this._importarStoria(data); break;
        case 'imitazione': this._importarImitazione(data); break;
        case 'vocab':      this._importarVocab(data); break;
        default: throw new Error('Tipo desconhecido: ' + this.tipoAtual);
      }
      this._setFeedback('✅ Importado com sucesso!', 'ok');
      setTimeout(() => this.fechar(), 1400);
    } catch (e) {
      this._setFeedback('❌ Erro ao importar: ' + e.message, 'error');
    }
  },

  _setFeedback(msg, tipo) {
    const fb = document.getElementById('ia-feedback');
    if (!fb) return;
    fb.textContent = msg;
    fb.className = 'ia-feedback ia-feedback-' + tipo;
  },

  // ── Importadores por tipo ────────────────────────────────
  _importarDialogo(data) {
    const arr = Array.isArray(data) ? data : [data];
    const key = 'it_dialoghi_custom';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    arr.forEach((d, i) => {
      if (!d.id) d.id = 'dial_custom_' + Date.now() + '_' + i;
      d._custom = true;
    });
    try { localStorage.setItem(key, JSON.stringify([...existing, ...arr])); } catch(e) { if(e.name === 'QuotaExceededError') { App.notificar('Memoria piena! Elimina vecchie storie/canzoni.', 'erro'); } }
    // Recarregar módulo se estiver ativo
    if (typeof Dialoghi !== 'undefined') {
      Dialoghi.dados = null;
      Dialoghi.renderizarSeletor?.();
    }
  },

  _importarCanzone(data) {
    let arr;
    if (Array.isArray(data) && data.length > 0 && (data[0].w !== undefined || data[0].word !== undefined)) {
      // Array de palavras com timestamps do Gemini
      arr = [{
        id: 'can_custom_' + Date.now(),
        titulo: 'Música Sincronizada (IA)',
        artista: 'Gemini',
        nivel: 'B1',
        icone: '🎧',
        versos_sincronizados: data,
        letra_raw: JSON.stringify(data),
        _custom: true
      }];
    } else {
      arr = Array.isArray(data) ? data : [data];
      arr.forEach((d, i) => {
        if (!d.id) d.id = 'can_custom_' + Date.now() + '_' + i;
        d._custom = true;
      });
    }
    const key = 'it_canzoni_custom';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    try { localStorage.setItem(key, JSON.stringify([...existing, ...arr])); } catch(e) { if(e.name === 'QuotaExceededError') { App.notificar('Memoria piena! Elimina vecchie storie/canzoni.', 'erro'); } }
    if (typeof Canzoni !== 'undefined') {
      Canzoni.dados = null;
      Canzoni.renderizarSeletor?.();
    }
  },

  _importarStoria(data) {
    const arr = Array.isArray(data) ? data : [data];
    const key = 'it_storie_custom';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    arr.forEach((d, i) => {
      if (!d.id) d.id = 'stor_custom_' + Date.now() + '_' + i;
      d._custom = true;
    });
    try { localStorage.setItem(key, JSON.stringify([...existing, ...arr])); } catch(e) { if(e.name === 'QuotaExceededError') { App.notificar('Memoria piena! Elimina vecchie storie/canzoni.', 'erro'); } }
    if (typeof Storie !== 'undefined') {
      Storie.dados = null;
      Storie.renderizarSeletor?.();
    }
  },

  _importarImitazione(data) {
    const arr = Array.isArray(data) ? data : [data];
    const key = 'it_imitazioni_custom';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    arr.forEach((d, i) => {
      if (!d.id) d.id = 'imi_custom_' + Date.now() + '_' + i;
      d._custom = true;
    });
    try { localStorage.setItem(key, JSON.stringify([...existing, ...arr])); } catch(e) { if(e.name === 'QuotaExceededError') { App.notificar('Memoria piena! Elimina vecchie storie/canzoni.', 'erro'); } }
    if (typeof Imitazione !== 'undefined') {
      Imitazione.dados = null;
      Imitazione.renderizar?.();
    }
  },

  _importarVocab(data) {
    const arr = Array.isArray(data) ? data : [data];
    const key = 'it_vocab_custom';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    
    // Normalizador de texto italiano para comparação e slug
    const normalizarTermo = (s) => (s || '')
      .toLowerCase()
      .trim()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]/g, '');

    // Mapeia termos já existentes em todo o acervo (Templos 1-51 + custom)
    const todosVocab = (typeof App !== 'undefined' && App.estado?.vocabCache)
      ? App.estado.vocabCache
      : existing;
    const termosExistentes = new Set(
      todosVocab.map(w => normalizarTermo(w.italiano || w.word || w.frase || ''))
    );

    const palavrasNovas = [];
    let duplicatasIgnoradas = 0;

    arr.forEach((d) => {
      const termo = (d.italiano || d.word || '').trim();
      if (!termo) return;
      const chaveNorm = normalizarTermo(termo);

      if (termosExistentes.has(chaveNorm)) {
        duplicatasIgnoradas++;
        return;
      }

      // Gera ID determinístico baseado no slug da palavra italiana
      d.id = 'w_custom_' + (chaveNorm || ('rnd_' + Math.random().toString(36).substring(2, 7)));
      d.italiano = termo;
      d._custom = true;
      if (!d.templo_num) d.templo_num = 0; // "Extra" / deck customizado

      termosExistentes.add(chaveNorm);
      palavrasNovas.push(d);
    });

    if (palavrasNovas.length === 0) {
      if (duplicatasIgnoradas > 0) {
        throw new Error(`Todas as ${duplicatasIgnoradas} palavras já existem no vocabulário!`);
      }
      throw new Error('Nenhuma palavra válida encontrada para importação.');
    }

    try {
      localStorage.setItem(key, JSON.stringify([...existing, ...palavrasNovas]));
    } catch(e) {
      if (e.name === 'QuotaExceededError') {
        App.notificar('Memoria piena! Elimina vecchie storie/canzoni.', 'erro');
      }
    }

    // Injeta no vocabCache do App
    if (typeof App !== 'undefined' && App.estado?.vocabCache) {
      palavrasNovas.forEach(w => {
        if (!App.estado.vocabCache.find(v => v.id === w.id)) {
          App.estado.vocabCache.unshift(w);
        }
      });
      if (App.estado.progresso) {
        App.estado.progresso.total_palavras = App.estado.vocabCache.length;
        App.salvarProgresso();
      }
    }

    // Feedback descritivo
    let msgFeedback = `✅ ${palavrasNovas.length} nova(s) palavra(s) importada(s)!`;
    if (duplicatasIgnoradas > 0) {
      msgFeedback += ` (${duplicatasIgnoradas} já existiam e foram ignoradas)`;
    }
    this._setFeedback(msgFeedback, 'ok');

    if (typeof Vocab !== 'undefined') Vocab.renderizar?.();
    if (typeof Flashcards !== 'undefined') Flashcards.atualizarSelectTemplo?.();

    // Se a importação ocorreu na aba de Flashcards (ou com flag origem = 'flashcard')
    const veioDeFlashcards = this.origemAtual === 'flashcard' || (typeof App !== 'undefined' && App.estado?.secaoAtiva === 'flashcard');
    if (veioDeFlashcards && typeof Flashcards !== 'undefined') {
      setTimeout(() => {
        const sel = document.getElementById('flashcard-templo-select');
        if (sel) sel.value = 'custom';
        Flashcards.init('custom');
        App.notificar('🎴 Estudo iniciado com os novos Flashcards!', 'sucesso');
      }, 500);
    }
  },

  // ── Excluir item customizado ─────────────────────────────
  excluir(tipo, id) {
    if (!confirm('Remover este item?')) return;
    const keys = {
      dialogo: 'it_dialoghi_custom',
      canzone: 'it_canzoni_custom',
      storia:  'it_storie_custom',
      imitazione: 'it_imitazioni_custom',
      vocab:   'it_vocab_custom',
    };
    const key = keys[tipo];
    if (!key) return;
    const arr = JSON.parse(localStorage.getItem(key) || '[]').filter(x => x.id !== id);
    try { localStorage.setItem(key, JSON.stringify(arr)); } catch(e) { if(e.name === 'QuotaExceededError') { App.notificar('Memoria piena! Elimina vecchie storie/canzoni.', 'erro'); } }
    // Re-renderizar seção
    const renders = {
      dialogo:    () => { if (typeof Dialoghi !== 'undefined') { Dialoghi.dados=null; Dialoghi.renderizarSeletor?.(); } },
      canzone:    () => { if (typeof Canzoni !== 'undefined')  { Canzoni.dados=null;  Canzoni.renderizarSeletor?.();  } },
      storia:     () => { if (typeof Storie !== 'undefined')   { Storie.dados=null;   Storie.renderizarSeletor?.();   } },
      imitazione: () => { if (typeof Imitazione !== 'undefined') { Imitazione.dados=null; Imitazione.renderizar?.(); } },
      vocab:      () => {
        if (typeof App !== 'undefined' && App.estado?.vocabCache) {
          App.estado.vocabCache = App.estado.vocabCache.filter(v => v.id !== id);
        }
        if (typeof Vocab !== 'undefined') Vocab.renderizar?.();
      },
    };
    renders[tipo]?.();
  },
};
