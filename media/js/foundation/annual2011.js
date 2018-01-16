/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var $window = $(window);
    var wideMode = false;
    var $nav = $('#page-nav');
    var $head = $('#masthead');
    var navTop = $nav.offset();
    var navHeight = $nav.height() + 30;
    var ARIASHOW = $('button.read').data('aria-show');
    var ARIAHIDE = $('button.read').data('aria-hide');
    var queryTablet = matchMedia('(min-width: 768px)');

    setupThumbnails();

    if (queryTablet.matches) {
        wideMode = true;
        setupCarousel();
        setStage();
        $('#video-stage').show();
    } else {
        wideMode = false;
        $('#video-stage').hide();
    }

    queryTablet.addListener(function(mq) {
        if (mq.matches) {
            wideMode = true;
            setupCarousel();
            setStage();
            $('#video-stage').show();
        } else {
            wideMode = false;
            $('#video-stage').hide();
        }
    });

    // Add the read buttons
    $('button.read').clone().insertBefore('.overlay').attr({
        'aria-pressed': 'false',
        'aria-label': ARIASHOW
    });

    // Reveal text overlays when hovering over a block
    // @Uses hoverIntent plugin: http://cherne.net/brian/resources/jquery.hoverIntent.html
    $('.overlay-wrap').hoverIntent(function() {
        if (wideMode) {
            var overlayHeight = $(this).height() - 80;
            $(this).find('.overlay').css({
                'minHeight' : overlayHeight
            }).fadeIn(200);
            $(this).find('button.read').attr({
                'aria-pressed':'true'
            });
        }
    }, function() {
        if (wideMode) {
            $(this).find('.overlay').delay(300).fadeOut(600, function() {
                $(this).removeAttr('style');
                $(this).prev('button.read').attr({
                    'aria-pressed':'false'
                });
            });
        }
    });

    // Reveal overlays when buttons are activated (for keyboard, touch, and screen readers)
    $('.overlay-wrap .read').on('click', function() {

        if (wideMode) {
            // First hide any visible overlays
            $('.overlay[style]').stop().delay(300).fadeOut(600, function() {
                // Then reset them to normal (hidden in the style sheet)
                $(this).removeAttr('style');
                $(this).prev('button.read').attr({
                    'aria-pressed':'false'
                });
            });

            if ($(this).attr('aria-pressed') === 'false') {

                $(this).attr({
                    'aria-pressed': 'true',
                    'aria-label': ARIAHIDE
                });

                var overlayHeight = $(this).parents('.overlay-wrap').height() - 80;

                $(this).parents('.overlay-wrap').find('.overlay').css({
                    'minHeight' : overlayHeight
                }).fadeIn(200);

                $('html, body').animate({
                    scrollTop: $(this).parents('.overlay-wrap').offset().top -40
                }, 300);
            } else {
                $(this).attr({
                    'aria-pressed': 'false',
                    'aria-label': ARIASHOW
                });
            }
        }
    });


    // Sticky navigation
    var fixed = false;
    var didScroll = false;

    $window.on('scroll', function() {
        didScroll = true;
    });

    $(document).ready(function() {
        var scrollTop = $window.scrollTop();
        if (scrollTop >= navTop.top) {
            didScroll = true;
        }
    });

    function adjustScrollbar() {
        if (didScroll) {
            didScroll = false;
            var scrollTop = $window.scrollTop();
            if (scrollTop >= navTop.top) {
                if (!fixed) {
                    fixed = true;
                    $nav.addClass('fixed');
                    $head.css({
                        'margin-bottom' : navHeight
                    });
                }
            } else {
                if (fixed) {
                    fixed = false;
                    $nav.removeAttr('class');
                    $head.css({
                        'margin-bottom' : '0'
                    });
                }
            }
        }
    }

    // Check for an adjusted scrollbar every 100ms.
    setInterval(adjustScrollbar, 100);

    // Show/hide the navigation in small viewports
    if (!wideMode) {
        $nav.on('click', function() {
            $(this).animate({ 'top': '0' }, 'fast'); // Slide down
            $(this).on('mouseleave', function() {
                $(this).removeAttr('style');
            });
            $('body').on('click', function() {
                $nav.removeAttr('style');
            });
        });
    }

    // Change the navbar color and current item to match the section waypoint
    function waypointCallback(current, previous) {
        return function(dir) {
            if (fixed) {
                if (dir === 'down') {
                    $nav.attr('class', 'fixed ' + current);
                    $nav.find('li').removeClass();
                    $('#nav-' + current).addClass('current');
                }
                else {
                    $nav.attr('class', 'fixed ' + previous);
                    $nav.find('li').removeClass();
                    $('#nav-' + previous).addClass('current');
                }
            }
        };
    }

    //Fire the waypoints for each section, passing classes for the current and previous sections
    //Uses jQuery Waypoints http://imakewebthings.com/jquery-waypoints/
    $('#welcome').waypoint(waypointCallback('welcome', 'welcome'), { offset: navHeight });
    $('#mobilized').waypoint(waypointCallback('mobilized', 'welcome'), { offset: navHeight });
    $('#action').waypoint(waypointCallback('action', 'mobilized'), { offset: navHeight });
    $('#community').waypoint(waypointCallback('community', 'action'), { offset: navHeight });
    $('#sustainability').waypoint(waypointCallback('sustainability', 'community'), { offset: navHeight });


    //Scroll to the linked section
    $window.on('click', '#page-nav a[href^="#"]', function(e) {
        e.preventDefault();
        // Extract the target element's ID from the link's href.
        var elem = $(this).attr('href').replace( /.*?(#.*)/g, '$1' );

        $('html, body').animate({
            scrollTop: $(elem).offset().top - 35
        }, 1000, function() {
            $(elem).attr('tabindex','100').trigger('focus').removeAttr('tabindex');
            if (!wideMode) {
                $nav.removeAttr('style');
            }
        });
    });

    // Load links in new tab/window
    $('a[rel="external"]').on('click', function(e) {
        e.preventDefault();
        window.open(this.href);
    });

    // Load videos in a full-page modal
    $('a.video-play').on('click', function(e) {
        e.preventDefault();
        var $origin = $(this);
        var video = $origin.data('videoSource');
        var poster = $(this).children('img').attr('src');
        var content = '<video id="video" poster="' + poster + '" controls>' +
                      '<source src="' + video + '.mp4" type="video/mp4">' +
                      '<source src="' + video + '.webm" type="video/webm">' +
                      '</video>';
        createModal($origin, content);
    });

    // Load the YouTube video in a full-page modal
    $('a.vid-youtube').on('click', function(e) {
        e.preventDefault();
        var $origin = $(this);
        var content = '<iframe width="640" height="360" src="//www.youtube-nocookie.com/embed/f_f5wNw-2c0?rel=0" frameborder="0" allowfullscreen></iframe>';
        createModal($origin, content);
    });

    // Set up the contributor stories carousel
    function setupCarousel() {
        $('.jcarousel-clip').jcarousel({
            scroll: 4,
            visible: 4,
            buttonNextHTML: null,
            buttonPrevHTML: null,
            itemLastOutCallback: { onAfterAnimation: disableButtons },
            itemLastInCallback: { onAfterAnimation: disableButtons },
            initCallback: controlButtons
        });

        if ($('#story-vid').length > 0) {
            $('#story-vid')[0].pause();
        }

        setStage();
        setupThumbnails();
        controlButtons();
    }

    // Set up video stage
    function setStage() {
        var video = $('#story-slider a.contributor:first').attr('href');
        var poster = $('#story-slider a.contributor:first').data('poster');
        var desc = $('#story-slider .vcard:first .note').html();

        if ($('#story-vid').length > 0) {
            $('#story-vid').attr('poster', poster).attr('src', video);
        }

        if ($('#video-stage figcaption').length > 0) {
            $('#video-stage figcaption').remove();
        }

        $('#video-stage').append('<figcaption>' + desc + '</figcaption>');

        // Add a play button overlay
        if ($('span.btn-play').length > 0) {
            $('span.btn-play').remove();
        }

        $('<span class="btn-play"></span>').appendTo('#video-stage .player').on('click', function() {
            $('#story-vid').attr('controls','controls')[0].play();
            $(this).fadeOut('fast', function() {
                $(this).remove();
            });
        });
    }

    // Add the left and right control buttons
    function controlButtons() {
        $('.btn-prev').on('jcarouselcontrol:active', function() {
            $(this).removeClass('inactive');
        }).on('jcarouselcontrol:inactive', function() {
            $(this).addClass('inactive');
        }).jcarouselControl({
            target: '-=1'
        });

        $('.btn-next').on('jcarouselcontrol:active', function() {
            $(this).removeClass('inactive');
        }).on('jcarouselcontrol:inactive', function() {
            $(this).addClass('inactive');
        }).jcarouselControl({
            target: '+=1'
        });
    }

    // Disable the buttons at the end of the carousel
    function disableButtons(carousel) {
        if (carousel.first === 1) {
            $('.btn-prev').attr('disabled','disabled').addClass('disabled');
        } else {
            $('.btn-prev').removeAttr('disabled').removeClass('disabled');
        }

        if (carousel.last === carousel.size()) {
            $('.btn-next').attr('disabled','disabled').addClass('disabled');
        } else {
            $('.btn-next').removeAttr('disabled').removeClass('disabled');
        }
    }

    // Contributor story thumbnails play the corresponding video
    function setupThumbnails() {
        $('a.contributor').on('click', function(e) {
            e.preventDefault();
            var video = $(this).attr('href');
            var poster = $(this).attr('data-poster');
            var desc = $(this).find('.note').html();

            if (wideMode) {
                $('#story-vid')[0].pause();

                if ($('span.btn-play').length > 0) {
                    $('span.btn-play').remove();
                }

                $('#video-stage figcaption').fadeOut('fast', function() {
                    $(this).html(desc).fadeIn('fast');
                });

                $('#story-vid').attr('controls','controls').attr('src', video)[0].play();

                $('html, body').animate({
                    scrollTop: $('#video-stage').offset().top - 80
                }, 200, function() {
                    $('#story-vid').trigger('focus');
                });
            } else {
                var $origin = $(this);
                var content = '<video id="video" poster="'+poster+'" src="'+video+'" controls autoplay type="video/webm">'+
                              '<p class="desc">'+desc+'</p>';
                createModal($origin, content);
            }
        });
    }

    // Create a full-page overlay and append the content
    function createModal(origin, content) {
        if ($('#fill').length > 0) {
            $('#video')[0].pause();
            $('#fill').remove();
        }
        $('body').addClass('noscroll').append('<div id="fill"><div id="inner"></div></div>');
        $('#inner').append(content);

        if ($('#inner #video').length > 0) {
            $('#video').trigger('focus')[0].play();
        }

        // Add the close button
        $('#done').clone().appendTo('#inner');
        $('#fill #done').on('click', function() {
            if ($('#inner #video').length > 0) {
                $('#video')[0].pause();
            }
            $('#fill').remove();
            $('body').removeClass('noscroll');
        });

        // Close on escape
        $('#fill').on('keyup', function(e) {
            if (e.keyCode === 27) { // esc
                if ($('#inner #video').length > 0) {
                    $('#video')[0].pause();
                }
                $('#fill').remove();
                $('body').removeClass('noscroll');
                origin.trigger('focus');
            }
        });
    }
})();
