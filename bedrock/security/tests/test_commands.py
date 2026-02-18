# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os.path
from unittest.mock import patch

from django.conf import settings

from bedrock.mozorg.tests import TestCase
from bedrock.security.management.commands import update_security_advisories
from bedrock.security.models import Product


class TestStripHtmlComments:
    """Verify strip_html_comments removes HTML comments from advisory HTML."""

    def test_strips_single_line_comment(self):
        html = "<ul><li>keep</li><!-- remove --></ul>"
        result = update_security_advisories.strip_html_comments(html)
        assert result == "<ul><li>keep</li></ul>"

    def test_strips_multiline_comment(self):
        html = '<ul>\n  <li>keep</li>\n<!--\n  <li><a href="http://example.com">CVE-2009-xxxx</a></li>\n-->\n</ul>'
        result = update_security_advisories.strip_html_comments(html)
        assert "<!--" not in result
        assert "-->" not in result
        assert "CVE-2009-xxxx" not in result
        assert "<li>keep</li>" in result

    def test_strips_multiple_comments(self):
        html = "<p>a</p><!-- one --><p>b</p><!-- two --><p>c</p>"
        result = update_security_advisories.strip_html_comments(html)
        assert result == "<p>a</p><p>b</p><p>c</p>"

    def test_no_comments_unchanged(self):
        html = "<p>No comments here</p>"
        result = update_security_advisories.strip_html_comments(html)
        assert result == html

    def test_empty_comment(self):
        html = "<p>before</p><!----><p>after</p>"
        result = update_security_advisories.strip_html_comments(html)
        assert result == "<p>before</p><p>after</p>"


class TestSanitizeAdvisoryHtml:
    """Verify advisory HTML sanitization strips dangerous content."""

    def test_strips_script_tags(self):
        html = '<p>Safe</p><script>alert("xss")</script>'
        result = update_security_advisories.sanitize_advisory_html(html)
        assert "<script" not in result
        assert "Safe" in result

    def test_strips_event_handlers(self):
        html = '<img src=x onerror=alert("XSS")>'
        result = update_security_advisories.sanitize_advisory_html(html)
        assert "onerror" not in result

    def test_strips_javascript_urls(self):
        html = "<a href=\"javascript:alert('xss')\">click</a>"
        result = update_security_advisories.sanitize_advisory_html(html)
        assert "javascript:" not in result.lower()

    def test_preserves_safe_advisory_html(self):
        """Tags used by the CVE partial template and markdown must survive."""
        html = (
            '<section class="cve">'
            '<h4 id="CVE-2024-0001"><a href="#CVE-2024-0001">'
            '<span class="anchor">#</span>CVE-2024-0001: Title</a></h4>'
            '<dl class="summary"><dt>Reporter</dt><dd>Alice</dd>'
            '<dt>Impact</dt><dd><span class="level critical">critical</span></dd></dl>'
            "<h5>Description</h5><p>A <strong>bad</strong> thing.</p>"
            "<h5>References</h5><ul><li>"
            '<a href="https://bugzilla.mozilla.org/show_bug.cgi?id=12345">Bug 12345</a>'
            "</li></ul></section>"
        )
        result = update_security_advisories.sanitize_advisory_html(html)
        # All structural tags preserved
        for tag in ["<section", "<h4", "<h5", "<dl", "<dt", "<dd", "<span", "<a ", "<ul", "<li", "<p>", "<strong>"]:
            assert tag in result
        assert 'href="https://bugzilla.mozilla.org' in result
        assert 'id="CVE-2024-0001"' in result
        assert 'class="cve"' in result

    def test_preserves_markdown_output_tags(self):
        """Standard markdown output tags must survive."""
        html = (
            "<h1>Title</h1><h2>Sub</h2><h3>Sub2</h3>"
            "<p><em>emphasis</em> and <code>code</code></p>"
            "<pre><code>block</code></pre>"
            "<blockquote><p>quote</p></blockquote>"
            "<ol><li>one</li></ol><ul><li>two</li></ul>"
            "<hr><br>"
        )
        result = update_security_advisories.sanitize_advisory_html(html)
        for tag in ["<h1>", "<h2>", "<h3>", "<em>", "<code>", "<pre>", "<blockquote>", "<ol>", "<hr", "<br"]:
            assert tag in result

    def test_strips_svg_tags(self):
        html = '<p>ok</p><svg onload="alert(1)"></svg>'
        result = update_security_advisories.sanitize_advisory_html(html)
        assert "<svg" not in result

    def test_strips_iframe_tags(self):
        html = '<p>ok</p><iframe src="https://evil.com"></iframe>'
        result = update_security_advisories.sanitize_advisory_html(html)
        assert "<iframe" not in result

    def test_strips_disallowed_attrs_on_allowed_tags(self):
        html = '<span class="ok" onclick="bad()">text</span>'
        result = update_security_advisories.sanitize_advisory_html(html)
        assert 'class="ok"' in result
        assert "onclick" not in result

    def test_preserves_additional_allowlisted_tags(self):
        html = (
            "<p><del>removed</del> <b>bold</b> <i>italic</i> "
            "<small>fine print</small> <abbr>abbr</abbr></p>"
            '<img src="https://example.com/pic.png" alt="pic">'
        )
        result = update_security_advisories.sanitize_advisory_html(html)
        for tag in ["<del>", "<b>", "<i>", "<small>", "<abbr>", "<img "]:
            assert tag in result
        assert 'src="https://example.com/pic.png"' in result
        assert 'alt="pic"' in result

    def test_strips_html_comments(self):
        html = "<ul><li>keep</li><!-- <li>commented out</li> --></ul>"
        result = update_security_advisories.sanitize_advisory_html(html)
        assert "<!--" not in result
        assert "&lt;!--" not in result
        assert "commented out" not in result
        assert "<li>keep</li>" in result

    def test_strips_javascript_img_src(self):
        html = '<img src="javascript:alert(1)" alt="x">'
        result = update_security_advisories.sanitize_advisory_html(html)
        assert "javascript:" not in result.lower()

    @patch.object(update_security_advisories, "add_or_update_advisory")
    @patch.object(update_security_advisories, "parse_md_file")
    def test_update_db_from_file_sanitizes_html(self, mock_parser, mock_add):
        """Integration: update_db_from_file must sanitize before storing."""
        mock_parser.return_value = (
            {
                "mfsa_id": "2024-01",
                "title": "T",
                "impact": "high",
                "fixed_in": ["Firefox 99"],
                "announced": "January 1, 2024",
            },
            '<p>ok</p><script>alert("xss")</script>',
        )
        update_security_advisories.update_db_from_file("/fake/path/mfsa2024-01.md")
        _data, html = mock_add.call_args[0]
        assert "<script" not in html
        assert "<p>ok</p>" in html


