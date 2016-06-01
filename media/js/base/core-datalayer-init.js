/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// init core dataLayer object and push into dataLayer
$(function() {
    var analytics = Mozilla.Analytics;
    var client = Mozilla.Client;
    var dataLayer = window.dataLayer;

    function sendCoreDataLayer() {
        var dataLayerCore = {
            'event': 'core-datalayer-loaded',
            'pageId': analytics.getPageId(),
            'pageHasDownload': analytics.pageHasDownload(),
            'pageHasVideo': analytics.pageHasVideo(),
            'pageVersion': analytics.getPageVersion(),
            // white listed for www.mozill.org, will always return false on other domains
            'testPilotUser': 'testpilotAddon' in navigator ? 'true' : 'false'
        };

        dataLayer.push(dataLayerCore);
    }

    if (client.isFirefoxDesktop || client.isFirefoxAndroid) {
        client.getFirefoxDetails(function(details) {
            dataLayer.push(details);
            sendCoreDataLayer();
        });
    } else {
        sendCoreDataLayer();
    }

    analytics.updateDataLayerPush();
});
