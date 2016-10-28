/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var isFirefox = /\sFirefox/.test(navigator.userAgent);
    var isLikeFirefox = /Iceweasel|IceCat|SeaMonkey|Camino|like\ Firefox/i.test(navigator.userAgent);

    function getFirefoxVersion() {
        var matches = /Firefox\/(\d+(?:\.\d+){1,2})/.exec(navigator.userAgent);
        var version = matches ? matches[1] : '0';

        return parseInt(version, 10);
    }

    if (isFirefox && !isLikeFirefox) {
        var userMajorVersion = getFirefoxVersion();
        var latestMajorVersion = parseInt(document.getElementsByTagName('html')[0].getAttribute('data-latest-firefox'), 10);

        // only run A/B test for up to date users.
        if (userMajorVersion === latestMajorVersion) {

            var cop = new Mozilla.TrafficCop({
                id: 'exp_fx_new_up_to_date_users',
                variations: {
                    'v=a': 33, // double control group
                    'v=b': 33, // download button underneath help links
                    'v=c': 33  // download button and refresh firefox button
                }
            });

            cop.init();
        }
    }

})(window.Mozilla);
