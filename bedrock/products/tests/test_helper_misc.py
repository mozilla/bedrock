# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_jinja.backend import Jinja2
from mock import patch

from bedrock.mozorg.tests import TestCase


TEST_FXA_ENDPOINT = 'https://accounts.firefox.com/'
TEST_VPN_ENDPOINT = 'https://vpn.mozilla.org/'
TEST_VPN_PRODUCT_ID = 'prod_FvnsFHIfezy3ZI'
TEST_VPN_FIXED_PRICE_MONTHLY_USD = 'plan_FvnxS1j9oFUZ7Y'
TEST_VPN_VARIABLE_PRICE_12_MONTH_EURO = ''
TEST_VPN_VARIABLE_PRICE_6_MONTH_EURO = ''
TEST_VPN_VARIABLE_PRICE_MONTHLY_EURO = ''

jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {})


@override_settings(
    FXA_ENDPOINT=TEST_FXA_ENDPOINT,
    VPN_ENDPOINT=TEST_VPN_ENDPOINT,
    VPN_PRODUCT_ID=TEST_VPN_PRODUCT_ID,
    VPN_FIXED_PRICE_MONTHLY_USD=TEST_VPN_FIXED_PRICE_MONTHLY_USD,
    VPN_VARIABLE_PRICE_12_MONTH_EURO=TEST_VPN_VARIABLE_PRICE_12_MONTH_EURO,
    VPN_VARIABLE_PRICE_6_MONTH_EURO=TEST_VPN_VARIABLE_PRICE_6_MONTH_EURO,
    VPN_VARIABLE_PRICE_MONTHLY_EURO=TEST_VPN_VARIABLE_PRICE_MONTHLY_EURO)
class TestVPNSubscribeLink(TestCase):
    rf = RequestFactory()

    def _render(self, entrypoint, link_text, plan=None, class_name=None, optional_parameters=None, optional_attributes=None):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ vpn_subscribe_link('{0}', '{1}', '{2}', '{3}', {4}, {5}) }}}}".format(
                      entrypoint, link_text, plan, class_name, optional_parameters, optional_attributes),
                      {'request': req})

    @patch.dict(os.environ, SWITCH_VPN_NEW_SUBSCRIPTION_URL_FORMAT='False')
    def test_vpn_subscribe_link_fixed_monthly_usd_old_format(self):
        """Should return expected markup for default fixed monthly plan in US$ using old format"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan=None, class_name='mzp-c-button',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe?entrypoint=www.mozilla.org-vpn-product-page'
            u'&form_type=button&utm_source=www.mozilla.org-vpn-product-page&utm_medium=referral'
            u'&utm_campaign=vpn-product-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary">'
            u'Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    @patch.dict(os.environ, SWITCH_VPN_NEW_SUBSCRIPTION_URL_FORMAT='True')
    def test_vpn_subscribe_link_fixed_monthly_usd(self):
        """Should return expected markup for default fixed monthly plan in US$"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan=None, class_name='mzp-c-button',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan=plan_FvnxS1j9oFUZ7Y'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary">'
            u'Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    @patch.dict(os.environ, SWITCH_VPN_NEW_SUBSCRIPTION_URL_FORMAT='True')
    def test_vpn_subscribe_link_variable_12_month_euro(self):
        """Should return expected markup for variable 12-month plan in euros"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='12-month-euro', class_name='mzp-c-button',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan='
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary">'
            u'Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    @patch.dict(os.environ, SWITCH_VPN_NEW_SUBSCRIPTION_URL_FORMAT='True')
    def test_vpn_subscribe_link_variable_6_month_euro(self):
        """Should return expected markup for variable 6-month plan in euros"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='6-month-euro', class_name='mzp-c-button',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan='
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary">'
            u'Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    @patch.dict(os.environ, SWITCH_VPN_NEW_SUBSCRIPTION_URL_FORMAT='True')
    def test_vpn_subscribe_link_variable_monthly_euro(self):
        """Should return expected markup for variable monthly plan in euros"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='monthly-euro', class_name='mzp-c-button',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FvnsFHIfezy3ZI?plan='
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary">'
            u'Get Mozilla VPN</a>')
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
            u'&utm_campaign=vpn-product-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-cta-link" data-cta-text="VPN Sign In" '
            u'data-cta-type="fxa-vpn" data-cta-position="navigation">Sign In</a>')
        self.assertEqual(markup, expected)
