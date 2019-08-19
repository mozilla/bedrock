/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    var UtilsIE = {};

    /**
     * Bug 393263 A special function for legacy IE.
     * Without this hack there is no prompt to download after they click. sigh.
     * @param {link} direct link to download URL
     */
    UtilsIE.triggerIEDownload = function(link) {
        if (link) {
            window.open(link, 'download_window', 'toolbar=0,location=no,directories=0,status=0,scrollbars=0,resizeable=0,width=1,height=1,top=0,left=0');
            window.focus();
        }
    };

    // attach an event to all the download buttons to trigger the special
    // ie functionality if on ie
    UtilsIE.initDownloadLinks = function() {
        $('.download-link').each(function() {
            var $el = $(this);
            $el.click(function() {
                UtilsIE.triggerIEDownload($el.data('direct-link'));
            });
        });
        $('.download-list').attr('role', 'presentation');
    };

    UtilsIE.initNavigation = function() {
        $('.mzp-c-navigation-menu-button').on('click', function(e) {
            e.preventDefault();
            var $menuButton = $(e.target);
            var $menu = $('#' + $menuButton.attr('aria-controls'));
            $menu.find('.mzp-c-navigation-menu').toggle();
        });
    };

    window.Mozilla.UtilsIE = UtilsIE;

})();
