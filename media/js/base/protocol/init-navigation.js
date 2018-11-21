/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * Initialize Protocol Navigation.
 */
(function() {
    if (typeof Mzp === 'undefined' || typeof Mzp.Menu === 'undefined' || typeof Mzp.Navigation === 'undefined') {
        return;
    }

    var hasMediaQueries = typeof window.matchMedia !== 'undefined';

    function onImageLoad(e) {
        e.target.removeAttribute('data-src');
        e.target.removeAttribute('data-srcset');
    }

    function handleOnMenuOpen(el) {
        if (!hasMediaQueries || !window.matchMedia('(min-width: 768px)').matches) {
            return;
        }

        var cardImage = el.querySelector('.mzp-c-card-image');

        if (cardImage) {
            var newSrc = cardImage.getAttribute('data-src');

            if (newSrc) {
                var newSrcSet = cardImage.getAttribute('data-srcset');

                if (newSrcSet) {
                    cardImage.srcset = newSrcSet;
                }

                cardImage.src = newSrc;
                cardImage.onload = onImageLoad;
            }

        }
    }

    Mzp.Menu.init({
        onMenuOpen: handleOnMenuOpen
    });

    Mzp.Navigation.init();
})();
