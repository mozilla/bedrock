/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

Mozilla.MonitorButton = (function(Mozilla) {
    'use strict';

    var monitorButton = document.getElementById('fxa-monitor-submit');
    var buttonURL = monitorButton.getAttribute('href');

    // fetch request
    var supportsFetch = 'fetch' in window;

    if (!supportsFetch) {
        return;
    }

    var destURL = monitorButton.getAttribute('action') + 'metrics-flow';

    fetch(destURL).then(function(resp) {
        return resp.json();
    }).then(function(r) {
        // add retrieved flowBeginTime and flowId values to cta url
        buttonURL += '&flowBeginTime=' + r.flowBeginTime;
        buttonURL += '&flowId=' + r.flowId;
        monitorButton.setAttribute('href', buttonURL);
    }).catch(function() {
        // silently fail, leaving flow_id and flow_begin_time as default empty value
    });
})(window.Mozilla);

