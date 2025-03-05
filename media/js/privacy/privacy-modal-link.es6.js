/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function preventNewTabAction(e) {
    const href = e.target.href;
    // Detect keyboard shortcuts, auxiliary mouse buttons.
    if (href && (e.ctrlKey || e.metaKey || e.shiftKey || e.button === 1)) {
        e.preventDefault();

        // Force the navigation to open in the same tab.
        window.location.href = href;
    }
}

document.querySelectorAll('a').forEach((link) => {
    // Prevent links being opened in a new tab.
    link.addEventListener('click', preventNewTabAction);

    // Prevent context menu from opening with right click.
    link.addEventListener('contextmenu', (e) => {
        e.preventDefault();
    });
});
