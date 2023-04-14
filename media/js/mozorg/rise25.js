/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    var facebookShare = document.querySelectorAll('.social-share .facebook');
    var twitterShare = document.querySelectorAll('.social-share .twitter');
    var emailShare = document.querySelectorAll('.social-share .email');
    var copyLinks = document.querySelectorAll('.social-share .copy-text');
    var staticImage = document.querySelector('.hero-static-container');
    var video = document.querySelector('.rise25-hero video');
    var timeout;

    function generateTweet() {
        var tweetUrl = encodeURIComponent(
            'https://www.mozilla.org/rise25/?utm_campaign=rise25&utm_medium=organicsocial&utm_source=twitter&utm_content=rise25-share'
        );
        var tweetText = encodeURIComponent(
            'Mozilla is searching for the next 25 rising stars who are shaping the future of the internet for the better.\n\n Five people from five categories will be selected and honored at an upcoming event. Submit your nomination today!\n'
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
            'https://www.mozilla.org/rise25/?utm_campaign=rise25&utm_medium=organicsocial&utm_source=facebook&utm_content=rise25-share'
        );
        var shareText = encodeURIComponent(
            'Mozilla is searching for the next 25 rising stars who are shaping the future of the internet for the better.\n\n Five people from five categories will be selected and honored at an upcoming event. The categories are: Activists, Builders, Artists, Creators, and Activists. Submit your nomination today!\n'
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
        navigator.clipboard.writeText('https://www.mozilla.com/rise25/');

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
        var subject = encodeURIComponent(
            'Mozilla is looking for the next 25 rising stars'
        );
        var body = encodeURIComponent(
            'In search of the game-changers shaping the internet. \n\nHelp us find the visionaries and builders shaping the future of the internet. \n\nMozilla is searching for the next 25 rising stars who are shaping the future of the internet for the better. Five people from five categories will be selected and honored at an upcoming event. The categories are: Activists, Builders, Artists, Creators, and Activists. Who will you nominate? \n\n Submit your nominations: https://www.mozilla.org/rise25/'
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

    staticImage.addEventListener('click', function () {
        var imageHeight = getComputedStyle(
            document.querySelector('.hero-static-container')
        ).height;
        staticImage.style.display = 'none';
        video.style.height = imageHeight;
        video.style.display = 'block';
        video.play();
    });

    video.addEventListener('ended', function () {
        staticImage.style.display = 'block';
        video.style.display = 'none';
        video.currentTime = 0;
    });
})();
