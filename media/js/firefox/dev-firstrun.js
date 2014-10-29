/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    $('a.video-play').attr('role', 'button').click(function(e) {
        e.preventDefault();

        var $this = $(this);

        Mozilla.Modal.createModal(this, $this.nextAll('.video'), {
            // grab the nearby h4 tag as the modal window title
            title: $this.siblings('h4,h2').text(),
            onCreate: function() {
                $("#modal").fitVids();
            }
        });
    });

})(window.jQuery, window.Mozilla);
