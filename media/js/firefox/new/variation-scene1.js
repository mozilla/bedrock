/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/*
For 'standard' /new variations, this file will append all query params
(most importantly the 'xv' param) to download button links
so the correct template is rendered on /download/thanks/.
*/

(function($) {
    'use strict';

    $('.download-link').each(function(i, link) {
        if (link.href.indexOf('download/thanks/') > -1) {
            link.href = link.href + location.search;
        }
    });
})(window.jQuery);
