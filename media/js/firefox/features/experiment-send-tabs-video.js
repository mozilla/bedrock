/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global YT */
/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope
function onYouTubeIframeAPIReady() {
    'use strict';

    Mozilla.firefoxFeaturesSendTabsOnYouTubeIframeAPIReady();
}

(function($) {
    var variation = (window.location.search.indexOf('v=a') > -1) ? 'a' : 'b';
    var $videoContainer = $('#video-wrap');

    // add experiment details to dataLayer at page load
    window.dataLayer.push({
        'data-ex-experiment': 'firefox-sync-videoPresent',
        'data-ex-variant': variation,
        'data-ex-present': 'true'
    });

    function onYouTubeIframeAPIReady() {
        var video = $videoContainer.find('.video')[0];

        new YT.Player(video, {
            height: '390',
            width: '640',
            videoId: 'CM40b14i41M',
            events: {
                'onStateChange': onPlayerStateChange
            }
        });

        function onPlayerStateChange(event) {
            var state;

            switch(event.data) {
            case YT.PlayerState.PLAYING:
                state = 'video play';
                break;
            case YT.PlayerState.PAUSED:
                state = 'video paused';
                break;
            case YT.PlayerState.ENDED:
                state = 'video complete';
                break;
            }

            if (state) {
                window.dataLayer.push({
                    'event': 'video-interaction',
                    'videoTitle': 'send tabs video',
                    'interaction': state
                });
            }
        }
    }

    if ($videoContainer.length) {
        var tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';

        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        Mozilla.firefoxFeaturesSendTabsOnYouTubeIframeAPIReady = onYouTubeIframeAPIReady;
    }

})(window.jQuery);
