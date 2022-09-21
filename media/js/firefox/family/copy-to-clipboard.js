/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// if the user clicks on c-module-tag, copy link to clipboard

(function () {
    'use strict';

    var linksArray = [];
    var timeout;

    document.querySelectorAll('.c-module-tag').forEach(function (occ) {
        linksArray.push(occ);
    });

    linksArray.map(function (e) {
        e.addEventListener('click', function copyLink(event) {
            event.preventDefault();

            var sectionLink = event.target.offsetParent;

            var link = sectionLink.href;
            var copiedText = sectionLink.children[2];
            var copyText = sectionLink.children[1];

            navigator.clipboard.writeText(link);

            copiedText.style.display = 'block';
            copyText.style.display = 'none';

            clearTimeout(timeout);

            timeout = setTimeout(function () {
                copiedText.style.display = 'none';
                copyText.style.display = 'block';
            }, 2000);
        });
    });
})();
