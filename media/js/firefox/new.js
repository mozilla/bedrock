;(function(window, $, Modernizr, _gaq, site) {
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

    function ga_track() {
        if (_gaq) {
            // track download click
            _gaq.push(['_trackPageview',
                       '/en-US/products/download.html?referrer=new-b']);
        }
    }

    function dl_redirect(url) {
        // delay redirect to ensure GA tracking occurs
        window.setTimeout(function() {
            window.location.href = url;
        }, 300);
    }

    // Bind events on domReady.
    $(function() {
        // Pull Firefox download link from the download button and add to the
        // 'click here' link.
        // TODO: Remove and generate link in bedrock.
        var $li = $('.download-list li:visible').filter(':first');
        var ff_dl_url = $li.find('a:first').attr('href');
        $('#direct-download-link').attr('href', ff_dl_url).on('click', function(e) {
            e.preventDefault();
            ga_track();
            dl_redirect($(this).attr('href'));
        });

        // Trigger animation after download.
        var $scene2 = $('#scene2');
        var $stage = $('#stage-firefox');
        var $thankYou = $('.thankyou');
        $('.download-firefox').on('click', function(e) {
            e.preventDefault();
            var $link = $(this);
            ga_track();

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
                window.setTimeout(function() {
                    $thankYou.focus();
                }, 500);
            }

            dl_redirect($link.attr('href'));
        });
    });
})(window, window.jQuery, window.Modernizr, window._gaq, window.site);
