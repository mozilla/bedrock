/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


(function() {
    'use strict';

    // courtesy of https://davidwalsh.name/query-string-javascript
    function getUrlParam(name) {
        name = name.replace(/[[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // if we already have a `v` parameter on the page don't enter into the experiment.
    if (!getUrlParam('v')) {
        var wallander = new Mozilla.TrafficCop({
            id: 'experiment_firefox_whatsnew_70',
            variations: {
                'v=0': 5,  // control
                'v=1': 5,  // Monitor, standard
                'v=2': 5,  // Monitor, emotive
                'v=3': 5,  // Sync, standard
                'v=4': 5,  // Sync, emotive
                'v=5': 5,  // Account, ETP
                'v=6': 5,  // Account, what's actually new
                'v=7': 5,  // Account, privacy
            }
        });

        wallander.init();
    }

})(window.Mozilla);
