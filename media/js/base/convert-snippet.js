/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    var CONVERT_PROJECT_ID = document
        .getElementsByTagName('html')[0]
        .getAttribute('data-convert-project-id');

    // Load third-party JS async and respect DNT.
    if (
        CONVERT_PROJECT_ID &&
        typeof Mozilla.dntEnabled === 'function' &&
        !Mozilla.dntEnabled()
    ) {
        var newScriptTag = document.createElement('script');
        var target = document.getElementsByTagName('script')[0];
        newScriptTag.src =
            'https://cdn-4.convertexperiments.com/js/' +
            CONVERT_PROJECT_ID +
            '.js';
        target.parentNode.insertBefore(newScriptTag, target);
    }
})();
