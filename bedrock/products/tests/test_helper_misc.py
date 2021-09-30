# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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
    "at": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["de"],
    },
    "be": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["nl"],
        "alt": {
            "fr": TEST_VPN_PLAN_ID_MATRIX["euro"]["fr"],
        },
    },
    "ch": {
        "default": TEST_VPN_PLAN_ID_MATRIX["chf"]["de"],
        "alt": {
            "fr": TEST_VPN_PLAN_ID_MATRIX["chf"]["fr"],
            "it": TEST_VPN_PLAN_ID_MATRIX["chf"]["it"],
        },
    },
    "de": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["de"],
    },
    "es": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["es"],
    },
    "fr": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["fr"],
    },
    "it": {
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["it"],
    },
    "us": {
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

    def _render(self, entrypoint, link_text, plan="12-month", class_name=None, lang=None, optional_parameters=None, optional_attributes=None):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(
            "{{{{ vpn_subscribe_link('{0}', '{1}', '{2}', '{3}', '{4}', {5}, {6}) }}}}".format(
                entrypoint, link_text, plan, class_name, lang, optional_parameters, optional_attributes
            ),
            {"request": req},
        )

    def test_vpn_subscribe_link_variable_12_month_en(self):
        """Should return expected markup for variable 12-month plan for en-US"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="12-month",
            class_name="mzp-c-button",
            lang="en-US",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            'data-action="https://accounts.firefox.com/" class="js-vpn-cta-link js-fxa-product-button mzp-c-button" '
            'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            'data-plan-at="price_1IgwblJNcmPzuWtRynC7dqQa" data-plan-be="price_1J5JRGJNcmPzuWtRXwXA84cm" '
            'data-plan-ch="price_1J5JssJNcmPzuWtR616BH4aU" data-plan-de="price_1IgwblJNcmPzuWtRynC7dqQa" '
            'data-plan-es="price_1J5JCdJNcmPzuWtRrvQMFLlP" data-plan-fr="price_1IgnlcJNcmPzuWtRjrNa39W4" '
            'data-plan-it="price_1J4owvJNcmPzuWtRomVhWQFq" data-plan-us="price_1Iw85dJNcmPzuWtRyhMDdtM7">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_6_month_en(self):
        """Should return expected markup for variable 6-month plan for en-US"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="6-month",
            class_name="mzp-c-button",
            lang="en-US",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw87cJNcmPzuWtRefuyqsOd'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            'data-action="https://accounts.firefox.com/" class="js-vpn-cta-link js-fxa-product-button mzp-c-button" '
            'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            'data-plan-at="price_1IgwaHJNcmPzuWtRuUfSR4l7" data-plan-be="price_1J5JRmJNcmPzuWtRyFGj0tkN" '
            'data-plan-ch="price_1J5JtWJNcmPzuWtRMd2siphH" data-plan-de="price_1IgwaHJNcmPzuWtRuUfSR4l7" '
            'data-plan-es="price_1J5JDFJNcmPzuWtRrC4IeXTs" data-plan-fr="price_1IgoxGJNcmPzuWtRG7l48EoV" '
            'data-plan-it="price_1J5J7eJNcmPzuWtRKdQi4Tkk" data-plan-us="price_1Iw87cJNcmPzuWtRefuyqsOd">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_monthly_en(self):
        """Should return expected markup for variable monthly plan for en-US"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="monthly",
            class_name="mzp-c-button",
            lang="en-US",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw7qSJNcmPzuWtRMUZpOwLm'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            'data-action="https://accounts.firefox.com/" class="js-vpn-cta-link js-fxa-product-button mzp-c-button" '
            'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            'data-plan-at="price_1IgwZVJNcmPzuWtRg9Wssh2y" data-plan-be="price_1J5JSkJNcmPzuWtR54LPH2zi" '
            'data-plan-ch="price_1J5Ju3JNcmPzuWtR3GpNYSWj" data-plan-de="price_1IgwZVJNcmPzuWtRg9Wssh2y" '
            'data-plan-es="price_1J5JDgJNcmPzuWtRqQtIbktk" data-plan-fr="price_1IgowHJNcmPzuWtRzD7SgAYb" '
            'data-plan-it="price_1J5J6iJNcmPzuWtRK5zfoguV" data-plan-us="price_1Iw7qSJNcmPzuWtRMUZpOwLm">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_12_month_de(self):
        """Should return expected markup for variable 12-month plan for de"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="12-month",
            class_name="mzp-c-button",
            lang="de",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1IgwblJNcmPzuWtRynC7dqQa'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            'data-action="https://accounts.firefox.com/" class="js-vpn-cta-link js-fxa-product-button mzp-c-button" '
            'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            'data-plan-at="price_1IgwblJNcmPzuWtRynC7dqQa" data-plan-be="price_1J5JRGJNcmPzuWtRXwXA84cm" '
            'data-plan-ch="price_1J5JssJNcmPzuWtR616BH4aU" data-plan-de="price_1IgwblJNcmPzuWtRynC7dqQa" '
            'data-plan-es="price_1J5JCdJNcmPzuWtRrvQMFLlP" data-plan-fr="price_1IgnlcJNcmPzuWtRjrNa39W4" '
            'data-plan-it="price_1J4owvJNcmPzuWtRomVhWQFq" data-plan-us="price_1Iw85dJNcmPzuWtRyhMDdtM7">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_6_month_de(self):
        """Should return expected markup for variable 6-month plan for de"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="6-month",
            class_name="mzp-c-button",
            lang="de",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1IgwaHJNcmPzuWtRuUfSR4l7'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            'data-action="https://accounts.firefox.com/" class="js-vpn-cta-link js-fxa-product-button mzp-c-button" '
            'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            'data-plan-at="price_1IgwaHJNcmPzuWtRuUfSR4l7" data-plan-be="price_1J5JRmJNcmPzuWtRyFGj0tkN" '
            'data-plan-ch="price_1J5JtWJNcmPzuWtRMd2siphH" data-plan-de="price_1IgwaHJNcmPzuWtRuUfSR4l7" '
            'data-plan-es="price_1J5JDFJNcmPzuWtRrC4IeXTs" data-plan-fr="price_1IgoxGJNcmPzuWtRG7l48EoV" '
            'data-plan-it="price_1J5J7eJNcmPzuWtRKdQi4Tkk" data-plan-us="price_1Iw87cJNcmPzuWtRefuyqsOd">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_monthly_de(self):
        """Should return expected markup for variable monthly plan for de"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="monthly",
            class_name="mzp-c-button",
            lang="de",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1IgwZVJNcmPzuWtRg9Wssh2y'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            'data-action="https://accounts.firefox.com/" class="js-vpn-cta-link js-fxa-product-button mzp-c-button" '
            'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            'data-plan-at="price_1IgwZVJNcmPzuWtRg9Wssh2y" data-plan-be="price_1J5JSkJNcmPzuWtR54LPH2zi" '
            'data-plan-ch="price_1J5Ju3JNcmPzuWtR3GpNYSWj" data-plan-de="price_1IgwZVJNcmPzuWtRg9Wssh2y" '
            'data-plan-es="price_1J5JDgJNcmPzuWtRqQtIbktk" data-plan-fr="price_1IgowHJNcmPzuWtRzD7SgAYb" '
            'data-plan-it="price_1J5J6iJNcmPzuWtRK5zfoguV" data-plan-us="price_1Iw7qSJNcmPzuWtRMUZpOwLm">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_12_month_fr(self):
        """Should return expected markup for variable 12-month plan for fr"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="12-month",
            class_name="mzp-c-button",
            lang="fr",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1IgnlcJNcmPzuWtRjrNa39W4'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            'data-action="https://accounts.firefox.com/" class="js-vpn-cta-link js-fxa-product-button mzp-c-button" '
            'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            'data-plan-at="price_1IgwblJNcmPzuWtRynC7dqQa" data-plan-be="price_1IgnlcJNcmPzuWtRjrNa39W4" '
            'data-plan-ch="price_1J5JunJNcmPzuWtRo9dLxn6M" data-plan-de="price_1IgwblJNcmPzuWtRynC7dqQa" '
            'data-plan-es="price_1J5JCdJNcmPzuWtRrvQMFLlP" data-plan-fr="price_1IgnlcJNcmPzuWtRjrNa39W4" '
            'data-plan-it="price_1J4owvJNcmPzuWtRomVhWQFq" data-plan-us="price_1Iw85dJNcmPzuWtRyhMDdtM7">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_6_month_fr(self):
        """Should return expected markup for variable 6-month plan for fr"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="6-month",
            class_name="mzp-c-button",
            lang="fr",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1IgoxGJNcmPzuWtRG7l48EoV'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
            'class="js-vpn-cta-link js-fxa-product-button mzp-c-button" data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" '
            'data-cta-position="primary" data-plan-at="price_1IgwaHJNcmPzuWtRuUfSR4l7" data-plan-be="price_1IgoxGJNcmPzuWtRG7l48EoV" '
            'data-plan-ch="price_1J5JvLJNcmPzuWtRayB4d7Ij" data-plan-de="price_1IgwaHJNcmPzuWtRuUfSR4l7" '
            'data-plan-es="price_1J5JDFJNcmPzuWtRrC4IeXTs" data-plan-fr="price_1IgoxGJNcmPzuWtRG7l48EoV" '
            'data-plan-it="price_1J5J7eJNcmPzuWtRKdQi4Tkk" data-plan-us="price_1Iw87cJNcmPzuWtRefuyqsOd">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_monthly_fr(self):
        """Should return expected markup for variable monthly plan for fr"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="monthly",
            class_name="mzp-c-button",
            lang="fr",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1IgowHJNcmPzuWtRzD7SgAYb'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            'data-action="https://accounts.firefox.com/" class="js-vpn-cta-link js-fxa-product-button mzp-c-button" '
            'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            'data-plan-at="price_1IgwZVJNcmPzuWtRg9Wssh2y" data-plan-be="price_1IgowHJNcmPzuWtRzD7SgAYb" '
            'data-plan-ch="price_1J5JvjJNcmPzuWtR3wwy1dcR" data-plan-de="price_1IgwZVJNcmPzuWtRg9Wssh2y" '
            'data-plan-es="price_1J5JDgJNcmPzuWtRqQtIbktk" data-plan-fr="price_1IgowHJNcmPzuWtRzD7SgAYb" '
            'data-plan-it="price_1J5J6iJNcmPzuWtRK5zfoguV" data-plan-us="price_1Iw7qSJNcmPzuWtRMUZpOwLm">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_12_month_es(self):
        """Should return expected markup for variable 12-month plan for es-ES"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="12-month",
            class_name="mzp-c-button",
            lang="es-ES",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1J5JCdJNcmPzuWtRrvQMFLlP'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            'data-action="https://accounts.firefox.com/" class="js-vpn-cta-link js-fxa-product-button mzp-c-button" '
            'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            'data-plan-at="price_1IgwblJNcmPzuWtRynC7dqQa" data-plan-be="price_1J5JRGJNcmPzuWtRXwXA84cm" '
            'data-plan-ch="price_1J5JssJNcmPzuWtR616BH4aU" data-plan-de="price_1IgwblJNcmPzuWtRynC7dqQa" '
            'data-plan-es="price_1J5JCdJNcmPzuWtRrvQMFLlP" data-plan-fr="price_1IgnlcJNcmPzuWtRjrNa39W4" '
            'data-plan-it="price_1J4owvJNcmPzuWtRomVhWQFq" data-plan-us="price_1Iw85dJNcmPzuWtRyhMDdtM7">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_6_month_es(self):
        """Should return expected markup for variable 6-month plan for es-ES"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="6-month",
            class_name="mzp-c-button",
            lang="es-ES",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1J5JDFJNcmPzuWtRrC4IeXTs'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
            'class="js-vpn-cta-link js-fxa-product-button mzp-c-button" data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" '
            'data-cta-position="primary" data-plan-at="price_1IgwaHJNcmPzuWtRuUfSR4l7" data-plan-be="price_1J5JRmJNcmPzuWtRyFGj0tkN" '
            'data-plan-ch="price_1J5JtWJNcmPzuWtRMd2siphH" data-plan-de="price_1IgwaHJNcmPzuWtRuUfSR4l7" '
            'data-plan-es="price_1J5JDFJNcmPzuWtRrC4IeXTs" data-plan-fr="price_1IgoxGJNcmPzuWtRG7l48EoV" '
            'data-plan-it="price_1J5J7eJNcmPzuWtRKdQi4Tkk" data-plan-us="price_1Iw87cJNcmPzuWtRefuyqsOd">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_monthly_es(self):
        """Should return expected markup for variable monthly plan for es-ES"""
        markup = self._render(
            entrypoint="www.mozilla.org-vpn-product-page",
            link_text="Get Mozilla VPN",
            plan="monthly",
            class_name="mzp-c-button",
            lang="es-ES",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1J5JDgJNcmPzuWtRqQtIbktk'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" '
            'data-action="https://accounts.firefox.com/" class="js-vpn-cta-link js-fxa-product-button mzp-c-button" '
            'data-cta-text="Get Mozilla VPN monthly" data-cta-type="fxa-vpn" data-cta-position="primary" '
            'data-plan-at="price_1IgwZVJNcmPzuWtRg9Wssh2y" data-plan-be="price_1J5JSkJNcmPzuWtR54LPH2zi" '
            'data-plan-ch="price_1J5Ju3JNcmPzuWtR3GpNYSWj" data-plan-de="price_1IgwZVJNcmPzuWtRg9Wssh2y" '
            'data-plan-es="price_1J5JDgJNcmPzuWtRqQtIbktk" data-plan-fr="price_1IgowHJNcmPzuWtRzD7SgAYb" '
            'data-plan-it="price_1J5J6iJNcmPzuWtRK5zfoguV" data-plan-us="price_1Iw7qSJNcmPzuWtRMUZpOwLm">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)


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

    def _render(self, plan):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render("{{{{ vpn_monthly_price('{0}') }}}}".format(plan), {"request": req})

    def test_vpn_monthly_price(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly")
        expected = (
            '<span class="js-vpn-monthly-price-display" data-price-usd="US$9.99<span>/month</span>" '
            'data-price-euro="9,99‎ €<span>/month</span>" data-price-chf="CHF 10.99<span>/month</span>">'
            "US$9.99<span>/month</span></span>"
        )
        self.assertEqual(markup, expected)

    def test_vpn_6_month_price(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month")
        expected = (
            '<span class="js-vpn-monthly-price-display" data-price-usd="US$7.99<span>/month</span>" '
            'data-price-euro="6,99 €<span>/month</span>" data-price-chf="CHF 7.99<span>/month</span>">'
            "US$7.99<span>/month</span></span>"
        )
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month")
        expected = (
            '<span class="js-vpn-monthly-price-display" data-price-usd="US$4.99<span>/month</span>" '
            'data-price-euro="4,99 €<span>/month</span>" data-price-chf="CHF 5.99<span>/month</span>">'
            "US$4.99<span>/month</span></span>"
        )
        self.assertEqual(markup, expected)


@override_settings(VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING)
class TestVPNTotalPrice(TestCase):
    rf = RequestFactory()

    def _render(self, plan):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render("{{{{ vpn_total_price('{0}') }}}}".format(plan), {"request": req})

    def test_vpn_6_month_total_price(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month")
        expected = (
            '<span class="js-vpn-total-price-display" data-price-usd="US$47.94 total" '
            'data-price-euro="41,94 € total" data-price-chf="CHF 47.94 total">US$47.94 total</span>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month")
        expected = (
            '<span class="js-vpn-total-price-display" data-price-usd="US$59.88 total" '
            'data-price-euro="59,88 € total" data-price-chf="CHF 71.88 total">US$59.88 total</span>'
        )
        self.assertEqual(markup, expected)


@override_settings(VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING)
class TestVPNSaving(TestCase):
    rf = RequestFactory()

    def _render(self, plan):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render("{{{{ vpn_saving('{0}') }}}}".format(plan), {"request": req})

    def test_vpn_6_month_saving(self):
        """Should return expected markup"""
        markup = self._render(plan="6-month")
        expected = (
            '<span class="js-vpn-saving-display" data-price-usd="Save 20%" ' 'data-price-euro="Save 30%" data-price-chf="Save 27%">Save 20%</span>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month")
        expected = (
            '<span class="js-vpn-saving-display" data-price-usd="Save 50%" ' 'data-price-euro="Save 50%" data-price-chf="Save 45%">Save 50%</span>'
        )
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
