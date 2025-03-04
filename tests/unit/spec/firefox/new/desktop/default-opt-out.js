/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import DefaultOptOut from '../../../../../../media/js/firefox/new/desktop/default-opt-out.es6';

describe('default-opt-out.es6.js', function () {
    beforeEach(function () {
        const optOut = `<div id="opt-out">
            <label for="default-opt-out-primary" class="default-browser-checkbox-label hidden">
                <input type="checkbox" id="default-opt-out-primary"" class="default-browser-checkbox-input">
                Set Firefox as your default browser.
            </label>
            <label for="default-opt-out-secondary" class="default-browser-checkbox-label hidden">
                <input type="checkbox" id="default-opt-out-secondary" class="default-browser-checkbox-input">
                Set Firefox as your default browser.
            </label>
        </div>`;

        document.body.insertAdjacentHTML('beforeend', optOut);
    });

    beforeEach(function () {
        window.site.platform = 'windows';
    });

    afterEach(function () {
        const optOut = document.getElementById('opt-out');
        optOut.parentNode.removeChild(optOut);

        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');

        window.site.platform = 'other';
    });

    describe('init()', function () {
        it('should return false if OS is not Windows', function () {
            window.site.platform = 'osx';

            const result = DefaultOptOut.init();
            expect(result).toBeFalse();

            const checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(0);
        });

        it('should return false if GPC is enabled', function () {
            window.Mozilla.gpcEnabled = sinon.stub().returns(true);

            const result = DefaultOptOut.init();
            expect(result).toBeFalse();
            delete window.Mozilla.gpcEnabled;

            const checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(0);
        });

        it('should return false if DNT is enabled', function () {
            window.Mozilla.dntEnabled = sinon.stub().returns(true);

            const result = DefaultOptOut.init();
            expect(result).toBeFalse();
            delete window.Mozilla.dntEnabled;

            const checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(0);
        });

        it('should return true if consent cookie accepts analytics', function () {
            spyOn(window.Mozilla.Cookies, 'hasItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'getItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(
                    JSON.stringify({
                        analytics: true,
                        preference: true
                    })
                );

            const result = DefaultOptOut.init();
            expect(result).toBeTrue();

            const checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(2);
        });

        it('should return false if consent cookie rejects analytics', function () {
            spyOn(window.Mozilla.Cookies, 'hasItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'getItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(
                    JSON.stringify({
                        analytics: false,
                        preference: true
                    })
                );

            const result = DefaultOptOut.init();
            expect(result).toBeFalse();

            const checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(0);
        });

        it('should return false if visitor is in EU/EAA country', function () {
            spyOn(window.Mozilla.Cookies, 'hasItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(false);

            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');

            const result = DefaultOptOut.init();
            expect(result).toBeFalse();

            const checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(0);
        });

        it('should return true if visitor is outside EU/EAA', function () {
            window.Mozilla.gpcEnabled = sinon.stub().returns(false);
            window.Mozilla.gpcEnabled = sinon.stub().returns(false);
            spyOn(window.Mozilla.Cookies, 'hasItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(false);
            spyOn(window.Mozilla.Cookies, 'getItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(false);
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(true);

            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');

            const result = DefaultOptOut.init();
            expect(result).toBeTrue();

            const checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(2);

            document
                .getElementsByTagName('html')[0]
                .removeAttribute('data-needs-consent');
        });

        it('should return false if attribution requirements are not satisfied', function () {
            spyOn(window.Mozilla.Cookies, 'hasItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(false);
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(false);

            const result = DefaultOptOut.init();
            expect(result).toBeFalse();

            const checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(0);
        });

        it('should refresh attribution data and and update URL when visitor unchecks input', function () {
            spyOn(DefaultOptOut, 'meetsRequirements').and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'removeAttributionData');
            spyOn(window.Mozilla.StubAttribution, 'init');
            spyOn(DefaultOptOut, 'removeUTMParams');
            spyOn(window.history, 'replaceState');

            const result = DefaultOptOut.init();
            expect(result).toBeTrue();

            let checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(2);

            document.getElementById('default-opt-out-primary').click();
            expect(
                window.Mozilla.StubAttribution.removeAttributionData
            ).toHaveBeenCalled();
            expect(DefaultOptOut.removeUTMParams).toHaveBeenCalled();
            expect(window.history.replaceState).toHaveBeenCalled();
            expect(window.Mozilla.StubAttribution.init).toHaveBeenCalled();

            checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(0);
        });

        it('should opt back into analytics and init attribution if visitor re-checks input', function () {
            spyOn(DefaultOptOut, 'meetsRequirements').and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'removeAttributionData');
            spyOn(window.Mozilla.StubAttribution, 'init').and.callFake(
                (callback) => {
                    callback();
                }
            );
            spyOn(DefaultOptOut, 'addUTMParams');
            spyOn(DefaultOptOut, 'removeUTMParams');
            spyOn(window.history, 'replaceState');

            const result = DefaultOptOut.init();
            expect(result).toBeTrue();

            let checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(2);

            // Opt out
            document.getElementById('default-opt-out-primary').click();

            checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(0);

            // Opt in
            document.getElementById('default-opt-out-secondary').click();

            expect(
                window.Mozilla.StubAttribution.removeAttributionData
            ).toHaveBeenCalledTimes(2);
            expect(DefaultOptOut.removeUTMParams).toHaveBeenCalledTimes(1);
            expect(DefaultOptOut.addUTMParams).toHaveBeenCalledTimes(1);
            expect(window.history.replaceState).toHaveBeenCalledTimes(2);
            expect(window.Mozilla.StubAttribution.init).toHaveBeenCalledTimes(
                2
            );

            checkboxes = document.querySelectorAll(
                '.default-browser-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(2);
        });
    });

    describe('removeUTMParams', function () {
        it('should remove UTM parameters from a URL as expected', function () {
            const href =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment&utm_source=www.mozilla.org&utm_campaign=SET_DEFAULT_BROWSER';
            const expected =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment';
            const result = DefaultOptOut.removeUTMParams(href);
            expect(result).toEqual(expected);

            const href2 =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment';
            const result2 = DefaultOptOut.removeUTMParams(href2);
            expect(result2).toEqual(href2);

            const href3 = 'https://www.mozilla.org/en-US/firefox/new/';
            const result3 = DefaultOptOut.removeUTMParams(href3);
            expect(result3).toEqual(href3);

            const href4 =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment&utm_source=www.mozilla.org&utm_campaign=SET_DEFAULT_BROWSER#download';
            const expected4 =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment#download';
            const result4 = DefaultOptOut.removeUTMParams(href4);
            expect(result4).toEqual(expected4);
        });
    });

    describe('addUTMParams', function () {
        it('should add UTM parameters to a URL as expected', function () {
            const href =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment';
            const expected =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment&utm_source=www.mozilla.org&utm_campaign=SET_DEFAULT_BROWSER';
            const result = DefaultOptOut.addUTMParams(href);
            expect(result).toEqual(expected);

            const href2 = 'https://www.mozilla.org/en-US/firefox/new/';
            const expected2 =
                'https://www.mozilla.org/en-US/firefox/new/?utm_source=www.mozilla.org&utm_campaign=SET_DEFAULT_BROWSER';
            const result2 = DefaultOptOut.addUTMParams(href2);
            expect(result2).toEqual(expected2);

            const href3 =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment#download';
            const expected3 =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment&utm_source=www.mozilla.org&utm_campaign=SET_DEFAULT_BROWSER#download';
            const result3 = DefaultOptOut.addUTMParams(href3);
            expect(result3).toEqual(expected3);
        });
    });
});
