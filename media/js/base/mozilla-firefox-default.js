/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function() {
    'use strict';

    var FirefoxDefault = {};

    FirefoxDefault.isDefaultBrowser = function(callback) {

        if (typeof callback !== 'function') {
            throw new Error('isDefaultBrowser: first argument is not a function');
        }

        Mozilla.UITour.getConfiguration('appinfo', function (config) {
            if (config && config.defaultBrowser === true) {
                callback('yes');
            } else if (config && config.defaultBrowser === false) {
                callback('no');
            } else {
                callback('unknown');
            }
        });
    };

    FirefoxDefault.setDefaultBrowser = function() {
        Mozilla.UITour.setConfiguration('defaultBrowser');
    };

    FirefoxDefault.bindButton = function(selector) {
        var $button = $(selector);

        if ($button.length === 0) {
            throw new Error('bindClickEvent: selector ' + selector + ' not found.');
        }
        $button.on('click.default-browser', FirefoxDefault.setDefaultBrowser);
    };

    FirefoxDefault.unbindButton = function(selector) {
        $(selector).off('click.default-browser');
    };

    window.Mozilla.FirefoxDefault = FirefoxDefault;

})();
