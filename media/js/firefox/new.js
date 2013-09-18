/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Modernizr, _gaq, site) {
    'use strict';

    var path_parts = window.location.pathname.split('/');
    var query_str = window.location.search ? window.location.search + '&' : '?';
    var referrer = path_parts[path_parts.length - 2];
    var locale = path_parts[1];
    var virtual_url = ('/' + locale + '/products/download.html' +
                       query_str + 'referrer=' + referrer);

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

    // Add GA custom tracking and external link tracking
    var state = 'Desktop, not Firefox';
    if ($html.hasClass('android')) {
        if ($html.hasClass('firefox-latest')) {
            state = 'Android, Firefox up-to-date';
        } else if ($html.hasClass('firefox-old')) {
            state = 'Android, Firefox not up-to-date';
        } else {
            state = 'Android, not Firefox';
        }
    } else if ($html.hasClass('ios')) {
        state = 'iOS, Firefox not supported';
    } else if ($html.hasClass('fxos')) {
        state = 'FxOS';
    } else {
        if ($html.hasClass('firefox-latest')) {
            state = 'Desktop, Firefox up-to-date';
        } else if ($html.hasClass('firefox-old')) {
            state = 'Desktop, Firefox not up-to-date';
        }
    }
    window._gaq = _gaq || [];
    window._gaq.push(['_setCustomVar', 4, '/new conditional message', state, 3]);

    $(document).ready(function() {
        var $scene1 = $('#scene1');
        var $stage = $('#stage-firefox');
        var $thankYou = $('.thankyou');
        var hash_change = ('onhashchange' in window);

        // Add external link tracking
        $(document).on('click', 'a', function(e) {
            // only track off-site links and don't track download.mozilla.org links
            if (this.hostname && this.hostname !== location.hostname && this.hostname !== 'download.mozilla.org') {
                var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
                var href = this.href;
                var callback = function() {
                    window.location = href;
                };

                if (newTab) {
                    gaTrack(['_trackEvent', '/new Interaction', 'click', href]);
                } else {
                    e.preventDefault();
                    gaTrack(['_trackEvent', '/new Interaction', 'click', href], callback);
                }
            }
        });

        if (site.platform === 'android') {
            $('#download-button-android .download-subtitle').html(
                $('.android.download-button-wrapper').data('upgradeSubtitle'));

            // On Android, skip all the scene transitions. We're just linking
            // to the Play Store.
            return;
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

        // Pull Firefox download link from the download button and add to the
        // 'click here' link.
        // TODO: Remove and generate link in bedrock.
        $('#direct-download-link').attr(
            'href', $('.download-list li:visible .download-link').attr('href')
        );

        $stage.on('click', '#direct-download-link, .download-link', function(e) {
            e.preventDefault();
            var url = $(e.currentTarget).attr('href');

            function track_and_redirect(url, virtual_url) {
                gaTrack(
                    ['_trackPageview', virtual_url],
                    function() { location.href = url; }
                );
            }

            // we must use a popup to trigger download for IE6/7/8 as the
            // asynchronous `setTimeout` in track_and_redirect() triggers
            // the IE security blocker. Sigh.
            function track_and_popup(url, virtual_url) {
                gaTrack(['_trackPageview', virtual_url]);
                window.open(url, 'download_window', 'toolbar=0,location=no,directories=0,status=0,scrollbars=0,resizeable=0,width=1,height=1,top=0,left=0');
            }

            if (site.platform === 'windows' && $.browser.msie && $.browser.version < 9) {
                // We do a popup for IE < 9 users when they click the download button
                // on scene 1. If they are going straight to scene 2 on page load,
                // we still need to use the regular track_and_redirect() function.
                if (hash_change && location.hash === '#download-fx') {
                    track_and_redirect(url, virtual_url);
                } else {
                    track_and_popup(url, virtual_url);
                }
            } else {
                track_and_redirect(url, virtual_url);
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
