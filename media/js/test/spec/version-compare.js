/* Base JS unit test spec for bedrock plugincheck/lib/version-comapre.js
 * For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe("version-compare.js", function() {
    it('should match', function() {
        var match = versionCompare('1.0.0.2', '1.0.0.2');
        expect(!match).toBe(true);
    });

    it('should not match', function() {
        var match = versionCompare('1.0.0.2', '1.0.1.2');
        expect(!match).toBe(false);
    });

    // this ignores things such as beta, a, b
    it('should be true', function() {
        var match = versionCompare('1.0.0.2b', '1.0.0.2a');
        expect(!match).toBe(true);
    });

    // different version length i.e 1.2 compared to 1.2.3
    it('should be true', function() {
        var match = versionCompare('1.0.2', '1.0.2.3');
        expect(!match).toBe(false);
    });

    // different version length i.e 1.2 compared to 1.2.3
    it('second version should be greater', function() {
        var match = versionCompare('1', '1.2');
        expect(match).toBeLessThan(0);
    });

    it('first version should be greater', function() {
        var match = versionCompare('1.0.3', '1.0.0');
        expect(match).toBeGreaterThan(0);
    });

    // this takes into account things such as beta, a, b
    it('should not match lexicographical', function() {
        var match = versionCompare('1.0.0.2b', '1.0.0.2a', {
            lexicographical: true
        });
        var matchBeta = versionCompare('1.0.0.2beta', '1.0.0.2alpha', {
            lexicographical: true
        });
        expect(!match).toBe(false);
        expect(!matchBeta).toBe(false);
    });
});
