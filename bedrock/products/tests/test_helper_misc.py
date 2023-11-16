# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.test.client import RequestFactory
from django.test.utils import override_settings

import pytest
from django_jinja.backend import Jinja2

from bedrock.mozorg.tests import TestCase
from bedrock.products.templatetags.misc import vpn_available_in_country, vpn_supported_locale

TEST_FXA_ENDPOINT = "https://accounts.firefox.com/"
TEST_VPN_ENDPOINT = "https://vpn.mozilla.org/"
TEST_VPN_PRODUCT_ID = "prod_FvnsFHIfezy3ZI"
TEST_VPN_SUBSCRIPTION_URL = "https://accounts.firefox.com/"

TEST_VPN_PLAN_ID_MATRIX = {
    "chf": {  # Swiss franc
        "de": {  # German
            "12-month": {
                "id": "price_1J5JssJNcmPzuWtR616BH4aU",
                "price": "5.99",
                "total": "71.88",
                "currency": "CHF",
                "saving": 45,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "60.00", "price": "71.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J5Ju3JNcmPzuWtR3GpNYSWj",
                "price": "10.99",
                "total": None,
                "currency": "CHF",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "0", "price": "10.99", "period": "monthly"},
            },
        },
        "fr": {  # French
            "12-month": {
                "id": "price_1J5JunJNcmPzuWtRo9dLxn6M",
                "price": "5.99",
                "total": "71.88",
                "currency": "CHF",
                "saving": 45,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "60.00", "price": "71.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J5JvjJNcmPzuWtR3wwy1dcR",
                "price": "10.99",
                "currency": "CHF",
                "total": None,
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "0", "price": "10.99", "period": "monthly"},
            },
        },
        "it": {  # Italian
            "12-month": {
                "id": "price_1J5JwWJNcmPzuWtRgrx5fjOc",
                "price": "5.99",
                "total": "71.88",
                "currency": "CHF",
                "saving": 45,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "60.00", "price": "71.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J5JxGJNcmPzuWtRrp5e1SUB",
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
                "id": "price_1N7PDwJNcmPzuWtR1IxSkZ0c",
                "price": "119",
                "total": "1428",
                "currency": "CZK",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CZK", "discount": "1416", "price": "1428", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7PESJNcmPzuWtRTgmv8Ve4",
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
                "id": "price_1N7PCQJNcmPzuWtRNqtksScA",
                "price": "37",
                "total": "444",
                "currency": "DKK",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "DKK", "discount": "456", "price": "444", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7PCsJNcmPzuWtRXIMBFQbq",
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
                "id": "price_1N7PGEJNcmPzuWtRzTe85nzw",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7PHRJNcmPzuWtRjZ8D8kwx",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "de": {  # German
            "12-month": {
                "id": "price_1IgwblJNcmPzuWtRynC7dqQa",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1IgwZVJNcmPzuWtRg9Wssh2y",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "el": {  # Greek
            "12-month": {
                "id": "price_1N7PPyJNcmPzuWtRkUbirJmB",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7PQIJNcmPzuWtR2BQdQbtL",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "en": {  # English
            "12-month": {
                "id": "price_1JcdvBJNcmPzuWtROLbEH9d2",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1JcdsSJNcmPzuWtRGF9Y5TMJ",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "es": {  # Spanish
            "12-month": {
                "id": "price_1J5JCdJNcmPzuWtRrvQMFLlP",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J5JDgJNcmPzuWtRqQtIbktk",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "fr": {  # French
            "12-month": {
                "id": "price_1IgnlcJNcmPzuWtRjrNa39W4",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1IgowHJNcmPzuWtRzD7SgAYb",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "hu": {  # Hungarian
            "12-month": {
                "id": "price_1N7PF1JNcmPzuWtRujxNI9yh",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7PFbJNcmPzuWtRlVNtHvgG",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "it": {  # Italian
            "12-month": {
                "id": "price_1J4owvJNcmPzuWtRomVhWQFq",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J5J6iJNcmPzuWtRK5zfoguV",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "nl": {  # Dutch
            "12-month": {
                "id": "price_1J5JRGJNcmPzuWtRXwXA84cm",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J5JSkJNcmPzuWtR54LPH2zi",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "pt": {  # Portuguese
            "12-month": {
                "id": "price_1N7PBOJNcmPzuWtRykt8Uyzm",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7PBsJNcmPzuWtRzS5kTc5B",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "ro": {  # Romanian
            "12-month": {
                "id": "price_1N7PADJNcmPzuWtRxHjlrDiy",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7PAmJNcmPzuWtR1zOoPIao",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "sk": {  # Slovak
            "12-month": {
                "id": "price_1N7PKUJNcmPzuWtRrnyAM0wd",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7PKyJNcmPzuWtROTKgdgW0",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "sl": {  # Slovenian
            "12-month": {
                "id": "price_1N7PMcJNcmPzuWtR8TWsjoHe",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7PN6JNcmPzuWtRpN8HAr7L",
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
                "id": "price_1N7P8TJNcmPzuWtRI7pI29bO",
                "price": "22",
                "total": "264",
                "currency": "PLN",
                "saving": 48,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "PLN", "discount": "276", "price": "264", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7P98JNcmPzuWtRbUaI24OH",
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
                "id": "price_1Iw85dJNcmPzuWtRyhMDdtM7",
                "price": "4.99",
                "total": "59.88",
                "currency": "USD",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "USD", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1Iw7qSJNcmPzuWtRMUZpOwLm",
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

TEST_VPN_RELAY_BUNDLE_PRODUCT_ID = "prod_MIex7Q079igFZJ"

TEST_VPN_RELAY_BUNDLE_PLAN_ID_MATRIX = {
    "usd": {
        "en": {
            "12-month": {"id": "price_1LwoSDJNcmPzuWtR6wPJZeoh", "price": "6.99", "total": "83.88", "currency": "USD", "saving": 50},
        }
    },
}

TEST_VPN_RELAY_BUNDLE_PRICING = {
    "US": {
        "default": TEST_VPN_RELAY_BUNDLE_PLAN_ID_MATRIX["usd"]["en"],
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
        "ach" "br",
        "sco",
        "xh",
    ],
)
def test_vpn_not_supported_locale(locale):
    """Should return False for locales where the VPN client is not localized"""
    assert vpn_supported_locale(locale) is False


@pytest.mark.parametrize("country_code", settings.VPN_COUNTRY_CODES)
def test_available_country_codes(country_code):
    """Should return True for country codes where VPN is available"""
    assert vpn_available_in_country(country_code) is True


@pytest.mark.parametrize("country_code", settings.VPN_EXCLUDED_COUNTRY_CODES)
def test_vpn_excluded_country_codes(country_code):
    """Should return False for country codes where VPN is not available"""
    assert vpn_available_in_country(country_code) is False


@pytest.mark.parametrize("country_code", settings.VPN_BLOCK_DOWNLOAD_COUNTRY_CODES)
def test_vpn_blocked_download_country_codes(country_code):
    """Should return False for country codes where VPN downloads are also blocked"""
    assert vpn_available_in_country(country_code) is False


jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {})


@override_settings(
    FXA_ENDPOINT=TEST_FXA_ENDPOINT,
    VPN_PRODUCT_ID=TEST_VPN_PRODUCT_ID,
    VPN_SUBSCRIPTION_URL=TEST_VPN_SUBSCRIPTION_URL,
    VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING,
    VPN_RELAY_BUNDLE_PRODUCT_ID=TEST_VPN_RELAY_BUNDLE_PRODUCT_ID,
    VPN_RELAY_BUNDLE_PRICING=TEST_VPN_RELAY_BUNDLE_PRICING,
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
        bundle_relay=False,
        optional_parameters=None,
        optional_attributes=None,
    ):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(
            f"""{{{{ vpn_subscribe_link('{entrypoint}', '{link_text}', '{plan}', '{class_name}', '{country_code}',
                                        '{lang}', {bundle_relay}, {optional_parameters}, {optional_attributes}) }}}}""",
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
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
            'class="js-fxa-product-cta-link js-fxa-product-button mzp-c-button ga-begin-checkout" data-cta-text="Get Mozilla VPN yearly" '
            "data-cta-type=\"fxa-vpn\" data-cta-position=\"primary\" data-ga-item=\"{'id' : 'price_1Iw85dJNcmPzuWtRyhMDdtM7','brand' : 'vpn',"
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
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral" data-action="https://accounts.firefox.com/" class="js-fxa-product-cta-link js-fxa-product-button mzp-c-button '
            "ga-begin-checkout\" data-ga-item=\"{'id' : 'price_1Iw85dJNcmPzuWtRyhMDdtM7','brand' : 'vpn','plan' : 'vpn','period' : 'yearly',"
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
            '<a href="https://accounts.firefox.com/subscriptions/products/prod_FvnsFHIfezy3ZI?plan=price_1Iw7qSJNcmPzuWtRMUZpOwLm'
            "&entrypoint=www.mozilla.org-vpn-product-page&form_type=button&service=e6eb0d1e856335fc&utm_source=www.mozilla.org-vpn-product-page"
            '&utm_medium=referral&utm_campaign=vpn-product-page&data_cta_position=primary" data-action="https://accounts.firefox.com/" '
            'class="js-fxa-product-cta-link js-fxa-product-button mzp-c-button ga-begin-checkout" data-cta-text="Get Mozilla VPN monthly" '
            "data-cta-type=\"fxa-vpn\" data-cta-position=\"primary\" data-ga-item=\"{'id' : 'price_1Iw7qSJNcmPzuWtRMUZpOwLm','brand' : 'vpn',"
            "'plan' : 'vpn','period' : 'monthly','price' : '9.99','discount' : '0','currency' : 'USD'}\">Get Mozilla VPN</a>"
        )
        self.assertEqual(markup, expected)

    def test_vpn_relay_bundle_subscribe_link_variable_12_month_us_en(self):
        """Should return expected markup for variable 12-month plan link"""
        markup = self._render(
            plan="12-month",
            country_code="US",
            lang="en-US",
            bundle_relay=True,
        )
        self.assertIn("/prod_MIex7Q079igFZJ?plan=price_1LwoSDJNcmPzuWtR6wPJZeoh", markup)

    def test_vpn_relay_bundle_subscribe_link_variable_12_month_ca_en(self):
        """Should return expected markup for variable 12-month plan link"""
        markup = self._render(
            plan="12-month",
            country_code="CA",
            lang="en-CA",
            bundle_relay=True,
        )
        self.assertIn("/prod_MIex7Q079igFZJ?plan=price_1LwoSDJNcmPzuWtR6wPJZeoh", markup)

    def test_vpn_subscribe_link_variable_12_month_us_en(self):
        """Should contain expected 12-month plan ID (US / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="US",
            lang="en-US",
        )
        self.assertIn("?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7", markup)

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

    def test_vpn_subscribe_link_variable_monthly_nl_nl(self):
        """Should contain expected monthly plan ID (NL / nl)"""
        markup = self._render(
            plan="monthly",
            country_code="NL",
            lang="nl",
        )
        self.assertIn("?plan=price_1J5JSkJNcmPzuWtR54LPH2zi", markup)

    def test_vpn_subscribe_link_variable_12_month_se_en(self):
        """Should contain expected 12-month plan ID (SE / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="SE",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdvBJNcmPzuWtROLbEH9d2", markup)

    def test_vpn_subscribe_link_variable_monthly_se_en(self):
        """Should contain expected monthly plan ID (SE / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="SE",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdsSJNcmPzuWtRGF9Y5TMJ", markup)

    def test_vpn_subscribe_link_variable_12_month_fi_en(self):
        """Should contain expected 12-month plan ID (FI / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="FI",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdvBJNcmPzuWtROLbEH9d2", markup)

    def test_vpn_subscribe_link_variable_monthly_fi_en(self):
        """Should contain expected monthly plan ID (FI / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="FI",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdsSJNcmPzuWtRGF9Y5TMJ", markup)

    def test_vpn_subscribe_link_variable_12_month_bg_en(self):
        """Should contain expected 12-month plan ID (BG / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="BG",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdvBJNcmPzuWtROLbEH9d2", markup)

    def test_vpn_subscribe_link_variable_monthly_bg_en(self):
        """Should contain expected monthly plan ID (BG / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="BG",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdsSJNcmPzuWtRGF9Y5TMJ", markup)

    def test_vpn_subscribe_link_variable_12_month_cy_el(self):
        """Should contain expected 12-month plan ID (CY / el)"""
        markup = self._render(
            plan="12-month",
            country_code="CY",
            lang="el",
        )
        self.assertIn("?plan=price_1N7PPyJNcmPzuWtRkUbirJmB", markup)

    def test_vpn_subscribe_link_variable_monthly_cy_el(self):
        """Should contain expected monthly plan ID (CY / el)"""
        markup = self._render(
            plan="monthly",
            country_code="CY",
            lang="el",
        )
        self.assertIn("?plan=price_1N7PQIJNcmPzuWtR2BQdQbtL", markup)

    def test_vpn_subscribe_link_variable_12_month_cy_en(self):
        """Should contain expected 12-month plan ID (CY / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="CY",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdvBJNcmPzuWtROLbEH9d2", markup)

    def test_vpn_subscribe_link_variable_monthly_cy_en(self):
        """Should contain expected monthly plan ID (CY / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="CY",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdsSJNcmPzuWtRGF9Y5TMJ", markup)

    def test_vpn_subscribe_link_variable_12_month_cz_cs(self):
        """Should contain expected 12-month plan ID (CZ / cs)"""
        markup = self._render(
            plan="12-month",
            country_code="CZ",
            lang="cs",
        )
        self.assertIn("?plan=price_1N7PDwJNcmPzuWtR1IxSkZ0c", markup)

    def test_vpn_subscribe_link_variable_monthly_cz_cs(self):
        """Should contain expected monthly plan ID (CZ / cs)"""
        markup = self._render(
            plan="monthly",
            country_code="CZ",
            lang="cs",
        )
        self.assertIn("?plan=price_1N7PESJNcmPzuWtRTgmv8Ve4", markup)

    def test_vpn_subscribe_link_variable_12_month_dk_da(self):
        """Should contain expected 12-month plan ID (DK / da)"""
        markup = self._render(
            plan="12-month",
            country_code="DK",
            lang="da",
        )
        self.assertIn("?plan=price_1N7PCQJNcmPzuWtRNqtksScA", markup)

    def test_vpn_subscribe_link_variable_monthly_dk_da(self):
        """Should contain expected monthly plan ID (DK / da)"""
        markup = self._render(
            plan="monthly",
            country_code="DK",
            lang="da",
        )
        self.assertIn("?plan=price_1N7PCsJNcmPzuWtRXIMBFQbq", markup)

    def test_vpn_subscribe_link_variable_12_month_hu_hu(self):
        """Should contain expected 12-month plan ID (HU / hu)"""
        markup = self._render(
            plan="12-month",
            country_code="HU",
            lang="hu",
        )
        self.assertIn("?plan=price_1N7PF1JNcmPzuWtRujxNI9yh", markup)

    def test_vpn_subscribe_link_variable_monthly_hu_hu(self):
        """Should contain expected monthly plan ID (HU / hu)"""
        markup = self._render(
            plan="monthly",
            country_code="HU",
            lang="hu",
        )
        self.assertIn("?plan=price_1N7PFbJNcmPzuWtRlVNtHvgG", markup)

    def test_vpn_subscribe_link_variable_12_month_pl_en(self):
        """Should contain expected 12-month plan ID (PL / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="PL",
            lang="en-US",
        )
        self.assertIn("?plan=price_1N7P8TJNcmPzuWtRI7pI29bO", markup)

    def test_vpn_subscribe_link_variable_monthly_pl_en(self):
        """Should contain expected monthly plan ID (PL / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="PL",
            lang="en-US",
        )
        self.assertIn("?plan=price_1N7P98JNcmPzuWtRbUaI24OH", markup)

    def test_vpn_subscribe_link_variable_12_month_ro_en(self):
        """Should contain expected 12-month plan ID (RO / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="RO",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdvBJNcmPzuWtROLbEH9d2", markup)

    def test_vpn_subscribe_link_variable_monthly_ro_en(self):
        """Should contain expected monthly plan ID (RO / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="RO",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdsSJNcmPzuWtRGF9Y5TMJ", markup)

    def test_vpn_subscribe_link_variable_12_month_ee_en(self):
        """Should contain expected 12-month plan ID (EE / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="EE",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdvBJNcmPzuWtROLbEH9d2", markup)

    def test_vpn_subscribe_link_variable_monthly_ee_en(self):
        """Should contain expected monthly plan ID (EE / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="EE",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdsSJNcmPzuWtRGF9Y5TMJ", markup)

    def test_vpn_subscribe_link_variable_12_month_hr_en(self):
        """Should contain expected 12-month plan ID (HR / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="HR",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdvBJNcmPzuWtROLbEH9d2", markup)

    def test_vpn_subscribe_link_variable_monthly_hr_en(self):
        """Should contain expected monthly plan ID (HR / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="HR",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdsSJNcmPzuWtRGF9Y5TMJ", markup)

    def test_vpn_subscribe_link_variable_12_month_lt_en(self):
        """Should contain expected 12-month plan ID (LT / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="LT",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdvBJNcmPzuWtROLbEH9d2", markup)

    def test_vpn_subscribe_link_variable_monthly_lt_en(self):
        """Should contain expected monthly plan ID (LT / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="LT",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdsSJNcmPzuWtRGF9Y5TMJ", markup)

    def test_vpn_subscribe_link_variable_12_month_lv_en(self):
        """Should contain expected 12-month plan ID (LV / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="LV",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdvBJNcmPzuWtROLbEH9d2", markup)

    def test_vpn_subscribe_link_variable_monthly_lv_en(self):
        """Should contain expected monthly plan ID (LV / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="LV",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdsSJNcmPzuWtRGF9Y5TMJ", markup)

    def test_vpn_subscribe_link_variable_12_month_mt_en(self):
        """Should contain expected 12-month plan ID (MT / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="MT",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdvBJNcmPzuWtROLbEH9d2", markup)

    def test_vpn_subscribe_link_variable_monthly_mt_en(self):
        """Should contain expected monthly plan ID (MT / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="MT",
            lang="en-US",
        )
        self.assertIn("?plan=price_1JcdsSJNcmPzuWtRGF9Y5TMJ", markup)

    def test_vpn_subscribe_link_variable_12_month_si_sl(self):
        """Should contain expected 12-month plan ID (SI / sl)"""
        markup = self._render(
            plan="12-month",
            country_code="SI",
            lang="sl",
        )
        self.assertIn("?plan=price_1N7PMcJNcmPzuWtR8TWsjoHe", markup)

    def test_vpn_subscribe_link_variable_monthly_si_sl(self):
        """Should contain expected monthly plan ID (SI / sl)"""
        markup = self._render(
            plan="monthly",
            country_code="SI",
            lang="sl",
        )
        self.assertIn("?plan=price_1N7PN6JNcmPzuWtRpN8HAr7L", markup)

    def test_vpn_subscribe_link_variable_12_month_sk_sk(self):
        """Should contain expected 12-month plan ID (SK / sk)"""
        markup = self._render(
            plan="12-month",
            country_code="SK",
            lang="sk",
        )
        self.assertIn("?plan=price_1N7PKUJNcmPzuWtRrnyAM0wd", markup)

    def test_vpn_subscribe_link_variable_monthly_sk_sk(self):
        """Should contain expected monthly plan ID (SK / sk)"""
        markup = self._render(
            plan="monthly",
            country_code="SK",
            lang="sk",
        )
        self.assertIn("?plan=price_1N7PKyJNcmPzuWtROTKgdgW0", markup)


@override_settings(VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING)
class TestVPNMonthlyPrice(TestCase):
    rf = RequestFactory()

    def _render(self, plan, country_code, lang):
        req = self.rf.get("/")
        req.locale = "en-US"
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


@override_settings(
    VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING,
    VPN_RELAY_BUNDLE_PRICING=TEST_VPN_RELAY_BUNDLE_PRICING,
)
class TestVPNTotalPrice(TestCase):
    rf = RequestFactory()

    def _render(self, country_code, lang, bundle_relay=False):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(f"{{{{ vpn_total_price('{country_code}', '{lang}', {bundle_relay}) }}}}", {"request": req})

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

    def test_vpn_relay_bundle_12_month_total_price_usd_en_us(self):
        """Should return expected markup"""
        markup = self._render(country_code="US", lang="en-US", bundle_relay=True)
        expected = "$83.88 total + tax"
        self.assertEqual(markup, expected)

    def test_vpn_relay_bundle_12_month_total_price_usd_en_ca(self):
        """Should return expected markup"""
        markup = self._render(country_code="CA", lang="en-CA", bundle_relay=True)
        expected = "US$83.88 total + tax"
        self.assertEqual(markup, expected)

    def test_vpn_12_month_total_price_unknown_locale(self):
        """Should return expected markup"""
        markup = self._render(country_code="US", lang="ach")
        expected = "$59.88 total + tax"
        self.assertEqual(markup, expected)


@override_settings(
    VPN_VARIABLE_PRICING=TEST_VPN_VARIABLE_PRICING,
    VPN_RELAY_BUNDLE_PRICING=TEST_VPN_RELAY_BUNDLE_PRICING,
)
class TestVPNSaving(TestCase):
    rf = RequestFactory()

    def _render(self, country_code, lang, bundle_relay=False):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(f"{{{{ vpn_saving('{country_code}', '{lang}', {bundle_relay}) }}}}", {"request": req})

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

    def test_vpn_relay_bundle_12_month_saving_usd(self):
        """Should return expected markup"""
        markup = self._render(country_code="US", lang="en-US", bundle_relay=True)
        expected = "Save 50%"
        self.assertEqual(markup, expected)

    def test_vpn_relay_bundle_12_month_saving_ca(self):
        """Should return expected markup"""
        markup = self._render(country_code="CA", lang="en-US", bundle_relay=True)
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
        class_name=None,
        optional_attributes=None,
        optional_parameters=None,
    ):
        with self.activate("en-US"):
            req = self.rf.get("/")
            req.locale = "en-US"

            return render(
                f"""{{{{ vpn_product_referral_link('{referral_id}', {link_to_pricing_page}, '{page_anchor}',
                                                   '{link_text}', '{class_name}', {optional_attributes}, {optional_parameters}) }}}}""",
                {"request": req},
            )

    def test_vpn_product_referral_link(self):
        """Should return expected markup"""
        markup = self._render(
            referral_id="navigation",
            page_anchor="#pricing",
            link_text="Get Mozilla VPN",
            class_name="mzp-t-product mzp-t-secondary mzp-t-md",
            optional_attributes={"data-cta-text": "Get Mozilla VPN", "data-cta-type": "button"},
        )
        expected = (
            '<a href="/en-US/products/vpn/#pricing" class="mzp-c-button js-fxa-product-referral-link '
            'mzp-t-product mzp-t-secondary mzp-t-md" data-referral-id="navigation" '
            'data-cta-text="Get Mozilla VPN" data-cta-type="button">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_product_referral_link_pricing_page(self):
        """Should return expected markup when linking to pricing page"""
        markup = self._render(
            referral_id="navigation",
            link_to_pricing_page=True,
            link_text="Get Mozilla VPN",
            class_name="mzp-t-product mzp-t-secondary mzp-t-md",
            optional_attributes={"data-cta-text": "Get Mozilla VPN", "data-cta-type": "button"},
        )
        expected = (
            '<a href="/en-US/products/vpn/pricing/" class="mzp-c-button js-fxa-product-referral-link '
            'mzp-t-product mzp-t-secondary mzp-t-md" data-referral-id="navigation" '
            'data-cta-text="Get Mozilla VPN" data-cta-type="button">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)

    def test_vpn_product_referral_link_optional_params(self):
        """Should return expected markup when adding optional parameters"""
        markup = self._render(
            referral_id="navigation",
            link_to_pricing_page=True,
            link_text="Get Mozilla VPN",
            class_name="mzp-t-product mzp-t-secondary mzp-t-md",
            optional_attributes={"data-cta-text": "Get Mozilla VPN", "data-cta-type": "button"},
            optional_parameters={"coupon": "cyber20"},
        )
        expected = (
            '<a href="/en-US/products/vpn/pricing/?coupon=cyber20" class="mzp-c-button js-fxa-product-referral-link '
            'mzp-t-product mzp-t-secondary mzp-t-md" data-referral-id="navigation" '
            'data-cta-text="Get Mozilla VPN" data-cta-type="button">Get Mozilla VPN</a>'
        )
        self.assertEqual(markup, expected)
