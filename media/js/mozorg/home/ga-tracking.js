/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    function trackGenericLink(action, href, callback) {
        if (typeof callback === 'function') {
            gaTrack(['_trackEvent', 'Homepage Interactions', action, href], callback);
        } else {
            gaTrack(['_trackEvent', 'Homepage Interactions', action, href]);
        }
    }

    function trackPromoTile(promoId, promoClass, promoName, callback) {
        gaTrack(['_setCustomVar', 10, 'Homepage Tile Position', promoId, 3]);
        gaTrack(['_setCustomVar', 11, 'Homepage Tile Size', promoClass, 3]);

        if (typeof callback === 'function') {
            gaTrack(['_trackEvent', 'Homepage Interactions', 'tile click', promoName], callback);
        } else {
            gaTrack(['_trackEvent', 'Homepage Interactions', 'tile click', promoName]);
        }
    }

    function trackDownloadButton(action, label, callback) {
        if (typeof callback === 'function') {
            gaTrack(['_trackEvent', 'Firefox Downloads', action, label], callback);
        } else {
            gaTrack(['_trackEvent', 'Firefox Downloads', action, label]);
        }
    }

    // track user scrolling through each section down the page
    $('.module').waypoint(function(direction) {
        if (direction === 'down') {
            var id = $(this).prop('id');
            gaTrack(['_trackEvent', 'Homepage Interactions', 'scroll', id]);
        }
    }, { offset: '100%' });

    // track clicks in main navigation
    $('#nav-main-menu li a').on('click', function(e) {
        var name = $(this).data('name');
        var href = this.href;
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var callback;

        if (newTab) {
            trackGenericLink('nav click', name);
        } else {
            e.preventDefault();
            callback = function() {
                window.location = href;
            };
            trackGenericLink('nav click', name, callback);
        }
    });

    // track large promo clicks
    $('.promo-large-portrait > a.panel-link, .promo-large-landscape > a.panel-link').on('click', function(e) {
        var $promo = $(this).parent();
        var id = $promo.prop('id');
        var promoName = $promo.data('name');
        var promoClass = $promo.hasClass('promo-large-portrait') ? 'portrait' : 'landscape';
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            trackPromoTile(id, 'promo-large-' + promoClass, promoName);
        } else {
            e.preventDefault();
            trackPromoTile(id, 'promo-large-' + promoClass, promoName, callback);
        }
    });

    // track small promo clicks
    $('.promo-small-landscape > a.panel-link').on('click', function(e) {
        var $promo = $(this).parent();
        var id = $promo.prop('id');
        var promoName = $promo.data('name');
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            trackPromoTile(id, 'promo-small-landscape', promoName);
        } else {
            e.preventDefault();
            trackPromoTile(id, 'promo-small-landscape', promoName, callback);
        }
    });

    // track Mozillian face clicks
    $('.promo-face > a').on('click', function(e) {
        var $promo = $(this).parent();
        var id = $promo.prop('id');
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            trackPromoTile(id, 'promo-face', 'Mozillians');
        } else {
            e.preventDefault();
            trackPromoTile(id, 'promo-face', 'Mozillians', callback);
        }
    });

    // track Tweet promo clicks
    $('.twt-actions > a').on('click', function(e) {
        var $this = $(this);
        var $promo = $this.closest('li');
        var id = $promo.prop('id');
        var action = $this.attr('title');
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            trackPromoTile(id, 'promo-small-landscape', 'Mozilla Tweets ' + action);
        } else {
            e.preventDefault();
            trackPromoTile(id, 'promo-small-landscape', 'Mozilla Tweets ' + action, callback);
        }
    });

    // track download firefox promo clicks
    $('.promo-small-landscape.firefox-download a.download-link').on('click', function(e) {
        var $this = $(this);
        var $promo = $this.closest('.promo-small-landscape');
        var id = $promo.prop('id');
        var isAndroid = $promo.find('li.os_android:visible').length > 0;
        var type = isAndroid ? 'Firefox Android' : 'Firefox Desktop';
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        gaTrack(['_setCustomVar', 10, 'Homepage Tile Position', id, 3]);
        gaTrack(['_setCustomVar', 11, 'Homepage Tile Size', 'promo-small-landscape', 3]);

        if (newTab) {
            trackDownloadButton('download click - top', type);
        } else {
            e.preventDefault();
            trackDownloadButton('download click - top', type, callback);
        }
    });

    // track Firefox download section button clicks
    $('#firefox-download-section a.download-link').on('click', function(e) {
        var $this = $(this);
        var isAndroid = $this.parent().hasClass('os_android');
        var type = isAndroid ? 'Firefox Android' : 'Firefox Desktop';
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            trackDownloadButton('download click - primary', type);
        } else {
            e.preventDefault();
            trackDownloadButton('download click - primary', type, callback);
        }
    });

    // track upcoming event link clicks
    $('#upcoming-events a').on('click', function(e) {
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            trackGenericLink('Upcoming Event Link Clicks', href);
        } else {
            e.preventDefault();
            trackGenericLink('Upcoming Event Link Clicks', href, callback);
        }
    });

    // track community section btc button clicks
    $('.contribute-btn').on('click', function(e) {
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            trackGenericLink('button click', 'Get Involved with Mozilla today');
        } else {
            e.preventDefault();
            trackGenericLink('button click', 'Get Involved with Mozilla today', callback);
        }
    });

    // track secondary link clicks
    $('#secondary-links a').on('click', function(e) {
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            trackGenericLink('Secondary Link Clicks', href);
        } else {
            e.preventDefault();
            trackGenericLink('Secondary Link Clicks', href, callback);
        }
    });

});
