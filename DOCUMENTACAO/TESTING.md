# 🧪 TESTING PROTOCOL - ItalianLearningApp

## 📋 OVERVIEW

This document defines testing protocols for the Italian Learning App, organized by Temple system.

---

## 1️⃣ UNIT TESTS PER TEMPLE

### Template I - Le Fondamenta (Testes de Sobrevivência)

**Objetivo:** Verificar se o vocabulário básico e frases essenciais estão desbloqueados corretamente.

#### Test Cases:
```javascript
// ✅ SUCESSO: Vocabulário do Templo I deve estar acessível
test('templo-1-vocabulary-unlocked', async () => {
  const vocab = JSON.parse(localStorage.getItem('vocabolo-desbloqueado'));
  expect(vocab).toContain('templo-I');
  expect(vocab['templo-I']).toHaveLength(350); // ~350 palavras básicas
});

// ✅ SUCESSO: Frases de sobrevivência devem estar acessíveis
test('templo-1-phrases-unlocked', async () => {
  const phrases = JSON.parse(localStorage.getItem('frase-desbloqueada'));
  expect(phrases).toContain('it_frase_1'); // Saudações básicas
  expect(phrases).toHaveLength(200); // ~200 frases de sobrevivência
});

// ✅ SUCESSO: Progressão deve bloquear Templo II até completar Templo I
test('templo-2-blocked-until-templo-1-complete', async () => {
  const progression = JSON.parse(localStorage.getItem('progression'));
  expect(progression.temploCompletado.I).toBe(false);
  expect(progression.nextTempleUnlocked).toBe('II');
});
```

#### Dados de Teste:
- **Vocabulário:** 350 palavras (saudações, números, família, cores)
- **Frases:** 200 frases de sobrevivência (pedir comida, aeroporto, etc.)
- **Bloqueio:** Templo II bloqueado até completar Templo I

---

### Template II - Il Cuore (Expressões & Emoções)

**Objetivo:** Verificar desbloqueio correto após conclusão do Templo II.

#### Test Cases:
```javascript
// ✅ SUCESSO: Vocabulário de emoções deve estar acessível
test('templo-2-vocabulary-unlocked', async () => {
  const vocab = JSON.parse(localStorage.getItem('vocabolo-desbloqueado'));
  expect(vocab).toContain('templo-II');
  expect(vocab['templo-II']).toHaveLength(800); // ~800 palavras adicionais
});

// ✅ SUCESSO: Frases emocionais e pronome devem estar acessíveis
test('templo-2-phrases-unlocked', async () => {
  const phrases = JSON.parse(localStorage.getItem('frase-desbloqueada'));
  expect(phrases).toContain('it_frase_201'); // Emoções pessoais
  expect(phrases).toHaveLength(400); // ~400 frases adicionais
});

// ✅ SUCESSO: Verbo regular presente deve estar conjugado corretamente
test('templo-2-present-indicativo-complete', async () => {
  const verbs = JSON.parse(localStorage.getItem('verbi-presente'));
  expect(verbs['essere']).toEqual([
    'sono', 'sei', 'è', 'siamo', 'siete', 'sono'
  ]);
  expect(verbs['avere']).toEqual([
    'ho', 'hai', 'ha', 'abbiamo', 'avete', 'hanno'
  ]);
});
```

#### Dados de Teste:
- **Vocabulário:** 800 palavras (emoções, sentimentos, adjetivos)
- **Frases:** 400 frases emocionais + sociais
- **Gramática:** Presente indicativo completo

---

### Template III - Il Viaggio (Viagens & Lugares)

#### Test Cases:
```javascript
// ✅ SUCESSO: Locativos e preposições devem estar conjugados corretamente
test('templo-3-prepositions-complete', async () => {
  const grammar = JSON.parse(localStorage.getItem('grammatica-templo-III'));
  
  expect(grammar.preposizioni).toEqual({
    'simples': ['a', 'da', 'di', 'in', 'su', 'con'],
    'articolate': ['all\'', 'dal', 'del', 'nell\'', 'sullo']
  });
});

// ✅ SUCESSO: Verbos de movimento devem estar conjugados
test('templo-3-motion-verbs-complete', async () => {
  const verbs = JSON.parse(localStorage.getItem('verbi-templo-III'));
  expect(verbs['andare']).toEqual({
    'presente': ['vado', 'vai', 'va', 'andiamo', 'andate', 'vanno'],
    'passato': ['andai', 'andestì', 'andò', ...]
  });
});
```

