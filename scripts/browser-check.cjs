#!/usr/bin/env node
/* Integration checks for the actual offline catalog. Requires Playwright. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '..');
const output = path.join(root, '.qa');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'manifest.json'), 'utf8'));

(async () => {
  fs.mkdirSync(output, {recursive: true});
  const browser = await chromium.launch({headless: true, ...(process.env.CHROME_PATH ? {executablePath: process.env.CHROME_PATH} : {})});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}, deviceScaleFactor: 1});
    const errors = [], remoteRequests = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('request', request => {if (/^https?:/.test(request.url())) remoteRequests.push(request.url());});
    await page.goto(pathToFileURL(path.join(root, 'index.html')).href);
    await page.evaluate(() => document.fonts.ready);
    assert.equal(await page.locator('.icon-card').count(), manifest.count);
    assert.equal(await page.locator('#count').textContent(), `${manifest.count} icons`);
    assert(await page.evaluate(() => document.fonts.check('600 24px Sora') && document.fonts.check('400 16px Roboto')));
    await page.screenshot({path: path.join(output, 'catalog-desktop.png')});
    for (const [category] of Object.entries(manifest.categories)) {
      await page.locator(`[data-category="${category}"]`).click();
      assert.equal(await page.locator('.icon-card').count(), manifest.icons.filter(i => i.category === category).length);
    }
    await page.locator('[data-category="all"]').click();
    await page.locator('#search').fill('bpe');
    assert.equal(await page.locator('.icon-card').count(), 1);
    assert.match(await page.locator('.icon-card').textContent(), /Tokenizer/);
    await page.locator('#search').fill('zz-no-such-artifact');
    assert(await page.locator('#empty').isVisible());
    await page.locator('#reset').click();
    assert.equal(await page.locator('.icon-card').count(), manifest.count);
    // Read back every detail view and decode its actual rendered image.
    for (const icon of manifest.icons) {
      await page.getByRole('button', {name: `View ${icon.name}`, exact: true}).click();
      assert.equal(await page.locator('#detail-name').textContent(), icon.name);
      const rendition = icon.renditions[icon.style];
      assert.equal(await page.locator('#detail-path').textContent(), rendition.tones.ivory || rendition.file);
      await page.locator('#detail-preview .detail-art').evaluate(image => image.decode());
      await page.keyboard.press('Escape');
    }
    // Style filters expose additional drawings without counting them as extra concepts.
    for (const [style, count] of Object.entries(manifest.styles)) {
      await page.locator('#style-filter').selectOption(style);
      assert.equal(await page.locator('.icon-card').count(), count);
    }
    await page.locator('#style-filter').selectOption('compact');
    await page.locator('#size-filter').selectOption('24');
    assert.equal(await page.locator('.icon-stage img').first().evaluate(el => el.getBoundingClientRect().width), 24);
    await page.getByRole('button', {name: 'View GPU', exact: true}).click();
    assert.equal(await page.locator('#detail-path').textContent(), 'variants/compact-ivory/compute/gpu.svg');
    assert.equal(await page.locator('.size-samples img[width="24"]').evaluate(el => el.getBoundingClientRect().width), 24);
    await page.locator('#detail-style').selectOption('illustrated');
    assert.equal(await page.locator('#detail-path').textContent(), 'icons/compute/gpu.svg');
    await page.locator('#detail-style').selectOption('compact');
    const [compactDownload] = await Promise.all([page.waitForEvent('download'), page.locator('#download').click()]);
    assert.equal(compactDownload.suggestedFilename(), 'gpu-compact-ivory.svg');
    await compactDownload.saveAs(path.join(output, 'gpu-compact-ivory.svg'));
    assert.equal(fs.readFileSync(path.join(output, 'gpu-compact-ivory.svg'), 'utf8'), fs.readFileSync(path.join(root, 'variants/compact-ivory/compute/gpu.svg'), 'utf8'));
    await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', {value: {writeText: async text => {window.copiedSvg = text;}}, configurable: true}));
    await page.locator('#copy').click();
    assert.equal(await page.evaluate(() => window.copiedSvg), fs.readFileSync(path.join(root, 'variants/compact-ivory/compute/gpu.svg'), 'utf8'));
    await page.screenshot({path: path.join(output, 'catalog-compact-detail.png')});
    await page.keyboard.press('Escape');
    await page.locator('#style-filter').selectOption('brand');
    await page.getByRole('button', {name: 'View GitHub', exact: true}).click();
    assert(await page.locator('#detail-attribution').isVisible());
    assert.equal(await page.locator('#detail-path').textContent(), 'variants/ivory/socials/github.svg');
    await page.keyboard.press('Escape');
    await page.locator('#style-filter').selectOption('all');
    await page.locator('[data-category="socials"]').click();
    await page.getByRole('button', {name: 'View GitHub', exact: true}).click();
    assert.equal(await page.locator('#detail-style').inputValue(), 'illustrated');
    assert.equal(await page.locator('#detail-path').textContent(), 'icons/socials/github.svg');
    const [celDownload] = await Promise.all([page.waitForEvent('download'), page.locator('#download').click()]);
    await celDownload.saveAs(path.join(output, 'github-cel.svg'));
    assert.equal(fs.readFileSync(path.join(output, 'github-cel.svg'), 'utf8'), fs.readFileSync(path.join(root, 'icons/socials/github.svg'), 'utf8'));
    await page.screenshot({path: path.join(output, 'catalog-social-detail.png')});
    await page.locator('#detail-style').selectOption('brand');
    assert.equal(await page.locator('#detail-path').textContent(), 'variants/ivory/socials/github.svg');
    await page.keyboard.press('Escape');
    await page.locator('[data-category="channels"]').click();
    await page.getByRole('button', {name: 'View Email', exact: true}).click();
    assert.equal(await page.locator('#detail-path').textContent(), 'icons/channels/email.svg');
    await page.locator('#detail-style').selectOption('compact');
    assert.equal(await page.locator('#detail-path').textContent(), 'variants/ivory/channels/email.svg');
    await page.keyboard.press('Escape');
    await page.locator('[data-category="all"]').click();
    await page.locator('#style-filter').selectOption('all');
    await page.locator('#size-filter').selectOption('fit');
    await page.locator('[data-bg="white"]').click();
    await page.getByRole('button', {name: 'View Straight arrow', exact: true}).click();
    assert.equal(await page.locator('#detail-path').textContent(), 'variants/ink/connectors/arrow-right.svg');
    const [download] = await Promise.all([page.waitForEvent('download'), page.locator('#download').click()]);
    assert.equal(download.suggestedFilename(), 'arrow-right-ink.svg');
    const downloadPath = path.join(output, download.suggestedFilename());
    await download.saveAs(downloadPath);
    assert.equal(fs.readFileSync(downloadPath, 'utf8'), fs.readFileSync(path.join(root, 'variants/ink/connectors/arrow-right.svg'), 'utf8'));
    await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', {value: {writeText: async () => {throw new Error('Forced clipboard fallback');}}, configurable: true}));
    await page.locator('#copy').click();
    assert(await page.locator('#copy-fallback').isVisible());
    assert.equal(await page.locator('#copy-fallback').inputValue(), fs.readFileSync(downloadPath, 'utf8'));
    await page.keyboard.press('Escape');
    await page.locator('[data-bg="dark"]').click();
    await page.getByRole('button', {name: 'View Tokenizer', exact: true}).click();
    await page.screenshot({path: path.join(output, 'catalog-detail.png')});
    await page.keyboard.press('Escape');
    await page.locator('#search').blur();
    await page.keyboard.press('/');
    assert(await page.locator('#search').evaluate(element => element === document.activeElement));
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
    await page.setViewportSize({width: 390, height: 844});
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({path: path.join(output, 'catalog-mobile.png')});
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
    await page.getByRole('button', {name: 'View Tokenizer', exact: true}).click();
    assert(await page.locator('#download').isVisible());
    await page.screenshot({path: path.join(output, 'catalog-mobile-detail.png')});
    await page.keyboard.press('Escape');
    await page.setViewportSize({width: 320, height: 740});
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
    await page.getByRole('button', {name: 'View GPU', exact: true}).click();
    await page.locator('#detail-style').selectOption('compact');
    assert.equal(await page.locator('.size-samples img[width="24"]').evaluate(el => el.getBoundingClientRect().width), 24);
    assert(await page.locator('#detail').evaluate(el => el.scrollWidth <= el.clientWidth));
    await page.screenshot({path: path.join(output, 'catalog-small-detail.png')});
    // Example typography and contact-sheet labels must fit their SVG canvases.
    const svgs = ['docs/overview.svg', 'docs/compact-comparison.svg', 'docs/web-overview.svg', ...fs.readdirSync(path.join(root, 'examples')).map(f => `examples/${f}`), ...fs.readdirSync(path.join(root, 'docs/contact-sheets')).map(f => `docs/contact-sheets/${f}`)].filter(f => f.endsWith('.svg'));
    for (const file of svgs) {
      await page.goto(pathToFileURL(path.join(root, file)).href);
      await page.evaluate(() => document.fonts.ready);
      const outside = await page.evaluate(() => {
        const svg = document.querySelector('svg'), box = svg.viewBox.baseVal;
        return [...svg.querySelectorAll('text')].filter(element => {const r = element.getBBox(); return r.x < 0 || r.y < 0 || r.x + r.width > box.width || r.y + r.height > box.height;}).map(element => element.textContent);
      });
      assert.deepEqual(outside, [], `Text outside ${file}`);
    }
    assert.deepEqual(errors, []);
    assert.deepEqual(remoteRequests, []);
    console.log(`Catalog passed: ${manifest.count} detail views, categories, search, fonts, SVG download, clipboard fallback, keyboard, responsive layout, and ${svgs.length} composition text bounds. No remote requests or page errors.`);
  } finally {await browser.close();}
})().catch(error => {console.error(error); process.exitCode = 1;});
