# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import path

import pytest
from wagtail.rich_text import RichText

from bedrock.base.i18n import bedrock_i18n_patterns
from bedrock.cms.decorators import prefer_cms
from bedrock.cms.tests import decorator_test_views
from bedrock.mozorg.util import page
from bedrock.urls.mozorg_mode import urlpatterns as mozorg_urlpatterns

from .factories import SimpleRichTextPageFactory

urlpatterns = (
    bedrock_i18n_patterns(
        path(
            "undecorated/view/path/",
            decorator_test_views.undecorated_dummy_view,
            name="undecorated_dummy_view",
        ),
        path(
            "decorated/view/path/",
            decorator_test_views.decorated_dummy_view,
            name="decorated_dummy_view",
        ),
        path(
            "wrapped/view/path/",
            prefer_cms(
                decorator_test_views.wrapped_dummy_view,
            ),
            name="url_wrapped_dummy_view",
        ),
        page("book/", "mozorg/book.html", decorators=[prefer_cms]),
    )
    + mozorg_urlpatterns  # we need to extend these so Jinja2 can call url() in the templates
)

pytestmark = [pytest.mark.django_db]


def _set_up_cms_pages(deepest_path, site):
    parent_page = site.root_page

    for slug in deepest_path.lstrip("/").rstrip("/").split("/"):
        new_page = SimpleRichTextPageFactory(
            slug=slug,
            parent=parent_page,
            content=RichText(f"This is a CMS page now, with the slug of {slug}"),
        )
        new_page.save_revision()
        new_page.publish(new_page.latest_revision)

        parent_page = new_page

    assert new_page.relative_url(site) == f"/en-US{deepest_path}"

    return new_page


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_decorating_django_view(lang_code_prefix, minimal_site, client):
    # Control case: undecorated view
    resp = client.get(f"{lang_code_prefix}/undecorated/view/path/", follow=True)
    assert resp.status_code == 200
    assert resp.content.decode("utf-8") == "This is a dummy response from the undecorated view"

    # Show decorated view renders Django view initially, because there is no CMS page at that route yet
    resp = client.get("/decorated/view/path/", follow=True)
    assert resp.status_code == 200
    assert resp.content.decode("utf-8") == "This is a dummy response from the decorated view"

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/decorated/view/path/",
        site=minimal_site,
    )

    resp = client.get(f"{lang_code_prefix}/decorated/view/path/", follow=True)
    assert resp.status_code == 200
    assert "This is a CMS page now, with the slug of path" in resp.content.decode("utf-8")


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_patching_in_urlconf__standard_django_view(lang_code_prefix, minimal_site, client):
    # Show wrapped view renders Django view initially,
    # because there is no CMS page at that route yet
    resp = client.get(f"{lang_code_prefix}/wrapped/view/path/", follow=True)
    assert resp.status_code == 200
    assert resp.content.decode("utf-8") == "This is a dummy response from the wrapped view"

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/wrapped/view/path/",
        site=minimal_site,
    )

    resp = client.get(f"{lang_code_prefix}/wrapped/view/path/", follow=True)
    assert resp.status_code == 200
    assert "This is a CMS page now, with the slug of path" in resp.content.decode("utf-8")


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_support_with_bedrock_page_view(lang_code_prefix, minimal_site, client):
    # Show decorated page() view renders Django view initially, because there is no CMS page at that route yet
    resp = client.get(f"{lang_code_prefix}/book/", follow=True)
    assert resp.status_code == 200
    assert "The Book of Mozilla" in resp.content.decode("utf-8")

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/book/",
        site=minimal_site,
    )

    resp = client.get(f"{lang_code_prefix}/book/", follow=True)
    assert resp.status_code == 200
    assert "This is a CMS page now, with the slug of book" in resp.content.decode("utf-8")


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_draft_pages_do_not_get_preferred_over_django_views(lang_code_prefix, minimal_site, client):
    # Show decorated view renders Django view initially, because there is no CMS page at that route yet
    resp = client.get("/decorated/view/path/", follow=True)
    assert resp.status_code == 200
    assert resp.content.decode("utf-8") == "This is a dummy response from the decorated view"

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    leaf_page = _set_up_cms_pages(
        deepest_path="/decorated/view/path/",
        site=minimal_site,
    )
    assert leaf_page.live is True
    resp = client.get(f"{lang_code_prefix}/decorated/view/path/", follow=True)
    assert resp.status_code == 200
    assert "This is a CMS page now, with the slug of path" in resp.content.decode("utf-8")

    # Show how unpublishing will give us the Django view's content, because there is no
    # live CMS page to "prefer"
    leaf_page.unpublish()
    resp = client.get("/decorated/view/path/", follow=True)
    assert resp.status_code == 200
    assert resp.content.decode("utf-8") == "This is a dummy response from the decorated view"
