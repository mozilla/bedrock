/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// YouTube API hook has to be in global scope
function onYouTubeIframeAPIReady() {
    'use strict';

    Mozilla.firstRunOnYouTubeIframeAPIReady();
}

;(function($, Mozilla) {
    'use strict';

    var $document;
    var $outerWrapper = $('#outer-wrapper');
    var tour;
    var installedAddons;

    var gaVariation;
    var ytLightbeam;
    var ytGhostery;

    // function vars
    var initYouTube;
    var onYouTubeIframeAPIReady;
    var listenYTStateChange;

    var closeTour;
    var logAddonInstall;
    var openFinalNotice;
    var enableIframes;

    // track Sync CTA click and link to about:accounts where posiible
    var trackSyncClick = function(e) {
        e.preventDefault();

        var goToAccounts = function () {
            // available on Firefox 31 and greater
            Mozilla.UITour.showFirefoxAccounts();
        };

        goToAccounts();

    };

    // in case UITour fails
    $outerWrapper.show();

    // Only run experiment content if user is on Firefox 35 for desktop and has not just submitted email form
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 35 && window.location.hash !== '#footer-email-form') {
        $document = $(document);
        installedAddons = [];

        // Add YouTube JS API
        initYouTube = function() {
            var tag = document.createElement('script');

            tag.src = 'https://www.youtube.com/iframe_api';
            var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        };

        closeTour = function() {
            // show default #outer-wrapper
            $outerWrapper.show();
            tour.doCloseTour();

            Mozilla.syncAnimation();
        };

        logAddonInstall = function(addon) {
            if (installedAddons.indexOf(addon) === -1) {
                installedAddons.push(addon);

                // cover up install button/iframe
                $('#' + addon).addClass('installed').find('.iframe-overlay').fadeIn('fast');

                // if both add-ons have been clicked, show final notice
                if (installedAddons.length === 2) {
                    // open up final notice box
                    setTimeout(function() {
                        openFinalNotice(false);
                    }, 500);
                // if only 1 add-on clicked, change heading
                } else {
                    $('#heading1').fadeOut('fast', function() {
                        $('#heading2').fadeIn('fast');
                    });
                }
            }
        };

        openFinalNotice = function(trackCloseClick) {
            $('#close-tour').fadeOut('fast');
            $('#ui-initial').fadeOut('fast', function() {
                $('#ui-final').fadeIn();

                // call twice to correctly position highlight
                // https://bugzilla.mozilla.org/show_bug.cgi?id=1049130
                Mozilla.UITour.showHighlight('addons', 'wobble');
                Mozilla.UITour.showHighlight('addons', 'wobble');

                $document.one('click', function() {
                    Mozilla.UITour.hideMenu('addons');
                });

                $('#thanks-exit').on('click', function(e) {
                    e.preventDefault();
                    closeTour();

                });
            });
        };

        enableIframes = function() {
            $('iframe').each(function(i, iframe) {
                var $iframe = $(iframe);

                $iframe.attr('src', $iframe.attr('data-src'));
            });
        };

        // listen for postMessage from AMO iframes
        window.addEventListener('message', function(e) {
            if (e.origin === 'https://addons.mozilla.org' && e.data.addon) {
                logAddonInstall(e.data.addon);

            }
        });

        // Query if the UITour API is working before we start the tour
        Mozilla.UITour.getConfiguration('sync', function() {
            $outerWrapper.hide();

            // wire up default content sync button
            $('.sync-cta').on('click', '.button', trackSyncClick);

            var suppressDoorhanger = Math.random() >= 0.5;

            // GA
            gaVariation = (suppressDoorhanger) ? 'a' : 'b';

            tour = new Mozilla.BrowserTour({
                id: $('#tour-page').data('telemetry'),
                allowScroll: true,
                suppressDoorhanger: suppressDoorhanger,
                startTour: function(buttonCopy) {
                    // load iframe src's
                    enableIframes();

                    // load youtube
                    initYouTube();

                    // show contents and close button
                    $('.mask-hidden').addClass('in');

                    // mark tour as finished (but don't get rid of mask yet)
                    tour.tourHasFinished = true;

                },
                cancelTour: function(buttonCopy) {
                    closeTour();

                }
            });

            tour.init();

            $('#close-tour').on('click', function() {
                openFinalNotice(true);
            });

            // if doorhanger is not shown in tour, we need to display the
            // contents & close button without user interaction
            if (suppressDoorhanger) {
                // load iframe src's
                enableIframes();

                // load youtube
                initYouTube();

                // show contents and close button
                $('.mask-hidden').addClass('in-delayed');
            }

            // listen for clicks on "here" in alternate secondary heading
            $('#highlight-addons').on('click', function(e) {
                e.preventDefault();

                // call twice to correctly position highlight
                // https://bugzilla.mozilla.org/show_bug.cgi?id=1049130
                Mozilla.UITour.showHighlight('addons', 'none');
                Mozilla.UITour.showHighlight('addons', 'none');

                // timeout so event isn't captured with *this* click
                setTimeout(function() {
                    $document.one('click', function() {
                        Mozilla.UITour.hideMenu('appMenu');
                    });
                }, 50);
            });
        });
    }

    listenYTStateChange = function(e) {
        var videoID = e.target.t.getAttribute('id');
        var state;

        switch (e.data) {
            case 1:
                state = 'play';
                break;
            case 0:
                state = 'finish';
                break;
        }
    };

    onYouTubeIframeAPIReady = function() {
        ytGhostery = new window.YT.Player($('#yt-ghostery').get(0), {
            height: '146',
            width: '260',
            videoId: 'EKzyifAvC_U',
            events: {
                'onStateChange': function(e) {
                    listenYTStateChange(e);
                }
            }
        });

        ytLightbeam = new window.YT.Player($('#yt-lightbeam').get(0), {
            height: '146',
            width: '260',
            videoId: 'PvqGy9wz_wA',
            events: {
                'onStateChange': function(e) {
                    listenYTStateChange(e);
                }
            }
        });
    };

    // make youtube ready handler globally available
    Mozilla.firstRunOnYouTubeIframeAPIReady = onYouTubeIframeAPIReady;
})(window.jQuery, window.Mozilla);
