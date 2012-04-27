$(document).ready(function() {

    var pager = Mozilla.Pager.rootPagers[0];
    pager.$container.bind('changePage', function(e, tab) {
        stopVideos();
    });


    function getNewObject($object)
    {
        var data = $object.attr('data');
        data = data.replace(/&/g, '&amp;');
        var html =
              '<object '
            + 'type="application/x-shockwave-flash" '
            + 'style="width: 528px; height: 317px;" '
            + 'data="' + data + '">'
            + '<param name="movie" value="' + data + '" />'
            + '<param name="wmode" value="transparent" />'
            + '<div class="video-player-no-flash">'
            + 'This video requires a browser with support for open video '
            + 'or the <a href="http://www.adobe.com/go/getflashplayer">Adobe '
            + 'Flash Player</a>.'
            + '</div>'
            + '</object>';

        return $(html);
    };

    var $videos = $('#platform .mozilla-video-control video');

    function stopVideos()
    {
        var el;
        for (var i = 0; i < $videos.length; i++) {
            el = $videos.get(i);
            if (typeof HTMLMediaElement != 'undefined') {
                el.pause();
                el.currentTime = 0;
                if (el._control) {
                    el._control.show();
                }
            } else {
                // Delete and re-add Flash object. We don't have the
                // documentation to script it :-(
                (function() {
                    var theEl = el;
                    var $object = $('object', theEl);
                    var $newObject = getNewObject($object);
                    setTimeout(function() {
                        $object.remove();
                        $newObject.appendTo(theEl);
                    }, 750);
                })();
            }
        }
    };

});
