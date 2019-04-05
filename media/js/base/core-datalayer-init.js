/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// init core dataLayer object and push into dataLayer
$(function() {
    var analytics = Mozilla.Analytics;
    var client = Mozilla.Client;
    var dataLayer = window.dataLayer = window.dataLayer || [];
    var firefoxDetailsComplete = false;
    var fxaDetailsComplete = false;

    function sendCoreDataLayer() {
        var dataLayerCore = {
            'event': 'core-datalayer-loaded',
            'pageHasDownload': analytics.pageHasDownload(),
            'pageHasVideo': analytics.pageHasVideo(),
            'pageVersion': analytics.getPageVersion(),
            // white listed for www.mozill.org, will always return false on other domains
            'testPilotUser': 'testpilotAddon' in navigator ? 'true' : 'false',
            'releaseWindowVersion': analytics.getLatestFxVersion(),
            'win10SUser': analytics.isWin10S()
        };

        dataLayer.push(dataLayerCore);
    }

    function checkSendCoreDataLayer() {
        if (firefoxDetailsComplete && fxaDetailsComplete) {
            sendCoreDataLayer();
        }
    }

    client.getFxaDetails(function(details) {
        dataLayer.push(analytics.formatFxaDetails(details));
        fxaDetailsComplete = true;
        checkSendCoreDataLayer();
    });

    if (client.isFirefoxDesktop || client.isFirefoxAndroid) {
        client.getFirefoxDetails(function(details) {
            dataLayer.push(details);
            firefoxDetailsComplete = true;
            checkSendCoreDataLayer();
        });
    } else {
        firefoxDetailsComplete = true;
        checkSendCoreDataLayer();
    }

    analytics.updateDataLayerPush();
});
