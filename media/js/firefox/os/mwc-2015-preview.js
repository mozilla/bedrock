/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    $('.modal-link').attr('data-track', 'true').on('click', function(e) {
        e.preventDefault();

        var href = $(this).attr('href');

        var $content = $(href);

        var createCallback;

        if (typeof(window.scrollMwcMap) === 'function') {
            createCallback = ($content.attr('id') === 'map') ? window.scrollMwcMap : null;
        }

        Mozilla.Modal.createModal(this, $content, {
            title: $content.find('.modal-content-header:first').text(),
            onCreate: createCallback
        });
    });

    // GA tracking on specific links
    $('.ga').attr('data-track', 'true');

    // trigger modal on page load if hash is present
    switch (window.location.hash) {
    case '#map':
        $('#map-link').trigger('click');
        break;
    case '#schedule':
        $('#schedule-link').trigger('click');
        break;
    }
})(window.jQuery);
