/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const items = document.querySelectorAll('.m24-c-springboard-item');

for (let i = 0; i < items.length; ++i) {
    const item = items[i];
    const preview = item.querySelector('.m24-c-springboard-link');
    item.classList.add('m24-is-clickable');
    item.addEventListener(
        'click',
        () => {
            preview.click();
        },
        false
    );
}

// when row clicked, pass action through to a href? (to preserve right click functionality?)
