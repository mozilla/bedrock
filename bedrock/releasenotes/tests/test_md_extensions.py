# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from ..md_extensions import CloseImgTagPostprocessor


@pytest.mark.parametrize(
    "input_text, expected_correct_text",
    (
        (
            '<p><img alt="Invalid img markup" src="https://www.example.org/images/test.png"></p>',
            '<p><img alt="Invalid img markup" src="https://www.example.org/images/test.png"></img></p>',
        ),
        (
            '<p><img alt="Valid img markup" src="https://www.example.org/images/test.png"></img></p>',
            '<p><img alt="Valid img markup" src="https://www.example.org/images/test.png"></img></p>',
        ),
        (
            '<p><img alt="Valid img markup" src="https://www.example.org/images/test.png"/></p>',
            '<p><img alt="Valid img markup" src="https://www.example.org/images/test.png"/></p>',
        ),
        (
            """
            <p><img alt="Valid img markup" src="https://www.example.org/images/test.png"/></p>
            <p><img alt="Invalid img markup" src="https://www.example.org/images/test.png"></p>
            <p><img alt="Invalid img markup" src="https://www.example.org/images/test.png"></p>
            <p><img alt="Valid img markup" src="https://www.example.org/images/test.png"></img></p>
            <p><img alt="Invalid img markup" src="https://www.example.org/images/test.png"></p>
            """,
            """
            <p><img alt="Valid img markup" src="https://www.example.org/images/test.png"/></p>
            <p><img alt="Invalid img markup" src="https://www.example.org/images/test.png"></img></p>
            <p><img alt="Invalid img markup" src="https://www.example.org/images/test.png"></img></p>
            <p><img alt="Valid img markup" src="https://www.example.org/images/test.png"></img></p>
            <p><img alt="Invalid img markup" src="https://www.example.org/images/test.png"></img></p>
            """,
        ),
    ),
    ids=[
        "Fixing unclosed img tag",
        "Leaving closed img tag unchanged",
        "Leaving self-closing img tag unchanged",
        "Multiple examples fixed while viable ones left unchanged",
    ],
)
def test_img_closing_extension(input_text, expected_correct_text):
    pp = CloseImgTagPostprocessor()
    processed = pp.run(input_text)
    assert processed == expected_correct_text
