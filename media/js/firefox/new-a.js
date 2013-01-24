;(function(window, $, _gaq) {
    'use strict';

    // Bind events on domReady.
    $(function() {
        $('.download-firefox').on('click', function(e) {
            e.preventDefault();
            var $link = $(this);

            if (_gaq) {
                // track download click
                _gaq.push(['_trackPageview',
                           '/en-US/products/download.html?referrer=new']);
            }

            window.setTimeout(function() {
                window.location.href = $link.attr('href');
            }, 500);
        });
    });
})(window, window.jQuery, window._gaq);
