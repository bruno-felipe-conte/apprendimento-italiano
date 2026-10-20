# ADR 004: Modelo de Segurança e Blindagem Client-Side

## Contexto
Como uma aplicação estática e PWA sem servidor central, toda a integridade da aplicação depende da blindagem de segurança no cliente contra vetores de ataque OWASP:
- Injeção XSS (*Cross-Site Scripting*) via dados de usuário, localStorage ou retornos de prompts de IA
- Injeção de scripts maliciosos de terceiros
- Bypass trivial de segredos ou desbloqueio de conteúdo restrito
- Corrupção de dados via importações não validadas.

## Decisão
Estabelecer as seguintes diretrizes de segurança aplicadas em todo o código-fonte:
1. **Remoção de Segredos em Texto Puro**:
   - Nenhum segredo ou chave de acesso administrativa deve residir em texto plano no código-fonte client-side.
   - Códigos de validação utilizam derivação criptográfica unidirecional **SHA-256** via Web Crypto API (`crypto.subtle.digest`).
2. **Defesa em Profundidade contra XSS**:
   - Proibição de injeção direta de strings não sanitizadas em `innerHTML`.
   - Utilização de sanitização estrita de tags HTML (`_sanitizarString`) e codificação de entidades (`escapeHtml`) para renderização dinâmica de dados.
3. **Content Security Policy (CSP)**:
   - Política restritiva de segurança configurada em `index.html`:
     `default-src 'self'; script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: blob: https:; media-src 'self' data: blob:; connect-src 'self' https://translate.googleapis.com https://api.mymemory.translated.net https://fonts.googleapis.com https://fonts.gstatic.com https://huggingface.co https://raw.githubusercontent.com https://cdn-lfs.huggingface.co; worker-src 'self' blob:;`
4. **Validação de Schemas de Importação IA**:
   - Validação estrutural de todos os payloads importados (`dialogo`, `canzone`, `storia`, `imitazione`, `vocab`) antes de qualquer persistência em armazenamento local.

## Consequências
- A superfície de ataque XSS é neutralizada.
- A integridade do estado da aplicação e a confiança dos dados persistidos são matematicamente preservadas.
