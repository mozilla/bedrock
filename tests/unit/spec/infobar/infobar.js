/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn */

describe('infobar.js', function() {

    'use strict';

    describe('InfoBar.prototype.getLanguageBidi', function () {
        it('should return true for a rtl language', function() {
            expect(InfoBar.prototype.getLanguageBidi('he')).toBeTruthy();
        });

        it('should return false for a ltr language', function() {
            expect(InfoBar.prototype.getLanguageBidi('en-US')).toBeFalsy();
        });
    });

    describe('InfoBar.prototype.normalize', function () {
        it('should return en-US when en-us is specified', function() {
            expect(InfoBar.prototype.normalize('en-us')).toBe('en-US');
        });

        it('should return ca when CA is specified', function() {
            expect(InfoBar.prototype.normalize('CA')).toBe('ca');
        });
    });

    describe('InfoBar.prototype.getAvailableLangs - hreflang', function () {

        beforeEach(function() {
            var hreflangLinks = [
                '<link rel="alternate" hreflang="es-ES" href="http://www.mozilla.org/es-ES/firefox/new/" />',
                '<link rel="alternate" hreflang="fr" href="http://www.mozilla.org/fr/firefox/new/" />'
            ].join();

            $(hreflangLinks).appendTo('head');
        });

        afterEach(function() {
            $('link[hreflang]').remove();
        });

        it('should populate the availableLangs object with two elements', function() {
            var availableLangs = InfoBar.prototype.getAvailableLangs();
            expect(Object.keys(availableLangs).length).toBe(2);
        });

        it('should have es-ES entry in availableLangs array', function() {
            var availableLangs = InfoBar.prototype.getAvailableLangs();
            expect(availableLangs['es-ES']).toBeDefined();
        });
    });

    describe('InfoBar.prototype.getAvailableLangs - language selector', function() {

        beforeEach(function() {
            var select = [
                '<select id="page-language-select" name="lang" dir="ltr">',
                  '<option value="es-ES" lang="es-ES">Español (de España)</option>',
                  '<option value="fr" lang="fr">Français</option>',
                 '</select>'
            ].join();

            $(select).appendTo('body');
        });

        afterEach(function() {
            $('#page-language-select').remove();
        });

        it('should populate the availableLangs object with two elements', function() {
            var availableLangs = InfoBar.prototype.getAvailableLangs();
            expect(Object.keys(availableLangs).length).toBe(2);
        });

        it('should have fr entry in availableLangs', function() {
            var availableLangs = InfoBar.prototype.getAvailableLangs();
            expect(availableLangs['fr']).toBeDefined();
        });
    });

    describe('InfoBar.prototype.getAvailableLangs - no translations', function() {
        it('should return false if no alternate translations exist', function() {
            var isAvailableLangs = InfoBar.prototype.getAvailableLangs();
            expect(isAvailableLangs).toBeFalsy();
        });
    });

    describe('InfoBar.prototype.userLangPageLangMatch', function() {
        it('should return true if the accept language match the page language', function() {
            var acceptLangs = ['en-US', 'en'];
            var match = InfoBar.prototype.userLangPageLangMatch(acceptLangs, 'en');
            expect(match).toBeTruthy();
        });

        it('should return true if the accept language array contains the page language', function() {
            var match = InfoBar.prototype.userLangPageLangMatch;
            expect(match(['en-US'], 'en-US')).toBeTruthy();
            expect(match(['en-US', 'en', 'fr'], 'en-US')).toBeTruthy();
            expect(match(['fr', 'de'], 'fr')).toBeTruthy();
            expect(match(['de', 'fr', 'en'], 'fr')).toBeTruthy();
            expect(match(['ja', 'pt-PT', 'el', 'fr', 'en'], 'el')).toBeTruthy();
            expect(match(['en-ZA', 'en-GB', 'en'], 'en-GB')).toBeTruthy();
            expect(match(['fr-FR'], 'fr')).toBeTruthy();
            expect(match(['el-GR'], 'el')).toBeTruthy();
        });

        it('should return false if the users language does not match the page language', function() {
            var acceptLangs = ['en-US', 'en'];
            var match = InfoBar.prototype.userLangPageLangMatch(acceptLangs, 'es-ES');
            expect(match).toBeFalsy();
        });
    });

    describe('InfoBar.prototype.getOfferedLang', function() {
        it('should return false if there are no alternate languages', function() {
            var offeredLang = InfoBar.prototype.getOfferedLang;
            expect(offeredLang(['en-US', 'en'], 'es-ES')).toBeFalsy();
        });
    });

    describe('InfoBar.prototype.getOfferedLang', function() {

        beforeEach(function() {
            var hreflangLinks = [
                '<link rel="alternate" hreflang="es-ES" href="http://www.mozilla.org/es-ES/firefox/new/" />',
                '<link rel="alternate" hreflang="fr" href="http://www.mozilla.org/fr/firefox/new/" />'
            ].join();

            $(hreflangLinks).appendTo('head');
        });

        afterEach(function() {
            $('link[hreflang]').remove();
        });

        it('should return false if the page language matches the user\'s primary language', function() {
            var offeredLang = InfoBar.prototype.getOfferedLang;
            expect(offeredLang(['es-ES', 'es'], 'es-ES')).toBeFalsy();
        });

        it('should return the available offered language', function() {
            var offeredLang = InfoBar.prototype.getOfferedLang;
            expect(offeredLang(['de', 'fr'], 'en-US')).toBe('fr');
            expect(offeredLang(['de', 'it', 'pt-PT', 'es'], 'en-US')).toBe('es-ES');
        });

        it('should return false if no primary language match, nor available language match were found', function() {
            var offeredLang = InfoBar.prototype.getOfferedLang;
            expect(offeredLang(['de', 'it'], 'en-US')).toBeFalsy();
        });
    });

    describe("infobar.update", function () {

        var setup = function (ua, buildID) {
            // Test a case where the latest version is a non-dot release
            var result1 = InfoBar.update('35.0', ua, buildID);
            // Test a case where the latest version is a dot release
            var result2 = InfoBar.update('35.0.1', ua, buildID);
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
