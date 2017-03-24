/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var OPTIMIZELY_PROJECT_ID = document.getElementsByTagName('html')[0].getAttribute('data-optimizely-project-id');

    // If doNotTrack is not enabled, it is ok to add Optimizely
    // @see https://bugzilla.mozilla.org/show_bug.cgi?id=1217896 for more details
    if (typeof window._dntEnabled === 'function' && !window._dntEnabled() && OPTIMIZELY_PROJECT_ID) {
        (function(d, optID) {
            var newScriptTag = d.createElement('script');
            var target = d.getElementsByTagName('script')[0];
            newScriptTag.src = 'https://cdn.optimizely.com/js/' + optID + '.js';
            target.parentNode.insertBefore(newScriptTag, target);
        }(document, OPTIMIZELY_PROJECT_ID));
    }
})();
