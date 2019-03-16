/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';

    // Show email newsletter modal on download button click.
    var downloadButton = document.querySelectorAll('.download-link[data-download-os="Desktop"]');
    var newsletterContent = document.getElementById('pre-download-modal');

    for(var i = 0; i < downloadButton.length; i++) {
        downloadButton[i].setAttribute('role', 'button');
        downloadButton[i].addEventListener('click', function(e) {
            e.preventDefault();

            Mzp.Modal.createModal(e.target, newsletterContent, {
                title: 'Download Firefox and sign up',
                className: 'mzp-t-firefox l-compact',
                closeText: window.Mozilla.Utils.trans('global-close'),
            });
        }, false);
    }

    // Listen for the newsletter sucess event
    document.addEventListener('newsletterSuccess', function () {
        // Close the modal
        Mzp.Modal.closeModal();

        // Redirect to /download/thanks/
        window.location.href = document.querySelector('.pre-download-continue a').href;
    }, false);
})();
