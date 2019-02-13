/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// This relies on base/mozilla-modal.js, included in the firefox_new_scene1 bundle

(function($) {
    'use strict';

    var client = window.Mozilla.Client;
    var $downloadButton = $('#download-button-desktop-release .download-link[data-download-os="Desktop"]');
    var $downloadAnyway = $('#download-fxa-modal .download-link[data-download-os="Desktop"]');

    var initFxAccountModal = function() {
        // To avoid showing users two similar forms back to back,
        // hide the form on the /thanks page by adding a param to
        // download links in the modal.
        $downloadAnyway.attr('href', function(i, h) {
            return h + (h.indexOf('?') !== -1 ? '&n=f' : '?n=f');
        });

        $downloadButton.on('click', function(e) {
            e.preventDefault();

            // Open the modal
            Mozilla.Modal.createModal(this, $('#firefox-account'), {
                title: $(this).text(),
                className: 'firefox-account-modal'
            });

            // Count the click in GA
            window.dataLayer.push({
                'event': 'in-page-interaction',
                'eAction': 'link click',
                'eLabel': 'Current Firefox user downloading Firefox'
            });
        });

        // Don't trigger the modal for signed in users
        client.getFxaDetails(function(details) {
            if (details.setup) {
                $downloadButton.unbind('click');
            }
        });
    };

    // Only Firefox desktop 57+ (post-quantum) should get the FxA modal
    if (client.isFirefoxDesktop && client._getFirefoxMajorVersion() >= '57') {
        initFxAccountModal();
    }

})(window.jQuery);
