# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations

STALE_MODELS = (
    "LeadershipPage",
)


def remove_stale_contenttypes(apps, schema_editor):
    # Migration 0043 dropped LeadershipPage
    # but Django doesn't auto-purge the django_content_type rows for deleted models. Anything
    # that resolves a log entry / permission via ContentType.get_object_for_this_type() (e.g.
    # the Wagtail admin home recent-edits panel) then crashes because model_class() is None.
    ContentType = apps.get_model("contenttypes", "ContentType")
    ContentType.objects.filter(app_label="cms", model__in=STALE_MODELS).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("mozorg", "0043_delete_leadershippage"),
    ]

    operations = [
        migrations.RunPython(remove_stale_contenttypes, reverse_code=migrations.RunPython.noop),
    ]
