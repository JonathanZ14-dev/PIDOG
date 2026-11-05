// Optional: node tests/browser_core.test.js (Python lessons do not require Node).
const assert = require('assert');
const c = require('../browser-core.js');
assert.deepStrictEqual(c.rgbHSV(0,0,255), [2/3,1,1]);
for (const [rgb, expected] of [[[20,60,220],true],[[255,0,0],false],[[0,0,0],false],[[210,210,210],false]]) {
  assert.strictEqual(c.bluePixel(rgb), expected);
}
assert.strictEqual(c.markerStatus(.08,.5,.08), 'marker_present');
assert.strictEqual(c.markerStatus(.5,.05,.08), 'unknown');
assert.strictEqual(c.markerStatus(0,.5,.08), 'marker_absent');
console.log('8 browser-core assertions passed');
