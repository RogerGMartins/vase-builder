---
name: vase-architecture
description: Use when implementing or reviewing Vase Builder JavaScript or Python logic, module boundaries, state ownership, build tooling, serialization, or architectural refactoring.
---

# JavaScript and Python architecture

Apply these rules to changed code. They are not an instruction to rewrite legacy
code, reformat dense modules, or introduce abstractions without a concrete need.
Read AGENTS.md and the affected implementation/tests first. Use vase-geometry or
vase-preview as well when those domains are affected.

## Boundaries and dependency direction

- Keep geometry/configuration calculations independent of DOM, localStorage,
  downloads, and browser event handling. `PlanterCore` consumes data/configuration;
  `app.js` coordinates side effects. Base/tray modules own their geometry; preview
  owns drawing; assembly owns guide generation. Do not make core call app code.
- Preserve global-script APIs and load order. Keep helpers private to their
  owning closure unless another module actually needs them. Extend the existing
  exported object deliberately; avoid new mutable globals and circular dependencies.
- Share calculations between preview and export through core rather than copying
  formulas into UI/worker code. Keep assembly placement separate from plate layout.
- Factor a small named function when it isolates a real invariant, complex branch,
  or reused operation. Do not add service/repository layers, factories, classes,
  or generic configuration systems for single-use behavior.
- When adding a module, update `scripts/build.py` and both page/worker dependency
  paths explicitly. Worker-loaded code must not touch DOM APIs at module load.
  Retain offline `file://` behavior and the self-contained HTML artifact.

## JavaScript practices

- Prefer `const`, with `let` for reassignment; explicit parameters and return values
  over ambient state. Name units and coordinate frames where ambiguous. Document
  why a tolerance, transform, or cache exclusion exists, not what syntax does.
- Normalize external configuration at entry points. Validate finite numbers,
  enum membership, array sizes and indices before expensive allocation/geometry.
  Avoid truthiness defaults when zero is valid. Preserve legacy import semantics.
- Keep application configuration owned by app; make derived state recomputable.
  Do not let render quality, worker retries, or caches mutate saved/export settings.
- Treat cached templates, meshes and image maps as shared. Clone at mutation
  boundaries, not indiscriminately inside hot loops. Cache keys must include every
  relevant input; retain bounded memory and explicit invalidation behavior.
- Prefer pure deterministic calculations for geometry and serialization. Keep
  user-triggered randomness separate from deterministic rebuild/export paths.
- Handle promise failures at the boundary that can show an actionable error.
  Use `finally` for resource cleanup and restoring controls. Empty catches belong
  only to genuinely optional operations with a defined fallback (such as storage).
- Pair acquisition with cleanup: workers, timers, object URLs, image bitmaps,
  listeners and GPU buffers. Preserve request IDs/epochs and cancellation semantics.
- Use `textContent` for untrusted text. Validate/escape at HTML, XML and generated
  source boundaries; JSON serialization alone is not escaping for every context.
  Keep import limits and inline-script closing-tag escaping in the build.
- Use typed arrays where they match the existing packed-buffer contract. Measure
  before optimizing; do not trade topology or selected quality for a faster preview.

## Python tooling practices

- Python is build/test tooling here, not a second geometry implementation. Prefer
  the standard library and reuse existing deterministic compression/build functions.
- Separate reusable computation from CLI orchestration, following `build()` and
  its `if __name__ == '__main__'` entry point. New reusable modules should not write
  files, launch subprocesses or parse arguments on import. Do not refactor existing
  script-only entry points merely to satisfy a template.
- Resolve repo inputs from `Path(__file__)`, not the caller's working directory.
  Use explicit UTF-8, stable ordering and deliberate newline/serialization behavior.
  Do not embed machine paths, timestamps or nondeterministic gzip headers.
- Use `argparse` for meaningful CLI options, `subprocess.run` with argument lists,
  explicit `cwd`, `check=True`, and bounded timeouts where appropriate. Avoid
  `shell=True`; propagate failures with nonzero exit status and useful context.
- Use `sys.executable` for child Python processes when inheriting the interpreter.
  Respect the documented Python 3.12/Node 24 baseline; do not silently install or
  upgrade tools. Report interpreter/version mismatches and their impact on evidence.
- Validate inputs and finish generation before replacing valuable output. For new
  multi-step writes to tracked/user-owned files, prefer a temporary sibling and
  atomic replace; clean up on failure. Disposable generated files need no elaborate
  transaction framework. A check mode must not overwrite the tracked artifact.
- Use exceptions/explicit checks for new external-input and CLI failure paths;
  assertions are for internal invariants/tests and can be disabled with optimization.
  Preserve causes when wrapping exceptions; never swallow a failed build.

## Architecture review and checks

For a new setting, trace defaults → normalization → controls/import/persistence →
cache keys → worker/preview → export/fit → assembly guidance as applicable.
For a refactor, state the boundary improved and preserve public behavior and data
formats. Change compatibility deliberately, with a migration only when requested.

Add a focused regression to the existing suite for nontrivial behavior. Prefer
observable results over implementation-shaped assertions; use the existing DOM/GL
doubles for their intended scope and real-browser checks for visual behavior.
Test failure paths relevant to the change, including malformed inputs or stale jobs.
Keep diagnostics and fixtures synthetic; avoid personal designs and image payloads.

Build first, then follow AGENTS.md's test selection. Build/toolchain changes need
the extended suite and reproducibility checks. Do not add dependencies, another
runner, or a benchmark harness without a demonstrated requirement. If API behavior
is uncertain, consult version-appropriate official documentation using available
documentation tools rather than encoding a guess in the architecture.
