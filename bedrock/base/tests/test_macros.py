# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from django_jinja.backend import Jinja2

jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {}).strip()


EXPECTED_IMAGES = {
    "basic": """<img src="/media/test.jpg" alt="" />""",
    "lazy": """<img src="/media/test.jpg" alt="" loading="lazy" />""",
    "with_alt": """<img src="/media/test.jpg" alt="test alt" />""",
    "with_class": """<img src="/media/test.jpg" alt="" class="test" />""",
    "with_dimensions": """<img src="/media/test.jpg" alt="" width="64" height="64" />""",
    "highres": """<img class="" src="/media/test.jpg" srcset="/media/test-high-res.jpg 1.5x" alt="">""",
    "l10n": """<img src="/media/img/l10n/en-US/test.jpg" alt="" />""",
    "external": """<img src="https://test.jpg" alt="" />""",
    "l10n_highres": """<img class="" src="/media/img/l10n/en-US/test.jpg" srcset="/media/img/l10n/en-US/test-high-res.jpg 1.5x" alt="">""",
    "highres_lazy": """<img class="" src="/media/test.jpg" srcset="/media/test-high-res.jpg 1.5x" alt="" loading="lazy">""",
    "all_attributes": """<img class="test" src="/media/img/l10n/en-US/test.jpg" srcset="/media/img/l10n/en-US/test-high-res.jpg 1.5x" alt="test" width="64" height="64" loading="lazy">""",  # noqa: E501
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
            "url='test.jpg', class='test', alt='test', loading='lazy', width='64', height='64',include_highres=True, include_l10n=True",
            EXPECTED_IMAGES["all_attributes"],
        ),
    ],
)
def test_markup(test_input, expected):
    # note: this isn't actually setting the locale, it's matching the default expected locale
    mock_request = {"request": {"locale": "en-US"}}
    # need to split these strings and re-combine them to allow python formatting
    # (otherwise it conflicts with jinja import syntax)
    # need to import with context for the request key to appear in l10n_img helper
    markup = render("{% from 'macros.html' import image with context %}" + "{{{{ image({0}) }}}}".format(test_input), mock_request)
    assert markup == expected
