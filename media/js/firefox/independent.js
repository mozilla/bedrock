/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


;(function($) {
    'use strict';

    var $html = $('html');

    // Defined in global.js
    if (!isFirefox()) {
        $('#fx10-download').show();
    }

    $('#fx10-download .download-link').on('click', function(e) {
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Firefox Downloads', 'download click', window.site.platform]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Firefox Downloads', 'download click', window.site.platform], callback);
        }
    });

    // Initialize the video
    // Defined in /js/base/firefox-anniversary-video.js
    Mozilla.FirefoxAnniversaryVideo.init({
        'deferEmbed': false,
        'onPlay': function() {
            Mozilla.FirefoxAnniversaryVideo.playEmbed();
            Mozilla.FirefoxAnniversaryVideo.setFooterButton('share');
            gaTrack(['_trackEvent', '/firefox/independent/ Interactions', 'click to play', '10th Anniversary Video']);
        },
        'onComplete': function() {
            Mozilla.FirefoxAnniversaryVideo.setOverlayButtons('replay');
            Mozilla.FirefoxAnniversaryVideo.hideEmbed();
            gaTrack(['_trackEvent', '/firefox/independent/ Interactions', 'Finish', '10th Anniversary Video']);
        }
    });

    // Autoplay if URL includes the proper hash and client is not a known mobile OS
    if (window.location.href.indexOf('#play') > -1 && !$html.hasClass('android') && !$html.hasClass('ios') && !$html.hasClass('fxos')) {
        Mozilla.FirefoxAnniversaryVideo.playEmbed();
        gaTrack(['_trackEvent', '/firefox/independent/ Interactions', 'autoplay', '10th Anniversary Video']);
    }

})(window.jQuery);
