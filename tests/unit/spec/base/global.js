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
            isFirefoxStub = sinon.stub(window, 'isFirefox').returns(true);
            spyOn(window.Mozilla.Client, 'getFirefoxDetails').and.callFake(function(callback) {
                callback({ version: '40.0', channel: 'release', isUpToDate: false, isESR: false });
            });

            update_download_text_for_old_fx();

            expect($('#download-button1').find('.download-subtitle').text()).toEqual('Free Download');
            expect($('#download-button2').find('.download-subtitle').text()).toEqual('Update your Firefox');
        });

        it('should not change the button text when not using fx', function () {
            isFirefoxStub = sinon.stub(window, 'isFirefox').returns(false);

            update_download_text_for_old_fx();

            expect($('#download-button1').find('.download-subtitle').text()).toEqual('Free Download');
            expect($('#download-button2').find('.download-subtitle').text()).toEqual('Free Download');
        });

        it('should not change the button text when using up to date fx', function () {
            isFirefoxStub = sinon.stub(window, 'isFirefox').returns(true);
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

    describe('getFirefoxMasterVersion', function () {

        it('should return the firefox master version number', function () {
            var result;
            // Pretend to be Firefox 23
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0';
            result = getFirefoxMasterVersion(ua);
            expect(result).toEqual(23);
        });

        it('should return 0 for non Firefox browsers', function () {
            var result;
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36';
            result = getFirefoxMasterVersion(ua);
            expect(result).toEqual(0);
        });
    });

    describe('isFirefox', function() {
        it('should consider Firefox to be Firefox', function() {
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0';
            var result = isFirefox(ua);
            expect(result).toBeTruthy();
        });

        it('should not consider Camino to be Firefox', function() {
            var ua = 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; en; rv:1.9.2.24) Gecko/20111114 Camino/2.1 (like Firefox/3.6.24)';
            var result = isFirefox(ua);
            expect(result).not.toBeTruthy();
        });

        it('should not consider Chrome to be Firefox', function() {
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36';
            var result = isFirefox(ua);
            expect(result).not.toBeTruthy();
        });

        it('should not consider Safari to be Firefox', function() {
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2';
            var result = isFirefox(ua);
            expect(result).not.toBeTruthy();
        });

        it('should not consider IE to be Firefox', function() {
            var ua = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)';
            var result = isFirefox(ua);
            expect(result).not.toBeTruthy();
        });

        it('should not consider SeaMonkey to be Firefox', function() {
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 SeaMonkey/2.22.1';
            var result = isFirefox(ua);
            expect(result).not.toBeTruthy();
        });

        it('should not consider Iceweasel to be Firefox', function() {
            var ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1';
            var result = isFirefox(ua);
            expect(result).not.toBeTruthy();
        });
    });

    describe('isFirefoxMobile', function () {

        it('should return false for Firefox on Desktop', function() {
            expect(isFirefoxMobile('Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')).not.toBeTruthy();
            expect(isFirefoxMobile('Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0')).not.toBeTruthy();
            expect(isFirefoxMobile('Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0')).not.toBeTruthy();
        });

        it('should return true for Firefox Android on Phone', function() {
            var ua = 'Mozilla/5.0 (Android; Mobile; rv:26.0) Gecko/26.0 Firefox/26.0';
            var result = isFirefoxMobile(ua);
            expect(result).toBeTruthy();
        });

        it('should return true for Firefox Android on Tablet', function() {
            var ua = 'Mozilla/5.0 (Android; Tablet; rv:26.0) Gecko/26.0 Firefox/26.0';
            var result = isFirefoxMobile(ua);
            expect(result).toBeTruthy();
        });

        it('should return true for Firefox OS on Phone', function() {
            var ua = 'Mozilla/5.0 (Mobile; rv:26.0) Gecko/26.0 Firefox/26.0';
            var result = isFirefoxMobile(ua);
            expect(result).toBeTruthy();
        });

        it('should return true for Firefox OS on Tablet', function() {
            var ua = 'Mozilla/5.0 (Tablet; rv:26.0) Gecko/26.0 Firefox/26.0';
            var result = isFirefoxMobile(ua);
            expect(result).toBeTruthy();
        });

        it('should return true for Firefox for Maemo (Nokia N900)', function() {
            var ua = 'Mozilla/5.0 (Maemo; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1';
            var result = isFirefoxMobile(ua);
            expect(result).toBeTruthy();
        });

    });

    describe('isFirefoxiOS', function () {

        it('should return false for Firefox on Desktop', function() {
            expect(isFirefoxiOS('Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')).not.toBeTruthy();
            expect(isFirefoxiOS('Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0')).not.toBeTruthy();
            expect(isFirefoxiOS('Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0')).not.toBeTruthy();
        });

        it('should return false for Firefox Android', function() {
            expect(isFirefoxiOS('Mozilla/5.0 (Android; Mobile; rv:26.0) Gecko/26.0 Firefox/26.0')).not.toBeTruthy();
        });

        it('should return true for Firefox on iPhone', function() {
            var ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.1 Mobile/12F69 Safari/600.1.4';
            var result = isFirefoxiOS(ua);
            expect(result).toBeTruthy();
        });

        it('should return true for Firefox on iPad', function() {
            var ua = 'Mozilla/5.0 (iPad; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4';
            var result = isFirefoxiOS(ua);
            expect(result).toBeTruthy();
        });
    });

    describe('isFirefoxUpToDate', function () {

        it('should consider up to date if latest version is equal to user version', function() {
            var result;
            /* Use a stub to return a pre-programmed value
             * from getFirefoxMasterVersion */
            getFirefoxMasterVersion = sinon.stub().returns(21);
            result = isFirefoxUpToDate('21.0');
            expect(getFirefoxMasterVersion.called).toBeTruthy();
            expect(result).toBeTruthy();
        });

        it('should consider up to date if latest version is less than user version', function() {
            var result;
            getFirefoxMasterVersion = sinon.stub().returns(22);
            result = isFirefoxUpToDate('21.0');
            expect(getFirefoxMasterVersion.called).toBeTruthy();
            expect(result).toBeTruthy();
        });

        it('should not consider up to date if latest version greater than user version', function() {
            var result;
            getFirefoxMasterVersion = sinon.stub().returns(20);
            result = isFirefoxUpToDate('21.0');
            expect(getFirefoxMasterVersion.called).toBeTruthy();
            expect(result).not.toBeTruthy();
        });
    });

    describe('isLikeFirefox', function() {

        it('should consider SeaMonkey to be like Firefox', function() {
            var ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0 SeaMonkey/2.37a1';
            var result = isLikeFirefox(ua);
            expect(result).toBeTruthy();
        });

        it('should consider IceWeasel to be like Firefox', function() {
            var ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1';
            var result = isLikeFirefox(ua);
            expect(result).toBeTruthy();
        });

        it('should consider IceCat to be like Firefox', function() {
            var ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121201 icecat/17.0.1';
            var result = isLikeFirefox(ua);
            expect(result).toBeTruthy();
        });

        it('should consider Camino to be like Firefox', function() {
            var ua = 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; en; rv:1.9.2.24) Gecko/20111114 Camino/2.1 (like Firefox/3.6.24)';
            var result = isLikeFirefox(ua);
            expect(result).toBeTruthy();
        });

        it('should consider Camino like userAgent to be like Firefox', function() {
            var ua = 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; en; rv:1.9.2.24) Gecko/20111114 (like Firefox/3.6.24)';
            var result = isLikeFirefox(ua);
            expect(result).toBeTruthy();
        });

        it('should not consider Firefox to be "like" Firefox', function() {
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0';
            var result = isLikeFirefox(ua);
            expect(result).not.toBeTruthy();
        });

        it('should not consider Chrome to be like Firefox', function() {
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36';
            var result = isLikeFirefox(ua);
            expect(result).not.toBeTruthy();
        });

        it('should not consider Safari to be like Firefox', function() {
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2';
            var result = isLikeFirefox(ua);
            expect(result).not.toBeTruthy();
        });

        it('should not consider IE to be like Firefox', function() {
            var ua = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)';
            var result = isLikeFirefox(ua);
            expect(result).not.toBeTruthy();
        });
    });
});
