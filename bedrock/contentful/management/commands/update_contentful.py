# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from hashlib import sha256
from typing import Dict, List, Tuple, Union

from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import RequestFactory
from django.utils.timezone import now as tz_now

import boto3
from sentry_sdk import capture_exception
from sentry_sdk.api import capture_message

from bedrock.contentful.api import ContentfulPage
from bedrock.contentful.constants import (
    ACTION_ARCHIVE,
    ACTION_AUTO_SAVE,
    ACTION_DELETE,
    ACTION_PUBLISH,
    ACTION_SAVE,
    ACTION_UNARCHIVE,
    ACTION_UNPUBLISH,
    COMPOSE_MAIN_PAGE_TYPE,
    MAX_MESSAGES_PER_QUEUE_POLL,
)
from bedrock.contentful.models import ContentfulEntry
from bedrock.utils.management.decorators import alert_sentry_on_exception


def data_hash(data: Dict) -> str:
    str_data = json.dumps(data, sort_keys=True)
    return sha256(str_data.encode("utf8")).hexdigest()


@alert_sentry_on_exception
class Command(BaseCommand):
    rf = RequestFactory()

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            dest="quiet",
            default=False,
            help="If no error occurs, swallow all output.",
        ),
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            dest="force",
            default=False,
            help="Load the data even if nothing new from Contentful.",
        ),

    def log(self, msg) -> None:
        if not self.quiet:
            print(msg)

    def handle(self, *args, **options):
        self.quiet = options["quiet"]
        self.force = options["force"]
        if settings.CONTENTFUL_SPACE_ID and settings.CONTENTFUL_SPACE_KEY:
            if self.force:
                self.log("Running forced update from Contentful data")
            else:
                self.log("Checking for updated Contentful data")

            update_ran, added_count, updated_count, deleted_count, errors_count = self.refresh()

            if update_ran:
                self.log(f"Done. Added: {added_count}. Updated: {updated_count}. Deleted: {deleted_count}. Errors: {errors_count}")
            else:
                self.log(f"Nothing to pull from Contentful")
        else:
            # This will always get shown, even if --quiet is passed
            print("Contentful credentials not configured")

    def refresh(self) -> Tuple[bool, int, int, int, int]:
        update_ran = False

        added_count = -1
        updated_count = -1
        deleted_count = -1
        errors_count = -1

        poll_contentful = self.force or self._queue_has_viable_messages()

        if poll_contentful:
            added_count, updated_count, deleted_count, errors_count = self._refresh_from_contentful()
            update_ran = True

        return update_ran, added_count, updated_count, deleted_count, errors_count

    def _get_message_action(self, msg: str) -> Union[str, None]:
        # Format for these messages is:
        # ContentManagement.Entry.publish,<currently_irrelevant_string>,<currently_irrelevant_string>
        try:
            label, _, _ = msg.split(",")
            _, _, action = label.split(".")
            return action
        except (AttributeError, ValueError) as e:
            self.log(f"Problem getting message action from {msg}: {e}")
            capture_exception(e)
            return None

    def _purge_queue(self, queue) -> None:
        """Remove all entries in the queue, without inspecting them

        Split out for clarity - there are a few caveats about queue purging from
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.purge_queue

        > The message deletion process takes up to 60 seconds.
        > We recommend waiting for 60 seconds regardless of your queue's size.

        This is fine, as we run this every 5 mins.

        > Messages sent to the queue before you call PurgeQueue might be received
        > but are deleted within the next minute.

        This is _probably_ fine - if a "publish" message arrives 'late' and is deleted
        rather than acted on, that's fine, because we only purge after a "go" action,
        so we'll already be updating from Contentful.

        > Messages sent to the queue after you call PurgeQueue might be deleted
        > while the queue is being purged.

        This one is a bit riskier, so we should keep an eye on real-world behaviour.
        It might be useful to do a forced rebuild a couple of times a day, to be safe.
        """
        self.log("Purging the rest of the queue")
        queue.purge()

    def _queue_has_viable_messages(self) -> bool:
        """
        When pages/entries change, Contentful uses a webhook to push a
        message into a queue. Here, we get all enqueued messages and if ANY ONE
        of them has an action of a 'go' type, we count that as enough and
        we re-sync all of our Contentful content.

        If we get a 'go' signal, we explicitly drain the queue rather than waste
        network I/O on pointless checking. If we don't get a 'go' signal at all,
        we still effectively have purged the queue, just iteratively.

        What action types count as a 'go' signal?

        * auto_save -> YES if using preview mode (ie on Dev/Stage)
        * create -> NO, NEVER - not on Prod, Stage or Dev
        * publish -> YES
        * save -> YES if using preview mode
        * unarchive -> YES
        * archive -> YES (and we'll remove the page from bedrock's DB as well)
        * unpublish  -> YES (as above)
        * delete -> YES (as above)
        """

        poll_queue = True
        may_purge_queue = False
        viable_message_found = False

        GO_ACTIONS = {
            ACTION_ARCHIVE,
            ACTION_PUBLISH,
            ACTION_UNARCHIVE,
            ACTION_UNPUBLISH,
            ACTION_DELETE,
        }
        EXTRA_PREVIEW_API_GO_ACTIONS = {
            # Sites that are using the preview API key (Dev and Stage) act upon
            # two more state changes
            ACTION_AUTO_SAVE,
            ACTION_SAVE,
        }

        if settings.APP_NAME in [
            # See settings.base.get_app_name()
            "bedrock",  # Default, returned for local dev
            "bedrock-dev",
            "bedrock-stage",
        ]:
            GO_ACTIONS = GO_ACTIONS.union(EXTRA_PREVIEW_API_GO_ACTIONS)

        if not settings.CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID:
            self.log(
                "AWS SQS Credentials not configured for Contentful webhook",
            )
            # We don't want things to block/fail if we don't have SQS config.
            # Instead, in this situation, it's better to just assume we got
            # a 'go' signal and poll Contentful anyway.
            return True

        sqs = boto3.resource(
            "sqs",
            region_name=settings.CONTENTFUL_NOTIFICATION_QUEUE_REGION,
            aws_access_key_id=settings.CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID,
            aws_secret_access_key=settings.CONTENTFUL_NOTIFICATION_QUEUE_SECRET_ACCESS_KEY,
        )
        queue = sqs.Queue(settings.CONTENTFUL_NOTIFICATION_QUEUE_URL)

        while poll_queue:
            msg_batch = queue.receive_messages(
                WaitTimeSeconds=settings.CONTENTFUL_NOTIFICATION_QUEUE_WAIT_TIME,
                MaxNumberOfMessages=MAX_MESSAGES_PER_QUEUE_POLL,
            )

            if len(msg_batch) == 0:
                self.log("No messages in the queue")
                break

            for sqs_msg in msg_batch:
                msg_body = sqs_msg.body
                action = self._get_message_action(msg_body)
                if action in GO_ACTIONS:
                    # we've found a viable one, so that's great. Drain down the queue and move on
                    viable_message_found = True
                    self.log(f"Got a viable message: {msg_body}")
                    may_purge_queue = True
                    poll_queue = False  # no need to get more messages
                    break
                else:
                    # Explicitly delete the message and move on to the next one.
                    # Note that we don't purge the entire queue even if all of the
                    # current messages are inviable, because we don't want the risk
                    # of a viable message being lost during the purge process.
                    sqs_msg.delete()
                    continue

        if not viable_message_found:
            self.log(f"No viable message found in queue")

        if may_purge_queue:
            self._purge_queue(queue)

        return viable_message_found

    def _detect_and_delete_absent_entries(self, contentful_ids_synced: List[int]) -> int:
        _entries_to_delete = ContentfulEntry.objects.exclude(contentful_id__in=contentful_ids_synced)
        _num_entries_to_delete = _entries_to_delete.count()

        res = _entries_to_delete.delete()
        self.log(f"Deleted by _detect_and_delete_absent_entries: {res}")

        # if things aren't right, we don't want to block the rest of the sync
        if res[0] != _num_entries_to_delete:
            capture_message(
                message="Deleted more objects than expected based on these ids slated for deletion. Check the Contentful sync!",
                level="warning",
            )
        return res[1]["contentful.ContentfulEntry"]

    def _refresh_from_contentful(self) -> Tuple[int, int, int]:
        self.log("Pulling from Contentful")
        updated_count = 0
        added_count = 0
        deleted_count = 0
        error_count = 0
        content_to_sync = []

        # TODO: Change to syncing only `page` content types when we're in an all-Compose setup
        for ctype in settings.CONTENTFUL_CONTENT_TYPES:
            for entry in ContentfulPage.client.entries(
                {
                    "content_type": ctype,
                    "include": 0,
                }
            ).items:
                content_to_sync.append((ctype, entry.sys["id"]))

        for ctype, page_id in content_to_sync:
            request = self.rf.get("/")
            request.locale = "en-US"
            try:
                page = ContentfulPage(request, page_id)
                page_data = page.get_content()
            except Exception as ex:
                # problem with the page, load other pages
                self.log(f"Problem with {ctype}:{page_id} -> {type(ex)}: {ex}")
                capture_exception(ex)
                error_count += 1
                continue

            # Compose-authored pages have a page_type of `page`
            # but really we want the entity the Compose page references
            if ctype == COMPOSE_MAIN_PAGE_TYPE:
                # TODO: make this standard when we _only_ have Compose pages,
                # because they all have a parent type of COMPOSE_MAIN_PAGE_TYPE
                ctype = page_data["page_type"]

            hash = data_hash(page_data)
            _info = page_data["info"]

            extra_params = dict(
                locale=_info["locale"],
                data_hash=hash,
                data=page_data,
                slug=_info["slug"],
                classification=_info.get("classification", ""),
                tags=_info.get("tags", []),
                category=_info.get("category", ""),
            )

            try:
                obj = ContentfulEntry.objects.get(contentful_id=page_id)
            except ContentfulEntry.DoesNotExist:
                self.log(f"Creating new ContentfulEntry for {ctype}:{page_id}")
                ContentfulEntry.objects.create(
                    contentful_id=page_id,
                    content_type=ctype,
                    **extra_params,
                )
                added_count += 1
            else:
                if self.force or hash != obj.data_hash:
                    self.log(f"Updating existing ContentfulEntry for {ctype}:{page_id}")
                    for key, value in extra_params.items():
                        setattr(obj, key, value)
                    obj.last_modified = tz_now()
                    obj.save()
                    updated_count += 1

        try:
            # Even if we failed to sync certain entities, we should act as if they
            # were synced when we come to look for records to delete. If it was just
            # a temporary glitch that caused the exception we would not want to unncessarily
            # delete a page, even if the failed sync means its content is potentially stale
            _ids_synced = [x[1] for x in content_to_sync]  # (x[0] is ctype, x[1] is the id)
            deleted_count = self._detect_and_delete_absent_entries(_ids_synced)
        except Exception as ex:
            self.log(ex)
            capture_exception(ex)

        return added_count, updated_count, deleted_count, error_count
