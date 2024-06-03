/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * This script is run in a conditional comment that only IE understands,
 * so all we care about is making sure that window.site.platform === 'windows'
 * for the stub attribution check.
 */
window.site = {
    platform:
        navigator.platform.indexOf('Win32') !== -1 ||
        navigator.platform.indexOf('Win64') !== -1
            ? 'windows'
            : 'other'
};
