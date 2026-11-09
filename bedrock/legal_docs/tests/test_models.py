# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from pathlib import Path
from unittest.mock import patch

from django.db import DatabaseError

import pytest

from bedrock.legal_docs.models import (
    LegalDoc,
    LegalDocsManager,
    is_legacy_layout,
    process_md_file,
    snake_case,
)

MODELS_LOGGER = "bedrock.legal_docs.models"


def warnings_logged(caplog):
    return [record for record in caplog.records if record.name == MODELS_LOGGER]


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

    def test_missing_file_is_logged(self, tmp_path, caplog):
        doc = tmp_path / "en" / "nope.md"
        with caplog.at_level(logging.WARNING, logger=MODELS_LOGGER):
            process_md_file(doc)
        (record,) = warnings_logged(caplog)
        assert record.levelname == "WARNING"
        assert str(doc) in record.getMessage()
        assert "No such file or directory" in record.getMessage()

    def test_non_utf8_file_is_logged(self, tmp_path, caplog):
        doc = tmp_path / "notice.md"
        doc.write_bytes("café naïve".encode("latin-1"))
        with caplog.at_level(logging.WARNING, logger=MODELS_LOGGER):
            process_md_file(doc)
        (record,) = warnings_logged(caplog)
        assert record.levelname == "WARNING"
        assert str(doc) in record.getMessage()
        assert "codec can't decode byte" in record.getMessage()

    @pytest.mark.parametrize("encoding", ["utf-16-le", "utf-16-be"])
    def test_utf16_file_without_bom_is_none(self, tmp_path, encoding):
        doc = tmp_path / "notice.md"
        doc.write_bytes("# Privacy Notice".encode(encoding))
        assert process_md_file(doc) is None

    def test_nul_character_is_logged(self, tmp_path, caplog):
        doc = write_doc(tmp_path, "en", "notice", "Legal\x00ese")
        with caplog.at_level(logging.WARNING, logger=MODELS_LOGGER):
            assert process_md_file(doc) is None
        (record,) = warnings_logged(caplog)
        assert str(doc) in record.getMessage()
        assert "NUL" in record.getMessage()

    def test_good_file_logs_nothing(self, tmp_path, caplog):
        with caplog.at_level(logging.WARNING, logger=MODELS_LOGGER):
            process_md_file(write_doc(tmp_path, "en", "notice", "Legalese"))
        assert warnings_logged(caplog) == []

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


