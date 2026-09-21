/**
 * E2E — TASK-010b mosaicos Por Plataforma + BUG-001 sem scroll
 */
const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const SHOTS = path.join(__dirname, '../../docs/06-validation/screenshots');

const SLIDES = [
  { index: 0, pattern: 'C', slice: 'platform_angle' },
  { index: 1, pattern: 'B', slice: 'WhatsApp' },
  { index: 2, pattern: 'B', slice: 'YouTube' },
  { index: 3, pattern: 'B', slice: 'Facebook' },
];

test.describe('TASK-010b + BUG-001', () => {
  test.beforeAll(() => fs.mkdirSync(SHOTS, { recursive: true }));

  test('Por Plataforma P1–P4 mosaicos C/B/B/B', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 720 });
    await page.goto('/por-plataforma/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('.dsn-dashboard', { timeout: 30000 });

    await expect(page.locator('.dsn-slide')).toHaveCount(4);

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
      await page.waitForTimeout(4000);
      await page.screenshot({
        path: path.join(SHOTS, `mosaic-plat-p${spec.index + 1}-${spec.pattern}-1280x720.png`),
        fullPage: false,
      });
    }
  });

  test('BUG-001: sem scroll de pagina em 1280x720 e 1920x1080', async ({ page }) => {
    for (const vp of [
      { w: 1280, h: 720 },
      { w: 1920, h: 1080 },
    ]) {
      await page.setViewportSize({ width: vp.w, height: vp.h });
      await page.goto('/por-tema/', { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForSelector('.dsn-dashboard', { timeout: 30000 });
      await page.waitForTimeout(1000);

      const metrics = await page.evaluate(() => {
        const doc = document.documentElement;
        const body = document.body;
        const dash = document.querySelector('.dsn-dashboard');
        return {
          hasScroll: Math.max(doc.scrollHeight, body.scrollHeight) > doc.clientHeight + 2,
          bodyFixed: getComputedStyle(body).position === 'fixed',
          bodyOverflow: getComputedStyle(body).overflow,
          dashFixed: dash ? getComputedStyle(dash).position === 'fixed' : false,
          headerHidden: (() => {
            const h = document.querySelector('header, .wp-block-template-part');
            if (!h) return true;
            return getComputedStyle(h).display === 'none';
          })(),
        };
      });

      expect(metrics.bodyFixed).toBeTruthy();
      expect(metrics.dashFixed).toBeTruthy();
      expect(metrics.hasScroll).toBeFalsy();

      fs.writeFileSync(
        path.join(SHOTS, `bug001-no-scroll-${vp.w}x${vp.h}.json`),
        JSON.stringify({ viewport: vp, ...metrics }, null, 2)
      );
    }
  });
});
