# OpenSCAD snapshot and CAD practices

Read this when changing `PlanterCore.editableSource`, `.scad` output, or introducing
OpenSCAD geometry. Consult current official docs for version-specific syntax/CLI
options. OpenSCAD is currently an export target, not the app's source generator or
a required build dependency. Do not add a parallel CAD implementation by default.

## Existing exporter contract

- `src/core.js` generates `polyhedron(points=..., faces=...)` snapshots from the
  selected mesh quality. Changing dimensions and textures belongs in Studio;
  exported coordinates do not recover the original parametric construction.
- Preserve millimetres, part selection, safe serialization, and metadata that does
  not expose private image data. Test geometry correspondence, not just text output.
- OpenSCAD's documented input convention is clockwise face vertices viewed from
  outside (left-hand rule). The exporter currently reverses each core face. Keep
  that conversion explicit and test it; never reverse faces globally without tracing
  both exporters. Reflections/negative scales also require orientation consideration.
- Require valid point indices, finite coordinates, nonzero-area faces, consistent
  edge orientation and closed intended solids. Avoid duplicate/coplanar internal
  faces and self-intersections; a positive total signed volume alone is insufficient.
- `convexity` assists preview display; increasing it does not fix invalid geometry.
  `uniform_scale` scales hardware and tolerances too, requiring new fit verification.

## If parametric OpenSCAD is explicitly requested

- Use named dimensional parameters with units and documented constraints; distinguish
  design dimensions, fit clearance and numerical Boolean overlap. Use modules for
  meaningful geometry parts and functions for calculations, not generic CAD wrappers.
- Derive repeated dimensions from one source. Keep local coordinate frames and
  transformation order clear; test transformed bounds and mating surfaces.
- Avoid zero-thickness contacts and coincident Boolean boundaries. Cutters should
  extend through the target; any small overlap must be deliberate and scale-aware,
  not a blanket epsilon that changes printable clearances.
- Choose `$fa`/`$fs` or local `$fn` deliberately for curved primitives, balancing
  chord error, physical resolution and mesh cost. They do not retessellate an already
  baked polyhedron. Preview simplification must not silently lower exported quality.
- Keep preview-only helpers and assembly illustrations separate from exported solid
  geometry. Avoid expensive repeated Boolean operations unless the shape needs them.

## Acceptance

Add a focused automated check to an existing relevant test for snapshot structure,
indices, face conversion, selected parts and representative dimensions as affected.
With OpenSCAD available, open the generated file, select changed part(s), perform
full Render (F6), inspect messages, export a mesh, and compare bounds/topology to
the source. Preview (F5) alone is insufficient. Even successful rendering/export
does not certify manifoldness; validate the resulting mesh independently and inspect
it in the target slicer for print-facing changes.

Record the OpenSCAD version/backend and actual checks. If unavailable, report the
OpenSCAD round-trip as unverified rather than treating a serializer test as equivalent.
Use ignored `dist/` for generated artifacts; never replace canonical mesh assets
with a round-trip export without an explicit, reviewed migration.

## References

- [OpenSCAD documentation](https://openscad.org/documentation.html)
- [Polyhedron input conventions](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/3D_Solids#polyhedron)
- [OpenSCAD implementation and tests](https://github.com/openscad/openscad)

The upstream polyhedron implementation reverses incoming face indices internally;
upstream export tests also document that export success can occur for non-manifold
meshes. Check the release in use rather than assuming all backends behave identically.
