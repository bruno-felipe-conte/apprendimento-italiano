import js from '@eslint/js';
import globals from 'globals';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.worker,
        ...globals.node,
        App: 'writable',
        AppState: 'writable',
        AppNavigation: 'writable',
        AppXP: 'writable',
        AppStats: 'writable',
        AppMeta: 'writable',
        AppFavorites: 'writable',
        AppTemploData: 'writable',
        AppTemploModal: 'writable',
        AppTemplos: 'writable',
        AppTTS: 'writable',
        ModalManager: 'writable',
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
        LevelUp: 'writable',
        Calor: 'writable',
        driver: 'writable',
        confetti: 'writable'
      }
    },
    rules: {
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-empty-function': 'off',
      'no-empty': ['warn', { allowEmptyCatch: true }],
      'no-console': 'off',
      'no-useless-escape': 'off',
      'no-misleading-character-class': 'off',
      'no-undef': 'off'
    }
  },
  {
    ignores: [
      'node_modules/**',
      'dist/**',
      'graphify-out/**',
      'wasm/**',
      'data/**'
    ]
  }
);
