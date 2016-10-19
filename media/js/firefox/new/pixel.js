/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // pixel status bug https://bugzilla.mozilla.org/show_bug.cgi?id=1311423
    function addPixel() {
        if (!window._dntEnabled()) {
            var $pixel = $('<img />', {
                width: '1',
                height: '1',
                src: 'https://servedby.flashtalking.com/spot/8/6247;40428;4669/?spotName=Mozilla_Download_Conversion'
            });
            $('body').append($pixel);
        }
    }

    addPixel();

})();
