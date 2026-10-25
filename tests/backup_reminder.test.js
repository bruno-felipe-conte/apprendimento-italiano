// @vitest-environment happy-dom
import { describe, it, expect, beforeEach, vi } from 'vitest';
import '../js/core/backup_reminder.js';

const BackupReminder = globalThis.BackupReminder;

describe('BackupReminder: Lembrete Periódico e Configurações de Backup', () => {
  beforeEach(() => {
    localStorage.clear();
    document.body.innerHTML = '';
    vi.restoreAllMocks();
  });

  it('deve retornar true em deveExibir() se nunca foi exibido antes', () => {
    expect(BackupReminder.deveExibir()).toBe(true);
  });

  it('deve retornar false em deveExibir() se foi exibido há menos de 3 dias', () => {
    const agora = Date.now();
    // 1 dia atrás
    localStorage.setItem(BackupReminder.CHAVE_STORAGE, (agora - 24 * 60 * 60 * 1000).toString());
    expect(BackupReminder.deveExibir()).toBe(false);

    // 2 dias e 23 horas atrás
    localStorage.setItem(BackupReminder.CHAVE_STORAGE, (agora - (3 * 24 * 60 * 60 * 1000 - 60000)).toString());
    expect(BackupReminder.deveExibir()).toBe(false);
  });

  it('deve retornar true em deveExibir() se já se passaram 3 dias ou mais', () => {
    const agora = Date.now();
    // Exatamente 3 dias atrás
    localStorage.setItem(BackupReminder.CHAVE_STORAGE, (agora - 3 * 24 * 60 * 60 * 1000).toString());
    expect(BackupReminder.deveExibir()).toBe(true);

    // 5 dias atrás
    localStorage.setItem(BackupReminder.CHAVE_STORAGE, (agora - 5 * 24 * 60 * 60 * 1000).toString());
    expect(BackupReminder.deveExibir()).toBe(true);
  });

  it('deve registrar timestamp atual ao chamar registrarExibicao()', () => {
    const antes = Date.now();
    BackupReminder.registrarExibicao();
    const salvo = parseInt(localStorage.getItem(BackupReminder.CHAVE_STORAGE), 10);
    expect(salvo).toBeGreaterThanOrEqual(antes);
    expect(salvo).toBeLessThanOrEqual(Date.now() + 1000);
  });

  it('deve renderizar o popup com atributos de acessibilidade e botão de ação', () => {
    BackupReminder.exibir();
    const popup = document.getElementById('backup-reminder-popup');
    expect(popup).not.toBeNull();
    expect(popup.getAttribute('role')).toBe('alert');
    expect(popup.getAttribute('aria-live')).toBe('polite');

    const btnAcao = document.getElementById('backup-popup-action-btn');
    expect(btnAcao).not.toBeNull();

    const btnFechar = document.getElementById('backup-popup-close-btn');
    expect(btnFechar).not.toBeNull();

    const progress = document.getElementById('backup-popup-progress-bar');
    expect(progress).not.toBeNull();
  });

  it('deve fechar e remover o popup do DOM', () => {
    BackupReminder.exibir();
    expect(document.getElementById('backup-reminder-popup')).not.toBeNull();

    BackupReminder.fechar(false);
    expect(document.getElementById('backup-reminder-popup')).toBeNull();
  });
});
