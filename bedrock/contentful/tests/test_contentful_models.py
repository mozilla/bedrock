# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import Mock, patch

import pytest

from bedrock.contentful.constants import CONTENT_TYPE_CONNECT_HOMEPAGE
from bedrock.contentful.models import ContentfulEntry

pytestmark = pytest.mark.django_db


@pytest.fixture
def dummy_homepages():
    ContentfulEntry.objects.create(
        contentful_id="home000001",
        content_type=CONTENT_TYPE_CONNECT_HOMEPAGE,
        classification="",
        data={"dummy": "Homepage FR"},
        locale="fr",
        slug="home",
        category="",
        tags=[],
    )
    ContentfulEntry.objects.create(
        contentful_id="home000002",
        content_type=CONTENT_TYPE_CONNECT_HOMEPAGE,
        classification="",
        data={"dummy": "Homepage DE"},
        locale="de",
        slug="home",
        category="",
        tags=[],
    )


@pytest.fixture
def dummy_entries():
    ContentfulEntry.objects.create(
        contentful_id="abcdef000001",
        content_type="test_type_1",
        classification="classification_1",
        data={"dummy": "Type 1, Classification 1, category one, tags 1-3"},
        locale="en-US",
        localisation_complete=True,
        slug="test-one",
        category="category one",
        tags=["tag 1", "tag 2", "tag 3"],
    )
    ContentfulEntry.objects.create(
        contentful_id="abcdef000002",
        content_type="test_type_1",
        classification="classification_2",  # nb, different from above
        data={"dummy": "Type 1, Classification 2, category one, tag 10 only"},
        locale="en-US",
        localisation_complete=True,
        slug="test-two",
        category="category one",  # nb, same as above
        tags=["tag 10"],
    )
    ContentfulEntry.objects.create(
        contentful_id="abcdef000003",
        content_type="test_type_2",
        classification="classification_1",
        data={"dummy": "Type 2, Classification 1, category one, tags 1-3"},
        locale="en-US",
        localisation_complete=True,
        slug="test-three",
        category="category one",  # nb, same as above
        tags=["tag 1", "tag 2", "tag 3"],
    )
    ContentfulEntry.objects.create(
        # identical to above, save for the classification
        contentful_id="abcdef000004",
        content_type="test_type_2",
        classification="classification_2",
        data={"dummy": "Type 2, Classification 2, category one, tags 2 and 3"},
        locale="en-US",
        localisation_complete=True,
        slug="test-four",
        category="category one",  # nb, same as above
        tags=[
            "tag 2",
        ],
    )
    ContentfulEntry.objects.create(
        contentful_id="abcdef000005",
        content_type="test_type_1",
        classification="classification_2",
        data={"dummy": "Type 1, Classification 2, category two, tags 2 and 10 only"},
        locale="en-US",
        localisation_complete=True,
        slug="test-five",
        category="category two",  # nb, same as above
        tags=["tag 10", "tag 2"],
    )
    ContentfulEntry.objects.create(
        contentful_id="abcdef000006",
        content_type="test_type_1",
        classification="classification_2",
        data={"dummy": "Type 1, Classification 2, category three, tags 2 and 7 only - French locale"},
        locale="fr",
        localisation_complete=True,
        slug="test-six",
        category="category three",  # nb, same as above
        tags=["tag 2", "tag 7"],
    )
    ContentfulEntry.objects.create(
        contentful_id="abcdef000007",
        content_type="test_type_1",
        classification="",
        data={"dummy": "Type 1, no classification, category three, tags 2 and 7 only - French locale"},
        locale="de",
        localisation_complete=True,
        slug="test-seven",
        category="category three",  # nb, same as above
        tags=["tag 2", "tag 7"],
    )


@pytest.mark.parametrize(
    "id,expected",
    (
        (
            "abcdef000001",
            {"dummy": "Type 1, Classification 1, category one, tags 1-3"},
        ),
        (
            "abcdef000002",
            {"dummy": "Type 1, Classification 2, category one, tag 10 only"},
        ),
        (
            "abcdef000005",
            {"dummy": "Type 1, Classification 2, category two, tags 2 and 10 only"},
        ),
    ),
)
def test_contentfulentrymanager__get_page_by_id(id, expected, dummy_entries):
    assert ContentfulEntry.objects.get_page_by_id(id) == expected


