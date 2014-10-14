/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    var $promos = $('.promo-grid');
    var $promoLarge = $('.promo-large-landscape, .promo-large-portrait');
    var $downloadPromo = $('.promo-small-landscape.firefox-download');
    var hasTouch = 'ontouchstart' in window || navigator.msMaxTouchPoints || navigator.maxTouchPoints;

    function initFirefoxDownloadPromo() {
        // show download button small links
        $downloadPromo.find('.download-other-desktop').show();
    }

    /*
     * For non-touch devices promos are transitioned on hover
     */
    function initPromoHover() {
        var scrollTimeout;

        function showCurrentHover() {
            var $this = $(this);
            if (!$promos.hasClass('scroll') && !$this.hasClass('show')) {
                $this.addClass('show');
            }
        }

        function showCurrent() {
            var $this = $(this);
            if (!$this.hasClass('show')) {
                $this.addClass('show');
            }
        }

        function hideCurrent() {
            var $this = $(this);
            if ($this.hasClass('show')) {
                $this.removeClass('show');
            }
        }

        $promoLarge.on('mousemove', showCurrentHover);
        $promoLarge.on('mouseleave', hideCurrent);
        $promoLarge.on('focus', showCurrent);

        // when the inner link loses focus, hide the secondary content again
        // assumes a single link in the panel
        $('.promo-large-landscape > a, .promo-large-portrait > a').on('blur', function() {
            var $this = $(this).parent();
            if ($this.hasClass('show')) {
                $this.removeClass('show');
            }
        });

        $downloadPromo.on('mouseenter focusin', showCurrent);
        $downloadPromo.on('mouseleave focusout', hideCurrent);

        // don't animate hover transitions on large promos
        // while the user is scrolling
        $(window).on('scroll', function() {
            clearTimeout(scrollTimeout);
            if (!$promos.hasClass('scroll')) {
                $promos.addClass('scroll');
            }

            scrollTimeout = setTimeout(function () {
                $promos.removeClass('scroll');
            }, 200);
        });
    }

    /*
     * For touch devices promos are transitioned on click
     */
    function initPromoTouch() {
        var showTimeout;

        function hideLargePromo() {
            var $this = $promos.find('.promo-large-landscape.show-touch, .promo-large-portrait.show-touch');
            var $primary;
            var $secondary;

            if ($this.length > 0) {
                $primary = $this.find('.primary');
                $secondary = $this.find('.secondary');

                setTimeout(function() {
                    $this.find('a.panel-link').css('visibility', 'hidden');
                    $secondary.removeClass('fadein');
                    $secondary.css('visibility', 'hidden');
                    $primary.css('visibility', 'visible');
                    $primary.removeClass('fadeout');
                    $this.removeClass('show-touch');
                }, 300);
            }
        }

        function hideFirefoxDownloadPromo() {
            if ($downloadPromo.hasClass('show-touch')) {
                $downloadPromo.find('.secondary').removeClass('fadein');

                setTimeout(function() {
                    $downloadPromo.find('.secondary').css('visibility', 'hidden');
                    $downloadPromo.find('.primary').removeClass('out');
                    $downloadPromo.removeClass('show-touch');
                }, 300);
            }
        }

        $promoLarge.on('click focus', function(e) {

            var $this = $(this);
            var $primary;
            var $secondary;

            if (!$this.hasClass('show-touch')) {
                e.preventDefault();

                $primary = $this.find('.primary');
                $secondary = $this.find('.secondary');

                //hide any previous promo
                hideLargePromo();
                hideFirefoxDownloadPromo();

                clearTimeout(showTimeout);
                $this.addClass('show-touch');
                $primary.addClass('fadeout');
                $this.find('a.panel-link').css('visibility', 'visible');

                showTimeout = setTimeout(function() {
                    $primary.css('visibility', 'hidden');
                    $secondary.css('visibility', 'visible');
                    $secondary.addClass('fadein');
                }, 300);
            }
        });

        $('.promo-large-landscape > a, .promo-large-portrait > a').on('blur', function() {
            var $this = $(this).parent();
            if ($this.hasClass('show-touch')) {
                hideLargePromo();
            }
        });

        $downloadPromo.on('click focus', function(e) {
            var $primary;
            var $secondary;

            if (!$downloadPromo.hasClass('show-touch')) {
                e.preventDefault();

                $primary = $downloadPromo.find('.primary');
                $secondary = $downloadPromo.find('.secondary');

                // hide any previous promo
                hideLargePromo();

                clearTimeout(showTimeout);
                $downloadPromo.addClass('show-touch');
                $primary.addClass('out');

                showTimeout = setTimeout(function() {
                    $secondary.css('visibility', 'visible').addClass('fadein');
                }, 300);
            }
        });
    }

    function initFacesGrid() {
        // There's currently a bug in Safari 7 when using multiple transition-delay times, which causes
        // the occasional flicker when the promos fade in. So for now they don't get the staggered effect :(
        var isSafari = navigator.userAgent.indexOf('Safari') !== -1 && navigator.userAgent.indexOf('Chrome') === -1;

        if (isSafari) {
            $promos.addClass('reveal');
        } else {
            // add stagger class to increment transition delay
            $promos.addClass('stagger reveal');
        }
    }

    function initEllipsis() {
        // if textoverflows on tweet promo, add an ellipsis.
        var $tweet = $('#twt-body');
        if ($tweet.length > 0 && ($tweet[0].scrollHeight > $tweet.innerHeight())) {
            // because the tweet contains inline html,
            // we are just adding an ellipsis pseudo element
            // at the bottom right of the container
            // if text overflows as opposed to truncating
            // the tweet content
            $tweet.find('.ellipsis').show();
        }
    }

    initFirefoxDownloadPromo();
    initEllipsis();
    initFacesGrid();

    // for touch devices we assume clicks/taps for promo interaction
    if (hasTouch) {
        $promos.addClass('has-touch');
        initPromoTouch();
    } else {
        // for non-touch devices we use hover
        initPromoHover();
    }
});
