/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope, ugh.
window.onYouTubeIframeAPIReady = function () {
    'use strict';

    // Play the video only once the API is ready.
    Mozilla.heroVideoPlay();
};

(function () {
    'use strict';

    var facebookShare = document.querySelectorAll(
        '.r25-c-social-share .facebook'
    );
    var twitterShare = document.querySelectorAll(
        '.r25-c-social-share .twitter'
    );
    var emailShare = document.querySelectorAll('.r25-c-social-share .email');
    var copyLinks = document.querySelectorAll('.r25-c-social-share .copy-text');
    var timeout;

    function generateTweet() {
        var tweetUrl = encodeURIComponent(
            'https://www.mozilla.org/rise25/nominate/?utm_campaign=rise25&utm_medium=organicsocial&utm_source=twitter&utm_content=rise25-share'
        );
        var tweetText = encodeURIComponent(
            'Mozilla is on the hunt for 25 visionaries making AI better for the people — not big corporations. \n\nWinners will be honored at the upcoming Rise25 awards in Dublin, Ireland. Submit your nomination today! \n\n'
        );
        return (
            'https://www.twitter.com/intent/tweet?url=' +
            tweetUrl +
            '&text=' +
            tweetText
        );
    }

    function generateFacebookShare() {
        var shareUrl = encodeURIComponent(
            'https://www.mozilla.org/rise25/nominate/?utm_campaign=rise25&utm_medium=organicsocial&utm_source=facebook&utm_content=rise25-share'
        );
        var shareText = encodeURIComponent(
            'Mozilla is on the hunt for 25 visionaries making AI better for the people — not big corporations. \n\nWinners will be honored at the upcoming Rise25 awards in Dublin, Ireland. Submit your nomination today! \n\n'
        );
        return (
            'https://facebook.com/sharer.php?u=' +
            shareUrl +
            '&quote=' +
            shareText
        );
    }

    function handleCopyLink(e) {
        e.preventDefault;
        navigator.clipboard.writeText(
            'https://www.mozilla.com/rise25/nominate/'
        );

        var copyText = e.currentTarget.querySelector('.social-share-copy');
        var copiedText = e.currentTarget.querySelector('.social-share-copied');

        clearTimeout(timeout);

        copiedText.style.display = 'block';
        copyText.style.display = 'none';

        timeout = setTimeout(function () {
            copiedText.style.display = 'none';
            copyText.style.display = 'block';
        }, 2000);
    }

    // used iifies to set attributes since the variables for `index` was being overwritten by each other
    (function () {
        for (var index = 0; index < facebookShare.length; index++) {
            var element = facebookShare[index];
            element.href = generateFacebookShare();
        }
    })();

    (function () {
        for (var index = 0; index < twitterShare.length; index++) {
            var element = twitterShare[index];
            element.href = generateTweet();
        }
    })();

    (function () {
        var subject = encodeURIComponent('Who will you nominate for Rise 25?');
        var body = encodeURIComponent(
            'Mozilla is searching for 25 visionaries making AI better for the people — not big corporations. Seeking individuals across 5 categories: Advocates, Builders, Artists, Entrepreneurs, and Change Agents. \n\nWinners will be honored at the upcoming Rise25 awards in Dublin, Ireland. Nominations close March 29. Get your nomination in today! \n\nNominate someone: https://www.mozilla.org/rise25/nominate/'
        );
        for (var index = 0; index < emailShare.length; index++) {
            var element = emailShare[index];
            element.href = 'mailto:?subject=' + subject + '&body=' + body;
        }
    })();

    for (var index = 0; index < copyLinks.length; index++) {
        var element = copyLinks[index];
        element.addEventListener('click', handleCopyLink);
    }

    // Video
    var heroVideo = document.querySelector('.r25-hero .video-player');
    var videoTitle = heroVideo.getAttribute('data-video-title');
    var videoId = heroVideo.getAttribute('data-video-id');
    var src = 'https://www.youtube.com/iframe_api';
    var player;

    function loadScript() {
        var tag = document.createElement('script');
        tag.src = src;
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }

    function isScriptLoaded() {
        return document.querySelector('script[src="' + src + '"]')
            ? true
            : false;
    }

    function playVideo() {
        // if youtube API fails or is blocked, try redirecting to youtube.com
        if (typeof window.YT === 'undefined') {
            window.location.href = 'https://www.youtube.com/watch?v=' + videoId;
        }

        player = new window.YT.Player(heroVideo, {
            width: 640,
            height: 360,
            videoId: videoId,
            playerVars: {
                modestbranding: 1, // hide YouTube logo.
                rel: 0 // do not show related videos on end.
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
            var state;

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
                    videoTitle: videoTitle,
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

    function destroyVideoPlayer() {
        if (player) {
            player.destroy();
        }
    }

    function openVideoModal(e) {
        e.preventDefault();

        var content = document.querySelector('.mzp-u-modal-content');

        window.MzpModal.createModal(e.target, content, {
            title: videoTitle,
            className: 'mzp-has-media',
            onCreate: initVideoPlayer,
            onDestroy: destroyVideoPlayer
        });
    }

    function initVideo() {
        var heroVideoButtons = document.querySelectorAll(
            '.r25-hero .js-video-play'
        );

        for (var i = 0; i < heroVideoButtons.length; i++) {
            heroVideoButtons[i].setAttribute('role', 'button');
            heroVideoButtons[i].addEventListener(
                'click',
                openVideoModal,
                false
            );
        }
    }

    Mozilla.heroVideoPlay = playVideo;

    if (heroVideo) {
        initVideo();
    }
})();
