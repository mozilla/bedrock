# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from django.test import override_settings
from django.urls import path

import pytest
from wagtail.models import Site
from wagtail.rich_text import RichText

from bedrock.base.i18n import bedrock_i18n_patterns
from bedrock.cms.decorators import prefer_cms
from bedrock.cms.tests import decorator_test_views
from bedrock.urls import urlpatterns as mozorg_urlpatterns

from .factories import LocaleFactory, SimpleRichTextPageFactory

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
            "decorated/view/path/with/locale/strings/",
            decorator_test_views.decorated_dummy_view_with_locale_strings,
            name="decorated_dummy_view_with_locale_strings",
        ),
        path(
            "decorated/view/path/with/fluent/files/",
            decorator_test_views.decorated_dummy_view_with_fluent_files,
            name="decorated_dummy_view_with_fluent_files",
        ),
        path(
            "decorated/view/path/with/a/callable/taking/<slug:a_slug>/",
            decorator_test_views.decorated_dummy_view_for_use_with_a_callable,
            name="decorated_dummy_view_for_use_with_a_callable",
        ),
        path(
            "wrapped/view/path/",
            prefer_cms(
                decorator_test_views.wrapped_dummy_view,
            ),
            name="url_wrapped_dummy_view",
        ),
        path(
            "wrapped/view/path/with/fluent/files/",
            prefer_cms(
                decorator_test_views.wrapped_dummy_view,
                fallback_ftl_files=["test/fluent1", "test/fluent2"],
            ),
            name="url_wrapped_dummy_view",
        ),
        path(
            "wrapped/view/path/with/locale/strings/",
            prefer_cms(
                decorator_test_views.wrapped_dummy_view,
                fallback_lang_codes=["fr-CA", "es-ES", "sco"],
            ),
            name="url_wrapped_dummy_view",
        ),
        path(
            "wrapped/view/path/with/a/callable/taking/<slug:a_slug>/",
            prefer_cms(
                decorator_test_views.wrapped_dummy_view,
                fallback_callable=decorator_test_views.test_callable_to_get_locales,
            ),
            name="url_wrapped_dummy_view",
        ),
        path(
            "prefer-cms-alias-test/",
            prefer_cms(
                decorator_test_views.wrapped_dummy_view,
                fallback_lang_codes=["es-AR", "es-ES", "en-US"],
            ),
            name="prefer_cms_alias_test",
        ),
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
    assert resp.text == "This is a dummy response from the undecorated view"

    # Show decorated view renders Django view initially, because there is no CMS page at that route yet
    resp = client.get("/decorated/view/path/", follow=True)
    assert resp.status_code == 200
    assert resp.text == "This is a dummy response from the decorated view"

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/decorated/view/path/",
        site=minimal_site,
    )

    resp = client.get(f"{lang_code_prefix}/decorated/view/path/", follow=True)
    assert resp.status_code == 200
    assert "This is a CMS page now, with the slug of path" in resp.text


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_decorating_django_view__passing_fallback_lang_codes(
    lang_code_prefix,
    minimal_site,
    client,
):
    resp = client.get(
        "/decorated/view/path/with/locale/strings/",
        follow=True,
    )
    assert resp.status_code == 200
    assert resp.text == "This is a dummy response from the decorated view with locale strings passed in"
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["fr-CA", "es-ES", "sco"]
    assert resp.wsgi_request._locales_available_via_cms == []  # No page in CMS yet

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/decorated/view/path/with/locale/strings/",
        site=minimal_site,
    )

    resp = client.get(f"{lang_code_prefix}/decorated/view/path/with/locale/strings/", follow=True)
    assert resp.status_code == 200
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["fr-CA", "es-ES", "sco"]
    assert resp.wsgi_request._locales_available_via_cms == ["en-US", "en-GB", "en-CA"]
    assert "This is a CMS page now, with the slug of strings" in resp.text


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_decorating_django_view__passing_callable_for_locales(
    lang_code_prefix,
    minimal_site,
    client,
):
    resp = client.get(
        "/decorated/view/path/with/a/callable/taking/a-slug-here/",
        follow=True,
    )
    assert resp.status_code == 200
    assert resp.text == "This is a dummy response from the decorated view for the callable, taking () and {'a_slug': 'a-slug-here'}"
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["sco", "es-ES"]
    assert resp.wsgi_request._locales_available_via_cms == []  # No page in CMS yet

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/decorated/view/path/with/a/callable/taking/a-slug-here/",
        site=minimal_site,
    )

    resp = client.get(f"{lang_code_prefix}/decorated/view/path/with/a/callable/taking/a-slug-here/", follow=True)
    assert resp.status_code == 200
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["sco", "es-ES"]
    assert resp.wsgi_request._locales_available_via_cms == ["en-US", "en-GB", "en-CA"]
    assert "This is a CMS page now, with the slug of a-slug-here" in resp.text


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_decorating_django_view__passing_ftl_files(lang_code_prefix, minimal_site, client, mocker):
    mock_get_active_locales = mocker.patch("bedrock.cms.decorators.get_active_locales")
    mock_get_active_locales.return_value = ["sco", "es-ES", "fr-CA"]

    assert not mock_get_active_locales.called
    resp = client.get(
        "/decorated/view/path/with/fluent/files/",
        follow=True,
    )
    assert resp.status_code == 200
    assert resp.text == "This is a dummy response from the decorated view with fluent files explicitly passed in"
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["sco", "es-ES", "fr-CA"]
    mock_get_active_locales.assert_called_once_with(
        ["test/fluentA", "test/fluentB"],
        force=True,
    )

    assert resp.wsgi_request._locales_available_via_cms == []  # No page in CMS yet

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/decorated/view/path/with/fluent/files/",
        site=minimal_site,
    )

    mock_get_active_locales.reset_mock()

    resp = client.get(f"{lang_code_prefix}/decorated/view/path/with/fluent/files/", follow=True)
    assert resp.status_code == 200
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["sco", "es-ES", "fr-CA"]
    mock_get_active_locales.assert_called_once_with(
        ["test/fluentA", "test/fluentB"],
        force=True,
    )
    assert resp.wsgi_request._locales_available_via_cms == ["en-US", "en-GB", "en-CA"]
    assert "This is a CMS page now, with the slug of files" in resp.text


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_patching_in_urlconf__standard_django_view(lang_code_prefix, minimal_site, client):
    # Show wrapped view renders Django view initially,
    # because there is no CMS page at that route yet
    resp = client.get(f"{lang_code_prefix}/wrapped/view/path/", follow=True)
    assert resp.status_code == 200
    assert resp.text == "This is a dummy response from the wrapped view"

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/wrapped/view/path/",
        site=minimal_site,
    )

    resp = client.get(f"{lang_code_prefix}/wrapped/view/path/", follow=True)
    assert resp.status_code == 200
    assert "This is a CMS page now, with the slug of path" in resp.text


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_patching_in_urlconf__standard_django_view__with_locale_list(
    lang_code_prefix,
    minimal_site,
    client,
):
    resp = client.get(
        "/wrapped/view/path/with/locale/strings/",
        follow=True,
    )
    assert resp.status_code == 200
    assert resp.text == "This is a dummy response from the wrapped view"
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["fr-CA", "es-ES", "sco"]
    assert resp.wsgi_request._locales_available_via_cms == []  # No page in CMS yet

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/wrapped/view/path/with/locale/strings/",
        site=minimal_site,
    )

    resp = client.get(f"{lang_code_prefix}/wrapped/view/path/with/locale/strings/", follow=True)
    assert resp.status_code == 200
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["fr-CA", "es-ES", "sco"]
    assert resp.wsgi_request._locales_available_via_cms == ["en-US", "en-GB", "en-CA"]
    assert "This is a CMS page now, with the slug of strings" in resp.text


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_patching_in_urlconf__standard_django_view__with_callback_for_locales(
    lang_code_prefix,
    minimal_site,
    client,
):
    resp = client.get(
        "/wrapped/view/path/with/a/callable/taking/a-slug-here/",
        follow=True,
    )
    assert resp.status_code == 200
    assert resp.text == "This is a dummy response from the wrapped view"
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["sco", "es-ES"]
    assert resp.wsgi_request._locales_available_via_cms == []  # No page in CMS yet

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/wrapped/view/path/with/a/callable/taking/a-slug-here/",
        site=minimal_site,
    )

    resp = client.get(f"{lang_code_prefix}/wrapped/view/path/with/a/callable/taking/a-slug-here/", follow=True)
    assert resp.status_code == 200
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["sco", "es-ES"]
    assert resp.wsgi_request._locales_available_via_cms == ["en-US", "en-GB", "en-CA"]
    assert "This is a CMS page now, with the slug of a-slug-here" in resp.text


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_patching_in_urlconf__standard_django_view__with_fluent_files(
    lang_code_prefix,
    minimal_site,
    client,
    mocker,
):
    mock_get_active_locales = mocker.patch("bedrock.cms.decorators.get_active_locales")
    mock_get_active_locales.return_value = ["sco", "es-ES", "fr-CA"]

    assert not mock_get_active_locales.called

    resp = client.get(
        "/wrapped/view/path/with/fluent/files/",
        follow=True,
    )
    assert resp.status_code == 200
    assert resp.text == "This is a dummy response from the wrapped view"

    mock_get_active_locales.assert_called_once_with(
        ["test/fluent1", "test/fluent2"],
        force=True,
    )
    assert resp.wsgi_request._locales_for_django_fallback_view == ["sco", "es-ES", "fr-CA"]
    assert resp.wsgi_request._locales_available_via_cms == []  # No page in CMS yet

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/wrapped/view/path/with/fluent/files/",
        site=minimal_site,
    )

    mock_get_active_locales.reset_mock()

    resp = client.get(f"{lang_code_prefix}/wrapped/view/path/with/fluent/files/", follow=True)
    assert resp.status_code == 200
    mock_get_active_locales.assert_called_once_with(
        ["test/fluent1", "test/fluent2"],
        force=True,
    )

    assert resp.wsgi_request._locales_for_django_fallback_view == ["sco", "es-ES", "fr-CA"]
    assert resp.wsgi_request._locales_available_via_cms == ["en-US", "en-GB", "en-CA"]
    assert "This is a CMS page now, with the slug of files" in resp.text


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("lang_code_prefix", ("", "/en-US"))
def test_draft_pages_do_not_get_preferred_over_django_views(lang_code_prefix, minimal_site, client):
    # Show decorated view renders Django view initially, because there is no CMS page at that route yet
    resp = client.get("/decorated/view/path/", follow=True)
    assert resp.status_code == 200
    assert resp.text == "This is a dummy response from the decorated view"

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    leaf_page = _set_up_cms_pages(
        deepest_path="/decorated/view/path/",
        site=minimal_site,
    )
    assert leaf_page.live is True
    resp = client.get(f"{lang_code_prefix}/decorated/view/path/", follow=True)
    assert resp.status_code == 200
    assert "This is a CMS page now, with the slug of path" in resp.text

    # Show how unpublishing will give us the Django view's content, because there is no
    # live CMS page to "prefer"
    leaf_page.unpublish()
    resp = client.get("/decorated/view/path/", follow=True)
    assert resp.status_code == 200
    assert resp.text == "This is a dummy response from the decorated view"


