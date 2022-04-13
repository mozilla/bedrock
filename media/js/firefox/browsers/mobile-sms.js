/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function (Mozilla) {
    'use strict';

    var sendToDevice = document.getElementById('s2d-sms');

    if (sendToDevice) {
        var form = new Mozilla.SendToDevice('s2d-sms');
        form.init();
    }
})(window.Mozilla);
