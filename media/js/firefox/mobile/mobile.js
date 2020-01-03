/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var modal = document.getElementById('modal');
    var mobileButtons = document.querySelectorAll('.js-mobile');
    var mobileContent = document.getElementById('modal-download-firefox');

    for(var i = 0; i < mobileButtons.length; i++) {
        mobileButtons[i].addEventListener('click', function() {
            mobileContent.style.display = 'block';
            Mzp.Modal.createModal(this, modal, {
                closeText: window.Mozilla.Utils.trans('global-close'),
                onDestroy: function() {
                    mobileContent.style.display = 'none';
                }
            });
        });
    }

    // initialize send to device widget
    var form = new Mozilla.SendToDevice();
    form.init();

})();
