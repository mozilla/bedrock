/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var utils = Mozilla.Utils;

    if ($('.story-more').length > 0) {
        var person = $('.story-title .name').text();
        var $more = $('.story-more');
        var $moreToggle = $('<div class="more-toggle"><button type="button">' + utils.trans('more') + '</button></div>');
        $moreToggle.insertAfter($more);
        var $toggleButton = $('.more-toggle button');

        $more.hide().attr('aria-hidden', 'true');

        // Show/hide the additional content and track the clicks
        $toggleButton.on('click', function() {
            $more.slideToggle('fast', function() {
                if ($more.is(':visible')) {
                    $toggleButton.addClass('open').text(utils.trans('less'));
                    $(this).attr('aria-hidden', 'false');
                    window.dataLayer.push({
                        'event': 'mozillian-stories-interaction',
                        'browserAction': person + ' - more',
                        'location': 'main'
                    });
                } else {
                    $toggleButton.removeClass('open').text(utils.trans('more'));
                    $(this).attr('aria-hidden', 'true');
                    window.dataLayer.push({
                        'event': 'mozillian-stories-interaction',
                        'browserAction': person + ' - less',
                        'location': 'main'
                    });
                }
            });
        });
    }

})(window.jQuery);
