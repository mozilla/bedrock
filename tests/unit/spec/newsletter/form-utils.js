/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FormUtils from '../../../../media/js/newsletter/form-utils.es6';

describe('checkEmailValidity', function () {
    it('should return true for primitive email format', function () {
        expect(FormUtils.checkEmailValidity('a@a')).toBeTruthy();
        expect(
            FormUtils.checkEmailValidity('example@example.com')
        ).toBeTruthy();
    });

    it('should return false for anything else', function () {
        expect(FormUtils.checkEmailValidity(1234567890)).toBeFalsy();
        expect(FormUtils.checkEmailValidity('aaa')).toBeFalsy();
        expect(FormUtils.checkEmailValidity(null)).toBeFalsy();
        expect(FormUtils.checkEmailValidity(undefined)).toBeFalsy();
        expect(FormUtils.checkEmailValidity(true)).toBeFalsy();
        expect(FormUtils.checkEmailValidity(false)).toBeFalsy();
    });
});

describe('getURLToken', function () {
    it('should return a UUID token from a URL', function () {
        const token = 'a1a2a3a4-abc1-12ab-a123-12345a12345b';
        const location = {
            pathname: `/en-US/newsletter/existing/${token}/`
        };
        expect(FormUtils.getURLToken(location)).toEqual(token);
    });

    it('should return an empty string if a valid token is not found', function () {
        const location = {
            pathname: `/en-US/newsletter/existing/`
        };
        expect(FormUtils.getURLToken(location)).toEqual('');
    });
});

describe('getUserToken', function () {
    it('should return a UUID token from cookie', function () {
        const token = 'a1a2a3a4-abc1-12ab-a123-12345a12345b';
        spyOn(Mozilla.Cookies, 'getItem').and.returnValue(token);
        expect(FormUtils.getUserToken()).toEqual(token);
    });

    it('should return an empty string if token is invalid', function () {
        const token = 'some invalid string';
        spyOn(Mozilla.Cookies, 'getItem').and.returnValue(token);
        expect(FormUtils.getUserToken()).toEqual('');
    });
});

describe('isValidToken', function () {
    it('should return true for a valid token', function () {
        const token = 'a1a2a3a4-abc1-12ab-a123-12345a12345b';
        expect(FormUtils.isValidToken(token)).toBeTrue();
    });

    it('should return false if a token is too long', function () {
        expect(
            FormUtils.isValidToken(
                'ffa1a2a3a4-abgc1-1g2ab-a12f3-12345a12345bgf'
            )
        ).toBeFalse();
    });

    it('should return false if a token is too short', function () {
        expect(FormUtils.isValidToken('a1-abc1-12ab-a123-12345a')).toBeFalse();
    });

    it('should return false for everything else', function () {
        expect(FormUtils.isValidToken('some-string')).toBeFalse();
        expect(FormUtils.isValidToken(true)).toBeFalse();
        expect(FormUtils.isValidToken(null)).toBeFalse();
        expect(FormUtils.isValidToken(undefined)).toBeFalse();
        expect(FormUtils.isValidToken()).toBeFalse();
        expect(FormUtils.isValidToken(123456789)).toBeFalse();
    });
});

describe('isWellFormedURL', function () {
    it('should return true for absolute URLs', function () {
        expect(
            FormUtils.isWellFormedURL(
                'http://localhost:8000/en-US/newsletter/updated/'
            )
        ).toBeTrue();
        expect(
            FormUtils.isWellFormedURL(
                'https://www.mozilla.org/en-US/newsletter/updated/'
            )
        ).toBeTrue();
    });

    it('should return true for relative URLs', function () {
        expect(
            FormUtils.isWellFormedURL('/en-US/newsletter/updated/')
        ).toBeTrue();
    });

    it('should return false for anything else', function () {
        expect(
            FormUtils.isWellFormedURL('undefined?unsub=1&token=null')
        ).toBeFalse();
        expect(FormUtils.isWellFormedURL(undefined)).toBeFalse();
        expect(FormUtils.isWellFormedURL(null)).toBeFalse();
    });
});

