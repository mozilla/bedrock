/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    // Init hero image carousel for large viewports only.
    var hasMediaQueries = typeof window.matchMedia !== 'undefined';

    if (!hasMediaQueries || !window.matchMedia('(min-width: 768px)').matches) {
        return;
    }

    var index = 0;
    var heroImage = document.querySelector('.vpn-hero-image');
    setInterval(function () {
        index = (index + 1) % 5;
        heroImage.setAttribute('data-illustration', 'n-' + (index + 1));
    }, 5000);
})();

(function () {
    'use strict';

    function openFaqItem(id) {
        var faq = document.getElementById(id);

        if (
            faq &&
            faq.classList.contains('vpn-faq-item') &&
            !faq.hasAttribute('open')
        ) {
            var summary = faq.querySelector('summary');

            if (summary) {
                summary.click();
            }
        }
    }

    function getHash() {
        var hash = window.location.hash;
        if (hash.indexOf('#') > -1) {
            hash = hash.split('#')[1];
        }

        return hash;
    }

    function handleHashChange() {
        var hash = getHash();

        if (hash) {
            openFaqItem(hash);
        }
    }

    // Open relevant FAQ section is URL contains a hash.
    if (window.location.hash) {
        handleHashChange();
    }

    window.addEventListener('hashchange', handleHashChange, false);
})();
