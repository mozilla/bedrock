# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import re
from typing import List, MutableSet
from unittest.mock import patch

import pytest

from lib.l10n_utils.templatetags.fluent import (
    ATTRS_ALLOWED_IN_FLUENT_STRINGS,
    TAGS_ALLOWED_IN_FLUENT_STRINGS,
    ftl,
)


@pytest.mark.parametrize(
    "mock_return_value, expected",
    (
        (
            '<strong>bolder</strong>and <a href="{ $mailto }">test@example.com</a>.<br><span>spanned</span> <em>emphasised</em> <abbr>abbreviation</abbr>',  # noqa: E501
            '<strong>bolder</strong>and <a href="{ $mailto }">test@example.com</a>.<br><span>spanned</span> <em>emphasised</em> <abbr>abbreviation</abbr>',  # noqa: E501
        ),
        (
            'test attrs <a href="https://www.mozilla.org/" class="test-link" id="target-for-link" rel="nofollow" title="test title">test</a>',
            'test attrs <a href="https://www.mozilla.org/" class="test-link" id="target-for-link" rel="nofollow" title="test title">test</a>',
        ),
        (
            "some string with a sneaky <script>alert('pwned');</script>",
            "some string with a sneaky &lt;script&gt;alert('pwned');&lt;/script&gt;",
        ),
        (
            'some string with disallowed attrs <a onclick="injectedScript()">test</a>',
            "some string with disallowed attrs <a>test</a>",
        ),
        ("String with no markup in it", "String with no markup in it"),
    ),
    ids=[
        "Tag test, no changes expected via sanitization",
        "Attr test, no changes expected via sanitization",
        "Proof that bleach is escaping tags that are not in the allowlists",
        "Proof that bleach is stripping attrs that are not in the allowlists",
        "String with no markup in it",
    ],
)
@patch("lib.l10n_utils.templatetags.fluent.fluent.translate")
@patch("lib.l10n_utils.templatetags.fluent.fluent.ftl")
def test_ftl_bleaches_string(mock_ftl, mock_translate, mock_return_value, expected):
    # Ensure the ftl() templatetag call bleaches the output of Markup
    mock_ftl.return_value = mock_return_value
    mock_translate.return_value = mock_return_value
    dummy_ctx = {
        "fluent_l10n": "dummy_fluent_l10n_in_ctx",
        "fluent_files": "dummy_fluent_files_in_ctx",
    }
    assert ftl(dummy_ctx, "dummy") == expected


def test_ftl_bleach_allowlists_are_comprehensive():
    """This is a canary test to confirm our bleach() settings for
    calls to the ftl() helper are appropriate for the content we expect.

    FTL strings in `en-US` are our default, so ensure the bleaching call
    expects all the _trusted_ markup that we can currently find in those
    en-US strings. If non-en-US strings contain disallowed markup, it will
    be escaped at runtime"""

    # Build a list of the tags and attrs we find in our fluent strings and
    # compare them with what's in our allowlists.

    tag_re = re.compile(r"<\w+")
    attr_re = re.compile(r"\s\w+=")

    filepaths = set()

    tags_found = set()
    attrs_found = set()

    def _clean_tag_matches(tag_matches: List) -> MutableSet:
        return set([x.replace("<", "") for x in tag_matches])

    def _clean_attr_matches(attr_matches: List) -> MutableSet:
        return set([x.replace("=", "").strip() for x in attr_matches if "?" not in x])

    for starting_dir in [
        "l10n/",
        "l10n-pocket",
    ]:
        for root, _, files in os.walk(starting_dir):
            for file in files:
                if file.endswith(".ftl"):
                    filepaths.add(os.path.join(root, file))

    for filepath in filepaths:
        with open(filepath) as fp:
            for line in fp.readlines():
                if tag_matches := re.findall(tag_re, line):
                    tags_found.update(_clean_tag_matches(tag_matches))
                if attr_matches := re.findall(attr_re, line):
                    attrs_found.update(_clean_attr_matches(attr_matches))

    assert TAGS_ALLOWED_IN_FLUENT_STRINGS.issuperset(tags_found), (
        "DANGER! HTML tags were detected in source FTL strings that are not in "
        "lib.l10n_utils.templatetags.fluent.TAGS_ALLOWED_IN_FLUENT_STRINGS. "
        f"Unexpected tag(s) found: {tags_found.difference(TAGS_ALLOWED_IN_FLUENT_STRINGS)}"
    )

    assert set(ATTRS_ALLOWED_IN_FLUENT_STRINGS).issuperset(attrs_found), (
        "DANGER! HTML attributes were detected in source FTL strings that are not in "
        "lib.l10n_utils.templatetags.fluent.ATTRS_ALLOWED_IN_FLUENT_STRINGS. "
        f"Unexpected attribute(s) found: {set(attrs_found).difference(set(ATTRS_ALLOWED_IN_FLUENT_STRINGS))}"
    )
