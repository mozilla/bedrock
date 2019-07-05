/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// This relies on base/mozilla-modal.js, included in the firefox_new_scene1 bundle

(function() {
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
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'Current Firefox user downloading Firefox'
        });
    }

    var initFxAccountModal = function() {
        var downloadLinkPrimary = document.querySelectorAll('#download-button-desktop-release .download-list .download-link[data-download-os="Desktop"]');
        var downloadLinkSecondary = document.querySelectorAll('#download-other-platforms-modal .download-list .download-link[data-download-os="Desktop"]');


        for (var j = 0; j < downloadLinkPrimary.length; j++) {
            downloadLinkPrimary[j].addEventListener('click', showFxAModal, false);
        }

        for (var k = 0; k < downloadLinkSecondary.length; k++) {
            downloadLinkSecondary[k].addEventListener('click', showFxAModal, false);
        }

        // Don't trigger the modal for signed in users
        client.getFxaDetails(function(details) {
            if (details.setup) {
                for (var i = 0; i < downloadLinkPrimary.length; i++) {
                    downloadLinkPrimary[i].removeEventListener('click', showFxAModal, false);
                }

                for (var j = 0; j < downloadLinkSecondary.length; j++) {
                    downloadLinkSecondary[j].removeEventListener('click', showFxAModal, false);
                }
            }
        });
    };

    // Only Firefox desktop 57+ (post-quantum) should get the FxA modal
    if (client.isFirefoxDesktop && client._getFirefoxMajorVersion() >= '57') {
        initFxAccountModal();
    }

})();