def test_fix_product_name():
    """Should fix SeaMonkey and strip '.0' from names."""
    assert update_security_advisories.fix_product_name("Seamonkey 2.2") == "SeaMonkey 2.2"
    assert update_security_advisories.fix_product_name("Firefox 2.2") == "Firefox 2.2"
    assert update_security_advisories.fix_product_name("fredflintstone 2.2") == "fredflintstone 2.2"
    assert update_security_advisories.fix_product_name("Firefox 32.0") == "Firefox 32"
    assert update_security_advisories.fix_product_name("Firefox 32.0.1") == "Firefox 32.0.1"


def test_filter_advisory_names():
    filenames = [
        "README.md",
        "LICENSE.txt",
        "announce/2015/mfsa2015-01.md",
        "announce/2015/mfsa2016-42.yml",
        "stuff/whatnot.md",
        "mfsa2015-02.md",
    ]
    good_filenames = [
        settings.MOFO_SECURITY_ADVISORIES_PATH + "/announce/2015/mfsa2015-01.md",
        settings.MOFO_SECURITY_ADVISORIES_PATH + "/announce/2015/mfsa2016-42.yml",
        settings.MOFO_SECURITY_ADVISORIES_PATH + "/mfsa2015-02.md",
    ]
    assert update_security_advisories.filter_advisory_filenames(filenames) == good_filenames


def test_get_ids_from_files():
    filenames = [
        "README.md",
        "LICENSE.txt",
        "announce/2015/mfsa2015-01.md",
        "announce/2015/mfsa2016-42.yml",
        "stuff/whatnot.md",
        "mfsa2015-02.md",
    ]
    good_ids = ["2015-01", "2016-42", "2015-02"]
    assert update_security_advisories.get_ids_from_files(filenames) == good_ids


def make_mfsa(mfsa_id):
    update_security_advisories.add_or_update_advisory(
        {
            "mfsa_id": mfsa_id,
            "title": "The Dude is insecure",
            "impact": "High",
            "announced": "December 25, 2015",
            "fixed_in": ["Firefox 43.0.1"],
        },
        "The Dude minds, man!",
    )


class TestDBActions(TestCase):
    def test_get_files_to_delete_from_db(self):
        make_mfsa("2015-100")
        make_mfsa("2015-101")
        make_mfsa("2015-102")
        make_mfsa("2015-103")
        all_files = ["mfsa2015-100.md", "mfsa2015-101.md"]
        assert set(update_security_advisories.get_files_to_delete_from_db(all_files)) == {"mfsa2015-102.md", "mfsa2015-103.md"}

    def test_delete_orphaned_products(self):
        make_mfsa("2015-100")
        Product.objects.create(name="Firefox 43.0.2")
        Product.objects.create(name="Firefox 43.0.3")
        assert update_security_advisories.delete_orphaned_products() == 2
        assert Product.objects.get().name == "Firefox 43.0.1"

    @patch.object(update_security_advisories, "get_all_file_names")
    @patch.object(update_security_advisories, "delete_files")
    @patch.object(update_security_advisories, "update_db_from_file")
    @patch.object(update_security_advisories, "GitRepo")
    def test_file_name_extension_change(self, git_mock, udbff_mock, df_mock, gafn_mock):
        """
        An MFSA file can now be either .md or .yml. Make sure this is an update, not a delete.
        """
        make_mfsa("2016-42")
        make_mfsa("2016-43")
        all_files = [os.path.join(update_security_advisories.ADVISORIES_PATH, "mfsa2016-42.yml")]
        gafn_mock.return_value = all_files
        git_mock().has_changes.return_value = True
        update_security_advisories.Command().handle_safe(quiet=True, no_git=False, clear_db=False)
        udbff_mock.assert_called_with(update_security_advisories.filter_advisory_filenames(all_files)[0])
        df_mock.assert_called_with(["mfsa2016-43.md"])
