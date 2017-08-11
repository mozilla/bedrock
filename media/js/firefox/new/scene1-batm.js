/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var title = $('#main-header-copy');
    var exp = title.data('experience');
    var variant = title.data('variant');
    var newParams = 'scene=2';

    // conditionally construct new params for download links
    if (exp) {
        newParams += '&xv=' + exp;
    }

    if (variant) {
        newParams += '&v=' + variant;
    }

    $('.download-link').each(function(i, link) {
        link.href = link.href.replace('scene=2', newParams);
    });

    // trigger fade-in CSS animation
    $(function() {
        $('html').addClass('ready');
    });

})(window.jQuery);
