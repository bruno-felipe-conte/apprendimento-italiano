const Canzoni = {
  dados: null,
  musicaAtual: null,
  trechoAtual: 0,
  acertos: 0,
  player: null,

  async carregar() {
    if (this.dados) return;
    try {
      const r = await fetch('data/canzoni.json');
      this.dados = await r.json();
    } catch (e) {
      console.error('Erro ao carregar canzoni.json', e);
    }
  },

  async renderizarSeletor() {
    await this.carregar();
    const c = document.getElementById('canzoni-container');
    if (!c || !this.dados) return;

    let html = '<div class="dialogo-grid">';
    for (const m of this.dados.canzoni) {
      html += `
        <div class="dialogo-card" onclick="Canzoni.abrirMusica('${m.id}')">
          <div class="dialogo-icone">${m.icone}</div>
          <div class="dialogo-titulo">${m.titulo}</div>
          <div style="font-size:0.85rem;color:#666;margin-bottom:0.4rem">${m.artista}</div>
          <div class="dialogo-nivel">${m.nivel}</div>
          <div style="font-size:0.75rem;color:#888;margin-top:0.3rem">🎁 ${m.xp_recompensa} XP</div>
        </div>
      `;
    }
    html += '</div>';
    c.innerHTML = html;
  },

  abrirMusica(id) {
    this.musicaAtual = this.dados.canzoni.find(m => m.id === id);
    if (!this.musicaAtual) return;
    this.trechoAtual = 0;
    this.acertos = 0;
    this.renderizarMusica();
    this.iniciarYouTubePlayer();
  },

  iniciarYouTubePlayer() {
    // We load YouTube iframe API dynamically if not present
    if (!window.YT) {
      const tag = document.createElement('script');
      tag.src = "https://www.youtube.com/iframe_api";
      const firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
      window.onYouTubeIframeAPIReady = () => this.criarPlayer();
    } else {
      this.criarPlayer();
    }
  },

  criarPlayer() {
    if (this.player) {
      this.player.destroy();
    }
    const trecho = this.musicaAtual.trechos[this.trechoAtual];
    this.player = new YT.Player('youtube-player', {
      height: '0',
      width: '0',
      videoId: this.musicaAtual.youtube_id,
      playerVars: {
        'autoplay': 0,
        'controls': 0,
        'start': trecho.tempo_inicio,
        'end': trecho.tempo_fim
      },
      events: {
        'onReady': (event) => {
          // Ready to play
        }
      }
    });
  },

  tocarTrechoAtual() {
    if (this.player && this.player.playVideo) {
      const trecho = this.musicaAtual.trechos[this.trechoAtual];
      this.player.seekTo(trecho.tempo_inicio);
      this.player.playVideo();
      // Optional: Stop when reaches end, YouTube iframe handles 'end' param but sometimes it's flaky
      setTimeout(() => {
        if (this.player && this.player.pauseVideo) this.player.pauseVideo();
      }, (trecho.tempo_fim - trecho.tempo_inicio) * 1000);
    }
  },

  renderizarMusica() {
    const c = document.getElementById('canzoni-container');
    const m = this.musicaAtual;
    const trecho = m.trechos[this.trechoAtual];

    // Build the lyrics text with inputs for gaps
    let letraHtml = trecho.letra.replace(/\n/g, '<br>');
    trecho.gaps.forEach((gap, index) => {
      // Replace "[gap]" with an input or placeholder
      letraHtml = letraHtml.replace(`[${gap}]`, `<span class="canzone-gap" id="gap-${index}">___</span>`);
    });

    let html = `
      <div style="margin-bottom:1rem;display:flex;align-items:center;justify-content:space-between">
        <button class="btn-secondario" onclick="Canzoni.pararMusica();Canzoni.renderizarSeletor()" style="padding:0.4rem 0.8rem">‹ Voltar</button>
      </div>
      <div style="text-align:center;margin-bottom:1rem">
        <div style="font-size:2rem">${m.icone}</div>
        <h3 style="font-family:'Cinzel',serif;color:#9B2335;margin:0.2rem 0">${m.titulo}</h3>
        <p style="font-size:0.85rem;color:#888;">${m.artista}</p>
      </div>

      <div id="youtube-player" style="display:none;"></div>

      <div class="dialogo-conversa">
        <div style="text-align:center;margin-bottom:1.5rem">
          <button class="btn-primario" onclick="Canzoni.tocarTrechoAtual()" style="font-size:1.2rem;padding:0.5rem 1.5rem">▶️ Ouvir Trecho</button>
        </div>
        
        <div class="canzone-letra">
          ${letraHtml}
        </div>

        <div style="margin-top:1.5rem">
          <div class="dialogo-pratica-frase">Qual palavra falta?</div>
          <div class="dialogo-opcoes">
    `;

    trecho.opcoes.forEach(opcao => {
      html += `<button class="dialogo-opcao" onclick="Canzoni.checarResposta('${opcao}', this, '${trecho.gaps[0]}')">${opcao}</button>`;
    });

    html += `
          </div>
        </div>
      </div>
    `;

    c.innerHTML = html;
  },

  pararMusica() {
    if (this.player && this.player.pauseVideo) {
      this.player.pauseVideo();
    }
  },

  checarResposta(opcao, btn, correto) {
    const isCorreto = opcao === correto;
    
    // Desabilita botões
    const container = btn.parentElement;
    container.querySelectorAll('button').forEach(b => {
      b.disabled = true;
      b.style.cursor = 'default';
    });

    // Fill the gap
    const gapEl = document.getElementById('gap-0'); // supporting single gap for now

    if (isCorreto) {
      this.acertos++;
      btn.classList.add('correta');
      if (gapEl) {
        gapEl.textContent = correto;
        gapEl.classList.add('correta');
      }
      setTimeout(() => {
        this.avancarTrecho();
      }, 1500);
    } else {
      btn.classList.add('errada');
      if (gapEl) {
        gapEl.textContent = opcao;
        gapEl.classList.add('errada');
      }
      
      // Highlight correct answer
      container.querySelectorAll('button').forEach(b => {
        if (b.textContent === correto) b.classList.add('correta');
      });

      setTimeout(() => {
        this.avancarTrecho();
      }, 2500);
    }
  },

  avancarTrecho() {
    this.trechoAtual++;
    if (this.trechoAtual >= this.musicaAtual.trechos.length) {
      this.mostrarResultado();
    } else {
      this.renderizarMusica();
      this.player.loadVideoById({
        videoId: this.musicaAtual.youtube_id,
        startSeconds: this.musicaAtual.trechos[this.trechoAtual].tempo_inicio,
        endSeconds: this.musicaAtual.trechos[this.trechoAtual].tempo_fim
      });
      this.player.pauseVideo(); // pause wait for user
    }
  },

  mostrarResultado() {
    const m = this.musicaAtual;
    const total = m.trechos.length;
    const pct = Math.round((this.acertos / total) * 100);
    
    let ganhouXp = false;
    if (pct >= 50) {
      Progressao.ganhar(m.xp_recompensa);
      ganhouXp = true;
    }
    
    const c = document.getElementById('canzoni-container');
    c.innerHTML = `
      <div style="text-align:center;padding:2rem 1rem">
        <div style="font-size:3rem">${pct >= 80 ? '🌟' : (pct >= 50 ? '👍' : '🔄')}</div>
        <h3 style="font-family:'Cinzel',serif;color:#9B2335;font-size:1.5rem;margin:1rem 0">Música Concluída</h3>
        <div style="font-size:1.1rem;margin-bottom:1rem">Acertos: <strong>${this.acertos} / ${total}</strong></div>
        ${ganhouXp ? `<div style="color:#D4A843;font-weight:700;font-size:1.2rem;margin-bottom:1.5rem">+${m.xp_recompensa} XP</div>` : ''}
        
        <div style="display:flex;gap:1rem;justify-content:center">
          <button class="btn-secondario" onclick="Canzoni.renderizarSeletor()">‹ Voltar</button>
          <button class="btn-primario" onclick="Canzoni.abrirMusica('${m.id}')">Tentar Novamente 🔄</button>
        </div>
      </div>
    `;
  }
};
