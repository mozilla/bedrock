/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function() {
    'use strict';

    var $share = $('#mozilla-share-cta');
    var $heading = $share.find('h3');
    var $links = $share.find('ul');
    var showTimeout;

    $share.css('height', $heading.outerHeight());

    function showLinks() {
        $share.addClass('reveal');
        $heading.addClass('out');

        clearTimeout(showTimeout);
        showTimeout = setTimeout(function () {
            $heading.css('visibility', 'hidden');
            $links.css('visibility', 'visible').addClass('in');
        }, 200);
    }

    function hideLinks() {
        $share.removeClass('reveal');
        $links.removeClass('in');

        clearTimeout(showTimeout);
        showTimeout = setTimeout(function () {
            $links.css('visibility', 'hidden');
            $heading.css('visibility', 'visible').removeClass('out');
        }, 200);
    }

    $share.on('mouseenter focusin', function() {
        if (!$share.hasClass('reveal')) {
            showLinks();
        }
    });

    $share.on('mouseleave', function() {
        if ($share.hasClass('reveal')) {
            hideLinks();
        }
    });

    $share.on('focusout', function(e) {
        // only toggle state if target is last link in list
        if ($share.hasClass('reveal') && $(e.target).parent().is('li:last-child')) {
            hideLinks();
        }
    });

    $links.find('a').on('click', function (e) {
        var $this = $(this);
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Share CTA Interactions', 'Social link click', $this.attr('title')]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Share CTA Interactions', 'Social link click', $this.attr('title')], callback);
        }
    });
});
