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

    var $scene2 = $('#scene2');
    var $stage = $('#stage-firefox');
    var $thankYou = $('.thankyou');
    // drop support for IE7/8. good?
    var can_hashchange = ('onhashchange' in window && 'addEventListener' in window);

    function show_scene(scene) {
        if (scene === 2) {
            if (!Modernizr.csstransitions) {
                $scene2.css('visibility', 'visible'); // ensure visibility prior to animation
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
        } else {
            if (!Modernizr.csstransitions) {
                $stage.animate({
                    bottom: '0px'
                }, 400, function() {
                    $scene2.css('visibility', 'hidden'); // revert scene2 to hidden
                    $thankYou.blur();
                });
            } else {
                $scene2.css('visibility', 'visible'); // ensure visibility through animation
                $stage.removeClass('scene2'); // remove class - transition to scene 1
                window.setTimeout(function() {
                    $scene2.css('visibility', ''); // revert to default (hidden)
                    $thankYou.blur();
                }, 500);
            }
        }
    }

    // Bind events on domReady.
    $(function() {
        if (can_hashchange) {
            window.addEventListener('hashchange', function(e) {
                if (window.location.hash === '#download') {
                    show_scene(2);
                } else {
                    show_scene(1);
                }
            });
        }

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
        $('.download-firefox').on('click', function(e) {
            e.preventDefault();

            var $link = $(this);
            ga_track();

            if (can_hashchange) {
                window.location.href += '#download';
            } else {
                show_scene(2);
            }

            dl_redirect($link.attr('href'));
        });
    });
})(window, window.jQuery, window.Modernizr, window._gaq, window.site);