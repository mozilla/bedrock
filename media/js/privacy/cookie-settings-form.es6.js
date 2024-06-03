/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    consentRequired,
    getConsentCookie,
    setConsentCookie
} from '../base/consent/utils.es6';

const CookieSettingsForm = {};

/**
 * Get the consent status object from the form data.
 * @returns {Object} - Consent status for analytics and preference cookies.
 */
CookieSettingsForm.getFormData = () => {
    return {
        preference:
            document.querySelector(
                'input[name="cookie-radio-preference"]:checked'
            ).value === 'yes',
        analytics:
            document.querySelector(
                'input[name="cookie-radio-analytics"]:checked'
            ).value === 'yes'
    };
};

/**
 * Set the form data based on the consent status object.
 */
CookieSettingsForm.setFormData = (data) => {
    if (data.preference) {
        document
            .getElementById('cookie-radio-preference-yes')
            .setAttribute('checked', '');
        document
            .getElementById('cookie-radio-preference-no')
            .removeAttribute('checked');
    } else {
        document
            .getElementById('cookie-radio-preference-yes')
            .removeAttribute('checked');
        document
            .getElementById('cookie-radio-preference-no')
            .setAttribute('checked', '');
    }

    if (data.analytics) {
        document
            .getElementById('cookie-radio-analytics-yes')
            .setAttribute('checked', '');
        document
            .getElementById('cookie-radio-analytics-no')
            .removeAttribute('checked');
    } else {
        document
            .getElementById('cookie-radio-analytics-yes')
            .removeAttribute('checked');
        document
            .getElementById('cookie-radio-analytics-no')
            .setAttribute('checked', '');
    }
};

/**
 * Handle the form submission event.
 * Sets the consent cookie based on the form data.
 * Shows a success message.
 * @param {Object} e - Event object.
 */
CookieSettingsForm.onFormSubmit = (e) => {
    e.preventDefault();
    const config = CookieSettingsForm.getFormData();
    setConsentCookie(config);
    CookieSettingsForm.showSuccessMessage();
};

CookieSettingsForm.showSuccessMessage = () => {
    const msg = document.querySelector('.cookie-consent-form-submit-success');
    msg.classList.remove('hidden');
    msg.focus();
};

CookieSettingsForm.unbindEvents = () => {
    document
        .querySelector('.cookie-consent-form')
        .removeEventListener('submit', CookieSettingsForm.onFormSubmit, false);
};

CookieSettingsForm.bindEvents = () => {
    document
        .querySelector('.cookie-consent-form')
        .addEventListener('submit', CookieSettingsForm.onFormSubmit, false);
};

/**
 * Binds click event for previous page link to go back in history.
 */
CookieSettingsForm.initBreadCrumbLinks = () => {
    const breadCrumbLinks = document.querySelector('.mzp-c-breadcrumb');

    if (!breadCrumbLinks) {
        return;
    }

    // Only show previous page link if there's page history.
    if (window.history.length > 1) {
        breadCrumbLinks.classList.remove('is-hidden');

        breadCrumbLinks.addEventListener(
            'click',
            (e) => {
                e.preventDefault();
                window.history.back();
            },
            false
        );
    }
};

/**
 * Initialize the form.
 * Sets the form data based on the consent cookie.
 * Binds form submission event.
 */
CookieSettingsForm.init = () => {
    const defaultConfig = {
        analytics: consentRequired() ? false : true,
        preference: consentRequired() ? false : true
    };
    const config = getConsentCookie() || defaultConfig;

    CookieSettingsForm.setFormData(config);
    CookieSettingsForm.bindEvents();
    CookieSettingsForm.initBreadCrumbLinks();
};

export default CookieSettingsForm;
