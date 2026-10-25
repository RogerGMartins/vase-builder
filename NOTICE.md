# Provenance and dependency inventory

The project already carried a CC0-1.0 dedication before this publication preparation.
That dedication is retained, with the full legal text in LICENSE:
https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt

## Included materials

| Material | Origin and status |
| --- | --- |
| JavaScript, HTML and CSS | Existing project implementation; original geometry and export code carry CC0 notices. |
| Template mesh data | Existing original project geometry. The included JSON is the canonical template input; no external model download is required. |
| Compressed preview scaffold | Derived from those templates with the included generator. |
| Build tools, tests and documentation | Project tooling, covered by the same dedication. |
| PNG geometry previews | Original project software renders; textual and EXIF metadata removed. No reference photographs or user-uploaded maps included. |

The upstream creative workflow used AI-assisted code/design work. Existing notices
and local provenance were reviewed; this inventory is not an independent legal
clearance of all possible third-party rights. CC0 does not waive patent or trademark
rights and only applies to rights the contributor can grant.

## Dependencies

There are **no vendored or package-managed third-party runtime or development
libraries**. `package.json` provides optional command aliases; its lockfile contains
only the root project. No package registry downloads are needed for local checks.

| Component | Role | Distributed with this repository? |
| --- | --- | --- |
| Browser WebGL, workers, image APIs, gzip decompression | Runtime platform | No |
| Python 3.12 standard library: pathlib, gzip, json, base64, etc. | Build and checks | No |
| Node.js 24 built-ins: fs, vm, assert, zlib, worker_threads | Geometry and worker tests | No |
| GitHub Actions checkout, setup-python and setup-node | Optional hosted CI | No; fetched by GitHub at pinned commit IDs |

Python, Node.js, the browser and GitHub-hosted actions retain their own licenses.
The CI actions are MIT-licensed projects; their source is linked from the pinned
`uses` entries in `.github/workflows/ci.yml`. They are not included in the app bundle.
External gardening/slicer guidance remains ordinary links; its content is not copied.
No external font, JavaScript CDN, analytics or telemetry client is bundled.

## Excluded from publication

Session/hosting metadata, existing Git directories and history, credentials,
machine-specific paths, reference photographs, concept renders, user settings and
height maps, historical STL/3MF exports, archives and old validation dumps are excluded.
Scans are heuristic and do not guarantee that every possible secret is detectable.

CI references reviewed against the official releases on 2026-10-25:
- [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1)
- [setup-node v7.1.0](https://github.com/actions/setup-node/releases/tag/v7.1.0)
- [setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0)

They are pinned to their release commit IDs. This review does not assert that
all transitive dependencies of the hosted actions are vulnerability-free.
