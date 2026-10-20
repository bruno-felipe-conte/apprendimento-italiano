// @vitest-environment happy-dom
import { describe, it, expect, beforeEach } from 'vitest';
import VoiceEngine from '../js/voice_engine';

describe('ARC-03: Motor de Voz e Prosódia em TypeScript (VoiceEngine)', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('deve normalizar texto italiano removendo elisões incorretas e colchetes', () => {
    const raw = "l' amico [l-a-mi-co] parla subito (ele fala logo)";
    const norm = VoiceEngine.normalizarParaFala(raw);
    expect(norm).toContain("l'amico");
    expect(norm).not.toContain('[');
    expect(norm).not.toContain('(');
  });

  it('deve aplicar acentuação tônica do léxico fonético sdrucciolo', () => {
    const texto = 'parlano subito e telefonano';
    const fonico = VoiceEngine.aplicarLexicoFonico(texto);
    expect(fonico).toContain('pàrlano');
    expect(fonico).toContain('sùbito');
    expect(fonico).toContain('telèfonano');
  });

  it('deve dividir sentenças respeitando honoríficos italianos (Dott., Sig., etc.)', () => {
    const texto = 'Il Dott. Rossi è arrivato. Ha salutato la Sig.ra Bianchi.';
    const sentencas = VoiceEngine.dividirEmSentencas(texto);
    expect(sentencas.length).toBe(2);
    expect(sentencas[0]).toContain('Dott. Rossi');
    expect(sentencas[1]).toContain('Sig.ra Bianchi');
  });

  it('deve ranquear e priorizar vozes neurais/naturais sobre vozes sintéticas comuns', () => {
    const vozesFalsas: any[] = [
      { name: 'Microsoft Desktop Italian', lang: 'it-IT' },
      { name: 'Microsoft Elsa Online (Natural) - Italian', lang: 'it-IT' },
      { name: 'Generic Italian', lang: 'it-IT' }
    ];

    window.speechSynthesis = {
      getVoices: () => vozesFalsas
    } as any;

    VoiceEngine._cacheVozes = null;
    const selecionada = VoiceEngine.obterVozSelecionada();
    expect(selecionada?.name).toContain('Natural');
  });
});
