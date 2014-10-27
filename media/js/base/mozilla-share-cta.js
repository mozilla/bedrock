/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function() {
    'use strict';

    var $shares = $('.mozilla-share-cta');
    var $allLinks = $('.mozilla-share-cta ul');
    var showTimeout;

    $shares.each(function(share) {
        var $this = $(share);
        $this.css('height', $this.find('h3'));
    });

    function showLinks($share) {
        var $heading = $share.find('h3');

        $share.addClass('reveal');
        $heading.addClass('out');

        clearTimeout(showTimeout);
        showTimeout = setTimeout(function () {
            $heading.css('visibility', 'hidden');
            $share.find('ul').css('visibility', 'visible').addClass('in');
        }, 200);
    }

    function hideLinks($share) {
        var $links = $share.find('ul');

        $share.removeClass('reveal');
        $links.removeClass('in');

        clearTimeout(showTimeout);
        showTimeout = setTimeout(function () {
            $links.css('visibility', 'hidden');
            $share.find('h3').css('visibility', 'visible').removeClass('out');
        }, 200);
    }

    $shares.on('mouseenter focusin', function() {
        var $this = $(this);
        if (!$this.hasClass('reveal')) {
            showLinks($this);
        }
    });

    $shares.on('mouseleave', function() {
        var $this = $(this);
        if ($this.hasClass('reveal')) {
            hideLinks($this);
        }
    });

    $shares.on('focusout', function(e) {
        var $this = $(this);
        // only toggle state if target is last link in list
        if ($this.hasClass('reveal') && $(e.target).parent().is('li:last-child')) {
            hideLinks($this);
        }
    });

    $allLinks.find('a').on('click', function (e) {
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
