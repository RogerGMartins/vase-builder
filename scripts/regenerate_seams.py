"""Regenerate the checked-in preview scaffold; requires Node.js on PATH."""
from pathlib import Path
import argparse
import subprocess
from build import ROOT, deterministic_gzip

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify without modifying the asset')
    args = parser.parse_args()
    subprocess.run(['node', '--max-old-space-size=4096',
                    str(ROOT / 'scripts/prepare_seams.cjs')], cwd=ROOT, check=True)
    raw = (ROOT / 'dist/seam-data.json').read_bytes()
    compressed = deterministic_gzip(raw)
    target = ROOT / 'assets/seam-data.json.gz'
    if args.check:
        assert target.read_bytes() == compressed, 'Scaffold is stale: regenerate and commit it.'
        print('Scaffold matches its generator byte for byte.')
    else:
        target.write_bytes(compressed)
        print('Updated assets/seam-data.json.gz')
