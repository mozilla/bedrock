/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    $('a.video-play').attr('role', 'button').on('click', function(e) {
        e.preventDefault();

        var $this = $(this);

        Mozilla.Modal.createModal(this, $this.next(), {
            title: $this.attr('data-title'),
            onCreate: function() {
                playVideo();
            }
        });
    });

    var playVideo = function() {
        // give the modal a chance to open before playing
        setTimeout(function() {
            $('#modal video:first')[0].play();
        }, 400);
    };

})(window.jQuery);
