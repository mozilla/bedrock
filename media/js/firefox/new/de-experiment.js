/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    /* update dataLayer with experiment info */
    var href = window.location.href;
    if(href.indexOf('v=') !== -1) {
        if(href.indexOf('v=a') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'de-page',
                'data-ex-name': 'Berlin-Campaign-Landing-Page'
            });
        } else if (href.indexOf('v=b') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'campaign-page',
                'data-ex-name': 'Berlin-Campaign-Landing-Page'
            });
        }
    } else {
        var cop = new Mozilla.TrafficCop({
            id: 'experiment_firefox_new_de_hearts',
            variations: {
                'v=a': 10,
                'v=b': 10
            }
        });

        cop.init();
    }

})(window.Mozilla);
