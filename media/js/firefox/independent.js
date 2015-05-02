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

    //set up GA tracking through GTM
    $('#fx10-download .download-link').attr({'data-interaction': 'download-click', 'data-download-version': window.site.platform});

    // Initialize the video
    // Defined in /js/base/firefox-anniversary-video.js
    Mozilla.FirefoxAnniversaryVideo.init({
        'deferEmbed': false,
        'onPlay': function() {
            Mozilla.FirefoxAnniversaryVideo.playEmbed();
            Mozilla.FirefoxAnniversaryVideo.setFooterButton('share');
            window.dataLayer.push({
                event: 'video-interaction',
                interaction: 'click to play',
                videoTitle: '10th Anniversary'
            });
        },
        'onComplete': function() {
            Mozilla.FirefoxAnniversaryVideo.setOverlayButtons('replay');
            Mozilla.FirefoxAnniversaryVideo.hideEmbed();
            window.dataLayer.push({
                event: 'video-interaction',
                interaction: 'Finish',
                videoTitle: '10th Anniversary'
            });
        }
    });

    // Autoplay if URL includes the proper hash and client is not a known mobile OS
    if (window.location.href.indexOf('#play') > -1 && !$html.hasClass('android') && !$html.hasClass('ios') && !$html.hasClass('fxos')) {
        Mozilla.FirefoxAnniversaryVideo.playEmbed();
        window.dataLayer.push({
            event: 'video-interaction',
            interaction: 'autoplay',
            videoTitle: '10th Anniversary'
        });
    }

})(window.jQuery);
