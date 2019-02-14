/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    function isChromeDesktopWin() {
        /**
         * Thankfully this is only for a short-term, targeted experiment.
         * This is not something we should ever do in fully-featured code.
         * Let us never speak of this again.
         **/
        var isChrome = !!window.chrome;
        var isOpera = typeof window.opr !== 'undefined';
        var isEdge = window.navigator.userAgent.indexOf('Edge') > -1;
        var isYandex = window.navigator.userAgent.indexOf('YaBrowser') > -1;

        // Limit the platform to Windows (i.e. desktop).
        if (window.site.platform !== 'windows') {
            return false;
        }

        // Attack of the clones!
        if (isEdge || isOpera || isYandex) {
            return false;
        }

        // Filter out all other non-Chromium browsers.
        if (!isChrome) {
            return false;
        }

        // Assume Chrome (likely not 100% accurate).
        return true;
    }


    // courtesy of https://davidwalsh.name/query-string-javascript
    function getUrlParam(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // if we already have a utm_content parameter, don't clobber existing stub attribution data.
    if (isChromeDesktopWin() && !getUrlParam('utm_content')) {
        var cooper = new Mozilla.TrafficCop({
            id: 'experiment_firefox_download_install',
            variations: {
                'v=a': 50, // control
                'v=b': 25, // install instructions
                'v=c': 25  // mobile app store buttons
            }
        });

        cooper.init();
    }

})(window.Mozilla);
