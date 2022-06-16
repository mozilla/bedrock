/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    var client = window.Mozilla.Client;
    var joinFirefoxContent = document.querySelector('.join-firefox-content');

    function showFxAModal(e) {
        e.preventDefault();

        // Open the modal
        Mzp.Modal.createModal(this, joinFirefoxContent, {
            title: e.target.textContent,
            className: 'join-firefox-modal'
        });

        // Count the click in GA
        window.dataLayer.push({
            event: 'in-page-interaction',
            eAction: 'link click',
            eLabel: 'Current Firefox user downloading Firefox'
        });
    }

    var initFxAccountModal = function () {
        var downloadLinkPrimary = document.querySelectorAll(
            '.main-download .c-button-download-thanks > .download-link'
        );
        for (var i = 0; i < downloadLinkPrimary.length; i++) {
            downloadLinkPrimary[i].addEventListener(
                'click',
                showFxAModal,
                false
            );

            // If we're opening a modal on click, prevent Glean from
            // delaying & redirecting the click (issue 11770)
            downloadLinkPrimary[i].classList.remove('js-glean-delay-click');
        }

        // Don't trigger the modal for signed in users
        client.getFxaDetails(function (details) {
            if (details.setup) {
                for (var i = 0; i < downloadLinkPrimary.length; i++) {
                    downloadLinkPrimary[i].removeEventListener(
                        'click',
                        showFxAModal,
                        false
                    );

                    // add back click delay for Glean (issue 11770)
                    downloadLinkPrimary[i].classList.add(
                        'js-glean-delay-click'
                    );
                }
            }
        });
    };

    // Only Firefox desktop 57+ (post-quantum) should get the FxA modal
    if (client.isFirefoxDesktop && client._getFirefoxMajorVersion() >= '57') {
        initFxAccountModal();
    }
})();
