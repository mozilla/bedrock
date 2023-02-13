# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from markupsafe import Markup

from bedrock.contentful.templatetags.helpers import (
    ALLOWED_ATTRS,
    ALLOWED_TAGS,
    _allowed_attrs,
    external_html,
)


@pytest.mark.parametrize(
    "attr, allowed",
    (
        ("alt", True),
        ("class", True),
        ("href", True),
        ("id", True),
        ("src", True),
        ("srcset", True),
        ("rel", True),
        ("title", True),
        ("data-foo", True),
        ("data-bar", True),
        ("custom", False),
    ),
)
def test__allowed_attrs(attr, allowed):
    assert _allowed_attrs(None, attr, None) == allowed


@pytest.mark.parametrize(
    "content,expected",
    (
        (
            '<script>alert("boo!")</script>',
            '&lt;script&gt;alert("boo!")&lt;/script&gt;',
        ),
        (
            '<a id="test" foo="bar" href="#test">test</a>',
            '<a id="test" href="#test">test</a>',
        ),
    ),
    ids=[
        "disallowed tag, so is escaped",
        "allowed tag but disallowed attr",
    ],
)
def test_external_html(content, expected):
    # light test of our bleaching
    output = external_html(content)

    assert type(content) == str
    assert output == Markup(expected)


def test_allowed_attrs_const__remains_what_we_expect():
    # Regression safety net so that any amendment to ALLOWED_ATTRS is 100% deliberate

    assert ALLOWED_ATTRS == [
        "alt",
        "class",
        "href",
        "id",
        "src",
        "srcset",
        "rel",
        "title",
    ]


def test_allowed_tags_const__remains_what_we_expect():
    # Regression safety net so that any amendment to ALLOWED_TAGS is 100% deliberate

    assert ALLOWED_TAGS == {
        "a",
        "abbr",
        "acronym",
        "b",
        "blockquote",
        "button",
        "cite",
        "code",
        "div",
        "em",
        "figure",
        "figcaption",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "hr",
        "i",
        "img",
        "li",
        "ol",
        "p",
        "small",
        "span",
        "strike",
        "strong",
        "ul",
    }
