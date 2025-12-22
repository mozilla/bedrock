/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    function initToggleableItems() {
        const toggleButtons = document.querySelectorAll('.mzan-toggle');
        const contentDivs = document.querySelectorAll('.mzan-toggle-content');

        // Show first item by default
        if (toggleButtons.length > 0 && contentDivs.length > 0) {
            toggleButtons[0].setAttribute('aria-expanded', 'true');
            contentDivs[0].hidden = false;
        }

        // Add click handlers
        toggleButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                const toggleId = this.getAttribute('data-toggle-id');
                const contentDiv = document.querySelector(
                    '.mzan-toggle-content[data-content-id="' + toggleId + '"]'
                );

                if (contentDiv) {
                    // Hide all content and set all buttons to collapsed
                    contentDivs.forEach(function (div) {
                        div.hidden = true;
                    });
                    toggleButtons.forEach(function (btn) {
                        btn.setAttribute('aria-expanded', 'false');
                    });

                    // Show the clicked toggle's content
                    contentDiv.hidden = false;
                    this.setAttribute('aria-expanded', 'true');
                }
            });
        });
    }

    // Initialize when DOM is ready
    if (document.readyState !== 'loading') {
        initToggleableItems();
    } else {
        document.addEventListener('DOMContentLoaded', initToggleableItems);
    }
})();
