/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var mobileButtons = document.querySelectorAll('.js-mobile');
    var mobileModal = document.getElementById('modal-download-firefox');
    var focusButtons = document.querySelectorAll('.js-focus');
    var focusModal = document.getElementById('modal-download-focus');

    for(var i = 0; i < mobileButtons.length; i++) {
        mobileButtons[i].addEventListener('click', function() {
            Mzp.Modal.createModal(this, mobileModal);
        });
    }

    for(var j = 0; j < focusButtons.length; j++) {
        focusButtons[j].addEventListener('click', function() {
            Mzp.Modal.createModal(this, focusModal);
        });
    }

    // initialize send to device widget
    var form = new Mozilla.SendToDevice();
    form.init();

})();
