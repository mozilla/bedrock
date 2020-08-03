/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    var Utils = {};

    // Vanilla JS DOM Ready handler
    Utils.onDocumentReady = function(callback) {
        if (document.readyState !== 'loading') {
            callback();
        } else {
            document.addEventListener('DOMContentLoaded', callback);
        }
    };

    // Replace Google Play links on Android devices to let them open the marketplace app
    Utils.initMobileDownloadLinks = function() {
        if (site.platform === 'android') {
            var playLinks = document.querySelectorAll('a[href^="https://play.google.com/store/apps/"]');
            for (var i = 0; i < playLinks.length; ++i) {
                var playLink = playLinks[i];
                var oldHref = playLink.getAttribute('href');
                var newHref = oldHref.replace('https://play.google.com/store/apps/', 'market://');
                playLink.setAttribute('href', newHref);
            }
        }
    };

    // Bug 1264843: link to China build of Fx4A, for display within Fx China repack
    Utils.maybeSwitchToChinaRepackImages = function(client) {
        if (!client.distribution || client.distribution === 'default') {
            return;
        }

        var distribution = client.distribution.toLowerCase();
        var images = document.querySelectorAll('img[data-' + distribution + '-link]');

        for (var j = 0; j < images.length; j++) {
            var distributionSrc = images[j].getAttribute('data-' + distribution + '-link');
            images[j].setAttribute('src', distributionSrc);
        }
    };

    // client-side redirects (handy for testing)
    Utils.doRedirect = function(destination) {
        if (destination) {
            window.location.href = destination;
        }
    };

    // Create text translation function using #strings element.
    // TODO: Move to docs
    // In order to use it, you need a block string_data bit inside your template,
    // then, each key name needs to be preceded by data- as this uses data attributes
    // to work. After this, you can access all strings defined inside the
    // string_data block in JS using Mozilla.Utils.trans('key-of-string'); Thank @mkelly
    var _strings = document.getElementById('strings');
    Utils.trans = function(stringId) {
        if (_strings) {
            return _strings.getAttribute('data-' + stringId);
        } else {
            return undefined;
        }
    };

    window.Mozilla.Utils = Utils;

})();
