/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var dataLayer = window.dataLayer = window.dataLayer || [];

    function initGA() {
        var GTM_CONTAINER_ID = document.getElementsByTagName('html')[0].getAttribute('data-gtm-container-id');

        if (GTM_CONTAINER_ID) {
            (function(w,d,s,l,i,j,f,dl,k,q){
                w[l]=w[l]||[];w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});f=d.getElementsByTagName(s)[0];
                k=i.length;q='//www.googletagmanager.com/gtm.js?id=@&l='+(l||'dataLayer');
                while(k--){j=d.createElement(s);j.async=!0;j.src=q.replace('@',i[k]);f.parentNode.insertBefore(j,f);}
            }(window,document,'script','dataLayer',[GTM_CONTAINER_ID]));
        }
    }

    function getPageId() {
        var pageId = document.getElementsByTagName('html')[0].getAttribute('data-gtm-page-id');
        var pathName = document.location.pathname;

        return pageId ? pageId : pathName.replace(/^(\/\w{2}-\w{2}\/|\/\w{2,3}\/)/, '/');
    }

    /**
     * Monkey patch for dataLayer.push
     * Adds href stripped of locale to link click objects when pushed to the dataLayer,
     * also removes protocol and host if same as parent page from href.
     */
    function updateDataLayerPush() {
        var dataLayer = window.dataLayer = window.dataLayer || [];
        var hostname = document.location.hostname;

        dataLayer.defaultPush = dataLayer.push;
        dataLayer.push = function() {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i].event === 'gtm.linkClick') {
                    var element = arguments[i]['gtm.element'];
                    var href = element.href;

                    if (element.hostname === hostname) {
                        // remove host and locale from internal links
                        var path = href.replace(/^(?:https?:\/\/)(?:[^/])*/, '');
                        var locale = path.match(/^(\/\w{2}-\w{2}\/|\/\w{2,3}\/)/);

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

    // Push page ID into dataLayer so it's ready when GTM container loads.
    dataLayer.push({
        'event': 'page-id-loaded',
        'pageId': getPageId()
    });

    // Load GA script.
    initGA();

    // Monkey patch dataLayer.push() click events
    updateDataLayerPush();

})();