def _fake_callable():
    pass


@pytest.mark.parametrize(
    "config, expect_exeption",
    (
        (
            {
                "fallback_ftl_files": ["test/files"],
                "fallback_lang_codes": ["sco", "en-CA"],
            },
            True,
        ),
        (
            {
                "fallback_ftl_files": ["test/files"],
                "fallback_callable": _fake_callable,
            },
            True,
        ),
        (
            {
                "fallback_lang_codes": ["sco", "en-CA"],
                "fallback_callable": _fake_callable,
            },
            True,
        ),
        (
            {
                "fallback_ftl_files": ["test/files"],
                "fallback_lang_codes": ["sco", "en-CA"],
                "fallback_callable": _fake_callable,
            },
            True,
        ),
        (
            {
                "fallback_ftl_files": ["test/files"],
            },
            False,
        ),
        (
            {
                "fallback_lang_codes": ["sco", "en-CA"],
            },
            False,
        ),
        (
            {
                "fallback_callable": _fake_callable,
            },
            False,
        ),
    ),
)
def test_prefer_cms_rejects_invalid_setup(mocker, config, expect_exeption):
    fake_view = mocker.Mock(name="fake view")

    if expect_exeption:
        with pytest.raises(RuntimeError):
            prefer_cms(view_func=fake_view, **config)
    else:
        prefer_cms(view_func=fake_view, **config)


