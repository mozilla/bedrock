/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const FxaLink = {};
const client = Mozilla.Client;
const allowedList = [
    'https://accounts.firefox.com/',
    'https://accounts.stage.mozaws.net/',
    'https://accounts.firefox.com.cn/'
];

/**
 * Configures Sync for Firefox browsers.
 * @param href {String}
 * @returns href {String}
 */
FxaLink.updateURL = function (href) {
    const contextParam = 'context=fx_desktop_v3';
    const separator = href.indexOf('?') > 0 ? '&' : '?';
    href += separator + contextParam;
    return href;
};

/**
 * Returns the hostname for a given URL.
 * @param {String} url.
 * @returns {String} hostname.
 */
FxaLink.getHostName = function (url) {
    const matches = url.match(/^https?:\/\/(?:[^/?#]+)(?:[/?#]|$)/i);
    return matches && matches[0];
};

/**
 * Intercept event handler for FxA links and forms, lets the browser drive the FxA Flow using
 * the `showFirefoxAccounts` UITour API. Attaches several UTM parameters from the current page
 * that will be forwarded to the browser and later on to FxA services.
 * @param event {Event}
 * @private
 */
FxaLink.interceptFxANavigation = function (event) {
    event.preventDefault();
    const search = new URL(event.target.href).search;
    const urlParams = new window._SearchParams(search).params;
    const extraURLParams = {};
    const allowedChars = /^[\w/.%-]+$/;
    const knownParams = [
        'flow_id',
        'flow_begin_time',
        'device_id',
        'entrypoint',
        'entrypoint_experiment',
        'entrypoint_variation',
        'utm_source',
        'utm_campaign',
        'utm_content',
        'utm_term',
        'utm_medium'
    ];

    for (let i = 0; i < knownParams.length; i++) {
        const known = knownParams[i];
        if (Object.prototype.hasOwnProperty.call(urlParams, known)) {
            const param = decodeURIComponent(urlParams[known]);
            if (allowedChars.test(param)) {
                extraURLParams[known] = param;
            }
        }
    }
    const entrypoint = extraURLParams.entrypoint;
    // 'entrypoint' is sent separately and should not be in the extras
    delete extraURLParams.entrypoint;
    return Mozilla.UITour.showFirefoxAccounts(extraURLParams, entrypoint);
};

/**
 * Updates FxA links with Sync params.
 * Only applicable for Firefox desktop user agents.
 */
FxaLink.init = function (callback) {
    callback =
        callback ||
        function noop() {
            // do nothing
        };
    if (!client._isFirefoxDesktop()) {
        return;
    }

    const userVer = parseFloat(client._getFirefoxVersion());
    const useUITourForFxA =
        userVer >= 80 && typeof Mozilla.UITour !== 'undefined';
    const fxaSigninLink = document.querySelectorAll('.js-fxa-cta-link');

    if (useUITourForFxA) {
        Mozilla.UITour.ping(() => {
            for (let i = 0; i < fxaSigninLink.length; i++) {
                const link = fxaSigninLink[i];
                const hostName = FxaLink.getHostName(link.href);
                // check if link is in the FxA referral allowedList domains.
                if (hostName && allowedList.indexOf(hostName) === -1) {
                    continue;
                }
                // update link href.
                link.href = FxaLink.updateURL(link.href);

                link.setAttribute('role', 'button');
                link.oncontextmenu = (e) => {
                    e.preventDefault();
                };
                // intercept the flow and submit the form using the UITour API.
                link.addEventListener(
                    'auxclick',
                    FxaLink.interceptFxANavigation
                );
                link.addEventListener('click', FxaLink.interceptFxANavigation);
            }
            callback();
        });
    }
};

export default FxaLink;
