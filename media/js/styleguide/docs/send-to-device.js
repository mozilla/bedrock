/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* eslint-disable no-console */

$(function() {
    'use strict';

    var form = new Mozilla.SendToDevice();

    form.geoCallback = function(countryCode) {
        console.log('The country code is: ' + countryCode);
    };

    form.init();
});
