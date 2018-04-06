/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* A simple HTML5 Video poster image helper.
 * https://bugzilla.mozilla.org/show_bug.cgi?id=1040213
 * CSS Styles: 'media/css/base/mozilla-video-poster.less' */

/* HTML markup:
<div class="moz-video-container">
  <button class="moz-video-button" type="button" aria-controls="some-video">{{ _('Play video') }}</button>
  <video id="some-video"></video>
</div>
*/

// create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

/*
 * HTML5 Video poster image helper.
 * @param selector (string) container for one or more video elements
 */
Mozilla.VideoPosterHelper = function (selector) {
    'use strict';

    this.$container = $(selector);
};

/*
 * If browser supports HTML5 Video show the poster button and bind events.
 * Else fallback content will be displayed natively by the browser.
 */
Mozilla.VideoPosterHelper.prototype.init = function () {
    'use strict';

    if (this.$container.length && this.supportsVideo()) {
        this.showPoster();
        this.bindEvents();
    }
};

/*
 * Check for HTML5 Video playback support
 */
Mozilla.VideoPosterHelper.prototype.supportsVideo = function () {
    'use strict';

    return typeof HTMLMediaElement !== 'undefined';
};

/*
 * Add CSS class to container to display .moz-video-button.
 */
Mozilla.VideoPosterHelper.prototype.showPoster = function () {
    'use strict';

    this.$container.addClass('supports-video');
};

/*
 * Bind click event to container and delegate events to .moz-video-button
 */
Mozilla.VideoPosterHelper.prototype.bindEvents = function () {
    'use strict';

    this.$container.on('click.moz-video', '.moz-video-button', function () {
        var $poster = $(this);
        var $video = $poster.closest('.moz-video-container').find('video');
        $video.css('visibility', 'visible');
        var videoMedia = $video[0];

        try {
            if (videoMedia && videoMedia.readyState && videoMedia.readyState > 0) {
                videoMedia.play();
            } else {
                videoMedia.load();
                videoMedia.play();
            }
        } catch(e) {
            // fail silently.
        }

        $poster.hide();
    });
};

/*
 * Unbind events and hide overlay button
 */
Mozilla.VideoPosterHelper.prototype.destroy = function () {
    'use strict';

    this.$container.off('click.moz-video');
    this.$container.removeClass('supports-video');
};
