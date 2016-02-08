/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
     'use strict';

    var $tooltipTrigger = $('.tooltip-trigger');
    var $currentItem = {};
    var $tooltip = {};

    $tooltipTrigger.on('mouseenter', function() {
        $currentItem = $(this).parents('li');
        $tooltip = $('.tooltip', $currentItem);

        $tooltip.removeClass('hidden')
                .attr('aria-hidden', false);
    });

    $tooltipTrigger.on('mouseleave', function() {
        $currentItem = $(this).parents('li');
        $tooltip = $('.tooltip', $currentItem);

        $tooltip.addClass('hidden')
                .attr('aria-hidden', true);
    });

    /**
     * Sends data to GA about the interaction steps a user has taken.
     * @param {string} interaction - The kind of interaction
     * @param {int} variation - Whether it is a v1 or v2 task.
     */
    function trackInteraction(interaction, variation) {
        window.dataLayer.push({
            event: 'get-involved-task-selection',
            interaction: interaction,
            variation: variation
        });
    }

    $('.simple, .challenging').on('click', 'a', function() {
        trackInteraction(this.dataset['task'], this.dataset['variant']);
    });

})();
