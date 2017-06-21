/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // swiped from mozilla-client.js
    var ua = navigator.userAgent;
    var isLikeFirefox = /Iceweasel|IceCat|SeaMonkey|Camino|like\ Firefox/i.test(ua);
    var isFirefox = /\s(Firefox|FxiOS)/.test(ua) && !isLikeFirefox;
    var isMobile = /^(android|ios|fxos)$/.test(window.site.platform);

    var isWin64 = (ua.indexOf('WOW64') > -1 || ua.indexOf('Win64') > -1);

    if (window.site.platform === 'windows' && isWin64 && !isFirefox && !isMobile) {
        var russell = new Mozilla.TrafficCop({
            id: 'experiment_win64_funnelcake',
            variations: {
                'f=105': 11, // 32-bit
                'f=106': 11 // 64-bit
            }
        });

        russell.init();
    }
})(window.Mozilla);
