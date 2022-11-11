# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test import override_settings

import pytest

from bedrock.contentful.constants import CONTENT_TYPE_PAGE_RESOURCE_CENTER
from bedrock.contentful.models import ContentfulEntry
from bedrock.contentful.utils import can_use_locale, get_active_locales


@pytest.mark.django_db
@pytest.mark.parametrize(
    "creation_params, threshold_setting, function_params, expected",
    (
        (
            [
                [3, "en-US", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [2, "fr", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [1, "de", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
            ],
            float(66),
            [CONTENT_TYPE_PAGE_RESOURCE_CENTER, "classification_one", "fr"],
            True,
        ),
        (
            [
                [3, "en-US", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [2, "fr", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [1, "de", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
            ],
            float(66),
            [CONTENT_TYPE_PAGE_RESOURCE_CENTER, "classification_one", "de"],
            False,
        ),
        (
            [
                [3, "en-US", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [4, "fr", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [1, "de", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
            ],
            float(66),
            [CONTENT_TYPE_PAGE_RESOURCE_CENTER, "classification_one", "fr"],
            True,
        ),
        (
            [
                [3, "en-US", "classification_one", "some-other-content-type"],
                [4, "fr", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [1, "de", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
            ],
            float(66),
            [CONTENT_TYPE_PAGE_RESOURCE_CENTER, "classification_one", "fr"],
            False,
        ),
        (
            [],  # no entries should return a False
            float(66),
            [CONTENT_TYPE_PAGE_RESOURCE_CENTER, "classification_one", "fr"],
            False,
        ),
        (
            [
                [3, "en-US", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [2, "fr", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [1, "de", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
            ],
            float(0),
            [CONTENT_TYPE_PAGE_RESOURCE_CENTER, "classification_one", "fr"],
            True,
        ),
        (
            [
                [3, "en-US", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [2, "fr", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [1, "de", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
            ],
            float(100),
            [CONTENT_TYPE_PAGE_RESOURCE_CENTER, "classification_one", "fr"],
            False,
        ),
    ),
    ids=[
        "Threshold exceeded",
        "Threshold not met",
        "Chosen locale can have more content than default locale",
        "Content type matters",
        "No entries at all returns False",
        "Threshold of 0%",
        "Threshold of 100%",
    ],
)
def test_can_use_locale(
    creation_params,
    threshold_setting,
    function_params,
    expected,
):
    for count, locale, classification, content_type in creation_params:
        for i in range(count):
            ContentfulEntry.objects.create(
                content_type=content_type,
                contentful_id=f"entry_{i+1}",
                classification=classification,
                locale=locale,
            )

    with override_settings(CONTENTFUL_LOCALE_SUFFICIENT_CONTENT_PERCENTAGE=threshold_setting):
        decision = can_use_locale(*function_params)
        assert decision == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "creation_params, threshold_setting, function_params, expected",
    (
        (
            [
                [3, "en-US", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [1, "fr", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [2, "de", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [4, "jp", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [1, "it", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [3, "ru", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
            ],
            float(66),
            [CONTENT_TYPE_PAGE_RESOURCE_CENTER, "classification_one"],
            ["de", "en-US", "jp", "ru"],  # sorted
        ),
        (
            [],
            float(66),
            [CONTENT_TYPE_PAGE_RESOURCE_CENTER, "classification_one"],
            [],  # sorted
        ),
        (
            [
                [3, "en-US", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [3, "fr", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [3, "de", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [4, "jp", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [3, "it", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
                [3, "ru", "classification_one", CONTENT_TYPE_PAGE_RESOURCE_CENTER],
            ],
            float(66),
            [CONTENT_TYPE_PAGE_RESOURCE_CENTER, "classification_one"],
            ["de", "en-US", "fr", "it", "jp", "ru"],  # sorted
        ),
    ),
    ids=[
        "Various locales, some active, some not",
        "no locales",
        "all locales active",
    ],
)
def test_get_active_locales(
    creation_params,
    threshold_setting,
    function_params,
    expected,
):
    for count, locale, classification, content_type in creation_params:
        for i in range(count):
            ContentfulEntry.objects.create(
                content_type=content_type,
                contentful_id=f"entry_{i+1}",
                classification=classification,
                locale=locale,
            )

    with override_settings(CONTENTFUL_LOCALE_SUFFICIENT_CONTENT_PERCENTAGE=threshold_setting):
        active_locales = get_active_locales(*function_params)
        assert active_locales == expected
