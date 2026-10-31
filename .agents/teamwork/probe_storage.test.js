// @vitest-environment happy-dom
import { describe, it } from 'vitest';

describe('Probe happy-dom storage', () => {
  it('inspects localStorage methods and prototype', () => {
    console.log('--- PROBE START ---');
    console.log('typeof window.localStorage:', typeof window.localStorage);
    console.log('typeof window.localStorage.setItem:', typeof window.localStorage.setItem);
    console.log('localStorage keys:', Object.getOwnPropertyNames(window.localStorage));
    console.log('proto keys:', Object.getOwnPropertyNames(Object.getPrototypeOf(window.localStorage)));
    console.log('Storage.prototype === proto:', Storage.prototype === Object.getPrototypeOf(window.localStorage));
    console.log('window.localStorage === localStorage:', window.localStorage === localStorage);
    
    // Test overriding window.localStorage.setItem directly
    const orig = window.localStorage.setItem;
    let called = false;
    window.localStorage.setItem = function(...args) {
      called = true;
      return orig.apply(this, args);
    };
    window.localStorage.setItem('probe_key', 'probe_val');
    console.log('called override on instance?', called);

    // Test overriding Object.getPrototypeOf(window.localStorage).setItem
    const protoOrig = Object.getPrototypeOf(window.localStorage).setItem;
    let protoCalled = false;
    Object.getPrototypeOf(window.localStorage).setItem = function(...args) {
      protoCalled = true;
      return protoOrig.apply(this, args);
    };
    window.localStorage.setItem('probe_key2', 'probe_val2');
    console.log('called override on proto?', protoCalled);
    console.log('--- PROBE END ---');
  });
});
