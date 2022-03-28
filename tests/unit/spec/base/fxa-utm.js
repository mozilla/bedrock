/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import FxaUtm from '../../../../media/js/base/fxa-utm.es6.js';

describe('fxa-utm.js', function () {
    describe('getHostName', function () {
        it('should return a hostname as expected', function () {
            const url1 =
                'https://monitor.firefox.com/oauth/init?form_type=button&entrypoint=mozilla.org-firefox-accounts';
            const url2 =
                'https://accounts.firefox.com/?utm_campaign=campaign-one&utm_source=source-one&utm_content=content-one';
            const url3 =
                'https://getpocket.com/ff_signup?s=ffwelcome2&form_type=button&entrypoint=mozilla.org-firefox-welcome-2&utm_source=source-one&utm_campaign=campaign-one';

            expect(FxaUtm.getHostName(url1)).toEqual(
                'https://monitor.firefox.com/'
            );
            expect(FxaUtm.getHostName(url2)).toEqual(
                'https://accounts.firefox.com/'
            );
            expect(FxaUtm.getHostName(url3)).toEqual('https://getpocket.com/');
        });

        it('should return null if no match is found', function () {
            const url = 'thedude';
            expect(FxaUtm.getHostName(url)).toBeNull();
        });
    });

    describe('hasUtmParams', function () {
        it('should return true when utm params are present', function () {
            const data = {
                utm_source: 'vpn-client',
                utm_content: 'download-first-experiment',
                utm_medium: 'referral',
                entrypoint_experiment: 'test-id',
                entrypoint_variation: 'test-variation'
            };

            expect(FxaUtm.hasUtmParams(data)).toBeTruthy();
        });

        it('should return false when utm params are not present', function () {
            const data = {
                entrypoint_experiment: 'test-id',
                entrypoint_variation: 'test-variation'
            };

            expect(FxaUtm.hasUtmParams(data)).toBeFalsy();
        });

        it('should return false when data is not a valid object', function () {
            const data1 = undefined;
            expect(FxaUtm.hasUtmParams(data1)).toBeFalsy();
            const data2 = null;
            expect(FxaUtm.hasUtmParams(data2)).toBeFalsy();
            const data3 = {};
            expect(FxaUtm.hasUtmParams(data3)).toBeFalsy();
        });
    });

    describe('getAttributionData', function () {
        it('should return a valid object unchanged', function () {
            const validObj = {
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242,
                utm_campaign: 'F100_4242_otherstuff_in_here'
            };

            const validData = {
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: '4242',
                utm_campaign: 'F100_4242_otherstuff_in_here'
            };

            expect(FxaUtm.getAttributionData(validObj)).toEqual(validData);
        });

        it('should return a additional entrypoint params if present', function () {
            const validObj = {
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242,
                utm_campaign: 'F100_4242_otherstuff_in_here',
                entrypoint_experiment: 'test-id',
                entrypoint_variation: 'test-variation'
            };

            const validData = {
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: '4242',
                utm_campaign: 'F100_4242_otherstuff_in_here',
                entrypoint_experiment: 'test-id',
                entrypoint_variation: 'test-variation'
            };

            expect(FxaUtm.getAttributionData(validObj)).toEqual(validData);
        });

        it('should return entrypoint params if not utms are present', function () {
            const validObj = {
                entrypoint_experiment: 'test-id',
                entrypoint_variation: 'test-variation'
            };

            const validData = {
                entrypoint_experiment: 'test-id',
                entrypoint_variation: 'test-variation'
            };

            expect(FxaUtm.getAttributionData(validObj)).toEqual(validData);
        });

        it('should return FxA flow params if present together with experiment entrypoint params', function () {
            const validObj = {
                utm_source: 'vpn-client',
                utm_content: 'download-first-experiment',
                utm_medium: 'referral',
                utm_term: 4242,
                utm_campaign: 'F100_4242_otherstuff_in_here',
                entrypoint_experiment: 'test-id',
                entrypoint_variation: 'test-variation',
                device_id: 123456789,
                flow_id: 987654321,
                flow_begin_time: 1234567899
            };

            const validData = {
                utm_source: 'vpn-client',
                utm_content: 'download-first-experiment',
                utm_medium: 'referral',
                utm_term: '4242',
                utm_campaign: 'F100_4242_otherstuff_in_here',
                entrypoint_experiment: 'test-id',
                entrypoint_variation: 'test-variation',
                device_id: '123456789',
                flow_id: '987654321',
                flow_begin_time: '1234567899'
            };

            expect(FxaUtm.getAttributionData(validObj)).toEqual(validData);
        });

        it('should not return FxA flow params if experiment entrypoint params are also not present', function () {
            const validObj = {
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242,
                utm_campaign: 'F100_4242_otherstuff_in_here',
                device_id: 123456789,
                flow_id: 987654321,
                flow_begin_time: 1234567899
            };

            const validData = {
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: '4242',
                utm_campaign: 'F100_4242_otherstuff_in_here'
            };

            expect(FxaUtm.getAttributionData(validObj)).toEqual(validData);
        });

        it('should return entrypoint and utm params if supported source attribute is present', function () {
            const validObj1 = {
                source: 'whatsnew88'
            };

            const validData1 = {
                entrypoint: 'www.mozilla.org-whatsnew',
                utm_source: 'www.mozilla.org-whatsnew',
                utm_campaign: 'whatsnew88'
            };

            expect(FxaUtm.getAttributionData(validObj1)).toEqual(validData1);

            const validObj2 = {
                source: 'welcome9'
            };

            const validData2 = {
                entrypoint: 'www.mozilla.org-welcome',
                utm_source: 'www.mozilla.org-welcome',
                utm_campaign: 'welcome9'
            };

            expect(FxaUtm.getAttributionData(validObj2)).toEqual(validData2);
        });

        it('should return null if source attribute is non-specific', function () {
            const validObj = {
                source: 'the-dude'
            };

            expect(FxaUtm.getAttributionData(validObj)).toBeNull();
        });

        it('should return an object without any danagerous params', function () {
            const dangerousSource = {
                utm_source: 'www.mozilla.org',
                utm_campaign: 'rel-esr',
                utm_content: '<script>console.log("test");</script>'
            };

            const safeSource = {
                utm_source: 'www.mozilla.org',
                utm_campaign: 'rel-esr'
            };

            expect(FxaUtm.getAttributionData(dangerousSource)).toEqual(
                safeSource
            );
        });

        it('should not return an object if all params are unsafe', function () {
            const dangerousData = {
                utm_source: '%5C',
                utm_content: '%3C',
                utm_medium: '%24',
                utm_term: '%40',
                utm_campaign: '%22'
            };

            expect(FxaUtm.getAttributionData(dangerousData)).toBeNull();
        });

        it('should not return an object if utm_source is missing', function () {
            const data = {
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242,
                utm_campaign: 'F100_4242_otherstuff_in_here'
            };

            expect(FxaUtm.getAttributionData(data)).toBeNull();
        });

        it('should not return an object if utm_campaign is missing', function () {
            const data = {
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242
            };

            expect(FxaUtm.getAttributionData(data)).toBeNull();
        });

        it('should not strip allowed special characters', function () {
            const specialData = {
                utm_source: 'blog.mozilla.org',
                utm_campaign: 'my-experiment',
                utm_medium: '%25',
                utm_term: '%2F'
            };

            const specialSource = {
                utm_source: 'blog.mozilla.org',
                utm_campaign: 'my-experiment',
                utm_medium: '%',
                utm_term: '/'
            };

            expect(FxaUtm.getAttributionData(specialData)).toEqual(
                specialSource
            );
        });

        it('should decode URL components', function () {
            const encodedData = {
                utm_source: '%25',
                utm_campaign: '%2F'
            };

            const encodedSource = {
                utm_source: '%',
                utm_campaign: '/'
            };

            expect(FxaUtm.getAttributionData(encodedData)).toEqual(
                encodedSource
            );
        });

        it('should drop any malformed parameter values', function () {
            const encodedData = {
                utm_source: 'email',
                utm_campaign: 'fxa',
                utm_content: 'uns_footer%'
            };

            const encodedSource = {
                utm_source: 'email',
                utm_campaign: 'fxa'
            };

            expect(FxaUtm.getAttributionData(encodedData)).toEqual(
                encodedSource
            );
        });
    });

    describe('appendToDownloadURL', function () {
        it("should append a new query string if there isn't one", function () {
            const data = {
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242,
                utm_campaign: 'F100_4242_otherstuff_in_here'
            };

            const url = 'https://accounts.firefox.com/';

            expect(FxaUtm.appendToDownloadURL(url, data)).toEqual(
                'https://accounts.firefox.com/?utm_source=desktop-snippet&utm_content=rel-esr&utm_medium=referral&utm_term=4242&utm_campaign=F100_4242_otherstuff_in_here'
            );
        });

        it('should add UTM params without overwriting other query string params', function () {
            const data = {
                utm_source: 'test-source'
            };

            const url = 'https://accounts.firefox.com/?spice=pumpkin';

            expect(FxaUtm.appendToDownloadURL(url, data)).toEqual(
                'https://accounts.firefox.com/?spice=pumpkin&utm_source=test-source'
            );
        });

        it('should over-write existing UTM params', function () {
            const data = {
                utm_source: 'source-two',
                utm_content: 'content-two',
                utm_medium: 'medium-two',
                utm_term: 'term-two',
                utm_campaign: 'campaign-two'
            };

            const url =
                'https://accounts.firefox.com/?utm_medium=medium-one&utm_term=term-one&utm_campaign=campaign-one&utm_source=source-one&utm_content=content-one';

            expect(FxaUtm.appendToDownloadURL(url, data)).toEqual(
                'https://accounts.firefox.com/?utm_source=source-two&utm_content=content-two&utm_medium=medium-two&utm_term=term-two&utm_campaign=campaign-two'
            );
        });

        it('should not leave out new params if there are existing params to over write', function () {
            const data = {
                utm_source: 'source-two',
                utm_content: 'content-two',
                utm_medium: 'medium-two',
                utm_term: 'term-two',
                utm_campaign: 'campaign-two'
            };

            const url =
                'https://accounts.firefox.com/?utm_campaign=campaign-one&utm_source=source-one&utm_content=content-one';

            expect(FxaUtm.appendToDownloadURL(url, data)).toEqual(
                'https://accounts.firefox.com/?utm_source=source-two&utm_content=content-two&utm_medium=medium-two&utm_term=term-two&utm_campaign=campaign-two'
            );
        });

        it('should remove UTM params that are no longer present in the new referral data', function () {
            const data = {
                utm_source: 'source-two',
                utm_campaign: 'campaign-two'
            };

            const url =
                'https://accounts.firefox.com/?utm_campaign=campaign-one&utm_source=source-one&utm_content=content-one';

            expect(FxaUtm.appendToDownloadURL(url, data)).toEqual(
                'https://accounts.firefox.com/?utm_source=source-two&utm_campaign=campaign-two'
            );
        });

        it('should not override port, path, or file name', function () {
            const data = {
                utm_source: 'test-source'
            };

            const url =
                'https://accounts.firefox.com:8000/grande/nofat.html?spice=pumpkin';

            expect(FxaUtm.appendToDownloadURL(url, data)).toEqual(
                'https://accounts.firefox.com:8000/grande/nofat.html?spice=pumpkin&utm_source=test-source'
            );
        });

        it('should add additional entrypoint parameters if present', function () {
            const data = {
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242,
                utm_campaign: 'F100_4242_otherstuff_in_here',
                entrypoint_experiment: 'test-id',
                entrypoint_variation: 'test-variation'
            };

            const url = 'https://accounts.firefox.com/';

            expect(FxaUtm.appendToDownloadURL(url, data)).toEqual(
                'https://accounts.firefox.com/?utm_source=desktop-snippet&utm_content=rel-esr&utm_medium=referral&utm_term=4242&utm_campaign=F100_4242_otherstuff_in_here&entrypoint_experiment=test-id&entrypoint_variation=test-variation'
            );
        });

        it('should not wipe out existing utms if only enytrpoint params are present', function () {
            const data = {
                entrypoint_experiment: 'test-id',
                entrypoint_variation: 'test-variation'
            };

            const url =
                'https://accounts.firefox.com/?utm_medium=medium-one&utm_term=term-one&utm_campaign=campaign-one&utm_source=source-one&utm_content=content-one';

            expect(FxaUtm.appendToDownloadURL(url, data)).toEqual(
                'https://accounts.firefox.com/?utm_medium=medium-one&utm_term=term-one&utm_campaign=campaign-one&utm_source=source-one&utm_content=content-one&entrypoint_experiment=test-id&entrypoint_variation=test-variation'
            );
        });
    });

    describe('setFxALinkReferralCookie', function () {
        it('should set a referral cookie as expected', function () {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(Mozilla.Cookies, 'setItem');
            spyOn(FxaUtm, 'hasFxALinkReferralCookie').and.returnValue(false);

            FxaUtm.setFxALinkReferralCookie('navigation');

            expect(Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                'fxa-product-referral-id',
                'navigation',
                jasmine.any(String),
                '/'
            );
        });

        it('should not set a referral cookie if one already exists', function () {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(Mozilla.Cookies, 'setItem');
            spyOn(FxaUtm, 'hasFxALinkReferralCookie').and.returnValue(true);

            FxaUtm.setFxALinkReferralCookie('navigation');

            expect(Mozilla.Cookies.setItem).not.toHaveBeenCalled();
        });
    });

    describe('init', function () {
        beforeEach(function () {
            // assume cookie are enabled.
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(true);

            // assume DNT is disabled
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);

            // link to change
            const links = `<div id="test-links">
                    <a id="test-expected" class="js-fxa-cta-link" href="https://accounts.firefox.com/?service=sync&amp;action=email&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-accounts_page&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page">Create a Firefox Account</a>
                    <a id="test-not-accounts" class="js-fxa-cta-link" href="https://www.mozilla.org/?service=sync&amp;action=email&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-accounts_page&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page">Create a Firefox Account</a>
                    <a id="test-second-expected" class="js-fxa-cta-link" href="https://monitor.firefox.com/oauth/init?form_type=button&amp;entrypoint=mozilla.org-firefox-accounts&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page">Sign In to Firefox Monitor</a>
                    <a id="test-third-expected" class="js-fxa-cta-link" href="https://getpocket.com/ff_signup?s=ffwelcome2&form_type=button&entrypoint=mozilla.org-firefox-welcome-2&utm_source=mozilla.org-firefox-welcome-2&utm_campaign=welcome-2-pocket&utm_medium=referral">Activate Pocket</a>
                </div>`;

            document.body.insertAdjacentHTML('beforeend', links);
        });

        afterEach(function () {
            var content = document.getElementById('test-links');
            content.parentNode.removeChild(content);
        });

        it('should update the href of links with class js-fxa-cta-link', function () {
            const data = {
                utm_source: 'source-two',
                utm_content: 'content-two',
                utm_medium: 'medium-two',
                utm_term: 'term-two',
                utm_campaign: 'campaign-two'
            };

            FxaUtm.init(data);

            const expected = document.getElementById('test-expected');
            const expectedHref = expected.getAttribute('href');
            const secondExpected = document.getElementById(
                'test-second-expected'
            );
            const secondExpectedHref = secondExpected.getAttribute('href');
            const thirdExpected = document.getElementById(
                'test-third-expected'
            );
            const thirdExpectedHref = thirdExpected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_source=source-two&utm_campaign=campaign-two&utm_content=content-two&utm_term=term-two&utm_medium=medium-two'
            );
            expect(secondExpectedHref).toEqual(
                'https://monitor.firefox.com/oauth/init?form_type=button&entrypoint=mozilla.org-firefox-accounts&utm_source=source-two&utm_campaign=campaign-two&utm_content=content-two&utm_term=term-two&utm_medium=medium-two'
            );
            expect(thirdExpectedHref).toEqual(
                'https://getpocket.com/ff_signup?s=ffwelcome2&form_type=button&entrypoint=mozilla.org-firefox-welcome-2&utm_source=source-two&utm_campaign=campaign-two&utm_content=content-two&utm_term=term-two&utm_medium=medium-two'
            );
        });

        it('should not make changes if there are no UTM params', function () {
            const data = {};

            FxaUtm.init(data);

            const expected = document.getElementById('test-expected');
            const expectedHref = expected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page'
            );
        });

        it('should not make changes if the link is not in the FxA referral allowedList', function () {
            const data = {
                utm_source: 'source-two',
                utm_content: 'content-two',
                utm_medium: 'medium-two',
                utm_term: 'term-two',
                utm_campaign: 'campaign-two'
            };

            FxaUtm.init(data);

            const unexpected = document.getElementById('test-not-accounts');
            const unexpectedHref = unexpected.getAttribute('href');

            expect(unexpectedHref).toEqual(
                'https://www.mozilla.org/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page'
            );
        });

        it('should get referral cookie data if there are no UTM params', function () {
            const data = {};
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('navigation');
            spyOn(FxaUtm, 'hasFxALinkReferralCookie').and.returnValue(true);

            FxaUtm.init(data);

            const expected = document.getElementById('test-expected');
            const expectedHref = expected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=www.mozilla.org&utm_source=www.mozilla.org&utm_medium=referral&utm_campaign=navigation'
            );
        });

        it('should set expected values for in-product /whatsnew page referrals', function () {
            const data = {};
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('whatsnew92');
            spyOn(FxaUtm, 'hasFxALinkReferralCookie').and.returnValue(true);

            FxaUtm.init(data);

            const expected = document.getElementById('test-expected');
            const expectedHref = expected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=www.mozilla.org-whatsnew&utm_source=www.mozilla.org-whatsnew&utm_medium=referral&utm_campaign=whatsnew92'
            );
        });

        it('should set expected values for in-product /welcome page referrals', function () {
            const data = {};
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('welcome12');
            spyOn(FxaUtm, 'hasFxALinkReferralCookie').and.returnValue(true);

            FxaUtm.init(data);

            const expected = document.getElementById('test-expected');
            const expectedHref = expected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=www.mozilla.org-welcome&utm_source=www.mozilla.org-welcome&utm_medium=referral&utm_campaign=welcome12'
            );
        });

        it('should not overwrite other allowed non-UTM params when cookie referral data exists', function () {
            const data = {
                entrypoint_experiment: 'test-experiment',
                entrypoint_variation: 'test-variation'
            };
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('navigation');
            spyOn(FxaUtm, 'hasFxALinkReferralCookie').and.returnValue(true);

            FxaUtm.init(data);

            const expected = document.getElementById('test-expected');
            const expectedHref = expected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=www.mozilla.org&entrypoint_experiment=test-experiment&entrypoint_variation=test-variation&utm_source=www.mozilla.org&utm_medium=referral&utm_campaign=navigation'
            );
        });
    });
});
