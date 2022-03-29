/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const FxaUtm = {};

const allowedList = [
    'https://accounts.firefox.com/',
    'https://accounts.stage.mozaws.net/',
    'https://monitor.firefox.com/',
    'https://getpocket.com/',
    'https://vpn.mozilla.org/',
    'https://stage-vpn.guardian.nonprod.cloudops.mozgcp.net/',
    'https://guardian-dev.herokuapp.com/'
];

const utms = [
    'utm_source',
    'utm_campaign',
    'utm_content',
    'utm_term',
    'utm_medium'
];

const fxaParams = [
    'device_id',
    'flow_id',
    'flow_begin_time',
    'entrypoint_experiment',
    'entrypoint_variation'
];

const sameSiteParams = ['source'];
const acceptedParams = utms.concat(fxaParams, sameSiteParams);
const referralCookieID = 'fxa-product-referral-id';

/**
 * Returns the hostname for a given URL.
 * @param {String} url.
 * @returns {String} hostname.
 */
FxaUtm.getHostName = function (url) {
    const matches = url.match(/^https?:\/\/(?:[^/?#]+)(?:[/?#]|$)/i);
    return matches && matches[0];
};

/**
 * Detect if a given object contains keys that map to utm parameters.
 * @param {Object} params.
 * @returns {Boolean}.
 */
FxaUtm.hasUtmParams = function (params) {
    if (typeof params !== 'object') {
        return false;
    }

    for (const param in params) {
        if (Object.prototype.hasOwnProperty.call(params, param)) {
            if (param.indexOf('utm_') === 0) {
                return true;
            }
        }
    }
    return false;
};

FxaUtm.getFxALinkReferralData = function (params) {
    const cookiesEnabled =
        typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();
    const allowedChars = /^[\w/.%-]+$/;
    let data;

    if (cookiesEnabled && FxaUtm.hasFxALinkReferralCookie()) {
        const campaign = FxaUtm.getFxALinkReferralCookie();

        if (typeof campaign === 'string' && allowedChars.test(campaign)) {
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

    if (data && params && typeof params === 'object') {
        return Object.assign(params, data);
    } else if (data) {
        return data;
    }

    return null;
};

FxaUtm.hasFxALinkReferralCookie = function () {
    return Mozilla.Cookies.hasItem(referralCookieID);
};

FxaUtm.getFxALinkReferralCookie = function () {
    return Mozilla.Cookies.getItem(referralCookieID);
};

FxaUtm.setFxALinkReferralCookie = function (id) {
    const cookiesEnabled =
        typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();

    if (id && cookiesEnabled && !FxaUtm.hasFxALinkReferralCookie()) {
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

FxaUtm.onFxALinkReferralClick = function (e) {
    const newTab = e.target.target === '_blank' || e.metaKey || e.ctrlKey;
    const referralId = e.target.getAttribute('data-referral-id');

    if (!newTab) {
        e.preventDefault();
    }

    FxaUtm.setFxALinkReferralCookie(referralId);

    if (!newTab) {
        window.location.href = e.target.href;
    }
};

FxaUtm.bindFxALinkReferrals = function () {
    const ctaLinks = document.querySelectorAll('.js-fxa-product-referral-link');

    for (let i = 0; i < ctaLinks.length; i++) {
        ctaLinks[i].addEventListener(
            'click',
            FxaUtm.onFxALinkReferralClick,
            false
        );
    }
};

/**
 * Fetch and validate accepted params from the page URL for FxA referral.
 * https://mozilla.github.io/ecosystem-platform/docs/relying-parties/metrics-for-relying-parties#metrics-related-query-parameters
 * @returns {Object} if params are valid, else {null}.
 */
FxaUtm.getAttributionData = function (params) {
    const allowedChars = /^[\w/.%-]+$/;
    const finalParams = {};

    for (let i = 0; i < acceptedParams.length; i++) {
        const acceptedParam = acceptedParams[i];
        if (Object.prototype.hasOwnProperty.call(params, acceptedParam)) {
            try {
                const foundParam = decodeURIComponent(params[acceptedParam]);
                if (allowedChars.test(foundParam)) {
                    finalParams[acceptedParam] = foundParam;
                }
            } catch (e) {
                // silently drop malformed parameter values (issue #10897)
            }
        }
    }

    /**
     * Occasionally we link to a mozorg product landing page (e.g. VPN) via an in-product page such as /whatsnew
     * or /welcome. Here we want to avoid using utm params on internal links since that's bad, so instead we support
     * the option of passing a `source` parameter to help connect attribution with FxA link referrals.
     */
    if (Object.prototype.hasOwnProperty.call(finalParams, 'source')) {
        if (
            finalParams['source'].indexOf('whatsnew') !== -1 ||
            finalParams['source'].indexOf('welcome') !== -1 ||
            finalParams['source'].indexOf('vpn-info') !== -1
        ) {
            // utm_source and entrypoint should always be consistent and omit a version number.
            if (finalParams['source'].indexOf('vpn-info') !== -1) {
                finalParams['utm_source'] = 'www.mozilla.org-vpn-info';
                finalParams['entrypoint'] = 'www.mozilla.org-vpn-info';
            } else if (finalParams['source'].indexOf('whatsnew') !== -1) {
                finalParams['utm_source'] = 'www.mozilla.org-whatsnew';
                finalParams['entrypoint'] = 'www.mozilla.org-whatsnew';
            } else {
                finalParams['utm_source'] = 'www.mozilla.org-welcome';
                finalParams['entrypoint'] = 'www.mozilla.org-welcome';
            }

            // utm_campaign should indicate which version the referral came from e.g. `whatsnew88`, `welcome9`.
            finalParams['utm_campaign'] = finalParams['source'];

            // delete the original source param afterward as it's no longer needed.
            delete finalParams['source'];

            return finalParams;
        } else {
            // if source doesn't contain a supported value then delete it.
            delete finalParams['source'];
        }
    }

    /**
     * Some experiments may redirect people back to the landing page from in-product (e.g. VPN Issue 10209).
     * In cases like this we want to support passing through FxA flow params to keep track of the funnel.
     */
    if (
        !Object.prototype.hasOwnProperty.call(
            finalParams,
            'entrypoint_experiment'
        ) ||
        !Object.prototype.hasOwnProperty.call(
            finalParams,
            'entrypoint_variation'
        )
    ) {
        if (Object.prototype.hasOwnProperty.call(finalParams, 'device_id')) {
            delete finalParams['device_id'];
        }

        if (Object.prototype.hasOwnProperty.call(finalParams, 'flow_id')) {
            delete finalParams['flow_id'];
        }

        if (
            Object.prototype.hasOwnProperty.call(finalParams, 'flow_begin_time')
        ) {
            delete finalParams['flow_begin_time'];
        }
    }

    // Both utm_source and utm_campaign are considered required, so only pass through referral data if they exist.
    // Alternatively, pass through entrypoint_experiment and entrypoint_variation independently.
    if (
        (Object.prototype.hasOwnProperty.call(finalParams, 'utm_source') &&
            Object.prototype.hasOwnProperty.call(
                finalParams,
                'utm_campaign'
            )) ||
        (Object.prototype.hasOwnProperty.call(
            finalParams,
            'entrypoint_experiment'
        ) &&
            Object.prototype.hasOwnProperty.call(
                finalParams,
                'entrypoint_variation'
            ))
    ) {
        return finalParams;
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
FxaUtm.appendToDownloadURL = function (url, data) {
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
            for (let i = 0; i < utms.length; i++) {
                const utmParam = utms[i];
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
            for (let j = 0; j < fxaParams.length; j++) {
                const fxaParam = fxaParams[j];
                if (
                    Object.prototype.hasOwnProperty.call(linkParams, fxaParam)
                ) {
                    delete linkParams[fxaParam];
                }
            }
        }

        finalParams = Object.assign(linkParams, data);
    } else {
        finalParams = data;
    }

    return (
        url.split('?')[0] +
        '?' +
        window._SearchParams.objectToQueryString(finalParams)
    );
};

/**
 * If there are validated referral params on the page URL, query the
 * DOM and update Firefox Account links with the new param data.
 */
FxaUtm.init = function (urlParams) {
    let params = FxaUtm.getAttributionData(urlParams);
    const ctaLinks = document.querySelectorAll(
        '.js-fxa-cta-link, .js-vpn-cta-link'
    );

    // feature detect support for object modification.
    if (typeof Object.assign !== 'function') {
        return;
    }

    // Track CTA clicks for FxA link referrals.
    FxaUtm.bindFxALinkReferrals();

    // If there a no utm params on the page URL, then assume this could have been a
    // same-site page navigation and check to see if there's a referral cookie.
    if (!FxaUtm.hasUtmParams(params)) {
        params = FxaUtm.getFxALinkReferralData(params);
    }

    // If there are is still no referral data, then do nothing.
    if (!params) {
        return;
    }

    for (let i = 0; i < ctaLinks.length; i++) {
        // get the link off the element
        const oldAccountsLink = ctaLinks[i].hasAttribute('href')
            ? ctaLinks[i].href
            : null;

        if (oldAccountsLink) {
            const hostName = FxaUtm.getHostName(oldAccountsLink);
            // check if link is in the FxA referral allowedList list.
            if (hostName && allowedList.indexOf(hostName) !== -1) {
                // append our new UTM param data to create new FxA links.
                const newAccountsLink = FxaUtm.appendToDownloadURL(
                    oldAccountsLink,
                    params
                );

                // set the FxA button to use the new link.
                ctaLinks[i].href = newAccountsLink;
            }
        }
    }
};

export default FxaUtm;
