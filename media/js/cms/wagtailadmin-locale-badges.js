/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

!(function () {
    'use strict';
    document.addEventListener('DOMContentLoaded', function () {
        var e = document.getElementById('locales-list');
        if (e) {
            var t = window.WAGTAIL_LOCALE_ALIAS_MAP || {};
            Object.entries(t).forEach(function (t) {
                var n = t[0],
                    a = t[1],
                    s = e.querySelector('a[href$="/locales/edit/' + n + '/"]');
                if (s) {
                    var c = document.createElement('span');
                    (c.className = 'w-status w-status--label'),
                        (c.textContent = 'alias → ' + a),
                        s.insertAdjacentElement('afterend', c);
                }
            });
        }
    });
})();
