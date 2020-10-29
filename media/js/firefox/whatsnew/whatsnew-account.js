/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function(Mozilla) {
    'use strict';

    var sendTo = document.getElementById('send-to-device');

    if (sendTo) {
        var form = new Mozilla.SendToDevice();
        form.init();
    }
})(window.Mozilla);
