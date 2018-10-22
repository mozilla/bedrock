/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var ua = navigator.userAgent;
    var isFirefox = /\s(Firefox)/.test(ua) && !/Iceweasel|IceCat|SeaMonkey|Camino|like\ Firefox/i.test(ua);
    var isDesktop = /\sFirefox/.test(ua) && !/Mobile|Tablet|Fennec|FxiOS/.test(ua);
    var firefoxVersion = /Firefox\/(\d+(?:\.\d+){1,2})/.exec(ua);
    var isUpToDate = firefoxVersion && firefoxVersion.hasOwnProperty(1) ? firefoxVersion[1].indexOf(62) === 0 : false;

    if(isFirefox && isDesktop && isUpToDate) {
        var cop = new Mozilla.TrafficCop({
            id: 'scene1_fx_experiment',
            variations: {
                '&v=y': 50, // control
                '&v=x': 50
            }
        });

        cop.init();
    }

})(window.Mozilla);
