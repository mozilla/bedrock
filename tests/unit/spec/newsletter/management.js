/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FormUtils from '../../../../media/js/newsletter/form-utils.es6';
import NewsletterManagementForm from '../../../../media/js/newsletter/management.es6';
import { userData, newsletterData, stringData } from './data.js';

const TOKEN_MOCK = 'a1a2a3a4-abc1-12ab-a123-12345a12345b';

describe('management.es6.js', function () {
    beforeEach(function () {
        const form = `<div id="newsletter-management-test-form">
            <header class="mzp-l-content mzp-t-content-lg">
                <h1>Manage your Email Preferences</h1>
                <div class="js-intro-msg">
                    <p>We love sharing updates about all the awesome things happening at Mozilla.</p>
                    <p>Set your preferences below to make sure you always receive the news you want.</p>
                </div>
                <div class="js-outdated-browser-msg mzp-c-emphasis-box">
                    <p>Your web browser needs to be updated in order to use this page.</p>
                    <div id="newsletter-management-outdated-browser" class="mzp-c-button-download-container c-button-download-thanks">
                        <a href="/firefox/download/thanks/" class="download-link mzp-c-button mzp-t-product mzp-t-xl">
                            Download Firefox
                        </a>
                        <small class="mzp-c-button-download-privacy-link">
                            <a href="/en-US/privacy/firefox/">Firefox Privacy Notice</a>
                        </small>
                    </div>
                </div>
            </header>
            <form method="post" action="https://basket.mozilla.org/news/user/" class="newsletter-management-form" data-newsletters-url="https://basket.mozilla.org/news/newsletters/" data-strings-url="/en-US/newsletter/newsletter-strings.json" data-updated-url="/en-US/newsletter/updated/" data-recovery-url="/en-US/newsletter/recovery/" data-unsubscribe-url="https://basket.mozilla.org/news/unsubscribe/">
                <input type="hidden" name="source_url" value="https://www.mozilla.org/en-US/newsletter/existing/">
                <div class="loading-spinner hidden"></div>
                <div class="mzp-c-form-errors hidden">
                    <ul class="mzp-u-list-styled"></ul>
                </div>
                <div class="newsletter-management-form-fields">
                    <div class="c-column">
                        <div class="c-column-content" id="basic-settings">
                        <p>
                            <label>Your email address:</label>
                            <span id="id_email"></span>
                        </p>
                        <div>
                            <label for="id_country">Country or region:</label>
                            <select name="country" id="id_country">
                                <option value="" selected="">Select a country or region</option>
                                <option value="es">Spain</option>
                                <option value="fr">France</option>
                                <option value="de">Germany</option>
                                <option value="gb">United Kingdom</option>
                                <option value="us">United States</option>
                            </select>
                        </div>
                        <div>
                            <label for="id_lang">Language:</label>
                            <select name="lang" id="id_lang">
                                <option value="" selected="">Select a language</option>
                                <option value="de">Deutsch</option>
                                <option value="en">English</option>
                                <option value="es">Español</option>
                                <option value="fr">Français</option>
                            </select>
                        </div>
                        <div>
                            <label for="id_format_0">Format:</label>
                            <label for="id_format_0"><input type="radio" name="format" value="H" required="" id="id_format_0" checked="">HTML</label>
                            <label for="id_format_1"><input type="radio" name="format" value="T" required="" id="id_format_1">Text</label>
                        </div>
                    </div>
                </div>
                <div class="c-column">
                    <div class="c-column-content">
                        <table class="newsletter-table">
                        <thead>
                            <tr>
                                <th></th>
                                <th colspan="2">Subscribe</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th>
                                    <label for="id_remove_all">Remove me from all the subscriptions on this page:</label>
                                </th>
                                <td>
                                    <input type="checkbox" name="remove_all" id="id_remove_all">
                                </td>
                            </tr>
                        </tbody>
                        </table>
                        <button type="submit" class="mzp-c-button">Save Preferences</button>
                    </div>
                </div>
            </form>
            <div class="template-error-strings" hidden="">
                <ul>
                    <li class="error-token-not-found">
                        The supplied link has expired. Please <a href="/en-US/newsletter/recovery/">request a new link here</a>.
                    </li>
                    <li class="error-invalid-email">
                        This is not a valid email address. Please check the spelling.
                    </li>
                    <li class="error-invalid-newsletter">
                        %newsletter% is not a valid newsletter
                    </li>
                    <li class="error-select-country">
                        Please select a country or region
                    </li>
                    <li class="error-select-lang">
                        Please select a language
                    </li>
                    <li class="error-try-again-later">
                        Something is amiss with our system, sorry! Please try again later.
                    </li>
                </ul>
            </div>
        </div>`;

        document.body.insertAdjacentHTML('beforeend', form);
    });

    afterEach(function () {
        const form = document.getElementById('newsletter-management-test-form');
        form.parentNode.removeChild(form);
        FormUtils.userToken = '';
    });

    describe('isFxALocale', function () {
        it('should return true for expected locales', function () {
            expect(NewsletterManagementForm.isFxALocale('en')).toBeTrue();
            expect(NewsletterManagementForm.isFxALocale('en-US')).toBeTrue();
            expect(NewsletterManagementForm.isFxALocale('en-GB')).toBeTrue();
            expect(NewsletterManagementForm.isFxALocale('en-CA')).toBeTrue();
            expect(NewsletterManagementForm.isFxALocale('de')).toBeTrue();
            expect(NewsletterManagementForm.isFxALocale('fr')).toBeTrue();
        });

        it('should return false for anything else', function () {
            expect(NewsletterManagementForm.isFxALocale('es')).toBeFalse();
            expect(NewsletterManagementForm.isFxALocale('es-ES')).toBeFalse();
            expect(NewsletterManagementForm.isFxALocale('it')).toBeFalse();
            expect(NewsletterManagementForm.isFxALocale('pt-BR')).toBeFalse();
        });
    });

    describe('sortNewsletterData', function () {
        it('should order data by order field when provided', function () {
            const unorderedData = [
                { title: 'Firefox News', order: 5 },
                { title: 'Firefox Accounts Tips', order: 1 },
                { title: 'New Product Testing', order: 3 },
                { title: 'Knowledge is Power', order: 2 },
                { title: 'Take Action for the Internet', order: 4 },
                { title: 'Mozilla VPN Waitlist', order: 49 }
            ];
            const orderedData = [
                { title: 'Firefox Accounts Tips', order: 1 },
                { title: 'Knowledge is Power', order: 2 },
                { title: 'New Product Testing', order: 3 },
                { title: 'Take Action for the Internet', order: 4 },
                { title: 'Firefox News', order: 5 },
                { title: 'Mozilla VPN Waitlist', order: 49 }
            ];

            expect(
                NewsletterManagementForm.sortNewsletterData(unorderedData)
            ).toEqual(orderedData);
        });

        it('should order data by title when order field is not provided', function () {
            const unorderedData = [
                { title: 'Firefox News' },
                { title: 'Firefox Accounts Tips' },
                { title: 'New Product Testing' },
                { title: 'Knowledge is Power' },
                { title: 'Take Action for the Internet' },
                { title: 'Mozilla VPN Waitlist' }
            ];
            const orderedData = [
                { title: 'Firefox Accounts Tips' },
                { title: 'Firefox News' },
                { title: 'Knowledge is Power' },
                { title: 'Mozilla VPN Waitlist' },
                { title: 'New Product Testing' },
                { title: 'Take Action for the Internet' }
            ];

            expect(
                NewsletterManagementForm.sortNewsletterData(unorderedData)
            ).toEqual(orderedData);
        });
    });

    describe('filterNewsletterData', function () {
        it('should return a filtered set of newsletters in the expected format', function () {
            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'en-US'
            );
            const newsletters = NewsletterManagementForm.filterNewsletterData(
                userData,
                newsletterData,
                stringData
            );
            const subscribed = newsletters.filter(
                (newsletter) => newsletter.subscribed === true
            );
            const active = newsletters.filter(
                (newsletter) => newsletter.active === true
            );
            const inactive = newsletters.filter(
                (newsletter) => newsletter.active === false
            );
            const show = newsletters.filter(
                (newsletter) => newsletter.show === true
            );
            const fxaNewsletters = newsletters.filter((newsletter) =>
                NewsletterManagementForm.isFxANewsletter(newsletter.newsletter)
            );

            // total number of active newsletters to display
            expect(newsletters.length).toEqual(10);
            expect(active.length).toEqual(10);

            // number of subscribed newsletters to display
            expect(subscribed.length).toEqual(3);

            // inactive newsletters should not be displaed
            expect(inactive.length).toEqual(0);

            // newsletters set to always show
            // ('mozilla-and-you', 'mozilla-foundation', 'mozilla-festival', 'internet-health-report', 'common-voice)
            expect(show.length).toEqual(5);

            // FxA newsletters to display
            expect(fxaNewsletters.length).toEqual(4);

            expect(newsletters[0].title).toEqual('Firefox Accounts Tips');
            expect(newsletters[0].newsletter).toEqual(
                'firefox-accounts-journey'
            );
            expect(newsletters[0].subscribed).toBeFalse();

            expect(newsletters[1].title).toEqual('Knowledge is Power');
            expect(newsletters[1].newsletter).toEqual('knowledge-is-power');
            expect(newsletters[1].subscribed).toBeFalse();

            expect(newsletters[2].title).toEqual('New Product Testing');
            expect(newsletters[2].newsletter).toEqual('test-pilot');
            expect(newsletters[2].subscribed).toBeFalse();

            expect(newsletters[3].title).toEqual(
                'Take Action for the Internet'
            );
            expect(newsletters[3].newsletter).toEqual(
                'take-action-for-the-internet'
            );
            expect(newsletters[3].subscribed).toBeFalse();

            expect(newsletters[4].title).toEqual('Firefox News');
            expect(newsletters[4].newsletter).toEqual('mozilla-and-you');
            expect(newsletters[4].subscribed).toBeTrue();

            expect(newsletters[5].title).toEqual('Mozilla News');
            expect(newsletters[5].newsletter).toEqual('mozilla-foundation');
            expect(newsletters[5].subscribed).toBeTrue();

            expect(newsletters[6].title).toEqual('Mozilla Festival');
            expect(newsletters[6].newsletter).toEqual('mozilla-festival');
            expect(newsletters[6].subscribed).toBeFalse();

            expect(newsletters[7].title).toEqual('Insights');
            expect(newsletters[7].newsletter).toEqual('internet-health-report');
            expect(newsletters[7].subscribed).toBeFalse();

            expect(newsletters[8].title).toEqual('Common Voice');
            expect(newsletters[8].newsletter).toEqual('common-voice');
            expect(newsletters[8].subscribed).toBeFalse();

            expect(newsletters[9].title).toEqual('Mozilla Community');
            expect(newsletters[9].newsletter).toEqual('about-mozilla');
            expect(newsletters[9].subscribed).toBeTrue();
        });

        it('should not include FxA newsletters if not an FxA user', function () {
            const nonFxaUser = {
                email: 'example@example.com',
                country: 'us',
                format: 'H',
                lang: 'en',
                newsletters: [
                    'about-mozilla',
                    'mozilla-and-you',
                    'mozilla-foundation'
                ],
                status: 'ok'
            };
            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'en-US'
            );
            const newsletters = NewsletterManagementForm.filterNewsletterData(
                nonFxaUser,
                newsletterData,
                stringData
            );
            const subscribed = newsletters.filter(
                (newsletter) => newsletter.subscribed === true
            );
            const active = newsletters.filter(
                (newsletter) => newsletter.active === true
            );
            const inactive = newsletters.filter(
                (newsletter) => newsletter.active === false
            );
            const show = newsletters.filter(
                (newsletter) => newsletter.show === true
            );
            const fxaNewsletters = newsletters.filter((newsletter) =>
                NewsletterManagementForm.isFxANewsletter(newsletter.newsletter)
            );

            // total number of active newsletters to display
            expect(newsletters.length).toEqual(6);
            expect(active.length).toEqual(6);

            // number of subscribed newsletters to display
            expect(subscribed.length).toEqual(3);

            // inactive newsletters should not be displaed
            expect(inactive.length).toEqual(0);

            // newsletters set to always show
            // ('mozilla-and-you', 'mozilla-foundation', 'mozilla-festival', 'internet-health-report', 'common-voice')
            expect(show.length).toEqual(5);

            // FxA newsletters to display
            expect(fxaNewsletters.length).toEqual(0);
        });
    });

    describe('setFormDefaults', function () {
        it('should update the form with basic settings', function () {
            const country = document.getElementById('id_country');
            const lang = document.getElementById('id_lang');

            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'en-US'
            );
            NewsletterManagementForm.setFormDefaults(userData);
            expect(document.getElementById('id_email').innerText).toEqual(
                userData.email
            );
            expect(country.options[country.selectedIndex].value).toEqual(
                userData.country
            );
            expect(lang.options[lang.selectedIndex].value).toEqual(
                userData.lang
            );
            expect(
                document.querySelector('input[name="format"]:checked').value
            ).toEqual(userData.format);
        });

        it('should derive country and lang from page locale when missing from user data', function () {
            const country = document.getElementById('id_country');
            const lang = document.getElementById('id_lang');
            const partialUserData = {
                email: 'example@example.com',
                format: 'H'
            };

            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'en-GB'
            );
            NewsletterManagementForm.setFormDefaults(partialUserData);
            expect(document.getElementById('id_email').innerText).toEqual(
                partialUserData.email
            );
            expect(country.options[country.selectedIndex].value).toEqual('gb');
            expect(lang.options[lang.selectedIndex].value).toEqual('en');
            expect(
                document.querySelector('input[name="format"]:checked').value
            ).toEqual(partialUserData.format);
        });

        it('should default to English / US when page locale info does not match available options', function () {
            const country = document.getElementById('id_country');
            const lang = document.getElementById('id_lang');
            const partialUserData = {
                email: 'example@example.com',
                format: 'T'
            };

            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'xx'
            );
            NewsletterManagementForm.setFormDefaults(partialUserData);
            expect(document.getElementById('id_email').innerText).toEqual(
                partialUserData.email
            );
            expect(country.options[country.selectedIndex].value).toEqual('us');
            expect(lang.options[lang.selectedIndex].value).toEqual('en');
            expect(
                document.querySelector('input[name="format"]:checked').value
            ).toEqual(partialUserData.format);
        });

        it('should default to English / US when user data does not match available options', function () {
            const country = document.getElementById('id_country');
            const lang = document.getElementById('id_lang');
            const partialUserData = {
                email: 'example@example.com',
                country: 'xx',
                format: 'T',
                lang: 'xx'
            };

            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'en-US'
            );
            NewsletterManagementForm.setFormDefaults(partialUserData);
            expect(document.getElementById('id_email').innerText).toEqual(
                partialUserData.email
            );
            expect(country.options[country.selectedIndex].value).toEqual('us');
            expect(lang.options[lang.selectedIndex].value).toEqual('en');
            expect(
                document.querySelector('input[name="format"]:checked').value
            ).toEqual(partialUserData.format);
        });

        it('should default to English / US when user data does not match available options', function () {
            const country = document.getElementById('id_country');
            const lang = document.getElementById('id_lang');
            const partialUserData = {
                email: 'example@example.com',
                country: 'xx',
                format: 'T',
                lang: 'xx'
            };

            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'en-US'
            );
            NewsletterManagementForm.setFormDefaults(partialUserData);
            expect(document.getElementById('id_email').innerText).toEqual(
                partialUserData.email
            );
            expect(country.options[country.selectedIndex].value).toEqual('us');
            expect(lang.options[lang.selectedIndex].value).toEqual('en');
            expect(
                document.querySelector('input[name="format"]:checked').value
            ).toEqual(partialUserData.format);
        });

        it('should fuzzy match language codes returned from basket', function () {
            const country = document.getElementById('id_country');
            const lang = document.getElementById('id_lang');
            const partialUserData = {
                email: 'example@example.com',
                country: 'es',
                format: 'H',
                lang: 'es-ES'
            };

            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'en-US'
            );
            NewsletterManagementForm.setFormDefaults(partialUserData);
            expect(document.getElementById('id_email').innerText).toEqual(
                partialUserData.email
            );
            expect(country.options[country.selectedIndex].value).toEqual('es');
            expect(lang.options[lang.selectedIndex].value).toEqual('es');
            expect(
                document.querySelector('input[name="format"]:checked').value
            ).toEqual(partialUserData.format);
        });
    });

    describe('renderNewsletters', function () {
        it('should render a list of newsletters as expected', function () {
            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'en-US'
            );
            const newsletters = NewsletterManagementForm.filterNewsletterData(
                userData,
                newsletterData,
                stringData
            );

            NewsletterManagementForm.renderNewsletters(newsletters);

            const rows = document.querySelectorAll(
                '.newsletter-table tbody > tr'
            );
            expect(rows.length).toEqual(11);

            expect(rows[0].querySelector('th > h4').innerText).toEqual(
                'Firefox Accounts Tips'
            );
            expect(
                rows[0].querySelector('td > input[type="checkbox"]').value
            ).toEqual('firefox-accounts-journey');
            expect(
                rows[0].querySelector('td > input[type="checkbox"]').checked
            ).toBeFalsy();

            expect(rows[4].querySelector('th > h4').innerText).toEqual(
                'Firefox News'
            );
            expect(
                rows[4].querySelector('td > input[type="checkbox"]').value
            ).toEqual('mozilla-and-you');
            expect(
                rows[4].querySelector('td > input[type="checkbox"]').checked
            ).toBeTruthy();
        });
    });

    describe('validateNewsletters', function () {
        it('should return true for valid newsletters', function () {
            spyOn(
                NewsletterManagementForm,
                'getCheckedNewsletters'
            ).and.returnValue(userData.newsletters);
            const result =
                NewsletterManagementForm.validateNewsletters(newsletterData);
            expect(result.length).toEqual(0);
        });

        it('should return false if an invalid newsletter is found', function () {
            const unexpected = [
                'about-mozilla',
                'mozilla-and-you',
                'bargain-hunters-weekly',
                'mozilla-foundation'
            ];
            spyOn(
                NewsletterManagementForm,
                'getCheckedNewsletters'
            ).and.returnValue(unexpected);
            const result =
                NewsletterManagementForm.validateNewsletters(newsletterData);
            expect(result.length).toEqual(1);
        });
    });

    describe('validateFields', function () {
        beforeEach(function () {
            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            spyOn(NewsletterManagementForm, 'setFormDefaults');
            spyOn(NewsletterManagementForm, 'renderNewsletters');

            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'en-US'
            );
            spyOn(NewsletterManagementForm, 'getUserData').and.returnValue(
                window.Promise.resolve(userData)
            );

            spyOn(
                NewsletterManagementForm,
                'getNewsletterData'
            ).and.returnValue(window.Promise.resolve(newsletterData));
            spyOn(
                NewsletterManagementForm,
                'getNewsletterStrings'
            ).and.returnValue(window.Promise.resolve(stringData));
        });

        it('should return return an empty array if form data is valid', function () {
            return NewsletterManagementForm.init().then(() => {
                spyOn(
                    NewsletterManagementForm,
                    'validateNewsletters'
                ).and.returnValue([]);
                spyOn(
                    NewsletterManagementForm,
                    'getFormCountry'
                ).and.returnValue('us');
                spyOn(NewsletterManagementForm, 'getFormLang').and.returnValue(
                    'en'
                );
                expect(NewsletterManagementForm.validateFields()).toEqual([]);
            });
        });

        it('should return return an array of errors if form data is invalid', function () {
            return NewsletterManagementForm.init().then(() => {
                spyOn(
                    NewsletterManagementForm,
                    'validateNewsletters'
                ).and.returnValue(['bargain-hunters-weekly']);
                spyOn(
                    NewsletterManagementForm,
                    'getFormCountry'
                ).and.returnValue(null);
                spyOn(NewsletterManagementForm, 'getFormLang').and.returnValue(
                    undefined
                );
                const errors = NewsletterManagementForm.validateFields();
                expect(errors[0].textContent.trim()).toEqual(
                    'bargain-hunters-weekly is not a valid newsletter'
                );
                expect(errors[1].textContent.trim()).toEqual(
                    'Please select a country or region'
                );
                expect(errors[2].textContent.trim()).toEqual(
                    'Please select a language'
                );
            });
        });
    });

    describe('getNewsletterStrings', function () {
        const url =
            'https://www.mozilla.org/en-US/newsletter/newsletter-strings.json';

        beforeEach(function () {
            const mockResponse = new window.Response(
                JSON.stringify(stringData),
                {
                    status: 200,
                    statusText: 'OK',
                    headers: {
                        Accept: 'application/json',
                        'Content-type': 'application/json'
                    }
                }
            );

            spyOn(window, 'fetch').and.returnValue(
                window.Promise.resolve(mockResponse)
            );

            spyOn(
                NewsletterManagementForm,
                'getNewsletterStringsURL'
            ).and.returnValue(url);
        });

        it('should query url and return object of newsletter strings', function () {
            return NewsletterManagementForm.getNewsletterStrings().then(
                (resp) => {
                    expect(window.fetch).toHaveBeenCalledWith(url, {
                        method: 'GET',
                        headers: {
                            Accept: 'application/json',
                            'Content-Type': 'application/json'
                        }
                    });

                    expect(resp).toEqual(stringData);
                }
            );
        });
    });

    describe('getNewsletterData', function () {
        const url = 'https://basket.mozilla.org/news/newsletters/';

        beforeEach(function () {
            const mockResponse = new window.Response(
                JSON.stringify({
                    newsletters: newsletterData
                }),
                {
                    status: 200,
                    statusText: 'OK',
                    headers: {
                        Accept: 'application/json',
                        'Content-type': 'application/json'
                    }
                }
            );

            spyOn(window, 'fetch').and.returnValue(
                window.Promise.resolve(mockResponse)
            );

            spyOn(
                NewsletterManagementForm,
                'getNewsletterDataURL'
            ).and.returnValue(url);
        });

        it('should query url and return object of all known newsletters', function () {
            return NewsletterManagementForm.getNewsletterData().then((resp) => {
                expect(window.fetch).toHaveBeenCalledWith(url, {
                    method: 'GET',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json'
                    }
                });

                expect(resp).toEqual(newsletterData);
            });
        });
    });

    describe('getUserData', function () {
        const url = 'https://basket.mozilla.org/news/user/1234567890/';

        beforeEach(function () {
            spyOn(NewsletterManagementForm, 'getUserDataURL').and.returnValue(
                url
            );
        });

        it('should query user data and ask for FxA status from Basket if not passed in the URL', function () {
            const mockResponse = new window.Response(JSON.stringify(userData), {
                status: 200,
                statusText: 'OK',
                headers: {
                    Accept: 'application/json',
                    'Content-type': 'application/json'
                }
            });

            spyOn(window, 'fetch').and.returnValue(
                window.Promise.resolve(mockResponse)
            );

            spyOn(NewsletterManagementForm, 'getPageURL').and.returnValue(
                'https://www.mozilla.org/en-US/newsletter/existing/1234567890/'
            );

            return NewsletterManagementForm.getUserData().then((resp) => {
                expect(window.fetch).toHaveBeenCalledWith(url + '?fxa=1', {
                    method: 'GET',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json'
                    }
                });

                expect(resp).toEqual(userData);
                expect(resp.has_fxa).toBeTrue();
            });
        });

        it('should query user data and set has_fxa if param is passed in the page URL', function () {
            const nonFxAUser = {
                email: 'example@example.com',
                country: 'us',
                format: 'H',
                lang: 'en',
                newsletters: [
                    'about-mozilla',
                    'mozilla-and-you',
                    'mozilla-foundation'
                ],
                status: 'ok'
            };

            const mockResponse = new window.Response(
                JSON.stringify(nonFxAUser),
                {
                    status: 200,
                    statusText: 'OK',
                    headers: {
                        Accept: 'application/json',
                        'Content-type': 'application/json'
                    }
                }
            );

            spyOn(window, 'fetch').and.returnValue(
                window.Promise.resolve(mockResponse)
            );

            spyOn(NewsletterManagementForm, 'getPageURL').and.returnValue(
                'https://www.mozilla.org/en-US/newsletter/existing/1234567890/?fxa=1'
            );

            return NewsletterManagementForm.getUserData().then((resp) => {
                expect(window.fetch).toHaveBeenCalledWith(url, {
                    method: 'GET',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json'
                    }
                });

                expect(resp.email).toEqual(nonFxAUser.email);
                expect(resp.has_fxa).toBeTrue();
            });
        });

        it('should query user data and set has_fxa to false when expected', function () {
            const nonFxAUser = {
                email: 'example@example.com',
                country: 'us',
                format: 'H',
                lang: 'en',
                newsletters: [
                    'about-mozilla',
                    'mozilla-and-you',
                    'mozilla-foundation'
                ],
                status: 'ok'
            };

            const mockResponse = new window.Response(
                JSON.stringify(nonFxAUser),
                {
                    status: 200,
                    statusText: 'OK',
                    headers: {
                        Accept: 'application/json',
                        'Content-type': 'application/json'
                    }
                }
            );

            spyOn(window, 'fetch').and.returnValue(
                window.Promise.resolve(mockResponse)
            );

            spyOn(NewsletterManagementForm, 'getPageURL').and.returnValue(
                'https://www.mozilla.org/en-US/newsletter/existing/1234567890/'
            );

            return NewsletterManagementForm.getUserData().then((resp) => {
                expect(window.fetch).toHaveBeenCalledWith(url + '?fxa=1', {
                    method: 'GET',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json'
                    }
                });

                expect(resp.email).toEqual(nonFxAUser.email);
                expect(resp.has_fxa).toBeDefined();
                expect(resp.has_fxa).toBeFalse();
            });
        });
    });

    describe('init', function () {
        beforeEach(function () {
            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'en-US'
            );
        });

        it('should should fetch data and initialise the form as expected', function () {
            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            spyOn(NewsletterManagementForm, 'getUserData').and.returnValue(
                window.Promise.resolve(userData)
            );
            spyOn(
                NewsletterManagementForm,
                'getNewsletterData'
            ).and.returnValue(window.Promise.resolve(newsletterData));
            spyOn(
                NewsletterManagementForm,
                'getNewsletterStrings'
            ).and.returnValue(window.Promise.resolve(stringData));
            spyOn(
                NewsletterManagementForm,
                'filterNewsletterData'
            ).and.callThrough();
            spyOn(NewsletterManagementForm, 'setFormDefaults');
            spyOn(NewsletterManagementForm, 'renderNewsletters');
            spyOn(NewsletterManagementForm, 'bindEvents');

            return NewsletterManagementForm.init().then(() => {
                expect(
                    NewsletterManagementForm.filterNewsletterData
                ).toHaveBeenCalledWith(userData, newsletterData, stringData);
                expect(
                    NewsletterManagementForm.setFormDefaults
                ).toHaveBeenCalledWith(userData);
                expect(
                    NewsletterManagementForm.renderNewsletters
                ).toHaveBeenCalled();
                expect(NewsletterManagementForm.bindEvents).toHaveBeenCalled();
            });
        });

        it('should render an error message for an invalid / expired token', function () {
            const error = { statusText: 'Not Found' };

            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            spyOn(NewsletterManagementForm, 'getUserData').and.returnValue(
                window.Promise.reject(error)
            );
            spyOn(
                NewsletterManagementForm,
                'getNewsletterData'
            ).and.returnValue(window.Promise.reject(newsletterData));
            spyOn(
                NewsletterManagementForm,
                'getNewsletterStrings'
            ).and.returnValue(window.Promise.resolve(stringData));

            return NewsletterManagementForm.init().then(() => {
                const error = document
                    .querySelector('.mzp-c-form-errors li:nth-child(1)')
                    .innerHTML.trim();
                expect(error).toEqual(
                    'The supplied link has expired. Please <a href="/en-US/newsletter/recovery/">request a new link here</a>.'
                );
            });
        });

        it('should render an error message if fetching from basket fails', function () {
            const error = { statusText: 'Unknown non-helpful error' };

            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            spyOn(NewsletterManagementForm, 'getUserData').and.returnValue(
                window.Promise.reject(error)
            );
            spyOn(
                NewsletterManagementForm,
                'getNewsletterData'
            ).and.returnValue(window.Promise.reject(error));
            spyOn(
                NewsletterManagementForm,
                'getNewsletterStrings'
            ).and.returnValue(window.Promise.resolve(stringData));

            return NewsletterManagementForm.init().then(() => {
                const error = document
                    .querySelector('.mzp-c-form-errors li:nth-child(1)')
                    .innerHTML.trim();
                expect(error).toEqual(
                    'Something is amiss with our system, sorry! Please try again later.'
                );
            });
        });

        it('should display download Firefox prompt to outdated browsers', function () {
            spyOn(
                NewsletterManagementForm,
                'meetsRequirements'
            ).and.returnValue(false);

            return NewsletterManagementForm.init().catch(() => {
                expect(
                    document
                        .querySelector('.js-outdated-browser-msg')
                        .classList.contains('show')
                ).toBeTrue();
            });
        });

        it('should redirect to the /recovery/ page is a valid token is not found', function () {
            spyOn(FormUtils, 'getUserToken').and.returnValue('');
            spyOn(NewsletterManagementForm, 'redirectToRecoveryPage');

            return NewsletterManagementForm.init().catch(() => {
                expect(
                    NewsletterManagementForm.redirectToRecoveryPage
                ).toHaveBeenCalled();
            });
        });
    });

    describe('onSubmit', function () {
        let xhr;
        let xhrRequests = [];

        beforeEach(function () {
            xhr = sinon.useFakeXMLHttpRequest();
            xhr.onCreate = (req) => {
                xhrRequests.push(req);
            };

            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            spyOn(NewsletterManagementForm, 'getUserData').and.returnValue(
                window.Promise.resolve(userData)
            );
            spyOn(
                NewsletterManagementForm,
                'getNewsletterData'
            ).and.returnValue(window.Promise.resolve(newsletterData));
            spyOn(
                NewsletterManagementForm,
                'getNewsletterStrings'
            ).and.returnValue(window.Promise.resolve(stringData));
            spyOn(NewsletterManagementForm, 'getPageLocale').and.returnValue(
                'en-US'
            );
        });

        afterEach(function () {
            xhr.restore();
            xhrRequests = [];
        });

        it('should successfully handle form submission of valid data', function () {
            spyOn(NewsletterManagementForm, 'onFormSuccess');

            return NewsletterManagementForm.init().then(() => {
                document.querySelector('button[type="submit"]').click();

                expect(xhrRequests[0].url).toEqual(
                    `https://basket.mozilla.org/news/user/${TOKEN_MOCK}/`
                );
                expect(xhrRequests[0].requestBody).toEqual(
                    'format=H&country=us&lang=en&newsletters=mozilla-and-you%2Cmozilla-foundation%2Cabout-mozilla&optin=Y&source_url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2Fnewsletter%2Fexisting%2F'
                );
                xhrRequests[0].respond(
                    200,
                    { 'Content-Type': 'application/json' },
                    '{"status": "ok"}'
                );
                expect(
                    NewsletterManagementForm.onFormSuccess
                ).toHaveBeenCalled();
            });
        });

        it('should successfully subscribe to an additional newsletter', function () {
            spyOn(NewsletterManagementForm, 'onFormSuccess');

            return NewsletterManagementForm.init().then(() => {
                document.querySelector('input[value="common-voice"]').click();
                document.querySelector('button[type="submit"]').click();

                expect(xhrRequests[0].requestBody).toEqual(
                    'format=H&country=us&lang=en&newsletters=mozilla-and-you%2Cmozilla-foundation%2Ccommon-voice%2Cabout-mozilla&optin=Y&source_url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2Fnewsletter%2Fexisting%2F'
                );
                xhrRequests[0].respond(
                    200,
                    { 'Content-Type': 'application/json' },
                    '{"status": "ok"}'
                );
                expect(
                    NewsletterManagementForm.onFormSuccess
                ).toHaveBeenCalled();
            });
        });

        it('should successfully unsubscribe from an existing newsletter', function () {
            spyOn(NewsletterManagementForm, 'onFormSuccess');

            return NewsletterManagementForm.init().then(() => {
                document
                    .querySelector('input[value="mozilla-and-you"]')
                    .click();
                document.querySelector('button[type="submit"]').click();

                expect(xhrRequests[0].requestBody).toEqual(
                    'format=H&country=us&lang=en&newsletters=mozilla-foundation%2Cabout-mozilla&optin=Y&source_url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2Fnewsletter%2Fexisting%2F'
                );
                xhrRequests[0].respond(
                    200,
                    { 'Content-Type': 'application/json' },
                    '{"status": "ok"}'
                );
                expect(
                    NewsletterManagementForm.onFormSuccess
                ).toHaveBeenCalled();
            });
        });

        it('should successfully unsubscribe from all newsletters', function () {
            spyOn(NewsletterManagementForm, 'onUnsubscribeAll');

            return NewsletterManagementForm.init().then(() => {
                document.getElementById('id_remove_all').click();
                document.querySelector('button[type="submit"]').click();

                expect(xhrRequests[0].url).toEqual(
                    `https://basket.mozilla.org/news/unsubscribe/${TOKEN_MOCK}/`
                );
                expect(xhrRequests[0].requestBody).toEqual('optout=Y');
                xhrRequests[0].respond(
                    200,
                    { 'Content-Type': 'application/json' },
                    '{"status": "ok"}'
                );
                expect(
                    NewsletterManagementForm.onUnsubscribeAll
                ).toHaveBeenCalled();
            });
        });

        it('should render error messages and not post to basket if local form data is invalid', function () {
            spyOn(NewsletterManagementForm, 'onFormSuccess');

            return NewsletterManagementForm.init().then(() => {
                document.getElementById('id_lang').selectedIndex = -1;
                document.getElementById('id_country').selectedIndex = -1;
                document.querySelector('button[type="submit"]').click();
                expect(
                    NewsletterManagementForm.onFormSuccess
                ).not.toHaveBeenCalled();
                expect(
                    document.querySelector('.mzp-c-form-errors li:nth-child(1)')
                        .innerText
                ).toEqual('Please select a language');
                expect(
                    document.querySelector('.mzp-c-form-errors li:nth-child(2)')
                        .innerText
                ).toEqual('Please select a country or region');
            });
        });

        it('should render an error message if basket encounters an error', function () {
            spyOn(NewsletterManagementForm, 'onFormSuccess');

            return NewsletterManagementForm.init().then(() => {
                document.querySelector('button[type="submit"]').click();
                xhrRequests[0].respond(
                    400,
                    { 'Content-Type': 'application/json' },
                    '{"status": "error", "desc": "Unknown non-helpful error"}'
                );
                expect(
                    NewsletterManagementForm.onFormSuccess
                ).not.toHaveBeenCalled();
                expect(
                    document.querySelector('.mzp-c-form-errors li:nth-child(1)')
                        .innerText
                ).toEqual(
                    'Something is amiss with our system, sorry! Please try again later.'
                );
            });
        });
    });
});