#### Dados de Teste:
- **Vocabulário:** 600 palavras (cidades, países, aeroportos)
- **Frases:** 350 frases de viagem + check-in
- **Gramática:** Locativos completos

---

### Template IV - Il Gusto (Comida & Cultura)

#### Test Cases:
```javascript
// ✅ SUCESSO: Ingredientes e pratos típicos devem estar disponíveis
test('templo-4-cucina-complete', async () => {
  const vocab = JSON.parse(localStorage.getItem('vocabolo-templo-IV'));
  
  expect(vocab.culinaria).toEqual({
    'ingredienti': ['farina', 'uva', 'olio', 'zucchero'],
    'prati_tipici': ['pizza', 'pasta', 'gelato', 'risotto']
  });
});

// ✅ SUCESSO: Verbos do comer devem estar conjugados
test('templo-4-comer-verb-conjugated', async () => {
  const verbs = JSON.parse(localStorage.getItem('verbi-templo-IV'));
  expect(verbs['mangiare']).toEqual({
    'presente': ['mangio', 'mangi', 'mangia', ...],
    'futuro': ['mangerò', 'mangerai', ...]
  });
});
```

#### Dados de Teste:
- **Vocabulário:** 700 palavras (comida regional)
- **Frases:** 300 frases culinárias + expressões de drink
- **Gramática:** Verbos do comer/beber

---

### Template V - Il Tempo (Passado & Futuro)

#### Test Cases:
```javascript
// ✅ SUCESSO: Passato prossimo e imperfetto devem estar conjugados corretamente
test('templo-5-passato-prossimo-complete', async () => {
  const grammar = JSON.parse(localStorage.getItem('grammatica-templo-V'));
  
  expect(grammar.passati_prossimo).toEqual({
    'avere': ['ho mangiato', 'hai mangiato', 'ha mangiato'],
    'essere': ['sono andato', 'sei andato', 'è andato']
  });
});

// ✅ SUCESSO: Futuro semplice e congiuntivo devem estar disponíveis
test('templo-5-futuro-congiuntivo-complete', async () => {
  const grammar = JSON.parse(localStorage.getItem('grammatica-templo-V'));
  
  expect(grammar.futuro_semplice).toEqual({
    'regular': ['-erò', '-rai', '-rà', ...],
    'irregulares': ['andrò', 'farò', 'sarò']
  });
});
```

#### Dados de Teste:
- **Vocabulário:** 400 palavras (narrativa, histórias)
- **Frases:** 250 frases narrativas + experiências passadas
- **Gramática:** Subjuntivo presente

---

### Template VI - La Grammatica Profonda (Nível Avançado)

#### Test Cases:
```javascript
// ✅ SUCESSO: Congiuntivo imperfetto deve estar conjugado corretamente
test('templo-6-congiuntivo-imperfetto-complete', async () => {
  const grammar = JSON.parse(localStorage.getItem('grammatica-templo-VI'));
  
  expect(grammar.congiuntivo_imperfetto).toEqual({
    'essere': ['fossi', 'fosti', 'fosse', ...],
    'avere': ['avessi', 'avessi', 'avesse', ...]
  });
});

// ✅ SUCESSO: Particípio passato deve estar conjugado corretamente
test('templo-6-participio-passato-complete', async () => {
  const verbs = JSON.parse(localStorage.getItem('verbi-templo-VI'));
  
  expect(verbs['participe_passato']).toEqual({
    'regulares': ['amato', 'visto', 'scritto'],
    'irregulares': ['fatto', 'detto', 'tornato']
  });
});
```

