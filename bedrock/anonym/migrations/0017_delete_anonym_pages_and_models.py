# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations

ANONYM_PAGE_MODELS = [
    "anonymcasestudyitempage",
    "anonymcasestudypage",
    "anonymcontactpage",
    "anonymcontentsubpage",
    "anonymindexpage",
    "anonymnewsitempage",
    "anonymnewspage",
]


def delete_anonym_pages(apps, schema_editor):
    # Use the real Page model rather than the historical one so that treebeard
    # removes descendants and keeps parent numchild counts correct. The
    # anonym_* tables have already been dropped by this point, so only the
    # wagtailcore_page rows (plus their revisions etc) remain to be removed.
    from wagtail.models import Page

    ContentType = apps.get_model("contenttypes", "ContentType")
    content_type_ids = ContentType.objects.filter(app_label="anonym", model__in=ANONYM_PAGE_MODELS).values_list("id", flat=True)
    anonym_pages = Page.objects.filter(content_type_id__in=list(content_type_ids))

    # Only delete the top-most Anonym pages; deleting them removes their descendants too
    anonym_paths = list(anonym_pages.values_list("path", flat=True))
    top_level_ids = [
        page_id for page_id, path in anonym_pages.values_list("id", "path") if not any(path != other and path.startswith(other) for other in anonym_paths)
    ]
    Page.objects.filter(id__in=top_level_ids).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("anonym", "0016_populate_analytics_ids"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("wagtailcore", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(name="AnonymCaseStudyItemPage"),
        migrations.DeleteModel(name="AnonymCaseStudyPage"),
        migrations.DeleteModel(name="AnonymContactPage"),
        migrations.DeleteModel(name="AnonymContentSubPage"),
        migrations.DeleteModel(name="AnonymIndexPage"),
        migrations.DeleteModel(name="AnonymNewsItemPage"),
        migrations.DeleteModel(name="AnonymNewsPage"),
        migrations.DeleteModel(name="Person"),
        migrations.RunPython(delete_anonym_pages, migrations.RunPython.noop),
    ]
