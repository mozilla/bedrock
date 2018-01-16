/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global Waypoint */
/* eslint no-unused-vars: [2, { "varsIgnorePattern": "[wW]aypoint" }] */


(function($) {
    'use strict';

    var $document = $(document);
    var $html = $(document.documentElement);
    var utils = Mozilla.Utils;

    var $gridVideo = $('#grid-video');
    var frameSrc = $gridVideo.data('frameSrc');

    var featureQueriesSupported = typeof CSS !== 'undefined' && typeof CSS.supports !== 'undefined';

    if (window.Mozilla.Client.isFirefox) {
        if (featureQueriesSupported && CSS.supports('display', 'grid')) {
            $html.addClass('firefox-has-grid');
        } else {
            $html.addClass('old-firefox');
            $gridVideo.attr('src', frameSrc);
        }
    } else {
        $html.addClass('not-firefox');
        $gridVideo.attr('src', frameSrc);
    }

    if (window.Mozilla.Client.isMobile) {
        $html.addClass('not-desktop');
    }


    var tallMode = false;

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
    }


    // Scroll smoothly to the linked section
    $document.on('click', '#page-nav .page-nav-menu a[href^="#"]', function(e) {
        e.preventDefault();
        // Extract the target element's ID from the link's href.
        var elem = $(this).attr('href').replace(/.*?(#.*)/g, '$1');
        var offset = $(elem).offset().top;

        Mozilla.smoothScroll({
            top: offset
        });
    });


    // Switch demo styles
    $document.on('click', '.demo-controls .example-switch', function() {
        var demoId = $(this).parents('.demo-section').attr('id');
        var demo = $('#' + demoId);
        var switches = $(this).parents('.demo-controls').find('.example-switch');
        var newClass = $(this).data('example-class');

        demo.removeClass('example-1 example-2 example-3').addClass(newClass);
        switches.removeClass('active');
        $(this).addClass('active');

        window.dataLayer.push({
            'eAction': 'button click', // action
            'eLabel': demoId + ' - ' + newClass, // label
            'event': 'in-page-interaction'
        });
    });


    // Set up the sticky download bar
    var $fxdownload = $('#download-firefox');
    var buttonClose = '<button type="button" class="close" title="'+ utils.trans('global-close') +'">'+ utils.trans('global-close') +'</button>';

    // If the bar exists and the window is tall
    if (tallMode) {
        // Initiate the sticky download bar
        initStickyBar();

        // Unstick the download bar when we reach the footer
        var unstickBarWaypoint = new Waypoint({
            element: $('#colophon'),
            offset: '102%',
            handler: function(direction) {
                if ((direction === 'down') && (!$html.hasClass('download-closed'))) {
                    $fxdownload.removeClass('stuck').removeAttr('style').find('.close').remove();
                } else if ((direction === 'up') && (!$html.hasClass('download-closed'))) {
                    $fxdownload.addClass('stuck').append(buttonClose);
                    initUnstickBar();
                }
            }
        });
    }

    // Show the sticky download bar
    function initStickyBar() {
        setTimeout(function() {
            $fxdownload.addClass('stuck').append(buttonClose).css({ bottom: '-' + $fxdownload.height() + 'px' }).animate({ bottom: '0' }, 750);
            initUnstickBar();
        }, 500);
    }

    // Dismiss the sticky download bar
    function initUnstickBar() {
        $('#download-firefox button.close').on('click', function() {
            $fxdownload.animate({ bottom: '-' + $fxdownload.height() + 'px' }, 500, function() {
                $fxdownload.removeClass('stuck').removeAttr('style').find('.close').remove();
            });

            // A class lets us check if the bar was dismissed on purpose
            // so we don't show it again during scrolling
            $html.addClass('download-closed');
        });
    }

    // Count right clicks
    $(document).on('click', function(e) {
        if (e.button === 2) {
            window.dataLayer.push({
                'eAction': 'click',
                'eLabel': 'Right click',
                'event': 'in-page-interaction'
            });
        }
    });

})(window.jQuery);
