// ============================================================
// ia-import.js — Adição de conteúdo via IA (Prompt-Assisted Import)
// Fluxo: copiar prompt → colar no LLM → colar JSON de volta → importar
// ============================================================

const IAImport = {
  tipoAtual: null,

  // ── Prompts por tipo ─────────────────────────────────────
  prompts: {
    dialogo: `Gere um diálogo em italiano para aprendizes. Retorne APENAS o JSON abaixo, sem texto extra:
{
  "id": "dial_custom_001",
  "titulo": "Nome do Diálogo",
  "icone": "🎭",
  "nivel": "A1",
  "contexto": "Descrição da situação em português",
  "turni": [
    {
      "id": 1,
      "personaggio": "Nomedalapessoa",
      "frase": "Frase em italiano",
      "traducao": "Tradução em português",
      "audio_ipa": ""
    },
    {
      "id": 2,
      "personaggio": "Tu",
      "frase": "",
      "traducao": "",
      "audio_ipa": "",
      "alternativas": ["opção A em italiano", "opção B em italiano", "opção C em italiano", "opção D em italiano"],
      "resposta_correta": 0
    }
  ],
  "vocabulario_chave": ["palavra1", "palavra2", "palavra3"],
  "xp_recompensa": 50
}

Notas:
- "nivel" deve ser A1, A2, B1, B2 ou C1
- Turnos do personagem só têm "frase" e "traducao"
- Turnos do "Tu" têm "alternativas" (4 opções) e "resposta_correta" (índice 0-3 da opção certa)
- Inclua 6 a 10 turnos no total alternando personagem e "Tu"

Tema do diálogo: [DESCREVA AQUI O TEMA — ex: pedir informações numa farmácia]`,

    canzone: `Gere dados de uma música italiana para aprendizes. Retorne APENAS o JSON abaixo, sem texto extra:
{
  "id": "can_custom_001",
  "titulo": "Nome da Música",
  "artista": "Nome do Artista",
  "nivel": "A2",
  "icone": "🎵",
  "tema": "amore",
  "estrofes": [
    {
      "id": 1,
      "texto_completo": "Verso completo da música em italiano",
      "texto_lacuna": "Verso com ___ no lugar de uma palavra-chave",
      "palavra_oculta": "palavra",
      "traducao": "Tradução do verso em português",
      "dica": "Dica gramatical sobre a palavra oculta"
    }
  ],
  "vocabulario_chave": ["palavra1", "palavra2", "palavra3"],
  "xp_recompensa": 40
}

Notas:
- "tema" pode ser: amore, vita, storia, natureza, festa, saudade
- "texto_lacuna" é igual ao "texto_completo" mas com a "palavra_oculta" substituída por ___
- Inclua de 4 a 8 estrofes/versos

Música: [NOME DA MÚSICA E ARTISTA — ex: "Volare" de Domenico Modugno]`,

    storia: `Gere uma história curta em italiano para aprendizes. Retorne APENAS o JSON abaixo, sem texto extra:
{
  "id": "stor_custom_001",
  "titulo": "Titolo in italiano",
  "titulo_pt": "Título em Português",
  "nivel": "A1",
  "icone": "📖",
  "autor": "Nome do Autor ou Tradizionale",
  "tema": "quotidiano",
  "descricao": "Breve descrição da história em italiano",
  "descricao_pt": "Breve descrição da história em português",
  "xp_recompensa": 80,
  "testo": [
    {
      "id": "stor_custom_001_p1",
      "italiano": "Primeiro parágrafo em italiano.",
      "portugues": "Primeiro parágrafo em português.",
      "parole": [
        {
          "parola": "palavra-chave",
          "traduzione": "tradução",
          "ipa": "/ipa/",
          "categoria": "sostantivo"
        }
      ]
    }
  ]
}

Notas:
- "nivel" deve ser A1, A2, B1, B2, C1 ou C2
- "tema" pode ser: quotidiano, fiaba, avventura, storia, cultura, umorismo
- Inclua de 4 a 8 parágrafos em "testo"
- Em cada parágrafo, "parole" deve ter de 2 a 4 palavras-chave com tradução e IPA
- "categoria" pode ser: sostantivo, verbo, aggettivo, espressione, avverbio

Tema/assunto da história: [DESCREVA AQUI — ex: uma manhã típica de uma família italiana]`,

    imitazione: `Gere frases italianas para prática de pronúncia. Retorne APENAS um array JSON, sem texto extra:
[
  {
    "id": "imi_custom_001",
    "frase_italiano": "Frase em italiano",
    "frase_portugues": "Tradução em português",
    "nivel": "A1",
    "contexto": "Quando e como usar esta frase",
    "audio_ipa": "",
    "xp_recompensa": 15
  },
  {
    "id": "imi_custom_002",
    "frase_italiano": "Segunda frase",
    "frase_portugues": "Tradução",
    "nivel": "A1",
    "contexto": "Contexto de uso",
    "audio_ipa": "",
    "xp_recompensa": 15
  }
]

Notas:
- "nivel" deve ser A1, A2, B1, B2 ou C1
- Gere de 5 a 10 frases relacionadas ao tema
- "contexto" deve explicar em português quando/como usar a frase
- Deixe "audio_ipa" como string vazia ""

Tema/contexto das frases: [DESCREVA AQUI — ex: expressões para pedir desculpas]`,

    vocab: `Gere palavras de vocabulário italiano. Retorne APENAS um array JSON, sem texto extra:
[
  {
    "id": "vocab_custom_001",
    "italiano": "parola",
    "portugues": "palavra em português",
    "genero": "m",
    "plural": "parole",
    "exemplo": "Frase de exemplo em italiano usando a palavra.",
    "exemplo_pt": "Frase de exemplo em português.",
    "categoria": "sostantivi",
    "dificuldade": "medio",
    "audio_ipa": "/ˈpa.ro.la/"
  }
]

Notas:
- "genero" deve ser "m" (masculino), "f" (feminino) ou null para verbos/expressões
- "plural" deve ser null para verbos
- "categoria" pode ser: sostantivi, verbi, aggettivi, espressioni, saudacoes, numeri, colori, corpo, famiglia, cibo, viaggio
- "dificuldade" pode ser: "facil", "medio" ou "dificil"
- Gere de 10 a 20 palavras relacionadas ao tema

Tema/categoria das palavras: [DESCREVA AQUI — ex: palavras relacionadas a viagem de trem]`
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
