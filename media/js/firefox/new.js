/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Modernizr, _gaq, site) {
    'use strict';
    var $html = $(document.documentElement);

    if (isFirefox()) {
        var latestFirefoxVersion = $html.attr('data-latest-firefox');
        latestFirefoxVersion = parseInt(latestFirefoxVersion.split('.')[0], 10);
        latestFirefoxVersion--; // subtract one since a silent update may be
                                // complete and the user hasn't restarted their
                                // browser. This will be removed once there's
                                // a way to get the current version directly
                                // from the browser

        if (isFirefoxUpToDate(latestFirefoxVersion + '')) {
            $html.addClass('firefox-latest');
        } else {
            $html.addClass('firefox-old');
        }
    }

    if (site.platform === 'android') {
        $('#download-button-android .download-subtitle').html(
            $('.android.download-button-wrapper').data('upgradeSubtitle'));

        return;
    }

    var path_parts = window.location.pathname.split('/');
    var query_str = window.location.search ? window.location.search + '&' : '?';
    var referrer = path_parts[path_parts.length-2];
    var locale = path_parts[1];
    var virtual_url = ('/' + locale + '/products/download.html' +
                       query_str + 'referrer=' + referrer);

    $(document).ready(function() {
        var $scene1 = $('#scene1');
        var $stage = $('#stage-firefox');
        var $thankYou = $('.thankyou');
        var hash_change = ('onhashchange' in window);

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
                var href = $(e.currentTarget).attr('href');
                gaTrack(
                    ['_trackPageview', virtual_url],
                    function() { location.href = href; }
                );

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
    });

    // Add GA custom tracking and external link tracking
    var state = 'Original State';
    if ($html.hasClass('android')) {
        if ($html.hasClass('firefox-latest')) {
            state = 'Android, up-to-date';
        } else if ($html.hasClass('firefox-old')) {
            state = 'Android, not up-to-date';
        } else {
            state = 'Android, no Fx detected';
        }
    } else if ($html.hasClass('ios')) {
        state = 'iOS';
    } else if ($html.hasClass('fxos')) {
        state = 'FxOS';
    } else {
        if ($html.hasClass('firefox-latest')) {
            state = 'Desktop, up-to-date';
        } else if ($html.hasClass('firefox-old')) {
            state = 'Desktop, not up-to-date';
        }
    }
    window._gaq = _gaq || [];
    window._gaq.push(['_setCustomVar', 4, '/new conditional message', state, 3]);

    // Add external link tracking
    $(document).click(function(e) {
        if (e.target.nodeName === 'A' && e.target.hostname && e.target.hostname !== location.hostname) {
            var newTab = (e.target.target === '_blank' || e.metaKey || e.crtlKey);
            var href = e.target.href;
            var callback = function() {
                window.location = href;
            };

            if (!newTab) {
                gaTrack(['_trackEvent', '/new Interaction', 'click', href]);
            } else {
                e.preventDefault();
                gaTrack(['_trackEvent', '/new Interaction', 'click', href], callback);
            }
        }
    });


})(window.jQuery, window.Modernizr, window._gaq, window.site);
