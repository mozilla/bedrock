/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    window.Mozilla.run = function(callback) {
        var isModernBrowser = window.site && window.site.isModernBrowser;

        if (isModernBrowser && typeof callback === 'function') {
            callback();
        }
    };
})(window.Mozilla);
