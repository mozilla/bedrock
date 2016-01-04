/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn */

describe('global.js', function() {

    'use strict';

    describe('trigger_ie_download', function () {

        beforeEach(function() {
            window.site.platform = 'windows';
        });

        afterEach(function() {
            window.site.platform = 'other';
        });

        it('should open a popup for IE < 9', function () {
            var userAgent = 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)';
            window.open = sinon.stub();
            trigger_ie_download('foo', userAgent);
            expect(window.open.called).toBeTruthy();
        });

        it('should not open a popup for IE 9', function () {
            var userAgent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)';
            window.open = sinon.stub();
            trigger_ie_download('foo', userAgent);
            expect(window.open.called).not.toBeTruthy();
        });

        it('should not open a popup for other browsers', function () {
            var userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36';
            window.open = sinon.stub();
            trigger_ie_download('foo', userAgent);
            expect(window.open.called).not.toBeTruthy();
        });

    });

    describe('init_download_links', function () {

        /* Append an HTML fixture to the document body
         * for each test in the scope of this suite */
        beforeEach(function () {
            $('<a class="download-link" data-direct-link="bar">foo</a>').appendTo('body');
        });

        /* Then after each test remove the fixture */
        afterEach(function() {
            $('.download-link').remove();
        });

        it('should call trigger_ie_download when clicked', function () {
            trigger_ie_download = sinon.stub();
            init_download_links();
            $('.download-link').trigger('click');
            expect(trigger_ie_download.called).toBeTruthy();
        });

    });

    describe('update_download_text_for_old_fx', function () {
        var windowTransStub;
        var isFirefoxStub;

        // append HTML to body for each test
        beforeEach(function () {
            // Download button that is not set to check for old fx.
            // Button subtitle text should never change.
            var html1 = ['<div id="download-button1" class="download-button download-button-simple">',
                '<ul class="download-list" role="presentation">',
                '<li class="os_win">',
                '<a class="download-link" href="/firefox/new/?scene=2#download-fx">',
                '<span class="download-content">',
                    '<strong class="download-title">Firefox</strong>',
                    '<span class="download-subtitle">Free Download</span>',
                '</span>',
                '</a>',
                '</li>',
                '</ul>',
                '</div>'].join('\n');

            // Download button that is set to check for old fx.
            // Button subtitle text should change only when
            // isFirefox() == true and isFirefoxUpToDate() == true.
            var html2 = ['<div id="download-button2" class="download-button download-button-simple download-button-check-old-fx">',
                '<ul class="download-list" role="presentation">',
                '<li class="os_win">',
                '<a class="download-link" href="/firefox/new/?scene=2#download-fx">',
                '<span class="download-content">',
                    '<strong class="download-title">Firefox</strong>',
                    '<span class="download-subtitle">Free Download</span>',
                '</span>',
                '</a>',
                '</li>',
                '</ul>',
                '</div>'].join('\n');

            $(html1).appendTo('body');
            $(html2).appendTo('body');

            windowTransStub = sinon.stub(window, 'trans').returns('Update your Firefox');
        });

        afterEach(function () {
            $('.download-button').remove();

            // set global functions back to original state
            isFirefoxStub.restore();
            windowTransStub.restore();
        });

        it('should change the button text when using old fx', function () {
            isFirefoxStub = sinon.stub(window.Mozilla.Client, '_isFirefox').returns(true);
            spyOn(window.Mozilla.Client, 'getFirefoxDetails').and.callFake(function(callback) {
                callback({ version: '40.0', channel: 'release', isUpToDate: false, isESR: false });
            });

            update_download_text_for_old_fx();

            expect($('#download-button1').find('.download-subtitle').text()).toEqual('Free Download');
            expect($('#download-button2').find('.download-subtitle').text()).toEqual('Update your Firefox');
        });

        it('should not change the button text when not using fx', function () {
            isFirefoxStub = sinon.stub(window.Mozilla.Client, '_isFirefox').returns(false);

            update_download_text_for_old_fx();

            expect($('#download-button1').find('.download-subtitle').text()).toEqual('Free Download');
            expect($('#download-button2').find('.download-subtitle').text()).toEqual('Free Download');
        });

        it('should not change the button text when using up to date fx', function () {
            isFirefoxStub = sinon.stub(window.Mozilla.Client, '_isFirefox').returns(true);
            spyOn(window.Mozilla.Client, 'getFirefoxDetails').and.callFake(function(callback) {
                callback({ version: '41.0', channel: 'release', isUpToDate: true, isESR: false });
            });

            update_download_text_for_old_fx();

            expect($('#download-button1').find('.download-subtitle').text()).toEqual('Free Download');
            expect($('#download-button2').find('.download-subtitle').text()).toEqual('Free Download');
        });
    });

    describe('init_mobile_download_links', function () {

        var $link;

        afterEach(function(){
            window.site.platform = 'other';
            $link.remove();
        });

        it('should set a URL with the market scheme on Android', function () {
            window.site.platform = 'android';
            $link = $('<a class="download-link" href="https://play.google.com/store/apps/details?id=org.mozilla.firefox">foo</a>').appendTo('body');
            init_mobile_download_links();
            expect($link.attr('href')).toEqual('market://details?id=org.mozilla.firefox');
        });

        it('should set a URL with the itms-apps scheme on iOS', function () {
            window.site.platform = 'ios';
            $link = $('<a class="download-link" href="https://itunes.apple.com/us/app/apple-store/id989804926?mt=8">foo</a>').appendTo('body');
            init_mobile_download_links();
            expect($link.attr('href')).toEqual('itms-apps://itunes.apple.com/us/app/apple-store/id989804926?mt=8');
        });

    });

});
