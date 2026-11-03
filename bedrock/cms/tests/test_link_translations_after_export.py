# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command

import pytest
from wagtail.models import Page, Site
from wagtail_localize.models import StringSegment, StringTranslation, Translation, TranslationSource
from wagtail_localize.segments.extract import extract_segments

from bedrock.cms.management.commands import link_translations_after_export
from bedrock.cms.tests.factories import LocaleFactory, SimpleRichTextPageFactory
from bedrock.mozorg.models import AdvertisingIndexPage, ContactBannerSnippet

pytestmark = pytest.mark.django_db


@pytest.fixture
def fr_locale():
    return LocaleFactory(language_code="fr")


def make_page(title, slug, content):
    site = Site.objects.get(is_default_site=True)
    return SimpleRichTextPageFactory(parent=site.root_page, title=title, slug=slug, content=content)


def translate(instance, locale, **fields):
    if isinstance(instance, Page):
        translated = instance.copy_for_translation(locale, copy_parents=True)
    else:
        translated = instance.copy_for_translation(locale)
    for name, value in fields.items():
        setattr(translated, name, value)
    translated.save()
    return translated


@pytest.fixture
def en_page():
    return make_page("Hello", "hello", "<p>Hello world</p>")


@pytest.fixture
def fr_page(en_page, fr_locale):
    return translate(en_page, fr_locale, title="Bonjour", content="<p>Bonjour le monde</p>")


def run(*args):
    out, err = StringIO(), StringIO()
    call_command("link_translations_after_export", *args, stdout=out, stderr=err)
    return out.getvalue(), err.getvalue()


def string_translations(instance, locale):
    return {
        (st.translation_of.data, st.data)
        for st in StringTranslation.objects.filter(context__object_id=instance.translation_key, locale=locale).select_related("translation_of")
    }


def test_translated_page_is_linked_to_its_source(en_page, fr_page, fr_locale):
    run()

    source = TranslationSource.objects.get(object_id=en_page.translation_key)
    assert source.locale == en_page.locale
    assert source.get_source_instance() == en_page
    translation = Translation.objects.get(source=source)
    assert translation.target_locale == fr_locale
    assert translation.enabled is True


def test_translated_strings_are_recreated(en_page, fr_page, fr_locale):
    run()

    assert string_translations(en_page, fr_locale) == {("Hello", "Bonjour"), ("Hello world", "Bonjour le monde")}
    for st in StringTranslation.objects.filter(locale=fr_locale):
        assert st.translation_type == "manual"
        assert st.tool_name == "export_reconstruction"
        assert st.has_error is False


def test_untranslated_strings_are_skipped(en_page, fr_locale):
    translate(en_page, fr_locale, title="Bonjour")

    run()

    assert string_translations(en_page, fr_locale) == {("Hello", "Bonjour")}


def test_untranslated_copy_is_linked_without_strings(en_page, fr_locale):
    translate(en_page, fr_locale)

    run()

    assert Translation.objects.filter(source__object_id=en_page.translation_key, target_locale=fr_locale).exists()
    assert string_translations(en_page, fr_locale) == set()


def test_single_locale_pages_are_left_alone(fr_page):
    en_only_page = make_page("Only English", "only-english", "<p>Hi</p>")

    run()

    assert not TranslationSource.objects.filter(object_id=en_only_page.translation_key).exists()


def test_dry_run_changes_nothing(en_page, fr_page):
    out, _ = run("--dry-run")

    assert out.startswith("DRY RUN")
    assert "Would link: Hello → Bonjour" in out
    assert "Done. TranslationSources: 0, Translations: 0, StringTranslations: 0, Errors: 0" in out
    assert not TranslationSource.objects.exists()
    assert not Translation.objects.exists()
    assert not StringTranslation.objects.exists()


def test_skip_string_translations(en_page, fr_page):
    run("--skip-string-translations")

    assert Translation.objects.filter(source__object_id=en_page.translation_key).exists()
    assert not StringTranslation.objects.exists()


def test_pages_option_limits_the_groups(en_page, fr_page, fr_locale):
    en_about = make_page("About", "about", "<p>About us</p>")
    fr_about = translate(en_about, fr_locale, title="À propos", content="<p>À propos de nous</p>")

    out, _ = run("--pages", str(fr_about.pk))

    assert "Found 1 multi-locale page groups" in out
    assert "Done. TranslationSources: 1, Translations: 1, StringTranslations: 2, Errors: 0" in out
    assert string_translations(en_about, fr_locale) == {("About", "À propos"), ("About us", "À propos de nous")}
    assert not TranslationSource.objects.filter(object_id=en_page.translation_key).exists()


@pytest.mark.parametrize("pages", ["1,two", "1,", "1;2"])
def test_pages_option_must_be_integers(pages):
    with pytest.raises(SystemExit, match="--pages must be a comma-separated list of integers"):
        run("--pages", pages)


def test_rerun_does_not_duplicate_records(en_page, fr_page, fr_locale):
    run()

    out, _ = run()

    assert "TranslationSources: 0, Translations: 0" in out
    assert TranslationSource.objects.filter(object_id=en_page.translation_key).count() == 1
    assert Translation.objects.filter(source__object_id=en_page.translation_key).count() == 1
    assert string_translations(en_page, fr_locale) == {("Hello", "Bonjour"), ("Hello world", "Bonjour le monde")}


def test_rerun_keeps_translations_it_can_no_longer_rebuild(en_page, fr_page, fr_locale):
    run()
    fr_page.title = "Salut"
    fr_page.content = "<p>Bonjour</p><p>le monde</p>"
    fr_page.save()

    run()

    assert string_translations(en_page, fr_locale) == {("Hello", "Salut"), ("Hello world", "Bonjour le monde")}


