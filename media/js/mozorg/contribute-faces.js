/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var $facesVid = $('#faces-video');
    var $caption = $('#video-stage .caption');
    var path = $('#video-stage').data('video-path');
    var vidnumber = 0;

    var videoList = [
        path + 'contribute-faces001',
        path + 'contribute-faces02',
        path + 'contribute-faces03',
        path + 'contribute-faces04',
        path + 'contribute-faces05'
    ];

    // How long to play the video
    // We'll actually start the transition just before the video ends
    // to hide the slight delay before the 'ended' event fires.
    var videoTime = 9.75; // currentTime returns seconds, not milliseconds

    // How long to show the caption
    var captionTime = 2500;

    // Start the video after the page loads
    var captionTimer = setTimeout(function() {
        if (!!document.createElement('video').canPlayType) {
            $caption.fadeOut(350, function() {
                $facesVid[0].play();
                $('#video-stage button').show();
                $facesVid.on('timeupdate', videoSequence);
            });
        } else {
            $caption.delay(1000).fadeOut(500, function() {
                $('#video-stage').hover(
                    function() {
                        $caption.fadeIn(350);
                    },
                    function() {
                        $caption.fadeOut(350);
                    }
                );
            });
        }
    }, captionTime);

    // Run the video sequence
    function videoSequence() {
        if ($facesVid[0].currentTime >= videoTime) {
            showCaption();
            captionTimer = setTimeout(hideCaption, captionTime);
        }
    }

    // Show the caption, change the video behind it
    function showCaption() {
        $caption.fadeIn(350, changeVideo);
        $('#video-stage button').hide();
    }

    // Hide the caption, play the video
    function hideCaption() {
        $caption.fadeOut(350, function() {
            $('#video-stage button').show();
            $facesVid[0].play();
        });
    }

    // Change to the next video in the array
    function changeVideo() {
        vidnumber++;
        if (vidnumber >= videoList.length){
            vidnumber = 0;
        }

        // Replace the element with new sources
        var element =
            '<video id="faces-video" preload="auto">' +
            '  <source src="' + videoList[vidnumber] + '.webm" type="video/webm">' +
            '  <source src="' + videoList[vidnumber] + '.mp4" type="video/mp4">' +
            '</video>';

        $facesVid.replaceWith(element);
        $facesVid = $('#faces-video'); // Reassert the variable for the new object
        $facesVid.off().on('timeupdate', videoSequence); // Rebind the event to the new object
        $facesVid[0].load();
    }

    // Add a button to play/pause the video (if supported)
    $('<button type="button" class="btn-pause">' + window.trans('button-pause') + '</button>').appendTo('#video-stage').hide();

    var paused = false;

    // Pause or play the video
    $('#video-stage button').click(function() {
        if ($caption.is(':visible') || $caption.is(':animated')) {
            return;
        }

        if (!$facesVid[0].paused) { // If the video is not paused
            $facesVid[0].pause();
            gaTrack(['_trackEvent', '/contribute Page Interactions', 'pause', 'Get Involved video']);
            paused = true;
        } else if ($caption.is(':hidden') && $facesVid[0].paused) { // If the video is paused and caption is hidden
            $facesVid[0].play();
            gaTrack(['_trackEvent', '/contribute Page Interactions', 'play', 'Get Involved video']);
            paused = false;
        }

        // Toggle the button content/style
        if (paused) {
            $(this).attr('class', 'btn-play').text(window.trans('button-play'));
        } else {
            $(this).blur().attr('class', 'btn-pause').text(window.trans('button-pause'));
        }
    });

    // Track interest form submissions
    $('#help-form').on('submit', function(e) {
        e.preventDefault();
        var $form = $(this);
        $form.unbind('submit');

        gaTrack(
            ['_trackEvent', '/contribute Page Interactions', 'Want to Help Form - Area of Interest', $('#id_contribute-interest')[0].value],
            function() { $form.submit(); }
        );
    });

    // Track opportunity links
    $('#opportunities a').on('click', function(e) {
        e.preventDefault();
        var href = this.href;
        gaTrack(
            ['_trackEvent', '/contribute Page Interactions', 'exit link', href],
            function() { window.location = href; }
        );
    });


})(window.jQuery);
