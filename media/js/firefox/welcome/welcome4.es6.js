/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import SendToDevice from '../../base/send-to-device.es6';

const sendTo = document.getElementById('send-to-device');

if (sendTo) {
    const form = new SendToDevice();
    form.init();
}