@pytest.mark.parametrize(
    "slug,locale,content_type,classification,expected_contentful_id",
    (
        (
            "test-one",
            "en-US",
            "test_type_1",
            "classification_1",
            "abcdef000001",
        ),
        (
            "test-two",
            "en-US",
            "test_type_1",
            "classification_2",
            "abcdef000002",
        ),
        (
            "test-four",
            "en-US",
            "test_type_2",
            "classification_2",
            "abcdef000004",
        ),
        (
            "test-six",
            "fr",
            "test_type_1",
            "classification_2",
            "abcdef000006",
        ),
        (
            "test-seven",
            "de",
            "test_type_1",
            None,
            "abcdef000007",
        ),
    ),
)
def test_contentfulentrymanager__get_entry_by_slug__happy_paths(
    slug,
    locale,
    content_type,
    classification,
    expected_contentful_id,
    dummy_entries,
):
    assert (
        ContentfulEntry.objects.get_entry_by_slug(
            slug=slug,
            locale=locale,
            content_type=content_type,
            classification=classification,
        ).contentful_id
        == expected_contentful_id
    )


@pytest.mark.parametrize(
    "slug, locale, content_type, classification",
    (
        (
            "test-one",
            "fr",
            "test_type_1",
            "classification_1",
        ),
        (
            "test-one",
            "en-US",
            "test_type_2",
            "classification_1",
        ),
        (
            "test-one",
            "en-US",
            "test_type_1",
            "classification_3",
        ),
        (
            "test-one-bad-slug",
            "en-US",
            "test_type_1",
            "classification_1",
        ),
    ),
    ids=[
        "locale mismatch",
        "content_type mismatch",
        "classification mismatch",
        "slug mismatch",
    ],
)
def test_contentfulentrymanager__get_entry_by_slug__unhappy_paths(
    slug,
    locale,
    content_type,
    classification,
):

    try:
        ContentfulEntry.objects.get_entry_by_slug(
            slug=slug,
            locale=locale,
            content_type=content_type,
            classification=classification,
        )
        assert False, "Should not have found a ContentfulEntry"
    except ContentfulEntry.DoesNotExist:
        pass


@patch("bedrock.contentful.models.ContentfulEntry.objects.get_entry_by_slug")
def test_contentfulentrymanager__get_page_by_slug(mock_get_entry_by_slug):

    mock_retval = Mock(name="mock_retval")
    mock_retval.data = {"mocked": "data"}
    mock_get_entry_by_slug.return_value = mock_retval

    res = ContentfulEntry.objects.get_page_by_slug(
        slug="test_slug",
        locale="test_locale",
        content_type="test_content_type",
        classification="test_classification",
    )
    assert res == {"mocked": "data"}
    mock_get_entry_by_slug.assert_called_once_with(
        slug="test_slug",
        locale="test_locale",
        content_type="test_content_type",
        classification="test_classification",
        localisation_complete=True,
    )


def test_contentfulentrymanager__get_active_locales_for_slug():

    for i in range(3):
        for locale in [
            "de",
            "ja",
            "it",
        ]:
            ContentfulEntry.objects.create(
                contentful_id=f"{locale}-locale00{i}",
                content_type="test_type_1",
                classification="",
                data={"dummy": "dummy"},
                locale=locale,
                localisation_complete=True,
                slug=f"locale00{i}",
            )

    for i in range(3):
        for locale in [
            "pt",
            "zh-CN",
        ]:
            ContentfulEntry.objects.create(
                contentful_id=f"{locale}-locale00{i}",
                content_type="test_type_1",
                classification="test-classification",
                data={"dummy": "dummy"},
                locale=locale,
                localisation_complete=True,
                slug=f"locale00{i}",
            )

    for locale in [
        "en-US",
        "fr",
        "es-ES",
    ]:
        ContentfulEntry.objects.create(
            contentful_id=f"{locale}-locale00{i}",
            content_type="test_type_1",
            classification="",
            data={"dummy": "dummy"},
            locale=locale,
            localisation_complete=False,
            slug=f"locale00{i}",
        )

    # no match for slug
    assert (
        ContentfulEntry.objects.get_active_locales_for_slug(
            slug="non-matching-slug",
            content_type="test_type_1",
        )
        == []
    )

    # no match for content type
    assert (
        ContentfulEntry.objects.get_active_locales_for_slug(
            slug="locale001",
            content_type="test_type_DOES_NOT_EXIST",
        )
        == []
    )

    # match for slug and content type, but only on those with localisation complete
    assert ContentfulEntry.objects.get_active_locales_for_slug(
        slug="locale001",
        content_type="test_type_1",
    ) == ["de", "it", "ja", "pt", "zh-CN"]

    # match for slug and content type and classifcation,
    # but only on those with localisation complete
    assert ContentfulEntry.objects.get_active_locales_for_slug(
        slug="locale001",
        content_type="test_type_1",
        classification="test-classification",
    ) == ["pt", "zh-CN"]


