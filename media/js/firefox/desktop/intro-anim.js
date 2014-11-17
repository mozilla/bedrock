/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var isIE = /MSIE/.test(navigator.userAgent);
    var isTrident = /Trident/.test(navigator.userAgent);
    var isOldOpera= /Presto/.test(navigator.userAgent);

    function cutsTheMustard() {
        // temporarily disable on Firefox OSX until graphics bug (1083079) is fixed
        if (window.isFirefox() && window.getFirefoxMasterVersion() >= 35 && $('html').hasClass('osx')) {
            return false;
        }

        return supportsInlineSVG() && !isIE && !isTrident && !isOldOpera;
    }

    function supportsInlineSVG () {
        var div = document.createElement('div');
        div.innerHTML = '<svg/>';
        return (div.firstChild && div.firstChild.namespaceURI) == 'http://www.w3.org/2000/svg';
    }

    if (!cutsTheMustard()) {
        // use fallback browser image
        $('body').addClass('no-svg-anim');
    } else {
        // show svg anim
        $(window).on('load', function() {
            $('body').addClass('svg-anim');
        });
    }

})(window.jQuery);
