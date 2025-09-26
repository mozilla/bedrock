# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test.client import RequestFactory
from django.test.utils import override_settings

import pytest
from django_jinja.backend import Jinja2

from bedrock.mozorg.tests import TestCase
from bedrock.products.templatetags.misc import vpn_supported_locale

TEST_FXA_ENDPOINT = "https://accounts.firefox.com/"
TEST_VPN_ENDPOINT = "https://vpn.mozilla.org/"
TEST_VPN_PRODUCT_ID = "prod_FvnsFHIfezy3ZI"
TEST_VPN_SUBSCRIPTION_URL = "https://accounts.firefox.com/"
TEST_VPN_SUBSCRIPTION_URL_NEXT = "https://payments.firefox.com/"
TEST_VPN_PRODUCT_ID_NEXT = "vpn"

TEST_VPN_PLAN_ID_MATRIX = {
    "chf": {  # Swiss franc
        "de": {  # German
            "12-month": {
                "price": "5.99",
                "total": "71.88",
                "currency": "CHF",
                "saving": 45,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "60.00", "price": "71.88", "period": "yearly"},
            },
            "monthly": {
                "price": "10.99",
                "total": None,
                "currency": "CHF",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "0", "price": "10.99", "period": "monthly"},
            },
        },
        "fr": {  # French
            "12-month": {
                "price": "5.99",
                "total": "71.88",
                "currency": "CHF",
                "saving": 45,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "60.00", "price": "71.88", "period": "yearly"},
            },
            "monthly": {
                "price": "10.99",
                "currency": "CHF",
                "total": None,
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "0", "price": "10.99", "period": "monthly"},
            },
        },
        "it": {  # Italian
            "12-month": {
                "price": "5.99",
                "total": "71.88",
                "currency": "CHF",
                "saving": 45,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "60.00", "price": "71.88", "period": "yearly"},
            },
            "monthly": {
                "price": "10.99",
                "total": None,
                "currency": "CHF",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "0", "price": "10.99", "period": "monthly"},
            },
        },
    },
    "czk": {  # Czech koruna
        "cs": {  # Czech
            "12-month": {
                "price": "119",
                "total": "1428",
                "currency": "CZK",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CZK", "discount": "1416", "price": "1428", "period": "yearly"},
            },
            "monthly": {
                "price": "237",
                "total": None,
                "currency": "CZK",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CZK", "discount": "0", "price": "237", "period": "monthly"},
            },
        },
    },
    "dkk": {  # Danish krone
        "da": {  # Dansk
            "12-month": {
                "price": "37",
                "total": "444",
                "currency": "DKK",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "DKK", "discount": "456", "price": "444", "period": "yearly"},
            },
            "monthly": {
                "price": "75",
                "total": None,
                "currency": "DKK",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "DKK", "discount": "0", "price": "75", "period": "monthly"},
            },
        },
    },
    "euro": {  # Euro
        "bg": {  # Bulgarian
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "de": {  # German
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "el": {  # Greek
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "en": {  # English
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "es": {  # Spanish
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "fr": {  # French
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "hu": {  # Hungarian
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "it": {  # Italian
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "nl": {  # Dutch
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "pt": {  # Portuguese
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "ro": {  # Romanian
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "sk": {  # Slovak
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "sl": {  # Slovenian
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
    },
    "pln": {  # Polish złoty
        "en": {  # English
            "12-month": {
                "price": "22",
                "total": "264",
                "currency": "PLN",
                "saving": 48,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "PLN", "discount": "276", "price": "264", "period": "yearly"},
            },
            "monthly": {
                "price": "45",
                "total": None,
                "currency": "PLN",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "PLN", "discount": "0", "price": "45", "period": "monthly"},
            },
        },
    },
    "usd": {  # US dollar
        "en": {  # English
            "12-month": {
                "price": "4.99",
                "total": "59.88",
                "currency": "USD",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "USD", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "price": "9.99",
                "total": None,
                "currency": "USD",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "USD", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        }
    },
}

TEST_VPN_VARIABLE_PRICING = {
    "AT": {  # Austria
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["de"],
    },
    "BG": {  # Bulgaria
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "BE": {  # Belgium
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["nl"],
        "de": TEST_VPN_PLAN_ID_MATRIX["euro"]["de"],
        "fr": TEST_VPN_PLAN_ID_MATRIX["euro"]["fr"],
    },
    "CH": {  # Switzerland
        "default": TEST_VPN_PLAN_ID_MATRIX["chf"]["de"],
        "fr": TEST_VPN_PLAN_ID_MATRIX["chf"]["fr"],
        "it": TEST_VPN_PLAN_ID_MATRIX["chf"]["it"],
    },
    "CY": {  # Cyprus
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
        "el": TEST_VPN_PLAN_ID_MATRIX["euro"]["el"],
    },
    "CZ": {  # Czech Republic
        "default": TEST_VPN_PLAN_ID_MATRIX["czk"]["cs"],
    },
    "DE": {  # Germany
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["de"],
    },
    "DK": {  # Denmark
        "default": TEST_VPN_PLAN_ID_MATRIX["dkk"]["da"],
    },
    "EE": {  # Estonia
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "ES": {  # Spain
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["es"],
    },
    "FI": {  # Finland
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "FR": {  # France
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["fr"],
    },
    "HR": {  # Croatia
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "HU": {  # Hungary
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["hu"],
    },
    "IE": {  # Ireland
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "IT": {  # Italy
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["it"],
    },
    "LT": {  # Lithuania
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "LU": {  # Luxembourg
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["fr"],
        "de": TEST_VPN_PLAN_ID_MATRIX["euro"]["de"],
    },
    "LV": {  # Latvia
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "MT": {  # Malta
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "NL": {  # the Netherlands
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["nl"],
    },
    "PL": {  # Poland
        "default": TEST_VPN_PLAN_ID_MATRIX["pln"]["en"],
    },
    "PT": {  # Portugal
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["pt"],
    },
    "RO": {  # Romania
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "SE": {  # Sweden
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "SI": {  # Slovenia
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["sl"],
    },
    "SK": {  # Slovakia
        "default": TEST_VPN_PLAN_ID_MATRIX["euro"]["sk"],
    },
    "US": {  # USA
        "default": TEST_VPN_PLAN_ID_MATRIX["usd"]["en"],
    },
}


@pytest.mark.parametrize(
    "locale",
    [
        "de",
        "el",
        "en-CA",
        "en-GB",
        "en-US",
        "es-ES",
        "es-MX",
        "pl",
        "pt-BR",
        "pt-PT",
        "tr",
        "uk",
        "zh-TW",
        "zh-CN",
    ],
)
def test_vpn_supported_locale(locale):
    """Should return True for locales where the VPN client is localized"""
    assert vpn_supported_locale(locale) is True


@pytest.mark.parametrize(
    "locale",
    [
        "ach",
        "br",
        "sco",
        "xh",
    ],
)
def test_vpn_not_supported_locale(locale):
    """Should return False for locales where the VPN client is not localized"""
    assert vpn_supported_locale(locale) is False


jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {})


@override_settings(
    FXA_ENDPOINT=TEST_FXA_ENDPOINT,
    VPN_PRODUCT_ID=TEST_VPN_PRODUCT_ID,
    VPN_SUBSCRIPTION_URL_NEXT=TEST_VPN_SUBSCRIPTION_URL_NEXT,
    VPN_PRODUCT_ID_NEXT=TEST_VPN_PRODUCT_ID_NEXT,
    VPN_SUBSCRIPTION_URL=TEST_VPN_SUBSCRIPTION_URL,
    VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING,
    VPN_SUBSCRIPTION_USE_DAILY_MODE__QA_ONLY=False,
)
class TestVPNSubscribeLinkNext(TestCase):
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
            f"""{{{{ vpn_subscribe_link('{entrypoint}', '{link_text}', '{plan}', '{class_name}', '{country_code}',
                                        '{lang}', {optional_parameters}, {optional_attributes}) }}}}""",
            {"request": req},
        )

    def test_vpn_subscribe_link_variable_12_month(self):
        """Should return expected markup for variable 12-month plan link"""
        markup = self._render(
            plan="12-month",
            country_code="US",
            lang="en-US",
            optional_parameters={"utm_campaign": "vpn-product-page"},
            optional_attributes={"data-cta-text": "Get Mozilla VPN yearly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://payments.firefox.com/vpn/yearly/landing/'
            "?entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
            'class="js-fxa-product-cta-link js-fxa-product-button mzp-c-button ga-begin-checkout" data-cta-text="Get Mozilla VPN yearly" '
            'data-cta-type="fxa-vpn" data-cta-position="primary" data-ga-item="{\'brand\' : \'vpn\','
            "'plan' : 'vpn','period' : 'yearly','price' : '59.88','discount' : '60.00','currency' : 'USD'}\">Get Mozilla VPN</a>"
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_variable_12_month_no_options(self):
        """Should return expected markup for variable 12-month plan link with analytics"""
        markup = self._render(
            plan="12-month",
            country_code="US",
            lang="en-US",
        )
        expected = (
            '<a href="https://payments.firefox.com/vpn/yearly/landing/'
            "?entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral" data-action="https://accounts.firefox.com/" class="js-fxa-product-cta-link js-fxa-product-button mzp-c-button '
            "ga-begin-checkout\" data-ga-item=\"{'brand' : 'vpn','plan' : 'vpn','period' : 'yearly',"
            "'price' : '59.88','discount' : '60.00','currency' : 'USD'}\">Get Mozilla VPN</a>"
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
            '<a href="https://payments.firefox.com/vpn/monthly/landing/'
            "?entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
            'class="js-fxa-product-cta-link js-fxa-product-button mzp-c-button ga-begin-checkout" data-cta-text="Get Mozilla VPN monthly" '
            'data-cta-type="fxa-vpn" data-cta-position="primary" data-ga-item="{\'brand\' : \'vpn\','
            "'plan' : 'vpn','period' : 'monthly','price' : '9.99','discount' : '0','currency' : 'USD'}\">Get Mozilla VPN</a>"
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_daily_instead_of_monthly_for_staging_testing_only(self):
        """Should return expected markup for a link to a daily subscription that ONLY exists on the staging server for QA"""

        with override_settings(VPN_SUBSCRIPTION_USE_DAILY_MODE__QA_ONLY=True):
            markup = self._render(
                plan="monthly",
                country_code="US",
                lang="en-US",
                optional_parameters={"utm_campaign": "vpn-product-page"},
                optional_attributes={"data-cta-text": "Get Mozilla VPN monthly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
            )

        # The only change compared to monthly sub is the /daily/ in the URL, not any of the params
        expected = (
            '<a href="https://payments.firefox.com/vpn/daily/landing/'
            "?entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
            'class="js-fxa-product-cta-link js-fxa-product-button mzp-c-button ga-begin-checkout" data-cta-text="Get Mozilla VPN monthly" '
            'data-cta-type="fxa-vpn" data-cta-position="primary" data-ga-item="{\'brand\' : \'vpn\','
            "'plan' : 'vpn','period' : 'monthly','price' : '9.99','discount' : '0','currency' : 'USD'}\">Get Mozilla VPN</a>"
        )
        self.assertEqual(markup, expected)

    def test_vpn_subscribe_link_remains_annual_when_qa_mode_is_on(self):
        """Should return expected markup for a link to an annual subscription even though
        the QA mode for daily subscription is on, because that only affects 'monthly' mode

        The output here is the same as for test_vpn_subscribe_link_variable_12_month
        """

        with override_settings(VPN_SUBSCRIPTION_USE_DAILY_MODE__QA_ONLY=True):
            markup = self._render(
                plan="12-month",
                country_code="US",
                lang="en-US",
                optional_parameters={"utm_campaign": "vpn-product-page"},
                optional_attributes={"data-cta-text": "Get Mozilla VPN yearly", "data-cta-type": "fxa-vpn", "data-cta-position": "primary"},
            )
            expected = (
                '<a href="https://payments.firefox.com/vpn/yearly/landing/'
                "?entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page"
                '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
                'class="js-fxa-product-cta-link js-fxa-product-button mzp-c-button ga-begin-checkout" data-cta-text="Get Mozilla VPN yearly" '
                'data-cta-type="fxa-vpn" data-cta-position="primary" data-ga-item="{\'brand\' : \'vpn\','
                "'plan' : 'vpn','period' : 'yearly','price' : '59.88','discount' : '60.00','currency' : 'USD'}\">Get Mozilla VPN</a>"
            )

        self.assertEqual(markup, expected)


@override_settings(VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING)
class TestVPNMonthlyPrice(TestCase):
    rf = RequestFactory()

    def _render(self, plan, country_code, lang):
        req = self.rf.get("/")
        req.locale = lang
        return render(f"{{{{ vpn_monthly_price('{plan}', '{country_code}', '{lang}') }}}}", {"request": req})

    def test_vpn_monthly_price_usd_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="US", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$9.99<span>/month + tax</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_usd_en_ca(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="CA", lang="en-CA")
        expected = '<span class="vpn-monthly-price-display">US$9.99<span>/month + tax</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_euro_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="DE", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">€9.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_euro_de(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="DE", lang="de")
        expected = '<span class="vpn-monthly-price-display">9,99\xa0€<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_euro_fi(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="FI", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">€9.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_chf_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="CH", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">CHF10.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_chf_de(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="CH", lang="de")
        expected = '<span class="vpn-monthly-price-display">10,99\xa0CHF<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_usd_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="US", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$4.99<span>/month + tax</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_usd_en_ca(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="CA", lang="en-CA")
        expected = '<span class="vpn-monthly-price-display">US$4.99<span>/month + tax</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_euro_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="DE", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">€4.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_euro_de(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="DE", lang="de")
        expected = '<span class="vpn-monthly-price-display">4,99\xa0€<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_euro_fi(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="FI", lang="fi")
        expected = '<span class="vpn-monthly-price-display">4,99\xa0€<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_chf_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="CH", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">CHF5.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_chf_de(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="CH", lang="de")
        expected = '<span class="vpn-monthly-price-display">5,99\xa0CHF<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_czk_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="CZ", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">CZK237.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_czk_cs(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="CZ", lang="cs")
        expected = '<span class="vpn-monthly-price-display">237,00\xa0Kč<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_czk_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="CZ", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">CZK119.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_czk_cs(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="CZ", lang="cs")
        expected = '<span class="vpn-monthly-price-display">119,00\xa0Kč<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_dkk_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="DK", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">DKK75.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_dkk_da(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="DK", lang="da")
        expected = '<span class="vpn-monthly-price-display">75,00\xa0kr.<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_dkk_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="DK", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">DKK37.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_dkk_da(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="DK", lang="da")
        expected = '<span class="vpn-monthly-price-display">37,00\xa0kr.<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_pln_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="PL", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">PLN45.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_pln_pl(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="PL", lang="pl")
        expected = '<span class="vpn-monthly-price-display">45,00\xa0zł<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_pln_pl(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="PL", lang="pl")
        expected = '<span class="vpn-monthly-price-display">22,00\xa0zł<span>/month</span></span>'
        self.assertEqual(markup, expected)


class TestVPNMobileMonthlyPrice(TestCase):
    rf = RequestFactory()

    def _render(self, plan, country_code, lang):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(f"{{{{ vpn_mobile_monthly_price('{plan}', '{country_code}', '{lang}') }}}}", {"request": req})

    def test_vpn_monthly_price_au_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="AU", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">A$14.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_au_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="AU", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">A$7.50<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_bd_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="BD", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">BDT1,200.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_bd_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="BD", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">BDT583.33<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_br_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="BR", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">R$56.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_br_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="BR", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">R$27.50<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_cl_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="CL", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">CLP9,300<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_cl_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="CL", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">CLP4,582<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_co_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="CO", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">COP41,900.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_co_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="CO", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">COP20,825.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_eg_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="EG", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">EGP479.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_eg_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="EG", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">EGP241.67<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_gr_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="GR", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">€9.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_gr_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="GR", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">€4.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_id_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="ID", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">IDR155,000.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_id_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="ID", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">IDR75,000.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_in_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="IN", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">₹839.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_in_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="IN", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">₹416.58<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_ke_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="KE", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$9.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_ke_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="KE", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$5.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_kr_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="KR", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">₩13,500<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_kr_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="KR", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">₩6,658<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_ma_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="MA", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">MAD99.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_ma_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="MA", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">MAD50.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_mx_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="MX", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">MX$189.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_mx_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="MX", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">MX$95.75<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_ng_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="NG", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">NGN15,900.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_ng_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="NG", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">NGN8,325.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_no_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="NO", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">NOK110.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_no_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="NO", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">NOK54.17<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_sa_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="SA", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">SAR36.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_sa_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="SA", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">SAR18.75<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_sn_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="SN", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$9.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_sn_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="SN", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$4.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_th_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="TH", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">THB330.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_th_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="TH", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">THB165.83<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_tr_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="TR", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">TRY339.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_tr_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="TR", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">TRY166.67<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_tw_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="TW", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">NT$320.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_tw_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="TW", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">NT$158.33<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_ua_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="UA", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$9.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_ua_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="UA", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$5.00<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_ug_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="UG", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$9.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_ug_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="UG", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$4.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_vn_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="VN", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">₫249,000<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_vn_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="VN", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">₫124,917<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_za_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="ZA", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">ZAR169.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_za_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="ZA", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">ZAR83.33<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_monthly_price_unknown_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="monthly", country_code="", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$9.99<span>/month</span></span>'
        self.assertEqual(markup, expected)

    def test_vpn_12_month_price_unknown_en_us(self):
        """Should return expected markup"""
        markup = self._render(plan="12-month", country_code="", lang="en-US")
        expected = '<span class="vpn-monthly-price-display">$4.99<span>/month</span></span>'
        self.assertEqual(markup, expected)


@override_settings(
    VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING,
)
class TestVPNTotalPrice(TestCase):
    rf = RequestFactory()

    def _render(self, country_code, lang):
        req = self.rf.get("/")
        req.locale = lang
        return render(f"{{{{ vpn_total_price('{country_code}', '{lang}') }}}}", {"request": req})

    def test_vpn_12_month_total_price_usd_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="US", lang="en-US")
        expected = "$59.88 total + tax"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_usd_en_cs(self):
        """Should return expected markup"""
        markup = self._render(country_code="CA", lang="en-CA")
        expected = "US$59.88 total + tax"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_euro_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="DE", lang="en-US")
        expected = "€59.88 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_euro_de(self):
        """Should return expected markup"""
        markup = self._render(country_code="DE", lang="de")
        expected = "59,88\xa0€ total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_euro_fi(self):
        """Should return expected markup"""
        markup = self._render(country_code="FI", lang="fi")
        expected = "59,88\xa0€ total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_chf_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="CH", lang="en-US")
        expected = "CHF71.88 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_chf_de(self):
        """Should return expected markup"""
        markup = self._render(country_code="CH", lang="de")
        expected = "71,88\xa0CHF total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_czk_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="CZ", lang="en-US")
        expected = "CZK1,428.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_czk_cs(self):
        """Should return expected markup"""
        markup = self._render(country_code="CZ", lang="cs")
        expected = "1\xa0428,00\xa0Kč total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_dkk_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="DK", lang="en-US")
        expected = "DKK444.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_dkk_da(self):
        """Should return expected markup"""
        markup = self._render(country_code="DK", lang="da")
        expected = "444,00\xa0kr. total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_pln_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="PL", lang="en-US")
        expected = "PLN264.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_pln_pl(self):
        """Should return expected markup"""
        markup = self._render(country_code="PL", lang="pl")
        expected = "264,00\xa0zł total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_unknown_locale(self):
        """Should return expected markup"""
        markup = self._render(country_code="US", lang="ach")
        expected = "$59.88 total + tax"
        self.assertEqual(markup, expected)


class TestVPNMobileTotalPrice(TestCase):
    rf = RequestFactory()

    def _render(self, country_code, lang):
        req = self.rf.get("/")
        req.locale = lang
        return render(f"{{{{ vpn_mobile_total_price('{country_code}', '{lang}') }}}}", {"request": req})

    def test_vpn_12_month_total_price_au_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="AU", lang="en-US")
        expected = "A$89.99 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_bd_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="BD", lang="en-US")
        expected = "BDT7,000.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_br_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="BR", lang="en-US")
        expected = "R$330.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_cl_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="CL", lang="en-US")
        expected = "CLP54,990 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_co_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="CO", lang="en-US")
        expected = "COP249,900.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_eg_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="EG", lang="en-US")
        expected = "EGP2,899.99 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_gr_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="GR", lang="en-US")
        expected = "€59.88 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_id_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="ID", lang="en-US")
        expected = "IDR900,000.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_in_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="IN", lang="en-US")
        expected = "₹4,999.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_ke_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="KE", lang="en-US")
        expected = "$59.99 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_kr_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="KR", lang="en-US")
        expected = "₩79,900 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_ma_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="MA", lang="en-US")
        expected = "MAD600.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_mx_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="MX", lang="en-US")
        expected = "MX$1,149.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_ng_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="NG", lang="en-US")
        expected = "NGN99,900.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_no_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="NO", lang="en-US")
        expected = "NOK650.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_sa_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="SA", lang="en-US")
        expected = "SAR224.99 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_sn_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="SN", lang="en-US")
        expected = "$59.88 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_th_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="TH", lang="en-US")
        expected = "THB1,990.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_tr_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="TR", lang="en-US")
        expected = "TRY1,999.99 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_tw_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="TW", lang="en-US")
        expected = "NT$1,900.00 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_ua_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="UA", lang="en-US")
        expected = "$59.99 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_ug_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="UG", lang="en-US")
        expected = "$59.88 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_vn_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="VN", lang="en-US")
        expected = "₫1,499,000 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_za_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="ZA", lang="en-US")
        expected = "ZAR999.99 total"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_unknown_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="", lang="en-US")
        expected = "$59.88 total"
        self.assertEqual(markup, expected)


@override_settings(
    VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING,
)
class TestVPNSaving(TestCase):
    rf = RequestFactory()

    def _render(self, country_code, lang):
        req = self.rf.get("/")
        req.locale = lang
        return render(f"{{{{ vpn_saving('{country_code}', '{lang}') }}}}", {"request": req})

    def test_vpn_12_month_saving_usd(self):
        """Should return expected markup"""
        markup = self._render(country_code="US", lang="en-US")
        expected = "Save 50%"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving_euro(self):
        """Should return expected markup"""
        markup = self._render(country_code="DE", lang="en-US")
        expected = "Save 50%"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving_chf(self):
        """Should return expected markup"""
        markup = self._render(country_code="CH", lang="en-US")
        expected = "Save 45%"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving_bgn(self):
        """Should return expected markup"""
        markup = self._render(country_code="BG", lang="en-US")
        expected = "Save 50%"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving_czk(self):
        """Should return expected markup"""
        markup = self._render(country_code="CZ", lang="en-US")
        expected = "Save 50%"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving_dkk(self):
        """Should return expected markup"""
        markup = self._render(country_code="DK", lang="en-US")
        expected = "Save 50%"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving_huf(self):
        """Should return expected markup"""
        markup = self._render(country_code="HU", lang="en-US")
        expected = "Save 50%"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving_pln(self):
        """Should return expected markup"""
        markup = self._render(country_code="PL", lang="en-US")
        expected = "Save 48%"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_saving_ron(self):
        """Should return expected markup"""
        markup = self._render(country_code="RO", lang="en-US")
        expected = "Save 50%"
        self.assertEqual(markup, expected)


class TestVPNProductReferralLink(TestCase):
    rf = RequestFactory()

    def _render(
        self,
        referral_id="",
        link_to_pricing_page=False,
        page_anchor="",
        link_text=None,
        is_cta_button_styled=True,
        class_name=None,
        optional_attributes=None,
        optional_parameters=None,
    ):
        with self.activate_locale("en-US"):
            req = self.rf.get("/")
            req.locale = "en-US"

            return render(
                f"""{{{{ vpn_product_referral_link(
                    '{referral_id}',
                    {link_to_pricing_page},
                    '{page_anchor}',
                    '{link_text}',
                    {is_cta_button_styled},
                    '{class_name}',
                    {optional_attributes},
                    {optional_parameters}
                ) }}}}""",
                {"request": req},
            )

    def test_vpn_product_referral_link(self):
        """Should return expected markup"""
        markup = self._render(
            referral_id="navigation",
            page_anchor="#pricing",
            link_text="Get Mozilla VPN",
            class_name="mzp-t-product mzp-t-secondary mzp-t-md",
            optional_attributes={"data-cta-text": "Get Mozilla VPN", "data-cta-type": "vpn"},
        )
        expected = (
            '<a href="/en-US/products/vpn/#pricing" class="mzp-c-button js-fxa-product-referral-link '
            'mzp-t-product mzp-t-secondary mzp-t-md" data-referral-id="navigation" '
            'data-cta-text="Get Mozilla VPN" data-cta-type="vpn">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_product_referral_link_pricing_page(self):
        """Should return expected markup when linking to pricing page"""
        markup = self._render(
            referral_id="navigation",
            link_to_pricing_page=True,
            link_text="Get Mozilla VPN",
            class_name="mzp-t-product mzp-t-secondary mzp-t-md",
            optional_attributes={"data-cta-text": "Get Mozilla VPN", "data-cta-type": "vpn"},
        )
        expected = (
            '<a href="/en-US/products/vpn/pricing/" class="mzp-c-button js-fxa-product-referral-link '
            'mzp-t-product mzp-t-secondary mzp-t-md" data-referral-id="navigation" '
            'data-cta-text="Get Mozilla VPN" data-cta-type="vpn">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_product_referral_link_optional_params(self):
        """Should return expected markup when adding optional parameters"""
        markup = self._render(
            referral_id="navigation",
            link_to_pricing_page=True,
            link_text="Get Mozilla VPN",
            is_cta_button_styled=False,
            class_name="mzp-t-product mzp-t-secondary mzp-t-md",
            optional_attributes={"data-cta-text": "Get Mozilla VPN", "data-cta-type": "vpn"},
            optional_parameters={"coupon": "cyber20"},
        )
        expected = (
            '<a href="/en-US/products/vpn/pricing/?coupon=cyber20" class="js-fxa-product-referral-link '
            'mzp-t-product mzp-t-secondary mzp-t-md" data-referral-id="navigation" '
            'data-cta-text="Get Mozilla VPN" data-cta-type="vpn">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)
