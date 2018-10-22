/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    // Show email newsletter modal on download button click.
    document.getElementById('pre-download-button').addEventListener('click', function(e) {
        e.preventDefault();

        Mozilla.Modal.createModal(this, $('.pre-download-newsletter'));
    }, false);

    // Listen for the regular newsletter form submit response.
    $(document).ajaxSuccess(function(evt, xhr, settings, response) {
        // Check that it's the correct form and the response was a non-error.
        if ((settings.url.indexOf('/newsletter/') > -1) && response.success) {

            // Hide the regular newsletter title and description.
            document.querySelector('.pre-download-newsletter-title').classList.add('hidden');
            document.querySelector('.pre-download-newsletter-desc').classList.add('hidden');

            // Pause for 2 seconds (?) to read the confirmation message before preceeding to download.
            setTimeout(function() {
                window.location.href = document.querySelector('.pre-download-continue a').href;
            }, 2000);
        }
    });

    window.dataLayer.push({
        'data-ex-name': 'email_form_first',
        'data-ex-variant': document.querySelector('.pre-download-button-container').getAttribute('data-variant-name')
    });

})(window.Mozilla);

