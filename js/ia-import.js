// ============================================================
// ia-import.js — Adição de conteúdo via IA (Prompt-Assisted Import)
// Fluxo: copiar prompt → colar no LLM → colar JSON de volta → importar
// ============================================================

const IAImport = {
  tipoAtual: null,

  // ── Prompts por tipo ─────────────────────────────────────
  prompts: {
    dialogo: `Crie um diálogo em italiano para aprendizes de português. Retorne APENAS o JSON, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. Turnos do PERSONAGEM: campos "frase" (italiano), "traducao" (português), "audio_ipa" (deixe "")
2. Turnos do "Tu": campo "frase" = a resposta CORRETA em italiano, "traducao" = tradução dessa resposta, MAIS "alternativas" (4 opções em italiano, a correta INCLUÍDA) e "resposta_correta" = índice 0-3 da correta em alternativas
3. Alterne sempre: PERSONAGEM → Tu → PERSONAGEM → Tu... (sem limite de turnos — use quantos forem necessários para cobrir a conversa completa)
4. Todas as falas em italiano correto, todas as traduções em português brasileiro

EXEMPLO de dois turnos (copie exatamente este formato):
{
  "id": "dial_custom_001",
  "titulo": "No Mercato",
  "icone": "🛒",
  "nivel": "A1",
  "contexto": "Você está num mercado comprando frutas.",
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
        "Dov'è il bagno?",
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

TEMA DO DIÁLOGO: [SUBSTITUA AQUI — ex: "comprando passagem de trem em Milão", "pedindo ajuda numa farmácia", "fazendo check-in no hotel". Pode ter quantos turnos forem necessários para cobrir a conversa completa — sem limite]`,

    canzone: `Crie os dados de uma música italiana para estudo. Pode ser qualquer música — italiana, traduzida para o italiano, ou uma composição própria. Retorne APENAS o JSON, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. Inclua TODOS os versos da música, sem limite de quantidade
2. Para versos com conteúdo único e palavra interessante para aprender:
   - "palavra_oculta" = a palavra a ser adivinhada
   - "texto_lacuna" = o verso com essa palavra substituída por ___
   - "dica" = explicação gramatical breve
   - "repeticoes" = quantas vezes consecutivas esse verso se repete na música (1 se não repete)
3. Para versos PURAMENTE repetitivos (refrão idêntico já incluído antes, interjeições sem valor pedagógico):
   - Deixe "palavra_oculta" como "" (string vazia)
   - "texto_lacuna" = "" (vazio)
   - "dica" = "" (vazio)
   - "repeticoes" = número de vezes que aparece em sequência
4. NUNCA omita versos — use o campo "repeticoes" para indicar repetições em vez de duplicar linhas

EXEMPLO COMPLETO com repetições (copie exatamente este formato):
{
  "id": "can_custom_001",
  "titulo": "Bella Ciao",
  "artista": "Canto Partigiano",
  "nivel": "A2",
  "icone": "🌹",
  "tema": "storia",
  "estrofes": [
    {
      "id": 1,
      "texto_completo": "Una mattina mi sono alzato",
      "texto_lacuna": "Una mattina mi sono ___",
      "palavra_oculta": "alzato",
      "traducao": "Uma manhã eu me levantei",
      "dica": "participio passato de 'alzarsi' (levantar-se)",
      "repeticoes": 1
    },
    {
      "id": 2,
      "texto_completo": "O bella ciao, bella ciao, bella ciao ciao ciao",
      "texto_lacuna": "O ___ ciao, bella ciao, bella ciao ciao ciao",
      "palavra_oculta": "bella",
      "traducao": "Ó adeus bonita, adeus bonita, adeus adeus adeus",
      "dica": "aggettivo feminino singular — bela, bonita",
      "repeticoes": 3
    },
    {
      "id": 3,
      "texto_completo": "E questo è il fiore del partigiano",
      "texto_lacuna": "E questo è il ___ del partigiano",
      "palavra_oculta": "fiore",
      "traducao": "E esta é a flor do partigiano",
      "dica": "sostantivo maschile — flor",
      "repeticoes": 1
    },
    {
      "id": 4,
      "texto_completo": "O bella ciao, bella ciao, bella ciao ciao ciao",
      "texto_lacuna": "",
      "palavra_oculta": "",
      "traducao": "Ó adeus bonita, adeus bonita, adeus adeus adeus",
      "dica": "",
      "repeticoes": 2
    }
  ],
  "vocabulario_chave": ["alzarsi", "fiore", "partigiano"],
  "xp_recompensa": 40
}

MÚSICA: [SUBSTITUA AQUI — pode ser qualquer música, ex: "Azzurro de Adriano Celentano", "uma música que compus sobre Roma", "Volare de Domenico Modugno"]`,

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

    imitazione: `Crie frases italianas para prática de pronúncia. Retorne APENAS um array JSON, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. Gere de 8 a 12 frases relacionadas ao tema
2. "frase_italiano" = frase natural em italiano, nem curta demais nem longa demais
3. "frase_portugues" = tradução em português brasileiro
4. "contexto" = explicação em português de quando/como usar a frase (1-2 frases)
5. "nivel" deve ser A1, A2, B1, B2 ou C1
6. Deixe "audio_ipa" sempre como string vazia ""

EXEMPLO COMPLETO (copie exatamente este formato):
[
  {
    "id": "imi_custom_001",
    "frase_italiano": "Mi scusi, sa dov'è la stazione?",
    "frase_portugues": "Com licença, o senhor sabe onde é a estação?",
    "nivel": "A1",
    "contexto": "Use para pedir informações sobre direções de forma educada para um desconhecido.",
    "audio_ipa": "",
    "xp_recompensa": 15
  },
  {
    "id": "imi_custom_002",
    "frase_italiano": "Potrebbe ripetere più lentamente, per favore?",
    "frase_portugues": "Poderia repetir mais devagar, por favor?",
    "nivel": "A2",
    "contexto": "Use quando não entender o que alguém disse e precisar que repita mais devagar.",
    "audio_ipa": "",
    "xp_recompensa": 15
  }
]

TEMA DAS FRASES: [SUBSTITUA AQUI — ex: "pedir informações na rua", "no restaurante pedindo a conta", "expressões de surpresa e admiração"]`,

    vocab: `Crie palavras de vocabulário italiano. Retorne APENAS um array JSON, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. Gere de 12 a 20 palavras relacionadas ao tema
2. "genero": "m" para masculino, "f" para feminino, null para verbos e expressões
3. "plural": forma plural do substantivo/adjetivo, null para verbos
4. "exemplo" = frase real em italiano usando a palavra em contexto
5. "exemplo_pt" = tradução da frase de exemplo em português brasileiro
6. "audio_ipa" = transcrição IPA da palavra (só a palavra, não a frase)
7. "dificuldade": "facil" (básica), "medio" (intermediária) ou "dificil" (avançada)

EXEMPLO COMPLETO (copie exatamente este formato):
[
  {
    "id": "vocab_custom_001",
    "italiano": "treno",
    "portugues": "trem",
    "genero": "m",
    "plural": "treni",
    "exemplo": "Il treno parte alle nove dalla stazione centrale.",
    "exemplo_pt": "O trem parte às nove da estação central.",
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
    "exemplo": "Ho prenotato un posto sul treno per Venezia.",
    "exemplo_pt": "Reservei um lugar no trem para Veneza.",
    "categoria": "verbi",
    "dificuldade": "medio",
    "audio_ipa": "/prenoˈtaːre/"
  }
]

TEMA DO VOCABULÁRIO: [SUBSTITUA AQUI — ex: "vocabulário de viagem de trem", "palavras do restaurante e comida", "partes do corpo humano"]`
  },

  // ── Títulos do modal por tipo ────────────────────────────
  titulos: {
    dialogo:    '🤖 Adicionar Diálogo via IA',
    canzone:    '🤖 Adicionar Canção via IA',
    storia:     '🤖 Adicionar História via IA',
    imitazione: '🤖 Adicionar Imitação via IA',
    vocab:      '🤖 Adicionar Vocabulário via IA',
  },

  // ── Abrir modal ──────────────────────────────────────────
  abrir(tipo) {
    this.tipoAtual = tipo;
    const modal = document.getElementById('ia-import-modal');
    if (!modal) return;
    document.getElementById('ia-import-titulo').textContent = this.titulos[tipo] || '🤖 Adicionar via IA';
    document.getElementById('ia-prompt-text').textContent = this.prompts[tipo] || '';
    document.getElementById('ia-paste-area').value = '';
    const fb = document.getElementById('ia-feedback');
    if (fb) { fb.textContent = ''; fb.className = 'ia-feedback'; }
    modal.style.display = 'flex';
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
    localStorage.setItem(key, JSON.stringify([...existing, ...arr]));
    // Recarregar módulo se estiver ativo
    if (typeof Dialoghi !== 'undefined') {
      Dialoghi.dados = null;
      Dialoghi.renderizarSeletor?.();
    }
  },

  _importarCanzone(data) {
    const arr = Array.isArray(data) ? data : [data];
    const key = 'it_canzoni_custom';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    arr.forEach((d, i) => {
      if (!d.id) d.id = 'can_custom_' + Date.now() + '_' + i;
      d._custom = true;
    });
    localStorage.setItem(key, JSON.stringify([...existing, ...arr]));
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
    localStorage.setItem(key, JSON.stringify([...existing, ...arr]));
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
    localStorage.setItem(key, JSON.stringify([...existing, ...arr]));
    if (typeof Imitazione !== 'undefined') {
      Imitazione.dados = null;
      Imitazione.renderizar?.();
    }
  },

  _importarVocab(data) {
    const arr = Array.isArray(data) ? data : [data];
    const key = 'it_vocab_custom';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    arr.forEach((d, i) => {
      if (!d.id) d.id = 'vocab_custom_' + Date.now() + '_' + i;
      d._custom = true;
    });
    localStorage.setItem(key, JSON.stringify([...existing, ...arr]));
    // Injeta no vocabCache do App e re-renderiza
    if (typeof App !== 'undefined' && App.estado?.vocabCache) {
      arr.forEach(w => {
        if (!w.templo_num) w.templo_num = 0; // "Extra" / sem templo
        if (!App.estado.vocabCache.find(v => v.id === w.id)) {
          App.estado.vocabCache.push(w);
        }
      });
    }
    if (typeof Vocab !== 'undefined') Vocab.renderizar?.();
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
    localStorage.setItem(key, JSON.stringify(arr));
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
