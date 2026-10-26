// ============================================================
// js/plugins/index.ts — Built-in Feature Plugins (EV-01)
// Converte as seções de estudo em plugins com rotas e ciclo de vida.
// ============================================================

import type { IPlugin } from '../../types/app';
import { AppPluginManager } from '../core/plugins.js';

const _precisaRender = (containerId: string): boolean => {
  if (typeof document === 'undefined') return false;
  const el = document.getElementById(containerId);
  if (!el) return true;
  return (
    el.children.length === 0 ||
    !!el.querySelector('.skeleton-box, .skeleton-card-media, .skeleton-card-templo, .skeleton-vocab-row')
  );
};

export const FlashcardsPlugin: IPlugin = {
  id: 'flashcards',
  name: 'Flashcards FSRS',
  version: '1.0.0',
  routes: [
    {
      path: 'flashcard',
      title: 'Flashcards',
      handler: () => {
        const win = typeof window !== 'undefined' ? window : null;
        if (win?.Flashcards?.atualizarSelectTemplo) {
          win.Flashcards.atualizarSelectTemplo();
        }
      }
    }
  ],
  init: () => {}
};

export const QuizPlugin: IPlugin = {
  id: 'quiz',
  name: 'Quiz Morfológico',
  version: '1.0.0',
  routes: [
    {
      path: 'quiz',
      title: 'Quiz',
      handler: () => {
        const win = typeof window !== 'undefined' ? window : null;
        if (win?.Quiz && _precisaRender('quiz-templo-selector')) {
          win.Quiz.renderizarSeletor();
        }
      }
    }
  ],
  init: () => {}
};

export const VocabPlugin: IPlugin = {
  id: 'vocabolario',
  name: 'Vocabolario dei Templi',
  version: '1.0.0',
  routes: [
    {
      path: 'vocabolario',
      title: 'Vocabolario',
      handler: () => {
        const win = typeof window !== 'undefined' ? window : null;
        if (win?.Vocab && _precisaRender('vocab-list')) {
          win.Vocab.renderizar();
        }
      }
    }
  ],
  init: () => {}
};

export const GrammaticaPlugin: IPlugin = {
  id: 'grammatica',
  name: 'Grammatica Metodo NMA',
  version: '1.0.0',
  routes: [
    {
      path: 'grammatica',
      title: 'Grammatica',
      handler: () => {
        const win = typeof window !== 'undefined' ? window : null;
        if (win?.Grammatica && _precisaRender('grammatica-container')) {
          win.Grammatica.renderizarSeletor();
        }
      }
    }
  ],
  init: () => {}
};

export const StoriePlugin: IPlugin = {
  id: 'storie',
  name: 'Storie & Filosofia',
  version: '1.0.0',
  routes: [
    {
      path: 'storie',
      title: 'Storie',
      handler: () => {
        const win = typeof window !== 'undefined' ? window : null;
        if (win?.Storie && _precisaRender('storie-container')) {
          win.Storie.renderizarSeletor();
        }
      }
    }
  ],
  init: () => {}
};

export const DialoghiPlugin: IPlugin = {
  id: 'dialoghi',
  name: 'Dialoghi Situazionali',
  version: '1.0.0',
  routes: [
    {
      path: 'dialoghi',
      title: 'Dialoghi',
      handler: () => {
        const win = typeof window !== 'undefined' ? window : null;
        if (win?.Dialoghi && _precisaRender('dialoghi-container') && !win.Dialoghi.dialogoAtual) {
          win.Dialoghi.renderizarSeletor();
        }
      }
    }
  ],
  init: () => {}
};

export const CanzoniPlugin: IPlugin = {
  id: 'canzoni',
  name: 'Canzoni Italiane',
  version: '1.0.0',
  routes: [
    {
      path: 'canzoni',
      title: 'Canzoni',
      handler: () => {
        const win = typeof window !== 'undefined' ? window : null;
        if (win?.Canzoni && _precisaRender('canzoni-container')) {
          win.Canzoni.renderizarSeletor();
        }
      }
    }
  ],
  onSectionChange: (novaSecao) => {
    const win = typeof window !== 'undefined' ? window : null;
    if (novaSecao !== 'canzoni' && win?.Canzoni?.tocandoKaraoke) {
      win.Canzoni.pararAudio();
    }
  },
  destroy: () => {
    const win = typeof window !== 'undefined' ? window : null;
    if (win?.Canzoni?.pararAudio) {
      win.Canzoni.pararAudio();
    }
  },
  init: () => {}
};

export const ImitazionePlugin: IPlugin = {
  id: 'imitazione',
  name: 'Treino de Shadowing & Fonética',
  version: '1.0.0',
  routes: [
    {
      path: 'imitazione',
      title: 'Imitazione',
      handler: () => {
        const win = typeof window !== 'undefined' ? window : null;
        if (win?.Imitazione && _precisaRender('imitazione-container')) {
          win.Imitazione.renderizar();
        }
      }
    }
  ],
  init: () => {}
};

export const ProfiloPlugin: IPlugin = {
  id: 'profilo',
  name: 'Profilo dello Studente',
  version: '1.0.0',
  routes: [
    {
      path: 'profilo',
      title: 'Profilo',
      handler: () => {
        const win = typeof window !== 'undefined' ? window : null;
        if (win?.Profilo) {
          win.Profilo.renderizar();
        }
      }
    }
  ],
  init: () => {}
};

export const CorePlugins: IPlugin[] = [
  FlashcardsPlugin,
  QuizPlugin,
  VocabPlugin,
  GrammaticaPlugin,
  StoriePlugin,
  DialoghiPlugin,
  CanzoniPlugin,
  ImitazionePlugin,
  ProfiloPlugin
];

export function registrarPluginsPadrao(): void {
  for (const plugin of CorePlugins) {
    AppPluginManager.register(plugin);
  }
}

// Auto-registro global se em ambiente de navegador
if (typeof window !== 'undefined') {
  registrarPluginsPadrao();
}
