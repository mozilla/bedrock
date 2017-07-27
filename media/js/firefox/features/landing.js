/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    Mozilla.LazyLoad.init();

    // as features roll in and are localized (displayed for some locales, not
    // for others), data-link-positions cannot be set directly in HTML
    $('.features-list').each(function(i, list) {
        var $list = $(list);
        var type = $list.data('feature-type');

        $list.find('.features-list-item').each(function(j, item) {
            // results in something like data-link-position="privacy 2"
            $(item).find('a[data-link-type="link"]').attr('data-link-position', type + ' ' + (j + 1));
        });
    });
})(window.jQuery);
