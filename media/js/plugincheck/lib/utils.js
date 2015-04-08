/*globals versionCompare */

(function(exports) {

    'use strict';

    var Utils = {
        /**
        * Tests a substring against the userAgent string to determine the current
        * operating system. If a match is found, it returns the identity as set
        * in the operatingSystems array. Based on PPK's BrowserDetect library.
        *
        * @param {string} userAgent - The navigator.userAgent string
        *
        * @returns The operating system identity or Unknown OS
        */
        getOS: function(userAgent) {
            var operatingSystems = [{ substring: 'Win', identity: 'win' },
                { substring: 'Mac', identity: 'mac' },
                { substring: 'Linux', identity: 'lin' }];

            for (var i = 0, l = operatingSystems.length; i < l; i++) {
                var currentOS = operatingSystems[i];

                if (userAgent.indexOf(currentOS.substring) > -1) {
                    return currentOS.identity;
                }
            }
            return 'Unknown OS';
        },
        /**
        * Determines whether there is an exact match between the installedVersion
        * and a version number is the list of knownReleases.
        *
        * @param {string} installedVersion - The current version number
        * @param {array} knownReleases - Array of versions to compare against
        * @returns the matched release' plugin info or false for no match
        */
        isMatch: function(installedVersion, knownReleases) {

            for (var i = 0, l = knownReleases.length; i < l; i++) {
                // TODO: the server currently returns some versions with a leading
                // space, therefore the trim workaround is currently required.
                // Remove the trims once the backend rewrite is done.
                var knownVersion = $.trim(knownReleases[i].version);
                var match = versionCompare(installedVersion, knownVersion,
                { zeroExtend: true });

                if (!match) {
                    return knownReleases[i];
                }
            }
            return false;
        }
    };

    exports.Utils = Utils;

})(window);
