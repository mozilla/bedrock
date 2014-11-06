/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

// Create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

// needs to be in the global scope
function onYouTubePlayerAPIReady() {
    'use strict';

    Mozilla.FirefoxAnniversaryVideo.initYouTubePlayer();
}

Mozilla.FirefoxAnniversaryVideo = (function($) {
    'use strict';

    var $html = $('html');

    var _isOldIE = (/MSIE\s[1-8]\./.test(navigator.userAgent));
    var _isIOS = $html.hasClass('ios');
    var _isAndroid = $html.hasClass('android');

    // holds configuration options
    var _opts = {};

    // valid states for each button group/container
    var _buttonStates = {
        'overlay': 'play replay play-share share-replay',
        'footer': 'share download none'
    };

    var _$buttonOverlay = $('#fx-anniversary-video-overlay');
    var _$embedWrapper = $('#fx-anniversary-video-embed-wrapper');
    var _$embedIframe = $('#fx-anniversary-video-embed');
    var _hasVideo = (_$embedIframe.length > 0);

    var _$overlayButtons = $('#fx-anniversary-video-buttons');
    var _$footerButtons = $('#fx-anniversary-video-footer-button');

    var _embedReady = false;
    var _youtubeAPIready = false;
    var _waitingToPlay = false;
    var _youtubePlayer;

    /*
    Injects YouTube script tag into page.
    */
    var _initYouTubeAPI = function() {
        var tag = document.createElement('script');
        tag.src = '//www.youtube.com/player_api';
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        _youtubeAPIready = true;
    };

    /*
    Initializes the video widget. Must be called on page load.

    @param Object options - An object literal containing optional config:
        onPlay Function: A function to execute when a play or replay
            button is clicked. Useful for playing the video or opening
            a modal containing the video.

        onComplete Function: A function to execute after the video has
            finished playing. Useful for updating and re-displaying buttons.

        deferEmbed Boolean: If true, do not set the src for the embed iframe
            (as setting src breaks tour for some reason).
    */
    var _init = function(config) {
        if (!_isOldIE) {
            // store config options
            _opts = config;

            _$overlayButtons.find('a.button-play').attr('role', 'button');

            // if a callback was passed, add listener to all play and replay buttons
            if (typeof _opts.onPlay === 'function') {
                _$overlayButtons.find('.button-play, .button-replay').on('click.fxanniversaryvideo', function(e) {
                    e.preventDefault();
                    _opts.onPlay(this);
                });
            }

            // if embed is present and deferEmbed is false, get embed ready for playback
            if (_hasVideo && !_opts.deferEmbed) {
                _enableEmbed();
            }
        } else {
            // hide all share buttons
            $('.mozilla-share-cta').hide();

            // show only the round play button
            _setButtonState(_$overlayButtons, 'overlay', 'play');
        }
    };

    var _setButtonState = function($buttonsContainer, buttonGroup, state) {
        // make sure state should change and a valid state was passed
        if (!$buttonsContainer.hasClass(state) && _buttonStates[buttonGroup].indexOf(state) > -1) {
            // fade container out while view is swapped
            $buttonsContainer.addClass('changing');

            setTimeout(function() {
                $buttonsContainer.removeClass(_buttonStates[buttonGroup]).addClass(state).removeClass('changing');
            }, 300);
        }
    };

    /*
    Changes the visible button(s) in the overlay.

    @param String state - A button state. Valid values are:
        play, replay, play-share, share-replay
        Passing an invalid value results in no change.
    */
    var _setOverlayButtons = function(state) {
        _setButtonState(_$overlayButtons, 'overlay', state);
    };

    /*
    Changes the visible button in the footer.

    @param String state - A button state. Valid values are:
        share, download, none
        Passing an invalid value results in no change.
    */
    var _setFooterButton = function(state) {
        _setButtonState(_$footerButtons, 'footer', state);
    };

    /*
    Makes sure embed is ready and YouTube API is initialized.
    */
    var _enableEmbed = function() {
        if (!_embedReady) {
            var newSrc = _$embedIframe.attr('data-src');

            // check if supports HTML5 video
            if (!!document.createElement('video').canPlayType) {
                newSrc += '&html5=1';
            }

            _$embedIframe.attr('src', newSrc);

            _embedReady = true;
        }

        // make sure YouTube API is initialized (if needed)
        if (!_youtubeAPIready) {
            _initYouTubeAPI();
        }
    };

    /*
    Disables the embed. Useful when tour is re-opened.
    */
    var _disableEmbed = function() {
        _$embedIframe.attr('src', '');
        _embedReady = false;
    };

    /*
    Hides the button overlay, shows & plays embedded YouTube video.
    */
    var _playEmbed = function() {
        if (_hasVideo) {
            if (!_embedReady || !_youtubeAPIready || !_youtubePlayer) {
                _waitingToPlay = true;
                _enableEmbed();
            } else {
                // show embed just before fading buttons out
                _$embedWrapper.show();

                _$buttonOverlay.fadeOut('normal', function() {
                    // iOS & Chrome on Android don't allow play to be triggered by API
                    if (!_isIOS && !_isAndroid) {
                        _youtubePlayer.playVideo();
                    }
                });
            }
        }
    };

    /*
    Fades button overlay back in.
    */
    var _hideEmbed = function() {
        _$buttonOverlay.fadeIn('normal', function() {
            // make sure embed doesn't get keyboard focus
            _$embedWrapper.hide();
        });
    };

    /*
    When embedded video is complete, call the user-specified
    onComplete function.
    */
    var _videoComplete = function(state) {
        // if ended
        if (state.data === 0) {
            _opts.onComplete();
        }
    };

    return {
        // PUBLIC METHODS
        // see implementation details above

        init: function(config) {
            _init(config);
        },
        setOverlayButtons: function(state) {
            _setOverlayButtons(state);
        },
        setFooterButton: function(state) {
            _setFooterButton(state);
        },
        enableEmbed: function() {
            _enableEmbed();
        },
        disableEmbed: function() {
            _disableEmbed();
        },
        playEmbed: function() {
            _playEmbed();
        },
        hideEmbed: function() {
            _hideEmbed();
        },
        // Called only by YouTube when YouTube is ready.
        initYouTubePlayer: function() {
            _youtubePlayer = new YT.Player('fx-anniversary-video-embed', {
                events: {
                    // listen for state change to take action when complete
                    'onStateChange': _videoComplete,
                    // in the event embed is lazy loaded, wait until player
                    // is ready to being playing - not the best UI here, as
                    // response time is variable. this case only exists on
                    // post-tour page, and may be obviated by updating tour
                    // API to enable embed when tour closes.
                    'onReady': function() {
                        if (_waitingToPlay) {
                            _waitingToPlay = false;
                            _playEmbed();
                        }
                    }
                }
            });
        }
    };
})(window.jQuery);
