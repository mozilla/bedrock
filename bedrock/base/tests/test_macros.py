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