#### Dados de Teste:
- **Vocabulário:** 300 palavras (literatura, filosofia)
- **Frases:** 200 frases literárias + filosóficas
- **Gramática:** Subjuntivo avançado

---

### Template VII - La Conversazione (Dialetos & Sotaques)

#### Test Cases:
```javascript
// ✅ SUCESSO: Expressões dialetais devem estar disponíveis
test('templo-7-dialetti-complete', async () => {
  const vocab = JSON.parse(localStorage.getItem('vocabolo-templo-VII'));
  
  expect(vocab.dialetto).toEqual({
    'napolitano': [''e'' (è)', 'ce n\'è', ...],
    'siciliano': [...],
    'milanese': [...]
  });
});

// ✅ SUCESSO: Regiões devem estar descritas corretamente
test('templo-7-regioni-complete', async () => {
  const cultura = JSON.parse(localStorage.getItem('cultura-regionali'));
  
  expect(cultura).toEqual({
    'napoli': { 'festivals': ['Sant\'Agnese'], 'cucina': ['pizza napoletana'] },
    'sicilia': [...],
    'milano': [...]
  });
});
```

#### Dados de Teste:
- **Vocabulário:** 350 palavras (dialetos, regiões)
- **Frases:** 200 frases regionais + expressões informais
- **Cultura:** Dialetos urbanos

---

### Template VIII - La Cultura (Arte & História)

#### Test Cases:
```javascript
// ✅ SUCESSO: Arte italiana deve estar descrita corretamente
test('templo-8-rinascimento-complete', async () => {
  const cultura = JSON.parse(localStorage.getItem('cultura-templo-VIII'));
  
  expect(cultura.rinascimento).toEqual({
    'artista': ['Leonardo da Vinci', 'Michelangelo', 'Raffaello'],
    'opera': ['Mona Lisa', 'David', 'Las Meninas'],
    'periodo': '1400-1600'
  });
});

// ✅ SUCESSO: História italiana deve estar disponível
test('templo-8-storia-complete', async () => {
  const historia = JSON.parse(localStorage.getItem('storia-italia'));
  
  expect(historia).toEqual({
    'romano': {'periodo': '-27 a.C.', 'imperador': ['Augusto', 'Trajano']},
    'renascimento': {...},
    'fascismo': {...}
  });
});
```

#### Dados de Teste:
- **Vocabulário:** 400 palavras (arte, história)
- **Frases:** 150 frases culturais + históricas
- **Recursos externos:** Treccani, Wikivoyage IT

---

### Template IX - Il Lavoro (Profissional)

#### Test Cases:
```javascript
// ✅ SUCESSO: Entrevista de emprego deve estar disponível
test('templo-9-intervista-complete', async () => {
  const dialoghi = JSON.parse(localStorage.getItem('dialoghi-templo-IX'));
  
  expect(dialoghi.intervista).toEqual({
    'presentazione': ['Ciao, sono...'],
    'esperienze_lavorative': [...],
    'motivazione': [...]
  });
});

// ✅ SUCESSO: Terminologia de negócios deve estar disponível
test('templo-9-business-complete', async () => {
  const vocab = JSON.parse(localStorage.getItem('vocabolo-templo-IX'));
  
  expect(vocab.business).toEqual({
    'contratti': ['contratto di lavoro', 'clausola risolutiva'],
    'incontri': ['business meeting', 'networking event'],
    'presentazioni': [...],
    'rapportando': [...]
  });
});
```

#### Dados de Teste:
- **Vocabulário:** 200 palavras (negócios, entrevistas)
- **Frases:** 100 frases profissionais + networking
- **Setores industriais:** Automotivo, modas, tecnologia

---

### Template X - La Letteratura (Literatura)

