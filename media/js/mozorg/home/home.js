/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    var $promos = $('.promo-grid');
    var $promoItems = $('.promo-grid .item');

    function initFirefoxDownloadPromo() {
        var $downloadPromo = $('.firefox-download');

        $downloadPromo.on('mouseenter focusin', function () {
            $downloadPromo.addClass('show');
        });

        $downloadPromo.on('mouseleave focusout', function () {
            $downloadPromo.removeClass('show');
        });

        // show download button small links
        $('.firefox-download .download-other-desktop').show();
    }

    initFirefoxDownloadPromo();

    function initPromoHoverOver() {
        var $promoLarge = $('.promo-large-landscape, .promo-large-portrait');
        var scrollTimeout;
        var gaTimeout;

        $promoLarge.on('mousemove', function() {
            var $this = $(this);
            // for slightly less jank css transitions are only triggered
            // when the user is not scrolling
            if (!$promos.hasClass('scroll') && !$this.hasClass('show')) {
                $this.addClass('show');

                // only track a GA hover event once the mouse cursor
                // rests over a promo for over half a second
                clearTimeout(gaTimeout);
                gaTimeout = setTimeout(function () {
                    // TODO console.log('GA Track');
                }, 600);
            }
        });

        $promoLarge.on('mouseleave', function() {
            var $this = $(this);
            if ($this.hasClass('show')) {
                $this.removeClass('show');
            }
        });

        $promoLarge.on('click focus', function(e) {
            var $this = $(this);
            if (!$this.hasClass('show')) {
                e.preventDefault();
                $this.addClass('show');
            }
        });

        // when the inner link loses focus, hide the secondary content again
        // assumes a single link in the panel
        $('.promo-large-landscape > a, .promo-large-portrait > a').on('blur', function() {
            var $this = $(this);
            if ($this.parent().hasClass('show')) {
                $this.parent().removeClass('show');
            }
        });

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

    function initFacesGrid() {
        // add stagger class to increment transition delay
        $promos.addClass('stagger');
        // show each promo
        $promoItems.addClass('reveal');
        // remove stagger class once set to reset transition delay
        setTimeout(function () {
            $promos.removeClass('stagger');
        }, 50);
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
            $tweet.addClass('ellipsis');
        }
    }

    initEllipsis();
    initFacesGrid();
    initPromoHoverOver();

});
