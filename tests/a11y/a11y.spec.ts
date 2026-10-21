import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('HAR-05: Auditoria de Acessibilidade com @axe-core (WCAG 2.1 AA)', () => {
  test.beforeEach(async ({ context }) => {
    // Evita recarregamentos causados pelo ciclo de vida do Service Worker durante os testes
    await context.route('**/sw.js', (route) => route.abort());

    // Desativa animações e transições CSS para evitar artefatos de opacidade/cor transitória
    await context.addInitScript(() => {
      try {
        localStorage.setItem('it_onboarding_done', 'true');
      } catch (_) {}

      const injectStyle = () => {
        const id = 'axe-disable-animations';
        if (document.getElementById(id)) return;
        const style = document.createElement('style');
        style.id = id;
        style.innerHTML = `
          *, *::before, *::after {
            animation: none !important;
            transition: none !important;
          }
        `;
        if (document.head) {
          document.head.appendChild(style);
        } else {
          document.documentElement.appendChild(style);
        }
      };
      injectStyle();
      document.addEventListener('DOMContentLoaded', injectStyle);
    });
  });

  test('Página Inicial (Landing/Templos) deve estar livre de violações críticas/sérias de acessibilidade', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    const criticalOrSerious = accessibilityScanResults.violations.filter(
      (v) => v.impact === 'critical' || v.impact === 'serious'
    );

    expect(criticalOrSerious, JSON.stringify(criticalOrSerious, null, 2)).toEqual([]);
  });

  test('Modo Escuro (Dark Mode) deve manter contraste e conformidade WCAG 2.1 AA', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    // Alterna tema clicando no toggle de forma robusta
    await page.evaluate(() => {
      const toggle = document.getElementById('theme-toggle');
      if (toggle) toggle.click();
      else if ((window as any).App?.alternarTema) (window as any).App.alternarTema();
    });
    await page.waitForTimeout(650);

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    const criticalOrSerious = accessibilityScanResults.violations.filter(
      (v) => v.impact === 'critical' || v.impact === 'serious'
    );

    expect(criticalOrSerious, JSON.stringify(criticalOrSerious, null, 2)).toEqual([]);
  });

  test('Todas as 9 seções principais devem estar acessíveis ao navegar', async ({ page }) => {
    test.setTimeout(90000);
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    const secoes = [
      'flashcard',
      'quiz',
      'vocabolario',
      'grammatica',
      'storie',
      'dialoghi',
      'canzoni',
      'imitazione',
      'profilo',
    ];

    for (const sec of secoes) {
      await page.evaluate((s) => {
        const app = (window as any).App;
        if (app && typeof app.navegar === 'function') {
          app.navegar(s);
        }
      }, sec);

      await page.waitForTimeout(350);

      const scanResults = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
        .analyze();

      const criticalOrSerious = scanResults.violations.filter(
        (v) => v.impact === 'critical' || v.impact === 'serious'
      );

      expect(
        criticalOrSerious,
        `Violação detectada na seção ${sec}: ${JSON.stringify(criticalOrSerious, null, 2)}`
      ).toEqual([]);
    }
  });

  test('Modais interativos devem conter roles, atributos ARIA e foco acessível', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    // 1. Testa Meta Settings Modal
    await page.evaluate(() => {
      const app = (window as any).App;
      if (app && typeof app.abrirMetaSettings === 'function') app.abrirMetaSettings();
    });
    await page.waitForTimeout(200);

    let scan = await new AxeBuilder({ page })
      .include('#meta-settings-modal')
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    let criticalOrSerious = scan.violations.filter((v) => v.impact === 'critical' || v.impact === 'serious');
    expect(criticalOrSerious, 'Meta Settings Modal').toEqual([]);

    await page.evaluate(() => {
      const app = (window as any).App;
      if (app && typeof app.fecharMetaSettings === 'function') app.fecharMetaSettings();
    });

    // 2. Testa IA Import Modal
    await page.evaluate(() => {
      const ia = (window as any).IAImport;
      if (ia && typeof ia.abrir === 'function') ia.abrir('vocab');
    });
    await page.waitForTimeout(200);

    scan = await new AxeBuilder({ page })
      .include('#ia-import-modal')
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    criticalOrSerious = scan.violations.filter((v) => v.impact === 'critical' || v.impact === 'serious');
    expect(criticalOrSerious, 'IA Import Modal').toEqual([]);

    await page.evaluate(() => {
      const ia = (window as any).IAImport;
      if (ia && typeof ia.fechar === 'function') ia.fechar();
    });

    // 3. Testa Modal de Meta com Prazo
    await page.evaluate(() => {
      const app = (window as any).App;
      if (app && typeof app.abrirModalMetaPrazo === 'function') app.abrirModalMetaPrazo();
    });
    await page.waitForTimeout(200);

    scan = await new AxeBuilder({ page })
      .include('#modal-meta-prazo')
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    criticalOrSerious = scan.violations.filter((v) => v.impact === 'critical' || v.impact === 'serious');
    expect(criticalOrSerious, 'Modal Meta Prazo').toEqual([]);
  });
});
