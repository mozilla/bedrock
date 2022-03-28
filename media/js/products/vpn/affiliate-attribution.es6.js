/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FxaProductButton from '../../base/fxa-product-button.es6.js';

const AffiliateAttribution = {};
const _marketingCookieID = 'moz-vpn-affiliate';
const _preferenceCookieID = 'moz-pref-vpn-affiliate';

AffiliateAttribution.hasMarketingCookie = function () {
    return Mozilla.Cookies.hasItem(_marketingCookieID);
};

AffiliateAttribution.getMarketingCookie = function () {
    return Mozilla.Cookies.getItem(_marketingCookieID);
};

AffiliateAttribution.setMarketingCookie = function (value, expires) {
    // convert timestamp to milliseconds.
    const date = new Date(expires * 1000);
    Mozilla.Cookies.setItem(
        _marketingCookieID,
        value,
        date.toUTCString(),
        '/',
        null,
        false,
        'lax'
    );
};

AffiliateAttribution.removeMarketingCookie = function () {
    return Mozilla.Cookies.removeItem(_marketingCookieID, '/', null);
};

AffiliateAttribution.hasPreferenceCookie = function () {
    return Mozilla.Cookies.hasItem(_preferenceCookieID);
};

AffiliateAttribution.getPreferenceCookie = function () {
    return Mozilla.Cookies.getItem(_preferenceCookieID);
};

AffiliateAttribution.setPreferenceCookie = function (value) {
    const date = new Date();
    const cookieDuration = 30 * 24 * 60 * 60 * 1000; // 30 day expiration
    date.setTime(date.getTime() + cookieDuration);
    Mozilla.Cookies.setItem(
        _preferenceCookieID,
        value,
        date.toUTCString(),
        '/',
        null,
        false,
        'lax'
    );
};

AffiliateAttribution.meetsRequirements = function () {
    if (
        typeof Mozilla.Cookies === 'undefined' ||
        !Mozilla.Cookies.enabled() ||
        typeof window._SearchParams === 'undefined'
    ) {
        return false;
    }

    return 'Promise' in window && 'fetch' in window;
};

AffiliateAttribution.getQueryStringParam = function (name, qs) {
    const query = typeof qs === 'string' ? qs : window.location.search;
    const params = new window._SearchParams(query);
    return decodeURIComponent(params.get(name));
};

AffiliateAttribution.getCJEventParam = function () {
    const value = AffiliateAttribution.getQueryStringParam('cjevent');
    const allowedChars = /^\w{1,64}$/; // alpha-numeric string up to 64 chars.

    if (value === 'undefined' || !value || !allowedChars.test(value)) {
        return false;
    }

    return value.toString();
};

AffiliateAttribution.getCJMSEndpoint = function () {
    return document
        .getElementsByTagName('html')[0]
        .getAttribute('data-vpn-affiliate-endpoint');
};

AffiliateAttribution.fetch = function (flowId, cjID, value) {
    return new window.Promise((resolve, reject) => {
        const endpoint = AffiliateAttribution.getCJMSEndpoint();

        if (!endpoint) {
            reject('CJMS endpoint was not found.');
            return;
        }

        const endpointPath =
            typeof value === 'string' ? `${endpoint}/${value}` : endpoint;
        const method = typeof value === 'string' ? 'PUT' : 'POST';

        const obj = cjID
            ? { flow_id: flowId, cj_id: cjID }
            : { flow_id: flowId };

        window
            .fetch(endpointPath, {
                method: method,
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(obj)
            })
            .then((resp) => {
                if (resp.status >= 200 && resp.status <= 299) {
                    return resp.json();
                } else if (resp.status === 404 && method === 'PUT') {
                    return `Unknown aicID: ${value}`;
                } else {
                    return resp
                        .text()
                        .then((message) => {
                            return message;
                        })
                        .catch((e) => {
                            return e;
                        });
                }
            })
            .then((resp) => {
                if (resp.aic_id && resp.expires) {
                    resolve(resp);
                } else {
                    reject(resp);
                }
            })
            .catch((e) => {
                reject(e);
            });
    });
};

AffiliateAttribution.optOut = function () {
    return new window.Promise((resolve, reject) => {
        const overwrite = true;
        FxaProductButton.init(overwrite)
            .then(() => {
                AffiliateAttribution.setPreferenceCookie('reject');
                AffiliateAttribution.removeMarketingCookie();
                resolve();
            })
            .catch(() => {
                reject();
            });
    });
};

AffiliateAttribution.shouldShowOptOutNotification = function () {
    return (
        (Boolean(AffiliateAttribution.getCJEventParam()) ||
            AffiliateAttribution.hasMarketingCookie()) &&
        !AffiliateAttribution.hasPreferenceCookie()
    );
};

AffiliateAttribution.shouldInitiateAttributionFlow = function () {
    return (
        AffiliateAttribution.meetsRequirements() &&
        AffiliateAttribution.getPreferenceCookie() !== 'reject'
    );
};

AffiliateAttribution.addFlowParams = function () {
    FxaProductButton.init();
};

AffiliateAttribution.init = function () {
    if (!AffiliateAttribution.meetsRequirements()) {
        return false;
    }

    return new window.Promise((resolve, reject) => {
        const cjEventParamValue = AffiliateAttribution.getCJEventParam();

        FxaProductButton.init()
            .then((flowParams) => {
                const flowId = AffiliateAttribution.getQueryStringParam(
                    'flow_id',
                    flowParams
                );

                // If `cjevent` param exists in page URL.
                if (cjEventParamValue) {
                    // If marketing cookie already exists.
                    if (AffiliateAttribution.hasMarketingCookie()) {
                        const value = AffiliateAttribution.getMarketingCookie();
                        // Send the flow ID, cjevent param and cookie ID to the micro service.
                        AffiliateAttribution.fetch(
                            flowId,
                            cjEventParamValue,
                            value
                        )
                            .then((data) => {
                                AffiliateAttribution.setMarketingCookie(
                                    data.aic_id,
                                    data.expires
                                );
                                resolve();
                            })
                            .catch((e) => {
                                reject(e);
                            });
                    } else {
                        // Else just send the flow ID and cjevent param.
                        AffiliateAttribution.fetch(flowId, cjEventParamValue)
                            .then((data) => {
                                AffiliateAttribution.setMarketingCookie(
                                    data.aic_id,
                                    data.expires
                                );
                                resolve();
                            })
                            .catch((e) => {
                                reject(e);
                            });
                    }
                    // Else if no`cjevent` param exists but there is an marketing cookie set.
                } else if (AffiliateAttribution.hasMarketingCookie()) {
                    const value = AffiliateAttribution.getMarketingCookie();

                    // Send only the flow ID and cookie ID to the micro service.
                    AffiliateAttribution.fetch(flowId, null, value)
                        .then((data) => {
                            AffiliateAttribution.setMarketingCookie(
                                data.aic_id,
                                data.expires
                            );
                            resolve();
                        })
                        .catch((e) => {
                            reject(e);
                        });
                }
            })
            .catch((e) => {
                reject(e);
            });
    });
};

export default AffiliateAttribution;
