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

    FxaForm.init = function() {
        var fxaForm = document.getElementById('fxa-email-form');
        var fxaSubmitButton = document.getElementById('fxa-email-form-submit');
        var fxaFormContextField = fxaForm.querySelector('[name="context"]');
        var fxaFormServiceField = fxaForm.querySelector('[name="service"]');
        var supportsFetch = 'fetch' in window;

        // swap form action for Fx China re-pack
        function init() {
            // disable form while we check distribution
            fxaSubmitButton.disabled = true;

            var mozillaonlineAction = fxaForm.dataset.mozillaonlineAction;

            if (mozillaonlineAction) {
                Mozilla.Client.getFirefoxDetails(function(data) {
                    // only switch to China re-pack URL if UITour call is successful
                    // (marked by data.accurate being true)
                    if (data.accurate && data.distribution && data.distribution.toLowerCase() === 'mozillaonline') {
                        fxaForm.action = mozillaonlineAction;
                    }
                    fetchTokens();
                });
            } else {
                fetchTokens();
            }
        }

        // get tokens from FxA for analytics purposes
        function fetchTokens() {
            if (!supportsFetch) {
                return;
            }

            fxaSubmitButton.disabled = false;

            // track external UTM referrals
            var urlParams = new window._SearchParams().utmParams();
            var attributionData = Mozilla.UtmUrl.getAttributionData(urlParams);

            if (attributionData) {
                var utms = ['utm_source', 'utm_campaign', 'utm_content', 'utm_term', 'utm_medium'];
                for (var i = 0; i < utms.length; i++) {
                    if (Object.prototype.hasOwnProperty.call(attributionData, utms[i])) {
                        // check if input is available
                        if (fxaForm.querySelector('[name="' + utms[i] + '"]')) {
                            fxaForm.querySelector('[name="' + utms[i] + '"]').value = attributionData[utms[i]];
                        } else {
                            // create input if one is not present
                            var input = document.createElement('input');
                            input.type = 'hidden';
                            input.name = utms[i];
                            input.value = attributionData[utms[i]];
                            fxaForm.appendChild(input);
                        }
                    } else {
                        // do not update form params.
                    }
                }
            }

            var entrypoint = document.getElementById('fxa-email-form-entrypoint');
            var entrypointExp = document.getElementById('fxa-email-form-entrypoint-experiment');
            var entrypointVar = document.getElementById('fxa-email-form-entrypoint-variation');
            var utmSource = document.getElementById('fxa-email-form-utm-source');

            var destURL = fxaForm.getAttribute('action') + 'metrics-flow';

            // add required params to the token fetch request
            destURL += '?form_type=email';
            destURL += '&entrypoint=' + entrypoint.value;
            destURL += '&utm_source=' + utmSource.value;

            // add optional utm params to the token fetch request

            var utmTerm = document.getElementById('fxa-email-form-utm-term');
            var utmCampaign = document.getElementById('fxa-email-form-utm-campaign');
            var utmContent = document.getElementById('fxa-email-form-utm-content');

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

            fetch(destURL).then(function(resp) {
                return resp.json();
            }).then(function(r) {
                fxaForm.querySelector('[name="device_id"]').value = r.deviceId;
                fxaForm.querySelector('[name="flow_id"]').value = r.flowId;
                fxaForm.querySelector('[name="flow_begin_time"]').value = r.flowBeginTime;
            }).catch(function() {
                // silently fail, leaving flow_id and flow_begin_time as default empty value
            });
        }

        if (fxaForm) {
            // Sync is Firefox for desktop only.
            if (Mozilla.Client.isFirefoxDesktop) {
                init();
            } else {
                // Omit the fields required for sync.
                // This allows non-Firefoxes to create accounts.
                fxaForm.removeChild(fxaFormContextField);
                fxaForm.removeChild(fxaFormServiceField);
                fetchTokens();
            }
        }
    };

    window.Mozilla.FxaForm = FxaForm;

})(window.Mozilla);
