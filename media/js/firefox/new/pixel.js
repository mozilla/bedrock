/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // pixel status bug https://bugzilla.mozilla.org/show_bug.cgi?id=1311423
    function addPixel() {
        if (!window._dntEnabled()) {
            var href = $('#strings').data('trackingPixel');

            if (href) {
                var $pixel = $('<img />', {
                    width: '1',
                    height: '1',
                    src: href
                });
                $('body').append($pixel);
            }
        }
    }

    addPixel();

})();
