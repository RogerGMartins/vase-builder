"""Run portable local checks. No package installation or network access required."""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*command, timeout=900):
    print('+', ' '.join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True, timeout=timeout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extended', action='store_true')
    args = parser.parse_args()
    run(sys.executable, 'scripts/audit.py')
    for file in sorted((ROOT / 'src').glob('*.js')):
        run('node', '--check', str(file.relative_to(ROOT)))
    run(sys.executable, 'scripts/parse_dom.py')
    run('node', 'tests/controls.cjs')
    run('node', 'tests/renderer.cjs')
    run('node', '--max-old-space-size=4096', 'tests/geometry.cjs')
    run(sys.executable, 'tests/test_build.py')
    if args.extended:
        run('node', '--max-old-space-size=4096', 'tests/worker.cjs')
        run('node', '--max-old-space-size=4096', 'tests/watchdog.cjs')
        run('node', '--max-old-space-size=4096', 'tests/watchdog.cjs', 'fail')
        run(sys.executable, 'scripts/regenerate_seams.py', '--check')
    print('All requested checks passed.')
