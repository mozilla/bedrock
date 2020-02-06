/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    var Convert = {};

    Convert.onLoaded = function(callback) {
        var timeout;
        var pollRetry = 0;

        /**
         * This is a crude function that checks for the existence of
         * a global `convert` variable which gets set once the Convert
         * snippet loads, and then fires a callback with a reference to
         * that variable. If the snippet does not load after polling
         * repeatedly, we give up and callback with a falsy value.
         */
        function checkHasLoaded() {
            if (window.convert) {
                clearTimeout(timeout);
                window.convert.$(document).ready(function() {
                    callback(window.convert);
                });
            } else {
                if (pollRetry > 30) {
                    clearTimeout(timeout);
                    callback(false);
                } else {
                    pollRetry += 1;
                    timeout = setTimeout(checkHasLoaded, 200);
                }
            }
        }

        checkHasLoaded();
    };

    Convert.getCurrentExperiment = function(convert) {
        /**
         * The following code relies on an object constructed by
         * a third-party, so let's use a safety net.
         */
        try {
            var refObject = convert['data']['experiments'];
            var key;

            // Get the variation key
            for (key in convert['currentData']['experiments']) {
                if (!Object.prototype.hasOwnProperty.call(convert['currentData']['experiments'], key)) {
                    continue;
                }
            }

            /**
             * If a variation key exists, look up the related experiment data.
             * Then get the experiment name and variation name.
             */
            if (key) {
                var currentExperiment = convert['currentData']['experiments'][key];
                var curExperimentName = refObject[key] && refObject[key].n ? refObject[key].n : null;
                var curVariant = currentExperiment['variation_name'] ? currentExperiment['variation_name'] : null;

                if (curExperimentName && curVariant) {
                    var reg = new RegExp('^[0-9]+$');

                    var data = {
                        experimentName: curExperimentName.replace('Test #', ''),
                        experimentVariation: curVariant.replace('Var #', '')
                    };

                    if (reg.test(data.experimentName) && reg.test(data.experimentVariation)) {
                        return data;
                    }

                    throw new Error('Mozilla.Convert.getCurrentExperiment: data was malformed');
                }
            }

            return false;

        } catch(e) {
            // log errors thrown in the console to make debugging easier.
            if ('console' in window && typeof console.error === 'function') {
                console.error(e);
            }
            return false;
        }
    };

    window.Mozilla.Convert = Convert;

})();
