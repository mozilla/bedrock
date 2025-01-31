/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    consentRequired,
    getConsentCookie,
    getConsentState,
    getHostName,
    hasConsentCookie,
    isFirefoxDownloadThanks,
    isURLExceptionAllowed,
    isURLPermitted,
    setConsentCookie
} from '../../../../../media/js/base/consent/utils.es6';

describe('consentRequired()', function () {
    afterEach(function () {
        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');
    });

    it('should return true when expected', function () {
        document
            .getElementsByTagName('html')[0]
            .setAttribute('data-needs-consent', 'True');
        expect(consentRequired()).toBeTrue();
    });

    it('should return false when expected', function () {
        document
            .getElementsByTagName('html')[0]
            .setAttribute('data-needs-consent', 'False');
        expect(consentRequired()).toBeFalse();
    });

    it('should return false when data attribute is missing', function () {
        expect(consentRequired()).toBeFalse();
    });

    it('should return false when data attribute is bad value', function () {
        document
            .getElementsByTagName('html')[0]
            .setAttribute('data-needs-consent', 'undefined');
        expect(consentRequired()).toBeFalse();
    });
});

describe('getConsentCookie()', function () {
    it('should return consent object if a consent cookie exists', function () {
        const obj = {
            analytics: true,
            preference: true
        };
        spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
            JSON.stringify(obj)
        );
        const consent = getConsentCookie();
        expect(consent).toEqual(obj);
        expect(window.Mozilla.Cookies.getItem).toHaveBeenCalledWith(
            'moz-consent-pref'
        );
    });

    it('should return false if a consent cookie does not exist', function () {
        spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(false);
        expect(getConsentCookie()).toBeFalse();
    });
});

describe('getConsentState()', function () {
    describe('Global visitors', function () {
        it('should return the expected state when GPC is enabled', function () {
            const stateA = getConsentState({
                hasConsentCookie: false,
                gpcEnabled: true,
                dntEnabled: false,
                consentRequired: false,
                isURLExceptionAllowed: false,
                isURLPermitted: false
            });
            expect(stateA).toEqual('STATE_GPC_ENABLED');

            const stateB = getConsentState({
                hasConsentCookie: true,
                gpcEnabled: true,
                dntEnabled: false,
                consentRequired: true,
                isURLExceptionAllowed: false,
                isURLPermitted: true
            });
            expect(stateB).toEqual('STATE_GPC_ENABLED');
        });

        it('should return the expected state when DNT is enabled', function () {
            const stateA = getConsentState({
                hasConsentCookie: false,
                gpcEnabled: false,
                dntEnabled: true,
                consentRequired: false,
                isURLExceptionAllowed: false,
                isURLPermitted: false
            });
            expect(stateA).toEqual('STATE_DNT_ENABLED');

            const stateB = getConsentState({
                hasConsentCookie: true,
                gpcEnabled: false,
                dntEnabled: true,
                consentRequired: true,
                isURLExceptionAllowed: false,
                isURLPermitted: true
            });
            expect(stateB).toEqual('STATE_DNT_ENABLED');
        });
    });

    describe('Non-EU visitors (explicit consent not required)', function () {
        it('should return the expected state when consent cookie does not exist', function () {
            const state = getConsentState({
                hasConsentCookie: false,
                gpcEnabled: false,
                dntEnabled: false,
                consentRequired: false,
                isURLExceptionAllowed: false,
                isURLPermitted: false
            });
            expect(state).toEqual('STATE_COOKIES_PERMITTED');
        });

        it('should return the expected state when consent cookie does exist', function () {
            const state = getConsentState({
                hasConsentCookie: true,
                gpcEnabled: false,
                dntEnabled: false,
                consentRequired: false,
                isURLExceptionAllowed: false,
                isURLPermitted: false
            });
            expect(state).toEqual('STATE_HAS_CONSENT_COOKIE');
        });
    });

    describe('EU visitors (explicit consent required)', function () {
        it('should return the expected state when banner is permitted for the page and consent cookie exists', function () {
            const state = getConsentState({
                hasConsentCookie: true,
                gpcEnabled: false,
                dntEnabled: false,
                consentRequired: true,
                isURLExceptionAllowed: false,
                isURLPermitted: true
            });
            expect(state).toEqual('STATE_HAS_CONSENT_COOKIE');
        });

        it('should return the expected state when banner is permitted for the page and no existing consent cookie', function () {
            const state = getConsentState({
                hasConsentCookie: false,
                gpcEnabled: false,
                dntEnabled: false,
                consentRequired: true,
                isURLExceptionAllowed: false,
                isURLPermitted: true
            });
            expect(state).toEqual('STATE_SHOW_COOKIE_BANNER');
        });

        it('should return the expected state when banner is not permitted for the page', function () {
            const state = getConsentState({
                hasConsentCookie: true,
                gpcEnabled: false,
                dntEnabled: false,
                consentRequired: true,
                isURLExceptionAllowed: false,
                isURLPermitted: false
            });
            expect(state).toEqual('STATE_BANNER_NOT_PERMITTED');
        });

        it('should return the expected state when URL exception is allowed and consent cookie exists', function () {
            const state = getConsentState({
                hasConsentCookie: true,
                gpcEnabled: false,
                dntEnabled: false,
                consentRequired: true,
                isURLExceptionAllowed: true,
                isURLPermitted: false
            });
            expect(state).toEqual('STATE_HAS_CONSENT_COOKIE');
        });

        it('should return the expected state when URL exception is allowed and no existing consent cookie', function () {
            const state = getConsentState({
                hasConsentCookie: false,
                gpcEnabled: false,
                dntEnabled: false,
                consentRequired: true,
                isURLExceptionAllowed: true,
                isURLPermitted: false
            });
            expect(state).toEqual('STATE_SHOW_COOKIE_BANNER');
        });
    });
});

