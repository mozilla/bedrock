/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn */

describe('utils.js', function() {

    'use strict';

    var macUA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:36.0) Gecko/20100101 Firefox/36.0';
    var winUA = 'Mozilla/5.0 (Windows NT 6.1; rv:36.0) Gecko/20100101 Firefox/36.0';
    var linUA = 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0';
    var knownVersions = [];

    // set some variable values used by the below tests.
    beforeEach(function () {
        // simplified knownVersions array for testing
        knownVersions = [
            { version: '7.6.6', status: 'outdated' },
            { version: '7.6.6.0', status: 'outdated' },
            { version: '7.6.9', status: 'outdated' },
            { version: '7.7.1', status: 'latest' }
        ];
    });

    it('should return mac', function() {
        var os = Utils.getOS(macUA);
        expect(os).toBe('mac');
    });

    it('should return win', function() {
        var os = Utils.getOS(winUA);
        expect(os).toBe('win');
    });

    it('should return lin', function() {
        var os = Utils.getOS(linUA);
        expect(os).toBe('lin');
    });

    it('should return plugin info object for a match', function() {
        var match = Utils.isMatch('7.7.1', knownVersions);
        expect('latest').toBe(match.status);
    });

    it('should return false for non match', function() {
        var match = Utils.isMatch('7.6.9.1', knownVersions);
        expect(match).toBe(false);
    })
});
