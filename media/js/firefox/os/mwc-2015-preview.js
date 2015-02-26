/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    $('.modal-link').on('click', function(e) {
        e.preventDefault();

        var href = $(this).attr('href');

        var $content = $(href);

        var create_callback;

        if (typeof(window.scrollMwcMap) === 'function') {
          create_callback = ($content.attr('id') === 'map') ? window.scrollMwcMap : null;
        }

        Mozilla.Modal.createModal(this, $content, {
            title: $content.find('.modal-content-header:first').text(),
            onCreate: create_callback
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

    // trigger modal on page load if hash is present
    switch (window.location.hash) {
    case '#map':
        $('#map-link').trigger('click');
        break;
    case '#schedule':
        $('#schedule-link').trigger('click');
        break;
    }

    // initialize fx family nav
    Mozilla.FxFamilyNav.init({ primaryId: 'os', subId: 'mwc' });
})(window.jQuery);
