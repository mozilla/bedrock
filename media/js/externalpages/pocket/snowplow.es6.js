/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* global snowplow */

(function () {
    const isProduction = !window.location.host.includes('localhost');
    const SNOWPLOW_URL = `https://assets.getpocket.com/web-utilities/public/static/${
        isProduction ? 'te' : 'sp'
    }.js`;
    function getUserData() {
        const data = {
            hashed_user_id: Mozilla.Cookies.getItem('a95b4b6'),
            hashed_guid: Mozilla.Cookies.getItem('sess_guid')
        };
        Object.keys(data).forEach((key) => {
            if (data[key] === null) {
                delete data[key];
            }
        });
        if (Object.keys(data).length) {
            return data;
        } else {
            return null;
        }
    }
    // https://docs.snowplowanalytics.com/docs/collecting-data/collecting-from-own-applications/javascript-trackers/javascript-tracker/javascript-tracker-v3/tracker-setup/loading/
    (function (p, l, o, w, i, n, g) {
        if (!p[i]) {
            p.GlobalSnowplowNamespace = p.GlobalSnowplowNamespace || [];
            p.GlobalSnowplowNamespace.push(i);
            p[i] = function () {
                (p[i].q = p[i].q || []).push(arguments);
            };
            p[i].q = p[i].q || [];
            n = l.createElement(o);
            g = l.getElementsByTagName(o)[0];
            n.async = 1;
            n.src = w;
            g.parentNode.insertBefore(n, g);
        }
    })(window, document, 'script', SNOWPLOW_URL, 'snowplow');
    const connectorUrl = isProduction
        ? 'getpocket.com'
        : 'com-getpocket-prod1.mini.snplow.net';
    const appId = isProduction ? 'pocket-web-mktg' : 'pocket-web-mktg-dev';
    // https://docs.snowplowanalytics.com/docs/collecting-data/collecting-from-own-applications/javascript-trackers/javascript-tracker/javascript-tracker-v3/tracker-setup/initialization-options/
    snowplow('newTracker', 'sp', connectorUrl, {
        appId,
        platform: 'web',
        eventMethod: 'beacon',
        respectDoNotTrack: false,
        contexts: {
            webPage: true,
            performanceTiming: true
        }
    });
    const data = getUserData();
    if (data) {
        snowplow('addGlobalContexts', [
            {
                schema: `iglu:com.pocket/user/jsonschema/1-0-0`,
                data
            }
        ]);
    }
    snowplow(
        'enableActivityTracking',
        10, // heartbeat delay
        10 // heartbeat interval
    );
    snowplow('enableLinkClickTracking');
    snowplow('enableFormTracking');
    snowplow('trackPageView');
})();
