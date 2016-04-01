/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {
    'use strict';

    if ($('#nav-main').length === 0) {
        return;
    }

    var mainMenuItems = $('#nav-main [tabindex="0"]');
    var prevItem;
    var newItem;
    var focusedItem;

    $('#nav-main > .has-submenus > li').bind('mouseover focusin', function() {
        newItem = $(this);

        if (!prevItem || prevItem.attr('id') !== newItem.attr('id')) {
            // Open the menu
            newItem.addClass('hover').find('[aria-expanded="false"]').attr('aria-expanded', 'true');
            if (prevItem) {
                // Close the last selected menu
                prevItem.dequeue();
            }
        } else {
            prevItem.clearQueue();
        }
    }).bind('mouseout focusout', function() {
        prevItem = $(this);
        prevItem.delay(100).queue(function() {
            if (prevItem) {
                prevItem.clearQueue();
                // Close the menu
                prevItem.removeClass('hover').find('[aria-expanded="true"]').attr('aria-expanded', 'false');
                prevItem = null;
                if (focusedItem) {
                    focusedItem.get(0).blur();
                }
            }
        });
    }).each(function(menuIdx) {
        var menuitems = $(this).find('a');

        menuitems.mouseover(function() {
            this.focus(); // Sometimes $(this).focus() doesn"t work
        }).focus(function() {
            focusedItem = $(this);
        }).each(function(itemIdx) {
            // Enable keyboard navigation
            $(this).keydown(function(event) {
                var target;
                if(event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) {
                    return true;
                }
                switch (event.keyCode) {
                case 33: // Page Up
                case 36: // Home
                    target = menuitems.first();
                    break;
                case 34: // Page Down
                case 35: // End
                    target = menuitems.last();
                    break;
                case 38: // Up
                    target = (itemIdx > 0) ? menuitems.eq(itemIdx - 1) : menuitems.last();
                    break;
                case 40: // Down
                    target = (itemIdx < menuitems.length - 1) ? menuitems.eq(itemIdx + 1) : menuitems.first();
                    break;
                case 37: // Left
                    target = (menuIdx > 0) ? mainMenuItems.eq(menuIdx - 1) : mainMenuItems.last();
                    break;
                case 39: // Right
                    target = (menuIdx < mainMenuItems.length - 1) ? mainMenuItems.eq(menuIdx + 1) : mainMenuItems.first();
                    break;
                }
                if (target) {
                    target.get(0).focus(); // Sometimes target.focus() doesn't work
                    return false;
                }
                return true;
            });
        });
    });

    // With JavaScript enabled, we can provide a full navigation with #nav-main.
    // Now "hide" the duplicated #footer-menu from AT.
    $('#footer-menu').attr('role', 'presentation');

});
