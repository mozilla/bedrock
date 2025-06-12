/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import DownloadAsDefault from '../../../../../../media/js/firefox/new/desktop/download-as-default.es6';

describe('download-as-default.es6.js', function () {
    beforeEach(function () {
        const optOut = `<div id="opt-out">
            <label for="default-opt-out-primary" class="default-browser-label hidden">
                <input type="checkbox" id="default-opt-out-primary"" class="default-browser-checkbox">
                Set Firefox as your default browser.
            </label>
            <label for="default-opt-out-secondary" class="default-browser-label hidden">
                <input type="checkbox" id="default-opt-out-secondary" class="default-browser-checkbox">
                Set Firefox as your default browser.
            </label>
        </div>`;

        document.body.insertAdjacentHTML('beforeend', optOut);
    });

    beforeEach(function () {
        window.site.platform = 'windows';
        window.site.fxSupported = 'true';
    });

    afterEach(function () {
        const optOut = document.getElementById('opt-out');
        optOut.parentNode.removeChild(optOut);

        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');

        window.site.platform = 'other';
    });

    describe('meetsRequirements', function () {
        it('should return false if OS is not Windows', function () {
            window.site.platform = 'osx';

            const result = DownloadAsDefault.meetsRequirements();
            expect(result).toBeFalse();
        });

        it('should return false if OS is too old', function () {
            window.site.fxSupported = false;

            const result = DownloadAsDefault.meetsRequirements();
            expect(result).toBeFalse();
        });

        it('should return false if GPC is enabled', function () {
            window.Mozilla.gpcEnabled = sinon.stub().returns(true);

            const result = DownloadAsDefault.meetsRequirements();
            expect(result).toBeFalse();
            delete window.Mozilla.gpcEnabled;
        });

        it('should return false if DNT is enabled', function () {
            window.Mozilla.dntEnabled = sinon.stub().returns(true);

            const result = DownloadAsDefault.meetsRequirements();
            expect(result).toBeFalse();
            delete window.Mozilla.dntEnabled;
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

            const result = DownloadAsDefault.meetsRequirements();
            expect(result).toBeFalse();
        });

        it('should return false if visitor is in EU/EAA country', function () {
            spyOn(window.Mozilla.Cookies, 'hasItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(false);

            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');

            const result = DownloadAsDefault.meetsRequirements();
            expect(result).toBeFalse();
        });

        it('should return false if attribution requirements are not satisfied', function () {
            spyOn(window.Mozilla.Cookies, 'hasItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(false);
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(false);

            const result = DownloadAsDefault.meetsRequirements();
            expect(result).toBeFalse();
        });

        it('should return true if attribution requirements are satisfied', function () {
            const result = DownloadAsDefault.meetsRequirements();
            expect(result).toBeTrue();
        });
    });
    describe('init()', function () {
        it('should refresh attribution data and and update URL when visitor unchecks input', function () {
            spyOn(DownloadAsDefault, 'meetsRequirements').and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'removeAttributionData');
            spyOn(window.Mozilla.StubAttribution, 'init').and.callFake(
                (callback) => {
                    callback();
                }
            );
            spyOn(DownloadAsDefault, 'removeUTMParams').and.callThrough();
            spyOn(window.history, 'replaceState');

            const result = DownloadAsDefault.init();
            expect(result).toBeTrue();

            let checkboxes = document.querySelectorAll(
                '.default-browser-checkbox:checked'
            );
            expect(checkboxes.length).toEqual(2);

            document.getElementById('default-opt-out-primary').click();
            expect(
                window.Mozilla.StubAttribution.removeAttributionData
            ).toHaveBeenCalled();

            expect(DownloadAsDefault.removeUTMParams).toHaveBeenCalled();
            expect(window.history.replaceState).toHaveBeenCalled();
            expect(window.Mozilla.StubAttribution.init).toHaveBeenCalled();

            checkboxes = document.querySelectorAll(
                '.default-browser-checkbox:checked'
            );
            expect(checkboxes.length).toEqual(0);
        });

        it('should opt back into analytics and init attribution if visitor re-checks input', function () {
            spyOn(DownloadAsDefault, 'meetsRequirements').and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'removeAttributionData');
            spyOn(window.Mozilla.StubAttribution, 'init').and.callFake(
                (callback) => {
                    callback();
                }
            );
            spyOn(DownloadAsDefault, 'addUTMParams').and.callThrough();
            spyOn(DownloadAsDefault, 'removeUTMParams').and.callThrough();
            spyOn(window.history, 'replaceState');

            const result = DownloadAsDefault.init();
            expect(result).toBeTrue();

            let checkboxes = document.querySelectorAll(
                '.default-browser-checkbox:checked'
            );
            expect(checkboxes.length).toEqual(2);

            // Opt out
            document.getElementById('default-opt-out-primary').click();

            checkboxes = document.querySelectorAll(
                '.default-browser-checkbox:checked'
            );
            expect(checkboxes.length).toEqual(0);

            // Opt in
            document.getElementById('default-opt-out-secondary').click();

            expect(
                window.Mozilla.StubAttribution.removeAttributionData
            ).toHaveBeenCalledTimes(3);
            expect(DownloadAsDefault.removeUTMParams).toHaveBeenCalledTimes(3);
            expect(DownloadAsDefault.addUTMParams).toHaveBeenCalledTimes(2);
            expect(window.history.replaceState).toHaveBeenCalledTimes(3);
            expect(window.Mozilla.StubAttribution.init).toHaveBeenCalledTimes(
                3
            );

            checkboxes = document.querySelectorAll(
                '.default-browser-checkbox:checked'
            );
            expect(checkboxes.length).toEqual(2);
        });
    });

    describe('removeUTMParams', function () {
        it('should remove UTM parameters from a URL as expected', function () {
            const href =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment&utm_source=www.mozilla.org&utm_campaign=SET_DEFAULT_BROWSER';
            const expected = 'https://www.mozilla.org/en-US/firefox/new/';
            const result = DownloadAsDefault.removeUTMParams(href);
            expect(result).toEqual(expected);

            const href2 =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment';
            const expected2 = 'https://www.mozilla.org/en-US/firefox/new/';
            const result2 = DownloadAsDefault.removeUTMParams(href2);
            expect(result2).toEqual(expected2);

            const href3 = 'https://www.mozilla.org/en-US/firefox/new/';
            const result3 = DownloadAsDefault.removeUTMParams(href3);
            expect(result3).toEqual(href3);

            const href4 =
                'https://www.mozilla.org/en-US/firefox/new/?experiment=download-as-default&variation=treatment&utm_source=www.mozilla.org&utm_campaign=SET_DEFAULT_BROWSER#download';
            const expected4 =
                'https://www.mozilla.org/en-US/firefox/new/#download';
            const result4 = DownloadAsDefault.removeUTMParams(href4);
            expect(result4).toEqual(expected4);
        });
    });

    describe('addUTMParams', function () {
        it('should add UTM parameters to a URL as expected', function () {
            const href = 'https://www.mozilla.org/en-US/firefox/new/';
            const expected =
                'https://www.mozilla.org/en-US/firefox/new/?utm_campaign=SET_DEFAULT_BROWSER';
            const result = DownloadAsDefault.addUTMParams(href);
            expect(result).toEqual(expected);

            const href2 = 'https://www.mozilla.org/en-US/firefox/new/';
            const expected2 =
                'https://www.mozilla.org/en-US/firefox/new/?utm_campaign=SET_DEFAULT_BROWSER';
            const result2 = DownloadAsDefault.addUTMParams(href2);
            expect(result2).toEqual(expected2);

            const href3 = 'https://www.mozilla.org/en-US/firefox/new/#download';
            const expected3 =
                'https://www.mozilla.org/en-US/firefox/new/?utm_campaign=SET_DEFAULT_BROWSER#download';
            const result3 = DownloadAsDefault.addUTMParams(href3);
            expect(result3).toEqual(expected3);
        });
    });
});