@pytest.mark.parametrize(
    "content_type, locale, classification, expected_ids",
    (
        (
            "test_type_1",
            "en-US",
            "classification_1",
            ["abcdef000001"],
        ),
        (
            "test_type_1",
            "en-US",
            "classification_2",
            ["abcdef000002", "abcdef000005"],
        ),
        (
            "test_type_1",
            "fr",
            "classification_2",
            ["abcdef000006"],
        ),
        (
            "test_type_1",
            "en-US",
            None,
            ["abcdef000001", "abcdef000002", "abcdef000005"],
        ),
        (
            "test_type_2",
            "en-US",
            None,
            ["abcdef000003", "abcdef000004"],
        ),
        (
            "test_type_1",
            "es",
            "classification_1",
            [],
        ),
    ),
)
def test_contentfulentrymanager__get_entries_by_type(
    locale,
    content_type,
    classification,
    expected_ids,
    dummy_entries,
):
    res = ContentfulEntry.objects.get_entries_by_type(
        locale=locale,
        content_type=content_type,
        classification=classification,
    )
    assert [x.contentful_id for x in res] == expected_ids


def test_contentfulentrymanager__get_entries_by_type__ordering(dummy_entries):

    kwargs = dict(content_type="test_type_1", locale="en-US", classification=None)

    # default ordering: last_modified
    res_1 = [x.contentful_id for x in ContentfulEntry.objects.get_entries_by_type(**kwargs)]
    assert res_1 == ["abcdef000001", "abcdef000002", "abcdef000005"]

    res_2 = [x.contentful_id for x in ContentfulEntry.objects.get_entries_by_type(order_by="-last_modified", **kwargs)]
    assert res_2 == ["abcdef000005", "abcdef000002", "abcdef000001"]
    assert [x for x in reversed(res_1)] == res_2


@pytest.mark.parametrize(
    "locale, expected_data",
    (
        ("fr", {"dummy": "Homepage FR"}),
        ("de", {"dummy": "Homepage DE"}),
    ),
)
def test_contentfulentrymanager__get_homepage(locale, expected_data, dummy_homepages):
    assert ContentfulEntry.objects.get_homepage(locale) == expected_data


@pytest.mark.parametrize(
    "source_id, expected_related_ids",
    (
        (
            "abcdef000001",
            [
                "abcdef000003",  # tag 1
                "abcdef000004",  # tag 2
                "abcdef000005",  # tag 2
            ],
        ),
        (
            "abcdef000005",
            [
                "abcdef000001",  # tag 2
                "abcdef000002",  # tag 10
                "abcdef000003",  # tag 2
                "abcdef000004",  # tag 2
                # "abcdef000006",  # tag 2, but NOT same locale
                # "abcdef000007",  # tag 2, but NOT same locale
            ],
        ),
        (
            "abcdef000006",
            [
                # "abcdef000007",  # tag 2, and tag 7, but NOT same locale
            ],
        ),
    ),
)
def test_contentfulentry__get_related_entries(
    source_id,
    expected_related_ids,
    dummy_entries,
):
    # update all the classifications and content_types to be the same, for the sake of this test
    ContentfulEntry.objects.all().update(
        classification="relations-test",
        content_type="relation-test-type",
    )

    entry = ContentfulEntry.objects.get(contentful_id=source_id)
    assert [x.contentful_id for x in entry.get_related_entries()] == expected_related_ids


@pytest.mark.parametrize(
    "source_id, expected_related_ids",
    (
        (
            "abcdef000001",
            [],
        ),
        (
            "abcdef000005",
            ["abcdef000002"],
        ),
        (
            "abcdef000006",
            [],
        ),
    ),
)
def test_contentfulentry__get_related_entries__show_content_type_and_classification_matter(
    source_id,
    expected_related_ids,
    dummy_entries,
):
    "Similar to above, but without standardising the content_type or classification"

    entry = ContentfulEntry.objects.get(contentful_id=source_id)
    assert [x.contentful_id for x in entry.get_related_entries()] == expected_related_ids


def test_contentfulentry__get_related_entries__no_tags(dummy_entries):
    entry = ContentfulEntry.objects.get(contentful_id="abcdef000005")

    assert entry.tags and len(entry.get_related_entries()) != 0  # initially related items are shown

    entry.tags = {}
    entry.save()
    assert not entry.tags and len(entry.get_related_entries()) == 0  # Because not tags, no related items


def test_contentfulentry__str__method(dummy_entries):
    entry = ContentfulEntry.objects.get(contentful_id="abcdef000005")
    assert f"{entry}" == "ContentfulEntry test_type_1:abcdef000005[en-US]"
