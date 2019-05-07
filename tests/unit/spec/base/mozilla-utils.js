/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.4/introduction
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect */

describe('mozilla-utils.js', function() {
    'use strict';

    describe('trans', function () {
        var stringDiv;

        beforeEach(function () {
            stringDiv = '<div id="strings" data-global-close="Close" ' +
            'data-global-next="Next" ' +
            'data-global-previous="Previous"> ' +
            '</div>';

            var container = document.createElement('div');
            container.innerHTML = stringDiv;
            $(container).appendTo('body');
        });

        afterEach(function() {
            $(stringDiv).remove();
        });

        it('should correctly return translation value', function () {
            var translation = Mozilla.Utils.trans('global-next');
            expect(translation === 'Next');
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
        var partnerAHref = defaultHref.replace('org.mozilla.firefox', 'com.partnera.firefox');

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
