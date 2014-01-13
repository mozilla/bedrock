/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    "use strict";

    var mozMap = {

        /*
         * Sets the initial active tab and nav items on page load
         * using the id and data-tab attribute of the entry section element
         */
        setInitialPageNavState: function () {
            var $entry = $('#entry-container .entry');
            var tab = $entry.data('tab');
            var id = $entry.attr('id');

            // set the current tab navigation item
            $('ul.category-tabs li[data-id="' + tab + '"]').addClass('current');

            // set the current list menu navigation item
            $('.nav-category li[data-id="' + id + '"]').addClass('current');

            // hide the community sub menu's
            $('.accordion .submenu').hide();

            // show the correct menu navigation
            mozMap.toggleNav(tab);

            // show the correct community sub menu
            mozMap.toggleCommunitySubMenu();
        },

        /*
         * Toggles the active tab nav menu visibility
         */
        toggleNav: function (tab) {
            if (tab === 'spaces') {
                $('#nav-communities, #meta-communities').hide();
                $('#nav-spaces, #meta-spaces').show();
            } else if (tab === 'communities') {
                $('#nav-spaces, #meta-spaces').hide();
                $('#nav-communities, #meta-communities').show();
            }
        },

        /*
         * Toggles the active community submenu nav
         */
        toggleCommunitySubMenu: function () {
            var $current = $('#nav-communities li.current');
            var $parent = $current.parent();

            // if current item has a sub-menu which isn't open
            if ($current.hasClass('hasmenu') && !$current.hasClass('open')) {
                $('.accordion .submenu:visible').hide().parent().removeClass('open');
                $current.addClass('open');
                $current.find('.submenu').show();
            }

            // if current item is within a sub-menu and it's parent is not open
            if ($parent.hasClass('submenu') && !$parent.is(':visible')) {
                $('.accordion .submenu:visible').hide().parent().removeClass('open');
                $parent.show().parent().addClass('open');
            }
        }
    };

    mozMap.setInitialPageNavState();

})(jQuery);
