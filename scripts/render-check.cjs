#!/usr/bin/env node
/* Optional visual QA. Requires sharp. */
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('sharp');
const root = path.resolve(__dirname, '..');
const output = path.join(root, '.qa');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'manifest.json'), 'utf8'));

(async () => {
  fs.mkdirSync(output, {recursive: true});
  const failures = [];
  const bounds = {};
  let count = 0;
  for (const icon of manifest.icons) {
    for (const rendition of Object.values(icon.renditions)) for (const filename of new Set(Object.values(rendition.tones))) {
      const size = rendition.size, padding = size / 8, scale = size === 24 ? 8 : 1, extent = size + 2 * padding;
      const input = fs.readFileSync(path.join(root, filename), 'utf8');
      // An expanded viewport detects artwork clipped by the original canvas.
      const expanded = input.replace(`width="${size}" height="${size}" viewBox="0 0 ${size} ${size}"`, `width="${extent * scale}" height="${extent * scale}" viewBox="-${padding} -${padding} ${extent} ${extent}"`);
      const {data, info} = await sharp(Buffer.from(expanded)).ensureAlpha().raw().toBuffer({resolveWithObject: true});
      let minX = extent, minY = extent, maxX = -1, maxY = -1, pixels = 0;
      for (let y = 0; y < info.height; y++) for (let x = 0; x < info.width; x++) {
        if (data[(y * info.width + x) * info.channels + 3] > 16) {
          pixels++; minX = Math.min(minX, x / scale - padding); maxX = Math.max(maxX, x / scale - padding);
          minY = Math.min(minY, y / scale - padding); maxY = Math.max(maxY, y / scale - padding);
        }
      }
      if (!pixels) failures.push(`${filename}: blank render`);
      const margin = size === 24 ? 1 : 8;
      if (minX < margin || minY < margin || maxX > size - margin || maxY > size - margin) failures.push(`${filename}: insufficient canvas margin [${minX}, ${minY}, ${maxX}, ${maxY}]`);
      bounds[filename] = [minX, minY, maxX, maxY];
      count++;
    }
  }
  for (const category of Object.keys(manifest.categories)) {
    await sharp(path.join(root, `docs/contact-sheets/${category}.svg`)).png().toFile(path.join(output, `${category}.png`));
  }
  for (const file of fs.readdirSync(path.join(root, 'examples')).filter(file => file.endsWith('.svg'))) {
    await sharp(path.join(root, 'examples', file)).png().toFile(path.join(output, file.replace('.svg', '.png')));
  }
  await sharp(path.join(root, 'docs/overview.svg')).png().toFile(path.join(output, 'overview.png'));
  await sharp(path.join(root, 'docs/web-overview.svg')).png().toFile(path.join(output, 'web-overview.png'));
  await sharp(path.join(root, 'docs/compact-comparison.svg')).png().toFile(path.join(output, 'compact-comparison.png'));
  fs.writeFileSync(path.join(output, 'bounds.json'), JSON.stringify(bounds, null, 2) + '\n');
  if (failures.length) throw new Error(failures.join('\n'));
  console.log(`Rendered ${count} SVGs; every asset is nonempty and contained with at least 8 units clearance on 256-unit grids and 1 unit on 24-unit grids. Contact sheets and examples: .qa/`);
})().catch(error => {console.error(error.message); process.exitCode = 1;});
