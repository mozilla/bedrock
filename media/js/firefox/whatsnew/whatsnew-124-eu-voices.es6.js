/* eslint-disable no-console */
/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MzpModal from '@mozilla-protocol/core/protocol/js/modal';

(function () {
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
                eLabel: 'Share now'
            });
            // GA4
            window.dataLayer.push({
                event: 'widget_action',
                type: 'modal',
                action: 'open',
                name: 'Share now'
            });
        },
        false
    );
})();

(function () {
    const copyButton = document.getElementById('copy-button');
    const copyButtonText = document.getElementById('share-cta');
    const textCopiedMessage = document.getElementById('text-copied');
    const text = document.getElementById('text-to-copy').innerText;
    let timeout;

    copyButton.addEventListener('click', copyText, false);

    function copyText(e) {
        e.preventDefault();

        clearTimeout(timeout);

        navigator.clipboard.writeText(text);

        textCopiedMessage.style.display = 'block';
        copyButtonText.style.display = 'none';

        timeout = setTimeout(function () {
            textCopiedMessage.style.display = 'none';
            copyButtonText.style.display = 'block';
        }, 2500);
    }
})();
