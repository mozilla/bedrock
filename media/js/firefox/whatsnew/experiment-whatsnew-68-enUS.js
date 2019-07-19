/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


(function() {
    'use strict';

    // Exclude signed in users
    function fxaSignedOut() {
        Mozilla.Client.getFxaDetails(function(details) {
            if (!details.setup) {
                return true;
            } else {
                return false;
            }
        });
    }

    // courtesy of https://davidwalsh.name/query-string-javascript
    function getUrlParam(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // if we already have a `v` parameter on the page, or the user is signed into Sync, don't enter into the experiment.
    if (!getUrlParam('v') && fxaSignedOut) {
        var deckard = new Mozilla.TrafficCop({
            id: 'experiment_firefox_whatsnew_68',
            variations: {
                'v=a': 1,  // control
                'v=b': 1,  // new layout, light
                'v=c': 1,  // new layout, dark
                'v=d': 1,  // notification favicon
                'v=e': 1   // monitor CTA
            }
        });

        deckard.init();
    }

})(window.Mozilla);
