/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

Mozilla.MonitorButton = (function () {
    'use strict';

    var monitorButton = document.getElementById('fxa-monitor-submit');

    // fetch request
    var supportsFetch = 'fetch' in window;

    if (!supportsFetch || !monitorButton) {
        return;
    }

    var buttonURL = monitorButton.getAttribute('href');
    // strip url to everything after `?`
    buttonURL = buttonURL.match(/\?(.*)/)[1];

    var destURL = monitorButton.getAttribute('data-action') + 'metrics-flow';

    // collect values from monitor button
    var utmParams = _SearchParams.queryStringToObject(buttonURL);

    var utmSource = utmParams.utm_source;
    var utmCampaign = utmParams.utm_campaign;
    var entrypoint = utmParams.entrypoint;
    var formType = utmParams.form_type;

    // add required params to the token fetch request
    destURL += '?' + formType;
    destURL += '&' + entrypoint;
    destURL += '&' + utmSource;

    // pass utm_campaign if available
    if (utmCampaign) {
        destURL += '&' + utmCampaign;
    }

    fetch(destURL).then(function (resp) {
        return resp.json();
    }).then(function (r) {
        // add retrieved deviceID, flowBeginTime and flowId values to cta url
        buttonURL += '&deviceId=' + r.deviceId;
        buttonURL += '&flowBeginTime=' + r.flowBeginTime;
        buttonURL += '&flowId=' + r.flowId;
        monitorButton.setAttribute('href', buttonURL);
    }).catch(function () {
        // silently fail: deviceId, flowBeginTime, flowId are not added to url.
    });
})();

