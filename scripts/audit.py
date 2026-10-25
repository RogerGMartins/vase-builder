"""Local publication hygiene check; heuristic scanning is not a security guarantee."""
from pathlib import Path
import gzip
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'private key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'GitHub token': r'gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,}',
    'cloud access key': r'(?:AKIA|ASIA)[A-Z0-9]{16}',
    'credential URL': r'https?://[^\s/]+:[^\s/@]+@',
    'personal machine path': r'[A-Za-z]:[/\\]Users[/\\][A-Za-z0-9_.-]+|/Users/[A-Za-z0-9_.-]+',
    'assigned credential': r'''(?im)(?:api[_-]?key|password|client[_-]?secret|access[_-]?token)\s*[:=]\s*["'][A-Za-z0-9_+/=-]{20,}["']''',
}
bad = []
checked = 0
for path in sorted(ROOT.rglob('*')):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT)
    if any(part in {'.git', '__pycache__', 'node_modules'} for part in rel.parts):
        continue
    if any(part in {'.openai', '.codex', '.agents'} for part in rel.parts) or path.name.startswith('.env'):
        bad.append((str(rel), 'private file type'))
    raw = path.read_bytes()
    if path.suffix == '.gz':
        raw = gzip.decompress(raw)
    if path.suffix == '.png':
        for chunk in [b'tEXt', b'zTXt', b'iTXt', b'eXIf']:
            if chunk in raw:
                bad.append((str(rel), 'image metadata needs review'))
        continue
    try:
        text = raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        continue
    checked += 1
    for label, pattern in PATTERNS.items():
        if re.search(pattern, text):
            bad.append((str(rel), label))
    if path.suffix in {'.js', '.html'} and re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket|sendBeacon)\s*\(', text):
        bad.append((str(rel), 'unexpected network client'))
package = json.loads((ROOT / 'package.json').read_text(encoding='utf-8'))
assert not package.get('dependencies') and not package.get('devDependencies')
if bad:
    for name, label in bad:
        print(f'REVIEW {name}: {label}')  # Never print matched secret values.
    sys.exit(1)
print(f'Hygiene checks passed for {checked} text assets; zero third-party packages.')
