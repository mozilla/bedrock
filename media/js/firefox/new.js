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

        if (isFirefoxUpToDate(latestFirefoxVersion + '')) {
            $html.addClass('firefox-latest');
        } else {
            $html.addClass('firefox-old');
        }
    }

    // scene2 install images are unique for IE < 9
    if (window.site.isIELT9) {
        $html.addClass('winIE8');
    }

    // Add GA custom tracking and external link tracking
    var state = 'Desktop, not Firefox';
    if (site.platform === 'android') {
        if ($html.hasClass('firefox-latest')) {
            state = 'Android, Firefox up-to-date';
        } else if ($html.hasClass('firefox-old')) {
            state = 'Android, Firefox not up-to-date';
        } else {
            state = 'Android, not Firefox';
        }
    } else if (site.platform === 'ios') {
        state = 'iOS, Firefox not supported';
    } else if (site.platform === 'fxos') {
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

    // conditions in which scene2 should not be shown, even when the
    // #download-fx hash is set
    var no_scene2 = (
           $html.hasClass('firefox-latest')
        || site.platform === 'other'    // no download available
        || site.platform === 'ios'      // unsupported platform
        || site.platform === 'fxos'     // no download available
        || site.platform === 'android'  // download goes to Play Store
    );

    $(document).ready(function() {
        var $scene1 = $('#scene1');
        var $stage = $('#stage-firefox');
        var $thankYou = $('.thankyou');
        var hash_change = ('onhashchange' in window);

        // Add external link tracking, excluding links in Tabzilla that will be
        // logged in tabzilla.js
        $('#outer-wrapper').on('click', 'a', function(e) {
            // only track off-site links and don't track download links which are
            // tracked by global.js
            if (this.hostname && this.hostname !== location.hostname &&
                    !$(this).data('channel') && !$(this).data('type')) {
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

        function show_scene(scene, animate) {
            if (animate) {
                $stage.removeClass('stage-no-anim');
            } else {
                $stage.addClass('stage-no-anim');
            }

            var CSSbottom = (scene === 2) ? '-400px' : 0;
            $stage.data('scene', scene);
            $('.scene').css('visibility', 'visible');
            if (!Modernizr.csstransitions && animate) {
                $stage.animate({
                    bottom: CSSbottom
                }, 400);
            } else {
                $stage.toggleClass('scene2');
            }
            if (scene === 2) {
                // after animation, hide scene1 so it's not focusable and
                // reset focus
                setTimeout(function() {
                    $scene1.css('visibility', 'hidden');
                    $thankYou.focus();
                }, 500);
            }
        }

        function show_scene_anim(scene) {
            show_scene(scene, true);
        }

        // Pull download link from the download button and add to the
        // 'click here' link.
        // TODO: Remove and generate link in bedrock.
        var active_download_link = $('.download-list li:visible .download-link');
        $('#direct-download-link').attr({
            'href': active_download_link.attr('href'),
            'data-channel': active_download_link.data('channel')
        });

        $stage.on('click', '.download-link', function(e) {
            if ($stage.data('scene') !== 2) {
                if (hash_change) {
                    window.location.hash = '#download-fx';
                } else {
                    show_scene_anim(2);
                }
            }
        });

        if (hash_change && !no_scene2) {
            $(window).on('hashchange', function() {
                if (window.location.hash === '#download-fx') {
                    show_scene_anim(2);
                }
                if (window.location.hash === '') {
                    show_scene_anim(1);
                }
            });
        }

        $(window).on('load', function() {
            // Add CSS class that allows scene2 images to load. Done on ready()
            // so as not to block the loading of other images.
            $('body').addClass('ready-for-scene2');

            // initiate download/scene2 if coming directly to #download-fx
            if (window.location.hash === '#download-fx') {
                if (no_scene2) {
                    // if using latest Firefox or an unsupported platform just
                    // try to drop the URL hash
                    if (window.history && window.history.replaceState) {
                        var uri = window.location.href.split('#')[0];
                        window.history.replaceState({}, '', uri);
                    }
                } else {
                    show_scene(2);
                    // We initiate the download on a timeout because when the
                    // download starts, any assets that are downloading (i.e.
                    // images from CSS) are cancelled. The delay is to give
                    // the assets time to download. An iframe was used in the
                    // past to work around this issue but it was blocked when
                    // using HTTPS in some browsers.
                    setTimeout(function() {
                        $('#direct-download-link').trigger('click');
                    }, 1500);
                }
            }
        });
    });

    // Override the standard tracking function in global.js
    window.track_download_link = function (event, cmd, url) {
        event.preventDefault();

        // We do a popup for IE < 9 users when they click the download button
        // on scene1. If they are going straight to scene2 on page load, we
        // still need to use the regular track_and_redirect() function because
        // the popup will be blocked and then the download will also be blocked
        // in the popup.
        if (window.site.isIELT9 && window.location.hash !== '#download-fx') {
            track_and_popup(event, cmd, url);
        } else {
            // Delay to initiate download is required to allow animation
            // to finish loading in IE. If delay is removed, the DOM will
            // unload before the animation completes and the page will
            // stop in a half-animated state.
            window.setTimeout(function() {
                track_and_redirect(event, cmd, url);
            }, 500);
        }

        // Log a virtual PV on /firefox/new/ for backward compatibility.
        // Once we confirm the event tracking works well, we can remove
        // the following code.
        gaTrack(['_trackPageview', virtual_url]);
    };

})(window.jQuery, window.Modernizr, window._gaq, window.site);
