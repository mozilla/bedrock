# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.db import DatabaseError

import pytest

from bedrock.legal_docs.models import (
    LegalDoc,
    LegalDocsManager,
    process_md_file,
    snake_case,
)


def write_doc(root, locale, doc_name, content="# Legalese"):
    """Write a legal doc into the repo layout `<root>/<locale>/<doc_name>.md`."""
    doc_dir = root / locale
    doc_dir.mkdir(parents=True, exist_ok=True)
    doc_file = doc_dir / f"{doc_name}.md"
    doc_file.write_text(content, encoding="utf-8")
    return doc_file


class TestProcessMdFile:
    def test_markdown_is_converted_to_html(self, tmp_path):
        doc = write_doc(tmp_path, "en", "notice", "Some *emphasis* and a [link](https://example.com/).")
        assert process_md_file(doc) == '<p>Some <em>emphasis</em> and a <a href="https://example.com/">link</a>.</p>'

    def test_headings_are_given_ids(self, tmp_path):
        doc = write_doc(tmp_path, "en", "notice", "# Privacy Notice")
        assert '<h1 id="privacy-notice">Privacy Notice</h1>' in process_md_file(doc)

    def test_attribute_lists_are_applied(self, tmp_path):
        doc = write_doc(tmp_path, "en", "notice", "## Data We Collect {: .fancy }")
        assert '<h2 class="fancy" id="data-we-collect">Data We Collect</h2>' in process_md_file(doc)

    def test_tables_are_rendered(self, tmp_path):
        doc = write_doc(tmp_path, "en", "notice", "| a | b |\n|---|---|\n| 1 | 2 |")
        content = process_md_file(doc)
        assert "<table>" in content
        assert "<th>a</th>" in content
        assert "<td>1</td>" in content

    def test_headings_are_wrapped_in_nested_sections(self, tmp_path):
        doc = write_doc(tmp_path, "en", "notice", "# Top\n\ncontent\n\n## Sub\n\nmore")
        content = process_md_file(doc)
        assert '<section class="section1">' in content
        assert '<section class="section2">' in content

    def test_non_ascii_content_survives_the_round_trip(self, tmp_path):
        doc = write_doc(tmp_path, "de", "notice", "Datenschutzerklärung — ✓")
        assert process_md_file(doc) == "<p>Datenschutzerklärung — ✓</p>"

    def test_missing_file_is_none(self, tmp_path):
        assert process_md_file(tmp_path / "en" / "nope.md") is None

    def test_unreadable_path_is_none(self, tmp_path):
        # any OSError is swallowed; a directory stands in for a path that cannot be opened
        assert process_md_file(tmp_path) is None

    def test_non_utf8_file_is_none(self, tmp_path):
        doc = tmp_path / "notice.md"
        doc.write_bytes("café naïve".encode("latin-1"))
        assert process_md_file(doc) is None

    def test_binary_file_is_none(self, tmp_path):
        doc = tmp_path / "notice.md"
        doc.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")
        assert process_md_file(doc) is None

    def test_empty_file_is_empty_string(self, tmp_path):
        # falsy but not None, which is what refresh() counts as an error
        assert process_md_file(write_doc(tmp_path, "en", "notice", "")) == ""

    def test_whitespace_only_file_is_empty_string(self, tmp_path):
        assert process_md_file(write_doc(tmp_path, "en", "notice", "   \n\n")) == ""

    def test_path_is_accepted_as_a_string(self, tmp_path):
        doc = write_doc(tmp_path, "en", "notice", "Legalese")
        assert process_md_file(str(doc)) == "<p>Legalese</p>"


class TestSnakeCase:
    def test_hyphens_become_underscores(self):
        assert snake_case("websites-privacy-notice") == "websites_privacy_notice"

    def test_name_is_lowercased(self):
        assert snake_case("WebRTC-ToS") == "webrtc_tos"

    def test_snake_case_name_is_unchanged(self):
        assert snake_case("websites_privacy_notice") == "websites_privacy_notice"


