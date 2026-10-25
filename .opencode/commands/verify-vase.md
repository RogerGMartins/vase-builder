---
description: Verify the current Vase Builder changes and report evidence without fixing them.
agent: vase-dev
---

Verify the current changes, with this optional focus: $ARGUMENTS

Read AGENTS.md, inspect git status and diff, and identify affected contracts.
Do not edit source or silently fix failures. For documentation/OpenCode-only
changes, run the hygiene audit and check file references and OpenCode discovery.
For code changes, build then run the extended suite once. If scaffold inputs
changed, let --check identify staleness; do not regenerate the tracked asset.
Generated ignored test/build artifacts are expected.

Request the relevant focused review subagent(s) for nontrivial changes. Perform
real-browser checks for UI/render changes when tools are available. Report
commands and results, concrete findings with locations, and missing browser,
slicer or physical evidence separately. If no diff exists, ask what baseline or
scope to verify before running expensive checks. Do not commit or publish.
