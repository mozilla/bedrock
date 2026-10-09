# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import heapq
from datetime import UTC, datetime
from operator import attrgetter

from django.core.management.base import BaseCommand

from wagtail.models import ModelLogEntry, PageLogEntry

from bedrock.cms.audit_log import audit_logger, format_log_entry


def utc_datetime(value: str) -> datetime:
    """Parse an ISO 8601 date or datetime, treating one without an offset as UTC."""
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


class Command(BaseCommand):
    help = (
        "Send existing Wagtail audit log entries to the audit.wagtail logger, oldest first. "
        "Running it again sends them again; log_entry_id identifies the duplicates. "
        "Only a container's main process reaches its log, so run this as its own container "
        "rather than through `kubectl exec`."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--since",
            type=utc_datetime,
            help="Only send entries timestamped at or after this ISO 8601 date or datetime (UTC unless an offset is given)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print the lines that would be sent instead of sending them",
        )

    def handle(self, *args, since, dry_run, **options):
        entries_by_model = []
        for log_entry_model in (PageLogEntry, ModelLogEntry):
            log_entries = log_entry_model.objects.order_by("timestamp", "pk")
            if since:
                log_entries = log_entries.filter(timestamp__gte=since)
            entries_by_model.append(log_entries.iterator())

        sent_count = 0
        for log_entry in heapq.merge(*entries_by_model, key=attrgetter("timestamp")):
            log_line = format_log_entry(log_entry)
            if dry_run:
                self.stdout.write(log_line)
            else:
                audit_logger.info(log_line)
            sent_count += 1

        self.stdout.write(f"{'Would have sent' if dry_run else 'Sent'} {sent_count} audit log entries")
