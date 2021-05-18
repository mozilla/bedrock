# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_jinja.backend import Jinja2

from bedrock.mozorg.tests import TestCase


TEST_FXA_ENDPOINT = 'https://accounts.firefox.com/'
TEST_VPN_ENDPOINT = 'https://vpn.mozilla.org/'
TEST_VPN_PRODUCT_ID = 'prod_FvnsFHIfezy3ZI'
TEST_VPN_FIXED_PRICE_MONTHLY_USD = 'plan_FvnxS1j9oFUZ7Y'
TEST_VPN_VARIABLE_PRICING = {
    'de': {
        '12-month': {
            'id': 'price_1IgwblJNcmPzuWtRynC7dqQa',
            'price': '4,99 €',
            'total': '59,88 €'
        },
        '6-month': {
            'id': 'price_1IgwaHJNcmPzuWtRuUfSR4l7',
            'price': '6,99 €',
            'total': '41,94 €'
        },
        'monthly': {
            'id': 'price_1IgwZVJNcmPzuWtRg9Wssh2y',
            'price': '9,99‎ €',
            'total': None
        }
    },
    'fr': {
        '12-month': {
            'id': 'price_1IgnlcJNcmPzuWtRjrNa39W4',
            'price': '4,99 €',
            'total': '59,88 €'
        },
        '6-month': {
            'id': 'price_1IgoxGJNcmPzuWtRG7l48EoV',
            'price': '6,99 €',
            'total': '41,94 €'
        },
        'monthly': {
            'id': 'price_1IgowHJNcmPzuWtRzD7SgAYb',
            'price': '9,99‎ €',
            'total': None
        }
    },
    'us': {
        '12-month': {
            'id': 'price_1Iw85dJNcmPzuWtRyhMDdtM7',
            'price': 'TBD',
            'total': 'TBD'
        },
        '6-month': {
            'id': 'price_1Iw87cJNcmPzuWtRefuyqsOd',
            'price': 'TBD',
            'total': 'TBD'
        },
        'monthly': {
            'id': 'price_1Iw7qSJNcmPzuWtRMUZpOwLm',
            'price': 'TBD',
            'total': None
        }
    }
}

jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {})


@override_settings(
    FXA_ENDPOINT=TEST_FXA_ENDPOINT,
    VPN_ENDPOINT=TEST_VPN_ENDPOINT,
    VPN_PRODUCT_ID=TEST_VPN_PRODUCT_ID,
    VPN_FIXED_PRICE_MONTHLY_USD=TEST_VPN_FIXED_PRICE_MONTHLY_USD,
    VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING)
