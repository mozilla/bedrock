# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.contrib.auth import get_user_model
from django.test import override_settings

import pytest

from bedrock.anonym.fixtures.base_fixtures import (
    get_placeholder_image,
    get_test_anonym_index_page,
    get_test_person,
)
from bedrock.anonym.fixtures.page_fixtures import (
    get_anonym_case_study_item_test_page,
    get_anonym_case_study_test_page,
    get_anonym_contact_test_page,
    get_anonym_content_sub_test_page,
    get_anonym_index_test_page,
    get_anonym_news_item_test_page,
    get_anonym_news_test_page,
)

User = get_user_model()


@pytest.fixture
def admin_client(client, db):
    """Force-login a superuser using the ModelBackend rather than the project's
    default SSO backend. Without the override, mozilla_django_oidc's
    SessionRefresh middleware sees an OIDC-authenticated user with no OIDC
    token in the session and redirects every admin GET to the auth0 login URL
    (302) — which would break the 302/200 assertions below.
    """
    with override_settings(
        AUTHENTICATION_BACKENDS=("django.contrib.auth.backends.ModelBackend",),
        USE_SSO_AUTH=False,
    ):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass",
        )
        client.force_login(admin, backend="django.contrib.auth.backends.ModelBackend")
        yield client


@pytest.fixture
def placeholder_image():
    """Fixture providing a placeholder image for testing."""
    return get_placeholder_image()


@pytest.fixture
def test_person(placeholder_image):
    """Fixture providing a test Person snippet."""
    return get_test_person()


@pytest.fixture
def anonym_index_page():
    """Fixture providing a test AnonymIndexPage (basic, without content)."""
    return get_test_anonym_index_page()


@pytest.fixture
def anonym_index_page_with_content():
    """Fixture providing a test AnonymIndexPage with full content."""
    return get_anonym_index_test_page()


@pytest.fixture
def anonym_content_sub_page(anonym_index_page):
    """Fixture providing a test AnonymContentSubPage."""
    return get_anonym_content_sub_test_page()


@pytest.fixture
def anonym_news_page(anonym_index_page):
    """Fixture providing a test AnonymNewsPage."""
    return get_anonym_news_test_page()


@pytest.fixture
def anonym_news_item_page(anonym_news_page):
    """Fixture providing a test AnonymNewsItemPage."""
    return get_anonym_news_item_test_page(news_page=anonym_news_page)


@pytest.fixture
def anonym_case_study_page(anonym_index_page):
    """Fixture providing a test AnonymCaseStudyPage."""
    return get_anonym_case_study_test_page()


@pytest.fixture
def anonym_case_study_item_page(anonym_case_study_page):
    """Fixture providing a test AnonymCaseStudyItemPage."""
    return get_anonym_case_study_item_test_page(case_study_page=anonym_case_study_page)


@pytest.fixture
def anonym_contact_page(anonym_index_page):
    """Fixture providing a test AnonymContactPage."""
    return get_anonym_contact_test_page()
