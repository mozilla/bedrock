/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;$(function () {
    'use strict';

    // If Firefox is the latest version and not mobile,
    // hide the out-of-date messaging and show up-to-date
    if (isFirefox() && !isMobile() && isFirefoxUpToDate()) {
        $('#out-of-date').hide();
        $('#up-to-date').show();
    }
});
