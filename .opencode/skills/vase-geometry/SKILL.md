---
name: vase-geometry
description: Use when changing or reviewing Vase Builder meshes, textures, drains, joints, trays, print fit, scaffold generation, or 3MF/OpenSCAD export.
---

# Geometry and export changes

For code changes, also load `vase-architecture`. Read these references when their
scope applies (paths relative to this skill directory):

- [Printing design and acceptance](references/printing.md): walls, drains, joints,
  trays, texture projections, orientation and process metadata changes.
- [OpenSCAD practices](references/openscad.md): `editableSource`, `.scad` snapshots,
  winding conversion, rendering/export checks and explicitly requested CAD authoring.

## Read the affected path

- `src/core.js`: `defaults`, `normalize`, `makeMesh`, `modulePitch`,
  `shellCoordinate`, `sampleTexture`, `sculptValue`, `nestingSurface`,
  `prepareSeamSource`, `surfaceSource`, `estimateSize`, `fit`, `platePlan`, `export3mf`.
- `src/tray.js`: `outline`, `footprint`, `make`, `flattenFloor`.
- `src/base.js`: `dims`, `make`, voxel topology repair.
- `tests/geometry.cjs` and `tests/test_build.py` for existing geometry/export checks.

## Contracts to preserve

1. Templates contain semantic coordinates, outer tags, and drain loops. They are
   not arbitrary interchangeable meshes. `warpZ` preserves connector zones;
   width transforms preserve circular hardware holes. Do not uniformly scale them.
2. Use `modulePitch(config)` for repeat spacing: flush and ordinary joints differ.
   Opposite walls mirror phase; rotated end modules must remain interchangeable.
   Procedural repeat rules do not automatically apply to imported-image relief.
3. Body and nesting tray share `nestingSurface` and a combined-height envelope.
   Check both sides of their split and the receiving ridge clearance. Floor
   rebuilding must preserve/remap `exteriorVertices`, `cutNormals`, and drain data.
4. Tessellation must share edge vertices and preserve removed-drain-face provenance.
   Deleting degenerate triangles alone can open a shell. Keep repair logic unless
   a regression demonstrates a correct replacement.
5. Prepared sources and some generated meshes are cached/shared. Clone before
   transforms; check all affected cache keys when adding geometry settings.
6. `previewOnly` controls tessellation; `forPreview` requests rendering metadata.
   Test selected export detail as well as responsive preview for the changed case.
7. Update fit estimates (`textureProjection`, `estimateSize`, tray `footprint`) when
   protrusions change. Assembly placement and print-plate placement are distinct.
8. 3MF is unsliced ZIP/XML with Orca-derived plate/process metadata and a 36-plate
   limit. Preserve object references, units, actual bounds, and connector process
   settings. OpenSCAD export is a mesh snapshot, not the parametric source.

## Smallest useful regression

Use sanitized config that reproduces the defect and add an assertion to the
existing relevant test. For topology, check finite coordinates, nonzero triangle
area, two oppositely directed incidences per edge, and positive volume. Core
`validate()` alone does not establish manifoldness. Existing topology checks cover
representative preview meshes, not every full-detail body or parameter combination.
For texture changes, include a straight/curved wall and module or tray transition.
For export changes, inspect generated ZIP/XML and plate bounds/process values.

Build and run `python scripts/test.py`; use the extended suite for final code
handoff. For targeted investigation, run
`node --max-old-space-size=4096 tests/geometry.cjs` after building. It produces
the fit-test export consumed by `python tests/test_build.py`; keep that order.

## Does the scaffold need regeneration?

Read `scripts/prepare_seams.cjs` and `scripts/regenerate_seams.py`. Regenerate for
canonical fixed-template changes or changes to `prepareSeamSource` and its boundary
tagging, cuts, refinement, triangulation, sampling, or serialization dependencies.
Ordinary final displacement/UI/export edits do not inherently require regeneration.

```sh
python scripts/regenerate_seams.py
python scripts/build.py
python scripts/test.py --extended
```

`--check` verifies the compressed asset but still writes intermediate data in
`dist/`. Byte comparisons require a consistent compression toolchain. Keep source
and changed compressed scaffold together. Report visual/slicer/physical checks
separately; preserve calibration clearances and recommend fit samples for changed joints.
