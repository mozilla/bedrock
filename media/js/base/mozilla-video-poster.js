/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* A simple HTML5 Video poster image helper.
 * https://bugzilla.mozilla.org/show_bug.cgi?id=1040213
 */

/* HTML markup:
<div class="moz-video-container">
  <button class="moz-video-button" type="button" aria-controls="some-video">Play video</button>
  <video id="some-video"></video>
</div>
*/

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

/*
 * HTML5 Video poster image helper.
 * @param selector (string) container for one or more video elements
 */
Mozilla.VideoPosterHelper = function (selector) {
    'use strict';

    this.container = document.querySelector(selector);
};

/*
 * If browser supports HTML5 Video show the poster button and bind events.
 * Else fallback content will be displayed natively by the browser.
 */
Mozilla.VideoPosterHelper.prototype.init = function () {
    'use strict';

    if (this.container && this.supportsVideo()) {
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

    this.container.classList.add('supports-video');
};

/*
 * Hide the poster image, play the video.
 */
Mozilla.VideoPosterHelper.prototype.play = function (e) {
    'use strict';

    var poster = e.target;
    var video = this.container.querySelector('video');
    video.setAttribute('style', 'visibility: visible;');

    try {
        if (video && video.readyState && video.readyState > 0) {
            video.play();
        } else {
            video.load();
            video.play();
        }
    } catch (e) {
        // fail silently.
    }

    poster.setAttribute('style', 'display: none;');
};

/*
 * Bind click event to container and delegate events to .moz-video-button
 */
Mozilla.VideoPosterHelper.prototype.bindEvents = function () {
    'use strict';

    this.button = this.container.querySelector('.moz-video-button');
    this.onPlayHandler = Mozilla.VideoPosterHelper.prototype.play.bind(this);
    this.button.addEventListener('click', this.onPlayHandler, false);
};

/*
 * Unbind events and hide overlay button
 */
Mozilla.VideoPosterHelper.prototype.destroy = function () {
    'use strict';

    this.button.removeEventListener('click', this.onPlayHandler, false);
    this.container.classList.remove('supports-video');
};
