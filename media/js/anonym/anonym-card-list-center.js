/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    const programmaticScrollEls = new WeakSet();

    function centerCardLists() {
        const cardLists = document.querySelectorAll('.mzan-cards');

        cardLists.forEach(function (cardsEl) {
            const listEl = cardsEl.querySelector(
                '.mzan-card-list.scroll-on-mobile'
            );
            if (
                cardsEl.dataset.mzanUserScrolled === 'true' ||
                !listEl ||
                cardsEl.scrollWidth <= cardsEl.clientWidth
            ) {
                return;
            }

            const cardsRect = cardsEl.getBoundingClientRect();
            const viewportCenterX = document.documentElement.clientWidth / 2;
            const listWidth = listEl.scrollWidth;
            const listOffsetWithinScroller = listEl.offsetLeft;
            const viewportCenterWithinScroller =
                viewportCenterX - cardsRect.left;
            const targetLeft =
                listOffsetWithinScroller +
                listWidth / 2 -
                viewportCenterWithinScroller;
            const maxLeft = cardsEl.scrollWidth - cardsEl.clientWidth;
            const nextLeft = Math.max(0, Math.min(maxLeft, targetLeft));
            const prevBehavior = cardsEl.style.scrollBehavior;
            cardsEl.style.scrollBehavior = 'auto';
            programmaticScrollEls.add(cardsEl);
            cardsEl.scrollLeft = nextLeft;
            window.setTimeout(function () {
                programmaticScrollEls.delete(cardsEl);
            }, 0);
            cardsEl.style.scrollBehavior = prevBehavior;
        });
    }

    function init() {
        window.requestAnimationFrame(centerCardLists);
        window.addEventListener(
            'load',
            function () {
                centerCardLists();
            },
            { once: true }
        );
        let resizeTimer = null;
        window.addEventListener('resize', function () {
            window.clearTimeout(resizeTimer);
            resizeTimer = window.setTimeout(centerCardLists, 150);
        });
        document.querySelectorAll('.mzan-cards').forEach(function (cardsEl) {
            cardsEl.addEventListener('scroll', function () {
                if (programmaticScrollEls.has(cardsEl)) {
                    return;
                }
                cardsEl.dataset.mzanUserScrolled = 'true';
            });
        });
    }

    if (document.readyState !== 'loading') {
        init();
    } else {
        document.addEventListener('DOMContentLoaded', init);
    }
})();
