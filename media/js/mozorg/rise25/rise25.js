/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

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
})();
