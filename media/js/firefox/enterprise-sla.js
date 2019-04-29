/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

window.Mzp.Details.init('.mzp-c-article .mzp-c-details > h3');

(function() {
    'use strict';

    var sidebarLinks = document.querySelectorAll('#sidebar-menu a[href^="#"]');

    for (var i = 0; i < sidebarLinks.length; i++) {
        sidebarLinks[i].addEventListener('click', function() {
            // Extract the target element's ID from the link's href.
            var target = this.getAttribute('href').replace( /.*?(#.*)/g, '$1' );

            if (document.querySelector(target + ' > .is-summary > button[aria-expanded=false]')) {
                document.querySelector(target + ' > .is-summary > button[aria-expanded=false]').click();
            }
        });
    }

    // Open a section on pageload if URL has a fragment identifier
    if (window.location.hash) {
        var target = document.querySelector(window.location.hash + ' > .is-summary > button[aria-expanded=false]');

        if (target) {
            target.click();
        }
    }

})();
