/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var client = Mozilla.Client;
    if(client.isFirefox){
        client.getFirefoxDetails(function(details) {
            // only initialize experiment if current Firefox user not logged into FxA
            if (details.firefox && !details.setup && (client.FirefoxVersion.indexOf(62) === 0)) {
                var cop = new Mozilla.TrafficCop({
                    id: 'scene1_fx_experiment',
                    variations: {
                        '&v=y': 50, // control
                        '&v=x': 50
                    }
                });

                cop.init();
            }
        });
    }

})(window.Mozilla);
