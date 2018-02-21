/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla, dataLayer) {
    'use strict';

    // do not run on mobile OS's
    var isDesktop = !/android|ios/.test(site.platform);
    // do not run on IE < 9
    var isIELT9 = /MSIE\s[1-8]\./.test(navigator.userAgent);
    // only run if referrer is present and does not contain www.mozilla.org
    var isReferral = document.referrer !== '' && !/www\.mozilla\.org/.test(document.referrer);

    if (isReferral && isDesktop && !isIELT9) {
        var callback = function(variation) {
            dataLayer.push({
                'data-ex-present': 'true',
                'data-ex-variant': variation === 'a' ? 'dev-link-present' : 'control',
                'data-ex-experiment': 'fx-dev-ed-on-new'
            });

            if (variation === 'a') {
                // wait for DOM load so we can find/alter the callout element
                document.addEventListener('DOMContentLoaded', function() {
                    var callout = document.getElementById('callout');
                    callout.setAttribute('class', 'visible');
                });
            }
        };

        var ramathorn = new Mozilla.TrafficCop({
            id: 'experiment_firefox_new_dev_edition',
            customCallback: callback,
            variations: {
                'a': 5
            }
        });

        ramathorn.init();
    }
})(window.Mozilla, window.dataLayer || []);
