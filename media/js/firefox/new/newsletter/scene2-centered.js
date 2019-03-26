/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// This relies on base/mozilla-modal.js, included in the firefox_new_scene1 bundle

(function() {
    'use strict';

    // Listen for the newsletter sucess event
    document.addEventListener('newsletterSuccess', function () {

        // Hide all the things.
        document.querySelector('.content-main .headline').classList.add('hidden');
        document.querySelector('.content-main .tagline').classList.add('hidden');
        document.querySelector('.mzp-c-newsletter-thanks').style = 'display: none';

        // Show the mobile app store button CTA.
        document.querySelector('.mobile-download').classList.remove('hidden');
    }, false);
})();
