/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

import DataPreferencesCookie from '../../../../media/js/privacy/data-preferences-cookie.es6';

describe('doOptOut', function () {
    it('should set an opt-out cookie as expected', function () {
        spyOn(DataPreferencesCookie, 'hasOptedOut').and.returnValue(false);
        spyOn(DataPreferencesCookie, 'getCookieDomain').and.returnValue(
            '.mozilla.org'
        );
        spyOn(window.Mozilla.Cookies, 'setItem');
        DataPreferencesCookie.doOptOut();
        expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
            'moz-1st-party-data-opt-out',
            'true',
            jasmine.any(String),
            '/',
            '.mozilla.org',
            false,
            'lax'
        );
    });

    it('should do nothing if visitor has already opted out', function () {
        spyOn(DataPreferencesCookie, 'hasOptedOut').and.returnValue(true);
        spyOn(window.Mozilla.Cookies, 'setItem');
        DataPreferencesCookie.doOptOut();
        expect(window.Mozilla.Cookies.setItem).not.toHaveBeenCalled();
    });
});

describe('doOptIn', function () {
    it('should remove opt-out cookie as expected', function () {
        spyOn(DataPreferencesCookie, 'hasOptedOut').and.returnValue(true);
        spyOn(DataPreferencesCookie, 'getCookieDomain').and.returnValue(
            '.mozilla.org'
        );
        spyOn(window.Mozilla.Cookies, 'removeItem');
        DataPreferencesCookie.doOptIn();
        expect(window.Mozilla.Cookies.removeItem).toHaveBeenCalledWith(
            'moz-1st-party-data-opt-out',
            '/',
            '.mozilla.org',
            false,
            'lax'
        );
    });

    it('should do nothing if visitor has already opted in', function () {
        spyOn(DataPreferencesCookie, 'hasOptedOut').and.returnValue(false);
        spyOn(window.Mozilla.Cookies, 'removeItem');
        DataPreferencesCookie.doOptIn();
        expect(window.Mozilla.Cookies.removeItem).not.toHaveBeenCalled();
    });

    // See https://github.com/mozilla/bedrock/issues/12056
    it('should also remove pre-existing cookies that specified the www.mozilla.org subdomain', function () {
        spyOn(DataPreferencesCookie, 'hasOptedOut').and.returnValue(true);
        spyOn(DataPreferencesCookie, 'getCookieDomain').and.returnValue(
            '.mozilla.org'
        );
        spyOn(window.Mozilla.Cookies, 'removeItem');
        spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(true);
        DataPreferencesCookie.doOptIn();
        expect(window.Mozilla.Cookies.removeItem).toHaveBeenCalledTimes(2);
        expect(Mozilla.Cookies.hasItem).toHaveBeenCalledWith(
            'moz-1st-party-data-opt-out'
        );
        expect(window.Mozilla.Cookies.removeItem).toHaveBeenCalledWith(
            'moz-1st-party-data-opt-out',
            '/',
            '.mozilla.org',
            false,
            'lax'
        );
        expect(window.Mozilla.Cookies.removeItem).toHaveBeenCalledWith(
            'moz-1st-party-data-opt-out',
            '/',
            'www.mozilla.org',
            false,
            'lax'
        );
    });
});

describe('getCookieDomain', function () {
    it('should return null by default', function () {
        expect(DataPreferencesCookie.getCookieDomain()).toEqual(null);
    });

    it('should return ".mozilla.org" in production', function () {
        expect(
            DataPreferencesCookie.getCookieDomain(
                'https://www.mozilla.org/en-US/privacy/websites/data-preferences/'
            )
        ).toEqual('.mozilla.org');
    });

    it('should return ".allizom.org" in staging', function () {
        expect(
            DataPreferencesCookie.getCookieDomain(
                'https://www.allizom.org/en-US/privacy/websites/data-preferences/'
            )
        ).toEqual('.allizom.org');
    });

    it('should return null when any other domain is specified', function () {
        expect(
            DataPreferencesCookie.getCookieDomain('https://www.example.com')
        ).toEqual(null);
    });
});
