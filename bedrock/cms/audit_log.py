# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Send each new Wagtail audit log entry, and each user deletion, to the `audit.wagtail` logger
as one JSON line.

Wagtail's own log tables can be edited by anyone with database access and are rolled back by
a database restore. These lines go to centralised logging, which keeps them unchanged, so they
are the authoritative record and the tables are a working view of it.

Actors are identified by user ID only. The user-deletion line is the one place an email
address appears, so the ID can still be traced to a person once their account is gone.
"""

import json
import logging
from datetime import UTC, datetime
from functools import partial

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from wagtail.log_actions import get_active_log_context
from wagtail.models import ModelLogEntry, PageLogEntry

audit_logger = logging.getLogger("audit.wagtail")


def format_log_entry(log_entry: PageLogEntry | ModelLogEntry) -> str:
    """Return the JSON line that records one Wagtail audit log entry."""
    content_type_label = None
    if log_entry.content_type_id:
        content_type = ContentType.objects.get_for_id(log_entry.content_type_id)
        content_type_label = f"{content_type.app_label}.{content_type.model}"

    # Wagtail labels entries about a user with str(user), the username, and usernames here are email addresses
    is_about_a_user = content_type_label == settings.AUTH_USER_MODEL.lower()

    return json.dumps(
        {
            "event": "wagtail.audit",
            "tenant": settings.AUDIT_LOG_TENANT,
            "environment": settings.AUDIT_LOG_ENVIRONMENT,
            "log_model": type(log_entry).__name__,
            "log_entry_id": log_entry.pk,
            "timestamp": log_entry.timestamp.astimezone(UTC).isoformat(),
            "action": log_entry.action,
            "user_id": log_entry.user_id,
            "content_type": content_type_label,
            # A string for both models, so the field keeps a single type wherever the lines are queried
            "object_id": str(log_entry.page_id) if isinstance(log_entry, PageLogEntry) else log_entry.object_id,
            "label": None if is_about_a_user else log_entry.label,
            "uuid": str(log_entry.uuid) if log_entry.uuid else None,
            "revision_id": log_entry.revision_id,
            "content_changed": log_entry.content_changed,
            "deleted": log_entry.deleted,
            "data": log_entry.data,
        },
        cls=DjangoJSONEncoder,
    )


# Each line is sent once the transaction commits, so an action that rolls back leaves no line behind.


@receiver(post_save, sender=PageLogEntry, dispatch_uid="audit_log_page_log_entry_saved")
@receiver(post_save, sender=ModelLogEntry, dispatch_uid="audit_log_model_log_entry_saved")
def send_new_log_entry(sender, instance, created, using, **kwargs):
    if created:
        transaction.on_commit(partial(audit_logger.info, format_log_entry(instance)), using=using)


@receiver(pre_delete, sender=get_user_model(), dispatch_uid="audit_log_user_deleted")
def send_user_deletion(sender, instance, using, **kwargs):
    # Wagtail's admin sets the acting user on the log context for every admin view
    acting_user = get_active_log_context().user
    user_deleted_line = json.dumps(
        {
            "event": "wagtail.audit.user_deleted",
            "tenant": settings.AUDIT_LOG_TENANT,
            "environment": settings.AUDIT_LOG_ENVIRONMENT,
            "timestamp": datetime.now(UTC).isoformat(),
            "user_id": instance.pk,
            "user_email": instance.email,
            "deleted_by_user_id": getattr(acting_user, "pk", None),
        }
    )
    transaction.on_commit(partial(audit_logger.info, user_deleted_line), using=using)
