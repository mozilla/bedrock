/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var exp;

    $('.download-link').each(function(i, link) {
        if (link.href.indexOf('scene=2') > -1) {
            exp = $('#head_content_title').attr('data-experience');

            // specify v=1 template for scene 2
            link.href = link.href.replace('scene=2', 'scene=2&xv=' + exp);
        }
    });
})(window.jQuery);
