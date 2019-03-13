/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var isWithinSampleRate = Math.random() <= 0.5;

    // Check that cookies are supported.
    if (typeof Mozilla.Cookies === 'undefined' || !Mozilla.Cookies.enabled()) {
        return;
    }

    // Exclude users who are in alternate headline experiment (Issue #6851)
    if (Mozilla.Cookies.hasItem('experiment-firefox-new-headline-us')) {
        return;
    }

    // Exclude existing Firefox users.
    if (/\s(Firefox)/.test(navigator.userAgent)) {
        return;
    }

    // Allow 50% of users to drop through to alternate headline experiment (Issue #6851)
    if (!isWithinSampleRate && !Mozilla.Cookies.hasItem('priv-dmt')) {
        return;
    }

    // courtesy of https://davidwalsh.name/query-string-javascript
    function getUrlParam(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // if we already have an `xv` parameter on the page, don't enter into the experiment.
    if (!getUrlParam('xv')) {
        var murphy = new Mozilla.TrafficCop({
            id: 'priv-dmt',
            variations: {
                'xv=priv-dmt&v=1': 98.2, // control
                'xv=priv-dmt&v=a': 0.3,
                'xv=priv-dmt&v=b': 0.3,
                'xv=priv-dmt&v=c': 0.3,
                'xv=priv-dmt&v=d': 0.3,
                'xv=priv-dmt&v=e': 0.3,
                'xv=priv-dmt&v=f': 0.3,
            }
        });

        murphy.init();
    }

})(window.Mozilla);