class TestVPNSubscribeLink(TestCase):
    rf = RequestFactory()

    def _render(self, entrypoint, link_text, plan=None, class_name=None, lang=None, optional_parameters=None, optional_attributes=None):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ vpn_subscribe_link('{0}', '{1}', '{2}', '{3}', '{4}', {5}, {6}) }}}}".format(
                      entrypoint, link_text, plan, class_name, lang, optional_parameters, optional_attributes),
                      {'request': req})

    def test_vpn_subscribe_link_fixed_monthly_usd(self):
        """Should return expected markup for default fixed monthly plan in US$"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan=None, class_name='mzp-c-button', lang='en-US',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan=plan_FvnxS1j9oFUZ7Y'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            u'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary">Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_12_month_en(self):
        """Should return expected markup for variable 12-month plan for en-US"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='12-month', class_name='mzp-c-button', lang='en-US',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            u'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            u'data-plan-de="price_1IgwblJNcmPzuWtRynC7dqQa" data-plan-fr="price_1IgnlcJNcmPzuWtRjrNa39W4" '
            u'data-plan-us="price_1Iw85dJNcmPzuWtRyhMDdtM7">Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_6_month_en(self):
        """Should return expected markup for variable 6-month plan for en-US"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='6-month', class_name='mzp-c-button', lang='en-US',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw87cJNcmPzuWtRefuyqsOd'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            u'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            u'data-plan-de="price_1IgwaHJNcmPzuWtRuUfSR4l7" data-plan-fr="price_1IgoxGJNcmPzuWtRG7l48EoV" '
            u'data-plan-us="price_1Iw87cJNcmPzuWtRefuyqsOd">Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_monthly_en(self):
        """Should return expected markup for variable monthly plan for en-US"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='monthly', class_name='mzp-c-button', lang='en-US',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw7qSJNcmPzuWtRMUZpOwLm'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            u'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            u'data-plan-de="price_1IgwZVJNcmPzuWtRg9Wssh2y" data-plan-fr="price_1IgowHJNcmPzuWtRzD7SgAYb" '
            u'data-plan-us="price_1Iw7qSJNcmPzuWtRMUZpOwLm">Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_12_month_de(self):
        """Should return expected markup for variable 12-month plan for de"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='12-month', class_name='mzp-c-button', lang='de',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan=price_1IgwblJNcmPzuWtRynC7dqQa'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            u'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            u'data-plan-de="price_1IgwblJNcmPzuWtRynC7dqQa" data-plan-fr="price_1IgnlcJNcmPzuWtRjrNa39W4" '
            u'data-plan-us="price_1Iw85dJNcmPzuWtRyhMDdtM7">Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_6_month_de(self):
        """Should return expected markup for variable 6-month plan for de"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='6-month', class_name='mzp-c-button', lang='de',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan=price_1IgwaHJNcmPzuWtRuUfSR4l7'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            u'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            u'data-plan-de="price_1IgwaHJNcmPzuWtRuUfSR4l7" data-plan-fr="price_1IgoxGJNcmPzuWtRG7l48EoV" '
            u'data-plan-us="price_1Iw87cJNcmPzuWtRefuyqsOd">Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_monthly_de(self):
        """Should return expected markup for variable monthly plan for de"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='monthly', class_name='mzp-c-button', lang='de',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan=price_1IgwZVJNcmPzuWtRg9Wssh2y'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            u'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            u'data-plan-de="price_1IgwZVJNcmPzuWtRg9Wssh2y" data-plan-fr="price_1IgowHJNcmPzuWtRzD7SgAYb" '
            u'data-plan-us="price_1Iw7qSJNcmPzuWtRMUZpOwLm">Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_12_month_fr(self):
        """Should return expected markup for variable 12-month plan for fr"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='12-month', class_name='mzp-c-button', lang='fr',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan=price_1IgnlcJNcmPzuWtRjrNa39W4'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            u'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            u'data-plan-de="price_1IgwblJNcmPzuWtRynC7dqQa" data-plan-fr="price_1IgnlcJNcmPzuWtRjrNa39W4" '
            u'data-plan-us="price_1Iw85dJNcmPzuWtRyhMDdtM7">Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_6_month_fr(self):
        """Should return expected markup for variable 6-month plan for fr"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='6-month', class_name='mzp-c-button', lang='fr',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan=price_1IgoxGJNcmPzuWtRG7l48EoV'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            u'data-plan-de="price_1IgwaHJNcmPzuWtRuUfSR4l7" data-plan-fr="price_1IgoxGJNcmPzuWtRG7l48EoV" '
            u'data-plan-us="price_1Iw87cJNcmPzuWtRefuyqsOd">Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_monthly_fr(self):
        """Should return expected markup for variable monthly plan for fr"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='monthly', class_name='mzp-c-button', lang='fr',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan=price_1IgowHJNcmPzuWtRzD7SgAYb'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            u'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            u'data-plan-de="price_1IgwZVJNcmPzuWtRg9Wssh2y" data-plan-fr="price_1IgowHJNcmPzuWtRzD7SgAYb" '
            u'data-plan-us="price_1Iw7qSJNcmPzuWtRMUZpOwLm">Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)


