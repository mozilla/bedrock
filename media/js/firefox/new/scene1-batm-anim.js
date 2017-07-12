/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var title = $('#main-header-copy');
    var exp = title.data('experience');
    var variant = title.data('variant');

    $('.download-link').each(function(i, link) {
        if (exp && variant && link.href.indexOf('scene=2') > -1) {
            // specify v=1 template for scene 2
            link.href = link.href.replace('scene=2', 'scene=2&xv=' + exp + '&v=' + variant);
        }
    });

    // trigger fade-in CSS animation
    $(function() {
        $('html').addClass('ready');
    });
})(window.jQuery);
