/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var isChrome = !!window.chrome;

    // courtesy of https://davidwalsh.name/query-string-javascript
    function getUrlParam(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // if we already have a utm_content parameter, don't clobber existing stub attribution data.
    if (window.site.platform === 'windows' && isChrome && !getUrlParam('utm_content')) {
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
