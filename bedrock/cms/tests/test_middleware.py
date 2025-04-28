# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound

import pytest
from wagtail.models import Page

from bedrock.cms.middleware import CMSLocaleFallbackMiddleware

pytestmark = [pytest.mark.django_db]


def get_200_response(*args, **kwargs):
    return HttpResponse()


def get_404_response(*args, **kwargs):
    return HttpResponseNotFound()


def test_CMSLocaleFallbackMiddleware_200_response_means_middleware_does_not_fire(
    rf,
):
    request = rf.get("/en-US/some/page/path/")
    middleware = CMSLocaleFallbackMiddleware(get_response=get_200_response)
    response = middleware(request)
    assert response.status_code == 200


def test_CMSLocaleFallbackMiddleware__no_accept_language_header(
    rf,
    tiny_localized_site,
):
    request = rf.get("/es-MX/test-page/child-page/")  # page does not exist in es-MX
    middleware = CMSLocaleFallbackMiddleware(get_response=get_404_response)
    response = middleware(request)
    assert response.status_code == 302
    assert response.headers["Location"] == "/en-US/test-page/child-page/"


def test_CMSLocaleFallbackMiddleware_fallback_to_most_preferred_and_existing_locale(
    rf,
    tiny_localized_site,
):
    # tiny_localized_site supports en-US, fr and pt-BR, but not de
    request = rf.get(
        "/pl/test-page/child-page/",
        HTTP_ACCEPT_LANGUAGE="de-DE,pt-BR;q=0.8,sco;q=0.6",
    )
    middleware = CMSLocaleFallbackMiddleware(get_response=get_404_response)
    response = middleware(request)
    assert response.status_code == 302
    assert response.headers["Location"] == "/pt-BR/test-page/child-page/"


def test_CMSLocaleFallbackMiddleware_en_US_selected_because_is_in_accept_language_headers(
    rf,
    tiny_localized_site,
):
    # tiny_localized_site supports en-US, fr and pt-BR, but not de, so en-US should get picked
    request = rf.get(
        "/pl/test-page/child-page/",
        HTTP_ACCEPT_LANGUAGE="de-DE,en-US;q=0.9,fr;q=0.8,sco;q=0.6",
    )
    middleware = CMSLocaleFallbackMiddleware(get_response=get_404_response)
    response = middleware(request)
    assert response.status_code == 302
    assert response.headers["Location"] == "/en-US/test-page/child-page/"


def test_CMSLocaleFallbackMiddleware_en_US_is_selected_as_fallback_locale(
    rf,
    tiny_localized_site,
):
    # tiny_localized_site supports en-US, fr and pt-BR, but not de, es-MX or sco
    # so we should fall back to en-US
    assert settings.LANGUAGE_CODE == "en-US"
    request = rf.get(
        "/fr-CA//test-page/child-page/",
        HTTP_ACCEPT_LANGUAGE="de-DE,es-MX;q=0.8,sco;q=0.6",
    )
    middleware = CMSLocaleFallbackMiddleware(get_response=get_404_response)
    response = middleware(request)
    assert response.status_code == 302
    assert response.headers["Location"] == "/en-US/test-page/child-page/"


def test_CMSLocaleFallbackMiddleware_url_path_without_trailing_slash(
    rf,
    tiny_localized_site,
):
    # Unlikely that this code path will get triggered in reality, but worth
    # testing just in case

    # tiny_localized_site supports en-US, fr and pt-BR, but not de
    request = rf.get(
        "/sv/test-page/child-page",
        HTTP_ACCEPT_LANGUAGE="de-DE,fr;q=0.8,sco;q=0.6",
    )
    middleware = CMSLocaleFallbackMiddleware(get_response=get_404_response)
    response = middleware(request)
    assert response.status_code == 302
    assert response.headers["Location"] == "/fr/test-page/child-page/"


def test_CMSLocaleFallbackMiddleware_404_when_no_page_exists_in_any_locale(
    rf,
    tiny_localized_site,
):
    request = rf.get(
        "/en-GB/non-existent/page/",
        HTTP_ACCEPT_LANGUAGE="de-DE,fr;q=0.8,sco;q=0.6",
    )
    middleware = CMSLocaleFallbackMiddleware(get_response=get_404_response)
    response = middleware(request)
    assert response.status_code == 404


def test_CMSLocaleFallbackMiddleware_404_when_no_page_exists_in_any_locale__more_exacting(
    rf,
    tiny_localized_site,
):
    request = rf.get(
        "/en-GB/child-page/grandchild-page/",  # this doesn't match as a full path, only a sub-path
        HTTP_ACCEPT_LANGUAGE="de-DE,fr;q=0.8,sco;q=0.6",
    )
    middleware = CMSLocaleFallbackMiddleware(get_response=get_404_response)
    response = middleware(request)
    assert response.status_code == 404


def test_CMSLocaleFallbackMiddleware_accept_language_header_lang_codes_are_converted(
    rf,
    tiny_localized_site,
):
    request = rf.get(
        "/en-GB/test-page/child-page/",
        HTTP_ACCEPT_LANGUAGE="de-DE,Pt-bR;q=0.8,sco;q=0.6",  # note misformatted pt-BR
    )
    middleware = CMSLocaleFallbackMiddleware(get_response=get_404_response)
    response = middleware(request)
    assert response.status_code == 302
    assert response.headers["Location"] == "/pt-BR/test-page/child-page/"


def test_CMSLocaleFallbackMiddleware_404_when_no_live_page_exists_only_drafts(
    rf,
    tiny_localized_site,
):
    # See https://github.com/mozilla/bedrock/issues/16202

    # Unpublish all pages with the matching slug, so only drafts exist - and
    # we don't expect to be served any of those, of course
    child_pages = Page.objects.filter(slug="child-page")
    child_pages.unpublish()

    request = rf.get(
        "/pt-BR/test-page/child-page/",
        HTTP_ACCEPT_LANGUAGE="Pt-bR,de-DE,fr;q=0.8,sco;q=0.6",
    )
    middleware = CMSLocaleFallbackMiddleware(get_response=get_404_response)
    response = middleware(request)
    assert response.status_code == 404  # rather than a redirect to `child_page`


@pytest.mark.parametrize(
    "bad_url_path",
    [
        "/bad/\x00/path",
        "/bad/path/\x00",
        "/bad/path/\x00/",
        "/bad/\x00/path/\x00",
        "is/download/badfilename\x00.jpg/some-follow-on/path/",
    ],
)
def test_CMSLocaleFallbackMiddleware_404_with_null_byte_in_url(
    rf,
    tiny_localized_site,
    bad_url_path,
):
    # See https://github.com/mozilla/bedrock/issues/16222

    request = rf.get(
        bad_url_path,
    )
    middleware = CMSLocaleFallbackMiddleware(get_response=get_404_response)
    response = middleware(request)
    assert response.status_code == 404  # rather than a 500 when using postgres
