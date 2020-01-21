/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    Mozilla.UITour.getConfiguration('appinfo', function(details) {
        if (details.defaultBrowser) {
            document.querySelector('body').classList.add('is-firefox-default');
        }
    });

    // modal
    var content = document.querySelector('.mzp-u-modal-content');
    var trigger = document.querySelector('.js-modal-link');

    trigger.addEventListener('click', function(e) {
        e.preventDefault();
        Mzp.Modal.createModal(this, content, {
            closeText: window.Mozilla.Utils.trans('global-close'),
        });

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'Get Firefox for mobile'
        });
    }, false);

    // initialize send to device widget
    var form = new Mozilla.SendToDevice();
    form.init();

})(window.Mozilla);
