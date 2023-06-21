/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import FxaAttribution from '../../../../media/js/base/fxa-attribution.es6.js';

describe('fxa-attribution.js', function () {
    beforeEach(function () {
        window.Mozilla.dntEnabled = sinon.stub();
    });

    describe('getHostName', function () {
        it('should return a hostname as expected', function () {
            const url1 =
                'https://monitor.firefox.com/oauth/init?form_type=button&entrypoint=mozilla.org-firefox-accounts';
            const url2 =
                'https://accounts.firefox.com/?utm_campaign=campaign-one&utm_source=source-one&utm_content=content-one';
            const url3 =
                'https://getpocket.com/ff_signup?s=ffwelcome2&form_type=button&entrypoint=mozilla.org-firefox-welcome-2&utm_source=source-one&utm_campaign=campaign-one';

            expect(FxaAttribution.getHostName(url1)).toEqual(
                'https://monitor.firefox.com/'
            );
            expect(FxaAttribution.getHostName(url2)).toEqual(
                'https://accounts.firefox.com/'
            );
            expect(FxaAttribution.getHostName(url3)).toEqual(
                'https://getpocket.com/'
            );
        });

        it('should return null if no match is found', function () {
            const url = 'thedude';
            expect(FxaAttribution.getHostName(url)).toBeNull();
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

            expect(FxaAttribution.getAttributionData(validObj)).toEqual(
                validData
            );
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

            expect(FxaAttribution.getAttributionData(validObj)).toEqual(
                validData
            );
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

            expect(FxaAttribution.getAttributionData(validObj)).toEqual(
                validData
            );
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

            expect(FxaAttribution.getAttributionData(validObj)).toEqual(
                validData
            );
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

            expect(FxaAttribution.getAttributionData(validObj)).toEqual(
                validData
            );
        });

        it('should return an object without any dangerous params', function () {
            const dangerousSource = {
                utm_source: 'www.mozilla.org',
                utm_campaign: 'rel-esr',
                utm_content: '<script>console.log("test");</script>'
            };

            const safeSource = {
                utm_source: 'www.mozilla.org',
                utm_campaign: 'rel-esr'
            };

            expect(FxaAttribution.getAttributionData(dangerousSource)).toEqual(
                safeSource
            );
        });

        it('should return an empty object if all params are unsafe', function () {
            const dangerousData = {
                utm_source: '%5C',
                utm_content: '%3C',
                utm_medium: '%24',
                utm_term: '%40',
                utm_campaign: '%22'
            };

            const result = FxaAttribution.getAttributionData(dangerousData);
            expect(Object.keys(result).length).toEqual(0);
        });

        it('should return an empty object if utm_source is missing', function () {
            const data = {
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242,
                utm_campaign: 'F100_4242_otherstuff_in_here'
            };

            const result = FxaAttribution.getAttributionData(data);
            expect(Object.keys(result).length).toEqual(0);
        });

        it('should return an empty object if utm_campaign is missing', function () {
            const data = {
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242
            };

            const result = FxaAttribution.getAttributionData(data);
            expect(Object.keys(result).length).toEqual(0);
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

            expect(FxaAttribution.getAttributionData(specialData)).toEqual(
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

            expect(FxaAttribution.getAttributionData(encodedData)).toEqual(
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

            expect(FxaAttribution.getAttributionData(encodedData)).toEqual(
                encodedSource
            );
        });
    });

    describe('appendToProductURL', function () {
        it("should append a new query string if there isn't one", function () {
            const data = {
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242,
                utm_campaign: 'F100_4242_otherstuff_in_here'
            };

            const url = 'https://accounts.firefox.com/';

            expect(FxaAttribution.appendToProductURL(url, data)).toEqual(
                'https://accounts.firefox.com/?utm_source=desktop-snippet&utm_content=rel-esr&utm_medium=referral&utm_term=4242&utm_campaign=F100_4242_otherstuff_in_here'
            );
        });

        it('should add UTM params without overwriting other query string params', function () {
            const data = {
                utm_source: 'test-source'
            };

            const url = 'https://accounts.firefox.com/?spice=pumpkin';

            expect(FxaAttribution.appendToProductURL(url, data)).toEqual(
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

            expect(FxaAttribution.appendToProductURL(url, data)).toEqual(
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

            expect(FxaAttribution.appendToProductURL(url, data)).toEqual(
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

            expect(FxaAttribution.appendToProductURL(url, data)).toEqual(
                'https://accounts.firefox.com/?utm_source=source-two&utm_campaign=campaign-two'
            );
        });

        it('should not override port, path, or file name', function () {
            const data = {
                utm_source: 'test-source'
            };

            const url =
                'https://accounts.firefox.com:8000/grande/nofat.html?spice=pumpkin';

            expect(FxaAttribution.appendToProductURL(url, data)).toEqual(
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

            expect(FxaAttribution.appendToProductURL(url, data)).toEqual(
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

            expect(FxaAttribution.appendToProductURL(url, data)).toEqual(
                'https://accounts.firefox.com/?utm_medium=medium-one&utm_term=term-one&utm_campaign=campaign-one&utm_source=source-one&utm_content=content-one&entrypoint_experiment=test-id&entrypoint_variation=test-variation'
            );
        });

        it('should append coupon parameter when present', function () {
            const data = {
                coupon: 'test'
            };

            const url =
                'https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=pricing';

            expect(FxaAttribution.appendToProductURL(url, data)).toEqual(
                'https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=pricing&coupon=test'
            );
        });
    });

    describe('getSearchReferralData', function () {
        it('should return correct utms for google referrals', function () {
            const expected = {
                utm_medium: 'organic',
                utm_source: 'google'
            };
            const supportedDomains = [
                'https://www.google.com',
                'https://www.google.com/search?q=firefox',
                'https://www.google.com.au',
                'https://www.google.co.ma/',
                'https://www.google.de',
                'https://www.google.fr/',
                'https://www.google.cat/'
            ];

            supportedDomains.forEach((domain) => {
                expect(FxaAttribution.getSearchReferralData(domain)).toEqual(
                    expected
                );
            });
        });

        it('should return correct utms for bing referrals', function () {
            const expected = {
                utm_medium: 'organic',
                utm_source: 'bing'
            };
            const supportedDomains = [
                'https://www.bing.com',
                'https://www.bing.com/?cc=gb',
                'https://www.bing.com/search?q=firefox'
            ];

            supportedDomains.forEach((domain) => {
                expect(FxaAttribution.getSearchReferralData(domain)).toEqual(
                    expected
                );
            });
        });

        it('should return correct utms for yahoo referrals', function () {
            const expected = {
                utm_medium: 'organic',
                utm_source: 'yahoo'
            };
            const supportedDomains = [
                'https://search.yahoo.com',
                'https://uk.search.yahoo.com',
                'https://de.search.yahoo.com/search'
            ];

            supportedDomains.forEach((domain) => {
                expect(FxaAttribution.getSearchReferralData(domain)).toEqual(
                    expected
                );
            });
        });

        it('should return correct utms for duckduckgo referrals', function () {
            const expected = {
                utm_medium: 'organic',
                utm_source: 'duckduckgo'
            };
            const supportedDomains = [
                'https://duckduckgo.com/',
                'https://duckduckgo.com/?q=firefox'
            ];

            supportedDomains.forEach((domain) => {
                expect(FxaAttribution.getSearchReferralData(domain)).toEqual(
                    expected
                );
            });
        });

        it('should return correct utms for yandex referrals', function () {
            const expected = {
                utm_medium: 'organic',
                utm_source: 'yandex'
            };
            const supportedDomains = [
                'https://yandex.com',
                'https://yandex.com/search/?text=firefox',
                'https://yandex.ru/',
                'https://yandex.com.tr'
            ];

            supportedDomains.forEach((domain) => {
                expect(FxaAttribution.getSearchReferralData(domain)).toEqual(
                    expected
                );
            });
        });

        it('should return correct utms for baidu referrals', function () {
            const expected = {
                utm_medium: 'organic',
                utm_source: 'baidu'
            };
            const supportedDomains = [
                'https://www.baidu.com',
                'https://www.baidu.com/s?wd=firefox'
            ];

            supportedDomains.forEach((domain) => {
                expect(FxaAttribution.getSearchReferralData(domain)).toEqual(
                    expected
                );
            });
        });

        it('should return correct utms for naver referrals', function () {
            const expected = {
                utm_medium: 'organic',
                utm_source: 'naver'
            };
            const supportedDomains = [
                'https://search.naver.com',
                'https://search.naver.com/search.naver?query=firefox'
            ];

            supportedDomains.forEach((domain) => {
                expect(FxaAttribution.getSearchReferralData(domain)).toEqual(
                    expected
                );
            });
        });
    });

    describe('setFxALinkReferralCookie', function () {
        it('should set a referral cookie as expected', function () {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(Mozilla.Cookies, 'setItem');
            spyOn(FxaAttribution, 'hasFxALinkReferralCookie').and.returnValue(
                false
            );

            FxaAttribution.setFxALinkReferralCookie('navigation');

            expect(Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                'fxa-product-referral-id',
                'navigation',
                jasmine.any(String),
                '/',
                undefined,
                false,
                'lax'
            );
        });

        it('should not set a referral cookie if one already exists', function () {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(Mozilla.Cookies, 'setItem');
            spyOn(FxaAttribution, 'hasFxALinkReferralCookie').and.returnValue(
                true
            );

            FxaAttribution.setFxALinkReferralCookie('navigation');

            expect(Mozilla.Cookies.setItem).not.toHaveBeenCalled();
        });
    });

    describe('init', function () {
        beforeEach(function () {
            // assume cookie are enabled.
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(true);

            // link to change
            const links = `<div id="test-links">
                    <a id="test-expected" class="js-fxa-cta-link" href="https://accounts.firefox.com/?service=sync&amp;action=email&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-accounts_page&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page">Create a Firefox Account</a>
                    <a id="test-not-accounts" class="js-fxa-cta-link" href="https://www.mozilla.org/?service=sync&amp;action=email&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-accounts_page&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page">Create a Firefox Account</a>
                    <a id="test-second-expected" class="js-fxa-cta-link" href="https://monitor.firefox.com/oauth/init?form_type=button&amp;entrypoint=mozilla.org-firefox-accounts&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page">Sign In to Firefox Monitor</a>
                    <a id="test-third-expected" class="js-fxa-cta-link" href="https://getpocket.com/ff_signup?s=ffwelcome2&form_type=button&entrypoint=mozilla.org-firefox-welcome-2&utm_source=mozilla.org-firefox-welcome-2&utm_campaign=welcome-2-pocket&utm_medium=referral">Activate Pocket</a>
                    <a id="test-subscription" class="js-fxa-product-cta-link" href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7&amp;entrypoint=www.mozilla.org-vpn-product-page&amp;form_type=button&amp;service=e6eb0d1e856335fc&amp;utm_source=www.mozilla.org-vpn-product-page&amp;utm_medium=referral&amp;utm_campaign=vpn-product-page&amp;data_cta_position=pricing">Get Mozilla VPN</a>
                </div>`;

            document.body.insertAdjacentHTML('beforeend', links);
        });

        afterEach(function () {
            var content = document.getElementById('test-links');
            content.parentNode.removeChild(content);
        });

        it('should update UTM parameters on links with class js-fxa-cta-link and js-fxa-product-cta-link', function () {
            const data = {
                utm_source: 'source-two',
                utm_content: 'content-two',
                utm_medium: 'medium-two',
                utm_term: 'term-two',
                utm_campaign: 'campaign-two'
            };

            FxaAttribution.init(data);

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
            const fourthExpected = document.getElementById('test-subscription');
            const fourthExpectedHref = fourthExpected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_source=source-two&utm_campaign=campaign-two&utm_content=content-two&utm_term=term-two&utm_medium=medium-two'
            );
            expect(secondExpectedHref).toEqual(
                'https://monitor.firefox.com/oauth/init?form_type=button&entrypoint=mozilla.org-firefox-accounts&utm_source=source-two&utm_campaign=campaign-two&utm_content=content-two&utm_term=term-two&utm_medium=medium-two'
            );
            expect(thirdExpectedHref).toEqual(
                'https://getpocket.com/ff_signup?s=ffwelcome2&form_type=button&entrypoint=mozilla.org-firefox-welcome-2&utm_source=source-two&utm_campaign=campaign-two&utm_content=content-two&utm_term=term-two&utm_medium=medium-two'
            );
            expect(fourthExpectedHref).toEqual(
                'https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&data_cta_position=pricing&utm_source=source-two&utm_campaign=campaign-two&utm_content=content-two&utm_term=term-two&utm_medium=medium-two'
            );
        });

        it('should not make changes if there are no UTM params', function () {
            const data = {};

            FxaAttribution.init(data);

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

            FxaAttribution.init(data);

            const unexpected = document.getElementById('test-not-accounts');
            const unexpectedHref = unexpected.getAttribute('href');

            expect(unexpectedHref).toEqual(
                'https://www.mozilla.org/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page'
            );
        });

        it('should pass experimental parameters to FxA links', function () {
            const data = {
                entrypoint_experiment: 'test-experiment',
                entrypoint_variation: 'test-variation',
                device_id: '10646c078bb9484585971c1451fc2ab2',
                flow_begin_time: '1683735311599',
                flow_id:
                    '2f8d4301abb8b864ff76ee9058e5cdc1e727fe286ad6ea47a698fd430c4d3222'
            };

            spyOn(FxaAttribution, 'hasFxALinkReferralCookie').and.returnValue(
                false
            );
            spyOn(FxaAttribution, 'getSearchReferralData').and.returnValue(
                null
            );

            FxaAttribution.init(data);

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
            const fourthExpected = document.getElementById('test-subscription');
            const fourthExpectedHref = fourthExpected.getAttribute('href');

            const unexpected = document.getElementById('test-not-accounts');
            const unexpectedHref = unexpected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page&device_id=10646c078bb9484585971c1451fc2ab2&flow_id=2f8d4301abb8b864ff76ee9058e5cdc1e727fe286ad6ea47a698fd430c4d3222&flow_begin_time=1683735311599&entrypoint_experiment=test-experiment&entrypoint_variation=test-variation'
            );
            expect(secondExpectedHref).toEqual(
                'https://monitor.firefox.com/oauth/init?form_type=button&entrypoint=mozilla.org-firefox-accounts&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page&device_id=10646c078bb9484585971c1451fc2ab2&flow_id=2f8d4301abb8b864ff76ee9058e5cdc1e727fe286ad6ea47a698fd430c4d3222&flow_begin_time=1683735311599&entrypoint_experiment=test-experiment&entrypoint_variation=test-variation'
            );
            expect(thirdExpectedHref).toEqual(
                'https://getpocket.com/ff_signup?s=ffwelcome2&form_type=button&entrypoint=mozilla.org-firefox-welcome-2&utm_source=mozilla.org-firefox-welcome-2&utm_campaign=welcome-2-pocket&utm_medium=referral&device_id=10646c078bb9484585971c1451fc2ab2&flow_id=2f8d4301abb8b864ff76ee9058e5cdc1e727fe286ad6ea47a698fd430c4d3222&flow_begin_time=1683735311599&entrypoint_experiment=test-experiment&entrypoint_variation=test-variation'
            );
            expect(fourthExpectedHref).toEqual(
                'https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=pricing&device_id=10646c078bb9484585971c1451fc2ab2&flow_id=2f8d4301abb8b864ff76ee9058e5cdc1e727fe286ad6ea47a698fd430c4d3222&flow_begin_time=1683735311599&entrypoint_experiment=test-experiment&entrypoint_variation=test-variation'
            );
            expect(unexpectedHref).toEqual(
                'https://www.mozilla.org/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page'
            );
        });

        it('should pass coupon parameter only to FxA subscription links', function () {
            const data = {
                coupon: 'test'
            };
            spyOn(FxaAttribution, 'hasFxALinkReferralCookie').and.returnValue(
                false
            );
            spyOn(FxaAttribution, 'getSearchReferralData').and.returnValue(
                null
            );

            FxaAttribution.init(data);

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
            const fourthExpected = document.getElementById('test-subscription');
            const fourthExpectedHref = fourthExpected.getAttribute('href');

            const unexpected = document.getElementById('test-not-accounts');
            const unexpectedHref = unexpected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page'
            );
            expect(secondExpectedHref).toEqual(
                'https://monitor.firefox.com/oauth/init?form_type=button&entrypoint=mozilla.org-firefox-accounts&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page'
            );
            expect(thirdExpectedHref).toEqual(
                'https://getpocket.com/ff_signup?s=ffwelcome2&form_type=button&entrypoint=mozilla.org-firefox-welcome-2&utm_source=mozilla.org-firefox-welcome-2&utm_campaign=welcome-2-pocket&utm_medium=referral'
            );
            expect(fourthExpectedHref).toEqual(
                'https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=pricing&coupon=test'
            );
            expect(unexpectedHref).toEqual(
                'https://www.mozilla.org/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page'
            );
        });

        it('should handle padding all accepted query parameters together', function () {
            const data = {
                utm_source: 'source-two',
                utm_content: 'content-two',
                utm_medium: 'medium-two',
                utm_term: 'term-two',
                utm_campaign: 'campaign-two',
                entrypoint_experiment: 'test-experiment',
                entrypoint_variation: 'test-variation',
                coupon: 'test'
            };
            spyOn(FxaAttribution, 'hasFxALinkReferralCookie').and.returnValue(
                false
            );
            spyOn(FxaAttribution, 'getSearchReferralData').and.returnValue(
                null
            );

            FxaAttribution.init(data);

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
            const fourthExpected = document.getElementById('test-subscription');
            const fourthExpectedHref = fourthExpected.getAttribute('href');

            const unexpected = document.getElementById('test-not-accounts');
            const unexpectedHref = unexpected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_source=source-two&utm_campaign=campaign-two&utm_content=content-two&utm_term=term-two&utm_medium=medium-two&entrypoint_experiment=test-experiment&entrypoint_variation=test-variation'
            );
            expect(secondExpectedHref).toEqual(
                'https://monitor.firefox.com/oauth/init?form_type=button&entrypoint=mozilla.org-firefox-accounts&utm_source=source-two&utm_campaign=campaign-two&utm_content=content-two&utm_term=term-two&utm_medium=medium-two&entrypoint_experiment=test-experiment&entrypoint_variation=test-variation'
            );
            expect(thirdExpectedHref).toEqual(
                'https://getpocket.com/ff_signup?s=ffwelcome2&form_type=button&entrypoint=mozilla.org-firefox-welcome-2&utm_source=source-two&utm_campaign=campaign-two&utm_content=content-two&utm_term=term-two&utm_medium=medium-two&entrypoint_experiment=test-experiment&entrypoint_variation=test-variation'
            );
            expect(fourthExpectedHref).toEqual(
                'https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&data_cta_position=pricing&utm_source=source-two&utm_campaign=campaign-two&utm_content=content-two&utm_term=term-two&utm_medium=medium-two&entrypoint_experiment=test-experiment&entrypoint_variation=test-variation&coupon=test'
            );
            expect(unexpectedHref).toEqual(
                'https://www.mozilla.org/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=accounts-page&utm_medium=referral&utm_campaign=fxa-benefits-page'
            );
        });

        it('should get referral cookie data if there are no UTM params', function () {
            const data = {};
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('navigation');
            spyOn(FxaAttribution, 'hasFxALinkReferralCookie').and.returnValue(
                true
            );

            FxaAttribution.init(data);

            const expected = document.getElementById('test-expected');
            const expectedHref = expected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=www.mozilla.org&utm_source=www.mozilla.org&utm_medium=referral&utm_campaign=navigation'
            );
        });

        it('should set expected values for in-product /whatsnew page referrals', function () {
            const data = {};
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('whatsnew92');
            spyOn(FxaAttribution, 'hasFxALinkReferralCookie').and.returnValue(
                true
            );

            FxaAttribution.init(data);

            const expected = document.getElementById('test-expected');
            const expectedHref = expected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=www.mozilla.org-whatsnew&utm_source=www.mozilla.org-whatsnew&utm_medium=referral&utm_campaign=whatsnew92'
            );
        });

        it('should set expected values for in-product /welcome page referrals', function () {
            const data = {};
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('welcome12');
            spyOn(FxaAttribution, 'hasFxALinkReferralCookie').and.returnValue(
                true
            );

            FxaAttribution.init(data);

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
            spyOn(FxaAttribution, 'hasFxALinkReferralCookie').and.returnValue(
                true
            );

            FxaAttribution.init(data);

            const expected = document.getElementById('test-expected');
            const expectedHref = expected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=www.mozilla.org&utm_source=www.mozilla.org&utm_medium=referral&utm_campaign=navigation&entrypoint_experiment=test-experiment&entrypoint_variation=test-variation'
            );
        });

        it('should pass through search referral data if there are no UTM params present in the page', function () {
            const data = {};
            spyOn(FxaAttribution, 'hasFxALinkReferralCookie').and.returnValue(
                false
            );
            spyOn(FxaAttribution, 'getSearchReferralData').and.returnValue({
                utm_medium: 'organic',
                utm_source: 'google'
            });

            FxaAttribution.init(data);

            const expected = document.getElementById('test-expected');
            const expectedHref = expected.getAttribute('href');

            expect(expectedHref).toEqual(
                'https://accounts.firefox.com/?service=sync&action=email&context=fx_desktop_v3&entrypoint=mozilla.org-accounts_page&utm_content=accounts-page-top-cta&utm_source=google&utm_medium=organic&utm_campaign=fxa-benefits-page'
            );
        });
    });
});
