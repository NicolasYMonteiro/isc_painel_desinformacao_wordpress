const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('fs');
const path = require('path');

const OUT = path.join(__dirname, '../../docs/06-validation');
const SHOTS = path.join(OUT, 'screenshots');

function ensureDirs() {
  fs.mkdirSync(SHOTS, { recursive: true });
}

async function measureNoScroll(page) {
  return page.evaluate(() => {
    const doc = document.documentElement;
    const body = document.body;
    return {
      docOverflow: getComputedStyle(doc).overflowY,
      bodyOverflow: getComputedStyle(body).overflowY,
      scrollHeight: Math.max(doc.scrollHeight, body.scrollHeight),
      clientHeight: doc.clientHeight,
      scrollY: window.scrollY,
      hasScroll: Math.max(doc.scrollHeight, body.scrollHeight) > doc.clientHeight + 1,
    };
  });
}

async function measureTransition(page) {
  return page.evaluate(() => {
    return new Promise((resolve) => {
      const root = document.querySelector('.dsn-swiper');
      const next = document.querySelector('.swiper-button-next');
      const t0 = performance.now();
      let done = false;
      const finish = () => {
        if (done) return;
        done = true;
        resolve(performance.now() - t0);
      };
      const onEnd = () => finish();
      root.addEventListener('transitionend', onEnd, { once: true });
      // Swiper also fires slideChangeTransitionEnd via instance if present
      next.click();
      setTimeout(finish, 500); // cap
    });
  });
}

