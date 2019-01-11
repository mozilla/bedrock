/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var ua = navigator.userAgent;
    var isLikeFirefox = /Iceweasel|IceCat|SeaMonkey|Camino|like\ Firefox/i.test(ua);
    var isFirefox = /\s(Firefox|FxiOS)/.test(ua) && !isLikeFirefox;

    var isWin10 = (ua.indexOf('Windows NT 10') > -1);

    if (window.site.platform === 'windows' && isWin10 && !isFirefox) {
        var mclane = new Mozilla.TrafficCop({
            id: 'experiment_win10_taskbar_funnelcake',
            variations: {
                'f=138': 9, // control build
                'f=139': 9  // taskbar build
            }
        });

        mclane.init();
    }

})(window.Mozilla);
