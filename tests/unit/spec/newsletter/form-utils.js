/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    checkEmailValidity,
    serialize,
    stripHTML
} from '../../../../media/js/newsletter/form-utils.es6';

describe('checkEmailValidity', function () {
    it('should return true for primitive email format', function () {
        expect(checkEmailValidity('a@a')).toBeTruthy();
        expect(checkEmailValidity('example@example.com')).toBeTruthy();
    });

    it('should return false for anything else', function () {
        expect(checkEmailValidity(1234567890)).toBeFalsy();
        expect(checkEmailValidity('aaa')).toBeFalsy();
        expect(checkEmailValidity(null)).toBeFalsy();
        expect(checkEmailValidity(undefined)).toBeFalsy();
        expect(checkEmailValidity(true)).toBeFalsy();
        expect(checkEmailValidity(false)).toBeFalsy();
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
            serialize(document.querySelector('.send-to-device-form'))
        ).toEqual(
            'newsletters=download-firefox-mobile-reco&source-url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2Ffirefox%2Fbrowsers%2Fmobile%2Fios%2F&email=example%40example.com'
        );
    });

    it('should return an empty string if no form elements are found', function () {
        const form = `<form class="send-to-device-form" action="https://basket.mozilla.org/news/subscribe/" method="post"></form>`;
        document.body.insertAdjacentHTML('beforeend', form);
        expect(
            serialize(document.querySelector('.send-to-device-form'))
        ).toEqual('');
    });
});

describe('stripHTML', function () {
    it('should strip HTML tags from strings as expected', function () {
        expect(stripHTML('This string should not contain HTML.')).toEqual(
            'This string should not contain HTML.'
        );
        expect(
            stripHTML(
                'This string<script></script> should <strong>not</strong> contain <br>HTML<img src="/img/placeholder.png">.'
            )
        ).toEqual('This string should not contain HTML.');
        expect(
            stripHTML(
                'This%20string%3Cscript%3E%3C%2Fscript%3E%20should%20%3Cstrong%3Enot%3C%2Fstrong%3E%20contain%20%3Cbr%3EHTML%3Cimg%20src%3D%22%2Fimg%2Fplaceholder.png%22%20%2F%3E.'
            )
        ).toEqual('This string should not contain HTML.');
    });
});
