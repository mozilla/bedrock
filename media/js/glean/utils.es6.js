/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const Utils = {
    getUrl: (str) => {
        const urlString = typeof str === 'string' ? str : window.location.href;
        const url = new URL(urlString);

        // Ensure we don't include tokens in newsletter page load event pings
        // Issue https://github.com/mozilla/bedrock/issues/13583
        const newsletterPaths = [
            '/newsletter/existing/',
            '/newsletter/country/'
        ];

        newsletterPaths.forEach((path) => {
            // Find the index of the newsletter pathname
            const index = url.pathname.indexOf(path);

            // Remove everything after the pathname (which is the token)
            if (index !== -1) {
                const newPathname = url.pathname.substring(
                    0,
                    index + path.length
                );
                url.pathname = newPathname;
            }
        });

        return url.toString();
    },

    getPathFromUrl: (str) => {
        let pathName =
            typeof str === 'string' ? str : document.location.pathname;
        pathName = pathName.replace(/^(\/\w{2}-\w{2}\/|\/\w{2,3}\/)/, '/');
        const newsletterPaths = [
            '/newsletter/existing/',
            '/newsletter/country/'
        ];

        // Ensure we don't include tokens in newsletter page pings
        // Issue https://github.com/mozilla/bedrock/issues/13583
        newsletterPaths.forEach((path) => {
            if (pathName.includes(path)) {
                pathName = path;
            }
        });

        return pathName;
    },

    getLocaleFromUrl: (str) => {
        const pathName =
            typeof str === 'string' ? str : document.location.pathname;
        const locale = pathName.match(/^\/(\w{2}-\w{2}|\w{2,3})\//);
        // If there's no locale in the path then assume language is `en-US`;
        return locale && locale.length > 0 ? locale[1] : 'en-US';
    },

    getQueryParamsFromUrl: (str) => {
        const query = typeof str === 'string' ? str : window.location.search;

        if (typeof window._SearchParams !== 'undefined') {
            return new window._SearchParams(query);
        }

        return false;
    },

    getReferrer: (str) => {
        const referrer = typeof str === 'string' ? str : document.referrer;

        if (typeof window.Mozilla.Analytics !== 'undefined') {
            return Mozilla.Analytics.getReferrer(referrer);
        }

        return referrer;
    },

    getHttpStatus: () => {
        const pageId = document
            .getElementsByTagName('html')[0]
            .getAttribute('data-http-status');
        return pageId && pageId === '404' ? '404' : '200';
    },

    isValidHttpUrl: (str) => {
        let url;

        try {
            url = new URL(str);
        } catch (e) {
            return false;
        }

        return url.protocol === 'http:' || url.protocol === 'https:';
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