describe('removeTokenFromURL', function () {
    it('should remove token from URL path name', function () {
        spyOn(window.history, 'replaceState');
        const token = 'a1a2a3a4-abc1-12ab-a123-12345a12345b';
        const location = {
            pathname: `/en-US/newsletter/existing/${token}/`,
            search: ''
        };
        FormUtils.removeTokenFromURL(location, token);
        expect(window.history.replaceState).toHaveBeenCalledWith(
            null,
            null,
            '/en-US/newsletter/existing/'
        );
    });

    it('should maintain existing query parameters', function () {
        spyOn(window.history, 'replaceState');
        const token = 'a1a2a3a4-abc1-12ab-a123-12345a12345b';
        const location = {
            pathname: `/en-US/newsletter/existing/${token}/`,
            search: '?fxa=1'
        };
        FormUtils.removeTokenFromURL(location, token);
        expect(window.history.replaceState).toHaveBeenCalledWith(
            null,
            null,
            '/en-US/newsletter/existing/?fxa=1'
        );
    });

    it('should not update the URL is a token is not present', function () {
        spyOn(window.history, 'replaceState');
        const token = 'a1a2a3a4-abc1-12ab-a123-12345a12345b';
        const location = {
            pathname: '/en-US/newsletter/existing/'
        };
        FormUtils.removeTokenFromURL(location, token);
        expect(window.history.replaceState).not.toHaveBeenCalled();
    });
});

describe('setUserToken', function () {
    it('should set a cookie with a valid UUID token', function () {
        const token = 'a1a2a3a4-abc1-12ab-a123-12345a12345b';
        spyOn(Mozilla.Cookies, 'setItem');
        FormUtils.setUserToken(token);
        expect(Mozilla.Cookies.setItem).toHaveBeenCalledOnceWith(
            'nl-token',
            token,
            jasmine.any(String),
            '/',
            undefined,
            false,
            'lax'
        );
    });

    it('should not set a cookie if token is invalid', function () {
        const token = 'some invalid string';
        spyOn(Mozilla.Cookies, 'setItem');
        FormUtils.setUserToken(token);
        expect(Mozilla.Cookies.setItem).not.toHaveBeenCalled();
    });
});

describe('serialize', function () {
    afterEach(function () {
        const form = document.querySelector('.send-to-device-form');
        form.parentNode.removeChild(form);
    });

    it('should return a query string as expected', function () {
        const form = `<form class="send-to-device-form" action="https://basket.mozilla.org/news/subscribe/" method="post">
            <div class="send-to-device-form-fields">
                <div class="platform-container">
                    <input type="hidden" name="newsletters" value="download-firefox-mobile-reco">
                    <input type="hidden" name="source-url" value="https://www.mozilla.org/en-US/firefox/browsers/mobile/ios/">
                </div>
                <div class="mzp-c-field mzp-l-stretch">
                    <label class="mzp-c-field-label" for="s2d-hero-input">Enter your email</label>
                    <input id="s2d-hero-input" class="mzp-c-field-control send-to-device-input" name="email" type="text" required="" value="example@example.com">
                </div>
                <div class="mzp-c-button-container mzp-l-stretch">
                    <button type="submit" class="button mzp-c-button  mzp-t-product ">Send</button>
                </div>
            </div>
        </form>`;
        document.body.insertAdjacentHTML('beforeend', form);
        expect(
            FormUtils.serialize(document.querySelector('.send-to-device-form'))
        ).toEqual(
            'newsletters=download-firefox-mobile-reco&source-url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2Ffirefox%2Fbrowsers%2Fmobile%2Fios%2F&email=example%40example.com'
        );
    });

    it('should return an empty string if no form elements are found', function () {
        const form = `<form class="send-to-device-form" action="https://basket.mozilla.org/news/subscribe/" method="post"></form>`;
        document.body.insertAdjacentHTML('beforeend', form);
        expect(
            FormUtils.serialize(document.querySelector('.send-to-device-form'))
        ).toEqual('');
    });
});

describe('stripHTML', function () {
    it('should strip HTML tags from strings as expected', function () {
        expect(
            FormUtils.stripHTML('This string should not contain HTML.')
        ).toEqual('This string should not contain HTML.');
        expect(
            FormUtils.stripHTML(
                'This string<script></script> should <strong>not</strong> contain <br>HTML<img src="/img/placeholder.png" />.'
            )
        ).toEqual('This string should not contain HTML.');
        expect(
            FormUtils.stripHTML(
                'This%20string%3Cscript%3E%3C%2Fscript%3E%20should%20%3Cstrong%3Enot%3C%2Fstrong%3E%20contain%20%3Cbr%3EHTML%3Cimg%20src%3D%22%2Fimg%2Fplaceholder.png%22%20%2F%3E.'
            )
        ).toEqual('This string should not contain HTML.');
    });
});