def test_snippets_are_linked(fr_locale):
    en_banner = ContactBannerSnippet.objects.create(heading="Contact us", button_text="Write to us", button_link="https://example.com/")
    translate(en_banner, fr_locale, heading="Contactez-nous", button_text="Écrivez-nous")

    out, _ = run()

    assert "Processing ContactBannerSnippet snippets (1 multi-locale groups)..." in out
    source = TranslationSource.objects.get(object_id=en_banner.translation_key)
    assert source.get_source_instance() == en_banner
    assert Translation.objects.get(source=source).target_locale == fr_locale
    assert string_translations(en_banner, fr_locale) == {("Contact us", "Contactez-nous"), ("Write to us", "Écrivez-nous")}


def test_failed_group_is_rolled_back_and_reported(en_page, fr_page, fr_locale):
    en_about = make_page("About", "about", "<p>About us</p>")
    translate(en_about, fr_locale, title="À propos")
    infer = link_translations_after_export._infer_string_translations

    def fail_for_hello(translation, source_segs, target_instance):
        if target_instance.pk == fr_page.pk:
            raise ValueError("boom")
        return infer(translation, source_segs, target_instance)

    with patch.object(link_translations_after_export, "_infer_string_translations", side_effect=fail_for_hello):
        out, err = run()

    assert f"Error processing group for Hello (translation_key={en_page.translation_key}): boom" in err
    assert "Errors: 1" in out
    assert not TranslationSource.objects.filter(object_id=en_page.translation_key).exists()
    assert string_translations(en_about, fr_locale) == {("About", "À propos")}


def test_unset_char_blocks_are_blanked_before_extraction():
    page = AdvertisingIndexPage(
        title="Advertising",
        sections=[
            {
                "type": "section",
                "id": "e4b5c0a2-1f5e-4c4e-9a0f-0c6f4b0f8b11",
                "value": {
                    "settings": {"anchor_id": None},
                    "header": {"anchor_id": None, "heading_text": "Reach people"},
                    "content": [
                        {
                            "type": "section_header_block",
                            "id": "0f1d2c3b-4a59-4687-b6a5-c4d3e2f1a0b9",
                            "value": {"anchor_id": None, "heading_text": "Why Mozilla"},
                        }
                    ],
                    "call_to_action": [
                        {
                            "type": "item",
                            "id": "9a8b7c6d-5e4f-4321-8fed-cba987654321",
                            "value": {"text": None, "link_text": "Get in touch"},
                        }
                    ],
                },
            }
        ],
    )
    with pytest.raises(TypeError, match="Got `NoneType`"):
        extract_segments(page)

    link_translations_after_export._sanitize_stream_fields(page)

    section = page.sections[0].value
    assert section["settings"]["anchor_id"] == ""
    assert section["header"]["anchor_id"] == ""
    assert section["content"][0].value["anchor_id"] == ""
    assert section["call_to_action"][0]["text"] == ""
    assert section["header"]["heading_text"] == "Reach people"
    assert section["content"][0].value["heading_text"] == "Why Mozilla"
    extract_segments(page)


def test_page_with_unset_char_blocks_is_linked(fr_locale):
    def sections(subheading):
        value = {"settings": {"anchor_id": None}, "header": {"anchor_id": None, "heading_text": "", "subheading_text": subheading}}
        return json.dumps([{"type": "section", "id": "e4b5c0a2-1f5e-4c4e-9a0f-0c6f4b0f8b11", "value": value}])

    en_page = AdvertisingIndexPage(title="Advertising", slug="advertising", sections=sections("<p>Reach people</p>"))
    Site.objects.get(is_default_site=True).root_page.add_child(instance=en_page)
    translate(en_page, fr_locale, title="Publicité", sections=sections("<p>Touchez les gens</p>"))

    out, err = run()

    assert "Errors: 0" in out, err
    assert string_translations(en_page, fr_locale) == {("Advertising", "Publicité"), ("Reach people", "Touchez les gens")}


def test_rich_text_paragraphs_are_paired_in_order(fr_locale):
    en_page = make_page("Hello", "hello", "<p>Hello world</p><p>Goodbye</p><p>See you</p>")
    translate(en_page, fr_locale, content="<p>Bonjour le monde</p><p>Au revoir</p><p>See you</p>")

    run()

    assert string_translations(en_page, fr_locale) == {("Hello world", "Bonjour le monde"), ("Goodbye", "Au revoir")}


def test_paragraphs_that_no_longer_line_up_are_skipped(fr_locale):
    en_page = make_page("Hello", "hello", "<p>Hello world</p><p>Goodbye</p>")
    translate(en_page, fr_locale, title="Bonjour", content="<p>Bonjour</p><p>le monde</p><p>Au revoir</p>")

    run()

    assert string_translations(en_page, fr_locale) == {("Hello", "Bonjour")}


def test_pairing_does_not_depend_on_the_order_segments_arrive_in(fr_locale):
    en_page = make_page("Hello", "hello", "<p>One</p><p>Two</p><p>Three</p>")
    fr_page = translate(en_page, fr_locale, content="<p>Un</p><p>Deux</p><p>Trois</p>")
    run("--skip-string-translations")
    translation = Translation.objects.get(source__object_id=en_page.translation_key)
    source_segs = list(StringSegment.objects.filter(source=translation.source).select_related("string", "context").order_by("-order"))

    link_translations_after_export._infer_string_translations(translation, source_segs, fr_page)

    assert string_translations(en_page, fr_locale) == {("One", "Un"), ("Two", "Deux"), ("Three", "Trois")}
