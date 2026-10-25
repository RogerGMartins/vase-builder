"""Build the offline app using only Python's standard library."""
from pathlib import Path
import argparse
import base64
import gzip
import hashlib
import io
import json

ROOT = Path(__file__).resolve().parents[1]
MODULES = ['base', 'tray', 'core', 'preview', 'mesh-worker', 'assembly', 'app', 'ux']


def deterministic_gzip(data):
    buffer = io.BytesIO()
    with gzip.GzipFile(filename='', mode='wb', fileobj=buffer,
                       compresslevel=9, mtime=0) as stream:
        stream.write(data)
    return buffer.getvalue()


def build():
    geometry = json.loads((ROOT / 'assets/mesh-data.json').read_text(encoding='utf-8'))
    seams = json.loads(gzip.decompress((ROOT / 'assets/seam-data.json.gz').read_bytes()))
    for kind, seam in seams.items():
        geometry[kind]['seamPrepared'] = seam
    raw = json.dumps(geometry, separators=(',', ':')).encode('utf-8')
    encoded = base64.b64encode(deterministic_gzip(raw)).decode('ascii')
    modules = {name: (ROOT / 'src' / (name + '.js')).read_text(encoding='utf-8')
               for name in MODULES}
    worker = '\n'.join(modules[name] for name in MODULES[:5])
    scripts = ('globalThis.CapsuleMeshWorkerSource=' + json.dumps(worker) + ';\n'
               + '\n'.join(modules.values()))
    html = (ROOT / 'src/index.template.html').read_text(encoding='utf-8')
    guide = ('<section class="assembly-wrap"><details id="assemblyGuide">'
             '<summary>Assembly · illustrated steps and your parts list</summary>'
             '<div class="assembly-body" id="assemblyContent"></div></details></section>')
    assert html.count('<!-- ASSEMBLY_GUIDE -->') == 1
    assert html.count('<!-- INLINE_SCRIPTS -->') == 1
    html = html.replace('<!-- ASSEMBLY_GUIDE -->', guide)
    html = html.replace('<!-- INLINE_SCRIPTS -->',
                        '<script id="meshData" type="application/octet-stream">'
                        + encoded + '</script>\n<script>'
                        + scripts.replace('</script', '<\\/script') + '</script>')
    return html.encode('utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/index.html')
    args = parser.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(result)
    print(f'Built {len(result):,} bytes; SHA-256 {hashlib.sha256(result).hexdigest()}')
