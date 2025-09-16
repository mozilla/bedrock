/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const FxaCoupon = {};

const _allowedDomains = [
    'accounts.firefox.com',
    'accounts.stage.mozaws.net',
    'payments-next.allizom.org',
    'payments.firefox.com'
];

FxaCoupon.getCoupon = (url) => {
    const _validParamChars = /^[\w/.%-]+$/;
    const coupon = url.searchParams.get('coupon');

    if (coupon && _validParamChars.test(coupon)) {
        return coupon;
    }

    return null;
};

FxaCoupon.verifyLink = (url) => {
    return (
        _allowedDomains.indexOf(url.hostname) !== -1 &&
        (url.pathname.startsWith('/subscriptions/products/') ||
            url.pathname.startsWith('/mozillavpnstage/'))
    );
};

FxaCoupon.init = (url) => {
    if (!window.URL) {
        return;
    }

    try {
        const pageUrl = new URL(url);
        const coupon = FxaCoupon.getCoupon(pageUrl);

        // If there is no coupon data, then do nothing.
        if (!coupon) {
            return false;
        }

        const subscriptionLinks = document.querySelectorAll(
            '.js-fxa-cta-link, .js-fxa-product-cta-link'
        );

        for (let i = 0; i < subscriptionLinks.length; i++) {
            const href = subscriptionLinks[i].hasAttribute('href')
                ? subscriptionLinks[i].href
                : null;

            if (href) {
                const url = new URL(href);
                if (FxaCoupon.verifyLink(url)) {
                    url.searchParams.append('coupon', coupon);
                    subscriptionLinks[i].href = url;
                }
            }
        }

        return true;
    } catch (e) {
        return false;
    }
};

export default FxaCoupon;
