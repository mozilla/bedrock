/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function(Mozilla) {
    'use strict';
    var sendToPrimary = document.getElementById('s2d-primary');
    // var sendToSecondary = document.getElementById('s2d-secondary');

    // if (sendToPrimary && sendToSecondary) {
    if (sendToPrimary) {
        var formPrimary = new Mozilla.SendToDevice('s2d-primary');
        formPrimary.init();

        // var formSecondary = new Mozilla.SendToDevice('s2d-secondary');
        // formSecondary.init();
    }

})(window.Mozilla);
