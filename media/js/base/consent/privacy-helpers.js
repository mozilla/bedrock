/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

var dntEnabled = require('@mozmeao/dnt-helper');

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

// Expose dntEnabled to the global namespace
window.Mozilla.dntEnabled = dntEnabled;

// Expose gpcEnabled to the global namespace
window.Mozilla.gpcEnabled = function () {
    'use strict';
    return navigator.globalPrivacyControl;
};
