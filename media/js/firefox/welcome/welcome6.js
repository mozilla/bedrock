/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

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
            Mzp.Modal.createModal(e.target, content, {
                closeText: window.Mozilla.Utils.trans('global-close')
            });

            window.dataLayer.push({
                event: 'in-page-interaction',
                eAction: 'link click',
                eLabel: 'Get Firefox for mobile'
            });
        },
        false
    );

    // initialize send to device widget
    const form = new Mozilla.SendToDevice();
    form.init();
})(window.Mozilla);