class TestIsLegacyLayout:
    def test_legacy_layout_is_doc_name_then_locale(self):
        assert is_legacy_layout(Path("/repo/websites_privacy_notice/de.md")) is True

    def test_new_layout_is_locale_then_doc_name(self):
        assert is_legacy_layout(Path("/repo/de/websites_privacy_notice.md")) is False

    def test_locales_with_a_region_are_recognised(self):
        assert is_legacy_layout(Path("/repo/websites_privacy_notice/en-US.md")) is True
        assert is_legacy_layout(Path("/repo/firefox_privacy_notice/es-ES_b.md")) is True


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

    def test_empty_doc_is_logged(self, tmp_path, settings, caplog):
        settings.LEGAL_DOCS_PATH = tmp_path
        doc = write_doc(tmp_path, "de", "websites_privacy_notice", "")

        with caplog.at_level(logging.WARNING, logger=MODELS_LOGGER):
            LegalDoc.objects.refresh()

        (record,) = warnings_logged(caplog)
        assert str(doc) in record.getMessage()
        assert "is empty" in record.getMessage()

    def test_unreadable_doc_is_logged_once(self, tmp_path, settings, caplog):
        settings.LEGAL_DOCS_PATH = tmp_path
        (tmp_path / "de").mkdir()
        (tmp_path / "de" / "websites_privacy_notice.md").write_bytes("café".encode("latin-1"))

        with caplog.at_level(logging.WARNING, logger=MODELS_LOGGER):
            LegalDoc.objects.refresh()

        assert len(warnings_logged(caplog)) == 1

    def test_doc_with_nul_does_not_abort_the_run(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice")
        write_doc(tmp_path, "de", "websites_privacy_notice", "Legal\x00ese")

        assert LegalDoc.objects.refresh() == (1, 1)
        assert LegalDoc.objects.values_list("name", "locale").get() == ("websites_privacy_notice", "en")

    @pytest.mark.parametrize(
        "locale, doc_name",
        [
            ("ast-ES", "websites_privacy_notice"),
            ("ja-JP_m", "websites_privacy_notice"),
            ("de", "x" * 101),
        ],
    )
    def test_overlong_name_or_locale_is_counted_and_skipped(self, tmp_path, settings, caplog, locale, doc_name):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice")
        doc = write_doc(tmp_path, locale, doc_name)

        with caplog.at_level(logging.WARNING, logger=MODELS_LOGGER):
            assert LegalDoc.objects.refresh() == (1, 1)

        assert LegalDoc.objects.values_list("name", "locale").get() == ("websites_privacy_notice", "en")
        (record,) = warnings_logged(caplog)
        assert str(doc) in record.getMessage()

    def test_name_and_locale_at_the_limit_are_loaded(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "es-ES", "x" * 100)

        assert LegalDoc.objects.refresh() == (1, 0)

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

    def test_doc_in_both_layouts_is_stored_once(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice", "# New layout")
        write_doc(tmp_path, "websites_privacy_notice", "en", "# Legacy layout")

        assert LegalDoc.objects.refresh() == (1, 0)
        assert LegalDoc.objects.values_list("name", "locale").get() == ("websites_privacy_notice", "en")

    def test_new_layout_wins_over_the_legacy_copy(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice", "# New layout")
        write_doc(tmp_path, "websites_privacy_notice", "en", "# Legacy layout")

        LegalDoc.objects.refresh()
        assert "New layout" in LegalDoc.objects.get().content

    def test_new_layout_wins_whatever_order_the_files_arrive_in(self, tmp_path, settings):
        # glob order is down to the filesystem, so hand refresh() the awkward order
        settings.LEGAL_DOCS_PATH = tmp_path
        new = write_doc(tmp_path, "en", "websites_privacy_notice", "# New layout")
        legacy = write_doc(tmp_path, "websites_privacy_notice", "en", "# Legacy layout")

        with patch.object(Path, "glob", return_value=[legacy, new]):
            LegalDoc.objects.refresh()

        assert "New layout" in LegalDoc.objects.get().content

    def test_duplicate_doc_no_longer_breaks_get_doc(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        settings.PROD_LANGUAGES = ["en-US", "de"]
        write_doc(tmp_path, "en", "websites_privacy_notice", "# New layout")
        write_doc(tmp_path, "websites_privacy_notice", "en", "# Legacy layout")

        LegalDoc.objects.refresh()
        assert "New layout" in LegalDoc.objects.get_doc("websites_privacy_notice", "en")["content"]

    def test_ignored_duplicate_is_logged(self, tmp_path, settings, caplog):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice", "# New layout")
        legacy = write_doc(tmp_path, "websites_privacy_notice", "en", "# Legacy layout")

        with caplog.at_level(logging.WARNING, logger=MODELS_LOGGER):
            LegalDoc.objects.refresh()

        (record,) = warnings_logged(caplog)
        assert str(legacy) in record.getMessage()
        assert "duplicates" in record.getMessage()

    def test_unreadable_copy_does_not_shut_out_the_other_layout(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice", "")
        write_doc(tmp_path, "websites_privacy_notice", "en", "# Legacy layout")

        assert LegalDoc.objects.refresh() == (1, 1)
        assert "Legacy layout" in LegalDoc.objects.get().content

    def test_duplicate_is_not_counted_as_an_error(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice", "# New layout")
        write_doc(tmp_path, "websites_privacy_notice", "en", "# Legacy layout")

        assert LegalDoc.objects.refresh()[1] == 0

    def test_same_doc_in_different_locales_is_not_deduplicated(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "en", "websites_privacy_notice", "# English")
        write_doc(tmp_path, "websites_privacy_notice", "de", "# German")

        assert LegalDoc.objects.refresh() == (2, 0)
        assert set(LegalDoc.objects.values_list("name", "locale")) == {
            ("websites_privacy_notice", "en"),
            ("websites_privacy_notice", "de"),
        }

    def test_duplicates_across_mapped_locales_are_caught(self, tmp_path, settings):
        settings.LEGAL_DOCS_PATH = tmp_path
        write_doc(tmp_path, "hi", "websites_privacy_notice", "# New layout")
        write_doc(tmp_path, "websites_privacy_notice", "hi", "# Legacy layout")

        assert LegalDoc.objects.refresh() == (1, 0)
        assert LegalDoc.objects.values_list("name", "locale").get() == ("websites_privacy_notice", "hi-IN")

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
