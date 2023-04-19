/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrackBeginCheckout from './datalayer-begincheckout.es6';

(function () {
    const buttons = document.querySelectorAll('.ga-begin-checkout');
    for (let i = 0; i < buttons.length; ++i) {
        buttons[i].addEventListener('click', function (event) {
            TrackBeginCheckout.handleLinkWithItemData(event);
        });
    }
})();
