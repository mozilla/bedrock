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

        $promoLarge.on('mousemove', function() {
            var $this = $(this);
            // for slightly less jank css transitions are only triggered
            // when the user is not scrolling
            if (!$promos.hasClass('scroll') && !$this.hasClass('show')) {
                $this.addClass('show');
            }
        });

        $promoLarge.on('mouseleave', function() {
            var $this = $(this);
            if ($this.hasClass('show')) {
                $this.removeClass('show');
            }
        });

        $promoLarge.on('mousedown focus', function(e) {
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
        // There's currently a bug in Safari 7 when using multiple transition-delay times, which causes
        // the occasional flicker when the promos fade in. So for now they don't get the staggered effect.
        var isSafari = navigator.userAgent.indexOf('Safari') !== -1 && navigator.userAgent.indexOf('Chrome') === -1;

        if (isSafari) {
            $promos.addClass('reveal');
        } else {
            // add stagger class to increment transition delay
            $promos.addClass('stagger reveal');
            // remove stagger class once set to reset transition delay
            setTimeout(function () {
                $promos.removeClass('stagger');
            }, 50);
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

    initEllipsis();
    initFacesGrid();
    initPromoHoverOver();

});
