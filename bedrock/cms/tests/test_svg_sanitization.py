# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Tests for SVG sanitization in image uploads.
"""

import hashlib
from io import BytesIO
from unittest import mock

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

import defusedxml.ElementTree as ET
import pytest
from wagtail.images.fields import WagtailImageField

from bedrock.cms.fields import SanitizingWagtailImageField

# This is a clean SVG as it might come from a design tool
# (with UTF-8 encoding, normal attribute order)
CLEAN_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <circle cx="50" cy="50" r="40" fill="red"/>
</svg>"""

MALICIOUS_SVG_WITH_SCRIPT = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <circle cx="50" cy="50" r="40" fill="red"/>
    <script>alert('XSS')</script>
</svg>"""

MALICIOUS_SVG_WITH_ONCLICK = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <circle cx="50" cy="50" r="40" fill="red" onclick="alert('XSS')"/>
</svg>"""

SVG_WITH_ALLOWED_DATA_URL = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100" height="100">
    <image href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==" />
</svg>"""

pytestmark = [pytest.mark.django_db]


class SVGSanitizationFieldTestCase(TestCase):
    """Tests for the SanitizingWagtailImageField."""

    def setUp(self):
        self.field = SanitizingWagtailImageField()

    def test_clean_svg_passes_validation(self):
        """A clean SVG should pass validation without errors."""
        svg_file = SimpleUploadedFile(
            "test.svg",
            CLEAN_SVG.encode("utf-8"),
            content_type="image/svg+xml",
        )

        # Should not raise ValidationError
        result = self.field._sanitize_svg(svg_file)
        self.assertIsNone(result)

    def test_malicious_svg_with_script_rejected(self):
        """SVG with <script> tag should be rejected."""
        svg_file = SimpleUploadedFile(
            "malicious.svg",
            MALICIOUS_SVG_WITH_SCRIPT.encode("utf-8"),
            content_type="image/svg+xml",
        )

        result = self.field._sanitize_svg(svg_file)
        self.assertIsInstance(result, ValidationError)
        self.assertEqual(result.code, "svg_dangerous_content")

    def test_malicious_svg_with_event_handler_rejected(self):
        """SVG with event handler should be rejected."""
        svg_file = SimpleUploadedFile(
            "onclick.svg",
            MALICIOUS_SVG_WITH_ONCLICK.encode("utf-8"),
            content_type="image/svg+xml",
        )

        result = self.field._sanitize_svg(svg_file)
        self.assertIsInstance(result, ValidationError)
        self.assertEqual(result.code, "svg_dangerous_content")

    def test_svg_detection_by_extension(self):
        """Should detect SVG by .svg extension."""
        svg_file = SimpleUploadedFile(
            "test.svg",
            CLEAN_SVG.encode("utf-8"),
        )
        self.assertTrue(self.field._is_svg_file(svg_file))

    def test_svg_detection_by_content_type(self):
        """Should detect SVG by content type."""
        svg_file = SimpleUploadedFile(
            "test.txt",  # Wrong extension
            CLEAN_SVG.encode("utf-8"),
            content_type="image/svg+xml",
        )
        self.assertTrue(self.field._is_svg_file(svg_file))

    def test_non_svg_not_detected(self):
        """Should not detect non-SVG files as SVG."""
        png_file = SimpleUploadedFile(
            "test.png",
            b"fake png content",
            content_type="image/png",
        )
        self.assertFalse(self.field._is_svg_file(png_file))

    def test_hash_computation(self):
        """Hash computation should be consistent."""
        content = b"test content"
        hash1 = self.field._compute_hash(content)
        hash2 = self.field._compute_hash(content)
        self.assertEqual(hash1, hash2)
        self.assertEqual(hash1, hashlib.sha256(content).hexdigest())

    def test_file_reading_preserves_position(self):
        """Reading file content should preserve file position."""
        content = b"test content"
        file_obj = BytesIO(content)
        file_obj.seek(5)  # Move to middle

        read_content = self.field._read_file_content(file_obj)

        self.assertEqual(read_content, content)
        self.assertEqual(file_obj.tell(), 5)  # Position restored

    def test_error_messages_defined(self):
        """Field should have custom error messages."""
        self.assertIn("svg_dangerous_content", self.field.error_messages)
        self.assertIn("svg_sanitization_error", self.field.error_messages)

    def test_svg_with_allowed_data_url_passes(self):
        """SVG with allowed image data URLs should pass."""
        # Image data URLs are allowed and should not be flagged as dangerous
        svg_file = SimpleUploadedFile(
            "data_url.svg",
            SVG_WITH_ALLOWED_DATA_URL.encode("utf-8"),
            content_type="image/svg+xml",
        )

        result = self.field._sanitize_svg(svg_file)
        # Should pass - image data URLs are safe
        self.assertIsNone(result)

    def test_svg_with_javascript_url_rejected(self):
        """SVG with javascript: URL should be rejected."""
        svg_with_js = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <a href="javascript:alert('XSS')">
        <circle cx="50" cy="50" r="40" fill="red"/>
    </a>
</svg>"""
        svg_file = SimpleUploadedFile(
            "javascript_url.svg",
            svg_with_js.encode("utf-8"),
            content_type="image/svg+xml",
        )

        result = self.field._sanitize_svg(svg_file)
        self.assertIsInstance(result, ValidationError)
        self.assertEqual(result.code, "svg_dangerous_content")

    def test_regex_detection_finds_script_tag(self):
        """Regex detection should find <script> tags."""
        content = b'<svg><script>alert("xss")</script></svg>'
        self.assertTrue(self.field._has_dangerous_patterns_regex(content))

    def test_regex_detection_finds_event_handler(self):
        """Regex detection should find event handler attributes."""
        content = b'<svg><circle onclick="alert()" /></svg>'
        self.assertTrue(self.field._has_dangerous_patterns_regex(content))

    def test_regex_detection_clean_svg(self):
        """Regex detection should not flag clean SVGs."""
        content = CLEAN_SVG.encode("utf-8")
        self.assertFalse(self.field._has_dangerous_patterns_regex(content))

    def test_xml_detection_finds_script_element(self):
        """XML detection should find <script> elements."""
        content = MALICIOUS_SVG_WITH_SCRIPT.encode("utf-8")
        self.assertTrue(self.field._has_dangerous_elements_xml(content))

    def test_xml_detection_finds_event_attribute(self):
        """XML detection should find event handler attributes."""
        content = MALICIOUS_SVG_WITH_ONCLICK.encode("utf-8")
        self.assertTrue(self.field._has_dangerous_elements_xml(content))

    def test_xml_detection_clean_svg(self):
        """XML detection should not flag clean SVGs."""
        content = CLEAN_SVG.encode("utf-8")
        self.assertFalse(self.field._has_dangerous_elements_xml(content))

    # Integration tests for to_python() method
    def test_to_python_with_clean_svg(self):
        """to_python() should successfully process clean SVG files."""
        svg_file = SimpleUploadedFile(
            "clean.svg",
            CLEAN_SVG.encode("utf-8"),
            content_type="image/svg+xml",
        )

        # Mock parent's to_python to return the file (simulating successful validation)
        with mock.patch.object(WagtailImageField, "to_python", return_value=svg_file):
            result = self.field.to_python(svg_file)

        # Should return the file object, not raise
        self.assertEqual(result, svg_file)

    def test_to_python_with_malicious_svg_raises(self):
        """to_python() should raise ValidationError for malicious SVG files."""
        svg_file = SimpleUploadedFile(
            "malicious.svg",
            MALICIOUS_SVG_WITH_SCRIPT.encode("utf-8"),
            content_type="image/svg+xml",
        )

        # Mock parent's to_python
        with mock.patch.object(WagtailImageField, "to_python", return_value=svg_file):
            with self.assertRaises(ValidationError) as cm:
                self.field.to_python(svg_file)

        self.assertEqual(cm.exception.code, "svg_dangerous_content")

    def test_to_python_with_non_svg_passes_through(self):
        """to_python() should pass through non-SVG files without sanitization."""
        png_file = SimpleUploadedFile(
            "image.png",
            b"fake png content",
            content_type="image/png",
        )

        # Mock parent's to_python
        with mock.patch.object(WagtailImageField, "to_python", return_value=png_file):
            # _sanitize_svg should not be called for non-SVG files
            with mock.patch.object(self.field, "_sanitize_svg") as mock_sanitize:
                result = self.field.to_python(png_file)

                # Sanitization should not have been called
                mock_sanitize.assert_not_called()
                self.assertEqual(result, png_file)

    def test_to_python_with_none_returns_none(self):
        """to_python() should return None when parent returns None."""
        # Mock parent's to_python to return None
        with mock.patch.object(WagtailImageField, "to_python", return_value=None):
            result = self.field.to_python(None)

        self.assertIsNone(result)

    # Tests for py-svg-hush failure paths (Layer 3)
    def test_py_svg_hush_failure_returns_error(self):
        """When py-svg-hush fails to process SVG, should return sanitization error."""
        # Create SVG that passes regex and XML checks but will fail py-svg-hush
        malformed_svg = b"""<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="40"/></svg>"""

        svg_file = SimpleUploadedFile(
            "malformed.svg",
            malformed_svg,
            content_type="image/svg+xml",
        )

        # Mock filter_svg to raise ValueError (py-svg-hush error)
        with mock.patch("bedrock.cms.fields.filter_svg", side_effect=ValueError("Invalid SVG structure")):
            result = self.field._sanitize_svg(svg_file)

        self.assertIsInstance(result, ValidationError)
        self.assertEqual(result.code, "svg_sanitization_error")
        self.assertIn("Invalid SVG structure", str(result))

    def test_py_svg_hush_parse_error_returns_error(self):
        """When py-svg-hush raises ParseError, should return sanitization error."""
        svg_file = SimpleUploadedFile(
            "broken.svg",
            b"<svg><broken></svg>",
            content_type="image/svg+xml",
        )

        # Mock filter_svg to raise ET.ParseError
        with mock.patch("bedrock.cms.fields.filter_svg", side_effect=ET.ParseError("XML parse failed")):
            result = self.field._sanitize_svg(svg_file)

        self.assertIsInstance(result, ValidationError)
        self.assertEqual(result.code, "svg_sanitization_error")

    # Test for file I/O error handling
    def test_os_error_returns_error(self):
        """When file access fails with OSError, should return sanitization error."""
        svg_file = SimpleUploadedFile(
            "test.svg",
            CLEAN_SVG.encode("utf-8"),
            content_type="image/svg+xml",
        )

        # Mock _read_file_content to raise OSError
        with mock.patch.object(self.field, "_read_file_content", side_effect=OSError("Permission denied")):
            result = self.field._sanitize_svg(svg_file)

        self.assertIsInstance(result, ValidationError)
        self.assertEqual(result.code, "svg_sanitization_error")
        self.assertIn("Permission denied", str(result))

    # Tests for malformed XML handling
    def test_malformed_xml_handled_gracefully(self):
        """Malformed XML should not crash _has_dangerous_elements_xml."""
        # Malformed XML that will fail ET.fromstring
        malformed_xml = b"<svg><unclosed><circle/></svg>"

        # Should return False (not crash), allowing layer 3 to handle it
        result = self.field._has_dangerous_elements_xml(malformed_xml)

        self.assertFalse(result)

    def test_severely_malformed_svg_rejected(self):
        """Severely malformed SVG should be rejected by layer 3 (py-svg-hush)."""
        # SVG with mismatched tags that won't parse
        malformed_svg = b"""<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="40">
    <g>
        <rect/>
    <!-- unclosed comment
</svg>"""

        svg_file = SimpleUploadedFile(
            "broken.svg",
            malformed_svg,
            content_type="image/svg+xml",
        )

        result = self.field._sanitize_svg(svg_file)

        # Should fail because py-svg-hush can't parse it
        self.assertIsInstance(result, ValidationError)
        self.assertEqual(result.code, "svg_sanitization_error")

    # Test for alternate SVG content types
    def test_svg_detection_by_alternate_content_types(self):
        """Should detect SVG by all allowed content types."""
        # Test "image/svg" content type
        svg_file_1 = SimpleUploadedFile(
            "test.txt",  # Wrong extension to test content type detection
            CLEAN_SVG.encode("utf-8"),
            content_type="image/svg",
        )
        self.assertTrue(self.field._is_svg_file(svg_file_1))

        # Test "text/xml" content type
        svg_file_2 = SimpleUploadedFile(
            "test.txt",
            CLEAN_SVG.encode("utf-8"),
            content_type="text/xml",
        )
        self.assertTrue(self.field._is_svg_file(svg_file_2))
