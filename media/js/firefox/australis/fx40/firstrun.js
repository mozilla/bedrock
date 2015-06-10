;(function($, Mozilla) {
    'use strict';

    var hasVideo = $('#video').length > 0;
    var $videoFrame = $('#video-frame');
    var $videoTitle = $('#video-title');
    var $video = $('#firstrun-video');
    var $fxaFrame = $('#fxa');
    var fxaIframeSrc = $('#intro').data('fxa-iframe-src');
    var fxaFrameTarget = ($fxaFrame.length) ? $('#fxa')[0].contentWindow : null;
    var videoOnLoad = false;
    var resizeTimer;

    // remove trailing slash from iframe src (if present)
    fxaIframeSrc = (fxaIframeSrc[fxaIframeSrc.length - 1] === '/') ? fxaIframeSrc.substr(0, fxaIframeSrc.length - 1) : fxaIframeSrc;

    // communicate with FxA iframe
    window.addEventListener('message', function (e) {
        var data;
        // make sure origin is as expected
        if (e.origin === fxaIframeSrc) {
            data = JSON.parse(e.data);

            switch (data.command) {
            // tell iframe we are expecting it
            case 'ping':
                fxaFrameTarget.postMessage(e.data, fxaIframeSrc);
                break;
            // just GA tracking when iframe loads
            case 'loaded':
                window.dataLayer.push({
                    'event': 'firstrun-fxa',
                    'interaction': 'fxa-loaded'
                });

                break;
            // resize container when iframe resizes for nicer UI
            case 'resize':
                clearTimeout(resizeTimer);
                // sometimes resizes come in bunches - only want to react to the last of a set
                resizeTimer = setTimeout(function() {
                    $fxaFrame.css('height', data.data.height + 'px').addClass('visible');
                }, 300);

                break;
            // track when user signs up successfully (but hasn't yet verified email)
            case 'signup_must_verify':
                window.dataLayer.push({
                    'event': 'firstrun-fxa',
                    'interaction': 'fxa-signup'
                });

                break;
            // track when user returns to page after verifying email (may never happen)
            case 'verification_complete':
                window.dataLayer.push({
                    'event': 'firstrun-fxa',
                    'interaction': 'fxa-verified'
                });

                break;
            // track user with FxA account logging in (very rare for firstrun)
            case 'login':
                window.dataLayer.push({
                    'event': 'firstrun-fxa',
                    'interaction': 'fxa-login'
                });

                break;
            }
        }
    }, true);

    // if locale has video, do A/B test
    if (hasVideo) {
        // manual override to test videos
        if (window.location.href.indexOf('v=') !== -1) {
            var variation = window.location.href.split('v=')[1];

            videoOnLoad = (variation === '1') ? false : true;
        } else {
            videoOnLoad = Math.random() >= 0.5;
        }

        window.dataLayer.push({
            'event': 'firstrun-video',
            'videoPosition': (videoOnLoad) ? 'overlay' : 'bottom',
            'videoTitle': '/firstrun/ video'
        });

        $video.on('play', function() {
            // GA track video play
            window.dataLayer.push({
                'event': 'firstrun-video',
                'interaction': 'play',
                'videoTitle': '/firstrun/ video'
            });
        }).on('ended', function() {
            // GA track video finish
            window.dataLayer.push({
                'event': 'firstrun-video',
                'interaction': 'finish',
                'videoTitle': '/firstrun/ video'
            });

            // take a little breath before closing modal
            setTimeout(function() {
                Mozilla.Modal.closeModal();
            }, 500);
        });
    }

    var showVideo = function(origin, autoplay) {
        var opts = {
            title: $videoTitle.text(),
            onDestroy: function() {
                window.dataLayer.push({
                    'event': 'firstrun-video',
                    'interaction': 'close',
                    'videoTitle': '/firstrun/ video'
                });
            }
        };

        if (autoplay) {
            opts.onCreate = function() {
                // slight pause after modal opens
                setTimeout(function() {
                    $video[0].play();
                }, 250);
            };
        }

        Mozilla.Modal.createModal(origin, $videoFrame, opts);
    };

    // if showing video on page load, hide video copy/CTA and show video
    if (videoOnLoad) {
        $('#video').addClass('hidden');
        showVideo(document.documentElement, false);
    // if not showing video on page load, attach click listener to video CTA
    } else if (hasVideo) {
        $('#cta-video').on('click', function(e) {
            e.preventDefault();
            showVideo(this, true);
        });
    }
})(window.jQuery, window.Mozilla);
