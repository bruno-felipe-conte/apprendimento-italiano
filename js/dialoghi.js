const Dialoghi = {
  dados: null,
  dialogoAtual: null,
  turnoAtual: 0,
  modo: 'leitura', // 'leitura' | 'pratica'
  acertos: 0,
  
  async carregar() {
    if (this.dados) return;
    try {
      const r = await fetch('data/dialogi.json');
      this.dados = await r.json();
    } catch (e) {
      console.error('Erro ao carregar dialogi.json', e);
    }
  },
  
  async renderizarSeletor() {
    await this.carregar();
    const c = document.getElementById('dialoghi-container');
    if (!c || !this.dados) return;
    
    let html = '<div class="dialogo-grid">';
    for (const d of this.dados.dialogi) {
      html += `
        <div class="dialogo-card" onclick="Dialoghi.abrirDialogo('${d.id}')">
          <div class="dialogo-icone">${d.icone}</div>
          <div class="dialogo-titulo">${d.titulo}</div>
          <div class="dialogo-nivel">${d.nivel}</div>
          <div style="font-size:0.75rem;color:var(--cor-pietra);margin-top:0.3rem">🎁 ${d.xp_recompensa} XP</div>
        </div>
      `;
    }
    html += '</div>';
    c.innerHTML = html;
  },
  
  abrirDialogo(id, modo) {
    this.dialogoAtual = this.dados.dialogi.find(d => d.id === id);
    if (!this.dialogoAtual) return;
    this.turnoAtual = 0;
    this.acertos = 0;
    this.modo = modo || 'leitura';
    this.renderizarDialogo();
  },
  
  renderizarDialogo() {
    const c = document.getElementById('dialoghi-container');
    const d = this.dialogoAtual;
    
    let html = `
      <div style="margin-bottom:1rem;display:flex;align-items:center;justify-content:space-between">
        <button class="btn-secondario" onclick="Dialoghi.renderizarSeletor()" style="padding:0.4rem 0.8rem">‹ Voltar</button>
        <div style="display:flex;gap:0.5rem">
          <button class="btn-modo-toggle ${this.modo === 'leitura' ? 'ativo' : ''}" onclick="Dialoghi.modo='leitura';Dialoghi.turnoAtual=0;Dialoghi.renderizarDialogo()" title="Modo Leitura">📖</button>
          <button class="btn-modo-toggle ${this.modo === 'pratica' ? 'ativo' : ''}" onclick="Dialoghi.modo='pratica';Dialoghi.turnoAtual=0;Dialoghi.renderizarDialogo()" title="Modo Prática">✍️</button>
        </div>
      </div>
      <div style="text-align:center;margin-bottom:1rem">
        <div style="font-size:2rem">${d.icone}</div>
        <h3 style="font-family:'Cinzel',serif;color:var(--cor-veneziano-escuro);margin:0.2rem 0">${d.titulo}</h3>
        <p style="font-size:0.85rem;color:var(--cor-pietra);font-style:italic">${d.contexto}</p>
      </div>
      <div class="dialogo-conversa">
    `;
    
    if (this.modo === 'leitura') {
      for (const t of d.turni) {
        const isUtente = t.personaggio === 'Tu';
        const cssClass = isUtente ? 'utente' : 'personaggio';
        html += `
          <div class="dialogo-turno ${cssClass}">
            <div class="dialogo-bubble">
              <div class="dialogo-nome">${t.personaggio}</div>
              <div>${t.frase} <button class="dialogo-audio-btn" onclick="App.pronunciar('${t.frase.replace(/'/g, "\\'")}')">🔊</button></div>
              <div class="dialogo-traducao">${t.traducao}</div>
            </div>
          </div>
        `;
      }
      html += `
        <div style="text-align:center;margin-top:1.5rem">
          <button class="btn-primario" onclick="Dialoghi.modo='pratica';Dialoghi.turnoAtual=0;Dialoghi.renderizarDialogo()">Praticar Diálogo ✍️</button>
        </div>
      `;
    } else {
      // Modo prática: renderiza apenas o turno atual e os anteriores
      for (let i = 0; i <= this.turnoAtual; i++) {
        const t = d.turni[i];
        const isUtente = t.personaggio === 'Tu';
        const cssClass = isUtente ? 'utente' : 'personaggio';
        
        if (i < this.turnoAtual) {
          // Histórico (já respondido)
          html += `
            <div class="dialogo-turno ${cssClass}">
              <div class="dialogo-bubble">
                <div class="dialogo-nome">${t.personaggio}</div>
                <div>${t.frase}</div>
              </div>
            </div>
          `;
        } else {
          // Turno ativo
          if (!isUtente) {
            // Fala do personagem
            html += `
              <div class="dialogo-turno ${cssClass}" style="animation:fadeIn 0.3s ease">
                <div class="dialogo-bubble">
                  <div class="dialogo-nome">${t.personaggio}</div>
                  <div>${t.frase} <button class="dialogo-audio-btn" onclick="App.pronunciar('${t.frase.replace(/'/g, "\\'")}')">🔊</button></div>
                  <div class="dialogo-traducao">${t.traducao}</div>
                </div>
              </div>
              <div style="text-align:center;margin-top:1rem">
                <button class="btn-primario" onclick="Dialoghi.avancarTurno()">Continuar</button>
              </div>
            `;
          } else {
            // Escolha do usuário
            html += `
              <div style="margin-top:1rem;animation:fadeIn 0.3s ease">
                <div class="dialogo-pratica-frase">Sua vez de falar. Escolha a melhor resposta:</div>
                <div class="dialogo-opcoes">
            `;
            t.alternativas.forEach((alt, idx) => {
              html += `<button class="dialogo-opcao" onclick="Dialoghi.checarResposta(${idx}, this)">${alt}</button>`;
            });
            html += `
                </div>
              </div>
            `;
          }
        }
      }
    }
    
    html += '</div>';
    c.innerHTML = html;
  },
  
  avancarTurno() {
    this.turnoAtual++;
    if (this.turnoAtual >= this.dialogoAtual.turni.length) {
      this.mostrarResultado();
    } else {
      this.renderizarDialogo();
    }
  },
  
  checarResposta(indice, btn) {
    const turno = this.dialogoAtual.turni[this.turnoAtual];
    const correto = indice === turno.resposta_correta;
    
    // Desabilita botões
    const container = btn.parentElement;
    container.querySelectorAll('button').forEach(b => {
      b.disabled = true;
      b.style.cursor = 'default';
    });
    
    if (correto) {
      this.acertos++;
      btn.classList.add('correta');
      App.pronunciar(turno.alternativas[indice]);
      setTimeout(() => {
        this.avancarTurno();
      }, 1200);
    } else {
      btn.classList.add('errada');
      container.children[turno.resposta_correta].classList.add('correta');
      setTimeout(() => {
        this.avancarTurno();
      }, 2500);
    }
  },
  
  mostrarResultado() {
    const d = this.dialogoAtual;
    const totalTu = d.turni.filter(t => t.personaggio === 'Tu').length;
    const pct = Math.round((this.acertos / totalTu) * 100);
    
    // Apenas ganha XP se acertar a maioria e estiver no modo prática
    let ganhouXp = false;
    if (this.modo === 'pratica' && pct >= 60) {
      Progressao.ganhar(d.xp_recompensa);
      ganhouXp = true;
    }
    
    const c = document.getElementById('dialoghi-container');
    c.innerHTML = `
      <div style="text-align:center;padding:2rem 1rem">
        <div style="font-size:3rem">${pct >= 80 ? '🌟' : (pct >= 50 ? '👍' : '🔄')}</div>
        <h3 style="font-family:'Cinzel',serif;color:var(--cor-veneziano-escuro);font-size:1.5rem;margin:1rem 0">Diálogo Concluído</h3>
        <div style="font-size:1.1rem;margin-bottom:1rem">Acertos: <strong>${this.acertos} / ${totalTu}</strong></div>
        ${ganhouXp ? `<div style="color:var(--cor-toscano);font-weight:700;font-size:1.2rem;margin-bottom:1.5rem">+${d.xp_recompensa} XP</div>` : ''}
        
        <div style="background:var(--cor-marmore);border-radius:12px;padding:1rem;margin-bottom:1.5rem;text-align:left;box-shadow:0 2px 10px rgba(0,0,0,0.05)">
          <div style="font-size:0.8rem;color:var(--cor-pietra);text-transform:uppercase;font-weight:700;margin-bottom:0.5rem">Vocabulário Chave:</div>
          <div style="display:flex;gap:0.5rem;flex-wrap:wrap">
            ${d.vocabulario_chave.map(v => `<span style="background:var(--cor-pergaminho);color:var(--cor-veneziano-escuro);padding:0.2rem 0.6rem;border-radius:20px;font-size:0.85rem">${v}</span>`).join('')}
          </div>
        </div>
        
        <div style="display:flex;gap:1rem;justify-content:center">
          <button class="btn-secondario" onclick="Dialoghi.renderizarSeletor()">‹ Voltar</button>
          <button class="btn-primario" onclick="Dialoghi.abrirDialogo('${d.id}', 'pratica')">Praticar Novamente 🔄</button>
        </div>
      </div>
    `;
  }
};
