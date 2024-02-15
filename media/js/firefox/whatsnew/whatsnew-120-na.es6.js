/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MzpModal from '@mozilla-protocol/core/protocol/js/modal';

const qrButton = document.querySelector('.qr-code-btn');
const modalContent = document.querySelector('.mzp-u-modal-content');

// click handler for opening Modal with QR Code

function handleQrCodeModal(e) {
    e.preventDefault();
    MzpModal.createModal(e.target, modalContent, {
        closeText: 'Close Modal'
    });
}

qrButton.addEventListener('click', handleQrCodeModal, false);
