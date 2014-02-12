/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var $mapContainer = $('#map-container');

    var scrollMap = function() {
        setTimeout(function() {
            $mapContainer.animate({
                scrollLeft: '300px'
            }, 250, function() {
                setTimeout(function() {
                    $mapContainer.animate({
                        scrollLeft: '0px'
                    }, 250);
                }, 350);
            });
        }, 500);
    };

    $('.modal-link').on('click', function(e) {
        e.preventDefault();

        var href = $(this).attr('href');

        var $content = $(href);

        var createCallback = ($content.attr('id') === 'map') ? scrollMap : null;

        Mozilla.Modal.createModal(this, $content, {
            title: $content.find('.modal-content-header:first').text(),
            onCreate: createCallback
        });

        gaTrack(['_trackEvent','/mwc/ Interactions','link click', href]);
    });

    // GA tracking on specific links
    $('.ga').on('click', function(e) {
        e.preventDefault();

        var href = this.href;

        var callback = function() {
            window.location = href;
        };

        gaTrack(['_trackEvent','/mwc/ Interactions','link click', href], callback);
    });
})(window.jQuery);
