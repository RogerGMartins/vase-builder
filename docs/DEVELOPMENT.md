# Development and reproducibility

## Reference environment

- Python 3.12.14, including zlib support.
- Node.js 24.19.0 with standard built-ins.
- Git for source management; no external build packages.

Version files record the toolchain. The standard build reads all files relative
to its script, writes LF-terminated UTF-8 output, and fixes gzip mtime to zero with
no original filename. It does not embed the current date or an absolute path.
The test suite checks equality against a second build after a clock delay.
Exact compressed bytes are only promised for an unchanged toolchain and inputs;
different zlib releases can emit different valid compression streams.

## Geometry assets

`assets/mesh-data.json` is canonical triangulated input. Parametric transformations,
texture fields and connector behavior live in `src/core.js` and the base/tray
modules. The earlier primitive OpenSCAD design is not the current mesh generator
and is deliberately excluded to avoid implying it reproduces the app's geometry.

`assets/seam-data.json.gz` is a checked-in acceleration asset, not a hidden external
dependency. `python scripts/regenerate_seams.py --check` rebuilds it from the
canonical template using the current source and verifies its compressed bytes.
The intermediate JSON is ignored in `dist/`. Large assets are ordinary Git files;
Git LFS is not required.

## Tests

`python scripts/test.py` checks source hygiene, syntax, control behavior, packed
render-buffer caching, Mineral coverage and repeat behavior, representative
body/tray topology, one-plate fit export, ZIP integrity, XML and process values,
and repeatable HTML generation.

`--extended` adds actual background workers, last-edit updates, full-preview
cancellation, successful and exhausted watchdog recovery, and scaffold regeneration.
The worker tests emulate browser DOM/canvas APIs. WebGL calls are checked with a
test double; these checks do not prove native GPU appearance or all slicer behavior.

For manual acceptance, inspect straight/curved texture walls, the top transition,
tray cut and interlock, module joints, the imported-image path and exported plates.
Print small fit samples before a full planter.

## Export implementation

3MF is written by a small project-local ZIP-store/CRC32 and XML exporter. It embeds
unsliced geometry and Orca-derived plate/process metadata, not a printer firmware
program. Compatibility fields include legacy slicer version identifiers. They are
format hints, not a statement that the exporting application is that slicer or that
the file has been tested in every named version. Select actual printer/material
presets and inspect settings in the target slicer.

## Publication workflow

The repository contains source, assets, documentation and checks. `dist/` is
generated and excluded from Git. A future release can attach `dist/index.html`
along with a SHA-256 digest after review. CI has read-only repository permissions,
immutable action references, no secrets and no deployment/publishing step.
Repository visibility and release publication require the owner's approval.
