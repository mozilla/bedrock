/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.4/introduction
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, spyOn */

describe('mozilla-utils.js', function() {

    'use strict';

    describe('switchPathLanguage', function () {
        var location = {};

        it('should return the same URL with a different language prefix', function () {
            location.pathname = '/en-US/firefox/new/';
            location.search = '';
            expect(Mozilla.Utils.switchPathLanguage(location, 'de')).toEqual('/de/firefox/new/');

            location.pathname = '/fr/firefox/';
            expect(Mozilla.Utils.switchPathLanguage(location, 'zh-TW')).toEqual('/zh-TW/firefox/');

            location.pathname = '/de/';
            expect(Mozilla.Utils.switchPathLanguage(location, 'fr')).toEqual('/fr/');
        });

        it('should return the same URL with a different language prefix and include the query string', function () {
            location.pathname = '/en-US/firefox/new/';
            location.search = '?dude=abide';
            expect(Mozilla.Utils.switchPathLanguage(location, 'de')).toEqual('/de/firefox/new/?dude=abide');

            location.pathname = '/fr/firefox/';
            expect(Mozilla.Utils.switchPathLanguage(location, 'zh-TW')).toEqual('/zh-TW/firefox/?dude=abide');

            location.pathname = '/de/';
            expect(Mozilla.Utils.switchPathLanguage(location, 'fr')).toEqual('/fr/?dude=abide');
        });
    });

    describe('initMobileDownloadLinks', function () {

        var $link;

        afterEach(function(){
            window.site.platform = 'other';
            $link.remove();
        });

        it('should set a URL with the market scheme on Android', function () {
            window.site.platform = 'android';
            $link = $('<a class="download-link" href="https://play.google.com/store/apps/details?id=org.mozilla.firefox">foo</a>').appendTo('body');
            Mozilla.Utils.initMobileDownloadLinks();
            expect($link.attr('href')).toEqual('market://details?id=org.mozilla.firefox');
        });
    });

    describe('maybeSwitchToDistDownloadLinks', function() {

        var $link;
        var defaultHref = 'https://test.example.com/?id=org.mozilla.firefox';
        var partnerAHref = defaultHref.replace('org.mozilla.firefox',
                                               'com.partnera.firefox');

        beforeEach(function () {
            $link = $([
                '<a href="' + defaultHref +
                '" data-partnera-link="' + partnerAHref +
                '">download</a>'
            ].join()).appendTo('body');
        });

        afterEach(function() {
            $link.remove();
        });

        it('should use specified download link for certain distributions', function () {
            Mozilla.Utils.maybeSwitchToDistDownloadLinks({
                distribution: 'PartnerA'
            });
            expect($link.attr('href')).toEqual(partnerAHref);
        });

        it('should use default download link for other distributions', function () {
            Mozilla.Utils.maybeSwitchToDistDownloadLinks({
                distribution: 'PartnerB'
            });
            expect($link.attr('href')).toEqual(defaultHref);
        });

    });
});
