/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect */

describe('core-datalayer.js', function() {

    describe('pageHasDownload', function() {

        afterEach(function() {
            $('.download').remove();
        });

        it('will return "true" when download button is present on page.', function() {
            var downloadMarkup = '<a class="download" href="#" data-link-type="download" data-download-os="Desktop">';

            $(downloadMarkup).appendTo('body');
            expect(Mozilla.Analytics.pageHasDownload()).toBe('true');
        });

        it('will return "false" when download button is not present on page.', function() {
            expect(Mozilla.Analytics.pageHasDownload()).toBe('false');
        });
    });

    describe('pageHasVideo', function() {

        afterEach(function() {
            $('#htmlPlayer').remove();
            $('#iframePlayer').remove();
        });

        it('will return "true" when HTML5 video is present on page.', function() {
            var videoMarkup = '<video id="htmlPlayer"></video>';

            $(videoMarkup).appendTo('body');
            expect(Mozilla.Analytics.pageHasVideo()).toBe('true');
        });

        it('will return "true" when YouTube iframe video is present on page.', function() {
            var videoMarkup = '<iframe id="iframePlayer" src="https://www.youtube-nocookie.com/embed/NqxUdc0P6YE?rel=0"></iframe>';

            $(videoMarkup).appendTo('body');
            expect(Mozilla.Analytics.pageHasVideo()).toBe('true');
        });

        it('will return "false" when download button is not present on page.', function() {
            expect(Mozilla.Analytics.pageHasVideo()).toBe('false');
        });
    });

    describe('getPageVersion', function() {
        it('will return the Firefox version number form the URL if present', function() {
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/107.0.11/firstrun/')).toBe('107.0.11');
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/46.0.1/firstrun/learnmore/')).toBe('46.0.1');
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/11.0/whatsnew/')).toBe('11.0');
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/46.0.1a2/firstrun/')).toBe('46.0.1a2');
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/46.0a1/whatsnew/')).toBe('46.0a1');
        });

        it('will return null if no version number present in URL', function() {
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/')).toBeNull();
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/new')).toBeNull();
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/whatsnew')).toBeNull();
        });
    });

    describe('updateDataLayerPush', function() {
        var linkElement;

        beforeEach(function() {
            var link = '<a id="link" href="https://www.mozilla.org/en-US/firefox/new/">';
            $(link).appendTo('body');
            linkElement = $('#link')[0];

            window.dataLayer = [];
        });

        afterEach(function() {
            $('body').remove('#link');
            delete window.dataLayer;
        });

        it('will add newClickHref property to link click object when pushed to the dataLayer', function() {
            Mozilla.Analytics.updateDataLayerPush('www.allizom.org');

            window.dataLayer.push({
                'event': 'gtm.linkClick',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toBeDefined();
        });

        it('will not add newClickHref property to object pushed to dataLayer if not a link click object', function() {
            Mozilla.Analytics.updateDataLayerPush('www.allizom.org');

            window.dataLayer.push({
                'event': 'gtm.click',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toBeUndefined();
        });

        it('will keep host in newClickHref when clicked link\'s href host value is different thatn the page\'s', function() {
            Mozilla.Analytics.updateDataLayerPush('www.allizom.org');

            window.dataLayer.push({
                'event': 'gtm.linkClick',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toEqual('https://www.mozilla.org/en-US/firefox/new/');
        });

        it('will remove host and locale in newClickHref when clicked link\'s href value matches the page\'s', function() {
            Mozilla.Analytics.updateDataLayerPush('www.mozilla.org');

            // Bug 1278426
            linkElement.href = 'https://www.mozilla.org:443/en-US/firefox/new/';

            window.dataLayer.push({
                'event': 'gtm.linkClick',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toEqual('/firefox/new/');
        });

        it('will remove host and non-en-US locale', function() {
            Mozilla.Analytics.updateDataLayerPush('www.mozilla.org');

            linkElement.href = 'https://www.mozilla.org:443/de/firefox/new/';

            window.dataLayer.push({
                'event': 'gtm.linkClick',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toEqual('/firefox/new/');
        });

        it('will not remove locale if absent from the URL', function() {
            Mozilla.Analytics.updateDataLayerPush('www.mozilla.org');

            linkElement.href = 'https://www.mozilla.org/firefox/new/';

            window.dataLayer.push({
                'event': 'gtm.linkClick',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toEqual('/firefox/new/');
        });
    });
});