describe('getHostName()', function () {
    it('should return ".mozilla.org" when hostname matches', function () {
        const expected = '.mozilla.org';
        expect(getHostName('www.mozilla.org')).toEqual(expected);
        expect(getHostName('future.mozilla.org')).toEqual(expected);
        expect(getHostName('support.mozilla.org')).toEqual(expected);
        expect(getHostName('addons.mozilla.org')).toEqual(expected);
        expect(getHostName('bugzilla.mozilla.org')).toEqual(expected);
    });

    it('should return ".allizom.org" when hostname matches', function () {
        const expected = '.allizom.org';
        expect(getHostName('www.allizom.org')).toEqual(expected);
        expect(getHostName('www-dev.allizom.org')).toEqual(expected);
        expect(getHostName('www-demo1.allizom.org')).toEqual(expected);
    });

    it('should return null for other hostnames', function () {
        expect(getHostName('localhost')).toEqual(null);
        expect(getHostName('127.0.0.1')).toEqual(null);
        expect(getHostName('bedrock-stage.gcp.moz.works')).toEqual(null);
    });
});

describe('hasConsentCookie()', function () {
    it('should return true if a consent cookie exists', function () {
        spyOn(window.Mozilla.Cookies, 'enabled').and.returnValue(true);
        spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(true);
        expect(hasConsentCookie()).toBeTrue();
        expect(window.Mozilla.Cookies.hasItem).toHaveBeenCalledWith(
            'moz-consent-pref'
        );
    });

    it('should return false if a consent cookie does not exist', function () {
        spyOn(window.Mozilla.Cookies, 'enabled').and.returnValue(true);
        spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(false);
        expect(hasConsentCookie()).toBeFalse();
    });

    it('should return false if a cookies are disabled', function () {
        spyOn(window.Mozilla.Cookies, 'enabled').and.returnValue(false);
        spyOn(window.Mozilla.Cookies, 'hasItem');
        expect(hasConsentCookie()).toBeFalse();
    });
});

