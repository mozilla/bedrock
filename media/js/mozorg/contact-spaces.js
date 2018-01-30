/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var utils = Mozilla.Utils;
    var $page = $('#entry-container');
    var $nav = $('.nav-category');

    function initPhotoGallery() {
        // init photo galleries using event delegation
        $('.page-content').magnificPopup({
            delegate: '.gallery-list a',
            gallery: { enabled: true },
            type: 'image'
        });
    }

    // Create select form inputs for primary mobile navigation
    function initMobileNav() {
        var $label = $('<label for="nav-category-select">' + utils.trans('navLabel') + '</label>');
        var $select = $('<select id="nav-category-select" class="nav-category-select">');
        var $default = $('<option value="" disabled selected>-- ' + utils.trans('navLabel') + ' --</option>');

        $default.prependTo($select);

        $nav.find('li').each(function() {
            var $li = $(this);
            var $a = $li.find('> a');
            var $p = $li.parents('li');
            var prefix = new Array($p.length + 1).join('-');
            var option = $('<option>').text(prefix + ' ' + $a.text());
            var pathName = $a[0].pathname;

            // IE will omit a leading slash when using pathname. Yay standards!
            pathName = pathName.substr(0, 1) !== '/' ? '/' + pathName : pathName;

            option.val(pathName);
            option.appendTo($select);
        });

        $select.prependTo($page);
        $label.prependTo($page);

        // Set the selected item for the current page
        setSelectedMobileNavItem();
        bindMobileNavChange();
    }

    function setSelectedMobileNavItem() {
        $('.nav-category-select option[value="' + window.location.pathname + '"]').prop('selected', 'selected');
    }

    function bindMobileNavChange() {
        $('.nav-category-select').on('change', function() {
            window.location.href = window.location.protocol + '//' + window.location.host + this.value;
        });
    }

    if ($nav.length) {
        initMobileNav();
    }

    initPhotoGallery();

})(jQuery);
