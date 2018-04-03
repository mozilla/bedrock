/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    $('.download-link').each(function(i, link) {
        if (link.href.indexOf('download/thanks/') > -1) {
            // add funnelcake param
            link.href = link.href + '?f=135';
        }
    });
})(window.jQuery);

