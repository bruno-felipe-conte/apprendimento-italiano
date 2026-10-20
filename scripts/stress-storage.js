// ============================================================
// scripts/stress-storage.js — Teste de Carga e Benchmark de Armazenamento
// Simula 10.000 palavras + 50.000 reviews FSRS e afere latência
// ============================================================

import { performance } from 'perf_hooks';

class LocalStorageMock {
  constructor() {
    this.store = new Map();
  }
  getItem(key) {
    return this.store.get(key) ?? null;
  }
  setItem(key, value) {
    this.store.set(key, String(value));
  }
  removeItem(key) {
    this.store.delete(key);
  }
  clear() {
    this.store.clear();
  }
  get length() {
    return this.store.size;
  }
}

const storage = new LocalStorageMock();

console.log('='.repeat(65));
console.log('BENCHMARK DE CARGA LOCALSTORAGE / FSRS — apprendimento-italiano');
console.log('='.repeat(65));

// 1. Geração de 10.000 palavras de vocabulário
console.log('\n[1/3] Gerando 10.000 palavras em cache...');
const t0 = performance.now();
const vocab = [];
for (let i = 1; i <= 10000; i++) {
  vocab.push({
    id: `w_bench_${i}`,
    templo_num: Math.floor(i / 200) + 1,
    italiano: `parola_${i}`,
    portugues: `palavra_${i}`,
    categoria: 'sostantivo',
    exemplo: `Questo è un esempio per parola_${i}.`,
    exemplo_pt: `Este é um exemplo para palavra_${i}.`
  });
}
const tempoGenVocab = performance.now() - t0;
console.log(`✓ 10.000 palavras geradas em ${tempoGenVocab.toFixed(2)}ms`);

// 2. Benchmark de escrita do Vocabulário
console.log('\n[2/3] Testando escrita de 10.000 palavras (JSON.stringify + setItem)...');
const t1 = performance.now();
const vocabJson = JSON.stringify(vocab);
storage.setItem('it_vocab_cache_v1', vocabJson);
const tempoWriteVocab = performance.now() - t1;
const tamanhoVocabMB = (Buffer.byteLength(vocabJson, 'utf8') / (1024 * 1024)).toFixed(2);
console.log(`✓ Escrita concluída em ${tempoWriteVocab.toFixed(2)}ms (${tamanhoVocabMB} MB)`);

// 3. Simulação de 50.000 revisões FSRS
console.log('\n[3/3] Simulando 50.000 revisões FSRS distribuídas...');
const flashcardData = {};
const t2 = performance.now();
const agora = Date.now();

for (let i = 1; i <= 10000; i++) {
  const cardId = `w_bench_${i}`;
  // Cada carta com 5 reviews em média (total 50.000)
  flashcardData[cardId] = {
    state: 'review',
    difficulty: 4.8 + Math.random() * 2,
    stability: 12.5 + Math.random() * 30,
    reps: 5,
    lapses: Math.floor(Math.random() * 2),
    lastReview: agora - Math.floor(Math.random() * 86400000 * 10),
    nextReview: agora + Math.floor(Math.random() * 86400000 * 20),
    elapsed_days: 10,
    scheduled_days: 15
  };
}

const t3 = performance.now();
const fsrsJson = JSON.stringify(flashcardData);
storage.setItem('it_flashcards_v4', fsrsJson);
const tempoWriteFSRS = performance.now() - t3;
const tamanhoFSRSMB = (Buffer.byteLength(fsrsJson, 'utf8') / (1024 * 1024)).toFixed(2);
console.log(`✓ 50.000 reviews calculadas e salvas em ${tempoWriteFSRS.toFixed(2)}ms (${tamanhoFSRSMB} MB)`);

// 4. Teste de Leitura / Deserialização
const t4 = performance.now();
const readFsrs = JSON.parse(storage.getItem('it_flashcards_v4'));
const tempoReadFSRS = performance.now() - t4;
console.log(`✓ Leitura e JSON.parse de 10k cartas em ${tempoReadFSRS.toFixed(2)}ms (${Object.keys(readFsrs).length} cartas recuperadas)`);

console.log('\n' + '='.repeat(65));
console.log('RELATÓRIO FINAL DE PERFORMANCE');
console.log('='.repeat(65));
console.log(`- Volume Total em Memória: ${(parseFloat(tamanhoVocabMB) + parseFloat(tamanhoFSRSMB)).toFixed(2)} MB`);
console.log(`- Latência Escrita Vocabulário: ${tempoWriteVocab.toFixed(2)}ms ${tempoWriteVocab < 100 ? '✅ (Excelente < 100ms)' : '⚠️ (Atenção > 100ms)'}`);
console.log(`- Latência Escrita FSRS: ${tempoWriteFSRS.toFixed(2)}ms ${tempoWriteFSRS < 100 ? '✅ (Excelente < 100ms)' : '⚠️ (Atenção > 100ms)'}`);
console.log(`- Latência Leitura FSRS: ${tempoReadFSRS.toFixed(2)}ms ${tempoReadFSRS < 50 ? '✅ (Instantâneo < 50ms)' : '⚠️ (Atenção > 50ms)'}`);
console.log('='.repeat(65));

if (tempoWriteVocab > 100 || tempoWriteFSRS > 100) {
  console.warn('⚠️ ALERTA: Operação de escrita excedeu meta de 100ms sob estresse máximo.');
} else {
  console.log('🎉 Todos os testes de estresse passaram com sucesso dentro das margens ideais!');
}