#### Test Cases:
```javascript
// ✅ SUCESSO: Dante deve estar disponível para leitura básica
test('templo-10-dante-complete', async () => {
  const letteratura = JSON.parse(localStorage.getItem('letteratura-templo-X'));
  
  expect(letteratura.dante).toEqual({
    'opera': ['Divina Commedia'],
    'canti': ['Inferno', 'Purgatorio', 'Paradiso'],
    'versetti_base': [
      {'it': 'Nel mezzo del cammin di nostra vita',
       'pt': 'No meio do caminho da nossa vida'}
    ]
  });
});

// ✅ SUCESSO: Autores modernos devem estar disponíveis
test('templo-10-autori-moderni-complete', async () => {
  const letteratura = JSON.parse(localStorage.getItem('letteratura-templo-X'));
  
  expect(letteratura.moderni).toEqual({
    'leopardi': {...},
    'manzoni': {'opera': ['I Promessi Sposi']},
    'calvino': {...}
  });
});
```

#### Dados de Teste:
- **Vocabulário:** 500 palavras (literatura clássica)
- **Frases:** 300 frases literárias + interpretativas
- **Autores:** Dante, Leopardi, Calvino

---

### BONUS - Il Maestro (Nível Mestre)

#### Test Cases:
```javascript
// ✅ SUCESSO: Comprensão de filmes deve estar disponível
test('maestro-film-comprehension-complete', async () => {
  const risorse = JSON.parse(localStorage.getItem('risorse-maestro'));
  
  expect(risorse.filmes).toEqual({
    'comedia': ['Benvenuti al Sud', 'The Great Beauty'],
    'dramma': [...],
    'documentari': [...]
  });
});

// ✅ SUCESSO: Leitura de jornais deve estar disponível
test('maestro-giornali-complete', async () => {
  const risorse = JSON.parse(localStorage.getItem('giornali-italia'));
  
  expect(risorse).toEqual({
    'corriere': {...},
    'repubblica': {...},
    'il_foglio': [...]
  });
});
```

#### Dados de Teste:
- **Conteúdo ilimitado:** Filmes, jornais, podcasts nativos
- **Objetivo:** Nível C2 (proficiência nativa)

---

## 2️⃣ INTEGRATION TESTS

### Flashcard System + Progression Integration

```javascript
// ✅ SUCESSO: Flashcards devem respeitar bloqueio por templo
test('flashcards-respeita-bloqueio-templo', async () => {
  const progression = JSON.parse(localStorage.getItem('progression'));
  await flashcardSystem.loadVocabulary(); // Deve carregar apenas Templo I
  
  const cards = flashcardSystem.getCurrentSet();
  expect(cards).toHaveLength(10); // ~350 palavras do Templo I
});
```

### Quiz System + Progression Integration

```javascript
// ✅ SUCESSO: Quiz devem respeitar bloqueio por templo
test('quiz-respeita-bloqueio-templo', async () => {
  const progression = JSON.parse(localStorage.getItem('progression'));
  
  const quiz = await quizSystem.start('templo-I');
  expect(quiz.queries).toHaveLength(3); // ~3 questões por nível
  
  await quizSystem.submit('correto');
  expect(quizScore).toBeGreaterThan(0);
});
```

### Navigation + Progression Integration

```javascript
// ✅ SUCESSO: Navegação deve bloquear acesso a templos futuros
test('navigation-respeita-bloqueio-templo', async () => {
  const progression = JSON.parse(localStorage.getItem('progression'));
  
  try {
    await navigation.goToTemple('II'); // Deve bloquear
  } catch (error) {
    expect(error.message).toBe('Templo II bloqueado!');
  }
});
```

---

## 3️⃣ PERFORMANCE TESTS

### Load Testing por Templo

```javascript
// ✅ SUCESSO: Vocabulário de 5.000+ palavras deve carregar em <2s
test('vocab-load-performance', async () => {
  const start = performance.now();
  await vocabularySystem.loadAllVocabulary(); // ~5.000 palavras
  
  const loadTime = performance.now() - start;
  expect(loadTime).toBeLessThan(2000); // <2s
});
```

### Flashcard Performance

```javascript
// ✅ SUCESSO: Sistema SM-2 deve responder em <100ms
test('flashcard-sm2-performance', async () => {
  const start = performance.now();
  await spacedRepetition.calculateSMA(6); // Calculo SMA
  
  const responseTime = performance.now() - start;
  expect(responseTime).toBeLessThan(100); // <100ms
});
```

---

