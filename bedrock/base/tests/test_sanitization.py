# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from bedrock.base.sanitization import sanitize_html, strip_all_tags


class TestStripAllTags:
    @pytest.mark.parametrize(
        "html, expected",
        [
            ("<p>Hello</p>", "Hello"),
            ("<div><p>Hello</p></div>", "Hello"),
            ("<b>bold</b> and <i>italic</i>", "bold and italic"),
            ("pre <script>alert('xss')</script> post", "pre alert('xss') post"),
            ("pre <style>body{color:red}</style> post", "pre body{color:red} post"),
            ("<div><span><b>text</b></span></div>", "text"),
            ("", ""),
            ("just plain text", "just plain text"),
            ("<p>unclosed", "unclosed"),
            ("before<br/>after", "beforeafter"),
            ("<p>hello   world</p>", "hello   world"),
        ],
    )
    def test_strip_all_tags(self, html, expected):
        assert strip_all_tags(html) == expected


class TestSanitizeHtml:
    def test_allowed_tags_pass_through(self):
        result = sanitize_html("<p>Hello <b>world</b></p>", {"p", "b"}, {"*": []})
        assert "<p>" in result
        assert "<b>" in result

    def test_disallowed_tags_escaped(self):
        # Note: script/style tags are dropped entirely for security
        result = sanitize_html("<p>Hello</p><div>world</div>", {"p"}, {"*": []})
        assert "<p>" in result
        assert "<div>" not in result
        assert "&lt;div&gt;" in result

    def test_allowed_attributes(self):
        result = sanitize_html(
            '<a href="https://example.com" class="link">Click</a>',
            {"a"},
            {"a": ["href", "class"]},
        )
        assert 'href="https://example.com"' in result
        assert 'class="link"' in result

    def test_disallowed_attributes_removed(self):
        result = sanitize_html(
            '<a href="https://example.com" onclick="evil()">Click</a>',
            {"a"},
            {"a": ["href"]},
        )
        assert 'href="https://example.com"' in result
        assert "onclick" not in result

    def test_global_attributes(self):
        result = sanitize_html(
            '<p class="para" id="p1">Text</p><a class="link" href="#">Link</a>',
            {"p", "a"},
            {"*": ["class", "id"], "a": ["href"]},
        )
        assert 'class="para"' in result
        assert 'id="p1"' in result
        assert 'href="#"' in result

    @pytest.mark.parametrize(
        "html",
        [
            '<script>alert("xss")</script>',
            '<img src="x" onerror="alert(\'xss\')">',
            "<a href=\"javascript:alert('xss')\">click</a>",
            "<svg onload=\"alert('xss')\"></svg>",
        ],
    )
    def test_xss_prevention(self, html):
        result = sanitize_html(html, {"a", "img", "div"}, {"*": ["class"], "a": ["href"], "img": ["src"]})
        assert "javascript:" not in result.lower()
        assert "onerror" not in result.lower()
        assert "onload" not in result.lower()
        assert "<script" not in result.lower()
        assert "<svg" not in result.lower()

    @pytest.mark.parametrize(
        "scheme,should_pass",
        [
            ("http://example.com", True),
            ("https://example.com", True),
            ("mailto:test@example.com", True),
            ("tel:+1234567890", True),
            ("javascript:alert('xss')", False),
            ("data:text/html,<script>alert('xss')</script>", False),
            ("vbscript:msgbox('xss')", False),
        ],
    )
    def test_url_scheme_handling(self, scheme, should_pass):
        """Test that URL policy correctly allows/strips different URL schemes."""
        html = f'<a href="{scheme}">link</a>'
        result = sanitize_html(html, {"a"}, {"a": ["href"]})
        if should_pass:
            assert scheme in result
        else:
            assert scheme not in result

    def test_img_src_url_scheme_handling(self):
        """Test that img src attributes also have URL policy applied."""
        # Valid schemes
        result = sanitize_html('<img src="https://example.com/img.png">', {"img"}, {"img": ["src"]})
        assert "https://example.com/img.png" in result

        # javascript: should be stripped
        result = sanitize_html("<img src=\"javascript:alert('xss')\">", {"img"}, {"img": ["src"]})
        assert "javascript:" not in result.lower()
