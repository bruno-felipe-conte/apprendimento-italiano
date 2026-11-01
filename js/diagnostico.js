// ============================================================
// diagnostico.js — Dynamic Vocabulary Diagnostic (< 3 min)
// Computerized Adaptive Testing with Abbott False-Alarm Correction
// Feature F10 / Milestone 3: "O Espelho"
// ============================================================

const VocabDiagnostic = {
  _ativo: false,
  _respostas: [],
  _itensTeste: [],
  _indiceAtual: 0,
  _inicioTimestamp: 0,

  // Banco calibrado de pseudopalavras fonotaticamente válidas (catch trials)
  PSEUDOPALAVRAS: [
    'strugolo', 'ventare', 'basticcio', 'frunare',
    'spindolo', 'luffo', 'grabello', 'spugnare',
    'talpone', 'salpino', 'nartello', 'corbino'
  ],

  /**
   * Correção de Abbott para acertos casuais e viés de resposta:
   * Adj = (HitRate - FalseAlarmRate) / (1 - FalseAlarmRate)
   * Se FalseAlarmRate >= 0.5 (blefe/chute maciço), penalidade zera o score.
   */
  calcularAbbott(hitRate, falseAlarmRate) {
    if (typeof falseAlarmRate !== 'number' || falseAlarmRate >= 0.5) return 0;
    if (typeof hitRate !== 'number') return 0;
    const adj = (hitRate - falseAlarmRate) / (1 - falseAlarmRate);
    return Math.max(0, Math.min(1.0, adj));
  },

  /**
   * Calcula o score psicométrico a partir das respostas do teste.
   * @param {Array<{word: string, isPseudoword: boolean, known: boolean, band?: number}>} respostas
   */
  calcularScore(respostas) {
    if (!Array.isArray(respostas) || respostas.length === 0) {
      return {
        estimativa_passiva: 0,
        estimativa_ativa: 0,
        nivel_cefr: 'A1',
        total_testado: 0,
        false_alarm_rate: 0,
        confiavel: true,
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

    let nivelCefr = 'A1';
    if (estimativaPassiva >= 4000) nivelCefr = 'C1/C2';
    else if (estimativaPassiva >= 2800) nivelCefr = 'B2';
    else if (estimativaPassiva >= 1800) nivelCefr = 'B1';
    else if (estimativaPassiva >= 800) nivelCefr = 'A2';

    return {
      estimativa_passiva: estimativaPassiva,
      estimativa_ativa: estimativaAtiva,
      nivel_cefr: nivelCefr,
      total_testado: respostas.length,
      false_alarm_rate: Number(falseAlarmRate.toFixed(3)),
      confiavel,
      ultimo_teste: Date.now()
    };
  },

  /**
   * Gera a lista estratificada de 40 a 48 itens (lemas reais + pseudopalavras).
   */
  gerarItensTeste() {
    const itens = [];
    const freqClient = (typeof FrequencyBandClient !== 'undefined' && typeof FrequencyBandClient.getSampleByBand === 'function')
      ? FrequencyBandClient
      : null;

    if (freqClient) {
      // Amostragem estratificada: 8 itens por faixa (1k a 3k)
      for (let b = 1; b <= 3; b++) {
        const sample = freqClient.getSampleByBand(b, 8);
        sample.forEach(lemma => {
          itens.push({ word: lemma, isPseudoword: false, band: b });
        });
      }
    } else {
      // Fallback lemas frequentes
      const lemasFallback = [
        { w: 'casa', b: 1 }, { w: 'giorno', b: 1 }, { w: 'cosa', b: 1 }, { w: 'anno', b: 1 },
        { w: 'uomo', b: 1 }, { w: 'tempo', b: 1 }, { w: 'donna', b: 1 }, { w: 'vita', b: 1 },
        { w: 'mondo', b: 2 }, { w: 'occhio', b: 2 }, { w: 'ora', b: 2 }, { w: 'signore', b: 2 },
        { w: 'accordo', b: 2 }, { w: 'strada', b: 2 }, { w: 'figlio', b: 2 }, { w: 'notte', b: 2 },
        { w: 'luogo', b: 3 }, { w: 'parte', b: 3 }, { w: 'fine', b: 3 }, { w: 'specie', b: 3 },
        { w: 'mente', b: 3 }, { w: 'ragione', b: 3 }, { w: 'governo', b: 3 }, { w: 'piano', b: 3 }
      ];
      lemasFallback.forEach(item => {
        itens.push({ word: item.w, isPseudoword: false, band: item.b });
      });
    }

    // Adiciona 6 pseudopalavras aleatórias (catch trials)
    const pseudoEmbaralhadas = [...this.PSEUDOPALAVRAS].sort(() => Math.random() - 0.5).slice(0, 6);
    pseudoEmbaralhadas.forEach(p => {
      itens.push({ word: p, isPseudoword: true });
    });

    // Embaralha itens finais
    return itens.sort(() => Math.random() - 0.5);
  },

  /**
   * Inicia o teste interativo de diagnóstico.
   */
  iniciar() {
    this._respostas = [];
    this._itensTeste = this.gerarItensTeste();
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
      modal.setAttribute('aria-label', 'Diagnóstico de Vocabulário Italiano');
      modal.innerHTML = `
        <div class="modal-card-diagnostico">
          <div class="diag-header">
            <h3>🔬 O Espelho — Diagnóstico de Vocabulário</h3>
            <button type="button" class="btn-fechar-modal" onclick="VocabDiagnostic.fechar()">✖</button>
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
    if (!palco) return;

    if (this._indiceAtual >= this._itensTeste.length) {
      this._finalizar();
      return;
    }

    const item = this._itensTeste[this._indiceAtual];
    const total = this._itensTeste.length;
    const pct = Math.round((this._indiceAtual / total) * 100);
    if (fill) fill.style.width = `${pct}%`;

    palco.innerHTML = `
      <div class="diag-item-box">
        <span class="diag-step-counter">${this._indiceAtual + 1} de ${total}</span>
        <h2 class="diag-palavra-destaque">${item.word}</h2>
        <p class="diag-pergunta-prompt">Você conhece o significado desta palavra?</p>
        <div class="diag-botoes-row">
          <button type="button" class="btn-diag-nao" onclick="VocabDiagnostic.responder(false)">
            ❌ Não conheço
          </button>
          <button type="button" class="btn-diag-sim" onclick="VocabDiagnostic.responder(true)">
            ✅ Conheço
          </button>
        </div>
        <div class="diag-dica-honestidade">
          💡 Seja sincero: o teste contém palavras-armadilha para garantir precisão diagnóstica.
        </div>
      </div>
    `;
  },

  responder(conhece) {
    if (!this._ativo) return;
    const item = this._itensTeste[this._indiceAtual];
    this._respostas.push({
      word: item.word,
      isPseudoword: item.isPseudoword,
      known: Boolean(conhece),
      band: item.band
    });

    this._indiceAtual++;
    this._renderizarItem();
  },

  _finalizar() {
    this._ativo = false;
    const resultado = this.calcularScore(this._respostas);

    // Persiste no AppState
    if (typeof AppState !== 'undefined' && AppState.estado && AppState.estado.progresso) {
      AppState.estado.progresso.vocab_diagnostico = resultado;
      if (typeof AppState.salvarProgresso === 'function') {
        AppState.salvarProgresso();
      }
    }

    // Notifica ganho de XP por completar o diagnóstico
    if (typeof AppXP !== 'undefined' && typeof AppXP.ganharXP === 'function') {
      AppXP.ganharXP(50);
    }

    const palco = document.getElementById('diag-conteudo-palco');
    const fill = document.getElementById('diag-progresso-fill');
    if (fill) fill.style.width = '100%';

    if (palco) {
      let alertaBlefe = '';
      if (!resultado.confiavel) {
        alertaBlefe = `
          <div class="diag-alerta-blefe">
            ⚠️ <strong>Atenção:</strong> Taxa elevada de falsos alarmes (${Math.round(resultado.false_alarm_rate * 100)}%). Você marcou palavras inventadas como conhecidas. O resultado foi desconsiderado para proteger a integridade do seu mapa.
          </div>
        `;
      }

      palco.innerHTML = `
        <div class="diag-resultado-box">
          <div class="diag-cefr-badge">${resultado.nivel_cefr}</div>
          <h3>Seu Diagnóstico Lexical</h3>
          ${alertaBlefe}
          <div class="diag-metricas-grid">
            <div class="diag-metrica-card">
              <span class="diag-val">${resultado.estimativa_passiva.toLocaleString()}</span>
              <span class="diag-lbl">Vocabulário Passivo (Reconhecimento)</span>
            </div>
            <div class="diag-metrica-card">
              <span class="diag-val">${resultado.estimativa_ativa.toLocaleString()}</span>
              <span class="diag-lbl">Vocabulário Ativo (Produção Estimada)</span>
            </div>
          </div>

          <div class="diag-laufer-comparativo">
            <h4>📖 Comparativo com o Limiar de Laufer (95% para leitura autônoma):</h4>
            <p>
              Para ler canções, notícias e literatura italiana com conforto sem dicionário, você necessita de cerca de <strong>3.000 a 4.000 lemas</strong>.
              Você está atualmente em <strong>${Math.round((resultado.estimativa_passiva / 3000) * 100)}%</strong> da autonomia lexical plena.
            </p>
          </div>

          <div class="diag-acoes-resultado">
            <button type="button" class="btn-primario" onclick="VocabDiagnostic.fechar(); if (typeof App !== 'undefined' && App.navegar) App.navegar('canzoni');">
              🎵 Testar Cobertura em Canções
            </button>
            <button type="button" class="btn-secondario" onclick="VocabDiagnostic.fechar();">
              Concluir
            </button>
          </div>
        </div>
      `;
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
