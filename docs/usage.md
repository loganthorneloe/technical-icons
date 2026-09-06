# Using the icons

## Direct file use

The SVGs are ordinary files in `icons/<category>/`; the previewer is optional. Copy a file into a website's public assets directory and reference it as an image, for example:

```html
<img src="/icons/compute/gpu.svg" width="128" height="128" alt="GPU">
```

Use an empty `alt` value when an adjacent label describes a decorative icon. Use compact technical symbols at 32px or larger, and their flat website/social alternatives at 24px or larger. Cel-shaded social, website, and contact defaults target 64px or larger:

```html
<img src="/variants/compact/compute/gpu.svg" width="32" height="32" alt="GPU">
<a href="https://github.com/your-profile" aria-label="GitHub profile">
  <img src="/icons/socials/github.svg" width="64" height="64" alt="">
</a>
```

Use `variants/compact-ivory/` for compact technical symbols on dark surfaces. Compact website and contact alternatives use `variants/compact/<category>/` for ink and `variants/ivory/<category>/` for ivory. Flat social marks use `variants/brand/socials/` for ink and `variants/ivory/socials/` for ivory. Read the rendition paths from the manifest rather than constructing them from a naming assumption.

Cel-shaded social/web/contact SVGs in `icons/` have fixed material colors, visible depth, and a 256-unit canvas. Their 1.1 counterparts used 24-unit flat geometry; use the alternate rendition paths above when preserving that appearance or size. Setting CSS `color` on an `<img>` does not recolor its SVG; choose an available tone file instead.

Social SVGs include source and license attribution in `<desc>`. Preserve that metadata and the corresponding notice when redistributing the assets; see [third-party notices](../THIRD_PARTY_NOTICES.md).

## Slides and diagram editors

Download an icon from `index.html`, or select its SVG directly from `icons/<category>/`. Insert that file with your editor's picture/image insertion command. For PowerPoint, use **Insert → Pictures** and select the SVG; wording varies by platform. Downloading and inserting the file preserves its vector source. Copying an image from a browser may produce a raster image instead.

Set the slide background to **`#101527`** for the intended appearance. Keep the icon's aspect ratio locked. Start with a 1.2–1.8 inch square on a widescreen slide, then adjust for the number of nodes and viewing distance. Reserve room below for a short label.

Use separate text boxes for names, values, and annotations. The icons intentionally have no visible text, so they work across topics and languages. Label a database icon “Vector store”, “Customer DB”, or “Feature store” according to its role. Prefer a specialized icon when that distinction is central to the explanation.

Some editors offer **Convert to Shape** or an ungroup action for imported SVGs. Where supported, this exposes the native paths and fills for recoloring. Keep an original copy before editing. The library does not require this feature to display the icons.

## Connectors and alignment

Use native presentation connectors when nodes will move: these remain adjustable and can attach to shapes. Use the supplied SVG connectors for fixed compositions or when consistent arrow geometry matters more than attachment behavior.

- Use **ivory `#E9DDC7`** arrows on deep blue. These are in `icons/connectors/`.
- Use **ink `#101527`** arrows on light backgrounds. These are in `variants/ink/connectors/`; the catalog selects them automatically for ivory/white previews.
- Keep normal arrows around 2–3px at slide scale, with simple open arrowheads.
- Use solid arrows for the primary flow and dashed arrows for a relationship defined in your diagram's legend.
- Keep lines outside the objects and label ambiguous relationships.
- Keep icon aspect ratios fixed. Horizontal or vertical stretching distorts cel-shaded depth and stroke weight.

Illustrated icons have a 256-unit layout box; compact symbols and brand marks use 24 units. The manifest records each rendition's dimensions. Its top-level cardinal anchors describe the canonical rendition and are **canvas layout anchors**, not guaranteed physical ports on the drawing. Actual silhouettes differ and sit inside the box. Route from the visible silhouette where appropriate, or attach native connectors to invisible layout rectangles.

The connector SVGs also use square canvases. A straight arrow's visible endpoints are `(25,128)` and `(229,128)`. Crop excess transparent space or recreate long arrows natively; stretching a whole connector also stretches its arrowhead.

## Color and scale

The reference's navy/ivory/steel/red treatment is the default. The browser lets you inspect individual shapes on light surfaces, but object colors do not change with the preview background. Ivory lines inside some compound icons have lower contrast on light slides. Use the intended navy canvas, adjust those lines in a vector editor, or use a dark panel behind the diagram.

Use 96px or more for illustrated technical objects and 64px or more for the cel-shaded social/web/contact collection. For denser diagrams, choose a compact rendition: 26 technical concepts have simplified geometry with fewer connections, pins, or compartments. Start at 32px for these technical symbols and 24px for compact website controls and flat social marks. The previewer offers literal 24/32/48/96px card sizes and actual-size samples in icon details. Review at the intended display size; 16px is not a target for this release.

Red identifies emphasis, an active stage, or a meaningful part of an object; it does not universally mean error. Pair color with a distinct shape and a short label. Avoid making every stage red in the same diagram.

## Example SVGs

The `examples/` files are complete compositions with an opaque navy background. Individual icon files are transparent. Example captions are live SVG text. Sora and Roboto fonts are embedded in those SVGs and included in `catalog/fonts/`; applications that ignore SVG font embedding may substitute a local font. Installing the included fonts or recreating the captions in slide text boxes preserves the intended typography.

The tokenization example uses illustrative vocabulary IDs from the supplied reference. It is not a claim about the output of a particular tokenizer. The RAG example abstracts prompt assembly: the original question accompanies the retrieved passages in the generation prompt. The service example shows initiating request/data direction and omits responses.

## Browser catalog

Open `index.html` directly. Search matches names, descriptions, categories, and technology aliases. Multiple search terms must all match. Click a category to narrow the results; choose **All icons** to remove that filter. Press `/` to focus search and `Escape` to close details.

**Style** filters select illustrated, compact, or flat-mark artwork. The category folders and default preview use the cel-shaded treatment for social, website, and contact icons. Details also let you switch between a concept's available styles. Preview backgrounds select the matching ink/ivory tone when available. **Download SVG** saves the exact standalone asset currently shown; the file path in details identifies it. **Copy SVG code** is for vector-aware tools and code editors. If clipboard access is unavailable, the catalog selects the SVG source in a text area for manual copying. Neither action sends data to a service.

For applications that prefer HTTP, serve the repository locally:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8000`. Stop the server with `Ctrl+C`.

## Manifest and programmatic use

`manifest.json` uses schema version 2. `count` counts concepts; `assetCount` counts all standalone files. `styles` reports concept availability by style, so those counts overlap. Each icon has a canonical `file`, `style`, `size`, `viewBox`, and `anchors` plus explicit `renditions`:

```json
"compact": {
  "file": "variants/compact/compute/gpu.svg",
  "size": 24,
  "viewBox": [0, 0, 24, 24],
  "recommendedMinSize": 32,
  "tones": {
    "ink": "variants/compact/compute/gpu.svg",
    "ivory": "variants/compact-ivory/compute/gpu.svg"
  }
}
```

Read each rendition's dimensions instead of assuming 256 units. If a tone is unavailable, use that rendition's `file`. Top-level `variants` remains a map of canonical tone alternatives for compatibility; it does not enumerate compact renditions. The offline previewer embeds the same manifest plus an `assets` map keyed by file path in `catalog/data.js`.
