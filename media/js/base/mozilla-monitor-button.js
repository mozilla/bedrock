/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    var MonitorButton = {};

    MonitorButton.init = function(buttonId){

        // check for custom buttonId, used in case of multiple buttons.
        if(!buttonId){
            buttonId = 'fxa-monitor-submit';
        }

        var monitorButton = document.getElementById(buttonId);

        // fetch request
        var supportsFetch = 'fetch' in window;

        if (!supportsFetch || !monitorButton) {
            return;
        }

        var buttonURL = monitorButton.getAttribute('href');
        // strip url to everything after `?`
        var buttonURLParams = buttonURL.match(/\?(.*)/)[1];

        var destURL = monitorButton.getAttribute('data-action') + 'metrics-flow';

        // collect values from monitor button
        var params = window._SearchParams.queryStringToObject(buttonURLParams);

        // add required params to the token fetch request
        destURL += '&entrypoint=' + params.entrypoint;
        destURL += '&form_type=' + params.form_type;
        destURL += '&utm_campaign=' + params.campaign;
        destURL += '&utm_content=' + params.content;
        destURL += '&utm_source=' + params.source;

        fetch(destURL).then(function(resp) {
            return resp.json();
        }).then(function(r) {
            // add retrieved deviceID, flowBeginTime and flowId values to cta url
            buttonURL += '&deviceId=' + r.deviceId;
            buttonURL += '&flowBeginTime=' + r.flowBeginTime;
            buttonURL += '&flowId=' + r.flowId;
            monitorButton.setAttribute('href', buttonURL);
        }).catch(function() {
            // silently fail: deviceId, flowBeginTime, flowId are not added to url.
        });
    };

    window.Mozilla.MonitorButton = MonitorButton;
})();

