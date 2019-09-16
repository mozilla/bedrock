/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';

    var urlParams = new window._SearchParams().utmParams();

    // Track external UTM referrals for Firefox Accounts related CTAs.
    Mozilla.UtmUrl.init(urlParams);
})();
