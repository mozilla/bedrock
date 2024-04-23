/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import FxaCoupon from '../../../../media/js/base/fxa-coupon.es6';

describe('fxa-coupon.js', function () {
    beforeEach(function () {
        // link to change
        const links = `<div id="test-links">
                <a id="test-not-subscription" class="js-fxa-product-cta-link" href="https://accounts.firefox.com/?service=sync&amp;action=email&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-accounts_page&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page">Create a Mozilla account</a>
                <a id="test-not-accounts" class="js-fxa-cta-link" href="https://www.mozilla.org/?service=sync&amp;action=email&amp;context=fx_desktop_v3&amp;entrypoint=mozilla.org-accounts_page&amp;utm_content=accounts-page-top-cta&amp;utm_source=accounts-page&amp;utm_medium=referral&amp;utm_campaign=fxa-benefits-page">Create a Mozilla account</a>
                <a id="test-subscription-stage" class="js-fxa-product-cta-link" href="https://accounts.stage.mozaws.net/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7&amp;entrypoint=www.mozilla.org-vpn-product-page&amp;form_type=button&amp;service=e6eb0d1e856335fc&amp;utm_source=www.mozilla.org-vpn-product-page&amp;utm_medium=referral&amp;utm_campaign=vpn-product-page&amp;data_cta_position=pricing">Get Mozilla VPN</a>
                <a id="test-subscription-prod" class="js-fxa-cta-link" href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7&amp;entrypoint=www.mozilla.org-vpn-product-page&amp;form_type=button&amp;service=e6eb0d1e856335fc&amp;utm_source=www.mozilla.org-vpn-product-page&amp;utm_medium=referral&amp;utm_campaign=vpn-product-page&amp;data_cta_position=pricing">Get Mozilla VPN</a>
            </div>`;

        document.body.insertAdjacentHTML('beforeend', links);
    });

    afterEach(function () {
        const content = document.getElementById('test-links');
        content.parentNode.removeChild(content);
    });

    it('should append coupon parameter to Fxa subscription links when present', function () {
        const url = 'https://www.mozilla.org/en-US/products/vpn/?coupon=TEST';

        FxaCoupon.init(url);

        expect(
            document.getElementById('test-not-subscription').href
        ).not.toContain('coupon=TEST');
        expect(document.getElementById('test-not-accounts').href).not.toContain(
            'coupon=TEST'
        );
        expect(
            document.getElementById('test-subscription-stage').href
        ).toContain('coupon=TEST');
        expect(
            document.getElementById('test-subscription-prod').href
        ).toContain('coupon=TEST');
    });
});
