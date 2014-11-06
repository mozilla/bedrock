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

    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    var $window = $(window);
    var $document = $(document);
    var TARGET_1 = 'devtools';
    var TARGET_2 = 'webide';
    var TARGET_3 = 'appMenu';
    var TARGET_4 = 'accountStatus';
    var current = TARGET_1;
    var tourSkipped = false;
    var highlightTimeout;
    var queryIsLargeScreen = matchMedia('(min-width: 900px)');
    var isHighRes = Mozilla.ImageHelper.isHighDpi();

    var trackClick = function (gaArgs, href, event) {
        event.preventDefault();
        gaTrack(gaArgs, function() {
            window.location = href;
        });
    };

    // Setup GA tracking for misc links
    $('.feature .more').on('click', function(e) {
        trackClick([
            '_trackEvent',
            'Developer /firstrun/ Interactions',
            'learn more link clicks',
            $(this).text()
        ], $(this).attr('href'), e);
    });

    // Setup GA tracking for theme reset link
    $('.notice .more').on('click', function(e) {
        trackClick([
            '_trackEvent',
            'Developer /firstrun/ Interactions',
            'learn more link clicks',
            'Want the old look back?'
        ], $(this).attr('href'), e);
    });

    function onYouTubeIframeAPIReady() {

        // show video modal when user clicks a video play link
        $('a.video-play').attr('role', 'button').click(function(e) {
            e.preventDefault();

            var $this = $(this);
            var $video = $this.siblings('.video');

            // grab the nearby h4 tag as the modal window title
            var videoTitle = $this.siblings('h4,h2').text();

            var player = new YT.Player($video.get(0), {
                height: '390',
                width: '640',
                videoId: $video.data('video-id'),
                events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });

            function onPlayerReady(event) {
                event.target.playVideo();
                gaTrack(['_trackEvent', 'Developer /firstrun/ Interactions', 'play', videoTitle + ' video']);
            }

            function onPlayerStateChange(event) {
                if (event.data === YT.PlayerState.ENDED) {
                    gaTrack(['_trackEvent', 'Developer /firstrun/ Interactions', 'finish', videoTitle + ' video']);
                }
            }

            // if user clicks on a video link,
            // close any UITour panels and skip the tour
            clearTimeout(highlightTimeout);
            Mozilla.UITour.hideInfo();
            skipTour();

            Mozilla.Modal.createModal(this, $this.nextAll('.video'), {
                title: videoTitle,
                onCreate: function() {
                    $('#modal').fitVids();
                },
                onDestroy: function() {
                    player.destroy();
                }
            });
        });

    }

    // shows the Dev Tools doorhanger step
    function showDevToolsDoorhanger() {
        var icon = isHighRes ? window.trans('devtoolsIconHighRes') : window.trans('devtoolsIcon');
        var buttons = [];
        var options = {};
        var nextTarget = TARGET_2;

        Mozilla.UITour.getConfiguration('availableTargets', function(config) {

            if (!config.targets) {
                return;
            }

            var nextAvailable = $.inArray(nextTarget, config.targets) !== -1;
            var nextLabel = nextAvailable ? 'nextWebide' : 'nextSync';
            var nextStep = nextAvailable ? nextWebIDEButton : nextSyncButton;

            buttons = [
                {
                    label: window.trans('doorhangerClose'),
                    style: 'link',
                    callback: devToolsDoorhangerClose
                },
                {
                    label: window.trans(nextLabel),
                    style: 'primary',
                    callback: nextStep
                }
            ];

            options = {
                closeButtonCallback: devToolsDoorhangerClose
            };

            showHighlight(TARGET_1);

            setTimeout(function() {
                Mozilla.UITour.showInfo(
                    TARGET_1,
                    window.trans('devtoolsTitle'),
                    window.trans('devtoolsText'),
                    icon,
                    buttons,
                    options
                );
            }, 10);

            current = TARGET_1;
        });
    }

    // close tour and track button click
    function devToolsDoorhangerClose() {
        skipTour();
        gaTrack(['_trackEvent', 'Developer /firstrun/ Interactions', 'Developer Tools doorhanger - link click', 'Close Tour']);
    }

    // show webIDE doorhanger and track button click
    function nextWebIDEButton() {
        showWebIDEDoorhanger();
        gaTrack(['_trackEvent', 'Developer /firstrun/ Interactions', 'Developer Tools doorhanger - button click', 'Next:WebIDE']);
    }

    // shows the WebIDE doorhanger step
    function showWebIDEDoorhanger() {
        var icon = isHighRes ? window.trans('webideIconHighRes') : window.trans('webideIcon');
        var buttons = [];
        var options = {};

        Mozilla.UITour.getConfiguration('availableTargets', function(config) {

            if (!config.targets || $.inArray(TARGET_2, config.targets) === -1) {
                return;
            }

            buttons = [
                {
                    label: window.trans('doorhangerClose'),
                    style: 'link',
                    callback: webIDEDoorhangerClose
                },
                {
                    label: window.trans('nextSync'),
                    style: 'primary',
                    callback: nextSyncButton
                }
            ];

            options = {
                closeButtonCallback: webIDEDoorhangerClose
            };

            Mozilla.UITour.hideInfo();
            showHighlight(TARGET_2);

            setTimeout(function() {
                Mozilla.UITour.showInfo(
                    TARGET_2,
                    window.trans('webideTitle'),
                    window.trans('webideText'),
                    icon,
                    buttons,
                    options
                );
            }, 10);

            current = TARGET_2;
        });
    }

    function webIDEDoorhangerClose() {
        skipTour();
        gaTrack(['_trackEvent', 'Developer /firstrun/ Interactions', 'Try WebIDE doorhanger - link click', 'Close Tour']);
    }

    // show webIDE doorhanger and track button click
    function nextSyncButton() {
        showSyncDoorhanger();
        gaTrack(['_trackEvent', 'Developer /firstrun/ Interactions', 'Try WebIDE doorhanger - button click', 'Next:Sync']);
    }

    // shows the Sync doorhanger step
    function showSyncDoorhanger() {
        var icon = isHighRes ? window.trans('syncIconHighRes') : window.trans('syncIcon');
        var buttons = [
            {
                label: window.trans('doorhangerNothanks'),
                style: 'link',
                callback: syncDoorhangerClose
            },
            {
                label: window.trans('doorhangerSync'),
                style: 'primary',
                callback: showSyncInMenu
            }
        ];
        var options = {
            closeButtonCallback: syncDoorhangerClose
        };

        Mozilla.UITour.hideInfo();
        showHighlight(TARGET_3);

        Mozilla.UITour.showInfo(
            TARGET_3,
            window.trans('syncTitle'),
            window.trans('syncText'),
            icon,
            buttons,
            options
        );

        current = TARGET_3;
    }

    function syncDoorhangerClose() {
        skipTour();
        gaTrack(['_trackEvent', 'Developer /firstrun/ Interactions', 'Sync doorhanger - link click', 'No Thanks']);
    }

    // highlights sync sign in button in the app menu
    function showSyncInMenu() {
        showHighlight(TARGET_4);

        // hide app menu when user clicks anywhere on the page
        $(document.body).one('click', function () {
            Mozilla.UITour.hideHighlight();
        });

        current = TARGET_4;

        gaTrack(['_trackEvent', 'Developer /firstrun/ Interactions', 'Sync doorhanger - button click', 'Sync My Firefox']);
    }

    // hides the current highlight annotation
    function hideAnnotation() {
        Mozilla.UITour.hideMenu('appMenu');
        Mozilla.UITour.hideHighlight();
    }

    // skips the tour when user presses doorhanger close button
    function skipTour() {
        tourSkipped = true;
        hideAnnotation();
    }

    // shows the a given highlight target
    // note showHighlight is called twice due to Bug 1049130
    function showHighlight(target) {
        Mozilla.UITour.showHighlight(target, 'wobble');
        Mozilla.UITour.showHighlight(target, 'wobble');
    }

    // Show the current tour step, based on the current target value
    // and its corresponding highlight availability
    function showTourStep() {
        Mozilla.UITour.getConfiguration('availableTargets', function(config) {
            if (config.targets) {

                var showStep1 = $.inArray(TARGET_1, config.targets) !== -1;
                var showStep2 = $.inArray(TARGET_2, config.targets) !== -1;

                if (current === TARGET_1) {
                    if (showStep1) {
                        showDevToolsDoorhanger();
                    } else if (showStep2) {
                        showWebIDEDoorhanger();
                    } else {
                        showSyncDoorhanger();
                    }
                } else if (current === TARGET_2) {
                    if (showStep2) {
                        showWebIDEDoorhanger();
                    } else {
                        showSyncDoorhanger();
                    }
                } else if (current === TARGET_3) {
                    showSyncDoorhanger();
                }
            }
        });
    }

    // show/hide current highlight based on page visibility
    function handleVisibilityChange() {
        if (document.hidden) {
            Mozilla.UITour.hideInfo();
            hideAnnotation();
            clearTimeout(highlightTimeout);
        } else if (!tourSkipped) {
            highlightTimeout = setTimeout(function () {
                showTourStep();
            }, 900);
        }
    }

    function hideAppMenu() {
        Mozilla.UITour.hideMenu('appMenu');
    }

    // shows the current tour step and binds event listeners
    function bindTour() {
        clearTimeout(highlightTimeout);
        highlightTimeout = setTimeout(function () {
            showTourStep();
        }, 900);
        $document.on('visibilitychange', handleVisibilityChange);
        $window.on('beforeunload', hideAppMenu);
    }

    // hides UITour highlights and undinds event listeners
    function unbindTour() {
        Mozilla.UITour.hideInfo();
        hideAnnotation();
        $document.off('visibilitychange', handleVisibilityChange);
        $window.off('beforeunload', hideAppMenu);
    }

    //Only run the tour if user is on Firefox 35 for desktop.
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 35) {

        // if viewport is wider than 900px show the tour doorhanger
        if(queryIsLargeScreen.matches) {
            bindTour();
        }

        queryIsLargeScreen.addListener(function(mq) {
            clearTimeout(highlightTimeout);
            if (mq.matches) {
                if (!tourSkipped) {
                    bindTour();
                }
            } else {
                unbindTour();
            }
        });

        // register tour ID for telemetry
        Mozilla.UITour.registerPageID('dev-firstrun-35.0a2');
    }

    Mozilla.firstRunOnYouTubeIframeAPIReady = onYouTubeIframeAPIReady;

})(window.jQuery, window.Mozilla);
