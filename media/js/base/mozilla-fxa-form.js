/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function(Mozilla) {
    'use strict';

    var FxaForm = {};
    var formElem;

    /**
     * Creates a hidden form input.
     * @param name {String} input name.
     * @param value (String) input value.
     * @returns HTML element.
     */
    FxaForm.createInput = function(name, value) {
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = value;
        return input;
    };

    /**
     * Pass through utm_params from URL if present,
     * to attribute external marketing campaigns.
     *
     * @returns {Object} of utm parameters
     */
    FxaForm.getUTMParams = function() {
        var urlParams = new window._SearchParams().utmParams();
        return Mozilla.UtmUrl.getAttributionData(urlParams) || {};
    };

    /**
     * Get tokens from FxA for analytics purposes.
     * This is non-critical to the user flow.
     */
    FxaForm.fetchTokens = function() {
        var destURL = formElem.getAttribute('action') + 'metrics-flow';
        var entrypoint = document.getElementById('fxa-email-form-entrypoint');
        var entrypointExp = document.getElementById('fxa-email-form-entrypoint-experiment');
        var entrypointVar = document.getElementById('fxa-email-form-entrypoint-variation');
        var utmCampaign = document.getElementById('fxa-email-form-utm-campaign');
        var utmContent = document.getElementById('fxa-email-form-utm-content');
        var utmSource = document.getElementById('fxa-email-form-utm-source');
        var utmTerm = document.getElementById('fxa-email-form-utm-term');

        // add required params to the token fetch request
        destURL += '?form_type=email';
        destURL += '&entrypoint=' + entrypoint.value;
        destURL += '&utm_source=' + utmSource.value;

        if (utmContent) {
            destURL += '&utm_content=' + utmContent.value;
        }

        if (utmCampaign) {
            destURL += '&utm_campaign=' + utmCampaign.value;
        }

        if (utmTerm) {
            destURL += '&utm_term=' + utmTerm.value;
        }

        if (entrypointExp) {
            destURL += '&entrypoint_experiment=' + entrypointExp.value;
        }

        if (entrypointVar) {
            destURL += '&entrypoint_variation=' + entrypointVar.value;
        }

        return fetch(destURL).then(function(resp) {
            return resp.json();
        }).then(function(r) {
            formElem.querySelector('[name="device_id"]').value = r.deviceId;
            formElem.querySelector('[name="flow_id"]').value = r.flowId;
            formElem.querySelector('[name="flow_begin_time"]').value = r.flowBeginTime;
        }).catch(function() {
            // silently fail, leaving flow_id and flow_begin_time as default empty value
        });
    };


    /**
     * Intercept event handler for FxA forms, lets the browser drive the FxA Flow using
     * the `showFirefoxAccounts` UITour API. Attaches several UTM parameters from the current page
     * that will be forwarded to the browser and later on to FxA services.
     * @param event {Event}
     * @private
     */
    FxaForm.interceptFxANavigation = function(event) {
        event.preventDefault();
        var extraURLParams = FxaForm.getUTMParams();

        var entrypointInput = document.getElementById('fxa-email-form-entrypoint');
        var entrypointExp = document.getElementById('fxa-email-form-entrypoint-experiment');
        var entrypointVar = document.getElementById('fxa-email-form-entrypoint-variation');
        var entrypoint = null;
        if (entrypointInput && entrypointInput.value) {
            entrypoint = entrypointInput.value;
        }
        if (entrypointExp && entrypointExp.value) {
            extraURLParams['entrypoint_experiment'] = entrypointExp.value;
        }
        if (entrypointVar && entrypointVar.value) {
            extraURLParams['entrypoint_variation'] = entrypointVar.value;
        }

        var email = document.getElementById('fxa-email-field');
        if (email) {
            email = email.value;
        }

        var formElem = document.getElementById('fxa-email-form');
        if (formElem) {
            var deviceId = formElem.querySelector('[name="device_id"]');
            var flowId = formElem.querySelector('[name="flow_id"]');
            var flowBeginTime = formElem.querySelector('[name="flow_begin_time"]');
            if (deviceId && deviceId.value) {
                extraURLParams['device_id'] = deviceId.value;
            }
            if (flowId && flowId.value) {
                extraURLParams['flow_id'] = flowId.value;
            }
            if (flowBeginTime && flowBeginTime.value) {
                extraURLParams['flow_begin_time'] = parseInt(flowBeginTime.value, 10);
            }
        }
        return Mozilla.UITour.showFirefoxAccounts(extraURLParams, entrypoint, email);
    };

    /**
     * Configures Sync for Firefox browsers.
     * Only Firefox < 71 requires `service=sync`.
     */
    FxaForm.setServiceContext = function() {
        var contextField = formElem.querySelector('[name="context"]');
        var serviceField = formElem.querySelector('[name="service"]');
        var userVer = parseFloat(Mozilla.Client._getFirefoxVersion());
        var self = this;
        var useUITourForFxA = userVer >= 80 && typeof Mozilla.UITour !== 'undefined';

        if (useUITourForFxA) {
            Mozilla.UITour.ping(function() {
                // intercept the flow and submit the form using the UITour API instead.
                // In the future we should fully migrate to this API for Firefox Desktop login.
                formElem.addEventListener('submit', self.interceptFxANavigation);
            });
        }
        /**
         * Context is required for all Firefox desktop clients.
         */
        if (!contextField) {
            var context = FxaForm.createInput('context', 'fx_desktop_v3');
            formElem.appendChild(context);
        }

        /**
         * Sync is an optional flow on Firefox 71 and above,
         * so only set it explicitly for older clients.
         */
        if (!serviceField && userVer < 71) {
            var service = FxaForm.createInput('service', 'sync');
            formElem.appendChild(service);
        }
    };

    /**
     * Checks for China repack, before making a metrics-flow request.
     * Once completed, then configures Sync `context` and `service` params.
     */
    FxaForm.configureRequest = function() {
        var formSubmitButton = document.getElementById('fxa-email-form-submit');
        var mozillaonlineAction = formElem.dataset.mozillaonlineAction;
        var metrics;

        var dist = new window.Promise(function(resolve) {
            // disable form while we configure the distribution.
            formSubmitButton.disabled = true;

            Mozilla.Client.getFirefoxDetails(function(data) {
                // only switch to China re-pack URL if UITour call is successful
                // (marked by data.accurate being true)
                if (mozillaonlineAction && data.accurate && data.distribution && data.distribution.toLowerCase() === 'mozillaonline') {
                    formElem.action = mozillaonlineAction;
                }
                formSubmitButton.disabled = false;

                metrics = new window.Promise(function(resolve) {
                    FxaForm.fetchTokens().then(function() {
                        resolve();
                    });
                });

                resolve();
            });
        });

        // Configure Sync once metrics request has finished.
        return window.Promise.all([dist, metrics]).then(function() {
            FxaForm.setServiceContext();
        });
    };

    FxaForm.isSupported = function() {
        return 'Promise' in window && 'fetch' in window;
    };

    FxaForm.init = function() {
        if (!FxaForm.isSupported()) {
            return false;
        }

        formElem = document.getElementById('fxa-email-form');

        return new window.Promise(function(resolve, reject) {
            if (formElem) {
                // Pass through UTM params from the URL to the form.
                var utms = FxaForm.getUTMParams();
                Object.keys(utms).forEach(function (i) {
                    // check if input is available
                    if (formElem.querySelector('[name="' + i + '"]')) {
                        formElem.querySelector('[name="' + i + '"]').value = utms[i];
                    } else {
                        // create input if one is not present
                        var input = FxaForm.createInput(i, utms[i]);
                        formElem.appendChild(input);
                    }
                });

                // Configure Sync for Firefox desktop browsers.
                if (Mozilla.Client._isFirefoxDesktop()) {
                    FxaForm.configureRequest().then(function() {
                        resolve();
                    });
                } else {
                    FxaForm.fetchTokens().then(function() {
                        resolve();
                    });
                }
            } else {
                reject();
            }
        });
    };

    window.Mozilla.FxaForm = FxaForm;

})(window.Mozilla);
