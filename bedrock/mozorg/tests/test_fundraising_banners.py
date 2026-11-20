# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.utils import translation

import pytest
from bs4 import BeautifulSoup
from waffle.testutils import override_switch

from bedrock.cms.tests.conftest import minimal_site  # noqa: F401
from bedrock.mozorg.tests import factories

pytestmark = [pytest.mark.django_db]

GIVING_TUESDAY_SWITCH = "FUNDRAISING_BANNER_2026EOY_GIVING_TUESDAY"
FINAL_STRETCH_SWITCH = "FUNDRAISING_BANNER_2026EOY_FINAL_STRETCH"
PENCIL_SWITCH = "SHOW_PENCIL_BANNER"


def render_homepage(site, rf, giving_tuesday=False, final_stretch=False, pencil=False, language="en-US"):
    page = factories.HomePageFactory(parent=site.root_page)
    with (
        override_switch(GIVING_TUESDAY_SWITCH, active=giving_tuesday),
        override_switch(FINAL_STRETCH_SWITCH, active=final_stretch),
        override_switch(PENCIL_SWITCH, active=pencil),
        translation.override(language),
    ):
        resp = page.serve(rf.get(page.relative_url(site)))
    assert resp.status_code == 200
    return BeautifulSoup(resp.text, "html.parser")


def test_giving_tuesday_banner_shows_and_hides_pencil(minimal_site, rf):  # noqa: F811
    soup = render_homepage(minimal_site, rf, giving_tuesday=True, pencil=True)

    banner = soup.select_one(".c-banner-fundraising")
    assert banner["id"] == "fundraising-banner-eoy2026-giving-tuesday"
    button = banner.select_one(".c-banner-button")
    assert button["href"] == "https://www.mozillafoundation.org/?form=26-eoy-org-gt"
    # The heart is added by CSS, so the copy must not include one.
    assert button.get_text(strip=True) == "Donate"
    assert soup.select_one(".m24-pencil-banner") is None


def test_final_stretch_banner(minimal_site, rf):  # noqa: F811
    soup = render_homepage(minimal_site, rf, final_stretch=True)

    banner = soup.select_one(".c-banner-fundraising")
    assert banner["id"] == "fundraising-banner-eoy2026-final-stretch"
    assert banner.select_one(".c-banner-button")["href"] == "https://www.mozillafoundation.org/?form=26-eoy-org-fs"


def test_final_stretch_wins_when_both_large_switches_are_on(minimal_site, rf):  # noqa: F811
    soup = render_homepage(minimal_site, rf, giving_tuesday=True, final_stretch=True)

    assert soup.select_one(".c-banner-fundraising")["id"] == "fundraising-banner-eoy2026-final-stretch"


def test_pencil_banner_shows_on_cms_homepage(minimal_site, rf):  # noqa: F811
    soup = render_homepage(minimal_site, rf, pencil=True)

    assert soup.select_one(".c-banner-fundraising") is None
    pencil = soup.select_one(".m24-pencil-banner")
    assert pencil is not None
    assert pencil.select_one("a")["href"] == "https://www.mozillafoundation.org/?form=26-eoy-org-gen"


@pytest.mark.parametrize(
    "language, tagline",
    [
        ("es-ES", "Apoya una tecnología mejor. Ayúdanos a alcanzar nuestro objetivo antes del 31 de diciembre."),
        ("es-AR", "Apoya a tecnología mejor. Ayúdanos a alcanzar nuestra meta antes del 31 de diciembre."),
        ("nl", "Steun betere tech. Help ons uiterlijk 31 december ons doel te bereiken."),
        ("pt-BR", "Apoie um futuro tecnológico melhor e ajude a bater nossa meta até 31 de dezembro."),
    ],
)
def test_final_stretch_banner_uses_locale_copy(minimal_site, rf, language, tagline):  # noqa: F811
    soup = render_homepage(minimal_site, rf, final_stretch=True, language=language)

    assert soup.select_one(".c-banner-tagline").get_text(strip=True) == tagline


@pytest.mark.parametrize("language", ["it", "pl", "pt-PT"])
def test_no_banners_in_locales_without_copy(minimal_site, rf, language):  # noqa: F811
    soup = render_homepage(minimal_site, rf, final_stretch=True, pencil=True, language=language)

    assert soup.select_one(".c-banner-fundraising") is None
    assert soup.select_one(".m24-pencil-banner") is None


def test_no_banners_when_switches_off(minimal_site, rf):  # noqa: F811
    soup = render_homepage(minimal_site, rf)

    assert soup.select_one(".c-banner-fundraising") is None
    assert soup.select_one(".m24-pencil-banner") is None
