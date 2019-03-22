/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* eslint no-unused-vars: [2, { "varsIgnorePattern": "stickyNav" }] */

(function($, Mozilla) {
    'use strict';

    var client = Mozilla.Client;
    var $html = $('html');

    // navigation drop-down menu
    function initSubMenu() {
        var $subMenu = $('.submenu-title');
        var $subMenuLinks = $subMenu.find('.submenu > li > a');
        var $subMenuTitle = $subMenu.find('> a');

        $subMenu.on('mouseenter', function() {
            $subMenu.attr('aria-expanded', true);
        });

        $subMenu.on('mouseout', function() {
            $subMenu.attr('aria-expanded', false);
        });

        $subMenuTitle.on('focus', function() {
            $subMenu.attr('aria-expanded', true);
        });

        $subMenuTitle.on('keydown', function(e) {
            // hide the menu if we're shift-tabbing off the title link.
            if (e.which === 9 && e.shiftKey) {
                $subMenu.attr('aria-expanded', false);
            }
        });

        $subMenuLinks.on('keydown', function(e) {
            // only hide the menu if we're on the last link,
            // and the shift key is not used to reverse tab.
            if (e.which === 9 && !e.shiftKey && $(e.target).parent().is('li:last-child')) {
                $subMenu.attr('aria-expanded', false);
            }
        });

        $subMenuTitle.on('click', function(e) {
            e.preventDefault();
        });
    }

    if (client.isFirefox) {
        // iOS
        if (client.isFirefoxiOS) {
            $html.addClass('firefox-up-to-date');

        // Android or desktop
        // bug 1301721 only use major Firefox version until 49.0 is released
        } else {
            $html.addClass(client._isFirefoxUpToDate(false) ? 'firefox-up-to-date' : 'firefox-old');
        }
    } else {
        $html.addClass('non-firefox');
    }

    initSubMenu();

})(window.jQuery, window.Mozilla);
