# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_jinja.backend import Jinja2

from bedrock.mozorg.tests import TestCase

TEST_FXA_ENDPOINT = "https://accounts.firefox.com/"
TEST_VPN_ENDPOINT = "https://vpn.mozilla.org/"
TEST_VPN_PRODUCT_ID = "prod_FvnsFHIfezy3ZI"
TEST_VPN_SUBSCRIPTION_URL = "https://accounts.firefox.com/"

TEST_VPN_PLAN_ID_MATRIX = {
    "chf": {
        "de": {
            "12-month": {"id": "price_1J5JssJNcmPzuWtR616BH4aU", "price": "CHF 5.99", "total": "CHF 71.88", "saving": 45},
            "6-month": {"id": "price_1J5JtWJNcmPzuWtRMd2siphH", "price": "CHF 7.99", "total": "CHF 47.94", "saving": 27},
            "monthly": {"id": "price_1J5Ju3JNcmPzuWtR3GpNYSWj", "price": "CHF 10.99", "total": None, "saving": None},
        },
        "fr": {
            "12-month": {"id": "price_1J5JunJNcmPzuWtRo9dLxn6M", "price": "CHF 5.99", "total": "CHF 71.88", "saving": 45},
            "6-month": {"id": "price_1J5JvLJNcmPzuWtRayB4d7Ij", "price": "CHF 7.99", "total": "CHF 47.94", "saving": 27},
            "monthly": {"id": "price_1J5JvjJNcmPzuWtR3wwy1dcR", "price": "CHF 10.99", "total": None, "saving": None},
        },
        "it": {
            "12-month": {"id": "price_1J5JwWJNcmPzuWtRgrx5fjOc", "price": "CHF 5.99", "total": "CHF 71.88", "saving": 45},
            "6-month": {"id": "price_1J5JwvJNcmPzuWtRH2HuhWM5", "price": "CHF 7.99", "total": "CHF 47.94", "saving": 27},
            "monthly": {"id": "price_1J5JxGJNcmPzuWtRrp5e1SUB", "price": "CHF 10.99", "total": None, "saving": None},
        },
    },
    "euro": {
        "de": {
            "12-month": {"id": "price_1IgwblJNcmPzuWtRynC7dqQa", "price": "4,99 €", "total": "59,88 €", "saving": 50},
            "6-month": {"id": "price_1IgwaHJNcmPzuWtRuUfSR4l7", "price": "6,99 €", "total": "41,94 €", "saving": 30},
            "monthly": {"id": "price_1IgwZVJNcmPzuWtRg9Wssh2y", "price": "9,99‎ €", "total": None, "saving": None},
        },
        "en": {
            "12-month": {
                "id": "price_1JcdvBJNcmPzuWtROLbEH9d2",
                "price": "4,99 €",
                "total": "59,88 €",
                "saving": 50,
            },
            "6-month": {
                "id": "price_1Jcdu8JNcmPzuWtRK6u5TUoZ",
                "price": "6,99 €",
                "total": "41,94 €",
                "saving": 30,
            },
            "monthly": {
                "id": "price_1JcdsSJNcmPzuWtRGF9Y5TMJ",
                "price": "9,99‎ €",
                "total": None,
                "saving": None,
            },
        },
        "es": {
            "12-month": {"id": "price_1J5JCdJNcmPzuWtRrvQMFLlP", "price": "4,99 €", "total": "59,88 €", "saving": 50},
            "6-month": {"id": "price_1J5JDFJNcmPzuWtRrC4IeXTs", "price": "6,99 €", "total": "41,94 €", "saving": 30},
            "monthly": {"id": "price_1J5JDgJNcmPzuWtRqQtIbktk", "price": "9,99‎ €", "total": None, "saving": None},
        },
        "fr": {
            "12-month": {"id": "price_1IgnlcJNcmPzuWtRjrNa39W4", "price": "4,99 €", "total": "59,88 €", "saving": 50},
            "6-month": {"id": "price_1IgoxGJNcmPzuWtRG7l48EoV", "price": "6,99 €", "total": "41,94 €", "saving": 30},
            "monthly": {"id": "price_1IgowHJNcmPzuWtRzD7SgAYb", "price": "9,99‎ €", "total": None, "saving": None},
        },
        "it": {
            "12-month": {"id": "price_1J4owvJNcmPzuWtRomVhWQFq", "price": "4,99 €", "total": "59,88 €", "saving": 50},
            "6-month": {"id": "price_1J5J7eJNcmPzuWtRKdQi4Tkk", "price": "6,99 €", "total": "41,94 €", "saving": 30},
            "monthly": {"id": "price_1J5J6iJNcmPzuWtRK5zfoguV", "price": "9,99‎ €", "total": None, "saving": None},
        },
        "nl": {
            "12-month": {"id": "price_1J5JRGJNcmPzuWtRXwXA84cm", "price": "4,99 €", "total": "59,88 €", "saving": 50},
            "6-month": {"id": "price_1J5JRmJNcmPzuWtRyFGj0tkN", "price": "6,99 €", "total": "41,94 €", "saving": 30},
            "monthly": {"id": "price_1J5JSkJNcmPzuWtR54LPH2zi", "price": "9,99‎ €", "total": None, "saving": None},
        },
    },
    "usd": {
        "en": {
            "12-month": {"id": "price_1Iw85dJNcmPzuWtRyhMDdtM7", "price": "US$4.99", "total": "US$59.88", "saving": 50},
            "6-month": {"id": "price_1Iw87cJNcmPzuWtRefuyqsOd", "price": "US$7.99", "total": "US$47.94", "saving": 20},
            "monthly": {"id": "price_1Iw7qSJNcmPzuWtRMUZpOwLm", "price": "US$9.99", "total": None, "saving": None},
        }
    },
}

