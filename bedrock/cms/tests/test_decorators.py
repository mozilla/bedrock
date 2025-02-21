# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from django.http import Http404, HttpResponse
from django.urls import path

import pytest
from wagtail.rich_text import RichText

from bedrock.base.i18n import bedrock_i18n_patterns
from bedrock.cms.decorators import pre_check_for_cms_404, prefer_cms
from bedrock.cms.tests import decorator_test_views
from bedrock.urls import urlpatterns as mozorg_urlpatterns

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
                fallback_lang_codes=["fr-CA", "es-MX", "sco"],
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
    assert resp.content.decode("utf-8") == "This is a dummy response from the decorated view with locale strings passed in"
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["fr-CA", "es-MX", "sco"]
    assert resp.wsgi_request._locales_available_via_cms == []  # No page in CMS yet

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/decorated/view/path/with/locale/strings/",
        site=minimal_site,
    )

    resp = client.get(f"{lang_code_prefix}/decorated/view/path/with/locale/strings/", follow=True)
    assert resp.status_code == 200
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["fr-CA", "es-MX", "sco"]
    assert resp.wsgi_request._locales_available_via_cms == ["en-US"]
    assert "This is a CMS page now, with the slug of strings" in resp.content.decode("utf-8")


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
    assert (
        resp.content.decode("utf-8") == "This is a dummy response from the decorated view for the callable, taking () and {'a_slug': 'a-slug-here'}"
    )
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
    assert resp.wsgi_request._locales_available_via_cms == ["en-US"]
    assert "This is a CMS page now, with the slug of a-slug-here" in resp.content.decode("utf-8")


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
    assert resp.content.decode("utf-8") == "This is a dummy response from the decorated view with fluent files explicitly passed in"
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
    assert resp.wsgi_request._locales_available_via_cms == ["en-US"]
    assert "This is a CMS page now, with the slug of files" in resp.content.decode("utf-8")


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
    assert resp.content.decode("utf-8") == "This is a dummy response from the wrapped view"
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["fr-CA", "es-MX", "sco"]
    assert resp.wsgi_request._locales_available_via_cms == []  # No page in CMS yet

    # Show the decorated view will "prefer" to render the Wagtail page when it exists
    _set_up_cms_pages(
        deepest_path="/wrapped/view/path/with/locale/strings/",
        site=minimal_site,
    )

    resp = client.get(f"{lang_code_prefix}/wrapped/view/path/with/locale/strings/", follow=True)
    assert resp.status_code == 200
    # Show that the expected locales are annotated onto the request
    assert resp.wsgi_request._locales_for_django_fallback_view == ["fr-CA", "es-MX", "sco"]
    assert resp.wsgi_request._locales_available_via_cms == ["en-US"]
    assert "This is a CMS page now, with the slug of strings" in resp.content.decode("utf-8")


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
    assert resp.content.decode("utf-8") == "This is a dummy response from the wrapped view"
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
    assert resp.wsgi_request._locales_available_via_cms == ["en-US"]
    assert "This is a CMS page now, with the slug of a-slug-here" in resp.content.decode("utf-8")


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
    assert resp.content.decode("utf-8") == "This is a dummy response from the wrapped view"

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
    assert resp.wsgi_request._locales_available_via_cms == ["en-US"]
    assert "This is a CMS page now, with the slug of files" in resp.content.decode("utf-8")


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


def dummy_view(request, *args, **kwargs):
    return HttpResponse("Hello, world!")


@pytest.mark.parametrize("pretend_that_path_exists", [True, False])
def test_pre_check_for_cms_404(
    pretend_that_path_exists,
    mocker,
    rf,
    settings,
    client,
    tiny_localized_site,
):
    settings.CMS_DO_PAGE_PATH_PRECHECK = True
    mocked_view = mocker.spy(dummy_view, "__call__")  # Spy on the test view
    mocked_path_exists_in_cms = mocker.patch("bedrock.cms.decorators.path_exists_in_cms")
    mocked_path_exists_in_cms.return_value = pretend_that_path_exists

    decorated_view = pre_check_for_cms_404(mocked_view)
    request = rf.get("/path/is/irrelevant/because/we/are/mocking/path_exists_in_cms")

    if pretend_that_path_exists:
        response = decorated_view(request)
        # Assert: Verify the original view was called
        mocked_view.assert_called_once_with(request)
        assert response.content == b"Hello, world!"
    else:
        with pytest.raises(Http404):  # Expect an Http404 since path_exists_in_cms returns False
            decorated_view(request)
        mocked_view.assert_not_called()


@pytest.mark.parametrize("pretend_that_path_exists", [True, False])
def test_pre_check_for_cms_404__show_can_be_disabled_with_settings(
    pretend_that_path_exists,
    mocker,
    rf,
    settings,
    client,
    tiny_localized_site,
):
    settings.CMS_DO_PAGE_PATH_PRECHECK = False
    mocked_view = mocker.spy(dummy_view, "__call__")  # Spy on the test view
    mocked_path_exists_in_cms = mocker.patch("bedrock.cms.decorators.path_exists_in_cms")
    mocked_path_exists_in_cms.return_value = pretend_that_path_exists

    decorated_view = pre_check_for_cms_404(mocked_view)
    request = rf.get("/path/is/irrelevant/because/we/are/mocking/path_exists_in_cms")

    # The fake view will always be called because the pre-check isn't being used
    response = decorated_view(request)
    mocked_view.assert_called_once_with(request)
    assert response.content == b"Hello, world!"
