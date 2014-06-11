/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    // Customize global setting.
    Mozilla.Pager.AUTO_ROTATE_INTERVAL = 4000;

    var pager3;

    $('#pager3-enable').on('click', function() {
        if (!pager3) {
            pager3 = new Mozilla.Pager($('#pager-example3'));
        }
    });

    $('#pager3-disable').on('click', function() {
        if (pager3) {
            Mozilla.Pager.destroyPagerById(pager3.id);
            pager3 = null;
        }
    });

    // Bind custom next/previous buttons inside document ready
    // to ensure pager is initialized.
    $(function() {
        var pager4 = Mozilla.Pager.findPagerById('pager-example4');

        $('#next').on('click', function() {
            pager4.nextPageWithAnimation();
        });

        $('#prev').on('click', function() {
            pager4.prevPageWithAnimation();
        });
    });
})(window.jQuery);
