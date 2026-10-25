# AI development guide

Vase Builder is an offline modular-planter designer, not a general vase CAD tool.
Read `README.md`, `CONTRIBUTING.md`, and `docs/DEVELOPMENT.md` for product scope,
contribution expectations, and reproducibility. OpenCode usage: `docs/AI_DEVELOPMENT.md`.

## Architecture

- Plain JavaScript global scripts; Python standard-library build; Node built-ins
  for tests. No package installation is required. Preserve the offline,
  self-contained output; do not introduce a framework or bundler by default.
- `scripts/build.py` embeds assets and scripts into ignored `dist/index.html`.
  Edit `src/`, never generated HTML. Script order is base, tray, core, preview,
  mesh-worker, assembly, app, ux; the worker has its own embedded source bundle.
- `src/core.js` exposes `PlanterCore`: defaults/normalization, texture fields,
  mesh transforms, assembly placement, plate planning, and exporters.
- `src/base.js` and `src/tray.js` own support geometry. Tray code also rebuilds
  the body floor; a tray edit can affect body topology.
- `src/app.js` owns configuration, persistence, worker scheduling and downloads;
  `src/index.template.html` owns layout/style/controls; `src/ux.js` augments controls.
- `src/mesh-worker.js` generates cached packed buffers; `src/preview.js` renders
  them with WebGL; `src/assembly.js` builds the configuration-aware guide.
- `assets/mesh-data.json` is canonical template geometry. The checked-in
  `assets/seam-data.json.gz` is a regenerable scaffold, not disposable output.
  Avoid dumping these large assets into context.

## Working rules

1. Inspect `git status --short` and relevant source/tests before editing. Preserve
   existing user changes. Use a small scoped diff; do not reformat dense files wholesale.
2. Trace new settings through defaults, `normalize`, UI, saved settings, caches,
   preview, export, and assembly guidance as applicable. Keep existing design keys
   and legacy Capsule names compatible unless migration is explicitly requested.
3. Load `vase-architecture` for JavaScript/Python logic, tooling, or architecture
   changes. Also load `vase-geometry` for mesh/texture/fit/export changes and
   `vase-preview` for controls, renderer, worker, or browser behavior. Geometry's
   printing/OpenSCAD references are required when those areas are affected.
4. Preserve physical clearances, hardware dimensions, topology metadata, and
   selected export quality. Lighter preview recovery must not change export settings.
5. Add a focused regression to the existing relevant test for nontrivial behavior.
   Do not introduce a test framework or a second test runner.
6. Treat imported JSON/images as untrusted. Preserve validation and resource limits.
   Do not commit personal settings, exports, reference images, credentials or machine paths.
7. Use available documentation tools for library/API-specific questions. Browser
   tooling is optional, but report a missing real-browser check honestly.
8. Commit, push, publish, or operate physical printers only when explicitly requested.

## Verification

Run from the repository root (Python 3.12, Node 24; see version files):

```sh
python scripts/build.py
python scripts/test.py
```

Build first: tests consume generated HTML; the runner does not build it. For
worker/recovery, scaffold, build-pipeline changes, or a merge-ready code handoff,
run `python scripts/test.py --extended` after building (it includes the normal suite).
Allow several minutes and up to about 4 GB heap for dense geometry checks.

If template or surface-preparation inputs change:

```sh
python scripts/regenerate_seams.py
python scripts/build.py
python scripts/test.py --extended
```

Commit regenerated scaffold and source together. For documentation/OpenCode-only
edits, run `python scripts/audit.py` and validate discovery/references instead of
re-running geometry. UI changes also need a real-browser check; DOM/WebGL doubles
do not establish visual correctness. Mesh checks do not prove physical fit or
watertightness. Label evidence as automated, browser, slicer, or physical print.

Finish with what changed, checks actually run and results, and any remaining
acceptance gaps. Never claim skipped checks passed.
