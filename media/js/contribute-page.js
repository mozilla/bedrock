/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {
    var $opportunities = $('#opportunities');
    function scrollTo($el) {
      var top = $el.offset().top;
      $("html:not(:animated),body:not(:animated)").animate(
        { scrollTop: top - 20 },
        100
      );
    }

    var pager = Mozilla.Pager.rootPagers[0];

    $('#interest-header').click(function(e) {
      e.preventDefault();
      pager.setPageWithAnimation(pager.pagesById['interest']);
      scrollTo($opportunities);
    });

    $('#location-header').click(function(e) {
      e.preventDefault();
      pager.setPageWithAnimation(pager.pagesById['location']);
      scrollTo($opportunities);
    });

    $('#time-header').click(function(e) {
      e.preventDefault();
      pager.setPageWithAnimation(pager.pagesById['time']);
      scrollTo($opportunities);
    });

});

