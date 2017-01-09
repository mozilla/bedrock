/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $document = $(document);

    // Scroll smoothly to the linked section
    $document.on('click', '.head-pagenav a[href^="#"]', function(e) {
        e.preventDefault();
        // Extract the target element's ID from the link's href.
        var elem = $(this).attr('href').replace(/.*?(#.*)/g, '$1');
        var offset = $(elem).offset().top;

        Mozilla.smoothScroll({
            top: offset
        });
    });

})(window.jQuery);
