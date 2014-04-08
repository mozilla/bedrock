/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/*global $:true, isDoNotTrackEnabled:true */
$(function() {
    "use strict";

    // Detects whether do not track is enabled and takes one of two possible actions:
    // 1. If an element with the id #dnt-enabled exists it will
    // 1.1 if positive, set the element text to the positive message text below
    // 1.2 if negative, set the element text to the negative message text and, change
    //     the class of the element to button insensitive instead of the default of button
    // 2. If an element with the id #dnt-enabled does not exist, the function will simply
    //    either return true or false.
    function setDoNotTrackStatus() {
        var enabled = window.navigator.doNotTrack === "yes",
        dntEnabledButton = document.getElementById("dnt-enabled"),
        msgText = enabled ? document.createTextNode("Do Not Track Is On »") : document.createTextNode("Do Not Track Is Off »");

        if(enabled) {
            if(dntEnabledButton) {
                dntEnabledButton.appendChild(msgText);
            } else {
                return true;
            }
        } else {
            if(dntEnabledButton) {
                dntEnabledButton.appendChild(msgText);
                dntEnabledButton.setAttribute("class", "button insensitive");
            } else {
                return false;
            }
        }
    }

    setDoNotTrackStatus();

    var panel_open_text = window.trans('tabpanel-open-text');
    var panel_close_text = window.trans('tabpanel-close-text');

    // Accordion widgets in the highlight box
    $('#main-content .accordion').each(function() {
        $(this).attr({
          'role': 'tablist',
          'aria-multiselectable': 'true'
        }).find('[role="tab"]').each(function() {
            var expanded = false;
            var id = this.id || $(this).parent().attr('id');
            var $tab = $(this).attr({
              'tabindex': '-1',
              'aria-controls': id + '-tabpanel',
              'aria-expaned': 'false'
            });
            var $panel = $('#' + $(this).attr('aria-controls'));
            var $anchor = $('<a href="#" role="button">' + panel_open_text + '</a>');

            if (!$panel.length) {
              $panel = $tab.next('[role="tabpanel"]').attr('id', id + '-tabpanel');
            }

            $panel.attr({
              'tabindex': '-1',
              'aria-hidden': 'true'
            });

            $tab.on('click', function (event) {
                event.preventDefault();
                expanded = !expanded;
                $tab.attr('aria-expaned', expanded);
                $panel.attr('aria-hidden', !expanded);
                $anchor.text((expanded) ? panel_close_text : panel_open_text);
            });

            $anchor.on('click', function (event) {
                event.preventDefault();
            }).appendTo(($tab.find(':last-child').length) ? $tab.find(':last-child') : $tab);
        });
    });
});
