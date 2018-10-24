/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * Initialize Protocol language switcher.
 */
(function() {
    if (typeof Mozilla === 'undefined' || typeof Mozilla.Menu === 'undefined' || typeof Mozilla.Navigation === 'undefined') {
        return;
    }

    if (!Mozilla.Menu.isSupported()) {
        return;
    }

    var _mqWideNav = window.matchMedia('(min-width: 768px)');

    function onImageLoad(e) {
        e.target.removeAttribute('data-src');
        e.target.removeAttribute('data-srcset');
    }

    function handleOnMenuOpen(el) {
        if (!_mqWideNav.matches) {
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

    Mozilla.Menu.init({
        onMenuOpen: handleOnMenuOpen
    });

    Mozilla.Navigation.init();
})();
