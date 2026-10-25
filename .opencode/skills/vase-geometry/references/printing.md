# Design for printing and physical verification

Read this for changes to walls, floors, drains, joints, supports, trays, texture
projections, print orientation or process metadata. These are review criteria,
not universal printer settings or proof that existing designs pass every criterion.

## Establish the manufacturing assumptions

- Record target nozzle/line width, layer height, material, printer/build volume and
  intended orientation when making manufacturing claims. If unknown, preserve
  current defaults and state what remains unverified; do not invent calibration.
- Work in millimetres. Distinguish nominal geometry, actual mesh bounds, usable
  plate area with brim/reserved regions, and assembled dimensions.
- Preserve user-adjustable clearances. State whether a tolerance is radial,
  diametral, per-side or total; never apply one interpretation as another.

## Geometry that can be manufactured

- Evaluate the thinnest wall/floor after relief, shaping, bevels, drains and cuts,
  not just the nominal setting. Relate small ribs/bars/gaps to extrusion width and
  layer resolution; verify actual toolpaths rather than requiring an arbitrary
  universal wall thickness or exact integer line-width multiples.
- Check overhangs, bridge spans, support access/removal and first-layer contact in
  intended orientation. A fixed overhang angle is a heuristic, not a guarantee.
  Preserve smooth transitions and avoid tiny unsupported islands/sharp fragile tips.
- Consider layer-direction strength and stress concentrations in clips, rails and
  bolts. Preserve hardware envelopes, tool access and assembly order. Chamfers or
  fillets must not consume mating surfaces or change calibrated engagement.
- Inspect first-layer expansion (elephant foot), hole undersizing and shrinkage
  when revising fit. Prefer a small measured coupon over changing every clearance.
  Do not silently compensate in both CAD and slicer.
- Evaluate wet-soil load, sustained creep, temperature/UV exposure and material
  behavior for intended use. Do not equate higher infill with adequate strength or
  claim watertightness/material suitability from mesh validity alone.
- Check drainage paths from soil to outlet and tray, screen retention, cleanability,
  and channels after slicing. Consider clogging and trapped water. A closed tray
  mesh is not proof of leak resistance; confirm physically when that is required.

## Slicer acceptance for changed printable geometry

1. Export the actual selected-quality model/configuration. Inspect finite geometry,
   edge incidence/winding, degenerate faces, volume and bounds. Multiple shells can
   be intentional for separate parts; check connectivity per intended physical part.
   These checks do not rule out all self-intersections or overlapping internal shells.
2. Open the 3MF as a project in the target slicer. Record slicer version, printer,
   nozzle/material/process presets and any repair warnings. Automatic repair is not
   evidence that the original exporter was correct.
3. Check every plate's grouping, orientation, bed contact, brim/reserved area and
   machine limits. Confirm imported process metadata rather than assuming it survives.
4. Inspect layer toolpaths around thin walls, drains, floor/roof transitions, clips,
   unsupported features and mating surfaces. Confirm separate moving/mating parts
   are not fused; note missing features, unwanted supports or internal cavities.
5. Print the relevant fit coupon before a full part. Record nominal versus measured
   clearance and the material/profile/orientation used. Full parts may still warp
   or creep differently; a coupon pass is limited evidence.

Report automated, browser, slicer and physical evidence separately. Include the
sanitized config and relevant before/after observations. Never report a print,
leak/load test or slicer inspection as passed unless actually performed. Operating
a printer requires explicit user authorization; generating geometry does not grant it.
