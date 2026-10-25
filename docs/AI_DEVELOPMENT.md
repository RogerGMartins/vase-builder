# Developing with OpenCode

## Start here

Open OpenCode from the repository root. **Quit and restart OpenCode after adding
or editing these definitions**; the current session retains its loaded agents,
commands and skills. This setup targets the installed OpenCode **1.19.x** format.
When upgrading to v2, re-check permission and agent syntax before migrating.

No plugin, dependency, API key, project model pin, or MCP installation is added.
Markdown agents, commands and skills are discovered automatically. Your existing
provider/model/tool configuration remains the source of those choices. `AGENTS.md`
also applies when using the built-in Build or Plan agents.

## What is included

| File or component | Purpose |
| --- | --- |
| `AGENTS.md` | Always-loaded repo map, constraints and test selection |
| `.opencode/agents/vase-dev.md` | Primary implementation agent; select it in OpenCode |
| `vase-geometry-review` | Read-only subagent for geometry, continuity, fit and exports |
| `vase-preview-review` | Read-only subagent for UI, settings, workers and rendering |
| `.opencode/skills/vase-geometry/SKILL.md` | On-demand geometry/export contracts and regression workflow |
| `.opencode/skills/vase-preview/SKILL.md` | On-demand UI/preview contracts and browser workflow |
| `.opencode/skills/vase-architecture/SKILL.md` | JavaScript/Python boundaries, state, errors, resource ownership and reproducible tooling |
| `vase-geometry/references/printing.md` | Printer-dependent design criteria and slicer/physical acceptance |
| `vase-geometry/references/openscad.md` | Snapshot conventions, CAD practices and OpenSCAD round-trip checks |
| `/develop <task>` | Routes a scoped implementation task to vase-dev |
| `/verify-vase [focus]` | Checks current changes without source fixes |

The reviewers have file edits and general shell execution denied; status/diff/log
are allowed. Their instructions prohibit artifact-writing tests and external-tool
mutations. The primary agent runs checks and supplies evidence. They are review
specialists, not duplicate implementation workers; ordinary small edits do not
need child sessions.

## Everyday workflow

1. **Describe the behavior.** Include current versus expected behavior, a sanitized
   settings example and acceptance criteria where useful. Avoid private image data.
2. **Plan when needed.** Use built-in Plan for ambiguous or large changes. Ask it to
   identify affected source, risks and a small first slice. Small fixes can go
   straight to `/develop`.
3. **Implement.** `vase-dev` reads relevant contracts, edits source, and adds focused
   coverage in existing tests. It delegates independent reviews for substantial work.
4. **Verify.** Build before tests. Extended checks cover real workers, watchdogs and
   scaffold reproducibility. Browser checks cover what the doubles cannot. Use
   `/verify-vase` for a separate final pass, avoiding redundant checks within a task.
5. **Review the handoff.** Require changed behavior, commands/results and outstanding
   acceptance gaps. Commit/push/release remain explicit user actions.

Examples:

```text
/develop Fix stale preview geometry after rapidly changing tray style and width.
/develop Add a texture control while preserving existing saved designs and module seams.
/verify-vase Check fit-test plate export and saved-settings compatibility.
```

For a targeted review, mention `@vase-geometry-review` or `@vase-preview-review`
with the relevant diff, intended behavior and test evidence. Reviewers report
findings; ask `vase-dev` to apply agreed corrections.

## Why these skills

The architecture skill codifies the shared JavaScript/Python engineering rules.
Two domain skills cover physical geometry and asynchronous preview/UI behavior.
Export belongs with geometry because fit estimates, mesh generation and plate
packing must agree. Printing and OpenSCAD details are on-demand references inside
that skill; they do not require additional agents. Build/test commands remain in
`AGENTS.md` and the existing development notes.

Architecture guidance applies to changed code, not an unsolicited wholesale
refactor. Printing guidance distinguishes design targets from printer/material
calibration; OpenSCAD guidance distinguishes snapshot export from parametric CAD.
These instructions guide reviews but are not mechanical enforcement: regression
tests, real rendering, slicer inspection and physical checks provide the evidence.

Generic framework skills, separate agents for every file, custom plugins and a
second task-management system add no current capability. The globally available
`customize-opencode` skill is appropriate when changing this setup; it is not an
application-development skill. Ponytail guidance fits the dependency-free design.
PRD/Ralph skills are optional only if you choose that task-orchestration workflow.
No third-party skill installation is needed for this baseline.

Optional tools: documentation lookup for API questions and browser automation for
real UI checks. Blender, slicers and printer tools are not required to build or
test this app. Slicer/physical evidence may still be needed for specific geometry
acceptance; availability must never be confused with permission to start a print.

## Maintaining the setup

- Update the relevant skill when a contract or its test workflow changes; keep
  general product documentation in README/development notes rather than duplicating it.
- Check discovery with `opencode agent list` and `opencode debug skill`.
  Check that `/develop` and `/verify-vase` appear after restarting.
- Run `python scripts/audit.py` for guidance-only changes. A geometry suite run
  adds no evidence about Markdown agent configuration.
- Do not commit resolved global configuration/debug dumps: they may contain local
  paths, provider details or secrets. Keep project guidance portable.
