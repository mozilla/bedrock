/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// init core dataLayer object and push into dataLayer
(function () {
    'use strict';

    var analytics = Mozilla.Analytics;
    var client = Mozilla.Client;
    var dataLayer = (window.dataLayer = window.dataLayer || []);
    var firefoxDetailsComplete = false;
    var fxaDetailsComplete = false;

    function sendCoreDataLayer() {
        var dataLayerCore = {
            event: 'core-datalayer-loaded',
            pageHasDownload: analytics.pageHasDownload(),
            pageHasVideo: analytics.pageHasVideo(),
            pageVersion: analytics.getPageVersion(),
            // permitted for www.mozill.org, will always return false on other domains
            testPilotUser: 'testpilotAddon' in navigator ? 'true' : 'false',
            releaseWindowVersion: analytics.getLatestFxVersion()
        };

        dataLayer.push(dataLayerCore);
    }

    function checkSendCoreDataLayer() {
        if (firefoxDetailsComplete && fxaDetailsComplete) {
            sendCoreDataLayer();
        }
    }

    function initCoreDataLayer() {
        client.getFxaDetails(function (details) {
            dataLayer.push(analytics.formatFxaDetails(details));
            fxaDetailsComplete = true;
            checkSendCoreDataLayer();
        });

        if (client.isFirefoxDesktop || client.isFirefoxAndroid) {
            client.getFirefoxDetails(function (details) {
                dataLayer.push(details);
                firefoxDetailsComplete = true;
                checkSendCoreDataLayer();
            });
        } else {
            firefoxDetailsComplete = true;
            checkSendCoreDataLayer();
        }

        analytics.updateDataLayerPush();
    }

    // Init dataLayer event on DOM Ready.
    if (typeof Mozilla.Utils !== 'undefined') {
        Mozilla.Utils.onDocumentReady(function () {
            initCoreDataLayer();

            // Add GA custom dimension for AMO experiments (Issue 10175).
            if (typeof window._SearchParams !== 'undefined') {
                var params = new window._SearchParams().params;
                var validParams = analytics.getAMOExperiment(params);

                if (validParams) {
                    dataLayer.push({
                        'data-ex-name': validParams['experiment'],
                        'data-ex-variant': validParams['variation']
                    });
                }
            }
        });
    }
})();
