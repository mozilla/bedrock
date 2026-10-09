# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging
from datetime import UTC, datetime
from io import StringIO
from logging.handlers import BufferingHandler

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.db import transaction

import pytest
from freezegun import freeze_time
from wagtail.log_actions import LogContext, log
from wagtail.models import PageLogEntry

from bedrock.cms.tests.factories import SimpleRichTextPageFactory, WagtailUserFactory
from bedrock.cms.utils import get_cms_environment
from bedrock.settings.base import get_deployment_environment

pytestmark = pytest.mark.django_db


class AbandonedAction(Exception):
    pass


@pytest.fixture
def sent_audit_lines():
    """Return a callable listing the lines sent to the audit.wagtail logger so far, parsed from JSON."""
    collecting_handler = BufferingHandler(capacity=1000)
    audit_logger = logging.getLogger("audit.wagtail")
    audit_logger.addHandler(collecting_handler)
    yield lambda: [json.loads(record.getMessage()) for record in collecting_handler.buffer]
    audit_logger.removeHandler(collecting_handler)


@pytest.fixture
def editor():
    return WagtailUserFactory(username="editor@example.com", email="editor@example.com")


@pytest.fixture
def page():
    return SimpleRichTextPageFactory(title="Audited page")


def test_new_page_log_entry_is_sent_with_every_field(editor, page, sent_audit_lines, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=True):
        log_entry = log(page, "wagtail.edit", user=editor, content_changed=True, data={"note": "kept as-is"})

    assert sent_audit_lines() == [
        {
            "event": "wagtail.audit",
            "tenant": "bedrock",
            "environment": settings.AUDIT_LOG_ENVIRONMENT,
            "log_model": "PageLogEntry",
            "log_entry_id": log_entry.pk,
            "timestamp": log_entry.timestamp.astimezone(UTC).isoformat(),
            "action": "wagtail.edit",
            "user_id": editor.pk,
            "content_type": "cms.simplerichtextpage",
            "object_id": str(page.pk),
            "label": "Audited page",
            "uuid": None,
            "revision_id": None,
            "content_changed": True,
            "deleted": False,
            "data": {"note": "kept as-is"},
        }
    ]


def test_new_model_log_entry_is_sent_with_the_log_context(editor, sent_audit_lines, django_capture_on_commit_callbacks):
    group = Group.objects.create(name="Audit reviewers")

    with django_capture_on_commit_callbacks(execute=True), LogContext(user=editor) as log_context:
        log(group, "wagtail.create")

    [sent_line] = sent_audit_lines()
    assert sent_line["log_model"] == "ModelLogEntry"
    assert sent_line["content_type"] == "auth.group"
    assert sent_line["object_id"] == str(group.pk)
    assert sent_line["label"] == "Audit reviewers"
    assert sent_line["user_id"] == editor.pk
    assert sent_line["uuid"] == str(log_context.uuid)


def test_system_action_is_sent_without_a_user(page, sent_audit_lines, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=True):
        log(page, "wagtail.publish")

    [sent_line] = sent_audit_lines()
    assert sent_line["user_id"] is None


def test_saving_an_existing_log_entry_sends_nothing(editor, page, sent_audit_lines, django_capture_on_commit_callbacks):
    log_entry = log(page, "wagtail.edit", user=editor)

    with django_capture_on_commit_callbacks(execute=True):
        log_entry.save()

    assert sent_audit_lines() == []


def test_log_entry_rolled_back_with_its_action_sends_nothing(editor, page, sent_audit_lines, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=True), pytest.raises(AbandonedAction):
        with transaction.atomic():
            log(page, "wagtail.edit", user=editor)
            raise AbandonedAction

    assert sent_audit_lines() == []


def test_entry_about_a_user_identifies_them_by_id_only(editor, sent_audit_lines, django_capture_on_commit_callbacks):
    edited_user = WagtailUserFactory(username="edited@example.com", email="edited@example.com")

    with django_capture_on_commit_callbacks(execute=True):
        log(edited_user, "wagtail.edit", user=editor)

    [sent_line] = sent_audit_lines()
    assert sent_line["content_type"] == "auth.user"
    assert sent_line["object_id"] == str(edited_user.pk)
    assert sent_line["user_id"] == editor.pk
    assert sent_line["label"] is None
    assert "@example.com" not in json.dumps(sent_line)


