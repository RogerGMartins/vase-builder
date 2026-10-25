# Contributing

Start with an issue describing the user-visible problem and a minimal reproduction.
For a change, create a branch, edit `src/`, build, and run the test suites documented
in README.md. This project uses plain JavaScript and Python standard-library tools.
Keep new dependencies justified and document their license and update policy.

For geometry changes, attach sanitized settings and before/after images. Check
closed edges, winding, finite coordinates, nondegenerate faces, print bounds,
texture continuity and connector clearances. Regenerate the scaffold if its source
changes. Identify whether evidence is a software render, browser view, slicer result
or actual print; do not conflate them.

For UI changes, test mouse, keyboard, numeric entry, collapsed sections and error
states. Run a real-browser visual check in addition to the automated doubles.
Respect existing configuration keys and compatibility with saved designs.

Do not commit generated exports, personal settings, reference images, credentials
or local machine paths. Run `python scripts/audit.py` before proposing changes.
New code and original assets must be compatible with the project's CC0-1.0
dedication. Document third-party provenance before adding an asset.
