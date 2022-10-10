/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* global ga */

(function (i, s, o, g, r, a, m) {
    'use strict';

    i['GoogleAnalyticsObject'] = r;
    (i[r] =
        i[r] ||
        function () {
            (i[r].q = i[r].q || []).push(arguments);
        }),
        (i[r].l = 1 * new Date());
    (a = s.createElement(o)), (m = s.getElementsByTagName(o)[0]);
    a.async = 1;
    a.src = g;
    m.parentNode.insertBefore(a, m);
})(
    window,
    document,
    'script',
    'https://www.google-analytics.com/analytics.js',
    'ga'
);
ga('create', 'UA-370613-9', 'auto');
ga('require', 'displayfeatures');
ga('send', 'pageview');
