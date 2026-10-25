/* SPDX-License-Identifier: CC0-1.0 */
'use strict';
const fs = require('node:fs'), vm = require('node:vm');
const assert = require('node:assert/strict'), zlib = require('node:zlib');
for (const file of ['base', 'tray', 'core']) vm.runInThisContext(fs.readFileSync('src/' + file + '.js', 'utf8'));
const C = PlanterCore;
const data = JSON.parse(fs.readFileSync('assets/mesh-data.json', 'utf8'));
for (const [kind, seam] of Object.entries(JSON.parse(zlib.gunzipSync(fs.readFileSync('assets/seam-data.json.gz'))))) {
  data[kind].seamPrepared = seam;
}
function topology(mesh) {
  const edges = new Map();
  for (const face of mesh.f) {
    const [a,b,c] = face.map(i => mesh.v[i]);
    assert([...a,...b,...c].every(Number.isFinite));
    const u = b.map((x,i) => x-a[i]), v = c.map((x,i) => x-a[i]);
    assert(Math.hypot(u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]) > 2e-9);
    for (let j=0; j<3; j++) {
      const a=face[j], b=face[(j+1)%3], key=a<b?a+','+b:b+','+a;
      const entry=edges.get(key)||[0,0]; entry[0]++;entry[1]+=a<b?1:-1;edges.set(key,entry);
    }
  }
  assert([...edges.values()].every(([count,winding]) => count===2 && winding===0));
  C.validate(mesh);
}
assert.throws(() => C.normalize({...C.defaults, rimBand:0}));
for (const contrast of [1,4,6]) {
  const c = C.normalize({...C.defaults, pattern:'mineral', contrast, surfaceSoftness:0});
  const pitch=C.modulePitch(c); let flat=0, samples=0;
  for (let z=40; z<100; z+=1.3) for (let s=0; s<pitch; s+=1.3) {
    const value=C.sampleTexture(c,s,z);
    assert(Number.isFinite(value) && value>0 && value<1);
    const gradient=Math.hypot(C.sampleTexture(c,s+.02,z)-value,C.sampleTexture(c,s,z+.02)-value)/.02;
    if (gradient<1e-5) flat++;samples++;
    assert(Math.abs(value-C.sampleTexture(c,s+pitch,z))<1e-7);
  }
  assert(flat/samples<.005, 'Mineral has flat background patches');
}
for (const shape of ['capsule','rounded','rectangle','faceted']) {
  const c=C.normalize({...C.defaults,shape});
  assert(C.fit(c).ok);
}
for (const [baseMode,pattern,kind] of [
  ['none','mineral','end'], ['stacked','mineral','middle'],
  ['stacked','waves','end'], ['stacked','voronoi','middle']
]) {
  const c=C.normalize({...C.defaults,baseMode,pattern,contrast:6,depth:4,rimBand:.2,previewOnly:true});
  const mesh=C.makeMesh(data,kind,c);topology(mesh);
  console.log('Closed/wound/nondegenerate:',kind,baseMode,pattern,mesh.f.length,'triangles');
}
const tray=C.makeBaseMesh('tray_middle',C.normalize({...C.defaults,baseMode:'stacked'}));topology(tray);
const test=C.export3mf(data,C.normalize(C.defaults),['mineral'],true);
assert.equal(test.plates.length,1);
assert(test.plates[0].objects.length>=5);
fs.writeFileSync('dist/test-fit.3mf',test.bytes);
console.log('Mineral coverage, periodicity, bounds, trays and one-plate 3MF export passed.');
