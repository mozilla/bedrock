/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import Spinner from '../libs/spin.min';

import FormUtils from './form-utils.es6';

const FXA_NEWSLETTERS = [
    'firefox-accounts-journey',
    'test-pilot',
    'take-action-for-the-internet',
    'knowledge-is-power'
];

const FXA_NEWSLETTERS_LOCALES = ['en', 'de', 'fr'];

const UNSUB_UNSUBSCRIBED_ALL = 1;

let _form;
let _userData;
let _newsletterData;
let _stringData;

/**
 * Returns true if a given value is found in a given list of <select> options.
 * @param {Array} options
 * @param {String} value
 * @returns {Boolean}
 */
function _hasOption(options, value) {
    const index = options.findIndex((option) => option.value === value);

    if (index !== -1) {
        return true;
    }

    return false;
}

/**
 * Sets the value of a <select> input to the given value if found.
 * @param {Array} options
 * @param {String} value
 */
function _setOption(options, value) {
    const index = options.findIndex((option) => option.value === value);

    if (index !== -1) {
        options[index].selected = 'selected';
    }
}

/**
 * Convenience helper for window.fetch() that returns a Promise.
 * @param {String} url
 * @param {String} method
 * @returns {Promise}
 */
function _fetch(url, method) {
    return new window.Promise((resolve, reject) => {
        window
            .fetch(url, {
                method: method,
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json'
                }
            })
            .then((resp) => {
                if (resp.status >= 200 && resp.status < 300) {
                    resolve(resp.json());
                } else {
                    reject(resp);
                }
            })
            .catch((e) => {
                reject(e);
            });
    });
}

/**
 * Main newsletter management form object.
 */
