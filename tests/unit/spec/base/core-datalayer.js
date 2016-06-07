/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect */

describe('core-datalayer.js', function() {

    describe('getPageId', function(){
        var html = document.documentElement;

        afterEach(function() {
            html.removeAttribute('data-gtm-page-id');
        });

        it('will grab data-gtm-page-id value if present on <html> element', function(){
            html.setAttribute('data-gtm-page-id', 'test');

            expect(Mozilla.Analytics.getPageId('/en-US/firefox/new/')).toBe('test');
        });

        it('will grab the pathname minus the first directory if no data-gtm-page-id value is present on <html> element', function(){
            expect(Mozilla.Analytics.getPageId('/en-US/firefox/new/')).toBe('/firefox/new/');
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
