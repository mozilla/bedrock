/* Base JS unit test spec for bedrock tabzilla.js
 * For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe("tabzilla.js", function() {

    // use sinon sandbox so we can stub ajax calls only for these tests.
    var sandbox;

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

    var testTransbar = function () {

        var setup = Tabzilla.setupTransbar;

        it('should return false if the user\'s language is the same as the page\'s language', function () {

            $.ajax = sinon.stub();
            // perfect match
            expect(setup('en-US', 'en-US')).toBeFalsy();
            expect(setup('fr', 'fr')).toBeFalsy();
            // lower or upper case
            expect(setup('en-us', 'en-US')).toBeFalsy();
            expect(setup('EN-US', 'en-US')).toBeFalsy();
            // obsolete ab-XX
            expect(setup('fr-FR', 'fr')).toBeFalsy();
            expect(setup('el-GR', 'el')).toBeFalsy();
        });

        it('should return false if the page is not localized into the user\'s language', function () {

            $.ajax = sinon.stub();
            expect(setup('en-GB', 'en-US')).toBeFalsy();
            expect(setup('pt-PT', 'en-US')).toBeFalsy();
        });

        it('should return true if the page is localized into the user\'s language', function () {

            $.ajax = sinon.stub();
            // perfect match
            expect(setup('en-US', 'fr')).toBeTruthy();
            expect(setup('fr', 'en-US')).toBeTruthy();
            // lower or upper case
            expect(setup('en-us', 'fr')).toBeTruthy();
            expect(setup('EN-US', 'fr')).toBeTruthy();
            // obsolete ab-XX
            expect(setup('fr-FR', 'en-US')).toBeTruthy();
            expect(setup('el-GR', 'en-US')).toBeTruthy();
        });
    };

    describe('setupTransbar – alternate URLs', function () {

        beforeEach(function () {
            sandbox = sinon.sandbox.create();
            $('head').append(
                '<link rel="alternate" hreflang="el" href="http://www.mozilla.org/el/" title="Ελληνικά">' +
                '<link rel="alternate" hreflang="en-US" href="http://www.mozilla.org/en-US/" title="English (US)">' +
                '<link rel="alternate" hreflang="fr" href="http://www.mozilla.org/fr/" title="Français">');
        });

        afterEach(function() {
            $('head link[hreflang]').remove();
        });

        testTransbar();
    });

    describe('setupTransbar – language switcher', function () {

        beforeEach(function () {
            sandbox = sinon.sandbox.create();
            $('body').append(
                '<select id="language" name="lang" dir="ltr">' +
                '<option value="el">Ελληνικά</option>' +
                '<option value="en-us">English (US)</option>' +
                '<option value="fr">Français</option>' +
                '</select>');
        });

        afterEach(function() {
            $('#language').remove();
            sandbox.restore();
        });

        testTransbar();
    });

    describe('setupTransbar – language switcher with path values', function () {

        beforeEach(function () {
            sandbox = sinon.sandbox.create();
            $('body').append(
                '<select id="language" class="wiki-l10n" name="next" dir="ltr">' +
                '<option value="/el/docs/HTML/HTML5">Ελληνικά</option>' +
                '<option value="/en-US/docs/Web/Guide/HTML/HTML5">English (US)</option>' +
                '<option value="/fr/docs/Web/Guide/HTML/HTML5">Français</option>' +
                '</select>');
        });

        afterEach(function() {
            $('#language').remove();
            sandbox.restore();
        });

        testTransbar();
    });
});