test.describe('DSN-DASH QA validation', () => {
  test.beforeAll(() => ensureDirs());

  for (const pageSlug of ['por-tema', 'por-plataforma']) {
    test(`page ${pageSlug}: structure, carousel, screenshots, a11y`, async ({ page }) => {
      const consoleErrors = [];
      page.on('console', (msg) => {
        if (msg.type() === 'error') consoleErrors.push(msg.text());
      });
      page.on('pageerror', (err) => consoleErrors.push(String(err)));

      await page.setViewportSize({ width: 1366, height: 768 });
      await page.goto(`/${pageSlug}/`, { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('.dsn-dashboard', { timeout: 30000 });

      // RF-018 badge
      await expect(page.locator('.dsn-badge-fake')).toBeVisible();

      // RF-004/005: 4 slides
      const slides = page.locator('.dsn-slide');
      await expect(slides).toHaveCount(4);

      // RF-007/RNF-007 titles
      const iframes = page.locator('.dsn-embed-iframe');
      const iframeCount = await iframes.count();
      for (let i = 0; i < iframeCount; i++) {
        const title = await iframes.nth(i).getAttribute('title');
        expect(title && title.trim().length > 0).toBeTruthy();
      }

      // embed types present
      const types = await page.$$eval('.dsn-slide', (els) =>
        els.map((e) => e.getAttribute('data-embed-type'))
      );
      expect(types).toContain('kibana');
      expect(types).toContain('shiny');

      // captions RF-016
      for (let i = 0; i < 4; i++) {
        const caption = await slides.nth(i).locator('.dsn-slide-caption').innerText();
        expect(caption.trim().length).toBeGreaterThan(10);
      }

      // RNF-002 no scroll 1366x768
      const scroll1366 = await measureNoScroll(page);
      test.info().annotations.push({ type: 'scroll-1366', description: JSON.stringify(scroll1366) });

      // screenshots each slide
      for (let i = 0; i < 4; i++) {
        if (i > 0) {
          await page.locator('.swiper-button-next').click();
          await page.waitForTimeout(400);
        }
        const name = `${pageSlug}-slide-${i + 1}.png`;
        await page.screenshot({ path: path.join(SHOTS, name), fullPage: false });
      }

      // RNF-001 transition (after being on last, go prev then measure next)
      await page.locator('.swiper-button-prev').click();
      await page.waitForTimeout(200);
      const ms = await measureTransition(page);
      test.info().annotations.push({ type: 'transition-ms', description: String(ms) });
      fs.appendFileSync(
        path.join(OUT, 'metrics.jsonl'),
        JSON.stringify({ page: pageSlug, transitionMs: ms, scroll: scroll1366 }) + '\n'
      );

      // RNF-006 keyboard
      await page.locator('.swiper-button-next').focus();
      await page.keyboard.press('Enter');
      await page.waitForTimeout(300);

      // axe
      const axe = await new AxeBuilder({ page }).exclude('iframe').analyze();
      const serious = axe.violations.filter((v) => ['serious', 'critical'].includes(v.impact));
      fs.writeFileSync(
        path.join(OUT, `axe-${pageSlug}.json`),
        JSON.stringify({ violations: axe.violations, seriousCount: serious.length }, null, 2)
      );
      test.info().annotations.push({
        type: 'axe-serious',
        description: String(serious.length),
      });

      // framing console keywords
      const framingHits = consoleErrors.filter((t) =>
        /x-frame|frame-ancestors|refused to display|framing/i.test(t)
      );
      fs.writeFileSync(
        path.join(OUT, `console-${pageSlug}.json`),
        JSON.stringify({ consoleErrors, framingHits }, null, 2)
      );

      // 1920x1080 scroll check
      await page.setViewportSize({ width: 1920, height: 1080 });
      await page.reload({ waitUntil: 'domcontentloaded' });
      await page.waitForSelector('.dsn-dashboard');
      const scroll1920 = await measureNoScroll(page);
      fs.appendFileSync(
        path.join(OUT, 'metrics.jsonl'),
        JSON.stringify({ page: pageSlug, viewport: '1920x1080', scroll: scroll1920 }) + '\n'
      );
    });
  }

  test('nav between pages RF-013 / RNF-012', async ({ page }) => {
    await page.goto('/por-tema/');
    await page.waitForSelector('.dsn-dashboard');
    await page.locator('a.dsn-nav__link', { hasText: 'Por Plataforma' }).click();
    await expect(page).toHaveURL(/por-plataforma/);
    await page.locator('a.dsn-nav__link', { hasText: 'Por Tema' }).click();
    await expect(page).toHaveURL(/por-tema/);
  });

  test('RNF-003 first embed visibility budget', async ({ page }) => {
    const t0 = Date.now();
    await page.goto('/por-tema/', { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('.dsn-embed-iframe, .dsn-state--empty', { timeout: 10000 });
    // wait for iframe load or state ready
    await page.waitForTimeout(100);
    const iframe = page.locator('.dsn-embed-iframe').first();
    if (await iframe.count()) {
      await iframe.waitFor({ state: 'visible', timeout: 8000 });
    }
    const elapsed = Date.now() - t0;
    fs.appendFileSync(
      path.join(OUT, 'metrics.jsonl'),
      JSON.stringify({ metric: 'first-embed-ms', elapsed }) + '\n'
    );
    test.info().annotations.push({ type: 'first-embed-ms', description: String(elapsed) });
  });

  test('RNF-009 ES exposure from browser context (informational)', async ({ page }) => {
    // Attempts fetch to ES from page origin — CORS/network result documented
    await page.goto('/por-tema/');
    const result = await page.evaluate(async () => {
      try {
        const r = await fetch('http://localhost:9200/', { mode: 'no-cors' });
        return { ok: true, type: r.type };
      } catch (e) {
        return { ok: false, error: String(e) };
      }
    });
    // Also direct request from test runner (simulates browser can reach port)
    let direct = null;
    try {
      const r = await page.request.get('http://localhost:9200/');
      direct = { status: r.status() };
    } catch (e) {
      direct = { error: String(e) };
    }
    fs.writeFileSync(path.join(OUT, 'es-exposure.json'), JSON.stringify({ result, direct }, null, 2));
  });

  test('homogeneity tokens RNF-005', async ({ page }) => {
    await page.goto('/por-tema/');
    await page.waitForSelector('.dsn-dashboard');
    const tokens = await page.evaluate(() => {
      const cs = getComputedStyle(document.documentElement);
      const keys = [
        '--dsn-color-bg',
        '--dsn-color-surface',
        '--dsn-color-accent',
        '--dsn-color-text',
        '--dsn-font-family',
        '--dsn-embed-pad',
      ];
      const vals = {};
      keys.forEach((k) => {
        vals[k] = cs.getPropertyValue(k).trim();
      });
      const frames = [...document.querySelectorAll('.dsn-embed-frame')].map((el) => {
        const s = getComputedStyle(el);
        return {
          paddingTop: s.paddingTop,
          paddingRight: s.paddingRight,
          paddingBottom: s.paddingBottom,
          paddingLeft: s.paddingLeft,
        };
      });
      return { vals, frames };
    });
    fs.writeFileSync(path.join(OUT, 'homogeneity.json'), JSON.stringify(tokens, null, 2));
    const colorTokens = Object.entries(tokens.vals).filter(([k, v]) => k.includes('color') && v);
    expect(colorTokens.length).toBeGreaterThanOrEqual(4);
  });
});
