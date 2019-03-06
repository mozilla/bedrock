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

    var nav = document.querySelector('.mzp-c-navigation');
    var fxaButton = document.querySelector('.mzp-c-navigation .c-navigation-fxa-cta');

    if (fxaButton) {
        var fxaButtonAltHref = fxaButton.getAttribute('data-alt-href');
    }

    function showFxAButton() {
        nav.classList.add('show-fxa-button');
    }

    function meetsRequirements() {
        if (typeof Mozilla.Client === 'undefined') {
            return false;
        }

        // User should be on Firefox desktop, nav should be present on page, and the FxA button should exist.
        if (!Mozilla.Client.isFirefoxDesktop || !nav || !fxaButton) {
            return false;
        }

        var userMajorVersion = Mozilla.Client._getFirefoxMajorVersion();
        var latestMajorVersion = parseInt(document.documentElement.getAttribute('data-latest-firefox'), 10);

        if (!userMajorVersion || !latestMajorVersion) {
            return false;
        }

        // User should be on Firefox Quantum or greater.
        return userMajorVersion >= 57;
    }

    function updateFxAButton() {
        fxaButton.href = fxaButtonAltHref;
    }

    // If all other requirements are met, check the account state
    if (meetsRequirements()) {
        $(function() {
            // Update the button if they're signed in
            Mozilla.Client.getFxaDetails(function(details) {
                if (details.setup) {
                    updateFxAButton();
                }
            });
        });
    }

    function initFxAButton() {
        if (meetsRequirements()) {
            showFxAButton();
        }
    }

    initFxAButton();

    Mzp.Menu.init({
        onMenuOpen: handleOnMenuOpen
    });

    Mzp.Navigation.init();
})();
