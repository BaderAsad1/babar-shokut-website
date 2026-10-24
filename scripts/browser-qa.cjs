/* CI-only browser QA. The published site has no Node dependency. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const { spawn } = require('node:child_process');
const live = process.argv.includes('--live');
const base = live ? 'https://baderasad1.github.io/babar-shokut-website/' : 'http://127.0.0.1:8000/';
const routes = ['', 'advice/', 'advice/washing-machine-not-draining/'];
(async () => {
  let server, browser;
  const report = [];
  await fs.mkdir('qa-output', { recursive: true });
  try {
    if (!live) {
      server = spawn('python3', ['-m', 'http.server', '8000', '--bind', '127.0.0.1', '--directory', 'dist']);
      for (let i = 0; i < 40; i++) {
        try { if ((await fetch(base)).ok) break; } catch {}
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }
    browser = await chromium.launch({ headless: true });
    for (const width of [320, 390, 768, 1440]) {
      const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 1 });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      for (const [index, route] of routes.entries()) {
        const response = await page.goto(base + route, { waitUntil: 'networkidle' });
        assert.equal(response.status(), 200, route + ' HTTP status');
        await page.evaluate(async () => {
          await document.fonts.ready;
          for (const image of document.images) {
            image.loading = 'eager';
            await image.decode().catch(() => {});
          }
        });
        assert.match(await page.locator('meta[name="robots"]').getAttribute('content'), /noindex/);
        const geometry = await page.evaluate(() => ({
          overflow: document.documentElement.scrollWidth > innerWidth,
          brokenImages: [...document.images].filter(img => !img.complete || !img.naturalWidth).map(img => img.src),
          h1: document.querySelector('h1').textContent,
        }));
        assert.equal(geometry.overflow, false, `${width} ${route} overflow`);
        assert.deepEqual(geometry.brokenImages, [], `${width} ${route} images`);
        assert.equal(await page.locator('a[href="tel:+971552434708"]').count() > 0, true);
        if (width === 390 || width === 1440) {
          await page.screenshot({ path: `qa-output/${live ? 'live' : 'local'}-${width}-${['home','advice','article'][index]}.jpg`, fullPage: true });
        }
        report.push({ width, route, status: response.status(), ...geometry });
      }
      assert.deepEqual(errors, []);
      await page.close();
    }
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    await page.goto(base);
    await page.locator('.menu-toggle').click();
    assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'true');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'false');
    await page.locator('.service-card .open-enquiry').first().click();
    assert.equal(await page.locator('#appliance').inputValue(), 'Washing machine');
    assert.equal(await page.locator('#inspection-dialog').evaluate(el => el.open), true);
    await page.locator('#city').selectOption('Sharjah');
    // Capture the URL without opening WhatsApp or sending anything.
    await page.evaluate(() => { window.open = url => { window.preparedUrl = url; }; });
    await page.locator('#inspection-form button[type="submit"]').click();
    const prepared = await page.evaluate(() => window.preparedUrl);
    assert.match(prepared, /^https:\/\/wa\.me\/971552434708\?text=/);
    assert.match(decodeURIComponent(prepared), /AED 50 inspection/);
    assert.match(await page.locator('#enquiry-status').textContent(), /not been confirmed/);
    await page.locator('.dialog-close').click();
    await page.goto(base + 'advice/');
    await page.locator('[data-category="fridges"]').first().click();
    assert.equal(await page.locator('.article-card:visible').count(), 2);
    await page.locator('#guide-search').fill('zznomatch');
    assert.equal(await page.locator('.no-results').isVisible(), true);
    await page.locator('[data-reset-filters]').click();
    assert.equal(await page.locator('.featured-guide').isVisible(), true);
    await fs.writeFile('qa-output/report.json', JSON.stringify(report, null, 2));
    console.log(JSON.stringify({ base, pagesChecked: report.length, interactions: 'pass', report }, null, 2));
  } finally {
    await browser?.close();
    server?.kill();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
