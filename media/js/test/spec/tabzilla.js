/* Base JS unit test spec for bedrock tabzilla.js
 * For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe("tabzilla.js", function() {

    describe("compareVersion", function () {

        it("should return 1 if jQuery does meet the minimum required version", function () {
            var result1 = Tabzilla.compareVersion('1.10.0', '1.7.1');
            var result2 = Tabzilla.compareVersion('1.9', '1.7.1');
            var result3 = Tabzilla.compareVersion('2', '1.7.1');
            expect(result1).toEqual(1);
            expect(result2).toEqual(1);
            expect(result3).toEqual(1);
        });

        it("should return -1 if jQuery does not meet the minimum required version", function () {
            var result1 = Tabzilla.compareVersion('1.6.1', '1.7.1');
            var result2 = Tabzilla.compareVersion('1.5', '1.7.1');
            var result3 = Tabzilla.compareVersion('1', '1.7.1');
            var result4 = Tabzilla.compareVersion('0.10', '1.7.1');
            expect(result1).toEqual(-1);
            expect(result2).toEqual(-1);
            expect(result3).toEqual(-1);
            expect(result4).toEqual(-1);
        });

        it("should return 0 if jQuery versions are the same", function () {
            var result1 = Tabzilla.compareVersion('1.7.1', '1.7.1');
            var result2 = Tabzilla.compareVersion('0.10', '0.10');
            var result3 = Tabzilla.compareVersion('1', '1');
            expect(result1).toEqual(0);
            expect(result2).toEqual(0);
            expect(result3).toEqual(0);
        });
    });
});
