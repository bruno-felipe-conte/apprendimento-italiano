// ============================================================
// i18n.js — Sistema de Localização (Imersão Total em Italiano)
// ============================================================

const I18n = {
  idioma: 'pt',
  
  dict: {
    // ── Abas de Navegação (Bottom / Mobile) ──
    'nav_inicio': { pt: 'Início', it: 'Inizio' },
    'nav_dialogos': { pt: 'Diálogos', it: 'Dialoghi' },
    'nav_canzoni': { pt: 'Canzoni', it: 'Canzoni' },
    'nav_imitacao': { pt: 'Imitação', it: 'Imitazione' },
    'nav_flashcard': { pt: 'Flashcard', it: 'Cartoline' },
    'nav_quiz': { pt: 'Quiz', it: 'Testo' },
    'nav_vocab': { pt: 'Vocab', it: 'Vocabolario' },
    'nav_gramatica': { pt: 'Gramática', it: 'Grammatica' },
    
    // ── Abas de Navegação (Top / Desktop) ──
    'top_nav_templi': { pt: 'Templi', it: 'Templi' },
    'top_nav_dialoghi': { pt: 'Dialoghi', it: 'Dialoghi' },
    'top_nav_canzoni': { pt: 'Canzoni', it: 'Canzoni' },
    'top_nav_imitazione': { pt: 'Imitazione', it: 'Imitazione' },
    'top_nav_flashcard': { pt: 'Flashcard', it: 'Cartoline' },
    'top_nav_quiz': { pt: 'Quiz', it: 'Testo' },
    'top_nav_vocabolario': { pt: 'Vocabolario', it: 'Vocabolario' },
    'top_nav_grammatica': { pt: 'Grammatica', it: 'Grammatica' },

    // ── Elementos Globais ──
    'meta_do_dia': { pt: 'Meta do dia', it: 'Obiettivo del giorno' },
    'config_perfil': { pt: 'Configurações & Perfil', it: 'Impostazioni & Profilo' },
    'btn_fechar': { pt: 'Fechar', it: 'Chiudi' },
    'btn_cancelar': { pt: 'Cancelar', it: 'Annulla' },
    'btn_salvar': { pt: 'Salvar', it: 'Salva' },

    // ── Modal de Configurações ──
    'cfg_titulo': { pt: 'Configurações', it: 'Impostazioni' },
    'cfg_idioma_app': { pt: 'Idioma do App', it: 'Lingua dell\'App' },
    'cfg_idioma_pt': { pt: 'Português (PT)', it: 'Portoghese (PT)' },
    'cfg_idioma_it': { pt: 'Italiano (IT) - Imersão', it: 'Italiano (IT) - Immersione' },
    'cfg_tema_claro': { pt: 'Modo Claro', it: 'Tema Chiaro' },
    'cfg_tema_escuro': { pt: 'Modo Escuro', it: 'Tema Scuro' },
    'cfg_sons_ligados': { pt: 'Sons: Ligados', it: 'Suoni: Attivi' },
    'cfg_sons_desligados': { pt: 'Sons: Desligados', it: 'Suoni: Disattivati' },
    
    // ── Seção Templos ──
    'templi_titulo': { pt: 'Sua Jornada', it: 'Il Tuo Viaggio' },
    'templi_sub': { pt: 'Explore os templos e domine o vocabulário.', it: 'Esplora i templi e padroneggia il vocabolario.' },
    'btn_continuar': { pt: 'Continuar de Onde Parou', it: 'Continua da Dove Eri Rimasto' },

    // ── Feedback e Notificações (Usados no JS) ──
    'notif_salvo': { pt: 'Salvo com sucesso!', it: 'Salvato con successo!' },
    'notif_erro': { pt: 'Ocorreu um erro.', it: 'Si è verificato un errore.' },
    'notif_bloqueado': { pt: 'Templo não desbloqueado.', it: 'Tempio non sbloccato.' }
  },

  inicializar() {
    this.idioma = localStorage.getItem('it_idioma') || 'pt';
    this.traduzirDOM();
  },

  mudarIdioma(lang) {
    if (lang !== 'pt' && lang !== 'it') return;
    this.idioma = lang;
    localStorage.setItem('it_idioma', lang);
    this.traduzirDOM();
    if (typeof App !== 'undefined') App.notificar(lang === 'it' ? 'Lingua cambiata in Italiano!' : 'Idioma alterado para Português!', 'sucesso');
  },

  toggleIdioma() {
    this.mudarIdioma(this.idioma === 'pt' ? 'it' : 'pt');
  },

  // Retorna a string traduzida baseada na chave
  t(chave) {
    if (!this.dict[chave]) return chave; // Retorna a chave se não existir tradução
    return this.dict[chave][this.idioma] || this.dict[chave]['pt'];
  },

  // Busca todos os elementos com data-i18n e substitui o innerText (ou HTML mantendo ícones)
  traduzirDOM() {
    const elementos = document.querySelectorAll('[data-i18n]');
    elementos.forEach(el => {
      const chave = el.getAttribute('data-i18n');
      if (this.dict[chave]) {
        const texto = this.dict[chave][this.idioma] || this.dict[chave]['pt'];
        
        if (el.tagName.toLowerCase() === 'input' && el.type === 'button') {
          el.value = texto;
        } else if (el.tagName.toLowerCase() === 'button' && el.querySelector('span')) {
            // Se o botão tiver um <span> dentro (como bottom nav), traduz o textContent apenas do <span>, 
            // assumindo que há um ícone emoji fora do span. Se o HTML for 🏛️<span>Início</span>
            el.querySelector('span').textContent = texto;
        } else {
            // Se houver emoji junto no texto (ex: 💬 Dialoghi), isso vai sobrescrever.
            // Para prevenir a remoção dos emojis, vamos usar replace no HTML ou os data-i18n devem 
            // envolver apenas o texto.
            // Para as navs do topo, vamos considerar: `💬 <span data-i18n="...">Dialoghi</span>`
          el.textContent = texto;
        }
      }
    });

    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) {
      langBtn.textContent = this.idioma === 'pt' ? '🇮🇹' : '🇧🇷';
      langBtn.title = this.idioma === 'pt' ? 'Mudar para Italiano' : 'Cambia in Portoghese';
    }
  }
};
