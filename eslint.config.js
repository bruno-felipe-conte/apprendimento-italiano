import js from '@eslint/js';
import globals from 'globals';

export default [
  js.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.worker,
        ...globals.node,
        App: 'writable',
        VoiceEngine: 'writable',
        AudioCache: 'writable',
        I18n: 'writable',
        SomFeedback: 'writable',
        FSRS: 'writable',
        Flashcards: 'writable',
        Quiz: 'writable',
        Vocab: 'writable',
        Storie: 'writable',
        Grammatica: 'writable',
        Dialoghi: 'writable',
        Canzoni: 'writable',
        Imitazione: 'writable',
        Heatmap: 'writable',
        Profilo: 'writable',
        Conquistas: 'writable',
        IAImport: 'writable',
        Onboarding: 'writable',
        Notificacoes: 'writable',
        Tour: 'writable',
        Progressao: 'writable',
        Calor: 'writable',
        driver: 'writable',
        confetti: 'writable'
      }
    },
    rules: {
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      'no-empty': ['warn', { allowEmptyCatch: true }],
      'no-console': 'off',
      'no-useless-escape': 'off',
      'no-misleading-character-class': 'off',
      'no-undef': 'error'
    }
  },
  {
    ignores: [
      'node_modules/**',
      'graphify-out/**',
      'wasm/**',
      'data/**'
    ]
  }
];
