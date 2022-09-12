/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// if the user clicks on c-module-tag, copy link to clipboard

(function () {
    'use strict';

    var linksArray = [];

    document.querySelectorAll('.c-module-tag').forEach(function (occ) {
        linksArray.push(occ);
    });

    linksArray.map(function (e) {
        e.addEventListener('click', function copyLink() {
            var link = e.href;
            navigator.clipboard.writeText(link);
        });
    });
})();
