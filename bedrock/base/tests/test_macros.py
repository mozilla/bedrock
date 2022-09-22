# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re

import pytest
from django_jinja.backend import Jinja2
from pyquery import PyQuery as pq

jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {}).strip()


def inner_html(el):
    # always remove newlines and excess whitespace
    return re.sub(r"\s+", " ", el.html()).strip()


EXPECTED_IMAGES = {
    "basic": '<img src="/media/test.jpg" alt="" />',
    "lazy": '<img src="/media/test.jpg" alt="" loading="lazy" />',
    "with_alt": '<img src="/media/test.jpg" alt="test alt" />',
    "with_class": '<img src="/media/test.jpg" alt="" class="test" />',
    "with_dimensions": '<img src="/media/test.jpg" alt="" width="64" height="64" />',
    "highres": '<img class="" src="/media/test.jpg" srcset="/media/test-high-res.jpg 1.5x" alt="">',
    "l10n": '<img src="/media/img/l10n/en-US/test.jpg" alt="" />',
    "external": '<img src="https://test.jpg" alt="" />',
    "l10n_highres": '<img class="" src="/media/img/l10n/en-US/test.jpg" srcset="/media/img/l10n/en-US/test-high-res.jpg 1.5x" alt="">',
    "highres_lazy": '<img class="" src="/media/test.jpg" srcset="/media/test-high-res.jpg 1.5x" alt="" loading="lazy">',
    "all_attributes": (
        '<img class="test" src="/media/img/l10n/en-US/test.jpg" '
        'srcset="/media/img/l10n/en-US/test-high-res.jpg 1.5x" alt="test" width="64" height="64" loading="lazy">'
    ),
    "resp_img": (
        '<img src="/media/test-500.jpg" srcset="/media/test-500.png 500w,/media/test-1000.png 1000w" '
        'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)" alt="">'
    ),
    "resp_img_srcset": '<img src="/media/test.jpg" srcset="/media/test-high-res.png 2x" alt="">',
    "resp_img_l10n": (
        '<img src="/media/img/l10n/en-US/test-500.jpg" '
        'srcset="/media/img/l10n/en-US/test-500.png 500w,/media/img/l10n/en-US/test-1000.png 1000w" '
        'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)" alt="">'
    ),
    "resp_img_attributes": (
        '<img src="/media/test-500.jpg" srcset="/media/test-500.png 500w,/media/test-1000.png 1000w" '
        'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)" '
        'alt="test" class="test" width="64" height="64" loading="lazy">'
    ),
    "picture": (
        '<picture><source media="(max-width: 799px)" srcset="/media/test-mobile.png">'
        '<source media="(min-width: 800px)" srcset="/media/test-desktop.png">'
        '<img src="/media/test-mobile.jpg" alt=""></picture>'
    ),
    "picture_l10n": (
        '<picture><source media="(max-width: 799px)" srcset="/media/img/l10n/en-US/test-mobile.png">'
        '<source media="(min-width: 800px)" srcset="/media/img/l10n/en-US/test-desktop.png">'
        '<img src="/media/img/l10n/en-US/test-mobile.jpg" alt=""></picture>'
    ),
    "picture_attributes": (
        '<picture><source media="(max-width: 799px)" srcset="/media/test-mobile.png">'
        '<source media="(min-width: 800px)" srcset="/media/test-desktop.png">'
        '<img src="/media/test-mobile.jpg" alt="test" class="test" width="64" height="64" loading="lazy"></picture>'
    ),
    "highres_image_url": ('<img src="https://www.example.com/test.jpg" srcset="https://www.example.com/test-high-res.jpg 2x" alt="" />'),
}


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("url='test.jpg'", EXPECTED_IMAGES["basic"]),
        ("url='test.jpg', loading='lazy'", EXPECTED_IMAGES["lazy"]),
        ("url='test.jpg', alt='test alt'", EXPECTED_IMAGES["with_alt"]),
        ("url='test.jpg', class='test'", EXPECTED_IMAGES["with_class"]),
        ("url='test.jpg', width='64', height='64'", EXPECTED_IMAGES["with_dimensions"]),
        ("url='test.jpg', include_highres=True", EXPECTED_IMAGES["highres"]),
        ("url='test.jpg', include_l10n=True", EXPECTED_IMAGES["l10n"]),
        ("url='https://test.jpg'", EXPECTED_IMAGES["external"]),
        ("url='test.jpg', include_highres=True, include_l10n=True", EXPECTED_IMAGES["l10n_highres"]),
        ("url='test.jpg', include_highres=True, loading='lazy'", EXPECTED_IMAGES["highres_lazy"]),
        (
            "url='test.jpg', class='test', alt='test', loading='lazy', width='64', height='64', include_highres=True, include_l10n=True",
            EXPECTED_IMAGES["all_attributes"],
        ),
        (
            (
                "url='test-500.jpg', "
                "srcset={'test-500.png': '500w', 'test-1000.png': '1000w'}, "
                "sizes={'(min-width: 1000px)': 'calc(50vw - 200px)', 'default': 'calc(100vw - 50px)'}"
            ),
            EXPECTED_IMAGES["resp_img"],
        ),
        ("url='test.jpg', " "srcset={'test-high-res.png': '2x'}", EXPECTED_IMAGES["resp_img_srcset"]),
        (
            (
                "url='test-500.jpg', include_l10n=True, "
                "srcset={'test-500.png': '500w', 'test-1000.png': '1000w'}, "
                "sizes={'(min-width: 1000px)': 'calc(50vw - 200px)', 'default': 'calc(100vw - 50px)'}"
            ),
            EXPECTED_IMAGES["resp_img_l10n"],
        ),
        (
            (
                "url='test-500.jpg', class='test', alt='test', loading='lazy', width='64', height='64', "
                "srcset={'test-500.png': '500w', 'test-1000.png': '1000w'}, "
                "sizes={'(min-width: 1000px)': 'calc(50vw - 200px)', 'default': 'calc(100vw - 50px)'}"
            ),
            EXPECTED_IMAGES["resp_img_attributes"],
        ),
        (
            (
                "url='test-mobile.jpg', "
                "sources=[{'media': '(max-width: 799px)', 'srcset': {'test-mobile.png': 'default'}}, "
                "{'media': '(min-width: 800px)', 'srcset': {'test-desktop.png': 'default'}}]"
            ),
            EXPECTED_IMAGES["picture"],
        ),
        (
            (
                "url='test-mobile.jpg', include_l10n=True, "
                "sources=[{'media': '(max-width: 799px)', 'srcset': {'test-mobile.png': 'default'}}, "
                "{'media': '(min-width: 800px)', 'srcset': {'test-desktop.png': 'default'}}]"
            ),
            EXPECTED_IMAGES["picture_l10n"],
        ),
        (
            (
                "url='test-mobile.jpg', class='test', alt='test', loading='lazy', width='64', height='64', "
                "sources=[{'media': '(max-width: 799px)', 'srcset': {'test-mobile.png': 'default'}}, "
                "{'media': '(min-width: 800px)', 'srcset': {'test-desktop.png': 'default'}}]"
            ),
            EXPECTED_IMAGES["picture_attributes"],
        ),
        (
            "url='https://www.example.com/test.jpg', highres_image_url='https://www.example.com/test-high-res.jpg'",
            EXPECTED_IMAGES["highres_image_url"],
        ),
    ],
)
def test_image_markup(test_input, expected):
    # note: this isn't actually setting the locale, it's matching the default expected locale
    mock_request = {"request": {"locale": "en-US"}}
    # need to split these strings and re-combine them to allow python formatting
    # (otherwise it conflicts with jinja import syntax)
    # need to import with context for the request key to appear in l10n_img helper
    markup = render("{% from 'macros.html' import image with context %}" + "{{{{ image({0}) }}}}".format(test_input), mock_request)
    assert markup == expected


