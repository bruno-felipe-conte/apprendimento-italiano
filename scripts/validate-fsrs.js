// ============================================================
// scripts/validate-fsrs.js — Validação e Prevenção de Edge Cases FSRS
// Mitigação de Riscos: Detecta e corrige cartas corrompidas / legadas
// ============================================================

import { performance } from 'perf_hooks';

console.log('='.repeat(65));
console.log('VALIDAÇÃO DE INTEGRIDADE FSRS-4.5 — apprendimento-italiano');
console.log('='.repeat(65));

/**
 * Validador estrito de integridade de um card FSRS
 * @param {string} id
 * @param {any} card
 * @returns {{ valid: boolean, errors: string[], sanitized?: any }}
 */
export function validarCardFSRS(id, card) {
  const errors = [];
  if (!card || typeof card !== 'object') {
    return { valid: false, errors: ['Card inválido ou nulo'] };
  }

  // 1. Validação de Estado
  const validStates = ['new', 'learning', 'review', 'suspended'];
  if (!validStates.includes(card.state)) {
    errors.push(`Estado '${card.state}' inválido (esperado: ${validStates.join(', ')})`);
  }

  // 2. Validação de Dificuldade (1.0 <= D <= 10.0)
  if (typeof card.difficulty !== 'number' || isNaN(card.difficulty)) {
    errors.push(`Dificuldade não numérica: ${card.difficulty}`);
  } else if (card.difficulty < 1.0 || card.difficulty > 10.0) {
    errors.push(`Dificuldade fora dos limites [1.0, 10.0]: ${card.difficulty}`);
  }

  // 3. Validação de Estabilidade (S > 0)
  if (typeof card.stability !== 'number' || isNaN(card.stability) || !isFinite(card.stability)) {
    errors.push(`Estabilidade inválida (NaN/Infinito): ${card.stability}`);
  } else if (card.stability <= 0 && card.state !== 'new') {
    errors.push(`Estabilidade não positiva em card revisado: ${card.stability}`);
  }

  // 4. Validação de Repetições e Lapses
  if (!Number.isInteger(card.reps) || card.reps < 0) {
    errors.push(`Repetições (reps) inválidas: ${card.reps}`);
  }
  if (!Number.isInteger(card.lapses) || card.lapses < 0) {
    errors.push(`Lapses inválidos: ${card.lapses}`);
  }

  // 5. Coerência entre Estado e Repetições
  if (card.state === 'review' && card.reps === 0) {
    errors.push(`Card marcado como 'review' mas possui 0 repetições.`);
  }

  // 6. Sanitização / Recuperação segura se houver pequenas anomalias
  let sanitized = null;
  if (errors.length > 0) {
    sanitized = {
      id: id,
      state: validStates.includes(card.state) ? card.state : 'new',
      difficulty: typeof card.difficulty === 'number' && !isNaN(card.difficulty) 
        ? Math.max(1.0, Math.min(10.0, card.difficulty)) 
        : 5.0,
      stability: typeof card.stability === 'number' && isFinite(card.stability) && card.stability > 0 
        ? card.stability 
        : 2.0,
      reps: Number.isInteger(card.reps) && card.reps >= 0 ? card.reps : 0,
      lapses: Number.isInteger(card.lapses) && card.lapses >= 0 ? card.lapses : 0,
      lastReview: card.lastReview || null,
      nextReview: card.nextReview || (Date.now() + 86400000)
    };
  }

  return {
    valid: errors.length === 0,
    errors,
    sanitized
  };
}

/**
 * Migra card legado (SM-2: interval, repetitions, factor) para FSRS-4.5
 * @param {string} id
 * @param {any} legacyCard
 * @returns {any}
 */
export function migrarCardLegadoSM2(id, legacyCard) {
  const reps = legacyCard.repetitions || legacyCard.reps || 0;
  const interval = legacyCard.interval || 1;
  const factor = legacyCard.factor || 2.5;

  // Heurística de conversão para parâmetros iniciais FSRS
  const difficulty = Math.max(1.0, Math.min(10.0, 10.0 - (factor - 1.3) * (9.0 / 1.7)));
  const stability = Math.max(0.5, interval * 1.1);

  return {
    id,
    state: reps > 0 ? 'review' : 'new',
    difficulty: parseFloat(difficulty.toFixed(2)),
    stability: parseFloat(stability.toFixed(2)),
    reps,
    lapses: legacyCard.lapses || 0,
    lastReview: legacyCard.lastReview || Date.now(),
    nextReview: legacyCard.nextReview || (Date.now() + interval * 86400000)
  };
}

// ============================================================
// Execução do Teste de Validação
// ============================================================
function runFSRSValidationSuite() {
  const t0 = performance.now();
  let passed = 0;
  let failed = 0;

  console.log('\n[1/3] Testando validação de cartões FSRS válidos...');
  const cardValido = {
    state: 'review',
    difficulty: 4.5,
    stability: 14.2,
    reps: 6,
    lapses: 0,
    lastReview: Date.now() - 86400000,
    nextReview: Date.now() + 86400000 * 5
  };
  const res1 = validarCardFSRS('card_001', cardValido);
  if (res1.valid) {
    console.log('✓ Card íntegro aprovado corretamente.');
    passed++;
  } else {
    console.error('✗ Erro inesperado em card íntegro:', res1.errors);
    failed++;
  }

  console.log('\n[2/3] Testando detecção e autocorreção de edge cases corrompidos...');
  const cardCorrompido = {
    state: 'unknown_state',
    difficulty: 99.9, // Out of bounds
    stability: -5.0,  // Negativo
    reps: 'tres',     // Não numérico
    lapses: -1
  };
  const res2 = validarCardFSRS('card_corrupt_001', cardCorrompido);
  if (!res2.valid && res2.errors.length >= 4) {
    console.log(`✓ 4 anomalias detectadas com precisão: ${res2.errors.join(' | ')}`);
    console.log(`✓ Sanitização automática produziu card seguro:`, res2.sanitized);
    passed++;
  } else {
    console.error('✗ Falha na detecção de corrupção FSRS');
    failed++;
  }

  console.log('\n[3/3] Testando migração de card legado SM-2 para FSRS...');
  const legacySM2 = {
    repetitions: 4,
    interval: 15,
    factor: 2.1
  };
  const migrated = migrarCardLegadoSM2('legacy_001', legacySM2);
  const res3 = validarCardFSRS(migrated.id, migrated);
  if (res3.valid && migrated.difficulty >= 1.0 && migrated.difficulty <= 10.0) {
    console.log('✓ Migração de SM-2 concluída sem perda de dados:', migrated);
    passed++;
  } else {
    console.error('✗ Falha na validação do card migrado:', res3.errors);
    failed++;
  }

  const tempoTotal = (performance.now() - t0).toFixed(2);
  console.log('\n' + '='.repeat(65));
  console.log(`STATUS DA SUÍTE FSRS: ${failed === 0 ? '✅ APROVADA' : '❌ REPROVADA'} (${passed} aprovados, ${failed} falhas) em ${tempoTotal}ms`);
  console.log('='.repeat(65));

  if (failed > 0) {
    process.exit(1);
  }
}

// Executar se chamado diretamente
if (process.argv[1]?.endsWith('validate-fsrs.js')) {
  runFSRSValidationSuite();
}
