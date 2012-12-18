$(document).ready(function() {

    var isMSIEpre9 = (function() {
        return (/MSIE\ (4|5|6|7|8)/.test(navigator.userAgent));
    })();

    var sizes = [
        {
            to      : 480,
            width   : 320,
            height  : 180,
            padding : 0
        },
        {
            from    : 480,
            to      : 760,
            width   : 440,
            height  : 248,
            padding : 0
        },
        {
            from    : 760,
            to      : 1000,
            width   : 720,
            height  : 405,
            padding : 20
        },
        {
            from    : 1000,
            width   : 853,
            height  : 480,
            padding : 20
        }
    ];

    function getSize()
    {
        var width = $(window).width();
        var size  = {
            width   : sizes[0].width,
            height  : sizes[0].height,
            padding : sizes[0].padding
        };

        if (isMSIEpre9) {
            width = 1001;
        }

        for (var i = 0; i < sizes.length; i++) {
            if (
                   (!sizes[i].from || width >= sizes[i].from)
                && (!sizes[i].to || width < sizes[i].to)
            ) {
                size = {
                    width   : sizes[i].width,
                    height  : sizes[i].height,
                    padding : sizes[i].padding
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

        opened = true;

        var height = $link.height();
        var width  = $link.width();

        var thumbOffset   = $thumb.offset();
        var thumbPosition = $thumb.position();
        var thumbWidth    = $thumb.width();
        var linkPosition  = $link.position();

        var size = getSize();

        $link.css('display', 'none');

        $container
            .height(height)
            .css('display', 'block');

        $close
            .insertBefore($container)
            .css(
                {
                    'right' : 'auto'
                }
            )
            .offset(
                {
                    'left'  : thumbOffset.left + thumbWidth
                }
            )
            .animate(
                {
                    'left' : Math.floor(((width - 2 * margin) / 2) + (size.width / 2) + margin),
                    'top'  : size.padding
                },
                duration
            );

        var goHeight = $goLink.height();
        $goLink.css('left', Math.floor(((width - 2 * margin) / 2) - (size.width / 2) + margin));

        $container
            .animate(
                {
                    'height' : size.height + margin + goHeight + 10 + size.padding
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
                    'height' : size.height,
                    'width'  : size.width,
                    'left'   : Math.floor(((width - 2 * margin) / 2) - (size.width / 2) + margin),
                    'top'    : size.padding
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
                videoJS.play();
            });
        }
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

        var height = $container.height();

        $container.css('display', 'none');

        $link
            .height(height)
            .css('display', 'block')
            .animate(
                {
                    'height' : startHeight + 2 * margin
                },
                duration,
                easing
            );

        $thumb.animate(
            {
                'height' : startHeight,
                'width'  : startWidth,
                'left'   : startPosition.left
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
        var width = $(window).width();

        if (videoJS) {
            var size = getSize();
            var videoWidth = $videoContainer.width();

            if (size.width != videoWidth) {
                videoJS.size(size.width, size.height);
                reposition(size.padding);
            }
        }
    };

    function reposition(videoMargin)
    {
        var $offsetParent = $videoContainer.offsetParent();

        var totalWidth = $offsetParent.width();
        var width      = $videoContainer.width();
        var height     = $videoContainer.height();
        var goHeight   = $goLink.height();
        var goLeft     = Math.max(Math.floor((totalWidth - width) / 2), margin);

        $videoContainer.css(
            {
                'right' : 'auto',
                'top'   : videoMargin,
                'left'  : Math.floor((totalWidth - width) / 2)
            }
        );

        $close.css(
            {
                'right' : 'auto',
                'top'   : videoMargin,
                'left'  : Math.floor((totalWidth + width) / 2)
            }
        );

        $goLink.css(
            {
                'bottom' : 'auto',
                'left'   : goLeft,
                'top'    : height + videoMargin + 10
            }
        );

        $container.css(
            {
                'height' : videoMargin + height + goHeight + 10 + margin
            }
        );

    };

    if (!isMSIEpre9) {
        $(window).resize(handleResize);
        handleResize();
    }


});