@pytest.fixture()
def prefer_cms_alias_site(tiny_localized_site):
    """Site with a CMS page at /prefer-cms-alias-test/ in en-US, with es-ES locale available.

    Uses tiny_localized_site (not minimal_site) because its root page is at depth 2 with a
    proper parent, which is required for copy_for_translation to succeed.
    """
    site = Site.objects.get(is_default_site=True)
    es_es_locale = LocaleFactory(language_code="es-ES")
    # Translate the site root so child pages can be translated without copy_parents=True.
    site.root_page.copy_for_translation(es_es_locale)

    en_us_page = SimpleRichTextPageFactory(
        slug="prefer-cms-alias-test",
        parent=site.root_page,
        content=RichText("CMS page content"),
    )
    en_us_page.save_revision()
    en_us_page.publish(en_us_page.latest_revision)

    return {"site": site, "es_es_locale": es_es_locale, "en_us_page": en_us_page}


@pytest.mark.urls(__name__)
@override_settings(FALLBACK_LOCALES={"es-AR": "es-ES"})
def test_prefer_cms_serves_alias_fallback_cms_page(prefer_cms_alias_site, client):
    """
    prefer_cms serves the CMS's fallback page for an alias locale, rather than the static es-AR page.

    This test verifies the following scenario:
        - a static page exists in an alias locale (es-AR)
        - a CMS page does NOT exist in an alias locale (es-AR)
        - a CMS page does exist in the fallback locale (es-ES)
    In this case, the user should get the CMS's es-ES page at the es-AR URL.
    """
    en_us_page = prefer_cms_alias_site["en_us_page"]
    es_es_locale = prefer_cms_alias_site["es_es_locale"]

    es_es_page = en_us_page.copy_for_translation(es_es_locale)
    es_es_page.content = RichText("ES-ES CMS page content")
    es_es_page.save()
    es_es_page.save_revision()
    es_es_page.publish(es_es_page.latest_revision)

    response = client.get("/es-AR/prefer-cms-alias-test/")

    assert response.status_code == 200
    # The es-ES CMS page was served
    assert "ES-ES CMS page content" in response.text
    assert "dummy response from the wrapped view" not in response.text  # Django view was NOT reached
    assert set(response.wsgi_request._locales_available_via_cms) == {"es-ES", "en-US", "es-AR"}


