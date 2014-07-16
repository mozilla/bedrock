/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    $('#nightly-box a').on('click', function(e) {
        e.preventDefault();

        var href = this.href;

        gaTrack(['_trackEvent', 'Nightly Firstrun Interactions', 'button click', href], function() {
            window.location = href;
        });
    });

    $('main > .blue-box a').on('click', function(e) {
        e.preventDefault();

        var href = this.href;

        gaTrack(['_trackEvent', 'Nightly Firstrun Interactions', 'link click', href], function() {
            window.location = href;
        });
    });
})(window.jQuery);
