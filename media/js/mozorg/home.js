if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

if (typeof Mozilla.page === 'undefined') {
    Mozilla.page = {};
}

Mozilla.page.Home = {
    'closeText' : 'close',
    'shareText' : 'Share'
};

$(document).ready(function() {

    // {{{ showLink()

    function showLink() {
        // hide container and show link at same dimensions
        $container.css('display', 'none');
        $link.css('display', 'block');
    }

    // }}}
    // {{{ hideLink()

    function hideLink() {
        var linkHeight = $link.height();
        var linkWidth = $link.width();

        // hide link and show container with same dimensions
        $link.css('display', 'none');
        $container.height(linkHeight)
            .css('display', 'block');

        $goLink.css(
            'left',
            Math.max(Math.floor((linkWidth - currentSize.videoWidth) / 2), 20)
        );
    }

    // }}}
    // {{{ showVideo()

    function showVideo() {
        var thumbPosition = $thumb.position();

        $video.attr('width', currentSize.videoWidth)
            .attr('height', currentSize.videoHeight);

        $thumb.css('display', 'none');

        $videoContainer.css({
            'top' : thumbPosition.top,
            'right' : 'auto',
            'left' : thumbPosition.left,
            'width' : currentSize.videoWidth,
            'height' : currentSize.videoHeight,
            'display' : 'block'
        });

        if (videoJS) {
            // let the loading and big play buttons show up again.
            $videoContainer.find('.video-js').removeClass('vjs-moz-ended');

            videoJS.size(currentSize.videoWidth, currentSize.videoHeight);
            videoJS.play();
        } else {
            _V_('video-player', {}, function() {
                videoJS = this;

                // add share button to controls on first play
                videoJS.addEvent('play', function() {
                    if (!$shareButton) {
                        $shareButton = $(
                            '<button class="vjs-sandstone-share">' +
                            Mozilla.page.Home.shareText +
                            '</button>'
                        );
                        $shareButton.click(function() {
                            videoJS.pause();
                            showOverlay(false);
                        });
                        var $controls = $(videoJS.controlBar.el);
                        $controls.append($shareButton);
                    }
                });

                // Ideally, we'd like to show the overlay on pause. Video-js
                // Issue 159 prevents us from doing so:
                // https://github.com/zencoder/video-js/issues/159

                // Flash player fails to initialize dynamically inserted source
                // elements. Set up the sources after the player exists. See
                // http://help.videojs.com/discussions/questions/350-flash-fallback-in-ie8
                if (!hasVideo) {
                    videoJS.src(sources);
                }
                videoJS.addEvent('ended', function() { showOverlay(true); });
                videoJS.play();
            });
        }
    }

    // }}}
    // {{{ hideVideo()

    function hideVideo() {
        if (videoJS) {
            videoJS.pause();
        }

        var videoPosition = $videoContainer.position();

        $videoContainer.css('display', 'none');
        $overlay.css('display', 'none');

        $thumb.css({
            'top' : videoPosition.top,
            'right' : 'auto',
            'left' : videoPosition.left,
            'display' : 'block'
        });

        if (currentSize.videoWidth < 720) {
            $thumb.css({
                'width' : currentSize.thumbWidth,
                'height' : currentSize.thumbHeight
            });
        }

        $close.detach();
    }

    // }}}
    // {{{ showOverlay()

    function showOverlay(ended) {
        var width = $videoContainer.width();
        var height = $videoContainer.height();
        var position = $videoContainer.position();

        if (ended) {
            $overlay.find('.video-replay').css('display', 'inline-block');
            $overlay.find('.video-continue').css('display', 'none');
        } else {
            $overlay.find('.video-replay').css('display', 'none');
            $overlay.find('.video-continue').css('display', 'inline-block');
        }

        $overlay.css({
            'top' : position.top,
            'left' : position.left,
            'width' : width,
            'height' : height,
            'display' : 'block'
        });

        if (ended) {
            // hide video-js big play button and loading spinner (Chrome
            // shows spinner for some videos after they are finished)
            $videoContainer.find('.video-js').addClass('vjs-moz-ended');
        }
    }

    // }}}
    // {{{ hideOverlay()

    function hideOverlay() {
        $overlay.css('display', 'none');
    }

    // }}}
    // {{{ open()

    function open() {
        if (state !== 'closed') {
            return;
        }

        state = 'opening';

        // if pager is auto-rotating, stop rotating when video opened
        Mozilla.Pager.pagers['home-promo'].stopAutoRotate();
        Mozilla.Pager.pagers['home-promo'].autoRotate = false;

        var thumbOffset = $thumb.offset();

        // show close link
        $close.insertBefore($container)
            .css('right', 'auto')
            .offset({
                'left' : thumbOffset.left + currentSize.thumbWidth,
                'top' : thumbOffset.top
            });

        if (currentSize.videoWidth >= 720) {

            var linkWidth = $link.width();

            hideLink();

            var goHeight = $goLink.height();

            $container.animate(
                {
                    'height' : currentSize.videoHeight + goHeight + 10 + currentSize.marginHeight * 2
                },
                duration,
                easing
            );

            $close.animate(
                {
                    'left' : Math.floor((linkWidth + currentSize.videoWidth) / 2),
                    'top'  : currentSize.marginHeight
                },
                duration
            );

            $thumb.css('right', 'auto')
                .offset({ 'left' : thumbOffset.left })
                .animate(
                    {
                        'height' : currentSize.videoHeight,
                        'width' : currentSize.videoWidth,
                        'left' : Math.floor((linkWidth - currentSize.videoWidth) / 2),
                        'top' : currentSize.marginHeight
                    },
                    duration,
                    easing,
                    function() {
                        showVideo();
                        // only allow closing after opened
                        state = 'opened';
                    }
                );

            $('body').animate(
                {
                    scrollTop: $('#home-promo').position().top - 20
                },
                duration,
                easing
            );

        } else {
            // for small sizes, no animation required
            showVideo();
            state = 'opened';
        }
    }

    // }}}
    // {{{ close()

    function close() {
        if (state !== 'opened') {
            return;
        }

        state = 'closing';

        hideVideo();

        var linkWidth = $container.width();
        var linkHeight = $container.height();

        if (currentSize.videoWidth >= 720) {

            showLink();
            $link.height(linkHeight)
                .animate(
                    {
                        'height' : currentSize.thumbHeight + 2 * currentSize.marginHeight
                    },
                    duration,
                    easing
                );

            $thumb.animate(
                {
                    'height' : currentSize.thumbHeight,
                    'width'  : currentSize.thumbWidth,
                    'left'   : linkWidth - currentSize.thumbWidth - currentSize.marginWidth
                },
                duration,
                easing,
                function() {
                    // only allow opening after closing finished
                    state = 'closed';
                }
            );
        } else {
            state = 'closed';
        }

    }

    // }}}
    // {{{ getSize()

    function getSize() {
        if (hasMediaQueries && matchMedia('(max-width: 480px)').matches) {
            return sizes[0];
        }

        if (hasMediaQueries && matchMedia('(min-width: 480px) and (max-width: 760px)').matches) {
            return sizes[1];
        }

        if (hasMediaQueries && matchMedia('(min-width: 760px) and (max-width: 1000px)').matches) {
            return sizes[2];
        }

        return sizes[3];
    }

    // }}}
    // {{{ handleResize()

    function handleResize() {
        var size = getSize();
        if (size.videoWidth !== currentSize.videoWidth) {
            currentSize = size;
            reposition();
        }
    }

    // }}}
    // {{{ resposition()

    function reposition() {
        var linkWidth;

        // TODO: check for and stop animations
        if (state === 'opened' || state === 'opening') {
            if (videoJS) {
                videoJS.size(currentSize.videoWidth, currentSize.videoHeight);
            }

            $overlay.css({
                'width' : currentSize.videoWidth,
                'height' : currentSize.videoHeight
            });

            var $offsetParent = $videoContainer.offsetParent();
            linkWidth = $offsetParent.width();

            $videoContainer.css({
                'right' : 'auto',
                'top' : currentSize.marginHeight,
                'left' : Math.floor((linkWidth - currentSize.videoWidth) / 2),
                'width' : currentSize.videoWidth,
                'height' : currentSize.videoHeight
            });

            $overlay.css({
                'right' : 'auto',
                'top' : currentSize.marginHeight,
                'left' : Math.floor((linkWidth - currentSize.videoWidth) / 2)
            });

            $close.css({
                'right' : 'auto',
                'top' : currentSize.marginHeight,
                'left' : Math.floor((linkWidth + currentSize.videoWidth) / 2)
            });

            $thumb.css({
                'width' : currentSize.videoWidth,
                'height' : currentSize.videoHeight
            });

            if (currentSize.videoWidth >= 720) {
                $goLink.css({
                    'bottom' : 'auto',
                    'left' : Math.max(Math.floor((linkWidth - currentSize.videoWidth) / 2), 20),
                    'top' : currentSize.videoHeight + currentSize.marginHeight + 10
                });

                hideLink();

                var goHeight = $goLink.height();

                $container.css(
                    'height',
                    currentSize.marginHeight + currentSize.videoHeight + goHeight + 10 + 20
                );
            } else {
                showLink();
                $link.css('height', 'auto');
            }
        // TODO: check for and stop animations
        } else {
            linkWidth = $link.width();

            $thumb.css({
                'right' : 'auto',
                'top' : currentSize.marginHeight,
                'left' : linkWidth - currentSize.thumbWidth - currentSize.marginWidth,
                'width' : currentSize.thumbWidth,
                'height' : currentSize.thumbHeight
            });

            var height;
            if (currentSize.videoWidth >= 720) {
                height = currentSize.thumbHeight + currentSize.marginHeight * 2;
            } else {
                height = 'auto';
            }

            $link.css('height', height);
        }
    }

    // }}}
    // {{{ createVideo()

    function createVideo() {
        // IE9 didn't like a video element build using jQuery so we build it
        // using the DOM API.
        var video = document.createElement('video');
        video.id = 'video-player';
        video.className = 'video-js vjs-default-skin';
        video.controls = 'controls';
        video.preload = 'none';

        for (var i = 0; i < sources.length; i++) {
            var source = document.createElement('source');
            source.src = sources[i].src;
            source.type = sources[i].type;
            video.appendChild(source);
        }

        return $(video);
    }

    // }}}
    // {{{ createCloseButton()

    function createCloseButton() {
        var $close = $(
            '<span class="video-close" tabindex="0" role="button">×</span>'
        );

        $close.attr('title', Mozilla.page.Home.closeText)
            .click(function(e) { close(); })
            .keypress(function(e) {
                if (e.keyCode === 13 || e.keyCode === 32) {
                    e.preventDefault(e);
                    close();
                }
            });

        return $close;
    }

    // }}}
    // {{{ createThumb()

    function createThumb() {
        var $thumb = $('#promo-flicks-keyframe');

        $thumb.click(function(e) { open(); })
            .keypress(function(e) {
                if (e.keyCode === 13 || e.keyCode === 32) {
                    e.preventDefault(e);
                    open();
                }
            });

        return $thumb;
    }

    // }}}
    // {{{ createContainer()

    function createContainer() {
        var $container = $('<div class="container"></div>');
        $container.css('display', 'none')
        return $container;
    }

    // }}}
    // {{{ createGoLink()

    function createGoLink($link) {
        var $goLink = $('<a class="go"></a>');
        $goLink.attr('href', $link.attr('href'))
            .text($link.find('.go').text());

        return $goLink;
    }

    // }}}
    // {{{ createVideoContainer()

    function createVideoContainer() {
        var $videoContainer = $('<div class="video-container"></div>');
        $videoContainer.css('display', 'none')
        return $videoContainer;
    }

    // }}}
    // {{{ createSocialOverlay()

    function createSocialOverlay() {
        var $overlay = $('#promo-flicks-overlay');
        $overlay.find('.video-replay').click(function(e) {
            handleReplayAction();
        }).keypress(function(e) {
            if (e.keyCode === 13 || e.keyCode === 32) {
                e.preventDefault(e);
                handleReplayAction();
            }
        });
        $overlay.find('.video-continue').click(function(e) {
            handleContinueAction();
        }).keypress(function(e) {
            if (e.keyCode === 13 || e.keyCode === 32) {
                e.preventDefault(e);
                handleContinueAction();
            }
        });
        return $overlay;
    }

    // }}}
    // {{{ handleReplayAction()

    function handleReplayAction() {
        hideOverlay();
        if (videoJS) {
            // let the loading and big play buttons show up again.
            $videoContainer.find('.video-js').removeClass('vjs-moz-ended');
            videoJS.currentTime(0);
            videoJS.play();
        }
    }

    // }}}
    // {{{ handleContinueAction()

    function handleContinueAction() {
        hideOverlay();
        if (videoJS) {
            videoJS.play();
        }
    }

    // }}}

    var hasMediaQueries = (typeof matchMedia !== 'undefined');
    var hasVideo = (typeof HTMLMediaElement !== 'undefined');

    var sizes = [
        {
            thumbWidth : 320,
            thumbHeight : 180,
            videoWidth : 320,
            videoHeight : 180,
            marginWidth : 0,
            marginHeight : 0
        },
        {
            thumbWidth : 440,
            thumbHeight : 248,
            videoWidth : 440,
            videoHeight : 248,
            marginWidth : 0,
            marginHeight : 0
        },
        {
            thumbWidth : 280,
            thumbHeight : 158,
            videoWidth : 720,
            videoHeight : 405,
            marginWidth : 20,
            marginHeight : 20
        },
        {
            thumbWidth : 380,
            thumbHeight : 214,
            videoWidth : 853,
            videoHeight : 480,
            marginWidth : 30,
            marginHeight : 25
        }
    ];

    var sources = [{
        src: 'http://videos-cdn.mozilla.net/serv/firefoxflicks/FireFoxFlicks_2013-Teaser.mp4',
        type: 'video/mp4'
    }, {
        src: 'http://videos-cdn.mozilla.net/serv/firefoxflicks/FireFoxFlicks_2013-Teaser.webm',
        type: 'video/webm'
    }];

    var currentSize = getSize();
    var $thumb = createThumb();
    var $link = $thumb.next();
    var $container = createContainer();
    var $goLink = createGoLink($link);
    var $close = createCloseButton();
    var $videoContainer = createVideoContainer();
    var $video = createVideo();
    var $overlay = createSocialOverlay();
    var $shareButton;

    $container.insertBefore($link);
    $goLink.appendTo($container);
    $videoContainer.insertAfter($thumb);
    $video.appendTo($videoContainer);

    var state = 'closed';

    // shared animation settings
    var duration = 400;
    var easing = 'swing';

    // the video.js player when it exists
    var videoJS;

    if (hasMediaQueries) {
        $(window).resize(handleResize);
        handleResize();
    }

    // pause video if pager changes pages
    Mozilla.Pager.pagers['home-promo'].$container.bind('changePage', function() {
        if (videoJS) {
            videoJS.pause();
        }
    });

    // video.js configuration of Flash player. If the SWF is moved to a
    // Mozilla CDN in the future, a crossdomain.xml file will need to be
    // configured before the SWF will work.
    var base = location.protocol + '//' + location.host;
    _V_.options.flash.swf = base + '/media/js/libs/video-js/video-js.swf';

});
