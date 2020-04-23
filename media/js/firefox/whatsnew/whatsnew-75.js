/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function(Mozilla) {
    'use strict';

    var client = Mozilla.Client;
    var body = document.getElementsByTagName('body')[0];

    // bug 1419573 - only show "Your Firefox is up to date" if it's the latest version.
    if (client.isFirefoxDesktop) {
        client.getFirefoxDetails(function(data) {
            if (data.isUpToDate) {
                document.querySelector('.c-page-header').classList.add('show-up-to-date-message');
            }
        });

        client.getFxaDetails(function(details) {
            body.classList.remove('state-fxa-default');

            // if signed in with more than one device, show the Monitor CTA.
            if ((details.setup && details.browserServices.sync.mobileDevices > 0) || window.location.search.indexOf('has-devices=true') !== -1) {
                body.classList.add('state-fxa-has-devices');
            }
            // else if signed in with no other devices, show connect device CTA.
            else if ((details.setup && details.browserServices.sync.mobileDevices === 0) || window.location.search.indexOf('has-no-devices=true') !== -1) {
                body.classList.add('state-fxa-has-no-devices');
            }
        });
    }

})(window.Mozilla);
