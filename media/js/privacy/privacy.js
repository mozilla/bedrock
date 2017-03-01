/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function() {
    'use strict';

    var utils = Mozilla.Utils;

    /**
     * Detects whether do not track is enabled and takes one of two possible actions:
     * 1. If an element with the id #dnt-enabled exists it will
     * 1.1 if positive, set the element text to the positive message text below
     * 1.2 if negative, set the element text to the negative message text and, change
     *     the class of the element to button insensitive instead of the default of button
     * 2. If an element with the id #dnt-enabled does not exist, the function will simply
     *    either return true or false.
     */
    function setDoNotTrackStatus() {
        var enabled = window.navigator.doNotTrack === 'yes';
        var dntEnabledButton = document.getElementById('dnt-enabled');
        var msgText = enabled ? document.createTextNode('Do Not Track Is On »') : document.createTextNode('Do Not Track Is Off »');

        if (enabled) {
            if (dntEnabledButton) {
                dntEnabledButton.appendChild(msgText);
            } else {
                return true;
            }
        } else {
            if (dntEnabledButton) {
                dntEnabledButton.appendChild(msgText);
                dntEnabledButton.setAttribute('class', 'button insensitive');
            } else {
                return false;
            }
        }
    }

    setDoNotTrackStatus();

    var panelOpenText = utils.trans('tabpanel-open-text');
    var panelCloseText = utils.trans('tabpanel-close-text');

    // Accordion widgets in the highlight box
    $('#main-content .accordion').each(function(accordionIndex) {
        $(this).attr({
            'role': 'tablist',
            'aria-multiselectable': 'true'
        }).find('[role="tab"]').each(function(tabIndex) {
            var expanded = false;
            var id = this.id || $(this).parent().attr('id')
                             || 'accordion-' + accordionIndex + '-tab-' + tabIndex;
            var $tab = $(this);
            var $panel = $('#' + $(this).attr('aria-controls'));
            var $anchor = $('<a href="#" role="button">' + panelOpenText + '</a>');

            if (!$panel.length) {
                $panel = $tab.next('[role="tabpanel"]').attr('id', id + '-tabpanel');
            }

            // Still cannot find the tabpanel, stop adding tweaks
            if (!$panel.length) {
                $tab.removeAttr('role');
                return;
            }

            $tab.attr({
                'tabindex': '-1',
                'aria-controls': id + '-tabpanel',
                'aria-expaned': 'false'
            });

            $panel.attr({
                'tabindex': '-1',
                'aria-hidden': 'true'
            });

            $tab.on('click', function (event) {
                event.preventDefault();
                expanded = !expanded;
                $tab.attr('aria-expaned', expanded);
                $panel.attr('aria-hidden', !expanded);
                $anchor.text((expanded) ? panelCloseText : panelOpenText);
            });

            $anchor.on('click', function (event) {
                event.preventDefault();
            }).appendTo(($tab.find(':last-child').length) ? $tab.find(':last-child') : $tab);
        });
    });

    // Support location hashes, including the following Firefox in-product
    // links: #health-report, #telemetry and #crash-reporter
    $(window).on('load hashchange', function () {
        if (location.hash && $(location.hash).length) {
            var $tabpanel = $(location.hash).parents('[role="tabpanel"]');

            if ($tabpanel.length) {
                var $tab = $('[aria-controls="' + $tabpanel.attr('id') + '"]');

                if ($tab && $tab.attr('aria-expaned') === 'false') {
                    $tab.click(); // Expand accordion
                    $(location.hash).get(0).scrollIntoView();
                }
            }
        }
    });
});
