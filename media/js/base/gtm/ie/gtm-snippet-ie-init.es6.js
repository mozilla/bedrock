/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import GTMSnippet from '../gtm-snippet.es6.js';

// Push page ID into dataLayer so it's ready when GTM container loads.
const dataLayer = (window.dataLayer = window.dataLayer || []);

/**
 * Get the page ID from the data-gtm-page-id attribute on the html element.
 * @returns {string} The page ID to be used in GTM.
 */
function getPageId() {
    const pageId = document
        .getElementsByTagName('html')[0]
        .getAttribute('data-gtm-page-id');
    const pathName = document.location.pathname;

    return pageId
        ? pageId
        : pathName.replace(/^(\/\w{2}-\w{2}\/|\/\w{2,3}\/)/, '/');
}

/**
 * Monkey patch for dataLayer.push
 * Adds href stripped of locale to link click objects when pushed to the dataLayer,
 * also removes protocol and host if same as parent page from href.
 */
function updateDataLayerPush() {
    const dataLayer = (window.dataLayer = window.dataLayer || []);
    const hostname = document.location.hostname;

    dataLayer.defaultPush = dataLayer.push;
    dataLayer.push = function () {
        for (let i = 0; i < arguments.length; i++) {
            if (arguments[i].event === 'gtm.linkClick') {
                const element = arguments[i]['gtm.element'];
                const href = element.href;

                if (element.hostname === hostname) {
                    // remove host and locale from internal links
                    let path = href.replace(/^(?:https?:\/\/)(?:[^/])*/, '');
                    const locale = path.match(/^(\/\w{2}-\w{2}\/|\/\w{2,3}\/)/);

                    path = locale ? path.replace(locale[0], '/') : path;
                    arguments[i].newClickHref = path;
                } else {
                    arguments[i].newClickHref = href;
                }

                dataLayer.defaultPush(arguments[i]);
            } else {
                dataLayer.defaultPush(arguments[i]);
            }
        }
    };
}

dataLayer.push({
    event: 'page-id-loaded',
    pageId: getPageId()
});

GTMSnippet.init();

// Monkey patch dataLayer.push() click events
updateDataLayerPush();
