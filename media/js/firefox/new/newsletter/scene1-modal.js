/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    var client = window.Mozilla.Client;

    function initNewsletterModal() {
        // Show email newsletter modal on download button click.
        var downloadButton = document.querySelectorAll('.download-button .download-list .download-link[data-download-os="Desktop"]');

        for(var i = 0; i < downloadButton.length; i++) {
            downloadButton[i].setAttribute('role', 'button');
            downloadButton[i].addEventListener('click', function(e) {
                e.preventDefault();

                Mozilla.Modal.createModal(this, $('.pre-download-newsletter'));

            }, false);
        }

        // Listen for the regular newsletter form submit response.
        $(document).ajaxSuccess(function(evt, xhr, settings, response) {
            // Check that it's the correct form and the response was a non-error.
            if ((settings.url.indexOf('/newsletter/') > -1) && response.success) {

                // Close the modal
                Mozilla.Modal.closeModal();

                // Redirect to /download/thanks/
                window.location.href = downloadButton[0].href + '?xv=pre-dl&v=c&s=t';
            }
        });
    }

    // Only show newsletter modal if not Firefox desktop.
    if (!client.isFirefoxDesktop) {
        initNewsletterModal();
    }

})(window.Mozilla);
