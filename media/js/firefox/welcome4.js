/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function(Mozilla) {
    'use strict';

    var content = document.querySelector('.mzp-u-modal-content');
    var buttons = document.getElementsByClassName('js-modal-link');
    var sendTo = document.getElementById('send-to-device');

    for (var i = 0, len = buttons.length; i < len; i++) {
        var button = buttons[i];
        button.addEventListener('click', openModal);
        button.setAttribute('aria-role', 'button');
    }

    if (sendTo) {
        var form = new Mozilla.SendToDevice();
        form.init();
    }

    function openModal(e) {
        e.preventDefault();

        Mzp.Modal.createModal(e.target, content, {
            closeText: window.Mozilla.Utils.trans('global-close')
        });
    }

})(window.Mozilla);
