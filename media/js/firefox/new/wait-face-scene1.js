/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var extraParams = location.search.replace(/^\?/, '&');

    $('.download-link').each(function(i, link) {
        if (link.href.indexOf('scene=2') > -1) {
            link.href = link.href.replace('scene=2', 'scene=2' + extraParams);
        }
    });
})(window.jQuery);
