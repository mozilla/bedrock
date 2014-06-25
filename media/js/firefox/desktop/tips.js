/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Hammer) {
    'use strict';

    var $html = $('html');
    var $window = $(window);
    var $tipPrev = $('#tip-prev');
    var $tipNext = $('#tip-next');
    var $tipsNavDirect = $('#tips-nav-direct');
    var $tipsTabLinks = $tipsNavDirect.find('a');
    var $tipsNavDots = $('#tips-nav-dots');

    // only show download button for users on desktop platforms, using either a non-Firefox browser
    // or an out of date version of Firefox
    if ((window.isFirefox() && window.isFirefoxUpToDate()) || $html.hasClass('android') || $html.hasClass('ios') || $html.hasClass('fxos')) {
        $('#footer').addClass('hide-download');
    }

    // mozilla pager stuff must be in doc ready wrapper
    $(function() {
        // GA tracking on page load
        // Google doesn't recognize hash by default
        var currentURL = window.location.protocol + '//' + window.location.host + window.location.pathname + window.location.hash;
        gaTrack(['_trackEvent','/desktop/tips/ Interactions','page load', currentURL, 0, true]);

        var pager = Mozilla.Pager.pagers[0];

        // sets the current pager tab based on the url hash
        function setCurrentPage (noAnim) {
            var currentHash = window.location.hash.replace(/#/, '') + '-tip';
            var page = pager.pages[0];

            if (pager.currentPage.id === currentHash) {
                // if hashchange has fired from a click, do nothing
                return;
            }

            if (window.location.hash !== '') {
                // loop through all pages, find page with matching id
                for (var i = 0; i < pager.pages.length; i++) {
                    if (pager.pages[i].id === currentHash) {
                        page = pager.pages[i];
                        break;
                    }
                }
            }

            if (noAnim) {
                pager.setPage(page);
            } else {
                pager.setPageWithAnimation(page);
            }
        }

        // set the initial page content
        setCurrentPage(true);
        $('#page-content').css('visibility', 'visible');

        // updates nav links based on current page index
        var updateNavLinks = function() {
            var current = pager.currentPage.id.replace('-tip', '');

            // update direct nav links
            $tipsTabLinks.removeClass('selected').attr('aria-selected', 'false');
            $tipsNavDirect.find('a[href="#' + current + '"]').addClass('selected').attr('aria-selected', 'true');

            // update next/prev links
            if (pager.currentPage.index === 0) {
                $tipPrev.prop('disabled', true);
                $tipNext.prop('disabled', false);
            } else if (pager.currentPage.index === (pager.pages.length - 1)) {
                $tipNext.prop('disabled', true);
                $tipPrev.prop('disabled', false);
            } else {
                $tipNext.prop('disabled', false);
                $tipPrev.prop('disabled', false);
            }

            // update dots (visible on mobile only)
            $tipsNavDots.find('span').removeClass('active');
            $tipsNavDots.find('span[data-tip="' + current + '"]').addClass('active');
        };

        // update nav links based on page visible on load (using URL hash)
        updateNavLinks();

        // handle hash change events
        function onHashChange () {
            setCurrentPage();
            updateNavLinks();
        }

        // listen for hash changes
        $window.on('hashchange', onHashChange);

        // handle top nav clicks
        $tipsNavDirect.on('click', 'a', function(e) {
            e.preventDefault();

            var $this = $(this);

            var selectedPageId = $this.attr('href').replace('#', '') + '-tip';
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

            window.location.hash = $this.attr('href').replace('#', '');

            // GA tracking
            gaTrack(['_trackEvent', '/desktop/tips/ Interactions', 'tab clicks to', $this.attr('href')]);
        });

        // handle next/prev nav clicks
        $('#tips-nav-prev-next').on('click', 'button', function(e) {
            e.preventDefault();

            var $this = $(this);
            var isPrev = $this.prop('id') === 'tip-prev';

            if (!$this.is(':disabled')) {
                if (isPrev) {
                    pager.prevPageWithAnimation();
                } else {
                    pager.nextPageWithAnimation();
                }

                window.location.hash = pager.currentPage.id.replace('-tip', '');

                // GA tracking
                var gaAction = (isPrev) ? 'prev link to' : 'next link to';
                gaTrack(['_trackEvent', '/desktop/tips/ Interactions', gaAction, '#' + pager.currentPage.id]);
            }
        });

        // handle swipe
        new Hammer($('#tips-wrapper')[0], {
            swipeVelocityX: 0.4
        }).on('swipeleft swiperight', function(e) {
            e.gesture.preventDefault();

            if (e.gesture.direction === 'right' && pager.currentPage.index > 0) {
                pager.prevPageWithAnimation();
            } else if (e.gesture.direction === 'left' && pager.currentPage.index < (pager.pages.length - 1)) {
                pager.nextPageWithAnimation();
            }

            window.location.hash = pager.currentPage.id.replace('-tip', '');
        });

        // GA tracking
        $('.share-button').on('click', function() {
            // determine position
            var pos = ($(this).closest('.share-wrapper').prop('id') === 'share-nav-wrapper') ? 'top' : 'bottom';

            gaTrack(['_trackEvent','/desktop/tips/ Interactions','Social Share', 'share drop-down ' + pos]);
        });

        $('a[rel="external"]').on('click', function(e) {
            e.preventDefault();

            var href = this.href;

            gaTrack(['_trackEvent', '/desktop/tips/ Interactions', 'outbound link', href], function() {
                window.location = href;
            });
        });

        $('#footer-download .download-link').on('click', function(e) {
            e.preventDefault();

            var href = this.href;

            gaTrack(['_trackEvent', 'Firefox Downloads', 'download click', 'Firefox for Desktop'], function() {
                window.location = href;
            });
        });
    });
})(window.jQuery, window.Hammer);
