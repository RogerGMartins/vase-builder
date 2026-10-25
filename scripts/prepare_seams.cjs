/* SPDX-License-Identifier: CC0-1.0 */
'use strict';
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
for (const name of ['base', 'tray', 'core']) {
  vm.runInThisContext(fs.readFileSync(path.join(root, 'src', name + '.js'), 'utf8'));
}
const data = JSON.parse(fs.readFileSync(path.join(root, 'assets/mesh-data.json'), 'utf8'));
const output = {};
for (const kind of ['end', 'middle']) {
  const mesh = PlanterCore.prepareSeamSource(data[kind + '_fixed'], kind, true);
  output[kind + '_fixed'] = {
    regularSurface: true, previewOnly: true, v: mesh.v, f: mesh.f,
    outer: mesh.outer, holes: mesh._drains.holes, removed: [...mesh._drains.removed]
  };
  console.log(kind, mesh.v.length, mesh.f.length);
}
fs.mkdirSync(path.join(root, 'dist'), {recursive: true});
fs.writeFileSync(path.join(root, 'dist/seam-data.json'), JSON.stringify(output));
