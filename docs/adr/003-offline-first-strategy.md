# ADR 003: Estratégia de Arquitetura Offline-First (PWA & Cache)

## Contexto
O aplicativo deve funcionar integralmente em trens, aviões ou locais sem conexão estável com a internet. O usuário não deve perder nenhum progresso de estudo nem encontrar telas em branco de erro de rede.

## Decisão
Implementar uma arquitetura estritamente **Offline-First** combinando:
1. **Service Worker (`sw.js`)**:
   - Cache versionado (`italiano-vXXX`) com estratégia *cache-first* para todos os assets estáticos (HTML, CSS, JS, ícones, dicionários de tradução i18n).
   - Estratégia *stale-while-revalidate* para dados de conteúdo (`/data/*.json`) e Google Fonts, garantindo inicialização instantânea e atualização transparente em segundo plano.
2. **Armazenamento Local Duplo**:
   - **`localStorage`**: Para dados estruturados leves de sessão (progresso de XP, streak diário, histórico de quizzes, estado de flashcards FSRS e preferências do usuário).
   - **`IndexedDB` (`it_audio_db`)**: Para payloads de mídia e arquivos grandes (arquivos de áudio sintetizados e cache persistente de traduções com TTL de 7 dias).
3. **Resiliência a Falhas de Rede**:
   - Utilitário `fetchWithRetry` com backoff exponencial e tratamento de HTTP 429 (*Too Many Requests*).
   - Fallback defensivo com respostas sintéticas estruturadas para evitar quebras de runtime.

## Consequências
- Tempo de carregamento subsequente < 500ms (TTI).
- A aplicação é 100% utilizável sem conexão ativa à internet.
- Todo o progresso do usuário é persistido localmente e protegido contra perdas acidentais.