@pytest.mark.django_db
class TestRefresh:
    def test_docs_are_loaded_from_the_repo(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice", "# Privacy")
        write_doc(tmp_path, "de", "websites_privacy_notice", "# Datenschutz")

        assert LegalDoc.objects.refresh() == (2, 0)
        assert set(LegalDoc.objects.values_list("name", "locale")) == {
            ("websites_privacy_notice", "en"),
            ("websites_privacy_notice", "de"),
        }

    def test_content_is_the_rendered_html(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice", "Legalese")

        LegalDoc.objects.refresh()
        assert LegalDoc.objects.get(name="websites_privacy_notice").content == "<p>Legalese</p>"

    def test_stale_docs_are_removed(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        LegalDoc.objects.create(name="retired_notice", locale="en", content="<p>Gone</p>")
        write_doc(tmp_path, "en", "websites_privacy_notice")

        assert LegalDoc.objects.refresh() == (1, 0)
        assert not LegalDoc.objects.filter(name="retired_notice").exists()

    def test_unprocessable_docs_are_counted_and_skipped(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice")
        write_doc(tmp_path, "en", "empty_notice", "")

        assert LegalDoc.objects.refresh() == (1, 1)
        assert list(LegalDoc.objects.values_list("name", flat=True)) == ["websites_privacy_notice"]

    def test_one_bad_doc_does_not_abort_the_run(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice")
        (tmp_path / "de").mkdir()
        (tmp_path / "de" / "websites_privacy_notice.md").write_bytes("café".encode("latin-1"))

        assert LegalDoc.objects.refresh() == (1, 1)
        assert LegalDoc.objects.values_list("name", "locale").get() == ("websites_privacy_notice", "en")

    def test_non_markdown_files_are_ignored(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice")
        (tmp_path / "en" / "README.txt").write_text("not a doc", encoding="utf-8")

        assert LegalDoc.objects.refresh() == (1, 0)

    def test_only_files_one_directory_deep_are_loaded(self, tmp_path, settings):
        # the glob is "*/*.md", so docs at the root or nested deeper are not picked up
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice")
        (tmp_path / "top_level.md").write_text("# Top", encoding="utf-8")
        write_doc(tmp_path / "en", "nested", "too_deep")

        assert LegalDoc.objects.refresh() == (1, 0)
        assert list(LegalDoc.objects.values_list("name", flat=True)) == ["websites_privacy_notice"]

    def test_legacy_repo_layout_is_loaded(self, tmp_path, settings):
        # the old layout is `<doc_name>/<locale>.md`, which get_data_from_file_path flips back
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "websites_privacy_notice", "de")

        assert LegalDoc.objects.refresh() == (1, 0)
        assert LegalDoc.objects.values_list("name", "locale").get() == ("websites_privacy_notice", "de")

    def test_legal_docs_locales_are_mapped_to_bedrock_locales(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "hi", "websites_privacy_notice")

        LegalDoc.objects.refresh()
        assert LegalDoc.objects.get(name="websites_privacy_notice").locale == "hi-IN"

    def test_missing_docs_path_loads_nothing(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path / "not-checked-out"

        assert LegalDoc.objects.refresh() == (0, 0)

    def test_empty_repo_wipes_the_table(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        LegalDoc.objects.create(name="websites_privacy_notice", locale="en", content="<p>Legalese</p>")

        assert LegalDoc.objects.refresh() == (0, 0)
        assert not LegalDoc.objects.exists()

    def test_existing_docs_survive_a_failed_load(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        LegalDoc.objects.create(name="websites_privacy_notice", locale="en", content="<p>Legalese</p>")
        write_doc(tmp_path, "de", "websites_privacy_notice")

        with patch.object(LegalDocsManager, "bulk_create", side_effect=DatabaseError("nope")):
            with pytest.raises(DatabaseError):
                LegalDoc.objects.refresh()

        # the delete at the top of refresh() is rolled back with the rest of the atomic block
        assert LegalDoc.objects.values_list("name", "locale").get() == ("websites_privacy_notice", "en")


class TestLegalDocStr:
    def test_str_is_name_and_locale(self):
        doc = LegalDoc(name="websites_privacy_notice", locale="de", content="<p>Legalese</p>")
        assert str(doc) == "websites_privacy_notice - de"
