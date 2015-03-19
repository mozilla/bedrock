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

        var setup = Tabzilla.infobar.translation;

        it('should return false if the user\'s language is the same as the page\'s language', function () {

            $.ajax = sinon.stub();
            expect(setup(['en-US'], 'en-US')).toBeFalsy();
            expect(setup(['en'], 'en-US')).toBeFalsy();
            expect(setup(['en-US', 'en', 'fr'], 'en-US')).toBeFalsy();
            expect(setup(['fr', 'de'], 'fr')).toBeFalsy();
            expect(setup(['de', 'fr', 'en'], 'fr')).toBeFalsy();
            expect(setup(['ja', 'pt-PT', 'el', 'fr', 'en'], 'el')).toBeFalsy();
            expect(setup(['en-ZA', 'en-GB', 'en'], 'en-GB')).toBeFalsy();
            // obsolete ab-XX
            expect(setup(['fr-FR'], 'fr')).toBeFalsy();
            expect(setup(['el-GR'], 'el')).toBeFalsy();
        });

        it('should return false if the page is not localized into the user\'s language', function () {

            $.ajax = sinon.stub();
            expect(setup(['en-GB'], 'en-US')).toBeFalsy();
            expect(setup(['en-GB', 'en'], 'en-US')).toBeFalsy();
            expect(setup(['pt-PT', 'pt'], 'fr')).toBeFalsy();
        });

        it('should return true if the page is localized into the user\'s language', function () {

            $.ajax = sinon.stub();
            expect(setup(['en-US'], 'fr')).toEqual('en-US');
            expect(setup(['en-US', 'en'], 'fr')).toEqual('en-US');
            expect(setup(['fr'], 'el')).toEqual('fr');
            expect(setup(['ar', 'fr'], 'el')).toEqual('fr');
            expect(setup(['de', 'fr', 'en'], 'en-US')).toEqual('fr');
            expect(setup(['de', 'el', 'fr', 'en-US'], 'fr')).toEqual('el');
            expect(setup(['el', 'en-US'], 'en-US')).toEqual('el');
            // obsolete ab-XX
            expect(setup(['fr-FR'], 'en-US')).toEqual('fr');
            expect(setup(['el-GR'], 'fr')).toEqual('el');
        });
    };

    describe('infobar.translation – alternate URLs', function () {

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

    describe('infobar.translation – language switcher', function () {

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

    describe('infobar.translation – language switcher with path values', function () {

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

    describe("infobar.update", function () {

        var setup = function (ua, buildID) {
            // Test a case where the latest version is a non-dot release
            var result1 = Tabzilla.infobar.update('35.0', ua, buildID);

            // Cleanup
            $('#tabzilla-infobar').remove();

            // Test a case where the latest version is a dot release
            var result2 = Tabzilla.infobar.update('35.0.1', ua, buildID);

            // Cleanup
            $('#tabzilla-infobar').remove();

            return result1 && result2;
        }

        it('should return false if the user agent is not Firefox', function () {
            expect(setup('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')).toBeFalsy();
            expect(setup('Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; en; rv:1.9.2.24) Gecko/20111114 Camino/2.1 (like Firefox/3.6.24)')).toBeFalsy();
            expect(setup('Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1')).toBeFalsy();
            expect(setup('Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36')).toBeFalsy();
        });

        it('should return false if the user agent is a latest Firefox version', function () {
            expect(setup('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:39.0) Gecko/20100101 Firefox/39.0')).toBeFalsy();
            expect(setup('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0')).toBeFalsy();
            expect(setup('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:34.0) Gecko/20100101 Firefox/34.0')).toBeFalsy();
        });

        it('should return false if the user agent is Firefox for mobile', function () {
            // Nokia N900 Linux mobile, on the Fennec browser
            expect(setup('Mozilla/5.0 (Maemo; Linux armv7l; rv:10.0) Gecko/20100101 Firefox/10.0 Fennec/10.0')).toBeFalsy();
            // Android phone and tablet
            expect(setup('Mozilla/5.0 (Android; Mobile; rv:26.0) Gecko/26.0 Firefox/26.0')).toBeFalsy();
            expect(setup('Mozilla/5.0 (Android; Tablet; rv:26.0) Gecko/26.0 Firefox/26.0')).toBeFalsy();
            // Firefox OS phone and tablet
            expect(setup('Mozilla/5.0 (Mobile; rv:26.0) Gecko/26.0 Firefox/26.0')).toBeFalsy();
            expect(setup('Mozilla/5.0 (Tablet; rv:26.0) Gecko/26.0 Firefox/26.0')).toBeFalsy();
        });

        it('should return false if the user agent is Firefox ESR', function () {
            // Firefox 31 ESR
            expect(setup('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:31.0) Gecko/20100101 Firefox/31.0', '20140717132905')).toBeFalsy();
            // Firefox 31.4.0 ESR
            expect(setup('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:31.0) Gecko/20100101 Firefox/31.0', '20150105205548')).toBeFalsy();
        });

        it('should return true if the user agent is an outdated Firefox version', function () {
            expect(setup('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20100101 Firefox/22.0')).toBeTruthy();
            expect(setup('Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1')).toBeTruthy();
            expect(setup('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9')).toBeTruthy();
            // Firefox 31 non-ESR
            expect(setup('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:31.0) Gecko/20100101 Firefox/31.0', '20140716183446')).toBeTruthy();
        });

    });
});
