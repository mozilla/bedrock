/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const Utils = {
    getPathFromUrl: (path) => {
        const pathName = path ? path : document.location.pathname;
        return pathName.replace(/^(\/\w{2}-\w{2}\/|\/\w{2,3}\/)/, '/');
    },

    getLocaleFromUrl: (path) => {
        const pathName = path ? path : document.location.pathname;
        const locale = pathName.match(/^\/(\w{2}-\w{2}|\w{2,3})\//);
        // If there's no locale in the path then assume language is `en-US`;
        return locale && locale.length > 0 ? locale[1] : 'en-US';
    },

    getQueryParamsFromURL: (qs) => {
        const query = typeof qs === 'string' ? qs : window.location.search;

        if (typeof window._SearchParams !== 'undefined') {
            return new window._SearchParams(query);
        }

        return false;
    },

    getReferrer: (ref) => {
        return typeof ref === 'string' ? ref : document.referrer;
    },

    getHttpStatus: () => {
        const pageId = document
            .getElementsByTagName('html')[0]
            .getAttribute('data-http-status');
        return pageId && pageId === '404' ? '404' : '200';
    },

    hasValidURLScheme: (url) => {
        return /^https?:\/\//.test(url);
    },

    isTelemetryEnabled: () => {
        if (
            typeof Mozilla.Cookies !== 'undefined' &&
            Mozilla.Cookies.enabled()
        ) {
            return !Mozilla.Cookies.hasItem('moz-1st-party-data-opt-out');
        }
        return true;
    }
};

export default Utils;
