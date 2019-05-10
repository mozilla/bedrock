/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var isFirefox = /\sFirefox/.test(navigator.userAgent);

    if (window.site.platform !== 'windows' || isFirefox) {
        return;
    }

    var cop = new Mozilla.TrafficCop({
        id: 'experiment-firefox-new-pre-download',
        variations: {
            'xv=th&v=a': 2, // control
            'xv=th&v=b': 2 // redesign
        }
    });

    cop.init();

})();
