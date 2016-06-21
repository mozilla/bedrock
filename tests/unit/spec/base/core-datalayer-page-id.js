/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect */

describe('core-datalayer-page-id.js', function() {

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

        it('will return the full page path when no data-gtm-page-id value is present and no locale is in page path', function(){
            expect(Mozilla.Analytics.getPageId('/firefox/new/')).toBe('/firefox/new/');
        });
    });
});
