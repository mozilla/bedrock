/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof Mozilla == 'undefined') {
    var Mozilla = {};
}

/**
* Utility class for core dataLayer object to track contextual user and page data
*/

(function() {
    var Analytics = {};

    /** Returns page ID used in Event Category for GA events tracked on page.
    * @param {String} path - URL path name fallback if page ID does not exist.
    * @return {String} GTM page ID.
    */
    Analytics.getPageId = function(path) {
        var pageId = $('html').attr('data-gtm-page-id');
        var pathName = path ? path : document.location.pathname;

        return pageId ? pageId : pathName.replace(/\/[^\/]*/, '');
    };

    Mozilla.Analytics = Analytics;

})();