describe('isFirefoxDownloadThanks()', function () {
    it('should return true if URL is /thanks/', function () {
        expect(
            isFirefoxDownloadThanks(
                'https://www.mozilla.org/en-US/firefox/download/thanks/'
            )
        ).toBeTrue();
        expect(
            isFirefoxDownloadThanks(
                'https://www.allizom.org/en-US/firefox/download/thanks/'
            )
        ).toBeTrue();
        expect(
            isFirefoxDownloadThanks(
                'https://localhost:8000/en-US/firefox/download/thanks/'
            )
        ).toBeTrue();
    });

    it('should return false if URL is not /thanks/', function () {
        expect(
            isFirefoxDownloadThanks(
                'https://www.mozilla.org/en-US/firefox/download/'
            )
        ).toBeFalse();
        expect(
            isFirefoxDownloadThanks(
                'https://www.allizom.org/en-US/firefox/download/'
            )
        ).toBeFalse();
        expect(
            isFirefoxDownloadThanks(
                'https://localhost:8000/en-US/firefox/download/'
            )
        ).toBeFalse();
        expect(isFirefoxDownloadThanks('')).toBeFalse();
        expect(isFirefoxDownloadThanks(null)).toBeFalse();
        expect(isFirefoxDownloadThanks(undefined)).toBeFalse();
        expect(isFirefoxDownloadThanks(true)).toBeFalse();
    });
});

describe('isURLExceptionAllowed()', function () {
    it('should return true for URL exceptions', function () {
        expect(isURLExceptionAllowed('?mozcb=y')).toBeTrue();
        expect(isURLExceptionAllowed('?mozcb=y&foo=bar')).toBeTrue();
        expect(isURLExceptionAllowed('?foo=bar&mozcb=y')).toBeTrue();
        expect(isURLExceptionAllowed('?foo=bar&mozcb=y&baz=qux')).toBeTrue();
    });

    it('should return false for URLs without exceptions', function () {
        expect(isURLExceptionAllowed('?mozcb=n')).toBeFalse();
        expect(isURLExceptionAllowed('?mozcb=n&foo=bar')).toBeFalse();
        expect(isURLExceptionAllowed('?foo=bar&mozcb=n')).toBeFalse();
        expect(isURLExceptionAllowed('?foo=bar&mozcb=n&baz=qux')).toBeFalse();
        expect(isURLExceptionAllowed('')).toBeFalse();
        expect(isURLExceptionAllowed(null)).toBeFalse();
        expect(isURLExceptionAllowed(undefined)).toBeFalse();
        expect(isURLExceptionAllowed(true)).toBeFalse();
    });
});

describe('isURLPermitted()', function () {
    it('should return true for pathnames in the allow-list', function () {
        expect(isURLPermitted('/en-US/newsletter/')).toBeTrue();
    });

    it('should true for pathnames in the allow list irrespective of page locale', function () {
        expect(isURLPermitted('/en-US/newsletter/')).toBeTrue();
        expect(isURLPermitted('/de/newsletter/')).toBeTrue();
    });

    it('should still true for allowed pathnames when locale is omitted', function () {
        expect(isURLPermitted('/newsletter/')).toBeTrue();
    });

    it('should return false for pathnames not in the allow-list', function () {
        expect(isURLPermitted('/en-US/firefox/')).toBeFalse();
        expect(isURLPermitted('/en-US/firefox/download/')).toBeFalse();
        expect(isURLPermitted('/en-US/firefox/download/all/')).toBeFalse();
        expect(
            isURLPermitted('/en-US/firefox/124.0.2/releasenotes/')
        ).toBeFalse();
        expect(
            isURLPermitted('/en-US/privacy/websites/cookie-settings/')
        ).toBeFalse();
    });
});

describe('setConsentCookie()', function () {
    it('should set a consent cookie as expected', function () {
        const data = {
            analytics: false,
            preference: true
        };
        spyOn(window.Mozilla.Cookies, 'setItem');
        const result = setConsentCookie(data);
        expect(result).toBeTrue();
        expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
            'moz-consent-pref',
            '{"analytics":false,"preference":true}',
            jasmine.any(String),
            '/',
            null,
            false,
            'lax'
        );
    });

    it('should return false when an object is not passed correctly', function () {
        spyOn(window.Mozilla.Cookies, 'setItem');
        const data = true;
        const result = setConsentCookie(data);
        expect(result).toBeFalse();
    });
});
