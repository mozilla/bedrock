/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    var PocketButton = {};

    PocketButton.init = function(){

        var pocketButton = document.getElementById('pocket-cta');

        // fetch request
        var supportsFetch = 'fetch' in window;

        if (!supportsFetch || !pocketButton) {
            return;
        }

        var buttonURL = pocketButton.getAttribute('href');
        // strip url to everything after `?`
        var buttonURLParams = buttonURL.match(/\?(.*)/)[1];

        var destURL = pocketButton.getAttribute('data-action') + 'metrics-flow';

        // collect values from monitor button
        var params = window._SearchParams.queryStringToObject(buttonURLParams);

        // add required params to the token fetch request
        destURL += '?entrypoint=' + params.entrypoint;
        destURL += '&form_type=' + params.form_type;
        destURL += '&utm_source=' + params.utm_source;

        // add optional utm params to the token fetch request
        if (params.utm_campaign) {
            destURL += '&utm_campaign=' + params.utm_campaign;
        }

        if (params.utm_content) {
            destURL += '&utm_content=' + params.utm_content;
        }

        if (params.utm_term) {
            destURL += '&utm_term=' + params.utm_term;
        }

        fetch(destURL).then(function(resp) {
            return resp.json();
        }).then(function(r) {
            // add retrieved deviceID, flowBeginTime and flowId values to cta url
            buttonURL += '&deviceId=' + r.deviceId;
            buttonURL += '&flowBeginTime=' + r.flowBeginTime;
            buttonURL += '&flowId=' + r.flowId;
            pocketButton.setAttribute('href', buttonURL);
        }).catch(function() {
            // silently fail: deviceId, flowBeginTime, flowId are not added to url.
        });
    };

    window.Mozilla.PocketButton = PocketButton;
})();