TEST_VPN_VARIABLE_PRICING = {
    "AT": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["de"],
    },
    "BE": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["nl"],
        "de": TEST_VPN_PLAN_ID_MATRIX["euro"]["de"],
        "fr": TEST_VPN_PLAN_ID_MATRIX["euro"]["fr"],
    },
    "CH": {
        "default": TEST_VPN_PLAN_ID_MATRIX["chf"]["de"],
        "fr": TEST_VPN_PLAN_ID_MATRIX["chf"]["fr"],
        "it": TEST_VPN_PLAN_ID_MATRIX["chf"]["it"],
    },
    "DE": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["de"],
    },
    "ES": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["es"],
    },
    "FR": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["fr"],
    },
    "IE": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "IT": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["it"],
    },
    "NL": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["nl"],
    },
    "US": {
        "default": TEST_VPN_PLAN_ID_MATRIX["usd"]["en"],
    },
}

jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {})


@override_settings(
    FXA_ENDPOINT=TEST_FXA_ENDPOINT,
    VPN_PRODUCT_ID=TEST_VPN_PRODUCT_ID,
    VPN_SUBSCRIPTION_URL=TEST_VPN_SUBSCRIPTION_URL,
    VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING,
)
class TestVPNSubscribeLink(TestCase):
    rf = RequestFactory()

    def _render(
        self,
        entrypoint="www.mozilla.org-vpn-product-page",
        link_text="Get Mozilla VPN",
        plan="12-month",
        class_name="mzp-c-button",
        country_code=None,
        lang=None,
        optional_parameters=None,
        optional_attributes=None,
    ):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(
            "{{{{ vpn_subscribe_link('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}) }}}}".format(
                entrypoint, link_text, plan, class_name, country_code, lang, optional_parameters, optional_attributes
            ),
            {"request": req},
        )

    def test_vpn_subscribe_link_variable_12_month(self):
        """Should return expected markup for variable 12-month plan link"""
        markup = self._render(
            plan="12-month",
            country_code="US",
            lang="en-US",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
            'class="js-vpn-cta-link js-fxa-product-button mzp-c-button" data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" '
            'data-cta-position="primary">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_6_month(self):
        """Should return expected markup for variable 6-month plan link"""
        markup = self._render(
            plan="6-month",
            country_code="US",
            lang="en-US",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw87cJNcmPzuWtRefuyqsOd'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
            'class="js-vpn-cta-link js-fxa-product-button mzp-c-button" data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" '
            'data-cta-position="primary">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_monthly(self):
        """Should return expected markup for variable monthly plan link"""
        markup = self._render(
            plan="monthly",
            country_code="US",
            lang="en-US",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw7qSJNcmPzuWtRMUZpOwLm'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
            'class="js-vpn-cta-link js-fxa-product-button mzp-c-button" data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" '
            'data-cta-position="primary">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_12_month_us_en(self):
        """Should contain expected 12-month plan ID (US / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="US",
            lang="en-US",
        )
        self.assertIn("?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7", markup)

    def test_vpn_subscribe_link_variable_6_month_us_en(self):
        """Should contain expected 6-month plan ID (US / en-US)"""
        markup = self._render(
            plan="6-month",
            country_code="US",
            lang="en-US",
        )
        self.assertIn("?plan=price_1Iw87cJNcmPzuWtRefuyqsOd", markup)

    def test_vpn_subscribe_link_variable_monthly_us_en(self):
        """Should contain expected monthly plan ID (US / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="US",
            lang="en-US",
        )
        self.assertIn("?plan=price_1Iw7qSJNcmPzuWtRMUZpOwLm", markup)

    def test_vpn_subscribe_link_variable_12_month_ca_en(self):
        """Should contain expected 12-month plan ID (CA / en-CA)"""
        markup = self._render(
            plan="12-month",
            country_code="CA",
            lang="en-CA",
        )
        self.assertIn("?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7", markup)

    def test_vpn_subscribe_link_variable_6_month_ca_en(self):
        """Should contain expected 6-month plan ID (CA / en-CA)"""
        markup = self._render(
            plan="6-month",
            country_code="CA",
            lang="en-CA",
        )
        self.assertIn("?plan=price_1Iw87cJNcmPzuWtRefuyqsOd", markup)

    def test_vpn_subscribe_link_variable_monthly_ca_en(self):
        """Should contain expected monthly plan ID in (CA / en-CA)"""
        markup = self._render(
            plan="monthly",
            country_code="CA",
            lang="en-CA",
        )
        self.assertIn("?plan=price_1Iw7qSJNcmPzuWtRMUZpOwLm", markup)

    def test_vpn_subscribe_link_variable_12_month_gb_en(self):
        """Should contain expected 12-month plan ID (GB / en-GB)"""
        markup = self._render(
            plan="12-month",
            country_code="GB",
            lang="en-GB",
        )
        self.assertIn("?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7", markup)

    def test_vpn_subscribe_link_variable_6_month_gb_en(self):
        """Should contain expected 6-month plan ID (GB / en-GB)"""
        markup = self._render(
            plan="6-month",
            country_code="GB",
            lang="en-GB",
        )
        self.assertIn("?plan=price_1Iw87cJNcmPzuWtRefuyqsOd", markup)

    def test_vpn_subscribe_link_variable_monthly_gb_en(self):
        """Should contain expected monthly plan ID (GB / en-GB)"""
        markup = self._render(
            plan="monthly",
            country_code="GB",
            lang="en-GB",
        )
        self.assertIn("?plan=price_1Iw7qSJNcmPzuWtRMUZpOwLm", markup)

    def test_vpn_subscribe_link_variable_12_month_at_de(self):
        """Should contain expected 12-month plan ID (AT / de)"""
        markup = self._render(
            plan="12-month",
            country_code="AT",
            lang="de",
        )
        self.assertIn("?plan=price_1IgwblJNcmPzuWtRynC7dqQa", markup)

    def test_vpn_subscribe_link_variable_6_month_at_de(self):
        """Should contain expected 6-month plan ID (AT / de)"""
        markup = self._render(
            plan="6-month",
            country_code="AT",
            lang="de",
        )
        self.assertIn("?plan=price_1IgwaHJNcmPzuWtRuUfSR4l7", markup)

    def test_vpn_subscribe_link_variable_monthly_at_de(self):
        """Should contain expected monthly plan ID (AT / de)"""
        markup = self._render(
            plan="monthly",
            country_code="AT",
            lang="de",
        )
        self.assertIn("?plan=price_1IgwZVJNcmPzuWtRg9Wssh2y", markup)

    def test_vpn_subscribe_link_variable_12_month_be_nl(self):
        """Should contain expected 12-month plan ID (BE / nl)"""
        markup = self._render(
            plan="12-month",
            country_code="BE",
            lang="nl",
        )
        self.assertIn("?plan=price_1J5JRGJNcmPzuWtRXwXA84cm", markup)

    def test_vpn_subscribe_link_variable_6_month_be_nl(self):
        """Should contain expected 6-month plan ID (BE / nl)"""
        markup = self._render(
            plan="6-month",
            country_code="BE",
            lang="nl",
        )
        self.assertIn("?plan=price_1J5JRmJNcmPzuWtRyFGj0tkN", markup)

    def test_vpn_subscribe_link_variable_monthly_be_nl(self):
        """Should contain expected monthly plan ID (BE / nl)"""
        markup = self._render(
            plan="monthly",
            country_code="BE",
            lang="nl",
        )
        self.assertIn("?plan=price_1J5JSkJNcmPzuWtR54LPH2zi", markup)

    def test_vpn_subscribe_link_variable_12_month_be_de(self):
        """Should contain expected 12-month plan ID (BE / de)"""
        markup = self._render(
            plan="12-month",
            country_code="BE",
            lang="de",
        )
        self.assertIn("?plan=price_1IgwblJNcmPzuWtRynC7dqQa", markup)

    def test_vpn_subscribe_link_variable_6_month_be_de(self):
        """Should contain expected 6-month plan ID (BE / de)"""
        markup = self._render(
            plan="6-month",
            country_code="BE",
            lang="de",
        )
        self.assertIn("?plan=price_1IgwaHJNcmPzuWtRuUfSR4l7", markup)

    def test_vpn_subscribe_link_variable_monthly_be_de(self):
        """Should contain expected monthly plan ID (BE / de)"""
        markup = self._render(
            plan="monthly",
            country_code="BE",
            lang="de",
        )
        self.assertIn("?plan=price_1IgwZVJNcmPzuWtRg9Wssh2y", markup)

    def test_vpn_subscribe_link_variable_12_month_be_fr(self):
        """Should contain expected 12-month plan ID (BE / fr)"""
        markup = self._render(
            plan="12-month",
            country_code="BE",
            lang="fr",
        )
        self.assertIn("?plan=price_1IgnlcJNcmPzuWtRjrNa39W4", markup)

    def test_vpn_subscribe_link_variable_6_month_be_fr(self):
        """Should contain expected 6-month plan ID (BE / fr)"""
        markup = self._render(
            plan="6-month",
            country_code="BE",
            lang="fr",
        )
        self.assertIn("?plan=price_1IgoxGJNcmPzuWtRG7l48EoV", markup)

    def test_vpn_subscribe_link_variable_monthly_be_fr(self):
        """Should contain expected monthly plan ID (BE / fr)"""
        markup = self._render(
            plan="monthly",
            country_code="BE",
            lang="fr",
        )
        self.assertIn("?plan=price_1IgowHJNcmPzuWtRzD7SgAYb", markup)

    def test_vpn_default_language_selection_be_en(self):
        """Should should select default language if no match is found (BE / en)"""
        markup = self._render(
            plan="monthly",
            country_code="BE",
            lang="en-US",
        )
        self.assertIn("?plan=price_1J5JSkJNcmPzuWtR54LPH2zi", markup)

    def test_vpn_subscribe_link_variable_12_month_ch_de(self):
        """Should contain expected 12-month plan ID (CH / de)"""
        markup = self._render(
            plan="12-month",
            country_code="CH",
            lang="de",
        )
        self.assertIn("?plan=price_1J5JssJNcmPzuWtR616BH4aU", markup)

    def test_vpn_subscribe_link_variable_6_month_ch_de(self):
        """Should contain expected 6-month plan ID (CH / de)"""
        markup = self._render(
            plan="6-month",
            country_code="CH",
            lang="de",
        )
        self.assertIn("?plan=price_1J5JtWJNcmPzuWtRMd2siphH", markup)

    def test_vpn_subscribe_link_variable_monthly_ch_de(self):
        """Should contain expected monthly plan ID (CH / de)"""
        markup = self._render(
            plan="monthly",
            country_code="CH",
            lang="de",
        )
        self.assertIn("?plan=price_1J5Ju3JNcmPzuWtR3GpNYSWj", markup)

    def test_vpn_subscribe_link_variable_12_month_ch_fr(self):
        """Should contain expected 12-month plan ID (CH / fr)"""
        markup = self._render(
            plan="12-month",
            country_code="CH",
            lang="fr",
        )
        self.assertIn("?plan=price_1J5JunJNcmPzuWtRo9dLxn6M", markup)

    def test_vpn_subscribe_link_variable_6_month_ch_fr(self):
        """Should contain expected 6-month plan ID (CH / fr)"""
        markup = self._render(
            plan="6-month",
            country_code="CH",
            lang="fr",
        )
        self.assertIn("?plan=price_1J5JvLJNcmPzuWtRayB4d7Ij", markup)

    def test_vpn_subscribe_link_variable_monthly_ch_fr(self):
        """Should contain expected monthly plan ID (CH / fr)"""
        markup = self._render(
            plan="monthly",
            country_code="CH",
            lang="fr",
        )
        self.assertIn("?plan=price_1J5JvjJNcmPzuWtR3wwy1dcR", markup)

    def test_vpn_subscribe_link_variable_12_month_ch_it(self):
        """Should contain expected 12-month plan ID (CH / it)"""
        markup = self._render(
            plan="12-month",
            country_code="CH",
            lang="it",
        )
        self.assertIn("?plan=price_1J5JwWJNcmPzuWtRgrx5fjOc", markup)

    def test_vpn_subscribe_link_variable_6_month_ch_it(self):
        """Should contain expected 6-month plan ID (CH / it)"""
        markup = self._render(
            plan="6-month",
            country_code="CH",
            lang="it",
        )
        self.assertIn("?plan=price_1J5JwvJNcmPzuWtRH2HuhWM5", markup)

    def test_vpn_subscribe_link_variable_monthly_ch_it(self):
        """Should contain expected monthly plan ID (CH / it)"""
        markup = self._render(
            plan="monthly",
            country_code="CH",
            lang="it",
        )
        self.assertIn("?plan=price_1J5JxGJNcmPzuWtRrp5e1SUB", markup)

    def test_vpn_default_language_selection_ch_en(self):
        """Should should select default language if no match is found (CH / en)"""
        markup = self._render(
            plan="monthly",
            country_code="CH",
            lang="en-US",
        )
        self.assertIn("?plan=price_1J5Ju3JNcmPzuWtR3GpNYSWj", markup)

    def test_vpn_subscribe_link_variable_12_month_de_de(self):
        """Should contain expected 12-month plan ID (DE / de)"""
        markup = self._render(
            plan="12-month",
            country_code="DE",
            lang="de",
        )
        self.assertIn("?plan=price_1IgwblJNcmPzuWtRynC7dqQa", markup)

    def test_vpn_subscribe_link_variable_6_month_de_de(self):
        """Should contain expected 6-month plan ID (DE / de)"""
        markup = self._render(
            plan="6-month",
            country_code="DE",
            lang="de",
        )
        self.assertIn("?plan=price_1IgwaHJNcmPzuWtRuUfSR4l7", markup)

    def test_vpn_subscribe_link_variable_monthly_de_de(self):
        """Should contain expected monthly plan ID (DE / de)"""
        markup = self._render(
            plan="monthly",
            country_code="DE",
            lang="de",
        )
        self.assertIn("?plan=price_1IgwZVJNcmPzuWtRg9Wssh2y", markup)

    def test_vpn_subscribe_link_variable_12_month_fr_fr(self):
        """Should contain expected 12-month plan ID (FR / fr)"""
        markup = self._render(
            plan="12-month",
            country_code="FR",
            lang="fr",
        )
        self.assertIn("?plan=price_1IgnlcJNcmPzuWtRjrNa39W4", markup)

    def test_vpn_subscribe_link_variable_6_month_fr_fr(self):
        """Should contain expected 6-month plan ID (FR / fr)"""
        markup = self._render(
            plan="6-month",
            country_code="FR",
            lang="fr",
        )
        self.assertIn("?plan=price_1IgoxGJNcmPzuWtRG7l48EoV", markup)

    def test_vpn_subscribe_link_variable_monthly_fr_fr(self):
        """Should contain expected monthly plan ID (FR / fr)"""
        markup = self._render(
            plan="monthly",
            country_code="FR",
            lang="fr",
        )
        self.assertIn("?plan=price_1IgowHJNcmPzuWtRzD7SgAYb", markup)

    def test_vpn_subscribe_link_variable_12_month_es_es(self):
        """Should contain expected 12-month plan ID (ES / es-ES)"""
        markup = self._render(
            plan="12-month",
            country_code="ES",
            lang="es-ES",
        )
        self.assertIn("?plan=price_1J5JCdJNcmPzuWtRrvQMFLlP", markup)

    def test_vpn_subscribe_link_variable_6_month_es_es(self):
        """Should contain expected 6-month plan ID (ES / es-ES)"""
        markup = self._render(
            plan="6-month",
            country_code="ES",
            lang="es-ES",
        )
        self.assertIn("?plan=price_1J5JDFJNcmPzuWtRrC4IeXTs", markup)

    def test_vpn_subscribe_link_variable_monthly_es_es(self):
        """Should contain expected monthly plan ID (ES / es-ES)"""
        markup = self._render(
            plan="monthly",
            country_code="ES",
            lang="es-ES",
        )
        self.assertIn("?plan=price_1J5JDgJNcmPzuWtRqQtIbktk", markup)

    def test_vpn_subscribe_link_variable_12_month_it_it(self):
        """Should contain expected 12-month plan ID (IT / it)"""
        markup = self._render(
            plan="12-month",
            country_code="IT",
            lang="it",
        )
        self.assertIn("?plan=price_1J4owvJNcmPzuWtRomVhWQFq", markup)

    def test_vpn_subscribe_link_variable_6_month_it_it(self):
        """Should contain expected 6-month plan ID (IT / it)"""
        markup = self._render(
            plan="6-month",
            country_code="IT",
            lang="it",
        )
        self.assertIn("?plan=price_1J5J7eJNcmPzuWtRKdQi4Tkk", markup)

    def test_vpn_subscribe_link_variable_monthly_it_it(self):
        """Should contain expected monthly plan ID (IT / it)"""
        markup = self._render(
            plan="monthly",
            country_code="IT",
            lang="it",
        )
        self.assertIn("?plan=price_1J5J6iJNcmPzuWtRK5zfoguV", markup)

    def test_vpn_subscribe_link_variable_12_month_ie_en(self):
        """Should contain expected 12-month plan ID (IE / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="IE",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdvBJNcmPzuWtROLbEH9d2", markup)

    def test_vpn_subscribe_link_variable_6_month_ie_en(self):
        """Should contain expected 6-month plan ID (IE / en-US)"""
        markup = self._render(
            plan="6-month",
            country_code="IE",
            lang="en-US",
        )
        self.assertIn("?plan=price_1Jcdu8JNcmPzuWtRK6u5TUoZ", markup)

    def test_vpn_subscribe_link_variable_monthly_ie_en(self):
        """Should contain expected monthly plan ID (IE / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="IE",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdsSJNcmPzuWtRGF9Y5TMJ", markup)

    def test_vpn_subscribe_link_variable_12_month_nl_nl(self):
        """Should contain expected 12-month plan ID (NL / nl)"""
        markup = self._render(
            plan="12-month",
            country_code="NL",
            lang="nl",
        )
        self.assertIn("?plan=price_1J5JRGJNcmPzuWtRXwXA84cm", markup)

    def test_vpn_subscribe_link_variable_6_month_nl_nl(self):
        """Should contain expected 16-month plan ID (NL / nl)"""
        markup = self._render(
            plan="6-month",
            country_code="NL",
            lang="nl",
        )
        self.assertIn("?plan=price_1J5JRmJNcmPzuWtRyFGj0tkN", markup)

    def test_vpn_subscribe_link_variable_monthly_nl_nl(self):
        """Should contain expected monthly plan ID (NL / nl)"""
        markup = self._render(
            plan="monthly",
            country_code="NL",
            lang="nl",
        )
        self.assertIn("?plan=price_1J5JSkJNcmPzuWtR54LPH2zi", markup)


@override_settings(FXA_ENDPOINT=TEST_FXA_ENDPOINT, VPN_ENDPOINT=TEST_VPN_ENDPOINT)
class TestVPNSignInLink(TestCase):
    rf = RequestFactory()

    def _render(self, entrypoint, link_text, class_name=None, optional_parameters=None, optional_attributes=None):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(
            "{{{{ vpn_sign_in_link('{0}', '{1}', '{2}', {3}, {4}) }}}}".format(
                entrypoint, link_text, class_name, optional_parameters, optional_attributes
            ),
            {"request": req},
        )

    def test_vpn_sign_in_link(self):
        """Should return expected markup"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Sign In",
            class_name="mzp-c-cta-link",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "VPN Sign In", "data-cta-type": "fxa-vpn", "data-cta-position": "navigation"},
        )
        expected = (
            '<a href="https://vpn.mozilla.org/oauth/init?entrypoint=www.mozilla.org-vpn-product-page'
            "&form_type=button&utm_source=www.mozilla.org-vpn-product-page&utm_medium=referral"
            '&utm_campaign=vpn-product-page&data_cta_position=navigation" data-action="https://accounts.firefox.com/" '
            'class="js-vpn-cta-link js-fxa-product-button mzp-c-cta-link" data-cta-text="VPN Sign In" '
            'data-cta-type="fxa-vpn" data-cta-position="navigation">Sign In</a>'
        )
        self.assertEqual(markup, expected)


@override_settings(VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING)
class TestVPNMonthlyPrice(TestCase):
    rf = RequestFactory()

    def _render(self, plan, country_code, lang):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render("{{{{ vpn_monthly_price('{0}', '{1}', '{2}') }}}}".format(plan, country_code, lang), {"request": req})

    def test_vpn_monthly_price_usd(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="US", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">US$9.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_euro(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="DE", lang="de")
        expected = '<span class="vpn-monthly-price-display">9,99‎ €<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_chf(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="CH", lang="de")
        expected = '<span class="vpn-monthly-price-display">CHF 10.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_6_month_price_usd(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month", country_code="US", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">US$7.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_6_month_price_euro(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month", country_code="DE", lang="de")
        expected = '<span class="vpn-monthly-price-display">6,99 €<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_6_month_price_chf(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month", country_code="CH", lang="de")
        expected = '<span class="vpn-monthly-price-display">CHF 7.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_usd(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="US", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">US$4.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_euro(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="DE", lang="de")
        expected = '<span class="vpn-monthly-price-display">4,99 €<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_chf(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="CH", lang="de")
        expected = '<span class="vpn-monthly-price-display">CHF 5.99<span>/month</span></span>'
        self.assertEqual(markup, expected)


@override_settings(VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING)
class TestVPNTotalPrice(TestCase):
    rf = RequestFactory()

    def _render(self, plan, country_code, lang):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render("{{{{ vpn_total_price('{0}', '{1}', '{2}') }}}}".format(plan, country_code, lang), {"request": req})

    def test_vpn_6_month_total_price_usd(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month", country_code="US", lang="en-US")
        expected = "US$47.94 total"
        self.assertEqual(markup, expected)

    def test_vpn_6_month_total_price_euro(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month", country_code="DE", lang="de")
        expected = "41,94 € total"
        self.assertEqual(markup, expected)

    def test_vpn_6_month_total_price_chf(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month", country_code="CH", lang="de")
        expected = "CHF 47.94 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_usd(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="US", lang="en-US")
        expected = "US$59.88 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_euro(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="DE", lang="de")
        expected = "59,88 € total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_chf(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="CH", lang="de")
        expected = "CHF 71.88 total"
        self.assertEqual(markup, expected)


@override_settings(VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING)
class TestVPNSaving(TestCase):
    rf = RequestFactory()

    def _render(self, plan, country_code, lang):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render("{{{{ vpn_saving('{0}', '{1}', '{2}') }}}}".format(plan, country_code, lang), {"request": req})

    def test_vpn_6_month_saving_usd(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month", country_code="US", lang="en-US")
        expected = "Save 20%"
        self.assertEqual(markup, expected)

    def test_vpn_6_month_saving_euro(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month", country_code="DE", lang="de")
        expected = "Save 30%"
        self.assertEqual(markup, expected)

    def test_vpn_6_month_saving_chf(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month", country_code="CH", lang="de")
        expected = "Save 27%"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving_usd(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="US", lang="en-US")
        expected = "Save 50%"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving_euro(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="DE", lang="de")
        expected = "Save 50%"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving_chf(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="CH", lang="de")
        expected = "Save 45%"
        self.assertEqual(markup, expected)


class TestVPNProductReferralLink(TestCase):
    rf = RequestFactory()

    def _render(self, referral_id, page_anchor, link_text, class_name, optional_attributes):
        with self.activate("en-US"):
            req = self.rf.get("/")
            req.locale = "en-US"
            return render(
                "{{{{ vpn_product_referral_link('{0}', '{1}', '{2}', '{3}', {4}) }}}}".format(
                    referral_id, page_anchor, link_text, class_name, optional_attributes
                ),
                {"request": req},
            )

    def test_vpn_product_referral_link(self):
        """Should return expected markup"""
        markup = self._render(
            referral_id="navigation",
            page_anchor="#pricing",
            link_text="Get Mozilla VPN",
            class_name="mzp-t-secondary mzp-t-md",
            optional_attributes={"data-cta-text": "Get Mozilla VPN", "data-cta-type": "button"},
        )
        expected = (
            '<a href="/en-US/products/vpn/#pricing" class="mzp-c-button mzp-t-product '
            'js-fxa-product-referral-link mzp-t-secondary mzp-t-md" data-referral-id="navigation" '
            'data-cta-text="Get Mozilla VPN" data-cta-type="button">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)
