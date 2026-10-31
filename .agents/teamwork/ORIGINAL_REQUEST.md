# Original User Request

## 2026-10-30T23:53:49Z

Auditoria profunda de estresse e resiliência para identificar e corrigir falhas limítrofes ("problemas impensáveis"), atritos de fluxo de trabalho e refinamento contínuo da experiência de usuário (UX) em todas as camadas da aplicação Aprendimento Italiano.

Working directory: /mnt/c/Users/bruno/Documents/apprendimento-italiano
Integrity mode: development

## Requirements

### R1. Diagnóstico de Falhas Limítrofes e Cenários Críticos Ocultos
Identificar proativamente cenários anômalos que quebram o estado ou a consistência da aplicação:
- Corrupção ou perda silenciosa de dados no `localStorage`/`IndexedDB` (ex: limite de cota atingido, sessões concorrentes em múltiplas abas, importação de JSON corrompido ou payload legado).
- Anomalias matemáticas e de borda no algoritmo FSRS/Ebbinghaus (ex: avaliações em timestamps passados, descompasso de timezone, saltos temporais de anos, estabilidade tendendo a zero ou infinito).
- Falhas de concorrência e transições de tela durante reprodução de áudio/TTS ou durante micro-pausas e animações interativas (ex: duplo-clique rápido, navegação abrupta entre abas enquanto requisições ou timers assíncronos estão em voo).

### R2. Otimização de Ergonomia, Experiência de Uso (UX) e Redução de Atrito
Eliminar fricções na rotina diária de aprendizado e no comportamento PWA/Mobile:
- Eliminar engasgos visuais e comportamentos inesperados de rolagem e viewport (como o overscroll pull-to-refresh acidental arrastando cabeçalhos em modo PWA/standalone).
- Garantir coerência e acessibilidade integral em atalhos de teclado, leitores de tela e áreas de toque mínimas (44x44px) nos cards e quizes.
- Aprimorar o feedback visual e cognitivo durante a resolução de exercícios e transições de tela, prevenindo fadiga mental do usuário.

### R3. Implementação e Resolução das Falhas Críticas Encontradas
Aplicar correções limpas e modulares para todos os problemas de alta e média severidade detectados durante a investigação, mantendo a arquitetura zero-external-runtime-deps e preservando 100% de retrocompatibilidade com o progresso dos usuários.

### R4. Estruturação do Framework de Melhoria Contínua
Criar testes de estresse automatizados (fuzzing de payloads, testes de borda temporal e validação de migração de schemas) que blindem o aplicativo contra regressões futuras, acompanhado de um roteiro documentado de evolução de longo prazo.

## Verification Resources
- Suíte de testes existente (`npm test` rodando via Vitest).
- Build de validação (`npm run build`).
- Scripts e fixtures de dados em `data/` e `tests/`.

## Acceptance Criteria

### Integridade e Resiliência Técnica
- [ ] Testes de estresse/fuzzing implementados e cobrindo cenários de importação maliciosa/corrompida, limites de cota de armazenamento e múltiplos eventos concorrentes.
- [ ] O algoritmo FSRS e o cálculo da Curva de Ebbinghaus continuam matematicamente estáveis e sem erros de NaN/Infinity em qualquer input de data ou avaliação repetida.
- [ ] Zero erros não tratados no console (`unhandled promise rejection` ou exceções silenciosas) durante interrupções abruptas de áudio, troca rápida de abas ou cancelamento de navegação.

### Qualidade de UX e PWA
- [ ] Comportamento do layout em modo tela cheia / PWA blindado contra arrasto indesejado (`overscroll-behavior` e prevenção de bounce nos headers).
- [ ] Feedback visual claro em todas as ações de estudo (micro-pausas, indicadores de status e atalhos de teclado responsivos sem travamentos).

### Verificação de Regressão e Produção
- [ ] 100% dos testes existentes e novos passam com sucesso (`npm test`).
- [ ] O comando `npm run build` executa e conclui com código 0 gerando todos os assets estáticos sem warnings críticos.
- [ ] Relatório detalhado gerado catalogando: anomalias encontradas, correções aplicadas e propostas priorizadas de melhoria contínua de UX.
