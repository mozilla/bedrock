/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * Initialize Protocol Navigation.
 */
(function() {
    'use strict';

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

    function initFxAButton() {
        if (typeof Mozilla.Client === 'undefined') {
            return false;
        }

        var nav = document.querySelector('.mzp-c-navigation');
        var fxaButton = document.querySelector('.mzp-c-navigation .c-navigation-fxa-cta');

        // User should be on Firefox desktop, nav should be present on page, and the FxA button should exist.
        if (!Mozilla.Client.isFirefoxDesktop || !nav || !fxaButton) {
            return false;
        }

        // Button is hidden from most locales for now so make sure it exists before we mess with it.
        if (fxaButton) {
            var fxaButtonAltHref = fxaButton.getAttribute('data-alt-href');

            // Update the button if user is signed in
            Mozilla.Client.getFxaDetails(function(details) {
                if (details.setup) {
                    nav.classList.add('fxa-signed-in');
                    fxaButton.href = fxaButtonAltHref;
                }
            });
        }
    }

    initFxAButton();

    Mzp.Menu.init({
        onMenuOpen: handleOnMenuOpen
    });

    Mzp.Navigation.init();
})();
