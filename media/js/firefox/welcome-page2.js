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

    PocketButton.init = function() {
        var buttons;

        // Exit if no fetch support
        var supportsFetch = 'fetch' in window;
        if (!supportsFetch) {
            return;
        }

        // Collect all monitor buttons
        buttons = document.getElementsByClassName('js-pocket-button');

        // Exit if no valid button in DOM
        if (buttons.length === 0) {
            return;
        }


        var buttonURL = buttons[0].getAttribute('href');
        // strip url to everything after `?`
        var buttonURLParams = buttonURL.match(/\?(.*)/)[1];

        var destURL = buttons[0].getAttribute('data-action') + 'metrics-flow';

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
            var flowParams = '&deviceId=' + r.deviceId;
            flowParams += '&flowBeginTime=' + r.flowBeginTime;
            flowParams += '&flowId=' + r.flowId;
            // applies url to all buttons and adds cta position
            for (var i=0; i<buttons.length; i++) {
                buttons[i].href += flowParams;
            }
        }).catch(function() {
            // silently fail: deviceId, flowBeginTime, flowId are not added to url.
        });
    };

    window.Mozilla.PocketButton = PocketButton;
})();

