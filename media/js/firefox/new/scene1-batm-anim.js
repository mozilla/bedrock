/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var title = $('#main-header-copy');
    var exp = title.data('experience');
    var variant = title.data('variant');
    var mqDesktop;
    var buttonOpen = '<button type="button" class="open" title="'+ Mozilla.Utils.trans('global-open') +'">'+ Mozilla.Utils.trans('global-open') +'</button>';
    var buttonNext = '<button type="button" class="next" title="'+ Mozilla.Utils.trans('global-next') +'">'+ Mozilla.Utils.trans('global-next') +'</button>';
    var allPoints = $('.points .label');
    var point1 = $('#point-1 .label');
    var point2 = $('#point-2 .label');
    var point3 = $('#point-3 .label');

    $('.download-link').each(function(i, link) {
        if (exp && variant && link.href.indexOf('scene=2') > -1) {
            // specify v=1 template for scene 2
            link.href = link.href.replace('scene=2', 'scene=2&xv=' + exp + '&v=' + variant);
        }
    });

    // trigger fade-in CSS animation
    $(function() {
        $('html').addClass('ready');
    });

    if (typeof matchMedia !== 'undefined') {
        // Set desktop media query
        mqDesktop = matchMedia('(min-width: 1000px)');

        // Fire the points for desktop and up
        if (mqDesktop.matches) {
            setupPoints();
        }

        // Set or unset points on resize
        mqDesktop.addListener(function(mq) {
            if (mq.matches) {
                setupPoints();
            } else {
                unsetPoints();
            }
        });
    }

    // Set up three points, two with buttons
    function setupPoints() {
        $(buttonOpen).insertBefore([point1, point2]); // Add the open buttons
        $(buttonNext).appendTo([point1, point2]); // Add the next buttons

        var point1Next = point1.find('.next');
        var point2Next = point2.find('.next');

        // Show the first point
        point1.show();

        // Hide point 1, show point 2
        point1Next.on('click', function() {
            point1.fadeOut(100);
            point2.fadeIn(100, function() {
                trackPoints(point2.data('point'));
            }).attr('tabindex', -1).focus();
        });

        // Hide point 2, show point 3
        point2Next.on('click', function() {
            point2.fadeOut(100);
            point3.fadeIn(100, function() {
                trackPoints(point3.data('point'));
            }).attr('tabindex', -1).focus();
        });

        // Hide all points and just show the clicked one
        $('.point .open').on('click', function() {
            allPoints.fadeOut();
            $(this).next('.label').fadeIn(100, function() {
                trackPoints($(this).data('point'));
            }).attr('tabindex', -1).focus();
        });
    }

    // Reset all points to default state and remove buttons.
    function unsetPoints() {
        allPoints.attr('style', '');
        $('.points > .point').find('button.open, button.next').remove();
    }

    function trackPoints(point) {
        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'popup interaction',
            'eLabel': 'Show ' + point
        });
    }

})(window.jQuery);
