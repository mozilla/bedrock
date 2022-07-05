/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('core-datalayer.js', function () {
    describe('pageHasDownload', function () {
        it('will return "true" when download button is present on page.', function () {
            const downloadMarkup =
                '<a class="download" href="#" data-link-type="download" data-download-os="Desktop">';

            document.body.insertAdjacentHTML('beforeend', downloadMarkup);
            expect(Mozilla.Analytics.pageHasDownload()).toBe('true');

            var content = document.querySelector('.download');
            content.parentNode.removeChild(content);
        });

        it('will return "false" when download button is not present on page.', function () {
            expect(Mozilla.Analytics.pageHasDownload()).toBe('false');
        });
    });

    describe('pageHasVideo', function () {
        it('will return "true" when HTML5 video is present on page.', function () {
            const videoMarkup = '<video id="video-content"></video>';

            document.body.insertAdjacentHTML('beforeend', videoMarkup);
            expect(Mozilla.Analytics.pageHasVideo()).toBe('true');

            const content = document.getElementById('video-content');
            content.parentNode.removeChild(content);
        });

        it('will return "true" when YouTube iframe video is present on page.', function () {
            const videoMarkup =
                '<iframe id="video-content" src="https://www.youtube-nocookie.com/embed/NqxUdc0P6YE?rel=0"></iframe>';

            document.body.insertAdjacentHTML('beforeend', videoMarkup);
            expect(Mozilla.Analytics.pageHasVideo()).toBe('true');

            const content = document.getElementById('video-content');
            content.parentNode.removeChild(content);
        });

        it('will return "false" when download button is not present on page.', function () {
            expect(Mozilla.Analytics.pageHasVideo()).toBe('false');
        });
    });

    describe('getPageVersion', function () {
        it('will return the Firefox version number form the URL if present', function () {
            expect(
                Mozilla.Analytics.getPageVersion(
                    'https://www.mozilla.org/en-US/firefox/107.0.11/firstrun/'
                )
            ).toBe('107.0.11');
            expect(
                Mozilla.Analytics.getPageVersion(
                    'https://www.mozilla.org/en-US/firefox/46.0.1/firstrun/learnmore/'
                )
            ).toBe('46.0.1');
            expect(
                Mozilla.Analytics.getPageVersion(
                    'https://www.mozilla.org/en-US/firefox/11.0/whatsnew/'
                )
            ).toBe('11.0');
            expect(
                Mozilla.Analytics.getPageVersion(
                    'https://www.mozilla.org/en-US/firefox/46.0.1a2/firstrun/'
                )
            ).toBe('46.0.1a2');
            expect(
                Mozilla.Analytics.getPageVersion(
                    'https://www.mozilla.org/en-US/firefox/46.0a1/whatsnew/'
                )
            ).toBe('46.0a1');
        });

        it('will return null if no version number present in URL', function () {
            expect(
                Mozilla.Analytics.getPageVersion(
                    'https://www.mozilla.org/en-US/'
                )
            ).toBeNull();
            expect(
                Mozilla.Analytics.getPageVersion(
                    'https://www.mozilla.org/en-US/firefox/new'
                )
            ).toBeNull();
            expect(
                Mozilla.Analytics.getPageVersion(
                    'https://www.mozilla.org/en-US/firefox/whatsnew'
                )
            ).toBeNull();
        });
    });

    describe('getLatestFxVersion', function () {
        afterEach(function () {
            document
                .getElementsByTagName('html')[0]
                .removeAttribute('data-latest-firefox');
        });

        it('will return the Firefox version from the data-latest-firefox attribute from the html element if present', function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-latest-firefox', '48.0');
            expect(Mozilla.Analytics.getLatestFxVersion()).toBe('48.0');
        });

        it('will return null if no data-latest-firefox attribute is present on the html element', function () {
            expect(Mozilla.Analytics.getLatestFxVersion()).toBe(null);
        });
    });

    describe('getAMOExperiment', function () {
        it('should return true when experiment and variation params are well formatted', function () {
            const params = {
                experiment: '20210708_amo_experiment_name',
                variation: 'variation_1_name'
            };
            expect(Mozilla.Analytics.getAMOExperiment(params)).toEqual(params);
        });

        it('should return falsy when experiment and variation params are not specific to amo', function () {
            const params = {
                experiment: 'some_other_experiment',
                variation: 'variation_1_name'
            };
            expect(Mozilla.Analytics.getAMOExperiment(params)).toBeFalsy();
        });

        it('should return falsy when experiment and variation params contain dangerous characters', function () {
            const params = {
                experiment: '20210708_amo_"><h1>hello</h1>',
                variation: '<script>alert("test");</script>'
            };
            expect(Mozilla.Analytics.getAMOExperiment(params)).toBeFalsy();

            const params2 = {
                experiment: '20210708_amo_%22%3E%3Ch1%3Ehello%3C%2Fh1%3E',
                variation: '%3Cscript%3Ealert%28%22test%22%29%3B%3C%2Fscript%3E'
            };
            expect(Mozilla.Analytics.getAMOExperiment(params2)).toBeFalsy();
        });

        it('should return falsy if parameters values are more than 50 chars', function () {
            const params = {
                experiment: '20210708_amo_experiment_name',
                variation:
                    'a_very_very_very_very_very_long_experiment_variation_name_much_much_much_more_than_50_chars'
            };
            expect(Mozilla.Analytics.getAMOExperiment(params)).toBeFalsy();

            const params2 = {
                experiment:
                    '20210708_amo_a_very_very_very_long_experiment_name_much_much_much_much_more_than_50_chars',
                variation: 'variation_1_name'
            };
            expect(Mozilla.Analytics.getAMOExperiment(params2)).toBeFalsy();
        });
    });

    describe('formatFxaDetails', function () {
        it('will correctly format FxA data returned from UITour', function () {
            // Current Firefox Desktop, not logged in
            const input1 = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: false,
                browserServices: {
                    sync: {
                        setup: false,
                        desktopDevices: 'unknown',
                        mobileDevices: 'unknown',
                        totalDevices: 'unknown'
                    }
                }
            };

            const output1 = {
                FxALogin: false,
                FxASegment: 'Not logged in'
            };

            // Current Firefox Desktop, logged in, 1 desktop configured
            const input2 = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: true,
                browserServices: {
                    sync: {
                        setup: true,
                        desktopDevices: 1,
                        mobileDevices: 0,
                        totalDevices: 1
                    }
                }
            };

            const output2 = {
                FxALogin: true,
                FxAMultiDesktopSync: false,
                FxAMobileSync: false,
                FxASegment: 'Logged in'
            };

            // Current Firefox Desktop, logged in, 2 desktops configured
            const input3 = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: true,
                browserServices: {
                    sync: {
                        setup: true,
                        desktopDevices: 2,
                        mobileDevices: 0,
                        totalDevices: 2
                    }
                }
            };

            const output3 = {
                FxALogin: true,
                FxAMultiDesktopSync: true,
                FxAMobileSync: false,
                FxASegment: 'Multi-Desktop Sync'
            };

            // Current Firefox Desktop, logged in, 1 desktops 1 mobile configured
            const input4 = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: true,
                browserServices: {
                    sync: {
                        setup: true,
                        desktopDevices: 1,
                        mobileDevices: 1,
                        totalDevices: 2
                    }
                }
            };

            const output4 = {
                FxALogin: true,
                FxAMultiDesktopSync: false,
                FxAMobileSync: true,
                FxASegment: 'Desktop and Mobile Sync'
            };

            // Current Firefox Desktop, logged in, 2 desktops 1 mobile configured
            const input5 = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: true,
                browserServices: {
                    sync: {
                        setup: true,
                        desktopDevices: 2,
                        mobileDevices: 1,
                        totalDevices: 3
                    }
                }
            };

            const output5 = {
                FxALogin: true,
                FxAMultiDesktopSync: true,
                FxAMobileSync: true,
                FxASegment: 'Multi-Desktop and Mobile Sync'
            };

            // Firefox Desktop < 50, logged in to FxA
            const input6 = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: true,
                browserServices: {
                    sync: {
                        setup: true,
                        desktopDevices: 'unknown',
                        mobileDevices: 'unknown',
                        totalDevices: 'unknown'
                    }
                }
            };

            const output6 = {
                FxALogin: true,
                FxAMobileSync: 'unknown',
                FxAMultiDesktopSync: 'unknown',
                FxASegment: 'Logged in'
            };

            // Firefox Desktop < 50, logged out
            const input7 = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: false,
                browserServices: {
                    sync: {
                        setup: false,
                        desktopDevices: 'unknown',
                        mobileDevices: 'unknown',
                        totalDevices: 'unknown'
                    }
                }
            };

            const output7 = {
                FxALogin: false,
                FxASegment: 'Not logged in'
            };

            // Firefox Desktop < FxALastSupported, logged in
            const input8 = {
                firefox: true,
                legacy: true,
                mobile: false,
                setup: true,
                browserServices: {
                    sync: {
                        setup: true,
                        desktopDevices: 'unknown',
                        mobileDevices: 'unknown',
                        totalDevices: 'unknown'
                    }
                }
            };

            const output8 = {
                FxALogin: true,
                FxAMobileSync: 'unknown',
                FxAMultiDesktopSync: 'unknown',
                FxASegment: 'Legacy Firefox'
            };

            // Firefox Desktop < FxALastSupported, logged out
            const input9 = {
                firefox: true,
                legacy: true,
                mobile: false,
                setup: false,
                browserServices: {
                    sync: {
                        setup: false,
                        desktopDevices: 'unknown',
                        mobileDevices: 'unknown',
                        totalDevices: 'unknown'
                    }
                }
            };

            const output9 = {
                FxALogin: 'unknown',
                FxASegment: 'Legacy Firefox'
            };

            // Firefox Desktop < 29
            const input10 = {
                firefox: true,
                legacy: true,
                mobile: false,
                setup: false,
                browserServices: {
                    sync: {
                        setup: false,
                        desktopDevices: 'unknown',
                        mobileDevices: 'unknown',
                        totalDevices: 'unknown'
                    }
                }
            };

            const output10 = {
                FxALogin: 'unknown',
                FxASegment: 'Legacy Firefox'
            };

            // Firefox Android
            const input11 = {
                firefox: true,
                legacy: false,
                mobile: 'android',
                setup: false,
                browserServices: {
                    sync: {
                        setup: false,
                        desktopDevices: 'unknown',
                        mobileDevices: 'unknown',
                        totalDevices: 'unknown'
                    }
                }
            };

            const output11 = {
                FxASegment: 'Firefox Mobile'
            };

            // Firefox iOS
            const input12 = {
                firefox: true,
                legacy: false,
                mobile: 'ios',
                setup: false,
                browserServices: {
                    sync: {
                        setup: false,
                        desktopDevices: 'unknown',
                        mobileDevices: 'unknown',
                        totalDevices: 'unknown'
                    }
                }
            };

            const output12 = {
                FxASegment: 'Firefox Mobile'
            };

            // Not Firefox
            const input13 = {
                firefox: false,
                legacy: false,
                mobile: false,
                setup: false,
                browserServices: {
                    sync: {
                        setup: false,
                        desktopDevices: 'unknown',
                        mobileDevices: 'unknown',
                        totalDevices: 'unknown'
                    }
                }
            };

            const output13 = {
                FxASegment: 'Not Firefox'
            };

            // browserServices.sync is unexpectedly undefined (issue 10118).
            const input14 = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: true,
                browserServices: {
                    sync: undefined
                }
            };

            const output14 = {
                FxALogin: true,
                FxAMultiDesktopSync: 'unknown',
                FxAMobileSync: 'unknown',
                FxASegment: 'Logged in'
            };

            // we could do a loop for this but then we loose line specific error reporting
            expect(Mozilla.Analytics.formatFxaDetails(input1)).toEqual(output1);
            expect(Mozilla.Analytics.formatFxaDetails(input2)).toEqual(output2);
            expect(Mozilla.Analytics.formatFxaDetails(input3)).toEqual(output3);
            expect(Mozilla.Analytics.formatFxaDetails(input4)).toEqual(output4);
            expect(Mozilla.Analytics.formatFxaDetails(input5)).toEqual(output5);
            expect(Mozilla.Analytics.formatFxaDetails(input6)).toEqual(output6);
            expect(Mozilla.Analytics.formatFxaDetails(input7)).toEqual(output7);
            expect(Mozilla.Analytics.formatFxaDetails(input8)).toEqual(output8);
            expect(Mozilla.Analytics.formatFxaDetails(input9)).toEqual(output9);
            expect(Mozilla.Analytics.formatFxaDetails(input10)).toEqual(
                output10
            );
            expect(Mozilla.Analytics.formatFxaDetails(input11)).toEqual(
                output11
            );
            expect(Mozilla.Analytics.formatFxaDetails(input12)).toEqual(
                output12
            );
            expect(Mozilla.Analytics.formatFxaDetails(input13)).toEqual(
                output13
            );
            expect(Mozilla.Analytics.formatFxaDetails(input14)).toEqual(
                output14
            );
        });
    });

    describe('updateDataLayerPush', function () {
        beforeEach(function () {
            const link =
                '<a id="link" href="https://www.mozilla.org/en-US/firefox/new/">';
            document.body.insertAdjacentHTML('beforeend', link);

            window.dataLayer = [];
        });

        afterEach(function () {
            const content = document.getElementById('link');
            content.parentNode.removeChild(content);
            delete window.dataLayer;
        });

        it('will add newClickHref property to link click object when pushed to the dataLayer', function () {
            Mozilla.Analytics.updateDataLayerPush('www.allizom.org');

            window.dataLayer.push({
                event: 'gtm.linkClick',
                'gtm.element': document.getElementById('link')
            });

            expect(window.dataLayer[0].newClickHref).toBeDefined();
        });

        it('will not add newClickHref property to object pushed to dataLayer if not a link click object', function () {
            Mozilla.Analytics.updateDataLayerPush('www.allizom.org');

            window.dataLayer.push({
                event: 'gtm.click',
                'gtm.element': document.getElementById('link')
            });

            expect(window.dataLayer[0].newClickHref).toBeUndefined();
        });

        it("will keep host in newClickHref when clicked link's href host value is different thatn the page's", function () {
            Mozilla.Analytics.updateDataLayerPush('www.allizom.org');

            window.dataLayer.push({
                event: 'gtm.linkClick',
                'gtm.element': document.getElementById('link')
            });

            expect(window.dataLayer[0].newClickHref).toEqual(
                'https://www.mozilla.org/en-US/firefox/new/'
            );
        });

        it("will remove host and locale in newClickHref when clicked link's href value matches the page's", function () {
            const link = document.getElementById('link');
            Mozilla.Analytics.updateDataLayerPush('www.mozilla.org');

            // Bug 1278426
            link.href = 'https://www.mozilla.org:443/en-US/firefox/new/';

            window.dataLayer.push({
                event: 'gtm.linkClick',
                'gtm.element': link
            });

            expect(window.dataLayer[0].newClickHref).toEqual('/firefox/new/');
        });

        it('will remove host and non-en-US locale', function () {
            const link = document.getElementById('link');
            Mozilla.Analytics.updateDataLayerPush('www.mozilla.org');

            link.href = 'https://www.mozilla.org:443/de/firefox/new/';

            window.dataLayer.push({
                event: 'gtm.linkClick',
                'gtm.element': link
            });

            expect(window.dataLayer[0].newClickHref).toEqual('/firefox/new/');
        });

        it('will not remove locale if absent from the URL', function () {
            const link = document.getElementById('link');
            Mozilla.Analytics.updateDataLayerPush('www.mozilla.org');

            link.href = 'https://www.mozilla.org/firefox/new/';

            window.dataLayer.push({
                event: 'gtm.linkClick',
                'gtm.element': link
            });

            expect(window.dataLayer[0].newClickHref).toEqual('/firefox/new/');
        });
    });
});
