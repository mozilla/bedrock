/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    var $mainNav;

    //generic links
    $mainNav = $('#nav-main-menu li a');
    $mainNav.attr({
        'data-element-location': 'nav click',
        'data-link-type': $mainNav.data('name')
    });

    // track download firefox promo clicks
    $('.promo-small-landscape.firefox-download a.download-link').each(function() {
        var $this = $(this);
        var $promo = $this.closest('.promo-small-landscape');
        var isAndroid = $promo.find('li.os_android:visible').length > 0;
        var type = isAndroid ? 'Firefox Android' : 'Firefox Desktop';
        var tilePosition = $promo.prop('id');
        var tileSize = 'promo-small-landscape';

        $this.attr({
            'data-interaction': 'download click - top',
            'data-download-version': type,
            'data-tile-position': tilePosition,
            'data-tile-size': tileSize
        });
    });

    // track Firefox download section button clicks
    $('#firefox-download-section a.download-link').each(function() {
        var platform;
        var $this = $(this);
        if ($this.parents('li').hasClass('os_android')) {
            platform = 'Firefox Android';
        } else {
            platform = 'Firefox Desktop';
        }
        $this.attr({
            'data-interaction': 'download click - primary',
            'data-download-version': platform
        });

    });

});
