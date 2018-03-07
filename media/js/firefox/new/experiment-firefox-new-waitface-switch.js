/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var isDesktop = !/android|ios/.test(site.platform);

    var notFirefox= !/\sFirefox/.test(navigator.userAgent);

    var paramsMatch = function() {
        var params = {
            'utm_medium': 'display',
            'utm_source': 'facebook',
            'utm_campaign': 'x',
            'utm_content': 'switch-lp'
        };

        for (var key in params) {
            if (!(new RegExp('[\&\?]' + key + '=' + params[key])).test(location.search)) {
                return false;
            }
        }

        return true;
    };

    if (isDesktop && notFirefox && paramsMatch()) {
        var marimow = new Mozilla.TrafficCop({
            id: 'exp_firefox_new_switch_waitface',
            variations: {
                'v=1': 33, // control
                'v=2': 33, // altered copy
                'v=3': 33 // loads /firefox/switch.html template
            }
        });

        marimow.init();
    }
})(window.Mozilla);

