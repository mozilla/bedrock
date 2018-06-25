/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    Mozilla.Client.getFxaDetails(function(details) {
        Mozilla.WNP61.init(details);
    });
})(window.Mozilla);
