/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const FxaAttribution = {};

const _allowedDomains = [
    'https://accounts.firefox.com/',
    'https://accounts.stage.mozaws.net/',
    'https://monitor.firefox.com/',
    'https://getpocket.com/',
    'https://vpn.mozilla.org/',
    'https://stage.guardian.nonprod.cloudops.mozgcp.net/',
    'https://guardian-dev.herokuapp.com/'
];

const _allowedUtmParams = [
    'utm_source',
    'utm_campaign',
    'utm_content',
    'utm_term',
    'utm_medium'
];

const _allowedFxaParams = [
    'device_id',
    'flow_id',
    'flow_begin_time',
    'entrypoint_experiment',
    'entrypoint_variation'
];

const _validParamChars = /^[\w/.%-]+$/;
const _referralCookieID = 'fxa-product-referral-id';

/**
 * Returns the hostname for a given URL.
 * @param {String} url.
 * @returns {String} hostname.
 */
FxaAttribution.getHostName = (url) => {
    const matches = url.match(/^https?:\/\/(?:[^/?#]+)(?:[/?#]|$)/i);
    return matches && matches[0];
};

FxaAttribution.getFxALinkReferralData = () => {
    const cookiesEnabled =
        typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();
    let data;

    if (cookiesEnabled && FxaAttribution.hasFxALinkReferralCookie()) {
        const campaign = FxaAttribution.getFxALinkReferralCookie();

        if (typeof campaign === 'string' && _validParamChars.test(campaign)) {
            let utmSource = 'www.mozilla.org';

            if (campaign.indexOf('whatsnew') !== -1) {
                utmSource = 'www.mozilla.org-whatsnew';
            }

            if (campaign.indexOf('welcome') !== -1) {
                utmSource = 'www.mozilla.org-welcome';
            }

            data = {
                entrypoint: utmSource,
                utm_source: utmSource,
                utm_medium: 'referral',
                utm_campaign: campaign
            };
        }
    }

    if (data) {
        return data;
    }

    return null;
};

FxaAttribution.getReferrer = (ref) => {
    const referrer = typeof ref === 'string' ? ref : document.referrer;

    if (typeof window.Mozilla.Analytics !== 'undefined') {
        return Mozilla.Analytics.getReferrer(referrer);
    }

    return referrer;
};

FxaAttribution.getSearchReferralData = (ref) => {
    const referrer = FxaAttribution.getReferrer(ref);
    const google = /^https?:\/\/www\.google\.\w{2,3}(\.\w{2})?\/?/;
    const bing = /^https?:\/\/www\.bing\.com\/?/;
    const yahoo = /^https?:\/\/(\w*\.)?search\.yahoo\.com\/?/;
    const duckduckgo = /^https?:\/\/duckduckgo\.com\/?/;
    const yandex = /^https?:\/\/yandex\.\w{2,3}(\.\w{2})?\/?/;
    const baidu = /^https?:\/\/www\.baidu\.com\/?/;
    const naver = /^https?:\/\/search\.naver\.com\/?/;

    let data = {
        utm_medium: 'organic'
    };

    switch (true) {
        case google.test(referrer):
            data.utm_source = 'google';
            break;
        case bing.test(referrer):
            data.utm_source = 'bing';
            break;
        case yahoo.test(referrer):
            data.utm_source = 'yahoo';
            break;
        case duckduckgo.test(referrer):
            data.utm_source = 'duckduckgo';
            break;
        case yandex.test(referrer):
            data.utm_source = 'yandex';
            break;
        case baidu.test(referrer):
            data.utm_source = 'baidu';
            break;
        case naver.test(referrer):
            data.utm_source = 'naver';
            break;
        default:
            data = null;
    }

    return data;
};

FxaAttribution.hasFxALinkReferralCookie = () => {
    return Mozilla.Cookies.hasItem(_referralCookieID);
};

FxaAttribution.getFxALinkReferralCookie = () => {
    return Mozilla.Cookies.getItem(_referralCookieID);
};

FxaAttribution.setFxALinkReferralCookie = (id) => {
    const cookiesEnabled =
        typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();

    if (id && cookiesEnabled && !FxaAttribution.hasFxALinkReferralCookie()) {
        const date = new Date();
        date.setTime(date.getTime() + 1 * 3600 * 1000); // expiry in 1 hour.
        const expires = date.toUTCString();

        Mozilla.Cookies.setItem(
            'fxa-product-referral-id',
            id,
            expires,
            '/',
            undefined,
            false,
            'lax'
        );
    }
};

FxaAttribution.onFxALinkReferralClick = (e) => {
    const newTab = e.target.target === '_blank' || e.metaKey || e.ctrlKey;
    const referralId = e.target.getAttribute('data-referral-id');

    if (!newTab) {
        e.preventDefault();
    }

    FxaAttribution.setFxALinkReferralCookie(referralId);

    if (!newTab) {
        window.location.href = e.target.href;
    }
};

FxaAttribution.bindFxALinkReferrals = () => {
    const ctaLinks = document.querySelectorAll('.js-fxa-product-referral-link');

    for (let i = 0; i < ctaLinks.length; i++) {
        ctaLinks[i].addEventListener(
            'click',
            FxaAttribution.onFxALinkReferralClick,
            false
        );
    }
};

FxaAttribution.filterParams = (params, allowList) => {
    const filteredParams = {};

    for (let i = 0; i < allowList.length; i++) {
        const param = allowList[i];
        if (Object.prototype.hasOwnProperty.call(params, param)) {
            try {
                const foundParam = decodeURIComponent(params[param]);
                if (_validParamChars.test(foundParam)) {
                    filteredParams[param] = foundParam;
                }
            } catch (e) {
                // silently drop malformed parameter values (issue #10897)
            }
        }
    }

    return filteredParams;
};

FxaAttribution.getUtmData = (params) => {
    const finalParams = FxaAttribution.filterParams(params, _allowedUtmParams);

    // Both `utm_source` and `utm_campaign` are considered required, so only pass through UTM data if the both are both present.
    if (
        Object.prototype.hasOwnProperty.call(finalParams, 'utm_source') &&
        Object.prototype.hasOwnProperty.call(finalParams, 'utm_campaign')
    ) {
        return finalParams;
    }

    return null;
};

FxaAttribution.getExperimentData = (params) => {
    const finalParams = FxaAttribution.filterParams(params, _allowedFxaParams);

    // Pass through `entrypoint_experiment` and `entrypoint_variation` only if both are present.
    if (
        Object.prototype.hasOwnProperty.call(
            finalParams,
            'entrypoint_experiment'
        ) &&
        Object.prototype.hasOwnProperty.call(
            finalParams,
            'entrypoint_variation'
        )
    ) {
        return finalParams;
    }

    return null;
};

FxaAttribution.getCouponData = (params) => {
    if (typeof params !== 'object') {
        return null;
    }

    for (const param in params) {
        if (Object.prototype.hasOwnProperty.call(params, param)) {
            if (param === 'coupon' && _validParamChars.test(params[param])) {
                return { coupon: params[param] };
            }
        }
    }
    return null;
};

/**
 * Append an object of accepted parameters to a given URL.
 * Object parameters will erase all existing accepted parameters, whether present or not.
 * @param {String} URL to append parameters to.
 * @param {Object} data object consisting of one or more parameters.
 * @returns {String} URL containing updated parameters.
 */
FxaAttribution.appendToProductURL = (url, data) => {
    let finalParams;
    let linkParams;

    if (url.indexOf('?') > 0) {
        linkParams = window._SearchParams.queryStringToObject(
            url.split('?')[1]
        );

        // If we have utm parameters then remove them from the target URL,
        // as we don't want to muddle data from different campaign sources.
        if (
            Object.prototype.hasOwnProperty.call(data, 'utm_source') &&
            Object.prototype.hasOwnProperty.call(data, 'utm_campaign')
        ) {
            for (let i = 0; i < _allowedUtmParams.length; i++) {
                const utmParam = _allowedUtmParams[i];
                if (
                    Object.prototype.hasOwnProperty.call(linkParams, utmParam)
                ) {
                    delete linkParams[utmParam];
                }
            }
        }

        // In principle, experiments should never clobber eachother(!). However, if we have
        // new entrypoint_* parameters then assume they take precedence in the target URL.
        if (
            Object.prototype.hasOwnProperty.call(
                data,
                'entrypoint_experiment'
            ) &&
            Object.prototype.hasOwnProperty.call(data, 'entrypoint_variation')
        ) {
            for (let j = 0; j < _allowedFxaParams.length; j++) {
                const fxaParam = _allowedFxaParams[j];
                if (
                    Object.prototype.hasOwnProperty.call(linkParams, fxaParam)
                ) {
                    delete linkParams[fxaParam];
                }
            }
        }

        finalParams = Object.assign(linkParams, data);

        // Only append coupons to FxA /subscribe/ links.
        if (
            Object.prototype.hasOwnProperty.call(finalParams, 'coupon') &&
            url.indexOf('/subscriptions/') === -1
        ) {
            delete finalParams['coupon'];
        }
    } else {
        finalParams = data;
    }

    return (
        url.split('?')[0] +
        '?' +
        window._SearchParams.objectToQueryString(finalParams)
    );
};

FxaAttribution.getAttributionData = (urlParams) => {
    let params = {};
    const utmData = FxaAttribution.getUtmData(urlParams);
    const experimentData = FxaAttribution.getExperimentData(urlParams);
    const couponData = FxaAttribution.getCouponData(urlParams);

    // If there are UTM params in the page URL, then
    // validate those as referral data.
    if (utmData) {
        params = Object.assign(params, utmData);
    } else {
        // Check to see if there's a referral cookie.
        const linkData = FxaAttribution.getFxALinkReferralData();

        if (linkData) {
            params = Object.assign(params, linkData);
        } else {
            // Check to for search engine referral data.
            const searchData = FxaAttribution.getSearchReferralData();

            if (searchData) {
                params = Object.assign(params, searchData);
            }
        }
    }

    // Always pass along experiment data.
    if (experimentData) {
        params = Object.assign(params, experimentData);
    }

    // Always pass a coupon when present as a parameter.
    if (couponData) {
        params = Object.assign(params, couponData);
    }

    return params;
};

/**
 * If there are validated referral params on the page URL, query the
 * DOM and update Firefox Account links with the new param data.
 */
FxaAttribution.init = (urlParams) => {
    // feature detect support for object modification.
    if (typeof Object.assign !== 'function') {
        return;
    }

    const ctaLinks = document.querySelectorAll(
        '.js-fxa-cta-link, .js-fxa-product-cta-link'
    );

    // Track CTA clicks for FxA link referrals.
    FxaAttribution.bindFxALinkReferrals();

    const params = FxaAttribution.getAttributionData(urlParams);

    // If there is no referral data, then do nothing.
    if (Object.keys(params).length === 0) {
        return;
    }

    for (let i = 0; i < ctaLinks.length; i++) {
        // get the link off the element
        const oldAccountsLink = ctaLinks[i].hasAttribute('href')
            ? ctaLinks[i].href
            : null;

        if (oldAccountsLink) {
            const hostName = FxaAttribution.getHostName(oldAccountsLink);
            // check if link is in the FxA referral _allowedDomains list.
            if (hostName && _allowedDomains.indexOf(hostName) !== -1) {
                // append our new UTM param data to create new FxA links.
                const newAccountsLink = FxaAttribution.appendToProductURL(
                    oldAccountsLink,
                    params
                );

                // set the FxA button to use the new link.
                ctaLinks[i].href = newAccountsLink;
            }
        }
    }
};

export default FxaAttribution;
