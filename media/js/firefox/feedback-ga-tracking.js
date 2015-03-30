/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    function trackGenericLink(action, href, callback) {
        if (typeof callback === 'function') {
            gaTrack(['_trackEvent', 'Feedback Interactions', action, href], callback);
        } else {
            gaTrack(['_trackEvent', 'Feedback Interactions', action, href]);
        }
    }

    // track clicks in the secondary CTAs
    $('.action-secondary').on('click', 'a', function(e) {
        var name = $(this).data('name');
        var href = this.href;
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var callback;

        if (newTab) {
            trackGenericLink('CTA click', name);
        } else {
            e.preventDefault();
            callback = function() {
                window.location = href;
            };
            trackGenericLink('CTA click', name, callback);
        }
    });

    // track clicks in the SUMO links
    $('.support-links').on('click', 'a', function(e) {
        var label = $(this).text();
        var href = this.href;
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var callback;

        if (newTab) {
            trackGenericLink('SUMO click', label);
        } else {
            e.preventDefault();
            callback = function() {
                window.location = href;
            };
            trackGenericLink('SUMO click', label, callback);
        }
    });

})(window.jQuery);
