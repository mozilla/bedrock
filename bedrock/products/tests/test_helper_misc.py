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

jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {})


@override_settings(FXA_ENDPOINT=TEST_FXA_ENDPOINT)
@override_settings(VPN_ENDPOINT=TEST_VPN_ENDPOINT)
class TestVPNSubscribeLink(TestCase):
    rf = RequestFactory()

    def _render(self, entrypoint, link_text, plan=None, class_name=None, optional_parameters=None, optional_attributes=None):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ vpn_subscribe_link('{0}', '{1}', '{2}', '{3}', {4}, {5}) }}}}".format(
                      entrypoint, link_text, plan, class_name, optional_parameters, optional_attributes),
                      {'request': req})

    @patch.dict(os.environ, SWITCH_VPN_LAUNCH_GERMANY_FRANCE='False')
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

    @patch.dict(os.environ, SWITCH_VPN_LAUNCH_GERMANY_FRANCE='True')
    def test_vpn_subscribe_link_fixed_monthly_usd(self):
        """Should return expected markup for default fixed monthly plan in US$"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan=None, class_name='mzp-c-button',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FiJ42WCzZNRSbS?plan=plan_FvPMH5lVx1vhV0'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary">'
            u'Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    @patch.dict(os.environ, SWITCH_VPN_LAUNCH_GERMANY_FRANCE='True')
    def test_vpn_subscribe_link_variable_12_month_euro(self):
        """Should return expected markup for variable 12-month plan in euros"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='12-month-euro', class_name='mzp-c-button',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FiJ42WCzZNRSbS?plan=price_1IXw5oKb9q6OnNsLPMkWOid7'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary">'
            u'Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    @patch.dict(os.environ, SWITCH_VPN_LAUNCH_GERMANY_FRANCE='True')
    def test_vpn_subscribe_link_variable_6_month_euro(self):
        """Should return expected markup for variable 6-month plan in euros"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='6-month-euro', class_name='mzp-c-button',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FiJ42WCzZNRSbS?plan=price_1IXw5NKb9q6OnNsLLIyYuhWF'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary">'
            u'Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)

    @patch.dict(os.environ, SWITCH_VPN_LAUNCH_GERMANY_FRANCE='True')
    def test_vpn_subscribe_link_variable_monthly_euro(self):
        """Should return expected markup for variable monthly plan in euros"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN',
                              plan='monthly-euro', class_name='mzp-c-button',
                              optional_parameters={'utm_campaign': 'vpn-product-page'},
                              optional_attributes={'data-cta-text': 'Get Mozilla VPN monthly', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/products/prod_FiJ42WCzZNRSbS?plan=price_1IXw4eKb9q6OnNsLqnVP4PvO'
            u'&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page'
            u'&utm_medium=referral&utm_campaign=vpn-product-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-button" '
            u'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary">'
            u'Get Mozilla VPN</a>')
        self.assertEqual(markup, expected)


@override_settings(FXA_ENDPOINT=TEST_FXA_ENDPOINT)
@override_settings(VPN_ENDPOINT=TEST_VPN_ENDPOINT)
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
