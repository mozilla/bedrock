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

        // Helper function to swap icon between regular and white version
        function updateToggleIcon(toggle, isSelected) {
            const iconElement = toggle.querySelector('.mzan-icon');
            if (!iconElement) return;

            // Get all classes from the icon element
            const classes = Array.from(iconElement.classList);

            // Find the icon class (starts with 'icon-')
            const iconClass = classes.find(function (cls) {
                return cls.startsWith('icon-') && cls !== 'icon';
            });

            if (!iconClass) return;

            if (isSelected) {
                // Switch to white version if not already
                if (!iconClass.endsWith('-white')) {
                    iconElement.classList.remove(iconClass);
                    iconElement.classList.add(iconClass + '-white');
                }
            } else {
                // Switch to regular version
                if (iconClass.endsWith('-white')) {
                    const regularIcon = iconClass.replace(/-white$/, '');
                    iconElement.classList.remove(iconClass);
                    iconElement.classList.add(regularIcon);
                }
            }
        }

        // Show first item by default
        if (toggleButtons.length > 0 && contentDivs.length > 0) {
            toggleButtons[0].setAttribute('aria-expanded', 'true');
            toggleButtons[0].classList.add('is-selected');
            updateToggleIcon(toggleButtons[0], true);
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
                        btn.classList.remove('is-selected');
                        updateToggleIcon(btn, false);
                    });

                    // Show the clicked toggle's content
                    contentDiv.hidden = false;
                    this.setAttribute('aria-expanded', 'true');
                    this.classList.add('is-selected');
                    updateToggleIcon(this, true);
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
