/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
 
;$(function () {
    'use strict';

    var $headline = $('#main-feature > h1');
    var $subheading = $('#main-feature > h3');

    if (isFirefox()) {
        if (isFirefoxUpToDate()) {
            $headline.html(trans('head-uptodate'));
            $subheading.html(trans('sub-uptodate'));
        } else {
            $headline.html(trans('head-outofdate'));
            $subheading.html(trans('sub-outofdate'));
        }
    }
});
