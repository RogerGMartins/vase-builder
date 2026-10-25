---
description: Develop Vase Builder features and fixes across geometry, offline UI, preview workers, and export.
mode: primary
permission:
  question: allow
---

Follow AGENTS.md. Own implementation and verification end to end. Start from the
user-visible problem and acceptance criteria; ask only when an ambiguity blocks
correct work. Read the relevant tests before changing behavior.

Use vase-architecture for JavaScript/Python logic, tooling and architecture work;
also use vase-geometry and vase-preview when their scopes apply. Read the geometry
skill's printing/OpenSCAD references for affected manufacturing or CAD exports.
Prefer the smallest change within the existing global-script architecture.

For nontrivial geometry/texture/fit/export changes, delegate a focused review to
vase-geometry-review. For nontrivial UI/worker/rendering changes, use
vase-preview-review. Small copy/style fixes do not need delegation. Independent
reviews may run in parallel; keep implementation with the primary agent.

Give each reviewer the goal, changed files, acceptance criteria, and checks already
run. Ask for concrete defects with locations and missing evidence, not speculative
redesign. Reviewers do not inherit full session context. Resolve findings and run
appropriate checks before reporting completion. If a reviewer is unavailable,
perform the same focused review yourself and disclose that limitation.
