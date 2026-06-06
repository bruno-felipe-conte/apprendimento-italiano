const Imitazione = {
  dados: null,
  itemAtual: 0,
  recognition: null,
  isRecording: false,
  _filtroNivel: '',
  _listaAtual: null, // frases filtradas

  async carregar() {
    if (this.dados) return;
    try {
      const r = await fetch('data/imitazioni.json');
      this.dados = await r.json();
    } catch (e) {
      console.error('Erro ao carregar imitazioni.json', e);
    }
  },

  async renderizar() {
    await this.carregar();
    this._aplicarFiltro();
  },

  _aplicarFiltro() {
    const todas = this.dados?.imitazioni || [];
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
    const todas = this.dados?.imitazioni || [];
    const niveis = ['A1','A2','B1','B2','C1'];
    const counts = {};
    todas.forEach(f => { counts[f.nivel] = (counts[f.nivel]||0)+1; });

    const bar = document.getElementById('imit-filtro-bar') || (() => {
      const d = document.createElement('div');
      d.id = 'imit-filtro-bar';
      c.parentElement?.insertBefore(d, c);
      return d;
    })();

    bar.innerHTML = `<div style="display:flex;gap:0.3rem;flex-wrap:wrap;margin-bottom:0.8rem;padding:0 0.2rem">
      <button onclick="Imitazione._filtroNivel='';Imitazione._aplicarFiltro()"
        style="padding:0.25rem 0.7rem;border-radius:999px;border:1.5px solid ${!this._filtroNivel?'#9B2335':'#ddd'};background:${!this._filtroNivel?'#9B2335':'transparent'};color:${!this._filtroNivel?'#fff':'inherit'};cursor:pointer;font-size:0.78rem;font-weight:600">
        Tutte (${todas.length})</button>
      ${niveis.map(n => `<button onclick="Imitazione._filtroNivel='${n}';Imitazione._aplicarFiltro()"
        style="padding:0.25rem 0.7rem;border-radius:999px;border:1.5px solid ${this._filtroNivel===n?'#9B2335':'#ddd'};background:${this._filtroNivel===n?'#9B2335':'transparent'};color:${this._filtroNivel===n?'#fff':'inherit'};cursor:pointer;font-size:0.78rem;font-weight:600">
        ${n} (${counts[n]||0})</button>`).join('')}
    </div>`;
  },

  initSpeechRecognition() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert("Seu navegador não suporta reconhecimento de voz (use Chrome).");
      return false;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    this.recognition = new SpeechRecognition();
    this.recognition.lang = 'it-IT';
    this.recognition.interimResults = false;
    this.recognition.maxAlternatives = 1;

    this.recognition.onstart = () => {
      this.isRecording = true;
      document.getElementById('btn-mic').classList.add('recording');
      document.getElementById('mic-status').innerText = I18n.idioma === 'it' ? 'In ascolto... Parla adesso!' : 'Ouvindo... Fale agora!';
    };

    this.recognition.onresult = (event) => {
      const speechResult = event.results[0][0].transcript;
      this.avaliarPronuncia(speechResult);
    };

    this.recognition.onerror = (event) => {
      console.error('Erro de reconhecimento: ', event.error);
      this.isRecording = false;
      document.getElementById('btn-mic').classList.remove('recording');
      document.getElementById('mic-status').innerText = I18n.t('imit_erro_ouvir');
    };

    this.recognition.onend = () => {
      this.isRecording = false;
      const btnMic = document.getElementById('btn-mic');
      if (btnMic) btnMic.classList.remove('recording');
      const st = document.getElementById('mic-status');
      const ouvindo = I18n.idioma === 'it' ? 'In ascolto... Parla adesso!' : 'Ouvindo... Fale agora!';
      if (st && st.innerText === ouvindo) {
        st.innerText = I18n.idioma === 'it' ? 'Elaborazione...' : 'Processando...';
      }
    };
    
    return true;
  },

  toggleGravacao() {
    if (!this.recognition) {
      if (!this.initSpeechRecognition()) return;
    }

    if (this.isRecording) {
      this.recognition.stop();
    } else {
      this.recognition.start();
    }
  },

  normalizeText(text) {
    return text.toLowerCase().replace(/[.,!?;:]/g, '').trim();
  },

  avaliarPronuncia(textoOuvido) {
    const item = this.dados.imitazioni[this.itemAtual];
    const esperado = this.normalizeText(item.frase_italiano || item.frase);
    const recebido = this.normalizeText(textoOuvido);

    // Simple Jaro-Winkler or Levenshtein would be better, but we do simple string matching or token match
    const expectedTokens = esperado.split(' ');
    const receivedTokens = recebido.split(' ');
    
    let matches = 0;
    expectedTokens.forEach(token => {
      if (receivedTokens.includes(token)) matches++;
    });
    
    const score = matches / expectedTokens.length;
    
    const resContainer = document.getElementById('imitazione-resultado');
    resContainer.style.display = 'block';

    if (score >= 0.8) {
      resContainer.innerHTML = `
        <div style="color:#27AE60;font-size:1.5rem;margin-bottom:0.5rem">Perfetto! 🌟</div>
        <p>${I18n.t('imit_voce_disse')} <i>"${textoOuvido}"</i></p>
        <div style="margin-top:1rem;color:#D4A843;font-weight:700">+${item.xp_recompensa} XP</div>
        <button class="btn-primario" style="margin-top:1rem" onclick="Imitazione.avancar()">${I18n.t('imit_proxima_frase')}</button>
      `;
      Progressao.ganhar(item.xp_recompensa);
    } else if (score >= 0.5) {
      resContainer.innerHTML = `
        <div style="color:#E67E22;font-size:1.5rem;margin-bottom:0.5rem">Quasi! 👍</div>
        <p>${I18n.t('imit_ouvimos')} <i>"${textoOuvido}"</i></p>
        <p style="font-size:0.85rem;margin-top:0.5rem">${I18n.t('imit_pronunciar_melhor')}</p>
        <button class="btn-secondario" style="margin-top:1rem" onclick="Imitazione.mostrarDesafio()">${I18n.t('imit_tentar_novamente')}</button>
      `;
    } else {
      resContainer.innerHTML = `
        <div style="color:#C0392B;font-size:1.5rem;margin-bottom:0.5rem">Riprova! 🔄</div>
        <p>${I18n.t('imit_ouvimos')} <i>"${textoOuvido}"</i></p>
        <p style="font-size:0.85rem;margin-top:0.5rem">${I18n.t('imit_ouvir_exemplo')}</p>
        <button class="btn-secondario" style="margin-top:1rem" onclick="Imitazione.mostrarDesafio()">${I18n.t('imit_tentar_novamente')}</button>
      `;
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
    const lista = this._listaAtual || this.dados?.imitazioni || [];
    const item = lista[this.itemAtual];
    if (!item) { this.mostrarFinal(); return; }

    const it = I18n.idioma === 'it';
    c.innerHTML = `
      <div style="text-align:center;margin-bottom:1.5rem">
        <div style="font-size:0.8rem;color:var(--cor-pietra);text-transform:uppercase;margin-bottom:0.5rem">
          ${it ? 'Frase' : 'Frase'} ${this.itemAtual + 1} ${it ? 'di' : 'de'} ${lista.length}
          <span style="margin-left:0.5rem;background:rgba(155,35,53,0.1);border-radius:4px;padding:0.1rem 0.4rem">${item.nivel}</span>
        </div>
        <h3 style="font-family:'Cinzel',serif;font-size:1.8rem;color:var(--cor-veneziano-escuro);margin-bottom:0.5rem">"${item.frase_italiano || item.frase}"</h3>
        <p style="font-size:1.1rem;color:var(--cor-inchiostro);margin-bottom:1rem"><i>${item.frase_portugues || item.traducao}</i></p>
        
        <div style="background:var(--cor-marmore);padding:1rem;border-radius:12px;display:inline-block;box-shadow:0 2px 10px rgba(0,0,0,0.05);margin-bottom:1.5rem">
          <div style="font-size:0.75rem;color:var(--cor-pietra);font-weight:700;text-transform:uppercase;margin-bottom:0.3rem">Dica Fonética</div>
          <div style="font-family:monospace;color:var(--cor-inchiostro);font-size:1rem">${item.dica_fonetica || item.contexto}</div>
          <div style="font-family:monospace;color:var(--cor-pietra);font-size:0.8rem;margin-top:0.3rem">${item.audio_ipa}</div>
        </div>
        <br>
        <button class="btn-audio" onclick="App.pronunciar('${(item.frase_italiano || item.frase).replace(/'/g, "\\'")}')" style="font-size:1.1rem;padding:0.6rem 1.2rem">${I18n.t('imit_btn_ouvir_exemplo')}</button>
      </div>

      <div style="text-align:center;background:var(--cor-marmore-escuro);padding:2rem;border-radius:16px">
        <button id="btn-mic" class="mic-button" onclick="Imitazione.toggleGravacao()">🎙️</button>
        <div id="mic-status" style="margin-top:1rem;font-weight:700;color:var(--cor-inchiostro-claro)">${I18n.idioma === 'it' ? 'Clicca sul microfono per parlare' : 'Clique no microfone para falar'}</div>
      </div>

      <div id="imitazione-resultado" style="display:none;margin-top:1.5rem;text-align:center;background:var(--cor-marmore);padding:1.5rem;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,0.1)">
      </div>
    `;
  },

  mostrarFinal() {
    const c = document.getElementById('imitazione-container');
    const it = I18n.idioma === 'it';
    const lista = this._listaAtual || this.dados?.imitazioni || [];
    c.innerHTML = `
      <div style="text-align:center;padding:3rem 1rem">
        <div style="font-size:4rem;margin-bottom:1rem">🏆</div>
        <h3 style="font-family:'Cinzel',serif;color:#9B2335;font-size:1.8rem;margin-bottom:1rem">${it ? 'Eccellente!' : 'Excelente!'}</h3>
        <p style="font-size:1.1rem;color:#555;margin-bottom:1rem">
          ${it ? `Hai completato tutte le ${lista.length} frasi!` : `Você completou todas as ${lista.length} frases de imitação!`}
        </p>
        <div style="display:flex;gap:0.5rem;justify-content:center;flex-wrap:wrap">
          <button class="btn-secondario" onclick="Imitazione._aplicarFiltro()">${it ? '🔄 Ricominciare' : '🔄 Repetir'}</button>
          <button class="btn-primario" onclick="App.navegar('templi')">${it ? 'Torna all\'Inizio' : 'Voltar ao Início'}</button>
        </div>
      </div>
    `;
  }
};
