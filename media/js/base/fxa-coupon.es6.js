/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const FxaCoupon = {};

const _allowedDomains = ['accounts.firefox.com', 'accounts.stage.mozaws.net'];

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
        url.pathname.startsWith('/subscriptions/products/')
    );
};

FxaCoupon.init = () => {
    if (!window.URL) {
        return;
    }

    try {
        const pageUrl = new URL(window.location.href);
        const coupon = FxaCoupon.getCoupon(pageUrl);

        // If there is no coupon data, then do nothing.
        if (!coupon) {
            return;
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
    } catch (e) {
        //fail silently
    }
};

export default FxaCoupon;
