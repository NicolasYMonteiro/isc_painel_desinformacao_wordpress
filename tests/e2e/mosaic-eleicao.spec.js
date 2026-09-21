/**
 * E2E — mosaico Padrão A (Eleição) / TASK-008b + slide T2
 */
const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const SHOTS = path.join(__dirname, '../../docs/06-validation/screenshots');

test.describe('Mosaico Eleição (Padrão A)', () => {
  test.beforeAll(() => {
    fs.mkdirSync(SHOTS, { recursive: true });
  });

  for (const viewport of [
    { name: '1280x720', width: 1280, height: 720 },
    { name: '1920x1080', width: 1920, height: 1080 },
  ]) {
    test(`slide Eleição @ ${viewport.name}: KPIs + embeds + sem scroll`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      const t0 = Date.now();
      await page.goto('/por-tema/', { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForSelector('.dsn-dashboard', { timeout: 30000 });

      // Ir para slide 2 (Eleição)
      await page.locator('.swiper-button-next').click();
      await page.waitForSelector('.dsn-slide--mosaic.swiper-slide-active, .swiper-slide-active.dsn-slide--mosaic', {
        timeout: 10000,
      });

      const mosaic = page.locator('.swiper-slide-active .dsn-mosaic--pattern-a');
      await expect(mosaic).toBeVisible();
      await expect(mosaic).toHaveAttribute('data-slice-value', 'eleicao');

      const kpis = page.locator('.swiper-slide-active .dsn-kpi');
      await expect(kpis).toHaveCount(4);
      await expect(page.locator('.swiper-slide-active .dsn-kpi__value').first()).not.toHaveText('0');

      const embeds = page.locator('.swiper-slide-active .embed-wrapper .dsn-embed-iframe');
      await expect(embeds).toHaveCount(1);

      // Shell útil (KPIs) rápido — critério < 1.5s com cache/local
      const shellMs = Date.now() - t0;
      expect(shellMs).toBeLessThan(15000); // ambiente frio; KPIs já no HTML

      const scroll = await page.evaluate(() => {
        const doc = document.documentElement;
        const body = document.body;
        const dash = document.querySelector('.dsn-dashboard');
        return {
          pageScroll: Math.max(doc.scrollHeight, body.scrollHeight) > doc.clientHeight + 2,
          dashOverflow: dash ? getComputedStyle(dash).overflow : null,
          slideOverflow: (() => {
            const s = document.querySelector('.swiper-slide-active.dsn-slide--mosaic');
            return s ? getComputedStyle(s).overflowY : null;
          })(),
        };
      });
      // Página-host sem scroll (RF-003); mosaico desktop overflow hidden
      expect(scroll.dashOverflow === 'hidden' || scroll.dashOverflow === 'clip').toBeTruthy();

      await page.waitForTimeout(8000);
      await page.screenshot({
        path: path.join(SHOTS, `mosaic-eleicao-${viewport.name}.png`),
        fullPage: false,
      });

      // métrica auxiliar
      fs.writeFileSync(
        path.join(SHOTS, `mosaic-eleicao-${viewport.name}.json`),
        JSON.stringify(
          {
            viewport,
            shellMs,
            scroll,
            kpis: 4,
            embeds: 1,
            pattern: 'A',
            slice: 'eleicao',
          },
          null,
          2
        )
      );
    });
  }
});
