/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var $tipPrev = $('#tip-prev');
    var $tipNext = $('#tip-next');

    // mozilla pager stuff must be in doc ready wrapper
    $(function() {
        var pager = Mozilla.Pager.rootPagers[0];

        // update next/prev links based on page visible on load (using URL hash)
        if (pager.currentPage.index === 0) {
            $tipPrev.addClass('inactive');
        } else if (pager.currentPage.index === (pager.pages.length - 1)) {
            $tipNext.addClass('inactive');
        }

        $tipPrev.on('click', function(e) {
            e.preventDefault();

            if (!$tipPrev.hasClass('inactive')) {
                $tipNext.removeClass('inactive');

                // if current page is second in list, de-activate
                // previous link
                if (pager.currentPage.index === 1) {
                    $tipPrev.addClass('inactive');
                }

                pager.prevPageWithAnimation();
            }
        });

        $tipNext.on('click', function(e) {
            e.preventDefault();

            if (!$tipNext.hasClass('inactive')) {
                $tipPrev.removeClass('inactive');

                // if current page is next to last in list, de-activate
                // next link
                if (pager.currentPage.index === (pager.pages.length - 2)) {
                    $tipNext.addClass('inactive');
                }

                pager.nextPageWithAnimation();
            }
        });
    });
})(window.jQuery);
