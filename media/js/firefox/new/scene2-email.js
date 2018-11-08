/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var content = document.querySelector('.mzp-u-modal-content');
    var trigger = document.querySelector('.email-privacy-link');
    var title = document.querySelector('.email-privacy h3');

    trigger.addEventListener('click', function(e) {
        e.preventDefault();
        Mzp.Modal.createModal(e.target, content, {
            title: title.innerHTML,
            className: 'mzp-t-firefox',
            closeText: window.Mozilla.Utils.trans('global-close'),
        });

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'How will Mozilla use my email?'
        });
    }, false);

})();
