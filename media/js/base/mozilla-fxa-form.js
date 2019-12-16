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
     */
    FxaForm.getUTMParams = function() {
        var urlParams = new window._SearchParams().utmParams();
        var attributionData = Mozilla.UtmUrl.getAttributionData(urlParams);

        if (attributionData) {
            var utms = ['utm_source', 'utm_campaign', 'utm_content', 'utm_term', 'utm_medium'];
            for (var i = 0; i < utms.length; i++) {
                if (Object.prototype.hasOwnProperty.call(attributionData, utms[i])) {
                    // check if input is available
                    if (formElem.querySelector('[name="' + utms[i] + '"]')) {
                        formElem.querySelector('[name="' + utms[i] + '"]').value = attributionData[utms[i]];
                    } else {
                        // create input if one is not present
                        var input = FxaForm.createInput(utms[i], attributionData[utms[i]]);
                        formElem.appendChild(input);
                    }
                }
            }
        }
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
     * Configures Sync for Firefox browsers.
     * Only Firefox < 71 requires `service=sync`.
     */
    FxaForm.setServiceContext = function() {
        var contextField = formElem.querySelector('[name="context"]');
        var serviceField = formElem.querySelector('[name="service"]');
        var userVer = parseFloat(Mozilla.Client._getFirefoxVersion());

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
                FxaForm.getUTMParams();

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
