/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, KonamiCode) {
    'use strict';

    var $document = $(document);
    var $body = $('body');
    var $kzp = $('#kzp');

    new KonamiCode(function() {
        $kzp.removeClass('gone').addClass('visible');
        $body.addClass('easter');
        setTimeout(function() {
            endEgg();
        }, 150);
    });

    function endEgg() {
        $document.bind('keyup click', function(e) {
            if (!$(e.target).is('#kzkid')) {
                $kzp.removeClass('visible');

                setTimeout(function() {
                    $kzp.addClass('gone');
                    $body.removeClass('easter');
                    $document.unbind('keyup click');
                }, 150);
            }
        });
    }

})(window.jQuery, window.KonamiCode);
