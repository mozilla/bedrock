# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.base.templatetags.helpers import remove_p_tag


def test_remove_p_tag():
    input_html = '<p class="test-class">This is a paragraph.</p><p>This is another paragraph.</p>'
    expected_output = "This is a paragraph.<br/>This is another paragraph."
    assert remove_p_tag(input_html) == expected_output


def test_remove_p_tag_with_inner_tags():
    input_html = '<p class="test-class">This is a <strong>paragraph</strong>.</p><p>This is another paragraph.</p>'
    expected_output = "This is a <strong>paragraph</strong>.<br/>This is another paragraph."
    assert remove_p_tag(input_html) == expected_output


def test_remove_p_tag_preserves_escaped_entities():
    # Regression: `remove_p_tag` must not convert entity-encoded HTML inside text
    # nodes back into live markup (XSS).
    input_html = "<p>&lt;img src=x onerror=alert(1)&gt;</p>"
    expected_output = "&lt;img src=x onerror=alert(1)&gt;"
    assert remove_p_tag(input_html) == expected_output
