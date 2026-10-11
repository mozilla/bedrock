# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations


def delete_anonym_pages(apps, schema_editor):
    # Use the real Page model so treebeard's queryset delete removes
    # descendants and keeps parent numchild counts correct. The anonym_*
    # tables were dropped by the DeleteModel operations above.
    from wagtail.models import Page

    Page.objects.filter(content_type__app_label="anonym").delete()

    # Remove the stale content types so Revision, ReferenceIndex, Permission
    # and wagtail_localize rows pointing at them cascade away too.
    ContentType = apps.get_model("contenttypes", "ContentType")
    ContentType.objects.filter(app_label="anonym").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("anonym", "0016_populate_analytics_ids"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("wagtailcore", "0097_baselogentry_uuid_action_timestamp_indexes"),
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
