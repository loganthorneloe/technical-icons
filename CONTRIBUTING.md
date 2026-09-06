# Extending the library

Keep standalone SVGs in category folders and include each concept in the previewer. Preserve published IDs and paths when improving artwork.

## Source locations

| Source | Responsibility |
| --- | --- |
| `src/icons.py` | Original technical illustration recipes |
| `src/extensions.py` | Additional illustrated concepts and targeted revisions |
| `src/website.py` | Cel-shaded website and contact objects, including revisions to former flat defaults |
| `src/cel.py` | Shared hard-shaded extrusion, paper, rings, and metal forms |
| `src/compact.py` | `symbols()` for compact technical renditions; `additions()` for controls, channels, and flowchart shapes |
| `src/brands/marks.json` | Pinned source geometry, dimensions, hashes, and provenance for social marks |
| `src/catalog_model.py` | Categories, concept assembly, rendition dimensions, tone variants, and export paths |
| `src/drawing.py` | Portable SVG primitives and palette |
| `scripts/build.py` | Assets, manifest, offline data, inventory, contact sheets, comparison sheet, and example compositions |

Read [the design system](docs/design-system.md) before adding artwork. Use lowercase kebab-case IDs, accurate descriptions, and helpful search aliases. Add a new category to `CATEGORIES` in `src/catalog_model.py` when needed. Website search/settings are prefixed with `ui-` to distinguish their controls from technical concept illustrations.

Use 256-unit canvases with at least 8 units of clear margin for illustrated objects (including social/web/contact defaults), and 24-unit canvases with at least 1 unit for compact symbols. Review at the recommended display size and against neighboring icons. A compact technical rendition must simplify the geometry, not only resize the illustrated version.

For brand marks, retain the original source path, record the upstream package version and URL, verify package integrity, hash the path, and include its license and attribution. Keep the front path exact with uniform scaling. Cel-shaded side surfaces are derived from stored contours; the front is identified by `data-brand-face="true"` for validation. `scripts/prepare-brand-contours.py` prepares those contours when source paths change and requires the optional `fonttools` package. Ordinary builds use stored contours and remain dependency-free. The existing 23 Font Awesome paths are pinned at 7.3.1; the Substack path is pinned from Simple Icons 16.30.0; ordinary builds require no network access.

## Build and validate

Python 3.10+ with no third-party modules:

```sh
python3 scripts/build.py
python3 scripts/validate.py --rebuild
```

Never hand-edit generated files under `icons/`, `variants/`, `examples/`, or `docs/contact-sheets/`, or the manifest, `catalog/data.js`, `docs/catalog.md`, `docs/inventory.md`, `docs/overview.svg`, `docs/web-overview.svg`, and `docs/compact-comparison.svg`. Update README figures and the HTML's fallback totals when inventory changes; runtime totals and generated inventory come from the manifest.

The build does not delete old assets. If an ID must be removed or renamed, remove its old files in the same change and document the breaking change. Validation flags orphaned assets, duplicate IDs/drawings, stale browser data, unsupported SVG elements, and altered brand paths. It checks every rendition and tone at its own dimensions, plus deterministic build output.

## Visual and browser checks

Optional development checks use Node.js, `sharp`, and `playwright` with Chromium. Supply these from an existing development environment or a temporary directory:

```sh
qa_deps=$(mktemp -d)
npm install --prefix "$qa_deps" sharp playwright
NODE_PATH="$qa_deps/node_modules" node scripts/render-check.cjs
NODE_PATH="$qa_deps/node_modules" node scripts/browser-check.cjs
```

Set `CHROME_PATH` to an existing Chromium/Chrome executable when needed. Otherwise use Playwright's browser installer in the temporary environment.

The raster check renders all standalone files inside an expanded viewport to detect clipping, checks nonempty output and margins, and writes previews to `.qa/`. The browser check covers offline loading, every detail view, search, categories, style filters, real-size previews, tone-aware downloads and copying, clipboard fallback, keyboard dismissal, and desktop/mobile layout. It also checks text bounds in generated compositions. Inspect screenshots and affected contact sheets before delivery.

## Package

```sh
python3 scripts/package.py
```

This validates a reproducible build and writes `dist/icons.zip` with assets, catalog, examples, docs, source, scripts, and third-party notices. `dist/` and `.qa/` are ignored by Git.
