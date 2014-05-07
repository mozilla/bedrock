/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var $tipPrev = $('#tip-prev');
    var $tipNext = $('#tip-next');
    var $tipsNavDirect = $('#tips-nav-direct');

    // mozilla pager stuff must be in doc ready wrapper
    $(function() {
        var pager = Mozilla.Pager.rootPagers[0];

        // updates nav links based on current page index
        var updateNavLinks = function() {
            // update direct nav links
            $tipsNavDirect.find('a').removeClass('selected');
            $tipsNavDirect.find('a[href="#' + pager.currentPage.id + '"]').addClass('selected');

            // update next/prev links
            if (pager.currentPage.index === 0) {
                $tipPrev.addClass('inactive');
                $tipNext.removeClass('inactive');
            } else if (pager.currentPage.index === (pager.pages.length - 1)) {
                $tipNext.addClass('inactive');
                $tipPrev.removeClass('inactive');
            } else {
                $tipNext.removeClass('inactive');
                $tipPrev.removeClass('inactive');
            }
        };

        // update nav links based on page visible on load (using URL hash)
        updateNavLinks();

        // handle top nav clicks
        $tipsNavDirect.on('click', 'a', function(e) {
            e.preventDefault();

            var $this = $(this);

            var selectedPageId = $this.attr('href').replace(/#/, '');
            var selectedPageIndex;

            // loop through all pages, find page with matching id
            for (var i = 0; i < pager.pages.length; i++) {
                if (pager.pages[i].id === selectedPageId) {
                    selectedPageIndex = i;

                    break;
                }
            }

            // set page with animation
            pager.setPageWithAnimation(pager.pages[selectedPageIndex]);

            updateNavLinks();
        });

        // handle next/prev nav clicks
        $('#tips-nav-prev-next').on('click', 'a', function(e) {
            e.preventDefault();

            var $this = $(this);

            if (!$this.hasClass('inactive')) {
                if ($this.prop('id') === 'tip-prev') {
                    pager.prevPageWithAnimation();
                } else {
                    pager.nextPageWithAnimation();
                }

                updateNavLinks();
            }
        });
    });
})(window.jQuery);
