/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

Mozilla.FxaForm = (function(Mozilla) {
    'use strict';

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

        var destURL = fxaForm.getAttribute('action') + 'metrics-flow';
        var entrypoint = document.getElementById('fxa-email-form-entrypoint');
        var utmSource = document.getElementById('fxa-email-form-utm-source');
        var utmCampaign = document.getElementById('fxa-email-form-utm-campaign');

        // add required params to the token fetch request
        destURL += '?form_type=email';
        destURL += '&entrypoint=' + entrypoint.value;
        destURL += '&utm_source=' + utmSource.value;

        // pass utm_campaign if available
        if (utmCampaign) {
            destURL += '&utm_campaign=' + utmCampaign.value;
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
})(window.Mozilla);
