/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    var FxaProductButton = {};

    var allowedList = [
        'https://accounts.firefox.com/',
        'https://monitor.firefox.com/',
        'https://getpocket.com/',
        'https://latest.dev.lcip.org/',
        'https://accounts.firefox.com.cn/',
        'https://vpn.mozilla.org/',
        'https://stage-vpn.guardian.nonprod.cloudops.mozgcp.net/',
        'https://guardian-dev.herokuapp.com/'
    ];

    var _buttons;

    /**
     * Returns the hostname for a given URL.
     * @param {String} url.
     * @returns {String} hostname.
     */
    FxaProductButton.getHostName = function(url) {
        var matches = url.match(/^https?:\/\/(?:[^/?#]+)(?:[/?#]|$)/i);
        return matches && matches[0];
    };

    /**
     * Get tokens from FxA for analytics purposes.
     * This is non-critical to the user flow.
     */
    FxaProductButton.fetchTokens = function(buttons) {
        // assume the first button should dictate the metrics flow request
        var buttonURL = buttons[0].getAttribute('href');
        var metricsURL = buttons[0].getAttribute('data-action') + 'metrics-flow';

        // strip url to everything after `?`
        var buttonURLParams = buttonURL.match(/\?(.*)/)[1];

        // collect values from Fxa product button
        var params = window._SearchParams.queryStringToObject(buttonURLParams);

        // add required params to the token fetch request
        metricsURL += '?form_type=' + params.form_type;
        metricsURL += '&entrypoint=' + params.entrypoint;
        metricsURL += '&utm_source=' + params.utm_source;

        // add optional utm params to the token fetch request
        if (params.utm_campaign) {
            metricsURL += '&utm_campaign=' + params.utm_campaign;
        }

        if (params.utm_content) {
            metricsURL += '&utm_content=' + params.utm_content;
        }

        if (params.utm_term) {
            metricsURL += '&utm_term=' + params.utm_term;
        }

        if (params.entrypoint_experiment) {
            metricsURL += '&entrypoint_experiment=' + params.entrypoint_experiment;
        }

        if (params.entrypoint_variation) {
            metricsURL += '&entrypoint_variation=' + params.entrypoint_variation;
        }

        return fetch(metricsURL).then(function(resp) {
            return resp.json();
        }).then(function(r) {
            // add retrieved deviceID, flowBeginTime and flowId values to cta url
            var flowParams = '&device_id=' + r.deviceId;
            flowParams += '&flow_begin_time=' + r.flowBeginTime;
            flowParams += '&flow_id=' + r.flowId;
            return flowParams;
        }).catch(function() {
            // silently fail: deviceId, flowBeginTime, flowId are not added to url.
        });
    };

    /**
     * Attaches metrics flow parameters to FxA links.
     * @param {Object} Node List
     * @param {String} flowParams
     */
    FxaProductButton.updateProductLinks = function(buttons, flowParams) {
        // if flowParams are undefined (e.g. blocked by CORS), then do nothing.
        if (!flowParams) {
            return;
        }

        // applies url to all buttons and adds cta position
        for (var i = 0; i < buttons.length; i++) {
            var hostName = FxaProductButton.getHostName(buttons[i].href);
            // check if link is in the FxA referral allowedListDomains.
            if (hostName && allowedList.indexOf(hostName) !== -1) {
                buttons[i].href += flowParams;
            }
        }
    };

    /**
     * Switches FxA links to point to mozillaonline FxA server for China repack.
     * @param {Object} Node List
     */
    FxaProductButton.switchDistribution = function(buttons) {
        for (var i = 0; i < buttons.length; i++) {
            var mozillaonlineAction = buttons[i].getAttribute('data-mozillaonline-action');
            var mozillaonlineLink = buttons[i].getAttribute('data-mozillaonline-link');

            if (mozillaonlineAction && mozillaonlineLink) {
                buttons[i].href = mozillaonlineLink;
                buttons[i].setAttribute('data-action', mozillaonlineAction);
            }
        }
    };

    /**
     * Checks for China repack, before making a metrics-flow request.
     */
    FxaProductButton.configureRequest = function() {
        return new window.Promise(function(resolve) {
            Mozilla.Client.getFirefoxDetails(function(data) {
                var syncButtons = document.querySelectorAll('.js-fxa-product-button[data-mozillaonline-link]');
                /**
                 * Only switch to China repack URLs if there are Sync buttons on the page,
                 * and if UITour call is successful (marked by data.accurate being true)
                 */
                if (syncButtons.length && data.accurate && data.distribution && data.distribution.toLowerCase() === 'mozillaonline') {
                    FxaProductButton.switchDistribution(syncButtons);
                    /**
                     * Rather than waiting on requests from multiple servers,
                     * only attach metrics params to Sync buttons for China repack
                     * if there is more than one type of product button on a page.
                     */
                    FxaProductButton.fetchTokens(syncButtons).then(function(flowParams) {
                        FxaProductButton.updateProductLinks(syncButtons, flowParams);
                        resolve();
                    });
                } else {
                    FxaProductButton.fetchTokens(_buttons).then(function(flowParams) {
                        FxaProductButton.updateProductLinks(_buttons, flowParams);
                        resolve();
                    });
                }
            });
        });
    };

    FxaProductButton.isSupported = function() {
        return 'Promise' in window && 'fetch' in window;
    };

    FxaProductButton.init = function() {
        if (!FxaProductButton.isSupported()) {
            return false;
        }

        // Collect all Fxa product buttons
        _buttons = document.getElementsByClassName('js-fxa-product-button');

        return new window.Promise(function(resolve, reject) {
            if (_buttons.length) {
                // Configure Sync for Firefox desktop browsers
                if (Mozilla.Client._isFirefoxDesktop()) {
                    FxaProductButton.configureRequest().then(function() {
                        resolve();
                    });
                } else {
                    FxaProductButton.fetchTokens(_buttons).then(function(flowParams) {
                        FxaProductButton.updateProductLinks(_buttons, flowParams);
                        resolve();
                    });
                }
            } else {
                reject();
            }
        });
    };

    window.Mozilla.FxaProductButton = FxaProductButton;
})();

