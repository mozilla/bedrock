# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Recreates wagtail_localize Translation/TranslationSource/StringTranslation records
from exported page and snippet data.

After a DB export via bin/export-db-to-sqlite.sh, the wagtail_localize tables are
empty (they are excluded from the export to avoid leaking draft content from
TranslationSource.content_json). This command recreates the minimal structural
records needed for wagtail-localize to recognise translated pages as connected,
using only the live published content that is already in the export.

Source page identification: within a group of pages sharing the same translation_key,
the page with the lowest primary key is treated as the source (it was created first;
translated copies received higher PKs).

StringTranslation reconstruction: extract_segments() is run on each target page and
matched to the source's StringSegment records by context path. Block UUIDs are
preserved through the standard wagtail-localize workflow, so paths match correctly.
"""

import warnings
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction

import polib
from bs4 import MarkupResemblesLocatorWarning
from wagtail.blocks import CharBlock, ListBlock, StreamBlock, StructBlock, TextBlock
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail_localize.models import StringSegment, Translation, TranslationSource
from wagtail_localize.segments.extract import extract_segments
from wagtail_localize.segments.types import StringSegmentValue

from bedrock.anonym.models import Person
from bedrock.mozorg.models import ContactBannerSnippet
from bedrock.products.models import MonitorCallToActionSnippet, VPNCallToActionSnippet

# Suppress spurious BeautifulSoup warning that fires when wagtail-localize
# processes URL strings (e.g. custom_url in link blocks). The round-trip is
# correct; the warning is purely cosmetic.
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

TRANSLATABLE_SNIPPET_MODELS = [
    ContactBannerSnippet,
    VPNCallToActionSnippet,
    MonitorCallToActionSnippet,
    Person,
]


class Command(BaseCommand):
    help = (
        "Recreates wagtail_localize Translation/TranslationSource/StringTranslation records "
        "from exported page and snippet data so that translated pages appear connected."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without making any changes.",
        )
        parser.add_argument(
            "--skip-string-translations",
            action="store_true",
            help=(
                "Only create structural linking records (TranslationSource + Translation) "
                "without recreating StringTranslation records. Faster, but the translation "
                "editor will show untranslated strings."
            ),
        )
        parser.add_argument(
            "--pages",
            help=(
                "Comma-separated list of page IDs to process. Each ID's full translation "
                "group (source + all translated copies) is included. If omitted, all "
                "multi-locale page groups are processed."
            ),
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        skip_strings = options["skip_string_translations"]

        page_ids_filter = None
        if options["pages"]:
            try:
                page_ids_filter = {int(pk) for pk in options["pages"].split(",")}
            except ValueError:
                raise SystemExit("ERROR: --pages must be a comma-separated list of integers, e.g. --pages 1,2,3")

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN — no changes will be made."))

        totals = {"sources": 0, "translations": 0, "string_translations": 0, "errors": 0}

        self._process_pages(dry_run, skip_strings, totals, page_ids_filter)
        self._process_snippets(dry_run, skip_strings, totals)

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. TranslationSources: {totals['sources']}, "
                f"Translations: {totals['translations']}, "
                f"StringTranslations: {totals['string_translations']}, "
                f"Errors: {totals['errors']}"
            )
        )

    def _process_pages(self, dry_run, skip_strings, totals, page_ids_filter=None):
        self.stdout.write("Processing pages...")

        # Group page ids by translation_key. We fetch id+translation_key+locale_id
        # in one query, then filter to groups with >1 distinct locale in Python.
        # (The equivalent .values().annotate().filter() ORM query silently returns
        # an empty result set when evaluated in some Django/SQLite combinations.)
        groups = defaultdict(list)
        for page_id, tk, lid in Page.objects.order_by("id").values_list("id", "translation_key", "locale_id"):
            groups[tk].append((page_id, lid))

        multi_locale_keys = [(tk, [pid for pid, _ in entries]) for tk, entries in groups.items() if len({lid for _, lid in entries}) > 1]

        if page_ids_filter:
            multi_locale_keys = [(tk, ids) for tk, ids in multi_locale_keys if page_ids_filter.intersection(ids)]
            self.stdout.write(f"  Found {len(multi_locale_keys)} multi-locale page groups matching --page_ids filter.")
        else:
            self.stdout.write(f"  Found {len(multi_locale_keys)} multi-locale page groups.")

        if not multi_locale_keys:
            return

        # Batch-fetch all specific page instances across all groups in bulk (one query
        # per content type), rather than one query per page via the .specific property.
        # Also pre-fetch locales from the base Page table (which supports select_related)
        # and populate the FK cache on specific instances to avoid per-instance queries.
        all_page_ids = [pid for _, ids in multi_locale_keys for pid in ids]
        locale_by_id = {p.id: p.locale for p in Page.objects.filter(id__in=all_page_ids).select_related("locale")}
        specific_by_id = {p.pk: p for p in Page.objects.filter(id__in=all_page_ids).specific()}
        for page_id, page in specific_by_id.items():
            page.__dict__["locale"] = locale_by_id[page_id]

        for i, (translation_key, page_ids) in enumerate(multi_locale_keys, 1):
            source_page = specific_by_id[page_ids[0]]
            target_pages = [specific_by_id[pid] for pid in page_ids[1:]]

            self.stdout.write(
                f"  [{i}/{len(multi_locale_keys)}] {source_page} "
                f"({source_page.locale.language_code}) → " + ", ".join(f"{p} ({p.locale.language_code})" for p in target_pages)
            )
            self._process_group(source_page, target_pages, dry_run, skip_strings, totals)

    def _process_snippets(self, dry_run, skip_strings, totals):
        for Model in TRANSLATABLE_SNIPPET_MODELS:
            groups = defaultdict(list)
            for inst_id, tk, lid in Model.objects.order_by("id").values_list("id", "translation_key", "locale_id"):
                groups[tk].append((inst_id, lid))

            multi_locale_keys = [(tk, [iid for iid, _ in entries]) for tk, entries in groups.items() if len({lid for _, lid in entries}) > 1]

            self.stdout.write(f"Processing {Model.__name__} snippets ({len(multi_locale_keys)} multi-locale groups)...")

            for i, (translation_key, inst_ids) in enumerate(multi_locale_keys, 1):
                instances = list(Model.objects.filter(id__in=inst_ids).select_related("locale").order_by("id"))
                source_instance = instances[0]
                target_instances = instances[1:]

                self.stdout.write(
                    f"  [{i}/{len(multi_locale_keys)}] {source_instance} "
                    f"({source_instance.locale.language_code}) → " + ", ".join(f"{t} ({t.locale.language_code})" for t in target_instances)
                )
                self._process_group(source_instance, target_instances, dry_run, skip_strings, totals)

    def _process_group(self, source_instance, target_instances, dry_run, skip_strings, totals):
        try:
            with transaction.atomic():
                if dry_run:
                    self.stdout.write(f"  Would link: {source_instance} → " + ", ".join(str(t) for t in target_instances))
                    return

                # Coerce None CharBlock/TextBlock values to '' so extract_segments()
                # doesn't crash on optional block fields left unset (e.g. anchor_id).
                _sanitize_stream_fields(source_instance)

                translation_source, source_created = TranslationSource.get_or_create_from_instance(source_instance)
                if source_created:
                    totals["sources"] += 1

                # Fetch source StringSegments once per group; they are identical for every
                # target locale so there is no need to re-query inside the target loop.
                source_segs = (
                    list(StringSegment.objects.filter(source=translation_source).select_related("string", "context")) if not skip_strings else []
                )

                for target_instance in target_instances:
                    translation, trans_created = Translation.objects.get_or_create(
                        source=translation_source,
                        target_locale=target_instance.locale,
                        defaults={"enabled": True},
                    )
                    if trans_created:
                        totals["translations"] += 1

                    if not skip_strings:
                        _sanitize_stream_fields(target_instance)
                        count = _infer_string_translations(translation, source_segs, target_instance)
                        totals["string_translations"] += count

        except Exception as exc:
            self.stderr.write(
                self.style.ERROR(f"  Error processing group for {source_instance} (translation_key={source_instance.translation_key}): {exc}")
            )
            totals["errors"] += 1


def _fix_none_in_struct(block_type, struct_value):
    """
    Recursively coerce None CharBlock/TextBlock values to '' within a StructValue.
    Modifies the StructValue in place. Called only for StructBlock types.
    """
    for field_name, child_val in struct_value.items():
        child_block = block_type.child_blocks.get(field_name)
        if child_block is None:
            continue
        if isinstance(child_block, (CharBlock, TextBlock)) and child_val is None:
            struct_value[field_name] = ""
        elif isinstance(child_block, StructBlock) and child_val is not None:
            _fix_none_in_struct(child_block, child_val)
        elif isinstance(child_block, StreamBlock) and child_val is not None:
            _fix_none_in_stream(child_block, child_val)
        elif isinstance(child_block, ListBlock) and child_val is not None:
            for item in child_val:
                if isinstance(child_block.child_block, StructBlock):
                    _fix_none_in_struct(child_block.child_block, item)


def _fix_none_in_stream(block_type, stream_value):
    """
    Recursively coerce None CharBlock/TextBlock values to '' within a StreamValue.
    """
    for bound_block in stream_value:
        child_block = block_type.child_blocks.get(bound_block.block_type)
        if child_block is None:
            continue
        if isinstance(child_block, StructBlock) and bound_block.value is not None:
            _fix_none_in_struct(child_block, bound_block.value)
        elif isinstance(child_block, StreamBlock) and bound_block.value is not None:
            _fix_none_in_stream(child_block, bound_block.value)


def _sanitize_stream_fields(instance):
    """
    Coerce None CharBlock/TextBlock values to '' in all StreamField fields of an
    instance. wagtail-localize's extract_segments() raises TypeError when it
    encounters a None CharBlock value (e.g. an optional anchor_id left unset);
    defaulting to '' avoids this without touching the database.
    """
    for field in instance._meta.get_fields():
        if isinstance(field, StreamField):
            stream_value = getattr(instance, field.name)
            if stream_value is not None:
                _fix_none_in_stream(field.stream_block, stream_value)


def _infer_string_translations(translation, source_segs, target_instance):
    """
    Extracts translatable strings from the target instance and imports them as
    StringTranslation records by matching context paths with the source's segments.

    source_segs is a pre-fetched list of StringSegment objects (with string and context
    select_related) for the translation source; callers fetch it once per group.

    Returns the number of string translations imported.
    """
    # Use a walrus operator so render_html() is called once per segment, not twice.
    # (is_empty() calls render_html() internally; the dict value called it again.)
    target_segs_by_path = {
        seg.path: html for seg in extract_segments(target_instance) if isinstance(seg, StringSegmentValue) and (html := seg.render_html())
    }

    if not target_segs_by_path:
        return 0

    po = polib.POFile(wrapwidth=200)
    po.metadata = {
        "MIME-Version": "1.0",
        "Content-Type": "text/plain; charset=utf-8",
        "X-WagtailLocalize-TranslationID": str(translation.uuid),
    }

    for source_seg in source_segs:
        translated_html = target_segs_by_path.get(source_seg.context.path)
        if translated_html and translated_html != source_seg.string.data:
            po.append(
                polib.POEntry(
                    msgid=source_seg.string.data,
                    msgctxt=source_seg.context.path,
                    msgstr=translated_html,
                )
            )

    if not po:
        return 0

    translation.import_po(po, delete=False, translation_type="manual", tool_name="export_reconstruction")
    return len(po)
