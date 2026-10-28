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
    this._aplicarFiltro();
  },

  _aplicarFiltro() {
    let todas = this.dados?.imitazioni || [];
    if (this._filtroOrigem === 'custom') todas = todas.filter(f => f._custom || f.custom);
    if (this._filtroOrigem === 'nativo') todas = todas.filter(f => !f._custom && !f.custom);
    this._listaAtual = this._filtroNivel
      ? todas.filter(f => f.nivel === this._filtroNivel)
      : todas;
    this.itemAtual = 0;
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
      bar.className = 'dojo-filtro-bar';
      c.parentElement?.insertBefore(bar, c);
    }

    const pillOrigem = (v, label, count) => `
      <button class="dojo-level-pill ${_o === v ? 'ativo' : ''}"
              onclick="Imitazione._filtroOrigem='${v}';Imitazione._aplicarFiltro()">
        ${label} (${count})
      </button>
    `;

    const pillNivel = (lvl) => `
      <button class="dojo-level-pill ${_n === lvl ? 'ativo' : ''}"
              onclick="Imitazione._filtroNivel='${_n === lvl ? '' : lvl}';Imitazione._aplicarFiltro()">
        ${lvl} (${counts[lvl] || 0})
      </button>
    `;

    bar.innerHTML = `
      <div class="dojo-level-pills">
        <button class="btn-ia-add" onclick="IAImport.abrir('imitazione')" style="margin-right:0.3rem">🤖 + IA</button>
        ${pillOrigem('', 'Todas', todasRaw.length)}
        ${nC ? pillOrigem('custom', '🤖 Adicionadas', nC) : ''}
        ${nN ? pillOrigem('nativo', '📚 Nativas', nN) : ''}
      </div>
      <div class="dojo-level-pills">
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
          const resContainer = document.getElementById('imitazione-resultado');
          if (resContainer) {
            resContainer.style.display = 'block';
            resContainer.innerHTML = `
              <div style="font-size:1.3rem;font-weight:700;color:#2E86C1;margin-bottom:0.6rem;font-family:'Cinzel',serif">
                🎙️ Áudio Gravado com Sucesso!
              </div>
              <div style="font-size:0.95rem;color:var(--cor-inchiostro);margin-bottom:1rem">
                O reconhecimento automático requer Google Chrome (Android) ou Safari (iOS). Sua gravação está pronta para você se autoavaliar!
              </div>
              <div class="dojo-replay-toolbar">
                <button class="btn-dojo-replay" onclick="Imitazione.tocarMinhaGravacao()">
                  <span>🎧</span> Ouvir Minha Gravação
                </button>
                <button class="btn-dojo-replay" onclick="Imitazione.tocarModelo(1.0)">
                  <span>🔊</span> Ouvir Modelo Nativo
                </button>
              </div>
            `;
          }
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

  // Avaliação analítica palavra por palavra
  avaliarPronuncia(textoOuvido) {
    const lista = this._listaAtual || this.dados.imitazioni;
    const item = lista[this.itemAtual];
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

    const resContainer = document.getElementById('imitazione-resultado');
    if (!resContainer) return;
    resContainer.style.display = 'block';

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

    resContainer.innerHTML = `
      <div style="font-size:2rem;font-weight:700;color:${cor};margin-bottom:0.4rem;font-family:'Cinzel',serif">
        ${titulo}
      </div>
      <div style="font-size:1.1rem;color:var(--cor-inchiostro);margin-bottom:1rem">
        Precisão de Dicção: <strong>${precisao}%</strong>
        ${xpGanho > 0 ? ` <span style="background:rgba(212,168,67,0.2);color:#9B2335;padding:0.15rem 0.6rem;border-radius:999px;font-weight:800;font-size:0.82rem;margin-left:0.5rem">+${xpGanho} XP</span>` : ''}
      </div>

      <div style="font-size:0.85rem;color:var(--cor-pietra);margin-bottom:0.5rem">
        Diagnóstico Palavra por Palavra (toque em qualquer palavra para ouvir o som isolado):
      </div>

      <div class="dojo-words-breakdown">
        ${tokensDiagnostico.map(t => `
          <button class="dojo-word-pill ${t.status}"
                  onclick="App.pronunciar('${t.palavra.replace(/'/g, "\\'")}')"
                  title="Ouvir pronúncia de '${t.palavra}'">
            <span>${t.status === 'correta' ? '✓' : (t.status === 'proxima' ? '≈' : '•')}</span>
            <span>${t.palavra}</span>
          </button>
        `).join('')}
      </div>

      <div style="font-size:0.9rem;color:#666;font-style:italic;margin-top:0.6rem">
        Ouvimos: "${textoOuvido}"
      </div>

      <!-- Barra de comparação de áudio -->
      <div class="dojo-replay-toolbar">
        ${this._userAudioUrl ? `
          <button class="btn-dojo-replay" onclick="Imitazione.tocarMinhaGravacao()">
            <span>🎧</span> Ouvir Minha Gravação
          </button>
        ` : ''}
        <button class="btn-dojo-replay" onclick="Imitazione.tocarModelo(1.0)">
          <span>🔊</span> Ouvir Modelo Nativo
        </button>
      </div>

      <div style="display:flex;gap:0.8rem;justify-content:center;margin-top:1.25rem;flex-wrap:wrap">
        <button class="btn-secondario" onclick="Imitazione.mostrarDesafio()">
          🔄 Tentar Novamente
        </button>
        <button class="btn-primario" onclick="Imitazione.avancar()">
          ➡️ Próxima Frase
        </button>
      </div>
    `;

    resContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  },

  voltar() {
    if (this.itemAtual > 0) {
      this.itemAtual--;
      this.mostrarDesafio();
    }
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

    const frase = item.frase_italiano || item.frase;
    const traducao = item.frase_portugues || item.traducao;
    const contexto = item.contexto || 'Frase di uso comune in conversazione.';
    const dicaFonetica = item.dica_fonetica || 'Pronuncie com abertura vocal clara e ritmo cadenciado.';

    c.innerHTML = `
      <div class="imitazione-dojo">
        <div class="dojo-progress-hud">
          <span>Frase <strong>${this.itemAtual + 1}</strong> de ${lista.length}</span>
          <span style="background:rgba(155,35,53,0.1);color:#9B2335;padding:0.15rem 0.6rem;border-radius:999px;font-weight:700">${item.nivel || 'A1'}</span>
        </div>

        <div class="dojo-hero-card" style="padding:1.25rem 1.5rem">
          <div class="dojo-hero-badge">
            <span>🎙️ Studio di Pronuncia</span>
            ${item._custom ? ` · <button onclick="IAImport.excluir('imitazione','${item.id}')" style="background:none;border:none;color:#C0392B;cursor:pointer;font-size:0.75rem;font-weight:700">🗑️ Excluir</button>` : ''}
          </div>

          <div class="dojo-hero-frase" style="margin:0.4rem 0 0.25rem">"${frase}"</div>
          <div class="dojo-hero-traducao" style="margin-bottom:0.85rem">"${traducao}"</div>

          <!-- Estúdio de Áudio do Modelo Nativo (acima da dobra) -->
          <div class="dojo-audio-station" style="margin-bottom:0.85rem">
            <button class="btn-dojo-audio normal" onclick="Imitazione.tocarModelo(1.0)">
              <span>🔊</span> Ouvir Modelo (1.0x)
            </button>
            <button class="btn-dojo-audio slow" onclick="Imitazione.tocarModelo(0.75)">
              <span>🐢</span> Didático Lento (0.75x)
            </button>
            <div class="dojo-soundwave" id="dojo-wave">
              <span></span><span></span><span></span><span></span><span></span>
            </div>
          </div>

          <!-- Estúdio de Gravação do Aluno (compactado e centralizado) -->
          <div class="dojo-mic-studio" style="padding:1rem 1.25rem;margin-bottom:0.85rem">
            <div class="dojo-mic-btn-wrapper">
              <button id="dojo-btn-mic" class="dojo-mic-btn" onclick="Imitazione.toggleGravacao()" title="Clique para falar">
                🎙️
              </button>
            </div>
            <div id="dojo-mic-status" class="dojo-mic-status">
              Clique no microfone e fale a frase acima
            </div>
          </div>

          <!-- Accordions compactos para Contexto e Dica Fonética -->
          <div class="dojo-accordions-row">
            <details class="dojo-accordion">
              <summary>🏛️ Contexto & Origem Cultural</summary>
              <div class="dojo-accordion-content dojo-info-box contexto">${contexto}</div>
            </details>

            <details class="dojo-accordion">
              <summary>🎵 Dica de Ritmo & Entonação</summary>
              <div class="dojo-accordion-content dojo-info-box fonetica">${dicaFonetica}</div>
            </details>
          </div>

          <!-- Painel Dinâmico de Diagnóstico e Feedback -->
          <div id="imitazione-resultado" class="dojo-feedback-panel" style="display:none;margin-top:1.1rem">
          </div>
        </div>

        <!-- Barra inferior fixa de navegação entre frases -->
        <div class="dojo-sticky-nav">
          <button type="button" class="btn-secondario" onclick="Imitazione.voltar()" ${this.itemAtual <= 0 ? 'disabled style="opacity:0.45;cursor:not-allowed"' : ''}>
            ← Frase Anterior
          </button>
          <span style="font-size:0.82rem;font-weight:700;color:var(--cor-inchiostro-claro,#5A4535)">
            ${this.itemAtual + 1} / ${lista.length}
          </span>
          <button type="button" class="btn-primario" onclick="Imitazione.avancar()">
            Próxima Frase →
          </button>
        </div>
      </div>
    `;
  },

  mostrarFinal() {
    const c = document.getElementById('imitazione-container');
    if (!c) return;
    const lista = this._listaAtual || this.dados?.imitazioni || [];
    c.innerHTML = `
      <div class="imitazione-dojo">
        <div class="dojo-hero-card" style="padding:3.5rem 1.5rem">
          <div style="font-size:4.5rem;margin-bottom:1rem">🏆</div>
          <h3 style="font-family:'Cinzel',serif;color:#9B2335;font-size:2.2rem;margin-bottom:0.8rem">Bravissimo!</h3>
          <p style="font-size:1.15rem;color:var(--cor-inchiostro);margin-bottom:1.5rem;max-width:500px;margin-left:auto;margin-right:auto">
            Você completou com sucesso todas as ${lista.length} frases do treinamento auditivo e fonético!
          </p>
          <div style="display:flex;gap:0.75rem;justify-content:center;flex-wrap:wrap">
            <button class="btn-secondario" onclick="Imitazione._aplicarFiltro()">
              🔄 Repetir Lições
            </button>
            <button class="btn-primario" onclick="App.navegar('templi')">
              🏛️ Voltar aos Templos
            </button>
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
