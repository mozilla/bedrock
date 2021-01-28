# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_jinja.backend import Jinja2

from bedrock.mozorg.tests import TestCase


TEST_FXA_ENDPOINT = 'https://accounts.firefox.com/'

jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {})


@override_settings(FXA_ENDPOINT=TEST_FXA_ENDPOINT)
class TestVPNSubscribeLink(TestCase):
    rf = RequestFactory()

    def _render(self, entrypoint, link_text, class_name=None, optional_parameters=None, optional_attributes=None):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ vpn_subscribe_link('{0}', '{1}', '{2}', {3}, {4}) }}}}".format(
                      entrypoint, link_text, class_name, optional_parameters, optional_attributes),
                      {'request': req})

    def test_vpn_subscribe_link(self):
        """Should return expected markup"""
        markup = self._render(entrypoint='www.mozilla.org-vpn-product-page', link_text='Try Mozilla VPN',
                              class_name='vpn-button try js-try-vpn',
                              optional_parameters={'utm_campaign': 'vpn-landing-page'},
                              optional_attributes={'data-cta-text': 'Try Mozilla VPN', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'primary'})
        expected = (
            u'<a href="https://vpn.mozilla.org/r/vpn/subscribe/?entrypoint=www.mozilla.org-vpn-product-page'
            u'&form_type=button&utm_source=www.mozilla.org-vpn-product-page&utm_medium=referral'
            u'&utm_campaign=vpn-landing-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button vpn-button try js-try-vpn" '
            u'data-cta-text="Try Mozilla VPN" data-cta-type="fxa-vpn" data-cta-position="primary">'
            u'Try Mozilla VPN</a>')
        self.assertEqual(markup, expected)


@override_settings(FXA_ENDPOINT=TEST_FXA_ENDPOINT)
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
                              optional_parameters={'utm_campaign': 'vpn-landing-page'},
                              optional_attributes={'data-cta-text': 'Sign In', 'data-cta-type':
                                                   'fxa-vpn', 'data-cta-position': 'navigation'})
        expected = (
            u'<a href="https://vpn.mozilla.org/oauth/init/?entrypoint=www.mozilla.org-vpn-product-page'
            u'&form_type=button&utm_source=www.mozilla.org-vpn-product-page&utm_medium=referral'
            u'&utm_campaign=vpn-landing-page" data-action="https://accounts.firefox.com/" '
            u'class="js-fxa-cta-link js-fxa-product-button mzp-c-cta-link" data-cta-text="Sign In" '
            u'data-cta-type="fxa-vpn" data-cta-position="navigation">Sign In</a>')
        self.assertEqual(markup, expected)