@freeze_time("2026-10-01 12:00:00")
def test_deleting_a_user_sends_their_email_and_who_deleted_them(editor, sent_audit_lines, django_capture_on_commit_callbacks):
    departing_user = WagtailUserFactory(username="departing@example.com", email="departing@example.com")
    departing_user_id = departing_user.pk

    with django_capture_on_commit_callbacks(execute=True), LogContext(user=editor):
        departing_user.delete()

    assert sent_audit_lines() == [
        {
            "event": "wagtail.audit.user_deleted",
            "tenant": "bedrock",
            "environment": settings.AUDIT_LOG_ENVIRONMENT,
            "timestamp": "2026-10-01T12:00:00+00:00",
            "user_id": departing_user_id,
            "user_email": "departing@example.com",
            "deleted_by_user_id": editor.pk,
        }
    ]


def test_deleting_a_user_outside_the_admin_sends_no_deleting_user(sent_audit_lines, django_capture_on_commit_callbacks):
    departing_user = WagtailUserFactory(username="departing@example.com", email="departing@example.com")

    with django_capture_on_commit_callbacks(execute=True):
        departing_user.delete()

    [sent_line] = sent_audit_lines()
    assert sent_line["deleted_by_user_id"] is None


def test_audit_lines_stay_out_of_the_application_log():
    root_collecting_handler = BufferingHandler(capacity=10)
    logging.getLogger().addHandler(root_collecting_handler)
    try:
        logging.getLogger("audit.wagtail").info('{"event": "wagtail.audit"}')
    finally:
        logging.getLogger().removeHandler(root_collecting_handler)

    assert root_collecting_handler.buffer == []


def test_audit_lines_are_written_as_bare_json():
    [audit_handler_name] = settings.LOGGING["loggers"]["audit.wagtail"]["handlers"]
    formatter_name = settings.LOGGING["handlers"][audit_handler_name]["formatter"]
    audit_formatter = logging.Formatter(settings.LOGGING["formatters"][formatter_name]["format"])

    formatted_line = audit_formatter.format(logging.makeLogRecord({"msg": '{"event": "wagtail.audit"}'}))

    assert formatted_line == '{"event": "wagtail.audit"}'


@pytest.mark.parametrize(
    "app_name, expected_environment",
    [
        ("bedrock-prod", "prod"),
        ("bedrock-cms-stage", "stage"),
        ("bedrock-cms-dev", "dev"),
        ("bedrock-test", "test"),
        ("bedrock", "local"),
        ("www-demo3", "local"),
        ("another-service-prod", "local"),
        ("bedrock-prod-cms", "local"),
        ("bedrock-cms", "local"),
    ],
)
def test_get_deployment_environment(app_name, expected_environment):
    assert get_deployment_environment(app_name) == expected_environment


def test_get_cms_environment_matches_audit_log_environment(settings):
    settings.APP_NAME = "bedrock-cms-stage"
    assert get_cms_environment() == get_deployment_environment(settings.APP_NAME) == "stage"


@pytest.fixture
def entries_logged_out_of_order(editor, page):
    """Log a page entry and a group entry with timestamps that interleave against creation order."""
    group = Group.objects.create(name="Audit reviewers")
    # Creating the page logged its own wagtail.create entry; clear it so only the entries below exist
    PageLogEntry.objects.all().delete()
    return [
        log(page, "wagtail.edit", user=editor, timestamp=datetime(2026, 3, 1, tzinfo=UTC)),
        log(group, "wagtail.create", user=editor, timestamp=datetime(2026, 1, 1, tzinfo=UTC)),
        log(page, "wagtail.publish", user=editor, timestamp=datetime(2026, 2, 1, tzinfo=UTC)),
    ]


def test_backfill_sends_every_existing_entry_oldest_first(entries_logged_out_of_order, sent_audit_lines):
    command_output = StringIO()

    call_command("backfill_audit_log", stdout=command_output)

    assert [(line["log_model"], line["action"]) for line in sent_audit_lines()] == [
        ("ModelLogEntry", "wagtail.create"),
        ("PageLogEntry", "wagtail.publish"),
        ("PageLogEntry", "wagtail.edit"),
    ]
    assert command_output.getvalue() == "Sent 3 audit log entries\n"


def test_backfill_since_skips_older_entries(entries_logged_out_of_order, sent_audit_lines):
    call_command("backfill_audit_log", "--since", "2026-02-01", stdout=StringIO())

    assert [line["action"] for line in sent_audit_lines()] == ["wagtail.publish", "wagtail.edit"]


def test_backfill_dry_run_prints_lines_instead_of_sending_them(entries_logged_out_of_order, sent_audit_lines):
    command_output = StringIO()

    call_command("backfill_audit_log", "--dry-run", stdout=command_output)

    *printed_lines, summary = command_output.getvalue().splitlines()
    assert [json.loads(line)["log_entry_id"] for line in printed_lines] == [
        entries_logged_out_of_order[1].pk,
        entries_logged_out_of_order[2].pk,
        entries_logged_out_of_order[0].pk,
    ]
    assert summary == "Would have sent 3 audit log entries"
    assert sent_audit_lines() == []
