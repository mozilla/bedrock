/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

/**
 * User Agent string override for Linux/Chrome/64-bit.
 */
Object.defineProperty(navigator, 'userAgent', {
    value: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.3',
    configurable: true
});

Object.defineProperty(navigator, 'userAgentData', {
    value: {
        getHighEntropyValues: () => {
            return Promise.resolve({
                architecture: 'x64',
                bitness: '64',
                platform: 'Linux',
                platformVersion: ''
            });
        }
    }
});

Object.defineProperty(navigator, 'platform', {
    value: 'Linux',
    configurable: true
});
