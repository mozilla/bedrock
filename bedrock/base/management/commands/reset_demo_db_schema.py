# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# yourapp/management/commands/reset_schema.py
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from bedrock.base.config_manager import config


class Command(BaseCommand):
    help = "Drop and recreate the public schema (PostgreSQL only; for use on Cloud Run demos ONLY)."

    def handle(self, *args, **options):
        if not config("IS_DEMO", parser=bool, default="false"):
            raise CommandError("This may only be run on demos")

        if connection.vendor != "postgresql":
            raise CommandError("reset_schema only supports PostgreSQL")

        with connection.cursor() as cur:
            cur.execute("DROP SCHEMA IF EXISTS public CASCADE;")
            cur.execute("CREATE SCHEMA public AUTHORIZATION CURRENT_USER;")
        self.stdout.write(self.style.SUCCESS("Reset public schema"))
