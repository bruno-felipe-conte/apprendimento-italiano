const Imitazione = {
  dados: null,
  itemAtual: 0,
  recognition: null,
  isRecording: false,

  async carregar() {
    if (this.dados) return;
    try {
      const r = await fetch('data/imitazione.json');
      this.dados = await r.json();
    } catch (e) {
      console.error('Erro ao carregar imitazione.json', e);
    }
  },

  async renderizar() {
    await this.carregar();
    this.itemAtual = 0;
    this.mostrarDesafio();
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
      document.getElementById('mic-status').innerText = 'Ouvindo... Fale agora!';
    };

    this.recognition.onresult = (event) => {
      const speechResult = event.results[0][0].transcript;
      this.avaliarPronuncia(speechResult);
    };

    this.recognition.onerror = (event) => {
      console.error('Erro de reconhecimento: ', event.error);
      this.isRecording = false;
      document.getElementById('btn-mic').classList.remove('recording');
      document.getElementById('mic-status').innerText = 'Erro ao ouvir. Tente novamente.';
    };

    this.recognition.onend = () => {
      this.isRecording = false;
      const btnMic = document.getElementById('btn-mic');
      if (btnMic) btnMic.classList.remove('recording');
      const st = document.getElementById('mic-status');
      if (st && st.innerText === 'Ouvindo... Fale agora!') {
        st.innerText = 'Processando...';
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
    const item = this.dados.imitazione[this.itemAtual];
    const esperado = this.normalizeText(item.frase);
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
        <p>Você disse: <i>"${textoOuvido}"</i></p>
        <div style="margin-top:1rem;color:#D4A843;font-weight:700">+${item.xp_recompensa} XP</div>
        <button class="btn-primario" style="margin-top:1rem" onclick="Imitazione.avancar()">Próxima Frase</button>
      `;
      Progressao.ganhar(item.xp_recompensa);
    } else if (score >= 0.5) {
      resContainer.innerHTML = `
        <div style="color:#E67E22;font-size:1.5rem;margin-bottom:0.5rem">Quasi! 👍</div>
        <p>Ouvimos: <i>"${textoOuvido}"</i></p>
        <p style="font-size:0.85rem;margin-top:0.5rem">Tente pronunciar mais claramente.</p>
        <button class="btn-secondario" style="margin-top:1rem" onclick="Imitazione.mostrarDesafio()">Tentar Novamente</button>
      `;
    } else {
      resContainer.innerHTML = `
        <div style="color:#C0392B;font-size:1.5rem;margin-bottom:0.5rem">Riprova! 🔄</div>
        <p>Ouvimos: <i>"${textoOuvido}"</i></p>
        <p style="font-size:0.85rem;margin-top:0.5rem">Ouça o exemplo e tente de novo.</p>
        <button class="btn-secondario" style="margin-top:1rem" onclick="Imitazione.mostrarDesafio()">Tentar Novamente</button>
      `;
    }
  },

  avancar() {
    this.itemAtual++;
    if (this.itemAtual >= this.dados.imitazione.length) {
      this.mostrarFinal();
    } else {
      this.mostrarDesafio();
    }
  },

  mostrarDesafio() {
    const c = document.getElementById('imitazione-container');
    const item = this.dados.imitazione[this.itemAtual];

    c.innerHTML = `
      <div style="text-align:center;margin-bottom:1.5rem">
        <div style="font-size:0.8rem;color:#888;text-transform:uppercase;margin-bottom:0.5rem">Frase ${this.itemAtual + 1} de ${this.dados.imitazione.length}</div>
        <h3 style="font-family:'Cinzel',serif;font-size:1.8rem;color:#9B2335;margin-bottom:0.5rem">"${item.frase}"</h3>
        <p style="font-size:1.1rem;color:#555;margin-bottom:1rem"><i>${item.traducao}</i></p>
        
        <div style="background:white;padding:1rem;border-radius:12px;display:inline-block;box-shadow:0 2px 10px rgba(0,0,0,0.05);margin-bottom:1.5rem">
          <div style="font-size:0.75rem;color:#888;font-weight:700;text-transform:uppercase;margin-bottom:0.3rem">Dica Fonética</div>
          <div style="font-family:monospace;color:#2C2C2C;font-size:1rem">${item.dica_fonetica}</div>
          <div style="font-family:monospace;color:#777;font-size:0.8rem;margin-top:0.3rem">${item.audio_ipa}</div>
        </div>
        <br>
        <button class="btn-audio" onclick="App.pronunciar('${item.frase.replace(/'/g, "\\'")}')" style="font-size:1.1rem;padding:0.6rem 1.2rem">🔊 Ouvir Exemplo</button>
      </div>

      <div style="text-align:center;background:rgba(255,255,255,0.5);padding:2rem;border-radius:16px">
        <button id="btn-mic" class="mic-button" onclick="Imitazione.toggleGravacao()">🎙️</button>
        <div id="mic-status" style="margin-top:1rem;font-weight:700;color:#666">Clique no microfone para falar</div>
      </div>

      <div id="imitazione-resultado" style="display:none;margin-top:1.5rem;text-align:center;background:white;padding:1.5rem;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,0.1)">
      </div>
    `;
  },

  mostrarFinal() {
    const c = document.getElementById('imitazione-container');
    c.innerHTML = `
      <div style="text-align:center;padding:3rem 1rem">
        <div style="font-size:4rem;margin-bottom:1rem">🏆</div>
        <h3 style="font-family:'Cinzel',serif;color:#9B2335;font-size:1.8rem;margin-bottom:1rem">Excelente!</h3>
        <p style="font-size:1.1rem;color:#555;margin-bottom:2rem">Você completou todas as frases de imitação.</p>
        <button class="btn-primario" onclick="App.navegar('templi')">Voltar ao Início</button>
      </div>
    `;
  }
};
