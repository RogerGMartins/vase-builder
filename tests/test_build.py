"""Check clean builds and exported ZIP structure without third-party libraries."""
from pathlib import Path
import base64
import gzip
import hashlib
import io
import json
import re
import subprocess
import sys
import time
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build import build

first = (ROOT / 'dist/index.html').read_bytes()
time.sleep(1.1)  # Catch accidental use of a current-time gzip header.
second = build()
assert first == second, 'The checked build differs from the current sources.'
match = re.search(rb'id="meshData"[^>]*>([^<]+)', first)
geometry = json.loads(gzip.decompress(base64.b64decode(match[1])))
assert geometry['end_fixed']['seamPrepared']['regularSurface']
assert geometry['middle_fixed']['seamPrepared']['previewOnly']
assert b'<!-- INLINE_SCRIPTS -->' not in first
assert b'Vase Builder' in first
with zipfile.ZipFile(ROOT / 'dist/test-fit.3mf') as archive:
    assert archive.testzip() is None
    model = ET.fromstring(archive.read('3D/3dmodel.model'))
    assert model.attrib['unit'] == 'millimeter'
    settings = json.loads(archive.read('Metadata/project_settings.config'))
    assert settings['wall_loops'] == '8'
    assert settings['sparse_infill_pattern'] == 'rectilinear'
print('Repeat build identical; embedded geometry and 3MF ZIP/XML/settings passed.')
print('HTML SHA-256:', hashlib.sha256(first).hexdigest())
