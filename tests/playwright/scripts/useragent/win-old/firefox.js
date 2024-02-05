/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

/**
 * User Agent string override for Windows 8.1/Firefox/64-bit.
 */
Object.defineProperty(navigator, 'userAgent', {
    value: 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    configurable: true
});

Object.defineProperty(navigator, 'platform', {
    value: 'Win64',
    configurable: true
});
