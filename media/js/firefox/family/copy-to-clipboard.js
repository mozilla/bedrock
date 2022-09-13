/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// if the user clicks on c-module-tag, copy link to clipboard

(function () {
    'use strict';

    // var copyText = document.querySelector('.c-module-copy');
    // var copiedText = document.querySelector('.c-module-copied');

    var linksArray = [];

    document.querySelectorAll('.c-module-tag').forEach(function (occ) {
        linksArray.push(occ);
    });

    linksArray.map(function (e) {
        e.addEventListener('click', function copyLink() {
            var link = e.href;
            var copiedText = e.children[2];
            var copyText = e.children[1];

            navigator.clipboard.writeText(link);

            copiedText.style.display = 'block';
            copyText.style.display = 'none';
            setTimeout(function () {
                copiedText.style.display = 'none';
                copyText.style.display = 'block';
            }, 2000);
        });
    });
})();
