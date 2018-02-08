/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


/* Experiment: https://bugzilla.mozilla.org/show_bug.cgi?id=1434764
 * URL: https://www.mozilla.org/en-US/firefox/new/?xv=waitface
 * Audience: Desktop, Non-Fx, en-US with utm_medium=display&utm_source=doubleclick    
 * Traffic: 100% audience, 50/50 split*/

(function() {
    'use strict';

    var isDesktop = !/android|ios/.test(site.platform);

    var notFirefox= !/\sFirefox/.test(navigator.userAgent);

    var paramsMatch = function() {
        var params = {
            'utm_medium': 'display', 
            'utm_source': 'doubleclick'
        };

        for (var key in params) {
            if (!(new RegExp('[\&\?]' + key + '=' + params[key])).test(location.search)) {
                return false;
            }
        }
        return true;
    };

    if (isDesktop && notFirefox && paramsMatch()) {
        var cop = new Mozilla.TrafficCop({
            id: 'experiment_firefox_new_waitface',
            variations: {
                'v=a': 50, // 50% redirected to control
                'v=b': 50   // 50% redirected to video content
            }
        });
        cop.init();
    }

})(window.Mozilla);
