/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';

    var downloadButton = document.querySelector('.main-download .download-button .download-list .download-link[data-download-os="Desktop"]');

    // Listen for the regular newsletter form submit response.
    $(document).ajaxSuccess(function(evt, xhr, settings, response) {
        // Check that it's the correct form and the response was a non-error.
        if ((settings.url.indexOf('/newsletter/') > -1) && response.success) {

            document.getElementById('newsletter-form-thankyou').style.visibility = 'hidden';
            document.querySelector('.main-download .download-button-wrapper').style.visibility = 'hidden';

            // Redirect to /download/thanks/
            if (downloadButton) {
                window.location.href = downloadButton.href + '&s=t';
            }
        }
    });

})();
