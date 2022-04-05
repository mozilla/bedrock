/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */
(function () {
    'use strict';

    // https://davidwalsh.name/javascript-debounce-function
    function debounce(func, wait, immediate) {
        var timeout;
        return function () {
            var context = this,
                args = arguments;
            var later = function () {
                timeout = null;
                if (!immediate) {
                    func.apply(context, args);
                }
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) {
                func.apply(context, args);
            }
        };
    }

    function isInViewport(element) {
        // Calculate on each scroll if the footer is in the view port.
        var elementTop = element.offsetTop;
        var elementBottom = elementTop + element.offsetHeight;
        var viewportTop = window.scrollY || window.pageYOffset;
        var viewportBottom = viewportTop + window.screen.height;

        return elementBottom > viewportTop && elementTop < viewportBottom;
    }

    function onLoad() {
        // Check if promo exists on the page, or if smaller than tablet, or if user prefers reduced motion.
        var matchMediaNoMotion = window.matchMedia(
            '(prefers-reduced-motion: reduce)'
        ).matches;
        var matchMediaDesktop = window.matchMedia('(min-width: 768px)').matches;
        var promo = document.querySelector('.mzp-c-sticky-promo');

        if (!promo || !matchMediaDesktop || matchMediaNoMotion) {
            return;
        }

        // If the user is on Firefox and is NOT supposed to see sticky promo.
        var fxUser = document.documentElement.classList.contains('is-firefox');
        var hideFromFxUser = promo.classList.contains('hide-from-fx-user');

        if (fxUser && hideFromFxUser) {
            return;
        }

        var StickyPromo = {};
        var STICKY_PROMO_COOKIE_ID = 'firefox-sticky-promo';

        StickyPromo.bindEvents = function () {
            promo.addEventListener(
                'animationend',
                function () {
                    promo.classList.add('is-displayed');
                },
                false
            );
        };

        StickyPromo.hasCookie = function () {
            return Mozilla.Cookies.hasItem(STICKY_PROMO_COOKIE_ID);
        };

        StickyPromo.setCookie = function () {
            var date = new Date();
            var cookieDuration = 1 * 24 * 60 * 60 * 1000; // 1 day expiration
            date.setTime(date.getTime() + cookieDuration); // 1 day expiration
            Mozilla.Cookies.setItem(
                STICKY_PROMO_COOKIE_ID,
                true,
                date.toUTCString(),
                '/',
                undefined,
                false,
                'lax'
            );
        };

        StickyPromo.show = function () {
            function openOnScroll() {
                // Open promo
                Mzp.StickyPromo.open();
                document.removeEventListener('scroll', openOnScroll, false);
            }

            document.addEventListener('scroll', openOnScroll, false);

            var checkForFooterOnScroll = debounce(function () {
                // If the footer is in the viewport, fade out the promo.
                // Animate it back in when the footer leaves the viewport
                // if the user did not dismiss it.
                if (isInViewport(footer)) {
                    promo.classList.remove('mzp-a-slide-in');
                    promo.classList.add('mzp-a-fade-out');
                } else if (!promo.classList.contains('user-dismiss')) {
                    promo.classList.remove('mzp-a-fade-out');
                    promo.classList.add('mzp-a-slide-in');
                }
            }, 100);

            // Add modifier class to the footer to make sure the language selection drop-down is not obscured by the sticky promo
            var footer = document.querySelector('.mzp-c-footer');
            if (footer) {
                document.addEventListener(
                    'scroll',
                    checkForFooterOnScroll,
                    false
                );
            }

            // Set Close Button event
            var stickyBtnClose = document.querySelector(
                '.mzp-c-sticky-promo-close'
            );

            stickyBtnClose.addEventListener('click', function () {
                StickyPromo.setCookie(STICKY_PROMO_COOKIE_ID);
                promo.classList.add('user-dismiss');
            });
        };

        // Check on page load
        var cookiesEnabled =
            typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();

        if (cookiesEnabled && !StickyPromo.hasCookie()) {
            StickyPromo.bindEvents();
            StickyPromo.show();
        }
    }

    window.Mozilla.run(onLoad);
})(window.Mozilla);
