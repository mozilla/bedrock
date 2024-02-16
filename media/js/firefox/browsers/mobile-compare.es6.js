/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import SendToDevice from '../../base/send-to-device.es6';

const s2dFooter = document.getElementById('s2d-footer');

if (s2dFooter) {
    const form = new SendToDevice('s2d-footer');
    form.init();
}
