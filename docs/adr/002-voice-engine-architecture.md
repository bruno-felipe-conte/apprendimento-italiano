# ADR 002: Arquitetura do VoiceEngine e Síntese de Voz Híbrida

## Contexto
O aprendizado autêntico da língua italiana exige pronúncia precisa, respeitando regras fonéticas complexas:
- Acentuação tônica (palavras proparoxítonas / *sdrucciole*)
- Elisão e apócope (*l'amico*, *c'è*, *d'accordo*)
- Consoantes geminadas e pontuação entonacional (interrogação vs exclamação)
- Disponibilidade de áudio offline e em conexões lentas.

## Decisão
Criar uma pipeline híbrida em cascata no `js/voice_engine.js`:
1. **Normalização Fonética Prévia**:
   - Compilação de léxico de substituição fonética para termos irregulares.
   - Normalização de elisões e pontuação prosódica antes do envio ao motor TTS.
2. **Cascata de Síntese**:
   - **Camada 1 (Neural Local via WASM)**: Síntese de alta fidelidade via WebAssembly (`it_IT-riccardo-x_low`). Áudio renderizado é salvo automaticamente em cache binário permanente no `IndexedDB` (`audio_cache.js`).
   - **Camada 2 (Web Speech API Nativa)**: Fallback instantâneo usando vozes naturais do sistema operacional com filtro `it-IT`.
   - **Camada 3**: Fallback defensivo com cancelamento de timers e liberação de locks de áudio.
3. **Mastering de Áudio**:
   - Filtro passa-altas e compressão dinâmica via `AudioContext` para evitar distorções de graves em alto-falantes de dispositivos móveis.

## Consequências
- Áudios gerados ou tocados ficam disponíveis com 0ms de latência mesmo offline via `IndexedDB`.
- Eliminação de dependências legadas externas de terceiros (ex: scripts remotos não confiáveis).
