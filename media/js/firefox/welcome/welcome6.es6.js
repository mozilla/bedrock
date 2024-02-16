/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MzpModal from '@mozilla-protocol/core/protocol/js/modal';
import SendToDevice from '../../base/send-to-device.es6';

// used for testing purposes only.
if (window.location.search.indexOf('default=true') !== -1) {
    document.querySelector('body').classList.add('is-firefox-default');
}

Mozilla.UITour.getConfiguration('appinfo', (details) => {
    if (details.defaultBrowser) {
        document.querySelector('body').classList.add('is-firefox-default');
    }
});

// modal
const content = document.querySelector('.mzp-u-modal-content');
const trigger = document.querySelector('.js-modal-link');

trigger.addEventListener(
    'click',
    (e) => {
        e.preventDefault();
        MzpModal.createModal(e.target, content, {
            closeText: window.Mozilla.Utils.trans('global-close')
        });

        // UA
        window.dataLayer.push({
            event: 'in-page-interaction',
            eAction: 'link click',
            eLabel: 'Get Firefox for mobile'
        });
        // GA4
        window.dataLayer.push({
            event: 'widget_action',
            type: 'modal',
            action: 'open',
            name: 'Get Firefox for mobile'
        });
    },
    false
);

// initialize send to device widget
const form = new SendToDevice();
form.init();
