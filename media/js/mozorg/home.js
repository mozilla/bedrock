if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

if (typeof Mozilla.page === 'undefined') {
    Mozilla.page = {};
}

Mozilla.page.Home = {
    'closeText' : 'close'
};

$(document).ready(function() {

    var isMSIEpre9 = (/MSIE\ (4|5|6|7|8)/.test(navigator.userAgent));
    var hasMediaQueries = (typeof matchMedia !== 'undefined');
    var noVideo = (typeof HTMLMediaElement === 'undefined');

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

    var currentSize = getSize();

    var $thumb = $('#promo-flicks-keyframe');
    var $link = $thumb.next();

    // create container that replaces the link when the video is open
    var $container = $('<div class="container"></div>');
    $container.css('display', 'none')
        .insertBefore($link);

    // create go link shown when video is open
    var $goLink = $('<a class="go"></a>');
    $goLink.attr('href', $link.attr('href'))
        .text($link.find('.go').text())
        .appendTo($container);

    // get video-complteted overlay and set up replay button click handler
    var $overlay = $('#promo-flicks-overlay');
    $overlay.find('.video-replay').click(function(e) {
        e.preventDefault();
        hideOverlay();
        if (videoJS) {
            // let the loading and big play buttons show up again.
            $videoContainer.find('.video-js').removeClass('vjs-moz-ended');
            videoJS.currentTime(0);
            videoJS.play();
        }
    });

    var state = 'closed';

    // create close button for closing open video
    var $close = $(
        '<span class="video-close" tabindex="0" role="button">×</span>'
    );

    $close.attr('title', Mozilla.page.Home.closeText)
        .click(function(e) { close(); });

    // shared animation settings
    var duration = 400;
    var easing = 'swing';

    // create container to hold the video player
    var $videoContainer = $('<div class="video-container"></div>');
    $videoContainer.css('display', 'none')
        .insertAfter($thumb);

    // create video

    // IE9 didn't like a video element build using jQuery so we build it
    // using the DOM API.
    var video = document.createElement('video');
    video.id = 'video-player';
    video.className = 'video-js vjs-default-skin';
    video.controls = 'controls';
    video.preload = 'none';

    // create video sources
    var sources = [
        {
            src: 'http://videos.mozilla.org/uploads/brand/State%20of%20Mozilla%202011%20(fcp2)-RC%20-%20720p%20-%20MPEG-4.mp4',
            type: 'video/mp4'
        },
        {
            src: 'http://videos.mozilla.org/uploads/brand/State%20of%20Mozilla%202011%20(fcp2)-RC%20-%20720p%20-%20MPEG-4.webm',
            type: 'video/webm'
        }
    ];

    for (var i = 0; i < sources.length; i++) {
        var source = document.createElement('source');
        source.src = sources[i].src;
        source.type = sources[i].type;
        video.appendChild(source);
    }

    var $video = $(video);
    $video.appendTo($videoContainer);

    // shared reference to the video.js player when it exists
    var videoJS;

    function open() {
        if (state !== 'closed') {
            return;
        }

        state = 'opening';

        // if pager is auto-rotating, stop rotating when video opened
        Mozilla.Pager.pagers['home-promo'].stopAutoRotate();

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

    function showLink() {
        // hide container and show link at same dimensions
        $container.css('display', 'none');
        $link.css('display', 'block');
    }

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

                // Flash player fails to initialize dynamically inserted source
                // elements. Set up the sources after the player exists. See
                // http://help.videojs.com/discussions/questions/350-flash-fallback-in-ie8
                if (noVideo) {
                    videoJS.src(sources);
                }
                videoJS.addEvent('ended', showOverlay);
                videoJS.play();
            });
        }
    }

    function showOverlay() {
        var width = $videoContainer.width();
        var height = $videoContainer.height();
        var position = $videoContainer.position();

        $overlay.css({
            'top' : position.top,
            'left' : position.left,
            'width' : width,
            'height' : height,
            'display' : 'block'
        });

        // hide video-js big play button and loading spinner (Chrome
        // shows spinner for some videos after they are finished)
        $videoContainer.find('.video-js').addClass('vjs-moz-ended');
    }

    function hideOverlay() {
        $overlay.css('display', 'none');
    }

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

    $thumb.click(function(e) { open(); });

    function handleResize() {
        var size = getSize();
        if (size.videoWidth !== currentSize.videoWidth) {
            currentSize = size;
            reposition();
        }
    }

    function reposition() {
        var linkWidth;

        if (state === 'opened' || state === 'opening') {

            // TODO: check for and stop animations

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

        } else {

            // TODO: check for and stop animations

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

    if (!isMSIEpre9) {
        $(window).resize(handleResize);
        handleResize();
    }

    // pause video if pager changes pages
    Mozilla.Pager.pagers['home-promo'].$container.bind('changePage', function() {
        if (videoJS) {
            videoJS.pause();
        }
    });

});