@override_settings(FXA_ENDPOINT=TEST_FXA_ENDPOINT, VPN_ENDPOINT=TEST_VPN_ENDPOINT)
class TestVPNSignInLink(TestCase):
    rf = RequestFactory()

    def _render(self, entrypoint, link_text, class_name=None, optional_parameters=None, optional_attributes=None):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ vpn_sign_in_link('{0}', '{1}', '{2}', {3}, {4}) }}}}".format(
                      entrypoint, link_text, class_name, optional_parameters, optional_attributes),
                      {'request': req})

    def test_vpn_sign_in_link(self):
        """Should return expected markup"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Sign In', class_name='mzp-c-cta-link',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'VPN Sign In', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'navigation'})
        expected = (
            u'<a href="https://vpn.mozilla.org/oauth/init?entrypoint=www.mozilla.org-vpn-product-page'
            u'&form_type=button&utm_source=www.mozilla.org-vpn-product-page&utm_medium=referral'
            u'&utm_campaign=vpn-product-page&data_cta_position=navigation" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-cta-link" data-cta-text="VPN Sign In" '
            u'data-cta-type="fxa-vpn" data-cta-position="navigation">Sign In</a>')
        self.assertEqual(markup, expected)


class TestVPNMonthlyPrice(TestCase):
    rf = RequestFactory()

    def _render(self, plan):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ vpn_monthly_price('{0}') }}}}".format(plan), {'request': req})

    def test_vpn_monthly_price(self):
        """Should return expected markup"""
        markup = self._render(plan='monthly')
        expected = (
            u'<span class="js-vpn-monthly-price-display" data-price-usd="US$9.99<span>/month</span>" '
            u'data-price-euro="9,99‎ €<span>/month</span>">US$9.99<span>/month</span></span>')
        self.assertEqual(markup, expected)

    def test_vpn_6_month_price(self):
        """Should return expected markup"""
        markup = self._render(plan='6-month')
        expected = (
            u'<span class="js-vpn-monthly-price-display" data-price-usd="US$7.99<span>/month</span>" '
            u'data-price-euro="6,99 €<span>/month</span>">US$7.99<span>/month</span></span>')
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price(self):
        """Should return expected markup"""
        markup = self._render(plan='12-month')
        expected = (
            u'<span class="js-vpn-monthly-price-display" data-price-usd="US$4.99<span>/month</span>" '
            u'data-price-euro="4,99 €<span>/month</span>">US$4.99<span>/month</span></span>')
        self.assertEqual(markup, expected)


class TestVPNTotalPrice(TestCase):
    rf = RequestFactory()

    def _render(self, plan):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ vpn_total_price('{0}') }}}}".format(plan), {'request': req})

    def test_vpn_6_month_total_price(self):
        """Should return expected markup"""
        markup = self._render(plan='6-month')
        expected = (
            u'<span class="js-vpn-total-price-display" data-price-usd="US$47.94 total" '
            u'data-price-euro="41,94 € total">US$47.94 total</span>')
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price(self):
        """Should return expected markup"""
        markup = self._render(plan='12-month')
        expected = (
            u'<span class="js-vpn-total-price-display" data-price-usd="US$59.88 total" '
            u'data-price-euro="59,88 € total">US$59.88 total</span>')
        self.assertEqual(markup, expected)


class TestVPNSaving(TestCase):
    rf = RequestFactory()

    def _render(self, plan):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ vpn_saving('{0}') }}}}".format(plan), {'request': req})

    def test_vpn_6_month_saving(self):
        """Should return expected markup"""
        markup = self._render(plan='6-month')
        expected = (
            u'<span class="js-vpn-saving-display" data-price-usd="Save 20%" '
            u'data-price-euro="Save 30%">Save 20%</span>')
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving(self):
        """Should return expected markup"""
        markup = self._render(plan='12-month')
        expected = (
            u'<span class="js-vpn-saving-display" data-price-usd="Save 50%" '
            u'data-price-euro="Save 50%">Save 50%</span>')
        self.assertEqual(markup, expected)