const NewsletterManagementForm = {
    meetsRequirements: () => {
        return (
            'Promise' in window &&
            'fetch' in window &&
            typeof Array.prototype.includes === 'function'
        );
    },

    getPageLocale: (locale) => {
        return typeof locale !== 'undefined'
            ? locale
            : document.getElementsByTagName('html')[0].getAttribute('lang');
    },

    getPageURL: () => {
        return window.location.href;
    },

    getFormCountry: () => {
        return _form.querySelector('select[name="country"]').value;
    },

    getFormLang: () => {
        return _form.querySelector('#id_lang').value;
    },

    /**
     * Get an array of checked newsletter IDs from the management form.
     * @returns {Array}
     */
    getCheckedNewsletters: () => {
        return Array.from(
            document.querySelectorAll(
                '.newsletter-table .newsletter-checkbox:checked'
            )
        ).map((newsletter) => newsletter.value);
    },

    /**
     * Get Basket URL for querying user data.
     * @returns {String}
     */
    getUserDataURL: () => {
        const token = FormUtils.getUserToken();
        return `${_form.getAttribute('action')}${token}/`;
    },

    /**
     * Get Basket URL for unsubscribing to all newsletters.
     * @returns {String}
     */
    getUnsubscribeURL: () => {
        const token = FormUtils.getUserToken();
        return `${_form.getAttribute('data-unsubscribe-url')}${token}/`;
    },

    /**
     * Get Basket URL for updating user preferences.
     * @returns {String}
     */
    getFormActionURL: () => {
        const token = FormUtils.getUserToken();
        return `${_form.getAttribute('action')}${token}/`;
    },

    /**
     * Get Basket URL for querying newsletter data.
     * @returns {String}
     */
    getNewsletterDataURL: () => {
        return _form.getAttribute('data-newsletters-url');
    },

    /**
     * Get Bedrock URL for querying localized newsletter strings.
     * @returns {String}
     */
    getNewsletterStringsURL: () => {
        return _form.getAttribute('data-strings-url');
    },

    /**
     * Is the given locale in the list of supported locales for Firefox Account newsletters?
     * @param {String} locale
     * @returns  {Boolean}
     */
    isFxALocale: (locale) => {
        const loc = locale.includes('-') ? locale.split('-')[0] : locale;
        return FXA_NEWSLETTERS_LOCALES.includes(loc);
    },

    /**
     * Is the given newsletter ID in the list of Firefox Account newsletters?
     * @param {String} newsletter
     * @returns
     */
    isFxANewsletter: (newsletter) => {
        return FXA_NEWSLETTERS.includes(newsletter);
    },

    /**
     * Has the "Remove me from all subscriptions" form input been checked?
     * @returns {Boolean}
     */
    shouldUnsubscribeAll: () => {
        return document.getElementById('id_remove_all').checked;
    },

    /**
     * Figure out which newsletters to display.
     * @param {Object} user - user data including array of subscribed newsletters.
     * @param {Object} newsletters - all available newsletters.
     * @param {Object} strings - translated newsletter strings.
     * @returns {Object} newsletters to display.
     */
    filterNewsletterData: (user, newsletters, strings) => {
        const finalNewsletters = [];
        const locale = NewsletterManagementForm.getPageLocale();
        const isFxALocale = NewsletterManagementForm.isFxALocale(locale);

        for (const newsletter in newsletters) {
            if (
                !Object.prototype.hasOwnProperty.call(newsletters, newsletter)
            ) {
                continue;
            }

            /**
             * Only include a newsletter if 'active' === true AND 'show' === true
             * OR if user is already subscribed, OR if they have a Firefox Account
             * and it's an FxA related newsletter.
             */
            const obj = newsletters[newsletter];

            const shouldDisplayNewsletter =
                (obj.active && obj.show) ||
                user.newsletters.includes(newsletter) ||
                (user.has_fxa &&
                    NewsletterManagementForm.isFxANewsletter(newsletter) &&
                    isFxALocale);

            if (!shouldDisplayNewsletter) {
                continue;
            }

            // Replace default newsletter copy with localized translations.
            if (Object.prototype.hasOwnProperty.call(strings, newsletter)) {
                obj.title = strings[newsletter].title;

                // Localized descriptions are optional.
                if (strings[newsletter].description) {
                    obj.description = strings[newsletter].description;
                }
            }

            // Is user subscribed to newsletter
            obj.subscribed = user.newsletters.includes(newsletter);

            // Store reference to newsletter ID
            obj.newsletter = newsletter;

            // Ensure there's always an `indented` property for rendering.
            if (!obj.indent) {
                obj.indent = false;
            }

            // Localized "Subscribe" label copy
            obj.subscribeCopy = strings['subscribe-copy'].title;

            finalNewsletters.push(obj);
        }

        return NewsletterManagementForm.sortNewsletterData(finalNewsletters);
    },

    /**
     * Sort newsletter array either by order field (primary) or title (secondary).
     * @param {Array} newsletters
     * @returns {Array}
     */
    sortNewsletterData: (newsletters) => {
        const keyField = newsletters[0].order ? 'order' : 'title';

        return newsletters.sort((a, b) => {
            if (keyField === 'order') {
                return a.order - b.order;
            } else {
                const titleA = a.title.toLowerCase();
                const titleB = b.title.toLowerCase();

                if (titleA < titleB) {
                    return -1;
                }
                if (titleA > titleB) {
                    return 1;
                }
                return 0;
            }
        });
    },

    /**
     * Fetch JSON object of translated newsletter strings from Bedrock.
     * @returns {Promise}
     */
    getNewsletterStrings: () => {
        return new window.Promise((resolve, reject) => {
            const url = NewsletterManagementForm.getNewsletterStringsURL();

            _fetch(url, 'GET')
                .then((resp) => {
                    resolve(resp);
                })
                .catch((e) => {
                    reject(e);
                });
        });
    },

    /**
     * Fetch JSON object of all available newsletters from Basket.
     * @returns {Promise}
     */
    getNewsletterData: () => {
        return new window.Promise((resolve, reject) => {
            const url = NewsletterManagementForm.getNewsletterDataURL();

            _fetch(url, 'GET')
                .then((resp) => {
                    resolve(resp.newsletters);
                })
                .catch((e) => {
                    reject(e);
                });
        });
    },

    /**
     * Fetch JSON object of user data from Basket
     * @returns {Promise}
     */
    getUserData: () => {
        return new window.Promise((resolve, reject) => {
            const hasFxA =
                NewsletterManagementForm.getPageURL().indexOf('fxa') !== -1;
            const action = NewsletterManagementForm.getUserDataURL();
            const url = hasFxA ? action : action + '?fxa=1';

            _fetch(url, 'GET')
                .then((resp) => {
                    // if `has_fxa` not returned from basket, set it from the URL
                    if (!resp.has_fxa) {
                        resp.has_fxa = hasFxA;
                    }
                    resolve(resp);
                })
                .catch((e) => {
                    reject(e);
                });
        });
    },

    /**
     * Generate HTML markup for newsletter table row.
     * @param {Object} newsletter
     * @param {Number} index
     * @returns {String}
     */
    renderTableRow: (newsletter, index) => {
        const checked = newsletter.subscribed ? ' checked=""' : '';
        const indent = newsletter.indent ? ' class="indented"' : '';
        return `<tr${indent}>
            <th>
                <h4>${newsletter.title}</h4>
                <p>${newsletter.description}</p>
            </th>
            <td>
                <label for="id_form-${index}-subscribed_check">${newsletter.subscribeCopy}</label>
                <input type="checkbox" class="newsletter-checkbox" name="form-${index}-subscribed_check" id="id_form-${index}-subscribed_check" value="${newsletter.newsletter}"${checked}>
            </td>
        </tr>`;
    },

    /**
     * Render an HTML table column of newsletters.
     * @param {Array} newsletters
     */
    renderNewsletters: (newsletters) => {
        const rows = newsletters.map(NewsletterManagementForm.renderTableRow);
        const table = document.querySelector('.newsletter-table tbody');

        rows.reverse().forEach((row) => {
            table.insertAdjacentHTML('afterbegin', row);
        });
    },

    /**
     * Set initial HTML form values based on user data returned from Basket.
     * @param {Object} userData
     */
    setFormDefaults: (userData) => {
        const countryOptions = Array.from(
            document.getElementById('id_country').options
        );
        const langOptions = Array.from(
            document.getElementById('id_lang').options
        );
        const pageLocale = NewsletterManagementForm.getPageLocale();
        let finalCountry;
        let finalLang;
        let pageCountry;
        let pageLang;
        let userCountry = userData.country;
        let userLang = userData.lang;

        // Try to derive lang and country from page locale to use as fallbacks.
        if (pageLocale.includes('-')) {
            const codes = pageLocale.toLowerCase().split('-');
            pageLang = codes[0];
            pageCountry = codes[1];
        } else {
            pageLang = pageCountry = pageLocale.toLowerCase();
        }

        // Default to English / US if matches are not found in the options lists.
        pageLang = _hasOption(langOptions, pageLang) ? pageLang : 'en';
        pageCountry = _hasOption(countryOptions, pageCountry)
            ? pageCountry
            : 'us';

        // Use basket supplied lang first, falling back to locale.
        if (userLang) {
            userLang = userLang.toLowerCase();

            /**
             * Check if basket supplied lang might be in a different format
             * to our form options. E.g. we have 'es' on our list, but their
             * language might be 'es-ES'. Try to find a match for their
             * current lang in our list and use that.
             */
            if (userLang.includes('-')) {
                userLang = userLang.split('-')[0];
            }

            finalLang = _hasOption(langOptions, userLang) ? userLang : pageLang;
        } else {
            finalLang = pageLang;
        }

        // Use basket supplied country first, falling back to locale.
        if (userCountry) {
            userCountry = userCountry.toLowerCase();
            finalCountry = _hasOption(countryOptions, userCountry)
                ? userCountry
                : pageCountry;
        } else {
            finalCountry = pageCountry;
        }

        // Set user email for display
        document.getElementById('id_email').innerText = userData.email;

        // Set language and country selection
        _setOption(langOptions, finalLang);
        _setOption(countryOptions, finalCountry);

        // Finally, set the preferred email format
        if (userData.format) {
            const text = document.querySelector('input[value="T"]');
            const html = document.querySelector('input[value="H"]');

            if (userData.format === 'H') {
                html.checked = true;
                text.checked = false;
            } else {
                text.checked = true;
                html.checked = false;
            }
        }
    },

    /**
     * Renders a list of form error messages.
     * @param {Array} errors
     */
    renderErrorMessages: (errors) => {
        const errorContainer = document.querySelector('.mzp-c-form-errors');
        const list = errorContainer.querySelector('.mzp-c-form-errors ul');

        // clear any previously displayed errors.
        FormUtils.clearFormErrors(_form);

        errors.forEach((error) => {
            list.insertAdjacentElement('afterbegin', error);
        });

        errorContainer.classList.remove('hidden');
        window.scrollTo(0, 0); // Scroll to top of page for error visibility.

        FormUtils.enableFormFields(_form);
    },

    /**
     * Redirects for `/newsletter/updated/` page on successful POST.
     */
    onFormSuccess: () => {
        const url = _form.getAttribute('data-updated-url');

        if (FormUtils.isWellFormedURL(url)) {
            window.location.href = url;
        } else {
            NewsletterManagementForm.onDataError();
        }
    },

    /**
     * Redirects for `/newsletter/updated/` page on successful unsubscribe
     * from all newsletters. The `?unsub` param is required to display the
     * unsubscription survey form.
     */
    onUnsubscribeAll: () => {
        const updated = _form.getAttribute('data-updated-url');
        const url = `${updated}?unsub=${UNSUB_UNSUBSCRIBED_ALL}`;

        if (FormUtils.isWellFormedURL(url)) {
            window.location.href = url;
        } else {
            NewsletterManagementForm.onDataError();
        }
    },

    /**
     * Event handler for GET/POST error message processing.
     * @param {Object} e
     */
    onDataError: (e) => {
        const msg = e ? e.statusText : null;
        const errors = [];
        errors.push(NewsletterManagementForm.handleFormError(msg));
        NewsletterManagementForm.renderErrorMessages(errors);
    },

    /**
     * Returns a localized error string based on given error message ID.
     * We use server rendered error strings since we need them even when
     * fetching string JSON might fail.
     * @param {String} msg
     * @param {String} newsletterId (optional)
     * @returns {String}
     */
    handleFormError: (msg, newsletterId) => {
        const strings = document.querySelector('.template-error-strings');
        let error;

        switch (msg) {
            case FormUtils.errorList.NOT_FOUND:
                error = strings.querySelector('.error-token-not-found');
                break;
            case FormUtils.errorList.EMAIL_INVALID_ERROR:
                error = strings.querySelector('.error-invalid-email');
                break;
            case FormUtils.errorList.NEWSLETTER_ERROR:
                error = strings.querySelector('.error-invalid-newsletter');

                // replace '%newsletter%' placeholder with actual newsletter ID.
                if (typeof newsletterId === 'string') {
                    const temp = error.textContent.replace(
                        '%newsletter%',
                        newsletterId
                    );
                    error.textContent = temp;
                }
                break;
            case FormUtils.errorList.COUNTRY_ERROR:
                error = strings.querySelector('.error-select-country');
                break;
            case FormUtils.errorList.LANGUAGE_ERROR:
                error = strings.querySelector('.error-select-lang');
                break;
            default:
                error = strings.querySelector('.error-try-again-later');
        }

        if (error) {
            return error.cloneNode(true);
        }

        return error;
    },

    /**
     * Gets all checked newsletters from the form and validates those based on the
     * given list of all valid newsletters.
     * @param {Array} newsletterData
     * @returns {Array} of unexpected newsletter IDs (or an empty array if valid)
     */
    validateNewsletters: (newsletterData) => {
        const newsletters = NewsletterManagementForm.getCheckedNewsletters();
        const data =
            typeof newsletterData === 'object'
                ? newsletterData
                : _newsletterData;
        return newsletters.filter(
            (newsletter) =>
                !Object.prototype.hasOwnProperty.call(data, newsletter)
        );
    },

    /**
     * Validates all form fields
     * @returns {Array} of localized error messages (or an empty array if valid)
     */
    validateFields: () => {
        const errors = [];

        // Make sure all checked newsletters have valid IDs
        const unexpected = NewsletterManagementForm.validateNewsletters();
        if (unexpected.length > 0) {
            errors.push(
                NewsletterManagementForm.handleFormError(
                    FormUtils.errorList.NEWSLETTER_ERROR,
                    unexpected[0]
                )
            );
        }

        // Check for country selection value.
        const country = NewsletterManagementForm.getFormCountry();
        if (!country) {
            errors.push(
                NewsletterManagementForm.handleFormError(
                    FormUtils.errorList.COUNTRY_ERROR
                )
            );
        }

        // Check for language selection value.
        const lang = NewsletterManagementForm.getFormLang();
        if (!lang) {
            errors.push(
                NewsletterManagementForm.handleFormError(
                    FormUtils.errorList.LANGUAGE_ERROR
                )
            );
        }

        return errors;
    },

    /**
     * Builds a query parameter string based on form field inputs.
     * @returns {String}
     */
    serialize: () => {
        const country = _form.querySelector('select[name="country"]').value;
        const lang = _form.querySelector('#id_lang').value;
        const format = document.querySelector(
            'input[name="format"]:checked'
        ).value;
        const newsletters = encodeURIComponent(
            NewsletterManagementForm.getCheckedNewsletters().join(',')
        );
        // Source URL (hidden field)
        const sourceUrl = encodeURIComponent(
            _form.querySelector('input[name="source_url"]').value
        );

        return `format=${format}&country=${country}&lang=${lang}&newsletters=${newsletters}&optin=Y&source_url=${sourceUrl}`;
    },

    /**
     * Handles management form submission.
     * @param {Object} event
     */
    onSubmit: (e) => {
        e.preventDefault();

        FormUtils.disableFormFields(_form);

        // Perform client side form field validation.
        const errors = NewsletterManagementForm.validateFields();
        if (errors.length > 0) {
            NewsletterManagementForm.renderErrorMessages(errors);
            return;
        }

        // Has the user checked "Remove me from all the subscriptions"?
        const unsubscribeAll = NewsletterManagementForm.shouldUnsubscribeAll();

        if (unsubscribeAll) {
            FormUtils.postToBasket(
                null,
                `optout=Y`,
                NewsletterManagementForm.getUnsubscribeURL(),
                NewsletterManagementForm.onUnsubscribeAll,
                NewsletterManagementForm.onDataError
            );
        } else {
            // Update user data to reflect form changes.
            FormUtils.postToBasket(
                null,
                NewsletterManagementForm.serialize(),
                NewsletterManagementForm.getFormActionURL(),
                NewsletterManagementForm.onFormSuccess,
                NewsletterManagementForm.onDataError
            );
        }
    },

    bindEvents: () => {
        _form.addEventListener(
            'submit',
            NewsletterManagementForm.onSubmit,
            false
        );
    },

    showUpdateBrowserCopy: () => {
        document
            .querySelector('.js-outdated-browser-msg')
            .classList.add('show');
    },

    showIntroCopy: () => {
        const intro = document.querySelector('.js-intro-msg');

        // Intro copy is conditional on ?confirm=1, so
        // check that it exists in the DOM before trying
        // to display it.
        if (intro) {
            intro.classList.add('show');
        }
    },

    /**
     * Perform a client side redirect to the /newsletter/recovery/ page.
     */
    redirectToRecoveryPage: () => {
        const recoveryUrl = _form.getAttribute('data-recovery-url');

        if (FormUtils.isWellFormedURL(recoveryUrl)) {
            window.location.href = recoveryUrl;
        } else {
            NewsletterManagementForm.onDataError();
        }
    },

    init: () => {
        if (!NewsletterManagementForm.meetsRequirements()) {
            NewsletterManagementForm.showUpdateBrowserCopy();
            return window.Promise.reject();
        } else {
            NewsletterManagementForm.showIntroCopy();
        }

        _form = document.querySelector('.newsletter-management-form');

        // Look for a valid user token before rendering the page.
        // If not found, redirect to /newsletter/recovery/.
        return FormUtils.checkForUserToken()
            .then(() => {
                const userData = NewsletterManagementForm.getUserData();
                const newsletterData =
                    NewsletterManagementForm.getNewsletterData();
                const newsletterStrings =
                    NewsletterManagementForm.getNewsletterStrings();

                // Display a loading spinner whilst form data is being fetched.
                const spinnerTarget = _form.querySelector('.loading-spinner');
                const spinner = new Spinner({
                    lines: 12, // The number of lines to draw
                    length: 4, // The length of each line
                    width: 2, // The line thickness
                    radius: 4, // The radius of the inner circle
                    corners: 0, // Corner roundness (0..1)
                    rotate: 0, // The rotation offset
                    direction: 1, // 1: clockwise, -1: counterclockwise
                    color: '#000', // #rgb or #rrggbb or array of colors
                    speed: 1, // Rounds per second
                    trail: 60, // Afterglow percentage
                    shadow: false, // Whether to render a shadow
                    hwaccel: true // Whether to use hardware acceleration
                });

                spinnerTarget.classList.remove('hidden');
                spinner.spin(spinnerTarget);

                // Fetch all the required data needed to render the form.
                return window.Promise.all([
                    userData,
                    newsletterData,
                    newsletterStrings
                ])
                    .then((data) => {
                        _userData = data[0];
                        _newsletterData = data[1];
                        _stringData = data[2];

                        const newsletters =
                            NewsletterManagementForm.filterNewsletterData(
                                _userData,
                                _newsletterData,
                                _stringData
                            );

                        NewsletterManagementForm.setFormDefaults(_userData);
                        NewsletterManagementForm.renderNewsletters(newsletters);
                        NewsletterManagementForm.bindEvents();

                        // Hide loading spinner
                        spinnerTarget.classList.add('hidden');

                        // display form fields once we've processed the basket data.
                        document
                            .querySelector('.newsletter-management-form-fields')
                            .classList.add('show');
                    })
                    .catch((e) => {
                        spinnerTarget.classList.add('hidden');
                        NewsletterManagementForm.onDataError(e);
                    });
            })
            .catch(() => {
                if (!FormUtils.getUserToken()) {
                    NewsletterManagementForm.redirectToRecoveryPage();
                }
            });
    }
};

export default NewsletterManagementForm;
