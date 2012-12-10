$(document).ready(function() {

    var $keyframe = $('#promo-flicks-keyframe');
    var $link = $keyframe.next();
    var $container = $('<div class="container"></div>');
    var $keyframeParent = $keyframe.parent();

    var $goLink = $('<a class="go"></a>');
    $goLink.attr('href', $link.attr('href'));
    $goLink.text($link.find('.go').text());
    $goLink.appendTo($container);

    var open = false;

    var startHeight = $link.height();
    var startWidth  = $keyframe.width();

    var closeText = 'close';

    var $container;
    var $video;
    var $close;
    var videoJS;

    function openVideo()
    {
        if (open) {
            return;
        }

        open = true;

        var height = $link.height();
        var width  = $link.width();

        var destHeight = 480;
        var destWidth  = 853;

        $link.replaceWith($container);
        $container.height(height);

        var goHeight = $goLink.height();
        $goLink.css('left', ((width - 40) / 2) - (destWidth / 2) + 20);

        $container.animate({ height: destHeight + 40 + goHeight + 10 });

        $keyframe.animate(
            {
                height: destHeight,
                width: destWidth,
                right: ((width - 40) / 2) - (destWidth / 2) + 20
            },
            400,
            'swing',
            showVideo
        );

        $('body').animate(
            {
                scrollTop: $('#home-promo').position().top - 20
            }
        );
    };

    function showVideo()
    {
        $container = $('<div class="video-container"></div>');

        $video = $(
            '<video id="video-player" class="video-js vjs-default-skin" '
            + 'controls="controls"></video>'
        );

        $video
            .attr('width', $keyframe.width())
            .attr('height', $keyframe.height())
            .attr('controls', 'controls');

        $video.appendTo($container);

        var sources = [
            {
                src:  'http://videos.mozilla.org/uploads/brand/State%20of%20Mozilla%202011%20(fcp2)-RC%20-%20720p%20-%20MPEG-4.mp4',
                type: 'video/mp4'
            },
            {
                src:  'http://videos.mozilla.org/uploads/brand/State%20of%20Mozilla%202011%20(fcp2)-RC%20-%20720p%20-%20MPEG-4.webm',
                type: 'video/webm'
            },
        ];

        for (var i = 0; i < sources.length; i++) {
            $source = $(
                '<source src="' + sources[i].src + '" '
                + 'type="' + sources[i].type + '"></source>'
            );
            $source.appendTo($video);
        }

        var right = $keyframe.css('right');
        var top   = $keyframe.css('top');

        $keyframe.replaceWith($container);
        $container.css({
            'top'     : top,
            'right'   : right
        });

        $close = $(
            '<span class="video-close" tabindex="0" role="button"></span>'
        );
        $close
            .text(closeText)
            .click(function(e) {
                hideVideo();
                closeVideo();
            });

        $close.insertBefore($container);

        var $videoPlayer;

        _V_('video-player', {}, function() {
            $videoPlayer = $('#video-player');
            this.play();
            videoJS = this;
        });
    };

    function hideVideo()
    {
        if (videoJS) {
            videoJS.pause();
            videoJS = null;
        }
        $container.replaceWith($keyframe);
        $close.remove();
    }

    function closeVideo()
    {
        if (!open) {
            return;
        }

        open = false;

        var height = $container.height();

        $container.replaceWith($link);
        $link.height(height);

        $link.animate({ height: startHeight });

        $keyframe.animate(
            {
                height: startHeight - 40,
                width: startWidth,
                right: 20
            }
        );

    };

    function toggleVideo()
    {
        if (open) {
            closeVideo();
        } else {
            openVideo();
        }
    };

    $keyframe.click(function(e) {
        toggleVideo();
    });

});
