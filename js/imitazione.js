// ============================================================
// imitazione.js — Il Dojo di Pronuncia & Fonetica
// Reconhecimento de fala, análise fonética palavra por palavra,
// reprodução em velocidade dupla e auto-escuta comparativa (MediaRecorder)
// ============================================================

const Imitazione = {
  dados: null,
  itemAtual: 0,
  recognition: null,
  isRecording: false,
  _filtroNivel: '',
  _filtroOrigem: '',
  _filtroExpandido: false,
  _faseAtual: 'pratica',
  _mostrarDetalhes: false,
  _listaAtual: null,

  // Gravação de áudio do usuário (MediaRecorder para auto-escuta comparativa)
  _mediaRecorder: null,
  _mediaStream: null,
  _audioChunks: [],
  _userAudioUrl: null,
  _userAudioPlayer: null,

  async carregar() {
    if (!this.dados) {
      try {
        const cached = localStorage.getItem('it_swr_imitazioni');
        if (cached) {
          this.dados = JSON.parse(cached);
          fetch('data/imitazioni.json')
            .then(r => r.ok ? r.json() : null)
            .then(fresh => {
              if (fresh && Array.isArray(fresh.imitazioni)) {
                this.dados = fresh;
                try { localStorage.setItem('it_swr_imitazioni', JSON.stringify(fresh)); } catch (_) {}
              }
            })
            .catch(() => {});
        }
      } catch (_) {}
    }

    if (!this.dados) {
      try {
        const r = await fetch('data/imitazioni.json');
        this.dados = await r.json();
        try { localStorage.setItem('it_swr_imitazioni', JSON.stringify(this.dados)); } catch (_) {}
      } catch (e) {
        console.error('Erro ao carregar imitazioni.json', e);
        this.dados = { imitazioni: [] };
      }
    }

    // Mescla frases customizadas — custom primeiro
    try {
      const custom = JSON.parse(localStorage.getItem('it_imitazioni_custom') || '[]');
      if (custom.length) {
        this.dados.imitazioni = [...custom, ...(this.dados.imitazioni || [])];
      }
    } catch (e) {}
  },

  async renderizar() {
    await this.carregar();
    this._aplicarFiltro(false);
  },

  toggleFiltros(forcar) {
    this._filtroExpandido = typeof forcar === 'boolean' ? forcar : !this._filtroExpandido;
    this._renderizarFiltros();
  },

  toggleDetalhes() {
    this._mostrarDetalhes = !this._mostrarDetalhes;
    const grid = document.getElementById('dojo-info-grid');
    const btn = document.getElementById('btn-dojo-details-toggle');
    if (grid) grid.style.display = this._mostrarDetalhes ? 'grid' : 'none';
    if (btn) btn.innerHTML = `<span>${this._mostrarDetalhes ? '▾ Ocultar Dicas' : '▸ Dica & Contexto'}</span>`;
  },

  selecionarOrigem(origem) {
    this._filtroOrigem = origem;
    this._filtroExpandido = false;
    this._aplicarFiltro(true);
  },

  selecionarNivel(lvl) {
    this._filtroNivel = (this._filtroNivel === lvl) ? '' : lvl;
    this._filtroExpandido = false;
    this._aplicarFiltro(true);
  },

  _aplicarFiltro(redefinirItem = true) {
    let todas = this.dados?.imitazioni || [];
    if (this._filtroOrigem === 'custom') todas = todas.filter(f => f._custom || f.custom);
    if (this._filtroOrigem === 'nativo') todas = todas.filter(f => !f._custom && !f.custom);
    this._listaAtual = this._filtroNivel
      ? todas.filter(f => f.nivel === this._filtroNivel)
      : todas;
    if (redefinirItem) this.itemAtual = 0;
    this._renderizarFiltros();
    this.mostrarDesafio();
  },

  _renderizarFiltros() {
    const c = document.getElementById('imitazione-container');
    if (!c) return;

    const todasRaw = this.dados?.imitazioni || [];
    const niveis = ['A1','A2','B1','B2','C1'];
    const counts = {};
    todasRaw.forEach(f => { counts[f.nivel] = (counts[f.nivel]||0)+1; });
    const nC = todasRaw.filter(f => f._custom || f.custom).length;
    const nN = todasRaw.length - nC;
    const _o = this._filtroOrigem;
    const _n = this._filtroNivel;

    let bar = document.getElementById('imit-filtro-bar');
    if (!bar) {
      bar = document.createElement('div');
      bar.id = 'imit-filtro-bar';
      c.parentElement?.insertBefore(bar, c);
    }

    const lista = this._listaAtual || todasRaw;
    const totalLista = lista.length;
    const origemNome = _o === 'custom' ? '🤖 Adicionadas' : (_o === 'nativo' ? '📚 Nativas' : 'Todas');
    const nivelNome = _n ? `Nível ${_n}` : 'Todos os Níveis';

    if (!this._filtroExpandido) {
      bar.className = 'dojo-filtro-bar-compacta';
      bar.innerHTML = `
        <div class="dojo-filtro-compacto-wrap" onclick="Imitazione.toggleFiltros()">
          <div class="dojo-filtro-badge-group">
            <span class="dojo-filtro-chip">🏷️ ${nivelNome} · ${origemNome}</span>
            <span class="dojo-filtro-count">${this.itemAtual + 1} de ${totalLista}</span>
          </div>
          <button type="button" class="btn-dojo-toggle-filtro" aria-label="Abrir filtros de nível e origem">
            Filtros ▾
          </button>
        </div>
      `;
      return;
    }

    bar.className = 'dojo-filtro-bar';
    const pillOrigem = (v, label, count) => `
      <button type="button" class="dojo-level-pill ${_o === v ? 'ativo' : ''}"
              onclick="Imitazione.selecionarOrigem('${v}')">
        ${label} (${count})
      </button>
    `;

    const pillNivel = (lvl) => `
      <button type="button" class="dojo-level-pill ${_n === lvl ? 'ativo' : ''}"
              onclick="Imitazione.selecionarNivel('${lvl}')">
        ${lvl} (${counts[lvl] || 0})
      </button>
    `;

    bar.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;width:100%;margin-bottom:0.35rem">
        <span style="font-size:0.78rem;font-weight:700;color:var(--cor-veneziano-escuro,#6B1A2A);text-transform:uppercase;letter-spacing:0.04em">
          Seletor de Nível e Origem
        </span>
        <button type="button" class="btn-dojo-fechar-filtro" onclick="Imitazione.toggleFiltros(false)" style="background:none;border:none;cursor:pointer;font-size:0.76rem;color:#7a6245;font-weight:700">
          Recolher ▴
        </button>
      </div>
      <div class="dojo-level-pills">
        <button type="button" class="btn-ia-add" onclick="IAImport.abrir('imitazione')" style="margin-right:0.3rem">🤖 + IA</button>
        ${pillOrigem('', 'Todas', todasRaw.length)}
        ${nC ? pillOrigem('custom', '🤖 Adicionadas', nC) : ''}
        ${nN ? pillOrigem('nativo', '📚 Nativas', nN) : ''}
      </div>
      <div class="dojo-level-pills" style="margin-top:0.35rem">
        <span style="font-size:0.75rem;font-weight:700;color:var(--cor-inchiostro-claro, #5A4535);margin-right:0.2rem">NÍVEL:</span>
        ${niveis.map(lvl => pillNivel(lvl)).join('')}
      </div>
    `;
  },

  // Reprodução em velocidade dupla do modelo nativo
  tocarModelo(taxa = 1.0) {
    const lista = this._listaAtual || this.dados?.imitazioni || [];
    const item = lista[this.itemAtual];
    if (!item) return;
    const frase = item.frase_italiano || item.frase;

    const wave = document.getElementById('dojo-wave');
    if (wave) wave.classList.add('active');

    App.pronunciar(frase, taxa);

    setTimeout(() => {
      const w = document.getElementById('dojo-wave');
      if (w) w.classList.remove('active');
    }, Math.max(1200, frase.length * 75 * (1 / taxa)));
  },

  // Inicializa o gravador local de áudio (fallback para browsers sem SpeechRecognition)
  async _iniciarGravacaoMidia() {
    this._audioChunks = [];
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      alert("Seu navegador não possui suporte a gravação de áudio.");
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this._mediaStream = stream;
      
      // Detecção de formato suportado (WebM para Chrome/Android, MP4 para iOS/Safari)
      let mimeType = '';
      if (typeof MediaRecorder !== 'undefined' && typeof MediaRecorder.isTypeSupported === 'function') {
        if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) mimeType = 'audio/webm;codecs=opus';
        else if (MediaRecorder.isTypeSupported('audio/webm')) mimeType = 'audio/webm';
        else if (MediaRecorder.isTypeSupported('audio/mp4')) mimeType = 'audio/mp4';
        else if (MediaRecorder.isTypeSupported('audio/aac')) mimeType = 'audio/aac';
      }

      this._mediaRecorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream);
      this._mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) this._audioChunks.push(e.data);
      };
      this._mediaRecorder.onstop = () => {
        if (this._audioChunks.length > 0) {
          const tipoFinal = mimeType || 'audio/webm';
          const blob = new Blob(this._audioChunks, { type: tipoFinal });
          if (this._userAudioUrl) URL.revokeObjectURL(this._userAudioUrl);
          this._userAudioUrl = URL.createObjectURL(blob);
          
          const st = document.getElementById('dojo-mic-status');
          if (st) {
            st.innerHTML = '🎙️ Gravação concluída! Use <strong>🎧 Ouvir Minha Gravação</strong> para comparar com o áudio nativo.';
          }
          this._mostrarFeedbackMediaRecorder();
        }
        if (this._mediaStream) {
          this._mediaStream.getTracks().forEach(t => t.stop());
          this._mediaStream = null;
        }
      };
      this._mediaRecorder.start();
      this.isRecording = true;
      const btn = document.getElementById('dojo-btn-mic');
      if (btn) btn.classList.add('recording');
      const st = document.getElementById('dojo-mic-status');
      if (st) st.innerHTML = '<span style="color:#E74C3C">●</span> Gravando sua voz... Fale com confiança!';
    } catch (err) {
      console.warn('[Imitazione] Erro ao acessar microfone via getUserMedia:', err);
      const st = document.getElementById('dojo-mic-status');
      if (st) st.innerText = 'Permissão de microfone negada ou indisponível.';
    }
  },

  _pararGravacaoMidia() {
    if (this._mediaRecorder && this._mediaRecorder.state !== 'inactive') {
      try { this._mediaRecorder.stop(); } catch (_) {}
    }
    this.isRecording = false;
    const btn = document.getElementById('dojo-btn-mic');
    if (btn) btn.classList.remove('recording');
  },

  tocarMinhaGravacao() {
    if (!this._userAudioUrl) return;
    if (this._userAudioPlayer) {
      this._userAudioPlayer.pause();
      this._userAudioPlayer.currentTime = 0;
    }
    this._userAudioPlayer = new Audio(this._userAudioUrl);
    this._userAudioPlayer.play();
  },

  _mostrarFeedbackMediaRecorder() {
    const viewport = document.getElementById('dojo-card-viewport');
    if (!viewport) return;
    const lista = this._listaAtual || this.dados?.imitazioni || [];
    const item = lista[this.itemAtual];
    this._faseAtual = 'feedback';

    viewport.innerHTML = `
      <div class="dojo-hero-card fase-feedback">
        <div class="dojo-progress-hud">
          <span>Frase <strong>${this.itemAtual + 1}</strong> de ${lista.length}</span>
          <span class="dojo-badge-nivel">${item?.nivel || 'A1'}</span>
        </div>

        <div class="dojo-fb-header">
          <div class="dojo-fb-title" style="color:#2E86C1">🎙️ Áudio Gravado!</div>
          <div class="dojo-fb-score" style="font-size:0.92rem;color:var(--cor-inchiostro);margin-top:0.3rem">
            Sua gravação está pronta para comparação com a pronúncia nativa:
          </div>
        </div>

        <div class="dojo-replay-toolbar" style="margin:1.4rem 0">
          <button type="button" class="btn-dojo-replay" onclick="Imitazione.tocarMinhaGravacao()">
            <span>🎧</span> Minha Gravação
          </button>
          <button type="button" class="btn-dojo-replay" onclick="Imitazione.tocarModelo(1.0)">
            <span>🔊</span> Modelo Nativo
          </button>
        </div>

        <div class="dojo-action-buttons">
          <button type="button" class="btn-secondario btn-dojo-action" onclick="Imitazione.mostrarDesafio()">
            🔄 Gravar Novamente
          </button>
          <button type="button" class="btn-primario btn-dojo-action" onclick="Imitazione.avancar()">
            ➡️ Próxima Frase
          </button>
        </div>
      </div>
    `;
  },

  // ── Parar qualquer gravação ativa ───────────────────────────
  pararGravacao() {
    if (this.recognition) {
      try { this.recognition.stop(); } catch (_) {}
      this.recognition = null;
    }
    this._pararGravacaoMidia();
    this.isRecording = false;
    const btn = document.getElementById('dojo-btn-mic');
    if (btn) btn.classList.remove('recording');
    const st = document.getElementById('dojo-mic-status');
    if (st && st.innerText.includes('Ouvindo')) {
      st.innerText = 'Processando dicção...';
    }
  },

  // ── Iniciar ou alternar gravação no Modo Imitação ────────────
  toggleGravacao() {
    // 1. Pausa e cancela qualquer reprodução de áudio / síntese TTS em andamento
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (_) {}
    }
    if (typeof VoiceEngine !== 'undefined' && VoiceEngine.parar) {
      try { VoiceEngine.parar(); } catch (_) {}
    }
    if (this._userAudioPlayer) {
      try { this._userAudioPlayer.pause(); this._userAudioPlayer.currentTime = 0; } catch (_) {}
    }

    // 2. Se já estiver gravando, para imediatamente
    if (this.isRecording) {
      this.pararGravacao();
      return;
    }

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

    // 3. Se o browser suporta Web Speech API (Chrome no Android, Safari no iOS, Edge, Desktop)
    if (SR) {
      // Cria UMA NOVA instância por sessão (evita o bug de InvalidStateError no iOS Safari)
      const rec = new SR();
      rec.lang = 'it-IT';
      rec.continuous = false;
      rec.interimResults = false;
      rec.maxAlternatives = 1;

      rec.onstart = () => {
        this.isRecording = true;
        const btn = document.getElementById('dojo-btn-mic');
        if (btn) btn.classList.add('recording');
        const st = document.getElementById('dojo-mic-status');
        if (st) st.innerHTML = '<span style="color:#E74C3C">●</span> Ouvindo... Fale com confiança!';
      };

      rec.onresult = (event) => {
        const speechResult = event.results[0][0].transcript;
        this.avaliarPronuncia(speechResult);
      };

      rec.onerror = (event) => {
        console.warn('[Imitazione] Erro no reconhecimento de voz:', event?.error);
        this.isRecording = false;
        this.recognition = null;
        const btn = document.getElementById('dojo-btn-mic');
        if (btn) btn.classList.remove('recording');
        const st = document.getElementById('dojo-mic-status');
        
        if (st) {
          if (event?.error === 'not-allowed') {
            st.innerHTML = '⚠️ Permissão negada. Toque no cadeado da barra de endereços e permita o microfone.';
          } else if (event?.error === 'no-speech') {
            st.innerText = 'Nenhuma fala detectada. Fale mais próximo do microfone e tente novamente.';
          } else if (event?.error === 'audio-capture') {
            st.innerText = '⚠️ Microfone ocupado por outro app ou indisponível.';
          } else if (event?.error === 'network') {
            st.innerText = '⚠️ Erro de rede no serviço de voz. Verifique sua conexão à internet.';
          } else if (event?.error !== 'aborted') {
            st.innerText = I18n.t('imit_erro_ouvir');
          }
        }
      };

      rec.onend = () => {
        this.isRecording = false;
        this.recognition = null;
        const btn = document.getElementById('dojo-btn-mic');
        if (btn) btn.classList.remove('recording');
        const st = document.getElementById('dojo-mic-status');
        if (st && st.innerText.includes('Ouvindo')) {
          st.innerText = 'Processando dicção...';
        }
      };

      this.recognition = rec;

      // Disparo SÍNCRONO direto no evento de toque/clique para preservar ativação do usuário
      try {
        rec.start();
      } catch (err) {
        console.warn('[Imitazione] Falha ao disparar SpeechRecognition.start():', err);
        this.isRecording = false;
        this.recognition = null;
        // Fallback para gravação direta via MediaRecorder se start() falhar
        this._iniciarGravacaoMidia();
      }
      return;
    }

    // 4. Fallback resiliente para browsers sem SpeechRecognition (ex: Firefox Android, navegadores embutidos)
    this._iniciarGravacaoMidia();
  },

  normalizeText(text) {
    return (text || '').toLowerCase().replace(/[.,!?;:«»""'’]/g, '').trim();
  },

  // Avaliação analítica palavra por palavra com transição in-place
  avaliarPronuncia(textoOuvido) {
    const lista = this._listaAtual || this.dados.imitazioni;
    const item = lista[this.itemAtual];
    if (!item) return;
    const esperadoFrase = item.frase_italiano || item.frase;

    const palavrasEsperadas = esperadoFrase.split(/\s+/);
    const palavrasOuvidas = this.normalizeText(textoOuvido).split(/\s+/);

    let acertos = 0;
    const tokensDiagnostico = palavrasEsperadas.map(palavraAlvo => {
      const alvoNorm = this.normalizeText(palavraAlvo);
      if (!alvoNorm) return { palavra: palavraAlvo, status: 'correta' };

      // 1. Acerto exato
      if (palavrasOuvidas.includes(alvoNorm)) {
        acertos++;
        return { palavra: palavraAlvo, status: 'correta' };
      }

      // 2. Acerto aproximado (tolerância fonética / prefixo)
      const quase = palavrasOuvidas.some(o => {
        if (Math.abs(o.length - alvoNorm.length) > 2) return false;
        let matches = 0;
        for (let i = 0; i < Math.min(o.length, alvoNorm.length); i++) {
          if (o[i] === alvoNorm[i]) matches++;
        }
        return (matches / Math.max(o.length, alvoNorm.length)) >= 0.7;
      });

      if (quase) {
        acertos += 0.8;
        return { palavra: palavraAlvo, status: 'proxima' };
      }

      // 3. Necessita atenção
      return { palavra: palavraAlvo, status: 'revisar' };
    });

    const precisao = Math.min(100, Math.round((acertos / palavrasEsperadas.length) * 100));

    let titulo = '';
    let cor = '';
    let xpGanho = 0;

    if (precisao >= 80) {
      titulo = 'Perfetto! 🌟';
      cor = '#27AE60';
      xpGanho = item.xp_recompensa || 15;
      if (typeof Progressao !== 'undefined') Progressao.ganhar(xpGanho);
      else if (typeof App !== 'undefined') App.ganharXP(xpGanho);
    } else if (precisao >= 50) {
      titulo = 'Quasi! 👍';
      cor = '#E67E22';
      xpGanho = Math.round((item.xp_recompensa || 15) * 0.5);
      if (typeof Progressao !== 'undefined') Progressao.ganhar(xpGanho);
    } else {
      titulo = 'Riprova! 🔄';
      cor = '#C0392B';
    }

    this._faseAtual = 'feedback';
    const viewport = document.getElementById('dojo-card-viewport');
    if (!viewport) return;

    viewport.innerHTML = `
      <div class="dojo-hero-card fase-feedback">
        <div class="dojo-progress-hud">
          <span>Frase <strong>${this.itemAtual + 1}</strong> de ${lista.length}</span>
          <span class="dojo-badge-nivel">${item.nivel || 'A1'}</span>
        </div>

        <div class="dojo-fb-header">
          <div class="dojo-fb-title" style="color:${cor}">${titulo}</div>
          <div class="dojo-fb-score">
            Precisão de Dicção: <strong>${precisao}%</strong>
            ${xpGanho > 0 ? `<span class="dojo-xp-badge">+${xpGanho} XP</span>` : ''}
          </div>
        </div>

        <div class="dojo-fb-prompt-reminder">
          "${item.frase_italiano || item.frase}"
        </div>

        <div class="dojo-words-breakdown">
          ${tokensDiagnostico.map(t => `
            <button type="button" class="dojo-word-pill ${t.status}"
                    onclick="App.pronunciar('${t.palavra.replace(/'/g, "\\'")}')"
                    title="Ouvir som de '${t.palavra}'">
              <span class="word-pill-status">${t.status === 'correta' ? '✓' : (t.status === 'proxima' ? '≈' : '•')}</span>
              <span class="word-pill-txt">${t.palavra}</span>
            </button>
          `).join('')}
        </div>

        <div class="dojo-ouviu-texto">
          Ouvimos: <em>"${this.normalizeText(textoOuvido) ? textoOuvido : '...'}"</em>
        </div>

        <!-- Barra de comparação de áudio -->
        <div class="dojo-replay-toolbar">
          ${this._userAudioUrl ? `
            <button type="button" class="btn-dojo-replay" onclick="Imitazione.tocarMinhaGravacao()">
              <span>🎧</span> Minha Gravação
            </button>
          ` : ''}
          <button type="button" class="btn-dojo-replay" onclick="Imitazione.tocarModelo(1.0)">
            <span>🔊</span> Modelo Nativo
          </button>
        </div>

        <!-- Botões de Ação In-Place -->
        <div class="dojo-action-buttons">
          <button type="button" class="btn-secondario btn-dojo-action" onclick="Imitazione.mostrarDesafio()">
            🔄 Tentar Novamente
          </button>
          <button type="button" class="btn-primario btn-dojo-action" onclick="Imitazione.avancar()">
            ➡️ Próxima Frase
          </button>
        </div>
      </div>
    `;
  },

  avancar() {
    this.itemAtual++;
    const lista = this._listaAtual || this.dados?.imitazioni || [];
    if (this.itemAtual >= lista.length) {
      this.mostrarFinal();
    } else {
      this.mostrarDesafio();
    }
  },

  mostrarDesafio() {
    const c = document.getElementById('imitazione-container');
    if (!c) return;
    const lista = this._listaAtual || this.dados?.imitazioni || [];
    const item = lista[this.itemAtual];
    if (!item) { this.mostrarFinal(); return; }

    this._faseAtual = 'pratica';
    const frase = item.frase_italiano || item.frase;
    const traducao = item.frase_portugues || item.traducao;
    const contexto = item.contexto || 'Frase di uso comune in conversazione.';

    // Se o container ainda não possui o viewport estrutural, cria o esqueleto
    let viewport = document.getElementById('dojo-card-viewport');
    if (!viewport) {
      c.innerHTML = `
        <div class="imitazione-dojo">
          <div class="dojo-card-viewport" id="dojo-card-viewport"></div>
        </div>
      `;
      viewport = document.getElementById('dojo-card-viewport');
    }

    viewport.innerHTML = `
      <div class="dojo-hero-card fase-pratica">
        <div class="dojo-progress-hud">
          <span>Frase <strong>${this.itemAtual + 1}</strong> de ${lista.length}</span>
          <span class="dojo-badge-nivel">${item.nivel || 'A1'}</span>
        </div>

        <div class="dojo-hero-badge">
          <span>🎙️ Studio di Pronuncia</span>
          ${item._custom ? ` · <button type="button" onclick="IAImport.excluir('imitazione','${item.id}')" style="background:none;border:none;color:#C0392B;cursor:pointer;font-size:0.75rem;font-weight:700">🗑️ Excluir</button>` : ''}
        </div>

        <div class="dojo-hero-frase">"${frase}"</div>
        <div class="dojo-hero-traducao">"${traducao}"</div>

        <!-- Toggle sutil para Contexto & Dica de Ritmo -->
        <div class="dojo-details-toggle">
          <button type="button" id="btn-dojo-details-toggle" class="btn-dojo-toggle-details" onclick="Imitazione.toggleDetalhes()">
            <span>${this._mostrarDetalhes ? '▾ Ocultar Dicas' : '▸ Dica & Contexto'}</span>
          </button>
        </div>

        <div id="dojo-info-grid" class="dojo-info-grid" style="display:${this._mostrarDetalhes ? 'grid' : 'none'}">
          <div class="dojo-info-box contexto">
            <div class="dojo-info-title">🏛️ Contexto</div>
            <div class="dojo-info-content">${contexto}</div>
          </div>
          <div class="dojo-info-box fonetica">
            <div class="dojo-info-title">🎵 Dica de Ritmo</div>
            <div class="dojo-info-content">${item.dica_fonetica || 'Pronuncie com abertura vocal clara e ritmo cadenciado.'}</div>
          </div>
        </div>

        <!-- Estúdio de Áudio do Modelo Nativo -->
        <div class="dojo-audio-station">
          <button type="button" class="btn-dojo-audio normal" onclick="Imitazione.tocarModelo(1.0)">
            <span>🔊</span> Ouvir Modelo (1.0x)
          </button>
          <button type="button" class="btn-dojo-audio slow" onclick="Imitazione.tocarModelo(0.75)">
            <span>🐢</span> Lento (0.75x)
          </button>
          <div class="dojo-soundwave" id="dojo-wave">
            <span></span><span></span><span></span><span></span><span></span>
          </div>
        </div>

        <!-- Estúdio de Gravação do Aluno -->
        <div class="dojo-mic-studio">
          <div class="dojo-mic-btn-wrapper">
            <button type="button" id="dojo-btn-mic" class="dojo-mic-btn" onclick="Imitazione.toggleGravacao()" title="Clique para falar">
              🎙️
            </button>
          </div>
          <div id="dojo-mic-status" class="dojo-mic-status">
            Toque no microfone e pronuncie a frase
          </div>
        </div>
      </div>
    `;

    // Atualiza o contador na barra compacta de filtro se ela estiver recolhida
    const countEl = document.querySelector('.dojo-filtro-count');
    if (countEl) countEl.textContent = `${this.itemAtual + 1} de ${lista.length}`;
  },

  mostrarFinal() {
    const c = document.getElementById('imitazione-container');
    if (!c) return;
    const lista = this._listaAtual || this.dados?.imitazioni || [];
    this._filtroExpandido = true;
    this._renderizarFiltros();

    c.innerHTML = `
      <div class="imitazione-dojo">
        <div class="dojo-card-viewport">
          <div class="dojo-hero-card" style="padding:2.5rem 1.2rem">
            <div style="font-size:3.5rem;margin-bottom:0.8rem">🏆</div>
            <h3 style="font-family:'Cinzel',serif;color:#9B2335;font-size:1.8rem;margin-bottom:0.6rem">Bravissimo!</h3>
            <p style="font-size:1.05rem;color:var(--cor-inchiostro);margin-bottom:1.4rem;max-width:480px;margin-left:auto;margin-right:auto">
              Você completou com sucesso todas as ${lista.length} frases do treinamento de pronúncia!
            </p>
            <div class="dojo-action-buttons">
              <button type="button" class="btn-secondario btn-dojo-action" onclick="Imitazione._aplicarFiltro(true)">
                🔄 Repetir Lições
              </button>
              <button type="button" class="btn-primario btn-dojo-action" onclick="App.navegar('templi')">
                🏛️ Voltar aos Templos
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }
};


// Exposição global segura para navegadores e testes
if (typeof window !== 'undefined') window.Imitazione = Imitazione;
if (typeof globalThis !== 'undefined') globalThis.Imitazione = Imitazione;
if (typeof module !== 'undefined' && module.exports) module.exports = Imitazione;
