/**
 * E2E — TASK-009b: mosaicos T1–T4 (página Por Tema)
 */
const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const SHOTS = path.join(__dirname, '../../docs/06-validation/screenshots');

const SLIDES = [
  { index: 0, pattern: 'C', slice: 'all', title: /Plataformas/i },
  { index: 1, pattern: 'A', slice: 'eleicao', title: /Eleic/i },
  { index: 2, pattern: 'A', slice: 'vacinas', title: /Vacinas/i },
  { index: 3, pattern: 'D', slice: 'uf_region', title: /geograf/i },
];

test.describe('TASK-009b mosaicos Por Tema', () => {
  test.beforeAll(() => fs.mkdirSync(SHOTS, { recursive: true }));

  test('T1–T4: padroes C/A/A/D, KPIs e embeds', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 720 });
    await page.goto('/por-tema/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('.dsn-dashboard', { timeout: 30000 });

    const slides = page.locator('.dsn-slide');
    await expect(slides).toHaveCount(4);

    for (const spec of SLIDES) {
      if (spec.index > 0) {
        await page.locator('.swiper-button-next').click();
        await page.waitForTimeout(400);
      }

      const active = page.locator('.swiper-slide-active');
      await expect(active).toHaveClass(/dsn-slide--mosaic/);
      const mosaic = active.locator('.dsn-mosaic');
      await expect(mosaic).toHaveAttribute('data-mosaic-pattern', spec.pattern);
      await expect(mosaic).toHaveAttribute('data-slice-value', spec.slice);
      await expect(active.locator('.dsn-kpi')).toHaveCount(4);
      await expect(active.locator('.dsn-embed-iframe')).toHaveCount(1);
      await expect(active.locator('.dsn-mosaic__title')).toHaveText(spec.title);

      await page.waitForTimeout(5000);
      await page.screenshot({
        path: path.join(SHOTS, `mosaic-tema-t${spec.index + 1}-${spec.pattern}-1280x720.png`),
        fullPage: false,
      });
    }

    const scroll = await page.evaluate(() => {
      const dash = document.querySelector('.dsn-dashboard');
      return dash ? getComputedStyle(dash).overflow : null;
    });
    expect(scroll === 'hidden' || scroll === 'clip').toBeTruthy();
  });
});
