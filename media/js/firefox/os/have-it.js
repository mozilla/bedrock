/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var isSmallViewport = $(window).width() < 760;

    // setup have-it-all scrollorama controller
    var hiaController = $.superscrollorama({
        playoutAnimations: false
    });

    var $masthead = $('#have-it-all-masthead');

    // app screen shots
    var $contactsApp = $('#contacts-app');
    var $photosApp = $('#photos-app');
    var $photosEditApp = $('#photos-edit-app');
    var $musicApp = $('#music-app');
    var $radioApp = $('#radio-app');
    var $mapsApp = $('#maps-app');
    var $mailApp = $('#mail-app');
    var $messagesApp = $('#messages-app');
    var $marketplaceApp = $('#marketplace-app');
    var $landingHeading = $('#landing-heading');

    // sub sections for pinning
    var $stage = $('#stage');
    var $landing = $('#landing');
    var $social = $('#social');
    var $photos = $('#photos');
    var $music = $('#music');
    var $maps = $('#maps ');
    var $messages = $('#messages');
    var $marketplace = $('#marketplace');

    // sub section content for tweening
    var $socialLeftContent = $('#social .content.left');
    var $socialRightContent = $('#social .content.right');
    var $photosContent = $('#photos .content');
    var $musicContent = $('#music .content');
    var $mapsContent = $('#maps .content');
    var $messagesContent = $('#messages .content');
    var $marketplaceContent = $('#marketplace .content');

    /*
     * Setup DOM and CSS styles for Have-It-All scroller
     */
    function initHaveItAllScroller() {

        var SECTION_DURATION = 1000;
        var STAGE_DURATION = 7920;
        var MASTHEAD_DURATION = 8100;
        var LANDING_DURATION = 920;

        var $nav = $('#have-it-all-nav');
        var $secondaryNav = $('#masthead');
        var $stageContent = $('#stage .item');

        // viewport offsets for pinning items
        var navOffset = $masthead.height() - $nav.outerHeight() - $secondaryNav.height();
        var landingOffset = $nav.outerHeight() + $secondaryNav.height();

        // init timelines for tween animations
        var landingAnimations = new TimelineLite();
        var socialAnimations = new TimelineLite();
        var photosAnimations = new TimelineLite();
        var musicAnimations = new TimelineLite();
        var mapsAnimations = new TimelineLite();
        var messagesAnimations = new TimelineLite();
        var marketplaceAnimations = new TimelineLite();

        // add scroller-on class for css repositioning
        $('#have-it-all .main-wrapper').removeClass('scroller-off').addClass('scroller-on');

        // append the content to the stage
        // we do this for fixed horizontal animations
        // as the user scrolls vertically
        $contactsApp.appendTo($stageContent);
        $photosApp.appendTo($stageContent);
        $photosEditApp.appendTo($stageContent);
        $musicApp.appendTo($stageContent);
        $radioApp.appendTo($stageContent);
        $mapsApp.appendTo($stageContent);
        $mailApp.appendTo($stageContent);
        $messagesApp.appendTo($stageContent);
        $marketplaceApp.appendTo($stageContent);
        $landingHeading.appendTo($stageContent);
        $socialLeftContent.appendTo($stageContent);
        $socialRightContent.appendTo($stageContent);
        $photosContent.appendTo($stageContent);
        $musicContent.appendTo($stageContent);
        $mapsContent.appendTo($stageContent);
        $messagesContent.appendTo($stageContent);
        $marketplaceContent.appendTo($stageContent);

        // timeline of tweens for stage
        // at the end we bring in the social sub section content
        landingAnimations
            .add([
                TweenMax.from($musicApp, 2, {css: {top: '-270px'}}),
                TweenMax.to($musicApp, 2, {css: {top: '-400px'}}),
                TweenMax.from($photosApp, 2, {css: {top: '-270px'}}),
                TweenMax.to($photosApp, 2, {css: {top: '-400px'}}),
                TweenMax.from($mailApp, 2, {css: {top: '-270px'}}),
                TweenMax.to($mailApp, 2, {css: {top: '-400px'}}),
                TweenMax.from($marketplaceApp, 2, {css: {top: '350px'}}),
                TweenMax.to($marketplaceApp, 2, {css: {top: '560px'}}),
                TweenMax.from($contactsApp, 2, {css: {top: '350px'}}),
                TweenMax.to($contactsApp, 2, {css: {top: '560px'}}),
                TweenMax.from($mapsApp, 2, {css: {top: '350px'}}),
                TweenMax.to($mapsApp, 2, {css: {top: '560px'}}),
                TweenMax.to($landingHeading, 2, {css: {marginLeft: '-200%', opacity: 0}})
            ])
            .add([
                TweenMax.to($socialLeftContent, 2, {css: {marginLeft: 0, opacity: 1}}),
                TweenMax.to($socialRightContent, 2, {css: {marginRight: 0, opacity: 1}}),
                TweenMax.to($contactsApp, 2, {css: {top: '80px'}})
            ]);

        // timeline of tweens for social sub section
        // move the content out and bring in the photo section
        socialAnimations
            .add([
                TweenMax.to($socialLeftContent, 2, {css: {marginLeft: '-100%', opacity: 0}, delay: 3}),
                TweenMax.to($socialRightContent, 2, {css: {marginRight: '-100%', opacity: 0}, delay: 3}),
                TweenMax.to($contactsApp, 2, {css: {top: '560px'}, delay: 3})
            ])
            .add([
                TweenMax.to($photosContent, 2, {css: {marginLeft: 0, opacity: 1}}),
                TweenMax.to($photosApp, 2, {css: {top: '80px'}}),
                TweenMax.to($photosEditApp, 2, {css: {marginRight: 0, opacity: 1}})
            ]);

        // timeline of tweens for photos sub section
        // move the content out and bring in the music section
        photosAnimations
            .add([
                TweenMax.to($photosContent, 2, {css: {marginLeft: '-100%', opacity: 0}, delay: 3}),
                TweenMax.to($photosApp, 2, {css: {top: '-400px'}, delay: 3}),
                TweenMax.to($photosEditApp, 2, {css: {marginRight: '-100%', opacity: 0}, delay: 3})
            ])
            .add([
                TweenMax.to($radioApp, 2, {css: {marginLeft: '-150px', opacity: 1}})
            ])
            .add([
                TweenMax.to($musicApp, 2, {css: {top: '80px'}}),
                TweenMax.to($musicContent, 2, {css: {marginRight: 0, opacity: 1}})
            ]);

        // timeline of tweens for music sub section
        // move the content out and bring in the maps section
        musicAnimations
            .add([
                TweenMax.to($musicApp, 2, {css: {top: '-400px'}, delay: 3}),
                TweenMax.to($musicContent, 2, {css: {marginRight: '-100%', opacity: 0}, delay: 3})
            ])
            .add([
                TweenMax.to($radioApp, 2, {css: {marginLeft: '-175%', opacity: 0}})
            ])
            .add([
                TweenMax.to($mapsApp, 2, {css: {top: '80px'}}),
                TweenMax.to($mapsContent, 2, {css: {marginLeft: 0, opacity: 1}})
            ]);

        // timeline of tweens for maps sub section
        // move the content out and bring in the messages section
        mapsAnimations
            .add([
                TweenMax.to($mapsApp, 2, {css: {top: '560px'}, delay: 3}),
                TweenMax.to($mapsContent, 2, {css: {marginLeft: '-100%', opacity: 0}, delay: 3})
            ])
            .add([
                TweenMax.to($messagesContent, 2, {css: {marginLeft: 0, opacity: 1}, delay: 0.5}),
                TweenMax.to($messagesApp, 2, {css: {marginLeft: '-150px', opacity: 1}}),
                TweenMax.to($mailApp, 2, {css: {top: '80px'}})
            ]);

        // timeline of tweens for messages sub section
        // move the content out and bring in the marketplace section
        messagesAnimations
            .add([
                TweenMax.to($messagesContent, 2, {css: {marginLeft: '-100%', opacity: 0}, delay: 3}),
                TweenMax.to($messagesApp, 2, {css: {marginLeft: '-175%', opacity: 0}, delay: 3.5}),
                TweenMax.to($mailApp, 2, {css: {top: '-400px'}, delay: 3})
            ])
            .add([
                TweenMax.to($marketplaceApp, 2, {css: {top: '80px'}}),
                TweenMax.to($marketplaceContent, 2, {css: {marginRight: 0, opacity: 1}})
            ]);

        // timeline of tweens for marketplace sub section
        // here we just move the content out as it's the last section
        marketplaceAnimations
            .add([
                TweenMax.to($marketplaceApp, 2, {css: {top: '560px'}, delay: 3}),
                TweenMax.to($marketplaceContent, 2, {css: {marginRight: '-100%', opacity: 0}, delay: 3})
            ]);

        // reset default positions *before* we get to have-it-all
        // tweens sometimes don't finish when srolling up/down page too fast (e.g. home key)
        $('#adaptive-wrapper').waypoint(function () {
            $musicApp.css({'top': '-270px'});
            $photosApp.css({'top': '-270px'});
            $mailApp.css({'top': '-270px'});
            $contactsApp.css({'top': '350px'});
            $mapsApp.css({'top': '350px'});
            $marketplaceApp.css({'top': '350px'});
            $socialLeftContent.css('margin-left', '-100%');
            $socialRightContent.css('margin-right', '-100%');
            $photosContent.css('margin-left', '-100%');
            $photosEditApp.css({'margin-right': '-100%'});
            $radioApp.css({'margin-left': '-175%'});
            $musicContent.css('margin-right', '-100%');
            $mapsContent.css('margin-left', '-100%');
            $messagesContent.css('margin-left', '-100%');
            $messagesApp.css({'margin-left': '-175%'});
            $marketplaceContent.css('margin-right', '-100%');
        });

        $('#mission').waypoint(function () {
            $musicApp.css({'top': '-400px'});
            $photosApp.css({'top': '-400px'});
            $mailApp.css({'top': '-400px'});
            $contactsApp.css({'top': '560px'});
            $mapsApp.css({'top': '560px'});
            $marketplaceApp.css({'top': '560px'});
            $socialLeftContent.css('margin-left', '-100%');
            $socialRightContent.css('margin-right', '-100%');
            $photosContent.css('margin-left', '-100%');
            $photosEditApp.css({'margin-right': '-100%'});
            $radioApp.css({'margin-left': '-175%'});
            $musicContent.css('margin-right', '-100%');
            $mapsContent.css('margin-left', '-100%');
            $messagesContent.css('margin-left', '-100%');
            $messagesApp.css({'margin-left': '-175%'});
            $marketplaceContent.css('margin-right', '-100%');
        }, { offset: landingOffset });

        // sometimes if you scroll up really fast tweens can get missed
        // these waypoints act as safety nets, and set content to correct places
        // if a tween should get missed
        $('#messages').waypoint(function (direction) {
            if (direction === 'up') {
                $marketplaceApp.css({'top': '560px'});
                $marketplaceContent.css('margin-right', '-100%');
            }
        }, { offset: -2 });

        $('#maps').waypoint(function (direction) {
            if (direction === 'up') {
                $marketplaceApp.css({'top': '560px'});
                $marketplaceContent.css('margin-right', '-100%');
                $messagesContent.css('margin-left', '-100%');
                $messagesApp.css({'margin-left': '-175%'});
                $mailApp.css({'top': '-400px'});
            }
        }, { offset: -2 });

        $('#music').waypoint(function (direction) {
            if (direction === 'up') {
                $mapsApp.css({'top': '560px'});
                $mapsContent.css('margin-left', '-100%');
                $marketplaceApp.css({'top': '560px'});
                $marketplaceContent.css('margin-right', '-100%');
                $messagesContent.css('margin-left', '-100%');
                $messagesApp.css({'margin-left': '-175%'});
                $mailApp.css({'top': '-400px'});
            }
        }, { offset: -2 });

        $('#photos').waypoint(function (direction) {
            if (direction === 'up') {
                $musicApp.css({'top': '-400px'});
                $radioApp.css({'margin-left': '-175%'});
                $musicContent.css('margin-right', '-100%');
                $mapsApp.css({'top': '560px'});
                $mapsContent.css('margin-left', '-100%');
                $marketplaceApp.css({'top': '560px'});
                $marketplaceContent.css('margin-right', '-100%');
                $messagesContent.css('margin-left', '-100%');
                $messagesApp.css({'margin-left': '-175%'});
                $mailApp.css({'top': '-400px'});
            }
        }, { offset: -2 });

        $('#social').waypoint(function (direction) {
            if (direction === 'up') {
                $photosContent.css('margin-left', '-100%');
                $photosEditApp.css({'margin-right': '-100%'});
                $photosApp.css({'top': '-400px'});
                $musicApp.css({'top': '-400px'});
                $radioApp.css({'margin-left': '-175%'});
                $musicContent.css('margin-right', '-100%');
                $mapsApp.css({'top': '560px'});
                $mapsContent.css('margin-left', '-100%');
                $marketplaceApp.css({'top': '560px'});
                $marketplaceContent.css('margin-right', '-100%');
                $messagesContent.css('margin-left', '-100%');
                $messagesApp.css({'margin-left': '-175%'});
                $mailApp.css({'top': '-400px'});
            }
        }, { offset: -2 });

        $('#have-it-all').waypoint(function (direction) {
            if (direction === 'up') {
                $musicApp.css({'top': '-270px'});
                $photosApp.css({'top': '-270px'});
                $mailApp.css({'top': '-270px'});
                $contactsApp.css({'top': '350px'});
                $mapsApp.css({'top': '350px'});
                $marketplaceApp.css({'top': '350px'});
                $socialLeftContent.css('margin-left', '-100%');
                $socialRightContent.css('margin-right', '-100%');
                $photosContent.css('margin-left', '-100%');
                $photosEditApp.css({'margin-right': '-100%'});
                $radioApp.css({'margin-left': '-175%'});
                $musicContent.css('margin-right', '-100%');
                $mapsContent.css('margin-left', '-100%');
                $messagesContent.css('margin-left', '-100%');
                $messagesApp.css({'margin-left': '-175%'});
                $marketplaceContent.css('margin-right', '-100%');
            }
        }, { offset: -2 });

        // pin have-it-all masthead for the whole duration
        hiaController.pin($masthead, MASTHEAD_DURATION, {
            offset: navOffset,
            pushFollowers: false
        });

        // pin the stage for the whole duration
        hiaController.pin($stage, STAGE_DURATION, {
            offset: -landingOffset,
            pushFollowers: false
        });

        // then each sub section duration controls the different tween timelines
        // pined elements seem to cope with tweens better when scrolling fast
        hiaController.pin($landing, LANDING_DURATION, {
            anim: landingAnimations,
            offset: -(landingOffset * 2),
            pushFollowers: false
        });

        hiaController.pin($social, SECTION_DURATION, {
            anim: socialAnimations,
            offset: -landingOffset,
            pushFollowers: false
        });

        hiaController.pin($photos, SECTION_DURATION, {
            anim: photosAnimations,
            offset: -landingOffset,
            pushFollowers: false
        });

        hiaController.pin($music, SECTION_DURATION, {
            anim: musicAnimations,
            offset: -landingOffset,
            pushFollowers: false
        });

        hiaController.pin($maps, SECTION_DURATION, {
            anim: mapsAnimations,
            offset: -landingOffset,
            pushFollowers: false
        });

        hiaController.pin($messages, SECTION_DURATION, {
            anim: messagesAnimations,
            offset: -landingOffset,
            pushFollowers: false
        });

        hiaController.pin($marketplace, SECTION_DURATION, {
            anim: marketplaceAnimations,
            offset: -landingOffset,
            pushFollowers: false
        });

        function updateAnims () {
            hiaController.updatePin($masthead, MASTHEAD_DURATION, {
                offset: $masthead.height() - $nav.outerHeight() - $secondaryNav.height(),
                pushFollowers: false
            });
            hiaController.triggerCheckAnim();
        }

        $(window).resize(function () {
            clearTimeout(this.timeout);
            this.timeout = setTimeout(updateAnims, 100);
        });

        // handle clicks on nav links
        $('#have-it-all-nav').on('click', 'a', function (e) {
            e.preventDefault();

            var primaryNavHeight = $('#masthead').height();
            var secondaryNavHeight = $('#have-it-all-nav').outerHeight();
            var distance = Math.abs($(document).scrollTop() - ($($(this).attr('href')).offset().top - primaryNavHeight));

            $(window).scrollTop($($(this).attr('href')).offset().top - primaryNavHeight + secondaryNavHeight);

            // $('html, body').animate({
            //     scrollTop: $($(this).attr('href')).offset().top - primaryNavHeight + secondaryNavHeight
            // }, distance/2);

            //track GA event for icon clicks
            trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'click', this.hash]);
        });

        $('#landing').waypoint(function (direction) {
            $nav.find('a').removeClass('curr');
        });

        $('.hia-anchor').waypoint(function (direction) {
            if (direction === 'down') {
                $nav.find('a').removeClass('curr');
                $nav.find('a[href="#' + this.id + '"]').addClass('curr');
            }
        }, { offset: landingOffset });

        $('.hia-anchor').waypoint(function (direction) {
            if (direction === 'up') {
                $nav.find('a').removeClass('curr');
                $nav.find('a[href="#' + this.id + '"]').addClass('curr');
            }
        }, { offset: -landingOffset });
    }

    function initHaveItAllSlider() {
        var slider;

        // clone the social icons and place in left content
        // right content will get hidden using css
        var $socialIcons = $('#social .icon-list').clone();
        $('#social .content.left').append($socialIcons);

        //remove landing and stage so they aren't counted as slides
        $('#landing').detach();
        $('#stage').detach();

        slider = new $.plusSlider($('#have-it-all .main-wrapper'), {
            sliderEasing: 'swing',
            fullWidth: true,
            sliderType: 'slider',
            createArrows: true,
            autoPlay: false,
            afterSlide: updateActiveNav
        });

        function updateActiveNav (base) {
            $('#have-it-all-nav').find('a').removeClass('curr');
            $($('#have-it-all-nav a')[base.currentSlideIndex]).addClass('curr');
        }

        // add slider navigation on icon links
        $('#have-it-all-nav').on('click', 'a', function (e) {
            e.preventDefault();

            var hiaNavOffset = $('#masthead').height() + $('#have-it-all-nav').outerHeight();
            var offset = isSmallViewport ? 0 : hiaNavOffset;

            switch (this.id) {
            case 'social-link':
                slider.toSlide(0);
                break;
            case 'photos-link':
                slider.toSlide(1);
                break;
            case 'music-link':
                slider.toSlide(2);
                break;
            case 'maps-link':
                slider.toSlide(3);
                break;
            case 'messages-link':
                slider.toSlide(4);
                break;
            case 'marketplace-link':
                slider.toSlide(5);
                break;
            }

            $('html, body').animate({
                scrollTop: $('.plusslider').offset().top - offset
            }, 200);

            //track GA event for icon clicks
            trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'click', this.hash]);
        });
    }

    // if we have touch, pointer events or small viewport, use a slider
    // else use scrolling interactions
    if ('ontouchstart' in window || navigator.msMaxTouchPoints || navigator.maxTouchPoints || isSmallViewport) {
        initHaveItAllSlider();
    } else {
        initHaveItAllScroller();
    }
})(jQuery);
