/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    function setCohorts() {
        var lang = document.getElementsByTagName('html')[0].getAttribute('lang');
        var cohorts;

        switch(lang) {
        case 'en-GB':
            cohorts = {
                'a': 64,
                'b': 18,
                'c': 18
            };
            break;
        case 'de':
            cohorts = {
                'a': 84,
                'b': 8,
                'c': 8
            };
            break;
        }

        return cohorts;
    }

    if (window.site.platform !== 'windows') {
        return;
    }

    var cohorts = setCohorts();

    if (cohorts) {
        var cooper = new Mozilla.TrafficCop({
            id: 'experiment-firefox-new-features',
            variations: {
                'v=a': cohorts['a'], // control
                'v=b': cohorts['b'], // 3 short features
                'v=c': cohorts['c'], // long-form features
            }
        });

        cooper.init();
    }

})(window.Mozilla);
