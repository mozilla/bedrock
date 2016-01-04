/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var $document = $(document);
    var $body = $('body');

    if (window.Mozilla.Client.isFirefox) {
        $body.addClass('is-firefox');
    } else {
        $body.addClass('not-firefox');
    }

    var tallMode = false;
    var wideMode = false;

    if (typeof matchMedia !== 'undefined') {
        // Check window height
        var queryTall = matchMedia('(min-height: 650px)');
        if (queryTall.matches) {
            tallMode = true;
        } else {
            tallMode = false;
        }

        queryTall.addListener(function(mq) {
            if (mq.matches) {
                tallMode = true;
            } else {
                tallMode = false;
            }
        });

        // Check window width
        var queryWide = matchMedia('(min-width: 760px)');
        if (queryWide.matches) {
            wideMode = true;
        } else {
            wideMode = false;
        }

        queryWide.addListener(function(mq) {
            if (mq.matches) {
                wideMode = true;
            } else {
                wideMode = false;
            }
        });
    }

    // Set up the sticky header
    var $pageHeader = $('.page-header');

    if (($pageHeader.length > 0) && wideMode) {
        var stickyHeader = new Waypoint.Sticky({
            element: $pageHeader,
            offset: -16
        });
    }

    // Set up the sticky footer
    var $doSection = $('#do');
    var $pageFooter = $('#footer-cta');
    var buttonClose = '<button type="button" class="close" title="'+ window.trans('global-close') +'">'+ window.trans('global-close') +'</button>';

    if (($pageFooter.length > 0) && tallMode) {
        // Stick the footer when we're near the end of the page
        var stickyFooter = new Waypoint({
            element: $doSection,
            offset: '-80%',
            handler: function(direction) {
                if ((direction === 'down') && (!$body.hasClass('footer-closed'))) {
                    // slide up when scrolling down
                    $pageFooter.addClass('stuck').append(buttonClose).css({ bottom: '-' + $pageFooter.height() + 'px' }).animate({ bottom: '0' }, 750);
                    initFooterClose();
                } else if ((direction === 'up') && (!$body.hasClass('footer-closed'))) {
                    // slide down when scrolling up, then unstick
                    $pageFooter.animate({ bottom: '-' + $pageFooter.height() + 'px' }, 500, function() {
                        $pageFooter.removeClass('stuck').removeAttr('style').find('button.close').remove();
                    });
                }
            }
        });

        // Unstick the footer when we reach the bottom
        var unstickyFooter = new Waypoint({
            element: $('#colophon'),
            offset: '100%',
            handler: function(direction) {
                if ((direction === 'down') && (!$body.hasClass('footer-closed'))) {
                    $pageFooter.removeClass('stuck').find('button.close').remove();
                } else if ((direction === 'up') && (!$body.hasClass('footer-closed'))) {
                    $pageFooter.addClass('stuck').append(buttonClose);
                    initFooterClose();
                }
            }
        });
    }

    // Dismiss the sticky footer
    function initFooterClose() {
        var footerVisible = $('#footer-cta > .content:visible').data('footer-name');
        var footerDetails = $('.footer-cta #form-details, .footer-cta .form-details');

        $('.footer-cta .close').on('click', function() {
            if (tallMode && wideMode) {
                $pageFooter.animate({ bottom: '-' + $pageFooter.height() + 'px' }, 500, function() {
                    $pageFooter.removeClass('stuck').removeAttr('style').find('.close').remove();
                });
            } else {
                $pageFooter.removeClass('stuck').removeAttr('style').find('.close').remove();
            }

            // Close the form if it's open
            if (footerDetails.is(':visible')) {
                footerDetails.slideUp('fast');
            }

            // A class lets us check if the footer was dismissed on purpose
            // so we don't show it again during scrolling
            $body.addClass('footer-closed');

            // Track it and record which one was visible
            window.dataLayer.push({
                'event': 'smarton-interactions',
                'interaction': 'dismiss sticky footer',
                'footer': footerVisible
            });
        });
    }

    // Scroll smoothly to the linked section
    $document.on('click', '.nav-steps a[href^="#"]', function(e) {
        e.preventDefault();
        // Extract the target element's ID from the link's href.
        var elem = $(this).attr('href').replace(/.*?(#.*)/g, '$1');
        var offset = $(elem).offset().top;

        if (tallMode && wideMode) {
            offset = $(elem).offset().top - $pageHeader.height();
        } else {
            offset = $(elem).offset().top;
        }

        Mozilla.smoothScroll({
            top: offset
        });
    });

    // Change the navbar current item to match the section waypoint
    function navState(current, previous) {
        return function(direction) {
            if (direction === 'down') {
                $pageHeader.find('.nav-steps li').removeClass();
                $('#nav-step-' + current).addClass('current');
            }
            else {
                $pageHeader.find('.nav-steps li').removeClass();
                $('#nav-step-' + previous).addClass('current');
            }
        };
    }

    if ($pageHeader.length > 0) {
        //Fire the waypoints for each section, passing classes for the current and previous sections
        $('#ask').waypoint(navState('ask', 'ask'), { offset: $pageHeader.height() + 10 });
        $('#know').waypoint(navState('know', 'ask'), { offset: $pageHeader.height() + 10 });
        $('#do').waypoint(navState('do', 'know'), { offset: $pageHeader.height() + 10 });
        $('#chat').waypoint(navState('chat', 'do'), { offset: $pageHeader.height() + 10 });
    }

    // Draw animated SVG pie charts
    // Requires /libs/circles.min.js - http://lugolabs.com/circles
    function drawCircle(circleId, circleVal) {
        Circles.create({
          id:                  circleId,
          value:               circleVal,
          radius:              70,
          maxValue:            100,
          width:               12,
          text:                function(value) {return value + '%';},
          duration:            850,
          wrpClass:            'circles-wrap',
          textClass:           'circles-text',
          valueStrokeClass:    'circles-valueStroke',
          maxValueStrokeClass: 'circles-maxValueStroke',
          styleWrapper:        false,
          styleText:           false,
        });
    }

    // Trigger the chart when it scrolls into view
    $('.sidebar-chart').each(function() {
        var stage = $(this).children('.chart-stage');
        var circleId = stage.attr('id');
        var circleVal = stage.data('chart-value');
        var chart = new Waypoint({
            element: stage,
            handler: function(direction) {
                if (direction === 'down') {
                    drawCircle(circleId, circleVal);
                }
            },
            offset: '100%'
        });
    });

    // Track user scrolling through each section down the page
    $('.main .section').each(function() {
        var sectionId = $(this).attr('id');
        var waypoint = new Waypoint({
            element: $(this),
            handler: function(direction) {
                if (direction === 'down') {
                    window.dataLayer.push({
                        'event': 'smarton-interactions',
                        'interaction': 'scroll',
                        'section': sectionId
                    });
                }
            },
            offset: '100%'
        });
    });

    // Track which questions get tweeted
    $('.section-chat .button-tweet').on('click', function() {
        var question = $(this).parents('li').find('.chat-question').text();
        window.dataLayer.push({
            'event': 'smarton-interactions',
            'interaction': 'tweet this question',
            'question': question
        });
    });

})(window.jQuery);

