/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

(function () {
    'use strict';

    let timeout;

    function isDefaultBrowser() {
        return new window.Promise((resolve, reject) => {
            window.Mozilla.UITour.getConfiguration('appinfo', (details) => {
                if (details.defaultBrowser) {
                    resolve();
                } else {
                    reject();
                }
            });
        });
    }

    function showDefault() {
        clearTimeout(timeout);
        document.querySelector('.wnp-main-cta').classList.add('hide');

        // UA
        window.dataLayer.push({
            event: 'non-interaction',
            eAction: 'whatsnew-116',
            eLabel: 'firefox-default'
        });

        // GA4
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_default: true
        });
    }

    function showNotDefault() {
        clearTimeout(timeout);
        document.querySelector('.wnp-main-cta').classList.add('show');

        // UA
        window.dataLayer.push({
            event: 'non-interaction',
            eAction: 'whatsnew-116',
            eLabel: 'firefox-not-default'
        });

        // GA4
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_default: false
        });
    }

    function initDefault() {
        // show not default CTA after 2 seconds as a fallback.
        timeout = window.setTimeout(showNotDefault, 2000);

        isDefaultBrowser().then(showDefault).catch(showNotDefault);
    }

    if (
        typeof window.Mozilla.Client !== 'undefined' &&
        typeof window.Mozilla.UITour !== 'undefined' &&
        window.Mozilla.Client.isFirefoxDesktop
    ) {
        initDefault();
    } else {
        // Hide the make default button if other checks fail
        document.querySelector('.wnp-default').classList.add('hide');
    }
})();

// YouTube API hook has to be in global scope
window.onYouTubeIframeAPIReady = () => {
    'use strict';

    // Play the video only once the API is ready.
    Mozilla.pipVideoPlay();
};

(function () {
    'use strict';

    const videoLink = document.querySelector('.js-video-play');
    const src = 'https://www.youtube.com/iframe_api';

    function loadScript() {
        const tag = document.createElement('script');
        tag.src = src;
        const firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }

    function isScriptLoaded() {
        return document.querySelector('script[src="' + src + '"]')
            ? true
            : false;
    }

    function playVideo() {
        const videoId = videoLink.getAttribute('data-id');
        const title = videoLink.getAttribute('data-video-title');

        // return early if youtube API fails to load or is blocked.
        if (typeof window.YT === 'undefined') {
            return;
        }

        new window.YT.Player(videoLink, {
            width: 500,
            height: 281,
            videoId: videoId,
            playerVars: {
                modestbranding: 1, // hide YouTube logo.
                rel: 0, // do not show related videos on end.
                cc_load_policy: 1 // show captions.
            },
            events: {
                onReady: onPlayerReady,
                onStateChange: onPlayerStateChange
            }
        });

        function onPlayerReady(event) {
            event.target.playVideo();
        }

        function onPlayerStateChange(event) {
            let state;

            switch (event.data) {
                case window.YT.PlayerState.PLAYING:
                    state = 'video play';
                    break;
                case window.YT.PlayerState.PAUSED:
                    state = 'video paused';
                    break;
                case window.YT.PlayerState.ENDED:
                    state = 'video complete';
                    break;
            }

            if (state) {
                window.dataLayer.push({
                    event: 'video-interaction',
                    videoTitle: title,
                    interaction: state
                });
            }
        }
    }

    function initVideoPlayer() {
        // check to see if you youtube API is loaded before trying to play the video.
        if (!isScriptLoaded()) {
            loadScript();
        } else {
            playVideo();
        }
    }

    function init() {
        videoLink.setAttribute('role', 'button');

        videoLink.addEventListener(
            'click',
            function (e) {
                e.preventDefault();
                initVideoPlayer();
            },
            false
        );
    }

    Mozilla.pipVideoPlay = playVideo;

    init();
})();
