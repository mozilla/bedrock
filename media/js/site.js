/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    var site = {
        platform: 'windows'
    };

    if(navigator.platform.indexOf("Win32") != -1 ||
       navigator.platform.indexOf("Win64") != -1) {
        site.platform = 'windows';
    }
    else if (navigator.platform.indexOf("armv7l") != -1) {
        site.platform = 'android';
    }
    else if(navigator.platform.indexOf("Linux") != -1) {
        site.platform = 'linux';
    }
    else if(navigator.platform.indexOf("MacPPC") != -1) {
        site.platform = 'oldmac';
    }
    else if (/Mac OS X 10.[0-5]/.test(navigator.userAgent)) {
        site.platform = 'oldmac';
    }
    else if (navigator.userAgent.indexOf("Mac OS X") != -1) {
        site.platform = 'osx';
    }
    else if (navigator.userAgent.indexOf("MSIE 5.2") != -1) {
        site.platform = 'oldmac';
    }
    else if (navigator.platform.indexOf("Mac") != -1) {
        site.platform = 'oldmac';
    }
    else {
        site.platform = 'other';
    }

    function init() {
        // Add the platform as a classname on the html-element immediately to avoid lots
        // of flickering
        var h = document.documentElement;
        h.className = h.className.replace("windows", site.platform);

        // Add class to reflect javascript availability for CSS
        h.className = h.className.replace(/\bno-js\b/,'js');
    }

    init();
    window.site = site;
})();
