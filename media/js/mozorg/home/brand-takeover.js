/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global YT */
/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope
function onYouTubeIframeAPIReady() {
    'use strict';

    Mozilla.brandTakeOverOnIframeAPIReady();
}

(function($) {
    'use strict';

    var $body = $('body');
    var $takeoverModal = $('#brand-takeover');
    var $overlay = $('.page-overlay');
    var $closeModal = $('#close-takeover');
    var $videoPlaceholderButton = $('#video-placeholder-button');
    var isIOS = $('html').hasClass('ios');
    var player;

    function initYouTubeIframeAPI() {
        var tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';

        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }

    function onIframeAPIReady() {
        /*
         * iOS can only play framed video as a result of a user initiated click,
         * so instead of showing the placeholder just let them initiate normally.
         */
        if (isIOS) {
            loadVideo();
        } else {
            /*
             * For everyone else only load the YouTube video once the user clicks
             * the placeholder image.
             */
            $videoPlaceholderButton.on('click', function(e) {
                e.preventDefault();
                loadVideo();
            });
        }
    }

    function loadVideo() {

        var $videoContainer = $('#video-container');
        var video = $videoContainer.find('.video');

        player = new YT.Player(video.get(0), {
            height: '720',
            width: '1280',
            videoId: video.data('videoId'),
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
            },
            playerVars: {
                'showinfo': 0,
                'modestbranding': 1,
                'rel': 0
            }
        });

        function onPlayerReady(event) {
            $videoPlaceholderButton.addClass('hidden');
            $takeoverModal.addClass('dark');
            if (!isIOS) {
                event.target.playVideo();
            }
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
                break;
            }

            if (state) {
                window.dataLayer.push({
                    'event': 'video-interaction',
                    'videoTitle': 'mozilla brand',
                    'interaction': state
                });
            }
        }
    }

    Mozilla.brandTakeOverOnIframeAPIReady = onIframeAPIReady;

    // sets the mozorg.takeover state to true indicating that the user has
    // seen the takeover modal during their current session.
    function storeSession() {
        try {
            sessionStorage.setItem('mozorg.takeover.seen', 'true');
        } catch (ex) {
            // yum, errors taste nice ;)
        }
    }

    // Shows and hides the takeover modal
    // Removes the keyup event from body if specified
    function toggleModal(removeListener) {
        if (removeListener) {
            // no longer listen for keyup events.
            $body.off('keyup.takeover');
            // destroy youtube video.
            if (player) {
                player.destroy();
            }
        }

        $([$takeoverModal, $overlay]).each(function() {
            $(this).toggleClass('hidden');
        });
    }

    // Shows the take over modal, sets the required entry in
    // session storage and adds an `esc` key handler to close
    // the modal.
    function initTakeOver() {
        // load YouTube iFrame API
        initYouTubeIframeAPI();

        // show the takeover
        toggleModal();

        // set mozorg.takeover.seen to true
        storeSession();

        // trap key events, listening for escape.
        // we only want to do this here so, we do not attach the event
        // if we are not showing the modal.
        $body.on('keyup.takeover', function(event) {
            if (event.key === 'Escape' || event.keyCode === 27) {
                // close the modal
                toggleModal(true);
            }
        });

        $overlay.on('click', function(){
            toggleModal();
        });
    }

    // If a user clicks on 'continue to mozilla.org',
    // close the modal and overlay
    $closeModal.on('click', function(event) {
        event.preventDefault();
        toggleModal(true);
    });

    // Modal is waffled so first ensure it exists.
    if ($takeoverModal.length > 0) {
        try {
            // only show the takeover modal if the user has not already seen it
            // during this session.
            if (sessionStorage.getItem('mozorg.takeover.seen') !== 'true') {
                initTakeOver();
            }
        } catch (ex) {
            // Nothing to see here
        }
    }

    $('html').addClass('brand-takeover-loaded');

})(jQuery);
