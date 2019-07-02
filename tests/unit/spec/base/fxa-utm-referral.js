/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, it, expect, Mozilla */

describe('fxa-utm-referral.js', function() {

    'use strict';

    describe('getAttributionData', function () {

        it('should return a valid object unchanged', function () {
            var validObj = {
                'utm_source': 'desktop-snippet',
                'utm_content': 'rel-esr',
                'utm_medium': 'referral',
                'utm_term': 4242,
                'utm_campaign': 'F100_4242_otherstuff_in_here'
            };

            var validData = {
                'utm_source': 'desktop-snippet',
                'utm_content': 'rel-esr',
                'utm_medium': 'referral',
                'utm_term': '4242',
                'utm_campaign': 'F100_4242_otherstuff_in_here'
            };

            expect(Mozilla.UtmUrl.getAttributionData(validObj)).toEqual(validData);
        });

        it('should return an object without any danagerous params', function () {
            var dangerousSource = {
                'utm_source': '<script>console.log("test");</script>',
                'utm_content': 'rel-esr',
            };

            var safeSource = {
                'utm_content': 'rel-esr'
            };

            expect(Mozilla.UtmUrl.getAttributionData(dangerousSource)).toEqual(safeSource);
        });

        it('should not return an object if all params are unsafe', function () {
            var dangerousData = {
                'utm_source': '%5C',
                'utm_content': '%3C',
                'utm_medium': '%24',
                'utm_term': '%40',
                'utm_campaign': '%22'
            };

            expect(Mozilla.UtmUrl.getAttributionData(dangerousData)).toBeNull();
        });

        it('should not strip allowed special characters', function () {
            var specialData = {
                'utm_source': 'blog.mozilla.org',
                'utm_content': 'my-experiment',
                'utm_medium': '%25',
                'utm_term': '%2F'
            };

            var specialSource = {
                'utm_source': 'blog.mozilla.org',
                'utm_content': 'my-experiment',
                'utm_medium': '%',
                'utm_term': '/'
            };

            expect(Mozilla.UtmUrl.getAttributionData(specialData)).toEqual(specialSource);
        });

        it('decode URL components', function () {
            var encodedData = {
                'utm_medium': '%25',
                'utm_term': '%2F'
            };

            var encodedSource = {
                'utm_medium': '%',
                'utm_term': '/'
            };

            expect(Mozilla.UtmUrl.getAttributionData(encodedData)).toEqual(encodedSource);
        });

    });

    describe('appendToDownloadURL', function () {

        it('appends a new query string if there isn\'t one', function () {
            var data = {
                'utm_source': 'desktop-snippet',
                'utm_content': 'rel-esr',
                'utm_medium': 'referral',
                'utm_term': 4242,
                'utm_campaign': 'F100_4242_otherstuff_in_here'
            };

            var url = 'https://accounts.firefox.com/';

            expect(Mozilla.UtmUrl.appendToDownloadURL(url, data)).toEqual('https://accounts.firefox.com/?utm_source=desktop-snippet&utm_content=rel-esr&utm_medium=referral&utm_term=4242&utm_campaign=F100_4242_otherstuff_in_here');
        });

        it('adds UTM params without overwriting other query string params', function () {
            var data = {
                'utm_source': 'test-source'
            };

            var url = 'https://accounts.firefox.com/?spice=pumpkin';

            expect(Mozilla.UtmUrl.appendToDownloadURL(url, data)).toEqual('https://accounts.firefox.com/?spice=pumpkin&utm_source=test-source');
        });

        it('over-writes existing UTM params', function () {
            var data = {
                'utm_source': 'source-two',
                'utm_content': 'content-two',
                'utm_medium': 'medium-two',
                'utm_term': 'term-two',
                'utm_campaign': 'campaign-two'
            };

            var url = 'https://accounts.firefox.com/?utm_medium=medium-one&utm_term=term-one&utm_campaign=campaign-one&utm_source=source-one&utm_content=content-one';

            expect(Mozilla.UtmUrl.appendToDownloadURL(url, data)).toEqual('https://accounts.firefox.com/?utm_medium=medium-two&utm_term=term-two&utm_campaign=campaign-two&utm_source=source-two&utm_content=content-two');
        });

        it('does not leave out new params if there are existing params to over write', function () {
            var data = {
                'utm_source': 'source-two',
                'utm_content': 'content-two',
                'utm_medium': 'medium-two',
                'utm_term': 'term-two',
                'utm_campaign': 'campaign-two'
            };

            var url = 'https://accounts.firefox.com/?utm_campaign=campaign-one&utm_source=source-one&utm_content=content-one';

            expect(Mozilla.UtmUrl.appendToDownloadURL(url, data)).toEqual('https://accounts.firefox.com/?utm_campaign=campaign-two&utm_source=source-two&utm_content=content-two&utm_medium=medium-two&utm_term=term-two');
        });

        it('does not override port, path, or file name', function () {
            var data = {
                'utm_source': 'test-source'
            };

            var url = 'https://accounts.firefox.com:8000/grande/nofat.html?spice=pumpkin';

            expect(Mozilla.UtmUrl.appendToDownloadURL(url, data)).toEqual('https://accounts.firefox.com:8000/grande/nofat.html?spice=pumpkin&utm_source=test-source');
        });

    });

    describe('getAttributionData.init', function () {

        beforeEach(function () {
            // link to change
            var links =
                '<div id="test-links">' +
                '<a id="test-expected" class="js-fxa-cta-link" href="https://accounts.firefox.com/?service=sync&amp;action=email&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-accounts_page&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page" data-mozillaonline-link="https://accounts.firefox.com.cn/?service=sync&amp;action=email&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-accounts_page&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page">Create a Firefox Account</a>' +
                '<a id="test-not-accounts" class="js-fxa-cta-link" href="https://www.mozilla.org/?service=sync&amp;action=email&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-accounts_page&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page" data-mozillaonline-link="https://accounts.firefox.com.cn/?service=sync&amp;action=email&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-accounts_page&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page">Create a Firefox Account</a>' +
                '<a id="test-second-expected" class="js-fxa-cta-link" href="https://accounts.firefox.com/signup?service=sync&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-globalnav&amp;utm_content=get-firefox-account&amp;utm_source=www.mozilla.org&amp;utm_medium=referral&amp;utm_campaign=globalnav" data-mozillaonline-link="https://accounts.firefox.com.cn/signup?service=sync&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-globalnav&amp;utm_content=get-firefox-account&amp;utm_source=www.mozilla.org&amp;utm_medium=referral&amp;utm_campaign=globalnav">Create a Firefox Account</a>' +
                '</div>';

            $(links).appendTo('body');
        });

        afterEach(function () {
            $('#test-links').remove();
        });

        it('updates the href of links with class js-fxa-cta-link', function () {
            var data = {
                'utm_source': 'source-two',
                'utm_content': 'content-two',
                'utm_medium': 'medium-two',
                'utm_term': 'term-two',
                'utm_campaign': 'campaign-two'
            };

            Mozilla.UtmUrl.getAttributionData.init(data);

            var expected = document.getElementById('test-expected');
            var expectedHref = expected.getAttribute('href');
            var secondExpected = document.getElementById('test-second-expected');
            var secondExpectedHref = secondExpected.getAttribute('href');

            expect(expectedHref).toEqual('https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=content-two&utm_source=source-two&utm_medium=medium-two&utm_campaign=campaign-two&utm_term=term-two');
            expect(secondExpectedHref).toEqual('https://accounts.firefox.com/signup?service=sync&context=fx_desktop_v3&entrypoint=mozilla.org-globalnav&utm_content=content-two&utm_source=source-two&utm_medium=medium-two&utm_campaign=campaign-two&utm_term=term-two');
        });

        it('updates the data-mozilla-online attribute of links with class js-fxa-cta-link', function () {
            var data = {
                'utm_source': 'source-two',
                'utm_content': 'content-two',
                'utm_medium': 'medium-two',
                'utm_term': 'term-two',
                'utm_campaign': 'campaign-two'
            };

            Mozilla.UtmUrl.getAttributionData.init(data);

            var expected = document.getElementById('test-expected');
            var expectedOnline = expected.getAttribute('data-mozillaonline-link');
            var secondExpected = document.getElementById('test-second-expected');
            var secondExpectedOnline = secondExpected.getAttribute('data-mozillaonline-link');

            expect(expectedOnline).toEqual('https://accounts.firefox.com.cn/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=content-two&utm_source=source-two&utm_medium=medium-two&utm_campaign=campaign-two&utm_term=term-two');
            expect(secondExpectedOnline).toEqual('https://accounts.firefox.com.cn/signup?service=sync&context=fx_desktop_v3&entrypoint=mozilla.org-globalnav&utm_content=content-two&utm_source=source-two&utm_medium=medium-two&utm_campaign=campaign-two&utm_term=term-two');
        });

        it('does not make change if there are no UTM params', function () {
            var data = {};

            Mozilla.UtmUrl.getAttributionData.init(data);

            var expected = document.getElementById('test-expected');
            var expectedHref = expected.getAttribute('href');
            var expectedOnline = expected.getAttribute('data-mozillaonline-link');

            expect(expectedHref).toEqual('https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page');
            expect(expectedOnline).toEqual('https://accounts.firefox.com.cn/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page');
        });

        it('does not make changes if the link is not a link to accounts.firefox.com', function () {
            var data = {
                'utm_source': 'source-two',
                'utm_content': 'content-two',
                'utm_medium': 'medium-two',
                'utm_term': 'term-two',
                'utm_campaign': 'campaign-two'
            };

            Mozilla.UtmUrl.getAttributionData.init(data);

            var unexpected = document.getElementById('test-not-accounts');
            var unexpectedHref = unexpected.getAttribute('href');
            var unexpectedOnline = unexpected.getAttribute('data-mozillaonline-link');

            expect(unexpectedHref).toEqual('https://www.mozilla.org/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page');
            expect(unexpectedOnline).toEqual('https://accounts.firefox.com.cn/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page');
        });


    });
});
