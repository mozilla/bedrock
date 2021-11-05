/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function () {
    'use strict';

    var FxaLink = {};
    var client = Mozilla.Client;
    var allowedList = [
        'https://accounts.firefox.com/',
        'https://accounts.stage.mozaws.net/',
        'https://accounts.firefox.com.cn/'
    ];

    /**
     * Configures Sync for Firefox browsers.
     * Only Firefox < 71 requires `service=sync`.
     * @param href {String}
     * @returns href {String}
     */
    FxaLink.updateURL = function (href) {
        var userVer = parseFloat(client._getFirefoxVersion());
        var serviceParam = userVer < 71 ? 'service=sync' : null;
        var contextParam = 'context=fx_desktop_v3';
        var separator = href.indexOf('?') > 0 ? '&' : '?';

        if (serviceParam) {
            href += separator + contextParam + '&' + serviceParam;
        } else {
            href += separator + contextParam;
        }

        return href;
    };

    /**
     * Returns the hostname for a given URL.
     * @param {String} url.
     * @returns {String} hostname.
     */
    FxaLink.getHostName = function (url) {
        var matches = url.match(/^https?:\/\/(?:[^/?#]+)(?:[/?#]|$)/i);
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
        var search = new URL(event.target.href).search;
        var urlParams = new window._SearchParams(search).params;
        var extraURLParams = {};
        var allowedChars = /^[\w/.%-]+$/;
        var knownParams = [
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

        for (var i = 0; i < knownParams.length; i++) {
            var known = knownParams[i];
            if (Object.prototype.hasOwnProperty.call(urlParams, known)) {
                var param = decodeURIComponent(urlParams[known]);
                if (allowedChars.test(param)) {
                    extraURLParams[known] = param;
                }
            }
        }
        var entrypoint = extraURLParams.entrypoint;
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

        var userVer = parseFloat(client._getFirefoxVersion());
        var useUITourForFxA =
            userVer >= 80 && typeof Mozilla.UITour !== 'undefined';
        var self = this;
        var fxaSigninLink = document.querySelectorAll('.js-fxa-cta-link');

        for (var i = 0; i < fxaSigninLink.length; i++) {
            var link = fxaSigninLink[i];
            var hostName = FxaLink.getHostName(link.href);
            // check if link is in the FxA referral allowedList domains.
            if (hostName && allowedList.indexOf(hostName) === -1) {
                continue;
            }

            // update link href.
            link.href = FxaLink.updateURL(link.href);

            // update china repack URL.
            var mozillaOnlineLink = link.getAttribute(
                'data-mozillaonline-link'
            );
            if (mozillaOnlineLink) {
                link.setAttribute(
                    'data-mozillaonline-link',
                    FxaLink.updateURL(mozillaOnlineLink)
                );
            }
        }

        if (useUITourForFxA) {
            Mozilla.UITour.ping(function () {
                for (var i = 0; i < fxaSigninLink.length; i++) {
                    var link = fxaSigninLink[i];
                    var hostName = FxaLink.getHostName(link.href);
                    // check if link is in the FxA referral allowedList domains.
                    if (hostName && allowedList.indexOf(hostName) === -1) {
                        continue;
                    }
                    link.setAttribute('role', 'button');
                    link.oncontextmenu = function (e) {
                        e.preventDefault();
                    };
                    // intercept the flow and submit the form using the UITour API instead.
                    // In the future we should fully migrate to this API for Firefox Desktop login.
                    link.addEventListener(
                        'auxclick',
                        self.interceptFxANavigation
                    );
                    link.addEventListener('click', self.interceptFxANavigation);
                }
                callback();
            });
        } else {
            callback();
        }
    };

    window.Mozilla.FxaLink = FxaLink;
})();
