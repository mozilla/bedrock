/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    var openText = document
        .getElementById('strings')
        .getAttribute('data-details-open-text');
    var closeText = document
        .getElementById('strings')
        .getAttribute('data-details-close-text');
    var buttons;

    window.MzpDetails.init(
        '.format-headings .privacy-body section section > h3'
    );
    window.MzpDetails.init('.format-paragraphs .summary');

    // Add "Learn more" / "Show less" text.
    if (openText && closeText) {
        buttons = document.querySelectorAll('.is-summary button');

        for (var i = 0; i < buttons.length; i++) {
            buttons[i].setAttribute('data-open', openText);
            buttons[i].setAttribute('data-close', closeText);
        }
    }

    function openPrivacyItem(id) {
        var item = document.getElementById(id);

        // Pages such as /privacy/firefox/ use 'is-details', whilst other pages like /privacy/websites/ use 'is-summary'.
        // This is likely due to how the privacy notice markdown file is structured.
        if (
            item &&
            (item.classList.contains('is-details') ||
                item.classList.contains('is-summary'))
        ) {
            var button = item.querySelector('button');

            // Only expand the section if it is hidden.
            if (button && button.getAttribute('aria-expanded') !== true) {
                button.click();
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
            openPrivacyItem(hash);
        }
    }

    // Open relevant Privacy section is URL contains a matching hash.
    if (window.location.hash) {
        handleHashChange();
    }

    window.addEventListener('hashchange', handleHashChange, false);
})();
