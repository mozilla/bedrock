# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations

from wagtail.blocks.migrations.migrate_operation import MigrateStreamData
from wagtail.blocks.migrations.operations import BaseBlockOperation


class SetDefaultHeadingSizeOperation(BaseBlockOperation):
    """Keep springboard headings created before heading_size existed at their original small size."""

    def apply(self, block_value):
        if "heading_size" not in block_value:
            return {**block_value, "heading_size": "m24-t-sm"}
        return block_value

    @property
    def operation_name_fragment(self):
        return "set_default_heading_size"


class Migration(migrations.Migration):
    dependencies = [
        ("mozorg", "0051_springboard_editor_ux"),
    ]

    operations = [
        MigrateStreamData(
            app_name="mozorg",
            model_name="HomePage",
            field_name="content",
            operations_and_block_paths=[
                (SetDefaultHeadingSizeOperation(), "springboard_block.settings"),
            ],
        ),
    ]
