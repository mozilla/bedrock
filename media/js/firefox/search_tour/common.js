/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    function trackClick(e, href, label, newTab) {
        var callback;

        if (newTab) {
            gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', 'All', label]);
        } else {
            e.preventDefault();
            callback = function() {
                window.location = href;
            };
            gaTrack(['_trackEvent', 'whatsnew srch-chg interactions', 'All', label], callback);
        }
    }

    // track button clicks on Sync cta button
    $('.sync-cta a.button').on('click', function(e) {
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        trackClick(e, this.href, 'syncButton', newTab);
    });

    // track button clicks on fx10 banner
    $('aside a.button').on('click', function(e) {
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        trackClick(e, this.href, 'declareButton', newTab);
    });

})(window.jQuery, window.Mozilla);
