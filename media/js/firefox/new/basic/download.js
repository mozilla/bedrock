/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var client = window.Mozilla.Client;
    var otherPlatformsLink = document.querySelector('.js-platform-modal-button');
    var otherPlatformsContent = document.querySelector('.other-platforms-content');

    var initOtherPlatformsModal = function() {
        // show the modal cta button
        otherPlatformsLink.classList.remove('hidden');

        otherPlatformsLink.addEventListener('click', function(e) {
            e.preventDefault();

            Mzp.Modal.createModal(this, otherPlatformsContent, {
                title: otherPlatformsLink.textContent,
                className: 'other-platforms-modal'
            });

            window.dataLayer.push({
                'event': 'in-page-interaction',
                'eAction': 'link click',
                'eLabel': 'Download Firefox for another platform'
            });
        }, false);
    };

    /**
     * Enable modal to optionally download Firefox for other platforms.
     * Don't show the modal for iOS or Android.
     */
    if (otherPlatformsLink && client.isDesktop) {
        initOtherPlatformsModal();
    }

})();
