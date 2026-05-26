/**
 * VocabularioService - Carrega e gerencia dados do JSON dinamicamente
 */

class VocabularyService {
  constructor() {
    this.dataPath = 'data/templo-1.json';
    this.storageKey = 'vocabolo-desbloqueado';
    this.defaultData = []; // Cache para evitar recarregar a cada render
    this.loadPromise = null; // Promise singleton para load async
  }

  /**
   * Carrega o JSON de vocabulario dinamicamente (lazy load)
   */
  async carregarJSON() {
    if (this.loadPromise) return this.loadPromise;

    try {
      const response = await fetch(this.dataPath);
      if (!response.ok) throw new Error(`HTTP ${response.status}: Failed to load ${this.dataPath}`);

      const data = await response.json();
      this.defaultData = data; // Cache dos dados completos
      console.log(`[VocabularyService] Carregou ${data.length} palavras de ${this.dataPath}`);

      this.loadPromise = null;
      return data;
    } catch (error) {
      console.error('[VocabularyService]', error.message);
      // Fallback: carregar do localStorage se JSON não estiver disponível
      const cached = localStorage.getItem(this.storageKey);
      if (cached) {
        console.warn('[VocabularyService] JSON indisponível, usando cache:', cached);
        return JSON.parse(cached);
      }
      throw error;
    }
  }

  /**
   * Retorna todas as palavras (pelo menos uma vez assincrona)
   */
  async getTodasAsPalavras() {
    await this.carregarJSON(); // Lazy load
    return [...this.defaultData];
  }

  /**
   * Persiste array de palavras no localStorage
   */
  persistirPalavras(palavras) {
    const data = Array.isArray(palavras) ? palavras : palavras.data;
    if (!Array.isArray(data)) throw new Error('palavras não é array ou não tem .data');

    try {
      localStorage.setItem(this.storageKey, JSON.stringify(data));
      console.log(`[VocabularyService] Persistiu ${data.length} palavras`);
      return true;
    } catch (e) {
      if (/Quota/.test(e.name)) {
        console.warn('[VocabularyService]', 'localStorage full. Usando array em memória.');
        this.defaultData = data;
      } else throw e;
    }
  }

  /**
   * Garbage collector para limpar localStorage antigo (opcional)
   */
  limparLocalStorage() {
    if (typeof localStorage !== 'undefined') localStorage.removeItem(this.storageKey);
  }

  /**
   * Valida estrutura de palavra
   */
  validarPalavra(palavra) {
    const obrigatorio = ['id', 'italiano', 'portugues'];
    return obrigatorio.every(campo => campo in palavra) && !!palavra.italiano.trim();
  }

  /**
   * Retorna palavras filtradas por categoria (ex: 'saudacoes', 'verbos')
   */
  async filtrarPorCategoria(categoria) {
    const todas = await this.getTodasAsPalavras();
    return todas.filter(p => p.categoria === categoria);
  }

  /**
   * Retorna palavras por nível de dificuldade (facil, medio, dificil)
   */
  async filtrarPorDificuldade(dificuldade) {
    const todas = await this.getTodasAsPalavras();
    return todas.filter(p => p.dificuldade === dificuldade);
  }

  /**
   * Retorna palavras randomicas (número máximo de n, ou todas se null)
   */
  async obterAleatorias(n = 10) {
    const todas = await this.getTodasAsPalavras();
    return [...todas].sort(() => 0.5 - Math.random()).slice(0, n);
  }

  /**
   * Retorna palavras por categoria específica (ex: 'familia', 'numeros')
   */
  async obterPorCategoria(categoria) {
    const todas = await this.getTodasAsPalavras();
    return todas.filter(p => p.categoria === categoria);
  }

  /**
   * Exemplo de uso em main.js:
   * 
   * const vocabService = new VocabularyService();
   * const palavras = await vocabService.carregarJSON(); // Lazy load
   * App.vocabularyDB = new Map(palavras.map(p => [p.id, p]));
   * App.renderizarGrid();
   */
}

// Exemplo de uso (opcional - remover se não usado):
/*
window.onload = async () => {
  const vocabService = new VocabularyService();
  await vocabService.carregarJSON();
  
  // Persistir as palavras carregadas do JSON
  try {
    vocabService.persistirPalavras(vocabService.defaultData);
  } catch (e) {
    console.warn('[VocabularyService]', 'Não persistiu ao localStorage:', e.message);
  }
};
*/
