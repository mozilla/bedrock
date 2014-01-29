/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
  'use strict';

  $('.modal-link').on('click', function(e) {
    e.preventDefault();

    var $content = $($(this).attr('href'));

    var create_callback = ($content.attr('id') === 'map') ? scrollMap : null;

    Mozilla.Modal.createModal(this, $content, {
        title: $content.find('.modal-content-header:first').text(),
        onCreate: create_callback
    });
  });

  var scrollMap = function() {
    var $map_container = $('#map-container');

    setTimeout(function() {
        $map_container.animate({
            scrollLeft: '300px'
        }, 250, function() {
            setTimeout(function() {
                $map_container.animate({
                    scrollLeft: '0px'
                }, 250);
            }, 350);
        });
    }, 500);
  };
})(window.jQuery);
