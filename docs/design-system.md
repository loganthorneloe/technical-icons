# Design system

## Direction

The supplied tokenization illustration is the primary visual reference: ivory paper, industrial red processing hardware, blue-gray storage cylinders, cream arrows, and a deep-blue field. The brand's base colors and typography provide the foundation. The user's explicit request for colored, cel-shaded, retrofuturist diagram assets takes precedence over the brand guide's default monochrome treatment for technical graphics.

The drawing system translates that reference into clean vector geometry. It preserves material cues, crisp outlines, visible top/side planes, and recognizable silhouettes. Grain, photographic texture, and soft shadows are omitted to keep every SVG editable and predictable in slide tools.

## Palette

| Role | Hex | Use |
| --- | --- | --- |
| Ink | `#101527` | Canvas, outlines, recessed displays |
| Ivory | `#E9DDC7` | Documents, keys, node fills, connectors |
| Paper highlight | `#FFF4DE` | Top faces and narrow highlights |
| Paper shadow | `#B8AC99` | Folded corners and side faces |
| Steel | `#526B7A` | Infrastructure and machine housings |
| Steel highlight | `#78909B` | Top faces, metal details |
| Steel shadow | `#304654` | Side faces and recessed structures |
| Red | `#CC3333` | Processing, active parts, focused emphasis |
| Red highlight | `#E4604E` | Lit red planes |
| Red shadow | `#8F292C` | Shaded red planes |

Ink and red are exact brand colors; ivory and steel families are the controlled extension derived from the supplied reference. The catalog additionally uses the brand's elevated dark, border, muted, and secondary text tokens. White is reserved for interface text where needed.

## Illustrated geometry

- Canvas: `viewBox="0 0 256 256"`, transparent, square.
- Minimum clear margin: 8 units; typical main silhouette inset: 24–48 units.
- Base outline: 2.5 units, rounded joins and caps.
- Internal symbols: 3–6 units where needed for legibility.
- Projection: usually 8–18 units right and 70% of that upward, with flat top and side color planes.
- Main content occupies approximately 65–85% of the canvas; aspect ratios reflect the represented object.
- Physical parts should explain the object: cooling vents, processor pins, storage tiers, drive bays, folded paper, sockets, or seals.
- Abstract concepts use recognizable structures: layers, matrices, vectors, branches, queues, or directed edges.

Use the primitives in `src/drawing.py` so line caps, extrusion direction, and materials remain consistent. Do not turn every concept into the same enclosure with a new badge. Reuse a base when the shared structure is meaningful, such as specialized databases or members of one compute family.

## Compact geometry

Compact symbols are separate drawings on a `24 × 24` grid with a minimum 1-unit clear margin. Most outlines are 1.75 units with rounded joins and caps. Use ink on light surfaces and ivory on dark surfaces. Keep silhouettes distinct and prefer a small number of substantial features over miniature decoration.

Technical compact renditions target 32px and larger; website controls, channels, and flowchart primitives target 24px and larger. Database variants use one distinguishing structure. Neural networks use fewer nodes and edges; processors use fewer pins. Model weights use variable-size dots, while a table uses rows and a header. A service exposes an interface, while a worker represents job execution.

Preserve the illustrated rendition when adding compact geometry. Do not mechanically shrink a detailed drawing or remove the representation that makes the concept recognizable. Use [the comparison sheet](compact-comparison.svg) to inspect both sizes side by side.

## Labels and identity

Individual icons contain only shapes. Their `<title>` and `<desc>` elements are nonvisual accessibility metadata. Code brackets, cursors, and the function symbol are paths rather than font glyphs.

Use **Sora Semibold** for headings and **Roboto** for labels in the catalog and example diagrams. All required font files are local. Prefer 1–3 word node labels and one core idea per diagram. The longer titles in contact sheets are inventory names, not recommended slide labels.

No brand mark is placed on explanatory objects. Social brand marks are a separate collection sourced from Font Awesome Free and Simple Icons. Their front paths are preserved with uniform scaling and centering; the cel treatment adds explicit shaded extrusion around those silhouettes. Do not invent or distort a vendor mark. Attribution is embedded in each exported brand SVG and listed in the third-party notices. The `kubernetes` search ID uses a generic orchestration symbol, explicitly described as such in the catalog.

## Export contract

Individual icons use only `svg`, `g`, `path`, `rect`, `circle`, `ellipse`, `line`, `polygon`, `title`, and `desc`. All styles are explicit presentation attributes. No CSS variables, `currentColor`, gradients, masks, clipping paths, filters, raster payloads, script, fonts, `<use>`, or external references occur in these assets.

The examples and contact sheets are compositions, so their contract also permits live text and embedded font definitions. They have opaque backgrounds and are not individual transparent icons.

## Audit

Before accepting an icon, verify:

1. Its silhouette and key internal structure identify the intended concept.
2. Its colors, plane directions, and outline weights fit the collection.
3. Red serves a meaningful part of the representation.
4. It remains understandable at its recommended size: 96px illustrated technical, 64px cel-shaded social/web/contact, 32px compact technical, or 24px flat control/mark. Inspect the actual pixels, not only an enlarged preview.
5. The object is fully contained, including strokes and arrowheads.
6. It uses no raster data or typography dependencies.
7. Its name, description, and aliases match the actual drawing.
8. Its exported bytes reproduce from the source recipe.

Automated XML, manifest, reproducibility, and expanded-viewport raster checks complement visual inspection; they do not replace semantic review. Browser tests cover the catalog's main interactions. PowerPoint-specific import behavior remains an application-level check.

## Social, website, and contact objects

The default treatment follows the user's explicit request for the same cel-shaded material language throughout the library. Social marks are freestanding sculpted silhouettes. Website controls and contact concepts are distinct objects: folded paper, metal slats, lenses, handsets, trays, switches, and media keys. Avoid placing a different flat glyph onto an otherwise identical plaque for every concept.

Use consistent upper-right extrusion, crisp navy outlines, a flat front color, and separate top/side tones. Preserve empty space through cutouts and letterforms. Brand front paths remain source-exact; stored contour approximations generate their side surfaces. The dedicated small flat renditions are alternatives, not the default collection.
