/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function(Mozilla, w, $) {
    'use strict';

    var $w = $(w);
    var $document = $(document);
    var $introImage = $('#intro-image');
    var $animationStage = $('#animation-stage');
    var $videoLink = $('#video-link');
    var $videoContainer = $('#video-modal');
    var $video = $('#hello-video');

    var supportsHTML5Video = !!document.createElement('video').canPlayType;
    var isWideViewport = $w.width() >= 740;
    var mqIsWide;
    var tourSource = getParameterByName('utm_source');

    if (isWideViewport) {
        if (Mozilla.SVGAnimCheck()) {
            $w.on('load', function() {
                $animationStage.addClass('animate wide');
            });
        } else {
            $('body').addClass('no-animation');
        }
    } else {
        if (Mozilla.SVGAnimCheck.supportsCSSAnimations()) {
            $w.on('load', function() {
                $animationStage.addClass('animate mini');
            });
        } else {
            $('body').addClass('no-animation');
        }
    }

    // resizing the browser with animation just displays the intro image
    if (typeof matchMedia !== 'undefined') {
        mqIsWide = matchMedia('(min-width: 760px)');

        mqIsWide.addListener(function() {
            if ($animationStage.hasClass('animate')) {
                $animationStage.remove(); // why not?
                $introImage.css('display', 'block');
            }
        });
    }

    // listen for events in/on Hello menu
    var bindHelloObserver = function() {
        Mozilla.UITour.observe(function(e) {
            switch (e) {
                case 'Loop:ChatWindowOpened':
                    w.gaTrack(['_trackEvent', '/hello interactions', 'productPage', 'StartConversation-NoTour']);
                    break;
                case 'Loop:RoomURLCopied':
                    w.gaTrack(['_trackEvent', '/hello interactions', 'productPage', 'URLCopied-NoTour']);
                    break;
                case 'Loop:RoomURLEmailed':
                    w.gaTrack(['_trackEvent', '/hello interactions', 'productPage', 'URLEmailed-NoTour']);
                    break;
            }
        });
    };

    var handleVisibilityChange = function() {
        if (document.hidden) {
            // hide Hello menu & stop observer when changing tabs or minimizing window
            Mozilla.UITour.observe(null);
        } else {
            // listen for Hello menu/chat window events
            bindHelloObserver();
        }
    };

    var showFxFooterMessaging = function() {
        // show Fx with Hello footer messaging
        $('#ctacopy-hellofx').show();

        // hide footer download button
        $('#download-fx').hide();

        // show footer try button
        $('#try-hello-footer').css('display', 'block');
    };

    var addLinkEvent = function (linkSelector, eventName) {
        $(linkSelector).on('click', function(e) {
            var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
            var href = this.href;
            if (newTab) {
                w.gaTrack(['_trackEvent', '/hello interactions', 'productPage', eventName]);
            } else {
                e.preventDefault();
                w.gaTrack(['_trackEvent', '/hello interactions', 'productPage', eventName], function() {
                    w.location = href;
                });
            }
        });
    };

    // get query string parameters
    function getParameterByName (name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)'),
        results = regex.exec(location.search);
        return results === null ? 'none' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    if (w.isFirefox()) {
        // if Fx, hide all footer messaging
        // (correct messaging to display determined below)
        $('.dltry-copy').hide();

        // mobile Fx shouldn't see dl button, so best fallback is 'Try Hello' link to SUMO
        if (w.isFirefoxMobile()) {
            showFxFooterMessaging();
        }
        // Hello exists in desktop version 35 and up
        else if (w.getFirefoxMasterVersion() >= 35) {
            showFxFooterMessaging();

            // see if Hello is an available target in toolbar/overflow/customize menu
            Mozilla.UITour.getConfiguration('availableTargets', function(config) {
                // 'loop' is the snazzy internal code name for Hello
                if (config.targets && config.targets.indexOf('loop') > -1) {
                    // show the intro try hello button
                    $('#intro .try-hello').addClass('active');

                    // convert the footer try hello link to a button
                    $('#try-hello-footer').attr('role', 'button');

                    // clicking either 'try Hello' button (intro/footer) will open the Hello menu
                    $('.try-hello').on('click', function(e) {
                        e.preventDefault();

                        // (bug 1115227, bug 1130194) pass source to FTU; limit to set values.
                        if (tourSource === 'twitter' || tourSource === 'facebook' || tourSource === 'wiki' || tourSource === 'email') {
                            Mozilla.UITour.registerPageID('hello-tour_OpenPanel_' + tourSource);
                        }

                        // show Hello menu when icon in toolbar, customize menu, or overflow
                        Mozilla.UITour.showMenu('loop', function() {
                            // clicking Hello icon in toolbar does not close the menu
                            // (bug 1113896), so allow closing by clicking anywhere on page
                            $document.one('click', function() {
                                Mozilla.UITour.hideMenu('loop');
                            });

                            w.gaTrack(['_trackEvent', '/hello interactions', 'productPage', 'Open']);

                            // hide the hello panel when browser resizes due to
                            // https://bugzilla.mozilla.org/show_bug.cgi?id=1091785
                            $w.one('resize', function() {
                                Mozilla.UITour.hideMenu('loop');
                            });
                        });
                    });

                    // listen for events within Hello menu/chat window
                    bindHelloObserver();

                    // enable/disable listeners when document visibility changes
                    $document.on('visibilitychange', handleVisibilityChange);

                    w.gaTrack(['_trackEvent', '/hello interactions', 'productPage', 'EligibleView']);
                } else {
                    // if Hello is not in toolbar/menu, change footer button to link
                    // to a SUMO article and do some GA tracking
                    addLinkEvent('#try-hello-footer', 'IneligibleClick');

                    w.gaTrack(['_trackEvent', '/hello interactions', 'productPage', 'IneligibleView']);
                }
            });
        } else {
            // if Fx is version 34 or lower (no Hello support) display update messaging in footer
            $('#ctacopy-oldfx').show();

            addLinkEvent('.download-link', 'ClickUpgrade');
        }
    } else {
        // for non-Fx users, show get Fx feature & remove node to maintain nth-child margin rules
        // (we wont need this node/copy for non-Fx users)
        $('#feature-account').remove();
        $('#feature-getfx').show();

        addLinkEvent('.download-link', 'ClickDownload');
    }

    $videoLink.on('click', function(e) {
        e.preventDefault();

        Mozilla.Modal.createModal(this, $videoContainer, {
            title: 'Hello',
            onCreate: function() {
                if (supportsHTML5Video) {
                    setTimeout(function() {
                        $video[0].play();
                    }, 500);
                }
            }
        });
    });

    $video.on('play', function() {
        w.gaTrack(['_trackEvent', '/hello interactions', 'productPage', 'PlayVideo']);
    });

    Mozilla.FxFamilyNav.init({ primaryId: 'desktop', subId: 'hello' });
})(window.Mozilla, window, window.jQuery);