current_link_input = {"text": "Testing current link", "href": "/current", "cta_name": "Test Link"}
regular_link_input = {"text": "Testing link", "href": "/regular", "cta_name": "Test Link"}

EXPECTED_NAV_HTML = {
    "title_text": """Testing title""",
    "title_icon": """<img class="c-sub-navigation-icon" src="icon.png" width="24" height="24" alt="">""",
    "title_link": """<a href="/category" data-link-type="nav" data-link-position="subnav" data-link-name="Test Title">""",
    "current_link": """<a href="/current" data-link-type="nav" data-link-position="subnav" data-link-name="Test Link" aria-current="page"> Testing current link </a>""",  # noqa: E501
    "regular_link": """<a href="/regular" data-link-type="nav" data-link-position="subnav" data-link-name="Test Link"> Testing link </a>""",
    "is_summary": """is-summary""",
    "is_details_default_closed": """is-details is-closed""",
}


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            f"title={{'text': 'Testing title'}}, links=[{regular_link_input}, {regular_link_input}]",
            {"title_text": EXPECTED_NAV_HTML["title_text"], "links": [EXPECTED_NAV_HTML["regular_link"], EXPECTED_NAV_HTML["regular_link"]]},
        ),
        (
            f"title={{'text': 'Testing title', 'icon': 'icon.png'}}, links=[{regular_link_input}, {current_link_input}]",
            {
                "title_text": EXPECTED_NAV_HTML["title_text"],
                "title_icon": EXPECTED_NAV_HTML["title_icon"],
                "links": [EXPECTED_NAV_HTML["regular_link"], EXPECTED_NAV_HTML["current_link"]],
            },
        ),
        (
            f"title={{'text': 'Testing title', 'href': '/category', 'cta_name': 'Test Title'}}, links=[{current_link_input}, {regular_link_input}]",
            {
                "title_text": EXPECTED_NAV_HTML["title_text"],
                "title_link": EXPECTED_NAV_HTML["title_link"],
                "links": [EXPECTED_NAV_HTML["current_link"], EXPECTED_NAV_HTML["regular_link"]],
            },
        ),
        (
            f"title={{'text': 'Testing title', 'href': '/category', 'cta_name': 'Test Title', 'icon': 'icon.png'}}, links=[{regular_link_input}, {current_link_input}, {regular_link_input}]",  # noqa: E501
            {
                "title_text": EXPECTED_NAV_HTML["title_text"],
                "title_link": EXPECTED_NAV_HTML["title_link"],
                "title_icon": EXPECTED_NAV_HTML["title_icon"],
                "links": [EXPECTED_NAV_HTML["regular_link"], EXPECTED_NAV_HTML["current_link"], EXPECTED_NAV_HTML["regular_link"]],
            },
        ),
    ],
)
def test_sub_nav_markup(test_input, expected):
    mock_request = {"request": {"path": "/current"}}
    # need to import with context for the request key to pass along the path value
    markup = render("{% from 'macros.html' import sub_nav with context %}" + "{{{{ sub_nav({0}) }}}}".format(test_input), mock_request)
    doc = pq(markup)

    nav_title = doc(".c-sub-navigation-title")
    assert nav_title.text() == expected["title_text"]
    assert EXPECTED_NAV_HTML["is_summary"] in nav_title.outer_html()

    nav_list = doc(".c-sub-navigation-list")
    assert EXPECTED_NAV_HTML["is_details_default_closed"] in nav_list.outer_html()

    nav_links = nav_list.find(".c-sub-navigation-item")
    assert len(nav_links) == len(expected["links"])
    for index, nav_link in enumerate(nav_links):
        assert inner_html(pq(nav_link)) == expected["links"][index]

    if "title_icon" in expected:
        assert nav_title.find(".c-sub-navigation-icon").outer_html() == expected["title_icon"]

    if "title_link" in expected:
        assert expected["title_link"] in inner_html(nav_title)
