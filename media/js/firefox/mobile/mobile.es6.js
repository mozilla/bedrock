/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import SendToDevice from '../../base/send-to-device.es6';

const sendToPrimary = document.getElementById('s2d-primary');
const sendToSecondary = document.getElementById('s2d-primary');

if (sendToPrimary && sendToSecondary) {
    const formPrimary = new SendToDevice('s2d-primary');
    formPrimary.init();

    const formSecondary = new SendToDevice('s2d-secondary');
    formSecondary.init();
}
