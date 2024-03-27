/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const copyButton = document.getElementById('copy-button');
const copyButtonText = document.getElementById('share-cta');
const textCopiedMessage = document.getElementById('text-copied');
const text = document.getElementById('text-to-copy').innerText;
let timeout;

copyButton.addEventListener('click', copyText);

function copyText() {
    clearTimeout(timeout);

    navigator.clipboard.writeText(text);

    textCopiedMessage.style.display = 'block';
    copyButtonText.style.display = 'none';

    timeout = setTimeout(function () {
        textCopiedMessage.style.display = 'none';
        copyButtonText.style.display = 'block';
    }, 2500);

    // UA
    window.dataLayer.push({
        event: 'in-page-interaction',
        eAction: 'copy',
        eLabel: 'Copy and share'
    });

    // GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'copy',
        action: 'copy',
        name: 'Copy and share'
    });
}
