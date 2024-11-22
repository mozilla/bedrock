# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
import wagtail_factories
from wagtail.contrib.redirects.models import Redirect
from wagtail.models import Locale, Site

from bedrock.cms.tests.factories import LocaleFactory, SimpleRichTextPageFactory


@pytest.fixture
def minimal_site(
    client,
    top_level_page=None,
):
    # Bootstraps a minimal site with a root page at / and one child page at /test-page/

    if top_level_page is None:
        top_level_page = SimpleRichTextPageFactory(
            slug="root_page",  # this doesn't get shown
            live=True,
        )

    try:
        site = Site.objects.get(is_default_site=True)
        site.root_page = top_level_page
        site.hostname = client._base_environ()["SERVER_NAME"]
        site.save()
    except Site.DoesNotExist:
        site = wagtail_factories.SiteFactory(
            root_page=top_level_page,
            is_default_site=True,
            hostname=client._base_environ()["SERVER_NAME"],
        )

    LocaleFactory(language_code="fr")

    SimpleRichTextPageFactory(
        slug="test-page",
        parent=top_level_page,
        title="Test Page",
    )

    return site


@pytest.fixture
def tiny_localized_site():
    """
    Generates a small site tree with some pages in other languages:

    en-US:
        / [Page]
            /test-page [SimpleRichTextPage]
                /child-page [SimpleRichTextPage]
    fr:
        / [Page]
            /test-page [SimpleRichTextPage]
                /child-page [SimpleRichTextPage]
                    /grandchild-page [SimpleRichTextPage] <- no parallel page
    pt-BR:
        / [Page]
            /test-page [SimpleRichTextPage]
                /child-page [SimpleRichTextPage]

    Note: no aliases exist
    """

    en_us_locale = Locale.objects.get(language_code="en-US")
    fr_locale = LocaleFactory(language_code="fr")
    pt_br_locale = LocaleFactory(language_code="pt-BR")

    site = Site.objects.get(is_default_site=True)

    en_us_root_page = site.root_page

    fr_root_page = en_us_root_page.copy_for_translation(fr_locale)
    rev = fr_root_page.save_revision()
    fr_root_page.publish(rev)

    pt_br_root_page = en_us_root_page.copy_for_translation(pt_br_locale)
    rev = pt_br_root_page.save_revision()
    pt_br_root_page.publish(rev)

    en_us_homepage = SimpleRichTextPageFactory(
        title="Test Page",
        slug="test-page",
        parent=en_us_root_page,
    )

    en_us_child = SimpleRichTextPageFactory(
        title="Child",
        slug="child-page",
        parent=en_us_homepage,
    )

    fr_homepage = en_us_homepage.copy_for_translation(fr_locale)
    fr_homepage.title = "Page de Test"
    fr_homepage.save()
    rev = fr_homepage.save_revision()
    fr_homepage.publish(rev)

    fr_child = en_us_child.copy_for_translation(fr_locale)
    fr_child.title = "Enfant"
    fr_child.save()
    rev = fr_child.save_revision()
    fr_child.publish(rev)

    # WARNING: there may be a bug with the page tree here
    # fr_grandchild cannot be found with Page.find_for_request
    # when all the others can. TODO: debug this, but manually
    # it works
    fr_grandchild = SimpleRichTextPageFactory(
        title="Petit-enfant",
        slug="grandchild-page",
        locale=fr_locale,
        parent=fr_child,
    )

    pt_br_homepage = en_us_homepage.copy_for_translation(pt_br_locale)
    pt_br_homepage.title = "Página de Teste"
    pt_br_homepage.save()
    rev = pt_br_homepage.save_revision()
    pt_br_homepage.publish(rev)

    pt_br_child = fr_child.copy_for_translation(pt_br_locale)
    pt_br_child.title = "Página Filho"
    pt_br_child.save()
    rev = pt_br_child.save_revision()
    pt_br_child.publish(rev)

    assert en_us_root_page.locale == en_us_locale
    assert pt_br_root_page.locale == pt_br_locale
    assert fr_root_page.locale == fr_locale

    assert en_us_homepage.locale == en_us_locale
    assert en_us_child.locale == en_us_locale

    assert fr_homepage.locale == fr_locale
    assert fr_child.locale == fr_locale
    assert fr_grandchild.locale == fr_locale

    assert pt_br_homepage.locale == pt_br_locale
    assert pt_br_child.locale == pt_br_locale

    for page in (en_us_homepage, en_us_child, pt_br_homepage, pt_br_child, fr_homepage, fr_child, fr_grandchild):
        page.refresh_from_db()

    assert en_us_homepage.live is True
    assert en_us_child.live is True
    assert pt_br_homepage.live is True
    assert pt_br_child.live is True
    assert fr_homepage.live is True
    assert fr_child.live is True
    assert fr_grandchild.live is True


@pytest.fixture
def tiny_localized_site_redirects():
    """Some test redirects that complement the tiny_localized_site fixture.

    Useful for things like the tests for the cache-based lookup
    in bedrock.cms.tests.test_utils.test_path_exists_in_cms
    """

    Redirect.add_redirect(
        old_path="/fr/moved-page/",
        redirect_to="/fr/test-page/child-page/",
    )
    Redirect.add_redirect(
        old_path="/en-US/deeper/nested/moved-page/",
        redirect_to="/fr/test-page/",
    )
