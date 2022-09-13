/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import SendToDevice from '../../base/send-to-device.es6';

const s2dHero = document.getElementById('s2d-hero');

if (s2dHero) {
    const form = new SendToDevice('s2d-hero');
    form.init();
}