@pytest.mark.urls(__name__)
@override_settings(FALLBACK_LOCALES={"es-AR": "es-ES"})
def test_prefer_cms_serves_direct_cms_page_for_alias_locale(prefer_cms_alias_site, client):
    """
    When a CMS page exists in an alias locale, prefer_cms serves it, rather than the static alias locale page.

    This test verifies the following scenario:
        - a static page exists in an alias locale (es-AR)
        - a CMS page does exist in an alias locale (es-AR)
        - a CMS page does exist in a fallback locale (es-ES)
    In this case, the user should get the CMS's es-AR page at the es-AR URL.
    """
    en_us_page = prefer_cms_alias_site["en_us_page"]
    es_es_locale = prefer_cms_alias_site["es_es_locale"]

    # es-ES page must exist for the locale chain to be valid
    es_es_page = en_us_page.copy_for_translation(es_es_locale)
    es_es_page.content = RichText("ES-ES CMS page content")
    es_es_page.save()
    es_es_page.save_revision()
    es_es_page.publish(es_es_page.latest_revision)

    # es-AR also has its own promoted page; the root must be live so
    # _alias_needs_prewagtail_intercept returns False and Wagtail serves es-AR directly.
    es_ar_locale = LocaleFactory(language_code="es-AR")
    es_ar_root = prefer_cms_alias_site["site"].root_page.copy_for_translation(es_ar_locale)
    es_ar_root.live = True
    es_ar_root.save()
    es_ar_page = en_us_page.copy_for_translation(es_ar_locale)
    es_ar_page.content = RichText("ES-AR CMS page content")
    es_ar_page.save()
    es_ar_page.save_revision()
    es_ar_page.publish(es_ar_page.latest_revision)

    response = client.get("/es-AR/prefer-cms-alias-test/")

    assert response.status_code == 200
    # The es-AR CMS page was served
    assert "ES-AR CMS page content" in response.text
    assert "dummy response from the wrapped view" not in response.text
    assert set(response.wsgi_request._locales_available_via_cms) == {"es-ES", "en-US", "es-AR"}


@pytest.mark.urls(__name__)
@override_settings(FALLBACK_LOCALES={"es-AR": "es-ES"})
def test_prefer_cms_falls_through_to_django_when_no_alias_cms_page(prefer_cms_alias_site, client):
    """
    prefer_cms falls through to the Django view when CMS has no page for es-AR or es-ES.

    This test verifies the following scenario:
        - a static page exists in an alias locale (es-AR)
        - a CMS page does NOT exist in an alias locale (es-AR)
        - a CMS page does NOT exist in a fallback locale (es-ES)
        - a CMS page does exist in the default locale (en-US)
    In this case, the user should get the static es-AR page at the es-AR URL.
    """
    # prefer_cms_alias_site has an en-US CMS page only — no es-ES or es-AR translations.
    response = client.get("/es-AR/prefer-cms-alias-test/")
    assert response.status_code == 200
    assert "dummy response from the wrapped view" in response.text  # Django view served
    assert "CMS page content" not in response.text
