/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function(Mozilla) {
    'use strict';

    new Mozilla.Survey({
        copyIntro: 'Hello! Would you be willing to take a minute to answer a few questions for Mozilla?',
        copyLink: 'Sure. I\'ll help.',
        surveyURL: 'https://www.surveygizmo.com/s3/2933792/Brand-Perception-Survey-2016-Homepage-Prototype-B-UI-iteration',
        container: '#footer'
    });
})(window.Mozilla);
