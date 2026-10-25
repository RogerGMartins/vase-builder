---
name: vase-preview
description: Use when changing or reviewing Vase Builder UI controls, settings import, WebGL rendering, preview caches, worker scheduling, or timeout recovery.
---

# UI and preview changes

For JavaScript logic changes, also load `vase-architecture` for module boundaries,
state ownership, error handling and resource lifecycle practices.

## Trace the whole behavior

- `src/index.template.html`: IDs, labels, constraints, layout and styling.
- `src/app.js`: numeric/control registration, `setValues`, `refresh`, saved designs,
  image import, `rebuild`, `sendPreviewJob`, `startMeshWorker`, `previewTimedOut`.
- `src/ux.js`: enhanced numeric entry, help and accessibility.
- `src/core.js`: defaults and `normalize` are the configuration boundary.
- `src/mesh-worker.js`: `previewMeshKey`, `buildPreviewMeshes`, message protocol.
- `src/preview.js`: packed buffers, normals, rendering and GPU resource lifecycle.
- `src/assembly.js`: update the guide when a control changes assembly behavior.

## Invariants

1. Preserve saved-design keys and legacy localStorage names. New controls need
   defaults, normalization, UI synchronization and applicable persistence. Retain
   import size/type/value limits; never insert imported strings as trusted HTML.
2. Numeric typing, change events, ranges and enhanced controls must agree. Preserve
   labels, focus, keyboard access, collapsed panels, errors and disabled states.
3. Last edit wins: request IDs reject stale jobs; worker epochs reject terminated
   worker replies. Check partial as well as completed results. Pending updates and
   full-detail cancellation must not lose the latest design.
4. Timeout recovery is bounded: retry once with lighter preview, then expose failure.
   Never mutate selected export quality or saved design to achieve preview recovery.
5. Cache keys omit only render/process-only values. New geometry-affecting settings
   must invalidate affected meshes; color-only changes should not rebuild geometry.
   Keep byte/entry bounds. Do not transfer buffers in a way that detaches cached data.
6. Keep geometry off the UI thread where the current worker path supports it and
   preserve fallback behavior. Build-script changes must update both page and worker
   bundles without introducing network dependencies.

## Verify

Build first, then use existing focused checks as appropriate:

```sh
python scripts/parse_dom.py
node tests/controls.cjs
node tests/renderer.cjs
```

For scheduling/cache/recovery changes, run `python scripts/test.py --extended`
(includes real Node workers and both successful/exhausted watchdog recovery).
Add one focused regression to the applicable existing `.cjs` test for new logic.

For UI/render changes, serve the built app:

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Use available browser tools at `http://127.0.0.1:8000`, or document manual checks
if unavailable. Check the changed control with mouse, keyboard and numeric entry;
inspect console errors, actual geometry, and narrow layout when affected. For
worker changes, make rapid edits and toggle Full detail; verify the final preview
matches the last config. For import changes, use synthetic settings/images.

Useful browser hooks: `window.capsuleStudio` (getConfig/setConfig/getView/setView),
`window.capsulePreviewStats`, and `document.documentElement.dataset.ready`.
Test doubles do not prove GPU appearance. State exactly what was observed and
stop only servers/processes started for this task.
