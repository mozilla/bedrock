/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

/**
 * User Agent string override for Linux/Firefox/64-bit.
 */
Object.defineProperty(navigator, 'userAgent', {
    value: 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    configurable: true
});

Object.defineProperty(navigator, 'platform', {
    value: 'Linux',
    configurable: true
});
