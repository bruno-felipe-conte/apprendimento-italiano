const Canzoni = {
  dados: null,
  canzonAtual: null,
  estrofeAtual: 0,
  acertos: 0,
  
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
    for (const can of this.dados.canzoni) {
      html += `<div class="dialogo-card" onclick="Canzoni.abrirCanzone('${can.id}')">
        <div class="dialogo-icone">${can.icone}</div>
        <div class="dialogo-titulo">${can.titulo}</div>
        <div style="font-size:0.75rem;color:#888;margin:0.2rem 0">${can.artista}</div>
        <div class="dialogo-nivel">${can.nivel}</div>
      </div>`;
    }
    html += '</div>';
    c.innerHTML = html;
  },
  
  async abrirCanzone(id) {
    await this.carregar();
    this.canzonAtual = this.dados.canzoni.find(c => c.id === id);
    this.estrofeAtual = 0;
    this.acertos = 0;
    this.renderizarEstrofe();
  },
  
  renderizarEstrofe() {
    const c = document.getElementById('canzoni-container');
    if (!c || !this.canzonAtual) return;
    const can = this.canzonAtual;
    const est = can.estrofes[this.estrofeAtual];
    const total = can.estrofes.length;
    const pct = Math.round(this.estrofeAtual / total * 100);
    
    c.innerHTML = `
      <div class="gram-lesson-nav">
        <button class="gram-btn-back" onclick="Canzoni.renderizarSeletor()">‹ Canzoni</button>
        <span style="font-size:0.85rem;color:#888">${this.estrofeAtual+1}/${total}</span>
      </div>
      <div style="text-align:center;padding:1rem 0 0.5rem">
        <div style="font-size:1.5rem">${can.icone}</div>
        <div style="font-family:'Cinzel',serif;font-weight:700;color:#9B2335">${can.titulo}</div>
        <div style="font-size:0.8rem;color:#888">${can.artista}</div>
      </div>
      <div class="gram-ex-progress-bar" style="margin:0.5rem 1rem"><div class="gram-ex-progress-fill" style="width:${pct}%"></div></div>
      <div class="gram-card" style="margin:1rem">
        <div style="font-size:1rem;line-height:1.8;padding:1rem;text-align:center;font-style:italic;color:#2C2C2C">
          ${est.texto_lacuna.replace('___', '<input id="canzone-input" type="text" autocomplete="off" autocorrect="off" spellcheck="false" style="border:none;border-bottom:2px solid #9B2335;font-size:1rem;font-style:italic;width:100px;text-align:center;outline:none;background:transparent" placeholder="___" onkeydown="if(event.key===\'Enter\')Canzoni.verificar()">')}
        </div>
        <div style="text-align:center;font-size:0.82rem;color:#888;font-style:italic;padding:0 1rem 0.5rem">${est.traducao}</div>
        <div style="text-align:center;font-size:0.78rem;color:#D4A843;padding-bottom:1rem">💡 Dica: ${est.dica}</div>
        <div id="canzone-feedback"></div>
        <div style="display:flex;justify-content:center;gap:0.5rem;padding:0.5rem">
          <button class="btn-primario" onclick="Canzoni.verificar()">✔ Verificar</button>
          <button class="btn-secondario" onclick="App.pronunciar('${est.texto_completo.replace(/'/g,"\\'")}')">🔊 Ouvir</button>
        </div>
      </div>`;
    setTimeout(() => document.getElementById('canzone-input')?.focus(), 100);
  },
  
  verificar() {
    const est = this.canzonAtual.estrofes[this.estrofeAtual];
    const input = document.getElementById('canzone-input');
    const fb = document.getElementById('canzone-feedback');
    if (!input || !fb) return;
    const digitado = input.value.trim().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
    const correto = est.palavra_oculta.trim().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
    const acertou = digitado === correto;
    if (acertou) {
      this.acertos++;
      if (typeof App !== 'undefined' && App.ganharXP) App.ganharXP(5);
      fb.innerHTML = `<div style="color:#27AE60;text-align:center;padding:0.5rem;font-weight:700">✅ Corretto! "${est.palavra_oculta}"</div>`;
    } else {
      fb.innerHTML = `<div style="color:#C0392B;text-align:center;padding:0.5rem">❌ A palavra era: <strong>${est.palavra_oculta}</strong></div>`;
    }
    input.disabled = true;
    input.value = est.palavra_oculta;
    input.style.color = acertou ? '#27AE60' : '#C0392B';
    setTimeout(() => {
      this.estrofeAtual++;
      if (this.estrofeAtual >= this.canzonAtual.estrofes.length) this.mostrarResultado();
      else this.renderizarEstrofe();
    }, 1500);
  },
  
  mostrarResultado() {
    const can = this.canzonAtual;
    const total = can.estrofes.length;
    const pct = Math.round(this.acertos / total * 100);
    if (typeof Progressao !== 'undefined' && Progressao.ganhar) Progressao.ganhar(can.xp_recompensa);
    const c = document.getElementById('canzoni-container');
    c.innerHTML = `<div style="text-align:center;padding:2rem">
      <div style="font-size:3rem">${pct >= 80 ? '🎤' : '🎵'}</div>
      <div style="font-family:'Cinzel',serif;font-size:1.2rem;color:#9B2335;margin:0.5rem 0">${can.titulo}</div>
      <div style="font-size:1.5rem;font-weight:700;margin:0.5rem 0">${this.acertos}/${total} corretas</div>
      <div style="color:#888;margin-bottom:1rem">+${can.xp_recompensa} XP</div>
      <div style="display:flex;gap:0.5rem;justify-content:center">
        <button class="btn-primario" onclick="Canzoni.abrirCanzone('${can.id}')">🔄 Repetir</button>
        <button class="btn-secondario" onclick="Canzoni.renderizarSeletor()">‹ Outras músicas</button>
      </div>
    </div>`;
  }
};
