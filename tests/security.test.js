import { describe, it, expect } from 'vitest';
import crypto from 'crypto';

describe('Fase 1 — Segurança e Integridade', () => {
  describe('SEC-01: Verificação de Hash Criptográfico para Desbloqueio', () => {
    const UNLOCK_HASH = '4b9a7f50c0bb198c6f5414c5a8459f5d216d34ab521ea94c060ea35cac66f900';

    async function verificarCodigo(codigo) {
      if (!codigo || typeof codigo !== 'string') return false;
      const hash = crypto.createHash('sha256').update(codigo.trim()).digest('hex');
      return hash === UNLOCK_HASH;
    }

    it('deve aceitar a chave correta via SHA-256', async () => {
      const ok = await verificarCodigo('2012');
      expect(ok).toBe(true);
    });

    it('deve rejeitar chaves incorretas', async () => {
      expect(await verificarCodigo('1234')).toBe(false);
      expect(await verificarCodigo('admin')).toBe(false);
      expect(await verificarCodigo('')).toBe(false);
      expect(await verificarCodigo(null)).toBe(false);
    });
  });

  describe('SEC-02: Sanitização XSS e Escape de Strings', () => {
    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function sanitizarString(str) {
      if (typeof str !== 'string') return '';
      return str.replace(/<[^>]*>?/gm, '').trim();
    }

    it('deve neutralizar tags script perigosas via escapeHtml', () => {
      const payload = '<script>alert("xss")</script>';
      const escaped = escapeHtml(payload);
      expect(escaped).not.toContain('<script>');
      expect(escaped).toBe('&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;');
    });

    it('deve remover tags HTML em sanitizarString', () => {
      const payload = '<img src=x onerror=alert(1)>Texto Legítimo';
      const clean = sanitizarString(payload);
      expect(clean).toBe('Texto Legítimo');
      expect(clean).not.toContain('<img');
      expect(clean).not.toContain('onerror');
    });

    it('deve neutralizar injeção de atributos e aspas', () => {
      const payload = '" onmouseover="alert(1)';
      const escaped = escapeHtml(payload);
      expect(escaped).toBe('&quot; onmouseover=&quot;alert(1)');
    });
  });

  describe('SEC-04: Validação de Schemas de Importação IA', () => {
    function validarDialogo(data) {
      const arr = Array.isArray(data) ? data : [data];
      if (arr.length === 0) throw new Error('Nenhum diálogo encontrado.');
      for (let i = 0; i < arr.length; i++) {
        const item = arr[i];
        if (!item.titulo || typeof item.titulo !== 'string') {
          throw new Error(`Diálogo #${i + 1} sem campo "titulo".`);
        }
        if (!Array.isArray(item.turnos) || item.turnos.length === 0) {
          throw new Error(`Diálogo "${item.titulo}" deve conter lista de "turnos".`);
        }
      }
      return arr;
    }

    it('deve aprovar diálogo com estrutura completa', () => {
      const valido = {
        titulo: 'Al bar',
        nivel: 'A1',
        turnos: [
          { falante: 'Barista', frase: 'Buongiorno! Cosa desidera?', traducao: 'Bom dia! O que deseja?' },
          { falante: 'Cliente', frase: 'Un caffè per favore.', traducao: 'Um café por favor.' }
        ]
      };
      expect(() => validarDialogo(valido)).not.toThrow();
    });

    it('deve rejeitar payload malformado sem título ou turnos', () => {
      expect(() => validarDialogo({ nivel: 'A1' })).toThrow(/sem campo "titulo"/);
      expect(() => validarDialogo({ titulo: 'Sem turnos', turnos: [] })).toThrow(/deve conter lista de "turnos"/);
      expect(() => validarDialogo([])).toThrow(/Nenhum diálogo/);
    });
  });
});
