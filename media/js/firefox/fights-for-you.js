/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var client = Mozilla.Client;
    var survey = document.getElementById('fffy-survey-link');
    if (survey && !client.isMobile && Math.random() < 0.5) {
        var link = survey.querySelector('a');
        var linkHref = link.getAttribute('href');

        // show survey
        survey.style.display = 'block';
        window.dataLayer.push({
            'eLabel': 'Banner Impression',
            'data-banner-name': 'FFFY Survey Link',
            'data-banner-impression': '1',
            'event': 'non-interaction'
        });

        // survey tracking
        link.setAttribute('href', linkHref + window.location.search);
        link.addEventListener('click', function() {
            window.dataLayer.push({
                'eLabel': 'Banner Clickthrough',
                'data-banner-name': 'FFFY Survey Link',
                'data-banner-click': '1',
                'event': 'in-page-interaction'
            });
        }, false);
    }

    // Set up modal for the Focus link
    var focusContent = document.getElementById('fffy-focus-modal');
    var focusTrigger = document.querySelector('.fffy-t-focus .mzp-c-cta-link');
    var focusTitle = focusContent.querySelector('.c-modal-title');

    focusTrigger.addEventListener('click', function(e) {
        e.preventDefault();
        Mzp.Modal.createModal(e.target, focusContent, {
            title: focusTitle.innerHTML,
            className: 'mzp-t-firefox l-compact',
            closeText: window.Mozilla.Utils.trans('global-close'),
        });

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'Download Firefox Focus'
        });
    }, false);

})();

(function() {
    'use strict';

    /* global YT */
    /* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

    var content = document.getElementById('fffy-video-modal');
    var button = document.getElementById('fffy-video-button');
    var player = document.getElementById('fffy-video-player');
    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    function onYouTubeIframeAPIReady() {
        // lazy load video when visitor clicks the button
        var videoId = button.getAttribute('data-id');

        button.setAttribute('role', 'button');

        button.addEventListener('click', function(e) {
            e.preventDefault();

            var ytPlayer = new YT.Player(player, {
                height: '703',
                width: '1250',
                videoId: videoId,
                playerVars: {
                    modestbranding: 1, // hide YouTube logo.
                    rel: 0, // do not show related videos on end.
                },
                events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });

            Mzp.Modal.createModal(e.target, content, {
                title: 'Firefox Fights For You',
                className: 'mzp-has-media',
                closeText: 'Close modal',
                onDestroy: function() {
                    ytPlayer.destroy();
                }
            });

            function onPlayerReady(event) {
                event.target.playVideo();
            }

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
                    Mzp.Modal.closeModal();
                    break;
                }

                if (state) {
                    window.dataLayer.push({
                        'event': 'video-interaction',
                        'videoTitle': 'Firefox Fights For You',
                        'interaction': state
                    });
                }
            }
        });
    }

    Mozilla.fffyOnYouTubeIframeAPIReady = onYouTubeIframeAPIReady;
})();

// YouTube API hook has to be in global scope
function onYouTubeIframeAPIReady() {
    'use strict';

    Mozilla.fffyOnYouTubeIframeAPIReady();
}
