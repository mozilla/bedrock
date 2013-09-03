/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

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
            window._gaq.push(['_trackPageview', virtual_url]);
        }
        setTimeout(function() {
            window.location.href = url;
        }, 500);            
    }

    // we must use a popup to trigger download for IE6/7/8 as the
    // asynchronous `setTimeout` in track_and_redirect() triggers
    // the IE security blocker. Sigh.
    function track_and_popup(url) {
        if (_gaq) {
            window._gaq.push(['_trackPageview', virtual_url]);
        }
        window.open(url, 'download_window', 'toolbar=0,location=no,directories=0,status=0,scrollbars=0,resizeable=0,width=1,height=1,top=0,left=0');
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

    // Load images on load so as not to block the loading of other images.
    $(window).on('load', function() {
        // Screen 1 is unique for IE < 9
        if (site.platform === 'windows' && $.browser.msie && $.browser.version < 9) {
            $('html').addClass('winIE8');
        }

        $('body').addClass('ready-for-scene2');

        // initiate download/scene2 if coming directly to #download
        if (location.hash === '#download-fx' && site.platform !== 'other') {
            show_scene(2);
            $('#direct-download-link').trigger('click');
        }
    });

    $(function() {
        // Pull Firefox download link from the download button and add to the
        // 'click here' link.
        // TODO: Remove and generate link in bedrock.
        $('#direct-download-link').attr(
            'href', $('.download-list li:visible .download-link').attr('href')
        );

        $stage.on('click', '#direct-download-link, .download-link', function(e) {
            e.preventDefault();
            var url = $(e.currentTarget).attr('href');

            if (site.platform === 'windows' && $.browser.msie && $.browser.version < 9) {
                // We do a popup for IE < 9 users when they click the download button
                // on scene 1. If they are going straight to scene 2 on page load,
                // we still need to use the regular track_and_redirect() function.
                if (hash_change && location.hash === '#download-fx') {
                    track_and_redirect(url);
                } else {
                    track_and_popup(url);
                }
            } else {
                track_and_redirect(url);
            }

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
