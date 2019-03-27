/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, it, expect */

describe('new-ios-redirect-helper.js', function() {
    'use strict';

    describe('getDomainFromURL', function () {

        it('should parse the domain from a given URL', function () {
            var url = 'http://www.yahoo.com';
            var domain = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(domain).toEqual('yahoo.com');

            url = 'https://yahoo.com/foo/bar';
            domain  = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(domain).toEqual('yahoo.com');

            url = 'https://www.yahoo.com/#hash';
            domain  = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(domain).toEqual('yahoo.com');

            url = 'http://www.yahoo.com/?foo=bar';
            domain  = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(domain).toEqual('yahoo.com');

            url = 'https://www.yahoo.com/?foo=bar#hash';
            domain  = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(domain).toEqual('yahoo.com');

            url = 'https://www.täst.de';
            domain  = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(domain).toEqual('täst.de');
        });

        it('should return false when given a malformed URL', function () {
            var url = 'http:///www.yahoo.com';
            var domain = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(domain).toBeFalsy();

            url = 'correct.horse-battery staple';
            domain = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(domain).toBeFalsy();
        });

        it('should retain non-www subdomains', function () {
            var url = 'http://thedude.yahoo.com';
            var domain = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(domain).toEqual('thedude.yahoo.com');

            url = 'http://ko.wikipedia.org/wiki/위키백과:대문';
            domain  = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(domain).toEqual('ko.wikipedia.org');
        });
    });

    describe('isSearchEngine', function () {
        it('should return domain without a TLD when a domain is bing, duckduckgo, google, or search.yahoo', function () {
            var url = 'http://search.yahoo.com';
            var domain = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(Mozilla.FirefoxNewIosRedirectHelper.isSearchEngine(domain)).toEqual('yahoo');

            url = 'http://www.google.co.uk';
            domain = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(Mozilla.FirefoxNewIosRedirectHelper.isSearchEngine(domain)).toEqual('google');

            url = 'https://www.bing.com';
            domain = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(Mozilla.FirefoxNewIosRedirectHelper.isSearchEngine(domain)).toEqual('bing');

            url = 'http://duckduckgo.com';
            domain = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(Mozilla.FirefoxNewIosRedirectHelper.isSearchEngine(domain)).toEqual('duckduckgo');
        });

        it('should return false when the domain is not one of the predefined search engines', function () {
            var url = 'http://www.lycos.com';
            var domain = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(Mozilla.FirefoxNewIosRedirectHelper.isSearchEngine(domain)).toBeFalsy();

            url = 'http://www.mozilla.org';
            domain = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(url);

            expect(Mozilla.FirefoxNewIosRedirectHelper.isSearchEngine(domain)).toBeFalsy();
        });
    });
});
