# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest import mock

from django.test import override_settings

import pytest
import wagtail_factories
from wagtail.models import Page
from wagtail_localize_smartling.exceptions import IncapableVisualContextCallback
from wagtaildraftsharing.models import WagtaildraftsharingLink

from bedrock.cms.tests.factories import SimpleRichTextPageFactory, WagtailUserFactory
from bedrock.cms.wagtail_localize_smartling.callbacks import _get_html_for_sharing_link, visual_context


@pytest.mark.django_db
@override_settings(WAGTAILADMIN_BASE_URL="https://cms.example.com")
def test_visual_context__for_page(client):
    top_level_page = SimpleRichTextPageFactory()

    page = SimpleRichTextPageFactory(parent=top_level_page, slug="visual-context-text-page")
    page.save_revision()

    wagtail_factories.SiteFactory(
        root_page=top_level_page,
        is_default_site=True,
        hostname=client._base_environ()["SERVER_NAME"],
    )

    user = WagtailUserFactory()

    mock_job = mock.Mock()
    mock_job.translation_source.get_source_instance.return_value = page
    mock_job.user = user

    url, html = visual_context(smartling_job=mock_job)

    # light checks because we're not testing wagtaildraftsharing itself
    assert "<body" in html
    assert "Test SimpleRichTextPage" in html
    assert '<base href="https://www.mozilla.org/">' in html

    sharing_link_key = WagtaildraftsharingLink.objects.get().key
    assert url == f"https://cms.example.com/_internal_draft_preview/{sharing_link_key}/"


@pytest.mark.django_db
@override_settings(WAGTAILADMIN_BASE_URL="https://cms.example.com")
@mock.patch("bedrock.cms.wagtail_localize_smartling.callbacks._get_html_for_sharing_link")
def test_visual_context__cms_hostname_stripped_and_base_tag_injected(mock_get_html, client):
    top_level_page = SimpleRichTextPageFactory()
    page = SimpleRichTextPageFactory(parent=top_level_page, slug="visual-context-text-page")
    page.save_revision()

    site = wagtail_factories.SiteFactory(
        root_page=top_level_page,
        is_default_site=True,
        hostname="cms-internal.example.com",
        port=8080,
    )
    cms_root_url = site.root_url  # e.g. "http://cms-internal.example.com:8080"

    mock_get_html.return_value = f'<html><head></head><body><img src="{cms_root_url}/media/image.jpg"></body></html>'

    user = WagtailUserFactory()
    mock_job = mock.Mock()
    mock_job.translation_source.get_source_instance.return_value = page
    mock_job.user = user

    _, html = visual_context(smartling_job=mock_job)

    assert cms_root_url not in html
    assert "https://cms.example.com" not in html
    assert '<base href="https://www.mozilla.org/">' in html
    assert '<img src="/media/image.jpg">' in html


def test_visual_context__for_inviable_object(client):
    inviable_obj = mock.Mock()

    assert not isinstance(inviable_obj, Page)

    mock_job = mock.Mock()
    mock_job.translation_source.get_source_instance.return_value = inviable_obj

    with pytest.raises(IncapableVisualContextCallback) as exc:
        url, html = visual_context(smartling_job=mock_job)

    assert exc.value.args[0] == "Object was not visually previewable (i.e. not a Page)"


@pytest.mark.django_db
@mock.patch("bedrock.cms.wagtail_localize_smartling.callbacks.capture_message")
def test_visual_context__for_page__with_no_revision(mock_capture_message, client):
    top_level_page = SimpleRichTextPageFactory()

    page = SimpleRichTextPageFactory(parent=top_level_page, slug="visual-context-text-page")
    page.save_revision()

    wagtail_factories.SiteFactory(
        root_page=top_level_page,
        is_default_site=True,
        hostname=client._base_environ()["SERVER_NAME"],
    )

    user = WagtailUserFactory()

    mock_job = mock.Mock()
    mock_job.translation_source.get_source_instance.return_value = page
    mock_job.user = user

    page.latest_revision = None
    page.save()
    with pytest.raises(IncapableVisualContextCallback) as ctx:
        visual_context(smartling_job=mock_job)

    assert ctx.value.args[0] == (
        "Object was not visually previewable because it didn't have a saved revision. Are you a developer with a local export?"
    )
    mock_capture_message.assert_called_once_with(f"Unable to get a latest_revision for {page} so unable to send visual context.")


@override_settings(WAGTAILADMIN_BASE_URL="https://cms.example.com")
@mock.patch("bedrock.cms.wagtail_localize_smartling.callbacks.SharingLinkView.as_view")
@mock.patch("bedrock.cms.wagtail_localize_smartling.callbacks.RequestFactory")
def test__get_html_for_sharing_link__uses_cms_hostname_and_path_only(mock_factory_cls, mock_as_view):
    # sharing_link.url is a full URL — we should extract just the path and use
    # the CMS hostname as SERVER_NAME so make_preview_request doesn't fall back
    # to 'localhost' / 'testserver' and return a 400 error page.
    mock_response = mock.Mock()
    mock_response.text = "<html><body>page content</body></html>"
    mock_as_view.return_value = mock.Mock(return_value=mock_response)

    sharing_link = mock.Mock()
    sharing_link.url = "http://localhost/_internal_draft_preview/abc123/"

    result = _get_html_for_sharing_link(sharing_link)

    mock_factory_cls.assert_called_once_with(SERVER_NAME="cms.example.com")
    mock_factory_cls.return_value.get.assert_called_once_with("/_internal_draft_preview/abc123/")
    assert result == "<html><body>page content</body></html>"


# The happy path is implicitly tested in test_visual_context__*, above
@mock.patch("bedrock.cms.wagtail_localize_smartling.callbacks.capture_exception")
@mock.patch("bedrock.cms.wagtail_localize_smartling.callbacks.SharingLinkView.as_view")
def test__get_html_for_sharing_link__unhappy_path(mock_sharing_link_as_view, mock_capture_exception):
    test_exception = Exception("Boom!")
    mock_sharing_link_as_view.return_value = mock.Mock(side_effect=test_exception)

    sharing_link = mock.Mock()
    sharing_link.url = "https://example.com/1231313211/link"

    with pytest.raises(IncapableVisualContextCallback) as ctx:
        _get_html_for_sharing_link(sharing_link)

    assert ctx.value.args[0] == "Was not able to get a HTML export from the sharing link"

    mock_capture_exception.assert_called_once_with(test_exception)