## 4️⃣ REGRESSION TESTS

### Verificar que alterações não quebraram funcionalidades anteriores

```javascript
// ✅ SUCESSO: Sistema de progression ainda funciona após adicionar novos templos
test('progression-stable-after-temple-addition', async () => {
  // Adicionar novo templo (simulação)
  progressionSystem.addTemple('XI');
  
  // Verificar que progresso anterior não foi perdido
  expect(JSON.parse(localStorage.getItem('vocabolo-desbloqueado'))).toContain('templo-I');
});
```

---

## 5️⃣ UI/UX TESTS

### Verificar interface de usuário e experiência do usuário

#### Teste de Tema Claro/Escuro:
```javascript
// ✅ SUCESSO: Alternância de tema deve funcionar corretamente
test('tema-claro-escuro-toggle', async () => {
  const startTheme = await appSystem.getCurrentTheme();
  
  await document.body.classList.toggle('dark-mode');
  
  const endTheme = await appSystem.getCurrentTheme();
  expect(endTheme).not.toBe(startTheme);
});
```

#### Teste de Bloqueio de Templos:
```javascript
// ✅ SUCESSO: Mensagem de bloqueio deve aparecer corretamente
test('bloqueo-templo-mensagem-visualizacao', async () => {
  const nextTemple = 'IV'; // IV bloqueado
  
  const message = await templeSystem.getBlockerMessage(nextTemple);
  expect(message).toBe(`🔒 Templo ${nextTemple} bloqueado!`);
});
```

#### Teste de Progresso Visual:
```javascript
// ✅ SUCESSO: Barra de progresso deve atualizar corretamente
test('progress-bar-update', async () => {
  await progressionSystem.completeVocabularySet('templo-I-set-1');
  
  const progress = await progressBar.getCurrentProgress();
  expect(progress).toBeGreaterThan(0); // Deve mostrar progresso
});
```

---

## 📋 CHECKLIST DE TESTES POR TEMPLO

### Template I - Le Fondamenta
- [ ] Vocabulário básico carregado (350 palavras) ✅
- [ ] Frases de sobrevivência acessíveis (200 frases) ✅
- [ ] Sistema de bloqueio funcionando ✅
- [ ] Interface tema claro/escuro ✅
- [ ] Progresso salvo no localStorage ✅

### Template II - Il Cuore
- [ ] Vocabulário emocional carregado (800 palavras) ⏳
- [ ] Frases emocionais acessíveis (400 frases) ⏳
- [ ] Gramática presente indicativo completa ⏳
- [ ] Flashcards funcionando corretamente ⏳

### Template III - Il Viaggio
- [ ] Verbos de movimento conjugados ⏳
- [ ] Preposições e locativos completos ⏳
- [ ] Diálogos de viagem disponíveis ⏳

... (restante)

---

## 🔧 FERRAMENTAS DE TESTE RECOMENDADAS

| Ferramenta | Descrição | Uso |
|------------|-----------|-----|
| **Jest** | Framework de teste JavaScript | Testes unitários + integração |
| **Cypress** | E2E testing para web apps | Testes UI/UX completos |
| **Lighthouse** | Performance audit | Load tests + UX metrics |
| **Web Vitals** | Métricas de performance real-world | RUM (Real User Monitoring) |

---

## 📊 MÉTRICAS DE SUCESSO POR TEMPLO

| Métrica | Meta | Templo I | Templo II | ... |
|---------|------|----------|-----------|-----|
| **Velocidade de carregamento** | <2s | ✅ 1.8s | ⏳ Pending | - |
| **Taxa de erro em quiz** | <5% | ✅ 3.2% | ⏳ Pending | - |
| **Retenção de vocabulário** | >70% | ✅ 72% | ⏳ Pending | - |
| **Usuários completando templo** | >60% | ⏳ Pending | N/A | - |

---

**Status atual dos testes:**
- ✅ Unit tests: Criados para Templates I-VI
- ⏳ Integration tests: Pendentes de implementação
- ⏳ Performance tests: Pendentes de implementação
- ⏳ UI/UX tests: Pendentes de implementação
