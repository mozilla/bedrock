$(document).ready(function() {

    var isMSIEpre9 = (function() {
        return (/MSIE\ (4|5|6|7|8)/.test(navigator.userAgent));
    })();

    var sizes = [
        {
            to           : 479,
            thumbWidth   : 320,
            thumbHeight  : 180,
            videoWidth   : 320,
            videoHeight  : 180,
            marginWidth  : 0,
            marginHeight : 0
        },
        {
            from         : 480,
            to           : 760,
            thumbWidth   : 440,
            thumbHeight  : 248,
            videoWidth   : 440,
            videoHeight  : 248,
            marginWidth  : 0,
            marginHeight : 0
        },
        {
            from         : 761,
            to           : 1000,
            thumbWidth   : 280,
            thumbHeight  : 158,
            videoWidth   : 720,
            videoHeight  : 405,
            marginWidth  : 20,
            marginHeight : 20
        },
        {
            from         : 1001,
            thumbWidth   : 380,
            thumbHeight  : 214,
            videoWidth   : 853,
            videoHeight  : 480,
            marginWidth  : 30,
            marginHeight : 25
        }
    ];

    function getSize()
    {
        var width = $(window).width();
        var size  = {
            thumbWidth   : sizes[0].thumbWidth,
            thumbHeight  : sizes[0].thumbHeight,
            videoWidth   : sizes[0].thumbWidth,
            videoHeight  : sizes[0].thumbHeight,
            marginWidth  : sizes[0].marginWidth,
            marginHeight : sizes[0].marginHeight
        };

        if (isMSIEpre9) {
            // no media queries means we always use desktop width
            width = 1001;
        }

        for (var i = 0; i < sizes.length; i++) {
            if (
                   (!sizes[i].from || width >= sizes[i].from)
                && (!sizes[i].to || width <= sizes[i].to)
            ) {
                size = {
                    thumbWidth   : sizes[i].thumbWidth,
                    thumbHeight  : sizes[i].thumbHeight,
                    videoWidth   : sizes[i].videoWidth,
                    videoHeight  : sizes[i].videoHeight,
                    marginWidth  : sizes[i].marginWidth,
                    marginHeight : sizes[i].marginHeight
                };
                break;
            }
        }

        return size;
    };

    var $thumb = $('#promo-flicks-keyframe');
    var $link = $thumb.next();
    var $container = $('<div class="container"></div>');
    $container
        .css('display', 'none')
        .insertBefore($link);

    var $goLink = $('<a class="go"></a>');
    $goLink
        .attr('href', $link.attr('href'))
        .text($link.find('.go').text())
        .appendTo($container);

    var $overlay = $('#promo-flicks-overlay');
    $overlay.find('.video-replay').click(function(e) {
        e.preventDefault();
        hideOverlay();
        if (videoJS) {
            videoJS.currentTime(0);
            videoJS.play();
        }
    });

    var opened = false;

    var startWidth    = $thumb.width();
    var startHeight   = $thumb.height();
    var startPosition = $thumb.position();
    var startOffset   = $thumb.offset();

    var closeText = 'close';

    var $container;
    var $video;
    var $close;
    var videoJS;

    var $close = $(
        '<span class="video-close" tabindex="0" role="button">×</span>'
    );

    $close
        .attr('title', closeText)
        .click(function(e) {
            hideVideo();
            close();
        });

    var margin = 20;
    var duration = 400;
    var easing = 'swing';

    var $videoContainer = $('<div class="video-container"></div>');
    $videoContainer
        .css('display', 'none')
        .insertAfter($thumb);

    var $video = $(
        '<video id="video-player" class="video-js vjs-default-skin" '
        + 'controls="controls" preload="auto"></video>'
    );

    $video.appendTo($videoContainer);

    var sources = [
        {
            src:  'http://videos.mozilla.org/uploads/brand/State%20of%20Mozilla%202011%20(fcp2)-RC%20-%20720p%20-%20MPEG-4.mp4',
            type: 'video/mp4'
        },
        {
            src:  'http://videos.mozilla.org/uploads/brand/State%20of%20Mozilla%202011%20(fcp2)-RC%20-%20720p%20-%20MPEG-4.webm',
            type: 'video/webm'
        }
    ];

    for (var i = 0; i < sources.length; i++) {
        $video.append(
            $(
                '<source src="' + sources[i].src + '" '
                + 'type="' + sources[i].type + '"></source>'
            )
        );
    }

    function open()
    {
        if (opened) {
            return;
        }

        // if pager is auto-rotating, stop rotating when video opened
        Mozilla.Pager.pagers['home-promo'].stopAutoRotate();

        opened = true;

        var linkHeight   = $link.height();
        var linkWidth    = $link.width();
        var linkPosition = $link.position();

        var thumbOffset   = $thumb.offset();
        var thumbPosition = $thumb.position();

        var size = getSize();

        // hide link and show container with same dimensions
        $link.css('display', 'none');
        $container
            .height(linkHeight)
            .css('display', 'block');

        // show close link
        $close
            .insertBefore($container)
            .css(
                {
                    'right' : 'auto'
                }
            )
            .offset(
                {
                    'left'  : thumbOffset.left + size.thumbWidth
                }
            )
            .animate(
                {
                    'left' : Math.floor((linkWidth + size.videoWidth) / 2),
                    'top'  : size.marginHeight
                },
                duration
            );

        var goHeight = $goLink.height();
        $goLink.css(
            'left',
            Math.max(Math.floor((linkWidth - size.videoWidth) / 2), 20)
        );

        $container
            .animate(
                {
                    'height' : size.videoHeight + margin + goHeight + 10 + size.marginHeight
                },
                duration,
                easing
            );

        $thumb
            .css(
                {
                    'right' : 'auto'
                }
            )
            .offset(
                {
                    'left'  : thumbOffset.left
                }
            )
            .animate(
                {
                    'height' : size.videoHeight,
                    'width'  : size.videoWidth,
                    'left'   : Math.floor((linkWidth - size.videoWidth) / 2),
                    'top'    : size.marginHeight
                },
                duration,
                easing,
                showVideo
            );

        $('body').animate(
            {
                scrollTop: $('#home-promo').position().top - 20
            },
            duration,
            easing
        );
    };

    function showVideo()
    {
        var thumbPosition = $thumb.position();

        $video
            .attr('width', $thumb.width())
            .attr('height', $thumb.height());

        $thumb.css(
            {
                'display' : 'none'
            }
        );

        $videoContainer.css(
            {
                'top'     : thumbPosition.top,
                'right'   : 'auto',
                'left'    : thumbPosition.left,
                'display' : 'block'
            }
        );

        if (videoJS) {
            videoJS.play();
        } else {
            _V_('video-player', {}, function() {
                videoJS = this;
                videoJS.addEvent('ended', showOverlay);
                videoJS.play();
            });
        }
    };

    function showOverlay()
    {
        var width    = $videoContainer.width();
        var height   = $videoContainer.height();
        var position = $videoContainer.position();

        $overlay.css(
            {
                'top'     : position.top,
                'left'    : position.left,
                'width'   : width,
                'height'  : height,
                'display' : 'block'
            }
        );
    };

    function hideOverlay()
    {
        $overlay.css('display', 'none');
    };

    function hideVideo()
    {
        if (videoJS) {
            videoJS.pause();
        }

        var videoPosition = $videoContainer.position();

        $videoContainer.css(
            {
                'display' : 'none'
            }
        );

        $thumb.css(
            {
                'top'     : videoPosition.top,
                'right'   : 'auto',
                'left'    : videoPosition.left,
                'display' : 'block'
            }
        );

        $close.detach();
    }

    function close()
    {
        if (!opened) {
            return;
        }

        opened = false;

        var linkWidth  = $container.width();
        var linkHeight = $container.height();

        var size = getSize();

        //TODO: get to height better

        // hide container and show link at same dimensions
        $container.css('display', 'none');
        $link
            .height(linkHeight)
            .css('display', 'block')
            .animate(
                {
                    'height' : size.thumbHeight + 2 * size.marginHeight
                },
                duration,
                easing
            );

        $thumb.animate(
            {
                'height' : size.thumbHeight,
                'width'  : size.thumbWidth,
                'left'   : linkWidth - size.thumbWidth - size.marginWidth
            },
            duration,
            easing
        );

    };

    $thumb.click(function(e) {
        open();
    });

    function handleResize()
    {
        if (videoJS) {
            var width = $(window).width();
            var size = getSize();
            var videoWidth = $videoContainer.width();

            if (size.width != videoWidth) {
                videoJS.size(size.videoWidth, size.videoHeight);
                reposition(size);
            }
        }
    };

    function reposition(size)
    {
        var $offsetParent = $videoContainer.offsetParent();

        var linkWidth = $offsetParent.width();
        var goHeight  = $goLink.height();
        var goLeft    = Math.max(Math.floor((linkWidth - size.videoWidth) / 2), 20);

        $videoContainer.css(
            {
                'right' : 'auto',
                'top'   : size.marginHeight,
                'left'  : Math.floor((linkWidth - size.videoWidth) / 2)
            }
        );

        $close.css(
            {
                'right' : 'auto',
                'top'   : size.marginHeight,
                'left'  : Math.floor((linkWidth + size.videoWidth) / 2)
            }
        );

        $goLink.css(
            {
                'bottom' : 'auto',
                'left'   : goLeft,
                'top'    : size.videoHeight + size.marginHeight + 10
            }
        );

        $container.css(
            {
                'height' : size.marginHeight + size.videoHeight + goHeight + 10 + 20
            }
        );

    };

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
