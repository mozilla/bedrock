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
        var bounding = element.getBoundingClientRect();
        var elementHeight = element.offsetHeight;

        if (
            bounding.top >= -elementHeight &&
            bounding.bottom <=
                (window.innerHeight || document.documentElement.clientHeight) +
                    elementHeight
        ) {
            return true;
        } else {
            return;
        }
    }

    function onLoad() {
        // Check if user prefers reduced motion.
        var matchMediaNoMotion = window.matchMedia(
            '(prefers-reduced-motion: reduce)'
        ).matches;

        var things = document.querySelector('.c-common-things');

        if (matchMediaNoMotion) {
            things.classList.add('hide-gradient');
            return;
        }

        var CommonThings = {};

        CommonThings.gradient = function () {
            var lastitem = document.querySelector('.c-last-item');

            var checkForLastItemOnScroll = debounce(function () {
                // If the last list item is in the viewport, fade out the gradient.
                // Animate it back in when the last item leaves the viewport.
                if (isInViewport(lastitem)) {
                    things.classList.add('hide-gradient');
                } else {
                    things.classList.remove('hide-gradient');
                }
            });

            document.addEventListener(
                'scroll',
                checkForLastItemOnScroll,
                false
            );
        };

        CommonThings.gradient();
    }

    window.Mozilla.run(onLoad);
})(window.Mozilla);
