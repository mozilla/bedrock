/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    function generateTweet() {
        var tweetUrl = encodeURIComponent(
            'https://mozilla.org/rise25?utm_campaign=rise25&utm_medium=organicsocial&utm_source=twitter&utm_content=rise25-share'
        );
        var tweetText = encodeURIComponent('Hey');
        return (
            'https://www.twitter.com/intent/tweet?url=' +
            tweetUrl +
            '&text=' +
            tweetText
        );
    }

    function generateFacebookShare() {
        var shareUrl = encodeURIComponent(
            'https://mozilla.org/rise25?utm_campaign=rise25&utm_medium=organicsocial&utm_source=facebook&utm_content=rise25-share'
        );
        var shareText = encodeURIComponent('Hey');
        return (
            'https://facebook.com/sharer.php?u=' +
            shareUrl +
            '&quote=' +
            shareText
        );
    }

    function handleCopyLink(e) {
        e.preventDefault;
        navigator.clipboard.writeText('https://mozilla.com/rise25');
    }

    var facebookShare = document.querySelectorAll('.social-share .facebook');
    var twitterShare = document.querySelectorAll('.social-share .twitter');
    var emailShare = document.querySelectorAll('.social-share .email');
    var copyLinks = document.querySelectorAll('.social-share .copy-text');

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
        var subject = encodeURIComponent('');
        var body = encodeURIComponent('');
        for (var index = 0; index < emailShare.length; index++) {
            var element = emailShare[index];
            element.href =
                'mailto:example@website.com?subject=' +
                subject +
                '&body=' +
                body;
        }
    })();

    for (var index = 0; index < copyLinks.length; index++) {
        var element = copyLinks[index];
        element.addEventListener('click', handleCopyLink);
    }

    var video = document.querySelector('.rise25-hero video');

    video.addEventListener('ended', function () {
        video.currentTime = 0;
    });
})();
