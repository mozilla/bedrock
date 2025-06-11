/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    hasConsentCookie,
    getConsentCookie,
    consentRequired,
    dntEnabled,
    gpcEnabled
} from '../../../base/consent/utils.es6';

const DownloadAsDefault = {};

window.Mozilla.DownloadAsDefault = DownloadAsDefault;

/**
 * Removes UTM parameters from a given URL, preserving
 * all other parameters and URL information.
 * @param {String} href
 * @returns {String} href
 */
DownloadAsDefault.removeUTMParams = (href) => {
    const url = new URL(href);
    const searchParams = new URLSearchParams(url.search);

    // List of UTM parameters to remove
    const utmParams = [
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'utm_term',
        'utm_content',
        'experiment',
        'variation'
    ];

    // Remove UTM parameters
    utmParams.forEach((param) => searchParams.delete(param));

    // Construct new URL without UTM parameters
    const newUrl =
        url.origin +
        url.pathname +
        (searchParams.toString() ? '?' + searchParams.toString() : '') +
        url.hash;

    return newUrl;
};

/**
 * Adds UTM parameters to a given URL that are needed to trigger
 * the set-as-default functionality when Firefox is installed.
 * @param {String} href
 * @returns {String} href
 */
DownloadAsDefault.addUTMParams = (href) => {
    // sanitize URL so we don't pile on UTMs
    const url = new URL(DownloadAsDefault.removeUTMParams(href));
    const searchParams = new URLSearchParams(url.search);

    searchParams.append('utm_campaign', 'SET_DEFAULT_BROWSER');

    // Construct new URL with UTM parameters
    const newUrl =
        url.origin +
        url.pathname +
        (searchParams.toString() ? '?' + searchParams.toString() : '') +
        url.hash;

    return newUrl;
};

/**
 * Processes attribution changes depending on checkbox state.
 * @param {Boolean} checked - checkbox target value.
 */
DownloadAsDefault.processAttributionRequest = (checked) => {
    let url = window.location.href;

    // First remove all existing attribution data.
    window.Mozilla.StubAttribution.removeAttributionData();

    /**
     * If the checkbox has been unchecked, remove UTM parameters
     * from the page URL (`utm_campaign=SET_DEFAULT_BROWSER` is
     * what triggers the browser default functionality).
     */
    if (!checked) {
        url = DownloadAsDefault.removeUTMParams(url);
    } else {
        url = DownloadAsDefault.addUTMParams(url);
    }

    // Update the browser's URL without reloading
    window.history.replaceState({}, document.title, url);

    /**
     * Finally, re-initiate attribution based on the new URL
     * parameters. Only rebind events after attribution
     * request has been successful.
     */
    window.Mozilla.StubAttribution.init(() => {
        DownloadAsDefault.bindEvents();
    });
};

/**
 * Handles checkbox change event. Because checkbox state must be
 * synced between all checkboxes on the page, we must temporarily
 * unbind event listeners to avoid triggering multiple change
 * events at once.
 * @param {Object} e - change event object.
 */
DownloadAsDefault.handleChangeEvent = (e) => {
    DownloadAsDefault.unbindEvents();
    DownloadAsDefault.setCheckboxState(e.target.checked);
    DownloadAsDefault.processAttributionRequest(e.target.checked);
};

/**
 * Unbinds checkbox change event listeners and disables
 * inputs when unbound.
 */
DownloadAsDefault.unbindEvents = () => {
    const checkboxes = document.querySelectorAll('.default-browser-checkbox');

    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].removeEventListener(
            'change',
            DownloadAsDefault.handleChangeEvent,
            false
        );
        checkboxes[i].disabled = true;
    }
};

/**
 * Binds checkbox change event listeners and removes
 * disabled states on inputs when bound.
 */
DownloadAsDefault.bindEvents = () => {
    const checkboxes = document.querySelectorAll('.default-browser-checkbox');

    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].addEventListener(
            'change',
            DownloadAsDefault.handleChangeEvent,
            false
        );
        checkboxes[i].disabled = false;
    }
};

/**
 * Sets the checked state of all checkbox inputs.
 * @param {Boolean} checked state
 */
DownloadAsDefault.setCheckboxState = (checked) => {
    const checkboxes = document.querySelectorAll('.default-browser-checkbox');

    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = checked;
    }
};

/**
 * Displays checkboxes via CSS by removing the `hidden`
 * class on their corresponding `<label>` parent elements.
 */
DownloadAsDefault.showCheckbox = () => {
    const labels = document.querySelectorAll('.default-browser-label');
    for (let i = 0; i < labels.length; i++) {
        labels[i].classList.remove('hidden');
        labels[i].querySelector('.default-browser-checkbox').checked = true;
    }
};

/**
 * Determines if set-as-default checkbox should display.
 * @returns {Boolean}
 */
DownloadAsDefault.meetsRequirements = () => {
    if (
        typeof window.URL !== 'function' ||
        typeof window.URLSearchParams !== 'function' ||
        !window.history.replaceState
    ) {
        return false;
    } else if (window.site.platform !== 'windows') {
        // Ensure the visitor is on Windows OS
        return false;
    } else if (!window.site.fxSupported) {
        // Ensure the visitor is on a supported version
        return false;
    } else if (dntEnabled() || gpcEnabled()) {
        // Has the visitor set a browser-level privacy flag?
        return false;
    } else if (hasConsentCookie()) {
        // Does the visitor have an existing analytics consent cookie?
        const cookie = getConsentCookie();
        if (cookie && !cookie.analytics) {
            return false;
        }
    } else if (consentRequired()) {
        // Is the visitor in EU/EAA?
        return false;
    } else if (
        // Are requirements for stub attribution met?
        typeof window.Mozilla.StubAttribution === 'undefined' ||
        !window.Mozilla.StubAttribution.meetsRequirements()
    ) {
        return false;
    }

    return true;
};

/**
 * Init Firefox set-as-default opt-out flow.
 * @returns {Boolean}.
 */
DownloadAsDefault.init = () => {
    if (!DownloadAsDefault.meetsRequirements()) {
        return false;
    }

    DownloadAsDefault.showCheckbox();
    DownloadAsDefault.processAttributionRequest(true);
    // processAttributionRequest will bind the events

    return true;
};

export default DownloadAsDefault;
