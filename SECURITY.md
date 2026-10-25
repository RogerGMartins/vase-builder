# Security and privacy

The current source runs locally with no telemetry or application network client.
Images are decoded locally; settings are stored in browser localStorage and can be
exported as JSON. Custom height maps can be included in exported settings and 3MF
metadata. Review those files before sharing them.

Treat imported files as untrusted. Large or extreme configurations can consume
substantial memory and block exports, which are currently synchronous. The tool
is not a sandbox for arbitrary code. Use a maintained browser and do not open
unknown modified app bundles. A local development server should bind to loopback.

After the repository is published, use GitHub's private vulnerability reporting
feature if the maintainer has enabled it. Otherwise, open a minimal issue asking
for a private contact route without disclosing an exploit or secret. No monitored
private email address or response-time commitment is claimed here.

Only the current default branch is maintained at this stage. Security fixes should
include a regression test and a review of generated HTML and exports. The local
scanner detects common token formats and personal paths; it is not a full security
audit, package vulnerability service or assurance of physical print safety.
