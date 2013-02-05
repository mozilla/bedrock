;(function($, Modernizr, _gaq, site) {
    'use strict';

    if (site.platform === 'android') {
        return;
    }

    var path_parts = window.location.pathname.split('/');
    var query_str = window.location.search ? window.location.search + '&' : '?';
    var referrer = path_parts[path_parts.length-2];
    var locale = path_parts[1];
    var virtual_url = ('/' + locale + '/products/download.html' +
                       query_str + 'referrer=' + referrer);
    var $scene1 = $('#scene1');
    var $stage = $('#stage-firefox');
    var $thankYou = $('.thankyou');
    var hash_change = ('onhashchange' in window);

    function track_and_redirect(url) {
        if (_gaq) {
            _gaq.push(['_trackPageview', virtual_url]);
        }
        setTimeout(function() {
            window.location.href = url;
        }, 500);
    }
    function show_scene(scene) {
        var CSSbottom = (scene === 2) ? '-400px' : 0;
        $stage.data('scene', scene);
        $('.scene').css('visibility', 'visible');
        if (!Modernizr.csstransitions) {
            $stage.animate({
                bottom: CSSbottom
            }, 400);
        } else {
            $stage.toggleClass('scene2');
        }
        if (scene === 2) {
            setTimeout(function() {
                $scene1.css('visibility', 'hidden');
                $thankYou.focus();
            }, 500);
        }
    }
    function setup_scene2() {
        // Screen 1 is unique for IE < 9
        if (site.platform === 'windows' && $.browser.msie && $.browser.version < 9) {
            $('html').addClass('winIE8');
        }
        $('body').addClass('ready-for-scene2');
    }
    $(function() {
        // Pull Firefox download link from the download button and add to the
        // 'click here' link.
        $('#direct-download-link').attr(
            'href', $('.download-list li:visible .download-firefox').attr('href')
        );
        
        // initiate download/scene2 if coming directly to #download-fx
        if (location.hash === '#download-fx' && site.platform !== 'other') {
            // load assets for scene2 directly
            setup_scene2();
            // when all is loaded, show scene2 and trigger click
            $(window).on('load', function() {
                show_scene(2);
                $('#direct-download-link').trigger('click');
            });
        }else{
            // Load assets on load so as not to block the loading of other images.
            $(window).on('load', function() {
                setup_scene2();
            });
        }

        $stage.on('click', '#direct-download-link, .download-firefox', function(e) {
            e.preventDefault();

            track_and_redirect($(e.currentTarget).attr('href'));

            if ($stage.data('scene') !== 2) {
                if (hash_change) {
                    location.hash = '#download-fx';
                } else {
                    show_scene(2);
                }
            }
        });

        if (hash_change) {
            $(window).on('hashchange', function() {
                if (location.hash === '#download-fx') {
                    show_scene(2);
                }
                if (location.hash === '') {
                    show_scene(1);
                }
            });
        }
    });
})(window.jQuery, window.Modernizr, window._gaq, window.site);
