/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    let url = window.location.href;
    let hash;
    let redirect;
    let urlParts;

    // strip hash from URL (if present)
    if (url.indexOf('#') > -1) {
        urlParts = url.split('#');
        url = urlParts[0];
        hash = urlParts[1];
    }

    if (url.indexOf('xv=windows') > -1) {
        return;
    } else {
        redirect = url + (url.indexOf('?') > -1 ? '&' : '?') + 'xv=windows';

        // re-insert hash (if originally present)
        if (hash) {
            redirect += '#' + hash;
        }
    }

    if (
        redirect &&
        window.site.platform === 'windows' &&
        window.site.platformVersion <= 6.3 // Windows 8.1 and lower
    ) {
        window.location.href = redirect;
    } else {
        return;
    }
})();
