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

