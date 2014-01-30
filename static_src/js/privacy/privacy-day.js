/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function() {
    'use strict';

    // Hide the download button from Firefox users
    if (isFirefox()) {
        $('#download').hide();
    } else {
        $('#principles').hide();
    }
});
