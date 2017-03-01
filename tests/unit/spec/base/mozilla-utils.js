/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn */

describe('mozilla-utils.js', function() {

    'use strict';

    describe('triggerIEDownload', function () {

        beforeEach(function() {
            window.site.platform = 'windows';
        });

        afterEach(function() {
            window.site.platform = 'other';
        });

        it('should open a popup for IE < 9', function () {
            var userAgent = 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)';
            window.open = sinon.stub();
            Mozilla.Utils.triggerIEDownload('foo', userAgent);
            expect(window.open.called).toBeTruthy();
        });

        it('should not open a popup for IE 9', function () {
            var userAgent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)';
            window.open = sinon.stub();
            Mozilla.Utils.triggerIEDownload('foo', userAgent);
            expect(window.open.called).not.toBeTruthy();
        });

        it('should not open a popup for other browsers', function () {
            var userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36';
            window.open = sinon.stub();
            Mozilla.Utils.triggerIEDownload('foo', userAgent);
            expect(window.open.called).not.toBeTruthy();
        });

    });

    describe('initDownloadLinks', function () {

        /* Append an HTML fixture to the document body
         * for each test in the scope of this suite */
        beforeEach(function () {
            $('<a class="download-link" data-direct-link="bar">foo</a>').appendTo('body');
        });

        /* Then after each test remove the fixture */
        afterEach(function() {
            $('.download-link').remove();
        });

        it('should call triggerIEDownload when clicked', function () {
            spyOn(Mozilla.Utils, 'triggerIEDownload');
            Mozilla.Utils.initDownloadLinks();
            $('.download-link').trigger('click');
            expect(Mozilla.Utils.triggerIEDownload).toHaveBeenCalled();
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

        it('should set a URL with the itms-apps scheme on iOS', function () {
            window.site.platform = 'ios';
            $link = $('<a class="download-link" href="https://itunes.apple.com/us/app/apple-store/id989804926?mt=8">foo</a>').appendTo('body');
            Mozilla.Utils.initMobileDownloadLinks();
            expect($link.attr('href')).toEqual('itms-apps://itunes.apple.com/us/app/apple-store/id989804926?mt=8');
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
