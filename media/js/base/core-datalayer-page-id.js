/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function (Mozilla) {
    'use strict';

    // init dataLayer object
    var dataLayer = (window.dataLayer = window.dataLayer || []);
    var Analytics = {};

    /** Returns page ID used in Event Category for GA events tracked on page.
     * @param {String} path - URL path name fallback if page ID does not exist.
     * @return {String} GTM page ID.
     */
    Analytics.getPageId = function (path) {
        var pageId = document
            .getElementsByTagName('html')[0]
            .getAttribute('data-gtm-page-id');
        var pathName = path ? path : document.location.pathname;

        return pageId
            ? pageId
            : pathName.replace(/^(\/\w{2}-\w{2}\/|\/\w{2,3}\/)/, '/');
    };

    Analytics.buildDataObject = function () {
        var dataObj = {
            event: 'page-id-loaded',
            pageId: Analytics.getPageId()
        };

        return dataObj;
    };

    // Push page ID into dataLayer so it's ready when GTM container loads.
    dataLayer.push(Analytics.buildDataObject());

    Mozilla.Analytics = Analytics;
})(window.Mozilla);
