;(function($, Modernizr, _gaq, site) {
    'use strict';

    if (site.platform === 'android') {
        return;
    }

    // Load images on load so as not to block the loading of other images.
    $(window).on('load', function() {
        // Screen 1 is unique for IE < 9
        if (site.platform === 'windows' && $.browser.msie && $.browser.version < 9) {
            $('html').addClass('winIE8');
        }

        $('body').addClass('ready-for-scene2');
    });

    // Bind events on domReady.
    $(function() {
        // Pull Firefox download link from the download button and add to the
        // 'click here' link.
        // TODO: Remove and generate link in bedrock.
        var $li = $('.download-list li:visible').filter(':first');
        var ff_dl_link = $li.find('a:first').attr('href');
        $('#direct-download-link').attr('href', ff_dl_link);

        // Trigger animation after download.
        var $scene2 = $('#scene2');
        var $stage = $('#stage-firefox');
        var $thankYou = $('.thankyou');
        $('.download-firefox').on('click', function(e) {
            // cancel natural event
            e.preventDefault();

            // track download click
            if (_gaq) {
                _gaq.push(['_trackPageview',
                           '/en-US/products/download.html?referrer=new-b']);
            }
            if (!Modernizr.csstransitions) {
                $scene2.css('visibility', 'visible');
                $stage.animate({
                    bottom: '-400px'
                }, 400, function() {
                    $thankYou.focus();
                });
            } else {
                $stage.addClass('scene2');
                // transitionend fires multiple times in FF 17, including
                // before the transition actually finished.
                // Work-around with setTimeout.
                setTimeout(function() {
                    $thankYou.focus();
                }, 500);
            }

            // delay natural event
            var that = this;
            setTimeout(function() {
                window.location.href = $(that).attr('href');
            }, 300);
        });
    });
})(window.jQuery, window.Modernizr, window._gaq, window.site);
