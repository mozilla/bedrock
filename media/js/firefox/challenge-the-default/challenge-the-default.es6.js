/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import '@mozilla-protocol/core/protocol/js/details';

const compareSelect = document.querySelector('.mobile-select');
const compareTable = document.querySelector('.comparison-table');

compareSelect.addEventListener('change', function (e) {
    compareTable.dataset.selectedBrowser = e.target.value || 'chrome';
});
